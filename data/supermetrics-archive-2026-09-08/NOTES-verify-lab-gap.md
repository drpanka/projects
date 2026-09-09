# Verifying the "Functional Lab Testing gap" claim

Written 2026-09-08. Sources: `gmb-search-keywords.csv`, `gmb-search-keywords-classified.csv`,
`gmb-search-keywords-bucket-summary.csv`, `campaign-keywords.csv`, `campaign-negatives.csv`,
`ads-search-terms-rollup.csv`, `ads-search-terms-monthly.csv`, `ads-keywords-alltime.csv`,
`ads-impression-share-floor-analysis.csv`, `ads-cpa-like-for-like-monthly.csv`.
No new Supermetrics queries were run. Everything below is from the local archive.

## Verdict up front

**The gap is real but it is small, and it is already being served.** A dedicated Functional Lab
Testing ad group is **not worth launching at $10/day**. Recommended action is a
**Tier 1 eight-keyword addition to the existing Functional & Integrative Medicine ad group**, which
costs nothing structurally, or — more honestly — **do nothing in paid search and fix the free
channel instead**, because the same demand is reaching the Google Business Profile where the booking
count has been zero every month.

Spec is in `proposed-lab-testing-adgroup.csv`, written conditionally with the Tier 2 half explicitly
gated on a budget increase.

---

## 1. Non-brand demand reaching the Business Profile, by theme

