# NOTES: GA4 events, purchases and outbound clicks

Written 2026-09-08 to complete the analysis for the ten `ga4-*.csv` files that were captured at 19:47
before the responsible agent was killed by a rate limit. The data was saved; the analysis was not.
Everything below comes from the archived files, no subscription required.

---

## 1. `generate_lead` is a page-view trigger, not a lead. Definitively.

CLAUDE.md section 5 flagged this as an arithmetic impossibility: "95 events Jul–Sep, all on /contact,
26 from paid, none in Google Ads — but only 33 form_start and 1 form_submit, so 95 real submissions is
arithmetically impossible. Identify what fires this before trusting it."

Resolved. `generate_lead` fires on **page load of /contact**. The ratio of `generate_lead` to
`page_view` on that path is exactly 1.00 in every month the event has ever existed:

| Month | page_view on /contact | generate_lead | ratio |
|---|---|---|---|
| 2026-05 | 27 | 27 | 1.00 |
| 2026-06 | 38 | 38 | 1.00 |
| 2026-07 | 58 | 58 | 1.00 |
| 2026-08 | 36 | 36 | 1.00 |
| 2026-09 | 11 | 11 | 1.00 |
| **Total** | **170** | **170** | **1.00** |

Corroborating: `form_start` on /contact is 8 across all time, and `form_submit` on /contact is **0**.
A perfect 1:1 with page views across five months and 170 events, against 8 form starts, admits no
other explanation. The event was configured around May 2026 and has never measured a submission.

**Consequences.**
- The 54 lifetime `generate_lead` events from `google / cpc` are 54 contact-page **views**, not leads.
- The Monday guide's original step 1.4 proposed importing `generate_lead` into Google Ads as a
  **primary** conversion. That was withdrawn on compliance grounds. It must stay withdrawn on a
  second, independent ground: it would import contact-page views as leads — precisely the same error
  as the scheduling-page-load conversion this whole engagement has been unwinding.
- The Acuity addendum's suggestion to "check the contact inbox for spam before treating it as a lead
  count" is superseded. The events are not submissions at all, spam or otherwise. Corrected there.
- If real contact-form submissions ever need measuring, that is a new event to build, not this one.

## 2. GA4 holds about 2.5 years of Acuity booking revenue nobody knew was there

`ga4-purchases-detail.csv` reaches back to **December 2023** and records **$51,890** of purchase
revenue across 429 purchase events. Prior analysis in this engagement looked only at July–September
2026 and concluded there were "66 bookings, $7,753". The real archived series is far deeper.

Roughly $27,900 of that revenue falls in calendar 2024, a period nobody has examined at all.

Caveat that must travel with this number: GA4 purchase events overcount real Acuity bookings, because
one booking can fire up to three events. Treat the revenue as an indicative series and the event count
as an upper bound, not as a ledger. The Acuity export remains the booking truth.

### Free intro call versus paid appointment

Only purchases from 2026-06 onward carry an Acuity page path, so the split is only computable there.
Appointment type `41826455` is the free Introductory Phone Call, which the paths confirm.

| Month | Free intro call | Other appointment type | No path recorded |
|---|---|---|---|
| 2026-06 | 5 | 2 | 37 |
| 2026-07 | 12 | 0 | 27 |
| 2026-08 | 7 | 1 | 22 |
| 2026-09 | 1 | 0 | 5 |

400 of 429 lifetime purchase events carry no page path — these arrive through Acuity's server-side
integration. That is why source attribution fails for most bookings, and it is a second, independent
mechanism from the scheduler's domain jump already documented.

## 3. The intro-call CTA click tracking works in GA4 — and corroborates the August drop

`ga4-acuity-outbound-clicks.csv` records 60 click events on the off-domain intro-call URL
(`app.acuityscheduling.com/schedule.php?owner=27943652&appointmentType=41826455`) between June and
September 2026. So the click IS measured in GA4, contrary to the assumption that nothing tracks it.

Paid-search clicks on that CTA, by month: **July 9, August 2.** A 78% fall, in the same window that
like-for-like ad conversions halved (67 to 28) on identical spend and clicks. Small numbers, so this
is corroboration rather than proof, but it points toward a real behavioural change rather than a pure
measurement artefact. The August diagnosis should weigh it.

On the Google Ads "Intro Call Click" conversion action (id 7747774028) reporting zero: the action was
created around 2026-09-04, and total outbound clicks on that CTA since then are **1**, from direct
traffic, none paid. Zero conversions from roughly one eligible click is not evidence the tag is
broken. The Tag Assistant test CLAUDE.md calls for is still the right way to settle it.

## 4. Correction: the phone number IS tracked; the chatbot is not

CLAUDE.md section 5 states "`tel:+16125688382` and the Chatbase 'PNH Guide' chatbot have zero
tracking." Half of that is wrong.

- **Phone: tracked.** GA4 records `click` events with `linkUrl` of `tel:612.568.8382` (and a variant
  `tel:612-568-8382`), attributed to source/medium including `google / cpc`. They are GA4 events that
  were never imported into Google Ads, which is a different problem from being untracked. Note the
  two link formats — any future measurement must match both.
- **Chatbase: genuinely untracked.** It does not appear anywhere in the outbound-link data. Confirmed.

## 5. What the outbound-link data says about who is on the site

| Destination | Lifetime clicks | What it means |
|---|---|---|
| phr.charmtracker.com | 589 | Patient portal — existing patients |
| us.fullscript.com | 229 | Supplement dispensary — existing patients |
| instagram.com | 144 | Social |
| facebook.com | 105 | Social |
| app.acuityscheduling.com | 60 | Booking — prospects and patients |
| meet.google.com | 33 | Telehealth visits |

The two largest outbound destinations by a wide margin are both existing-patient tools. A substantial
share of site traffic is current patients doing administrative tasks, not prospects evaluating the
clinic. Any future "site conversion rate" that divides bookings by total sessions will understate
performance for exactly this reason, and should be computed against new-user sessions instead.

## 6. GA4 history is deeper than assumed

Event data reaches back to **February 2023** and purchase data to December 2023 — well beyond the
2025-06 horizon assumed earlier in this engagement, and far beyond Google Business Profile's hard
2025-03-08 wall. The archived GA4 files therefore contain the longest continuous record of this
business's online behaviour that exists anywhere outside Acuity.
