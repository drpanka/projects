# NOTES — Google Ads campaign & account performance history (auction diagnostics)

**Agent slug:** `ads-campaign-history`
**Pulled:** 2026-09-08 (final Supermetrics harvest; subscription ends 2026-09-09)
**Source:** Supermetrics MCP, `ds_id="AW"`, `ds_accounts="7473953248"`, `timezone="America/Chicago"`
**Report types used:** `Campaign` (campaign grain), `Customer` (account grain)
**Query window requested:** 2024-01-01 → 2026-09-08. **Actual data returned starts 2025-06-02.**
All queries ran with `settings={"include_zero_impressions": true}`.

---

## Files written

| File | Rows | Grain | Notes |
|---|---|---|---|
| `ads-campaign-daily.csv` | 239 | date × campaign | 53 columns. The most valuable file — pacing and budget-change effects. |
| `ads-campaign-weekly.csv` | 48 | ISO week × campaign | 42 columns, `Yearweekiso` |
| `ads-campaign-monthly.csv` | 15 | month × campaign | 53 columns |
| `ads-account-monthly.csv` | 10 | month, account total | 31 columns, `Customer` report type |
| `ads-campaign-inventory.csv` | 6 | campaign | lifetime totals + start dates + primary status reasons |
| `ads-impression-share-floor-analysis.csv` | 160 | date × campaign | derived; reported vs floor-corrected impression share |
| `raw-ads-campaign-daily.json` etc. | — | — | raw API payloads with `requested_field_ids`, kept for provenance |
| `build_campaign_history.py`, `analyze_is_floor.py`, `analyze_keynumbers.py` | — | — | the scripts that produced and verified the above |

### Verification performed
`build_campaign_history.py` re-aggregates the daily file to month, ISO week and account-month and
compares Impressions / Clicks / Cost / Conversions against the API's own rollups.
**Result: 0 mismatches across all three grains.** Lifetime per-campaign totals in
`ads-campaign-inventory.csv` also reconcile exactly to the sum of daily rows. Column order is mapped
from `requested_field_ids`, not the display-name header row (Supermetrics reorders columns — in the
daily pull `Currencycode` came back at position 8 although it was requested last).

---

## 5. THE 0.0999 QUESTION — ANSWER: IT IS A FLOOR, NOT A MEASUREMENT

**Conclusion, stated plainly: `SearchImpressionShare = 0.0999` is Google's anonymised sentinel for
"less than 10%". It is not a measured quantity. Any narrative built on "impression share fell from
12–15% to just below 10%" is overstating both the level and the precision. The honest statement is
that impression share is *at or below the reporting floor*, and the best available estimate of the
true value is roughly 2–5%, not 10%.**

Five independent lines of evidence, all reproducible from the archived CSVs:

**(a) Nothing is ever below it.** Across 160 daily campaign-rows, 32 weekly, 11 monthly and 8
account-monthly rows spanning four campaigns and fifteen months, the number of observations
strictly below 0.0999 is **zero**. A real measurement of a quantity that ranges over (0,1] does not
have a hard wall at exactly 0.0999 with 38% of daily observations sitting precisely on it. The
next distinct values above it are 0.1001, 0.1003, 0.1044 — i.e. the distribution resumes normally
just above the wall.

**(b) The arithmetic breaks.** Google defines search impression share, budget-lost IS and rank-lost
IS as an exhaustive partition of eligible impressions; they must sum to 1.0. In the daily data,
**106 of 160 rows sum to 1.000, and 54 rows overshoot — every single overshooting row is one where
SIS is reported as exactly 0.0999.** No row ever undershoots. Worked example, 2026-09-02:
`0.0999 + 0.9000 + 0.0839 = 1.0838`. Solving for the residual gives a true impression share of
**1.61%**, not 9.99%. The floor is inflating the reported figure by up to 8.4 percentage points
(median 5.0pp across floored rows).

