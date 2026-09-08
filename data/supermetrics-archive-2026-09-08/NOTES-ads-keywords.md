# NOTES — Google Ads keyword-level archive
**Agent slug:** `ads-keywords` · **Pulled:** 2026-09-08 · **Source:** Supermetrics MCP, `ds_id=AW`,
`ds_accounts=7473953248`, `timezone=America/Chicago`, `settings={"include_zero_impressions": true}`
**Window requested:** 2025-06-01 → 2026-09-08 (all available history; see §2)

This is the evidence base for the *"the rebuild diluted the budget"* question. Read §3 and §4 before
quoting any keyword count from this archive — the naive count is wrong in a specific, load-bearing way.

---

## 1. Files written

| File | Rows | What it is |
|---|---|---|
| `ads-keywords-monthly.csv` | 310 | Keyword × month, both campaigns, 24 fields. Task 1. |
| `ads-keywords-alltime.csv` | 170 | Lifetime keyword rollup, 59 fields incl. quality score, top-of-page/first-page CPC, full impression-share family. Task 2. Sorted by cost desc. |
| `ads-keywords-zero-conversion.csv` | 116 | Every keyword with zero lifetime conversions, cost desc, with `impressions_but_never_clicked` / `never_served` / `can_serve_today` flags. Task 3. |
| `ads-keyword-count-by-month.csv` | 16 | Distinct active keywords per month, five different definitions side by side, plus explicit `NO DATA` rows for the dark months. Task 4. |
| `ads-keywords-current-inventory.csv` | 114 | **Extra.** The authoritative current keyword list for Leads-Search-1 with per-keyword enabled/paused. Not requested, but it is the only correct source for the "now" number — see §4. |
| `ads-keywords-quality-score-monthly.csv` | 383 | **Extra.** Historical quality score / predicted CTR / ad relevance / landing-page experience by month (report type `KeywordViewQsMetrics`). |

Raw JSON kept alongside every CSV (`raw-*.json`) so the pulls can be re-derived without Supermetrics.
Build scripts: `build_kw.py`, `build_kw_counts.py`, `build_kw_inventory.py`.

**Column headers are the Supermetrics `requested_field_ids`, not the display names.** Row 0 of the API
response carries display names that collide (e.g. `MaxCPC` and `MaxCPCCurrency` both render as
"Max CPC"); every CSV here uses the field IDs instead.

---

## 2. History is shorter and more broken than "2025-06 → now" implies

Verified with a campaign-level monthly pull back to **2024-01-01**: nothing before 2025-06 exists.
Within the window there is a **seven-month dead zone**:

| Month | Leads-Search-1 | Other |
|---|---|---|
| 2025-06 | — | Campaign #1 (PMax) $357.26 |
| 2025-07 | $774.63 | Campaign #1 (PMax) $553.66 |
| 2025-08 | $659.60 | — |
| **2025-09 → 2026-03** | **nothing. zero rows, zero delivery, seven consecutive months** | |
| 2026-04 | $186.22 | — |
| 2026-05 | $190.24 | PNHdefense $0.01 |
| 2026-06 | $24.06 | PNHdefense $111.01 |
| 2026-07 | $626.29 | PNHdefense $47.04 |
| 2026-08 | $651.84 | — |
| 2026-09 (1–8) | $102.47 | — |

Lifetime keyword spend reconciles exactly: **$3,373.41** = $3,215.35 Leads-Search-1 + $158.06
PNHdefense. Campaign #1 is Performance Max and therefore has no keyword rows at all — its
$910.92 is outside this archive by definition.

The dark zone matters for the dilution question: 2025-08 and 2026-07 are **not** adjacent periods
that can be compared as "before and after a rebuild." They are eleven months apart with the account
switched off in between, and the conversion-counting regime changed too (see CLAUDE.md §4).

---

## 3. THE TRAP: ad-group and keyword status are current-state, not as-of-month

