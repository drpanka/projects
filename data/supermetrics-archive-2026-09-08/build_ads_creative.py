#!/usr/bin/env python3
"""Build creative + structural CSVs for the PNH Supermetrics archive (2026-09-08).

Inputs (raw Supermetrics tool output, saved verbatim):
  raw-ads-ad-daily.json           Date x AdID performance (report type: Ad)
  raw-ads-weekly-rsa-text.json    Yearweekiso x AdID + full RSA creative text
  raw-ads-asset-performance-enriched.json
                                  AdGroupAdAssetView: ad attributes + full RSA text
                                  + per-asset text/label/metrics. This is the only
                                  pull that returns ALL 16 ads: a time-segmented
                                  query drops ads that never served, so ad
                                  817157617842 (Pediatrics, Removed, 0 impressions)
                                  appears here and nowhere else.
  campaign-settings-<id>.json     campaign_and_resource_get full detail, 4 campaigns

Outputs: see FILES written at the bottom.
No data row is ever hand-typed; every CSV cell comes from one of the JSONs above.
"""
import csv, json, os
from collections import defaultdict, OrderedDict

A = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(A, n)

def load_query(name):
    """Return (list_of_field_ids, list_of_row_lists) for a data_query dump."""
    d = json.load(open(P(name)))["data"]
    fields = d["requested_field_ids"]
    rows = d["data"][1:]          # row 0 is display names; map by requested_field_ids
    return fields, [dict(zip(fields, r)) for r in rows]

def w(name, header, rows):
    with open(P(name), "w", newline="", encoding="utf-8") as f:
        cw = csv.writer(f)
        cw.writerow(header)
        cw.writerows(rows)
    print(f"wrote {name}: {len(rows)} rows")

num = lambda v: 0 if v in (None, "", "null") else float(v)
def rate(n, d, nd=4):
    return "" if not d else round(n / d, nd)

# ---------------------------------------------------------------- 1. ad perf
_, daily = load_query("raw-ads-ad-daily.json")
_, weekly = load_query("raw-ads-weekly-rsa-text.json")
_, assets = load_query("raw-ads-asset-performance-enriched.json")

# Identity attributes come from the asset-view pull, which is the only one that
# lists every ad ever created including those that never served.
ident = OrderedDict()
for r in assets:
    ident.setdefault(r["AdID"], {
        "Campaignname": r["Campaignname"], "CampaignID": r["CampaignID"],
        "Campaignstatus": r["Campaignstatus"],
        "Adgroupname": r["Adgroupname"], "AdgroupID": r["AdgroupID"],
        "Adgroupstatus": r["Adgroupstatus"],
        "Adtype": r["Adtype"], "Adstatus": r["Adstatus"],
        "Adapprovalstatus": r["Adapprovalstatus"], "ad_strength": r["ad_strength"],
        "finalURL": r["finalURL"],
    })
# DisplayURL / TrackingUrlTemplate only exist on the Ad-report pull
for r in weekly:
    if r["AdID"] in ident:
        ident[r["AdID"]].setdefault("DisplayURL", r.get("DisplayURL", ""))
        ident[r["AdID"]].setdefault("TrackingUrlTemplate", r.get("TrackingUrlTemplate", ""))

MET = ["Impressions", "Clicks", "Cost", "Conversions", "ConversionValue",
       "EstimatedTotalConversions"]
IDCOLS = ["Campaignname", "CampaignID", "Campaignstatus", "Adgroupname", "AdgroupID",
          "Adgroupstatus", "AdID", "Adtype", "Adstatus", "Adapprovalstatus",
          "ad_strength", "finalURL"]

def agg(keyfn):
    out = defaultdict(lambda: defaultdict(float))
    dates = defaultdict(list)
    for r in daily:
        k = keyfn(r)
        for m in MET:
            out[k][m] += num(r.get(m))
        dates[k].append(r["Date"])
    return out, dates

