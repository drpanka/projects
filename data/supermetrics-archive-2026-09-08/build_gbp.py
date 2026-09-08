import json, csv, re, datetime
from collections import defaultdict

D = "/home/user/projects/data/supermetrics-archive-2026-09-08/"
THRESHOLD = 15          # Google publishes an exact value only at >=15/mo; below that it returns a threshold
MIDPOINT  = 8           # midpoint estimate used for sub-threshold months

kw = json.load(open(D+"raw-gmb-search-keywords.json"))
rows = [r for r in kw["data"][1:] if r[3]]          # drop header + the empty 2026|08 stub

# ---------- 1. monthly detail ----------
with open(D+"gmb-search-keywords-monthly.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["year_month","location_name","location_id","keyword",
                "reported_impressions","is_sub_threshold","estimated_impressions_midpoint"])
    for ym,ln,lid,k,v in sorted(rows, key=lambda r:(r[0], -(r[4] or 0), r[3])):
        v = v or 0
        sub = 1 if v == 0 else 0
        w.writerow([ym.replace("|","-"),ln,lid,k,v,sub, MIDPOINT if sub else v])

# ---------- 2. keyword-level aggregate ----------
agg = defaultdict(lambda: {"rep":0,"sub":0,"mons":[],"mx":0})
for ym,ln,lid,k,v in rows:
    v = v or 0
    a = agg[k]
    a["mons"].append(ym.replace("|","-"))
    if v == 0: a["sub"] += 1
    else:
        a["rep"] += v
        a["mx"] = max(a["mx"], v)

def est(a): return a["rep"] + a["sub"]*MIDPOINT

ordered = sorted(agg.items(), key=lambda kv:(-est(kv[1]), -kv[1]["rep"], -len(kv[1]["mons"]), kv[0]))
with open(D+"gmb-search-keywords.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["keyword","estimated_impressions_midpoint","reported_impressions_total",
                "max_reported_month","months_appeared","sub_threshold_months",
                "est_low","est_high","first_month","last_month","months_list"])
    for k,a in ordered:
        ms = sorted(a["mons"])
        w.writerow([k, est(a), a["rep"], a["mx"], len(ms), a["sub"],
                    a["rep"]+a["sub"]*1, a["rep"]+a["sub"]*THRESHOLD,
                    ms[0], ms[-1], ";".join(ms)])

# ---------- 3. classification ----------
def bucket(k):
    s = k.lower().strip().strip('"')
    if "panka" in s or "pnh" in s or "dr haley" in s or "dr jacob" in s \
       or "901 1st street north" in s or "1st street north, hopkins" in s:
        return "brand"
    # specific practitioner / competitor clinic names
    if any(t in s for t in ["karissa kuhle","dr kat hopkins","jennifer alasko",
                            "kathryn l piha","champion naturopathic","psch anp","dr. pannoch"]):
        return "competitor/practitioner-name"
    if any(t in s for t in ["pediatric","pediatrician","kids","children","child","autism"]):
        return "Pediatrics"
    if any(t in s for t in ["fertility","infertility","pcos","hrt","menopause","thyroid","hormone","estrogen"]):
        return "Women's Health & Hormones"
    if "for men" in s or "mens health" in s or "men's health" in s:
        return "Men's Health"
    if any(t in s for t in ["diabetes","weight loss","metabolic","glp"]):
        return "Metabolic/Diabetes"
    if any(t in s for t in ["cholesterol","heart","cardio"]):
        return "Cholesterol/Heart"
    if any(t in s for t in ["gut health","gi health","bowel movement","digest","ibs"]):
        return "Gut Health"
    if any(t in s for t in ["anxiety","depression","adhd","insomnia","concussion","brain","neuro"]):
        return "Brain/Neuro"
    if any(t in s for t in ["food sensitivity","lymes disease testing","ebv","testing","test",
                            "panel","labs"]):
        return "Functional Lab Testing"
    if any(t in s for t in ["homeopath","ayurved","colonic","essential oils","supplements store",
                            "vitamin","nutritionist","cancer","leukemia","orthopedic","rash",
                            "allergic","nail fungus","healing centers","iridologist"]):
        return "modality/other-service"
    if any(t in s for t in ["naturopath","natural path","natural dr","natural doctor","naturopathic",
                            "holistic","functional medicine","integrative","alternative medicine",
                            "natural health","natural practitioner","natropath","nautropath",
                            "nutrapathic","natura ","naturistic","hollistic","natural removal",
                            "wellness","health and wellness","healthcare places","physician hopkins",
                            "natural pathologist","natural cancer","functional.medicine",
                            "naturalpath","natutherapist"]):
        return "geo/discovery"
    return "other/irrelevant"

with open(D+"gmb-search-keywords-classified.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["keyword","volume","bucket","reported_impressions_total","months_appeared",
                "sub_threshold_months","volume_basis"])
    for k,a in ordered:
        w.writerow([k, est(a), bucket(k), a["rep"], len(a["mons"]), a["sub"],
                    "midpoint_estimate (sub-threshold month = 8 impressions)"])

# ---------- bucket rollup ----------
brollup = defaultdict(lambda:{"kw":0,"rows":0,"est":0,"rep":0})
for k,a in agg.items():
    b = brollup[bucket(k)]
    b["kw"] += 1; b["rows"] += len(a["mons"]); b["est"] += est(a); b["rep"] += a["rep"]
tot_est = sum(v["est"] for v in brollup.values())
tot_rows = sum(v["rows"] for v in brollup.values())
with open(D+"gmb-search-keywords-bucket-summary.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["bucket","distinct_keywords","keyword_month_rows","pct_of_rows",
                "estimated_impressions","pct_of_estimated_impressions","reported_impressions_total"])
    for b,v in sorted(brollup.items(), key=lambda x:-x[1]["est"]):
        w.writerow([b,v["kw"],v["rows"],round(100*v["rows"]/tot_rows,1),
                    v["est"],round(100*v["est"]/tot_est,1),v["rep"]])
    w.writerow(["TOTAL",len(agg),tot_rows,100.0,tot_est,100.0,sum(v["rep"] for v in brollup.values())])

print("BUCKET SUMMARY  (est_impr / pct_est / rows / pct_rows / distinct_kw)")
for b,v in sorted(brollup.items(), key=lambda x:-x[1]["est"]):
    print(f"  {b:32s} {v['est']:5d}  {100*v['est']/tot_est:5.1f}%  {v['rows']:4d}  {100*v['rows']/tot_rows:5.1f}%  {v['kw']}")
print(f"  {'TOTAL':32s} {tot_est:5d}  100.0%  {tot_rows:4d}  100.0%  {len(agg)}")
print("\nTOP 15 KEYWORDS")
for k,a in ordered[:15]:
    print(f"  {est(a):5d} est | rep {a['rep']:3d} | {len(a['mons']):2d} mo | {bucket(k):28s} | {k}")
