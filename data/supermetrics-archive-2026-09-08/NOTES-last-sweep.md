# NOTES — last-chance sweep before the subscription ends

**Run 2026-09-08, ~23:00 UTC. Subscription ends 2026-09-09.**
Scope: (1) find any authenticated data source nobody had checked, (2) pull breakdowns nobody had
captured, prioritising what cannot be reconstructed later, (3) write `DATA-QUALITY.md`, (4) verify
the archive on disk.

Everything below was pulled live and is in this directory. Where a pull failed or returned nothing,
that is recorded too — "we checked and there was nothing" is worth as much as data, because nobody
can check again after tomorrow.

---

## 1. Data source inventory — checked, and there is nothing else

`data_source_discovery()` with no `ds_id` returned **172 sources**. Authentication status:

| Status | Count | Which |
|---|---|---|
| `AUTHENTICATED` | **3** | **AW** Google Ads · **GAWA** Google Analytics · **GMB** Google My Business |
| `NOT_REQUIRED` | 6 | APPD Apple Public Data · BLEND Data Blending · FBPD Facebook Public Data · **GT Google Trends** · PIPD Pinterest Public Data · E5C14 Custom Data Import |
| `NOT_AUTHENTICATED` | 163 | everything else |

**Conclusion: the three sources already archived are the only authenticated sources on this
subscription. There is no fourth connector holding PNH data.** No Meta/Facebook Ads, no Microsoft
Ads, no Mailchimp, no CRM, no Squarespace connector, no call-tracking platform. Nothing was missed by
the earlier passes.

The `NOT_REQUIRED` entries are public-data connectors, not PNH accounts. They hold no clinic data.
Two were probed:

- **GT (Google Trends)** — `NOT_REQUIRED` for auth but **not licensed**:
  `[LICENSE_DATA_SOURCE_NOT_AVAILABLE] Data source Google Trends (GT) is not available in your
  license 1834401`. Both a core-terms and a service-line query were rejected. **No Trends data could
  be captured.** This is a small loss: Google Trends is free and public at trends.google.com, needs
  no subscription, and will still be there next year. The seasonality baseline the task wanted can be
  rebuilt by hand any time — it was the one item on the list that was never actually at risk.
- **FBPD / PIPD / APPD** — public-page scrapers for brands the clinic does not run paid media on.
  Nothing to capture.

---

## 2. New data captured

Five files, all previously absent from the archive.

| File | Rows | What it is |
|---|---|---|
| `ads-age-monthly.csv` | 173 | Age-range × month × ad group: impressions, clicks, cost, conversions, all-conversions |
| `ads-gender-monthly.csv` | 76 | Gender × month × ad group, same metrics |
| `ads-call-details.csv` | 4 | **Every phone call Google Ads has ever recorded on this account** |
| `ads-pmax-assetgroup-monthly.csv` | 2 | Asset-group-level performance for the paused PMax campaigns |
| `ads-pmax-assetgroup-assets.csv` | 153 | Full asset inventory of both PMax campaigns — asset IDs, every headline/description, YouTube video IDs, and resolvable image URLs |

### 2a. The tel: number is not untracked — there are four calls

This corrects a standing assumption. `CLAUDE.md` §5 lists `tel:+16125688382` under "zero tracking".
Google Ads' `CallView` report has been recording calls the whole time, via the campaign call asset.
The lifetime total is **four calls**, all `Received`:

| Date | Ad group | Type | Duration | Caller area code |
|---|---|---|---|---|
| 2025-07-15 | Ad group 1 | Manually dialed | **451 s (7m31s)** | 952 |
| 2026-08-07 09:01 | Functional & Integrative Medicine | Mobile click-to-call | 60 s | 952 |
| 2026-08-07 10:33 | Functional & Integrative Medicine | Mobile click-to-call | 15 s | 952 |
| 2026-08-11 | Pediatrics | Mobile click-to-call | 42 s | **619** |

Reading: three of four are local (952 = west metro). The 7m31s call in July 2025 is the only one
long enough to have been a real conversation, and it came from the manually-dialled number rather
than a click-to-call. The 619 area code is San Diego — a Pediatrics click that was almost certainly
out of area. Four calls in fifteen months is a real, small number; it is not a tracking gap.

**Caveat before anyone builds on this:** `CallView` only sees calls that went through a Google call
asset. Calls placed by someone reading the number off the website are invisible here, and the
website `tel:` link genuinely has no tracking. So four is the floor, not the total.

### 2b. Demographics — never looked at before, and there is something in it

Aggregated from the two new files, Leads-Search-1 only. **Read the conversion and CPA columns with
`DATA-QUALITY.md` §1 open** — they blend five counting regimes and are indicative only. The
impression, click, cost and CTR columns are clean and directly comparable.

**Gender, lifetime:**

| Gender | Impr | share | Clicks | CTR | Cost | share |
|---|---|---|---|---|---|---|
| Female | 12,060 | 50.2% | 755 | 6.26% | $1,934.20 | **60.0%** |
| Undetermined | 8,809 | 36.7% | 479 | 5.44% | $954.07 | 29.6% |
| Male | 3,160 | 13.2% | 153 | 4.84% | $335.35 | 10.4% |