def emit(bucket_cols, keyfn, fname, sortfn):
    tot, dates = agg(keyfn)
    rows = []
    seen_ads = set()
    for k, m in tot.items():
        ad = k[-1] if isinstance(k, tuple) else k
        seen_ads.add(ad)
        i = ident.get(ad, {})
        pre = list(k[:-1]) if isinstance(k, tuple) else []
        rows.append(pre + [i.get(c, "") if c != "AdID" else ad for c in IDCOLS] + [
            int(m["Impressions"]), int(m["Clicks"]), round(m["Cost"], 4),
            rate(m["Clicks"], m["Impressions"]),
            round(m["Conversions"], 2),
            rate(m["Cost"], m["Conversions"], 4) if m["Conversions"] else "",
            rate(m["Conversions"], m["Clicks"]),
            round(m["ConversionValue"], 2),
            round(m["EstimatedTotalConversions"], 2),
            min(dates[k]), max(dates[k]), len(set(dates[k])),
        ])
    # ads that never served at all: present in the inventory, absent from daily
    if not bucket_cols:
        for ad, i in ident.items():
            if ad not in seen_ads:
                rows.append([i.get(c, "") if c != "AdID" else ad for c in IDCOLS]
                            + [0, 0, 0.0, "", 0, "", "", 0, 0, "", "", 0])
    rows.sort(key=sortfn)
    w(fname, bucket_cols + IDCOLS + [
        "Impressions", "Clicks", "Cost", "Ctr", "Conversions", "CostPerConversion",
        "ConversionRate", "ConversionValue", "AllConversions",
        "FirstServedDate", "LastServedDate", "DaysServed"], rows)
    return rows

alltime = emit([], lambda r: r["AdID"], "ads-ad-performance-alltime.csv",
               lambda r: -r[12])
emit(["Yearmonth"], lambda r: (r["Date"][:7], r["AdID"]),
     "ads-ad-performance-monthly.csv", lambda r: (r[0], -r[13]))

# ---------------------------------------------------------------- 2. RSA text
HL = [f"ResponsiveSearchAdHeadline{i}" for i in range(1, 16)]
DS = [f"ResponsiveSearchAdDescription{i}" for i in range(1, 6)]
PA = ["ResponsiveSearchAdPath1", "ResponsiveSearchAdPath2"]
TXT = PA + HL + DS

rsa, life = OrderedDict(), defaultdict(lambda: defaultdict(float))
for r in list(assets) + list(weekly):
    rsa.setdefault((r["AdID"], tuple(r.get(c, "") for c in TXT)), r)
for r in daily:
    for m in ("Impressions", "Clicks", "Cost", "Conversions"):
        life[r["AdID"]][m] += num(r.get(m))

rows = []
for (ad, txt), r in rsa.items():
    m = life[ad]
    n_hl = sum(1 for v in txt[2:17] if v)
    n_ds = sum(1 for v in txt[17:] if v)
    rows.append([r["Campaignname"], r["CampaignID"], r["Adgroupname"], r["AdgroupID"], ad,
                 r["Adtype"], r["Adstatus"], r["Adapprovalstatus"], r["ad_strength"],
                 r["finalURL"], n_hl, n_ds] + list(txt) + [
                 int(m["Impressions"]), int(m["Clicks"]), round(m["Cost"], 4),
                 round(m["Conversions"], 2)])
rows.sort(key=lambda x: (x[0], x[2], -x[-4]))
w("ads-rsa-text.csv",
  ["Campaignname", "CampaignID", "Adgroupname", "AdgroupID", "AdID", "Adtype",
   "Adstatus", "Adapprovalstatus", "ad_strength", "finalURL",
   "HeadlineCount", "DescriptionCount"] + TXT +
  ["LifetimeImpressions", "LifetimeClicks", "LifetimeCost", "LifetimeConversions"], rows)

# ---------------------------------------------------------------- 3. assets
# Flag assets whose text no longer appears in any live RSA. The asset view keeps
# retired assets and their lifetime metrics; they exist in no other export.
current_text = set()
for (ad, txt), r in rsa.items():
    current_text.update(v.strip() for v in txt if v)

