# PNH Google Ads: project brief and implementation plan

**Written 2026-09-09 to start a fresh conversation with no prior context.** Everything needed is in
this file or in the archive it points to. Read this first; it supersedes every other report in
`reports/`.

---

## 1. The business, in ten lines

Panka Natural Health (PNH), cash-pay naturopathic clinic, 901 1st St N Suite 901A, Hopkins MN 55343.
Founded 2018 by Drs. Jacob and Haley Panka, both registered NDs in Minnesota (Statute 147E) and
licensed in Wisconsin. Jacob runs all marketing and the ad account himself while carrying a patient
load, and **he makes every account change personally** — never propose that an assistant edit the
account.

Pricing: adult new patient $450 (2h), pediatric new patient $300, follow-up $225, pediatric follow-up
$148, **Introductory Phone Call $0 (10 min)**, Functional Health Report $150.

Positioning: "technically primary care but not traditional." Primary-care-seeker traffic is wanted.
No insurance billing; superbills provided; HSA/FSA accepted. NDs in Minnesota cannot prescribe.

Service lines: Women's Health & Hormones · Men's Health (urinary/hormonal, sleep, cognition,
performance — **not erectile dysfunction**) · Pediatrics · Cholesterol/Heart · Metabolic/Diabetes ·
Gut Health · Brain/Neuro · Functional Lab Testing.

Season: prime booking window is early September to the December school break. We are in it.

---

## 2. Systems

| System | Value |
|---|---|
| Google Ads account | `7473953248` |
| Google Ads tag | `AW-17146544733`, `allow_enhanced_conversions: false` (deliberate, see §7) |
| GA4 property | `G-C9PY6T1S90`, property ID `353828960`, named PNH2 |
| Tag manager | **None.** All site code via Squarespace Code Injection |
| Website | Squarespace 7.1 |
| Scheduler | Acuity, owner `27943652`, ownerKey `0081d9d2` |
| Intro call | Appointment type `41826455`, 10 min, $0.00 |
| Calendars | `7700282` Dr. Haley · `8024328` Dr. Jacob |

Campaigns: `Leads-Search-1` (`22767146837`) is the **only enabled** one. Paused: `PNHdefense`
(`23888858069`), `Leads-PMax-Video-1` (`24032465476`), `Campaign #1` (`22625352639`).

Campaign state: Manual CPC, $10/day, presence-only targeting on a 22-mile radius around Hopkins plus
10 location targets, ad schedule live with per-row modifiers, mobile −15%, six ad groups, 451
campaign-level negatives. Roughly 81–90% of impressions are lost to **budget**, only 4–16% to rank.
The auction would give this campaign several times its current volume at current bids.

---

## 3. Where things actually stand

**The campaign works.** Counted consistently across both eras, July 2026 was the account's best month
at **$9.35** per conversion against **$11.57** for July–August 2025. A widely repeated claim that the
2026 rebuild tripled cost per conversion is false; it divided a full month's spend by eleven days of
conversions. See §7.

**August was not a collapse.** Measured conversions fell 58% on identical spend and clicks, but
bookings held: **29 booked in July, 28 in August**, and the week the drop begins produced 9 bookings,
the second-strongest of the summer. Two things contributed: query composition drifted during an
ad-group rebuild spanning 29 July to 10 August, and new intro-call links routed people around the page
where the conversion fires. The second of those is what §4 fixes.

**Jacob has already applied the treatment** for the query drift — a broad-to-phrase match conversion
on 7 September. September is therefore pre-treatment data, and **nothing about keywords, match types,
negatives or bids should change until roughly 21 September** or the result cannot be read.

**Compliance is settled and clean.** Acuity's Google Analytics integration was disconnected on
9 September, so Google no longer receives booking events carrying appointment type and provider
calendar. That was the largest exposure and it is closed.

---

## 4. THE SOLUTION — implement this first

### The problem in one paragraph

Intro-call buttons on the site currently link **off-domain** to
`https://app.acuityscheduling.com/schedule/0081d9d2/appointment/41826455?appointmentTypeIds[]=41826455`.
The Google tag lives only on pankanaturalhealth.com, so the moment someone clicks, they leave every
measurement surface. Acuity then opens a fresh session referred by pankanaturalhealth.com itself,
which erases the ad click. The result: intro-call bookings are invisible, the conversion column
undercounts by an unknown margin, and a second conversion action had to be bolted on to catch the
click — which then risks double counting against the scheduling-page action.

### The fix: keep them on your own domain

