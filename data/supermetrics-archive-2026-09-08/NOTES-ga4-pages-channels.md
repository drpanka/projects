# NOTES — GA4 traffic, channels, landing pages, and the scheduling-page question

Property **353828960 (PNH2)**, ds_id `GAWA`. Captured 2026-09-08, timezone `America/Chicago`,
full history `2023-02-01` → `2026-09-08`. Written by the GA4 pages/channels agent; this file is
mine, the eight `NOTES-ads-*` / `NOTES-gbp-*` files and `README.md` belong to other agents.

---

## 1. Files written

| File | Rows | Grain |
|---|---|---|
| `ga4-channels-monthly.csv` | 260 | month × `sessionDefaultChannelGrouping` |
| `ga4-source-medium-monthly.csv` | 941 | month × `sessionSourceMedium` × channel |
| `ga4-landing-pages-monthly.csv` | 1641 | month × `landingPage`, all sources |
| `ga4-landing-pages-paid-monthly.csv` | 220 | month × `landingPage`, `sessionSourceMedium == google / cpc` |
| `ga4-pages-monthly.csv` | 3799 | month × `pagePath` × `pageTitle` |
| `ga4-device-monthly.csv` | 131 | month × `deviceCategory` |
| `ga4-newreturning-monthly.csv` | 133 | month × `newVsReturning` |
| `ga4-geo-monthly.csv` | 8849 | month × city × region × country |
| `ga4-schedule-page-reach.csv` | 187 | the item-6 analysis — see §3 |
| `ga4-schedule-page-reach-by-landing-paid.csv` | 15 | month × landing page × `/schedule-an-appointment`, paid only |
| `ga4-device-newreturning-channel-monthly.csv` | 1261 | the raw combined pull the two split files come from |

Builder: `build_ga4_pages_channels.py`. Raw API payloads: `raw-ga4-source-medium-monthly.json`,
`raw-ga4-landing-pages-monthly.json`, `raw-ga4-pages-monthly.json`, `raw-ga4-geo-monthly.json`,
`raw-ga4-device-newreturning-channel-monthly.json`, `raw-ga4-schedule-page-daily.json`.

### Provenance caveat you must know about
Two of these files — `ga4-channels-monthly.csv` and `ga4-landing-pages-paid-monthly.csv` — came
back small enough that the API returned them inline instead of writing a file, so they were
**transcribed** rather than machine-converted. Both were then validated cell-by-cell against
`ga4-source-medium-monthly.csv`, which *was* machine-converted from its raw payload:

- Channels: **1,299 of 1,300 cells match exactly.** The single exception is `2026|01 Organic
  Search sessions` (255 at channel grain, 256 summed from source/medium) — a genuine GA4
  cross-grain artefact, not a typo, confirmed because `engagedSessions/sessions = 170/255 =
  0.6667` reproduces the `engagementRate` GA4 itself returned on that row.
- Paid landing pages: month totals reconcile to `google / cpc` exactly once you account for the
  finding in §5 below; residual differences are ±1 session cross-grain noise.

---

## 2. Where the traffic actually comes from

Last 12 months (2025|10 – 2026|09), 8,542 sessions:

| Channel | Sessions | Share | Engagement rate | Key events |
|---|---|---|---|---|
| Direct | 3,603 | 42.2% | 34.3% | 432 |
| Organic Search | 2,632 | 30.8% | 62.8% | 314 |
| Referral | 1,095 | 12.8% | 81.8% | 125 |
| **Paid Search** | **893** | **10.5%** | 61.3% | 141 |
| Organic Social | 233 | 2.7% | 49.8% | 2 |
| Unassigned / Cross-network / AI Assistant | 86 | 1.0% | — | 132 |

Two things worth flagging to Jacob:

- **Direct is 42% of sessions and has by far the worst engagement rate (34%).** A direct share
  that large next to an engagement rate that small is the classic signature of attribution loss,
  not of brand strength. It is the same disease as the `(not set)` bookings already documented.
