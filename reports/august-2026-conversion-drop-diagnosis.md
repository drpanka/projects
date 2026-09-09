# Why August 2026 produced half the conversions on the same spend

**Leads-Search-1 (`22767146837`) · diagnosis written 2026-09-08 · all figures from
`data/supermetrics-archive-2026-09-08/`, no live API calls**

---

## The fact under investigation

| | Jul 2026 | Aug 2026 | Sep 1–8 2026 |
|---|---|---|---|
| Cost | $626.29 | $651.84 | $102.47 |
| Clicks | 309 | 315 | 50 |
| Impressions | 6,296 | 5,534 | 1,335 |
| CTR | 4.91% | 5.69% | 3.75% |
| Conversions (primary metric) | 46 | 22 | 1 |
| **Like-for-like (Begin checkout, all conv, click date)** | **67** | **28** | **4** |
| GA4-import `schedule_appointment` (one per click) | 44 | 22 | 1 |
| **Conversion rate** | **14.9%** | **7.0%** | **2.0%** |

Same money, same clicks, half the conversions. With n ≈ 310 clicks in each month the
difference is significant at p < 0.001 (z ≈ 3.3), so this is not sampling noise.

---

## Verdict

**The drop is real. It is not a measurement artefact, and the fix is in targeting, not tagging.**

But it is *not* the kind of "real" the mix hypothesis predicts. The campaign did not reallocate
itself into bad segments. **The same segments converted at half the rate.** What changed is the
query territory that a shrinking set of broad-match keywords was reaching inside each segment.

Confidence: high on "real, not measurement". Medium on the specific mechanism.

---

## 1. Why measurement is ruled out

### The decisive test: an independent system with a control group

GA4 is a separate measurement path from Google Ads. It records how many sessions reach
`/schedule-an-appointment`. Split it by paid vs everything else, by week:

| Week beginning | Paid sessions | Reached scheduler | Rate | Non-paid sessions | Reached | Rate |
|---|---|---|---|---|---|---|
| 2026-06-29 | 32 | 5 | 15.6% | 139 | 16 | 11.5% |
| 2026-07-06 | 81 | 21 | 25.9% | 149 | 22 | 14.8% |
| 2026-07-13 | 95 | 12 | 12.6% | 210 | 40 | 19.0% |
| 2026-07-20 | 78 | 12 | 15.4% | 284 | 34 | 12.0% |
| 2026-07-27 | 109 | 16 | 14.7% | 180 | 42 | 23.3% |
| **2026-08-03** | **101** | **8** | **7.9%** | 205 | 56 | **27.3%** |
| 2026-08-10 | 70 | 6 | 8.6% | 146 | 43 | 29.5% |
| 2026-08-17 | 43 | 3 | 7.0% | 121 | 33 | 27.3% |
| 2026-08-24 | 37 | 1 | 2.7% | 195 | 18 | 9.2% |
| 2026-08-31 | 34 | 1 | 2.9% | 148 | 23 | 15.5% |

Paid halved. **Non-paid, on the same site, the same page, through the same tag, went up** —
14.1% in July to 18.1% in August, peaking near 30% in the first three weeks of August.

A broken tag cannot break for one traffic source and improve for the others. This single table
kills the measurement hypothesis.

### Four supporting checks

1. **Two separately-configured conversion actions fell in step.** `Begin checkout`
   (`7152843979`, WEBPAGE_CODELESS, many-per-click) went 67 → 28. The GA4 import
   `PNH2 (web) schedule_appointment` (`7635668327`, one-per-click) went 44 → 22. They share a
   page but not a configuration. Both halved.
2. **Behaviour changed, not just counting.** Paid engagement rate fell 63.7% → 57.0%;
   pageviews per paid session fell 2.03 → 1.62 (710/350 → 470/291). Bounce rate rose
   36.3% → 43.0%. That is people leaving faster, which no tag records by accident.
3. **The 2026-07-12 conversion-action switch is not the cause.** It sits three weeks before the
   break, and the like-for-like `Begin checkout` series — which spans the switch untouched —
   shows the same halving.
