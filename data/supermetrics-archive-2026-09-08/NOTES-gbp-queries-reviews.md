# Google Business Profile — Search Keywords & Reviews Archive
**Pulled 2026-09-08 (final Supermetrics harvest; subscription ends 2026-09-09).**
Source: Supermetrics `ds_id: GMB`, account `accounts/100272753749399584663` (All locations of Panka Natural Health).
Location: `Panka Natural Health`, location ID `3326559683279742636`.

---

## 1. What was pulled, and the hard limits

| Dataset | File | Coverage | Rows |
|---|---|---|---|
| Search keywords, monthly detail | `gmb-search-keywords-monthly.csv` | 2025-04 → 2026-07 | 274 |
| Search keywords, aggregated + ranked | `gmb-search-keywords.csv` | same | 134 distinct |
| Search keywords, classified | `gmb-search-keywords-classified.csv` | same | 134 |
| Bucket rollup | `gmb-search-keywords-bucket-summary.csv` | same | 11 buckets |
| Reviews (individual) | `gmb-reviews.csv` | 4 retrievable of 15 lifetime | 4 |
| Reviews monthly rollup | `gmb-reviews-monthly.csv` | 3 bases, see below | 9 |
| Profile views (context) | `raw-gmb-profile-views-monthly.json` | 2025-03 → 2026-09 | 19 |
| Raw API payloads | `raw-gmb-*.json` | — | — |

### Limit 1 — the 2025-03-08 wall
Supermetrics refuses any GMB start date before **2025-03-08** (`[START_DATE_HISTORICAL]`), for *every*
report type, not just Performance. Anything older is unreachable through this tool. The clinic has
operated since 2018, so roughly seven years of profile history is simply not archivable here.

### Limit 2 — search keywords must be whole calendar months
`start_date`/`end_date` must be the first and last day of a month or the query errors. Combined with
Limit 1, the earliest usable keyword month is **2025-04**.

### Limit 3 — 2026-08 keyword data is not published yet
A query for 2026-08 alone returns a single row with an empty keyword and a null metric. Profile *views*
for 2026-08 return fine (567 views), so this is a publication lag in Google's keyword report, not a
permissions or query problem. **Last usable keyword month is 2026-07.** Effective window: 16 months.

### Limit 4 — the volume metric is bucketed (this matters a lot)
`search_impressions` returns **0 for 245 of 274 keyword-months**. That is not a true zero. Google's
Business Profile API returns either an exact `value` (only when monthly impressions are **≥ 15**) or a
`threshold` marker when below it; Supermetrics maps the threshold case to 0. Every non-zero figure in
this archive is 16 or higher — consistent with a threshold of 15.

**So: `0` means "1–15 impressions that month", not "no impressions".** Only **216 impressions across the
whole 16 months** are exactly reported. To make the data rankable I added an estimate column using a
midpoint of 8 for each sub-threshold month, plus `est_low` (=1/mo) and `est_high` (=15/mo) bounds.
Treat every ranking in these files as **ordinal, not cardinal**.

### Limit 5 — the keyword report is not a census
Profile views on Search over the same 16 months total **8,243** (9,595 views overall), against ~2,312
midpoint-estimated keyword impressions. Google truncates the keyword long tail. Use this data for
*which themes appear*, never for *how much volume exists*.

### Limit 6 — second location account is inaccessible
`100272753749399584663_10418367222074184209` ("Panka Natural Health (, : )") returns
*"You do not have permission to view the selected report. Please make sure you have at least Manager
access to the location."* Its lifetime review count comes back null. It appears to be an empty or
duplicate listing stub. Nothing was recoverable from it.

### Limit 7 — only 4 of 15 reviews are individually retrievable
The `ReviewsTotals` report gives a lifetime **15 reviews / 5.0 average**. The per-review `Reviews`
report returns only **4**. Supermetrics filters reviews by **modification date**, not creation date —
proof: a review created **2023-05-15** *is* returned, because it was replied to on 2026-07-17, and the
monthly rollup files it under **2026-07**. So the 11 missing reviews are ones created before
2025-03-08 that have never been edited or replied to since. Their text, dates, ratings and reply status
are permanently unavailable through this tool.

**One thing this limit does NOT undermine:** any review *created* on or after 2025-03-08 necessarily has
a modification time inside the window, so it would be returned. The recent-velocity counts below are
therefore trustworthy even though the lifetime list is incomplete.

---

## 2. Review picture

| Measure | Value |
|---|---|
| Lifetime reviews | **15** |
| Lifetime average rating | **5.0** (every retrievable review is 5★) |
| Reviews in last 12 months (2025-09-08 → 2026-09-08) | **1** |
| Reviews in last 18 months (2025-03-08 → 2026-09-08) | **3** |
| Reviews before 2025-03-08 (implied) | **12** |
| Most recent review | **2025-12-02** — **280 days ago** |
| Longest gap between retrievable reviews | **714 days** (2023-05-15 → 2025-04-28) |
| Currently unanswered (of the 4 retrievable) | **0** |

