import json, csv, datetime
from collections import defaultdict

def load(path, nested):
    d = json.load(open(path))
    return d['data'] if nested else d

def to_csv(payload, out, drop_display_header):
    fids = payload['requested_field_ids']
    rows = payload['data']
    if drop_display_header:
        rows = rows[1:]
    with open(out, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(fids)
        for r in rows:
            w.writerow(['' if v is None else v for v in r])
    return fids, rows

daily = load('raw-ads-campaign-daily.json', True)
dfids, drows = to_csv(daily, 'ads-campaign-daily.csv', True)

mon = load('raw-ads-campaign-monthly.json', False)
mfids, mrows = to_csv(mon, 'ads-campaign-monthly.csv', False)

wk = load('raw-ads-campaign-weekly.json', False)
wfids, wrows = to_csv(wk, 'ads-campaign-weekly.csv', False)

acct = load('raw-ads-account-monthly.json', False)
afids, arows = to_csv(acct, 'ads-account-monthly.csv', False)

print('daily  rows', len(drows))
print('monthly rows', len(mrows))
print('weekly rows', len(wrows))
print('account rows', len(arows))

# ---- cross-validate additive columns: daily -> month, daily -> week, daily -> account-month
di = {f:i for i,f in enumerate(dfids)}
mi = {f:i for i,f in enumerate(mfids)}
wi = {f:i for i,f in enumerate(wfids)}
ai = {f:i for i,f in enumerate(afids)}

ADD = ['Impressions','Clicks','Cost','Conversions']

def num(v): return 0.0 if v in (None,'') else float(v)

bym = defaultdict(lambda: defaultdict(float))
byw = defaultdict(lambda: defaultdict(float))
bya = defaultdict(lambda: defaultdict(float))
for r in drows:
    d = datetime.date.fromisoformat(r[di['Date']])
    ym = f"{d.year}|{d.month:02d}"
    iso = d.isocalendar()
    yw = f"{iso[0]}|{iso[1]:02d}"
    camp = r[di['Campaignname']]
    for c in ADD:
        bym[(ym,camp)][c] += num(r[di[c]])
        byw[(yw,camp)][c] += num(r[di[c]])
        bya[ym][c] += num(r[di[c]])

def check(label, api_rows, idx, keyfn, agg):
    print(f'\n== {label}: API vs sum-of-daily ==')
    problems = 0
    for r in api_rows:
        k = keyfn(r)
        got = agg.get(k)
        if got is None:
            print(f'  {k}: no daily rows (API imps={r[idx["Impressions"]]})'); continue
        for c in ADD:
            a = num(r[idx[c]]); b = got[c]
            if abs(a-b) > 0.02:
                print(f'  MISMATCH {k} {c}: api={a} daily={b}')
                problems += 1
    print(f'  mismatches: {problems}')
    return problems

p1 = check('MONTHLY', mrows, mi, lambda r:(r[mi['Yearmonth']], r[mi['Campaignname']]), bym)
p2 = check('WEEKLY',  wrows, wi, lambda r:(r[wi['Yearweekiso']], r[wi['Campaignname']]), byw)
p3 = check('ACCOUNT', arows, ai, lambda r: r[ai['Yearmonth']], bya)
print('\nTOTAL MISMATCHES:', p1+p2+p3)