- **Paid Search is only 10.5% of sessions** over twelve months, because the account was dark
  2025-09 → 2026-03. Over the live months it is much larger: 28% of July 2026 sessions.
- `Referral` includes the `pankanaturalhealth.com / referral` self-referral pollution already
  documented in `ga4-self-referral-pollution.csv`, plus two one-off spikes (2024|02 = 859
  sessions, 2025|10 = 586 sessions) that are bot/scanner traffic, not people.

---

## 3. ITEM 6 — the scheduling-page question, answered

### The verdict

**It is a drop in SESSIONS, not in event count. It is real behaviour, and it is confined to paid
search. The data distinguishes the two cleanly.** Three independent lines of evidence:

**(a) The event is redundant with `page_view`, so a tagging artefact is not available as an
explanation.** On `/schedule-an-appointment`, `schedule_appointment` and `page_view` track each
other exactly — July 2026 paid: 61 page_view events / 56 sessions vs 61 schedule_appointment
events / 56 sessions. August 2026 paid: 23 / 20 vs 23 / 20. `page_view` is a GA4 automatic event
fired by the base tag on every page of the site, and it kept firing normally everywhere else
(paid page_views site-wide: 710 in July, 470 in August). For the drop to be a tagging artefact,
GA4's own automatic `page_view` would have had to break on one page for one channel only.

**(b) Events per reaching session did not change; the number of reaching sessions did.** A
tagging artefact reduces events while sessions hold. The opposite happened:

| Paid Search | Jul 2026 | Aug 2026 |
|---|---|---|
| Sessions reaching the page | 56 | 20 |
| Page views of the page | 61 | 23 |
| **Page views per reaching session** | **1.09** | **1.15** |

The ratio is flat (slightly up). Only the population fell.

**(c) The other channels are a clean control, and they did not move.** Weekly reach rate
(sessions that viewed `/schedule-an-appointment` ÷ all sessions in that channel):

| Week beginning | Paid Search | Direct | Organic Search |
|---|---|---|---|
| 2026-07-06 | 23.5% | 17.1% | 6.0% |
| 2026-07-13 | 9.5% | 22.0% | 8.6% |
| 2026-07-20 | 15.4% | 10.4% | 14.8% |
| 2026-07-27 | 13.9% | 16.3% | 22.6% |
| **2026-08-03** | **7.9%** | 23.9% | 19.4% |
| **2026-08-10** | **5.7%** | 23.9% | 26.0% |
| **2026-08-17** | **7.0%** | 20.3% | 27.8% |
| **2026-08-24** | **2.7%** | 10.2% | 6.2% |
| **2026-08-31** | **2.9%** | 15.3% | 18.0% |

If the page's tag had broken, every channel would have fallen together. Direct and Organic
Search are flat-to-rising across exactly the weeks Paid Search collapses. Site-wide reach barely
moves at all (11–19% every week from June through August). **This is a paid-traffic problem, not
a measurement problem.**

### The week it breaks

**Monday 2026-08-03 (ISO 2026-W32).** Paid reach goes 13.9% → 7.9% that week and never recovers;
a second step down lands the week of 2026-08-24 (2.7%). Monthly: 15.95% (Jul) → 6.85% (Aug).

That week is not a spend week to blame. Google Ads for 2026-W32 shows **113 clicks and $240.64 —
the largest click and spend week in the whole series** — against W31's 110 clicks / $222.91. CTR
was steady (5.31% → 5.72%) and CPC was steady ($2.03 → $2.13). Same volume of clicks, same cost
per click, one third of the on-site follow-through. This is the same break the ads-side team
already found as "like-for-like conversions halved, 67 → 28, on identical spend and clicks" — it
is one event seen from two sides, and the GA4 side localises it to the week of Aug 3.

### Reconciling the "roughly 70 a month to about 6" claim

That claim does not survive contact with the data, and whoever repeats it should stop. Sessions
reaching `/schedule-an-appointment`, all channels, by month, run 180 (Jul 2026) → 152 (Aug 2026)
→ 21 (Sep 1–8, a partial month at a normal run rate). Across the whole 2023–2026 history the
series never leaves the 21–180 band except for the July 2025 bot spike (488). There is no 70 → 6
collapse anywhere in the site-wide series.

