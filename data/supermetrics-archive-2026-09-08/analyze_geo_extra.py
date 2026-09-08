import json,csv,collections,datetime,os
D='/home/user/projects/data/supermetrics-archive-2026-09-08'; os.chdir(D)
def n(v): return 0 if v is None else v
def load(p):
    j=json.load(open(p))['data']; return {x:i for i,x in enumerate(j['requested_field_ids'])}, j['data'][1:]

print('='*72); print('SERVING DATE RANGES / GAPS per campaign (from hourly file)'); print('='*72)
I,R=load('raw-hour-daily.json')
days=collections.defaultdict(set)
for r in R: days[r[I['Campaignname']]].add(r[I['Date']])
for c in sorted(days):
    ds=sorted(days[c]); print('\n %s: %d serving days, %s .. %s'%(c,len(ds),ds[0],ds[-1]))
    gaps=[]; 
    for a,b in zip(ds,ds[1:]):
        da,db=datetime.date.fromisoformat(a),datetime.date.fromisoformat(b)
        if (db-da).days>1: gaps.append((a,b,(db-da).days-1))
    for a,b,g in gaps:
        if g>=3: print('    GAP %3d days: %s -> %s'%(g,a,b))

print()
print('='*72); print('PER-CAMPAIGN: cities with lifetime spend >$20 and ZERO conversions'); print('='*72)
for lbl,src in [('GEOGRAPHIC(default)','raw-geo-monthly-default.json'),('USER LOCATION','raw-geo-monthly-userlocation.json')]:
    I,R=load(src)
    agg=collections.defaultdict(lambda:[0,0,0.0,0.0])
    for r in R:
        k=(r[I['Campaignname']],r[I['City']],r[I['Region']])
        a=agg[k]; a[0]+=n(r[I['Impressions']]); a[1]+=n(r[I['Clicks']]); a[2]+=n(r[I['Cost']]); a[3]+=n(r[I['Conversions']])
    print('\n %s:'%lbl)
    hits=[(v[2],k,v) for k,v in agg.items() if v[2]>20 and v[3]==0]
    if not hits: print('   (none)')
    for cost,k,v in sorted(hits,reverse=True):
        print('   %-34s %-20s %-12s $%7.2f imp=%5d clk=%3d'%(k[0],k[1],k[2],cost,v[0],v[1]))
    print('   subtotal $%.2f across %d campaign-cities'%(sum(h[0] for h in hits),len(hits)))

print()
print('='*72); print('OUT-OF-FOOTPRINT SERVING (USER LOCATION view = physical presence)'); print('='*72)
I,R=load('raw-geo-monthly-userlocation.json')
agg=collections.defaultdict(lambda:[0,0,0.0,0.0])
for r in R:
    reg=r[I['Region']]; ctry=r[I['Country']]; camp=r[I['Campaignname']]
    if ctry!='United States': bucket='NON-US'
    elif reg in ('Minnesota','Wisconsin'): bucket='MN/WI (in footprint)'
    else: bucket='US, outside MN/WI'
    a=agg[(camp,bucket)]
    a[0]+=n(r[I['Impressions']]); a[1]+=n(r[I['Clicks']]); a[2]+=n(r[I['Cost']]); a[3]+=n(r[I['Conversions']])
for camp in sorted({k[0] for k in agg}):
    tot=sum(agg[k][0] for k in agg if k[0]==camp)
    totc=sum(agg[k][2] for k in agg if k[0]==camp)
    print('\n %s  (lifetime imp=%d cost=$%.2f)'%(camp,tot,totc))
    for b in ['MN/WI (in footprint)','US, outside MN/WI','NON-US']:
        v=agg.get((camp,b))
        if not v: continue
        print('   %-22s imp=%6d (%5.2f%%) clk=%4d cost=$%8.2f (%5.2f%%) conv=%7.2f'%(
            b,v[0],100*v[0]/tot if tot else 0,v[1],v[2],100*v[2]/totc if totc else 0,v[3]))

print()
print('='*72); print('LEADS-SEARCH-1 off-schedule totals, split by era'); print('='*72)
I,R=load('raw-hour-daily.json')
SCHED={0:(7,20),1:(7,20),2:(7,20),3:(7,20),4:(7,20),5:(7,14),6:(8,20)}
eras=collections.defaultdict(lambda:[0,0,0.0,0.0,0,0,0.0,0.0])
for r in R:
    if r[I['Campaignname']]!='Leads-Search-1': continue
    d=datetime.date.fromisoformat(r[I['Date']]); h=int(r[I['Hour']])
    s,e=SCHED[d.weekday()]; off=not(s<=h<e)
    era='B. schedule live (2026-08-18 onward)' if d>=datetime.date(2026,8,18) else 'A. before schedule (<=2026-08-17)'
    a=eras[era]
    imp,clk,cost,conv=n(r[I['Impressions']]),n(r[I['Clicks']]),n(r[I['Cost']]),n(r[I['Conversions']])
    if off: a[0]+=imp;a[1]+=clk;a[2]+=cost;a[3]+=conv
    a[4]+=imp;a[5]+=clk;a[6]+=cost;a[7]+=conv
for k in sorted(eras):
    a=eras[k]
    print(' %s\n   off-schedule imp=%5d clk=%4d cost=$%8.2f conv=%6.2f   (%.2f%% of era spend)\n   era total    imp=%5d clk=%4d cost=$%8.2f conv=%6.2f'%(
        k,a[0],a[1],a[2],a[3],100*a[2]/a[6] if a[6] else 0,a[4],a[5],a[6],a[7]))

# all-time Monday off-schedule
mon=[0,0,0.0,0.0]
for r in R:
    if r[I['Campaignname']]!='Leads-Search-1': continue
    d=datetime.date.fromisoformat(r[I['Date']]); h=int(r[I['Hour']])
    if d.weekday()!=0: continue
    if not (7<=h<20):
        mon[0]+=n(r[I['Impressions']]);mon[1]+=n(r[I['Clicks']]);mon[2]+=n(r[I['Cost']]);mon[3]+=n(r[I['Conversions']])
print('\n MONDAY off-schedule, all time: imp=%d clk=%d cost=$%.2f conv=%.2f'%tuple(mon))

print()
print('='*72); print('HOUR-OF-DAY profile, Leads-Search-1 lifetime (all days)'); print('='*72)
hr=collections.defaultdict(lambda:[0,0,0.0,0.0])
for r in R:
    if r[I['Campaignname']]!='Leads-Search-1': continue
    a=hr[r[I['Hour']]]
    a[0]+=n(r[I['Impressions']]);a[1]+=n(r[I['Clicks']]);a[2]+=n(r[I['Cost']]);a[3]+=n(r[I['Conversions']])
for h in sorted(hr):
    a=hr[h]
    print('   %s  imp=%5d clk=%4d $%8.2f ctr=%5.2f%% conv=%6.2f cpa=%s'%(
        h,a[0],a[1],a[2],100*a[1]/a[0] if a[0] else 0,a[3],'$%.2f'%(a[2]/a[3]) if a[3] else 'n/a'))