134 distinct profile search terms, 274 keyword-month rows, 2025-04 through 2026-07 (16 months of
data, not 18 — the connector's window).

| Theme (bucket) | Distinct kw | kw-month rows | Est. impressions (midpoint) | % of est. | **Reported** impressions |
|---|---:|---:|---:|---:|---:|
| geo/discovery | 73 | 177 | 1,536 | 66.4% | 216 |
| brand | 6 | 24 | 192 | 8.3% | 0 |
| modality/other-service | 15 | 22 | 176 | 7.6% | 0 |
| **Functional Lab Testing** | **5** | **12** | **96** | **4.2%** | **0** |
| other/irrelevant | 6 | 9 | 72 | 3.1% | 0 |
| Women's Health & Hormones | 8 | 8 | 64 | 2.8% | 0 |
| Pediatrics | 7 | 8 | 64 | 2.8% | 0 |
| competitor/practitioner name | 7 | 7 | 56 | 2.4% | 0 |
| Gut Health | 4 | 4 | 32 | 1.4% | 0 |
| Metabolic/Diabetes | 2 | 2 | 16 | 0.7% | 0 |
| Men's Health | 1 | 1 | 8 | 0.3% | 0 |
| **TOTAL** | **134** | **274** | **2,312** | 100% | **216** |

### How uncertain these numbers are — this is the whole story

**262 of 274 keyword-month rows (95.6%) are below Google's reporting threshold and render as 0.**
The estimate imputes 8 impressions to each suppressed row (the midpoint of a 1–15 band).

- Only **216 impressions in the entire dataset were actually reported by Google.** All 216 belong to
  three keywords: `naturopathic doctor` (102), `naturopathic doctor near me` (79),
  `holistic doctor near me` (35). Everything else in the table above is imputation.
- Whole-file range: midpoint 2,312, **low 478, high 4,146** — a factor of 8.7 between bounds.
- **Functional Lab Testing bucket: midpoint 96, low 12, high 180.** Every one of its 12 rows is
  suppressed; its reported impressions are **zero**. The honest statement is "somewhere between
  about 1 and 11 profile impressions per month," not "four a month."
- The 4.2% share is therefore a **share of an imputation, not a measurement**. Because every bucket
  except geo/discovery is ~100% imputed, the *relative* shares are close to just a count of
  keyword-month rows. They are ordinally informative and quantitatively near-meaningless.
- Direction of bias: these are **underestimates of unknown size**. Suppression truncates from below
  only, and long-tail terms that never crossed threshold in any month are absent from the file
  entirely. There is no way from this data to bound how much is missing.

(The task brief said "72 estimated impressions across 18 months." The archive says **96 across 16
months**. Minor, but the archive figure is the one in the files.)

### The five lab-testing terms in full

| Profile keyword | Est. (mid / low / high) | Months seen | Window |
|---|---|---:|---|
| food sensitivity test | 40 / 5 / 75 | 5 | 2025-05 → 2025-12 |
| food sensitivity testing near me | 32 / 4 / 60 | 4 | 2025-08 → 2026-02 |
| ebv specialist holistic | 8 / 1 / 15 | 1 | 2026-03 |
| food sensitivity testing | 8 / 1 / 15 | 1 | 2025-11 |
| holistic lymes disease testing minneapolis | 8 / 1 / 15 | 1 | 2025-08 |

**Food sensitivity is 80 of the 96 estimated impressions and 10 of the 12 rows.** The "Functional Lab
Testing" theme on the profile is, in practice, *one query family* seen in six separate months. That
recurrence across months is the genuinely useful signal — a single term appearing in six distinct
months is harder to dismiss as noise than one appearing once with a bigger imputed number.

### Correction to the claim's framing

The claim's headline examples do not all belong to this theme:
- `thyroid testing` (1 month, est 8) is classified **Women's Health & Hormones**, not Lab Testing.
- `holistic doctor for pcos` (1 month, est 8) is **Women's Health & Hormones**.
- `pediatric functional medicine near me` (1 month, est 8) is **Pediatrics**.
- "a dozen suburb names" is real and is the **largest** finding here — but it is
  **geo/discovery, 66.4% of estimated volume**, and Leads-Search-1 already has a
  Geo-Qualified — Hopkins & West Metro ad group with 11 keywords. That is not a gap.

So three of the four named example queries map to service lines that **already have dedicated ad
groups with 34, 6 and 8 keywords respectively.** The claim overstates the gap by attributing
already-covered demand to the uncovered theme.

---

## 2. Verifying the gap in the campaign — and checking for active harm

### The literal gap is confirmed

`campaign-keywords.csv`, Leads-Search-1, 115 keywords across 6 live ad groups plus 15 stranded in the
dead "Ad group 1" (max CPC $0.01):

| Ad group | Keywords | Match types | Group max CPC |
|---|---:|---|---:|
| Women's Health & Hormones | 34 | 30 phrase / 4 broad | $2.60 |
| Men's Health | 31 | 14 phrase / 17 broad | $1.30 |
| Functional & Integrative Medicine | 17 | 12 phrase / 5 broad | $1.90 |
| Naturopath Near Me — Core | 15 | 3 phrase / 11 broad / 1 exact | $2.50 |
| Geo-Qualified — Hopkins & West Metro | 11 | 10 phrase / 1 exact | $2.60 |
| Pediatrics | 6 | 2 phrase / 4 broad | $2.40 |
| ~~Ad group 1~~ (dead) | 15 | 5 phrase / 10 exact | $0.01 |

**Not one keyword in any live ad group contains `test`, `testing`, `lab`, `labs`, `panel`, `dutch`,
`blood work`, or the name of any specific assay.** The claim is correct on its face.

### Are any protect-list terms sitting in the negatives? — checked, and the answer is no

This was the dangerous possibility, and it did not materialise. All 466 Leads-Search-1 campaign
negatives were scanned for the protect-list stems. Seven negatives touch testing vocabulary:

| Negative | Match | Assessment |
|---|---|---|
| `free testing` | phrase | Fine. Price-zero seekers, not cash-pay patients. |
| `free labs` | phrase | Fine, same. |
| `self test` | phrase | Fine. DIY intent. |
| `home test` | phrase | Fine. DIY kit intent. Contiguous-phrase only — does not block "at home food sensitivity testing". |
| `nrt testing` | phrase | Fine. Nutrition Response Testing is a chiropractic modality PNH does not offer. |
| `naturopath muscle testing` | phrase | Fine. Applied kinesiology, not offered. |
| `labcorp` | phrase | Fine. Brand-navigational to a competitor lab. |

**No blanket block on `test`, `testing`, `panel`, `labs`, `dutch`, `thyroid`, `pcos` or
`micronutrient` exists anywhere.** Nothing here is actively harmful. All seven are narrowly scoped
and every one of them should stay. The theme is *absent*, not *suppressed* — a meaningfully weaker
finding than "actively blocked," and worth saying plainly.

Two smaller notes:
- **Negative count is 466 for Leads-Search-1, not 451.** `CLAUDE.md` §3 and the reconciliation
  header both say 451. The archive shows 466 distinct campaign-level negatives (453 phrase, 11
  exact, 2 broad). Whichever is right, the docs are stale by ~15. Worth a one-minute check in the UI.
- All 15 proposed keywords were run against all 466 negatives with a match-type-correct blocking
  simulation (exact = string equality; phrase = contiguous token span; broad = all tokens present).
  **Zero conflicts.** Nothing on the list would look active and silently never serve.

### But the gap is not a coverage gap

`ads-search-terms-rollup.csv` shows the theme reaching the account anyway, through broad and phrase
keywords in the existing groups. Broad match still survives in five live ad groups (11 in Core, 17 in
Men's, 5 in Functional, 4 in Pediatrics, 4 in Women's), so this coverage is not going away.

Every lab query in section 3 below was matched by an existing keyword. **Adding a lab-testing ad
group does not open new demand. It re-routes demand the campaign already receives.**

---

## 3. What the theme has actually done in the account

Narrow definition — the query literally expresses testing/lab intent
(`test|tests|testing|tested|panel|panels|lab|labs|lab work|blood work|dutch|screening|assay`):

**184 distinct queries · 275 impressions · 15 clicks · $27.68 · 1 conversion**
= 2.0% of lifetime impressions, 1.7% of lifetime cost, 0.6% of lifetime conversions.

Every one of the 15 clicks, itemised:

| Query | Imp | Clicks | Cost | Conv | Matched by ad group |
|---|---:|---:|---:|---:|---|
| testosterone test | 4 | 1 | $4.62 | 0 | Men's Health |
| hormone testing near me women | 2 | 1 | $3.89 | 0 | Ad group 1 |
| dutch complete | 1 | 1 | $2.90 | 0 | Women's Health & Hormones |
| micronutrients testing | 2 | 1 | $2.34 | 0 | Functional & Integrative / Men's |
| **where to get hormones tested** | 1 | 1 | $2.34 | **1** | Women's Health & Hormones |
| food sensitivity test | 4 | 1 | $2.29 | 0 | Functional & Integrative |
| nrt testing near me | 3 | 1 | $2.20 | 0 | Functional & Integrative |
| sibo testing near me | 4 | 1 | $1.96 | 0 | Ad group 1 / Core |
| labcorp hormone panel | 1 | 1 | $1.18 | 0 | Women's Health & Hormones |
| food sensitivity test near me | 2 | 1 | $1.13 | 0 | Ad group 1 / Functional |
| hormone testing near me | 6 | 2 | $1.08 | 0 | Women's Health & Hormones |
| electrodermal screening near me | 3 | 1 | $0.74 | 0 | Functional / Core |
| dutch test hormones | 9 | 1 | $0.55 | 0 | Functional / Men's / Women's |
| how to get a prostate cancer test | 1 | 1 | $0.46 | 0 | Men's Health |

Plus **38 zero-cost queries with 2+ impressions each: 100 impressions, 0 clicks.** Highest:
`hormone testing for women` (7), `functional lab testing` (6), `dutch test near me` (6),
`functional lab testing near me` (4), `hormone testing for women near me` (4),
`nutrition response testing` (4), `food allergy testing near me` (3), `dutch hormone test` (3),
`sibo test` (3), `holistic hormone testing` (3).

### The named example queries, specifically

| Claimed query family | Distinct queries | Imp | Clicks | Cost | Conv |
|---|---:|---:|---:|---:|---:|
| food sensitivity / food allergy testing | 14 | 24 | 2 | $3.42 | 0 |
| DUTCH / hormone testing | 49 | 92 | 7 | $11.94 | **1** |
| micronutrient / nutrient testing | 4 | 6 | 1 | $2.34 | 0 |
| generic "functional lab testing" | 11 | 22 | 0 | $0.00 | 0 |
| gut / SIBO / stool testing | 11 | 17 | 1 | $1.96 | 0 |
| thyroid (all forms) | 86 | 133 | 7 | $14.61 | **1** |
| PCOS (all forms) | 68 | 146 | 8 | $14.52 | **3** |
| pediatric functional/integrative | 12 | 42 | 3 | $4.47 | 0 |

The four conversions in this whole space:
`holistic pcos doctor near me` (2 conv, $0.64, **Naturopath Near Me — Core**),
`where to get hormones tested` (1, $2.34, **Women's Health**),
`best pcos doctors near me` (1, $1.71, **Women's Health**),
`lump in neck thyroid` (1, $0.73, **Women's Health**).

**All four came from ad groups that already exist.** None came from a pure testing query — they came
from *condition* and *practitioner* queries. Pulling PCOS and thyroid into a lab-testing group would
move the account's only converting queries in this space out of the group that converts them.

### CTR and CVR test

- Theme CTR: 15/275 = **5.5%**. Campaign CTR: 4.9% (Jul 2026), 5.7% (Aug 2026). **Not better.**
- Theme CVR: 1/15 = **6.7%**. Not a usable estimate at n=15, but nothing in it argues "hot."
- Recent monthly footprint (`ads-search-terms-monthly.csv`, Leads-Search-1):
  Jul 2026 143 imp / 9 clicks / $14.81 / 1 conv (4.1% of impressions);
  Aug 2026 93 / 3 / $6.28 / 0 (2.8%); Sep 1–7 13 / 1 / $1.96 / 0 (1.6%).

**The theme runs about $6–15/month at present, on 1.6–4.1% of impressions, and has produced one
conversion in the account's entire history.**

### Landing page

`/clinical-laboratory-tests` was supplied in the brief and is not verifiable from this archive —
no page-path file here lists it. It does not appear in `ga4-events-by-page-monthly.csv` traffic
worth noting. **Confirm the URL loads before pasting it into any ad group.** If it exists it is the
right destination and is a genuine advantage over the current behaviour (these queries currently
land on generic functional-medicine pages).

---

## 4. The counter-argument, stated properly

**This should not launch as a new ad group now.** The reasons, strongest first:

1. **The budget is the binding constraint, and a new ad group does not relax it — it divides it.**
   Budget-lost impression share has been 67–90% every day since mid-August (Sep 1–7: 81%, 90%, 89%,
   81%, 89%, 89%, 67%). Rank-lost is 5–25%. Reported 9.99% search impression share is Google's
   reporting floor; true captured share is 1.6–7.7%. At $10/day the campaign already cannot serve
   the demand it has. **Every impression a new lab-testing group wins is an impression Women's Health
   or Core loses.** The lab theme's conversion record is 1 in 15 clicks; Women's Health's is 20 in
   188 and Core's is 10 in 71. Reallocating toward the untested theme is a bet against the account's
   own evidence.

2. **The demand is already being served.** All 275 impressions arrived through existing keywords.
   The new group would win the same auctions with better ad copy — a Quality Score and landing-page
   argument, not a reach argument. That is a real but second-order gain, and second-order gains do
   not justify structural changes during peak season on a starved budget.

3. **The nearest analogue ad group is the account's worst performer.** Functional & Integrative
   Medicine: 247 clicks, $513.48, 17 conversions = **$30.20 CPA**, against Men's $9.44, Pediatrics
   $13.17, Core $13.77, Geo $13.28, Women's $23.15. (Lifetime figures mixing conversion-counting
   regimes — directional only, see `ads-cpa-like-for-like-monthly.csv`.) A lab-testing group is a
   *narrower* Functional & Integrative. Betting that the narrow version beats the broad version, when
   the broad version is the weakest thing in the account, needs evidence this data does not contain.

4. **The GMB evidence is 100% imputed.** Zero reported impressions in the bucket. True range 12–180
   over 16 months. It is enough to say "the theme exists." It is not enough to size anything.

5. **The strongest thing this analysis found is not a paid-search finding at all.** The theme's best
   signal — food sensitivity testing, six distinct months on the profile — is *organic* profile
   demand. Google Business Profile bookings are **zero in every month of the 550-day record**, and a
   duplicate listing (`10418367222074184209`) is sharing the name, phone and website with the live
   one. Free demand is arriving at a profile that cannot convert it. Fixing that costs $0 and has a
   larger addressable base (2,312 est. profile impressions) than $10/day of paid search can buy.
   **Do that before spending money on this theme.**

### What to do instead — in order

**Step A (Jacob, ~5 minutes, do now).** Add the **8 Tier 1 phrase keywords** from
`proposed-lab-testing-adgroup.csv` to the **existing Functional & Integrative Medicine ad group**
(id `198432290338`). No new ad group, no new ad copy, no budget split, group max CPC already $1.90 —
which is the right bid anyway: realized CPC on this account's actual lab-testing clicks is $1.85, and
because 67–90% of loss is budget rather than rank, bidding higher buys nothing. Add
`/clinical-laboratory-tests` as a **sitelink** on the campaign rather than as a final URL, so the
page gets tested without restructuring anything. Add the four companion negatives listed at the
bottom of the CSV. This is reversible in one click and risks roughly $10/month of spend.

**Step B (free, higher value).** Resolve the duplicate GBP listing and get the booking link working
on the live profile. That addresses the same food-sensitivity demand at zero cost.

**Step C (gate).** Revisit the Tier 2 keywords and a dedicated ad group **only when both are true**:
daily budget is at $25+ (the level at which the account produced its best like-for-like CPA), **and**
Tier 1 has accumulated at least 20 clicks so there is something to judge. On current volume — 3–9
lab-theme clicks per month — that is a **three to six month wait**. Say so plainly rather than
reviewing it in two weeks and calling 5 clicks a result.

**Do not** move PCOS, thyroid, or hormone-condition keywords out of Women's Health & Hormones. That
is where all four of this space's conversions came from.

---

## 5. One-line answer to the claim

True that no keyword names the lab-testing service line; false that the demand is unserved — 275
impressions and 15 clicks have already reached the account through existing keywords, producing one
conversion, and three of the four queries the claim cites belong to service lines that already have
their own ad groups. The gap is worth **eight keywords in an existing ad group**, not a new ad group,
and not until the budget question in `CLAUDE.md` §8.1 is settled.

## Files written
- `/home/user/projects/data/supermetrics-archive-2026-09-08/proposed-lab-testing-adgroup.csv`
- `/home/user/projects/data/supermetrics-archive-2026-09-08/NOTES-verify-lab-gap.md`
