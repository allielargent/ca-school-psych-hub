"""Sync every published Zendesk Help Center article into a local knowledge base."""
import argparse
import json
import logging
import os
import re
import shutil
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from markdownify import markdownify as md

BASE_DIR = Path(__file__).resolve().parent
KB_DIR = BASE_DIR / "knowledge_base"
MARKDOWN_DIR = KB_DIR / "markdown"
JSON_DIR = KB_DIR / "json"
ATTACH_DIR = KB_DIR / "attachments"
DELETED_DIR = KB_DIR / "_deleted"
LOG_DIR = KB_DIR / "logs"
STATE_FILE = KB_DIR / ".sync_state.json"
INDEX_MD = BASE_DIR / "INDEX.md"
INDEX_JSON = BASE_DIR / "index.json"

REQUEST_TIMEOUT = 30
MAX_ATTEMPTS = 6


class ZendeskError(Exception):
    pass


def slugify(text, max_len=60):
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:max_len].strip("-") or "untitled"


def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def absolutize_html(html, base_url):
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    for tag, attr in (("a", "href"), ("img", "src")):
        for el in soup.find_all(tag):
            val = el.get(attr)
            if val and val.startswith("/"):
                el[attr] = base_url + val
    return str(soup)


class ZendeskClient:
    def __init__(self, subdomain, email, token, locale):
        self.base = f"https://{subdomain}.zendesk.com"
        self.locale = locale
        self.session = requests.Session()
        self.session.auth = (f"{email}/token", token)
        self._user_cache = {}

    def _request(self, method, url, **kwargs):
        resp = None
        for attempt in range(MAX_ATTEMPTS):
            resp = self.session.request(method, url, timeout=REQUEST_TIMEOUT, **kwargs)
            if resp.status_code == 429:
                time.sleep(int(resp.headers.get("Retry-After", "5")))
                continue
            if resp.status_code >= 500:
                time.sleep(2 ** attempt)
                continue
            return resp
        return resp

    def test_connection(self):
        resp = self._request(
            "GET",
            f"{self.base}/api/v2/help_center/{self.locale}/categories.json",
            params={"per_page": 1},
        )
        if resp is None:
            raise ZendeskError("No response from Zendesk (network error or repeated 5xx).")
        if resp.status_code == 401:
            raise ZendeskError("Authentication failed - check ZENDESK_EMAIL / ZENDESK_API_TOKEN in .env")
        if resp.status_code == 404:
            raise ZendeskError(f"Subdomain or locale not found ({self.base}, locale={self.locale}).")
        resp.raise_for_status()
        return True

    def _paginate(self, url, params, key):
        items = []
        while url:
            resp = self._request("GET", url, params=params)
            resp.raise_for_status()
            data = resp.json()
            items.extend(data[key])
            url = data.get("next_page")
            params = None
        return items

    def get_locales(self):
        resp = self._request("GET", f"{self.base}/api/v2/help_center/locales.json")
        resp.raise_for_status()
        return resp.json().get("locales") or [self.locale]

    def get_brands(self):
        return self._paginate(f"{self.base}/api/v2/brands.json", {"per_page": 100}, "brands")

    def rebase(self, host):
        self.base = f"https://{host}"

    def get_categories(self, locale):
        cats = self._paginate(
            f"{self.base}/api/v2/help_center/{locale}/categories.json",
            {"per_page": 100},
            "categories",
        )
        return {c["id"]: c["name"] for c in cats}

    def get_sections(self, locale):
        secs = self._paginate(
            f"{self.base}/api/v2/help_center/{locale}/sections.json",
            {"per_page": 100},
            "sections",
        )
        return {s["id"]: {"name": s["name"], "category_id": s["category_id"]} for s in secs}

    def iter_articles(self, locale, logger=None):
        url = f"{self.base}/api/v2/help_center/{locale}/articles.json"
        params = {"per_page": 100, "sort_by": "updated_at", "sort_order": "asc"}
        page, seen, total = 0, 0, None
        while url:
            resp = self._request("GET", url, params=params)
            resp.raise_for_status()
            data = resp.json()
            if total is None:
                total = data.get("count")
            page += 1
            batch = data["articles"]
            seen += len(batch)
            if logger:
                logger.info(
                    "%s (%s): page %d fetched (%d articles, %d/%s seen so far)",
                    self.base, locale, page, len(batch), seen, total,
                )
            for article in batch:
                yield article
            next_url = data.get("next_page")
            if next_url == url:
                break  # guard against a pagination cursor that fails to advance
            url = next_url
            params = None

    def get_user_name(self, user_id):
        if user_id is None:
            return "Unknown"
        if user_id in self._user_cache:
            return self._user_cache[user_id]
        resp = self._request("GET", f"{self.base}/api/v2/users/{user_id}.json")
        name = "Unknown"
        if resp is not None and resp.status_code == 200:
            name = resp.json()["user"]["name"]
        self._user_cache[user_id] = name
        return name

    def get_attachments(self, article_id):
        return self._paginate(
            f"{self.base}/api/v2/help_center/articles/{article_id}/attachments.json",
            {"per_page": 100},
            "article_attachments",
        )

    def download_file(self, url, dest_path):
        resp = self._request("GET", url, stream=True)
        resp.raise_for_status()
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dest_path, "wb") as fh:
            for chunk in resp.iter_content(8192):
                fh.write(chunk)


