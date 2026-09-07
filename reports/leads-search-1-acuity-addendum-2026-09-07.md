# Leads-Search-1: Acuity addendum

Date: 2026-09-07. Companion to the review (2026-09-06) and the Monday action guide (2026-09-07) in this folder.
Sources: de-identified Acuity Scheduling export (86 appointments, booked 2026-05-05 to 2026-09-02, held 2026-06-01 to 2026-09-04), Google Ads weekly spend, GA4 property PNH2. The export itself is not committed to the repo.

## Bottom line

Booking activity does rise with ad spend. In the five weeks the campaign spent about $195 a week, self-booked intro calls ran 3.4 a week and new-patient first appointments 1.8 a week. In the eight weeks it spent about $38 a week, those were 1.5 and 0.9. At a $450 first visit that is roughly $210 of ad spend per incremental new patient, positive before any follow-up revenue. This is a weekly correlation over 14 summer weeks with small counts, not proof, but it points the same way as your perception.

The reason Google Ads and GA4 cannot show this directly is a measurement break, not a campaign problem: the moment a visitor enters the Acuity scheduler, GA4 starts a new session attributed to your own site or to direct. Not one booking completed inside the scheduler since June is attributed to paid search. Fixing that is a 30-minute job and is the next step.

## What the Acuity export shows

Bookings made since June 1: 80. Self-booked online: 58. Staff-booked: 22.

| Self-booked since June 1 | Count |
|---|---|
| Introductory Phone Call | 31 |
| First Appointment (incl. pediatric, virtual) | 9 |
| Follow-up (incl. pediatric, virtual) | 18 |

First appointments booked, all bookers: May 2, June 4, July 6, August 8. Intro calls are 26 for Dr. Haley and 10 for Dr. Jacob. Median lead time from booking an intro call to holding it is 2 days.

## Weekly spend against weekly bookings

Bookings are counted by the date they were booked, not the appointment date. Ad figures are Leads-Search-1 only.

| ISO week | Ad clicks | Ad spend | GA4 schedule-page sessions (paid) | Intro calls self-booked | First appts (all) | All self-bookings |
|---|---|---|---|---|---|---|
| 23 | 0 | $0 | 0 | 2 | 0 | 4 |
| 24 | 4 | $24 | 2 | 1 | 2 | 5 |
| 25 | 0 | $0 | 3 | 2 | 1 | 2 |
| 26 | 0 | $0 | 1 | 1 | 0 | 2 |
| 27 | 17 | $39 | 5 | 1 | 2 | 3 |
| 28 | 61 | $89 | 19 | 3 | 1 | 4 |
| 29 | 83 | $166 | 9 | 1 | 1 | 2 |
| 30 | 73 | $182 | 12 | 7 | 3 | 11 |
| 31 | 110 | $223 | 15 | 3 | 0 | 3 |
| 32 | 113 | $241 | 8 | 4 | 3 | 6 |
| 33 | 82 | $162 | 4 | 2 | 2 | 6 |
| 34 | 48 | $101 | 3 | 2 | 2 | 5 |
| 35 | 34 | $67 | 1 | 0 | 1 | 1 |
| 36 | 43 | $88 | 1 | 2 | 0 | 4 |

| Spend band | Weeks | Avg spend | Intro calls / week | First appts / week |
|---|---|---|---|---|
| Under $100 | 23 to 28, 35, 36 | $38 | 1.5 | 0.9 |
| $150 or more | 29 to 33 | $195 | 3.4 | 1.8 |

Correlation of weekly clicks with self-booked intro calls is 0.49; with all self-bookings 0.35; with first appointments 0.32. Positive, moderate, small sample.

Read carefully: the incremental new-patient number above assumes the difference between the two bands is the ads. Summer seasonality, the brand campaign that ran in June and July, and clinician availability all sit inside the same weeks. The intake question below is what separates them.

## Why Google Ads and GA4 cannot see it

