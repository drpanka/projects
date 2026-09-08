import json, csv, collections

j = json.load(open('raw-ads-keywords-monthly.json'))
d = j['data']; rows = d['data'][1:]; f = d['requested_field_ids']
I = {n: i for i, n in enumerate(f)}

# every month in the window, so the dark period is explicit
allmonths = []
for y in (2025, 2026):
    for m in range(1, 13):
        if (y, m) < (2025, 6) or (y, m) > (2026, 9):
            continue
        allmonths.append('%d|%02d' % (y, m))

agg = collections.defaultdict(lambda: {
    'served': set(), 'reported': set(), 'served_texts': set(),
    'served_liveag': set(), 'reported_liveag': set(),
    'served_ls1': set(), 'reported_ls1': set(),
    'imp': 0, 'clicks': 0, 'cost': 0.0, 'conv': 0.0,
    'adgroups': set(),
})

for r in rows:
    m = r[I['Yearmonth']]
    key = (r[I['AdgroupID']], r[I['KeywordID']])
    text = (r[I['Keyword']], r[I['Matchtype']])
    imps = r[I['Impressions']] or 0
    a = agg[m]
    a['reported'].add(key)
    if imps > 0:
        a['served'].add(key)
        a['served_texts'].add(text)
        a['adgroups'].add(r[I['Adgroupname']])
    if r[I['Adgroupstatus']] != 'removed':
        a['reported_liveag'].add(key)
        if imps > 0:
            a['served_liveag'].add(key)
    if r[I['Campaignname']] == 'Leads-Search-1':
        a['reported_ls1'].add(key)
        if imps > 0:
            a['served_ls1'].add(key)
    a['imp'] += imps
    a['clicks'] += r[I['Clicks']] or 0
    a['cost'] += r[I['Cost']] or 0
    a['conv'] += r[I['Conversions']] or 0

header = ['Yearmonth', 'active_keywords_served', 'active_keywords_served_LeadsSearch1',
          'distinct_keyword_text_matchtype_served', 'keywords_reported_any',
          'served_in_currently_live_adgroups', 'ad_groups_serving',
          'Impressions', 'Clicks', 'Cost', 'Conversions', 'note']

out = []
for m in allmonths:
    a = agg.get(m)
    if not a:
        out.append([m, 0, 0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 'NO DATA - account dark, zero delivery'])
        continue
    note = ''
    if m in ('2025|07', '2025|08'):
        note = 'pre-rebuild; ALL delivery came from "Ad group 1" (183759893484), which is REMOVED today'
    if m == '2026|09':
        note = 'partial month: 2026-09-01 through 2026-09-08 only'
    out.append([m, len(a['served']), len(a['served_ls1']), len(a['served_texts']),
                len(a['reported']), len(a['served_liveag']), len(a['adgroups']),
                a['imp'], a['clicks'], round(a['cost'], 4), round(a['conv'], 4), note])

with open('ads-keyword-count-by-month.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(header); w.writerows(out)
print('wrote ads-keyword-count-by-month.csv', len(out), 'rows')
print()
print('%-9s %6s %6s %6s %6s %6s  %s' % ('month','served','LS1','texts','report','liveAG','note'))
for r in out:
    print('%-9s %6d %6d %6d %6d %6d  %s' % (r[0], r[1], r[2], r[3], r[4], r[5], r[11][:52]))
