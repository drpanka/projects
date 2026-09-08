# PNH Google Ads — Context & Status Reference

> **Session reconciliation, Sept 7, 2026 evening (added by Claude Code).** The reference below is Jacob's verified snapshot as of 1:52pm CDT. Changes made in the working session after that time, and verified live afterward, are recorded in `reports/leads-search-1-review-v2-forward-plan-2026-09-07.md`, which is the current working document. Where the two differ on campaign *state* (ad schedule modifiers, max CPCs, match types, location targets), the forward plan is newer. Where they differ on *decisions*, section 6 and section 7 below win; the forward plan's section 8 records how its earlier suggestions were reconciled to them. Summary of state changes since 1:52pm: all 22 ad-schedule rows now carry per-row modifiers (Mon–Thu +15 / −20 / −10 / +15, Fri −30 / −35 / −30 / −10, Sat +10, Sun −20); mobile −15%; six cities at −30% and three at +10%, nine exurb targets removed (10 location targets remain); Women's, Functional, Pediatrics, Core and the kept Men's keywords converted to phrase; 26 keywords paused; group max CPCs set to Core $2.50, Geo $2.60, Pediatrics $2.40, Men's $1.30, Women's $2.60, Functional $1.90. Negatives unchanged at 451.

**Last verified: Sept 7, 2026, 1:52pm CDT · All figures pulled live from Google Ads + GA4 · Rename or copy to `CLAUDE.md` in the working directory if handing to Claude Code**
> **How to use this file.** Everything below was verified against live APIs, not recalled. Sections 1–5 are state. Section 6 is a decision log — those calls were made deliberately by Jacob after review; do not re-litigate them without new evidence. Section 7 is a hard protect list. Section 8 is what's actually open. Section 9 has working query recipes.
---
## 1. Business context
Panka Natural Health (PNH) — cash-pay, fee-for-service naturopathic clinic, 901 1st St N Suite 901A, Hopkins MN 55343. Founded 2018 by Drs. Jacob and Haley Panka. Jacob runs all business operations, marketing, and the ad account himself while carrying a patient load.
- **Pricing:** Adult new patient $450 (2h) · Pediatric new patient $300 · Follow-up $225 · Pediatric follow-up $148 · **Introductory Phone Call $0 (10 min)** · Functional Health Report add-on $150
- **Positioning:** "technically primary care but not traditional." Primary-care-seeker traffic is *wanted*, not a mismatch. Cash-pay; no insurance billing; HSA/FSA accepted; superbills provided.
- **Service lines** (per live site): Women's Health & Hormones · Men's Health (urinary/hormonal, sleep, cognition, performance — **not ED**) · Pediatrics (infancy–21, well-child) · Cholesterol + Heart Health · Metabolic/Diabetes · Gut Health · Brain/Neuro (anxiety, depression, ADHD, insomnia, post-concussion) · Functional Lab Testing
- **Telehealth:** MN (registered) + WI (licensed)
- **Season:** prime booking window is early September → December school break. We are in it now.
- **Competitive:** MIMC has run conquest ads on the PNH brand. A brand-defense campaign exists but is **paused**.
## 2. Systems inventory — verified IDs
| System | Value |
|---|---|
| Google Ads account | `7473953248` (Panka Natural Health) |
| Google Ads tag | `AW-17146544733` — `allow_enhanced_conversions: false` is explicitly set |
| GA4 property | `G-C9PY6T1S90`, property ID `353828960`, named **PNH2** |
| GTM | **none** — all site code goes through Squarespace Code Injection |
| Website | Squarespace 7.1, site ID `639b5f145ddcf84ec32a8f1b`; header injection already in use |
| Scheduler | Acuity — owner `27943652`, ownerKey `0081d9d2`, Powerhouse plan |
| Intro call appointment type | `41826455` "Introductory Phone Call", 10 min, $0.00, intake form `2309402` |
| Calendars | `7700282` Dr. Haley · `8024328` Dr. Jacob |
| Data access | Supermetrics MCP — `ds_id: AW` (Google Ads), `ds_id: GAWA` (GA4) |
**Campaigns:** `Leads-Search-1` (`22767146837`) is the only ENABLED campaign. Paused: `PNHdefense-Website traffic-Search-2` (`23888858069`), `Leads-PMax-Video-1` (`24032465476`), `Campaign #1` (`22625352639`).
## 3. Current campaign state — Leads-Search-1
| Setting | Value | Note |
|---|---|---|
| Status | ENABLED | |
| **Daily budget** | **$10.00** | ⚠️ was $12 on Sept 3, $17 in mid-Aug, ~$25–29 in July. **Trending down, not up.** |
| Bidding | MANUAL_CPC | Google recommends Maximize Conversions — **declined on purpose**, see §6 |
| Geo | PRESENCE only — 6 geo targets + 22-mile radius around 44.9244, −93.4114 | |
| Ad schedule | Live since Aug 17, all 22 rows now carry per-row modifiers | Monday overnight anomaly RESOLVED 2026-09-08: all off-schedule impressions fall on 2026-08-17 only, the day the schedule was created (14 impr, 2 clicks, $5.11, before it took effect). Zero since. |
| Ad groups (6, all enabled) | Women's Health & Hormones (34 kw) · Men's Health (31) · Functional & Integrative Medicine (17) · Naturopath Near Me — Core (15) · Geo-Qualified — Hopkins & West Metro (10) · Pediatrics (6) | |
| Negative keywords | **451** at campaign level (445 phrase, 4 exact, 2 broad) | |
**Impression share is pinned at the 9.99% floor with 81–89% of impressions lost to budget every single day since July.** Rank loss is only 4–16%. The auction will give this campaign roughly 8–9× its current volume at current bids; budget is the only constraint.
## 4. Performance — and the counting trap that distorts it
**⚠️ Read this before comparing any two periods.** Through July, *two* conversion actions were both counted as primary: `PNH2 (web) schedule_appointment` and the older `Begin checkout (Page load …/schedule-an-appointment)`. The old one was demoted ~Aug 1. Raw July totals are therefore roughly double-counted. Every figure below uses **PNH2-only**, apples to apples.
| Period | $/day | Spend | Clicks | Conv | CPA | CVR | CTR |
|---|---|---|---|---|---|---|---|
| Jul 17 – Aug 13 | ~$29 | $849.31 | 383 | 41.98 | **$20.23** | 11.0% | ~4.9% |
| Aug 18 – 31 | ~$11 | $151.68 | 73 | 3 | $50.56 | 4.1% | ~5.7% |
| Sep 1 – 6 | ~$13 | $80.11 | 40 | 1 | $80.11 | 2.5% | 3.6% |
**The account's best-ever CPA came at its highest spend.** Every reduction since has made CPA worse, not better. Any claim that lower spend is producing more traction is not supported by the tracked data — but see §5, because the tracked metric is the wrong metric.
**September demand is clearly back:** impressions ran 1,098 over Sep 1–6 vs ~500 the prior week (Sep 4 alone hit 291). But **CTR fell to 3.6% from ~5%** as impressions rose — the campaign is reaching more marginal queries as seasonal volume returns. That argues for *more* negative-keyword discipline in September, not less.
## 5. Measurement architecture — the central problem
### What Google Ads currently optimizes toward
`PNH2 (web) schedule_appointment` (id `7635668327`, type `GOOGLE_ANALYTICS_4_CUSTOM`) — a **page-reach** event on `/schedule-an-appointment`. It counts interest, not bookings. Acuity exports are the only booking truth.
### What actually exists but isn't being used
**Acuity's GA4 integration is already live and recording real completed bookings as `purchase` events.** Jul 1 – Sep 3: **66 bookings, $7,753 revenue.** Google Ads has counted **one**.
Attribution breakdown (GA4 `purchase`, Jul 1 – Sep 3):
| Session source / medium | Bookings | Revenue |
|---|---|---|
| `(not set)` | 34 | $6,396 |
| `pankanaturalhealth.com / referral` | 14 | **$0.00** ← the free intro calls |
| `(direct) / (none)` | 9 | $451 |
| `google / organic` | 6 | $679 |
| **`google / cpc`** | **2** | **$226** |
| `ads.google.com / referral` | 1 | $1 |
**73% of bookings have unusable attribution.** Paid search is ~28% of site sessions but 3% of attributed bookings. That is a measurement failure, not a performance failure.
### Why: the off-site jump
The "Free Intro Call" CTAs pointed at `https://app.acuityscheduling.com/schedule.php?owner=27943652&appointmentType=41826455` — off-domain, where the AW tag doesn't exist. Acuity opens a **new session referred by pankanaturalhealth.com itself**, erasing the ad click. The 14 `$0.00` self-referral bookings are the fingerprint. There are **9 such CTAs**: homepage ×5, `/naturopathic-medicine` ×2, `/contact` ×2. Jul 1 – Sep 3: **47 outbound clicks (11 paid), 17 completed intro-call bookings, 0 visible to Google Ads.**
### The iframe detail that matters
Frame chain when Acuity is embedded: `pankanaturalhealth.com → app.acuityscheduling.com → sandbox.acuityinnovation.com` (a 1×1 sandboxed conversion frame). This is why the historical fix needed `window.top` rather than `window.parent`. **But that frame is cross-origin — `window.top.gtag(...)` throws a SecurityError and fails silently. Only `postMessage` works.** If any existing snippet calls `window.top.gtag` directly, it has never fired. Unverified; needs a console check on a live test booking.
Also verified from `embed.js` source: the iframe-src builder reads the **parent page's** `location.search` and forwards params matching an allowlist that includes `/appointmentType/` and `/field:[0-9]+?/` — but **not `gclid`**. So `/schedule-an-appointment?appointmentType=41826455` loads the existing page with the intro call preselected, and a gclid must be mapped into a `field:<ID>` param to survive.
### ✅ What's been fixed (Sept 4–7)
**`Intro Call Click` conversion action now exists** — id `7747774028`, type WEBPAGE, category BOOK_APPOINTMENT, ONE_PER_CLICK, ENABLED, label `AW-17146544733/WT76CMzMtu4cEN2EjvA_`.
**But it has recorded 0 conversions,** and GA4 shows only 2 intro-call outbound clicks in Sep 1–7 (both direct, none paid). Zero-with-zero-opportunity is indistinguishable from broken. **Action: click a Free Intro Call button yourself with Tag Assistant open and confirm the hit fires.** Also confirm it is set **Secondary** — clicks run ~2.8× hot against bookings (47 clicks → 17 bookings ≈ 36% completion), so it should not be a bidding target.
### Still open in the measurement stack
- Bookings remain unattributable — the click fires on-domain, the *booking* still completes on Acuity's domain as a self-referral. Fix: repoint the 9 CTAs to `/schedule-an-appointment?appointmentType=41826455` (no new page needed).
- `PNH2 (web) purchase` (id `7196843730`) is enabled but starved. It should become the primary conversion once attribution is repaired.
- `generate_lead`: 95 events Jul–Sep, all on `/contact`, 26 from paid, none in Google Ads — **but only 33 `form_start` and 1 `form_submit`, so 95 real submissions is arithmetically impossible.** Identify what fires this before trusting it.
- `tel:+16125688382` and the Chatbase "PNH Guide" chatbot have zero tracking.
- `allow_enhanced_conversions: false` blocks Enhanced Conversions for Leads and general uplift.
## 6. Decision log — settled, do not re-litigate
| Decision | Rationale |
|---|---|
| **Manual CPC retained; Maximize Conversions declined** | Smart bidding aimed at a page-reach event would optimize toward cheap curiosity clicks. Revisit only after real bookings are the primary conversion. |
| **ED terms blocked** (erectile, erection(s), ed, penis/pennis/penile, girth, enlarge/enlargement, hard on, get hard, sexual supplements, vacuum therapy, enhancement) | Men's Health advertises urinary/hormonal health, not ED. Already live since the August build. |
| **"estrogen" left open; `estrogen replacement`, `estrogen patches`, `hormone replacement`, `hrt` blocked** | Jacob's call — a woman researching estrogen may be a menopause patient; prescription-seeking phrasing is not servable. |
| **"primary care" left open; `primary physician(s)` blocked** | PNH is non-traditional primary care. The "physician" forms signal conventional-MD intent. |
| **General nouns left open** (diet, foods, exercises, vitamin, pill, products, symptoms) | Existing phrase negatives (`foods to`, `vitamins for`, `symptoms of`, `pills`, `relief`) already catch the junk forms; blanket blocks would kill "vitamin deficiency doctor near me" and similar. |
| **Dermatology, cardiology, rheumatology, allergist, geriatric left open** | Eczema/acne, heart health, autoimmune, and allergy testing are all live service lines; queries were "holistic/integrative/natural X". |
| **Block 6 (plain-pediatrician exact set) deferred to Oct 1** | Well-child visits are a service, peds competitors already blocked, and back-to-school is peak pediatric demand. Revisit with September data. |
| **`concierge` and `herbalist` removed from negatives** (Sept 4–7) | Concierge-medicine searchers expect direct-pay care; botanical medicine is core to the practice. |
| **No new `/intro-call` page** | Jacob's stated preference — click tracking via footer snippet instead. |
## 7. Protect list — never add as negatives
`test` · `testing` · `panel` · `labs` · `dutch` · `testosterone` · `low testosterone` · `adrenal fatigue` · `diabetes` · `cholesterol` · `weight loss` · `fertility` · `adhd` · `anxiety` · `depression` · `insomnia` · `sleep` · `menopause` · `perimenopause` · `pcos` · `hopkins` · bare `treatment` · `telehealth` · `virtual` · `primary care` · `estrogen` · `concierge` · `herbalist`
Rationale: each maps to a live service line or produced a tracked conversion. "where to get hormones tested," "severe daytime sleepiness," and "adrenal fatigue doctor near me" all reached the schedule page.
## 7b. SUPERSEDED BY THE 2026-09-08 DATA REVIEW

