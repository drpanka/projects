# PNH: final data review before the Supermetrics subscription ends

Date: 2026-09-08. Written after archiving the full dataset to `data/supermetrics-archive-2026-09-08/`
(about 150 files, 20 MB, committed to this repo and no longer dependent on any subscription).

This document supersedes the September 7 forward plan on two points and confirms it on the rest.
Where it contradicts the analysis from the other session, the correction and its evidence are shown.

---

## 1. The headline correction: the campaign did not get three times worse

The claim in circulation is that the 2026 rebuild diluted the budget, evidenced by "July–August 2025
delivered 124 conversions at $11.57 CPA on 19 keywords; July 2026 delivered 18 at $34.79 on 83
keywords, at the same monthly spend."

**The $34.79 figure is an artifact of a mid-month change in what Google was counting.** On
2026-07-12 the account switched primary conversion actions. "Begin checkout" was counted for July 1
to 11 only; the GA4 `schedule_appointment` import was counted for July 13 to 31 only. The 18 is
eleven days of one action. Dividing a whole month's spend by eleven days of conversions produces a
CPA roughly three times too high.

Counted the same way in both eras — "Begin checkout" all-conversions, click date, the action that
existed throughout — the series is:

| Month | Spend | Clicks | Like-for-like conversions | Like-for-like CPA |
|---|---|---|---|---|
| Jul 2025 | $774.63 | 290 | 70 | $11.07 |
| Aug 2025 | $659.60 | 266 | 54 | $12.21 |
| **Jul+Aug 2025** | **$1,434.23** | **556** | **124** | **$11.57** |
| Apr 2026 | $186.22 | 68 | 16 | $11.64 |
| May 2026 | $190.24 | 81 | 20 | $9.51 |
| **Jul 2026** | **$626.29** | **309** | **67** | **$9.35** |
| Aug 2026 | $651.84 | 315 | 28 | $23.28 |
| Sep 2026 (8 days) | $102.47 | 50 | 4 | $25.62 |

July 2026 was the account's **best month ever** on a like-for-like basis: $9.35 against $11.57 for
the 2025 benchmark, on comparable spend and clicks. The rebuild did not raise cost per outcome.

Source: `ads-cpa-like-for-like-monthly.csv`, which reconstructs five distinct counting regimes
(labelled A through E) and identifies the July 12 splice.

### What IS real

August 2026 genuinely degraded. Same spend as July ($652 versus $626), same clicks (315 versus 309),
but like-for-like conversions halved, 67 down to 28. September is tracking at that lower level.

So there is a real problem, it began in August, and it is not explained by keyword count — the
keyword count did not change between July and August in any way that would do this. Candidate causes,
in the order I would test them: a tagging change on the scheduling page (GA4 shows scheduling-page
reach collapsing on similar traffic); August seasonality in health search; and the mid-July
conversion-action switch disturbing something upstream. This is the open question worth your
attention, and it is a different question from the one the dilution story asks.

### Two further corrections to the dilution argument

**The keyword counts compare different things.** Counting only keywords that actually served, in ad
groups that could serve: 14 in July 2025, 17 in August 2025, 102 in July 2026, 71 in August 2026, 41
so far in September. The 2025 figures are one ad group — "Ad group 1", which is removed today. So it
is 14 keywords in one ad group versus 102 across seven, not 19 versus 83.
Source: `ads-keyword-count-by-month.csv`.

**The two eras are not consecutive.** The account was completely dark from September 2025 through
March 2026 — seven months, zero impressions, zero spend. July 2025 and July 2026 are two separate
campaign lifetimes with a seven-month gap, not two points on a trend. Whatever quality-score and ad-
rank history the 2025 campaign had accumulated was gone before the 2026 campaign started.

**The impression-share argument is half right.** Values of exactly 0.0999 are Google's reporting
floor, not measurements: on those days the three shares sum to exactly 1.0000. But July 2025 did
carry genuine higher readings on several days (0.1169, 0.1275, 0.2090, 0.2955), so impression share
really was better then. What changed most is the failure mode, not the total: in July 2025 the
campaign lost 70% of impressions to **rank** and 18% to budget; in August 2026 it lost 90% to
**budget** and 7% to rank. Meanwhile the share captured barely moved — 4,780 of 36,269 available
impressions in July 2025 (13.2%) versus 5,534 of 44,324 in August 2026 (12.5%).
Source: `ads-impression-share-floor-analysis.csv`.

---

## 2. Google Business Profile: the claim holds, with one figure corrected and one added

