# Google Business Profile booking link: does adding one expose patient scheduling data to Google?

**Prepared for:** Dr. Jacob Panka, Panka Natural Health (PNH), Hopkins MN
**Prepared by:** Claude Code, at Dr. Panka's direction
**Date:** 2026-09-08
**Status:** Standalone memo. Intended to be readable by an attorney or privacy advisor with no prior context on this engagement.

---

## 1. The question put to me

A recommendation circulating in this engagement reads:

> "Google Business Profile has no booking link and it is the clinic's biggest free channel. Acuity
> integrates with Google's booking link; paste the `appointmentType=41826455` URL straight in.
> Ten minutes, free, do it today."

That sentence quietly merges two different Google products. One is a hyperlink. The other is a data
integration in which Google itself takes the booking and transmits the patient's identity to the
scheduling vendor. Whether they are separable is the whole question, because:

- If they are separable, adding a link is a low-exposure marketing change.
- If adding a link enrols the clinic in the integration, then Google would begin receiving
  appointment-level scheduling activity for a health care practice — the exact thing this
  engagement ruled out this week, on the ground that Google will not sign a business associate
  agreement.

This memo establishes what each mechanism actually does, with citations, and gives options with
their respective exposures.

**Bottom line up front: the two are separable, and they are separated by an affirmative act that
only Dr. Panka can perform.** A plain booking URL is a displayed hyperlink and nothing more; it
returns no booking outcome to Google and, per Google's own documentation, generates no performance
data at all. Reserve with Google is a distinct integration requiring setup inside Acuity plus
Google's approval. Recommendation: **safe in a named configuration** (Section 8).

---

## 2. Correcting the premise before acting on it

Two factual claims in the recommendation do not survive checking.

**"Google Business Profile has no booking link."** This is unverified. The Supermetrics Google
Business Profile connector exposes 126 fields, none of which is a place-action or booking link
(`gmb-location-metadata.csv` carries address, phone, category, place ID, hours, description and
website URL — no action links). The archive therefore cannot tell us whether a booking link is
present. The evidence people have been citing for its absence is the **Bookings = 0** metric, and
Section 4 shows that metric proves nothing of the sort.

*Action: Dr. Panka should look at the profile directly (Google Search → Edit profile → Bookings)
before assuming the field is empty.*

**"It is the clinic's biggest free channel."** Directionally supportable but state it precisely.
Over 550 days (2025-03-08 to 2026-09-08) the profile produced 10,767 views and 1,768 actions:
981 direction requests, 711 website clicks, 76 calls, 0 messages, 0 bookings. It is a real channel.
Whether it is the *biggest* free channel was not tested against organic search in this archive.

---

## 3. Mechanism 1 — the plain booking / "Appointment links" field

### What it is, technically

Google's current help page, *Manage your local business links*, describes it as a link attached to
a button:

> "Your Business Profile can include 2 types of links that make it easier for customers to learn
> more about your business. They can also take action directly from your profile on Google Maps or
> Search... You can also add up to 10 links per category. Links can help customers: Book an
> appointment. Make a reservation. Place a food order. Place a shopping order."

> "Select **Add link**... **Enter the URL that you want to link to the button**. Select **Save**."