Female traffic clicks harder than male and absorbs 60% of spend off 50% of impressions. For a clinic
whose largest ad group is Women's Health & Hormones, that is the system working as designed, not a
leak. Men's Health is genuinely small on the demand side, not just under-bid.

**Age, current campaign structure only (2026-07 → 2026-09):**

| Age | Impr | share | Clicks | CTR | Cost | cost share |
|---|---|---|---|---|---|---|
| 18-24 | 503 | 3.8% | 11 | 2.19% | $26.84 | 1.9% |
| 25-34 | 1,752 | 13.2% | 86 | 4.91% | $218.51 | 15.7% |
| 35-44 | 1,986 | 15.0% | 104 | 5.24% | $240.53 | 17.3% |
| 45-54 | 1,657 | 12.5% | 74 | 4.47% | $158.53 | 11.4% |
| 55-64 | 1,156 | 8.7% | 50 | 4.33% | $109.07 | 7.9% |
| **65+** | **1,158** | **8.7%** | **86** | **7.43%** | **$204.29** | **14.7%** |
| Undetermined | 5,032 | 38.0% | 267 | 5.31% | $431.11 | 31.0% |

**The 65+ band is the finding.** It takes 8.7% of impressions but **14.7% of spend**, on the highest
CTR of any age band (7.43%, against a 4.3–5.2% middle). Over the full lifetime it also carries the
**worst CPA of any band, $19.03**, against $7.59 for 25-34.

The mechanism is plausible and worth Jacob's attention: older searchers click "naturopathic doctor
near me"-style ads readily, but this is a cash-pay clinic with no insurance billing, and a
Medicare-age searcher is the demographic most likely to expect insurance to apply. High click rate,
poor conversion, disproportionate spend share is exactly the shape that produces.

**A step Jacob could take himself,** if he wants it — in Google Ads, Campaigns → Leads-Search-1 →
Audiences, keywords and content → Demographics → Age, set a **negative bid modifier on the 65+ band**
(−20% is a conservative first move; −30% is defensible given the cost share). This is a bid
adjustment, not an exclusion — it keeps the traffic and stops overpaying for it. It pairs naturally
with the existing device (−15% mobile) and ad-schedule modifiers he already runs, and it does not
touch Manual CPC.

Two honest caveats. First, 38% of impressions are `Undetermined`, so every share above is measured on
62% of the account and the true 65+ share could be higher or lower. Second, the CPA figures cross
the counting-regime boundary; the CTR and cost-share figures do not, and the case rests on those.

### 2c. PMax creative — preserved, and one campaign never ran

`ads-pmax-assetgroup-assets.csv` captures **153 assets** across three asset groups:

