# NOTES — adversarial verification of the "dead inventory" claim

**Agent slug:** `verify-dead-inventory` · **Written:** 2026-09-08 · **Sources:** archive only, no
Supermetrics quota spent. Files used: `ads-keywords-alltime.csv`, `ads-keywords-zero-conversion.csv`,
`ads-keywords-current-inventory.csv`, `ads-keywords-monthly.csv`, `ads-geo-alltime.csv`,
`ads-geo-monthly.csv`, `ads-geo-locationtarget-alltime.csv`, `ads-geo-locationtarget-daily.csv`,
`ads-search-terms-alltime-incl-zero-cost.csv`, `ads-change-history.csv`,
`campaign-settings-22767146837.json`, `ads-cpa-like-for-like-monthly.csv`, `ads-campaign-monthly.csv`.

**Outputs:** `verified-pause-candidates.csv` (160 rows), `verified-city-performance.csv` (88 rows).

---

## 0. Verdict in one paragraph

The claim's **arithmetic is reproducible** — I hit $352.09 and $232.38 almost exactly from the archive —
but its **conclusion does not survive**. The Sept-7 rebuild already removed or paused nearly all of the
keyword spend it points at, so most of the money it names is unrecoverable history, not a live leak.
Of the live inventory, **zero keywords clear a defensible pause threshold**, and the single keyword that
clears the money bar turns out not to be a zero-conversion keyword at all once you look at all-conversions.
On cities, **five of the eight named cities are not location targets and cannot be paused** — the money
reached them through the 22-mile radius. The cannibalisation mechanism as stated is wrong: same-ad-group
keywords do not bid against each other. The real effect is reporting fragmentation, and it is worth
fixing for a reason the claim never mentions.

**Recommended action: pause nothing. Add one location exclusion, put two cities on watch, and delete
nine redundant phrase keywords for reporting hygiene only.** Expected performance impact: none.

---

## 1. Where the claim's numbers came from (they are real)

| Claim | Closest exact reproduction from the archive |
|---|---|
| "22 current keywords, $352 lifetime spend, zero conversions" | The **top 20 zero-conversion keyword rows by cost** in `Leads-Search-1` sum to **$352.09**. Deduped by keyword text, the top 18 sum to $350.07 and the top 22 to $381.25. The number is genuine; the count is off by about two either way. |
| "twelve near-duplicate functional medicine synonyms" | Of those top 20 rows, **13 sit in the *Functional & Integrative Medicine* ad group** and two more are `functional medicine for hormones` / `functional medicine hormones` in Women's Health. "Twelve" is fair. |
| "7 keywords served impressions and were never clicked" | **Understated.** 16 currently-**enabled** keywords have impressions and zero clicks; 41 such rows exist account-wide. All at **$0.00 cost** — no click, no charge. |
| "8 cities took $232 and never converted" | The **top 8 zero-conversion cities in the Geographic view for `Leads-Search-1`** sum to **$232.38**. Exact. |

So nobody made these up. The problem is what the numbers are attached to.

---

## 2. Keywords — the accurate split as of 2026-09-08

`verified-pause-candidates.csv` carries every zero-conversion keyword record in `Leads-Search-1`, with
a `bucket`, a `can_serve_today` flag, lifetime and current-regime stats, and a per-row verdict.

The task asked for three buckets. **There are four**, and the fourth is the one that dissolves the claim.

| Bucket | Meaning | Rows | Lifetime cost | Clicks | Impressions |
|---|---|---:|---:|---:|---:|
| **A — live** | enabled keyword, enabled ad group, enabled campaign. Can serve today. | **82** | **$52.03** | 22 | 504 |
| **B — paused** | paused on 2026-09-07. Cannot serve. | 21 | $146.01 | 78 | 1,713 |
| **C — dead ad group** | inside the removed "Ad group 1". Reports `Enabled`, **cannot serve**. | 20 | $36.87 | 15 | 255 |
| **D — criterion removed** | live ad group, but the criterion itself is `removed` — these are the **broad originals destroyed by the Sept-7 broad→phrase conversion**. Cannot serve. | **37** | **$225.40** | 106 | 2,351 |
| | | **160** | **$460.31** | 221 | 4,823 |

Bucket A's 82 rows are 35 keywords KeywordView knows about plus 47 that exist in the campaign resource
and have never accrued a single reportable statistic.