4. **Operator tag-testing pollution is absent from the window.** `ga4-self-referral-pollution.csv`
   records tagassistant/ads.google.com self-referrals in 2025-06, 2026-04, 2026-05 and 2026-06.
   **None in July, August or September 2026.** July's total was not inflated by Jacob's own tests.

### The confound worth naming, and killing

The tracked conversion is a page load of `/schedule-an-appointment`. A visitor who books through
the off-domain "Free Intro Call" CTA never loads that page and never counts. If August's paid
visitors had simply diverted to the Acuity CTA, measured conversions would fall with no real loss.

They did not. Acuity outbound clicks from `google / cpc`: **9 in July, 2 in August**. That route
fell harder than the page route. The confound is dead.

---

## 2. Why "the mix got worse" is also ruled out

Shift-share decomposition of the 7.90-point CVR fall, on every dimension the archive supports:

| Dimension | Mix effect | Within-cell rate effect | Share of fall that is within-cell |
|---|---|---|---|
| Network (Google search vs partners) | +0.49 pp | −8.39 pp | 106% |
| Device | −0.53 pp | −7.38 pp | 93% |
| Hour band | +2.42 pp | −10.32 pp | 131% |
| Geography (core west metro vs rest of MN) | −0.33 pp | −7.55 pp | 96% |
| Ad group | −0.71 pp | −7.19 pp | 91% |
| Match type | −0.61 pp | −5.54 pp | 90% |

**Mix never explains more than 0.7 points of a 7.9-point fall, and on two dimensions it points
the wrong way.** Every slice got worse on its own terms:

- Google search proper: 18.5% → 11.1% → 8.1% → 4.3% (half-month buckets Jul-a to Aug-b)
- Core west metro cities: 17.5% → 8.8%; rest of Minnesota: 12.0% → 5.4%
- Desktop: 19.4% → 4.7%; mobile: 13.4% → 7.2%
- Landing page `/`: schedule-page reach 14.0% → 6.4%
- Broad match: 12.6% → 6.1% → 0%

This is why "the traffic mix shifted" is the wrong frame. Reallocating the same budget to the
same segments in the same proportions would have produced roughly the same result.

---

## 3. When it broke

Two independent series agree on the same week.

| | Wk of Jul 27 | Wk of Aug 3 |
|---|---|---|
| Google Ads weekly CVR (ISO week 31 → 32) | 14.5% | 5.3% |
| GA4 paid schedule-page reach rate | 14.7% | 7.9% |

**The break is the week beginning Monday 2026-08-03.** A second, smaller step down follows in the
week of 2026-08-24 (2.7%).

The last account change before the break is **2026-07-31, 21:19–21:22 CDT**: targeting updated
(languages, negative keywords, location details), 3 ad groups updated, 1 ad group removed. A
second, similar batch landed 2026-08-03 18:18.

### What the timing rules out

- **The Aug 17 ad schedule is not the cause.** It went live two weeks *after* the break, and the
  weekly rate was already 7.9% and 8.6% before it. It plausibly contributes to the second step
  (week of Aug 24) but cannot explain the first.
- **The Jul 17 creative refresh is not the cause.** Six new RSAs went live 2026-07-17 and they did
  convert worse than the originals in July (8.2% vs 17.4% on 85 vs 224 clicks). But four of them
  were paused on 2026-08-12 and the decline continued — and in August the *original* ads fell to
  6.7% while the new ones held at 7.8%. The old creative degraded on its own.
- **The removed ad group is not the "Ad group 1" that mattered.** Leads-Search-1's `Ad group 1`
  last served in June 2026 with 4 clicks. Removing it on Jul 31 changed nothing.
- **The mid-August budget taper is not the cause of the *rate* fall.** Daily spend slid from
  ~$36 (Aug 1–7) to ~$8 (Aug 30–31), but the rate had already halved in the first week of August
  at full spend. Lower budget explains lower *volume* after Aug 15, not lower conversion rate.

---

## 4. What actually changed: the keyword base shrank while the budget did not

