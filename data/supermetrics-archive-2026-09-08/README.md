# PNH Supermetrics archive — captured 2026-09-08

The Supermetrics subscription ended 2026-09-09. **This directory cannot be regenerated.**
Everything here was pulled live from Google Ads (account 7473953248), GA4 (property 353828960
"PNH2") and Google Business Profile on 2026-09-08.

## How to read this archive

- `NOTES-*.md` — the analyst write-up for each area. Read these first; they carry the caveats.
- `*.csv` — the data, with real header rows.
- `raw-*.json` — unprocessed API responses, kept so any derived CSV can be re-checked.
- `build_*.py` / `analyze_*.py` — the scripts that produced the CSVs from the raw JSON.
- `campaign-settings-<id>.json` — full structural snapshot of each campaign (keywords, negatives,
  ad schedule, extensions, targeting) as of 2026-09-08.

## Hard limits discovered during capture

- **Google Business Profile history only reaches back to 2025-03-08.** Supermetrics returns
  "Earliest supported historical start date for Google My Business is 2025-03-08". The clinic's
  first 6.5 years on Google were already unrecoverable before this archive was made.
- **The Google Ads account was dark from 2025-09 through 2026-03** — seven consecutive months of
  zero delivery. Any comparison spanning that gap is comparing two separate campaign lifetimes,
  not a continuous trend.

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
5. **About 65 keywords in the removed ad group "Ad group 1" still report status "Enabled."**
   They cannot serve. Any keyword count that includes them is wrong. See
   `ads-keyword-count-by-month.csv`, which counts keywords that actually served.
6. **tagassistant.google.com and ads.google.com self-referrals pollute GA4 conversion data** —
   these are the operator's own tag tests. See `ga4-self-referral-pollution.csv`.
7. **`pankanaturalhealth.com / referral` in GA4 is NOT junk.** It is the fingerprint of real
   bookings whose attribution was destroyed when the Acuity scheduler opened a new session on its
   own domain. Do not filter it away; it is the only evidence those bookings happened.
8. **GBP search-term counts below roughly 15/month are suppressed by Google and render as 0.**
   In `gmb-*search*` files, 0 means "below threshold", never "none".

## Questions this archive CAN answer

Spend, clicks, impressions, CTR and CPC by campaign/ad group/keyword/search term/geo/device/hour,
daily since the account began; every search term ever paid for; the full negative keyword list and
campaign structure; every ad and RSA headline ever run; GA4 traffic, events, landing pages and
attribution by month and day; 18 months of Business Profile views, actions and search terms.

## Questions it CANNOT answer

Which ad clicks became patients (attribution breaks at the scheduler); Business Profile data before
2025-03-08; anything about the seven dark months; true booking counts (use the Acuity export).
