# NOTES-verify-pollution.md — GA4 pollution audit, PNH2 (property 353828960)

**Written 2026-09-08. Author: forensic-audit pass on `ga4-self-referral-pollution.csv`, which was
captured in the first pass and never analysed.**

Everything here comes from files already on disk. **No Supermetrics quota was spent.** Sources:
`raw-ga4-pagereferrer-monthly.json`, `ga4-events-by-source-monthly.csv`,
`ga4-purchases-detail.csv`, `ga4-purchases-by-page-monthly.csv`,
`ga4-purchases-monthly.csv`, `ga4-events-by-page-monthly.csv`, `ads-cpa-like-for-like-monthly.csv`,
`ads-conversions-by-action-daily.csv`.

Companion files, both in this directory:
- **`pollution-quantified.csv`** — 4,862 rows, the data behind every number below.
- **`build_pollution.py`** — the script that produced it from the raw JSON already in this archive.
  Re-runnable offline; it makes no API calls.

---

## READ THIS FIRST — how to use `pollution-quantified.csv` without double-counting

The file carries **three different detection grains** in the `detection_field` column:

| `detection_field` | Grain | Source |
|---|---|---|
| `sessionSourceMedium` | session-scoped attribution — what GA4 says the *session* came from | `ga4-events-by-source-monthly.csv` |
| `pageReferrer` | hit-scoped — what the *previous page* was, mid-session included | `raw-ga4-pagereferrer-monthly.json` |
| `purchase unit value == $1.00` | transaction-scoped test-firing signature | `ga4-purchases-detail.csv` |

**These overlap. Never sum across `detection_field`.** A single Tag Assistant session appears in the
`sessionSourceMedium` rows once and in the `pageReferrer` rows again for every page it touched.
Pick one grain for whatever question you are asking and stay in it.

`pct_of_month_events` and `pct_of_month_conversions` are computed against that month's GA4 totals
(`month_total_*` columns), so materiality is readable off the row without re-deriving denominators.

---

## 1. The claim, quantified

> "tagassistant.google.com shows 6 transactions in GA4, which means the tag test was run, but it is
> also polluting conversion data."

### Verdict: the transaction count is **exactly right**. The pollution charge is **right in kind,
### small in degree — with one month-sized exception, and one correction that matters.**

**tagassistant.google.com — every purchase event, all time:**

| Date | Source/medium | Page path | Events | Revenue |
|---|---|---|---|---|
| 2026-04-27 | tagassistant.google.com / referral | (grain unavailable) | 4 | $4.00 |
| 2026-06-04 | tagassistant.google.com / referral | `/schedule-an-appointment?gtm_debug=1780603273076` | 1 | $1.00 |
| 2026-06-04 | tagassistant.google.com / referral | `/schedule-an-appointment?gtm_debug=1780603737192` | 1 | $1.00 |
| | | **Total** | **6** | **$6.00** |

Six. The number in the claim is correct to the event. Two of the six carry `?gtm_debug=` in the page
path, which is unambiguous proof of a Tag Assistant preview session — no interpretation needed.

**ads.google.com is the larger sibling and was not in the claim:**

| Month | Purchase events | Revenue |
|---|---|---|
| 2026-06 (Jun 15 ×4, Jun 16 ×1, Jun 18 ×2) | 7 | $7.00 |
| 2026-07 (Jul 24) | 1 | $1.00 |
| **Total** | **8** | **$8.00** |

**Combined Google-tool referral purchases: 14 events, $14.00.** Every one is valued at exactly
$1.00, which is not a PNH price (see §3i).

### Full event breakdown, session grain

`tagassistant.google.com / referral`:

| Month | Sessions | Events | GA4 conversions | % of month's events | % of month's conversions |
|---|---|---|---|---|---|
| 2025-06 | 53 | 84 | 0 | 1.88% | 0.00% |
| 2026-04 | 19 | 70 | 4 | 2.02% | 4.55% |
| 2026-05 | 82 | 146 | 3 | 3.05% | 4.00% |
| 2026-06 | 5 | 9 | 2 | 0.20% | 0.94% |
| **All time** | **159** | **309** | **9** | | |

