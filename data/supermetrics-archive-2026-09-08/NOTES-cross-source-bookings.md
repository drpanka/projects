# NOTES — cross-source bookings: what the master table could not capture

**Author: the cross-source agent. Written 2026-09-08. Owns `master-monthly-channel-table.csv`,
`master-channel-summary.md`, `build_master_monthly.py` and this file. Do not append to another
agent's `NOTES-*.md`.**

`master-monthly-channel-table.csv` is one row per month, 2023-02 → 2026-09, 25 columns, built
entirely from CSVs already in this directory. No Supermetrics quota was spent on it. Everything
below is a limit of that table, recorded so nobody re-derives it or, worse, trusts a column it
should not.

---

## 1. The biggest hole: there is no bookings column, and there cannot be one

A "bookings" column is the one thing a cross-source table like this exists to provide, and this
archive cannot supply it. Three candidate sources, all unusable:

- **Google Ads conversions** count a page load on `/schedule-an-appointment`. Interest, not a
  booking. Included in the table as `ads_conversions_as_reported`, clearly labelled.
- **Google Business Profile bookings** are zero in all 18 months and all 550 days. Real zero — no
  booking link is attached to the profile — so it tells you nothing about volume.
- **GA4 `purchase`** is the closest thing, and still wrong three separate ways (section 3).

**The only booking truth is the Acuity export, and it is not in this archive.** Acuity is owner
`27943652`, ownerKey `0081d9d2`. A monthly export of completed appointments, split by appointment
type (`41826455` is the $0 intro call), is the missing column. If one number from this whole
exercise is worth doing by hand each month, it is that one.

## 2. Attribution stops at the scheduler, so no month can be joined at the patient level

The table joins three sources at the **month** grain and no finer, because there is no key that
survives the hop to Acuity's domain. GA4 sees a `click` to `app.acuityscheduling.com`; Acuity sees
a booking; nothing carries the ad click across. The `pankanaturalhealth.com / referral` rows in GA4
are the fingerprint of exactly this — self-referred sessions that are real bookings with their
origin erased.

Consequence: **no cost-per-booking exists at any level of this table**, for any channel, in any
month. `ads_cpa_like_for_like_usd` is cost per *page-reach event*, not cost per patient. It is
useful only as a relative signal between months on a constant basis.

Verified from `embed.js` during the earlier work: Acuity's iframe-src builder forwards parent-page
query params matching an allowlist that includes `appointmentType` and `field:<ID>` but **not
`gclid`**. And the conversion iframe (`sandbox.acuityinnovation.com`) is cross-origin, so
`window.top.gtag(...)` throws a SecurityError and fails silently — only `postMessage` works. Any
snippet in the site that calls `window.top.gtag` directly has never fired.

**Compliance constraint, decided this week:** sending completed-booking events, with appointment
type, tied to a browser identifier, to Google Analytics or Google Ads was judged a privacy risk
because Google will not sign a business associate agreement. So the technically obvious repair is
off the table unless a specific mechanism can be shown not to do that. This is why the table has no
bookings column rather than a broken one.

## 3. `ga4_purchase_events_*` changes meaning three times across the history

The two purchase columns are in the table because they are the best available proxy, not because
they are a booking count. Read them with the per-month `data_quality_note`:

| Period | What a `purchase` event actually was |
|---|---|
| 2023-12 → 2024-11 | Squarespace store orders and page-unattributed events. **Not appointments at all.** The 23 in 2024-02 and 24 in 2024-03 are shop orders. |
| 2024-12 → 2026-05 | Mix of Acuity scheduler pages and Squarespace orders. Not separable at month grain. |
| 2026-06 → 2026-09 | Predominantly Acuity scheduler, and the intro-call type is identifiable by page path. Still overcounts real bookings by roughly 45% — one Acuity booking can fire up to three purchase events. |

`ga4_purchase_events_google_cpc` is 6 events across the entire history. That is not a measurement
of paid-search bookings; it is a measurement of how thoroughly attribution is broken.

## 4. Paid search before June 2025 has traffic but no cost, anywhere

GA4 records **5,824 `google / cpc` sessions** between 2023-03 and 2025-03 (roughly Mar–Sep 2023 and
Feb 2024 – Mar 2025). Google Ads account `7473953248` has no delivery at all before 2025-06.

So PNH ran paid search from **an account that is not in this archive** — a prior account, an agency
account, or one never connected to Supermetrics. Its spend, clicks, keywords and search terms are
unrecoverable now that the subscription has lapsed. Those months therefore have GA4 session columns
populated and every Ads column blank, and the note column says why. Do not read the blank as zero,
and do not compute a blended cost-per-session across that boundary.

If anyone still has access to the Google Ads UI, the account list under Jacob's login is the one
place that history might still be recoverable. It is not recoverable from here.

