import json, csv, os
from collections import defaultdict

OUT = "/home/user/projects/data/supermetrics-archive-2026-09-08"
DAILY = "/root/.claude/projects/-home-user-projects/1ab3ed00-62c5-5428-bf41-415fdb420127/tool-results/mcp-Supermetrics_Marketing_Analytics-data_query-1788895255652.txt"
DEFS = os.path.join(OUT, "ads-conversion-action-definitions.json")
CAMP = os.path.join(OUT, "raw-ads-campaign-daily.json")

# ---------- 1. definitions CSV ----------
defs = json.load(open(DEFS))
res = {d["id"]: d for d in defs["resource_definitions"]}
rep = {d["id"]: d for d in defs["report_settings_2026_09_08"]}
all_ids = list(rep.keys()) + [i for i in res if i not in rep]

rows = []
for cid in all_ids:
    r = res.get(cid, {}); p = rep.get(cid, {})
    rows.append({
        "conversion_action_id": cid,
        "name": r.get("name") or p.get("name", ""),
        "type": r.get("type", "NOT_RETURNED_BY_RESOURCE_API"),
        "category_api": r.get("category", ""),
        "category_report": p.get("category", ""),
        "status": r.get("status") or p.get("status", "").upper(),
        "counting": r.get("counting") or p.get("counting", ""),
        "primary_for_goal": p.get("primary_for_goal", ""),
        "include_in_conversions_metric": p.get("include_in_conversions", ""),
        "attribution_model": p.get("attribution_model", ""),
        "all_conversions_lifetime_2025_06_to_2026_09_08": p.get("all_conversions_lifetime", ""),
        "all_conversion_value_lifetime": p.get("all_conversion_value_lifetime", ""),
        "google_tag_id": r.get("google_tag_id", ""),
        "send_to_label": r.get("send_to", ""),
    })
rows.sort(key=lambda x: -float(x["all_conversions_lifetime_2025_06_to_2026_09_08"] or 0))
with open(os.path.join(OUT, "ads-conversion-actions.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("ads-conversion-actions.csv rows:", len(rows))

# ---------- 2. daily by action ----------
d = json.load(open(DAILY))
fids = d["data"]["requested_field_ids"]
data = d["data"]["data"][1:]
IDX = {k: i for i, k in enumerate(fids)}

with open(os.path.join(OUT, "ads-conversions-by-action-daily.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(fids); w.writerows(data)
print("ads-conversions-by-action-daily.csv rows:", len(data))

def num(v):
    try: return float(v)
    except (TypeError, ValueError): return 0.0

METRICS = ["Conversions","conversionsByConversionDate","EstimatedTotalConversions",
           "allConversionsByConversionDate","ConversionValue","EstimatedTotalConversionValue",
           "allConversionsValueByConversionDate","Viewthroughconversions","EstimatedCrossDeviceConversions"]

# ---------- 3. monthly by action + campaign ----------
key_dims = ["Yearmonth","Campaignname","CampaignID","ConversionTrackerId","ConversionTypeName",
            "ConversionCategory","ExternalConversionSource"]
agg = defaultdict(lambda: defaultdict(float))
for r in data:
    ym = r[IDX["Date"]][:7].replace("-", "|")
    k = (ym, r[IDX["Campaignname"]], r[IDX["CampaignID"]], r[IDX["ConversionTrackerId"]],
         r[IDX["ConversionTypeName"]], r[IDX["ConversionCategory"]], r[IDX["ExternalConversionSource"]])
    for m in METRICS:
        agg[k][m] += num(r[IDX[m]])

hdr = key_dims + METRICS + ["primary_for_goal_now","include_in_conversions_now","counting","action_bucket"]

def bucket(cid, name):
    if cid in ("7152843979","7635668327"): return "scheduling_page_or_event"
    if cid in ("7154049482","7154049485"): return "doctor_bio_page_view"
    if cid == "7154049488": return "whypnh_page_view"
    if cid in ("7157480846","7160506736","7169930375","7180867432","7254459499"): return "google_hosted_local_action"
    if cid in ("7196843730","7163356268"): return "purchase"
    if cid in ("7217291006","7151526666","7151555473"): return "call_or_lead_form"
    if cid == "7747774028": return "intro_call_click"
    return "other"

mrows = []
for k, v in sorted(agg.items()):
    cid = k[3]
    p = rep.get(cid, {})
    mrows.append(list(k) + [round(v[m], 4) for m in METRICS] +
                 [p.get("primary_for_goal",""), p.get("include_in_conversions",""),
                  p.get("counting",""), bucket(cid, k[4])])
with open(os.path.join(OUT, "ads-conversions-by-action-monthly.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(hdr); w.writerows(mrows)
print("ads-conversions-by-action-monthly.csv rows:", len(mrows))

# ---------- 4. composition ----------
cagg = defaultdict(lambda: defaultdict(float))
for k, v in agg.items():
    ym, camp, cid = k[0], k[1], k[3]
    b = bucket(cid, k[4])
    cagg[(ym, camp)]["counted_" + b] += v["Conversions"]
    cagg[(ym, camp)]["all_" + b] += v["EstimatedTotalConversions"]

buckets = ["scheduling_page_or_event","doctor_bio_page_view","whypnh_page_view",
           "google_hosted_local_action","purchase","call_or_lead_form","intro_call_click","other"]
chdr = (["Yearmonth","Campaignname","counted_conversions_total"] +
        ["counted_" + b for b in buckets] +
        ["share_counted_scheduling","share_counted_bio_pages","share_counted_whypnh","share_counted_other_pct"] +
        ["all_conversions_total"] + ["all_" + b for b in buckets])
crows = []
for (ym, camp), v in sorted(cagg.items()):
    tot = sum(v.get("counted_" + b, 0.0) for b in buckets)
    atot = sum(v.get("all_" + b, 0.0) for b in buckets)
    def sh(x): return round(100.0 * x / tot, 2) if tot else ""
    sched = v.get("counted_scheduling_page_or_event", 0.0)
    bio = v.get("counted_doctor_bio_page_view", 0.0)
    why = v.get("counted_whypnh_page_view", 0.0)
    crows.append([ym, camp, round(tot, 4)] +
                 [round(v.get("counted_" + b, 0.0), 4) for b in buckets] +
                 [sh(sched), sh(bio), sh(why), sh(tot - sched - bio - why)] +
                 [round(atot, 4)] + [round(v.get("all_" + b, 0.0), 4) for b in buckets])
with open(os.path.join(OUT, "ads-conversions-composition.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(chdr); w.writerows(crows)
print("ads-conversions-composition.csv rows:", len(crows))

# ---------- 5. campaign monthly cost ----------
cd = json.load(open(CAMP))
cf = cd["data"]["requested_field_ids"]; cdata = cd["data"]["data"][1:]
CI = {k: i for i, k in enumerate(cf)}
cost = defaultdict(lambda: defaultdict(float))
for r in cdata:
    ym = r[CI["Date"]][:7].replace("-", "|")
    k = (ym, r[CI["Campaignname"]])
    for m in ["Impressions","Clicks","Cost","Conversions"]:
        cost[k][m] += num(r[CI[m]])
json.dump({f"{k[0]}||{k[1]}": dict(v) for k, v in cost.items()},
          open(os.path.join(OUT, "_tmp_cost.json"), "w"), indent=1)
print("cost months:", len(cost))