`ads.google.com / referral`:

| Month | Sessions | Events | GA4 conversions | % of month's events | % of month's conversions |
|---|---|---|---|---|---|
| 2026-06 | 143 | 299 | **37** | 6.52% | **17.45%** |
| 2026-07 | 78 | 117 | 8 | 1.83% | 2.65% |
| 2026-08 | 55 | 117 | 13 | 2.20% | 5.26% |
| **All time** | **276** | **533** | **58** | | |

Event composition, 2026-06 `ads.google.com`: 123 page_view, 68 user_engagement, 37 session_start,
28 scroll, **23 schedule_appointment**, **7 purchase**, **7 generate_lead**, 2 click, 1 file_download.
That is Jacob clicking through from the Google Ads interface — ad previews, "visit final URL",
landing-page checks — while a live tag counted him as a prospect.

Detected separately at `pageReferrer` grain (a **subset**, do not add): tagassistant 39 events /
26 sessions / 4 conversions; ads.google.com 5 events / 3 sessions / 0 conversions.

---

## 2. Materiality — does this change a conclusion drawn this month?

**Combined tagassistant + ads.google.com against GA4 totals:**

| Measure | Polluted | Total | Share |
|---|---|---|---|
| Purchase events, all time | 14 | 429 | **3.3%** |
| Purchase revenue, all time | $14 | $51,890 | **0.03%** |
| GA4 conversions, all time | 67 | 1,597 | **4.2%** |
| GA4 conversions, **2026-06** | **39** | **212** | **18.4%** |
| GA4 conversions, 2026-07 | 8 | 302 | 2.6% |
| GA4 conversions, 2026-08 | 13 | 247 | 5.3% |

**Three honest answers, in order of importance.**

**(a) It changes nothing about Google Ads spend, CPA, or the like-for-like history.** Google Ads only
counts a conversion it can tie to an ad click. Tag Assistant sessions, Google Ads UI click-throughs
and Squarespace preview loads are untagged browser traffic with no `gclid`. None of it can enter a
campaign's conversion column. Every CPA figure in `ads-cpa-like-for-like-monthly.csv` is untouched by
everything in this note.

**(b) June 2026 GA4 is not quotable raw.** 18.4% of that month's GA4 conversions came from Jacob's
own tag work, plus 7 of its 44 purchase events. June 2026 was when the on-site purchase snippet was
being built, and the numbers show the construction, not the business. If anyone builds a GA4 baseline
or a month-over-month chart that includes June 2026, it is wrong by roughly a fifth.

**(c) Everywhere else it is close to a rounding error** — 2.6% of July, 5.3% of August, 0.03% of
lifetime revenue. Honest answer: for the questions this project is actually asking (budget, CPA,
the August collapse, booking attribution), the tagassistant pollution on its own would not have
changed a single conclusion. **The reason it was worth analysing is what came out of the same
audit — §3i, the $1.00 signature, which does change a number in the reference document.**

---

## 3. Pollution nobody had looked for

Nine classes, all quantified in `pollution-quantified.csv` under `pollution_class`.

### (a) `wake-up-network.com` — UTM-injection ghost referral. **The largest single pollution event
### in the property's history, and nobody has ever mentioned it.**

- **2,349 sessions, 3,398 events, entirely within 2025-10.**
- October 2025 had 4,273 sessions total. **This is 55.0% of the month.**
- Fingerprint URL, verbatim from the referrer dimension:
  `https://pankanaturalhealth.com?utm_source=wake-up-network.com&utm_medium=referral&utm_campaign=wake-up-network.com`
- Composition: 505 page_view, 504 user_engagement, 68 scroll, 505 users, 505 sessions —
  one session per user, one page per session. Textbook ghost traffic.
- Zero conversions. Zero revenue.
- Fell to zero the following month and has never returned.

It landed during the seven-month dark period, so it does not corrupt any paid-search conclusion.
But **any organic or total-traffic trend line drawn through October 2025 is off by a factor of two**,
and nothing in the archive flagged it before now.

