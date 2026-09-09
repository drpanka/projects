# PNH Supermetrics archive — captured 2026-09-08

The Supermetrics subscription ended 2026-09-09. **This directory cannot be regenerated.**
Everything here was pulled live from Google Ads (account 7473953248), GA4 (property 353828960
"PNH2") and Google Business Profile on 2026-09-08.

**189 files, 24 MB: 97 CSV, 47 JSON, 22 Markdown, 21 Python, 2 field lists.** Independently
verified file by file on 2026-09-09 — see `NOTES-final-audit.md`.

## How to read this archive

- `NOTES-*.md` — the analyst write-up for each area. Read these first; they carry the caveats.
- `*.csv` — the data, with real header rows.
- `raw-*.json` — unprocessed API responses, kept so any derived CSV can be re-checked.
- `build_*.py` / `analyze_*.py` — the scripts that produced the CSVs from the raw JSON.
- `campaign-settings-<id>.json` — full structural snapshot of each campaign (keywords, negatives,
  ad schedule, extensions, targeting) as of 2026-09-08.

**Three files to read before anything else, in this order:**

1. `DATA-QUALITY.md` — the guardrail. Every hazard stated against the file and column it applies
   to, ending with 15 comparisons that are not valid to make with this data at all.
2. `NOTES-final-audit.md` — the independent verification, the cross-file reconciliations with
   their expected error bars, and **the four places where two archive documents disagree**.
3. `master-channel-summary.md` — the one-page narrative, with `master-monthly-channel-table.csv`
   beside it as one row per month across every channel.

## Hard limits discovered during capture

- **Google Business Profile history only reaches back to 2025-03-08.** Supermetrics returns
  "Earliest supported historical start date for Google My Business is 2025-03-08". The clinic's
  first 6.5 years on Google were already unrecoverable before this archive was made.
- **The Google Ads account was dark from 2025-09 through 2026-03** — seven consecutive months of
  zero delivery. Any comparison spanning that gap is comparing two separate campaign lifetimes,
  not a continuous trend. At day grain the gap is 243 days: last impression 2025-08-27, next
  2026-04-27.
- **Google Ads change history returns changed *field names*, never values**, and reaches back only
  to 2026-06-12. What a setting was changed *to* is not in this archive unless a settings snapshot
  happened to catch it.

## Caveats that change conclusions — read before quoting any number

1. **Conversion counting changed mid-history.** Through roughly August 2026 the action
   "Begin checkout (Page load .../schedule-an-appointment)" was primary AND the GA4
   `schedule_appointment` import was primary, so the two double-counted the same page load.
   Page views of the two doctor bio pages and /whypnh were also counted as primary conversions in
   2025. Cross-era conversion or CPA comparisons are invalid without adjustment. See
   `ads-cpa-like-for-like-monthly.csv` and `ads-conversions-composition.csv`.
2. **The tracked conversion is a page load, not a booking.** Acuity is the only booking truth.
3. **GA4 `purchase` overcounts real bookings by roughly 45%** — one Acuity booking can fire up to
   three purchase events. Good as a date-level indicator, bad as a volume count.
4. **Search impression share is frequently reported as exactly 0.0999 / 0.1.** Treat this as at or
   below Google's reporting floor rather than a precise measurement. See
   `ads-impression-share-floor-analysis.csv`.
   *Note on the proof:* on the 99 non-floored daily rows the three shares sum to 1.0000, as an
   exhaustive partition must. On 55 of the 61 floored rows they sum to **more than 1.0000** (up to
   1.0838) — which is impossible, and is exactly what shows the reported 0.0999 is inflated. True
   share runs as low as 1.61% against a reported 9.99%. Anyone who has been told the shares "sum to
   exactly 1.0000 on floored days" has it backwards.
