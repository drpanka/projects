# NOTES — the August 2026 conversion drop: method, caveats, and what I could not test

**Author: the August-diagnosis agent. Written 2026-09-08. I own this file and
`../../reports/august-2026-conversion-drop-diagnosis.md`. I appended to no other agent's notes and
wrote no CSV — every number below is derived from files already in this directory. No Supermetrics
quota was spent.**

The conclusion is in the report. This file is the working record: how each number was computed,
which files it came from, what is fragile about it, and which hypotheses could not be tested at all.

---

## 1. Headline conclusion, in one line

The Jul→Aug halving is **real, not a measurement artefact**, and it is **within-segment query
drift**, not a shift in the mix of segments. Break week: **2026-08-03**.

---

## 2. The load-bearing evidence, and why it is load-bearing

Everything rests on one structure: **an independent measurement system with a control group.**

GA4 is not Google Ads. It counts sessions reaching `/schedule-an-appointment` through its own tag,
its own sessionisation, its own channel grouping. Splitting it paid vs non-paid gives a natural
control — the non-paid rows are the same site, same page, same tag, same weeks.

Computed from `ga4-events-by-source-daily.csv`, weeks Monday-anchored, `session_start` as the
session count and `schedule_appointment` as the numerator:

| Week | Paid rate | Non-paid rate |
|---|---|---|
| 2026-07-06 | 25.9% | 14.8% |
| 2026-07-13 | 12.6% | 19.0% |
| 2026-07-20 | 15.4% | 12.0% |
| 2026-07-27 | 14.7% | 23.3% |
| 2026-08-03 | 7.9% | 27.3% |
| 2026-08-10 | 8.6% | 29.5% |
| 2026-08-17 | 7.0% | 27.3% |
| 2026-08-24 | 2.7% | 9.2% |
| 2026-08-31 | 2.9% | 15.5% |

Non-paid rising while paid halves is the whole argument. No single-channel tag failure exists that
does this.

**Fragility of this table.** `session_start` is a proxy for sessions, not GA4's `sessions` metric.
The cross-source agent measured that proxy at 0.5% low across the full history
(see `NOTES-cross-source-bookings.md` §5), so the bias is far below the effect size. The monthly
version of the same comparison, computed independently in `ga4-schedule-page-reach.csv` from a
different query, gives Paid 15.95% → 6.85% and non-paid 14.1% → 18.1%. Two builds, same answer.

---

## 3. Shift-share decomposition — the method

For each dimension, cells indexed *i*, clicks *c*, conversions *v*, share *s = c/Σc*,
rate *r = v/c*:

```
mix effect  = Σ_i (s_i^Aug − s_i^Jul) · r_i^Jul
rate effect = Σ_i  s_i^Aug · (r_i^Aug − r_i^Jul)
mix + rate  = CVR^Aug − CVR^Jul     (exactly, by construction)
```

Run over `ads-network-monthly.csv`, `ads-device-monthly.csv`, `ads-hour-dayofweek-monthly.csv`
(bucketed 00-06 / 07-09 / 10-14 / 15-16 / 17-19 / 20-23), `ads-geo-monthly.csv` (core-west metro
vs rest of MN vs other), `ads-keywords-monthly.csv` aggregated to ad group, and
`ads-search-terms-monthly.csv` by match type.

Result: mix contributes between −0.71 pp and +2.42 pp of a −7.90 pp move. On hour and network the
mix effect has the *wrong sign* — the composition change should have helped.

**Caveats on this method.**

- It uses the **primary conversions metric** (46 → 22), not the like-for-like `Begin checkout`
  series (67 → 28), because the segment files only carry `Conversions`. The primary metric is
  spliced on 2026-07-12 (Begin checkout Jul 1–11, GA4 import Jul 13–31). Both components are the
  same page load, so the splice does not bias the ratio much, but the absolute July figure is not
  a clean single-action count. The like-for-like series moves the same way (21.7% → 8.9%), so the
  conclusion does not depend on which metric is used.