Verified from 550 days of daily data, 2025-03-08 to 2026-09-08 (the connector will not return
anything earlier — the clinic's first six and a half years on Google were already unrecoverable).

| Metric | Full 18 months | Last 12 complete months |
|---|---|---|
| Profile views | 10,767 | 7,057 |
| Total actions | 1,768 | 1,103 |
| Website clicks | 711 | 438 (~37/month) |
| Direction requests | 981 | 616 |
| Phone calls | 76 | 49 |
| **Bookings** | **0** | **0** |

Bookings is zero in all 19 months and all 550 individual days. The connector does expose the field
and returns real integers beside non-zero values elsewhere, so this is a genuine zero rather than an
unsupported metric. The honest caveat: Google omits the bookings series entirely when no booking
provider is attached, and an absent series renders as 0, so "no bookings" and "no booking link
configured" look identical from this side. The latter is near-certain.

**Correction to the scale comparison.** Profile views and ad clicks are not the same unit and should
not be set against each other. The like-for-like comparison is website clicks: the profile produced
711 over 18 months, about 39 a month; paid search produced 1,383 clicks over the roughly 14 months it
actually ran, about 99 a month, for $3,215. Paid search delivers more site visits per month than the
profile does. The profile's advantage is that it costs nothing and also produces 981 direction
requests and 76 calls that paid search does not.

**Addition that strengthens the case.** I expected profile traffic to be mostly people who already
knew the name. It is not. Classifying 134 distinct profile search terms: 66% of estimated search
volume is geographic or discovery intent — "naturopathic doctor", "holistic doctor near me",
"naturopathic doctor near me", "functional medicine doctor near me" — against only 8% brand. The
profile is finding new people, and they arrive at a listing with no way to book.
Source: `gmb-search-keywords-classified.csv`, `gmb-search-keywords-bucket-summary.csv`.

**New finding: there is a duplicate listing.** Two Business Profile records exist. The live one
(3326559683279742636) has the Hopkins street address, category "Naturopathic practitioner", all
traffic and all 15 reviews. The second (10418367222074184209) carries the same name, same phone and
same website, but a different category ("Medical clinic"), no street address, service-area-only
configuration, and an older description. It returns no data for the entire 18-month window.
Duplicate listings that share a name, phone and website split ranking signal. Removing it costs
nothing measurable. Source: `gmb-location-metadata.csv`.

**Reviews are worse than reported.** 15 lifetime, 5.0 average — but the last review arrived
2025-12-02, nine months ago, and only three landed in the last 18 months. Every one has a reply, so
responsiveness is not the issue; asking is.

---

## 3. Where the "Functional Lab Testing has no keywords" claim lands

Real but small. Lab-testing intent is 4.2% of estimated profile search volume: "food sensitivity
test" and "food sensitivity testing near me" together account for roughly 72 estimated impressions
across 18 months, about four a month. That is a genuine unserved theme and it is cheap to add a few
phrase keywords for it, but it will not move the practice on its own, and the campaign is already
budget-limited. Treat it as a small addition when budget allows, not as a headline opportunity.

---

## 4. What this changes in the plan

| Prior position | Status |
|---|---|
| Concentrate keywords because dilution raised CPA | **Withdrawn.** July 2026 had the best like-for-like CPA in the account's history at 102 keywords. Pausing genuinely dead keywords is still fine housekeeping; do it for tidiness, not to fix CPA. |
| Restore budget toward $25/day in peak season | **Strengthened.** Budget-lost impression share is 86–90%, rank loss is 7%. The auction has roughly eight times the current volume available at current bids. |
| Add a Business Profile booking link | **Hold pending your compliance call.** See below. |
| Monday ad-schedule anomaly unverified | **Closed.** All off-schedule impressions fall on 2026-08-17, the day the schedule was created: 14 impressions, 2 clicks, $5.11, in the hours before it took effect. Zero since. |
| August CPA degradation | **New, and now the top analytical question.** |

### The booking-link compliance question is not resolved

The verifier assigned to this hit the session rate limit and never ran. I am not going to hand you a
compliance conclusion I did not verify. What I can say precisely: a plain appointment-link URL on the
profile and Reserve with Google are different mechanisms, and only the second transmits booking
transactions to Google. The profile's own "bookings" metric counts link clicks. That distinction is
the whole question, and it needs checking against Google's current documentation before you act.
Given your stance this week, treat it as a ten-minute question for your advisor, not a ten-minute fix.

---

## 5. Recommended order of work

1. **Diagnose the August drop.** Same spend, same clicks, half the outcomes. Everything else is
   secondary until this is understood. The archive has what you need:
   `ga4-events-by-source-daily.csv` and `ga4-purchases-detail.csv` will show whether the scheduling
   page stopped being reached or stopped being measured.
2. **Restore budget for the season.** The case is stronger now, not weaker. Peak booking window runs
   to the December school break.
3. **Remove the duplicate Business Profile listing.** Free, no downside, and you own both records.
4. **Ask for reviews systematically.** Nine months since the last one, on a 5.0 average.
5. **Resolve the booking-link question with your advisor**, then act on the answer either way.
6. Keyword and negative housekeeping from the September 7 plan — unchanged, but demoted in priority
   because it is not the CPA lever it was thought to be.

---

## 6. What did not get verified

The session hit its rate limit partway through. Eight of eleven archive agents finished; six
adversarial verifiers and both audit agents did not run. The archive itself is complete enough that
the missing agents' work can be done from the committed files with no subscription. Specifically
unverified: the compliance analysis of booking links, an independent reconciliation of the
zero-conversion keyword and dead-city lists against the post-September-7 live state, the
tag-assistant pollution quantification, and a data-integrity cross-check of the archive's internal
consistency. The conversion forensics, keyword counts, campaign history and all Business Profile
findings above did complete and are sourced to named files.