Every `Adgroupstatus` / `Keywordstatus` value in these files is **today's** status stamped onto
historical rows. Google's KeywordView report does not carry historical status. This creates the
exact hazard the task flagged, and one more on top of it:

**"Ad group 1" (`183759893484`)** is `removed` today. Its keywords still all report
`Keywordstatus = enabled`. So the naive filter *"enabled keyword AND non-removed ad group"* is
correct for **today** and catastrophically wrong for **history** — applied to 2025, it reports
**zero active keywords in a month that spent $659.60 and took 3,675 impressions.**

That ad group was the *entire* account through 2026-06. Lifetime it carries **$1,834.76 — 57% of
all Leads-Search-1 keyword spend ever** — and 253.02 of the 348.23 lifetime conversions.

**Correction to the task brief:** the brief said "~65 keywords" in that ad group. 65 is the number of
*monthly rows*. The distinct keyword count is **34**. All 34 report as Enabled inside a Removed ad
group.

Second, quieter trap: **Google criterion IDs are shared across ad groups.** `KeywordID` alone is not
unique — e.g. `296740931208` ("holistic dr near me") appears under both the removed *Ad group 1* and
the live *Naturopath Near Me — Core*. Every count in this archive keys on **(AdgroupID, KeywordID)**.
Keying on `KeywordID` alone undercounts by roughly 20%.

Third: a **match-type change mints a new criterion ID.** The Sept-2026 broad→phrase conversion did
not edit keywords, it created new ones and removed the old. That is why 61 Leads-Search-1 rows read
`Keywordstatus = removed` inside *enabled* ad groups, and why lifetime history for a "single" keyword
is split across two rows.

---

## 4. "19 keywords then, 83 now" — tested

### "19 then" — CONFIRMED, exactly.
**August 2025 reported exactly 19 keywords.** Not approximately. 17 of the 19 took impressions;
`naturopathic doctor Minneapolis` (Phrase) and `holistic healthcare Minneapolis` (Broad) took zero.
All 19 sat in *Ad group 1*. The top four — `integrative medicine near me`, `naturopathic doctor near
me`, `holistic dr near me`, `naturopathic doctor Minneapolis` — took $518.54 of the month's $659.60.

July 2025 was 15 reported / 14 serving, for comparison.

### "83 now" — CLOSE, but the correct figure is **88**.
From the campaign resource (authoritative for what exists today), cross-referenced against the
KeywordView paused set:

| Ad group | Enabled | Paused | Total |
|---|---:|---:|---:|
| Women's Health & Hormones | 30 | 4 | 34 |
| Men's Health | 16 | 15 | 31 |
| Functional & Integrative Medicine | 13 | 4 | 17 |
| Naturopath Near Me — Core | 12 | 3 | 15 |
| Geo-Qualified — Hopkins & West Metro | 11 | 0 | 11 |
| Pediatrics | 6 | 0 | 6 |
| **TOTAL** | **88** | **26** | **114** |

All six ad groups are ENABLED and the campaign is ENABLED, so all 88 can serve.

The 26 paused matches CLAUDE.md's "26 keywords paused" exactly, which is the cross-check that makes
the 88 trustworthy. **All 26 paused keywords are Broad match** — the Sept-7 pause was a clean sweep of
leftover broad. Live match-type mix is now **71 phrase / 15 broad / 2 exact**.

I could not find a defensible derivation for 83. The candidates in the data are 88 (enabled today),
114 (total today), 102 (served in 2026-07), and 45 (reported so far in 2026-09, a partial month).
Whoever quoted 83 may have counted before a later addition, or excluded the Geo group's 11.

### Why the naive query would have said something else
KeywordView, even with `include_zero_impressions: true`, returns only keywords that have accrued
reportable stats. It shows **67** current Leads-Search-1 keywords (41 enabled + 26 paused), not 114.
**57 of the 114 current keywords have never taken a single impression** and are invisible to every
performance report. That is why `ads-keywords-current-inventory.csv` is built from the campaign
resource, not from a data_query.

---

