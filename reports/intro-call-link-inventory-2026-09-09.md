# Intro-call link inventory — every link to change

Date: 2026-09-09. Method: full crawl of `pankanaturalhealth.com` (sitemap + link discovery),
42 pages fetched as rendered HTML, every `<a href>` on every page scanned for
`acuityscheduling.com` or the appointment type `41826455`. This is a complete site sweep,
not a spot check. It supersedes the "9 CTAs" figure in `CLAUDE.md` §5, which was inferred
from GA4 and undercounted.

**Replacement URL for every row below:**

```
https://www.pankanaturalhealth.com/schedule-an-appointment?appointmentType=41826455
```

## Summary

| | Links |
|---|---|
| Already repointed (homepage) | 6 |
| **Still pointing off-domain — to change** | **15** |
| Pages with no intro-call link | 31 |
| Total intro-call CTAs on the site | 21 |

Every one of the 15 remaining links uses the same old URL:
`https://app.acuityscheduling.com/schedule.php?owner=27943652&appointmentType=41826455`

## The 15 links to change

Nine pages. "Section #" is the count of Squarespace sections above the link, so #3 is
near the top of the page and a high number is far down.

| # | Page | Link text | Type | Where on the page |
|---|---|---|---|---|
| 1 | `/naturopathic-medicine` | Schedule a Free Introductory Phone Call | Button | §3, under **Our Services** |
| 2 | `/naturopathic-medicine` | Schedule a Free Introductory Phone Call | Button | §18, under **Pediatrics** (after the Men's Health block) |
| 3 | `/contact` | Book a Free Intro Call | Inline text link | §3, under **New to Panka?** |
| 4 | `/contact` | Free 10-Minute Intro Call | Inline text link | §3, under **Prefer to Talk It Through?** |
| 5 | `/mens-health` | Free Intro Call | Button | §3, hero — "Supporting men of all ages…" |
| 6 | `/womens-health-services` | Free Intro Call | Button | §3, hero — "Supporting people of all ages…" |
| 7 | `/womens-health-services` | Schedule a Free Intro Call | Button | §15, closing CTA after **Testimonials** |
| 8 | `/clinical-laboratory-tests` | Book a Free Intro Call | Button | §3, under **Functional Lab Testing** |
| 9 | `/clinical-laboratory-tests` | Book a Free Intro Call | Button | §5, "Learn more about our functional lab testing…" |
| 10 | `/cholesterol` | Free Intro Call | Button | §3, under **Natural & Integrative Cholesterol Support** |
| 11 | `/cholesterol` | Free Intro Call | Button | §24, under **Ready to understand your numbers?** |
| 12 | `/holistic-diabetes-care` | Schedule a Free Intro Call | Button | §3, hero |
| 13 | `/meet-dr-haley` | Free Intro Call | Button | §3, under **Dr. Haley Panka, ND** |
| 14 | `/meet-dr-haley` | Schedule an Introductory Phone Call | Button | §4, under **Healthy Aging + Breast Cancer Support** |
| 15 | `/meet-dr-jacob` | Free Intro Call | Button | §3, under **Distinctive Background** |

Two more URLs redirect into pages already on this list and need no separate visit:
`/cardiovascular-wellness-program` → `/cholesterol`, `/functional-health-report` →
`/clinical-laboratory-tests`.

## Already done

`/` (and its `/home` alias) — 6 links, all on the new on-domain URL:
"Free Intro Call", "Book a Free Intro Call", "Schedule one here", and three variants of
"book a free 10-minute intro call". Nothing left to change on the homepage.

## Pages confirmed clean

No intro-call link at all: `/schedule-an-appointment`, `/pediatrics`, `/whypnh`,
`/about-us`, `/faq`, `/prepare-for-your-visit`, `/followup-packages`,
`/dietary-supplements`, `/meal-plans-and-recipe-books`, `/patient-portal`,
`/pnh-fullscript`, `/legal-disclaimer`, `/blog`, and all 18 blog posts.

Worth noting: `/pediatrics` has no intro-call CTA and is a live service line in peak
back-to-school season. Adding one is an easy win, separate from this task.

## Three things this crawl turned up

**1. The `Intro Call Click` tag could never have fired on the new-format link.**
The snippet in Squarespace header injection matches an href only when it contains both
`acuityscheduling.com` *and* the literal string `appointmentType=41826455`. The URL you
have been sharing —
`app.acuityscheduling.com/schedule/0081d9d2/appointment/41826455?appointmentTypeIds[]=41826455`
— contains `appointmentTypeIds[]=41826455`, which is not `appointmentType=41826455`. The
condition fails. That is a sufficient explanation for the action's 0 lifetime conversions,
independent of whether the tag itself works.

It also means: once these 15 links are repointed on-domain, the snippet stops matching
anything at all. That is the intended end state — the on-domain page reach becomes the
conversion — but the `Intro Call Click` action (id 7747774028) should then be set
Secondary or paused rather than left enabled at zero, so it cannot be mistaken for a
broken tag later.

**2. The new-format URL appears nowhere on the website.** All 15 remaining links are the
old `schedule.php` format. So wherever you placed the new-format links in early August,
it was off-site. Places to check: the Google Business Profile appointment link, your email
signature, the Acuity confirmation and reminder emails, Instagram and Facebook bios, and
any newsletter. Those are outside this crawl's reach.

**3. The "Free 10-Min Intro Call" sitelink points at the bare page.** In Leads-Search-1 it
resolves to `/schedule-an-appointment` with no query string, so it lands on the general
scheduler rather than preselecting the intro call. Adding `?appointmentType=41826455`
makes the sitelink match its own promise. Same for the "Become a New Patient" sitelink if
you want that one to preselect a first appointment instead.

## Method notes

Rendered HTML was used, not raw source, so links injected by scripts or hidden behind
mobile-only blocks are included. The site-wide header snippet was stripped before matching
so its own reference to `acuityscheduling.com` did not create false positives on all 42
pages. Anchor counts per page ran 102–158, consistent with a full render rather than a
truncated fetch.

---

# VERIFICATION PASS — 2026-09-09, after the edits

Re-crawled every page that carried a link, plus the homepage, plus a live functional test
of the replacement URL and of the Acuity scheduler behind it.

## Link state: clean

| | Links |
|---|---|
| Pointing to the correct new URL | **21** |
| Still pointing off-domain to `acuityscheduling.com` | **0** |
| Malformed, typo'd, or pointing anywhere else | **0** |

All 21 are byte-identical to
`https://www.pankanaturalhealth.com/schedule-an-appointment?appointmentType=41826455`
— compared by exact string match, not by pattern, so a dropped `?`, a missing `www`, a
stray space or a truncated ID would all have failed.

Per page: `/` 6 · `/cholesterol` 2 · `/clinical-laboratory-tests` 2 · `/contact` 2 ·
`/holistic-diabetes-care` 1 · `/meet-dr-haley` 2 · `/meet-dr-jacob` 1 · `/mens-health` 1 ·
`/naturopathic-medicine` 2 · `/womens-health-services` 2.

All 15 rows in the checklist above are done. Nothing was missed and nothing regressed.

## Functional test: the links work

**1. The page forwards the parameter into the scheduler.** Loading
`/schedule-an-appointment?appointmentType=41826455` produces a scheduling block whose
iframe is:

```
https://app.acuityscheduling.com/schedule.php?owner=27943652&ref=sched_block&isInConfig=false&appointmentType=41826455
```

Control test — the same page *without* the query string produces
`...schedule.php?owner=27943652&ref=sched_block&isInConfig=false`, no appointment type.
So the parameter is doing the work, not a coincidence of default behavior.

**2. Acuity honors it.** Fetching that iframe URL directly returns a scheduler whose
`appointmentTypes` list contains exactly one entry — `Introductory Phone Call`, id
41826455, 10 minutes, $0.00, intake form 2309402. The rendered page asks only which
doctor, Haley or Jacob. The visitor never sees the full appointment-type menu.

**3. No UX regression versus the old off-domain link.** Acuity redirects
`schedule.php?...&appointmentType=41826455` to
`app.acuityscheduling.com/schedule/0081d9d2/appointment/41826455?appointmentTypeIds[]=41826455&isInConfig=false&ref=sched_block`
— the exact destination the August links pointed at directly. Same scheduler, same
preselection, same number of clicks to book. The only difference is that the visitor now
passes through your domain first, where the tag can see them.

## What this changes for measurement

The booking now begins on `/schedule-an-appointment`, so `PNH2 (web) schedule_appointment`
fires with the paid-search session still attached. The self-referral fingerprint —
`pankanaturalhealth.com / referral` with $0.00 revenue — should decay from here. Give it
about two weeks of data before judging.

One consequence to act on: the `Intro Call Click` snippet in header injection fires only on
hrefs containing `acuityscheduling.com`. Zero links now match, so that action
(id 7747774028) can never record anything. It is not broken — it is obsolete. Set it
Secondary or pause it so a future reader does not mistake its permanent zero for a
tracking failure.

## Incidental findings

- The Acuity account has `isHipaa: true` set. Worth knowing when the compliance question
  comes back up.
- The intro-call intake form (2309402) already asks **"How did you find out about Panka
  Natural Health?"** — optional, free text. That is the attribution question from the
  Acuity addendum, already live on this appointment type. It is still absent from the
  First Appointment forms, which remains open.

## Scope of this pass

Re-fetched live: the 9 pages that had links, the homepage, and the schedule page with and
without the parameter. The other 31 pages were confirmed link-free in the crawl earlier
the same day and were not edited since, so they were not re-fetched.
