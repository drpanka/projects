import json, csv, collections, datetime, os

D = '/home/user/projects/data/supermetrics-archive-2026-09-08'
os.chdir(D)

def load(p):
    j = json.load(open(p))['data']
    return j['requested_field_ids'], j['data'][1:]

def num(v):
    return 0 if v is None else v

def ratio(a, b):
    return round(a / b, 6) if b else ''

def money(x):
    return round(x + 0.0, 4)

def write_csv(path, header, rows):
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for r in rows:
            w.writerow(['' if v is None else v for v in r])
    print('wrote %-46s %5d rows' % (path, len(rows)))

# ---------------------------------------------------------------- helpers
def agg(rows, idx, keyfields, mnames=('Impressions','Clicks','Cost','Conversions')):
    """Group rows by keyfields, summing the base metrics."""
    out = collections.OrderedDict()
    for r in rows:
        k = tuple(r[idx[f]] for f in keyfields)
        acc = out.setdefault(k, [0, 0, 0.0, 0.0])
        acc[0] += num(r[idx['Impressions']])
        acc[1] += num(r[idx['Clicks']])
        acc[2] += num(r[idx['Cost']])
        acc[3] += num(r[idx['Conversions']])
    return out

def emit(aggd, keyfields, sortkey=None):
    rows = []
    for k, (imp, clk, cost, conv) in aggd.items():
        rows.append(list(k) + [imp, clk, money(cost), ratio(clk, imp), round(conv, 2),
                               (money(cost / conv) if conv else '')])
    if sortkey:
        rows.sort(key=sortkey)
    return rows

MET = ['Impressions', 'Clicks', 'Cost', 'Ctr', 'Conversions', 'CostPerConversion']

# ================================================================ 1+2. GEO
for tag, src, alltime_out, monthly_out in [
    ('default',      'raw-geo-monthly-default.json',      'ads-geo-alltime.csv',              'ads-geo-monthly.csv'),
    ('userlocation', 'raw-geo-monthly-userlocation.json', 'ads-geo-userlocation-alltime.csv', 'ads-geo-userlocation-monthly.csv'),
]:
    f, rows = load(src)
    I = {n: i for i, n in enumerate(f)}

    # all time, city level, all campaigns combined
    a = agg(rows, I, ['City', 'Region', 'Country'])
    out = emit(a, None, sortkey=lambda r: (-r[5], -r[3]))   # cost desc, then impressions desc
    write_csv(alltime_out, ['City', 'Region', 'Country'] + MET, out)

    # monthly, city level, split by campaign (full granularity as pulled)
    rows_sorted = sorted(rows, key=lambda r: (r[I['Yearmonth']], r[I['Campaignname']],
                                              -num(r[I['Cost']]), r[I['City']] or ''))
    write_csv(monthly_out,
              ['Yearmonth', 'Campaignname', 'CampaignID', 'City', 'Region', 'Country'] + MET,
              rows_sorted)

# ================================================================ 3. DEVICE
f, rows = load('raw-device-daily.json')
I = {n: i for i, n in enumerate(f)}
a = agg(rows, I, ['Yearmonth', 'Campaignname', 'CampaignID', 'Device'])
write_csv('ads-device-monthly.csv',
          ['Yearmonth', 'Campaignname', 'CampaignID', 'Device'] + MET,
          emit(a, None, sortkey=lambda r: (r[0], r[1], r[3])))
write_csv('ads-device-daily.csv', f,
          sorted(rows, key=lambda r: (r[I['Date']], r[I['Campaignname']], r[I['Device']])))

# device all-time rollup (bonus)
a = agg(rows, I, ['Campaignname', 'Device'])
write_csv('ads-device-alltime.csv', ['Campaignname', 'Device'] + MET,
          emit(a, None, sortkey=lambda r: (r[0], -r[4])))