Read `reports/leads-search-1-final-data-review-2026-09-08.md` before acting on section 4 or 8 below.
The full dataset is archived at `data/supermetrics-archive-2026-09-08/` and needs no subscription.
Corrections established there, with sources:

- The "$11.57 CPA in 2025 vs $34.79 in 2026" comparison is INVALID. The 18-conversion July 2026
  figure counts eleven days of one action; primary conversion actions were switched on 2026-07-12.
  Like-for-like, July 2026 was the account's best month ever at $9.35 CPA versus $11.57 for
  Jul-Aug 2025. The rebuild did not raise cost per outcome. (`ads-cpa-like-for-like-monthly.csv`)
- The real problem is AUGUST 2026: same spend and clicks as July, half the outcomes. Undiagnosed.
- The account was DARK 2025-09 through 2026-03. Cross-era comparisons span a seven-month gap.
- Keywords that actually served: 14 (Jul 2025, one ad group) vs 102 (Jul 2026, seven ad groups) —
  not 19 vs 83. (`ads-keyword-count-by-month.csv`)
- Impression share of exactly 0.0999 is Google's floor, not a measurement. July 2025 did carry
  genuine higher readings. The failure mode flipped from rank-loss to budget-loss; total share
  captured barely moved (13.2% to 12.5%). (`ads-impression-share-floor-analysis.csv`)