## 5. The dilution evidence, stated plainly

Spend and impressions per *serving* keyword, Leads-Search-1 only:

| Month | Keywords serving | Spend | $/keyword | Impressions | Impr/keyword |
|---|---:|---:|---:|---:|---:|
| 2025-07 | 14 | $774.63 | **$55.33** | 4,780 | 341 |
| 2025-08 | 17 | $659.60 | **$38.80** | 3,675 | 216 |
| 2026-04 | 7 | $186.22 | $26.60 | 1,160 | 166 |
| 2026-05 | 14 | $190.24 | $13.59 | 1,117 | 80 |
| 2026-06 | 7 | $24.06 | $3.44 | 53 | 8 |
| 2026-07 | 96 | $626.29 | **$6.52** | 6,250 | 65 |
| 2026-08 | 71 | $651.84 | **$9.18** | 5,534 | 78 |
| 2026-09 (8 days) | 41 | $102.47 | $2.50 | 1,331 | 32 |

**Monthly spend in 2026-07/08 is within 5% of 2025-07/08. The keyword count is 4–6× higher.**
Per-keyword budget fell from $38.80–$55.33 to $6.52–$9.18 — a **77–88% reduction in dollars behind
each keyword** at effectively unchanged total spend. Forward-looking it is tighter still: 88 enabled
keywords against the current $15/day budget is ~$456/month, **$5.18 per keyword per month**.

This is a mechanical fact about arithmetic, not a claim about what caused the CPA change. Two
confounders are large enough that they must travel with this number: the eleven-month gap and the
conversion-counting change described in CLAUDE.md §4. Impressions-per-keyword collapsing from 216–341
to 65–78 is the cleaner signal, because impressions are not affected by the conversion re-definition.

---

## 6. Zero-conversion keywords

**116 of 170 lifetime keyword rows have never produced a tracked conversion, on $488.66 of spend —
14.5% of all keyword spend ever.** Leads-Search-1 alone: 113 rows, $460.30 (14.3%).

Breakdown:
- **41 keywords took impressions and never once received a click.** Combined cost: **$0.00** (no
  click, no charge). These cost money only in the sense that they consumed auction entries. The
  largest is `naturalist dr near me` at 166 impressions / 0 clicks — currently *paused*.
  `pediatric holistic doctor near me` (152 impr / 0 clicks) is currently **enabled**.
- **19 keywords have never served at all** (zero impressions across their whole life).
- **35 zero-conversion keywords can still serve today** (enabled, live ad group, enabled campaign),
  carrying $52.03 of lifetime spend. This is the actionable slice; the other $436 sits on keywords
  already removed or paused and cannot be re-spent.

Largest single zero-conversion spends: `integrative medicine near me` Broad $47.27 (removed),
`functional medicine for hormones` Broad $42.00 (paused), `naturopaths in my area` Broad $23.95
(paused), `female naturopath` Broad $23.14 (paused). Note the pattern — the expensive
zero-conversion keywords are overwhelmingly **Broad**, and most have already been paused or removed.
The one still live and expensive is `naturopathic doctor Minneapolis` Phrase, $20.55 / 8 clicks / 0
conversions in the Geo group.

**Caveat that limits how far this file can be pushed:** "conversions" here is the Google Ads tracked
conversion, which per CLAUDE.md §5 is a *page-reach* event, and the counting basis changed around
2026-08-01. A keyword showing zero conversions may have produced real bookings that were never
attributed. Do not treat this file as a kill list. It is a list of candidates to *examine*.

---

## 7. Quality score

Current QS exists for only 24 of 170 lifetime rows (Google reports QS only for keywords with recent
serving history). `ads-keywords-quality-score-monthly.csv` has the historical series — 103 keyword-months
with a value.

Monthly average historical QS: 2025-07 **4.50** (n=6) → 2025-08 5.50 (n=6) → 2026-04 6.20 (n=5) →
2026-05 5.45 (n=11) → 2026-06 5.89 (n=9) → 2026-07 **6.59** (n=27) → 2026-08 5.96 (n=24) →
2026-09 6.13 (n=15).