def setup_logger():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_path = LOG_DIR / f"sync_{timestamp}.log"
    logger = logging.getLogger("zendesk_sync")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.addHandler(sh)
    return logger, log_path


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"articles": {}}


def save_state(state):
    write_json(STATE_FILE, state)


def rel(path):
    return path.relative_to(BASE_DIR).as_posix()


def resolve_brand(brands, requested_id, default_subdomain, logger):
    help_center_brands = [b for b in brands if b.get("has_help_center")]
    if requested_id is not None:
        for b in help_center_brands:
            if b["id"] == requested_id:
                return b
        available = ", ".join(f"{b['id']} ({b['name']})" for b in help_center_brands)
        raise ZendeskError(f"No Help-Center-enabled brand with id={requested_id}. Available brands: {available}")

    for b in help_center_brands:
        if b.get("subdomain") == default_subdomain:
            logger.info("No --brand-id given; defaulting to the brand matching ZENDESK_SUBDOMAIN.")
            return b

    if help_center_brands:
        logger.warning(
            "No --brand-id given and no brand matches ZENDESK_SUBDOMAIN; defaulting to the first "
            "Help-Center-enabled brand found."
        )
        return help_center_brands[0]

    raise ZendeskError("No Help-Center-enabled brand found on this account.")


def process_article(client, article, categories, sections, logger, brand, locale, multi_locale):
    article_id = article["id"]
    section = sections.get(article.get("section_id"))
    category_id = section["category_id"] if section else None
    category_name = categories.get(category_id, "Uncategorized")
    section_name = section["name"] if section else "Uncategorized"
    brand_slug = slugify(brand["name"])
    cat_slug = slugify(category_name)
    sec_slug = slugify(section_name)
    title = article.get("title") or f"untitled-{article_id}"
    slug = slugify(title)
    author_name = client.get_user_name(article.get("author_id"))
    labels = article.get("label_names") or []

    body_html = absolutize_html(article.get("body"), client.base)
    body_markdown = md(body_html, heading_style="ATX") if body_html else ""

    parts = (brand_slug, cat_slug, sec_slug, locale) if multi_locale else (brand_slug, cat_slug, sec_slug)
    markdown_path = MARKDOWN_DIR.joinpath(*parts) / f"{article_id}-{slug}.md"
    json_path = JSON_DIR.joinpath(*parts) / f"{article_id}.json"
    attachment_dir = ATTACH_DIR.joinpath(*parts) / str(article_id)

    frontmatter = "\n".join(
        [
            "---",
            f"id: {article_id}",
            f"brand: {json.dumps(brand['name'])}",
            f"brand_id: {brand['id']}",
            f"locale: {json.dumps(locale)}",
            f"title: {json.dumps(title)}",
            f"category: {json.dumps(category_name)}",
            f"section: {json.dumps(section_name)}",
            f"labels: {json.dumps(labels)}",
            f"author: {json.dumps(author_name)}",
            f"created_at: {json.dumps(article.get('created_at'))}",
            f"updated_at: {json.dumps(article.get('updated_at'))}",
            f"url: {json.dumps(article.get('html_url'))}",
            "---",
            "",
        ]
    )
    write_text(markdown_path, frontmatter + f"# {title}\n\n" + body_markdown + "\n")
    write_json(json_path, article)

    attachment_count = 0
    for att in client.get_attachments(article_id):
        dest = attachment_dir / att["file_name"]
        try:
            client.download_file(att["content_url"], dest)
            attachment_count += 1
        except Exception as exc:  # noqa: BLE001 - per-attachment isolation
            logger.error("Attachment download failed (article %s, file %s): %s", article_id, att.get("file_name"), exc)

    return {
        "id": article_id,
        "brand": brand["name"],
        "brand_id": brand["id"],
        "locale": locale,
        "title": title,
        "category": category_name,
        "section": section_name,
        "labels": labels,
        "author": author_name,
        "created_at": article.get("created_at"),
        "updated_at": article.get("updated_at"),
        "url": article.get("html_url"),
        "markdown_path": rel(markdown_path),
        "json_path": rel(json_path),
        "attachment_dir": rel(attachment_dir) if attachment_count else None,
        "attachment_count": attachment_count,
    }, attachment_count