### (b) `news.grets.store` and friends — referral spam

- `news.grets.store / referral`: 1,957 sessions all time, of which **3,352 events / ~3,352 sessions
  fell in 2024-02 alone — 49.5% of that month's 6,767 sessions.**
- Also `static.seders.website` (688), `rida.tokyo` (496), `info.seders.website` (168),
  `kar.razas.site` (168), `game.fertuk.site` / `ofer.bartikus.site` / `trast.mantero.online` (48 each),
  plus a long tail of ~470 throwaway domains.
- Class F all-time: **6,438 sessions / 7,660 events at session grain, 3 conversions.**
- In 2026-07: 0 sessions. In 2026-08: 6 sessions, 0 conversions. **Currently negligible.**

### (c) Squarespace preview domain — the biggest *continuous* operator pollution

`apricots-crow-dwjh.squarespace.com` is Jacob editing his own site.

- **7,286 events / 4,596 sessions at pageReferrer grain, present in 43 of the property's 44 months.**
- **52 GA4 conversions carry it as page referrer** — including **11 in July 2026 and 8 in August 2026**.
- At session grain it is much smaller (375 sessions, 3 conversions) because the preview referrer
  usually appears mid-session rather than at session start.
- 2026 monthly conversions with this referrer: Apr 0, May 1, **Jun 28**, **Jul 11**, **Aug 8**, Sep 0.

Event composition all time: 4,014 page_view, 1,258 session_start, 803 user_engagement, 783 scroll,
**97 schedule_appointment**, 100 meet_dr__jacob, 89 meet_dr__haley, 67 why_pnh, 19 generate_lead.
Those bio-page and why_pnh hits matter historically: in the 2025 counting regimes those page views
**were primary conversions** (see `DATA-QUALITY.md` §1, regimes A and B), so operator site-editing was
being counted as conversion volume.

**Residual unknown, and it cannot be closed:** the archive holds no `pageReferrer` × `sessionSourceMedium`
cross-tab, so there is no way to say which channel got session credit for those 52 conversions. The
subscription has ended, so this is now permanently unresolvable. Treat "11 July / 8 August preview
conversions" as an upper bound on the distortion and do not assign it to a channel.

### (d) Operator admin consoles

| Source | Sessions | Events | Window | Notes |
|---|---|---|---|---|
| `us19.admin.mailchimp.com / referral` | 1,008 | 2,134 | 2023-08 → **2026-03** | includes **116 schedule_appointment** events |
| `drlinkcheck.com / referral` | 46 | — | scattered | link checker |
| `www.deadlinkchecker.com` | 6 | 35 | 2024-11 | link checker |
| `account.squarespace.com` / `secure.squarespace.com` | 3+3 | 6 | 2026-09 / scattered | |
| `app.neilpatel.com`, `bize.admin.yelp.com`, `sidekick.badgermapping.com` | small | | 2026-08 | SEO/CRM tooling |

The Mailchimp admin traffic is substantial historically and **stops dead in 2026-03**, so it touches
none of the current-period analysis. It does inflate 2023–2025 engagement baselines.

### (e) Internal clinic / EHR traffic — real people, wrong bucket

`phr2.charmtracker.com / referral` (+ `phr.charmtracker.com`): **433 sessions / 566 events /
6 conversions at session grain; 395 sessions / 417 events at referrer grain; 92 schedule_appointment
events; 1 purchase worth $225 on 2026-05.** Last seen 2026-06.

These are **existing patients arriving from the Charm patient portal**. Not bots, not spam, not junk —
but not prospects either. They should be segmented out of any acquisition or channel analysis and they
should never be filtered as spam. Note the $225 purchase: a real booking that a naive spam filter
would have erased.

### (f) `googleads.g.doubleclick.net` — benign legacy hop

3,429 events / 3,297 sessions, **2023-03 → 2025-02 only**, zero conversions, then gone. This is the
old ad-click redirect appearing as a referrer. Harmless, but it means "referral" traffic in that era
is partly paid traffic wearing the wrong label.

