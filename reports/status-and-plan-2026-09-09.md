# PNH: complete status review and forward plan — 2026-09-09

Written after three changes Jacob reported: the Acuity Google Analytics integration is disconnected,
the general scheduling-page conversion actions stay, and the Google Business Profile has no booking
link — its link simply routes to the website scheduling page.

**This is now the current document. It supersedes `leads-search-1-session-handoff-2026-09-09.md`.**
Supermetrics ended 2026-09-09; the full dataset is archived at `data/supermetrics-archive-2026-09-08/`
and needs no subscription.

---

## 1. What the three changes settle

**Disconnecting Acuity's Analytics integration closes the top compliance item.** Google no longer
receives booking-completion events carrying appointment type and provider calendar. That was the
largest live exposure and the one thing the draft Privacy Policy did not plainly describe. It is
resolved, and the draft policy's statement that analytics tools are not configured to collect
scheduling form contents is now unambiguously accurate. Nothing further is needed there.

Three consequences to expect, none of them problems:

- `PNH2 (web) purchase` (id 7196843730) will never fire again. It has 3.21 lifetime conversions and
  is still marked primary. Set it to secondary or pause it, or it sits in the Conversions column
  permanently at zero.
- The `pankanaturalhealth.com / referral` sessions should decay toward zero over the next few weeks.
  That decay is the confirmation the disconnection took effect.
- GA4 can no longer see booking completions at all. The Acuity export is now the sole booking record.
  That was already the design; it is now the only option.

**The Google Business Profile finding needs correcting, and it is my error to fix.** I reported
"bookings genuinely zero across all 550 days" and framed the profile as a channel with no booking
path. That framing was wrong. Google only populates the `actions_bookings` metric for Reserve with
Google and similar booking-partner integrations. A plain website link never populates it, no matter
how many people click through and book. Those clicks are counted in `actions_website` — 711 lifetime,
about 39 a month.

So the profile is not missing a booking path. It has one, and it points at the scheduling page. What
is missing is *measurement* of it. The zero was never going to be anything else.

That collapses the Business Profile work to one item: **UTM-tag the link.** The booking-link
compliance memo is moot for the same reason — a plain URL to your own domain is not Reserve with
Google, which is precisely the distinction the memo drew. No compliance question remains there.

---

## 2. The double-counting problem, and the one setting that fixes it

You asked to have intro calls booked through the intro-call-specific link counted, without double
counting. Here is the current state, read from the archived conversion-action settings.

Four actions are currently **primary and included in the Conversions column**:

| Action | Counting | Lifetime | Status |
|---|---|---|---|
| `PNH2 (web) schedule_appointment` | One per click | 87.95 | Live, the real number |
| `PNH2 (web) purchase` | Many per click | 3.21 | **Now dead** — Acuity disconnected |
| `Intro Call Click` | One per click | 0 | Live, ~1 eligible click since created |
| `Lead form - Submit` | One per click | 0 | Google lead form, unused |

**The good news: `Intro Call Click` is already primary and already counted.** Nothing needs adding.
Its zero is not a broken tag; the action was created around September 4 and roughly one eligible click
has occurred since. That is zero opportunity, not zero performance.

**The real problem: "one per click" does not dedupe across actions.** It caps each action at one
conversion per ad click. It does not stop two different actions both firing on the same click. A
visitor who lands on the scheduling page and also clicks an intro-call link produces two conversions
in the Conversions column from one ad click. Google Ads has no cross-action deduplication. That is a
platform limitation, not a settings mistake.

There are exactly two ways out.

### The link is off-domain, which decides the design

You confirmed the intro-call link points to:

```
https://app.acuityscheduling.com/schedule/0081d9d2/appointment/41826455?appointmentTypeIds[]=41826455
```

That is `app.acuityscheduling.com`, not your domain. Two things follow, and together they settle it.

