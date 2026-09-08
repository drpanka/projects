# Google Business Profile (GMB) — full metric archive

**Harvested 2026-09-08** (final day before the Supermetrics subscription lapses 2026-09-09).
Source: Supermetrics MCP, `ds_id = "GMB"`, tool_version 1.14.15, connected via
`pankanaturalhealth@gmail.com` (Supermetrics team 1054989).
Everything below was pulled live; nothing is recalled or estimated.

---

## 1. The single most important limit: there is no history before 2025-03-08

Requesting `2024-01-01` returns:

> `[START_DATE_HISTORICAL] Earliest supported historical start date for Google My Business is 2025-03-08.`

That is a rolling ~18-month window, and it moves forward every day. **Everything before
2025-03-08 — the clinic's first six and a half years on Google — is already gone and was
never retrievable through this connector.** The archive here is the maximum that existed
on the day it was taken.

A practical consequence: because the window is 18 months and rolling, monthly and daily
data cover *exactly the same span*. There is no "longer monthly range" to fall back on.

## 2. Files written

| File | What it is | Rows |
|---|---|---|
| `gmb-field-list.txt` | Complete field inventory (126 fields), report-type legend, date-range rules, and the metrics that **do not** exist | — |
| `gmb-monthly-metrics.csv` | All 16 Performance metrics by month, All-locations account | 19 months |
| `gmb-daily-metrics.csv` | Same 16 metrics by day | 550 days |
| `gmb-monthly-by-location.csv` | Same, split by location ID, both listings | 38 |
| `gmb-location-metadata.csv` | Full profile record for both listings (address, category, place ID, hours, description) | 2 |
| `gmb-monthly-search-terms.csv` | Search terms that surfaced the profile, with monthly impressions | 275 |
| `gmb-monthly-media-and-reviews.csv` | Photos uploaded and reviews received, by month | 6 |
| `gmb-review-totals-lifetime.csv` | Lifetime review count and rating | 1 |

**Integrity check performed:** the 550 daily rows were summed by month and compared against
the independently-issued monthly query. All 19 months reconcile exactly on both
`views_total` and `actions_total`. The daily file is not a transcription approximation.

## 3. Headline numbers

**Full period, 2025-03-08 → 2026-09-08 (550 days):**

| Metric | Total |
|---|---|
| Total profile views | **10,767** |
| — on Search | 9,185 (85.3%) |
| — on Maps | 1,582 (14.7%) |
| Total actions | **1,768** |
| — Directions requests | **981 (55.5%)** |
| — Website clicks | **711 (40.2%)** |
| — Phone calls | **76 (4.3%)** |
| — Messages | **0** |
| — **Bookings** | **0** |

**Last 12 complete months, 2025-09-01 → 2026-08-31:**

| Metric | Total |
|---|---|
| Total profile views | **7,057** |
| — on Search / on Maps | 6,105 / 952 |
| Total actions | **1,103** |
| — Directions requests | **616 (55.8%)** |
| — Website clicks | **438 (39.7%)** |
| — Phone calls | **49 (4.4%)** |
| — Messages / **Bookings** | **0 / 0** |

Action rate is stable at roughly 16% of views (16.4% full period, 15.6% last 12 months).

## 4. Is the bookings field genuinely empty, or just unsupported?

**The field is fully supported by the connector. The value is a real zero.** The distinction
the task asked about resolves cleanly in favour of "not populated", not "not exposed."

Evidence:

1. `actions_bookings` is present in `field_discovery` as a first-class Performance metric
   ("Bookings — The number of bookings received from the profile").
2. It returned the integer `0` in **all 550 daily rows and all 19 monthly rows**, in the
   same query that returned real non-zero values for website, phone and directions. A
   metric the connector could not fetch would not ride along in those rows.
3. Queried **in isolation** (`yearMonth, actions_bookings, actions_messages` for July 2026)
   it returned a populated row `["2026|07", 0, 0]` — not `"No data found"`. Supermetrics
   *does* return `"No data found"` when it genuinely has nothing: that is exactly what the
   second location account returned for the same date range.
4. Supermetrics also emits real nulls when a value is absent — the searchKeyword report
   returned `null` for 2026-08. Bookings returned `0`, not `null`.

**The honest residual caveat:** Google's Performance API omits the `BUSINESS_BOOKINGS`
series entirely for a profile with no booking-partner integration, and Supermetrics renders
an absent series as `0`. So "zero bookings occurred" and "Google reports no booking series
because no booking provider is attached" are observationally identical from this side. Given
that PNH schedules through Acuity and Acuity is not wired to this profile as a Google booking
partner, the second explanation is the near-certain one. The field is empty because there is
nothing feeding it, not because the connector hides it.

`actions_messages` is zero on the same evidence and by the same reasoning — Google Business
messaging has never been switched on. `actions_food_menu_clicks` and `actions_food_orders`
are zero too; those are restaurant-only metrics and behave identically, which is a useful
control: it shows what "metric that legitimately does not apply" looks like in this data.

