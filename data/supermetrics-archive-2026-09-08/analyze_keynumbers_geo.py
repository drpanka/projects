import json,csv,collections,datetime,os
D='/home/user/projects/data/supermetrics-archive-2026-09-08'; os.chdir(D)
def n(v): return 0 if v is None else v
def load(p):
    j=json.load(open(p))['data']; return {x:i for i,x in enumerate(j['requested_field_ids'])}, j['data'][1:]

print('='*70); print('RECONCILIATION: lifetime totals by source file'); print('='*70)
for lbl,p in [('hour',   'raw-hour-daily.json'),
              ('device', 'raw-device-daily.json'),
              ('network','raw-network-daily.json'),
              ('geo-default','raw-geo-monthly-default.json'),
              ('geo-userloc','raw-geo-monthly-userlocation.json')]:
    I,R=load(p)
    tot=collections.defaultdict(lambda:[0,0,0.0,0.0])
    for r in R:
        k=r[I['Campaignname']]
        t=tot[k]; t[0]+=n(r[I['Impressions']]); t[1]+=n(r[I['Clicks']]); t[2]+=n(r[I['Cost']]); t[3]+=n(r[I['Conversions']])
    print('\n %s:'%lbl)
    for k in sorted(tot):
        t=tot[k]; print('   %-38s imp=%7d clk=%5d cost=$%9.2f conv=%8.2f'%(k,t[0],t[1],t[2],t[3]))

print()
print('='*70); print('MONDAY-BY-MONDAY off-schedule detail, Leads-Search-1'); print('='*70)
I,R=load('raw-hour-daily.json')
SCHED={0:(7,20),1:(7,20),2:(7,20),3:(7,20),4:(7,20),5:(7,14),6:(8,20)}
per=collections.defaultdict(lambda:[0,0,0.0,0.0,0,0,0.0,0.0])  # off imp,clk,cost,conv | tot...
for r in R:
    if r[I['Campaignname']]!='Leads-Search-1': continue
    d=datetime.date.fromisoformat(r[I['Date']]); h=int(r[I['Hour']])
    if d.weekday()!=0: continue
    s,e=SCHED[0]; off = not (s<=h<e)
    a=per[d]
    imp,clk,cost,conv=n(r[I['Impressions']]),n(r[I['Clicks']]),n(r[I['Cost']]),n(r[I['Conversions']])
    if off: a[0]+=imp; a[1]+=clk; a[2]+=cost; a[3]+=conv
    a[4]+=imp; a[5]+=clk; a[6]+=cost; a[7]+=conv
print(' %-12s %-28s %s'%('Monday','OFF-SCHEDULE (00-06,20-23)','DAY TOTAL'))
for d in sorted(per):
    a=per[d]
    flag='  <-- LEAK' if a[0] else ''
    print(' %s  imp=%4d clk=%2d $%7.2f      imp=%4d clk=%3d $%7.2f%s'%(d,a[0],a[1],a[2],a[4],a[5],a[6],flag))

print()
print('='*70); print('CITIES: lifetime spend > $20 AND zero lifetime conversions'); print('='*70)
for lbl,f in [('GEOGRAPHIC (default) view','ads-geo-alltime.csv'),
              ('USER LOCATION view','ads-geo-userlocation-alltime.csv')]:
    print('\n %s:'%lbl)
    hits=[]
    for r in csv.DictReader(open(f)):
        cost=float(r['Cost']); conv=float(r['Conversions'])
        if cost>20 and conv==0: hits.append((cost,r))
    if not hits: print('   (none)')
    for cost,r in sorted(hits,reverse=True):
        print('   %-22s %-14s $%8.2f  imp=%5s clk=%4s conv=0'%(r['City'],r['Region'],cost,r['Impressions'],r['Clicks']))
    print('   subtotal $%.2f across %d cities'%(sum(c for c,_ in hits),len(hits)))

print()
print('='*70); print('Top cities by lifetime spend (default view)'); print('='*70)
rs=list(csv.DictReader(open('ads-geo-alltime.csv')))[:15]
for r in rs:
    conv=float(r['Conversions'])
    print('   %-22s $%8.2f  imp=%6s clk=%5s conv=%7.2f cpa=%s'%(
        r['City'],float(r['Cost']),r['Impressions'],r['Clicks'],conv,r['CostPerConversion'] or 'n/a'))

print()
print('='*70); print('DEVICE all-time'); print('='*70)
for r in csv.DictReader(open('ads-device-alltime.csv')):
    print('   %-38s %-12s imp=%6s clk=%5s $%9s ctr=%-9s conv=%8s cpa=%s'%(
        r['Campaignname'],r['Device'],r['Impressions'],r['Clicks'],r['Cost'],r['Ctr'],r['Conversions'],r['CostPerConversion'] or 'n/a'))

print()
print('='*70); print('NETWORK all-time'); print('='*70)
for r in csv.DictReader(open('ads-network-alltime.csv')):
    print('   %-38s %-16s imp=%6s clk=%5s $%9s ctr=%-9s conv=%8s'%(
        r['Campaignname'],r['Networkwithsearchpartners'],r['Impressions'],r['Clicks'],r['Cost'],r['Ctr'],r['Conversions']))
