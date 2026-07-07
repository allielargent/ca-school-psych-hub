# Hub Conflict Report

Findings are presented, not silently resolved, per instructions. Each includes a recommended resolution and whether human review is required before acting on it.

**Status update (2026-07-06):** Compliance review has fully resolved Conflict 3 (crisis-response citation) and Conflict 2 (both the AB 1432/AB 1913/SB 848 mandated-reporter trainings and the AB 1172 positive-behavior training are now independently verified and correctly separated in the Hub). See the "Resolution" note added to each below. Conflict 6 remains open — nobody has confirmed it either way. No unresolved compliance concerns remain regarding California training requirements.

---

### Conflict 1 — Two different "evaluation timelines" risk being conflated

- **Hub section:** Clinical Toolbox → Timeline Calculator (lines 1875–1888, 2128–2153); Assessment & Eligibility → Timeline Master Reference
- **Hub language:** The calculator adds 60 calendar days to the consent date (with adjustment for breaks >5 days) — this is California's statutory assessment deadline (EC §56344, already cited elsewhere in the Hub's State Resources tab).
- **Help Center source:** [Psych Assessment Timelines](https://providerhelp.parallellearning.com/hc/en-us/articles/23474827019163-Psych-Assessment-Timelines) — Parallel's own internal operational cadence: Week 1 (review referral), Weeks 2–3 (testing sessions), Weeks 4–5 (complete report), Weeks 6–8 (results/eligibility meeting).
- **Conflict/concern:** These are not contradictory — Parallel's 6–8 week internal target is designed to land inside the 60-calendar-day legal ceiling — but they answer different questions (legal maximum vs. company operational target) and use different units (calendar days vs. weeks). If both are surfaced to a provider without clear labeling, it's easy to mistake one for the other, or to assume hitting Parallel's internal pace also guarantees legal compliance in every district calendar scenario (it doesn't automatically — breaks/holidays affect the legal clock differently than a flat week count would suggest).
- **Recommended resolution:** Add the Help Center link labeled explicitly as "Parallel's internal operational target (company expectation)" directly beside the Hub's calculator, which should keep its own label as "California's legal deadline (EC §56344)." Do not merge the two into one number.
- **Human review required:** No — labeling fix only, low risk.

---

### Conflict 2 — Mandated-reporter FAQ is legally accurate but omits Parallel's actual compliance requirement