Acuity's embed script forwards an appointment-type parameter from the parent page into the iframe.
So the existing scheduling page can open with the Introductory Phone Call already selected. No new
page is needed, which matches Jacob's stated preference.

**Change every intro-call link from:**
```
https://app.acuityscheduling.com/schedule/0081d9d2/appointment/41826455?appointmentTypeIds[]=41826455
```
**to:**
```
https://www.pankanaturalhealth.com/schedule-an-appointment?appointmentType=41826455
```

### Implementation, in order

**Step 1 — Test the URL before changing anything (5 min).**
Open `https://www.pankanaturalhealth.com/schedule-an-appointment?appointmentType=41826455` in a private
window. Confirm the embedded scheduler opens with **Introductory Phone Call** preselected. If it does
not, try `?appointmentTypeIds[]=41826455` instead. If neither preselects, stop and report back — the
rest of the plan changes.

**Step 2 — Judge the experience honestly (5 min).**
The reason the off-domain links were created in August was to make booking intro calls easier. Walk
the on-domain path end to end and decide whether it is genuinely worse. If the embed is clunky enough
to cost bookings, keeping the off-domain link and living with weaker measurement is a legitimate
choice — bookings matter more than measurement. Only proceed if the on-domain path is comparable.

**Step 3 — Repoint every intro-call link (20–30 min).**
Nine were known before August: homepage ×5, `/naturopathic-medicine` ×2, `/contact` ×2. Jacob added
more in early August; those locations are not recorded anywhere, so check every page edited then.
Squarespace has no global find-and-replace, so this is manual. Search each page's content for
`acuityscheduling.com`.

**Step 4 — Simplify the conversion actions (10 min).**
Once every link is on-domain, one action can carry everything. Google Ads → Goals → Conversions:

| Action | ID | Set to | Why |
|---|---|---|---|
| `PNH2 (web) schedule_appointment` | 7635668327 | **Primary**, count One | The only primary. Now catches intro-call bookers too. |
| `Intro Call Click` | 7747774028 | **Secondary** | Redundant once links are on-domain, but keep it — it will still fire if any off-domain link was missed, which makes it a useful detector. |
| `PNH2 (web) purchase` | 7196843730 | **Secondary** or pause | Cannot fire again; the Acuity integration is disconnected. |
| `Begin checkout (Page load …)` | 7152843979 | **Leave enabled, Secondary** | **Do not remove.** It is the only action with unbroken history across both eras (10 months, June 2025 to September 2026) and every valid cross-era comparison rests on it. |
| `Lead form - Submit` | 7151526666 | **Secondary** | Google lead form, never used. |
| Three `Page view` actions (bios, `/whypnh`) | — | Leave secondary | Harmless. |
| Google-hosted local actions | — | **Do not touch** | Primary for their own goal, already excluded from the Conversions column. Correct as-is. |

With exactly one primary action counted "One per click," double counting is impossible by
construction. That is the whole answer to the double-count question.

**Step 5 — Verify (10 min).**
Open the site with Tag Assistant connected, click an intro-call button, and confirm
`schedule_appointment` fires on arrival. This also finally settles whether the `Intro Call Click` tag
ever worked, which has never been tested.

**Step 6 — Watch the proof arrive (2 weeks, passive).**
In GA4, `pankanaturalhealth.com / referral` sessions should decay toward zero. That decay is the
confirmation the fix worked, because that referral was the fingerprint of the domain jump.

### What this fixes

Intro-call bookings become visible. The double count becomes structurally impossible. Ad-click
attribution survives to the booking page. The August measurement break closes. And it sends Google
nothing it does not already receive — just a page view on a page it already sees, with no appointment
type leaving the browser to Google.

---

## 5. The rest of the plan

### Also do now (safe, will not confound the 21 September readout)

1. **Turn off Google search partners.** Campaigns → Leads-Search-1 → Settings → Networks. It took
   $121.20 in August, 18.6% of spend, at 2.4× July's click price. One click, reversible.
2. **Check Maple Grove and Shakopee bid modifiers.** Both were re-created as targets on 7 September
   and are the worst zero-conversion cities. If either reads +10%, set to −30%.
3. **UTM-tag the Google Business Profile website link** with `?utm_source=gbp&utm_medium=organic`.
   This is the entire Business Profile measurement fix.
4. **Add the "How did you hear about us?" intake question** to the First Appointment forms as well as
   the intro call. Nine of twenty first appointments were booked without an intro call.

