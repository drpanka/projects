#!/usr/bin/env python3
"""Build the GA4 archive CSVs for PNH2 (property 353828960).

All rows come from Supermetrics JSON tool-result files; nothing is hand-typed.
Header rows are derived from requested_field_ids, NOT the row-0 display names.
"""
import json, csv, os, collections, re

BASE = "/home/user/projects/data/supermetrics-archive-2026-09-08/"

def load(fn):
    """Return (field_ids, rows) with the Supermetrics display-name header stripped."""
    j = json.load(open(BASE + fn))
    d = j["data"]
    fids = d["requested_field_ids"]
    raw = d["data"]
    if isinstance(raw, str):                       # compressed text form
        rows = []
        for line in raw.splitlines():
            m = re.match(r"\s*-\s*\[\d+,\]:\s?(.*)$", line)
            if not m:
                continue
            rows.append(next(csv.reader([m.group(1)])))
        rows = rows[1:]                            # drop display-name header
    else:
        rows = raw[1:]                             # drop display-name header
    return fids, rows

def write(fn, header, rows):
    with open(BASE + fn, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"  wrote {fn}: {len(rows)} rows x {len(header)} cols")

def num(v):
    if v in (None, "", "null", "(not set)"):
        return 0
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0

def i(v):
    return int(round(num(v)))

# ---------------------------------------------------------------- 2. events by source, monthly
print("[2] ga4-events-by-source-monthly.csv")
f23, r23 = load("raw-ga4-events-by-source-monthly-2023.json")
f24, r24 = load("raw-ga4-events-by-source-monthly.json")
assert f23 == f24, (f23, f24)
allrows = r23 + r24
allrows.sort(key=lambda r: (r[0], r[1], r[2]))
write("ga4-events-by-source-monthly.csv", f23, allrows)
EVENTS_FIDS, EVENTS_ROWS = f23, allrows

# ---------------------------------------------------------------- daily events by source (full history)
print("[daily source] ga4-events-by-source-daily.csv")
fd, rd = load("raw-ga4-events-daily-by-source.json")
rd.sort(key=lambda r: (r[0], r[1], r[2]))
write("ga4-events-by-source-daily.csv", fd, rd)
D = {k: n for n, k in enumerate(fd)}

# ---------------------------------------------------------------- monthly events by page (full history)
print("[monthly page] ga4-events-by-page-monthly.csv")
fp, rp = load("raw-ga4-events-monthly-by-page.json")
rp.sort(key=lambda r: (r[0], r[1], r[2]))
write("ga4-events-by-page-monthly.csv", fp, rp)
P = {k: n for n, k in enumerate(fp)}

# ---------------------------------------------------------------- 3. purchases
print("[3] purchases")
# 3a. richest detail: date x source x pagePath x transactionId (only where GA4 serves it)
ft, rt = load("raw-ga4-allevents-page-transaction.json")
T = {k: n for n, k in enumerate(ft)}
det = [r for r in rt if r[T["eventName"]] == "purchase"]
det.sort(key=lambda r: (r[T["date"]], r[T["sessionSourceMedium"]], r[T["pagePath"]]))
detail_dates = sorted({r[T["date"]] for r in det})

# 3b. full-history daily purchase rows (date x sessionSourceMedium) -- covers 2023-12 onward
dp = [r for r in rd if r[D["eventName"]] == "purchase"]
dp.sort(key=lambda r: (r[D["date"]], r[D["sessionSourceMedium"]]))

# Build one detail file: rich rows where available, coarse rows (pagePath/transactionId
# unavailable) for the older period GA4 will not serve at that grain.
CUT = detail_dates[0]
hdr = ["date", "sessionSourceMedium", "sessionDefaultChannelGrouping", "pagePath",
       "transactionId", "currencyCode", "eventCount", "purchaseRevenue", "totalRevenue",
       "transactions", "ecommercePurchases", "detail_grain"]
out = []
# channel grouping lookup from the daily file
cg = {}
for r in dp:
    cg[(r[D["date"]], r[D["sessionSourceMedium"]])] = r[D["sessionDefaultChannelGrouping"]]
for r in dp:
    if r[D["date"]] >= CUT:
        continue                                    # covered by rich rows below
    out.append([r[D["date"]], r[D["sessionSourceMedium"]], r[D["sessionDefaultChannelGrouping"]],
                "(unavailable-see-notes)", "(unavailable-see-notes)", "(not set)",
                i(r[D["eventCount"]]), num(r[D["purchaseRevenue"]]), num(r[D["totalRevenue"]]),
                i(r[D["transactions"]]), i(r[D["ecommercePurchases"]]),
                "date x sessionSourceMedium only"])
for r in det:
    k = (r[T["date"]], r[T["sessionSourceMedium"]])
    out.append([r[T["date"]], r[T["sessionSourceMedium"]], cg.get(k, "(not set)"),
                r[T["pagePath"]], r[T["transactionId"]], r[T["currencyCode"]],
                i(r[T["eventCount"]]), num(r[T["purchaseRevenue"]]), num(r[T["totalRevenue"]]),
                i(r[T["transactions"]]), i(r[T["ecommercePurchases"]]),
                "date x source x pagePath x transactionId"])
out.sort(key=lambda r: (r[0], r[1], r[3]))
write("ga4-purchases-detail.csv", hdr, out)