- Cells with very few clicks (evening hours in July: 17 clicks) make the hour decomposition the
  noisiest of the six. It is also the one with the largest mix effect. Weight it least.
- Shift-share on observable dimensions cannot detect drift in an unobserved dimension. The
  finding is properly stated as "mix does not explain it *on any dimension the archive records*",
  which is what pushed me toward query-level drift as the residual explanation.

---

## 4. Timing: how the break week was fixed

Two series, built from different files, agree:

- `ads-campaign-weekly.csv`, ISO week 31 (Jul 27–Aug 2) CVR 14.5% → week 32 (Aug 3–9) 5.3%.
- The GA4 weekly table in §2, 14.7% → 7.9% across the same boundary.

`ads-change-history.csv` covers 2026-06-12 → 2026-09-07 (569 rows; the API window does not reach
further back). The last edit before the break is **2026-07-31 21:19–21:22 CDT**, three rows:
targeting updated (languages, negative_keywords, location_details), 3 ad groups updated, 1 ad
group removed. Then **2026-08-03 18:18**, two more rows of the same shape.

**This is the weakest link in the causal chain and I want it recorded as such.** The change history
records `ChangedFields` at the resource level. It says "targeting updated"; it does not say which
keywords, which negatives, or which locations. The keyword-level story in the report is inferred
from before/after *serving* data — 19 keywords with ≥20 July impressions and exactly zero August
impressions, most carrying status `removed` — not from a log entry naming them. The inference is
strong but it is an inference.

---

## 5. Hypotheses I actively falsified, with the killing evidence

| Hypothesis | Killed by |
|---|---|
| Tag broke / page stopped being measured | Non-paid reach rate *rose* in the same weeks (§2) |
| The 2026-07-12 conversion-action switch disturbed something | Like-for-like `Begin checkout` spans the switch untouched and halves identically |
| Operator tag-testing inflated July | `ga4-self-referral-pollution.csv` has zero rows in 2026-07 / 08 / 09 |
| Visitors diverted to the off-domain Acuity CTA instead of the page | `ga4-acuity-outbound-clicks.csv`: `google / cpc` 9 → 2. That route fell harder. |
| The Aug 17 ad schedule | Break precedes it by two weeks; rate already 7.9% and 8.6% |
| The six RSAs added 2026-07-17 | Four paused Aug 12; in August the *original* ads fell to 6.7% while the new ones held 7.8% |
| The ad group removed on Jul 31 | It was Leads-Search-1's dormant `Ad group 1` — 4 clicks in June, none in July |
| August seasonality in health search | Organic sessions 232 → 248, organic reach rate 13.8% → 19.4% |
| PNHdefense pause removed assisting brand traffic | Separate campaign, not in the 67→28. Brand-adjusting the GA4 July paid rate: (56−5)/(351−30) = 15.9% vs 15.95% unadjusted — no effect. |
| Brand or scheduling-intent queries got blocked by a new negative | Search-term report: 1 brand impression each month, 0 brand clicks either month; no negative in `campaign-negatives.csv` matches brand or scheduling language |
| Mid-August budget taper | Rate had already halved in Aug 1–7 at full spend ($36/day). The taper explains volume after Aug 15, not rate. |

---

## 6. What I could not test — and now nobody can

Supermetrics access ends 2026-09-09. These are permanently open unless the Google Ads UI still
holds them:

1. **Which keywords were paused/removed on which date.** Not in the change history at the
   criterion level. The Google Ads UI change history may still show it under
   Tools → Change history, filtered to Keywords, 2026-07-25 → 2026-08-10. Worth ten minutes if
   anyone wants the causal link nailed rather than inferred.
2. **Search-partner placements.** No placement report for search partners exists in this archive,
   and the Ads API does not expose them for search anyway. So "partner traffic is low quality" is
   supported by CVR and CPC, not by seeing where it came from.