QS improved through the rebuild — but the sample grew from 6 to 27 keywords at the same time, so the
month-over-month averages are not comparable populations. The brand keywords in PNHdefense
(`panka natural health`, `panka health` = QS 10) sit in the same file and will pull any account-wide
average upward; filter on `Campaignname` before averaging.

---

## 8. State drift since CLAUDE.md was written (2026-09-07 1:52pm)

Observed live today, differing from the reference file:

- **Daily budget is $15, not $10.** CLAUDE.md §3 records $10.00 and flags the downward trend as open
  thread #1. It has since moved up.
- **Negative keywords now 466, not 451.** Fifteen added.
- **Geo-Qualified ad group has 11 keywords, not 10.** CLAUDE.md's ad-group line reads 34/31/17/15/10/6
  = 113; live is 34/31/17/15/**11**/6 = 114.
- Bidding confirmed still `MANUAL_CPC`; 10 location targets, matching the forward plan.

I did not change anything. These are read-only observations for Jacob to reconcile.

---

## 9. Gaps, failures, and things I could not get

1. **No history before 2025-06-01.** Confirmed by querying from 2024-01-01 — the API returns nothing
   earlier. Not a pull failure; the data does not exist.
2. **Seven months with no data at all** (2025-09 → 2026-03). Represented as explicit `NO DATA` rows in
   `ads-keyword-count-by-month.csv` rather than being silently absent.
3. **`include_zero_impressions: true` does not do what its name promises for keywords.** It surfaced 26
   zero-impression rows in the monthly pull and 19 never-served keywords in the lifetime pull, but it
   does **not** return the full current keyword inventory — 57 of 114 live keywords are missing from
   every performance report. Worked around with the campaign resource; flagging it because any future
   "how many keywords do we have" query written against data_query alone will be wrong.
4. **Per-keyword status is unavailable from the campaign resource.** `campaign_and_resource_get` returns
   all 114 keywords with `status: null`. The 88/26 split in `ads-keywords-current-inventory.csv` is
   therefore a **join**: 26 keywords confirmed paused from KeywordView, and the remaining 88 inferred
   enabled because they exist as live criteria and are not in the paused set. The `status_source`
   column records which of the two each row came from — 67 measured, 47 inferred. The inference is
   sound (a criterion in a live ad group is enabled, paused, or removed; removed ones are not returned
   by the resource) but it is an inference, and it is the number the "83 vs 88" question turns on.
5. **Historical ad-group / keyword status does not exist** in the Google Ads reporting API. §3.
6. **`FirstPositionCpc`, `EstimatedAddClicksAtFirstPositionCpc`, `EstimatedAddCostAtFirstPositionCpc`
   returned empty for every row.** The fields exist and were accepted; Google returned no values.
   Columns retained in the CSV so the absence is visible rather than assumed.
7. **`CreativeQualityScore` / `PostClickQualityScore` / `SearchPredictedCtr` are text labels**
   ("Above average" / "Average" / "Below average"), not numbers. The numeric equivalents are the
   `Historical*_metric` fields in the QS-monthly file.
8. **Impression-share metrics floor at 0.0999 (9.99%)**, Google's standard low-IS masking. A row
   reading 0.0999 means "≤10%", not "9.99%". Do not average these columns.
9. **Conversion figures are not comparable across the archive.** Per CLAUDE.md §4 two conversion
   actions were double-counted until ~2026-08-01. Cost, clicks and impressions are clean throughout;
   conversions, CPA, conversion rate and ROAS are not. Every conversion-derived number in this archive
   inherits that caveat, including §6.
10. **Campaign #1 (PMax, $910.92 over 2025-06/07) has no keyword rows** — correct for Performance Max,
    but it means keyword spend ≠ account spend for those two months.
11. **`Leads-PMax-Video-1` (24032465476) returned no rows in any pull** — no delivery in its lifetime.
