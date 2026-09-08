import json, csv, collections

REMOVED_AG_NOTE = "Ad group 1 (183759893484) is currently REMOVED but served historically."

def load(path):
    j = json.load(open(path))
    d = j['data']
    return d['requested_field_ids'], d['data'][1:]

def write_csv(path, header, rows):
    with open(path, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for r in rows:
            w.writerow(['' if v is None else v for v in r])
    print('wrote %-42s %4d rows' % (path, len(rows)))

# ---------------- 1. monthly ----------------
fm, rm = load('raw-ads-keywords-monthly.json')
Im = {n: i for i, n in enumerate(fm)}
rm.sort(key=lambda r: (r[Im['Yearmonth']], r[Im['Campaignname']], r[Im['Adgroupname']],
                       (r[Im['Keyword']] or ''), (r[Im['Matchtype']] or '')))
write_csv('ads-keywords-monthly.csv', fm, rm)

# ---------------- 2. all-time ----------------
fa, ra = load('raw-ads-keywords-alltime.json')
Ia = {n: i for i, n in enumerate(fa)}
ra.sort(key=lambda r: -(r[Ia['Cost']] or 0))
write_csv('ads-keywords-alltime.csv', fa, ra)

# ---------------- 3. zero-conversion ----------------
zc_header = ['Campaignname', 'Adgroupname', 'AdgroupID', 'Adgroupstatus', 'Keyword', 'KeywordID',
             'Matchtype', 'Keywordstatus', 'SystemServingStatus', 'MaxCPCCurrency',
             'LifetimeCost', 'LifetimeClicks', 'LifetimeImpressions', 'LifetimeConversions',
             'LifetimeAllConversions', 'Ctr', 'CPC', 'Qualityscore',
             'impressions_but_never_clicked', 'never_served', 'can_serve_today',
             'months_active', 'first_month', 'last_month']

# month coverage per (adgroup, keyword id) from monthly file
months = collections.defaultdict(list)
for r in rm:
    if (r[Im['Impressions']] or 0) > 0:
        months[(r[Im['AdgroupID']], r[Im['KeywordID']])].append(r[Im['Yearmonth']])

zc = []
for r in ra:
    conv = r[Ia['Conversions']] or 0
    if conv != 0:
        continue
    key = (r[Ia['AdgroupID']], r[Ia['KeywordID']])
    ms = sorted(months.get(key, []))
    imps = r[Ia['Impressions']] or 0
    clicks = r[Ia['Clicks']] or 0
    can_serve = (r[Ia['Adgroupstatus']] != 'removed'
                 and r[Ia['Keywordstatus']] == 'enabled'
                 and r[Ia['Campaignstatus']] == 'enabled')
    zc.append([
        r[Ia['Campaignname']], r[Ia['Adgroupname']], r[Ia['AdgroupID']], r[Ia['Adgroupstatus']],
        r[Ia['Keyword']], r[Ia['KeywordID']], r[Ia['Matchtype']], r[Ia['Keywordstatus']],
        r[Ia['SystemServingStatus']], r[Ia['MaxCPCCurrency']],
        round(r[Ia['Cost']] or 0, 4), clicks, imps, conv,
        r[Ia['EstimatedTotalConversions']] or 0, r[Ia['Ctr']], r[Ia['CPC']], r[Ia['Qualityscore']],
        'YES' if (imps > 0 and clicks == 0) else '',
        'YES' if imps == 0 else '',
        'YES' if can_serve else '',
        len(ms), ms[0] if ms else '', ms[-1] if ms else '',
    ])
zc.sort(key=lambda x: -x[10])
write_csv('ads-keywords-zero-conversion.csv', zc_header, zc)

zc_cost = sum(x[10] for x in zc)
zc_imp_no_click = [x for x in zc if x[18] == 'YES']
print()
print('ZERO-CONVERSION SUMMARY')
print('  keywords with zero lifetime conversions : %d of %d' % (len(zc), len(ra)))
print('  lifetime spend on them                  : $%.2f' % zc_cost)
print('  ... of total account keyword spend      : $%.2f (%.1f%%)'
      % (sum(r[Ia['Cost']] or 0 for r in ra), 100 * zc_cost / sum(r[Ia['Cost']] or 0 for r in ra)))
print('  impressions but never a single click    : %d keywords, $%.2f'
      % (len(zc_imp_no_click), sum(x[10] for x in zc_imp_no_click)))
print('  never served at all (0 impressions)     : %d keywords' % sum(1 for x in zc if x[19] == 'YES'))
print('  still able to serve today               : %d keywords, $%.2f lifetime'
      % (sum(1 for x in zc if x[20] == 'YES'), sum(x[10] for x in zc if x[20] == 'YES')))