### (g) `syndicatedsearch.goog` — NOT pollution, but nobody has looked at it

821 events / 799 sessions / **9 conversions**. This is Google **Search Partners** inventory. It
appears **only in months the Ads campaign was actually delivering**:

| Month | Events | Sessions | Conversions |
|---|---|---|---|
| 2025-06 | 187 | 185 | 0 |
| 2025-07 | 63 | 61 | 0 |
| 2025-08 | 33 | 33 | 0 |
| 2026-07 | 186 | 181 | 4 |
| **2026-08** | **252** | **245** | **5** |
| 2026-09 | 16 | 16 | 0 |

Real paid traffic, correctly counted. Flagging it because it is a **separate, unexamined inventory
PNH is paying for** — 245 sessions in August is not trivial against 293 `google / cpc` sessions the
same month — and because Search Partners is opt-out-able in the campaign's network settings. Nothing
in the archive's notes has ever separated it. Worth a look, not an action, on this evidence.

### (h) Duplicate purchase firing — corroborated, not new

Of 121 fully-detailed purchase rows (124 events, 119 distinct `transactionId`s): 3 transaction IDs
fire more than once (5 extra events), and **24 date-plus-amount clusters carry multiple distinct
transaction IDs (37 extra events)** — e.g. 2026-06-15 fires six $0.00 purchases, 2026-07-09 fires
four. Consistent with the archive's existing "~45% overcount" caveat (`README.md` caveat 3). No
change to that finding.

### (i) **The $1.00 test-purchase signature — the find that changes a number**

**30 purchase events all time carry a unit value of exactly $1.00.** $1.00 is not a PNH price —
the price list is $0 (intro call), $148, $225, $300, $450. Every one of the 30:

- sits on `/schedule-an-appointment`, the **on-site** page, never on an Acuity path
  (`/schedule/0081d9d2/...`), so none of them came from the Acuity GA4 integration;
- carries a `transactionId` of the form `pnh_<epoch_ms>_<random>` — the custom snippet's own format;
- two of them carry `?gtm_debug=` outright.

**Only 14 of the 30 are on tagassistant/ads.google referrers. The other 16 are camouflaged on
ordinary-looking sources:**

| Source/medium | $1 purchase events | Dates |
|---|---|---|
| `google / organic` | 7 | 2026-04-27, 04-28, 05-31, 07-09 ×3, 07-28 |
| `(direct) / (none)` | 5 | 2026-04-27 ×2, 05-11, 06-15, 07-21 |
| **`google / cpc`** | **3** | **2026-05-13 ×2, 2026-07-07** |
| `chatgpt.com / referral` | 1 | 2026-04-29 |
| `ads.google.com / referral` | 8 | 2026-06-15 ×4, 06-16, 06-18 ×2, 07-24 |
| `tagassistant.google.com / referral` | 6 | 2026-04-27 ×4, 06-04 ×2 |

**This corrects `CLAUDE.md` §5.** That table reports paid search as **"google / cpc — 2 bookings,
$226"** for Jul 1 – Sep 3. The archive shows exactly two `google / cpc` purchase events in that
window: 2026-07-07 at **$1.00** and 2026-07-08 at **$225.00**. The first is a test firing.

> **Corrected: paid search produced 1 attributed booking worth $225 in Jul 1 – Sep 3, not 2 worth
> $226.** The already-thin paid booking evidence is half as thick as recorded.

This does not change the *direction* of the attribution argument in §5 — paid search is still
drastically under-credited relative to its ~28% share of sessions — but the specific figure is wrong
and should be fixed wherever it is quoted. Across all time, `google / cpc` has 6 purchase events
worth $1,083, of which **3 events / $3 are tests**: the real figure is **3 bookings, $1,080**.

---

## 4. Can pollution explain the July → August 2026 halving? **No. Ruled out.**

This is the top open question in the project (`DATA-QUALITY.md`: same spend $652 vs $626, same clicks
315 vs 309, like-for-like conversions **67 → 28**). A measurement artefact was a live candidate.
It is not the answer, and here is why, in five independent ways.

