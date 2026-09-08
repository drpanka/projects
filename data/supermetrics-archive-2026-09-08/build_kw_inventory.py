import json, csv, collections

# current inventory from the campaign resource (authoritative for what EXISTS today)
jc = json.load(open('raw-campaign-full-leads-search-1.json'))
camp = jc['data']['data']['results'][0]

# statuses + lifetime stats from KeywordView (authoritative for status, but only
# covers keywords that have accrued reportable stats)
ja = json.load(open('raw-ads-keywords-alltime.json'))
d = ja['data']; ra = d['data'][1:]; fa = d['requested_field_ids']
Ia = {n: i for i, n in enumerate(fa)}
stat = {}
for r in ra:
    if r[Ia['Campaignname']] != 'Leads-Search-1':
        continue
    key = (r[Ia['AdgroupID']], (r[Ia['Keyword']] or '').lower(), (r[Ia['Matchtype']] or '').lower())
    # prefer the live (enabled/paused) row over an old removed criterion for the same text
    prev = stat.get(key)
    if prev and prev[Ia['Keywordstatus']] in ('enabled', 'paused'):
        continue
    stat[key] = r

header = ['Adgroupname', 'AdgroupID', 'Adgroupstatus', 'AdgroupMaxCPC', 'Keyword', 'Matchtype',
          'KeywordID', 'Keywordstatus', 'status_source', 'active_today',
          'LifetimeImpressions', 'LifetimeClicks', 'LifetimeCost', 'LifetimeConversions',
          'Qualityscore', 'SystemServingStatus']
out = []
for ag in camp['ad_groups']:
    for kw in (ag['targeting'].get('keywords') or []):
        text = kw['text']; mt = kw['match_type']
        key = (ag['ad_group_id'], text.lower(), mt.lower())
        r = stat.get(key)
        if r is not None and r[Ia['Keywordstatus']] in ('enabled', 'paused'):
            ks, src = r[Ia['Keywordstatus']], 'KeywordView report'
        else:
            # exists in the campaign resource but has no live KeywordView row:
            # it is a real, non-removed criterion that simply never accrued stats
            ks, src = 'enabled', 'inferred (exists in campaign, not in paused set)'
            r = None
        out.append([
            ag['name'], ag['ad_group_id'], ag['status'], ag['cpc_bid'], text, mt.title(),
            r[Ia['KeywordID']] if r else '', ks, src, 'YES' if ks == 'enabled' else '',
            (r[Ia['Impressions']] if r else '') or 0,
            (r[Ia['Clicks']] if r else '') or 0,
            round((r[Ia['Cost']] if r else 0) or 0, 4),
            (r[Ia['Conversions']] if r else '') or 0,
            (r[Ia['Qualityscore']] if r else '') or '',
            (r[Ia['SystemServingStatus']] if r else '') or '',
        ])

out.sort(key=lambda x: (x[0], x[7], x[4]))
with open('ads-keywords-current-inventory.csv', 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(header); w.writerows(out)
print('wrote ads-keywords-current-inventory.csv', len(out), 'rows')

print()
print('CURRENT INVENTORY, Leads-Search-1 (all 6 ad groups ENABLED, campaign ENABLED)')
per = collections.defaultdict(lambda: collections.Counter())
for r in out:
    per[r[0]][r[7]] += 1
tot = collections.Counter()
for ag in sorted(per):
    c = per[ag]
    print('  %-38s enabled=%3d paused=%3d total=%3d' % (ag, c['enabled'], c['paused'], sum(c.values())))
    tot += c
print('  %-38s enabled=%3d paused=%3d total=%3d' % ('TOTAL', tot['enabled'], tot['paused'], sum(tot.values())))
print()
print('  match types:', dict(collections.Counter(r[5] for r in out)))
print('  enabled-only match types:', dict(collections.Counter(r[5] for r in out if r[7] == 'enabled')))
print('  never accrued any stats (0 impressions):', sum(1 for r in out if (r[10] or 0) == 0))
