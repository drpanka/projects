# NOTES — final audit of the archive

**Author: the final-audit pass, 2026-09-08/09, the last hours of the Supermetrics subscription.
I own this file and `README.md`. I appended to no other agent's `NOTES-*.md`. No Supermetrics
quota was spent — every check below was run against files already on disk.**

Scope: (1) verify every file independently, (2) reconcile totals across files, (3) read every
`NOTES-*.md` and every report written today and check they agree on numbers, (4) rewrite the
archive index, (5) state what is now permanently unobtainable.

The point of this pass is narrow. Two people have already drawn a confident wrong conclusion from
this dataset. A third will come from **two archive documents disagreeing with each other**, because
whoever finds the disagreement will pick one and not know they picked. Section 3 lists every
disagreement I could find, says which side is right, and says whether the affected conclusion
survives.

---

## 1. File verification — independent, not a re-read of §5 of `NOTES-last-sweep.md`

**189 files, 24 MB: 97 CSV, 47 JSON, 22 Markdown, 21 Python, 2 field-list `.txt`.**
(The last-sweep pass verified 92/46/13/18/2 at ~23:00 UTC; nine agents' outputs landed after it.)

Method: every `.csv` parsed with `csv.reader`, checked for a header row, ≥1 data row, consistent
column count on every row, absence of the substrings `error` / `exception` / `traceback` / `quota` /
`rate limit` / `not authorized` / `"detail"` in the first 3 KB, and a row count not sitting on
100 / 200 / 500 / 1000 / 2000 / 5000 / 10000. Every `.json` parsed with `json.load` and inspected
for an error payload.

**Result: nothing empty, nothing header-only, nothing truncated at a round number, nothing carrying
an error string where data should be, no JSON with `success:false` or a populated `error` field.**

Three things that look like defects and are not:

- **`proposed-lab-testing-adgroup.csv` has 28 ragged rows.** It opens with an eight-line `#` comment
  preamble before the header. Deliberate; the file is a proposal, not a query result. Strip lines
  beginning `#` before parsing.
- **`gmb-monthly-media-and-reviews.csv` has 6 rows and `gmb-review-totals-lifetime.csv` has 1.**
  Correct at that size — the underlying reports have almost nothing in them, which is itself the
  finding.
- **`ads-recommendations.json` is 604 bytes.** Google returned exactly four live recommendations
  (one `MAXIMIZE_CONVERSIONS_OPT_IN`, three `KEYWORD`). Not a truncated pull.

One correction to `NOTES-last-sweep.md` §5: **not all `raw-*.json` are single-line.** The five
hand-assembled ones carrying a `requested_field_ids` key are pretty-printed
(`raw-ads-account-monthly.json` = 13 lines, `raw-gmb-reviews.json` = 75). The rest, which are
unmodified tool responses, are single-line with no trailing newline as described. Either shape is
fine; `wc -l` is simply not a health check for this directory.

---

## 2. Cross-file reconciliation

Every check states the direction and rough size of the discrepancy that **should** exist, so a
future reader can tell a normal gap from a broken file.

### 2a. Google Ads internal — exact where it should be exact

| Check | Expected | Found |
|---|---|---|
| `ads-campaign-monthly` vs `ads-account-monthly`, cost + clicks, every month | identical | **identical, all 10 months** |
| `ads-keywords-monthly` vs `ads-campaign-monthly`, cost per campaign-month | identical for Search campaigns; **zero** for PMax `Campaign #1` (no keywords exist) | **100.0% on every Search campaign-month; $910.92 of `Campaign #1` spend has no keyword rows, as it must** |
| `ads-keywords-quality-score-monthly` vs `ads-keywords-monthly` | identical (same grain) | **identical to the cent, all 11 campaign-months** |
| `ads-device-monthly`, `ads-network-monthly`, `ads-hour-dayofweek-monthly` vs campaign total | identical (exhaustive partitions) | **$4,284.33 = $4,284.33 on all three** |
| `master-monthly-channel-table` vs `ads-account-monthly` and `gmb-monthly-metrics` | identical | **zero mismatches on cost, clicks, and all six GBP metrics** |

### 2b. Google Ads partitions that legitimately lose rows

| Check | Expected | Found | Verdict |
|---|---|---|---|
| `ads-geo-monthly` vs campaign total | slightly low — clicks with no resolvable location | $4,250.43 / $4,284.33 = **99.2%** | normal |
| `ads-geo-userlocation-monthly` | same | **99.3%** | normal |
| `ads-age-monthly` / `ads-gender-monthly` vs campaign total | low — demographics are Search-only | $3,381.69 vs $3,927.06 = **86.1%** | **explained: the missing $553.66 is `Campaign #1` (PMax/Display), which these reports do not cover at all. Within Search campaigns the match is ~100%. Both files carry an explicit `Undetermined` bucket ($992.83 age, $988.01 gender) — that bucket is present, not dropped.** Do not compute a demographic share of *account* spend from these files. |

### 2c. Search terms — the biggest legitimate gap in the archive, and it is large

Google suppresses low-volume search terms. The expected direction is that search-term spend is
**lower** than keyword spend. The expected size, for a small account with a long tail, is 20–40%
hidden. **Here it is 51%.**

| Month | Search-campaign spend | Visible as search terms | Coverage |
|---|---|---|---|
| 2025-07 | $774.63 | $401.58 | 51.8% |
| 2025-08 | $659.60 | $316.22 | 47.9% |
| 2026-07 | $673.33 | $324.38 | 48.2% |
| 2026-08 | $651.84 | $322.14 | 49.4% |
| 2026-09 (1–8) | $102.47 | $51.73 | 50.5% |
| **All time** | **$3,373.41** | **$1,641.63** | **48.7%** |

Stable at ~49% across fourteen months, which is what a real suppression floor looks like rather than
a broken pull. `NOTES-ads-search-terms.md` §4 already says the true size of each search-term leak is
"plausibly about double what is listed"; **that doubling is not optional, it is the correct
adjustment, and it applies to `pollution-quantified.csv` and every negative-keyword sizing in the
archive.** Any statement of the form "$X of spend is wasted on Y queries" derived from a search-term
file is a *lower bound* at roughly half the true figure.

### 2d. GA4 sessions vs Google Ads clicks — reconciles well

| Month | GA4 `google / cpc` sessions | Ads clicks | Ratio |
|---|---|---|---|
| 2025-06 | 290 | 313 | 0.93 |
| 2025-07 | 2,970 | 3,363 | 0.88 |
| 2025-08 | 240 | 266 | 0.92 |
| 2026-04 | 60 | 68 | 0.88 |
| 2026-07 | 350 | 339 | 1.03 |
| 2026-08 | 291 | 315 | 0.92 |

Expected: sessions slightly **below** clicks (bounced clicks that never fire the tag, consent
refusals, invalid clicks removed on the Ads side but never counted on the GA4 side), typically
5–15% low. **Observed 0.88–1.03. Both systems are seeing the same traffic.** Ratios slightly above
1.0 in 2026-05 to 2026-07 are the same clicks re-sessionised across a 30-minute boundary; that is
normal and not evidence of untagged paid traffic.

This is worth stating positively because it is load-bearing: **the two systems agree completely
about traffic and completely disagree about what happened afterwards.** The measurement failure in
this account is downstream of the click, not at the click.

### 2e. GA4 internal

`ga4-purchases-detail.csv` **stacks two grains in one file** (`detail_grain` column):
`date x sessionSourceMedium only` for 2023-12-18 → 2026-05-13 (218 rows) and
`date x source x pagePath x transactionId` for 2026-05-18 → 2026-09-07 (121 rows). The date ranges
do not overlap, so the file total (429 events, $51,890) is safe — **but any breakdown by source or
page must filter on `detail_grain` first**, or it silently mixes two different row shapes. This is
the one file in the archive where a naive `groupby` gives a wrong answer without warning.

### 2f. Impression-share floor — the structure verified, and the brief has it backwards

`ads-impression-share-floor-analysis.csv`, 160 daily rows, 2025-07-08 → 2026-09-07. 61 rows (38%)
report `SearchImpressionShare` at exactly 0.0999.

The task brief states the floor is proved because "the three shares sum to exactly 1.0000 on those
days." **That is the opposite of what the data shows, and it matters.** The correct structure:

- On the **99 non-floored** rows the three shares sum to **1.0000** (89 exactly; 10 at 0.9999/1.0001
  from rounding). That is the partition behaving.
- On the **61 floored** rows only 6 sum to 1.0000; the other **55 sum to between 1.0012 and 1.0838**.
  The partition *overshoots 100%*, which is impossible for an exhaustive partition — and that
  overshoot is precisely the proof that the reported 0.0999 is inflated.

Solving for the residual gives true impression share as low as **1.61%** against a reported 9.99%
(2026-09-02), an overstatement of up to 8.4 percentage points. `NOTES-ads-campaign-history.md` §5
states this correctly ("106 of 160 rows sum to 1.000, and 54 rows overshoot"; my count is 105 and
55, a one-row difference from where the rounding tolerance is set — immaterial). **Quote the notes,
not the brief.** The conclusion — 0.0999 is a floor, not a measurement — is not merely intact, it is
better supported than the brief's version of the evidence.

---

## 3. Contradictions between documents

Four found. All four are recorded here with the resolution; **none of them reverses a headline
conclusion**, but two of them are shared stale premises sitting underneath live recommendations.

### 3.1 — `ga4-self-referral-pollution.csv` in July/August 2026. Material; the notes disagree flatly.

`NOTES-verify-august.md` §5 falsifies the hypothesis "operator tag-testing inflated July" with the
evidence: *"`ga4-self-referral-pollution.csv` has zero rows in 2026-07 / 08 / 09."*

**That is false.** The file has **7 rows in 2026-07 and 6 rows in 2026-08**, all
`ads.google.com / referral`, including **7 `schedule_appointment` events in July and 13 in August**.
`NOTES-verify-pollution.md` §4 states the same figures correctly ("contributed 13 conversions in
August against 8 in July").

**Resolution: `NOTES-verify-pollution.md` is right; that line of `NOTES-verify-august.md` is wrong.**

**Does the August conclusion survive? Yes, and I checked rather than assumed.** The pollution lands
in the *non-paid* control group (`ads.google.com` is a referral, not `google / cpc`), so the risk was
that it inflated the control. Recomputed from `ga4-events-by-source-monthly.csv` with the two
polluted sources removed:

| | July 2026 | August 2026 |
|---|---|---|
| Paid `schedule_appointment` rate | 17.4% | **7.8%** |
| Non-paid rate, as reported | 16.4% | 21.7% |
| **Non-paid rate, pollution removed** | **16.1%** | **20.5%** |

Non-paid still rises while paid halves. The argument holds on clean data. And because the pollution
was *larger* in August than July, removing it widens the July→August gap — it works against the
halving, exactly as `NOTES-verify-pollution.md` §4 concluded. **Fix the sentence, keep the finding.**

### 3.2 — The daily budget is $15, not $10. Six documents say $10.

`campaign-settings-22767146837.json` records `budget_amount: 15`, `budget_type: DAILY`,
budget id `14735867458`, snapshotted 2026-09-08. `ads-change-history.csv` shows the last change in
the account is `CAMPAIGN_BUDGET → amountMicros UPDATE` by `pankanaturalhealth@gmail.com` at
**2026-09-07 14:10:06** — eighteen minutes after the 1:52 pm snapshot that `CLAUDE.md` was built
from. `CLAUDE.md` was correct when written; Jacob raised the budget straight afterwards.

- **Correct ($15):** `NOTES-ads-creative-settings.md` §4, `NOTES-ads-keywords.md`.
- **Stale ($10):** `NOTES-gbp-metrics.md`, `NOTES-verify-august.md`, `NOTES-verify-lab-gap.md`
  (twice, including its verdict line), `reports/august-2026-conversion-drop-diagnosis.md` (twice).

**Resolution: $15.00/day as of 2026-09-07 14:10 CDT.** Open thread #1 in `CLAUDE.md` — "$10/day and
falling" — has been partially acted on and should not be re-raised in that form.

Neither dependent conclusion flips. `NOTES-verify-lab-gap.md`'s verdict ("do not launch a separate
Functional Lab Testing ad group at $10/day") holds at $15/day for the same reason — its own Tier 2
threshold is $25/day, which is still not met. `reports/august-2026-conversion-drop-diagnosis.md`'s
"$2/day is roughly a fifth of the budget" becomes **a seventh**, which weakens that sentence without
touching the diagnosis. **But both are now arguing from a number that is 50% wrong, and anyone
re-running the arithmetic will get a different answer than the document states.**

### 3.3 — "Lifetime CPA was far better in 2025 than in 2026" restates the debunked comparison.

`NOTES-ads-creative-settings.md` §4 leads with that sentence and cites Jul 2025 $7.17 / Aug 2025
$6.05 vs Jul 2026 $13.61 / Aug 2026 $29.63. Those are the `as_reported_CPA_DISTORTED` column of
`ads-cpa-like-for-like-monthly.csv` — the exact figures the archive exists to invalidate.

To its credit the entry carries a caveat and ends "Do not quote these across the boundary." **But
the caveat says the true gap is "smaller than it looks," and that is still wrong: on a like-for-like
basis the gap does not shrink, it reverses.** July 2026 at **$9.35** beats July 2025 at **$11.07**
and August 2025 at **$12.21**. This is confirmed identically in `ads-cpa-like-for-like-monthly.csv`,
`DATA-QUALITY.md`, `NOTES-ads-conversions.md` §7, `master-channel-summary.md`,
`NOTES-cross-source-bookings.md` §5, `NOTES-verify-dead-inventory.md` and
`reports/leads-search-1-final-data-review-2026-09-08.md` — seven documents against one.

**Resolution: the like-for-like series is $11.07 / $12.21 / $9.35 / $23.28 / $25.62. July 2026 was
the account's best month. Read `NOTES-ads-creative-settings.md` §4 as a caution about the raw
ad-level numbers, never as a finding about CPA.** This is the single most dangerous line in the
archive, because it is the one place a reader can find the original wrong conclusion restated inside
a document that is otherwise correct.

### 3.4 — `CLAUDE.md` numbers that the archive supersedes

Not contradictions between archive documents, but between the archive and the project reference the
next reader will open first. Recorded so the archive wins where it should:

| `CLAUDE.md` says | Archive says | Source |
|---|---|---|
| 451 campaign negatives | **466** on Leads-Search-1 (453 phrase, 11 exact, 2 broad); 506 rows in the file across all campaigns | `campaign-negatives.csv` |
| GA4 purchases Jul 1 – Sep 3: **66**, `(not set)` = 34 | **71 events / 67 distinct transaction IDs**, `(not set)` = **39**. Revenue matches exactly at **$7,753** and every other source bucket matches exactly | `ga4-purchases-detail.csv`, grain `date x source x pagePath x transactionId` |
| Budget $10/day | **$15/day** | see §3.2 |
| `Intro Call Click` — "confirm it is set Secondary" | It is **Primary**, `include_in_conversions_metric = TRUE`, 0 lifetime conversions. It is a live bidding target | `ads-conversion-actions.csv` (also caught in `NOTES-ads-conversions.md` §2) |
| Open thread #4: promote `PNH2 (web) purchase` to primary | Already **Primary** and included in the conversions metric since ~2026-06-26 | `ads-conversion-actions.csv` |

The revenue match at $7,753 with a 5-event count difference tells you what happened: the extra five
are `(not set)` rows at $0.00 — additional zero-value intro-call fires, consistent with the archive's
own finding that one Acuity booking can emit up to three `purchase` events.

### 3.5 — Things I checked that turned out NOT to be contradictions

Recorded so nobody re-opens them.

- **"Dark seven months" vs "243 days."** `NOTES-ads-creative-settings.md` says zero impressions
  2025-09-01 → 2026-03-31; `NOTES-cross-source-bookings.md` says no impressions between 2025-08-27
  and 2026-04-27. Both true. The last serving day was **2025-08-27** and the next was **2026-04-27**
  — a 243-day gap containing seven whole calendar months. Different grains, same fact.
- **"~65 keywords still reporting Enabled" vs "34."** `DATA-QUALITY.md` and `NOTES-ads-keywords.md`
  correct this to 34; `README.md` caveat 5 and the task brief carried 65. Verified in
  `ads-keywords-alltime.csv`: `AdgroupID 183759893484` has **34 rows, all `removed`/`enabled`**,
  covering **27 distinct keyword texts**. The 65 was a count of rows in
  `ads-keywords-monthly.csv` (one per keyword-month), not of keywords. **34 is right.**
- **`$1,434.23` vs `$1,434.24`** for Jul+Aug 2025 spend — one cent, floating-point rounding.
- **`campaign-keywords.csv` vs `ads-keywords-current-inventory.csv`** — 114 Leads-Search-1 keywords
  in both, identical sets. The column is `MatchType` in one file and `Matchtype` in the other, and
  the values are cased differently (`PHRASE` vs `Phrase`). A naive join returns zero matches. Not a
  data defect; a join hazard.
- **Purchase-overcount factor (~45%)** is used consistently in six documents, and
  `NOTES-verify-gbp-opportunity.md` §3a applies it correctly (41% raw ÷ 1.45 = 28%) — the divisor
  hits only the numerator, which is right, because the denominator is click events and those are
  not overcounted.
- **Ad schedule = 22 rows; 10 location targets; mobile −15%.** All three match `CLAUDE.md` exactly
  (`campaign-adschedule-and-targeting.csv`: 22 `ad_schedule` rows, 9 geo-target constants + 1
  custom radius for Leads-Search-1, `bid_adjustment_device MOBILE 0.85`).
- **Off-schedule serving.** Since the schedule was created on 2026-08-17: **14 impressions, 2
  clicks, $5.11**, all of it on Mondays, and the Monday-only and all-days slices are the same rows.
  Zero since. `ads-offschedule-check.csv` confirms the anomaly is closed exactly as stated.
- **GBP lifetime totals.** 10,767 views / 1,768 actions / 711 website clicks / 981 direction
  requests / 76 calls / **0 bookings**, and the monthly and daily files agree to the unit across all
  550 days. The duplicate listing `10418367222074184209` returns `NO_DATA` — **not zero** — for
  every one of its 19 months.

---

## 4. A structural gap nobody has flagged: the Sept 7 bid modifiers are not in this archive

`CLAUDE.md`'s reconciliation header records that on 2026-09-07 all 22 ad-schedule rows were given
per-row bid modifiers (Mon–Thu +15/−20/−10/+15, Fri −30/−35/−30/−10, Sat +10, Sun −20), six cities
were set to −30% and three to +10%.

**Those values are not recoverable from this archive.**

- `campaign-adschedule-and-targeting.csv` lists all 22 schedule rows and all 10 location targets but
  its `Detail` column is **empty for every schedule row**, and carries only the resource name for
  location rows. No bid modifier anywhere.
- `campaign-settings-22767146837.json` contains no per-criterion bid modifier values.
- `campaign-adschedule-bid-modifiers-history.csv` **does** carry modifiers with values — but only
  from two timestamps, **2026-07-17 17:55:59 and 2026-08-17 16:54:42**. Those are the *original*
  modifiers, superseded on Sept 7.
- `ads-change-history.csv` records that criteria changed on Sept 7 (`AD_GROUP_CRITERION →
  cpcBidMicros`, `CAMPAIGN_CRITERION` rows) but the change-history API returns changed *field
  names*, never values.

**Consequence:** if the current schedule and city modifiers are ever lost from the live account,
this archive cannot restore them. `CLAUDE.md`'s prose is the only record. That is worth a screenshot
of the Google Ads UI while access remains — it costs nothing and the archive cannot be re-pulled.

The same limit already bit the August diagnosis: `NOTES-verify-august.md` §4 correctly flags the
value-free change history as "the weakest link in the causal chain." It is a general property of
this archive, not a one-off.

---

## 5. What is now genuinely unobtainable

Confirmed against the whole archive; supersedes nothing, consolidates everything.

**Permanently gone, no route to recovery:**

1. **Google Business Profile before 2025-03-08.** The connector refuses earlier dates
   ("Earliest supported historical start date for Google My Business is 2025-03-08"). The clinic's
   first 6.5 years on Google were already unrecoverable before this archive existed.
2. **The seven dark months, 2025-09 → 2026-03.** Zero delivery is a verified fact, not a reporting
   gap, so there is nothing to recover — but nothing can be learned from them either.
3. **The other 51% of search terms.** Google's low-volume suppression is applied upstream. Half of
   every dollar this account has ever spent is attached to a query nobody will ever see.
4. **True impression share below 10%.** Floored by Google before the API. The floor-corrected
   estimates in `ads-impression-share-floor-analysis.csv` are the best that will ever exist.
5. **Auction Insights.** Never available through this connector. No competitor share data, which
   means the MIMC conquesting in `CLAUDE.md` §1 can never be sized from data.
6. **The link between an ad click and a patient.** Attribution breaks at the Acuity scheduler, and
   under the compliance stance set this week it stays broken by choice. Acuity's own export is the
   only booking truth and it lives outside this archive.
7. **Per-criterion bid modifier values as of Sept 7 2026.** See §4.

**Possibly recoverable, but not from here:**

8. **Paid search before 2025-06.** GA4 records **5,824 `google / cpc` sessions** between 2023-03 and
   2025-03 that Google Ads account `7473953248` has no delivery for. PNH ran paid search from an
   account that is not in this archive — a prior account, an agency account, or one never connected.
   **If Jacob's Google Ads login lists other accounts, that spend, keyword and search-term history
   may still exist in the UI.** It is not reachable from here, and it is the single largest missing
   block of the account's history — roughly two years of it. Already documented in
   `NOTES-cross-source-bookings.md` §4, `DATA-QUALITY.md` §11 and `NOTES-last-sweep.md` §7; now also
   in `README.md`, where a first-time reader will see it.
9. **Acuity's true booking count and appointment mix.** Acuity has no connector here. The export is
   a login away and it settles the one number the whole archive is missing — including the unresolved
   "3.4 intro calls a week vs 3.4–8.3 a month" discrepancy in `NOTES-verify-gbp-opportunity.md` (c),
   which changes a headline GBP scenario from a 40% lift to a 13% one.
10. **Google Trends seasonality.** Free at trends.google.com; never needed a subscription.
11. **Search Console.** No connector in this archive, so there are no queries, impressions or
    positions behind the 7,317 lifetime organic sessions. Still live and still free.

---

## 6. Verdict

The archive holds together. The numbers that matter — spend, clicks, conversions by counting regime,
the like-for-like CPA series, the impression-share floor, the GBP totals, the GA4/Ads traffic
reconciliation — agree across every file that should agree, and the files that disagree do so by the
expected amount in the expected direction. The four contradictions in §3 are corrections to
individual sentences, not to conclusions, and every affected conclusion was re-tested rather than
assumed.

Two of them are worth carrying forward as live corrections rather than footnotes: **the budget is
$15/day, not $10** (§3.2), and **`NOTES-ads-creative-settings.md` §4 contains a restatement of the
debunked CPA comparison** (§3.3). Those two are the ones most likely to seed a third wrong
conclusion, because in both cases a careful reader gets a plausible number from a document that is
otherwise trustworthy.