5. **Keywords in the removed ad group "Ad group 1" still report status "Enabled."** They cannot
   serve. Any keyword count that includes them is wrong. Use `ads-keyword-count-by-month.csv`,
   which counts keywords that actually served.
   **Corrected figure: 34, not the ~65 originally circulated.** `ads-keywords-alltime.csv` has 34
   rows under `AdgroupID 183759893484` marked `removed`/`enabled`, covering 27 distinct keyword
   texts. The 65 was a count of keyword-*month* rows in `ads-keywords-monthly.csv`.
6. **tagassistant.google.com and ads.google.com self-referrals pollute GA4 conversion data** —
   these are the operator's own tag tests. See `ga4-self-referral-pollution.csv` and, for the full
   forensic sizing, `NOTES-verify-pollution.md` and `pollution-quantified.csv`.
   **The pollution is small but it is not zero in 2026-07/08:** 7 rows in July and 6 in August, all
   `ads.google.com / referral`, carrying 7 and 13 `schedule_appointment` events respectively. One
   archive document states this file is empty for those months; it is not. Removing the pollution
   does not change any conclusion — see `NOTES-final-audit.md` §3.1.
7. **`pankanaturalhealth.com / referral` in GA4 is NOT junk.** It is the fingerprint of real
   bookings whose attribution was destroyed when the Acuity scheduler opened a new session on its
   own domain. Do not filter it away; it is the only evidence those bookings happened.
8. **GBP search-term counts below roughly 15/month are suppressed by Google and render as 0.**
   In `gmb-*search*` files, 0 means "below threshold", never "none".
9. **Google hides about half of all search terms in this account.** Search-term files carry only
   **48.7% of search-campaign spend**, stable at 47–52% in every month. Every "$X is being wasted
   on Y queries" figure derived from a search-term file is a **lower bound at roughly half the true
   size**, and should be doubled before it is used to size a decision.
10. **Blank Google Ads columns before 2025-06 are not zero spend.** GA4 records **5,824
    `google / cpc` sessions between 2023-03 and 2025-03** that this Ads account has no delivery for.
    PNH ran paid search from an account that is not in this archive. Do not compute a blended
    cost-per-session across that boundary.
11. **`ga4-purchases-detail.csv` stacks two grains in one file.** Filter on the `detail_grain`
    column before any breakdown by source or page: rows are `date x sessionSourceMedium only` for
    2023-12 → 2026-05-13, and `date x source x pagePath x transactionId` for 2026-05-18 → 2026-09-07.
    The date ranges do not overlap, so the file *total* is safe; a naive `groupby` is not.
12. **Demographic files cover Search campaigns only.** `ads-age-monthly.csv` and
    `ads-gender-monthly.csv` sum to 86% of account spend because they exclude PMax `Campaign #1`
    entirely. Within Search campaigns they reconcile. Do not read a demographic share of *account*
    spend from them.
13. **`campaign-keywords.csv` and `ads-keywords-current-inventory.csv` will not join naively.**
    The column is `MatchType` in one and `Matchtype` in the other, and the values are cased
    differently (`PHRASE` vs `Phrase`). Both hold the same 114 Leads-Search-1 keywords.
14. **`gbp actions_bookings` is 0 in every month and every day, and always will be.** Google
    defines that field as bookings made via Reserve with Google only; performance data is not
    available for a plain merchant booking link. A future check that measures a booking link
    through this field will wrongly conclude the work failed. See
    `NOTES-gbp-booking-link-compliance.md`.

## Where this archive supersedes `CLAUDE.md`

`CLAUDE.md` was verified at 1:52 pm CDT on 2026-09-07. The account changed after that.

| `CLAUDE.md` | Verified in this archive | Source |
|---|---|---|
| Daily budget $10 | **$15.00**, raised 2026-09-07 14:10:06 CDT | `campaign-settings-22767146837.json`, `ads-change-history.csv` |
| 451 campaign negatives | **466** on Leads-Search-1 (453 phrase / 11 exact / 2 broad) | `campaign-negatives.csv` |
| GA4 purchases Jul 1 – Sep 3 = 66 | **71 events, 67 transaction IDs** (revenue matches exactly at $7,753; the extra 5 are $0.00 `(not set)` rows) | `ga4-purchases-detail.csv` |
| "Confirm `Intro Call Click` is Secondary" | It is **Primary** and included in the conversions metric — a live bidding target with 0 lifetime conversions | `ads-conversion-actions.csv` |
| Open thread #4: promote `PNH2 (web) purchase` to primary | Already **Primary** since ~2026-06-26 | `ads-conversion-actions.csv` |

