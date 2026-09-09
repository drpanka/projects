# NOTES — Google Business Profile: sizing the opportunity, with the uncertainty left in

**Author: the GBP opportunity-sizing pass, 2026-09-08. Owns this file and
`gbp-opportunity-sizing.csv`. Do not append to another agent's `NOTES-*.md`.**

Built entirely from files already in this directory. **No Supermetrics quota was spent.**
Sources: `gmb-daily-metrics.csv` (550 rows), `gmb-monthly-metrics.csv` (19 rows),
`gmb-location-metadata.csv`, `gmb-reviews.csv`, `gmb-review-totals-lifetime.csv`,
`gmb-monthly-media-and-reviews.csv`, `gmb-search-keywords-bucket-summary.csv`,
`ga4-channels-monthly.csv`, `ga4-acuity-outbound-clicks.csv`,
`ga4-purchases-by-page-monthly.csv`, `ga4-outbound-links-monthly.csv`,
`ads-account-monthly.csv`.

The brief for this pass was "so what, in numbers Jacob can act on, without inventing precision."
Two of the five questions come back with an honest **"cannot be determined from this data"**, and
they are marked as such rather than filled in.

---

## 0. Three corrections to numbers already circulating in this engagement

**(a) The year-over-year decline is smaller than recorded.** `NOTES-gbp-metrics.md` reports
views −9.7% and actions −21.9% for Mar 8 – Sep 8. That window includes 2026-09-01 to 09-08, where
views are populated (81) but **every action metric reads 0 because of Google's reporting lag** —
the daily file shows normal views on Sep 1–4 with zero actions, and the 2025 side of the comparison
carries its full eight days of actions. The comparison is not like-for-like.

Re-run on the matched window **Mar 8 – Aug 31**, which ends where action reporting is complete:

| | 2025 | 2026 | Change |
|---|---|---|---|
| Profile views | 3,629 | 3,346 | **−7.8%** |
| Total actions | 665 | 536 | **−19.4%** |
| Website clicks | 273 | 231 | −15.4% |
| Direction requests | 365 | 281 | −23.0% |
| Phone calls | 27 | 24 | −11.1% |
| Action rate | 18.3% | 16.0% | −2.3pp |

The qualitative finding survives — **actions are falling about 2.5× faster than views** — but the
magnitudes are 2 points smaller than the ones in circulation. Use these.

**(b) `actions_bookings = 0` is not evidence of a missing booking link.** The compliance pass
established that Google defines `BUSINESS_BOOKINGS` as bookings made *via Reserve with Google*, and
that "performance data isn't available for custom links." Adding the link recommended below will
leave that field at 0 forever, by design. **Nothing in this file should be measured through that
metric**, and any future check that uses it will wrongly conclude the work failed.

**(c) The "3.4 self-booked intro calls a week" anchor in the task brief does not match the
archive.** GA4's intro-call purchase paths, divided by the archive's own ~45% overcount factor, give
roughly **3.4 / 8.3 / 4.8 intro calls per MONTH** for Jun / Jul / Aug 2026. If the weekly figure
comes from the Acuity export it supersedes this and every scenario below should be re-scaled up by
roughly 3×. **This is unresolved and it matters more than anything else here**, because clinic-wide
intro-call volume is the denominator that decides whether the central case below is a 40% lift or a
13% one. It is a ten-minute check in Acuity.

---

## 1. The trend, properly characterised

**Views are genuinely flat.** Eighteen complete months in a band of 497–765, mean 596, no trend in
either direction. October 2025 (765) is the only outlier.

**Actions fell and then came back.** The action rate (actions ÷ views) by month:

| Period | Action rate |
|---|---|
| Mar–Aug 2025 | 16.2% – 20.9% (mean 18.3%) |
| Sep 2025 – Jun 2026 | 11.6% – 20.9%, mostly 13–16% (trough: **Mar 2026, 11.6%**) |
| Jul–Aug 2026 | **17.4%, 20.3%** |

So the honest reading is not "the profile is converting worse over time." It is **"the profile had
a ten-month soft patch through the winter and has recovered to 2025 levels in the last two months."**
July and August 2026 are the two best action months since April 2025. A year-over-year headline of
−19.4% is real but it is dominated by the winter, and it is pointed the wrong way for a decision
being made in September.

