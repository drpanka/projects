# NOTES — Google Ads geographic / device / time-of-day archive
**Agent slug:** `ads-geo-device-time` · **Pulled:** 2026-09-08 · **Source:** Supermetrics MCP, `ds_id=AW`, `ds_accounts=7473953248`
**Account timezone (verified live):** `America/Chicago` · **Currency:** USD · All queries run with `timezone="America/Chicago"`.
**Date window requested:** 2024-01-01 → 2026-09-08. Earliest row returned anywhere is **2025-06-03**; nothing exists before that.

---

## 1. Headline answers

### The "Monday overnight serving" anomaly is REAL but it is already FIXED — and it was never a Monday problem.

The ad schedule on `Leads-Search-1` was read live from the campaign resource this session and matches the
documented intent exactly (22 rows): **Mon–Fri 07:00–20:00, Sat 07:00–14:00, Sun 08:00–20:00.**

Hour-level serving tells a clean story:

| Era | Off-schedule impressions | Clicks | Cost | % of era spend |
|---|---|---|---|---|
| Before schedule took effect (≤ 2026-08-17) | 5,226 | 378 | **$838.28** | 28.3% of $2,961.20 |
| Schedule live (2026-08-18 → 2026-09-08, 22 days) | **0** | **0** | **$0.00** | 0.0% of $254.15 |

**The schedule started biting on 2026-08-18.** Every one of the 22 serving days from 2026-08-18 through
2026-09-08 served strictly inside its configured window — verified day by day (e.g. Sat 2026-08-22 served
07–13 against a 07–14 window; Sun 2026-09-06 served 08–15 against 08–20). 2026-08-17 was the transition day:
it still leaked $5.11 across hours 00, 01, 02, 05, 06.

**Monday was never the problem.** Over the whole history, Monday accounts for only **$91.55 of the $838.28**
of off-schedule spend (10.9%), while Mondays are 15.3% of all serving days — Monday *under*-indexes. The real
off-schedule leaks were the weekend, because those windows are the narrowest:

| Day | Serving days | Off-schedule spend | Off-schedule share of that day's spend |
|---|---|---|---|
| Saturday | 16 | **$222.93** | **50.5%** |
| Sunday | 15 | **$177.40** | **34.2%** |
| Wednesday | 17 | $99.16 | 21.9% |
| Tuesday | 18 | $95.66 | 17.4% |
| Monday | 17 | $91.55 | 17.8% |
| Friday | 15 | $91.45 | 23.5% |
| Thursday | 13 | $60.12 | 17.3% |

Most likely explanation for the flag: whoever looked in early September used a trailing window that still
contained the pre-2026-08-18 Mondays (Aug 3 = $2.19, Aug 10 = $5.61, Aug 17 = $5.11) and read them as current.
Mondays 2026-08-24, 2026-08-31 and 2026-09-07 are all clean at $0.00.

**Nothing needs changing here.** Recorded so the thread can be closed rather than re-opened.

### Which geo view matches the targeting

Targeting is **PRESENCE only**, so the **User Location view** (`settings={"geo_view": true}`) is the faithful
one — it reports where the user physically was. The default *Geographic* report blends physical presence with
*area of interest*, which inflates any place-name people search *about*.

The difference is not academic. **Hopkins** — the clinic's own city — shows **1,894 impressions / $86.03** in
the default view but only **656 impressions / $83.60** in the User Location view. Roughly two-thirds of the
default view's "Hopkins" impressions are people located elsewhere searching about Hopkins.

An independent cut confirms the targeting is doing its job: in the Geographic view's `LocationType` split,
`Leads-Search-1` is **100.0% LOCATION_OF_PRESENCE, 0% AREA_OF_INTEREST** ($2,601.31 of resolvable spend).
Only the paused PMax `Campaign #1` shows any area-of-interest spend (2.4%).

Likewise, in the User Location view **100.00% of `Leads-Search-1` impressions and spend fell inside MN/WI**.
Every out-of-state and international row in `ads-geo-userlocation-alltime.csv` (Bengaluru, Karachi, Lagos,
Manila, London, …) belongs to the paused PMax `Campaign #1`, which leaked 0.57% of impressions to other US
states and 0.28% outside the US. **There is no geo leakage on the live search campaign.**

---

## 2. Key numbers requested

### (a) Cities with lifetime spend > $20 and ZERO lifetime conversions

**At account level (all campaigns combined): NONE, in either geo view.** Every city that spent more than $20
lifetime recorded at least one tracked conversion. This is partly an artifact — the paused PMax
`Campaign #1` sprayed 1,855 conversions across the same metro, papering over the search campaign.

**Restricted to `Leads-Search-1` (the only enabled campaign), five cities qualify — identical in both views:**

