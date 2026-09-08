# PNH marketing channels — what each one cost and produced

**Companion to `master-monthly-channel-table.csv`. Written 2026-09-08, the last day of the
Supermetrics subscription. Nothing here can be re-pulled.**

You are probably reading this a year later with no memory of September 2026. Start here, then open
the CSV. Every figure below was recomputed from the archive CSVs in this directory and matches them
exactly; a verification pass found zero mismatches against `ads-account-monthly.csv`,
`ads-campaign-monthly.csv`, `gmb-monthly-metrics.csv`, `ga4-purchases-monthly.csv` and
`ga4-events-by-source-monthly.csv`.

**Blank means no data. Zero means a measured zero.** In this dataset the difference decides
conclusions — Business Profile bookings are a real, verified zero in all 18 months; Google Ads
spend before June 2025 is genuinely unknown.

---

## 1. Google Ads — account 7473953248

Lifetime in this account, 2025-06-02 → 2026-09-08: **$4,284.33, 124,756 impressions, 4,835 clicks.**

| Campaign | Type | Spend | Impressions | Clicks | Avg CPC | Status |
|---|---|---|---|---|---|---|
| Leads-Search-1 | Search | $3,215.35 | 23,950 | 1,383 | $2.32 | the only live campaign |
| Campaign #1 | Performance Max | $910.92 | 100,443 | 3,386 | $0.27 | paused |
| PNHdefense | Search (brand defense) | $158.06 | 363 | 66 | $2.39 | paused |

Two things distort every naive comparison of this account:

**The seven dark months.** Zero delivery account-wide from September 2025 through March 2026 —
243 days with no impressions. Verified as real zero spend, not a reporting gap. There is no
comparable prior September, and any "year over year" spanning that gap compares two separate
campaign lifetimes.

**The conversion metric was redefined four times.** The action Google was counting changed in
2025-07, again during the dark period, and again on 2026-07-12. As-reported conversions and CPA are
therefore *not comparable across months*. The table carries the regime letter for each month in
`data_quality_note`, and a like-for-like pair of columns computed on one constant basis
(Begin-checkout, all-conversions, click date) so the months can actually be compared:

| | Jul 25 | Aug 25 | Apr 26 | May 26 | Jul 26 | Aug 26 | Sep 26 (8 d) |
|---|---|---|---|---|---|---|---|
| Leads-Search-1 spend | $774.63 | $659.60 | $186.22 | $190.24 | $626.29 | $651.84 | $102.47 |
| like-for-like CPA | $11.07 | $12.21 | $11.64 | $9.51 | **$9.35** | **$23.28** | $25.62 |

**July 2026 was the account's best month, not its worst.** The widely repeated "$11.57 in 2025 vs
$34.79 in July 2026" comparison is an artefact of the 2026-07-12 metric splice and should never be
quoted again. The genuine unexplained problem is **August 2026**: the same spend ($652 vs $626) and
the same clicks (315 vs 309) as July, but like-for-like conversions halved, 67 → 28.

Since serving became continuous on 2026-07-03, the campaign has lost **82–90% of available
impressions to budget** and only 7–12% to rank (Jul 0.82 / Aug 0.90 / Sep 0.86 budget-lost share).
It is budget-constrained, not auction-constrained. Earlier 2026 months ran a different failure mode
— April lost 57% to budget, May 23%, June 6% — but delivery was intermittent then and the shares
are not comparable.

## 2. GA4 — property 353828960 "PNH2"