- **Campaign #1 / `6582377332` "Asset Group 1"** — 110 assets. This is the campaign that actually
  spent: **100,443 impressions, 3,386 clicks, $910.92** across 2025-06 and 2025-07. Two distinct
  creative generations are visible in the asset IDs — an original `2428…`/`2429…` set (*"Feel Better,
  Naturally"*, *"Evidence-Based Wellness"*) and a later `2522…`/`2523…` cost-anxiety rewrite
  (*"Avoid Expensive Doctors"*, *"Health Crisis Help"*, *"Smart Health Investment"*,
  *"Direct Pay Health Care"*). Includes YouTube video `B5Naf08R6pA` and an auto-generated shortened
  cut `-Wna-NMKDhQ`.
- **Leads-PMax-Video-1 / `6730142616` "A doctor who listens"** — 25 assets, incl. videos
  `LgH5zsiiwYc` and `ZTn9Ob94J6A`.
- **Leads-PMax-Video-1 / `6730142790` "Functional labs & prevention"** — 23 assets.

**Leads-PMax-Video-1 never served.** `ads-pmax-assetgroup-monthly.csv` has rows only for Campaign #1;
`ads-campaign-inventory.csv` confirms 0 impressions, 0 clicks, $0 for all three campaigns carrying
that name. Its creative — which is markedly better written than Campaign #1's, and on-message for the
current positioning — exists and has never been tested. That is worth knowing before anyone writes
new PMax copy from scratch.

The existing `ads-asset-group-creative.csv` (60 rows, from the campaign-settings JSON) covers the
text only. The new file adds asset IDs, asset source (`Advertiser` vs `Automatically created`),
YouTube IDs and **resolvable `tpc.googlesyndication.com/simgad/...` image URLs** — the only surviving
pointer to the actual images, since the creative was never exported.

---

## 3. Pulled and confirmed empty — do not go looking again

| Attempted | Result |
|---|---|
| **Auction Insights / competitor share** | **Not exposed by the connector at all.** The Google Ads connector has 40 report types; none is an auction-insights view. The MIMC conquesting question cannot be answered from Supermetrics, and could not have been at any point. |
| `CampaignAudienceView` (audience × campaign) | **"No data found."** |
| `AdGroupAudienceView` (audience × ad group) | **"No data found."** |
| `AssetGroupListingGroupFilter` (PMax listing groups) | **"No data found."** Expected — these are retail/Merchant-Center constructs and PNH sells no products through PMax. |
| Google Trends, MN, core + service-line terms | **License error, twice.** See §1. |

The two audience results are a genuine finding rather than a null: **the account has never used
audience targeting or observation.** No in-market segments, no affinity audiences, no remarketing
lists, no customer match — not even in observation mode, which would cost nothing and would have
produced exactly the segmentation data that is missing everywhere else in this archive. For a
practice with a clearly-defined patient population, that is an unused lever, and it is one of the few
that does not require abandoning Manual CPC.

---

## 4. Two connector limits found while sweeping

Both are new to the archive and are now recorded in `DATA-QUALITY.md` §9.

- **Google Ads history wall: 2023-08-08.** `[START_DATE_HISTORICAL] Earliest supported historical
  start date for Google Ads is 2023-08-08.` Never binding for PNH (delivery began 2025-06), but it
  caps what any re-pull could ever have reached.
- **Queries spanning more than 37 months without a date breakdown must align to calendar-month
  boundaries** — start on the 1st, end on the last day. Two pulls failed on this before succeeding.
  Noted so nobody reads those errors, in a future transcript, as the data being absent.

---

## 5. Archive verification

Every file in the directory was opened and checked: header present, data rows present, column count
consistent, no error strings standing in for data, no row count sitting on a suspiciously round
number, and valid JSON with no `error` / `success:false` payloads.

**Result: 92 CSVs, 46 JSON files, 13 Markdown notes, 18 Python scripts, 2 field-list text files.
Nothing empty. Nothing header-only. Nothing truncated. Nothing carrying an error string instead of
data.**

Specific checks:

- **No header-only CSV.** The smallest are `gmb-review-totals-lifetime.csv` (1 data row) and
  `ads-pmax-assetgroup-monthly.csv` (2) — both correct at that size.
- **No row count landed on 100/200/250/500/1000/1500/2000/5000/10000**, the values that would suggest
  a silent `max_rows` cap. The largest files (`ga4-events-by-source-daily.csv` 29,605;
  `ads-search-terms-monthly.csv` 8,629; `ga4-geo-monthly.csv` 8,849) are all at irregular counts,
  which is what a complete pull looks like.
- **All 46 `raw-*.json` and `campaign-settings-*.json` files parse** and none carries an error field.
- **`raw-*.json` files are single-line with no trailing newline**, so `wc -l` returns 0. Confirmed
  normal, not a defect — flagged in `DATA-QUALITY.md` so a future reader does not "fix" it.

Files written by other agents while this sweep ran (`ga4-schedule-page-reach-by-landing-paid.csv`,
`NOTES-ga4-events.md`, `NOTES-ga4-pages-channels.md`) were included in the verification and pass.

---

## 6. `DATA-QUALITY.md` — what it covers

Written as instructed, at `DATA-QUALITY.md` in this directory. It documents, each against the
specific file and column it applies to: the five conversion-counting regimes and the 2026-07-12
splice; the seven-month dark period; the 0.0999 impression-share floor; the removed-ad-group keywords
still reporting Enabled; GA4 `purchase` overcounting bookings by ~45%; tag-assistant and
ads.google.com self-referral pollution; the GBP 2025-03-08 history wall; GBP search-term suppression
below ~15/month; and why `pankanaturalhealth.com / referral` is real booking evidence rather than
junk. It ends with **15 numbered comparisons that are not valid to make with this data**.

**One correction it carries, which supersedes the task brief and `README.md` caveat 5.** The figure
"~65 keywords in the removed ad group still reporting Enabled" is **34**. Verified in
`ads-keywords-alltime.csv`: 34 distinct keywords under `AdgroupID 183759893484` with
`Adgroupstatus = removed` and `Keywordstatus = enabled`. 65 was a count of monthly rows, not of
keywords. `NOTES-ads-keywords.md` had already caught this; `DATA-QUALITY.md` now states it where
someone reading only the guardrail will see it.

---

## 7. What is still gone, after this sweep

The sweep did not recover, and nothing can now recover:

- **Google Trends seasonality** — not licensed here, but freely available at trends.google.com. The
  only item on the task list that is not actually lost.
- **Auction Insights** — never available through this connector.
- **Paid search before 2025-06** — 5,824 `google / cpc` sessions in GA4 from a Google Ads account
  that is not this one. If Jacob's Google Ads login shows other accounts, that history may still
  exist in the UI. It is not reachable from here.
- **Business Profile before 2025-03-08.**
- **The seven dark months, 2025-09 → 2026-03.**
- **The link between an ad click and a patient.** Attribution breaks at the Acuity scheduler, and
  under the compliance stance set this week — no completed-booking events, with appointment type,
  tied to a browser identifier, sent to Google, absent a BAA — it stays broken by choice. The Acuity
  export remains the only booking truth, and it lives outside this archive.
