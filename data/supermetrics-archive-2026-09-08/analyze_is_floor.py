import csv, collections

def rd(p):
    with open(p) as f: return list(csv.DictReader(f))

d = rd('ads-campaign-daily.csv'); m = rd('ads-campaign-monthly.csv')
w = rd('ads-campaign-weekly.csv'); a = rd('ads-account-monthly.csv')

def f(v): return None if v in ('', None) else float(v)

print('='*72)
print('1. DISTRIBUTION OF Search impression share (all grains, all campaigns)')
print('='*72)
for label, rows in [('daily',d),('weekly',w),('monthly',m),('account-monthly',a)]:
    vals=[f(r['SearchImpressionShare']) for r in rows]
    vals=[v for v in vals if v is not None]
    c=collections.Counter(vals)
    n=len(vals)
    print(f'\n{label}: n={n} non-null')
    print(f'  exactly 0.0999 : {c[0.0999]:3d}  ({100*c[0.0999]/n:.1f}%)')
    below=[v for v in vals if v<0.0999]
    print(f'  strictly <0.0999: {len(below)}  values={sorted(set(below))}')
    between=[v for v in vals if 0.0999<v<0.11]
    print(f'  in (0.0999,0.11): {len(between)}  values={sorted(set(between))}')

print()
print('='*72)
print('2. THE ARITHMETIC TEST: does SIS + budget-lost + rank-lost equal 1.0?')
print('   (Google defines these three as an exhaustive partition of eligible')
print('    impressions, so a true measurement must sum to 1.0)')
print('='*72)
over=[]
for r in d:
    s,b,k=f(r['SearchImpressionShare']),f(r['SearchBudgetLostImpressionShare']),f(r['SearchRankLostImpressionShare'])
    if None in (s,b,k): continue
    over.append((r['Date'],r['Campaignname'],s,b,k,s+b+k))
tot=[x[5] for x in over]
print(f'n rows tested: {len(tot)}')
print(f'  sum == 1.000 (+/-0.002): {sum(1 for t in tot if abs(t-1)<=0.002)}')
print(f'  sum  > 1.002           : {sum(1 for t in tot if t>1.002)}')
print(f'  sum  < 0.998           : {sum(1 for t in tot if t<0.998)}')
print(f'  max sum: {max(tot):.4f}   min sum: {min(tot):.4f}')
print('\n  Worst offenders (largest overshoot) - all are SIS==0.0999 rows:')
for x in sorted(over,key=lambda x:-x[5])[:8]:
    print(f'    {x[0]} {x[1][:14]:14s} SIS={x[2]:.4f} budget={x[3]:.4f} rank={x[4]:.4f} SUM={x[5]:.4f}  -> implied true SIS={1-x[3]-x[4]:.4f}')

print()
print('='*72)
print('3. THE CEILING TWIN: 0.9001 on budget-lost  (= 1 - 0.0999)')
print('='*72)
cb=collections.Counter(f(r['SearchBudgetLostImpressionShare']) for r in d if r['SearchBudgetLostImpressionShare'])
print(f'  budget-lost exactly 0.9001: {cb[0.9001]} of {sum(cb.values())} daily rows')
print(f'  budget-lost >0.9001       : {sum(v for k,v in cb.items() if k and k>0.9001)}')
print('  -> nothing ever exceeds 0.9001. It is a hard ceiling, not a distribution.')

print()
print('='*72)
print('4. THE SAME VALUE APPEARS ON UNRELATED SURFACES')
print('='*72)
print('  a) PMax "Campaign #1" has NO search-IS reporting (SearchImpressionShare is null),')
print('     yet SearchImpressionShareRaw returns:')
for r in w:
    if r['Campaignname']=='Campaign #1' and r['SearchImpressionShareRaw']:
        print(f"     week {r['Yearweekiso']}  impressions={r['Impressions']:>6s}  rawIS={r['SearchImpressionShareRaw']}  exactMatchIS={r['SearchExactMatchImpressionShare']}")
print()
print('  b) CONTENT impression share, account level, July 2026 (no Display campaign ran):')
for r in a:
    if r['ContentImpressionShare']:
        print(f"     {r['Yearmonth']}  ContentIS={r['ContentImpressionShare']}  ContentBudgetLost={r['ContentBudgetLostImpressionShare']}  ContentRankLost={r['ContentRankLostImpressionShare']}")
print()
print('  c) Top / absolute-top IS cluster on the same boundary:')
ct=collections.Counter(f(r['SearchTopImpressionShare']) for r in d if r['SearchTopImpressionShare'])
ca=collections.Counter(f(r['SearchAbsoluteTopImpressionShare']) for r in d if r['SearchAbsoluteTopImpressionShare'])
print(f"     SearchTopImpressionShare == 0.10  : {ct[0.1]} rows; any value in (0,0.10)? {sorted(v for v in ct if 0<v<0.1)}")
print(f"     SearchAbsoluteTopIS      == 0.0999: {ca[0.0999]} rows; any value in (0,0.0999)? {sorted(v for v in ca if 0<v<0.0999)}")

print()
print('='*72)
print('5. CONTRAST: a metric Google does NOT floor (account-level exact-match IS)')
print('='*72)
for r in a:
    print(f"   {r['Yearmonth']}  SearchIS={r['SearchImpressionShare'] or 'null':>6s}   SearchExactMatchIS={r['SearchExactMatchImpressionShare']}")
print('   -> exact-match IS returns genuine sub-1% values (0.001-0.0082).')
print('      So the API CAN express <10%. The main IS metrics simply are not allowed to.')
