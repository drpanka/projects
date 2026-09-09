#!/usr/bin/env python3
"""Build pollution-quantified.csv for PNH GA4 property 353828960.

Sources (all local, no API calls):
  raw-ga4-pagereferrer-monthly.json   yearMonth x eventName x pageReferrer
  ga4-events-by-source-monthly.csv    yearMonth x eventName x sessionSourceMedium
  ga4-purchases-detail.csv            date x source x pagePath x transactionId
"""
import json, csv, collections, re
from urllib.parse import urlparse

B = "/home/user/projects/data/supermetrics-archive-2026-09-08/"

def n(v):
    try: return float(v)
    except (TypeError, ValueError): return 0.0

# ---------- load pageReferrer ----------
j = json.load(open(B + "raw-ga4-pagereferrer-monthly.json"))["data"]
RF = {k: i for i, k in enumerate(j["requested_field_ids"])}
REFROWS = j["data"][1:]

# ---------- load source/medium ----------
SRC = list(csv.DictReader(open(B + "ga4-events-by-source-monthly.csv")))

# ---------- totals per month (denominators) ----------
TOT = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
for r in SRC:
    a = TOT[r["yearMonth"]]
    a[0] += n(r["eventCount"]); a[1] += n(r["sessions"]); a[2] += n(r["conversions"])
PURTOT = collections.Counter()
for r in SRC:
    if r["eventName"] == "purchase":
        PURTOT[r["yearMonth"]] += n(r["eventCount"])

# ---------- classifiers ----------
KNOWN = re.compile(
    r'(google|bing|yahoo|duckduckgo|ecosia|baidu|yandex|facebook|instagram|youtube|linkedin'
    r'|twitter|t\.co|reddit|pinterest|tiktok|yelp|acuity|squarespace|charmtracker|mailchimp'
    r'|mailchi|paypal|pankanaturalhealth|doubleclick|googlesyndication|chatgpt|perplexity'
    r'|claude|gemini|linktr|msn\.com|office\.net|microsoft|webmd|drugs\.com|healthgrades'
    r'|npidb|zocdoc|sharecare|mnanp|oncanp|findanaturaldoctor|minnesotaintegrative|hbcamn'
    r'|thinkhopkins|novochiromn|ultalabtests|agilemoxie|deadlinkchecker|url-opener'
    r'|indiatimes|ampproject|investing\.com|dexknows|localhost|android|intakeq|badgermapping'
    r'|neilpatel|teams\.)', re.I)

def ref_class(host):
    if host in ("tagassistant.google.com",):                    return "A_tag_assistant_debug"
    if host in ("ads.google.com",):                             return "B_google_ads_ui_clickthrough"
    if host == "apricots-crow-dwjh.squarespace.com":            return "C_squarespace_preview_operator"
    if host in ("account.squarespace.com", "secure.squarespace.com",
                "us19.admin.mailchimp.com", "bize.admin.yelp.com",
                "app.neilpatel.com", "www.deadlinkchecker.com"): return "D_operator_admin_tools"
    if host.endswith("charmtracker.com"):                       return "E_internal_ehr_patient_portal"
    if host == "syndicatedsearch.goog":                         return "H_google_search_partners"
    if host == "googleads.g.doubleclick.net":                   return "G_doubleclick_adredirect_legacy"
    if host.endswith("pankanaturalhealth.com"):                 return "I_PROTECTED_own_domain_referrer"
    if "acuity" in host or host == "app.squarespacescheduling.com":
                                                                return "J_PROTECTED_acuity_scheduler"
    if not KNOWN.search(host):                                  return "F_referral_spam_bot"
    return None

def sm_class(sm):
    s = sm.lower()
    if s.startswith("tagassistant.google.com"):   return "A_tag_assistant_debug"
    if s.startswith("ads.google.com"):            return "B_google_ads_ui_clickthrough"
    if s.startswith("apricots-crow-dwjh"):        return "C_squarespace_preview_operator"
    if s.startswith(("account.squarespace.com", "secure.squarespace.com",
                     "us19.admin.mailchimp.com")): return "D_operator_admin_tools"
    if "charmtracker.com" in s:                   return "E_internal_ehr_patient_portal"
    if s.startswith("pankanaturalhealth.com"):    return "I_PROTECTED_own_domain_referrer"
    if s.startswith(("app.acuityscheduling.com", "app.squarespacescheduling.com")):
                                                  return "J_PROTECTED_acuity_scheduler"
    if s.startswith("syndicatedsearch"):          return "H_google_search_partners"
    if s.endswith("/ referral"):
        host = s.split(" / ")[0]
        if not KNOWN.search(host):                return "F_referral_spam_bot"
    return None