**$408.28 of the $460.31 — 89% — sits in buckets B, C and D. It is spent money on criteria that cannot
serve again.** Pausing them is not possible; they are already gone. The claim's $352 is drawn almost
entirely from that 89%.

The live slice is **$52.03 across 82 keywords, an average of $0.63 per keyword over the campaign's
entire life.**

### 2.1 Bucket A, ranked — everything that can actually serve and has ever cost money

| Keyword | Match | Ad group | Impr | Clicks | Lifetime $ | All-conv | Regime-E clicks |
|---|---|---|---:|---:|---:|---:|---:|
| naturopathic doctor Minneapolis | Phrase | Geo-Qualified | 77 | 8 | $20.55 | **7** | 4 |
| perimenopause doctor near me | Phrase | Women's | 24 | 3 | $6.42 | 0 | 3 |
| natural help for menopause | Phrase | Women's | 20 | 2 | $4.82 | 0 | 1 |
| holistic hormone doctor near me | Phrase | Women's | 2 | 1 | $4.43 | 0 | 0 |
| naturopath for endometriosis | Phrase | Women's | 2 | 2 | $4.00 | 0 | 2 |
| pcos specialist near me | Phrase | Women's | 5 | 1 | $2.91 | 0 | 1 |
| naturopathic dr near me | Broad | Core | 81 | 2 | $2.88 | 0 | 0 |
| endometriosis specialist near me | Phrase | Women's | 2 | 1 | $2.86 | 0 | 1 |
| functional medical doctors | Phrase | Functional | 2 | 1 | $1.81 | 0 | 1 |
| natural practitioner near me | Broad | Core | 2 | 1 | $1.35 | 0 | 1 |

The other 72 live zero-conversion keywords have spent **$0.00**: 16 took impressions and were never
clicked, 56 have never taken an impression at all.

---

## 3. The threshold, stated before it is applied

A keyword is a pause candidate only if **all four** hold:

1. **It can serve today.** Buckets B/C/D are moot by construction.
2. **Money bar — lifetime cost ≥ $20.00.** One new-patient enquiry is worth $450; $20 is roughly eight
   clicks at the campaign's $2.50 CPC. Below that there is not enough money at stake to justify the risk
   of removing a query that converts off-tracking.
3. **Evidence bar — lifetime clicks ≥ 15.** `Leads-Search-1` over 2026-07→09 ran **674 clicks / 69
   tracked conversions = 10.2% CVR** (like-for-like on begin-checkout all-conversions it is 99/674 =
   14.7%). At p = 0.102, the chance of a keyword with a *campaign-average* conversion rate producing
   zero conversions in 15 clicks is 0.898^15 = **0.20**. So 15 clicks with zero conversions is roughly
   80% confidence the keyword is below average. A 90% bar would require 22 clicks; a 95% bar, 28.
4. **Zero on all-conversions too, not just on the primary metric.** `DATA-QUALITY.md` documents five
   changes to what counted as a primary conversion in fifteen months. `Conversions = 0` can simply mean
   "the keyword's clicks landed in a month when a different action was primary." `AllConversions` is
   the regime-independent test.

I also record a fifth, stricter column — **regime-E clicks (2026-08 onward)** — because clicks split
across two counting definitions are not one sample.

### 3.1 Result of applying it

**Zero keywords qualify.** Not one.

- Only **one** live keyword clears the money bar: `naturopathic doctor Minneapolis`, $20.55.
  It fails criterion 4 outright — it has **7 lifetime all-conversions**. It is not a zero-conversion
  keyword; it is a keyword whose conversions were counted under a regime that is no longer primary.
  It also fails the evidence bar at 8 lifetime clicks.
- **No live keyword reaches 15 lifetime clicks.** The highest is 8.
- **Under the current conversion definition the maximum is 4 clicks** on any live zero-conversion
  keyword. There is no keyword in this campaign with enough post-August data to convict.

This is the honest state of the account: at $10–15/day with 88 enabled keywords, **no individual keyword
will ever accumulate enough clicks to be judged.** That is a budget-and-structure fact, not a keyword fact.

---

## 4. The cannibalisation claim — wrong as stated, but there is a real effect underneath