The one series that is unambiguously and durably down is **direction requests**: 365 → 281 (−23%),
with a collapse to 18 in March 2026 against a run-rate of ~52. Website clicks recovered; directions
only partly did.

Per-month figures for all 19 months are in `gbp-opportunity-sizing.csv`, section `monthly_trend`.

**Last 12 complete months (2025-09 → 2026-08), the base for everything below:**
7,057 views · 1,103 actions · **438 website clicks (36.5/mo)** · 616 directions (51.3/mo) ·
49 calls (4.1/mo) · action rate 15.6%.

---

## 2. Are direction requests existing patients? **Not testable. Three attempts, all weak.**

The hypothesis is reasonable and it is not confirmed here. What was tried:

**Test 1 — day of week.** Clinic hours are Mon–Fri 09:00–17:00. If directions were mostly patients
navigating to a booked appointment, directions should be the *most* weekday-concentrated of the
three series. Over 542 days:

| Series | Weekday (Mon–Fri) share |
|---|---|
| Profile views | 79.8% |
| Website clicks | 82.0% |
| **Direction requests** | **74.0%** |

Directions are the *least* weekday-loaded series, not the most. Directions per day barely dip at the
weekend (Sat 1.58, Sun 1.69, against a Tue low of 1.22) while views drop 40%. That leans **against**
the pure-navigation story. It does not kill it — someone can look up the route on a Sunday for a
Monday appointment.

**Test 2 — the seven-month ad blackout.** Directions per view ran 8.14% across the six ad-dark
months (2025-10 → 2026-03) and 9.16% across the eight months with delivery. Correlation of monthly
directions against ad spend is r = −0.10 (p ≈ 0.7). A complete halt in paid acquisition did not move
directions. This shows the Business Profile is **decoupled from paid search entirely** — useful in
itself — but it does not separate patients from prospects, because website clicks barely moved
either (35.3/mo dark vs 41.1/mo running).

**Test 3 — correlation with existing-patient behaviour.** Monthly directions against patient-portal
outbound clicks (`phr.charmtracker.com`) r = −0.26; against Fullscript r = −0.23. Both are
indistinguishable from zero at n = 18 (p ≈ 0.3). Underpowered, and the proxies are poor: portal
clicks measure patients who reach the portal *through the website*, which is a minority of them.

**Verdict: no key exists.** A GBP direction request never touches GA4, never touches Acuity, and
carries no identifier. It cannot be joined to appointment volume from anything PNH holds.

**Why it does not matter for the decision at hand.** A direction request does not put anyone on a
scheduling page. Patient or prospect, it is not addressable by a booking link, a website change, or
anything else on the action list below. The defensible framing is not "directions are existing
patients" — that is unproven — but **"directions are not addressable."**

**So the acquisition-relevant number is 37 website clicks a month, not 92 actions a month.** That
conclusion holds under either hypothesis. One thing directions *do* establish: 981 of them in 18
months is evidence the profile is being surfaced to people physically near Hopkins, which supports
the visibility work (item 3 below), just not the booking-path work.

---

## 3. Sizing the booking-link opportunity — grounded in PNH's own funnel

### 3a. What those 37 clicks are worth today

Two ratios, both measured on this clinic:

- **Site session → intro-call CTA click.** Jun–Aug 2026: Organic Search **2.59%** (18 CTA-click
  sessions / 695 sessions), Paid Search 1.59%, Direct 0.71%. Organic is the right analogue for a GBP
  website click — a discovery-intent visitor landing on the site cold.
- **CTA click → completed intro call.** 59 click events → 24 intro-call purchase events = **41%
  raw**, or **28%** after the archive's stated ~45% purchase overcount. Independently corroborated
  by CLAUDE.md's 47 clicks → 17 bookings = 36% over a different window.

Multiply through: **36.5 GBP website clicks/month × (2–5%) × (28–41%) ≈ 0.2 to 0.75 intro calls a
month, central ~0.35.**

That is the finding worth stopping on. **The entire Business Profile website-click channel is
currently producing well under one booking a month** — roughly four a year. It is not a small
leak in a big pipe; it is a big pipe that terminates almost nowhere. That is the number a booking
link has to beat, and it is why the link is worth more than the visibility work.

### 3b. Three cases

A booking link removes both hops: profile → scheduler, instead of profile → homepage → find the
CTA → scheduler. PNH has never had one, so **there is no observed booking-button click rate to
anchor on.** That single unknown is what makes the range wide, and it is stated as an assumption in
every case rather than buried.