# ================================================================ 4. NETWORK
f, rows = load('raw-network-daily.json')
I = {n: i for i, n in enumerate(f)}
a = agg(rows, I, ['Yearmonth', 'Campaignname', 'CampaignID', 'Network', 'Networkwithsearchpartners'])
write_csv('ads-network-monthly.csv',
          ['Yearmonth', 'Campaignname', 'CampaignID', 'Network', 'Networkwithsearchpartners'] + MET,
          emit(a, None, sortkey=lambda r: (r[0], r[1], r[4])))
write_csv('ads-network-daily.csv', f,
          sorted(rows, key=lambda r: (r[I['Date']], r[I['Campaignname']],
                                      r[I['Networkwithsearchpartners']], r[I['Device']])))
a = agg(rows, I, ['Campaignname', 'Networkwithsearchpartners'])
write_csv('ads-network-alltime.csv', ['Campaignname', 'Networkwithsearchpartners'] + MET,
          emit(a, None, sortkey=lambda r: (r[0], -r[4])))

# ================================================================ 5. HOUR x DOW
f, rows = load('raw-hour-daily.json')
I = {n: i for i, n in enumerate(f)}
write_csv('ads-hour-daily-by-campaign.csv', f,
          sorted(rows, key=lambda r: (r[I['Date']], r[I['Campaignname']], r[I['Hour']])))

DOW_ORDER = ['1 Monday', '2 Tuesday', '3 Wednesday', '4 Thursday', '5 Friday', '6 Saturday', '0 Sunday']
dow_seen = sorted({r[I['DayofweekWithNum']] for r in rows})
assert set(dow_seen) <= set(DOW_ORDER), dow_seen

# all-time grid, all campaigns, complete 7x24 including never-served cells
a = agg(rows, I, ['DayofweekWithNum', 'Hour'])
grid = []
for d in DOW_ORDER:
    for h in range(24):
        k = (d, '%02d' % h)
        imp, clk, cost, conv = a.get(k, [0, 0, 0.0, 0.0])
        grid.append([d, '%02d' % h, imp, clk, money(cost), ratio(clk, imp),
                     round(conv, 2), (money(cost / conv) if conv else '')])
write_csv('ads-hour-dayofweek-alltime.csv',
          ['DayofweekWithNum', 'Hour'] + MET, grid)

# all-time grid split by campaign (bonus)
a = agg(rows, I, ['Campaignname', 'DayofweekWithNum', 'Hour'])
write_csv('ads-hour-dayofweek-alltime-by-campaign.csv',
          ['Campaignname', 'DayofweekWithNum', 'Hour'] + MET,
          emit(a, None, sortkey=lambda r: (r[0], r[1], r[2])))

# monthly
a = agg(rows, I, ['Yearmonth' if 'Yearmonth' in I else 'Date', 'DayofweekWithNum', 'Hour']) \
    if 'Yearmonth' in I else None
if a is None:
    tmp = collections.OrderedDict()
    for r in rows:
        ym = r[I['Date']][:7].replace('-', '|')
        k = (ym, r[I['Campaignname']], r[I['CampaignID']], r[I['DayofweekWithNum']], r[I['Hour']])
        acc = tmp.setdefault(k, [0, 0, 0.0, 0.0])
        acc[0] += num(r[I['Impressions']]); acc[1] += num(r[I['Clicks']])
        acc[2] += num(r[I['Cost']]);        acc[3] += num(r[I['Conversions']])
    a = tmp
write_csv('ads-hour-dayofweek-monthly.csv',
          ['Yearmonth', 'Campaignname', 'CampaignID', 'DayofweekWithNum', 'Hour'] + MET,
          emit(a, None, sortkey=lambda r: (r[0], r[1], r[3], r[4])))

print('\n--- hour data coverage ---')
dates = sorted({r[I['Date']] for r in rows})
print('first date:', dates[0], ' last date:', dates[-1], ' distinct days:', len(dates))