VERDICT = {
 "A_tag_assistant_debug":          "JUNK - remove from any count",
 "B_google_ads_ui_clickthrough":   "JUNK - remove from any count",
 "C_squarespace_preview_operator": "JUNK - operator editing own site",
 "D_operator_admin_tools":         "JUNK - operator admin consoles",
 "E_internal_ehr_patient_portal":  "NOT-PROSPECT - existing patients via portal",
 "F_referral_spam_bot":            "JUNK - referral spam / bot",
 "G_doubleclick_adredirect_legacy":"BENIGN - legacy ad redirect, pre-2025|03 only",
 "H_google_search_partners":       "REAL but low quality - Search Partners inventory",
 "I_PROTECTED_own_domain_referrer":"DO NOT FILTER - see NOTES section 5",
 "J_PROTECTED_acuity_scheduler":   "DO NOT FILTER - booking fingerprint",
}

out = []

# ---- pass 1: pageReferrer grain ----
agg = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
for r in REFROWS:
    host = urlparse(r[RF["pageReferrer"]] or "").netloc.lower()
    if not host: continue
    c = ref_class(host)
    if not c: continue
    k = (c, "pageReferrer", host, r[RF["yearMonth"]], r[RF["eventName"]])
    a = agg[k]
    a[0] += n(r[RF["eventCount"]]); a[1] += n(r[RF["sessions"]]); a[2] += n(r[RF["conversions"]])
for k, v in agg.items():
    out.append(list(k) + [int(v[0]), int(v[1]), int(v[2]), 0.0])

# ---- pass 2: sessionSourceMedium grain ----
agg2 = collections.defaultdict(lambda: [0.0, 0.0, 0.0])
for r in SRC:
    c = sm_class(r["sessionSourceMedium"])
    if not c: continue
    k = (c, "sessionSourceMedium", r["sessionSourceMedium"], r["yearMonth"], r["eventName"])
    a = agg2[k]
    a[0] += n(r["eventCount"]); a[1] += n(r["sessions"]); a[2] += n(r["conversions"])
for k, v in agg2.items():
    out.append(list(k) + [int(v[0]), int(v[1]), int(v[2]), 0.0])

# ---- pass 3: $1.00 purchase test signature (transaction grain) ----
agg3 = collections.defaultdict(lambda: [0.0, 0.0])
for r in csv.DictReader(open(B + "ga4-purchases-detail.csv")):
    ec, rev = int(r["eventCount"]), n(r["totalRevenue"])
    if ec and abs(rev / ec - 1.0) < 1e-9:
        ym = r["date"][:4] + "|" + r["date"][5:7]
        k = ("K_dollar_one_test_purchase", "purchase unit value == $1.00",
             r["sessionSourceMedium"], ym, "purchase")
        a = agg3[k]; a[0] += ec; a[1] += rev
for k, v in agg3.items():
    out.append(list(k) + [int(v[0]), 0, int(v[0]), round(v[1], 2)])
VERDICT["K_dollar_one_test_purchase"] = "JUNK - $1 is not a PNH price; snippet test firing"

# ---- assemble ----
hdr = ["pollution_class", "detection_field", "detection_value", "yearMonth", "eventName",
       "eventCount", "sessions", "ga4_conversions", "revenue_usd",
       "month_total_events", "month_total_conversions", "month_total_purchase_events",
       "pct_of_month_events", "pct_of_month_conversions", "verdict"]
rows = []
for r in out:
    cls, ym = r[0], r[3]
    te, tc = TOT[ym][0], TOT[ym][2]
    tp = PURTOT[ym]
    rows.append(r + [int(te), int(tc), int(tp),
                     round(100 * r[5] / te, 3) if te else "",
                     round(100 * r[7] / tc, 3) if tc else "",
                     VERDICT[cls]])
rows.sort(key=lambda x: (x[0], x[3], x[1], x[2], x[4]))
with open(B + "pollution-quantified.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(hdr); w.writerows(rows)
print("wrote pollution-quantified.csv:", len(rows), "rows")

# ---- console summary ----
print("\n=== class totals (all time) ===")
ct = collections.defaultdict(lambda: [0, 0, 0, 0.0])
for r in rows:
    if r[1] == "sessionSourceMedium" or r[0] == "K_dollar_one_test_purchase":
        a = ct[(r[0], r[1])]
        a[0] += r[5]; a[1] += r[6]; a[2] += r[7]; a[3] += r[8]
for r in rows:
    if r[1] == "pageReferrer":
        a = ct[(r[0], r[1])]
        a[0] += r[5]; a[1] += r[6]; a[2] += r[7]
for k in sorted(ct):
    v = ct[k]
    print("  %-33s %-20s ev=%6d sess=%6d conv=%5d rev=$%.2f" % (k[0], k[1], v[0], v[1], v[2], v[3]))

print("\n=== July vs August 2026 by class ===")
for m in ("2026|07", "2026|08"):
    print(" ", m)
    ct2 = collections.defaultdict(lambda: [0, 0, 0])
    for r in rows:
        if r[3] == m:
            a = ct2[(r[0], r[1])]; a[0] += r[5]; a[1] += r[6]; a[2] += r[7]
    for k in sorted(ct2):
        v = ct2[k]
        print("    %-33s %-22s ev=%5d sess=%5d conv=%4d" % (k[0], k[1], v[0], v[1], v[2]))