def move_deleted(entry):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for key in ("markdown_path", "json_path"):
        src = BASE_DIR / entry[key]
        if src.exists():
            dest = DELETED_DIR / timestamp / entry[key]
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dest))
    if entry.get("attachment_dir"):
        src_dir = BASE_DIR / entry["attachment_dir"]
        if src_dir.exists():
            dest_dir = DELETED_DIR / timestamp / entry["attachment_dir"]
            dest_dir.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src_dir), str(dest_dir))


def build_index(state):
    articles = sorted(
        state["articles"].values(),
        key=lambda a: (a.get("brand", ""), a["category"], a["section"], a["title"]),
    )
    write_json(INDEX_JSON, articles)

    show_locale = len({a.get("locale", "en-us") for a in articles}) > 1

    lines = ["# Help Center Knowledge Base Index", ""]
    lines.append(f"_Last updated: {datetime.now(timezone.utc).isoformat()}_")
    lines.append(f"_Total articles: {len(articles)}_\n")
    current_brand, current_cat, current_sec = None, None, None
    for a in articles:
        brand = a.get("brand", "Unknown brand")
        if brand != current_brand:
            current_brand = brand
            current_cat, current_sec = None, None
            lines.append(f"# {current_brand}")
        if a["category"] != current_cat:
            current_cat = a["category"]
            current_sec = None
            lines.append(f"## {current_cat}")
        if a["section"] != current_sec:
            current_sec = a["section"]
            lines.append(f"### {current_sec}")
        labels = f" ({', '.join(a['labels'])})" if a["labels"] else ""
        locale_tag = f" [{a.get('locale', 'en-us')}]" if show_locale else ""
        lines.append(
            f"- [{a['title']}]({a['markdown_path']}){locale_tag} — updated {a['updated_at']}, by {a['author']}{labels} "
            f"[source]({a['url']})"
        )
    write_text(INDEX_MD, "\n".join(lines) + "\n")


def verify_sync(client, state, logger, brand):
    """Read-only check: compares Zendesk's current published articles for this brand against
    what's recorded in state and actually present on disk. Downloads nothing, writes nothing."""
    logger.info(
        "Verifying brand '%s' (id=%s) via host %s", brand["name"], brand["id"], client.base,
    )
    brand_slug = slugify(brand["name"])
    brand_prefix = f"{brand_slug}:"

    locales = client.get_locales()
    multi_locale = len(locales) > 1

    published = {}  # key -> article
    total_returned, drafts_skipped = 0, 0
    for locale in locales:
        for article in client.iter_articles(locale, logger=logger):
            total_returned += 1
            if article.get("draft"):
                drafts_skipped += 1
                continue
            key = f"{brand_slug}:{locale}:{article['id']}" if multi_locale else f"{brand_slug}:{article['id']}"
            published[key] = article

    brand_state_keys = {k for k in state["articles"] if k.startswith(brand_prefix)}

    missing = []
    stale_content = []
    for key, article in published.items():
        entry = state["articles"].get(key)
        if entry is None:
            missing.append(key)
            continue
        if not (BASE_DIR / entry["markdown_path"]).exists() or not (BASE_DIR / entry["json_path"]).exists():
            missing.append(key)
        elif entry.get("updated_at") != article.get("updated_at"):
            stale_content.append(key)

    orphaned_local = sorted(brand_state_keys - set(published))

    logger.info("----- VERIFY SUMMARY -----")
    logger.info("brand: %s", brand["name"])
    logger.info("host: %s", client.base)
    logger.info("total_articles_returned_by_zendesk: %d", total_returned)
    logger.info("published_articles: %d", len(published))
    logger.info("drafts_skipped: %d", drafts_skipped)
    logger.info("present_and_current: %d", len(published) - len(missing) - len(stale_content))
    logger.info("missing_locally: %d", len(missing))
    logger.info("stale_locally (needs re-sync): %d", len(stale_content))
    logger.info("orphaned_locally (no longer published remotely): %d", len(orphaned_local))

    ok = not missing and not stale_content
    if missing:
        logger.warning("Missing article keys: %s", missing)
    if stale_content:
        logger.warning("Out-of-date article keys (updated_at changed remotely): %s", stale_content)
    if orphaned_local:
        logger.info(
            "Orphaned local keys (run a normal sync to archive these to _deleted): %s", orphaned_local,
        )
    if ok:
        logger.info("VERIFY PASSED - all %d published articles are present and up to date on disk.", len(published))
    else:
        logger.warning("VERIFY FAILED - run `python sync_help_center.py --brand-id %s` to fix.", brand["id"])

    return ok