**The GA4 "one event, two triggers" approach I recommended earlier will not work.** Retracted. Your
Google tag lives in Squarespace code injection on pankanaturalhealth.com only, so nothing on the
Acuity page can fire a conversion. And now that you have disconnected the Acuity Analytics
integration, GA4 cannot see that page either — the integration was the only thing putting
`/schedule/0081d9d2/...` paths into your property.

**So the only measurable moment is the click itself, while the visitor is still on your site.** That
is exactly what `Intro Call Click` (7747774028) does: a page-level tag that fires on the outbound
click, before the visitor leaves. It is already primary, already counted, and it is the right and only
mechanism available. Nothing needs building.

**And the double-count risk is smaller than either of us feared.** The two actions fire on different
pages in different journeys:

| Action | Fires when | Where |
|---|---|---|
| `PNH2 (web) schedule_appointment` | the scheduling page loads | `/schedule-an-appointment` |
| `Intro Call Click` | an intro-call link is clicked | homepage, `/naturopathic-medicine`, `/contact` |

A visitor takes one path or the other. They only double count if someone loads the scheduling page
*and* clicks an intro-call link in the same ad click, which requires the two to coexist on one page.

**The one check that settles it:** open `/schedule-an-appointment` and look for a "Book an intro call"
button that points at the Acuity URL above. If there is none, the paths are mutually exclusive and
both actions can stay primary — you get both numbers with no meaningful overlap. If there is one,
either remove it from that page (the embedded scheduler already offers the intro call) or set
`Intro Call Click` to secondary. Two minutes, and it is the only thing standing between you and a
clean setup.

### Housekeeping worth doing under either option

- `Begin checkout (Page load .../schedule-an-appointment)` — **KEEP IT. I advised removing it earlier
  today; that was wrong and I am retracting it.** It is the only conversion action in the account with
  unbroken history across both campaign eras: 10 months of data from 2025-06 to 2026-09, spanning the
  seven-month dark period. Every valid cross-era comparison in this engagement rests on it, including
  the finding that July 2026 was the best month at $9.35 versus $11.57. Removing it ends that
  continuity going forward. It is already secondary, so it does not touch your headline number. It
  duplicates the scheduling-page load inside "All conversions" only, which is a column you can simply
  choose not to read. Leave it enabled and secondary, and know what it is.
- The three `Page view` actions on the doctor bios and `/whypnh` are already secondary. Leave them;
  they are harmless and occasionally informative.
- The Google-hosted local actions (directions, website visits, calls) are primary for their own goal
  but excluded from the Conversions metric. Correct as-is. Do not touch.

---

## 3. Everything else: current status

**The advertising picture is unchanged and stable.** July 2026 was the account's best month on a
like-for-like basis at $9.35 per conversion against $11.57 for July–August 2025. The apparent August
collapse was not a business decline — bookings held at 29 in July and 28 in August, and the pinned
break week produced 9 bookings, the second-strongest of the summer. What did fall is the paid
conversion *rate*, from 14.9% to 7.0%, and the best-supported cause is query drift from the ad-group
rebuild spanning July 29 to August 10, compounded by the new untagged booking links making some real
activity invisible.

**The treatment is already applied.** Your September 7 broad-to-phrase conversion addresses the drift
and landed after the analysed window. September is pre-treatment data.

**Four ways the Google Ads conversion column has misled a reader** are recorded in
`data/supermetrics-archive-2026-09-08/DATA-QUALITY.md`. Read it before quoting any conversion number
from before September.

---

## 4. Action plan, in order

### Now, this week

1. **Set `PNH2 (web) purchase` to secondary or pause it.** It cannot fire again. Two minutes.
2. **Fix the double count** — section 2, either the clean or the simple version.
3. **Check `/schedule-an-appointment` for an intro-call button** pointing at the Acuity URL. If absent, both conversion actions can stay primary. If present, set `Intro Call Click` to secondary. **Do not remove `Begin checkout`** — see section 2; it is the only continuous cross-era series.
4. **Turn off Google search partners.** Campaigns → Leads-Search-1 → Settings → Networks. It took
   $121.20 in August, 18.6% of spend, at 2.4 times July's click price. One click, reversible, and it
   sits on a different axis from match type so it will not confound the September 21 readout.
