# NOTES — Google Ads search-term archive (all campaigns, all time)

**Agent slug:** `ads-search-terms`
**Pulled:** 2026-09-08, final Supermetrics harvest before subscription ends 2026-09-09
**Source:** Supermetrics `ds_id="AW"`, `ds_accounts="7473953248"`, timezone `America/Chicago`
**Date range requested:** 2024-01-01 → 2026-09-08 (deliberately wider than the known history to prove where data starts)
**Report type used:** Google Ads `SearchTermView` (Supermetrics report type 36 — the only one that carries `Searchterm` + `QueryTargetingStatus`)

---

## 1. Files written

| File | Rows (excl. header) | What it is |
|---|---|---|
| `ads-search-terms-alltime.csv` | 612 | Verbatim conversion of the prior oversized pull (2025-06-01 → 2026-09-07, filter `Cost > 0`). Kept as handed over, unmodified. |
| `ads-search-terms-alltime-incl-zero-cost.csv` | 8,197 | **The master file.** Re-pull with NO cost filter, `include_zero_impressions: true`, plus `CampaignID` and `ConversionValue` added. One row per campaign × ad group × search term × matched keyword × match type. |
| `ads-search-terms-monthly.csv` | 8,629 | Same, sliced by `Yearmonth`. Use this for era comparisons. |
| `ads-search-terms-rollup.csv` | 5,463 | One row per distinct search term, all time. Totals + pipe-joined lists of the campaigns, ad groups, matched keywords, match types and query-targeting statuses that term ever appeared under. Sorted by cost descending. |

Header rows in the three new files are the literal `requested_field_ids` from the API, not display names. All conversions were done with `python3`; no data row was typed by hand.

**Note on the two "all-time" files:** the handed-over `ads-search-terms-alltime.csv` has 612 rows; my no-filter re-pull contains 613 rows with `Cost > 0`. The extra row is 2026-09-08 spend, which the earlier pull's end date excluded. Nothing else differs.

---

## 2. The account's whole paid-search history, in one table

Search-term data exists **only** for the two Search campaigns. Performance Max produces no search terms at all (see gaps).

| Month | Search campaign spend | Spend visible as search terms | Coverage | Distinct terms | Clicks | Conv (tracked) |
|---|---|---|---|---|---|---|
| 2025-07 | $774.63 | $401.58 | 51.8% | 943 | 156 | 43.00 |
| 2025-08 | $659.60 | $316.22 | 47.9% | 689 | 125 | 59.00 |
| 2025-09 → 2026-03 | **$0.00 — account dark** | — | — | — | — | — |
| 2026-04 | $186.22 | $99.18 | 53.3% | 383 | 37 | 10.00 |
| 2026-05 | $190.25 | $76.63 | 40.3% | 318 | 39 | 11.00 |
| 2026-06 | $135.07 | $49.77 | 36.9% | 12 | 19 | 16.02 |
| 2026-07 | $673.33 | $324.38 | 48.2% | 1,823 | 198 | 23.51 |
| 2026-08 | $651.84 | $322.14 | 49.4% | 2,114 | 170 | 9.98 |
| 2026-09 (1–8) | $102.47 | $51.73 | 50.5% | 574 | 27 | 1.00 |
| **Total** | **$3,373.41** | **$1,641.63** | **48.7%** | **5,463 distinct** | **771** | **173.51** |

Plus `Campaign #1` (Performance Max, Jun–Jul 2025): **$910.92** with **zero** search-term visibility. Against the whole account's $4,284.33 lifetime spend, the search-term archive accounts for **38.3%**.

The Sept 2025 → Mar 2026 blackout is real, not a data gap — the campaign-level pull returns no rows for those months either. 2026-06 is odd in a different way: only 12 distinct terms in `Leads-Search-1` (which spent $24.06 that month), because most of June's search spend was the brand-defense campaign.

`PNHdefense-Website traffic-Search-2` contributed just 4 search-term rows in total, all brand navigational: `panka natural health` (2026-05 / 06 / 07) and `dr panka` (2026-06). $59.33 of its $158.06 lifetime spend is visible.

---

## 3. Era comparison — 2025 vs 2026