The nearest real figures the claim may be a garbled memory of:
- **Paid sessions reaching the page: 56 → 20 → 3** (Jul / Aug / Sep-to-date). This is the real
  finding and is what should be quoted.
- **Paid sessions that *landed directly on* the scheduling page: 13 → 6.** That is the literal
  "about 6", but it is a landing-page count, not scheduling-page reach.

### Why it happened

One more query splits paid reach by the page the session started on
(`ga4-schedule-page-reach-by-landing-paid.csv` against `ga4-landing-pages-paid-monthly.csv`):

| Paid landing page | Jul sessions → reached | Jul rate | Aug sessions → reached | Aug rate |
|---|---|---|---|---|
| `/` (home) | 172 → 24 | 14.0% | 125 → 8 | **6.4%** |
| `/womens-health-services` | 63 → 11 | 17.5% | 92 → 2 | **2.2%** |
| `/mens-health` | 38 → 4 | 10.5% | 24 → 1 | 4.2% |
| `/pediatrics` | 24 → 4 | 16.7% | 12 → 2 | 16.7% |
| `/schedule-an-appointment` (landed on it) | 13 → 13 | — | 6 → 6 | — |

The rate fell on essentially every entry point, so this is **not** a landing-page mix shift —
although the mix did shift too (`/womens-health-services` went from 18% to 32% of paid sessions
while home fell from 49% to 43%). Both halves of reach fell: navigated-to 43 → 14, landed-on
13 → 6.

The mechanism that does fit is a change in **which queries were being bought**. The ad-group
click mix moved sharply in exactly this window:

| Ad group | Jul 2026 clicks | share | Aug 2026 clicks | share |
|---|---|---|---|---|
| Functional & Integrative Medicine | 102 | 30.1% | 131 | **41.6%** |
| Women's Health & Hormones | 71 | 20.9% | 98 | **31.1%** |
| Naturopath Near Me — Core | 36 | 10.6% | 23 | 7.3% |
| Geo-Qualified — Hopkins & West Metro | 36 | 10.6% | 19 | 6.0% |
| Men's Health | 39 | 11.5% | 24 | 7.6% |
| Pediatrics | 25 | 7.4% | 20 | 6.3% |
| Ad group 1 | 30 | 8.8% | — | removed 2026-07-31 |

The two groups that carry booking intent — "naturopath near me" and the Hopkins/West Metro geo
group — fell from 21.2% of clicks (72) to 13.3% (42), and "Ad group 1" was removed outright on
2026-07-31. Their share went to condition-and-modality research terms. `ads-change-history.csv`
shows ad-group and targeting edits on 2026-07-29, 07-31, **08-03**, 08-07 and 08-10 — the rebuild
straddles the exact week the reach rate breaks.

So: **August bought the same number of clicks at the same price from people who were researching
rather than looking for a local doctor.** The account did not stop measuring; it changed what it
was buying.

### What this does NOT tell us
- It says nothing about *bookings*, only about reaching the scheduling page. Booking attribution
  is still broken for the reasons already documented.
- Correlation with the ad-group rebuild is strong and the timing is tight, but no single change
  entry is a proven cause. A same-period search-term read (`ads-search-terms-monthly.csv`) would
  firm it up.
- Nothing here needs a change to how scheduling events reach Google, and nothing here is
  weakened by the compliance stance. This was diagnosed entirely from page-reach data.

### Steps for Jacob, if he wants to act on it
1. Compare the Jul vs Aug search-term reports for Functional & Integrative Medicine and Women's
   Health & Hormones side by side, and look for research-phrasing queries that entered in August.
2. Consider restoring bid weight to Naturopath Near Me — Core and Geo-Qualified — Hopkins &
   West Metro, which lost half their click share in the rebuild.