| City | Region | Lifetime cost | Impressions | Clicks | Conversions |
|---|---|---|---|---|---|
| Maple Grove | Minnesota | **$54.68** | 433 | 24 | 0 |
| Little Canada | Minnesota | **$45.10** | 453 | 29 | 0 |
| Shakopee | Minnesota | **$32.86** | 267 | 15 | 0 |
| Eagan | Minnesota | **$25.24** | 210 | 13 | 0 |
| Dellwood | Minnesota | **$23.29** | 66 | 5 | 0 |
| **Total** | | **$181.16** | 1,429 | 86 | **0** |

Caveat before anyone acts on this: the tracked conversion is `PNH2 (web) schedule_appointment`, a page-reach
event, not a booking (CLAUDE.md §5). "Zero conversions" here means zero page-reaches, not zero patients.
Little Canada in particular is a known Twin Cities IP-geolocation sink — its 10,041 account-wide impressions
at $0.61 CPA are almost entirely PMax artifacts, so treat its city label with suspicion.

### (b) Total spend served outside the configured schedule

- **Since the schedule took effect (2026-08-18 → 2026-09-08): $0.00.** Zero impressions, zero clicks.
- **Lifetime, measured against the schedule as configured today: $838.28** (5,226 impressions, 378 clicks,
  77.02 conversions) out of `Leads-Search-1`'s $3,215.35 lifetime spend — 26.1%.
  This is a **counterfactual, not a leak**: before 2026-08-18 the campaign had no effective schedule, so that
  money was not "escaping" anything. It is the honest answer to "what would today's schedule have blocked".
- **Mondays only, last 60 days (2026-07-11 → 2026-09-08): $22.34** (188 impressions, 11 clicks, 2.00 conv),
  all of it on or before 2026-08-17. By hour: 00 → $0.00/39 imp · 01 → $10.39/41 imp · 02 → $5.01/29 imp ·
  03 → $0.37/13 imp · 04 → $0.00/9 imp · 05 → $1.10/26 imp · 06 → $5.48/31 imp.
- **Mondays only, all time: $91.55** (634 impressions, 44 clicks, 8.00 conv).

---

## 3. Other findings worth keeping

**Search Partners share exploded in August 2026.** Partners were 1–5% of `Leads-Search-1` spend through
July, then jumped to **18.6% in August ($121.20 of $651.84, 1,106 impressions, 86 clicks, 6 conv)** and 9.3%
in September so far. Lifetime partner CPA is $11.32 vs $9.91 on Google search. Worth a look — the shift
coincides with the budget squeeze and the tighter schedule. Full series in `ads-network-monthly.csv`.

**The 22-mile proximity radius is the single worst-performing location target.** The campaign location-target
report attributes each click to exactly one target (the 20 targets sum to $3,215.35, matching the campaign
total exactly — no double counting), so this is clean:

| Location target | Lifetime cost | Conversions | CPA |
|---|---|---|---|
| Unnamed geo target `2490837516419` (almost certainly the 22-mile radius) | **$1,357.46** | 68.00 | **$19.96** |
| Minneapolis (City) | $966.29 | 141.02 | $6.85 |
| Hopkins (City) | $194.19 | 33.00 | $5.88 |
| Edina (City) | $151.30 | 14.00 | $10.81 |
| Golden Valley (City) | $138.82 | 19.00 | $7.31 |
| Plymouth (City) | $130.26 | 18.00 | $7.24 |
| Eden Prairie (City) | $125.03 | 16.00 | $7.81 |
| Chanhassen (City) | $55.21 | 3.00 | $18.40 |
| St. Louis Park (City) | $27.61 | 4.00 | $6.90 |
| Minnetonka (City) | $14.92 | 5.00 | $2.98 |

The radius is **42% of lifetime spend at ~3× the CPA of the named city targets**. Full table (including the
ten low-spend exurb targets) in `ads-geo-locationtarget-alltime.csv`. For Jacob to weigh — no change proposed here.

**The recently-removed exurb targets were never material.** The ten lowest-spend targets (Maple Grove,
Otsego, Wayzata, Deephaven, Dayton, Ramsey, Saint Michael, Albertville, Bloomington, Shakopee) spent
**$54.27 combined over the campaign's entire life** and produced 1 conversion. Removing them was correct but
should not be expected to move anything.

**Device: desktop beats mobile on CPA, lifetime.** `Leads-Search-1`: Mobile 17,071 imp / $2,376.02 / 223.02
conv / **CPA $10.65** (CTR 6.17%); Computers 6,604 imp / $792.37 / 97.00 conv / **CPA $8.17** (CTR 4.63%);
Tablets 275 imp / $46.96 / 2.00 conv / **CPA $23.48**. Mobile is 74% of spend at the worse CPA. Note the
−15% mobile modifier was only applied on 2026-09-07, so it is essentially absent from this history.

