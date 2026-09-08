import json, csv, datetime
from collections import defaultdict
D = "/home/user/projects/data/supermetrics-archive-2026-09-08/"
rv = json.load(open(D+"raw-gmb-reviews.json"))["data"][1:]
mon = json.load(open(D+"raw-gmb-reviews-monthly.json"))["data"][1:]
tot = json.load(open(D+"raw-gmb-review-totals-lifetime.json"))["data"][1:]

def d(s): return datetime.datetime.strptime(s[:10], "%Y-%m-%d").date()

with open(D+"gmb-reviews.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["review_create_date","review_create_time","review_id","location_name",
                "star_rating_numeric","star_rating_display","reviewer_name","reviewer_type",
                "review_comment","has_comment_text","comment_char_len",
                "business_replied","review_reply_comment","review_reply_time",
                "reply_lag_days","review_update_time"])
    for cd,ct,rid,ln,stars,name,comment,reply,rtime,utime in sorted(rv, key=lambda r:r[0]):
        n = stars.count("★")
        lag = (d(rtime)-d(cd)).days if rtime else ""
        w.writerow([cd,ct,rid,ln,n,stars,name,"not_available_in_api",
                    comment, "yes" if comment.strip() else "no", len(comment),
                    "yes" if reply.strip() else "no", reply, rtime, lag, utime])

# monthly rollup, two bases
with open(D+"gmb-reviews-monthly.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["basis","year_month","review_count","avg_star_rating",
                "avg_reply_response_minutes","note"])
    bym = defaultdict(list)
    for r in rv: bym[r[0][:7]].append(r[4].count("★"))
    for ym in sorted(bym):
        w.writerow(["create_date", ym, len(bym[ym]), round(sum(bym[ym])/len(bym[ym]),2), "",
                    "from individually retrievable reviews only (4 of 15 lifetime)"])
    for ym,ln,cnt,avg,rt in mon:
        w.writerow(["supermetrics_update_date", ym.replace("|","-"), cnt, avg, rt,
                    "Supermetrics buckets a review by reply/update month, not creation month"])
    w.writerow(["lifetime_total","ALL_TIME", tot[0][2], tot[0][3], "",
                "ReviewsTotals report; includes the 11 reviews that predate the 2025-03-08 API floor"])

# stats
dates = sorted(d(r[0]) for r in rv)
today = datetime.date(2026,9,8)
gaps = [((dates[i+1]-dates[i]).days, str(dates[i]), str(dates[i+1])) for i in range(len(dates)-1)]
print("retrievable review dates:", [str(x) for x in dates])
print("last 12 mo:", sum(1 for x in dates if x > today-datetime.timedelta(days=365)))
print("last 18 mo (>=2025-03-08):", sum(1 for x in dates if x >= datetime.date(2025,3,8)))
print("longest gap (retrievable):", max(gaps))
print("all gaps:", gaps)
print("days since most recent review:", (today-dates[-1]).days)
print("unanswered:", sum(1 for r in rv if not r[7].strip()))
print("reply lags (days):", [( r[0], (d(r[8])-d(r[0])).days ) for r in rv])