| | Assumption | Clicks/mo | Completion | **Net intro calls/mo** | **Per year** |
|---|---|---|---|---|---|
| **Low** | Booking button draws 10% of the website button's volume; a profile tap is less deliberate than a site CTA click, so completion is discounted to 15% | 3.7 | 15% | **+0.5** | **+6** |
| **Central** | 25% of the website button's volume, completing at PNH's own observed adjusted 28% | 9.1 | 28% | **+2.5** | **+30** |
| **High** | 50% of the website button's volume, completing at PNH's observed raw 41% | 18.3 | 41% | **+7.3** | **+88** |

(Net = gross minus the share of today's ~0.35 site-path bookings that simply move onto the new path
rather than being additional.)

**Sanity check, and the reason not to quote the midpoint.** The clinic books roughly 3–8 intro calls
a month today (or ~15/mo if the weekly figure in section 0c is right). The central case is a **30–50%
lift in clinic-wide intro-call volume from adding one button**. The high case would **more than
double it**. Treat the high case as a ceiling to falsify, not a target. If the true anchor is the
weekly figure, all three cases are proportionally smaller as a share of the base and the central case
becomes a modest ~15% lift — which would make it more plausible, not less.

**On money.** The intro call is $0. Converting these into revenue needs the **intro-call → paying
patient rate, which is not in this archive at all.** At an *invented* 1-in-3 and a $450 adult first
visit, the three cases are ≈ **$900 / $4,500 / $13,100 a year** in first-visit revenue, excluding
follow-ups. The 1-in-3 is doing all the work in that sentence. Jacob can replace it from the Acuity
export in ten minutes and should before quoting any dollar figure to anyone, including himself.

### 3c. The measurement trap

Because a merchant booking link is not Reserve with Google, **GBP will report zero bookings after
this change, exactly as it does now.** The only way to see whether it worked is to put a UTM on the
booking link and watch landings in GA4 — which is why the tagging step is ranked first below.

---

## 4. Sizing the review opportunity

**Well established, from the data:**

- **15 reviews lifetime, 5.0 average.**
- **Most recent review 2025-12-02** — 9.2 months stale as of today.
- **Organic acquisition ≈ 2.0 reviews/year.** Two independent estimates agree: 3 reviews in the
  18-month window, and 15 over ~96 months since the September 2018 opening (1.9/yr).
- All four individually retrievable reviews were replied to. One reply lagged 1,159 days (a 2023
  review answered in July 2026), so the back catalogue is being caught up.

**Established generally, but not from this data:** review count, recency, star rating and proximity
are inputs to local search ranking. That is domain knowledge, cited as such.

**Not establishable, and not claimed:** how much ranking or profile visibility would move. The test
was attempted — profile views in the months following each of the three reviews in the window
(Apr 2025: 621→667; Jun 2025: 603→598; Dec 2025: 519→602) are indistinguishable from month-to-month
noise. **At n = 3 the test cannot detect anything, which is not the same as there being nothing.**
Any number attached to "reviews → rankings → bookings" for this clinic would be fabricated.

**So size the input instead, which is the part Jacob controls.** Denominator: roughly **250–360
appointments a year** (GA4 purchase events Jun–Aug 2026, overcount-adjusted — indicative, not a
ledger; Acuity is the truth).

| | Assumption | New reviews/year | Count after 12 months |
|---|---|---|---|
| **Low** | asks after 25% of visits, 10% respond | **+8** | 23 |
| **Central** | asks after 50% of visits, 13% respond | **+20** | 35 |
| **High** | asks after 75% of visits, 20% respond | **+47** | 62 |

PNH has never run a request routine, so the response rate has no local anchor and these are
assumptions, not measurements.

**The change that is certain in all three cases is recency**: from a newest review 9 months old to a
continuously fresh profile. That is the review attribute that decays without action, and it is the
one that is conspicuously wrong today.

**One risk worth naming:** a 5.0 across only 15 reviews is a small sample, and adding volume can only
move the average down. That is a reason to ask well and ask satisfied patients, not a reason not to ask.

---

## 5. Ranked by expected value against effort

Ordering is deliberate and two of the positions are counter-intuitive; the reasons are given.