**1. The metric that halved cannot receive this pollution.** The like-for-like series is Google Ads
`Begin checkout` all-conversions on click date for Leads-Search-1. Google Ads counts a conversion only
when it can tie the hit to an ad click via `gclid`. Every pollution class above is untagged browser
traffic — Tag Assistant debug, Ads UI click-through, Squarespace preview, admin consoles, referral
spam. None carries a `gclid`. None can enter a campaign conversion column.

**2. Preview traffic cannot fire that tag at all.** `Begin checkout` is defined on the URL
`www.pankanaturalhealth.com/schedule-an-appointment`. Preview pages are served from
`apricots-crow-dwjh.squarespace.com`. The URL rule cannot match.

**3. GA4 reproduces the drop independently, on a different attribution model:**

| `google / cpc`, GA4 | Jul 2026 | Aug 2026 | Change |
|---|---|---|---|
| Sessions | 351 | 293 | −17% |
| `schedule_appointment` events | **61** | **23** | **−62%** |
| Events per session | 17.4% | 7.8% | **−55%** |

Two systems that share no attribution logic — Google Ads click-attributed conversions and GA4
session-scoped events — show the same collapse at the same magnitude in the same month. An artefact
of either instrument would not appear in both.

**4. What pollution there is makes August look *better*, not worse.** `ads.google.com / referral`
contributed **13** conversions in August against **8** in July. $1.00 test purchases: **7 in July,
0 in August.** Squarespace preview conversions: 11 in July, 8 in August. Subtract pollution from both
months and the July→August gap **widens**. Pollution is working against the halving, not causing it.

**5. Magnitude is off by an order.** Junk share of GA4 conversions was **2.6% in July and 5.3% in
August**. Moving 67 → 28 requires ~58% of the metric. Nothing found here is within reach of that.

> **Conclusion: the August 2026 collapse is a real conversion-rate collapse on paid traffic, not a
> measurement artefact.** Ruling this out is the useful result — the next investigator should stop
> looking at the tracking stack for this and look at what changed in the auction, the landing
> experience, or the query mix between 2026-07-31 and 2026-08-01. One concrete pointer from this
> audit: paid *sessions* only fell 17% while paid *conversion rate* fell 55%, so it is a conversion
> problem, not a traffic problem.

---

## 5. HANDLE WITH CARE — `pankanaturalhealth.com` self-referral is evidence, not junk

**Two different things wear similar names. Only one is the fingerprint, and neither should be
filtered right now.**

| Thing | Volume | What it is |
|---|---|---|
| `pageReferrer = www.pankanaturalhealth.com` | **48,084 events / 40,119 sessions / 794 conversions** — ~30% of every event in the property | **Ordinary internal page-to-page navigation.** Not a referral, not pollution, not the fingerprint. It appears in `pollution-quantified.csv` only so that nobody writes a naive "own domain in referrer" filter and sweeps up a third of the dataset. |
| `sessionSourceMedium = pankanaturalhealth.com / referral` | **1,594 events / 1,033 sessions / 46 purchase events worth $2,145** | **THIS is the fingerprint.** The Free Intro Call CTA jumps off-domain to Acuity; Acuity opens a brand-new GA4 session whose referrer is pankanaturalhealth.com itself; the originating ad click is erased at that instant. |

### Why removing it would destroy evidence

Those **46 purchase events are the second-largest source of purchases in the entire property**, behind
only `(not set)` (296) and ahead of `(direct)/(none)` (33) and `google / organic` (25). They are
currently the only surviving trace that those bookings happened through the scheduler hand-off.

Adding `pankanaturalhealth.com` to **List unwanted referrals** would stop GA4 starting a new session
on the Acuity round-trip. That *sounds* like the fix for the attribution break. **It is not — not
yet.** The original ad click is already gone by the time the referral fires; suppressing the referral
does not resurrect it, it just relabels those bookings as `(direct) / (none)`. The count survives; the
**diagnostic** does not. And the open work item that depends on it — repointing the 9 intro-call CTAs
to `/schedule-an-appointment?appointmentType=41826455` — would lose the before/after signal that
proves the fix worked.

