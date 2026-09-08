import csv, json
from collections import defaultdict, Counter

R = lambda f: list(csv.DictReader(open(f)))

print("=== 1. NEGATIVES PER CAMPAIGN (campaign level) ===")
neg = R("campaign-negatives.csv")
for (c, lvl), n in sorted(Counter((r["Campaignname"], r["Level"]) for r in neg).items()):
    print(f"  {c:38s} {lvl:9s} {n}")
print("  match-type split, Leads-Search-1:",
      Counter(r["MatchType"] for r in neg if r["Campaignname"] == "Leads-Search-1"))
print("  match-type split, PNHdefense:",
      Counter(r["MatchType"] for r in neg if r["Campaignname"].startswith("PNHdefense")))
print("  match-type split, Campaign #1:",
      Counter(r["MatchType"] for r in neg if r["Campaignname"] == "Campaign #1"))

print("\n=== 2. KEYWORDS PER CAMPAIGN PER AD GROUP ===")
kw = R("campaign-keywords.csv")
by = defaultdict(list)
for r in kw:
    by[(r["Campaignname"], r["Adgroupname"], r["AdgroupMaxCPC"])].append(r["MatchType"])
tot = Counter()
for (c, g, bid), mts in sorted(by.items()):
    tot[c] += len(mts)
    print(f"  {c:38s} {g:36s} maxcpc={bid:5s} n={len(mts):3d}  {dict(Counter(mts))}")
print("  campaign totals:", dict(tot))

print("\n=== 3. NON-STANDARD AD APPROVAL / STRENGTH ===")
ads = R("ads-ad-performance-alltime.csv")
print("  approval status counts:", Counter(r["Adapprovalstatus"] for r in ads))
for r in ads:
    if r["Adapprovalstatus"] != "Approved":
        print(f"    ** {r['Adapprovalstatus']:20s} AdID {r['AdID']} | {r['Campaignname']} | "
              f"{r['Adgroupname']} | status={r['Adstatus']} strength={r['ad_strength']} "
              f"| cost ${r['Cost']} conv {r['Conversions']}")
print("  ad strength counts:", Counter(r["ad_strength"] for r in ads))
for r in ads:
    if r["ad_strength"] in ("Poor", "Pending"):
        print(f"    -- strength={r['ad_strength']:8s} AdID {r['AdID']} | {r['Adgroupname']:36s}"
              f" status={r['Adstatus']:8s} impr={r['Impressions']:>6s} cost=${r['Cost']}")

print("\n=== 4. LIFETIME CTR RANKING ===")
rank = sorted((r for r in ads if int(r["Impressions"]) > 0),
              key=lambda r: -float(r["Ctr"]))
print(f"  {'AdID':14s} {'CTR':>7s} {'impr':>6s} {'clk':>5s} {'cost':>9s} {'conv':>6s}  ad group")
for r in rank:
    print(f"  {r['AdID']:14s} {float(r['Ctr'])*100:6.2f}% {r['Impressions']:>6s} "
          f"{r['Clicks']:>5s} {'$'+r['Cost']:>9s} {r['Conversions']:>6s}  "
          f"{r['Campaignname']} / {r['Adgroupname']}")
mv = [r for r in rank if int(r["Impressions"]) >= 400]
print("  best CTR at >=400 impressions:", mv[0]["AdID"], f"{float(mv[0]['Ctr'])*100:.2f}%",
      mv[0]["Adgroupname"])

print("\n=== 5. MONTHLY CAMPAIGN TOTALS (from ad-level data) ===")
mon = R("ads-ad-performance-monthly.csv")
agg = defaultdict(lambda: [0, 0, 0.0, 0.0])
for r in mon:
    a = agg[(r["Yearmonth"], r["Campaignname"])]
    a[0] += int(r["Impressions"]); a[1] += int(r["Clicks"])
    a[2] += float(r["Cost"]);      a[3] += float(r["Conversions"])
for k, v in sorted(agg.items()):
    ctr = v[1]/v[0]*100 if v[0] else 0
    cpa = v[2]/v[3] if v[3] else 0
    print(f"  {k[0]}  {k[1]:38s} impr={v[0]:6d} clk={v[1]:4d} ${v[2]:8.2f} "
          f"ctr={ctr:5.2f}% conv={v[3]:7.2f} cpa=${cpa:7.2f}")

print("\n=== 6. ASSET PERFORMANCE LABELS ===")
asset = R("ads-asset-performance.csv")
print("  label counts:", Counter(r["assetPerformanceLabel"] or "(blank)" for r in asset))
print("  field type counts:", Counter(r["assetFieldType"] for r in asset))
print("  distinct asset texts:", len(set(r["assetTextText"] for r in asset)))
for lbl in ("Best", "Good", "Low"):
    sel = [r for r in asset if r["assetPerformanceLabel"] == lbl]
    if sel:
        print(f"\n  --- {lbl} ({len(sel)}) ---")
        for r in sorted(sel, key=lambda x: -int(x["Impressions"]))[:14]:
            print(f"    {r['assetFieldType']:11s} impr={r['Impressions']:>6s} "
                  f"clk={r['Clicks']:>4s} conv={r['Conversions']:>7s} "
                  f"[{r['Adgroupname'][:22]}] {r['assetTextText'][:62]}")

print("\n=== 7. RSA TEXT COVERAGE ===")
rsa = R("ads-rsa-text.csv")
print("  ads in creative library:", len(rsa))
for r in sorted(rsa, key=lambda x: (x["Campaignname"], x["Adgroupname"], x["AdID"])):
    print(f"  {r['AdID']:14s} hl={r['HeadlineCount']:>2s} desc={r['DescriptionCount']:>2s} "
          f"path=/{r['ResponsiveSearchAdPath1']}/{r['ResponsiveSearchAdPath2']:<16s} "
          f"{r['Adstatus']:8s} {r['ad_strength']:9s} {r['Campaignname'][:22]:22s} {r['Adgroupname']}")
