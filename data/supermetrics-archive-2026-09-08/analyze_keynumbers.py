import csv, datetime, collections
def rd(p):
    with open(p) as f: return list(csv.DictReader(f))
def f(v): return None if v in ('',None) else float(v)
m=rd('ads-campaign-monthly.csv'); a=rd('ads-account-monthly.csv'); d=rd('ads-campaign-daily.csv')

print('='*100)
print('MONTHLY SPEND + CPA, ACCOUNT LEVEL (all campaigns combined)')
print('='*100)
print(f"{'month':8s} {'spend':>10s} {'clicks':>7s} {'conv':>9s} {'CPA':>10s} {'CPC':>7s} {'CTR':>7s} {'impr':>8s}")
for r in a:
    sp=f(r['Cost']); cv=f(r['Conversions']); cpa=f(r['CostPerConversion'])
    print(f"{r['Yearmonth']:8s} {sp:>10.2f} {r['Clicks']:>7s} {cv:>9.2f} {(f'{cpa:.2f}' if cpa else 'n/a'):>10s} {(f(r['CPC']) or 0):>7.2f} {(f(r['Ctr']) or 0)*100:>6.2f}% {r['Impressions']:>8s}")

print()
print('='*100)
print('MONTHLY SPEND + CPA, PER CAMPAIGN')
print('='*100)
print(f"{'month':8s} {'campaign':36s} {'spend':>9s} {'conv':>9s} {'CPA':>10s} {'budgetLostIS':>13s} {'rankLostIS':>11s} {'reportedSIS':>12s} {'impliedSIS':>11s}")
for r in m:
    sp=f(r['Cost']); cv=f(r['Conversions']); cpa=f(r['CostPerConversion'])
    b=f(r['SearchBudgetLostImpressionShare']); k=f(r['SearchRankLostImpressionShare']); s=f(r['SearchImpressionShare'])
    imp = (1-b-k) if (b is not None and k is not None) else None
    print(f"{r['Yearmonth']:8s} {r['Campaignname'][:36]:36s} {sp:>9.2f} {cv:>9.2f} "
          f"{(f'{cpa:.2f}' if cpa else 'n/a'):>10s} "
          f"{(f'{b*100:.2f}%' if b is not None else '-'):>13s} "
          f"{(f'{k*100:.2f}%' if k is not None else '-'):>11s} "
          f"{(f'{s*100:.2f}%' if s is not None else '-'):>12s} "
          f"{(f'{imp*100:.2f}%' if imp is not None else '-'):>11s}")

print()
print('='*100)
print('MONTHS WHERE BUDGET-LOST IMPRESSION SHARE EXCEEDED 80%')
print('='*100)
for r in m:
    b=f(r['SearchBudgetLostImpressionShare'])
    if b is not None and b>0.80:
        print(f"  {r['Yearmonth']}  {r['Campaignname']:36s} budget-lost={b*100:.2f}%  rank-lost={f(r['SearchRankLostImpressionShare'])*100:.2f}%  spend=${f(r['Cost']):.2f}")
print('  (account level)')
for r in a:
    b=f(r['SearchBudgetLostImpressionShare'])
    if b is not None and b>0.80:
        print(f"  {r['Yearmonth']}  {'ACCOUNT TOTAL':36s} budget-lost={b*100:.2f}%  rank-lost={f(r['SearchRankLostImpressionShare'])*100:.2f}%  spend=${f(r['Cost']):.2f}")

print()
print('='*100)
print('BUDGET-LOST vs RANK-LOST: July 2025  vs  July 2026 / August 2026  (Leads-Search-1)')
print('='*100)
for ym in ['2025|07','2025|08','2026|07','2026|08','2026|09']:
    for r in m:
        if r['Yearmonth']==ym and r['Campaignname']=='Leads-Search-1':
            b=f(r['SearchBudgetLostImpressionShare']); k=f(r['SearchRankLostImpressionShare']); s=f(r['SearchImpressionShare'])
            spend=f(r['Cost']); days=len({x['Date'] for x in d if x['Date'][:7].replace('-','|')==ym and x['Campaignname']=='Leads-Search-1' and float(x['Impressions'] or 0)>0})
            print(f"  {ym}  spend=${spend:>7.2f}  serving-days={days:>2d}  $/day={spend/max(days,1):>6.2f}  "
                  f"budget-lost={b*100:>6.2f}%  rank-lost={k*100:>6.2f}%  reported-SIS={s*100:>6.2f}%  "
                  f"ratio budget:rank = {b/k if k else float('inf'):.2f}:1")

print()
print('  READ: in Jul 2025 the campaign was mostly losing to RANK (70.35% rank vs 17.62% budget).')
print('        By Jul/Aug 2026 that inverted completely - budget is now ~7x to ~12x the rank loss.')
