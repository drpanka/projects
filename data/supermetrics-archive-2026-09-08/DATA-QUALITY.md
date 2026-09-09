# DATA-QUALITY.md — read this before quoting any number from this archive

**Status: guardrail file. Written 2026-09-08, the day before the Supermetrics subscription ended.**

This archive is honest but it is not self-explanatory. Two separate people have already drawn a
confident, wrong conclusion from it — one about CPA collapsing, one about the keyword count. Both
were arithmetic on top of a definition that had silently changed underneath them. Neither person was
careless. The data simply does not announce its own discontinuities.

Every hazard below is stated with **the file and the column it applies to**, so you can check whether
the number you are about to quote is standing on one of them. The last section lists the specific
comparisons that are **not valid to make with this data at all**, no matter how you slice it.

Where this file and an older `NOTES-*.md` disagree on a *count*, this file is newer and was checked
against the CSVs on disk on 2026-09-08.

---

## 1. Conversion counting changed five times. `Conversions` does not mean one thing.

The single most dangerous column in this archive is `Conversions` in the Google Ads files. It is the
count of whatever actions were flagged *primary* at the time — and that set changed five times in
fifteen months. Nothing in the data marks the change.

**Where the regimes are documented:** `ads-cpa-like-for-like-monthly.csv`, column `counting_regime`.
The five verbatim values, and the months each covers:

| Regime | What was counted as a conversion | Months |
|---|---|---|
| **A** | Begin checkout + 3 page-view actions primary (page-views dropped from Campaign #1 on 2025-07-07/08) | 2025-06, 2025-07 |
| **B** | Begin checkout + `meet-dr-haley` + `meet-dr-jacob` + `whypnh` page views, all primary | 2025-07, 2025-08 |
| **D** | Begin checkout primary only (page-views demoted during the dark period; `PNH2 purchase` promoted ~2026-06-26) | 2025-09, 2026-04, 2026-05, 2026-06 |
| **D→E SPLICE** | **2026-07-12.** Begin checkout counted Jul 1–11 only; `schedule_appointment` counted Jul 13–31 only | 2026-07 |
| **E** | `PNH2 (web) schedule_appointment` + `PNH2 (web) purchase` primary; Begin checkout demoted to secondary | 2026-08, 2026-09 |

(There is no regime C. The lettering was assigned during the first pass and is kept as-is so the
label in the CSV matches this table exactly.)

### The 2026-07-12 splice, specifically

This is the one that produced the wrong answer. On **2026-07-12** the primary conversion action was
switched. The consequence is not that July's number is noisy — it is that **July 2026's reported
conversion total is two partial months of two different metrics glued together**:

- `Begin checkout` counted **2026-07-01 through 07-11 only** (11 days)
- `schedule_appointment` counted **2026-07-13 through 07-31 only** (19 days)
- 2026-07-12 itself sits on the seam

The widely-quoted **"$11.57 CPA in 2025 vs $34.79 in July 2026, conversions fell to 18"** comparison
is **invalid**. The 18-conversion figure is eleven days of one metric. Corrected like-for-like, using
`Begin checkout` all-conversions on click date throughout:

| Month | Like-for-like CPA |
|---|---|
| 2025-07 | $11.07 |
| 2025-08 | $12.21 |
| **2026-07** | **$9.35 — the account's best month ever** |
| 2026-08 | $23.28 |
| 2026-09 | $25.62 |

**The real unexplained problem is August 2026, not July.** August ran essentially the same spend
($652 vs $626) and clicks (315 vs 309) as July, and like-for-like conversions **halved, 67 → 28**.
That is the question worth asking. July was the high-water mark.

### How to compare conversions safely

- Use `ads-cpa-like-for-like-monthly.csv`, columns `LFL_begin_checkout_all_conversions_clickdate`
  and `LFL_CPA_begin_checkout_clickdate`. These hold one definition constant across the whole history.
- Do **not** use `as_reported_conversions_metric` or `as_reported_CPA_DISTORTED` for cross-month
  comparison. The column is named `_DISTORTED` on purpose.
- `ads-conversions-composition.csv` breaks each month's counted total into what actually produced it
  (`counted_scheduling_page_or_event`, `counted_doctor_bio_page_view`, `counted_whypnh_page_view`,
  `counted_purchase`, `counted_other`). If you need to know *why* a month looks good, start here.
- `ads-conversions-by-action-monthly.csv` / `-daily.csv` carry `primary_for_goal_now` and
  `include_in_conversions_now`. The `_now` suffix is literal: these are **today's** flags stamped onto
  historical rows. They do **not** tell you what was primary at the time.

### And the tracked conversion is not a booking

Even within one regime, `schedule_appointment` is a **page-reach event** on
`/schedule-an-appointment`. It counts interest, not appointments. Acuity is the only booking truth,
and Acuity's export is not in this archive.

---

## 2. The account was dark for seven months (2025-09 → 2026-03)

`ads-campaign-monthly.csv`, column `Yearmonth`, contains only:
`2025|06, 2025|07, 2025|08, 2025|09, 2026|04, 2026|05, 2026|06, 2026|07, 2026|08, 2026|09`.

**2025-10 through 2026-03 are absent entirely, and 2025|09 is present but has `Impressions = 0` and
`Cost = 0`.** So the real gap is seven months of zero delivery, with a live-but-not-serving September.

Consequences:

- Any month-over-month or trend line that spans the gap is joining **two separate campaign
  lifetimes**, not a continuous series. The ad groups, keywords and creative differ completely on
  either side.
- A missing month is **not a zero**. Do not fill it, do not interpolate it, and do not include it in
  an average.
- Anything described as "year over year" across this gap is meaningless.

---

## 3. Search impression share of 0.0999 is a reporting floor, not a measurement

**File:** `ads-impression-share-floor-analysis.csv`. **Columns:** `reported_SearchImpressionShare`,
`reported_is_floored`, `implied_true_SIS_1_minus_lost`, `sum_of_three`, `overstatement_pp`.

**61 of the 160 day-rows are flagged `reported_is_floored`, and every single one reports exactly
`0.0999`.** On those days the three shares (impression share, lost-to-budget, lost-to-rank) sum to
exactly 1.0000, which is the fingerprint of a value that has been clamped rather than computed.

Treat 0.0999 (and 0.1) as **"at or below Google's reporting floor"** — the true value is unknown and
could be anything below it. Use `implied_true_SIS_1_minus_lost` when you need a usable estimate, and
never average `reported_SearchImpressionShare` across floored and non-floored days.

**What did and did not change.** Share actually captured barely moved: **13.2% (Jul 2025) → 12.5%
(Aug 2026).** What flipped is the *failure mode* — **70% rank-loss / 18% budget-loss** then, versus
**7% rank-loss / 90% budget-loss** now. A narrative built on "our impression share collapsed" is
reading the floor, not the auction. The correct statement is that the constraint moved from ad
quality to budget.

---

## 4. Keyword and ad-group statuses are today's status stamped on historical rows

Google's KeywordView report carries no historical status. Every `Adgroupstatus`, `Keywordstatus` and
`Campaignstatus` value in `ads-keywords-alltime.csv`, `ads-keywords-monthly.csv` and
`ads-keywords-quality-score-monthly.csv` is **the status as of 2026-09-08**, applied to rows from
every month in the file.

### The removed ad group that still says Enabled

**Ad group 1** (`AdgroupID = 183759893484`) in Leads-Search-1 is `removed` today. Its keywords all
still report `Keywordstatus = enabled`. They cannot serve.

**Correction to a figure in circulation:** the number is **34 distinct keywords, not ~65.**
Verified in `ads-keywords-alltime.csv`: 34 rows have `Adgroupname = "Ad group 1"`,
`Adgroupstatus = removed`, `Keywordstatus = enabled`, all under `AdgroupID 183759893484`. The 65 was
a count of *monthly rows*, not of keywords. (There is a second, unrelated "Ad group 1" — `196283052145`
in PNHdefense — which is genuinely enabled. Filter on `AdgroupID`, never on ad-group name.)

The obvious filter — *"enabled keyword AND non-removed ad group"* — is correct for today and
**catastrophically wrong for history**. Applied to August 2025 it reports **zero active keywords in a
month that spent $659.60 and took 3,675 impressions.** That ad group *was* the entire account
through 2026-06: lifetime **$1,834.76, 57% of all Leads-Search-1 keyword spend ever**, and 253.02 of
348.23 lifetime conversions.

**Use `ads-keyword-count-by-month.csv` instead.** Its `active_keywords_served` column counts keywords
that actually took an impression that month. The honest comparison is **14 keywords served in
Jul 2025** (all in the now-removed Ad group 1) versus **102 in Jul 2026** across seven ad groups.
Not "19 vs 83".

### Two more traps in the same files

- **Criterion IDs are shared across ad groups.** `KeywordID` alone is not unique — `296740931208`
  ("holistic dr near me") appears under both the removed *Ad group 1* and the live *Naturopath Near
  Me — Core*. Every count in this archive keys on **(AdgroupID, KeywordID)**. Keying on `KeywordID`
  alone undercounts by roughly 20%.
- **A match-type change mints a new criterion ID.** The Sept-2026 broad→phrase conversion did not
  edit keywords; it created new ones and removed the old. That is why 61 Leads-Search-1 rows read
  `Keywordstatus = removed` inside *enabled* ad groups, and why one "keyword" 's lifetime history is
  split across two rows.

### Campaign names are not unique either

`ads-campaign-inventory.csv` lists **three** campaigns named `Leads-PMax-Video-1`
(`24028056923`, `24032463085`, `24032465476`); two are `removed`. Always join on `CampaignID`.

---

## 5. GA4 `purchase` events are not a booking count

**Files:** `ga4-purchases-detail.csv`, `ga4-purchases-monthly.csv`, `ga4-purchases-by-page-monthly.csv`.

A GA4 `purchase` event has meant three different things:

| Period | What a `purchase` event actually was |
|---|---|
| 2023-12 → 2024-11 | Squarespace **store orders** and page-unattributed events. Not appointments at all. The 23 in 2024-02 and 24 in 2024-03 are shop orders. |
| 2024-12 → 2026-05 | A mix of Acuity scheduler pages and Squarespace orders. **Not separable at month grain.** |
| 2026-06 → 2026-09 | Predominantly Acuity scheduler; the intro-call type is identifiable by page path. **Still overcounts real bookings by roughly 45% — one Acuity booking can fire up to three purchase events.** |

So the 66 GA4 purchases recorded Jul 1 – Sep 3 are **not 66 bookings.** Good as a date-level
indicator that *something* happened; bad as a volume count; useless as a revenue figure across the
2024/2025 boundary.

Also note `ga4-purchases-detail.csv` mixes two row grains — see column `detail_grain`:
121 rows at `date x source x pagePath x transactionId` and 218 rows at
`date x sessionSourceMedium only`. **Summing the file without filtering on `detail_grain`
double-counts.**

`ga4_purchase_events_google_cpc` is **6 events across the entire history.** That is not a measurement
of paid-search bookings; it is a measurement of how thoroughly attribution is broken.

---

## 6. `pankanaturalhealth.com / referral` is NOT junk — do not filter it out

**Files:** `ga4-source-medium-monthly.csv` (`sessionSourceMedium`), `ga4-purchases-detail.csv`,
`ga4-self-referral-pollution.csv`.

This is the most counterintuitive item in the archive, and the easiest to "clean up" by mistake.

When a visitor clicked a Free Intro Call CTA, they were sent off-domain to
`app.acuityscheduling.com`, where the AW tag does not exist. Acuity opened a **new session referred
by pankanaturalhealth.com itself**, erasing the ad click. The 14 bookings that show
`pankanaturalhealth.com / referral` with **$0.00 revenue** are the free intro calls — they are the
**fingerprint of real bookings whose attribution the scheduler destroyed.**

Delete that row as "self-referral noise" and you delete the only surviving evidence those bookings
happened. Keep it. Label it. Never sum it into `(direct)`.

### What *is* genuine pollution, and is a different thing entirely

`ga4-self-referral-pollution.csv` (columns `detection_field`, `polluted_value`) isolates the
operator's own tag testing — **74 rows across four values**: `tagassistant.google.com / referral` (30),
`ads.google.com / referral` (25), `https://tagassistant.google.com/` (16), `https://ads.google.com/` (3).
*These* should be excluded from conversion analysis. They are Jacob's own Tag Assistant sessions, not
patients. Do not confuse them with the pankanaturalhealth.com self-referral above, which is real.

---

## 7. Paid search exists in GA4 before the Ads account did

GA4 records **5,824 `google / cpc` sessions between 2023-03 and 2025-03** (roughly Mar–Sep 2023 and
Feb 2024 – Mar 2025). Google Ads account `7473953248` has **no delivery at all before 2025-06**.

PNH therefore ran paid search from **an account that is not in this archive** — a prior account, an
agency account, or one never connected to Supermetrics. Its spend, clicks, keywords and search terms
are unrecoverable now that the subscription has lapsed.

Those months have GA4 session columns populated and **every Google Ads column blank**. Do not read
the blank as zero, and do not compute a blended cost-per-session across that boundary.

---

## 8. Google Business Profile: a hard history wall and a suppression threshold

**History wall.** GBP data begins **2025-03-08** and cannot go earlier — Supermetrics returns
"Earliest supported historical start date for Google My Business is 2025-03-08". Verified: the
earliest `date` in `gmb-daily-metrics.csv` is exactly `2025-03-08`. The clinic's first 6.5 years on
Google were already unrecoverable before this archive was made. 550 days are covered.

**Suppression threshold.** In `gmb-search-keywords-monthly.csv`, `gmb-search-keywords.csv` and
`gmb-monthly-search-terms.csv`, Google suppresses search-term counts below roughly **15/month** and
renders them as **0**. In this archive **262 of 274 monthly search-term rows are sub-threshold** —
flagged in column `is_sub_threshold`, with `reported_impressions = 0` on every one of them.

**A 0 in those files means "below threshold", never "none".** Use
`estimated_impressions_midpoint` if you need a usable magnitude, and never sum
`reported_impressions` to a total — it will understate by a wide and unknowable margin.

**Bookings are genuinely zero, though.** `gmb-daily-metrics.csv` / `gmb-monthly-metrics.csv`, column
`actions_bookings`, is 0 in **every month and every day** of the 550. That one is a real zero: no
booking action is wired to the profile. Against 10,767 views, 1,768 actions, 711 website clicks, 981
direction requests and 76 calls, that is a live finding, not a data gap.

**Duplicate listing.** A second GBP listing (`10418367222074184209`) shares the name, phone and
website with the live one (`3326559683279742636`) but has no address and no traffic. Any
location-level aggregate that does not filter on `location_id` will treat it as a real second
location.

---

## 9. Smaller traps worth knowing

- **Google Ads history wall: 2023-08-08.** Supermetrics refuses any Google Ads start date earlier
  than this. It never mattered for PNH (delivery began 2025-06) but it caps what any re-pull could
  have reached.
- **`Impressions` are unaffected by the conversion re-definition.** When the conversion columns are
  untrustworthy, impressions and clicks are still directly comparable across all periods. Reach for
  those.
- **`raw-*.json` files are single-line JSON with no trailing newline.** `wc -l` reports 0. That is
  normal and not a defect.
- **Off-schedule serving is a closed question.** `ads-offschedule-check.csv`: every off-schedule
  impression falls on **2026-08-17**, the day the ad schedule was created — 14 impressions, 2 clicks,
  $5.11, and zero since. It is not an ongoing leak.
- **`Cost` has no currency dimension** in the Ads CSVs. It is USD throughout; the Supermetrics API
  flags this on every query.
- **Non-aggregatable metrics.** `Ctr`, `CPC`, `CPM`, `ConversionRate`, `Bouncerate` and similar are
  pre-aggregated at source. Each row is correct on its own; averaging them across rows is
  mathematically invalid. Recompute from `Clicks / Impressions` and `Cost / Conversions` instead.

---

## 10. Comparisons that are NOT valid with this data

Stated flatly, because this is the section that exists to stop the third wrong conclusion.

1. **Any conversion or CPA comparison between two months in different counting regimes** — use the
   `LFL_*` columns of `ads-cpa-like-for-like-monthly.csv` or do not make the comparison.
2. **July 2026 vs anything, using reported conversions.** July 2026 is a spliced month: eleven days
   of one metric plus nineteen days of another. The "$11.57 vs $34.79, 18 conversions" comparison is
   dead. Do not revive it.
3. **Any comparison spanning 2025-09 → 2026-03.** Seven dark months separate two different campaign
   lifetimes. There is no trend across that gap, only a before and an after.
4. **Year-over-year anything.** See (3). There is no continuous year in this account.
5. **Impression-share trends built on `reported_SearchImpressionShare`.** 61 day-rows are clamped at
   0.0999. Compare `implied_true_SIS_1_minus_lost`, or compare the *failure mode* (budget-loss vs
   rank-loss) instead.
6. **Keyword counts that trust `Keywordstatus` on historical rows.** 34 keywords in a removed ad
   group report Enabled. Use `active_keywords_served`.
7. **Keyword aggregates keyed on `KeywordID` alone** — undercounts ~20%. Key on
   `(AdgroupID, KeywordID)`.
8. **Treating GA4 `purchase` counts as bookings**, in any period. Wrong thing entirely before
   2024-11; unseparable through 2026-05; ~45% overcounted after.
9. **Summing `ga4-purchases-detail.csv` without filtering `detail_grain`** — the file holds two row
   grains and will double-count.
10. **Filtering out `pankanaturalhealth.com / referral`.** Those are real bookings. Filter the
    tagassistant/ads.google.com rows instead.
11. **Reading blank Google Ads columns before 2025-06 as zero spend.** GA4 shows 5,824 paid sessions
    in that window from an account this archive never had access to.
12. **Reading a 0 in any `gmb-*search*` file as "nobody searched that."** It means "below Google's
    ~15/month threshold." 262 of 274 rows are suppressed.
13. **Comparing GBP performance to any period before 2025-03-08.** The data does not exist and cannot
    be obtained.
14. **Averaging `Ctr`, `CPC`, `CPM` or `ConversionRate` across rows.** Recompute from the underlying
    counts.
15. **Joining on campaign or ad-group *name*.** Three campaigns share the name
    `Leads-PMax-Video-1`; two ad groups share `Ad group 1`; two GBP listings share the clinic name.
    Join on IDs.

---

## 11. What this archive still cannot tell you

No amount of careful reading fixes these. They are absences, not hazards:

- **Which ad clicks became patients.** Attribution breaks at the Acuity scheduler. The archive can
  show that bookings happened and that paid search was ~28% of sessions; it cannot connect the two.
  Only the Acuity export can, and it is not here.
- **True booking counts.** Use Acuity's own export.
- **Anything about the seven dark months, or about paid search before 2025-06.**
- **Business Profile before 2025-03-08.**
- **Auction Insights / competitor share.** The Supermetrics Google Ads connector exposes no such
  report type — it does not exist in the connector's 40 report types. The MIMC conquesting question
  cannot be answered from this data at all.