3. Check whether `/womens-health-services` has a scheduling CTA above the fold. It took 32% of
   August paid traffic and converted 2.2% of it to the scheduling page, against home's 6.4%.

---

## 4. Coverage limits found while pulling

**GA4 will not serve `pagePath` broken down by `date` before 2026-05-17.** The same query at
`yearMonth` grain reaches back to 2026-05 only when a second dimension (channel) is added, and
back to 2023-02 with `pagePath` alone. Practical consequences:
- `ga4-schedule-page-reach.csv` has three sections, flagged in its `grain` column:
  `month_all_channels` (2023|05 – 2026|09, full history, no channel split),
  `month_by_channel` and `week_by_channel` (2026-05-17 onward only; 2026|05 and the week of
  2026-05-11 are therefore partial and should not be read as monthly figures).
- `eventCount` is empty in `ga4-events-by-page-monthly.csv` before 2026|05 for the same reason.
  The `sessions` column is populated for the whole history, which is why the long-run series in
  §3 is stated in sessions.
- **This is not recoverable after the subscription lapses.** Anything needing daily page-level
  history before 2026-05-17 is gone.

**`engagementRate` and `bounceRate` are flagged NON-AGGREGATABLE, but they are exactly derivable.**
Verified on all 260 channel rows: `engagementRate == engagedSessions / sessions` and
`bounceRate == 1 - engagementRate`, to 4 decimal places. `build_ga4_pages_channels.py` relies on
this to recompute both rates when splitting the combined device/new-vs-returning pull. `totalUsers`
is genuinely non-aggregatable and is never summed; where a derived file needed it, the column is
named `totalUsers_sum_NOT_DEDUPED` so nobody quotes it as a user count.

**`ga4-geo-monthly.csv` sums higher than `ga4-channels-monthly.csv` in every month** (e.g. 2023|05
+45 sessions). City × region × country splits sessions across more rows than GA4 dedups at the
coarse grain. Use geo for relative shape, not for totals.

---

## 5. `google / cpc` is split across TWO channel groupings

Not previously recorded anywhere in the archive, and it will silently corrupt any paid rollup that
filters on channel instead of source/medium:

| Month | `google / cpc` under Paid Search | `google / cpc` under Cross-network |
|---|---|---|
| 2025\|07 | 2,659 sessions | 311 sessions |
| 2025\|08 | 235 sessions | 5 sessions |

That is the PMax campaign (`Leads-PMax-Video-1`) spilling into the same source/medium string.
**Filtering on `sessionDefaultChannelGrouping == "Paid Search"` undercounts paid July 2025 by
10.5%.** Filter on `sessionSourceMedium == "google / cpc"` instead — which is what
`ga4-landing-pages-paid-monthly.csv` does, and why its 2025|07 total (2,968) exceeds the Paid
Search channel row (2,659).

---

## 6. Smaller things worth keeping

- **July 2025 was bot traffic, not demand.** Paid Search that month: 2,659 sessions at a 12.9%
  engagement rate and an 87.1% bounce rate, landing 1,065 sessions on `/whypnh` and 625 on
  `/schedule-an-appointment` directly. Compare July 2026 paid: 350 sessions at 63.7% engagement.
  The 2025 figure should never be used as a volume benchmark.
- **`/whypnh` has disappeared as a paid landing page** — 1,065 paid sessions in Jul 2025, 1 in
  Aug 2026.
- **Key-event counting changed around June 2026.** Site-wide `conversions` jump from 65 (2026|05)
  to 212 (2026|06) with no matching traffic jump. Any conversion comparison that crosses
  2026-05/06 is invalid for the same reason the ads-side team documented for 2026-07-12.
- **`/schedule-an-appointment` gets query-string variants** — `?fbclid=…`, `?fresh=1`,
  `?gtm_debug=…` — which split it into separate `pagePath` rows. Every schedule-page figure in
  this note matches on substring `schedule-an-appointment`, not on exact path.
- Two `gtm_debug` page views in June 2026 each carry a `purchase` event. Someone was testing with
  GTM Preview against live data; those two purchases are not real bookings.
