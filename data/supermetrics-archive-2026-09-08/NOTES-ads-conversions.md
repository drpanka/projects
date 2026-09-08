# NOTES — Google Ads conversion actions: definitions, full history, and the 2025-vs-2026 counting break

Archive slug: `ads-conversions` · Pulled 2026-09-08 · Account `7473953248` (Panka Natural Health)
All figures pulled live from Supermetrics `ds_id=AW`, timezone `America/Chicago`, before the
subscription lapses 2026-09-09. Nothing below is recalled; every number traces to a file in this folder.

---

## HEADLINE

**The widely-quoted "$11.57 CPA in 2025 versus $34.79 in 2026" is not sound. It compares two
different counting regimes, and the 2026 half of it divides a full month of spend by 11 days of
conversions.** Both numbers were reproduced exactly from the raw data (see §4). On a genuine
like-for-like basis the direction of the comparison **reverses**: July 2026 was *cheaper* per
scheduling-page load than July–August 2025.

| | quoted | what it actually is | corrected |
|---|---|---|---|
| 2025 | **$11.57** | Leads-Search-1 Jul+Aug 2025 cost $1,434.24 ÷ 124 `Begin checkout` conversions | $11.57 (valid — in 2025 this action's Conversions == All conversions) |
| 2026 | **$34.79** | Leads-Search-1 **July 2026 full-month** cost $626.29 ÷ **18** `Begin checkout` conversions | **$9.35** (÷ 67, the action's full-month All conversions) |

The 18 is not a July figure. It is a **1–11 July** figure. The action was dropped from the
`Conversions` metric on 2026-07-12. Spend for 1–11 July was **$113.80**, so even the matched-window
CPA is **$6.32**, not $34.79 — the quoted number overstates cost per conversion by **5.5×**.

---

## 1. Conversion action inventory

Files:
- `ads-conversion-action-definitions.json` — full definitions from both sources
- `ads-conversion-actions.csv` — id, name, type, category, status, counting, primary-for-goal, include-in-conversions, attribution model, lifetime volume

17 conversion actions exist. Two sources were used because they disagree:

- `campaign_and_resource_get(resource_type="conversion_types")` returned **15** — it omits actions
  whose status is not visible in the UI list.
- The `ConversionAction` report (`data_query`, report type 22) returned **17**, adding
  `7151555473 "Submit lead form"` (**REMOVED**) and `7196843733 "PNH2 (web) generate_lead"` (**HIDDEN**).
  Only the report exposes `PrimaryForGoal`, `IncludeInConversionsMetric`,
  `ConversionActionCountingType` and `AttributionModel`.

Current state, 2026-09-08 — the four actions that feed the `Conversions` column:

| id | name | counting | primary for goal | include in Conversions |
|---|---|---|---|---|
| 7635668327 | PNH2 (web) schedule_appointment | ONE_PER_CLICK | true | **true** |
| 7196843730 | PNH2 (web) purchase | MANY_PER_CLICK | true | **true** |
| 7151526666 | Lead form - Submit | ONE_PER_CLICK | true | **true** (0 lifetime) |
| 7747774028 | Intro Call Click | ONE_PER_CLICK | true | **true** (0 lifetime) |

**Oddity worth flagging to Jacob:** the five Google-hosted local actions (`Local actions - Website
visits`, `- Other engagements`, `- Menu views`, `- Directions`, `Clicks to call`) carry
`PrimaryForGoal = true` but `IncludeInConversions = false`. They have **never** appeared in the
`Conversions` column on any day in the account's history, yet they contribute 349 lifetime
"All conversions" — 213 of them from `Local actions - Other engagements` alone. Any report built on
"All conversions" is substantially Google-hosted map/profile noise.

`Intro Call Click` (7747774028) is **ONE_PER_CLICK, primary, include-in-conversions TRUE**. Per the
Sept 7 note in CLAUDE.md it was supposed to be set Secondary. It is not. It is currently a bidding
target with zero recorded conversions.

---

## 2. Full history by conversion action

Files:
- `ads-conversions-by-action-daily.csv` — 589 rows, every campaign × action × day, 2025-06-02 → 2026-09-08
- `ads-conversions-by-action-monthly.csv` — 89 rows, monthly rollup of the same
- `ads-cpa-like-for-like-monthly.csv` — cost joined to conversions with the regime labelled

Metrics carried on every row: `Conversions` (click-date, primary-only), `Conversions (by conv.
time)`, `All conversions` (click-date, all actions), `All conversions (by conv. time)`, the three
value columns, view-through and cross-device.

Monthly rollups were **derived from the daily rows and then verified cell-by-cell against an
independent monthly `data_query`**; every checked cell matched exactly (2025|07, 2025|08, 2026|06,
2026|07, 2026|08). The independent monthly query returned 91 rows to the derived 89; the two extras
are all-zero rows (2026|06 Leads-Search-1 `Begin checkout`, and one 2025|09 row) that carry no data.

**Data coverage.** Nothing exists before **2025-06-02**. The account was **dark from 2025-09-19 to
2026-04-26** — zero impressions, zero cost, no conversion rows in eight months. Any "year over year"
framing that spans that gap is comparing two disjoint bursts of activity, not a continuous account.

---

## 3. THE FORENSIC ANSWER — why 18 vs 66 in July 2026, and 70 vs 69 in July 2025

### The four-cell test that settles it

For Leads-Search-1, action `7152843979 "Begin checkout (Page load .../schedule-an-appointment)"`:

| | July **2025** | July **2026** |
|---|---|---|
| Conversions (click date) | 70 | **18** |
| Conversions (by conv. time) | 69 | **18** |
| All conversions (click date) | 70 | **67** |
| All conversions (by conv. time) | 69 | **66** |

This immediately **eliminates candidate (b), click-time vs conversion-time**. The two time bases
agree with each other in both years (70/69 and 18/18, 67/66). The gap is entirely on the other axis:
`Conversions` vs `All conversions`.

It also **eliminates candidate (d), "the action stopped firing"**. All conversions ran 67 in July
2026 versus 70 in July 2025 — the action fired essentially as often as ever. And it **eliminates
candidate (c), a counting-setting change**: `ConversionActionCountingType` is still MANY_PER_CLICK,
and a many→one change would have cut *both* columns, not one.

That leaves **candidate (a), and the daily data confirms it to the day.**

### The exact date: 2026-07-12

`Conversions` counts only actions whose `include_in_conversions_metric` is true, and Google applies
that flag **from the moment it is changed, forward** — historical rows keep their original
treatment. So the flag flip is visible as a hard boundary in the daily series.

Leads-Search-1, `Begin checkout`, daily `Conversions`:
`Jul 3 = 1, Jul 5 = 1, Jul 7 = 5, Jul 8 = 2, Jul 9 = 2, Jul 10 = 1, Jul 11 = 6` → **sum exactly 18**,
then **0 on every single day from Jul 13 to Sep 8** while All conversions keeps running.

Leads-Search-1, `PNH2 (web) schedule_appointment`, the mirror image:
`0` in `Conversions` on Jul 3–11 (while All conversions ran 1, 1, 4, 2, 2, 1, 6), then
`Jul 13 = 1, Jul 14 = 2.02, Jul 18 = 3, Jul 19 = 1, Jul 20 = 1, Jul 21 = 1.98, Jul 24 = 1,
Jul 25 = 5, Jul 27 = 2, Jul 28 = 1, Jul 29 = 6, Jul 30 = 2` → **sum exactly 27**, the reported
July figure.

The same boundary appears independently in the PNHdefense campaign (`Begin checkout` counted
through Jul 9, excluded from Jul 14; `schedule_appointment` excluded through Jul 12, counted from
Jul 14). Two campaigns, one date.

> **The primary conversion action was switched on or about 2026-07-12.** 2026-07-12 itself recorded
> no conversions for either action, so the boundary is exact to within one idle day. There is one
> minor anomaly: on 2026-07-10 `Begin checkout` shows 1 counted against 2 all on a conversion-date
> basis. It does not move the totals.

### Two corrections to CLAUDE.md §4

1. **The date is wrong.** CLAUDE.md says the old action "was demoted ~Aug 1". It was demoted
   **2026-07-12**, three weeks earlier.
2. **"Raw July totals are roughly double-counted" is wrong for the `Conversions` column.** The
   handoff was clean — **there is no day on which both actions were counted**. July 2026's
   Leads-Search-1 `Conversions` total of 46 is a *spliced* month (18 `Begin checkout` from Jul 1–11
   + 27 `schedule_appointment` from Jul 13–31 + 1 `PNH2 purchase`), not an inflated one.
   Double-counting **is** real in **All conversions** — both actions fire on the same
   `/schedule-an-appointment` page load, so July 2026 All conversions carries 67 + 44 = 111 for one
   underlying behaviour. Reports built on All conversions are the ones that are double-counted.

### The 2025 side, for completeness

The same mechanism is visible a year earlier, in the *other* direction. The three page-view actions
were dropped from **Campaign #1** (the Performance Max campaign) on **2025-07-07/08** —
`meet-dr-haley` shows a partial day on 2025-07-07 then zero; `whypnh` shows partial days
2025-07-07/08 then zero from 2025-07-09. They were **not** dropped from Leads-Search-1, which kept
counting them through 2025-08-26. That is a campaign-level conversion-goal change on the PMax
campaign, not an account-level one. By the time spend resumed in April 2026 they were secondary
everywhere; the demotion itself falls inside the dark period and **cannot be dated** from
performance data.

### Verdict on the quoted comparison

**Unsound, and the corrected version reverses the sign.** The $34.79 numerator is a full month of
spend; the denominator is 11 days of conversions. Three defensible readings of July 2026, all far
below $34.79:

- matched window (Jul 1–11 spend $113.80 ÷ 18) = **$6.32**
- full month ÷ the action's full-month All conversions (626.29 ÷ 67) = **$9.35**
- full month ÷ the spliced `Conversions` total (626.29 ÷ 46) = **$13.61**

---

## 4. Composition — how much of each era's "conversions" were bio-page and /whypnh views

File: `ads-conversions-composition.csv` (per month, per campaign, counted and all-conversions
splits across scheduling / doctor-bio / whypnh / Google-hosted local / purchase / call+lead-form /
intro-call-click).

**Leads-Search-1**

| month | counted conversions | scheduling | bio pages | /whypnh | **page-view share** |
|---|---|---|---|---|---|
| 2025-07 | 108 | 70 (64.8%) | 36 (33.3%) | 2 (1.9%) | **35.2%** |
| 2025-08 | 109 | 54 (49.5%) | 53 (48.6%) | 2 (1.8%) | **50.5%** |
| 2026-04 | 16 | 16 (100%) | 0 | 0 | **0%** |
| 2026-05 | 20 | 20 (100%) | 0 | 0 | **0%** |
| 2026-07 | 46 | 45 (97.8%) | 0 | 0 | **0%** |
| 2026-08 | 22 | 22 (100%) | 0 | 0 | **0%** |
| 2026-09 (to 8th) | 1 | 1 (100%) | 0 | 0 | **0%** |

Jul+Aug 2025 combined: **217 counted conversions, of which 89 (41.0%) were bio-page or /whypnh views.**

**Campaign #1 (Performance Max)** — far worse:

| month | counted | scheduling | bio | /whypnh | page-view share |
|---|---|---|---|---|---|
| 2025-06 | 173 | 55 (31.8%) | 34 (19.7%) | 84 (48.6%) | **68.2%** |
| 2025-07 | 1,682 | 622 (37.0%) | 54 (3.2%) | 1,006 (59.8%) | **63.0%** |

Account-wide across the 2025 era (Jun–Sep 2025, all campaigns): **2,072 counted conversions, of
which 1,271 — 61.3% — were doctor-bio or /whypnh page views.** In the 2026 era the figure is
**0%**. Any 2025 conversion count is majority page-view noise; any 2026 count is not.

---

## 5. The corrected, like-for-like CPA series

The only action that fires continuously across both eras is `7152843979 Begin checkout` (page load
of `/schedule-an-appointment`). Its **All conversions** column is regime-independent — it is
unaffected by every primary/secondary flip in the account's history. That is the correct spine.

**Leads-Search-1, cost ÷ `Begin checkout` All conversions:**

| month | cost | BC all (click date) | **CPA** | BC all (conv date) | CPA |
|---|---|---|---|---|---|
| 2025-07 | $774.63 | 70 | **$11.07** | 69 | $11.23 |
| 2025-08 | $659.60 | 54 | **$12.21** | 50 | $13.19 |
| 2025-09 → 2026-03 | — | account dark | — | — | — |
| 2026-04 | $186.22 | 16 | **$11.64** | 12 | $15.52 |
| 2026-05 | $190.24 | 20 | **$9.51** | 24 | $7.93 |
| 2026-06 | $24.06 | 0 | n/a (4 clicks) | 0 | n/a |
| 2026-07 | $626.29 | 67 | **$9.35** | 66 | $9.49 |
| 2026-08 | $651.84 | 28 | **$23.28** | 29 | $22.48 |
| 2026-09 (1–8) | $102.47 | 4 | **$25.62** | 4 | $25.62 |

**This series can be constructed, and it says something quite different from the quoted comparison.**
CPA was stable and slightly improving from July 2025 through July 2026 ($11.07 → $9.35). The real
deterioration is **August–September 2026** ($23.28, $25.62), which is exactly when the daily budget
was cut to $17 → $12 → $10. It is a budget story, not a July story.

**Caveat that must travel with this series.** `Begin checkout` is MANY_PER_CLICK — it counts repeat
page loads, not people. Where both actions ran side by side, `Begin checkout` all-conversions
exceeded the ONE_PER_CLICK `schedule_appointment` by **1.44×** (Leads-Search-1 Jul+Aug 2026: 95 vs
66; July alone 67 vs 44 = 1.52×; August 28 vs 22 = 1.27×; PNHdefense June 34 vs 18 = 1.89×). So the
series above is a page-load CPA, roughly 1.4× cheaper-looking than a per-click-deduplicated CPA
would be. Applying that 1.44 factor to translate 2025 into `schedule_appointment`-equivalent units:

- Jul+Aug 2025: $1,434.24 ÷ (124 / 1.44 ≈ 86) ≈ **$16.7**
- Jul+Aug 2026: $1,278.13 ÷ 66 = **$19.4**

≈ **16% worse year over year, not 3× worse.** Treat the 1.44 as an estimate — it rests on three
months of overlap in 2026 and is assumed to have held in 2025, which cannot be verified.

**None of these series measure bookings.** Every one of them counts a scheduling-page load. Acuity
remains the only booking truth (CLAUDE.md §5). The `PNH2 (web) purchase` action, which does track
real bookings, has **3.21 lifetime conversions across the entire account** — too thin to build any
CPA on.

---

## 6. Query recipes that worked (for whoever follows without Supermetrics)

```
# Conversion action DEFINITIONS incl. primary-for-goal — report type "ConversionAction"
# NOTE: the Conversions and ConversionValue metrics are NOT available on this report type;
#       only EstimatedTotalConversions / EstimatedTotalConversionValue are.
data_query(ds_id="AW", ds_accounts="7473953248", date_range_type="custom",
  start_date="2024-01-01", end_date="2026-09-08",
  fields="ConversionTrackerId,ConversionTypeName,ConversionCategory,ConversionActionStatus,"
         "ConversionActionCountingType,PrimaryForGoal,IncludeInConversionsMetric,AttributionModel,"
         "EstimatedTotalConversions,EstimatedTotalConversionValue")

# The four-cell forensic pull (this is the one that answers counting questions)
data_query(ds_id="AW", ds_accounts="7473953248", date_range_type="custom",
  start_date="2024-01-01", end_date="2026-09-08", timezone="America/Chicago",
  fields="Date,Campaignname,CampaignID,Campaignstatus,ConversionTrackerId,ConversionTypeName,"
         "ConversionCategory,ExternalConversionSource,Conversions,conversionsByConversionDate,"
         "EstimatedTotalConversions,allConversionsByConversionDate,ConversionValue,"
         "EstimatedTotalConversionValue,allConversionsValueByConversionDate,Viewthroughconversions,"
         "EstimatedCrossDeviceConversions", max_rows=100000)
```

Gotchas hit:
- `ExternalConversionSource` and `ConversionActionStatus` cannot be requested together — no common
  report type. Split into two queries.
- `PrimaryForGoal`, `ConversionActionStatus`, `ConversionActionCountingType`,
  `IncludeInConversionsMetric` and `AttributionModel` live **only** on report type `ConversionAction`,
  which carries no per-campaign or per-date breakdown and no `Conversions` metric.
- `conversionsByConversionDate` / `allConversionsByConversionDate` are **not** available on the
  `ConversionAction` report type.

---

## 7. GAPS AND LIMITS — read before quoting anything above

1. **No change log was obtainable.** Every demotion/promotion date in this document is *inferred*
   from the `Conversions` vs `All conversions` divergence in daily data, not read from an audit
   trail. Google Ads' `change_event` resource covers only the trailing ~30 days and does not log
   conversion-action setting edits at all, so 2026-07-12 and 2025-07-07/08 cannot be independently
   confirmed. The inference is strong (exact totals reconcile, two campaigns agree on the same
   boundary) but it is an inference.
2. **`PrimaryForGoal` / `IncludeInConversionsMetric` are current-state only.** The API exposes no
   historical version of these fields. There is no way to ask "what was primary in August 2025".
3. **The page-view demotion cannot be dated.** It happened somewhere inside the 2025-09-19 →
   2026-04-26 dark period. All that can be said is: primary in Aug 2025, secondary by Apr 2026.
4. **The 1.44× many-per-click factor is an estimate**, derived from three months of 2026 overlap and
   assumed stable back into 2025. It is the weakest link in the year-over-year translation.
5. **Two all-zero monthly rows** present in the direct monthly query are absent from the
   daily-derived monthly CSV. They carry no data.
6. **No pre-2025-06 history exists** in this data source; whether the account ran earlier is unknown.
7. **June 2026 Leads-Search-1 is unusable** — 4 clicks, $24.06, one 0.02 fractional conversion.
   Excluded from every rate calculation above.
8. **A residual divergence in Campaign #1 (PMax), July 2025, is only partly explained.** On a
   click-date basis `whypnh` shows 149.02 counted vs 155.02 all on Jul 1, widening to 10 vs 35 by
   Jul 7. The conversion-date basis resolves cleanly (equal through Jul 6, diverging from Jul 7),
   which is consistent with a Jul 7 goal change plus normal conversion lag — but PMax also mixes
   engaged-view and cross-environment credit into All conversions, and that portion was not
   separately isolated. It does not affect Leads-Search-1 or any conclusion above.
9. **Nothing here measures bookings.** See §5.
