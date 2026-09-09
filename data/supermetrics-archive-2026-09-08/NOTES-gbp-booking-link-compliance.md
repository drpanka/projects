# NOTES — GBP booking link: compliance verification (2026-09-08)

Owner of this file: the compliance-verifier pass. Do not append other agents' findings here.

Full memo lives OUTSIDE the archive, at
`/home/user/projects/reports/gbp-booking-link-compliance-2026-09-08.md`.

## Verdict

**Safe in a named configuration.** Add a plain merchant booking link pointing at
`https://pankanaturalhealth.com/schedule-an-appointment?appointmentType=41826455`.
Never enable Reserve with Google (Acuity Integrations → Set Up, or GBP → Bookings → Get started →
select provider).

## The four findings that decide it

1. **The metric everyone was reading is not what they thought.** Google defines
   `BUSINESS_BOOKINGS` as "The number of bookings made from the business profile **via Reserve with
   Google**." And its help page says "Performance data isn't available for custom links."
   → The 550 days of `actions_bookings = 0` in `gmb-daily-metrics.csv` are **not** evidence that a
   booking link is missing. They are evidence PNH is not enrolled in Reserve with Google. Adding a
   plain link will keep that number at 0 forever, by design.

2. **Link and integration are structurally distinct in Google's own schema.** `PlaceActionLink`
   carries an output-only `providerType`: `MERCHANT` ("a 1P provider such as a merchant") vs
   `AGGREGATOR_3P` ("a 3P aggregator, such as a Reserve with Google partner"). A typed-in URL is a
   MERCHANT link and cannot become an aggregator link.

3. **Reserve with Google enrolment requires four affirmative steps** (Acuity Integrations panel →
   Set Up → submit business name/address → Google approval over days), per Acuity's help article
   updated 2026-08-12. Pasting a URL into GBP cannot trigger it. Tell-tale that it happened
   anyway: a **Book Online** button appears, or Google starts showing bookable *times*.

4. **Reserve with Google is the thing the compliance stance rules out, and the docs say why.**
   Google Actions Center: "When a user creates a booking, Google sends you the user's given name,
   surname, phone number, and email." Google is the intake surface, not a bystander. Also: Acuity
   disables the RwG integration entirely on HIPAA-enabled accounts.

## Correction to the task premise

"GBP has no booking link" is **unverified**. The GMB connector exposes no place-action-link field
(`gmb-location-metadata.csv` has 24 columns, none of them action links). Jacob must look at the
profile UI. Bookings=0 does not establish it.

## Proportionality note that should not get lost

The GBP link is a minor exposure question. The live one is the **existing** Acuity→GA4 integration
already writing completed bookings as `purchase` events with appointment type in the page path
(66 bookings / $7,753, Jul 1 – Sep 3). That is completed-booking data with appointment type reaching
Google today. The GBP link changes it in neither direction.

## Left open for counsel (do not resolve from these notes)

- Minn. Stat. § 144.291 subd. 2(i) enumerates chapters 147, 147A–147D, 148, 148B, 148E, 148F, 150A,
  151, 153, 153A. Registered naturopathic doctors are chapter **147E** — absent from the list.
  Not traced further. Governs far more than this decision.
- Is PNH a HIPAA covered entity at all (cash-pay, no insurance billing, superbills only)?
- Is the PNH Acuity account currently HIPAA-enabled? Not recorded anywhere in this engagement.

## Method note

developers.google.com, support.google.com, help.acuityscheduling.com, squarespace.com and
revisor.mn.gov are all blocked by this session's egress proxy for direct fetch. All Google and
Acuity documentation quoted in the memo was retrieved live on 2026-09-08 through the Nimble
extraction service instead. No Supermetrics quota was spent on this pass.