- **Hub section:** FAQ Center ("Am I a mandated reporter when working remotely?"); Start Here onboarding checklist
- **Hub language (before):** *"Yes. Suspicion is the threshold…"* — a correct statement of the legal standard, but the answer stopped there.
- **Help Center sources:**
  - [California Mandated Reporter Training Requirements for School Personnel](https://providerhelp.parallellearning.com/hc/en-us/articles/51543899095067-California-Mandated-Reporter-Training-Requirements-for-School-Personnel) — AB 1432 Mandated Reporter Training and AB 1913/SB 848 Child Abuse Prevention Training.
  - [California AB 1172 Positive Behavior Training Requirements](https://providerhelp.parallellearning.com/hc/en-us/articles/51585450834203-California-AB-1172-Positive-Behavior-Training-Requirements) — a **separate** PBIS compliance requirement, not part of mandated-reporter training.
- **Status: RESOLVED (2026-07-06).** Compliance has verified both trainings independently:
  - **AB 1432 / AB 1913 / SB 848** confirmed as the correct California mandated reporter / child abuse prevention training requirements, aligned with current California law and guidance. The Hub should continue referencing them.
  - **AB 1172** confirmed as a distinct, official Parallel compliance requirement (certificates valid one calendar year; must remain valid through the end of the school year; Certificate of Completion + payment receipt submitted to support@parallellearning.com) — and explicitly **not** to be grouped under mandated-reporter training.
- **Resolution applied:** The Hub previously listed the AB 1172 article directly adjacent to the mandated-reporter article under one flat, unlabeled list (Start Here → Related Parallel Help Center Articles), and the onboarding checklist ran both training categories into a single clause. Both are now presented as two clearly labeled, separate sections — **"California Mandated Reporter & Child Abuse Prevention Training"** (AB 1432, AB 1913, SB 848) and **"California Positive Behavior Training"** (AB 1172) — with existing links unchanged. The onboarding checklist item was reworded to name the two categories separately.
- **Human review required:** No further action — resolved.

---

### Conflict 3 — Crisis & Safety Checklist references "Parallel's crisis-response flow" without a confirmed, citable source

- **Hub section:** Behavior & Mental Health → Crisis & Safety Checklist; FAQ Center ("A student disclosed self-harm — what do I do?")
- **Hub language (before):** Generic reference to an unnamed internal process — *"Follow Parallel's crisis-response flow."*
- **Help Center source candidates (before):** Two different articles could plausibly be "the" flow — [Emergency/Crisis Planning](https://providerhelp.parallellearning.com/hc/en-us/articles/21631455156379-Emergency-Crisis-Planning) (operational: secure facilitator contact info, review District 101, pre/post-event protocol with the on-site facilitator) and Client Emergencies and Incident Reporting Protocol (HR-section incident-reporting protocol).
- **Status: RESOLVED (2026-07-06).** Compliance confirmed **Emergency/Crisis Planning** (Provider Portal → Getting Started → Provider Expectations) as the sole authoritative source for all crisis/emergency response guidance in the Hub.
- **Resolution applied:**
  - Crisis & Safety Checklist restructured with a new "Before services begin" group (facilitator contact info secured, District 101 reviewed, pre-event communication protocol established — each per the article) and expanded "Reporting & follow-up" group (post-event follow-up with facilitator, resources offered as indicated), with an explicit source citation and link on the first item.
  - "In the moment" checklist items reworded to match the article's actual language: remain connected with the student until onsite personnel are reached; contact the onsite facilitator immediately using the predetermined communication method.
  - The self-harm-disclosure FAQ answer rewritten to name and link Emergency/Crisis Planning explicitly instead of the generic "crisis-response flow" phrase.
  - Emergency/Crisis Planning added to the Behavior & Mental Health tab's "Related Parallel Help Center Articles" block (listed first).
  - Verified via headless Chrome: full render, zero console errors, no remaining occurrences of the ambiguous "crisis-response flow" phrase anywhere in the file.
- **Human review required:** No further action — resolved.

---

### Conflict 4 — "District 101" (Pathway feature) and the Hub's "District Hub" tab risk being conflated

- **Hub section:** District Hub tab (1529–1550)
- **Hub language:** A 7-card template framework (profile, onboarding, contacts, reporting, local procedures, notes) — currently populated with only `[District A]`/`[District B]` placeholders.
- **Help Center source:** [What is District 101?](https://providerhelp.parallellearning.com/hc/en-us/articles/43762478641563-What-is-District-101) — a real, live Pathway feature with actual per-assignment data (contacts, blackout dates, service dates, local scheduling policy) that already replaced Parallel's old Provider Handbook.
- **Conflict/concern:** The similar names ("District 101" vs. "District Hub") could cause a provider to believe the Hub's currently-empty template *is* District 101, or that checking one substitutes for checking the other. They're complementary — District 101 has live operational facts per assignment; the Hub's District Hub is meant to hold deeper clinical/procedural notes per district/SELPA — but that relationship isn't stated anywhere.
- **Recommended resolution:** Add an explicit callout at the top of the District Hub tab clarifying the distinction and linking to District 101 as the authoritative live source for operational facts.
- **Human review required:** No — clarifying language only, but flagging since it affects how providers find real district information.

---

### Conflict 5 — A California-titled Help Center article that is off-topic for this Hub

- **Hub section:** Would be a tempting auto-match for State Resources or Start Here if linking by keyword
- **Hub language:** N/A (not currently linked)
- **Help Center source:** [State Specific Laws: California](https://providerhelp.parallellearning.com/hc/en-us/articles/50268719816475-State-Specific-Laws-California) — this article is entirely about CA **employment law** (State Disability Insurance, Paid Family Leave, CFRA, Pregnancy Disability Leave), not special-education law.
- **Conflict/concern:** Overly specific title match without topical relevance. If this Hub project (or a future automated sync) links Help Center articles by matching "California" in the title, this article would be pulled in incorrectly and would confuse or mislead a school psychologist looking for special-ed guidance.
- **Recommended resolution:** Explicitly excluded from all Hub sections in this update. Flagging so future maintainers (human or automated) don't re-add it based on title matching alone.
- **Human review required:** No — exclusion, not inclusion; no action needed beyond awareness.

---

### Conflict 6 — Possible IDEA vs. CA (5 CCR §3030) terminology mismatch in generated report language (low confidence)

- **Hub section:** Clinical Toolbox → California Eligibility Decision Support Tool's "Generate eligibility summary" / documentation-record feature (lines 2387–2442), built entirely around CA's 13 categories under 5 CCR §3030
- **Hub language:** Category criteria, "pearls," and citations are all framed in CA Ed Code / 5 CCR §3030 terms.
- **Help Center source:** [Report Writer: Eligibility Criteria (Psych Reports Only)](https://providerhelp.parallellearning.com/hc/en-us/articles/33751509827739-Report-Writer-Eligibility-Criteria-Psych-Reports-Only) — states the tool inserts *"some standard language from the Individuals with Disabilities Education Act about the specific eligibility you selected."*
- **Conflict/concern:** This may not be a real conflict — California's 13 eligibility categories are its state implementation of IDEA's federal categories, so the underlying frameworks likely align. But the Report Writer article's own wording names IDEA (federal) specifically, not 5 CCR §3030 (state), and I could not verify from the Help Center content alone whether the auto-inserted language is CA-specific or generic federal boilerplate that a provider would need to adapt. Raising this rather than asserting a contradiction I can't confirm either way.
- **Recommended resolution:** Before linking the Hub's Eligibility Decision Support Tool output directly to the Report Writer eligibility feature as a seamless pipeline, someone with access to Report Writer should confirm whether its auto-generated eligibility language is state-specific for CA users or generic IDEA language needing manual adaptation.
- **Human review required:** **Yes — still open.** Not addressed by the 2026-07-06 compliance review (which covered crisis response and AB 1172 only). This remains the one unresolved item from this report.

---

### Conflict 7 — Minor internal inconsistency, unrelated to Help Center sourcing (noted for completeness)

- **Hub section:** Checklists tab
- **Hub language:** `CHECKLISTS` array contains 13 entries and the panel's own copy (line 1763) says "Thirteen interactive checklists," but `NAV` (line 604) and `DASHBOARD.stats` (line 549) both display "12."
- **Help Center source:** N/A — this is a pre-existing Hub authoring inconsistency, not a Help Center conflict.
- **Conflict/concern:** Internally inconsistent count, could confuse users comparing the dashboard stat to the actual tab.
- **Recommended resolution:** Correct the two "12" references to "13" for consistency. Low-risk, mechanical fix — made as part of this update since it was already surfaced during the audit.
- **Human review required:** No.