rows = []
for r in assets:
    imp, clk = num(r["Impressions"]), num(r["Clicks"])
    cost, cv = num(r["Cost"]), num(r["Conversions"])
    rows.append([r["Campaignname"], r["CampaignID"], r["Adgroupname"], r["AdgroupID"],
                 r["AdID"], r["Adstatus"], r["ad_strength"],
                 r["assetFieldType"], r["assetType"],
                 r["assetPerformanceLabel"], r["assetTextText"],
                 "yes" if r["assetTextText"].strip() in current_text else "no",
                 int(imp), int(clk), round(cost, 4), rate(clk, imp),
                 round(cv, 2), rate(cost, cv) if cv else ""])
rows.sort(key=lambda x: (x[0], x[2], x[7], -x[12]))
w("ads-asset-performance.csv",
  ["Campaignname", "CampaignID", "Adgroupname", "AdgroupID", "AdID", "Adstatus",
   "ad_strength", "assetFieldType", "assetType", "assetPerformanceLabel",
   "assetTextText", "InCurrentCreative", "Impressions", "Clicks", "Cost", "Ctr",
   "Conversions", "CostPerConversion"], rows)

# ---------------------------------------------------------- 4. campaign structure
CAMPS = ["22767146837", "23888858069", "24032465476", "22625352639"]
negs, kws, exts, targ = [], [], [], []

for cid in CAMPS:
    c = json.load(open(P(f"campaign-settings-{cid}.json")))["data"]["data"]["results"][0]
    name, pd_ = c["name"], c["platform_details"]

    camp_neg = [(n["text"], n["match_type"]) for n in c["targeting"].get("negative_keywords", [])]
    for t, mt in camp_neg:
        negs.append([name, cid, "campaign", "", t, mt])
    for g in c["ad_groups"]:
        # The API echoes the campaign-level negative list onto every ad group.
        # Only emit an ad-group row when the list genuinely differs.
        ag_neg = [(n["text"], n["match_type"]) for n in g.get("targeting", {}).get("negative_keywords", [])]
        if ag_neg and ag_neg != camp_neg:
            for t, mt in ag_neg:
                negs.append([name, cid, "ad_group", g["name"], t, mt])
        for k in g.get("targeting", {}).get("keywords", []):
            kws.append([name, cid, g["name"], g["ad_group_id"], g["status"],
                        g.get("cpc_bid", ""), k["text"], k["match_type"]])

    e = c.get("extensions", {})
    for s in e.get("sitelinks", []):
        exts.append([name, cid, "sitelink", s.get("text", ""), s.get("url", ""),
                     s.get("description1", ""), s.get("description2", "")])
    for co in e.get("callouts", []):
        exts.append([name, cid, "callout", co, "", "", ""])
    for ss in e.get("structured_snippets", []):
        for v in ss.get("values", []):
            exts.append([name, cid, "structured_snippet", v, "", ss.get("header", ""), ""])
    for im in e.get("images", []):
        exts.append([name, cid, "image", im.get("id", ""), im.get("url", ""), "", ""])
    for ca in e.get("calls", []):
        exts.append([name, cid, "call", ca.get("phone_number", ""), "",
                     ca.get("country_code", ""), ""])

    T = lambda t, k, v, extra="": targ.append([name, cid, t, k, v, extra])
    T("campaign_setting", "status", c["status"])
    T("campaign_setting", "campaign_type", pd_.get("campaign_type", ""))
    T("campaign_setting", "start_date", c.get("start_date", ""))
    T("campaign_setting", "end_date", c.get("end_date") or "")
    T("campaign_setting", "daily_budget", c.get("budget_amount", ""),
      pd_.get("budget_name", ""))
    T("campaign_setting", "bidding_strategy", c.get("bidding_strategy", ""))
    T("campaign_setting", "geo_target_type", pd_.get("geo_target_type", ""))
    for k, v in (pd_.get("network_settings") or {}).items():
        T("network", k, v)
    T("campaign_setting", "languages", ",".join(c["targeting"].get("languages", [])))
    for s in pd_.get("ad_schedule", []):
        T("ad_schedule", s["day"], f"{s['start_hour']:02d}:00-{s['end_hour']:02d}:00",
          "" if s.get("bid_modifier") is None else s["bid_modifier"])
    for d in (pd_.get("bid_adjustments") or {}).get("devices", []):
        T("bid_adjustment_device", d.get("type", ""), d.get("bid_modifier", ""))
    for l in c["targeting"].get("location_details", []):
        if l["type"] == "custom_location":
            T("location", "custom_radius",
              f"{l['latitude']},{l['longitude']}", f"{l['radius']} {l['distance_unit']}")
        else:
            T("location", "geo_target_constant", l["key"], l.get("name", ""))
    for g in c["ad_groups"]:
        T("ad_group", g["name"], g["status"],
          f"id={g['ad_group_id']} type={g.get('type','')} cpc_bid={g.get('cpc_bid','')}")