| | Jul 2026 | Aug 2026 | Sep 1–8 |
|---|---|---|---|
| Keywords that actually served (Leads-Search-1) | 96 | 71 | 41 |
| Broad match share of search-term cost | 62% | 74% | 82% |
| Distinct search terms triggered | 1,823 | 2,114 | — |
| Impressions | 6,296 | 5,534 | 1,335 |

The same money, chasing the same impression volume, through a keyword set that shrank by 26% and
then another 42%. **Nineteen keywords with 20 or more July impressions went to exactly zero in
August** — 1,722 impressions, 72 clicks, $173, 6.01 conversions. The ones that hurt are the
specific and local ones:

| Keyword | Ad group | Jul impr / clicks / conv | Aug |
|---|---|---|---|
| `holistic medicine Minneapolis` (broad) | Geo-Qualified | 191 / 7 / 3.50 | removed |
| `naturopathic doctor Minneapolis` (broad) | Geo-Qualified | 86 / 5 / 1.00 | removed |
| `natural medicine Minnesota` (broad) | Geo-Qualified | 244 / 4 / 0 | removed |
| `functional medicine doctor hopkins` (broad) | Geo-Qualified | 46 / 0 / 0 | removed |
| `integrated doctor` (broad) | Functional | 85 / 3 / 1.00 | removed |
| `natural doctor near me` (broad) | Core | 90 / 2 / 0 | removed |
| `natural pediatrician near me` (broad) | Pediatrics | 51 / 0 / 0 | still enabled, 0 impr |
| `naturopathic practitioner near me` (broad) | Core | 72 / 7 / 4.00 | 46 impr, 0 clicks |

The Geo-Qualified ad group — the local-intent one, converting at 18.1% in July — lost its two
best keywords and its impressions collapsed 836 → 224 → 22.

Meanwhile the surviving broad keywords absorbed the freed budget and matched much wider:
`functional medicine` 19 → 35 clicks, `functional medicine near me` 11 → 31, `pediatric holistic
doctor` 4 → 15, `alternative medicine near me` 0 → 10. August's paid-for queries include
`how to fix memory loss from depression` ($9.84), `erectile dysfunction uptodate` ($4.87),
`costco fertility program`, `dr heather stone diet`, `first choice wellness near me`,
`finding a doctor near me`.

**That is the mechanism: a shrinking keyword set on a constant budget forces broad match to reach
further into marginal query space, and it degrades every segment simultaneously — which is exactly
the fingerprint the shift-share found.**

---

## 5. The second, independent problem: search partners

| | Jul 2026 | Aug 2026 |
|---|---|---|
| Search-partner cost | $31.31 (5.0% of spend) | **$121.20 (18.6%)** |
| Search-partner clicks | 53 | 86 |
| Search-partner CPC | $0.59 | $1.41 |
| Search-partner conversions | 10 | 6 |
| Search-partner CVR | 18.9% | 7.0% |

Partner spend quadrupled. In the first half of August it took $87.46 of $458 — 19% of the budget —
at more than twice the July click price. This is separable from the keyword story and separately
actionable. Invalid clicks also rose, 35 of 344 (10%) in July to 50 of 365 (14%) in August, and
GA4 paid sessions ran *below* ad clicks in August (291 vs 315) having run above them in July
(350 vs 339).

---

## 6. The real-world check

If real bookings had also halved, the campaign story would be corroborated at the clinic. They did
not — but the check is weaker than it looks.

| | Jul 2026 | Aug 2026 |
|---|---|---|
| GA4 `purchase` events, all sources (booking proxy) | 39 | 30 |
| `(not set)` bucket (largest, unattributed) | 16 | 22 |
| Acuity intro-call outbound clicks, all sources | 34 | 12 |
| …of which `google / cpc` | 9 | 2 |

Total booking activity fell ~23%, not 50%, and the unattributed bucket actually rose. So the
clinic did not lose half its bookings. But 73% of bookings have unusable attribution and paid is
~3% of attributed bookings, so **this cannot isolate whether paid-sourced bookings halved.** It
rules out a clinic-wide collapse; it does not exonerate the campaign. Treat it as consistent with
the diagnosis, not as proof of it.