— Google Business Profile Help, *Manage your local business links*
(https://support.google.com/business/answer/6218037)

The underlying data model confirms this is a URI, not an integration. In the Business Profile
Place Actions API, a `PlaceActionLink` is a record whose payload is essentially `{uri,
placeActionType}` — where `placeActionType` may be `APPOINTMENT` ("The action type is booking an
appointment") — plus a `providerType` field that Google marks **output only**:

> `MERCHANT` — "A 1P provider such as a merchant, or an agency on behalf of a merchant."
> `AGGREGATOR_3P` — "A 3P aggregator, such as a `Reserve with Google` partner."

— https://developers.google.com/my-business/reference/placeactions/rest/v1/locations.placeActionLinks

This is the structural answer to the crux question. Google's own schema treats a
merchant-supplied link and a Reserve with Google partner link as **two different provider types on
the same object**. A link you type into the box is a `MERCHANT` link. It does not and cannot
become an `AGGREGATOR_3P` link, because `providerType` is assigned by Google based on who supplied
the link, and is not writable.

### What Google learns when a user clicks it

Three things, and no more:

1. **The URL string itself** — because you typed it in. Google stores it in order to render the
   button. If the URL contains a query parameter, Google holds that parameter.
2. **That an interaction occurred on the profile** — Google renders the button on its own surface,
   so the click happens inside Google's UI before the browser navigates away. Google measures
   button clicks generally; `WEBSITE_CLICKS` ("The number of times the business profile website
   was clicked") already exists as a metric and has recorded 711 clicks for this profile.
3. **Standard referral data at the destination** — i.e. that the visitor arrived from Google. This
   is identical to what already happens on every one of those 711 website clicks.

**No booking outcome flows back.** There is no callback, no confirmation, no appointment record.
Google has no way to learn whether the person who clicked went on to book, or what they booked,
unless the destination page tells it — which is a property of the destination page's own tags, not
of the link (see Section 7).

> **Ambiguity, stated rather than resolved.** Google's documentation says performance data for
> custom links is not made available *to the merchant*. It does not say Google declines to observe
> or log the click for its own purposes. Nothing I found addresses that directly, and I would not
> assert either way. The prudent assumption is that Google observes a custom booking-link click
> exactly as it observes a website-button click — which the clinic has been generating for years.

---

## 4. The "Bookings" metric is not a count of link clicks — and this matters

The Business Profile Performance API defines the metric unambiguously:

> `BUSINESS_BOOKINGS` — "The number of bookings made from the business profile **via Reserve with
> Google**."

— https://developers.google.com/my-business/reference/performance/rest/v1/DailyMetric

And Google's help page on bookings is explicit that a merchant's own link produces nothing:

> "**View your bookings performance** — Performance data isn't available for custom links. You can
> check how well your bookings are doing with Reserve with Google."

— Google Business Profile Help, *Set up bookings through a provider*
(https://support.google.com/business/answer/7475773)

Three consequences follow, and all three matter to this decision:

1. **The 550 straight days of Bookings = 0 in the archive are not evidence of a missing link.**
   They are evidence that PNH is not enrolled in Reserve with Google. That is exactly what one
   would expect, and is arguably the reassuring reading.
2. **Adding a plain link will not make that number move.** If anyone later reports "we added the
   link and bookings are still zero," that is the documented behaviour, not a failure.
3. **Measurement of a plain link has to come from PNH's side.** Google will not report it. This is
   an argument for pointing the link somewhere PNH can count arrivals itself (Section 8).

---

## 5. Mechanism 2 — Reserve with Google

### What the provider transmits, and what Google transmits back

Reserve with Google is an end-to-end booking product operated through Google's Actions Center. The
provider sends Google an inventory feed (merchant, services, availability) and stands up a booking
server that Google calls. Google's integration guide states the data flow in one sentence:

> "When a user creates a booking, **Google sends you the user's given name, surname, phone number,
> and email.** From your point of view, this booking needs to be treated as a guest checkout,
> because the Actions Center can't look up the user's account in your system."

— Google Actions Center, *Step 4: Implement the booking server*
(https://developers.google.com/actions-center/verticals/local-services/e2e/integration-steps/implement-booking-server)

Read that in the direction that matters here. Google transmits the patient's name, phone and email
to the scheduling vendor **because Google collected them.** In an end-to-end Reserve with Google
booking, the appointment type, the time slot and the identity of the person booking it are all
handled inside Google's surface. Google is not a bystander to the booking; it is the intake form.

For a health care practice with no business associate agreement in place with Google, that is a
materially different posture from a hyperlink.

### Does Acuity support it, and can a plain link enrol you by accident?

Acuity supports it, and enrolment is unambiguously an affirmative, multi-step act. From Acuity's
current help article (last updated 2026-08-12):

> "Connect Acuity to Reserve with Google so clients can book appointments from Google search
> results, Google Maps, or Google Assistant."

> **Reserve with Google eligibility** — "To connect Acuity to Reserve with Google, you need to:
> Have a physical location. Have a Google Business Profile. Be in an approved industry."

> "When you connect Acuity to Reserve with Google, **publicly viewable data from your client
> scheduling page will be provided to Google.** After the connection is live, Google regularly
> updates information about your appointment types automatically."

> "To connect to Reserve with Google: ... Open the **Integrations** panel. In the Client Engagement
> section, find **Reserve with Google** and click **Set Up**. Enter your business's name and
> address, then click **Submit**. ... The integration will be live after Google approves your
> business, which could take days. **When a Book Online button appears, you'll know you've been
> approved.**"

— Acuity Scheduling Help Center, *Connect Acuity Scheduling to Reserve with Google*
(https://help.acuityscheduling.com/hc/en-us/articles/16676895486349-Connect-Acuity-Scheduling-to-Reserve-with-Google)

**So: enrolment requires (a) opening Acuity's Integrations panel, (b) clicking Set Up on the
Reserve with Google card, (c) submitting the business name and address, and (d) Google approving
the business over a period of days.** None of that can be triggered by typing a URL into the
Business Profile booking field. The two mechanisms live in different products, are performed by
different actions, and are recorded by Google under different `providerType` values.

There is also a hard interlock worth knowing about. Acuity's HIPAA documentation lists what changes
when an account is made HIPAA-enabled, and the list includes:

> "**Integration with Reserve with Google isn't enabled.**"

— Acuity Scheduling Help Center, *Acuity Scheduling and HIPAA*
(https://help.acuityscheduling.com/hc/en-us/articles/16689567523597-Acuity-Scheduling-and-HIPAA)

The same page confirms the BAA path is available on PNH's current plan:

> "You must be on the Premium or Powerhouse plan to enable HIPAA-related services and enter into a
> BAA with Squarespace... A BAA governs the use and protection of Protected Health Information
> exchanged between a 'covered entity' and a 'business associate.' In this situation, if you're a
> covered entity pursuant to HIPAA, then Squarespace is a business associate to you."

PNH is on the Powerhouse plan. Whether the Acuity account is currently HIPAA-enabled is not
recorded in this engagement's files and should be checked. If it is, Reserve with Google is
technically unavailable regardless of intent — a useful belt-and-braces control. Third-party
reporting of the same eligibility rules is consistent: Reserve with Google's approved industries
are named as beauty and fitness types, and "services that require to be insured or have legal
requirements, such as PHI or HIPAA compliance, are not supported."

### The one real accident risk, which runs the other way

Google's help page contains a warning that deserves attention independent of anything Dr. Panka
does:

> "**Remove third-party links.** To provide services for local businesses, Google works with select
> third-party providers... **Links to certain services can automatically appear on your Business
> Profile on Google Search and Maps. These links are provided and updated by third-party partners
> or through automated data from Google.**"

> "To remove a specific third-party booking link: ... On Google Search, select **Booking** →
> **Remove Provider**... Providers need to remove third-party links from your profile within 5 days
> of receiving a removal request."

— https://support.google.com/business/answer/6218037

So the risk of an unwanted third-party booking integration appearing on the profile exists whether
or not PNH adds its own link. That argues for *periodically inspecting* the Bookings section, not
for avoiding it.

---

## 6. Does `appointmentType=41826455` disclose anything meaningful?

Short answer: essentially nothing, and materially less than a condition-named link would.

What the parameter discloses to anyone who reads the URL — Google, or any person looking at the
profile — is that the clinic offers an appointment type whose internal numeric ID is 41826455.
It is an opaque integer. It names no condition, no body system, no service line.

What it resolves to is the **Introductory Phone Call**: 10 minutes, $0.00, offered to anyone,
non-diagnostic, essentially a "find out if we're a fit" conversation. It is the least
health-revealing thing on the menu.

The relevant comparison is what a *bad* version of this would look like. A booking link reading
`.../schedule?appointmentType=perimenopause-consult`, or a profile whose Bookings section lists
"ADHD evaluation" and "Post-concussion follow-up" as selectable services, would mean that a
person's click communicates a probable health condition. That is the fact pattern the FTC has
pursued (Section 7). It is not this fact pattern.

Two caveats worth stating plainly:

- **The intent signal is not literally zero.** Someone who clicks "Book" on a naturopathic clinic's
  profile is expressing intent to obtain health care from that clinic. That is a health-adjacent
  signal. But it is the same signal already carried by the 711 website-button clicks and the 981
  direction requests the profile has generated, and by every paid search click the clinic has ever
  bought.
- **This conclusion is tied to that specific appointment type.** If the link is ever changed to a
  condition-specific type, or if Reserve with Google is ever enabled (which publishes the *whole*
  appointment-type list to Google — "publicly viewable data from your client scheduling page will
  be provided to Google"), the analysis changes and should be redone.

---

## 7. Does health-privacy law reach a directory hyperlink?

This section is written for an advisor to check, not to substitute for advice.

### The distinction that does the work

Every enforcement action and every piece of agency guidance in this area concerns **a tracking
technology deployed by the business on a web property the business controls, transmitting
individual-level data to a third party.** A hyperlink displayed on Google's own directory listing
is a different object: it collects nothing, transmits nothing, and executes no code belonging to
PNH. It is closer to a phone number printed in a listing than to a pixel.

### HHS guidance on online tracking — and its current, diminished status

HHS OCR's bulletin on online tracking technologies was directed at regulated entities' own websites
and apps. Critically, a large part of it no longer stands. On 2024-06-20 the U.S. District Court
for the Northern District of Texas, in *American Hospital Association v. Becerra*, declared unlawful
and vacated the portion of the guidance providing that HIPAA obligations are triggered where an
online technology connects "(1) an individual's IP address with (2) a visit to an unauthenticated
public webpage addressing specific health conditions or health care providers." HHS OCR withdrew
its appeal on 2024-08-29.

(See e.g. Holland & Knight, *American Hospital Assn. v. Becerra: Are Tracking Tools OK Again?*,
https://www.hklaw.com/en/insights/publications/2024/06/american-hospital-assn-v-becerra-are-tracking-tools-ok-again
and Morrison Foerster, *HHS Withdraws Appeal of Federal Court Decision Regarding Online Tracking
Guidance*, https://www.mofo.com/resources/insights/240930-a-mofo-privacy-minute-q-a-hhs-withdraws)

Even at its most expansive, that guidance did not purport to reach a hyperlink on a third-party
directory listing.

**Threshold question that should be settled anyway:** is PNH a HIPAA covered entity at all? A
health care provider is covered only if it transmits health information electronically in
connection with a HIPAA standard transaction (claims, eligibility, referral authorisation, etc.).
PNH is cash-pay, bills no insurance, and provides superbills for patients to submit themselves.
That pattern commonly falls outside HIPAA. This has not been confirmed and should be, because it
determines which of the regimes below is actually the operative one.

### FTC — the regime that reaches non-HIPAA health businesses

The FTC has been the active enforcer against health businesses outside HIPAA, and tracking pixels
have been the recurring fact pattern: GoodRx ($1.5M civil penalty, first Health Breach Notification
Rule enforcement, for undisclosed sharing of prescription and condition data with Facebook, Google
and others); BetterHelp ($7.8M); Cerebral (>$7M, plus a ban on using or disclosing personal and
health information for targeted advertising).

(FTC press release, *FTC Enforcement Action to Bar GoodRx from Sharing Consumers' Sensitive Health
Info for Advertising*,
https://www.ftc.gov/news-events/news/press-releases/2023/02/ftc-enforcement-action-bar-goodrx-sharing-consumers-sensitive-health-info-advertising)

The Health Breach Notification Rule was amended effective 2024-07-29 to broaden coverage —
including new definitions of "covered health care provider" and "health care services or supplies,"
and confirmation that a covered breach includes voluntary unauthorised *disclosures*, not only
intrusions. (FTC, *Health Breach Notification Rule*,
https://www.ftc.gov/legal-library/browse/rules/health-breach-notification-rule; final rule at
https://www.federalregister.gov/documents/2024/05/30/2024-10855/health-breach-notification-rule)

Two observations. First, the HBNR applies to vendors of personal health records and related
entities; a clinic's marketing site and scheduling page are not obviously a personal health record,
though the amended definitions are broader than they were. Second, and more to the point: **none of
these cases is about a listing hyperlink.** All of them are about individual-level data being
transmitted to advertising platforms from pages the business controlled. Section 5 of the FTC Act
(deception and unfairness) applies to PNH regardless of HBNR coverage, which is a reason to keep the
privacy policy accurate — not a reason to avoid a hyperlink.

### Minnesota — the regime that may reach PNH regardless

Minnesota's Health Records Act (Minn. Stat. §§ 144.291–144.298) is more stringent than HIPAA and
applies on its own terms. Section 144.293 provides that a provider "may not release a patient's
health records to a person without: (1) a signed and dated consent from the patient..." and the
Act must be construed to protect privacy "in a more stringent manner than" the federal rules.
"Health record" is defined broadly at § 144.291 subd. 2(c) as "any information, whether oral or
recorded in any form or medium, that relates to the past, present, or future physical or mental
health or condition of a patient; the provision of health care to a patient; or the past, present,
or future payment for the provision of health care to a patient."

**A point for counsel, which I flag rather than resolve.** § 144.291 subd. 2(i) defines "provider"
as, in relevant part, "any person who furnishes health care services and is regulated to furnish
the services under chapter 147, 147A, 147B, 147C, 147D, 148, 148B, 148E, 148F, 150A, 151, 153, or
153A," plus licensed home care providers, licensed health care facilities and assisted living
facilities. Registered naturopathic doctors in Minnesota are regulated under **chapter 147E**
(Board of Medical Practice, Registered Naturopathic Doctor Advisory Council) — and 147E does not
appear in that enumeration, which runs 147 through 147D and then jumps to 148.
(Statute text: https://www.revisor.mn.gov/statutes/cite/144.291 ; chapter 147E:
https://www.revisor.mn.gov/statutes/cite/147E/full)

I did not trace whether another provision of chapter 147E or elsewhere pulls registered NDs back
within the Act, and I would not assume the omission is meaningful. It is exactly the kind of point
an advisor should settle once, because the answer governs far more than this hyperlink.

Separately, the Minnesota Consumer Data Privacy Act's thresholds (volume of consumers processed, or
revenue derived from selling personal data) are very unlikely to be met by a single-location clinic;
worth a one-line confirmation, not analysis.

### Where the real exposure actually sits

It is worth being blunt about proportion. The genuinely consequential privacy question in this
engagement is not the Business Profile link. It is the **existing** pipeline: Acuity's Google
Analytics integration is live and has been recording completed bookings into PNH's GA4 property as
`purchase` events, carrying Acuity page paths that encode the appointment type
(`/schedule/0081d9d2/appointment/<typeID>/...`) — 66 bookings and $7,753 of revenue between
2026-07-01 and 2026-09-03. That is completed-booking events, with appointment type, tied to a
browser identifier, arriving at Google. That is precisely the thing the compliance stance adopted
this week rules out, and it is already happening.

**The Business Profile link does not change that pipeline in either direction.** Whichever
destination is chosen, a person who books ends up in Acuity and is counted the same way. Anyone
reviewing this memo should treat the Acuity→GA4 integration as the priority item and this
hyperlink as the minor one.

---

## 8. Options and exposures

| # | Option | What Google gets | Booking outcome to Google? | Exposure | Verdict |
|---|---|---|---|---|---|
| A | Booking link → `pankanaturalhealth.com/schedule-an-appointment?appointmentType=41826455` | A URL on PNH's own domain; the fact of a click | No | Lowest. Nothing leaves PNH's domain in the link itself. PNH can measure arrivals in its own logs. | **Recommended** |
| B | Booking link → `app.acuityscheduling.com/schedule.php?owner=27943652&appointmentType=41826455` | A URL naming the scheduling vendor, the account owner ID and the appointment type; the fact of a click | No | Slightly higher and gains nothing: it hands Google a vendor-and-account-specific URL, and it repeats the known off-domain jump that has been destroying attribution all along. | Workable but inferior |
| C | Reserve with Google via Acuity Integrations | The full public appointment-type list, live availability, and the patient's given name, surname, phone and email at the moment of booking | Yes — Google *is* the booking surface | Highest by a wide margin. Google is not a business associate and will not sign a BAA. | **Do not enable** |
| D | Reserve with Google via Business Profile → Bookings → Get started → select provider | Same as C | Yes | Same as C, entered from the Google side instead of the Acuity side | **Do not enable** |
| E | Do nothing | Nothing new | No | No new exposure; forgoes the channel | Defensible, but Option A's marginal exposure over the status quo is very small |

### Recommendation: safe in a named configuration

**Verdict: safe to do, in the configuration named below.** This is not "needs professional advice
before acting" — the mechanism is documented, the separation between link and integration is
structural, and the marginal disclosure over the clinic's existing 711 website-button clicks is
close to nil. Two items *do* warrant an advisor's attention, but neither blocks the link: the
MHRA "provider" question in Section 7, and the pre-existing Acuity→GA4 pipeline in the same
section.

### Exact URL to use

```
https://pankanaturalhealth.com/schedule-an-appointment?appointmentType=41826455
```

HTTPS, PNH's own domain, intro call preselected. (The Acuity embed's iframe-source builder reads
the parent page's query string and forwards parameters matching an allowlist that includes
`appointmentType`, so this preselects the free intro call without a new page being built. Confirm
by loading the URL once before pasting it into Google.)

### Steps for Dr. Panka to perform himself

1. Open the Business Profile from Google Search while signed in as the owner. Confirm you are on
   the **live** listing (location ID `3326559683279742636`, 901 1st St N) and not the duplicate
   (`10418367222074184209`, no address, no traffic). Do not add a link to the duplicate.
2. Select **Bookings** (Search) or **Edit profile → Booking** (Maps).
3. **Before adding anything, look at what is already there.** Record any existing links and any
   third-party providers listed. Third-party links can appear without merchant action; if one is
   present that you did not add, use **Remove Provider**.
4. Select **Add link**, paste the URL above verbatim, and Save. Allow up to 3 days for it to
   appear.
5. Set it as the **preferred link** ("Business preferred") if any other booking link exists.
6. After it goes live, click it yourself from a signed-out browser and confirm it lands on the
   scheduling page with the Introductory Phone Call preselected.

### The exact settings to avoid

- **In Google Business Profile:** do **not** use **Bookings → Get started → select your provider**.
  That is the Reserve with Google third-party-provider enrolment flow (Option D), not the link
  field. The link field is reached via **Add link** only.
- **In Acuity:** do **not** click **Set Up** on the **Reserve with Google** card in the
  **Integrations** panel, Client Engagement section (Option C). Nothing else in that panel triggers
  it.
- **Tell-tale that the wrong thing happened:** a **Book Online** button appears on the profile, or
  Google begins showing selectable appointment *times* in the search result. Per Acuity's
  documentation, that button is the signal that Reserve with Google approval came through. A plain
  merchant link renders as a simple link/button and never exposes availability. If that button
  appears, disconnect from Acuity's Integrations panel (**Edit → Disconnect Reserve with Google**);
  removal from Google can take up to 72 hours.
- **Do not swap the appointment type** in the URL for a condition-specific one without redoing the
  Section 6 analysis.

### Two things to expect, so they are not misread later

- **Bookings will stay at 0.** Per Google, that metric counts Reserve with Google bookings only,
  and custom links generate no performance data at all. Zero is the correct and expected reading,
  and is in fact the ongoing confirmation that PNH is *not* enrolled in Reserve with Google. Treat
  a non-zero Bookings number as an alarm, not a success.
- **Google will not tell you how many people clicked it.** Measurement has to come from PNH's own
  side — server logs, or a distinguishable landing path.

---

## 9. What remains genuinely ambiguous

Stated as ambiguities rather than resolved, per instruction.

1. **Whether Google observes and retains clicks on a custom booking link for its own purposes.**
   Documentation says only that performance data is not available to the merchant. It does not say
   Google ignores the click. Assume it is observed, as website-button clicks plainly are.
2. **Whether custom booking-link clicks roll into the `WEBSITE_CLICKS` metric or are dropped
   entirely.** Undocumented. This affects only reporting continuity, not exposure.
3. **Whether the Minnesota Health Records Act reaches a naturopathic doctor registered under
   chapter 147E**, given that 147E is absent from the enumerated chapters in § 144.291 subd. 2(i).
   This should be settled by counsel; it matters well beyond this decision.
4. **Whether PNH is a HIPAA covered entity at all**, given cash-pay operations with no insurance
   billing. Determines which regime governs.
5. **Whether the PNH Acuity account is currently HIPAA-enabled.** Not recorded in this engagement's
   files. If it is, Reserve with Google is technically blocked, which is a meaningful additional
   safeguard.

---

## 10. Sources

- Google Business Profile Help, *Manage your local business links* — https://support.google.com/business/answer/6218037
- Google Business Profile Help, *Set up bookings through a provider* — https://support.google.com/business/answer/7475773
- Google Business Profile APIs, *DailyMetric* — https://developers.google.com/my-business/reference/performance/rest/v1/DailyMetric
- Google Business Profile APIs, *REST Resource: locations.placeActionLinks* — https://developers.google.com/my-business/reference/placeactions/rest/v1/locations.placeActionLinks
- Google Actions Center, *Step 4: Implement the booking server* — https://developers.google.com/actions-center/verticals/local-services/e2e/integration-steps/implement-booking-server
- Google Actions Center, *Reservations Business Link — Overview and Eligibility* — https://developers.google.com/actions-center/verticals/reservations/bl/overview
- Acuity Scheduling Help Center, *Connect Acuity Scheduling to Reserve with Google* (updated 2026-08-12) — https://help.acuityscheduling.com/hc/en-us/articles/16676895486349-Connect-Acuity-Scheduling-to-Reserve-with-Google
- Acuity Scheduling Help Center, *Acuity Scheduling and HIPAA* — https://help.acuityscheduling.com/hc/en-us/articles/16689567523597-Acuity-Scheduling-and-HIPAA
- Holland & Knight, *American Hospital Assn. v. Becerra: Are Tracking Tools OK Again? Court Dials Back OCR Bulletin* — https://www.hklaw.com/en/insights/publications/2024/06/american-hospital-assn-v-becerra-are-tracking-tools-ok-again
- Morrison Foerster, *HHS Withdraws Appeal of Federal Court Decision Regarding Online Tracking Guidance* — https://www.mofo.com/resources/insights/240930-a-mofo-privacy-minute-q-a-hhs-withdraws
- FTC, *FTC Enforcement Action to Bar GoodRx from Sharing Consumers' Sensitive Health Info for Advertising* — https://www.ftc.gov/news-events/news/press-releases/2023/02/ftc-enforcement-action-bar-goodrx-sharing-consumers-sensitive-health-info-advertising
- FTC, *Health Breach Notification Rule* — https://www.ftc.gov/legal-library/browse/rules/health-breach-notification-rule
- Federal Register, *Health Breach Notification Rule* final rule (eff. 2024-07-29) — https://www.federalregister.gov/documents/2024/05/30/2024-10855/health-breach-notification-rule
- Minn. Stat. § 144.291 (Minnesota Health Records Act, definitions) — https://www.revisor.mn.gov/statutes/cite/144.291
- Minn. Stat. § 144.293 (Release or disclosure of health records) — https://www.revisor.mn.gov/statutes/cite/144.293
- Minn. Stat. ch. 147E (Registered naturopathic doctors) — https://www.revisor.mn.gov/statutes/cite/147E/full

Internal data referenced: `/home/user/projects/data/supermetrics-archive-2026-09-08/gmb-location-metadata.csv`,
`gmb-monthly-metrics.csv`, `gmb-daily-metrics.csv`, `NOTES-gbp-metrics.md`.

*Google-domain pages were unreachable through this session's direct fetch path and were retrieved
via an alternate extraction service; quoted text is from the live pages as retrieved 2026-09-08.*