## 5. Deliberate choices in the table that a future reader might question

- **Sessions come from the `session_start` event**, per source/medium, summed per month, so that
  sessions and their channel split come from one self-contained file
  (`ga4-events-by-source-monthly.csv`) that this table does not share with any other agent's work.
  A sibling file, `ga4-channels-monthly.csv`, carries GA4's true `sessions` metric by default
  channel grouping; it was written concurrently and is not a dependency here, but it makes a good
  independent check. Against it the `session_start` proxy runs **0.5% low over the full history**
  (31,064 vs 31,221), never more than 27 sessions off in any month, worst as a percentage in the
  partial month 2026-09 (166 vs 173, −4%). Use `ga4-channels-monthly.csv` if you need the exact
  metric; use this table's column for the channel comparison, which is what it was built for. Summing the
  `sessions` column across all event names would multiply-count the same session once per event
  type. Channel buckets are assigned from `sessionSourceMedium`: medium `cpc`/`ppc` → paid search,
  `organic` → organic, `(direct) / (none)` → direct, `referral` → referral, everything else
  (social, `ai-assistant`, `fb / paid`, `(not set)`) falls outside the four columns. The four
  buckets therefore do **not** sum to `ga4_sessions_total`, by design; the remainder is small
  (48 sessions over the last twelve months).
- **`fb / paid` is not in the paid-search column.** It is paid social, 32 sessions lifetime.
- **The dark months 2025-10 → 2026-03 carry Ads zeros, not blanks.** Zero delivery there is a
  verified fact (`NOTES-ads-campaign-history.md`: no impressions between 2025-08-27 and 2026-04-27,
  genuinely zero spend, not a reporting gap). Months before 2025-06 carry blanks, because zero
  delivery *in this account* does not mean zero paid search — see section 4.
- **September 2026 Business Profile actions are blank, not zero.** Views are populated through
  2026-09-04 only, and every action metric reads 0 for every day from 09-01 while views are normal.
  That is Google's reporting lag, which runs longer for actions than for views. Filling zeros there
  would have manufactured a collapse that did not happen. The `gbp_profile_views` cell for that
  month is a real but partial 81.
- **Like-for-like conversions appear twice.** The account-wide pair blends Performance Max
  "Campaign #1", whose conversions were page-view actions counted in the thousands, so its blended
  CPA (e.g. $1.92 in Jul 2025) is meaningless. The `*_search_campaign` pair is Leads-Search-1 only
  and is the one to quote; it reproduces the established series exactly — $11.07, $12.21, $9.35,
  $23.28, $25.62.
- **2025-09 shows 0 click-date conversions but Google reports 5.** Those 5 are conversion-date
  spillover from August clicks. The table uses click-date throughout so that cost and conversions
  refer to the same clicks.

## 6. Channels this table does not contain at all

None of these have a connector in this archive, and several have no tracking anywhere:

- **Acuity** — the booking system itself. See section 1.
- **The phone.** `tel:+16125688382` has no click tracking on the site. The only phone signal in the
  entire archive is Business Profile's 76 calls over 18 months, which counts taps on the profile's
  call button and nothing else.
- **The Chatbase "PNH Guide" chatbot** — zero tracking.
- **Email / Mailchimp** — visible only as `us19.admin.mailchimp.com` and `mailchi.mp` referral
  sessions, both of which are mostly the operator's own admin sessions. No sends, opens or clicks.
- **Meta / Instagram** — 32 `fb / paid` sessions lifetime and some organic social referrals. No ad
  account in this archive.
- **Referring professional networks** (`mnanp.org`, `oncanp.org`, `findanaturaldoctor.com`,
  `hbcamn.com`, `wellconnectedtwincities.com`) appear as referral sessions. They may be a real
  patient source; there is no way to tell from here.
- **Organic search rankings.** GA4 records organic sessions but there is no Search Console data in
  this archive, so there are no queries, impressions or positions behind the 7,317 lifetime organic
  sessions.

## 7. Sanity checks that were run, and passed

`build_master_monthly.py` prints a mismatch warning if the campaign-level sum disagrees with the
account-level file; it printed none. A separate verification pass compared every month of the
finished table back against `ads-account-monthly.csv` (cost, impressions, clicks),
`gmb-monthly-metrics.csv` (all six metrics), `ga4-purchases-monthly.csv` (total and google/cpc) and
`ga4-events-by-source-monthly.csv` (sessions, and that the four channel buckets never exceed the
total), plus the Leads-Search-1 like-for-like conversions against
`ads-cpa-like-for-like-monthly.csv`. **Zero mismatches.**

One incidental cross-source agreement worth keeping: over 2025-10 → 2026-09-08, Google Ads recorded
**893 clicks** and GA4 recorded **891 paid-search sessions**. The two systems agree on traffic to
within 0.2%. They agree on nothing about what happened afterwards.