---

## 7. Hypotheses ranked

| Rank | Hypothesis | Verdict | Strength of evidence |
|---|---|---|---|
| 1 | **Real traffic-quality drift: shrinking keyword base → broad match reaching marginal queries** | **Supported** | Strong. Serving keywords 96→71→41; broad cost share 62→74→82%; distinct terms up 16% on fewer impressions; within-cell fall on every dimension; timing aligns with the Jul 31 / Aug 3 targeting edits. |
| 2 | Search partners over-serving | Supported, secondary | Strong and independent. 5%→18.6% of spend, CVR 18.9%→7.0%, CPC up 2.4×. Explains part of the loss, not all. |
| 3 | Structure: the Jul 31 targeting/keyword edit | Supported as trigger | Moderate. It is the last change before the break, but change history records only "targeting updated", not which keywords — so the causal link is inferred, not logged. |
| 4 | Delivery mix (device / hour / geo / network composition) | **Rejected as primary** | Shift-share: mix ≤0.7pp of a 7.9pp fall on every dimension. Real but marginal. |
| 5 | Creative: the six RSAs added 2026-07-17 | **Rejected** | New ads did convert worse in July, but four were paused Aug 12 and the *original* ads fell further than the new ones in August. |
| 6 | The Aug 17 ad schedule | **Rejected as primary** | Break precedes it by two weeks. May contribute to the second step at Aug 24. |
| 7 | Seasonality / August in health search | **Rejected** | Non-paid schedule-page reach rose to 27–30% during the exact weeks paid collapsed. Organic sessions were flat-to-up (232 → 248). |
| 8 | Brand campaign (PNHdefense) pause removing assisting traffic | **Rejected as an explanation of this number** | PNHdefense is a separate campaign; it is not in Leads-Search-1's 67→28. Brand-adjusting the GA4 paid rate changes July from 15.95% to 15.9% — no effect. It is a real ~5-conversion/month loss in its own right, not this one. |
| 9 | Measurement artefact | **Rejected** | Section 1. |

---

## 8. What I could not test from the archive

Named honestly, because Supermetrics access ends 2026-09-09 and these cannot be filled later:

- **Which specific keywords were paused or removed on which date.** `ads-change-history.csv`
  records `ChangedFields = targeting` and "Updated N ad group(s)" without naming the criteria.
  The keyword-level story in section 4 is inferred from before/after serving data, not from a log.
- **Whether search-partner traffic is bot-heavy.** No placement-level report exists in the
  archive, and the Google Ads API does not expose partner placements for search anyway.
- **Whether Acuity bookings sourced from paid actually fell.** Attribution breaks at the
  scheduler; the Acuity export is not in the archive and is the only booking truth.
- **Which RSA headline combinations Google served in each month.** `ads-asset-performance.csv`
  has lifetime asset performance, not date-level serving.
- **Whether the Women's Health ad's "Approved (limited)" status restricted delivery differently
  in August.** No policy-status history is available; the status is identical in both months, so
  it is unlikely, but it is untested.
- **Whether budget throttling changed which auctions Google entered.** Budget-lost impression
  share went 82% → 90%, but there is no auction-level data to test the selection effect.
- **The counterfactual.** One month-pair at ~310 clicks each is thin. Weekly CVR in 2026 has
  ranged 8.5% to 27.9% under a stable counting regime, so week-to-week volatility is real. The
  month-level difference is significant and GA4 corroborates it independently — but a third
  clean month would settle it, and September is not that month (41 serving keywords, $10/day).

---

## 9. What to act on first

**Act on hypothesis 1 — but most of the treatment is already applied.**

