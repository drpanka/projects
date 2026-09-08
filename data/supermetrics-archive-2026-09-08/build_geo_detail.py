import json,csv,collections,os
D='/home/user/projects/data/supermetrics-archive-2026-09-08'; os.chdir(D)
def n(v): return 0 if v is None else v
def load(p):
    j=json.load(open(p))['data']; return {x:i for i,x in enumerate(j['requested_field_ids'])}, j['data'][1:], j['requested_field_ids']
def rat(a,b): return round(a/b,6) if b else ''
MET=['Impressions','Clicks','Cost','Ctr','Conversions','CostPerConversion']
def emit(agg,keys):
    out=[]
    for k,(i,c,co,cv) in agg.items():
        out.append(list(k)+[i,c,round(co,4),rat(c,i),round(cv,2),(round(co/cv,4) if cv else '')])
    return out
def write(path,hdr,rows):
    with open(path,'w',newline='') as fh:
        w=csv.writer(fh); w.writerow(hdr)
        for r in rows: w.writerow(['' if v is None else v for v in r])
    print('wrote %-46s %5d rows'%(path,len(rows)))

# ---- location target view ----
I,R,F=load('raw-locationview-daily.json')
write('ads-geo-locationtarget-daily.csv',F,sorted(R,key=lambda r:(r[I['Date']],r[I['Campaignname']],str(r[I['Location']]))))
agg=collections.OrderedDict()
for r in R:
    k=(r[I['Campaignname']],r[I['CampaignID']],r[I['Location']],r[I['LocationType']])
    a=agg.setdefault(k,[0,0,0.0,0.0])
    a[0]+=n(r[I['Impressions']]);a[1]+=n(r[I['Clicks']]);a[2]+=n(r[I['Cost']]);a[3]+=n(r[I['Conversions']])
rows=emit(agg,None); rows.sort(key=lambda r:(r[0],-r[6]))
write('ads-geo-locationtarget-alltime.csv',['Campaignname','CampaignID','Location','LocationType']+MET,rows)

print('\n=== LIFETIME SPEND BY CONFIGURED LOCATION TARGET ===')
for r in rows:
    print('  %-36s %-28s %-14s imp=%6s clk=%5s $%9s conv=%7s cpa=%s'%(r[0],r[2],r[3],r[4],r[5],r[6],r[8],r[9] or 'n/a'))

# ---- geographic detail: metro / postal / location type ----
I,R,F=load('raw-geo-detail-monthly.json')
write('ads-geo-detail-monthly.csv',F,sorted(R,key=lambda r:(r[I['Yearmonth']],r[I['Campaignname']],-n(r[I['Cost']]))))

print('\n=== PHYSICAL LOCATION vs LOCATION OF INTEREST (Geographic view, lifetime) ===')
lt=collections.defaultdict(lambda:[0,0,0.0,0.0])
for r in R:
    lt[(r[I['Campaignname']],r[I['LocationType']])][0]+=n(r[I['Impressions']])
    lt[(r[I['Campaignname']],r[I['LocationType']])][1]+=n(r[I['Clicks']])
    lt[(r[I['Campaignname']],r[I['LocationType']])][2]+=n(r[I['Cost']])
    lt[(r[I['Campaignname']],r[I['LocationType']])][3]+=n(r[I['Conversions']])
for camp in sorted({k[0] for k in lt}):
    tc=sum(v[2] for k,v in lt.items() if k[0]==camp)
    print('\n %s (lifetime $%.2f)'%(camp,tc))
    for k,v in sorted(((k,v) for k,v in lt.items() if k[0]==camp),key=lambda kv:-kv[1][2]):
        print('   %-26s imp=%6d clk=%5d $%9.2f (%5.1f%%) conv=%7.2f'%(k[1],v[0],v[1],v[2],100*v[2]/tc if tc else 0,v[3]))

print('\n=== METRO AREA, lifetime, Leads-Search-1 ===')
mt=collections.defaultdict(lambda:[0,0,0.0,0.0])
for r in R:
    if r[I['Campaignname']]!='Leads-Search-1': continue
    a=mt[r[I['Metroarea']]]
    a[0]+=n(r[I['Impressions']]);a[1]+=n(r[I['Clicks']]);a[2]+=n(r[I['Cost']]);a[3]+=n(r[I['Conversions']])
for k,v in sorted(mt.items(),key=lambda kv:-kv[1][2])[:12]:
    print('   %-46s imp=%6d clk=%5d $%9.2f conv=%7.2f'%(k,v[0],v[1],v[2],v[3]))