| | Jul–Aug 2025 | Apr–Sep 2026 |
|---|---|---|
| Distinct terms | 1,437 | 4,424 |
| Impressions | 4,462 | 9,139 |
| Clicks | 281 | 490 |
| Visible cost | $717.80 | $923.83 |
| CPC | $2.55 | $1.89 |
| CTR | 6.30% | 5.36% |
| Tracked conv / click | 0.363 | 0.146 |

Only **398 terms overlap** between the two eras. 1,039 terms appeared only in 2025; 4,026 appear only in 2026. The 2026 account is matching against a query surface roughly three times as wide at two-thirds the CTR and 40% of the conversion rate per click. That is exactly the "reaching more marginal queries" pattern CLAUDE.md §4 describes, and this file quantifies it across the whole history rather than one week.

Caveat that matters for every conversion figure above: through ~Aug 1 2026 two conversion actions were both primary (CLAUDE.md §4), so 2025 and Apr–Jul 2026 conversion counts are roughly double-counted. And the tracked conversion is a page-reach on `/schedule-an-appointment`, not a booking. Treat all conversion columns in these CSVs as *interest*, not revenue.

---

## 4. The long tail is nearly the whole file

- 5,463 distinct terms ever.
- **4,932 of them (90%) never received a single click** — impressions only.
- 3,650 (67%) were seen exactly once.
- Only **531 terms ever got a click**, and only **73 terms ever recorded a conversion**.

The zero-click 90% is the diagnostically valuable half of this archive: it is Google's own answer to "what do you think these ads are about." Broad match is showing the ads to veterinary, out-of-state, jobs/schooling and pure-symptom queries that never cost anything but reveal where the next leak will open if bids or budget rise.

---

## 5. Terms still leaking money as of September 2026

Sept 1–8 2026 visible spend was $51.73 across 25 terms. **$17.01 of it (32.9%) sits on terms whose current `QueryTargetingStatus` is `Excluded`** — meaning the negatives Jacob added in the Sept 4–7 session are landing on real, recent spend: `low acth` $6.42, `holistic` $4.26, `dr bob zajac` $2.33, `pediatric clinics near me` $2.07, `hormone therapy` $1.06, `poop` $0.87. That is the negative-keyword work confirmed working, not a leak.

The leaks are the terms still showing `None`. Grouped over Aug + Sep 2026 (the current-configuration window), excluding anything already `Excluded`, and all with **zero** conversions unless noted:

| Pattern | Aug+Sep 2026 cost | Terms | Comment |
|---|---|---|---|
| **Named clinic / provider / street-address navigational** | **$48.92** | 22 | Biggest single leak. `hopkins clinic` $8.52 (all-time), `first choice wellness near me` $4.64, `m health women's clinic edina` $2.80, `bluestone physician services mn` $2.33, `broadway clinic near me` $2.30, `woodwinds clinic` $1.78, `hcmc south 8th street minneapolis mn` $1.71, `ramsey county public health center` $2.21, `lakeville specialty center suite 250` $2.30, `2855 campus drive ste 650suite 650plymouth mn 55441` $1.29, plus named individuals (`dr oppitz`, `dr silvia hugec`, `dr heather stone diet`, `allan warshowsky md`). Someone typing a street address or another clinic's name is navigating, not shopping. |
| **Symptom / how-to / "cure" self-research** | $25.62 | 11 | `how to fix memory loss from depression` **$9.84 on one click**, `menopause symptoms` $2.88, `thyroid symptoms` $2.87, `symptoms of perimenopause and menopause` $2.81, `hot flashes at night` $2.80, `signs of early menopause`, `how to cure ulcerative colitis permanently`, `how to cure gout permanently`, `preventive screenings for women`. CLAUDE.md §8 item 6 estimated this family at ~$14/week; over Aug+Sep it runs about $12–13/week, so the estimate holds and the "$3–4/mo" figure from when *symptoms* was left open is off by roughly 4×. |
| **Prescription-hormone shopping** | $23.36 | 11 | `female hormone therapy near me` $3.56, `weight gain and hormone replacement therapy` $2.91, `estrogen replacement options` $2.70, `where can i get estrogen patches` $1.99, `where to get estrogen patches` $1.83, `estrogen and sex drive` $1.88, `medicine for pcos` $2.82, `best thyroid medication for weight loss` $2.33. **This contradicts the decision log.** CLAUDE.md §6 records `estrogen replacement`, `estrogen patches`, `hormone replacement` and `hrt` as blocked, yet every one of these shows `QueryTargetingStatus = None` (not `Excluded`) in a pull taken 2026-09-08. `QueryTargetingStatus` is a live field, so `None` means not currently excluded. Worth a direct check of the negative list against these four phrases. |
| **ED / sexual** | $20.62 | 14 | `erectile dysfunction uptodate` $4.87, `most effective ed treatment` $3.06, `how can i make my penis stronger` $2.02, `vacuum therapy for erectile dysfunction` $1.13, `best for ed` $1.28. **All of it landed in Aug 2026; September 2026 is clean — zero ED impressions.** The block is working now; $25.75 of ED spend leaked in Jul–Aug 2026 before it took hold. Two of these terms recorded a "conversion" (`erectile dysfunction ncbi`, `erectile dysfunction treatment`) — independent corroboration that the tracked conversion is a page-load, not a booking, since an ED searcher is not a PNH patient. |
| **Fringe modality / device** | $10.49 | 6 | `biocharger near me` $2.32, `enema nurse near me` $2.30, `nrt testing near me` $2.20, `belief code practitioner near me` $1.65, `chakra tune up` $0.33. |
| **Insurance / free / low-cost** | $9.96 | 4 | `functional dr near me that takes insurance` $2.30, `free children clinic near me` $2.34, `ramsey county public health center` $2.21, `costco fertility program` $3.11. PNH is cash-pay; "takes insurance", "free clinic" and county-clinic queries are structurally unservable. Cleanest, safest family to block — it touches nothing on the protect list. |
| **Out-of-scope musculoskeletal** | $7.57 | 5 | `best sciatica treatment`, `how to cure gout permanently`, `best fibromyalgia doctor near me`, `holistic osteoporosis doctor near me`. |