The broad-to-phrase conversion Jacob made on **2026-09-07** (Women's, Functional, Pediatrics,
Core and the kept Men's keywords converted to phrase; 26 keywords paused) is precisely the right
treatment for the diagnosed cause. It went in *after* the window analysed here, so nothing in
this report measures its effect, and September's numbers to date are pre-treatment.

**So the first action is restraint: leave the campaign alone long enough to read it.** Make no
further keyword, match-type or negative changes until roughly 2026-09-21 — two full weeks of
post-change data — or the effect will be unreadable.

**The one change worth making now, because it is independent of that readout:**

> **Turn off Google search partners on Leads-Search-1.**
> Google Ads → Campaigns → Leads-Search-1 → Settings → Networks → uncheck
> "Include Google search partners" → Save.

It cost $121.20 in August (18.6% of spend) at a 7.0% conversion rate against Google search's own,
with a click price 2.4× July's. On a $10/day budget that is roughly $2/day — a fifth of the
budget — going to the weakest inventory in the account. It is one checkbox, reversible in one
click, it does not touch the settled decision log, and it does not confound the phrase-match
readout because it is a different axis.

Second, after the readout window: **rebuild the Geo-Qualified ad group's local coverage.** Add
back, as phrase match, the local-intent keywords that stopped serving —
`"holistic medicine minneapolis"`, `"naturopathic doctor minneapolis"`,
`"natural doctor near me"`, `"naturopathic practitioner near me"` — and set that ad group's max
CPC high enough to win. It converted at 18.1% in July and its impressions have fallen 836 → 224 →
22. It is the highest-intent inventory the account has and it is currently starved.

---

## 10. The ten-minute test

**In GA4, confirm that the fall is in paid behaviour and not in the tag.**

1. GA4 property PNH2 (`353828960`) → **Reports → Acquisition → Traffic acquisition**.
2. Set the date range to **2026-07-01 – 2026-07-31**, and turn on **Compare** →
   **2026-08-01 – 2026-08-31**.
3. In the metric picker, add the key event **`schedule_appointment`** (or use the "Key events"
   column and select it from the dropdown).
4. Read two rows only: **Paid Search** and **Organic Search**. Divide key events by sessions
   for each, in each month.

**What confirms the diagnosis:** Paid Search falls from roughly 16% to roughly 7%, while Organic
Search *rises* from roughly 14% to roughly 19%. Same property, same tag, same page, same month —
one channel halves and the other improves. That combination is only possible if paid visitors
changed, and impossible if the tag broke.

**What would refute it:** if Organic Search fell by a similar proportion, the problem is on the
site or in the tag, and the whole targeting conclusion above is wrong.

While in the browser, the belt-and-braces version costs five more minutes and clears open thread
#2 at the same time: open the live site with **Tag Assistant** connected, click a "Free Intro
Call" button, and confirm the `Intro Call Click` conversion (`7747774028`) fires — and that it is
set to **Secondary**, not Primary.

---

## Source files

All under `data/supermetrics-archive-2026-09-08/`:

`ads-cpa-like-for-like-monthly.csv` · `ads-campaign-daily.csv` · `ads-campaign-weekly.csv` ·
`ads-campaign-monthly.csv` · `ads-conversions-by-action-daily.csv` ·
`ads-conversions-composition.csv` · `ads-conversion-actions.csv` · `ads-network-monthly.csv` ·
`ads-network-daily.csv` · `ads-device-monthly.csv` · `ads-device-daily.csv` ·
`ads-hour-dayofweek-monthly.csv` · `ads-geo-monthly.csv` · `ads-keywords-monthly.csv` ·
`ads-keyword-count-by-month.csv` · `ads-search-terms-monthly.csv` ·
`ads-ad-performance-monthly.csv` · `ads-change-history.csv` · `campaign-negatives.csv` ·
`campaign-settings-22767146837.json` · `ga4-schedule-page-reach.csv` ·
`ga4-schedule-page-reach-by-landing-paid.csv` · `ga4-events-by-source-daily.csv` ·
`ga4-landing-pages-paid-monthly.csv` · `ga4-landing-pages-monthly.csv` ·
`ga4-channels-monthly.csv` · `ga4-device-newreturning-channel-monthly.csv` ·
`ga4-purchases-monthly.csv` · `ga4-acuity-outbound-clicks.csv` · `ga4-self-referral-pollution.csv`

Method notes and the exact decomposition are in
`data/supermetrics-archive-2026-09-08/NOTES-verify-august.md`.
