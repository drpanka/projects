import json, csv, collections, datetime, os
D='/home/user/projects/data/supermetrics-archive-2026-09-08'; os.chdir(D)

j=json.load(open('raw-hour-daily.json'))['data']
F=j['requested_field_ids']; ROWS=j['data'][1:]
I={n:i for i,n in enumerate(F)}
def n(v): return 0 if v is None else v

# live schedule read from the campaign resource (verified this session)
SCHED={0:(8,20),1:(7,20),2:(7,20),3:(7,20),4:(7,20),5:(7,20),6:(7,14)}  # python weekday(): 0=Mon..6=Sun
# remap: python .weekday() 0=Mon; schedule Mon-Fri 7-20, Sat 7-14, Sun 8-20
SCHED={0:(7,20),1:(7,20),2:(7,20),3:(7,20),4:(7,20),5:(7,14),6:(8,20)}
DOWNAME={0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}

def in_sched(d,h):
    s,e=SCHED[d.weekday()]
    return s<=h<e

LS='Leads-Search-1'
recs=[]
for r in ROWS:
    d=datetime.date.fromisoformat(r[I['Date']])
    h=int(r[I['Hour']])
    recs.append(dict(date=d,hour=h,dow=d.weekday(),camp=r[I['Campaignname']],
                     imp=n(r[I['Impressions']]),clk=n(r[I['Clicks']]),
                     cost=n(r[I['Cost']]),conv=n(r[I['Conversions']]),
                     insched=in_sched(d,h)))

TODAY=datetime.date(2026,9,8)
D60=TODAY-datetime.timedelta(days=59)   # 60-day window inclusive

print('=== WHEN DID THE AD SCHEDULE ACTUALLY TAKE EFFECT? (Leads-Search-1) ===')
byday=collections.defaultdict(list)
for r in recs:
    if r['camp']==LS and r['imp']>0: byday[r['date']].append(r['hour'])
for d in sorted(byday):
    if d>=datetime.date(2026,8,1):
        hs=sorted(byday[d]); s,e=SCHED[d.weekday()]
        off=[h for h in hs if not in_sched(d,h)]
        print(' %s %-9s served %02d-%02d  sched %02d-%02d  OFF:%s'%(
            d,DOWNAME[d.weekday()],min(hs),max(hs),s,e,off if off else '-'))

def summarize(label,pred):
    sel=[r for r in recs if pred(r)]
    tot=lambda k,f=lambda r:True: sum(r[k] for r in sel if f(r))
    off=lambda r: not r['insched']
    print('\n--- %s ---'%label)
    print(' total   imp=%6d clk=%4d cost=$%8.2f conv=%6.2f'%(tot('imp'),tot('clk'),tot('cost'),tot('conv')))
    print(' OFF-SCH imp=%6d clk=%4d cost=$%8.2f conv=%6.2f'%(tot('imp',off),tot('clk',off),tot('cost',off),tot('conv',off)))
    return sel

summarize('Leads-Search-1, Mondays, last 60d (2026-07-11..2026-09-08)',
          lambda r:r['camp']==LS and r['dow']==0 and D60<=r['date']<=TODAY)
summarize('Leads-Search-1, Mondays, since schedule went live 2026-08-17',
          lambda r:r['camp']==LS and r['dow']==0 and r['date']>=datetime.date(2026,8,17))
summarize('Leads-Search-1, ALL days, last 60d',
          lambda r:r['camp']==LS and D60<=r['date']<=TODAY)
summarize('Leads-Search-1, ALL days, since 2026-08-17',
          lambda r:r['camp']==LS and r['date']>=datetime.date(2026,8,17))
summarize('Leads-Search-1, ALL days, all time',
          lambda r:r['camp']==LS)

# ---------------- CSV ----------------
def block(scope,pred):
    agg=collections.OrderedDict()
    for r in recs:
        if not pred(r): continue
        k=(DOWNAME[r['dow']],r['hour'])
        a=agg.setdefault(k,[0,0,0.0,0.0])
        a[0]+=r['imp']; a[1]+=r['clk']; a[2]+=r['cost']; a[3]+=r['conv']
    out=[]
    for (dn,h),(imp,clk,cost,conv) in sorted(agg.items(),
            key=lambda kv:(list(DOWNAME.values()).index(kv[0][0]),kv[0][1])):
        wd=list(DOWNAME.values()).index(dn); s,e=SCHED[wd]
        out.append([scope,dn,'%02d'%h,'yes' if s<=h<e else 'NO','%02d:00-%02d:00'%(s,e),
                    imp,clk,round(cost,4),round(conv,2)])
    return out

rows=[]
rows+=block('LeadsSearch1_mondays_last60d',
            lambda r:r['camp']==LS and r['dow']==0 and D60<=r['date']<=TODAY)
rows+=block('LeadsSearch1_mondays_since_schedule_2026-08-17',
            lambda r:r['camp']==LS and r['dow']==0 and r['date']>=datetime.date(2026,8,17))
rows+=block('LeadsSearch1_alldays_last60d',
            lambda r:r['camp']==LS and D60<=r['date']<=TODAY)
rows+=block('LeadsSearch1_alldays_since_schedule_2026-08-17',
            lambda r:r['camp']==LS and r['date']>=datetime.date(2026,8,17))
rows+=block('LeadsSearch1_alldays_alltime',lambda r:r['camp']==LS)
rows+=block('AllCampaigns_alldays_alltime',lambda r:True)

hdr=['scope','day_of_week','hour','within_ad_schedule','scheduled_window',
     'Impressions','Clicks','Cost','Conversions']
with open('ads-offschedule-check.csv','w',newline='') as fh:
    w=csv.writer(fh); w.writerow(hdr); w.writerows(rows)
print('\nwrote ads-offschedule-check.csv  %d rows'%len(rows))

# Monday off-schedule hour detail for the notes
print('\n=== Monday OFF-SCHEDULE hours, Leads-Search-1, last 60 days ===')
any_off=False
for r in block('x',lambda r:r['camp']==LS and r['dow']==0 and D60<=r['date']<=TODAY):
    if r[3]=='NO' and (r[5] or r[6] or r[7]):
        any_off=True; print('  hour %s  imp=%d clk=%d cost=$%.2f conv=%.2f'%(r[2],r[5],r[6],r[7],r[8]))
if not any_off: print('  none')