Ad schedule (22 rows), location targets (10) and the mobile −15% modifier all match `CLAUDE.md`
exactly. **The Sept 7 per-row schedule and city bid modifier *values* are not in this archive** —
only that criteria changed. `CLAUDE.md`'s prose is the sole record; see `NOTES-final-audit.md` §4.

## File inventory

### Google Ads — spend, auction, structure
`ads-account-monthly.csv` · `ads-campaign-monthly.csv` / `-weekly.csv` / `-daily.csv` ·
`ads-campaign-inventory.csv` · `ads-impression-share-floor-analysis.csv` ·
`ads-change-history.csv` / `.json` · `ads-recommendations.json` ·
`campaign-settings-22767146837.json` (Leads-Search-1, full) and the same for `22625352639`,
`23888858069`, `24032465476` · `campaign-adschedule-and-targeting.csv` ·
`campaign-adschedule-bid-modifiers-history.csv` · `campaign-extensions.csv` ·
`campaign-keywords.csv` · `campaign-negatives.csv`

### Google Ads — conversions
`ads-conversion-actions.csv` · `ads-conversion-action-definitions.json` ·
`ads-conversions-by-action-monthly.csv` / `-daily.csv` · `ads-conversions-composition.csv` ·
`ads-cpa-like-for-like-monthly.csv` *(the five counting regimes — start here for any CPA question)* ·
`ads-call-details.csv`

### Google Ads — keywords and search terms
`ads-keywords-alltime.csv` · `ads-keywords-monthly.csv` · `ads-keywords-current-inventory.csv` ·
`ads-keywords-zero-conversion.csv` · `ads-keyword-count-by-month.csv` ·
`ads-keywords-quality-score-monthly.csv` · `ads-search-terms-alltime.csv` ·
`-incl-zero-cost.csv` · `-monthly.csv` · `-rollup.csv`

### Google Ads — geo, device, time, network, demographics
`ads-geo-alltime.csv` / `-monthly.csv` / `-detail-monthly.csv` ·
`ads-geo-userlocation-alltime.csv` / `-monthly.csv` ·
`ads-geo-locationtarget-alltime.csv` / `-daily.csv` · `ads-device-alltime.csv` / `-monthly.csv` /
`-daily.csv` · `ads-hour-dayofweek-alltime.csv` / `-alltime-by-campaign.csv` / `-monthly.csv` ·
`ads-hour-daily-by-campaign.csv` · `ads-offschedule-check.csv` ·
`ads-network-alltime.csv` / `-monthly.csv` / `-daily.csv` ·
`ads-age-monthly.csv` · `ads-gender-monthly.csv`

### Google Ads — creative
`ads-ad-performance-alltime.csv` / `-monthly.csv` · `ads-rsa-text.csv` ·
`ads-asset-performance.csv` *(includes 46 retired assets that exist nowhere else)* ·
`ads-asset-group-creative.csv` · `ads-pmax-assetgroup-assets.csv` / `-monthly.csv` /
`-conversions-monthly.csv` / `-conversions-daily.csv`

### GA4 (property 353828960 "PNH2")
`ga4-events-by-source-monthly.csv` / `-daily.csv` · `ga4-events-by-page-monthly.csv` ·
`ga4-events-by-adgroup-monthly.csv` · `ga4-source-medium-monthly.csv` · `ga4-channels-monthly.csv` ·
`ga4-pages-monthly.csv` · `ga4-landing-pages-monthly.csv` / `-paid-monthly.csv` ·
`ga4-geo-monthly.csv` · `ga4-device-monthly.csv` · `ga4-newreturning-monthly.csv` ·
`ga4-device-newreturning-channel-monthly.csv` · `ga4-purchases-detail.csv` / `-monthly.csv` /
`-by-page-monthly.csv` · `ga4-outbound-links-monthly.csv` · `ga4-acuity-outbound-clicks.csv` ·
`ga4-schedule-page-reach.csv` / `-by-landing-paid.csv` · `ga4-self-referral-pollution.csv` ·
`pollution-quantified.csv` · `ga4-field-list.txt`