### Velocity has stopped
Three reviews in 18 months, one in the last 12, and **nothing at all for over nine months**. Twelve of
the fifteen lifetime reviews predate March 2025. The profile is not accumulating social proof, and the
5.0 average is being carried almost entirely by reviews written years ago. For a cash-pay clinic where
the profile is the discovery surface (see §3), a stalled review count is a slow leak: 15 reviews is thin
against metro competitors, and the count has effectively been frozen since December.

There is no review-request step visible anywhere in the tracked funnel. The Acuity intro call
(type `41826455`) is the natural post-visit moment, and asking is entirely off-platform — it routes no
data to Google and so raises none of the compliance concerns that governed the scheduling-event decision.

### Reply behaviour
All four retrievable reviews have replies, and three were answered fast (0–1 days; 97, 1,147 and 1,260
minutes). The exception is stark: the 2023-05-15 review sat unanswered for **1,159 days** and was
finally replied to on **2026-07-17**. That looks like a deliberate backlog cleanup this summer. Because
the other 11 reviews are unreachable, **it cannot be confirmed from this data whether any of them are
still unanswered** — a manual look at the profile is the only way to close that question.

One review (Ariel, 2025-12-02) is a 5★ rating with **no text**. The two long reviews both name
**Dr. Haley** specifically and both describe the same arc: conventional care treated symptoms, lab and
food-sensitivity testing found the cause. Miranda Piehler's names eczema, food sensitivity testing,
postpartum and fertility prep; Kendra Hoffman's names four years of continuity and detailed notes.

---

## 3. Search keywords — brand vs discovery

| Basis | Brand | Non-brand (discovery + service lines + other) |
|---|---|---|
| Midpoint-estimated impressions | **8.3%** (192) | **91.7%** (2,120) |
| Keyword-month rows | **8.8%** (24) | **91.2%** (250) |
| Exactly reported impressions (≥15/mo) | **0 of 216 (0%)** | **216 (100%)** |

**The profile is overwhelmingly a discovery surface, not a brand-recall surface.** Roughly nine in ten
profile searches come from people who did not know the clinic's name. Six brand keywords appear
(`panka`, `panka natural health`, three address variants, and `panka natural health nail fungus oil
blens`), and **not one of them ever crossed 15 impressions in a month** — while `naturopathic doctor`
did so in 6 separate months (peaking at 22).

This is a genuinely useful finding and it cuts against the usual assumption that a Business Profile
mostly catches people already searching your name. Here the opposite holds: the profile is doing
top-of-funnel work. It also means the profile and the paid Leads-Search-1 campaign are competing for
substantially the same non-brand intent.

### Bucket rollup (full detail in `gmb-search-keywords-bucket-summary.csv`)

| Bucket | Distinct kw | Keyword-months | % rows | Est. impressions |
|---|---|---|---|---|
| geo/discovery | 73 | 177 | 64.6% | 1,536 |
| brand | 6 | 24 | 8.8% | 192 |
| modality/other-service | 15 | 22 | 8.0% | 176 |
| Functional Lab Testing | 5 | 12 | 4.4% | 96 |
| other/irrelevant | 6 | 9 | 3.3% | 72 |
| Women's Health & Hormones | 8 | 8 | 2.9% | 64 |
| Pediatrics | 7 | 8 | 2.9% | 64 |
| competitor/practitioner-name | 7 | 7 | 2.6% | 56 |
| Gut Health | 4 | 4 | 1.5% | 32 |
| Metabolic/Diabetes | 2 | 2 | 0.7% | 16 |
| Men's Health | 1 | 1 | 0.4% | 8 |
| Cholesterol/Heart | **0** | 0 | 0% | 0 |
| Brain/Neuro | **0** | 0 | 0% | 0 |

I added four buckets beyond the eight service lines plus brand and geo, because forcing everything into
the requested list would have hidden real signal: `modality/other-service` (homeopathy, ayurveda,
colonics, iridology, cancer), `competitor/practitioner-name` (people searching a named practitioner and
landing on PNH), and `other/irrelevant` (`prana`, `panacea`, `proactive`, `panakumen restaurant`,
`food near me` — unrelated businesses).

Classification judgement calls worth knowing: **thyroid** terms (4 of them) are filed under Women's
Health & Hormones on the hormone axis, though `thyroid testing` would sit equally well under Functional
Lab Testing. `hospital children` is filed under Pediatrics but is plainly a mis-trigger. `dr. pannoch
mn` is filed as a practitioner name though it may be a misspelling of Panka; moving it to brand would
shift the brand share by well under one point.

### Top discovery terms
`naturopathic doctor` (16 of 16 months, 102 reported impressions) · `holistic doctor near me`
(16 months, 35) · `naturopathic doctor near me` (11 months, 79) · `functional medicine doctor near me`
(11 months) · `naturopath` (11 months). These five are the profile's backbone and appear in essentially
every month of the archive.

Geography named organically: Minnetonka (5 keywords — the most-named suburb by far), Minneapolis, Edina,
Eden Prairie, Plymouth, St. Louis Park, Chaska, Chanhassen, Wayzata, St. Paul, Hennepin County, Rogers,
Walker, plus ZIPs 55343 and 55344.

---

