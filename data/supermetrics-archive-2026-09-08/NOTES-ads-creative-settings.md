# NOTES — Ads creative + full structural snapshot
**Agent slug:** `ads-creative-settings` · **Pulled:** 2026-09-08 · **Source:** Supermetrics MCP,
`ds_id="AW"`, `ds_accounts="7473953248"`, `timezone="America/Chicago"`
**Window requested on every pull:** `2024-01-01 → 2026-09-08` (data actually starts 2025-06-02).

This is the last Supermetrics harvest — the subscription ends 2026-09-09. Everything below is on disk.

---

## 1. What was pulled, and how

| Report | Supermetrics report type | Notes |
|---|---|---|
| Ad performance | `Ad` (report type 1) | Only Search campaigns have rows. PMax has none — see gap G1. |
| RSA creative text | `Ad` + `AdGroupAdAssetView` | All 15 headline / 5 description / 2 path fields. |
| Asset performance | `AdGroupAdAssetView` (report type 4) | `assetPerformanceLabel` exists **only** on this report type. |
| Campaign structure | `campaign_and_resource_get`, `campaign_detail_level="full"` | One call per campaign_id. |
| Recommendations / history | `resource_type="recommendations"` / `"history"` | |

**Method note worth keeping:** a time-segmented query (`Date`, `Yearmonth`, `Yearweekiso`) silently
drops ads that never served, *even with* `include_zero_impressions: true`. Ad `817157617842`
(Pediatrics, Removed, 0 impressions) appears only in an un-segmented query and in the
`AdGroupAdAssetView` pull. The enriched asset pull (`raw-ads-asset-performance-enriched.json`) is
therefore the authoritative ad inventory: it is the one export containing all **16** ads.

**Validation:** `ads-ad-performance-alltime.csv` was built by summing the daily pull, then checked
cell-by-cell against a separate un-segmented all-time query. All 16 ads × 6 metrics matched to
within 0.002 — **0 mismatches**. 8 spot-checked month/ad cells in the monthly CSV likewise matched a
separate `Yearmonth` query exactly. `Ctr` and `CostPerConversion` are recomputed from summed
clicks/impressions/cost/conversions (they are `is_non_aggregatable` at source and must not be averaged).

---

## 2. Files written

| File | Rows | What it is |
|---|---|---|
| `ads-ad-performance-alltime.csv` | 16 | One row per ad ever created. Lifetime metrics + first/last served date + days served. |
| `ads-ad-performance-monthly.csv` | 41 | Same, by `Yearmonth`. |
| `ads-rsa-text.csv` | 16 | **The creative library.** All 15 headlines, 5 descriptions, 2 paths, verbatim, per ad, + lifetime metrics. |
| `ads-asset-performance.csv` | 359 | Per-asset text, `assetPerformanceLabel`, metrics, and an `InCurrentCreative` flag. |
| `ads-asset-group-creative.csv` | 60 | PMax asset-group creative (headlines/descriptions/long headline/image URLs). Recovered from campaign JSON — see gap G1. |
| `ads-pmax-assetgroup-conversions-daily.csv` | 107 | PMax conversions by conversion action, per day, per asset group. |
| `ads-pmax-assetgroup-conversions-monthly.csv` | 12 | The same, rolled up. **Read this one.** |
| `campaign-settings-22767146837.json` | — | Leads-Search-1, full detail. |
| `campaign-settings-23888858069.json` | — | PNHdefense, full detail. |
| `campaign-settings-24032465476.json` | — | Leads-PMax-Video-1, full detail. |
| `campaign-settings-22625352639.json` | — | Campaign #1, full detail. |
| `campaign-negatives.csv` | 506 | Campaign, negative keyword, match type. |
| `campaign-keywords.csv` | 129 | Campaign, ad group, keyword, match type, ad-group max CPC. |
| `campaign-extensions.csv` | 95 | Sitelinks (with URL + both description lines), callouts, structured snippets, image asset URLs, call extension. |
| `campaign-adschedule-and-targeting.csv` | 87 | Budget, bidding, network, languages, ad schedule, device modifier, every location target, ad-group inventory. |
| `campaign-adschedule-bid-modifiers-history.csv` | 36 | The only surviving record of hour-of-day **bid modifiers** — see gap G3. |
| `ads-recommendations.json` | 4 | Google's open recommendations. |
| `ads-change-history.json` / `.csv` | 569 | Change log, both Google's and Supermetrics'. |
| `raw-*.json` | — | Verbatim tool output for every pull, kept so the CSVs can be rebuilt. |
| `build_ads_creative.py` | — | The script that produced every CSV. No data row was hand-typed. |