w("campaign-negatives.csv",
  ["Campaignname", "CampaignID", "Level", "Adgroupname", "NegativeKeyword", "MatchType"], negs)
w("campaign-keywords.csv",
  ["Campaignname", "CampaignID", "Adgroupname", "AdgroupID", "Adgroupstatus",
   "AdgroupMaxCPC", "Keyword", "MatchType"], kws)
w("campaign-extensions.csv",
  ["Campaignname", "CampaignID", "ExtensionType", "Text", "URL", "Description1/Header",
   "Description2"], exts)
w("campaign-adschedule-and-targeting.csv",
  ["Campaignname", "CampaignID", "SettingType", "Key", "Value", "Detail"], targ)

# ------------------------------------------------- 5. asset-group creative (PMax)
# Performance Max campaigns have no rows in the Ad report at all, so their
# creative exists only inside the campaign settings JSON. Preserve it verbatim.
rows = []
for cid in CAMPS:
    c = json.load(open(P(f"campaign-settings-{cid}.json")))["data"]["data"]["results"][0]
    for g in c["ad_groups"]:
        for a in g["ads"]:
            if a.get("type") != "ASSET_GROUP":
                continue
            cr = a.get("creative", {})
            hl = [h["text"] for h in cr.get("headlines", [])]
            ds = [d["text"] for d in cr.get("descriptions", [])]
            for i, t in enumerate(hl, 1):
                rows.append([c["name"], cid, g["name"], g["ad_group_id"], a["id"],
                             "Headline", i, t, "", ""])
            for i, t in enumerate(ds, 1):
                rows.append([c["name"], cid, g["name"], g["ad_group_id"], a["id"],
                             "Description", i, t, "", ""])
            if cr.get("long_headline"):
                rows.append([c["name"], cid, g["name"], g["ad_group_id"], a["id"],
                             "LongHeadline", 1, cr["long_headline"], "", ""])
            for k, u in (cr.get("image_urls") or {}).items():
                rows.append([c["name"], cid, g["name"], g["ad_group_id"], a["id"],
                             "Image", 1, k, u, ""])
            if c["platform_details"].get("logo_url"):
                rows.append([c["name"], cid, g["name"], g["ad_group_id"], a["id"],
                             "Logo", 1, c["platform_details"].get("business_name", ""),
                             c["platform_details"]["logo_url"], ""])
w("ads-asset-group-creative.csv",
  ["Campaignname", "CampaignID", "AssetGroupName", "AssetGroupID", "AdID",
   "AssetRole", "Position", "Text", "URL", "Notes"], rows)


# ------------------------------------------------- 6. change history -> CSV
h = json.load(open(P("ads-change-history.json")))["data"]["data"]["results"]
rows = []
for c in h.get("platform_change_list", []):
    rows.append(["google_ads", c.get("timestamp", ""), c.get("user_email", ""),
                 c.get("campaign_name", ""), c.get("campaign_id", ""),
                 c.get("resource_type", ""), c.get("operation", ""),
                 ";".join(c.get("changed_fields", []) or []),
                 c.get("description", "")])