### Google Business Profile
`gmb-monthly-metrics.csv` · `gmb-daily-metrics.csv` · `gmb-monthly-by-location.csv` ·
`gmb-location-metadata.csv` *(both listings, including the duplicate)* ·
`gmb-search-keywords.csv` / `-monthly.csv` / `-classified.csv` / `-bucket-summary.csv` ·
`gmb-monthly-search-terms.csv` · `gmb-reviews.csv` / `-monthly.csv` ·
`gmb-review-totals-lifetime.csv` · `gmb-monthly-media-and-reviews.csv` · `gmb-field-list.txt`

### Cross-source and derived
`master-monthly-channel-table.csv` + `master-channel-summary.md` — one row per month, 2023-02 →
2026-09, every channel, with a per-month data-quality note ·
`verified-pause-candidates.csv` · `verified-city-performance.csv` ·
`gbp-opportunity-sizing.csv` · `proposed-lab-testing-adgroup.csv` *(has a `#` comment preamble
before the header — strip it before parsing)*

### Analyst notes
`DATA-QUALITY.md` · `NOTES-final-audit.md` ·
`NOTES-ads-campaign-history.md` · `NOTES-ads-conversions.md` · `NOTES-ads-keywords.md` ·
`NOTES-ads-search-terms.md` · `NOTES-ads-geo-device-time.md` · `NOTES-ads-creative-settings.md` ·
`NOTES-ga4-events.md` · `NOTES-ga4-pages-channels.md` · `NOTES-cross-source-bookings.md` ·
`NOTES-gbp-metrics.md` · `NOTES-gbp-queries-reviews.md` · `NOTES-gbp-booking-link-compliance.md` ·
`NOTES-last-sweep.md` · `NOTES-verify-august.md` · `NOTES-verify-dead-inventory.md` ·
`NOTES-verify-pollution.md` · `NOTES-verify-lab-gap.md` · `NOTES-verify-gbp-opportunity.md`

Longer memos live outside this directory in `reports/`.

## Questions this archive CAN answer

Spend, clicks, impressions, CTR and CPC by campaign/ad group/keyword/search term/geo/device/hour,
daily since the account began; every search term Google was willing to show; the full negative
keyword list and campaign structure; every ad and RSA headline ever run, including 46 retired
assets; GA4 traffic, events, landing pages and attribution by month and day back to 2023-02;
18 months of Business Profile views, actions, search terms and reviews.

It also settles three specific questions that were previously answered wrongly: the 2025-vs-2026
CPA comparison (July 2026 was the account's **best** month at $9.35 like-for-like, not its worst),
the keyword-dilution story (dead — 102 serving keywords produced that best month), and the Monday
off-schedule serving anomaly (closed — 14 impressions, $5.11, all on 2026-08-17).

## Questions it CANNOT answer

Which ad clicks became patients (attribution breaks at the scheduler, and stays broken by choice
under the compliance stance set this week); Business Profile data before 2025-03-08; anything about
the seven dark months; true booking counts (use the Acuity export); the other ~51% of search terms;
true impression share below 10%; competitor auction share; the values of the Sept 7 bid modifiers;
and roughly two years of paid search — 5,824 GA4 `google / cpc` sessions from 2023-03 to 2025-03 —
that ran from a Google Ads account which is not this one.

**Three of those are still recoverable, but not from here, and only while access lasts:** the
Acuity export (settles booking truth), Jacob's Google Ads account list (may still hold the
2023–2025 history in the UI), and Search Console (free, never needed a subscription, and is the
only route to the queries behind 7,317 lifetime organic sessions).