## 4. Service lines with organic demand that paid search is not targeting

Leads-Search-1 has six ad groups: Women's Health & Hormones, Men's Health, Functional & Integrative
Medicine, Naturopath Near Me — Core, Geo-Qualified — Hopkins & West Metro, and Pediatrics. Setting the
organic keyword themes against that structure:

**Functional Lab Testing — the clearest unserved demand.** 5 distinct keywords across 12 keyword-months,
the largest non-brand service-line bucket. The `food sensitivity test` family alone appears in 10
keyword-months (`food sensitivity test` 5, `food sensitivity testing near me` 4, `food sensitivity
testing` 1), spanning 2025-05 through 2026-02. Also `holistic lymes disease testing minneapolis`,
`ebv specialist holistic`, and — filed under hormones — `thyroid testing` and `doctors who prescribe
natural thyroid supplements`. There is **no ad group for lab testing**; "Functional & Integrative
Medicine" targets the modality, not the test. This is also the service line the clinic's best review
describes in detail, and it is consistent with the §7 protect list (`test`, `testing`, `panel`, `labs`,
`dutch`), which already anticipates this intent as valuable. Worth Jacob's attention as the strongest
single finding in this dataset.

**Gut Health — no ad group at all.** 4 keywords: `top rated doctors that work with gut health and
inflammation near me`, `naturopathic gut health doctors chaska mn`, `fuctional gi health minneapolis`,
`bowel movement doctors`. A live service line with steady low-level organic demand and zero paid
coverage.

**Metabolic/Diabetes — no ad group.** `homeopathic diabetes managment`, `naturopathic doctor for weight
loss near me`. Thin, but `diabetes` and `weight loss` are both on the protect list.

**Cholesterol/Heart and Brain/Neuro — zero organic keywords in 16 months.** Both are live service lines
that produced no Business Profile search demand whatsoever. That is a real signal: people do not appear
to search for a naturopath by these conditions locally, whatever their value once someone is a patient.

**Men's Health — one keyword in 16 months** (`natural health for men near me`). The Men's Health ad
group carries 31 keywords against essentially no organic demand signal. Not a recommendation to change
anything, but the asymmetry is worth Jacob knowing when he weighs where budget goes, given the campaign
is budget-constrained at 81–89% impression share lost.

**Pediatrics — organic demand confirms the ad group.** 7 keywords, including `holistic pediatrician near
me` in two separate months, `pediatric functional medicine near me`, `holistic pediatric doctor 55344`,
and `"functional and integrative pediatrics minnesota"`. Supports keeping the Pediatrics group active
through the season; the CLAUDE.md decision to defer the plain-pediatrician negative block to Oct 1 looks
consistent with this.

**Two themes outside the service lines.** `homeopathic doctors near me` is the third-strongest
non-discovery keyword (7 months) and `homeopathic` appears in 2 more — PNH is naturopathic, not
homeopathic, so the profile is being surfaced for a modality it does not practise. And three separate
cancer/leukemia searches reached the profile (`holistic doctor for cancer patients mn`, `natural cancer
doctors in minnesota`, `natural doctor on leukemia in minnesota`). Both are observations for Jacob to
judge, not proposed negative keywords.

---

## 5. Method notes for anyone re-reading this later
- GMB report types are inferred from the fields requested; `has_report_type_selection` is false.
  Index map: 0 CustomerMedia, 1 Default, 2 Media, 3 Performance, 4 Post, 5 Reviews, 6 ReviewsTotals,
  7 searchKeyword. `search_keywords` + `search_impressions` = type 7; per-review fields = type 5;
  `total_review_count` / `total_review_star_rating` = type 6.
- Mixing a Performance metric with a Reviews dimension fails; keep report types separate.
- The keyword pull was independently reproduced by a parallel agent in this same harvest
  (`gmb-monthly-search-terms.csv`, 275 rows including the empty 2026-08 stub) and matches this
  archive's 274 data rows exactly. Lifetime review totals (15 / 5.0) also match. Both datasets here
  are cross-validated.
- `build_gbp.py` and `build_reviews.py` in this directory regenerate every CSV from the `raw-*.json`
  payloads. No data row was hand-entered into a CSV.

## 6. Recorded gaps
1. No GMB data of any kind before **2025-03-08**; ~7 years of history unarchivable.
2. **11 of 15 reviews** unreachable — text, dates, ratings, and reply status lost.
3. **2026-08 and 2026-09 keyword data unavailable** (Google publication lag).
4. Second location account **`..._10418367222074184209` returns a permissions error**; nothing recovered.
5. Volume metric is **bucketed at 15/month**; 245 of 274 keyword-months are sub-threshold. Rankings are
   ordinal only.
6. Keyword report captures only ~2,312 estimated impressions against 8,243 profile Search views —
   Google truncates the long tail; this is not a complete query list.
7. `review_reviewer_type` (e.g. Local Guide) **does not exist** in the GMB field set. Only
   `review_reviewer_name` is available; the column is present in `gmb-reviews.csv` filled with
   `not_available_in_api`.
8. Whether any of the 11 unreachable reviews is still unanswered **cannot be determined from this data**.
