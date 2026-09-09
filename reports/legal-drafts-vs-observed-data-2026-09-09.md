# Legal drafts read against the archived data — 2026-09-09

Reviewing the September 8 publication-candidate drafts of the Privacy Policy and Legal Disclaimer
against `data/supermetrics-archive-2026-09-08/`. Both drafts carry the header "resolve the factual
checks before use." This is that check, for the claims the archive can actually test.

I am not a lawyer and this is not legal advice. What follows is a factual reconciliation between what
the drafts say the systems do and what the data shows they do.

---

## 1. What the drafts settle that this engagement had left open

Three questions I flagged for counsel are answered by PNH's own published position.

| Open question | The drafts' position |
|---|---|
| Does the Minnesota Health Records Act reach a 147E registered ND? | Yes. "Independent of that Act, we comply with the Minnesota Health Records Act (Minn. Stat. §§ 144.291 to 144.298)." |
| Is PNH a HIPAA covered entity? | Treated as one. Health information is "safeguarded consistent with the HIPAA Privacy and Security Rules." |
| Is the Acuity account HIPAA-enabled? | Asserted. "Introductory-call and appointment scheduling is provided by a scheduling platform that operates under a Business Associate Agreement with PNH." |

That last one matters most. It means the booking data at rest in Acuity is contractually protected,
which is exactly why the standing recommendation has been to keep the source of truth there.

Two further points strengthen recommendations already made. The disclaimer states that scheduling a
free introductory call "does not establish a doctor-patient relationship," which supports treating the
intro call as the lowest-exposure booking destination. And a testimonials disclaimer already exists,
which de-risks the Business Profile review-request routine — that recommendation can proceed.

---

## 2. A correction to CLAUDE.md that matters

`CLAUDE.md` section 5 lists this under "Still open in the measurement stack":

> `allow_enhanced_conversions: false` blocks Enhanced Conversions for Leads and general uplift.

Framed as a gap to close. **It is not a gap. It is a deliberate privacy setting**, and the draft
policy publishes it as such: "our default settings deny advertising-cookie storage, use of user data
for advertising, and ad personalization; enhanced conversions are disabled."

Anyone reading that CLAUDE.md line without this context would reasonably "fix" it — and thereby put
the account out of step with the published policy on the day it goes live. Corrected in CLAUDE.md.

The same paragraph creates a second standing constraint worth recording: **"We do not use remarketing
or personalized advertising."** Two paused campaigns in the account, `Leads-PMax-Video-1` and
`Campaign #1`, are Performance Max, which uses audience signals by design. They must stay paused, or
the published statement stops being true. That is now a reason not to reactivate them, independent of
their performance.

---

## 3. The one real gap between the drafts and the observed data

The Privacy Policy says, twice:

> "We do not configure our analytics tools to collect the contents of scheduling, intake, or contact
> forms."

Narrowly, that is **true and verified**. Nothing in the archive shows form field contents reaching
Google Analytics or Google Ads.

But the archive shows something the drafts do not plainly describe. Google Analytics receives
completed-booking events from inside the Acuity scheduler, and the page path carries both the
appointment type and the individual provider's calendar:

```
/schedule/0081d9d2/appointment/41826455/calendar/7700282?appointmentTypeIds[]=41826455
```

`41826455` is the Introductory Phone Call. `7700282` is Dr. Haley's calendar; `8024328` is Dr. Jacob's.
The archive holds 429 such `purchase` events reaching back to December 2023, carrying $51,890 of
recorded revenue. That is a signal to Google meaning, in effect, *this browser completed a booking of
this appointment type with this provider*.

The policy does disclose that Google receives "page URLs" and that those signals "are not necessarily
anonymous," which is honest and unusually candid. So this is arguably covered. But a careful reader
would not learn from the current text that booking completions, appointment types and provider
identity flow to Google, and that is the fact most likely to matter if anyone ever asks.

**This is the same exposure flagged in `reports/gbp-booking-link-compliance-2026-09-08.md` as larger
than any Business Profile booking link, and it is live right now.** The drafts do not resolve it;
they make it more visible, because publishing a policy is a representation about what the systems do.

Two ways to close the gap, and they are not mutually exclusive:

- **Change the systems to match the narrower reading.** Disconnect Acuity's Google Analytics
  integration and pause the scheduling-page conversion actions in Google Ads. The campaign continues
  unaffected under Manual CPC; only reporting changes, and that reporting has already been shown to
  mislead four separate ways.
- **Change the text to match the systems.** Add a sentence to the Cookies section stating plainly that
  when an appointment is booked through the online scheduler, the analytics tools receive the page
  address of the booking confirmation, which identifies the appointment type and the provider, but not
  the patient's name or the contents of any form.

Whichever route, the decision belongs with counsel. The point here is only that the drafts and the
systems currently describe slightly different worlds, and the drafts are the more conservative of the
two.

---

## 4. Smaller factual checks the archive can confirm or flag

| Draft statement | Archive check |
|---|---|
| "enhanced conversions are disabled" | **Confirmed.** `allow_enhanced_conversions: false` is explicitly set on tag AW-17146544733. |
| "We do not use remarketing or personalized advertising" | **Consistent today.** No remarketing audiences in use; both PMax campaigns paused. Becomes false if either is reactivated. |
| "Our site may preserve ad-click information in links between pages" | **Consistent.** Ad-click identifiers appear in site URLs. |
| "The PNH Guide chat button is hidden on our appointment-scheduling page, but the chat software may still load" | **Cannot verify from the archive.** Chatbase appears nowhere in outbound-link data, so the chatbot generates no measurable tracked activity at all. Worth a browser check on the live page. |
| "Analytics cookies may be used when you visit, including on the appointment-scheduling page" | **Confirmed and material.** This is the page the ad conversion fires on. |
| Google Business Profile is not mentioned anywhere in either draft | **Gap.** If a booking link is added to the profile, the policy's list of third-party services should name it. Minor, but it is the one recommendation in the pipeline that would make the current text incomplete. |

One observation the drafts prompt but do not address: the top two outbound destinations on the site
are the Charm patient portal (589 lifetime clicks) and Fullscript (229). Both are correctly described
as third-party services in the drafts. Both are also existing-patient tools, which is a reminder that
a large share of site traffic is current patients, not prospects.

---

## 5. What this changes about the forward plan

Nothing about the advertising work. The hold until Sept 21, the search-partners change, and the
Business Profile sequence all stand.

What changes is **priority**. Before today, the Acuity-to-Google booking signal was one open item among
several. Publishing a privacy policy converts it from an internal question into a public
representation, so it should be settled before the drafts go live rather than after. It moves to the
top of the compliance list, above the Business Profile booking link, which is the smaller exposure of
the two and is now better documented than the one already running.