def run_sync(client, state, logger, force_full, brand):
    logger.info(
        "Syncing brand '%s' (id=%s) via host %s", brand["name"], brand["id"], client.base,
    )

    locales = client.get_locales()
    multi_locale = len(locales) > 1
    logger.info("Discovered locale(s) on this brand's Help Center: %s", locales)

    logger.info(
        "Note: Zendesk Help Center articles have only draft/published states (no separate "
        "'archived' state) - 'archived_or_deleted_skipped' below counts articles removed or "
        "unpublished (within this brand) since the last sync."
    )

    categories_by_locale = {}
    sections_by_locale = {}
    current = {}  # key -> {"article": ..., "locale": ...}
    total_returned = 0
    drafts_skipped = 0
    brand_slug = slugify(brand["name"])

    for locale in locales:
        categories_by_locale[locale] = client.get_categories(locale)
        sections_by_locale[locale] = client.get_sections(locale)

        for article in client.iter_articles(locale, logger=logger):
            aid = article["id"]
            total_returned += 1
            if article.get("draft"):
                drafts_skipped += 1
                continue
            key = f"{brand_slug}:{locale}:{aid}" if multi_locale else f"{brand_slug}:{aid}"
            current[key] = {"article": article, "locale": locale}

    published_count = len(current)

    new_ids, updated_ids, unchanged_ids = [], [], []
    for key, entry in current.items():
        old = None if force_full else state["articles"].get(key)
        if old is None:
            new_ids.append(key)
        elif old.get("updated_at") != entry["article"].get("updated_at"):
            updated_ids.append(key)
        else:
            unchanged_ids.append(key)

    # Only articles previously synced under this same brand can count as deleted this run -
    # other brands' entries in shared state must be left untouched.
    brand_prefix = f"{brand_slug}:"
    deleted_ids = [
        key for key in state["articles"]
        if key.startswith(brand_prefix) and key not in current
    ]

    errors = []
    attachments_downloaded = 0
    for key in new_ids + updated_ids:
        entry = current[key]
        locale = entry["locale"]
        try:
            metadata, count = process_article(
                client, entry["article"], categories_by_locale[locale], sections_by_locale[locale],
                logger, brand, locale, multi_locale,
            )
            state["articles"][key] = metadata
            attachments_downloaded += count
            logger.info("Synced article %s [%s]: %s", entry["article"]["id"], locale, metadata["title"])
        except Exception as exc:  # noqa: BLE001 - keep syncing remaining articles
            logger.error("Failed to sync article %s [%s]: %s", entry["article"]["id"], locale, exc)
            errors.append(f"article {key}: {exc}")

    for key in deleted_ids:
        try:
            move_deleted(state["articles"][key])
            logger.info("Archived deleted article %s", key)
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to archive deleted article %s: %s", key, exc)
            errors.append(f"deleted article {key}: {exc}")
        finally:
            del state["articles"][key]

    state["last_sync"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    build_index(state)

    written_to_disk = len(new_ids) + len(updated_ids)
    missing = [
        key for key in current
        if key not in state["articles"]
        or not (BASE_DIR / state["articles"][key]["markdown_path"]).exists()
        or not (BASE_DIR / state["articles"][key]["json_path"]).exists()
    ]
    if missing:
        errors.append(f"validation: {len(missing)} published article(s) missing local files: {missing}")

    summary = {
        "run_at": state["last_sync"],
        "brand": brand["name"],
        "brand_id": brand["id"],
        "host": client.base,
        "locales": locales,
        "total_articles_returned_by_zendesk": total_returned,
        "published_articles": published_count,
        "drafts_skipped": drafts_skipped,
        "archived_or_deleted_skipped": len(deleted_ids),
        "new_articles": len(new_ids),
        "updated_articles": len(updated_ids),
        "unchanged_articles": len(unchanged_ids),
        "written_to_disk": written_to_disk,
        "attachments_downloaded": attachments_downloaded,
        "errors": errors,
        "validated": not missing,
    }
    write_json(LOG_DIR / f"last_sync_summary_{brand_slug}.json", summary)

    logger.info("----- SYNC SUMMARY -----")
    for key, value in summary.items():
        logger.info("%s: %s", key, value)
    if missing:
        logger.warning("Validation FAILED - %d published article(s) not found on disk.", len(missing))
    else:
        logger.info(
            "Validation passed - all %d published articles in brand '%s' (matching Zendesk's own "
            "count) are present on disk.",
            published_count, brand["name"],
        )

    return summary


def main():
    parser = argparse.ArgumentParser(description="Sync Zendesk Help Center articles to a local knowledge base.")
    parser.add_argument(
        "--force-full", "--full", dest="force_full", action="store_true",
        help="Ignore saved state and re-download every article.",
    )
    parser.add_argument("--test-connection", action="store_true", help="Only test the Zendesk connection, then exit.")
    parser.add_argument(
        "--brand-id", type=int, default=None,
        help="Zendesk brand ID to sync. Zendesk routes multi-brand Guide content by hostname, so each "
        "brand has its own independent set of articles. Defaults to ZENDESK_BRAND_ID in .env, or the "
        "brand matching ZENDESK_SUBDOMAIN if that's also unset. Use --list-brands to see options.",
    )
    parser.add_argument(
        "--list-brands", action="store_true",
        help="List every Help-Center-enabled brand on this account (with its article count) and exit.",
    )
    parser.add_argument(
        "--verify", action="store_true",
        help="Read-only check: compare Zendesk's published articles for the selected brand against "
        "what's on disk. Downloads nothing. Exits non-zero if anything is missing or out of date.",
    )
    args = parser.parse_args()

    load_dotenv(BASE_DIR / ".env")
    subdomain = os.environ.get("ZENDESK_SUBDOMAIN")
    email = os.environ.get("ZENDESK_EMAIL")
    token = os.environ.get("ZENDESK_API_TOKEN")
    locale = os.environ.get("ZENDESK_LOCALE", "en-us")

    missing = [n for n, v in [("ZENDESK_SUBDOMAIN", subdomain), ("ZENDESK_EMAIL", email), ("ZENDESK_API_TOKEN", token)] if not v]
    if missing:
        print(f"Missing required .env values: {', '.join(missing)}")
        sys.exit(1)

    for d in (MARKDOWN_DIR, JSON_DIR, ATTACH_DIR, LOG_DIR):
        d.mkdir(parents=True, exist_ok=True)

    logger, log_path = setup_logger()
    client = ZendeskClient(subdomain, email, token, locale)

    try:
        client.test_connection()
        logger.info("Connection to Zendesk succeeded (subdomain=%s, locale=%s).", subdomain, locale)
    except Exception as exc:
        logger.error("Connection test failed: %s", exc)
        sys.exit(1)

    if args.test_connection:
        return

    brands = [b for b in client.get_brands() if b.get("has_help_center")]

    if args.list_brands:
        print("Help-Center-enabled brands on this account:")
        for b in brands:
            host = b.get("host_mapping") or f"{b.get('subdomain')}.zendesk.com"
            probe = ZendeskClient(subdomain, email, token, locale)
            probe.rebase(host)
            resp = probe._request("GET", f"{probe.base}/api/v2/help_center/{locale}/articles.json", params={"per_page": 1})
            total = resp.json().get("count") if resp is not None and resp.status_code == 200 else "?"
            print(f"  id={b['id']:<20} name={b['name']!r:<35} host={host:<30} total_articles={total}")
        return

    requested_brand_id = args.brand_id
    if requested_brand_id is None and os.environ.get("ZENDESK_BRAND_ID"):
        requested_brand_id = int(os.environ["ZENDESK_BRAND_ID"])

    brand = resolve_brand(brands, requested_brand_id, subdomain, logger)
    host = brand.get("host_mapping") or f"{brand.get('subdomain')}.zendesk.com"
    client.rebase(host)

    if args.verify:
        state = load_state()
        ok = verify_sync(client, state, logger, brand=brand)
        print(f"\nLog file: {log_path}")
        sys.exit(0 if ok else 1)

    state = {"articles": {}} if args.force_full else load_state()
    run_sync(client, state, logger, force_full=args.force_full, brand=brand)
    print(f"\nLog file: {log_path}")
    print(f"Index: {INDEX_MD}")


if __name__ == "__main__":
    main()