---

## 3. Key numbers

### Negatives per campaign (campaign level)
| Campaign | Negatives | Match types |
|---|---|---|
| **Leads-Search-1** | **466** | 453 phrase, 11 exact, 2 broad |
| PNHdefense-Website traffic-Search-2 | 11 | 10 phrase, 1 broad |
| Campaign #1 (PMax, paused) | 29 | 16 exact, 13 broad |
| Leads-PMax-Video-1 (PMax, paused) | 0 | — |
| **Total** | **506** | |

`CLAUDE.md` records 451 for Leads-Search-1 as of Sep 7 1:52pm. The live figure is **466** — 15 added since.

The API echoes the campaign-level negative list onto every ad group (6 identical copies of all 466).
Verified byte-for-byte identical, so `campaign-negatives.csv` records each negative once, at
campaign level. There are **no genuine ad-group-level negatives anywhere in the account.**

### Keywords per campaign per ad group
| Campaign | Ad group | Max CPC | Keywords | Match types |
|---|---|---|---|---|
| Leads-Search-1 | Women's Health & Hormones | $2.60 | 34 | 30 phrase, 4 broad |
| Leads-Search-1 | Men's Health | $1.30 | 31 | 14 phrase, 17 broad |
| Leads-Search-1 | Functional & Integrative Medicine | $1.90 | 17 | 12 phrase, 5 broad |
| Leads-Search-1 | Naturopath Near Me — Core | $2.50 | 15 | 11 broad, 3 phrase, 1 exact |
| Leads-Search-1 | Geo-Qualified — Hopkins & West Metro | $2.60 | 11 | 10 phrase, 1 exact |
| Leads-Search-1 | Pediatrics | $2.40 | 6 | 4 broad, 2 phrase |
| **Leads-Search-1 total** | | | **114** | |
| PNHdefense | Ad group 1 | $0.01 | 15 | 10 exact, 5 phrase |
| **Account total** | | | **129** | |

Max CPCs match the Sept 7 evening values in `CLAUDE.md` exactly. Geo-Qualified holds **11** keywords,
not the 10 recorded there.

### Non-standard approval status
Exactly one ad in the account is not plain `Approved`:

- **`812704389533` — "Approved (limited)"** · Leads-Search-1 / Women's Health & Hormones · status
  **Enabled** · ad strength Average · **2,866 impressions, 158 clicks, $372.43, 17.01 conversions**.
  This is the *single highest-spending live ad in the account* and it is running under a limitation.

Ad strength across the 16 ads: Good 4, Average 4, Excellent 3, **Pending 3**, **Poor 2**.
Poor: `817264858229` (Women's, Paused, $90.61) and **`817157424693` (Men's Health, still Enabled, $31.56)**.
The three "Pending" ads are all Paused or Removed.