**The stated mechanism is false.** Keywords in the same ad group do not bid against each other and do not
raise each other's CPC. When more than one keyword in an account is eligible for a query, Google runs
exactly one of them; for same-ad-group duplicates it picks the highest Ad Rank and the rest simply do not
enter. There is no double charge, no bid inflation, no budget waste from redundancy per se. Nothing in
this archive shows otherwise: every impression in `ads-search-terms-*` is attributed to exactly one
keyword, and the location-target and keyword rollups both reconcile to the campaign total of $3,215.35
with no double counting.

**What I checked for that *would* have been a real problem, and did not find:**

- **The same keyword text in two different ad groups** — the genuinely damaging case, because Google's
  pick is by Ad Rank and may route the query to the wrong ad and landing page. **0 occurrences** in the
  current 114-keyword inventory.
- **The same text twice inside one ad group at different match types.** **0 occurrences.**

**What is actually there — subsumption and dispersion.** In *Functional & Integrative Medicine*, 13
enabled keywords, of which:

- `functional medicine` (Phrase) **contains** and therefore covers six of the others:
  `functional medicine near me`, `functional medicine clinic near me`, `functional medicine doctors near me`,
  `functional medicine practice near me`, `functional medicine practitioner`,
  `functional medicine practitioner in my area`.
- `functional medicine practitioner` (Phrase) subsumes `functional medicine practitioner in my area`.
- `integrative medicine near me` (Phrase) subsumes `functional integrative medicine near me`.

The overlap shows up directly in the search-term log: of 1,614 distinct search terms this ad group has
ever matched, **304 (18.8%) were matched by more than one of its keywords over time.** The query
`integrative medicine` alone has been matched by **17 different keywords** in this one ad group;
`functional medicine doctor` by 11.

**So the effect is neither cannibalisation nor nothing. It is measurement dispersion, and it has three
components — one material, two not:**

| Effect | Real? | Size here |
|---|---|---|
| Duplicate spend / self-bidding | **No** | $0. Not a mechanism that exists. |
| **Unjudgeable reporting** | **Yes, material** | The ad group's $250.51 lifetime spend is split 26 ways. The two biggest keywords took 24 and 29 clicks; **24 of 26 never reached 10 clicks.** With a 15-click evidence bar, 24 of 26 keywords in this ad group are permanently unevaluable at current budget. This is exactly why section 3 returns nothing. |
| Diluted quality-score signal | **Yes, but mild** | Google reports a keyword-level QS for only 24 of 170 lifetime rows — the rest never earned enough volume. But QS falls back to ad-group, account and display-URL history when keyword data is thin, and all these keywords share one ad group and one landing page, so the fallback is the same signal. Historical QS actually *rose* through the rebuild (4.50 in 2025-07 → 6.59 in 2026-07). No evidence of harm. |

**Does it justify action? Yes — but as reporting hygiene, worth roughly an hour, with no expected
performance change.** Removing the nine subsumed keywords consolidates their traffic onto the covering
keyword and starts building a sample that can eventually be read. It will not lower CPC, will not raise
CTR, and will not change which queries the campaign can reach, because the covering keyword already
matches everything they match.

---

## 5. Cities — `verified-city-performance.csv`

### 5.1 The eight cities in the claim

| # | City | Lifetime $ | Clicks | Conv | Is it a location target? | Verdict |
|---|---|---:|---:|---:|---|---|
| 1 | Maple Grove MN | $54.68 | 24 | 0 | **Yes — re-created 2026-09-07** | WATCH (13 regime-E clicks) |
| 2 | Little Canada MN | $45.10 | 29 | 0 | **No** | Exclusion candidate — only reachable as an added exclusion |
| 3 | Shakopee MN | $32.86 | 15 | 0 | **Yes — re-created 2026-09-07** | WATCH (6 regime-E clicks) |
| 4 | Eagan MN | $25.24 | 13 | 0 | **No** | Below evidence bar |
| 5 | Dellwood MN | $23.29 | 5 | 0 | **No** | Below evidence bar |
| 6 | Savage MN | $18.18 | 11 | 0 | **No** | Below money bar |
| 7 | Lakeville MN | $17.00 | 9 | 0 | **No** | Below money bar |
| 8 | Otsego MN | $16.03 | 8 | 0 | Was — **removed 2026-09-07** | Moot |
| | **Total** | **$232.38** | | | | |