- Google Business Profile: bookings genuinely zero across all 550 days; a DUPLICATE LISTING exists
  (10418367222074184209) sharing name/phone/website with the live one; 66% of profile search volume
  is discovery intent, not brand; last review was 2025-12-02.
- Profile views are not comparable to ad clicks. Like-for-like: profile 711 website clicks over
  18 months (~39/mo) vs paid search 1,383 clicks over ~14 active months (~99/mo).

## 8. Open threads, ranked
1. **Budget: $10/day and falling, in peak season, with 81–89% of impressions lost to budget.** The account's best CPA ($20.23) came at ~$29/day. This is the single largest unexploited lever and it has moved the wrong way three times. Decide deliberately or restore to $25.
2. **Verify the Intro Call Click snippet actually fires** — manual test with Tag Assistant; confirm Secondary.
3. **Repoint the 9 intro-call CTAs** to `/schedule-an-appointment?appointmentType=41826455` to repair booking attribution without building a page. Test one booking end-to-end first.
4. **Promote `PNH2 (web) purchase` to primary** once attribution is clean (~2 weeks after #3), demote `schedule_appointment` to secondary.
5. **Reconcile GA4's 66 purchases against Acuity's own appointment count** for Jul 1 – Sep 3 before trusting `purchase` as the bidding signal.
6. **Residual search-term leakage:** $28.44 of $45.66 visible Sep 1–7 spend still passes through. Candidates: `[holistic]` exact ($4.26, 2 clicks on a bare one-word query), `poop`, `chakra`, and the symptom family (`thyroid symptoms`, `menopause symptoms`, `signs of early menopause`, `preventive screenings for women`, `low acth` = $14.07/week ≈ $56/mo, which runs well above the $3–4/mo estimated when "symptoms" was left open — worth revisiting now that CTR is falling).
7. **Un-applied recommendations from the Sept 3 list** (deliberate or overlooked, unclear): `psychiatrists`, `chronic` exact, bare GLP-1 brands (`ozempic`/`wegovy`/`semaglutide`/`mounjaro` — only purchase-phrase forms are live), `walgreens`, `cvs`, plural completions (`chiropractors`, `acupuncturists`, `hospitals`).
8. **Brand-defense campaign is paused** while MIMC conquesting continues and busy season runs.
9. **No PNH monitoring automation exists.** The only scheduled task on the account is an unrelated investing news watch. A mid-month pacing/CPA check was discussed but never created.
## 9. Query recipes that work
```
# Campaign settings + negatives + ad groups (large — output saves to file, parse with python)
campaign_and_resource_get(ds_id="AW", account_id="7473953248",
  resource_type="campaigns", params={"campaign_id":"22767146837","campaign_detail_level":"full"})
# Daily performance
data_query(ds_id="AW", ds_accounts="7473953248", date_range_type="custom",
  start_date=..., end_date=...,
  fields="Date,Impressions,Clicks,Cost,Conversions,Ctr,CPC,SearchImpressionShare,SearchBudgetLostImpressionShare,SearchRankLostImpressionShare",
  filters="Campaignname =@ Leads-Search")
# Search terms that cost money
data_query(ds_id="AW", ..., fields="Searchterm,Adgroupname,QueryTargetingStatus,Impressions,Clicks,Cost,Conversions",
  filters="Campaignname =@ Leads-Search AND Cost > 0")
# Conversion actions in the account
campaign_and_resource_get(ds_id="AW", account_id="7473953248", resource_type="conversion_types")
# GA4 — real bookings by attribution
data_query(ds_id="GAWA", ds_accounts="353828960", ...,
  fields="eventName,sessionSourceMedium,eventCount",
  filters="eventName == purchase OR eventName == click OR eventName == schedule_appointment")
# GA4 — intro-call outbound clicks
data_query(ds_id="GAWA", ds_accounts="353828960", ...,
  fields="sessionSourceMedium,linkDomain,eventCount", filters="linkDomain =@ acuity")
```
**Gotcha:** GA4 `purchase` events carry Acuity's page paths (`/schedule/0081d9d2/appointment/<typeID>/…`), which is how you separate intro calls ($0.00, type `41826455`) from paid appointments.
## 10. Companion documents
Both in `~/Documents/Marketing/`:
- `PNH_LeadsSearch1_Negative_Keywords_2026-09.md` — the ranked negative-keyword list with paste blocks and the protect list
- `PNH_Conversion_Tracking_Gap_2026-09-03.md` — the four ranked tracking fixes with working code (click snippet, Acuity `postMessage`, GCLID capture)

In this repository: `reports/` holds the Sept 6 review, the Sept 7 Monday guide, the Acuity addendum, and the forward plan (current working document).