**Best and worst hours, lifetime (`Leads-Search-1`).** Best CPA: 18:00 ($5.35, 22.00 conv), 17:00 ($5.54,
17.00 conv), 09:00 ($5.67, 44.00 conv). Worst inside-schedule hour: 10:00 ($12.89 CPA on $322.41 — the
single highest-spend hour of the day). Hour 20:00 burned $107.30 for 1.00 conversion, and it is now outside
the schedule. Overnight 00:00–05:00 lifetime: 2,105 impressions, $317.47, 19.51 conversions.

**A Search campaign served 46 Display Network impressions.** On 2026-07-18 only, `Leads-Search-1` recorded
45 mobile + 1 desktop Display impressions, 0 clicks, $0.00. Harmless in cost terms but it means display
expansion was reachable on that date. Single occurrence in the whole history.

**Serving history is far gappier than the campaign start date suggests.** `Leads-Search-1` has 111 actual
serving days between 2025-07-08 and 2026-09-08, not ~430. Gaps ≥ 3 days:
2025-07-23→08-04 (11d), 2025-08-12→08-22 (9d), **2025-08-27→2026-04-27 (242 days)**, 2026-05-04→05-12 (7d),
2026-05-13→05-30 (16d), 2026-05-30→06-10 (10d), 2026-06-10→07-03 (22d).
`Campaign #1` (PMax) served only 2025-06-03 → 2025-07-13 (41 days).
`PNHdefense` served 2026-05-29 → 2026-07-20 (50 days).
Any "all time" average in these files is an average over serving days, not calendar days.

---

## 4. Method, and how the all-time files were produced

Supermetrics returns small results inline (into context) and only writes a file when the payload is oversized.
To get everything onto disk **without ever hand-typing a data row**, each dataset was pulled at a granularity
fine enough to force the file path (daily, or monthly × campaign × city), saved as `raw-*.json`, and then
aggregated with `python3`. Base metrics (Impressions, Clicks, Cost, Conversions) are summed; `Ctr` and
`CostPerConversion` are **recomputed** from those sums rather than averaged, since averaging a pre-aggregated
ratio is invalid.

**The aggregation was validated against the direct all-time API response**, which was pulled separately and
read inline. Spot checks (Geographic view): Minneapolis 31,901 imp / 1,213 clk / $1,179.2583 / 490.67 conv →
rebuilt as 31,901 / 1,213 / $1,179.2584 / 490.68. Hopkins 1,894 / 46 / $86.0339 / 17 → exact. Chanhassen
740 / 45 / $105.6042 / 14 → exact. User Location view: Minneapolis 31,975 / 1,213 / $1,163.7535 / 491.67 →
rebuilt exact; Hopkins 656 / 41 / $83.6039 / 13 → exact. Deltas are ≤ $0.0001 (float summation) and ≤ 0.01
conversions (monthly fractional-conversion rounding).

**Cross-file reconciliation** — the hourly, device and network files agree to the cent on every campaign:
`Leads-Search-1` 23,950 imp / 1,383 clk / $3,215.35 / 322.02 conv; `Campaign #1` 100,443 / 3,386 / $910.92 /
1,855.01; `PNHdefense` 363 / 66 / $158.06 / 26.21.

---

## 5. Data-quality caveats (read before trusting a number)

1. **Geographic reports drop rows Google cannot resolve to a place.** City-level geo totals are slightly
   below campaign totals: `Leads-Search-1` 23,856 imp / $3,214.36 vs 23,950 / $3,215.35 (−0.4% imp, −$0.99);
   `Campaign #1` 99,450 vs 100,443 (−1.0%). Small, but geo files will never foot to campaign files exactly.
2. **The metro/postal/LocationType file drops far more.** `ads-geo-detail-monthly.csv` resolves only
   $2,601.31 of `Leads-Search-1`'s $3,215.35 (−19%), because requiring a postal code discards a lot of rows.
   Use it for *proportions* (presence vs interest, metro mix), never for totals.
3. **Conversions are `PNH2 (web) schedule_appointment`, a page-load proxy**, and July 2025 figures carry the
   double-counting problem described in CLAUDE.md §4. Every CPA in these files inherits that.
4. **`CostPerConversion` is blank, not zero, where conversions are zero.** Do not read blank as $0.
5. **Hour-of-day is in the account timezone (America/Chicago), confirmed live** — it is *not* affected by the
   `timezone` query parameter, so the schedule comparison is apples-to-apples.
6. **`Metroarea` for `Leads-Search-1` is 100% "Minneapolis-St. Paul, MN"** — the dimension carries no
   information for this account and was archived only for completeness.
7. **`IsTargetingLocation` could not be pulled.** Supermetrics rejects it unless `geo_view` is enabled, and it
   cannot be combined with `LocationType`. Recorded as a gap rather than worked around, since `LocationType`
   answered the presence-vs-interest question directly.
