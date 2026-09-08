#!/usr/bin/env python3
"""Build the GA4 traffic / channel / landing-page / page archive CSVs for PNH2 (353828960).

Inputs are Supermetrics JSON tool results saved in this directory, plus two CSVs that
were returned inline by the API and transcribed verbatim (ga4-channels-monthly.csv,
ga4-landing-pages-paid-monthly.csv -- both machine-validated against
ga4-source-medium-monthly.csv before use).

GA4 identity relied on below and verified against every row of the channel file:
    engagementRate == engagedSessions / sessions ; bounceRate == 1 - engagementRate
so those two "non-aggregatable" rates CAN be safely recomputed at any grain.
totalUsers is a de-duplicated count and is NEVER summed; where a split file needs it,
the column is named *_sum_NOT_DEDUPED.
"""
import json, csv, collections, datetime, re

BASE = "/home/user/projects/data/supermetrics-archive-2026-09-08/"

def load(fn):
    j = json.load(open(BASE + fn))
    d = j["data"]
    return d["requested_field_ids"], d["data"][1:]

def rd(fn):
    return list(csv.DictReader(open(BASE + fn)))

def write(fn, header, rows):
    with open(BASE + fn, "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)
    print(f"  wrote {fn}: {len(rows)} rows x {len(header)} cols")

def n(v):
    try: return float(v or 0)
    except (TypeError, ValueError): return 0.0

def i(v): return int(round(n(v)))

def rate(num, den, nd=4):
    return round(num / den, nd) if den else ""

def wk(datestr):
    d = datetime.date.fromisoformat(datestr)
    return (d - datetime.timedelta(days=d.weekday())).isoformat()   # Monday of that week

# ---------------------------------------------------------------- 5. device / new-vs-returning
# Split the one combined pull (deviceCategory x newVsReturning x channel x month) into the
# two single-dimension files the archive needs.
print("[5] device / new-vs-returning monthly")
COMB = rd("ga4-device-newreturning-channel-monthly.csv")
for dim, out in (("deviceCategory", "ga4-device-monthly.csv"),
                 ("newVsReturning", "ga4-newreturning-monthly.csv")):
    agg = collections.defaultdict(lambda: collections.defaultdict(float))
    for r in COMB:
        k = (r["yearMonth"], r[dim])
        for m in ("sessions", "newUsers", "engagedSessions", "conversions",
                  "screenPageViews", "totalUsers"):
            agg[k][m] += n(r[m])
    rows = []
    for (ym, v), a in sorted(agg.items()):
        s, e = a["sessions"], a["engagedSessions"]
        rows.append([ym, v, i(s), i(a["newUsers"]), i(e), rate(e, s),
                     rate(s - e, s), i(a["conversions"]), i(a["screenPageViews"]),
                     i(a["totalUsers"])])
    write(out, ["yearMonth", dim, "sessions", "newUsers", "engagedSessions",
                "engagementRate", "bounceRate", "conversions", "screenPageViews",
                "totalUsers_sum_NOT_DEDUPED"], rows)

# ---------------------------------------------------------------- 6. schedule-page reach
print("[6] ga4-schedule-page-reach.csv")

# (a) denominator: all sessions per channel per day, full history, from the existing archive
SRC = rd("ga4-events-by-source-daily.csv")
day_sessions = collections.defaultdict(float)          # (date, channel) -> sessions
for r in SRC:
    if r["eventName"] == "session_start":
        day_sessions[(r["date"], r["sessionDefaultChannelGrouping"])] += n(r["sessions"])

# (b) schedule-page daily, by channel (GA4 only serves pagePath x date back to 2026-05-17)
_, SP = load("raw-ga4-schedule-page-daily.json")
SPF = ["date", "pagePath", "sessionDefaultChannelGrouping", "eventName",
       "eventCount", "sessions", "totalUsers", "conversions"]
S = {k: j for j, k in enumerate(SPF)}

def reach_rows(keyfn, grain):
    """Aggregate schedule-page daily rows to `grain` x channel, with the all-channel denominator."""
    ev = collections.defaultdict(lambda: collections.defaultdict(float))
    for r in SP:
        k = (keyfn(r[S["date"]]), r[S["sessionDefaultChannelGrouping"]])
        e = r[S["eventName"]]
        ev[k][e + "_ev"] += n(r[S["eventCount"]])
        ev[k][e + "_ss"] += n(r[S["sessions"]])
    den = collections.defaultdict(float)
    for (d, ch), s in day_sessions.items():
        den[(keyfn(d), ch)] += s
    out = []
    for k in sorted(set(ev) | {x for x in den if x[0] in {y[0] for y in ev}}):
        a, tot = ev.get(k, {}), den.get(k, 0.0)
        pv_ss, pv_ev = a.get("page_view_ss", 0), a.get("page_view_ev", 0)
        sa_ss, sa_ev = a.get("schedule_appointment_ss", 0), a.get("schedule_appointment_ev", 0)
        out.append([grain, k[0], k[1], i(tot), i(pv_ss), i(pv_ev), i(sa_ss), i(sa_ev),
                    i(a.get("purchase_ev", 0)), i(a.get("session_start_ss", 0)),
                    rate(pv_ss, tot), rate(pv_ev, pv_ss) if pv_ss else "",
                    rate(sa_ev, pv_ev) if pv_ev else ""])
    return out

HDR = ["grain", "period", "sessionDefaultChannelGrouping", "channel_sessions_all_pages",
       "schedpage_pageview_sessions", "schedpage_pageview_events",
       "schedule_appointment_sessions", "schedule_appointment_events",
       "schedpage_purchase_events", "schedpage_session_start_sessions",
       "reach_rate_sessions_pv_over_channel", "pageviews_per_reaching_session",
       "sched_appt_events_per_pageview"]

rows = reach_rows(lambda d: d[:7].replace("-", "|"), "month_by_channel")
rows += reach_rows(wk, "week_by_channel")

# (c) full-history monthly, ALL channels, from the existing by-page archive file.
#     GA4 will not serve pagePath split by channel before 2026-05, so this section is the
#     only long-run series available. eventCount is empty before 2026-05 (GA4 retention);
#     the "sessions" column is populated for the whole history.
PAGE = rd("ga4-events-by-page-monthly.csv")
CH = rd("ga4-channels-monthly.csv")
tot_m = collections.defaultdict(float)
for r in CH:
    tot_m[r["yearMonth"]] += n(r["sessions"])
agg = collections.defaultdict(lambda: collections.defaultdict(float))
for r in PAGE:
    if "schedule-an-appointment" in r["pagePath"]:
        a = agg[r["yearMonth"]]
        a[r["eventName"] + "_ev"] += n(r["eventCount"])
        a[r["eventName"] + "_ss"] += n(r["sessions"])
hist = []
for ym in sorted(agg):
    a, tot = agg[ym], tot_m.get(ym, 0.0)
    pv_ss, pv_ev = a.get("page_view_ss", 0), a.get("page_view_ev", 0)
    hist.append(["month_all_channels", ym, "(all)", i(tot), i(pv_ss), i(pv_ev),
                 i(a.get("schedule_appointment_ss", 0)), i(a.get("schedule_appointment_ev", 0)),
                 i(a.get("purchase_ev", 0)), i(a.get("session_start_ss", 0)),
                 rate(pv_ss, tot), rate(pv_ev, pv_ss) if pv_ev else "",
                 rate(a.get("schedule_appointment_ev", 0), pv_ev) if pv_ev else ""])
write("ga4-schedule-page-reach.csv", HDR, hist + rows)
print("\nDONE")