for c in h.get("supermetrics_change_list", []):
    rows.append(["supermetrics", c.get("timestamp", ""), c.get("user_email", ""),
                 c.get("campaign_name", ""), c.get("campaign_id", ""),
                 c.get("app", ""), c.get("action", ""),
                 ";".join(sorted((c.get("changes") or {}).keys())),
                 c.get("description", "")])
rows.sort(key=lambda r: r[1], reverse=True)
w("ads-change-history.csv",
  ["Source", "Timestamp", "UserEmail", "Campaignname", "CampaignID",
   "ResourceType", "Operation", "ChangedFields", "Description"], rows)

# ------------------------------------ 7. ad-schedule bid modifiers (history only)
# campaign_and_resource_get returns ad_schedule WITHOUT bid_modifier, so the only
# surviving record of the modifiers is the Supermetrics change log.
rows = []
for c in h.get("supermetrics_change_list", []):
    nv = ((c.get("changes") or {}).get("platform_settings") or {}).get("new_value") or {}
    for s in (nv.get("ad_schedule") or []):
        rows.append([c.get("timestamp", ""), c.get("campaign_name", ""),
                     c.get("campaign_id", ""), s.get("day", ""),
                     s.get("start_hour", ""), s.get("end_hour", ""),
                     s.get("bid_modifier", "")])
rows.sort(key=lambda r: (r[0], r[3], r[4]), reverse=True)
w("campaign-adschedule-bid-modifiers-history.csv",
  ["ChangeTimestamp", "Campaignname", "CampaignID", "Day", "StartHour", "EndHour",
   "BidModifier"], rows)

# ---------------------------------- 8. PMax asset-group conversions by action
# Performance Max returns nothing in the Ad report (gap G1). Asset-group level is
# the finest grain available, and conversion-action segmentation cannot be combined
# with impressions/clicks/cost (Google rejects the field mix), so this file carries
# conversions only. Campaign #1 has exactly one asset group, so its impressions /
# clicks / cost at asset-group level are identical to campaign level.
_, pm = load_query("raw-ads-pmax-assetgroup-conversions.json")
rows = [[r["Date"], r["Yearmonth"], r["DayofweekWithNum"], r["Campaignname"],
         r["CampaignID"], r["Campaignstatus"], r["CampaignPrimaryStatusReasons"],
         r["assetGroupId"], r["assetGroupName"], r["assetGroupStatus"],
         r["ad_strength"], r["ConversionTypeName"], r["ConversionCategory"],
         r["ConversionTrackerId"], num(r["Conversions"]), num(r["ConversionValue"]),
         num(r["EstimatedTotalConversions"]), num(r["EstimatedTotalConversionValue"]),
         num(r["EstimatedCrossDeviceConversions"])] for r in pm]
rows.sort(key=lambda x: (x[0], x[11]))
w("ads-pmax-assetgroup-conversions-daily.csv",
  ["Date", "Yearmonth", "DayOfWeek", "Campaignname", "CampaignID", "Campaignstatus",
   "CampaignPrimaryStatusReasons", "assetGroupId", "assetGroupName", "assetGroupStatus",
   "ad_strength", "ConversionTypeName", "ConversionCategory", "ConversionTrackerId",
   "Conversions", "ConversionValue", "AllConversions", "AllConversionValue",
   "CrossDeviceConversions"], rows)

agg = defaultdict(lambda: defaultdict(float))
for r in pm:
    k = (r["Yearmonth"], r["Campaignname"], r["assetGroupName"],
         r["ConversionTypeName"], r["ConversionCategory"], r["ConversionTrackerId"])
    agg[k]["c"] += num(r["Conversions"])
    agg[k]["a"] += num(r["EstimatedTotalConversions"])
rows = [list(k) + [round(v["c"], 2), round(v["a"], 2)] for k, v in agg.items()]
rows.sort(key=lambda x: (x[0], -x[6]))
w("ads-pmax-assetgroup-conversions-monthly.csv",
  ["Yearmonth", "Campaignname", "assetGroupName", "ConversionTypeName",
   "ConversionCategory", "ConversionTrackerId", "Conversions", "AllConversions"], rows)