8. Row counts below are data rows, excluding the header.

---

## 6. Files written (all in `/home/user/projects/data/supermetrics-archive-2026-09-08/`)

### Requested deliverables
| File | Rows | Contents |
|---|---|---|
| `ads-geo-alltime.csv` | 466 | Geographic (default) view, city × region × country, all campaigns, all time |
| `ads-geo-userlocation-alltime.csv` | 817 | Same, User Location view (`geo_view: true`) — **the view that matches PRESENCE targeting** |
| `ads-geo-monthly.csv` | 955 | Geographic view by month × campaign × city |
| `ads-device-monthly.csv` | 35 | Month × campaign × device |
| `ads-hour-dayofweek-alltime.csv` | 168 | Complete 7 × 24 grid, all campaigns, incl. never-served cells |
| `ads-hour-dayofweek-monthly.csv` | 1,251 | Month × campaign × day-of-week × hour |
| `ads-network-monthly.csv` | 21 | Month × campaign × network (incl. Search Partners, Display) |
| `ads-offschedule-check.csv` | 620 | Off-schedule analysis, 6 scopes × day × hour, with `within_ad_schedule` flag |

### Supporting / higher-granularity files (kept — they are the true archive)
| File | Rows | Contents |
|---|---|---|
| `ads-geo-userlocation-monthly.csv` | 1,342 | User Location view by month × campaign × city |
| `ads-geo-locationtarget-alltime.csv` | 24 | **Spend per configured location target** — sums exactly to campaign totals |
| `ads-geo-locationtarget-daily.csv` | 575 | Same, daily |
| `ads-geo-detail-monthly.csv` | 1,380 | City × region × metro × postal × LocationType (presence vs interest) |
| `ads-hour-daily-by-campaign.csv` | 2,612 | Date × hour × campaign — everything else derives from this |
| `ads-hour-dayofweek-alltime-by-campaign.csv` | 423 | 7 × 24 grid split by campaign |
| `ads-device-daily.csv` | 492 | Date × campaign × device |
| `ads-device-alltime.csv` | 8 | Campaign × device lifetime |
| `ads-network-daily.csv` | 728 | Date × campaign × network × device |
| `ads-network-alltime.csv` | 5 | Campaign × network lifetime |

### Raw API payloads (unmodified tool output, for re-derivation after the subscription lapses)
`raw-geo-monthly-default.json` · `raw-geo-monthly-userlocation.json` · `raw-device-daily.json` ·
`raw-network-daily.json` · `raw-hour-daily.json` · `raw-locationview-daily.json` · `raw-geo-detail-monthly.json`

### Scripts (re-runnable against the raw payloads, no network needed)
`build_geo_device_time.py` · `build_offschedule.py` · `build_geo_detail.py` ·
`analyze_keynumbers_geo.py` · `analyze_geo_extra.py`

---

## 7. Gaps and things NOT retrieved

- **No data before 2025-06-03.** Queried back to 2024-01-01; the account returns nothing earlier.
- **`IsTargetingLocation` not pulled** — Supermetrics error: *"Is targeting location is only available when
  the Use user location view setting is enabled, and cannot be combined with Location type."* Not retried,
  because `LocationType` answered the same question. If needed, pull it alone with `geo_view: true`.
- **`ads-geo-monthly.csv` is the Geographic (default) view only.** The User Location monthly equivalent is
  saved separately as `ads-geo-userlocation-monthly.csv`; the task named one monthly geo file, so both were
  kept rather than choosing.
- **Hour × device and hour × geo were not crossed.** `Hour` is only available on report types
  AccountChanges / Ad / AdGroup / CallView / Campaign / Customer, and `City`/`Region` only on
  CAMPAIGN_LOCATION_TARGET_REPORT / GeographicView / LocationView — **the two cannot be combined in one
  query**. Hour × device *is* possible (both live on Campaign) but was not pulled.
- **Ad-group-level geo/device/hour not pulled** — this task was scoped to campaign level.
- **No impression-share metrics in these files.** `SearchImpressionShare` and
  `SearchBudgetLostImpressionShare` do not exist on GeographicView (report type 28), so they cannot be
  broken out by city. They are available by hour/device at campaign level but were left to the
  campaign-history agent, which already produced `ads-impression-share-floor-analysis.csv`.
- **The identity of geo target `2490837516419` is inferred, not confirmed.** It reports as
  "Unknown location" with a blank `LocationType`, which is how proximity/radius targets surface. Given
  CLAUDE.md documents a 22-mile radius around 44.9244, −93.4114, that is the near-certain match — but it was
  not verified against the campaign's criterion list, so treat the label as an inference.
- **`Conversions` is the account's tracked (page-reach) conversion**, not Acuity bookings. Nothing in this
  archive touches booking truth.
