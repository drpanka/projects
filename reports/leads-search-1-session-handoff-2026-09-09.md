# PNH session handoff — 2026-09-09

**This is the single current document. It supersedes every earlier plan in `reports/`.**
Read this first. The older reports remain as the record of how conclusions were reached, and two of
them contain conclusions that were later overturned — this file says which.

Supermetrics ended 2026-09-09. The full dataset is archived at `data/supermetrics-archive-2026-09-08/`
(about 150 files, 20 MB, committed) and needs no subscription. Start with its `README.md` and
`DATA-QUALITY.md`.

---

## 1. The one thing to carry forward

**Stop reading the Google Ads conversion column as a business signal.** It has now misled a reader in
four distinct, independently-verified ways:

1. Two actions counted the same page load as primary, double-counting through mid-2026.
2. Primary actions were switched mid-month on 2026-07-12, splicing July into two counting regimes and
   producing the false "$34.79 CPA" that drove a wrong diagnosis.
3. `generate_lead` fires on a page view of `/contact` and has never measured a form submission.
4. The conversion fires on reaching `/schedule-an-appointment`, so any booking path that bypasses that
   page is invisible — which is now the case.

All four are recorded in `DATA-QUALITY.md`. Acuity is the booking truth. Everything below assumes that.

---

## 2. Corrected picture of the last two months

Two claims that circulated widely are wrong, and one of my own corrections went too far.

**"The rebuild tripled CPA" — false.** Counted identically across both eras, July 2026 was the
account's best month ever: $9.35 per like-for-like conversion against $11.57 for July–August 2025.
The $34.79 figure divided a full month's spend by eleven days of conversions.

**"August collapsed" — half true, and the half matters.** Measured paid conversions fell 58% on
identical spend and clicks, and the paid conversion rate fell from 14.9% to 7.0%. That rate decline is
statistically real. But **bookings did not fall**: 29 booked in July, 28 in August, and the week the
break is pinned to, beginning 2026-08-03, produced 9 bookings — the second-strongest week of the
summer. There was no business emergency.

**My own correction overreached.** On seeing the booking data I attributed the whole drop to the new
intro-call links routing people past the tracked page. The diagnosis agent had already tested and
rejected a version of that: outbound clicks to the known off-domain Acuity call-to-action *fell* 9 to
2, rather than rising as rerouting would predict. More decisively, paid reach rate fell while
**organic reach rate rose** (roughly 14% to 19%) over the same weeks. A site-wide change to booking
buttons would have hit both channels. It did not.

**The best-supported reading is that both things happened.** Query composition genuinely drifted:
the ad-group rebuild spanning 2026-07-29 to 08-10 removed "Ad group 1" and moved click share from
booking-intent groups (Naturopath Core and Geo-Qualified, 21.2% of clicks down to 13.3%) toward
research-intent groups (Functional 30.1% to 41.6%, Women's 20.9% to 31.1%). Geo-Qualified, which
converted at 18.1% in July, saw impressions fall 836 to 224 to 22. Separately, the new booking links
are untagged, so some real activity is now invisible. Neither explanation alone fits all the evidence;
together they do.

**Why this matters for what you do next:** the treatment for query drift — the broad-to-phrase
conversion — was already applied on 2026-09-07, *after* the analysed window. September to date is
pre-treatment data. That is the entire basis for the hold in section 3.

---

## 3. What to do next session, in order

### Hold everything until about Sept 21
Make no further keyword, match-type, negative or bid changes. The Sept 7 phrase conversion is the
treatment being tested and two clean weeks are needed to read it. A trigger fires Sept 21 to collect
the readout. **This is the single most important instruction in this document**, because the standing
temptation is to keep optimising, and every change made now makes the readout unreadable.

### The two exceptions worth doing before then

**A. Turn off Google search partners.** Google Ads > Campaigns > Leads-Search-1 > Settings > Networks
> uncheck "Include Google search partners". It took $121.20 in August, 18.6% of spend, at 7.0%
conversion rate and 2.4x July's click price. On a $10/day budget that is a fifth of the money going to
the weakest inventory. It sits on a different axis from match type, so it will not confound the
readout. One click, reversible.

**B. Check Maple Grove and Shakopee bid modifiers.** Google Ads > Leads-Search-1 > Locations. These
are the #1 and #3 worst zero-conversion cities and were re-created as targets on 2026-09-07. If either
reads +10%, set it to -30%. Two minutes.

### Do not do these, despite earlier advice
- **Do not pause keywords.** Under a defensible threshold (able to serve, $20+ lifetime cost, 15+
  clicks, zero conversions), *zero* keywords qualify. 89% of the zero-conversion spend sits on criteria
  already paused or removed. Specifically do not pause `naturopathic doctor Minneapolis` — it has 7
  conversions and is Geo-Qualified's only keyword with history.
- **Do not launch a Functional Lab Testing ad group.** The campaign loses 67–90% of impressions to
  budget; a new group divides the same money to feed a theme with 1 conversion in 15 clicks. Instead
  add 8 phrase keywords to the existing Functional group (list in
  `data/supermetrics-archive-2026-09-08/proposed-lab-testing-adgroup.csv`), risking about $10/month.
- **Do not import `generate_lead`.** It measures page views.

### After the Sept 21 readout
Rebuild Geo-Qualified's local coverage as phrase match (`holistic medicine minneapolis`,
`naturopathic doctor minneapolis`, `natural doctor near me`, `naturopathic practitioner near me`) and
bid it high enough to win. It was the best-converting group before it stopped serving.

