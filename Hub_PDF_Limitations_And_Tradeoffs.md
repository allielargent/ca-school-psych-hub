# Fillable PDF: Limitations & Tradeoffs Before Scaling to All 13 Downloads

Read this before approving the pattern for rollout — these are the honest constraints of the approach, not bugs to be fixed later. Several are inherent to "works identically in Acrobat, Chrome, Edge, and Preview with zero PDF JavaScript," which was the explicit brief.

## 1. Typography does not match the Hub exactly

The PDF uses PDF's built-in Helvetica family, not the Hub's Fraunces (serif headings) / Inter (body) / IBM Plex Mono fonts.

**Why:** Embedding the Hub's actual web fonts requires bundling the TTF font files themselves plus `@pdf-lib/fontkit` (another ~250KB dependency), fetched from Google Fonts. I didn't have a safe way to fetch and vendor arbitrary binary font files in this session, and doing so adds real fragility (subsetting, glyph coverage, file size) for a purely cosmetic gain.

**Tradeoff if we want exact font matching later:** Vendor the actual font binaries + fontkit (adds ~250-800KB depending on how many font weights are embedded) and re-test rendering in all four viewers, since font embedding can occasionally expose renderer bugs (rare, but worth a dedicated QA pass rather than assuming it "just works").

**What we got instead:** Colors, layout, spacing, borders, and section structure are replicated exactly. Helvetica is also, frankly, a very standard choice for compliance/clinical forms — arguably more appropriate for a fillable form than a display serif.

## 2. "Placeholder text" means a static caption, not a disappearing hint

Your spec asked for "clear placeholder text" on fields. Native AcroForms (without JavaScript) have no equivalent to an HTML `<input placeholder="...">` — there's no text that displays inside an empty field and vanishes on focus.

**What we built instead:** A bold caption drawn directly above (or beside) each field, permanently visible, naming what goes in it (e.g., "Referral Date (MM/DD/YYYY)"). This is the standard, most-compatible pattern used by essentially all professional fillable PDFs — but it's a different UX than a web form's placeholder, and it's worth confirming that's what you meant before I apply it to 12 more documents.

## 3. No dynamic "required field" highlighting

Acrobat has a "Highlight Fields" toggle that colors all fillable fields when turned on — this is a *viewer* preference, not something a PDF author fully controls, and it doesn't exist in Chrome/Edge/Preview at all.

**What we built instead:** Fields I judged compliance-critical (Student Name, Referral Date, Consent Date, Evaluator, Completed by, Date Completed) get a permanently more-saturated teal border; everything else gets a light gray border. This is a static design choice baked in at generation time, not a toggle — it can't be turned off, and it doesn't adapt if you decide a different field should be "required" without regenerating the PDF.

**Judgment call made:** I chose which fields count as "required" for this checklist myself, since the request didn't specify. Worth confirming these are the right ones before the pattern propagates to 12 more documents, each of which will need its own required-field judgment call.

## 4. Auto-calculation, auto-check, and tooltips are absent, not degraded

Per your explicit instruction, I didn't ship a "does something in Acrobat, does nothing elsewhere" version of these features — they're simply not in the PDF at all. If you want live progress tracking, that already exists in the Hub's interactive Checklists tab (which is real JavaScript running in a browser, not inside a PDF, so it works everywhere without caveats).

## 5. No true digital/cryptographic signature field

"Signature" is a plain text field (someone types their name), not a PDF signature field with certificate-based validation. A real cryptographic signature field is a materially different, heavier feature (certificate handling, validation UI varies a lot by viewer) that weighs against the "works the same everywhere, no Acrobat-only behavior" goal — Chrome/Edge/Preview's signature-field support is inconsistent. This matches your instruction ("signature/date text fields if appropriate").

## 6. Accessibility is "reasonable," not fully PDF/UA-tagged

Full PDF accessibility (PDF/UA) involves a structured, tagged content tree that assistive technology can navigate (reading order, roles, alt text for images) — a substantially larger effort than field naming and visual captions. What's shipped (descriptive field names, on-page captions, logical creation order for tab flow) is a reasonable baseline, not a certified-accessible document. If PDF/UA compliance is a hard requirement (e.g., for ADA/Section 508), that's a separate, larger effort worth scoping explicitly.

## 7. Two-page layout, not one page

The Initial Evaluation Checklist (15 checklist items + 6 header fields + Most Common Misses box + Notes + sign-off) doesn't fit on one US Letter page at a legible size. It flows to a second page. This matches the "prioritize readability over forcing one page" principle from the earlier print-toolkit work — but it's worth flagging since some of the other 12 downloads are shorter and likely *will* fit on one page (e.g., Larry P., Timeline), while others (FBA's ABC data table, Eligibility Decision Worksheet) may run to 2-3 pages.

## 8. File size

The Hub HTML file grew from ~275KB to ~813KB (pdf-lib itself is ~525KB minified) after vendoring the library once. This is a one-time cost — adding the other 12 documents' field-layout code will add a few KB each, not another 525KB, since they all share the one vendored library and the one `newPdfWriter()` engine.

## 9. What's genuinely reusable vs. document-specific

Reusable (built once, used by all 13 eventually, and portable to future state hubs): `PDF_THEME`, `newPdfWriter()`, `showPdfError()`, `pdfDownload()`, the layout primitives (`sectionLabel`, `fieldGrid`, `multilineField`, `calloutBox`, `checklistItem`).

Document-specific (has to be authored per-document): the field list, section order, which items get a "HIGH-RISK" tag, which fields count as "required," and any document-specific content like the FBA's ABC data table or the Eligibility Worksheet's structured fields — these don't reuse the checklist-item layout at all and will need their own layout primitives added to the engine (e.g., a table-row primitive for FBA's ABC grid).

## Recommendation

The pattern is solid and ready to scale, with two things worth a quick yes/no before I proceed to the other 12: (1) is the static-caption approach to "placeholder text" what you had in mind, and (2) are you fine with the required-field judgment calls being made per-document by me, or do you want to specify which fields are required for each of the remaining 12 documents yourself?