**1 — UTM-tag the profile's website URL. 10 minutes, one-time. Zero bookings directly.**
`gmb-location-metadata.csv` shows the website URL as a bare `https://pankanaturalhealth.com/`. GBP
traffic therefore arrives untagged and is invisible inside GA4's Organic Search bucket — **nothing
else on this list can be verified after the fact until this is done.** Use
`?utm_source=gbp&utm_medium=organic`, which isolates GBP while keeping it in the Organic Search
channel so the historical series stays comparable. It does create a deliberate break in GA4
attribution on the day it goes live; note the date.

**2 — Add a plain merchant booking link.** Target
`https://pankanaturalhealth.com/schedule-an-appointment?appointmentType=41826455`.
**10 minutes to add, 5 minutes to test.** Expected value **+6 to +88 intro calls a year, central
~+30** — the highest on this list and the smallest effort of the substantive items. Compliance is
already answered: a typed-in merchant link is safe; **Reserve with Google must never be enabled**
(Acuity Integrations → Set Up, or GBP → Bookings → Get started), because that routes patient
identity through Google. Tell-tale that it happened by accident: a **Book Online** button appears or
Google starts showing bookable *times*. Before adding it, open the URL yourself and confirm the
`appointmentType` parameter actually preselects the intro call.

**3 — Complete categories and the services list. 30–45 minutes, one-time. Not estimable in bookings.**
The live listing carries **one** category (Naturopathic practitioner) and **zero** additional
categories — verified, the field is empty. 66% of profile search volume is discovery intent, and
categories decide which discovery queries can surface the profile at all. **Sequenced after the
booking link on purpose:** on today's leaky path, +10% profile views is worth about **+0.04**
bookings a month; with a booking link in place the same +10% is worth about **+0.26**. Visibility
work pays roughly six times more once the path exists. Do them in that order.

**4 — Start a review request routine. 2 minutes per patient, ongoing forever. +8 to +47 reviews/year.**
The only recurring cost on the list, which is why it sits below three one-time jobs. Its strongest
argument is recency, not volume. Do not attach a booking number to it.

**5 — File to remove the duplicate listing (`10418367222074184209`). 30–60 minutes to file, then
weeks of waiting. Zero measurable traffic gain.** Ranked fifth on purpose. The duplicate has recorded
**zero views and zero actions in 550 days** — `gmb-monthly-by-location.csv` returns `NO_DATA` for
every month — so there is no traffic to recover, and "it dilutes ranking signals" is plausible but
entirely unmeasured here. Its real value is **risk removal**: it shares the name, phone and website
with the live listing (a guidelines violation), is categorised differently as "Medical clinic," has
no address, and nobody is watching it if it collects a wrong detail or a bad review. Worth doing —
just not on the promise of a traffic number.

**6 — Posting and photo cadence. Recurring, 15–30 min/week. Weakest evidence on this list.**
Three photos in 18 months (one in Jun 2025, two in Jun 2026). The GMB connector exposes **no post
metrics at all**, so this cannot be measured from any data PNH holds, before or after. Last on
effort-adjusted grounds, not because it is worthless.

---

## 6. What would collapse these ranges, cheaply

In rough order of how much uncertainty each removes per minute spent:

1. **Acuity export: intro calls per month, and intro call → paying patient.** Settles section 0c
   (the 3× denominator ambiguity) and turns every scenario in section 3 from a booking count into a
   dollar figure. Ten minutes.
2. **Look at the live profile and record whether a booking link already exists.** The compliance pass
   flagged this as unverified — the connector exposes no place-action-link field, so nobody in this
   engagement has actually seen the profile's action buttons. If a link is already there, item 2
   above is not an opportunity but a broken-path check. **Do this before anything else.**
3. **After the UTM goes on, one month of GA4 data** gives the real GBP session count and the real
   GBP → CTA click rate, replacing the 2–5% assumption in section 3a with a measurement.
4. **A single month of booking-link clicks** replaces the 10/25/50% assumption that drives the entire
   width of the section 3b range.

---

## 7. Files

- `gbp-opportunity-sizing.csv` — 53 rows, sections `monthly_trend`, `yoy_mar08_to_aug31`,
  `directions_test`, `observed_funnel`, `booking_link_scenario`, `review_position`,
  `review_scenario`, `action_ranking`. Every scenario row carries its assumption in the `basis`
  column and an `evidence` column that says plainly whether the number is observed, derived or
  assumed. **Read the `evidence` column before quoting any figure from it.**
