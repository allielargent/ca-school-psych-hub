# Changelog

All notable changes to the California School Psychologist Hub (`CA_School_Psychologist_Hub_v3.html`) are recorded here in chronological order (newest first).

This file is the authoritative external record. The Hub's own **Version History** tab displays the same entries for in-app reference — keep both in sync when making changes.

Version metadata (Hub Version, Last Updated, Help Center Sync Date, synced article count, source brands, build date) is also embedded in the Hub itself as the `HUB_VERSION` object and shown in the page footer.

---

## v4.6 — 2026-07-07 — Homepage dashboard is now generated from live project data, not hand-typed

**New tool:** `build_dashboard.js` (project root) regenerates the entire homepage dashboard — Recently Updated, New Parallel Resources, California Updates, Recently Added Quick References, and the summary counts — from real project data. No homepage card should need hand-editing again.

**Added**
- Recently Updated pulls the most recent non-"note" entries straight from this Version History (`CHANGELOG`), auto-linking any mentioned Knowledge tab (e.g. Process & Compliance, State Resources) using the Hub's own live section names — never a guessed link target.
- New Parallel Resources and California Updates pull from synced Help Center metadata (`index.json`), restricted to articles the Hub already cites somewhere in its own content — relevance is reused from a prior human judgment call, never guessed fresh. California Updates further filters to California-titled articles; everything else goes to New Parallel Resources.
- Recently Added Quick References ranks guides by the real, synced last-updated date of whichever Help Center article each guide's body actually cites. Guides that don't cite a Help Center article simply don't appear in this feed, rather than being assigned a fabricated "date added."
- All 6 summary counts (Knowledge areas, Quick references, Checklists, Workflows, Answered FAQs, Toolbox tools) and the hero paragraph's numbers are computed directly from the live `KB`/`QREFS`/`CHECKLISTS`/`WORKFLOWS`/`FAQS`/`TOOLS_META` arrays.
- A small "Dashboard data last refreshed" date now appears in the hero, stamped automatically every time `build_dashboard.js` runs (`HUB_VERSION.dashboardRefreshedAt`), linking to Version History.

**Changed**
- The dashboard render code now omits any homepage card with zero reliable items instead of showing an empty box. Verified by running the build with `index.json` temporarily removed, which correctly dropped to 2 cards (Recently Updated + Start a Learning Path) with no layout breakage.

**Refresh workflow (replaces all manual homepage editing)**
1. `python sync_help_center.py` — refresh `index.json`
2. Edit `QREFS` / `CHECKLISTS` / `WORKFLOWS` / `FAQS` / `KB` / `TOOLS_META` / `DOWNLOADS` / `CHANGELOG` in the Hub as needed (ordinary content work, unrelated to this tool)
3. `node build_dashboard.js` — the only new step; recomputes and re-embeds the dashboard
4. Open/reload the Hub