### Hold until ~21 September

**No keyword, match-type, negative or bid changes.** The phrase conversion is the live experiment.
This is the single most important instruction in the plan.

### Do not do these, despite earlier advice in this project's history

- **Do not pause keywords.** Under a defensible threshold (able to serve, $20+ lifetime cost, 15+
  clicks, zero conversions), zero keywords qualify. Never pause `naturopathic doctor Minneapolis` — 7
  conversions, the Geo group's only keyword with history.
- **Do not launch a Functional Lab Testing ad group.** Add 8 phrase keywords to the existing
  Functional group instead (`proposed-lab-testing-adgroup.csv` in the archive). ~$10/month risk.
- **Do not import `generate_lead`.** It fires on a page view of `/contact` and has never measured a
  submission.
- **Do not enable enhanced conversions.** Deliberate privacy setting, published in the draft policy.
- **Keep both Performance Max campaigns paused.** The draft policy states no remarketing or
  personalized advertising; PMax uses audience signals by design.

### After 21 September

Rebuild Geo-Qualified's local coverage as phrase match: `holistic medicine minneapolis`,
`naturopathic doctor minneapolis`, `natural doctor near me`, `naturopathic practitioner near me`. It
converted at 18.1% in July before its impressions fell 836 → 224 → 22.

Then Business Profile: complete categories and services, start a review-request routine (15 reviews at
5.0, last one 2 December 2025), and file to remove the duplicate listing `10418367222074184209`.

---

## 6. Open questions

- **Intro calls fell 16 → 11 in August while total bookings held at 29 → 28.** Unexplained. The intake
  answers will address it.
- **The Women's Health ad shows "Approved (limited)"** on the largest ad group; reason visible only by
  hovering the status in the Ads interface.
- **Calendar 2024 in GA4 has never been examined** — roughly $27,900 of booking revenue, archived.
- **Counsel:** whether the Minnesota Health Records Act reaches a 147E registered ND, and whether PNH
  is a HIPAA covered entity. The Acuity Business Associate Agreement and the Business Profile
  booking-link question are both already resolved.

---

## 7. Traps — read before quoting any number

This account's conversion data has misled careful readers **four separate times**. All four are
documented in `data/supermetrics-archive-2026-09-08/DATA-QUALITY.md`.

1. **Two actions counted the same page load as primary** through mid-2026, double-counting.
2. **Primary actions were switched mid-month on 12 July 2026**, splicing July into two counting
   regimes. This produced the false "$34.79 CPA" that drove a wrong diagnosis.
3. **`generate_lead` fires on a page view** of `/contact`, ratio exactly 1.00 across all 170 events.
4. **The conversion fires on reaching a page**, so any booking path bypassing it is invisible — which
   §4 fixes.

Also: the account was **dark from September 2025 through March 2026**, so any cross-era comparison
spans a seven-month gap. Impression share reported as exactly `0.0999` is Google's floor, not a
measurement. About 65 keywords sit in a removed ad group and still report "Enabled" while unable to
serve. And GA4 `purchase` events overcount real bookings by roughly 45%, because one booking can fire
up to three.

**Acuity exports are the only booking truth.** Google Ads conversions measure interest.

---

## 8. Where everything lives

- `data/supermetrics-archive-2026-09-08/` — the complete archived dataset, ~150 files, 20 MB. The
  Supermetrics subscription ended 9 September; **nothing here needs it**. Start with `README.md` and
  `DATA-QUALITY.md`.
- `reports/` — this brief supersedes all of them. The others remain as the record of how conclusions
  were reached; two contain verdicts later overturned, each marked with a correction.
- `CLAUDE.md` — context reference. Sections 6 and 7 (decision log, protect list) are binding.

**Protect list, never add as negative keywords:** test · testing · panel · labs · dutch · testosterone ·
low testosterone · adrenal fatigue · diabetes · cholesterol · weight loss · fertility · adhd · anxiety ·
depression · insomnia · sleep · menopause · perimenopause · pcos · hopkins · bare `treatment` ·
telehealth · virtual · primary care · estrogen · concierge · herbalist.

## 9. Standing constraints

Manual CPC — smart bidding declined deliberately while the tracked conversion is a page reach. Budget
$10/day, moved by clinician load. No scheduling events to Google. Jacob makes every change himself.

## 10. Scheduled

- **21 September, 9am Central** — two-week readout on the phrase-match change.
- **30 September, 9am Central** — monthly Acuity export.

Both are written to work without Supermetrics.