**(c) There is a matching ceiling.** `SearchBudgetLostImpressionShare` hits exactly **0.9001**
(= 1 − 0.0999) on 30 daily rows and **never exceeds it**. A floor at 0.0999 and a ceiling at 0.9001
are the same anonymisation rule seen from both ends.

**(d) The same constant appears on unrelated surfaces.** `Campaign #1` is Performance Max and
returns `null` for search impression share, yet `SearchImpressionShareRaw` reports 0.0999 for five
of its six active weeks — including the week it served 79,342 impressions. At account level in
July 2026, **`ContentImpressionShare` is also exactly 0.0999** despite no Display campaign having
run. One number recurring across Search, Content and PMax raw is a sentinel, not three coincidences.
Note also that `SearchImpressionShareRaw` is **identical to `SearchImpressionShare` in every
Leads-Search-1 row** — the "raw" variant does not unmask the floor.

**(e) Contrast with a metric Google does *not* floor.** At account level,
`SearchExactMatchImpressionShare` returns genuine sub-1% values: 0.001, 0.0056, 0.0024, 0.0044,
0.0082, 0.0022, 0.001, 0.001. So the API is perfectly capable of expressing values below 10%. The
four headline IS metrics simply are not permitted to. (`SearchTopImpressionShare` shows the same
behaviour at 2dp — 86 rows at exactly 0.10, none between 0 and 0.10; `SearchAbsoluteTopImpressionShare`
piles up on 0.0999 in 100 rows.)

**Practical bottom line.** For Leads-Search-1 since 2026-07-01, **53 of 67 days (79%) report the
floor**. On those days the floor-corrected impression share has a median of **4.25%** and a range of
1.6%–9.99%. Monthly floor-corrected estimates: **Jul 2026 ≈ 6.9%, Aug 2026 ≈ 2.7%, Sep 2026 ≈ 2.4%**
(vs 9.99% reported for all three). The direction of the existing narrative is right — the campaign
is starved — but the magnitude is worse than reported, and the *series* is unusable: three months
all reading "9.99%" are not three equal months, they are 6.9%, 2.7% and 2.4%. Do not plot reported
SIS as a trend line. Use `ads-impression-share-floor-analysis.csv`, which carries the corrected
column, and note the correction is an estimate derived from the other two (also-rounded) percentages.

**Independent corroboration that does not depend on impression share at all:** Google's own
`CampaignPrimaryStatusReasons` for Leads-Search-1 reads **"Budget constrained, Has ads limited by
policy, Unknown"**. That is Google stating the constraint directly. It is a stronger citation for
the budget argument than any impression-share number, and it is in `ads-campaign-inventory.csv`.

---

## Structural findings that were not in CLAUDE.md

**1. There are SIX campaign entities, not four.** `Leads-PMax-Video-1` exists in **three copies**,
all created 2026-07-13, all with zero impressions and zero spend:
`24028056923` (removed), `24032463085` (removed), `24032465476` (paused — the ID in the brief).
The brief's ID is the surviving one. None ever served, so there is no history to lose here.

**2. The account was dark for 243 days.** Leads-Search-1 has no impressions between **2025-08-27 and
2026-04-27**. September 2025 through March 2026 is genuinely zero spend across the whole account —
not a reporting gap. Serving only became continuous again on **2026-07-03**. Earlier 2026 activity
was intermittent (gaps of 8, 17, 11 and 23 days through May–June). This materially changes how
"year over year" should be read: there is no comparable prior September.

**3. `dailybudget` is a current-state field, not history.** It returns **15** for Leads-Search-1 in
*every* month from 2025-07 to 2026-09, and 5 for PNHdefense and 6 for Campaign #1 throughout. Since
CLAUDE.md records the budget as $10/day as of 2026-09-07 (down from $12 on Sep 3, $17 mid-Aug,
$25–29 in July), this column is **not** a record of what the budget was on each day. It appears to
report a stored/most-recent configured value. `ConfiguredBudget` behaves identically. **Historical
budget changes are not recoverable from this archive** — see gaps below.