**How it works:** the script locates each `const NAME = <literal>` in the Hub's own script with a bracket/string-aware scanner, evaluates the literal with Node's own JS engine (safe only because the Hub file is this project's own trusted source), cross-references citations against `index.json`, and splices the recomputed `DASHBOARD` and `HUB_VERSION` literals back into the file using plain string slicing — never `String.replace()` with generated text, which corrupted a previous build (see v4.4) when replacement text happened to contain a `$&`-style special pattern.

**Verified**
- Build script tested against the full data set (4/4/3/4 items across the four feed cards) and against a deliberately missing `index.json` (correctly dropped to 0 items for the two Help-Center-dependent cards and the quick-reference feed; confirmed those cards were visually absent from the rendered page, not just uncounted).
- Full interactive Hub regression suite re-run afterward with zero console errors and no regressions.

---

## v4.5 — 2026-07-07 — SEIS resources resolved from the official California Linktree; State Systems section added

**Source:** the official California special-education Linktree, located as the user's own downloaded file (`California SLP Linktree.pdf`, plus a second independent export of the same page for cross-checking — both agreed). Every URL taken from it was confirmed live (HTTP 200) before being added to the Hub.

**Added**
- Replaced all 3 remaining SEIS video placeholders in Process & Compliance with the official videos: "How to Affirm an IEP," "Case Management in SEIS," and "Exit a Student from SEIS Caseload" (YouTube), plus the official SEIS Service Tracker User Guide PDF.
- New "California Systems" group in Process & Compliance: State SELPA Forms Manual (flippable, w/ videos, and PDF), State SELPA Supplemental Forms Manual (PDF), CA SELPA Administration, CALPADS (state SPED data reporting), and CDE Special Education — reusing the Hub's existing CDE Special Education URL rather than introducing a third variant of the same resource.
- New "SEIS & SELPA Systems" section in State Resources (SEIS portal, CA SELPA Administration, CALPADS reporting) — this was a genuine gap; State Resources previously had no dedicated SEIS/SELPA entries despite SEIS being referenced throughout the Hub. Uses the identical URLs as the Process & Compliance entries.

**Changed**
- Renamed the Process & Compliance "SEIS" group to "SEIS Quick Start." Kept the existing "Psych-specific SEIS quick steps" caveat item so the section reads as school-psychologist workflow guidance, not a raw resource dump. Deliberately excluded the source Linktree's speech-language-pathology-specific material (CA SLP Considerations, SLPA Supervision, Transition Services videos) — none of it was imported.

**Decision notes**
- "Test technical manuals library" (Assessment & Eligibility → Report writing) remains a "Coming soon" placeholder — it isn't SEIS-related and the source Linktree has no corresponding resource. This is the only placeholder left in the file.
- "CA Eligibility Categories" (a cahelp.org link in the source Linktree) was considered and not added — the Hub's own Eligibility Categories Guide (5 CCR §3030-based) already covers this more thoroughly than an external link would.

**Verified**
- Zero `url:"#"` links anywhere in the file; exactly one "Coming soon" tag remains (the item above).
- All new links render as real anchors with the correct href in both Process & Compliance and State Resources — checked programmatically, not just by reading the source.
- Search correctly indexes the new content ("affirm an iep," "selpa forms manual," "calpads" all return results).
- Full interactive Hub regression suite (FAQ / Checklist / Quick Reference / Print / Search / Fillable PDFs) re-run with zero console errors and no regressions.

---

## v4.4 — 2026-07-07 — All 10 Downloads are now interactive fillable PDFs

**Added**
- Every document in the Downloads section now has a "Download Fillable PDF" button in addition to the existing Print / Save option: CA Timeline Tracking Worksheet, Eligibility Decision Worksheet, FBA Planning Guide, Larry P. Decision Guide, Report Submission Checklist, Initial Evaluation Checklist, Manifestation Determination Checklist, Meeting Preparation Checklist, IEP Meeting Agenda, and Parent Guide.
- PDFs are real fillable AcroForms (native text fields, multiline fields, checkboxes, and dropdowns) built entirely client-side using a vendored copy of pdf-lib (MIT license, ~525KB, embedded inline) — no CDN, no network request, no data ever leaves the provider's computer. Generation works identically online or fully offline.
- Zero embedded PDF JavaScript anywhere — deliberately. No auto-calculated completion percentages, no auto-checking, no viewer-specific tooltips, since that behavior only runs in Adobe Acrobat Reader and would silently do nothing in Chrome PDF Viewer, Edge PDF Viewer, and macOS Preview. Every field type used (text, multiline, checkbox, dropdown) behaves identically across all four.
- A minimal, consistent required-field standard across every form: Student Name, School/District (where applicable), Evaluator/Provider (when appropriate), and one primary case date. Facilitator, interpreter, attendees, notes, recommendations, and district-specific fields stay optional so the forms support different district workflows. The Parent Guide has no required fields at all, per its own explicit spec.
- FBA Planning Guide includes a fillable 6-column ABC data table (Antecedent/Behavior/Consequence/Frequency/Duration/Intensity, 4 rows) and a Hypothesized Function dropdown. Eligibility Decision Worksheet includes a 13-category eligibility dropdown plus 7 structured decision fields. Larry P., Report Submission, Manifestation Determination, and Meeting Preparation reuse their live checklist / most-common-misses / bring-with-you data so the PDF can't drift out of sync with the interactive Hub.

**Fixed (caught during QA, not shipped with the bug)**
- A `String.replace()` special-pattern bug (`$&`) that corrupted the vendored library on first attempt — fixed with safe string slicing instead.
- Two WinAnsi font-encoding errors from using "≤" and "→" characters, which the base PDF fonts can't render — replaced with plain-text equivalents ("30 or fewer days," "->").
- A text-wrapping gap in the reference-callout box that let long lines overflow their border.
- A cursor-tracking bug where standalone (non-grid) text fields didn't advance the page layout position, causing two fields to render on top of each other in the Larry P. and Manifestation Determination documents.

**Decision notes**
- Scope was matched to the Hub's actual 10 Downloads entries. Two documents named in early planning — an "Assessment Planning Worksheet" and a "BIP Planning Worksheet" — have no corresponding entry in the Downloads section and were not created as new documents; related content was folded into the closest existing download instead (e.g., FBA Planning Guide).

**Verified**
- All 10 PDFs generate with zero console/page errors and no `undefined`/`NaN` artifacts.
- Every text field and checkbox round-trips correctly through an independent save/reload cycle (fill → save → reload → confirm value persisted) using pdf-lib's own parser — a different code path than the one that generated the files.
- Visually inspected every document in Chrome's PDF renderer for overlapping or clipped content; spot-checked rendering in Microsoft Edge.
- Full interactive Hub regression suite (FAQ / Checklist / Quick Reference / Print / Search) re-run with zero regressions.
- **Not verified directly:** Adobe Acrobat Reader was not available in this environment to test. The generated files are standard AcroForm PDFs with no proprietary Acrobat-only features — the same compatibility basis the no-JavaScript design relies on — but a direct Acrobat check is recommended before wide release.

---

## v4.3 — 2026-07-07 — Downloads elevated into a cohesive printable clinical toolkit

**Added**
- Every printed download (all 10: CA Timeline, Eligibility Categories, FBA, Larry P., Report Submission Checklist, Initial Evaluation Checklist, Manifestation Determination Checklist, Meeting Preparation Checklist, IEP Meeting Agenda, Parent Guide) now opens with a standardized Quick Facts panel: Best For, Keep Nearby, Time to Review, and Highest Compliance Risk.
- A consistent color-coded callout system across all printed documents: 📌 Key Rule / 📖 Regulation (blue), ⚠ Common Mistake (orange), 🟢 Best Practice (green), 🧠 Clinical Judgment / 📘 Parallel Workflow (purple), plus a dedicated red treatment for Highest Compliance Risk text and high-risk checklist item markers. Practical Tip (💡) uses the Hub's own teal rather than one of the five named risk colors, since a tip isn't a risk category.
- Every download's footer now shows Hub Version, Last Updated, and Source in addition to the print date, replacing the print-date-only footer.
- Checklists (Report Submission, Initial Evaluation, Manifestation Determination, Meeting Preparation): a boxed "Most Common Misses" section, a red-dot high-risk marker on the most compliance-sensitive items only, and a Time to Review estimate computed from item count using the same bucket logic as the interactive Checklists tab.
- IEP Meeting Agenda expanded into a facilitator guide with discussion checkpoints (parent concerns addressed, student strengths discussed first, eligibility explained, recommendations connected to needs, questions answered, PWN discussed).
- Meeting Preparation Checklist: a "Bring With You" section (report, assessment plan, previous IEP, parent concerns, protocols if needed, accommodation summary).
- Parent Guide: a compact "What Happens Next?" flow (Referral → Assessment Plan → Testing → Report → IEP Meeting → Eligibility Decision → Services Begin) and a 4-question family-friendly FAQ (testing vs. qualifying, refusing testing, bringing someone to the meeting, requesting an IEE), grounded in the two-prong test, the consent requirement, and the Hub's existing IEE guide.
- Quick reference downloads (Timeline, Eligibility, FBA, Larry P.) now open with a one-sentence Purpose statement. Eligibility gained a "Most Frequently Confused Categories" box (ED vs. OHI, SLD vs. ID, AUT vs. SLI, OHI vs. SLD); Larry P. gained a "Before Ordering Testing" checklist; FBA and the Manifestation Determination checklist gained compact printable flow diagrams.
- Every download now ends with a "Related Downloads" box (2–3 other toolkit documents).

**Changed**
- Refreshed the Initial Evaluation and Report Submission "Most Common Misses" wording to more specific phrasing (e.g., added "Wrong timeline start date" to Initial Evaluation) and applied the same wording to the interactive Checklists tab so print and in-app copies stay in sync.

**Decision notes**
- Scope was intentionally held to the 10 documents already listed in the Downloads section. The request's example flow diagrams included one for "Assessment Planning," which has no corresponding Downloads entry — it was not added, and no new document was created to host it.
- The request's callout-icon list (6 types) and color list (5 categories) don't map 1:1. Clinical Judgment and Parallel Workflow were both mapped to purple (both are "beyond the black-letter rule" guidance, and purple already meant Clinical Judgment everywhere else in the Hub); Practical Tip was given the Hub's own teal rather than forced into one of the five risk colors.
- No new legal or clinical guidance was introduced. All new content (myths, confused-category notes, decision paths, parent FAQ answers) restates what's already established elsewhere in the Hub, its checklists, or linked Parallel Help Center articles.

**Verified**
- Headless Chrome rendered all 10 downloads with zero console errors and no `undefined`/`NaN` artifacts.
- Quick Facts, Most Common Misses, risk dots, flow diagrams, and Related Downloads sections confirmed present with correct content for every applicable download.
- Print CSS colors confirmed computing correctly under print-media emulation (blue/orange/green/purple/red/teal all resolve as intended).
- Full FAQ/Checklist/Quick-Reference interactive regression suite re-run with no regressions — counts, filters, toggles, progress tracking, and search indexing all unchanged and passing.

---

## v4.2 — 2026-07-07 — Usability polish: FAQ triage signals, checklist risk markers, quick-reference decision support

**Added**
- FAQ Center: an "Escalate to your Clinical Manager if…" callout on 16 higher-risk/judgment-heavy FAQs (ED vs. OHI, SLD method selection, outside diagnosis, low incidence, parent disagreement, due process, district-specific procedures, crisis/self-harm, ERMHS intensity/residential placement, manifestation determination, SEIS/district workflow mismatches); a "Common mistake" note on 6 FAQs; Always/Usually/District-specific confidence badges on 20 FAQs.
- Checklists: a subtle time estimate (~2–4 min, scaled to item count) next to each checklist's category; a "High-risk" marker on the 30 highest compliance-risk items across 7 checklists (Initial Evaluation, Triennial, Assessment Planning, Report Submission, Virtual Testing, Manifestation Determination, Crisis & Safety); a "Most commonly missed" box on 5 major checklists (Initial Evaluation, Assessment Planning, Report Submission, Virtual Testing, Crisis & Safety); section-heading chips at the top of every multi-group checklist that jump to that section.
- Quick References: a "Best for" label on each guide's existing use-case line; a "Common misunderstanding" callout on 6 guides (Larry P., Eligibility, SLD, ERMHS, BIP, Parent Communication); a compact decision-path box on 5 guides (SLD, ERMHS, FBA, Manifestation Determination, Assessment Planning); a source-hierarchy line (CA law → district/SELPA procedure → Parallel SOP → clinical judgment, with the most relevant tier bolded per guide) on all 15 guides.

**Changed**
- FAQ related links refined: the assessment-plan FAQ now also links to the Assessment Planning and Initial Evaluation checklists; the six Parent Communication FAQs now consistently link to both the Parent Communication Guide and Checklist; FAQ links now support external Help Center URLs in addition to in-Hub navigation.

**Fixed**
- Removed a redundant closing banner on the Manifestation Determination guide that repeated the auto-rendered Legal/Judgment banner text almost verbatim; kept only the genuinely new instruction (document the team's reasoning) as a plain callout.
- Fixed 4 guides (ERMHS, Preschool Assessment, Report Writing Checklist, Parent Communication) where the same checklist link appeared twice on one guide — once under "Related checklists" and again as "Next recommended step" — by suppressing the redundant column when the two targets match.
- Lightened the "Back to Quick Reference Library" button (smaller, lower-contrast) so it reads as secondary navigation rather than a primary action.

**Decision notes**
- Full checklist-section collapsibility was considered and intentionally not implemented — it would have required new open/close state management interacting with the existing progress-tracking code, for limited benefit over simple jump-to-section chips. Chips were used instead, per the task's stated fallback.
- No new legal or clinical guidance was introduced. Every escalation condition, common-mistake note, misunderstanding callout, and decision path restates or reorganizes content already present in the Hub's own guides/checklists or in linked Parallel Help Center articles — none of it is a new claim.

**Verified**
- Search index updated so all new escalation/mistake/myth/decision-path/most-missed text is discoverable via search (confirmed directly against the `INDEX` array and via live search queries).
- Headless Chrome: zero console errors; FAQ category filters and open/close toggles work; checklist item-check/progress/reset tracking and print (`printChecklist`) unaffected by the new markup; quick-reference expand/collapse and print (`printQref`) unaffected; zero broken internal (`data-go`) links; zero `href="#"` placeholder links introduced; print media emulation renders without errors.

---

## v4.1 — 2026-07-07 — Pilot-release cleanup: finished the AI Assistants removal, resolved placeholder links

**Fixed**
- Removed leftover AI Assistant references the v4.0 pass missed: the footer sentence ("AI assistants surface approved guidance…"), two SEIS FAQ answers citing a "SEIS Documentation Assistant," and "review assistant" wording in the First Evaluation learning path. Footer now reads "Hub content surfaces approved guidance…"
- Removed AI-related CSS and code that v4.0's changelog claimed to remove but actually left live: the `.t-ai` tag, `.item.ai` icon style, `.fa-links a.ai` style, the `.prompt` quote-mark rule, the `--ai`/`--ai-bg`/`--ai-line` color tokens, and the dead `f.ai` FAQ-link branch in the FAQ renderer (no FAQ entry has used an `.ai` property since v4.0). The still-used `.example-out` callout (Parent Communication Guide example scripts) now borders in `--primary` instead of the retired `--ai` token.
- Removed the Upcoming Compliance Deadlines dashboard card and its backing `DASHBOARD.deadlines` data and `.deadline`/`.dl-days` CSS — these were sample rolling-day placeholders, not real caseload data. Dashboard grid reflows cleanly with 5 cards.

**Changed**
- Resolved the "CA procedural safeguards" dead `url:"#"` link to the real CDE *Notice of Procedural Safeguards* (T21-822). Relabeled the remaining genuine gaps — the test technical manuals library and the three SEIS how-to videos — as "Coming soon" (renamed the `t-tbd` tag from "Link TBD") instead of clickable-looking dead links.
- Sidebar owner card now renders from `HUB_VERSION` (added `owner` and `reviewCycle` fields) instead of hardcoded text, so it can't go stale independently of the version object again. Hub version bumped to v4.1.

**Verified**
- Spot-checked the California Updates dashboard feed against public sources: the CARES universal wellness screener, the AB 748 mental-health poster requirement, and the CASEMIS→CALPADS transition all confirmed real and current. Recently Updated / New Parallel Resources feeds link to real in-hub content and were left unchanged.
- Headless Chrome: zero console errors, all nav items and dashboard cards render, no remaining `url:"#"` links outside the explicitly labeled "Coming soon" items, no misleading AI Assistant references remain anywhere in the file.

---

## v4.0 — 2026-07-06 — Navigation simplification: removed AI Assistants and District Hub

**Removed**
- The entire AI Assistants section: nav item, dashboard count, search indexing, the directory/detail pages, the shared `GUARD` prompt, and every cross-reference from quick references, FAQs, checklists, workflows, and learning paths. These were prompt templates for external AI tools (Claude/Gemini/ChatGPT), not in-hub functionality — see the AI Assistants page framing work in the prior update for context on why that distinction mattered.
- The entire District Hub section: nav item, landing page, `DISTRICT_TEMPLATES` data, its render function, and every cross-reference. It only ever held placeholder `[District A]`/`[District B]` cards; its one real item (the District 101 Help Center link) was already duplicated in Start Here and remains there.
- Orphaned CSS (`.ai-hero`, `.ai-secgrid`, `.ai-box`, `.prompt`, `.codeblock`, `.crumb`) and dead code (the Eligibility tool's assistant fallback link, the related-content "AI assistants" footer column, the unused `t-ai` tag) left behind by the above.

**Added — real Clinical Toolbox tools replacing convertible assistant functionality**
- Timeline Calculator enhanced with the ≤30-days-before-year-end rule (EC §56344(a)).
- Manifestation Determination Helper — two-question guided decision support.
- FBA/BIP Builder — function-matched strategy suggestions from a fixed library, with a printable draft.
- ERMHS Report Builder — structured need/data/impact/service-intensity draft, printable.

**Changed — relocated rather than discarded**
- SEIS steps moved into Process & Compliance as a direct reference item.
- Report Review Assistant's role folded into the existing Report Writing Checklist (FAQ and banner text updated).
- 5 "District Procedures" FAQs and several quick-reference banners rewritten to redirect to District 101 (Pathway) and the District Escalation workflow instead of the removed District Hub. FAQ count unchanged (78).
- Dashboard hero, stats (added Toolbox tools count, corrected Knowledge areas from 7 to the actual 5 tabs), and FAQ Center intro copy updated to reflect the new structure.

**Verified:** headless Chrome — zero console errors, all 200 internal navigation references resolve to real ids, zero references to the removed sections remain anywhere in the file.

---

## v3.6 — 2026-07-06 — Separated AB 1172 from mandated-reporter training

**Changed**
- Start Here now presents California compliance trainings as two clearly labeled, separate sections instead of one flat list: **"California Mandated Reporter & Child Abuse Prevention Training"** (AB 1432, AB 1913, SB 848) and **"California Positive Behavior Training"** (AB 1172). AB 1172 was previously listed directly adjacent to the mandated-reporter article with no distinguishing heading; it is a separate Parallel compliance requirement (PBIS), not part of mandated-reporter training.
- Reworded the First-30-days onboarding checklist item to name the two training categories separately rather than running them into one clause.
- Existing links to both official Help Center articles preserved unchanged.

**Documentation**
- `output/Hub_Conflict_Report.md`: Conflict 2 marked fully **RESOLVED** — both AB 1432/AB 1913/SB 848 (verified as correct, current CA mandated-reporter/child-abuse-prevention trainings) and AB 1172 (verified as a separate, official Parallel Positive Behavior Training requirement) are confirmed. No remaining "needs verification" language for California training requirements.
- `output/Hub_Update_Summary.md`: readiness assessment confirmed as **Ready to Ship**, with no unresolved compliance concerns regarding California training requirements. Two non-blocking, non-compliance items remain tracked (Report Writer terminology question; pre-existing mobile overflow).

**Verified:** full headless-Chrome render with zero console errors; both new section headings confirmed present in rendered output; all existing Help Center links unchanged.

---

## v3.5 — 2026-07-06 — Compliance review: crisis response & AB 1172 resolved

**Fixed**
- Resolved the crisis-response citation ambiguity flagged in v3.3: [Emergency/Crisis Planning](https://providerhelp.parallellearning.com/hc/en-us/articles/21631455156379-Emergency-Crisis-Planning) confirmed as the sole authoritative Parallel SOP for crisis/emergency response. Crisis & Safety Checklist restructured with a new "Before services begin" group (facilitator contact info secured, District 101 reviewed, pre-event communication protocol established) and expanded "Reporting & follow-up" group (post-event follow-up, resources offered as indicated). "In the moment" items reworded to match the article's actual language.
- Self-harm-disclosure FAQ rewritten to name and link Emergency/Crisis Planning explicitly instead of the generic "crisis-response flow" phrase (now removed everywhere in the file).
- Added Emergency/Crisis Planning to the Behavior & Mental Health tab's "Related Parallel Help Center Articles" block.

**Changed**
- Confirmed AB 1172 Positive Behavior Training as a verified official Parallel compliance requirement (certificates valid one calendar year, must remain valid through the end of the school year, Certificate of Completion + payment receipt submitted to support@parallellearning.com). No Hub content change needed — it was already correctly referenced since v3.2.

**Documentation**
- `output/Hub_Conflict_Report.md`: Conflict 3 (crisis response) marked resolved; Conflict 2 (mandated-reporter FAQ) marked partially resolved — AB 1172 confirmed, but the specific AB 1432/AB 1913/SB 848 training details were not independently re-verified this round; Conflict 6 (IDEA/CA terminology) remains open.
- `output/Hub_Update_Summary.md`: readiness assessment raised from **Ready with Minor Risks** to **Ready to Ship**. Two non-blocking items remain tracked: the low-confidence Report Writer eligibility-language terminology question, and a pre-existing (pre-dates this project) mobile-viewport overflow issue in the dashboard hero.

**Verified:** no remaining occurrences of the ambiguous "crisis-response flow" phrase anywhere in the file; full headless-Chrome render with zero console errors after the change.

---

## v3.4 — 2026-07-06 — Version metadata & changelog tracking

**Added**
- `HUB_VERSION` object in the Hub (hub version, last-updated date, Help Center sync date, synced article count, source brands, build date) with an unobtrusive footer display (full detail on hover).
- This `CHANGELOG.md` file, to track all future Hub updates going forward.

---

## v3.3 — 2026-07-06 — Pre-release QA fixes

**Fixed**
- Critical: a JS syntax error introduced in v3.2 (an apostrophe inside a single-quoted string in the mandated-reporter FAQ terminated the string early) broke the entire script — no panel, search, or navigation would have rendered. Converted affected FAQ answers to double-quoted strings.
- Two missing closing `</div>` tags (FBA Guide and Meeting Preparation Guide banners) that left the page's HTML structurally unbalanced.
- A source note that cited one "last updated" date for two Help Center articles with different actual update dates (Report Writing Checklist).
- One stray curly apostrophe normalized to match the file's straight-apostrophe convention.

**Verified**
- Zero broken/stale Help Center links (21 checked against the live Zendesk sync).
- Zero broken internal navigation references (237 `go:` references checked).
- Full render with zero console errors after fixes (headless Chrome).
- Confirmed a mobile-viewport horizontal-overflow issue in the dashboard hero predates this update (present in the original v3 file) — out of scope for this content-focused pass; flagged for the Hub's frontend owner.

**Remaining concerns carried forward** (see `output/Hub_Conflict_Report.md`):
- Crisis & Safety Checklist's "Parallel's crisis-response flow" citation is still unconfirmed (two candidate Help Center articles, neither verified as authoritative).
- Named CA mandated-reporter/positive-behavior training requirements (AB 1432, AB 1913/SB 848, AB 1172) should get Compliance sign-off.
- Possible IDEA vs. CA 5 CCR §3030 terminology mismatch in Report Writer's auto-generated eligibility language — unconfirmed.

---

## v3.2 — 2026-07-06 — Help Center integration audit

**Added**
- "Related Parallel Help Center Articles" blocks to Start Here, Assessment & Eligibility, Behavior & Mental Health, and Process & Compliance, linking to official Parallel Provider Portal SOPs (Report Writer, assessment instrument library, billing/scope, indirect/direct time, archiving, mandated-reporter trainings).
- A new "Help Center" tag (`t-hc`) distinct from the existing "External" tag; relabeled "SOP" to "Parallel SOP" for clarity.
- Source notes to the Timeline Guide, FBA Guide, BIP Guide, Meeting Preparation Guide, and Report Writing Checklist citing specific Help Center articles, explicitly labeled where Hub content and Help Center content answer different questions (e.g., legal deadline vs. Parallel's internal operational pace).
- Updated knowledge sources for 5 AI Assistants (CA School Psych Gem, Eligibility Decision Assistant, Assessment Timeline Assistant, FBA/BIP Assistant, Report Review Assistant).
- A District 101 callout on the District Hub tab clarifying its relationship to the Hub's own district template.

**Changed**
- Resolved the "Parallel report template" TBD link to the real Report Writer: Overview of Templates article.
- Incorporated named CA mandated-reporter (AB 1432, AB 1913/SB 848) and positive-behavior (AB 1172) training requirements into the Start Here onboarding checklist and the mandated-reporter FAQ, replacing generic acknowledgment language.

**Fixed**
- Corrected the Checklists count from 12 to 13 in the dashboard stat and nav badge to match the actual 13 entries in `CHECKLISTS`.

**Reports produced:** `output/Hub_Help_Center_Relevance_Map.md`, `output/Hub_SOP_Gap_Report.md`, `output/Hub_Conflict_Report.md`, `output/Hub_Update_Summary.md`.

**Source data:** Zendesk Help Center sync — Parallel Help Center (25 published articles) + Parallel Provider Portal (490 published articles), synced 2026-07-06.

---

## v3.1 — July 2026 — California Eligibility Decision Support

**Added**
- Rebuilt the Eligibility Worksheet into a category-by-category decision-support tool grounded in 5 CCR §3030(b)(1)–(13), with per-criterion Yes/No/Unsure, notes, explanations, and citations.
- Clinical pearls, common mistakes, and red flags per category, plus context-sensitive guidance and a documentation record.
- Smarter search (abbreviation/synonym expansion — MD, MDR, IEE, SLD, RtI, PSW), contextual prev/next/back navigation, and accessibility improvements.

---

## v2.0 — June 2026 — The clinical knowledge platform

**Added**
- Dashboard with Recently Updated, New Parallel Resources, California Updates, Compliance Deadlines, and New Quick References.
- FAQ Center with 78 answered questions across 12 categories.
- 15 full Quick Reference guides with reading time, difficulty, use case, and related-resources footers.
- 13 interactive checklists with progress tracking and print.
- 11 CSS workflow diagrams.
- Dedicated pages for all 10 AI assistants, including system prompts.
- 5 provider learning paths and a Clinical Toolbox (timeline calculator, eligibility worksheet, assessment planner, agenda generator, observation/interview/documentation templates).
- Download Center with print-styled resources and an expanded District framework (7 templates).

**Changed**
- Rebuilt search to index titles, descriptions, article content, FAQs, quick references, checklists, and workflows, with match highlighting.
- Visual overhaul: grouped navigation, standardized banners, refined typography and spacing, mobile drawer, accessibility pass.

---

## v1.0 — May 2026 — First working hub

**Added**
- Seven workflow tabs replacing the SLP source-type structure.
- Cross-tab search and the Most-Asked deflector strip.
- Inline quick references and verified state-resource links.

**Fixed**
- Retired CSHA → CASP; removed SLPA supervision and the empty tab.

---

## v0.5 — April 2026 — Redesign blueprint

**Added**
- Workflow-first information architecture defined.
- SLP resource audit (keep/modify/remove/replace) completed.