### Correct order of operations

1. Repoint the 9 CTAs so the booking completes on-domain.
2. Confirm bookings start landing on-domain with a live end-to-end test.
3. Watch `pankanaturalhealth.com / referral` fall toward zero **on its own**. That decay *is* the
   proof the fix worked.
4. Only then, if it is still noisy, consider the unwanted-referral entry.

The same protection covers **`app.acuityscheduling.com` and `app.squarespacescheduling.com`**
(995 page-referrer sessions, 63 conversions; 105 session-grain sessions, 3 purchases). Same reason.
And `phr2.charmtracker.com` (§3e) — segment it out of marketing analysis, never filter it as spam;
one real $225 booking came through it.

**Compliance note:** nothing in §4 or §6 sends anything anywhere. Filtering pollution out of GA4 is
purely subtractive. The standing stance — completed-booking events carrying appointment type and tied
to a browser identifier do **not** go to Google — is untouched by every remedy below.

---

## 6. Remedies — steps Jacob performs himself

**Every one of these is a change Jacob makes in his own accounts. Nothing here is automatable and
nothing here should be delegated to an agent.**

### 6.1 Turn on the Developer traffic filter — the single highest-value, lowest-risk fix

This is the clean kill for the Tag Assistant pollution, and it costs nothing.

> GA4 → **Admin** (gear, bottom left) → **Data collection and modification** → **Data filters** →
> **Create filter** → **Developer traffic** → set **Filter state: Active** → Create.

It drops hits sent with `debug_mode` / Preview on — which is exactly what a Tag Assistant session is.
Do this before the next round of tag testing so the next test does not repeat 2026-06.

### 6.2 Unwanted referrals — for the *attribution* problem only

> GA4 → **Admin** → **Data collection and modification** → **Data streams** → click the **PNH2** web
> stream → **Configure tag settings** → **Show more** → **List unwanted referrals** →
> **Add condition** → match type **"Referral domain contains"**.

Add, one row each:

```
tagassistant.google.com
ads.google.com
apricots-crow-dwjh.squarespace.com
account.squarespace.com
secure.squarespace.com
us19.admin.mailchimp.com
wake-up-network.com
news.grets.store
seders.website
rida.tokyo
razas.site
drlinkcheck.com
deadlinkchecker.com
```

**DO NOT ADD — and this is the one that will get typed by mistake:**

```
pankanaturalhealth.com          ← §5. It is the booking fingerprint.
app.acuityscheduling.com        ← §5. Same.
app.squarespacescheduling.com   ← §5. Same.
squarespace.com                 ← too broad: it would also swallow app.squarespacescheduling.com.
                                   Use the two specific account./secure. hosts above instead.
phr2.charmtracker.com           ← §3e. Real patients. Segment, don't filter.
```

**Know what this setting actually does.** It does not delete traffic. It stops GA4 from *setting the
session source* from that referrer; the hit still lands and is re-attributed to whatever came before
(usually direct). It fixes labelling, not volume. For genuine bot and spam sessions (§3a, §3b) it is
the wrong tool — GA4's always-on "known bots and spiders" exclusion evidently did not catch these,
and there is no user-facing lever that will. Those months simply have to be read with the spam
counted.

### 6.3 Internal traffic filter by IP — for clinic traffic

Step 1, find the IP: from the clinic network, visit `whatismyipaddress.com` and note the public IPv4.
Ask the ISP whether it is static. If it is dynamic, use the stable prefix with "begins with".

Step 2, define it:

> GA4 → **Admin** → **Data collection and modification** → **Data streams** → **PNH2** →
> **Configure tag settings** → **Show more** → **Define internal traffic** → **Create** →
> Rule name `Clinic — Hopkins`, `traffic_type` value `internal`,
> Match type **IP address equals** (or **begins with**), value = the IP → **Create**.

Add a second rule for the home office IP if work is done from there.

Step 3, activate it:

> GA4 → **Admin** → **Data collection and modification** → **Data filters** → **Internal Traffic** →
> change **Testing** to **Active**.