The scheduler is embedded in an iframe. GA4 records those pages with host name `app.acuityscheduling.com` or blank, and the session that starts inside the scheduler is attributed to `pankanaturalhealth.com / referral` (74 sessions since June) or `(direct)` (25 sessions).

| Where the GA4 purchase event fired | Events since June 1 | Attributed to google / cpc |
|---|---|---|
| Inside the scheduler (/schedule/0081d9d2/...) | 28 | 0 |
| On the parent page (/schedule-an-appointment) | 34 | 4 |
| Acuity's own integration, no page | 55 | 0 |

GA4 logged 117 purchase events for 80 Acuity bookings, so a single booking can fire up to three. Purchase counts in GA4 overstate bookings by about 45 percent. On the plus side, 38 of the 39 dates with a self-booking also have a GA4 purchase event, so the event does track bookings of every type, intro calls included.

Of the 4 paid-search purchases GA4 does credit, 3 came from the brand campaign (PNHdefense, paused since late July after $158 spend and 66 clicks) and 1 from Leads-Search-1 (`hormone doctor near me`). The other 24 self-booked intro calls and first appointments in high-spend weeks have no source at all.

Consequence for the Monday guide: step 1.3 (make "PNH2 (web) purchase" primary) is still right, but it will undercount until the handoff is fixed. Do not judge the campaign by that column yet.

Appointment type 41826455: nearly every scheduler-path purchase carries it, and intro calls are the dominant self-booked type, so it is almost certainly the Introductory Phone Call. Confirm in Acuity under Appointment Types; the ID is in the URL.

## Fixing attribution, in order

1. GA4 cross-domain, 10 minutes. Admin > Data streams > PNH2 web stream > Configure tag settings > Configure your domains > add `acuityscheduling.com`. This lets the Google tag pass the session across to the scheduler when the visitor arrives by a link.
2. Send ad traffic through links, not the iframe, 15 minutes. The Google tag decorates links reliably and iframes unreliably. In Acuity, copy the direct scheduling link for the intro call (Appointment Types > the type > direct link; it will contain `appointmentType=41826455`). Point the three sitelinks that currently go to /schedule-an-appointment ("Free 10-Min Intro Call", "Become a New Patient", "MN & WI Telehealth Care") and the intro-call button on the home page at that link. Bookings then start in a session that still knows it came from google / cpc.
3. Test once, 5 minutes. Open the site with `?utm_source=test&utm_medium=test` appended, click through to the scheduler, book and cancel a test intro call, then check GA4 Realtime for a purchase event whose source is `test`. If it shows `pankanaturalhealth.com / referral`, step 2 is not complete.
4. Intake question, 5 minutes. Acuity > Intake Forms > add "How did you hear about us?" with options Google ad, Google search, referral from a friend or clinician, social media, other. Make it required on the intro call type. This is the only measure that survives every tracking gap, and it also separates the brand campaign and word of mouth from Leads-Search-1.
5. GA4 unwanted referrals, 3 minutes. Same screen as step 1, "List unwanted referrals": add `ads.google.com` and `tagassistant.google.com`. Both show up as purchase sources in June and are your own testing.

After steps 1 and 2, GA4 purchase becomes a usable booking signal by source, and the Google Ads import of it becomes meaningful. That is when the Conversions column starts telling the truth.

## Reporting cadence

Monthly, export the same de-identified appointment report from Acuity and drop it here. I pair it with weekly spend and produce three numbers: intro calls booked per $100 of spend, first appointments booked per $100, and, once the intake question has a month of answers, the share of new patients naming a Google ad. That replaces page-load conversions as the campaign's scorecard without changing anything about how you run it.

Two open items from the GA4 side: the /contact form fired generate_lead for 27 paid-search sessions in 90 days. Check the contact inbox for the same period to see how many were real inquiries versus spam before treating it as a lead count. And the "Intro Call Click" conversion in Google Ads has never fired; once the intro-call CTAs point at the direct Acuity link (step 2), that conversion can be retired or repointed.