Two more open items visible in the data, both already in CLAUDE.md §8 item 7 as "un-applied": `best primary care physician near me` $1.60 and `best primary care physicians near me` $1.37 both still serve as `None`. The decision log blocks `primary physician(s)` and protects `primary care`; the *"best primary care physician**s**"* form falls in the gap between those two rules.

**All figures above are what Google shows.** Because search terms cover only ~49% of spend, the true size of each leak is plausibly about double what is listed.

---

## 6. Terms that converted and are NOT keywords

Of 173.51 tracked conversions across the archive, **124.51 (71.8%) came from search terms whose `QueryTargetingStatus` was never `Added`** — i.e. terms the account has never bid on directly, reached only as broad-match spill. Only 8 terms in the entire history are both a keyword and a converter.

Highest-conversion terms that are not keywords (cross-checked against the live Aug–Sep 2026 keyword serving list):

| Search term | Conv | Cost | CPA | Nearest live keyword |
|---|---|---|---|---|
| `functional medicine doctor minneapolis` | 8.00 | $20.58 | $2.57 | none — closest is `functional medicine` phrase |
| `holistic doctor near me` | 7.00 | $50.07 | $7.15 | `holistic dr near me` (broad) — *dr* vs *doctor* |
| `functional medicine doctor` | 7.00 | $39.71 | $5.67 | `functional medicine` phrase |
| `functional medicine doctor near me` | 5.00 | $28.41 | $5.68 | `functional medicine near me` (removed) |
| `holistic doctor minneapolis` | 5.00 | $9.94 | $1.99 | `holistic medicine Minneapolis` phrase |
| `integrative health minneapolis` | 5.00 | $3.98 | $0.80 | `integrative health near me` phrase |
| `natural endocrinologist near me` | 5.00 | $1.91 | $0.38 | none |
| `doctors for perimenopause` | 5.00 | $2.02 | $0.40 | `perimenopause doctor near me` phrase |
| `holistic gynecologist near me` | 4.00 | $2.58 | $0.65 | none |
| `naturopath minneapolis` | 3.00 | $6.73 | $2.24 | `naturopathic doctor Minneapolis` phrase (would not match) |
| `top rated functional medicine doctor near me` | 3.00 | $5.01 | $1.67 | none |
| `functional medicine providers near me` | 2.00 | $8.40 | $4.20 | none |
| `naturopathic doctors near me` | 2.00 | $4.30 | $2.15 | `naturopathic doctor near me` exact — plural is a close variant |
| `best doctor for perimenopause near me` | 2.00 | $3.47 | $1.74 | none |
| `holistic obgyn` | 2.00 | $3.20 | $1.60 | none |
| `severe daytime sleepiness` | 2.00 | $2.94 | $1.47 | none — matched via `adrenal fatigue doctor near me` |
| `pediatric naturopathic doctor` | 2.00 | $2.72 | $1.36 | `pediatric naturopath near me` broad |
| `holistic pcos doctor near me` | 2.00 | $0.64 | $0.32 | `pcos specialist near me` phrase |
| `naturopathic doctors mn` | 2.00 | $2.09 | $1.04 | none |