**4. Lifetime spend, all time:** Leads-Search-1 $3,215.35 · Campaign #1 $910.92 ·
PNHdefense $158.06 · **account total $4,284.33** (23,950 / 100,443 / 363 impressions respectively).

**5. Campaign #1's July 2025 conversion count is not credible.** 1,682 conversions on $553.66 spend
(CPA $0.33, CVR 54.7%) from a Performance Max campaign. This is the double-counting era described in
CLAUDE.md §4 compounded by PMax's own attribution. Treat all pre-2025-08 conversion figures as
unusable for CPA comparison.

---

## Notes on specific fields

- **`Conversions` here is the account's total conversions across all primary actions**, not the
  PNH2-only figure CLAUDE.md §4 uses. That is why my Jul 2026 CPA reads $13.62 where the working
  documents say $20.23 for the overlapping Jul 17–Aug 13 window. Neither is wrong; they count
  different things. Do not mix them in one table.
- **`SearchClickShare`, `EligibleSearchClicks`, `LostSearchClicks` are unreliable.** Search click
  share returns values above 100% (3.0969 for Aug 2026, 15.1461 for PNHdefense Jun 2026) and lost
  search clicks returns negative numbers (−213, −277). Archived for completeness; do not use.
- **`TotalAvailableImpressions` / `LostImpressions` / `LostImpressionsDueToBudget` / `...DueToRank`
  are derived by Supermetrics from the floored percentages**, so they inherit the floor and are not
  an independent measurement. They do not reconcile internally (Aug 2026: 5,534 impressions +
  39,896 lost ≠ 44,324 available). Do not use them to back out true impression share.
- `SearchImpressionShareRaw` == `SearchImpressionShare` in every row. No extra information.
- `CampaignMobileBidModifier` reads **−15%** for Leads-Search-1 across all months, consistent with
  the mobile −15% recorded in CLAUDE.md's Sept 7 reconciliation — again a current-state read, not history.

---

## GAPS — things I could not get, stated explicitly

1. **No data before 2025-06-02.** Queried from 2024-01-01; the API returned nothing earlier. The
   account's history genuinely begins here (Campaign #1 started 2025-06-02).
2. **Historical daily-budget values are NOT in this archive.** The `dailybudget` and
   `ConfiguredBudget` fields return a constant current-state value per campaign. The documented
   budget trajectory ($25–29 July → $17 mid-Aug → $12 Sep 3 → $10 Sep 7) is therefore **not
   recoverable from Supermetrics** and will be lost when the subscription ends unless pulled from
   the Google Ads change history UI directly. This is the single most important gap in my scope.
   The `AccountChanges` report type exists in the AW field list and might carry it, but it is a
   different report type and was outside my assigned pulls — flagging it for whoever has time today.
3. **True impression share below 10% is unrecoverable.** The floor is applied upstream by Google,
   not by Supermetrics, so no field or report type in this data source can return it. My corrected
   column is an *estimate* computed as `1 − budgetLost − rankLost`, and those two inputs are
   themselves rounded to 4dp, so the estimate carries roughly ±0.5pp of slop.
4. **`SearchTopImpressionShare` and `SearchAbsoluteTopImpressionShare` are unavailable at account
   level.** They are not supported by the `Customer` report type (report_types 2,17,30,31 only), so
   `ads-account-monthly.csv` omits them. They are present at campaign grain in the other three files.
   I substituted `ImpressionShare`, `ContentImpressionShare`, `ContentBudgetLostImpressionShare` and
   `ContentRankLostImpressionShare` at account level instead.
5. **September 2026 is a partial month** (1st–8th) and 2026-09-08 is same-day data that may still be
   settling. The 2026-09-08 row has null impression-share fields.
6. **Minor instability observed:** an early monthly pull returned 1,333 impressions for 2026-09 and a
   pull minutes later returned 1,335. Same-day figures move. The archived value is 1,335 and it
   reconciles to the daily file.
7. `AdvertisingChannelSubType` returns empty string for all campaigns — no sub-type is set.