> **Compliance flag.** The obvious-looking "fix" for zero bookings — attaching Acuity to the
> profile via Reserve with Google — would send completed-appointment data to Google, which is
> precisely what was ruled out this week. This finding is recorded as a *measurement fact*, not
> as an argument for that integration. The website-click action already carries traffic to the
> site without transmitting appointment data.

## 5. What the trend actually says

**Views are flat and have been for eighteen months.** Monthly totals sit in a narrow band of
497–667, with one outlier month (October 2025, 765). There is no growth trend, no decay
trend — a steady state of roughly 600 profile views a month.

**Actions are drifting down, and faster than views.** Comparing the same calendar window
year over year (Mar 8 – Sep 8):

| | 2025 | 2026 | Change |
|---|---|---|---|
| Views | 3,794 | 3,427 | **−9.7%** |
| Total actions | 686 | 536 | **−21.9%** |
| Website clicks | 281 | 231 | −17.8% |
| Directions requests | 377 | 281 | −25.5% |
| Phone calls | 28 | 24 | −14.3% |

Actions falling twice as fast as views means the profile is converting its impressions less
well than a year ago, not merely getting seen less. Monthly action rate ran 17–21% through
mid-2025 and 11–17% through most of 2026, with a partial recovery in July–August 2026 (17.4%,
20.3%).

**Seasonality is weak but real.** The low point is November–December (83 and 73 actions;
website clicks bottom at 18 in December) and March 2026 is the worst single month for
directions (18, against a 52-month average). Late summer recovers. The pattern fits a clinic
whose demand tracks the school calendar, which is consistent with the September–December
booking window described in the project context.

**Day of week is a clean weekday/weekend split** (550 days, excluding the lagging tail):
Mon–Thu average 22.6–23.0 views/day, Friday 19.1, Saturday 13.1, Sunday 14.6. Actions per day
are highest Monday (3.96) and Thursday (3.88), lowest Saturday (2.36).

## 6. Which action types dominate — and why it matters

Directions requests are the largest action type in every single month, 55.5% of all actions
across the period, and they outnumber website clicks 981 to 711.

For a cash-pay clinic that books online, that mix deserves scepticism as a demand signal.
A directions request is overwhelmingly a *navigation* action — someone who already knows they
have an appointment at 901 1st St N and wants the route. Website clicks are the action that
actually maps to new-patient consideration. Read that way, the acquisition-relevant number
from Business Profile is **roughly 40 website clicks per month**, not 92 total actions.

Phone calls are strikingly rare: **76 calls in eighteen months**, about 4 a month, and
**zero in May 2026, one in June 2026**. Given the profile lists (612) 568-8382 and the site
has an untracked `tel:` link, this is worth knowing: the phone is not a meaningful inbound
channel from Google, so the untracked `tel:` link noted in the project context is a small
gap, not a large one.

Search vs Maps: 85.3% of views come from Search, only 14.7% from Maps. Mobile leads both
surfaces (68.5% of Search views, 64.5% of Maps views). Maps views did rise in the most recent
two months (110 and 125, against a 12-month average of 79), driven by mobile — the only
genuinely improving series in the file.

## 7. The duplicate listing — confirmed, and it is real

**There are two Google Business Profile listings for Panka Natural Health.** This was the
thing worth finding.

| | **Live listing** | **Duplicate** |
|---|---|---|
| Location ID | `3326559683279742636` | `10418367222074184209` |
| Store code | `02856059060526079777` | *(none)* |
| Address | 901 1st Street North, Suite 901A, Hopkins, MN 55343 | **none — no address at all** |
| Coordinates | 44.9262389, −93.4117187 | *(none)* |
| Primary category | **Naturopathic practitioner** | **Medical clinic** |
| Business type | Service at the business address and surrounding area | **Service only in the surrounding area** |
| Phone | (612) 568-8382 | **(612) 568-8382 — same** |
| Website | pankanaturalhealth.com | **pankanaturalhealth.com — same** |
| Place ID | `ChIJsWPTTrQn9ocRRITDvEC9gkA` | `ChIJqzYhX5yb_IcRFlsaHwLlz30` |
| Maps CID | 4648485851142259780 | 9065716372194614038 |
| Status | Open | **Open** |
| Opened | Sept 2018 | Sept 2018 |
| Google Ads label | `Adwords_9157175049` | *(none)* |
| **Views / actions, 18 months** | 10,767 / 1,768 | **query returns "No data found"** |

The live listing is `3326559683279742636` — it is the one with the address, the correct
"Naturopathic practitioner" category, the Google Ads location-extension link, and 100% of the
traffic. The "All locations" account returns only this one when performance metrics are
requested, which is why the monthly and daily files are unambiguous.