### Best lifetime click-through rate
| Rank | Ad ID | CTR | Impr | Clicks | Cost | Conv | Where |
|---|---|---|---|---|---|---|---|
| 1 | `817156208814` | **36.00 %** | 25 | 9 | $3.36 | 0 | PNHdefense (brand) |
| 2 | `810768274448` | 16.86 % | 338 | 57 | $154.70 | 26.21 | PNHdefense (brand) |
| 3 | `817157424693` | 15.53 % | 206 | 32 | $31.56 | 2 | Leads-Search-1 / Men's Health |
| 4 | `762584793075` | 6.57 % | 10,785 | 709 | $1,834.76 | 253.02 | Leads-Search-1 / Ad group 1 (retired) |

The top two are brand-defense ads on the paused PNHdefense campaign — brand traffic, not comparable
to prospecting. `817156208814` at 36 % has only 25 impressions and is not a meaningful sample.

- **Best CTR on a non-brand ad: `817157424693`, 15.53 %** (Men's Health) — 2.4× the next-best
  non-brand ad. Its ad strength is **Poor** and it carries only 12 of 15 headlines.
- **Best CTR at ≥400 impressions: `762584793075`, 6.57 %** — the retired original "Ad group 1" ad,
  which alone accounts for $1,834.76 of lifetime spend and 253.02 conversions.

---

## 4. Things worth flagging

- **Leads-Search-1 daily budget is $15.00, not $10.** `CLAUDE.md` §3 records $10 as of Sep 7 1:52pm;
  the change history shows a `CAMPAIGN_BUDGET → amountMicros` update at **2026-09-07 14:10:06** by
  `pankanaturalhealth@gmail.com`. Open thread #1 in `CLAUDE.md` has been acted on, partially.
- **The account went dark for roughly seven months.** Leads-Search-1 served in Jul–Aug 2025, then
  **zero impressions from 2025-09-01 through 2026-03-31**, resuming Apr 2026. Confirmed independently
  at campaign level. Any "since launch" average that spans that gap is meaningless.
- **Lifetime CPA was far better in 2025 than in 2026.** From ad-level data: Jul 2025 $7.17,
  Aug 2025 $6.05, vs Jul 2026 $13.61, Aug 2026 $29.63, Sep 2026 (1–8) $102.47. Note this is the
  raw tracked conversion and is subject to the double-counting caveat in `CLAUDE.md` §4 — the 2025
  figures predate the Aug 2026 demotion of the second conversion action, so 2025 conversions are
  inflated and the true gap is smaller than it looks. Do not quote these across the boundary.
- **46 retired creative assets are recoverable, with lifetime performance, and exist nowhere else.**
  `ads-asset-performance.csv` keeps assets that have been edited out of the live ads
  (`InCurrentCreative = no`). The two strongest are descriptions retired from the original ad:
  - *"Personalized natural medicine for families. Women's health, heart care, pediatrics."* —
    9,692 impr, 599 clicks, **224 conversions**
  - *"Root cause medicine. Hormone therapy, gut health, heart program. Hopkins clinic."* —
    5,722 impr, 424 clicks, **154 conversions**

  Retired headlines with real volume include "Hopkins Naturopath" (2,303 impr / 64.5 conv),
  "Downtown Hopkins" (2,013 / 81), "Natural Medicine MN" (2,593 / 45.5) and "Holistic Family Care"
  (2,401 / 40). These are worth reading before writing any new RSA.
- **Every one of Campaign #1's 1,855 recorded PMax "conversions" was a page load.** Segmenting by
  conversion action (`ads-pmax-assetgroup-conversions-monthly.csv`) resolves the campaign's entire
  conversion history into four page-reach actions and four "Local actions" — and **nothing else**:
  `Page view (…/whypnh)` 1,090, `Begin checkout (…/schedule-an-appointment)` 677,
  `Page view (…/meet-dr-haley)` 54, `Page view (…/meet-dr-jacob)` 34, plus Local-actions rows that
  contribute 0 to `Conversions` and 56 to `All conversions`. **Zero bookings.** July 2025 alone shows
  1,682 "conversions" on 3,073 clicks — a 55 % conversion rate, which is the arithmetic signature of
  a page-load counter, not of patients. This is independent, historical confirmation of the
  measurement thesis in `CLAUDE.md` §4–§5, and it predates the Aug 2026 demotion of the second
  conversion action. Any historical comparison that treats Campaign #1's PMax numbers as leads is
  wrong by roughly three orders of magnitude.
- **Google's asset ratings are almost entirely unformed:** of 359 asset rows, 285 are
  "Pending information", 67 blank (all Descriptions), 5 "Learning stats", and only **2 are rated
  "Good"** — both headlines on the retired ad ("Dr. Panka Hopkins MN", "Twin Cities Holistic
  Doctors"). No asset anywhere is rated "Best" or "Low". At current volume Google is not producing
  usable asset guidance, so asset-label-driven pruning has nothing to act on.
- **Four of the 16 ads carry only 12 of 15 headlines** — `817157424693` (Men's, **Enabled**),
  `817157827140` (Pediatrics, **Enabled**), `817264858229` (Women's, Paused) and `817157617842`
  (Pediatrics, Removed). Two of those are live. Every ad in the account has 4 of 5 descriptions;
  **description slot 5 is empty account-wide**, all 16 ads.
- **The open recommendation list is short and unchanged:** one `MAXIMIZE_CONVERSIONS_OPT_IN`
  (declined on purpose — `CLAUDE.md` §6) and three `KEYWORD` additions. Google returns no text for
  which keywords, only "Add recommended keyword" ×3.
- Only two structured-snippet headers exist ("Types" on Leads-Search-1, "Service catalog" on
  PNHdefense) and both Search campaigns share the same 20 image assets and the same call extension
  (612-568-8382).

---

## 5. Gaps and failures — recorded, not silently omitted

**G1 — Performance Max has no *ad*-level or *per-asset* performance data. Mostly closed.**
`Campaign #1` (22625352639) and `Leads-PMax-Video-1` (24032465476) return zero rows in both the `Ad`
report and `AdGroupAdAssetView`, because PMax uses asset *groups*. I chased this down rather than
leave it open, and here is exactly what is and is not recoverable:

- **Creative text: recovered.** `ads-asset-group-creative.csv` holds all 3 asset groups
  ("Asset Group 1" on Campaign #1; "A doctor who listens" and "Functional labs & prevention" on
  Leads-PMax-Video-1) — 35 headlines, 12 descriptions, 3 long headlines, 7 image URLs, 3 logo URLs.
- **Asset-group totals: recovered.** Report type `AssetGroup` does carry metrics. Campaign #1 /
  Asset Group 1: **Jun 2025 — 9,011 impr, 313 clicks, $357.26; Jul 2025 — 91,432 impr, 3,073 clicks,
  $553.66.** Campaign #1 has exactly one asset group, so these are identical to its campaign-level
  numbers already in `ads-campaign-daily.csv`. Ad strength "Average"; campaign primary status reason
  is **"Campaign paused, Has asset groups limited by policy"** — it was policy-limited, worth knowing.
- **`Leads-PMax-Video-1` never served.** Zero rows at every grain. Created 2026-07-13, paused, no
  impressions ever. Its creative is preserved in `ads-asset-group-creative.csv` and is the only
  record that it existed.
- **Per-asset PMax metrics: genuinely unavailable, not merely unpulled.** Report type
  `AssetGroupAsset` (11) supports the text/structural fields but **no metrics whatsoever** —
  `Impressions`, `Clicks`, `Cost` and `Conversions` all exclude report type 11 in the AW field
  index. There is no query that returns per-asset PMax performance through this connector. Nothing
  is lost by the subscription ending; it was never obtainable.
- **`assetPerformanceLabel` does not exist for PMax.** It is available on report type 4
  (`AdGroupAdAssetView`) only, which covers Search ads exclusively.

**G2 — `asset_level` settings were not needed and not used.** The default
(`ASSET_LEVEL_DEFAULT`, "based on fields selection") resolved correctly to `AdGroupAdAssetView` and
returned `assetPerformanceLabel`, which is available on that report type *only*. I did not need to
try `ASSET_LEVEL_CAMPAIGN` or `ASSET_LEVEL_AD_GROUP`, so those two paths are untested here.

**G3 — `campaign_and_resource_get` returns the ad schedule WITHOUT bid modifiers.** All 22
day/hour rows come back with `day`, `start_hour`, `end_hour` and no `bid_modifier` key at all.
The per-row modifiers described in `CLAUDE.md` (Mon–Thu +15/−20/−10/+15, Fri −30/−35/−30/−10,
Sat +10, Sun −20, set the evening of Sep 7) are **not retrievable through this API surface and are
not in this archive.** The only modifier data that survives anywhere is in the Supermetrics change
log, which captured two earlier snapshots — 2026-07-17 (14 rows) and 2026-08-17 (22 rows, showing
the older Mon 1.0 / 0.75 / 1.0 / 1.15 pattern). Both are saved in
`campaign-adschedule-bid-modifiers-history.csv`. **The current modifiers exist only in the Google Ads
UI. Screenshot or export them by hand before relying on this archive for that.**

**G4 — Location bid modifiers are not exposed either.** `campaign-adschedule-and-targeting.csv`
captures all 10 location targets and the single device modifier (MOBILE 0.85), but the per-city
modifiers in `CLAUDE.md` (six cities at −30 %, three at +10 %) do not appear in any field the API
returns. Same remedy as G3.

**G5 — Geo target IDs could not be resolved to place names.** The nine `geoTargetConstants/*` IDs
(1019810, 1019888, 1019925, 1020070, 9051607, 9051855, 9052387, 9052691, 9189294) are preserved as
IDs. `resource_type="targeting_search"` with `type="location"` returned an empty result and a note
that location search is a Meta-only capability on this connector; there is no AW location lookup
here. These IDs are stable Google constants and can be resolved offline any time against Google's
public geo-targets CSV — no urgency, no data lost.

**G6 — Change history is heavily truncated on the Google side.** `resource_type="history"` at
`max_rows=10000` returned only **536** Google platform rows spanning **2026-08-26 → 2026-09-07**;
raising max_rows from 500 to 10000 added only 36 rows, so this is an API-side retention limit
(~2 weeks), not a paging limit. Supermetrics' own change list is smaller (33 rows) but reaches
further back — **2026-06-12 → 2026-08-17** — and is the only record of the July/August restructure.
**Everything before 2026-06-12 is already gone and was gone before this harvest began.**
Of the 536 Google rows, 498 are `drjake@pankanaturalhealth.com` and 2 are
`pankanaturalhealth@gmail.com` (both the Sep 7 budget change); 377 are `CAMPAIGN_CRITERION`
(negative-keyword work) and 111 `AD_GROUP_CRITERION` (keyword work).

**G7 — No `Ctr` or `CostPerConversion` at asset level.** Neither metric supports report type 4,
so `ads-asset-performance.csv` computes both from the returned impressions/clicks/cost/conversions
rather than taking them from source. The arithmetic is exact, but they are derived, not pulled.

**G8 — Ad-level data does not reach back to the account's start.** The `Ad` report returns nothing
before 2025-07-08 (Leads-Search-1's start). `Campaign #1` ran from 2025-06-02 and is invisible at
ad level for the reason in G1.

---

## 6. Provenance

Every CSV is regenerated by `build_ads_creative.py`, which reads only the `raw-*.json` and
`campaign-settings-*.json` files in this directory. Nothing was typed by hand except the three
smaller `campaign-settings-*.json` files and `ads-recommendations.json`, which the MCP returned
inline rather than saving to disk; each was written verbatim and then re-validated by parsing it
and re-counting keywords, negatives, sitelinks, callouts, snippets, images, headlines and
descriptions against the inline response. All counts matched.