5. **Check Maple Grove and Shakopee bid modifiers.** Both were re-created as targets on September 7
   and are the worst zero-conversion cities. If either reads +10%, set it to −30%.
6. **UTM-tag the Business Profile website link** with `?utm_source=gbp&utm_medium=organic`. This is
   now the entire Business Profile measurement fix.

### Hold until about September 21

**Make no keyword, match-type, negative or bid changes.** The phrase conversion is the experiment
being run and two clean weeks are needed to read it. This remains the single most important
instruction in the plan, because the standing temptation is to keep optimising. A trigger fires
September 21 to collect the readout.

### Do not do these, despite earlier advice in this engagement

- **Do not pause keywords.** Under a defensible threshold — able to serve, $20+ lifetime cost, 15+
  clicks, zero conversions — *zero* keywords qualify. Specifically do not pause
  `naturopathic doctor Minneapolis`; it has 7 conversions and is Geo-Qualified's only keyword with
  history.
- **Do not launch a Functional Lab Testing ad group.** Add 8 phrase keywords to the existing
  Functional group instead (`proposed-lab-testing-adgroup.csv` in the archive), risking about $10 a
  month rather than splitting a budget-starved campaign.
- **Do not import `generate_lead`.** It fires on a page view of `/contact` and has never measured a
  submission.
- **Do not enable enhanced conversions**, and **keep both Performance Max campaigns paused.** Your
  draft Privacy Policy publishes both as deliberate choices; PMax uses audience signals by design.

### After the September 21 readout

Rebuild Geo-Qualified's local coverage as phrase match — `holistic medicine minneapolis`,
`naturopathic doctor minneapolis`, `natural doctor near me`, `naturopathic practitioner near me` — and
bid it high enough to win. It converted at 18.1% in July before its impressions fell 836 to 224 to 22.

### Business Profile, once the link is tagged

Complete the categories and services list (the listing has one category). Start a review-request
routine — 15 reviews at 5.0, last one December 2, 2025. File to remove the duplicate listing
(`10418367222074184209`), which shares your name, phone and website. The testimonials disclaimer in
your draft Legal Disclaimer already covers review solicitation.

---

## 5. What remains genuinely open

- ~~The intro-call destination URL~~ **ANSWERED 2026-09-09.** It is
  `app.acuityscheduling.com/schedule/0081d9d2/appointment/41826455?appointmentTypeIds[]=41826455` —
  off-domain, which is why it is invisible in the data and why the click-time tag is the only
  measurable moment. What remains open is verifying that tag actually fires.
- **Intro calls fell 16 to 11 in August while total bookings held at 29 and 28.** Smaller and more
  interesting than the question originally asked. The intake answers will address it.
- **The `Intro Call Click` tag has never been verified to fire.** Five minutes with Tag Assistant.
- **The Women's Health ad shows "Approved (limited)"** on your largest ad group, reason unknown; only
  visible by hovering the status in the Ads interface.
- **Calendar 2024 in GA4 has never been examined** — roughly $27,900 of booking revenue sits there,
  archived and readable with no subscription.
- **Counsel questions**, now narrowed to two by the draft policies and the disconnection: whether the
  Minnesota Health Records Act reaches a 147E registered ND, and whether PNH is a HIPAA covered
  entity. The Acuity Business Associate Agreement and the booking-link question are both resolved.

## 6. Standing constraints

Manual CPC. Budget $10/day, moved by clinician load. Jacob makes every account change himself. No
scheduling events to Google. Protect list in `CLAUDE.md` section 7 and decision log in section 6 both
stand.

## 7. Scheduled

- **Sept 21, 9am Central** — two-week readout on the phrase-match change.
- **Sept 30, 9am Central** — monthly Acuity export.

Both rewritten so they do not attempt Supermetrics.