# 3c. monthly rollup by source (full history, from the daily file)
agg = collections.defaultdict(lambda: [0, 0.0, 0.0, 0, 0])
for r in dp:
    ym = r[D["date"]][:4] + "|" + r[D["date"]][5:7]
    k = (ym, r[D["sessionSourceMedium"]], r[D["sessionDefaultChannelGrouping"]])
    a = agg[k]
    a[0] += i(r[D["eventCount"]]); a[1] += num(r[D["purchaseRevenue"]])
    a[2] += num(r[D["totalRevenue"]]); a[3] += i(r[D["transactions"]])
    a[4] += i(r[D["ecommercePurchases"]])
rows = [[k[0], k[1], k[2], v[0], round(v[1], 2), round(v[2], 2), v[3], v[4]]
        for k, v in sorted(agg.items())]
write("ga4-purchases-monthly.csv",
      ["yearMonth", "sessionSourceMedium", "sessionDefaultChannelGrouping", "eventCount",
       "purchaseRevenue", "totalRevenue", "transactions", "ecommercePurchases"], rows)

# 3d. purchases by page path, monthly (full history) -> free intro call vs paid split
pp = [r for r in rp if r[P["eventName"]] == "purchase"]
INTRO = "41826455"
def bucket(path):
    if INTRO in path:
        return "free_intro_call_41826455"
    if "/commerce/orders/" in path:
        return "squarespace_commerce_order"
    if path in ("(not set)", "", None):
        return "page_unattributed"
    if "/schedule/0081d9d2" in path:
        return "acuity_scheduler_other_type"
    if "/schedule-an-appointment" in path:
        return "onsite_schedule_page"
    return "other"
rows = [[r[P["yearMonth"]], r[P["pagePath"]], bucket(r[P["pagePath"]]), i(r[P["eventCount"]]),
         num(r[P["purchaseRevenue"]]), num(r[P["totalRevenue"]]), i(r[P["transactions"]])]
        for r in pp]
rows.sort(key=lambda r: (r[0], r[1]))
write("ga4-purchases-by-page-monthly.csv",
      ["yearMonth", "pagePath", "appointment_bucket", "eventCount", "purchaseRevenue",
       "totalRevenue", "transactions"], rows)

# ---------------------------------------------------------------- 4. ad-group attribution
print("[4] ga4-events-by-adgroup-monthly.csv")
fa, ra = load("raw-ga4-events-by-adgroup-monthly.json")
ra.sort(key=lambda r: (r[0], r[1], r[2], r[3], r[4]))
write("ga4-events-by-adgroup-monthly.csv", fa, ra)
A = {k: n for n, k in enumerate(fa)}

# ---------------------------------------------------------------- 5. acuity outbound clicks
print("[5] ga4-acuity-outbound-clicks.csv")
fl, rl = load("raw-ga4-links-monthly.json")
L = {k: n for n, k in enumerate(fl)}
ac = [r for r in rl if "acuity" in (r[L["linkDomain"]] or "").lower()]
ac.sort(key=lambda r: (r[0], r[2], r[3]))
write("ga4-acuity-outbound-clicks.csv", fl, ac)
# full link table too -- it is the only durable record of outbound-click tracking
rl.sort(key=lambda r: (r[0], r[3], r[2]))
write("ga4-outbound-links-monthly.csv", fl, rl)

# ---------------------------------------------------------------- 6. pollution audit
print("[6] ga4-self-referral-pollution.csv")
POLL = ("tagassistant.google.com", "ads.google.com")
prows = []
# (a) by sessionSourceMedium, from the full-history daily file -> monthly
sm = collections.defaultdict(lambda: [0, 0, 0, 0.0])
for r in rd:
    s = (r[D["sessionSourceMedium"]] or "").lower()
    if any(p in s for p in POLL):
        ym = r[D["date"]][:4] + "|" + r[D["date"]][5:7]
        k = ("sessionSourceMedium", r[D["sessionSourceMedium"]], ym, r[D["eventName"]])
        a = sm[k]
        a[0] += i(r[D["eventCount"]]); a[1] += i(r[D["sessions"]])
        a[2] += i(r[D["conversions"]]); a[3] += num(r[D["totalRevenue"]])
for k, v in sorted(sm.items()):
    prows.append([k[0], k[1], k[2], k[3], v[0], v[1], v[2], round(v[3], 2)])
# (b) by pageReferrer, from the full-history monthly file
fr, rr = load("raw-ga4-pagereferrer-monthly.json")
Rf = {k: n for n, k in enumerate(fr)}
for r in rr:
    ref = (r[Rf["pageReferrer"]] or "").lower()
    if any(p in ref for p in POLL):
        prows.append(["pageReferrer", r[Rf["pageReferrer"]], r[Rf["yearMonth"]],
                      r[Rf["eventName"]], i(r[Rf["eventCount"]]), i(r[Rf["sessions"]]),
                      i(r[Rf["conversions"]]), 0])
prows.sort(key=lambda r: (r[0], r[2], r[1], r[3]))
write("ga4-self-referral-pollution.csv",
      ["detection_field", "polluted_value", "yearMonth", "eventName", "eventCount",
       "sessions", "conversions", "totalRevenue"], prows)
print("\nDONE")