3. **Whether paid-sourced *bookings* fell.** Attribution breaks at the scheduler. The Acuity
   export is the only booking truth and it is not in this archive. `ga4-purchases-monthly.csv`
   gives 39 → 30 all-sources, but the largest bucket is `(not set)` (16 → 22) and paid is 2 → 0.
   Two versus zero decides nothing.
4. **Date-level RSA asset serving.** `ads-asset-performance.csv` is lifetime, so I cannot see
   whether Google rotated toward different headlines in August.
5. **Policy-status history for the Women's Health ad.** It reads "Approved (limited)" in both
   months, so it is unlikely to be a change — but there is no history to confirm the limitation
   did not tighten.
6. **Auction selection under budget throttling.** Budget-lost impression share went 82% → 90%.
   Whether harder throttling systematically selected cheaper, lower-intent auctions is a real
   mechanism and there is no auction-level data anywhere to test it. I flag it as the most
   plausible untested alternative to the keyword-shrinkage story: both predict within-segment
   query drift, and the archive cannot separate them.
7. **The counterfactual month.** One pair of ~310-click months is thin. Weekly CVR in 2026 under
   a stable counting regime has ranged 8.5% (wk 29) to 27.9% (wk 28). The monthly difference is
   significant (z ≈ 3.3) and GA4 corroborates independently, but a third clean month would settle
   it — and September is not that month: 41 serving keywords, $10/day, and the broad→phrase
   conversion landed 2026-09-07.

---

## 7. Numbers a future reader is most likely to want

| Quantity | Jul 2026 | Aug 2026 | Sep 1–8 |
|---|---|---|---|
| Leads-Search-1 cost / clicks | $626.29 / 309 | $651.84 / 315 | $102.47 / 50 |
| Primary conversions / CVR | 46 / 14.9% | 22 / 7.0% | 1 / 2.0% |
| LFL Begin checkout | 67 | 28 | 4 |
| GA4 paid sessions | 350 | 291 | 35 |
| GA4 paid → scheduler | 56 (15.95%) | 20 (6.85%) | 3 (8.6%) |
| GA4 non-paid → scheduler | 124 (14.1%) | 132 (18.1%) | 18 (13.0%) |
| Paid engagement rate | 63.7% | 57.0% | — |
| Paid pageviews / session | 2.03 | 1.62 | — |
| Search-partner cost (share) | $31.31 (5.0%) | $121.20 (18.6%) | $9.53 (9.3%) |
| Search-partner CVR | 18.9% | 7.0% | 0% |
| Desktop clicks / CVR | 72 / 19.4% | 43 / 4.7% | 9 / 11.1% |
| Keywords actually serving | 96 | 71 | 41 |
| Broad share of search-term cost | 62% | 74% | 82% |
| Distinct search terms | 1,823 | 2,114 | — |
| Invalid clicks | 35 / 344 (10%) | 50 / 365 (14%) | — |
| GA4 purchase events, all sources | 39 | 30 | 6 |
| Acuity intro-call clicks (paid) | 34 (9) | 12 (2) | 1 (0) |

Per-ad-group CVR, July → August: Core 25.0% → 4.3% · Geo-Qualified 18.1% → 10.5% ·
Women's 18.3% → 7.1% · Pediatrics 16.0% → 15.0% · Men's 11.6% → 8.3% · Functional 8.8% → 5.3%.
Pediatrics is the only ad group that held.

Geo-Qualified impressions: 836 → 224 → 22. That collapse is the single clearest structural
casualty and the clearest thing to rebuild.

---

## 8. One thing I did not do, deliberately

I did not recommend any change that would confound the readout of the broad→phrase conversion
Jacob made on 2026-09-07. That change is the correct treatment for the diagnosed cause and it
needs roughly two clean weeks. The one action in the report — turning off search partners — sits
on a different axis and does not contaminate it.

All account changes in the report are written as steps Jacob performs himself.