Leave it on **Testing** for a few days first and check it in Explore using the
**Test data filter name** dimension. An IP filter set Active with a wrong IP silently deletes real
traffic, and that is not recoverable either.

### 6.4 Stop the preview domain at the source — better than any filter

The robust fix for §3c is not a GA4 setting. It is a hostname guard in the measurement code so the
tag never fires on the preview domain in the first place:

> Squarespace → **Settings** → **Advanced** → **Code Injection** → **Header**

Wrap the existing analytics/tag block so it only runs on the live host:

```js
if (location.hostname === 'www.pankanaturalhealth.com') {
  /* existing gtag / analytics block goes here, unchanged */
}
```

This kills 43 months' worth of a recurring problem permanently, is independent of GA4's filter
machinery, and cannot accidentally drop real traffic. Test by loading the site editor preview with
the browser console open and confirming no tag hits fire.

### 6.5 Non-GA4: look at Search Partners once

`syndicatedsearch.goog` (§3g) delivered 245 sessions in August 2026 against 293 from `google / cpc`.
In Google Ads: **Campaigns → Leads-Search-1 → Settings → Networks**, the "Include Google search
partners" checkbox. This audit does not recommend unchecking it — 5 conversions came from it in
August and the data is too thin to call. It recommends *looking*, because nobody has.

---

## 7. GA4 filters are NOT retroactive — what that means for this archive

**None of §6 changes a single historical number.** GA4 data filters and the unwanted-referral list
apply only to data collected after they are switched on. Every month in this archive keeps its
pollution permanently, and the Supermetrics subscription has ended, so there will be no cleaner pull.

**Read history with `pollution-quantified.csv` open beside it.** Three months in particular cannot
be quoted raw:

| Month | Problem | Magnitude |
|---|---|---|
| **2024-02** | `news.grets.store` referral spam | ~3,352 of 6,767 sessions — **~50%** |
| **2025-10** | `wake-up-network.com` UTM injection | 2,349 of 4,273 sessions — **55.0%** |
| **2026-06** | tag-build period: ads.google.com + tagassistant | **18.4%** of conversions, 7 of 44 purchases |

And two standing adjustments for any period:

- Subtract the **$1.00 purchase events** before counting bookings (§3i) — 30 all time, 7 of them in
  July 2026, and 3 of them wearing `google / cpc`.
- Keep `pankanaturalhealth.com / referral`, `app.acuityscheduling.com` and `phr2.charmtracker.com`
  **in** the data (§5).

---

## 8. Limits of this audit — stated so nobody over-reads it

1. **Grains do not add.** `sessionSourceMedium` and `pageReferrer` rows in the CSV overlap by
   construction. §1's "do not sum" warning is not a formality.
2. **No referrer × source cross-tab exists** in the archive, so the 52 Squarespace-preview conversions
   cannot be assigned to a channel. Permanently unresolvable — the subscription is over.
3. **The spam classifier is a heuristic** — an allowlist of ~60 recognised domain patterns, everything
   else in class F. `reliefplusmn.com` (47 sessions) and a handful of small local-business referrers
   are probably legitimate and are misfiled. Class F carries only 3 conversions in its entire history,
   so the misclassification cannot affect a conclusion.
4. **GA4's `conversions` column carries today's key-event definitions stamped onto historical rows**,
   the same hazard as `DATA-QUALITY.md` §1. A 2024 row showing 0 conversions may mean "that event was
   not a key event then", not "nothing happened".
5. **IP-level internal traffic cannot be measured from this archive at all.** GA4 does not expose IP,
   and the clinic IP was never registered as internal traffic, so clinic-staff browsing is
   *unquantified* — it is sitting inside `(direct) / (none)` and `google / organic` in unknown volume.
   §3c–§3e catch only the parts that arrived via an identifiable referrer. The true operator/internal
   share is higher than anything in this note, and there is now no way to find out how much higher.
6. **`(not set)` — 296 of 429 purchase events, $43,602 — is not analysed here.** It is the known
   Acuity attribution void (`README.md` caveat 7), not pollution, and it is out of scope for this pass.