---

## 4. Google Business Profile — the free channel nobody was using

Verified over 550 days: 10,767 profile views, 1,768 actions, 711 website clicks, 981 direction
requests, 76 calls, and **zero bookings every single day**. 66% of profile search volume is discovery
intent, not brand, so it is finding new people. Correcting an earlier overstatement: profile views are
not comparable to ad clicks. Like-for-like it is 711 website clicks over 18 months, about 39/month,
against paid search's 1,383 over roughly 14 active months, about 99/month.

Ranked actions, all yours to perform:
1. **Look at the live profile and record whether a booking link already exists.** Nobody in this
   engagement has actually seen the profile's action buttons; the connector exposes no field for them.
   Every recommendation below is contingent on this.
2. **UTM-tag the profile website URL** with `?utm_source=gbp&utm_medium=organic`. Ten minutes, and
   nothing else on this list can be measured without it.
3. **Add a plain booking link** — the compliance memo (`reports/gbp-booking-link-compliance-2026-09-08.md`)
   concludes this is safe in a named configuration. Use
   `https://pankanaturalhealth.com/schedule-an-appointment?appointmentType=41826455` — your own domain,
   intro call preselected. **Never** enable Reserve with Google. The tell-tale that the wrong thing
   happened is a "Book Online" button or selectable appointment times appearing in search results.
   Expect the Bookings metric to stay at 0 forever; that is the correct reading and your ongoing
   confirmation you are not enrolled.
4. **Complete categories and the services list** — the listing has one category and no additional ones.
5. **Start a review request routine.** 15 reviews lifetime at 5.0, last one 2025-12-02, nine months ago.
6. **Remove the duplicate listing** (`10418367222074184209`) sharing your name, phone and website.

---

## 5. What was missed, and what is still genuinely open

**Missed and now fixed this session:** the `generate_lead` anomaly, flagged as "arithmetically
impossible" and never investigated; the claim that phone clicks were untracked, which was wrong; the
Monday off-schedule serving anomaly, which was a one-time $5.11 artifact; and the fact that GA4 holds
about 2.5 years of Acuity booking revenue ($51,890 back to December 2023, roughly $27,900 of it in
calendar 2024) that no analysis had examined.

**Missed and still open:**
- **Intro calls fell 16 to 11 in August while total bookings held at 29 and 28.** Smaller and more
  interesting than the question originally asked. A month of intake answers addresses it better than
  more analysis of existing data.
- **The new intro-call booking links are untagged**, so the next routing change will again arrive as a
  mystery. Tag them.
- **The "Intro Call Click" conversion action has never fired**, but only about one eligible click has
  occurred since it was created. Not diagnostic. The Tag Assistant test settles it in five minutes.
- **The Women's Health ad is "Approved (limited)"** on your largest ad group. Still unexplained; the
  reason is only visible by hovering the status in the Ads interface.
- **Calendar 2024 in GA4 has never been examined.** $27,900 of booking revenue sits there.
- **Counsel questions** from the compliance memo: whether the Minnesota Health Records Act reaches a
  registered ND, whether PNH is a HIPAA covered entity at all, and whether the Acuity account is
  HIPAA-enabled. Note the memo's sharpest point: the **existing** Acuity-to-GA4 integration already
  sends completed bookings with appointment type into Google. That is a bigger exposure than any
  booking link, and it is live right now.

**Structurally missed, worth naming:** this engagement twice produced a confident wrong diagnosis from
the same dataset, and both times the error was trusting a conversion metric whose definition had
changed underneath it. The archive now carries `DATA-QUALITY.md` specifically to stop a third.

---

## 6. Standing constraints — unchanged

Manual CPC. Budget $10/day, moved by clinician load. Jacob makes every account change himself. No
scheduling events to Google pending counsel. The protect list in `CLAUDE.md` section 7 stands, as does
the decision log in section 6.

## 7. Scheduled

- **Sept 21, 9am Central** — two-week readout. Rewritten today so it does not attempt Supermetrics.
- **Sept 30, 9am Central** — monthly Acuity export. Same rewrite.