The duplicate is a distinct, **currently Open** profile with its own place ID and Maps CID,
carrying the same business name, the same phone number and the same website, categorised
differently ("Medical clinic"), configured as a service-area business with no street address,
and with a shorter, older-sounding description that still advertises the free 10-minute call.
It has recorded no views and no actions in eighteen months.

Why this matters, plainly: duplicate profiles sharing a name, phone and website are what
Google's guidelines treat as a violation, and they dilute the signals — reviews, photos,
engagement — that the real listing depends on to rank. All 15 reviews and the 5.0 rating sit
on the live listing; the duplicate contributes nothing and can only subtract. Its zero
traffic means removing it costs nothing measurable. **This is a finding to hand to Jacob, who
makes all account changes himself** — the remedy is the duplicate-removal flow in the Business
Profile manager, and it should be confirmed against the live Maps entry
(`https://maps.google.com/maps?cid=9065716372194614038`) before anything is touched, since a
CID that no longer resolves would mean it has already been suppressed.

## 8. Search terms — read the zeros correctly

`gmb-monthly-search-terms.csv` holds 275 term-months from 2025-04 through 2026-08 (the
searchKeyword report requires whole-month boundaries, so March 2025 is not included; 2026-08
returned a single empty row with a null impression count and appears not yet populated).

**Only 12 of the 275 rows carry a non-zero impression count.** That is not because the other
263 terms had no impressions — Google suppresses per-term counts below a threshold of roughly
15 impressions/month and returns a bucketed placeholder, which Supermetrics renders as `0`.
Treat `0` in that file as "fewer than ~15 that month", never as "none".

The twelve terms that cleared the threshold are almost entirely two phrases:

| Term | Months above threshold | Range |
|---|---|---|
| `naturopathic doctor` | 2025-05, 08, 09, 12; 2026-01, 04 | 16–19 |
| `naturopathic doctor near me` | 2025-04, 05, 06, 07 | 16–22 |
| `holistic doctor near me` | 2025-05, 2025-12 | 16–19 |

Below the threshold the long tail is genuinely useful and worth keeping: `functional medicine
doctor near me`, `food sensitivity test(ing) near me`, `holistic pediatrician near me`,
`homeopathic doctors near me`, geographic variants (Minnetonka, Edina, Plymouth, Eden Prairie,
Chaska, St Louis Park, Wayzata, Rogers, St Paul), condition-led queries (`holistic doctor for
pcos`, `naturopathic gut health doctors chaska mn`, `doctors who prescribe natural thyroid
supplements`, `thyroid specialist natural`, `naturopathic infertility doctor minnesota`,
`pediatric functional medicine near me`, `natural health for men near me`), and brand queries
(`panka`, `panka natural health`, plus full-address lookups).

Notable: **`naturopathic doctor near me` cleared the threshold in four consecutive months in
2025 and never again in 2026** — consistent with the overall softening in the performance
data. Also worth flagging as a data-quality point: several terms are clearly other businesses
(`karissa kuhle hopkins mn`, `kathryn l piha md`, `champion naturopathic health, llc`,
`jennifer alasko minnesota alternative health`, `panakumen restaurant`) — Google matches the
profile to near-miss queries, which is normal and not a problem.

## 9. Photos and reviews — an underused asset

- **Lifetime: 15 reviews, 5.0 average.** Flawless rating.
- **Only 4 new reviews in eighteen months** — 2025-04, 2025-06, 2025-12, 2026-07. Roughly one
  every four and a half months.
- **Only 3 photos uploaded in eighteen months** — 1 in June 2025, 2 in June 2026.

A profile with a perfect 5.0 across 15 reviews and effectively no ongoing photo or review
cadence is the clearest cost-free lever visible in this dataset, and it sits alongside a
Google Ads campaign that has been budget-starved at $10/day. The Business Profile is
delivering ~600 views and ~40 website clicks a month for nothing.

## 10. Reporting lag — do not read the last week as a collapse

The tail of the daily file is incomplete, not catastrophic:

- Views are populated through **2026-09-04** (2026-09-05 shows 1, and 09-06 through 09-08 show 0).
- Actions are **zero for every day from 2026-09-01 onward**, while views for those days are normal.

Google's Performance API lags several days, and actions lag longer than views. The September
2026 row in the monthly file (81 views, 0 actions) is a partial month and must not be compared
against complete months. All 12-month figures in this document deliberately end 2026-08-31.

## 11. Method notes for anyone picking this up later

- `has_report_type_selection` is `false` for GMB — the report type is inferred from the fields
  requested. Mixing Performance metrics with Reviews or searchKeyword metrics in one query
  will fail; split them.
- The only valid setting key is `exclude_invalid_accounts`. `include_zero_impressions` is a
  Google Ads setting and returns `SETTING_KEY_INVALID` here.
- searchKeyword requires first-day/last-day-of-month boundaries and offers no daily grain.
- Querying `accounts/100272753749399584663` (All locations) and querying the live location
  account directly return byte-identical monthly numbers — verified. The All-locations account
  is sufficient.