Lifetime, 2023-02 → 2026-09-08: **31,064 sessions** (counted from `session_start` per source, which
runs 0.5% below GA4's own `sessions` metric — see `NOTES-cross-source-bookings.md` §5). Paid search 10,207 · direct 9,296 ·
organic 7,317 · referral 4,138.

Last twelve months (2025-10 → 2026-09-08): **8,483 sessions** — direct 3,601, organic 2,616,
paid search 891, referral 1,327 (of which 560 in a single month were bot referrals from
wake-up-network.com, see below), other 48.

One clean cross-source check: those 891 paid-search sessions sit against **893 recorded ad clicks**
over the same twelve months. Ads and GA4 agree on traffic. They disagree on nothing except what
happened after the click.

**GA4 knows nothing before 2023-02**, and the paid-search sessions in 2023 and 2024 (5,824
of them, Mar–Sep 2023 and Feb 2024 – Mar 2025) came from a Google Ads account that is **not** the
one in this archive. Those sessions have no cost, no clicks and no keywords anywhere in this
directory. That money is unrecoverable.

Three pollutants are flagged per-month in the table and must be subtracted before reading:
- **Bot referral spikes** — 2024-02 (~750 sessions from `news.grets.store`, `static.seders.website`,
  `rida.tokyo`) and 2025-10 (560 from `wake-up-network.com`). Neither is a marketing result.
- **Operator self-referrals** — `tagassistant.google.com` (2025-06, 2026-04/05/06) and
  `ads.google.com` (2026-06/07/08) are Jacob's own tag tests and ad previews, and they carry
  purchase and schedule_appointment events with them.
- **`pankanaturalhealth.com / referral` is NOT junk.** It is the fingerprint of real bookings whose
  attribution was destroyed when the Acuity scheduler opened a new session on its own domain.

## 3. Google Business Profile

18 months, 2025-03-08 → 2026-09-08 (the connector cannot reach earlier; PNH's first 6.5 years on
Google are already unrecoverable):

**10,767 profile views · 1,768 total actions · 711 website clicks · 981 direction requests ·
76 phone calls · 0 bookings.**

Bookings are **zero in every one of the 18 months and every one of the 550 days.** That is a
measured zero, not missing data — the Business Profile has no booking link attached.

66% of the search volume that reaches the profile is geo/discovery intent ("naturopath near me"
shaped) and only 8% is brand. 15 lifetime reviews, 5.0 average, most recent 2025-12-02.
A **duplicate listing** (`10418367222074184209`) shares the name, phone and website with the live
one (`3326559683279742636`) but has no address and no traffic.

### Comparing Business Profile with Ads — like with like only

**Profile views are not ad impressions and must never be put in the same column.** A profile view is
a person already looking at the business; an ad impression is a line of text in a results page.
The only honest comparison is **click to click**:

| Last 12 months (2025-10 → 2026-09-08) | Business Profile | Google Ads |
|---|---|---|
| clicks to the website | 404 | 893 |
| cost | $0 | $1,939.18 ($2.17/click) |
| direction requests | 556 | no equivalent |
| phone calls | 44 | no equivalent (tel: link is untracked) |

The free profile delivered 45% as many website clicks as the paid account, plus 600 actions ads
cannot produce at all. It is not a substitute for search advertising — its 66% discovery-intent
mix means it is largely catching the same "naturopath near me" demand — but it is the largest
unmeasured asset in the account, and the zero-bookings figure is the cheapest thing on this page
to fix.

## 4. What is measured badly, and why

**Nothing in this archive can tell you which ad click became a patient.** The chain breaks in one
specific place. The "Free Intro Call" buttons pointed at `app.acuityscheduling.com`, off-domain,
where the ad tag does not exist. Acuity opens a new session referred by pankanaturalhealth.com
itself, which erases the ad click. Over the current campaign period (Jul–Sep 2026) paid search is 28% of site sessions and about 3%
of attributed bookings; 73% of bookings have unusable attribution. **That is a measurement failure, not a
performance failure**, and the gap has been consistent for the whole life of the account.

The tracked "conversion" is a **page load on `/schedule-an-appointment`** — interest, not a booking.
GA4 `purchase` is closer to the truth but is not a booking count either: before 2024-12 those events
were Squarespace store orders, from 2024-12 to 2026-05 they are a mix, and even in the clean period
one Acuity booking can fire up to three events, overcounting by roughly 45%. **Acuity's own export is
the only booking truth and it is not in this archive.**

A compliance decision made this week constrains the obvious fix: sending completed-booking events,
with appointment type, tied to a browser identifier, to Google Analytics or Google Ads was judged a
privacy risk, because Google will not sign a business associate agreement. Any future proposal to
close the attribution gap has to clear that bar first.

## 5. The three numbers worth tracking from here

1. **Acuity completed bookings per month, split intro call (type 41826455, $0) vs paid visit.**
   Exported by hand from Acuity. This is the only ground truth about revenue and the only number in
   this document that is not distorted by something. Nothing else on this page is a substitute.
2. **Leads-Search-1 like-for-like CPA — spend ÷ Begin-checkout all-conversions on click date.**
   The one Ads figure comparable across the whole history, because it holds the counting basis
   constant while the account's primary conversion action changed four times. Read it next to
   *search impression share lost to budget*, which has run 82–90% since July 2026 and is the reason
   volume, not efficiency, is the binding constraint.
3. **Business Profile website clicks per month** (not views). The free channel's only unit
   comparable to a paid click — 404 in the last twelve months against 893 paid ones — and the
   number that will move first if the missing booking link is ever attached.

## 6. Provenance

Built by `build_master_monthly.py` in this directory, reading only local CSVs — no API calls.
Rerunning it reproduces `master-monthly-channel-table.csv` byte for byte. Caveats that change
conclusions are in `README.md`; per-area detail is in the eight `NOTES-*.md` files; what this table
could not capture is in `NOTES-cross-source-bookings.md`.