**Five of the eight — $128.81 — are not and never were location targets.** They are inside the 22-mile
radius around the clinic. "Pausing" them is not an available action; the only lever is an explicit
negative location, and excluding suburbs inside your own catchment because of a dozen clicks each is not
a defensible trade at this sample size. Otsego is already gone.

That leaves **two live targets**, and here is the finding worth Jacob's attention: **Maple Grove and
Shakopee were both re-created as location targets on 2026-09-07 at 13:08**, and they are the #1 and #3
worst zero-conversion cities in the account's history. Whether that matters depends on which bid modifier
each received — see 5.3.

### 5.2 What the location-target report says (the targeting-side truth)

`ads-geo-locationtarget-alltime.csv` attributes every click to exactly one target and sums to $3,215.35 —
the campaign total. On that basis:

- **The 22-mile radius is the campaign.** From 2026-07 onward it carries essentially all delivery:
  $626.29 of $626.29 in July, $633.20 of $651.84 in August, $97.98 of $102.47 in September.
  Lifetime $1,357.46 at a $19.96 CPA — **the worst CPA of any target**, against Minneapolis at $6.85.
- The named city targets (Minneapolis, Hopkins, Edina, Golden Valley, Plymouth, Eden Prairie, Chanhassen,
  St. Louis Park, Minnetonka, Maple Grove, Wayzata, Deephaven) stopped serving after **2026-06** — they
  were removed in the June restructure and replaced by the radius.
- Five exurb targets (Otsego, Dayton, Ramsey, Saint Michael, Albertville) were **added in 2026-08** and
  took **$21.14 lifetime with one conversion** before being removed on 2026-09-07.
- Zero-conversion location targets, lifetime: Maple Grove $17.57, Otsego $9.59, Wayzata $7.34,
  Deephaven $6.23, Dayton $5.82, Ramsey $4.07, plus Albertville / Bloomington / Shakopee at $0.00.
  **Nine targets, $50.61 total** — not $232. The $232 figure is a Geographic-view number and cannot be
  acted on through the targeting list.

### 5.3 Two things in CLAUDE.md I could not confirm, and one I can correct

- **Bid modifiers are not in this archive.** The campaign resource pulled 2026-09-08 exposes
  `bid_adjustments` containing **only** `devices: [{MOBILE, 0.85}]`. No location modifiers appear —
  Supermetrics' resource reader does not seem to return them, so **absence here is not evidence they
  are missing from the account.** The change history is consistent with them existing: nine
  `CAMPAIGN_CRITERION UPDATE` events run 13:08:28–13:10:03 on 2026-09-07, immediately after nine
  `CREATE` events at 13:08:21 — nine creations, nine modifier edits, matching "six cities at −30% and
  three at +10%" exactly. **Jacob should read the two rows for Maple Grove and Shakopee off the
  Locations tab himself.** If they are in the −30% set, this thread is closed.
- **"Nine exurb targets removed" is not supported.** The change history records **six**
  `CAMPAIGN_CRITERION REMOVE` events on 2026-09-07 between 13:39:06 and 13:42:11, and only five exurbs
  visibly stop serving (Otsego, Saint Michael, Albertville, Ramsey, Dayton). The count in CLAUDE.md
  should probably read six.
- **Six of the nine current geo targets are identifiable** by the fact that they began serving on
  2026-09-07 for the first time since June: **Bloomington, Eden Prairie, Hopkins, Maple Grove, Plymouth,
  Shakopee.** The remaining three took zero impressions in their first two days and cannot be named from
  this archive (the public geo-target-constant table is not reachable from this environment; the IDs are
  1019810, 1019888, 1019925, 1020070, 9051607, 9051855, 9052387, 9052691, 9189294 — Google Ads shows the
  names directly).

### 5.4 The confound that limits all of it

**Almost all of the zero-conversion city spend lands in 2026-08** — Maple Grove $31.54 of $54.68,
Little Canada $37.81 of $45.10, Eagan $17.08 of $25.24, Lakeville $14.96 of $17.00. August 2026 is the
month the archive has already established as anomalous: same spend and clicks as July, like-for-like
conversions halved from 67 to 28. These cities did not fail in isolation; they were mostly spending
during the month the whole campaign stopped converting. Attributing that to geography would be a
composition error.

---

## 6. Framing — what this work is and is not worth