The clearest patterns: **the account bids on "dr" but converts on "doctor"**, and **the `<service> minneapolis` / `<service> mn` geo-modified forms convert well and are almost entirely unbid** (`functional medicine doctor minneapolis`, `holistic doctor minneapolis`, `integrative health minneapolis`, `naturopath minneapolis`, `naturopathic doctors mn` together: 23 conversions on $43.32). The Geo-Qualified ad group exists but its live keywords are `holistic medicine Minneapolis`, `naturopathic doctor Minneapolis`, `functional medicine doctor minnetonka` — none of which match the four terms above.

Same caveat as everywhere: these are page-reach conversions on a metric that was double-counted before ~Aug 1 2026. Treat this table as a ranked hypothesis list for Jacob to check against Acuity bookings, not as proof of revenue. Jacob makes all account changes himself; nothing here should be read as an instruction to a tool.

---

## 7. Top 10 most expensive terms that never converted (all time)

| # | Cost | Clicks / Impr | Term | Current status |
|---|---|---|---|---|
| 1 | $15.84 | 2 / 5 | `women's health functional medicine near me` | None |
| 2 | $9.84 | 1 / 1 | `how to fix memory loss from depression` | None |
| 3 | $9.84 | 3 / 13 | `functional medicine doctors near me` | Added |
| 4 | $8.73 | 3 / 57 | `homeopathic doctors near me` | None |
| 5 | $8.71 | 3 / 57 | `integrative medicine near me` | Added |
| 6 | $8.67 | 4 / 7 | `holistic health minneapolis` | None |
| 7 | $8.52 | 1 / 4 | `hopkins clinic` | None |
| 8 | $8.14 | 1 / 1 | `chronic` | None |
| 9 | $7.97 | 2 / 2 | `healthpartners maple grove` | None |
| 10 | $7.96 | 2 / 87 | `functional medicine minneapolis` | None |

Top 10 combined: $94.22. All 5,390 never-converting terms combined: **$1,065.88 — 65% of all visible search-term spend.**

Note #3 and #5 are *added keywords* that have never converted, and #6/#10 are geo-modified functional-medicine terms whose non-geo siblings convert well. `chronic` (#8) is on CLAUDE.md's un-applied Sept 3 recommendation list and cost $8.14 for a single click on a one-word query.

---

## 8. Method / reproducibility

```
# master file
data_query(ds_id="AW", ds_accounts="7473953248", date_range_type="custom",
  start_date="2024-01-01", end_date="2026-09-08", timezone="America/Chicago",
  fields="Campaignname,CampaignID,Adgroupname,Searchterm,Keyword,Matchtype,QueryTargetingStatus,"
         "Impressions,Clicks,Cost,Ctr,CPC,Conversions,ConversionRate,CostPerConversion,ConversionValue",
  max_rows=100000, settings={"include_zero_impressions": true})
# monthly: prepend Yearmonth, drop the non-aggregatable rate fields
```

Both oversized results auto-saved to `~/.claude/projects/.../tool-results/` and were parsed with `python3`, mapping columns by `requested_field_ids`.

Field constraints discovered (worth recording — they cost time):
- `Searchterm` lives only in report types 35 (`PaidOrganicSearchTermView`) and 36 (`SearchTermView`).
- `QueryTargetingStatus` and `search_term_match_source` exist **only** in type 36.
- `Cost` and `Conversions` are **not** available in type 35, so paid+organic side-by-side is impossible in one query regardless of connections.
- `Ctr`, `CPC`, `ConversionRate`, `CostPerConversion` are `is_non_aggregatable` — they are correct per row but must not be summed. The rollup recomputes them from raw totals instead.