Today's like-for-like analysis established that **July 2026 was the account's best month ever, at
$9.35 CPA, running 102 keywords.** The "keyword dilution raised CPA" story is dead. It follows that
pruning keywords is **housekeeping, not a fix**, and nothing in this file should be read as a lever on
performance.

Concretely, the total live money at stake in the entire "dead inventory" thesis is **$52.03 spent over
fifteen months across 82 keywords**, and **$50.61 across nine location targets, six of which are already
removed.** Against a campaign losing 81–89% of its impressions to budget every day, this is a rounding
error. The measurable levers remain budget, the broken booking attribution, and whatever happened in
August — not this list.

The one non-obvious thing worth doing is the opposite of pruning: **the reporting fragmentation described
in section 4 is why none of these questions can be answered.** Fewer, broader keywords would let the
account accumulate a readable sample. That argument stands on its own and does not need a CPA story.

---

## 7. Recommended steps — for Jacob, performed by Jacob

Ordered by value. None of them is urgent.

1. **Look up two bid modifiers.** Google Ads → Leads-Search-1 → Locations. Read the bid adjustment on
   **Maple Grove** and **Shakopee**. If either is at +10%, set it to −30% to match the other underperformers.
   If both are already −30%, do nothing — this thread is closed. *Two minutes.*
2. **Pause no keywords.** Nothing in the live inventory clears the threshold in section 3. In particular
   do not pause `naturopathic doctor Minneapolis` — it has seven all-conversions and is the Geo group's
   only keyword with any history at all.
3. **Delete nine redundant phrase keywords in *Functional & Integrative Medicine*, for reporting only.**
   Keep `functional medicine` (Phrase) and remove the six it subsumes —
   `functional medicine near me`, `functional medicine clinic near me`, `functional medicine doctors near me`,
   `functional medicine practice near me`, `functional medicine practitioner`,
   `functional medicine practitioner in my area` — plus `functional integrative medicine near me`
   (subsumed by `integrative medicine near me`). That is seven; extend to nine by also dropping
   `best functional doctor near me` and `best functional doctors near me`, which have two impressions
   between them. Coverage does not change. Expect **no** CPA or CTR movement — the point is that the
   surviving keywords will finally accrue a readable sample. *Fifteen minutes.*
4. **Leave the 16 never-clicked keywords alone for now.** They have cost $0.00 — no click, no charge.
   Their only cost is CTR drag on Quality Score, and three of them (`pediatric holistic doctor near me`
   152 impressions, `natural pediatrician near me` 51, `best naturopath near me` 30) are Broad match in
   peak pediatric season, which CLAUDE.md §6 explicitly defers to Oct 1. Revisit with the rest of Block 6.
5. **Consider one location exclusion: Little Canada, MN.** $45.10 and 29 clicks with zero conversions,
   21 of those clicks under the current conversion definition — the only geographic entity in the account
   that clears both bars within one measurement regime. Caveat carried forward from `NOTES-ads-geo-device-time.md`:
   Little Canada is a known Twin Cities IP-geolocation sink, so some of those "clicks from Little Canada"
   are probably not from Little Canada. Excluding it is low-risk and low-value; it is a judgement call,
   not a finding. *Optional.*
6. **Correct CLAUDE.md** on two points: nine exurb targets removed → **six**; and note that the archive
   cannot see location bid modifiers, so that line rests on the change history, not on a state read.

---

## 8. Caveats on this file

- Every "zero conversions" here is zero on the **tracked** conversion, which per CLAUDE.md §5 is a
  page-reach event on `/schedule-an-appointment`, not a booking. Acuity is the only booking truth and
  Google Ads has seen one of 66 bookings. A keyword or a city showing zero may have produced real
  patients. This is the single strongest reason the recommendation is "pause nothing".
- Keyword and ad-group statuses in the source CSVs are **today's** status stamped on historical rows.
  Bucket assignment is therefore correct for *now* and meaningless as history — see `NOTES-ads-keywords.md` §3.
- Keyword criterion IDs are not unique across ad groups; every join in this work keys on
  (AdgroupID, keyword text, match type).
- The Geographic view blends physical presence with area of interest in general. For `Leads-Search-1`
  specifically it is 100% LOCATION_OF_PRESENCE, so section 5's city figures are safe on that axis.
- The three unnamed current geo targets are a genuine gap. They had taken zero impressions as of
  2026-09-08 and cannot be resolved from the archive.
