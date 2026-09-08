#!/usr/bin/env python3
"""Build master-monthly-channel-table.csv from the archive CSVs.

Reads only files already on disk in this directory. No API calls.
Blank cell = data does not exist. 0 = a measured zero.
"""
import csv, os, collections

D = os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(D, n)


def rows(name):
    with open(P(name), newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


def num(v):
    if v is None:
        return None
    v = v.strip()
    if v == '' or v.upper() == 'NO_DATA':
        return None
    try:
        return float(v)
    except ValueError:
        return None


def fmt(v, dp=None):
    if v is None:
        return ''
    if dp is None:
        return str(int(round(v))) if abs(v - round(v)) < 1e-9 else repr(v)
    return f'{v:.{dp}f}'


# ---------------------------------------------------------------- Google Ads
ads = collections.defaultdict(lambda: dict(cost=0.0, imp=0.0, clk=0.0, conv=0.0, campaigns=set()))
for x in rows('ads-campaign-monthly.csv'):
    m = x['Yearmonth']
    a = ads[m]
    a['cost'] += num(x['Cost']) or 0.0
    a['imp'] += num(x['Impressions']) or 0.0
    a['clk'] += num(x['Clicks']) or 0.0
    a['conv'] += num(x['Conversions']) or 0.0
    a['campaigns'].add(x['Campaignname'])

# sanity check against the account-level file
acct = {x['Yearmonth']: x for x in rows('ads-account-monthly.csv')}
for m, a in ads.items():
    ref = acct.get(m)
    if not ref:
        print(f'WARN no account row for {m}')
        continue
    for key, col in (('cost', 'Cost'), ('imp', 'Impressions'), ('clk', 'Clicks')):
        got, want = a[key], num(ref[col]) or 0.0
        if abs(got - want) > 0.02:
            print(f'MISMATCH {m} {col}: campaign-sum {got} vs account {want}')

# like-for-like conversions / CPA
lfl = collections.defaultdict(lambda: dict(conv=0.0, cost=0.0, regimes=set(), any=False))
# Leads-Search-1 only: the one campaign that runs continuously across the whole history.
# Blending Performance Max "Campaign #1" into a CPA is meaningless because its conversions
# were page-view actions counted in the thousands.
lfl_s = collections.defaultdict(lambda: dict(conv=0.0, cost=0.0, any=False))
for x in rows('ads-cpa-like-for-like-monthly.csv'):
    m = x['Yearmonth']
    v = num(x['LFL_begin_checkout_all_conversions_clickdate'])
    l = lfl[m]
    l['regimes'].add(x['counting_regime'])
    if v is not None:
        l['conv'] += v
        l['any'] = True
    l['cost'] += num(x['Cost']) or 0.0
    if x['Campaignname'] == 'Leads-Search-1':
        t = lfl_s[m]
        t['cost'] += num(x['Cost']) or 0.0
        if v is not None:
            t['conv'] += v
            t['any'] = True

# ------------------------------------------------------------------- GA4
def channel(sm):
    sm = sm.strip()
    if sm == '(direct) / (none)':
        return 'direct'
    med = sm.split(' / ')[-1].strip().lower() if ' / ' in sm else ''
    if med in ('cpc', 'ppc', 'paid_search'):
        return 'paid_search'
    if med == 'organic':
        return 'organic'
    if med == 'referral':
        return 'referral'
    return 'other'


ga4 = collections.defaultdict(lambda: collections.Counter())
for x in rows('ga4-events-by-source-monthly.csv'):
    if x['eventName'] != 'session_start':
        continue
    s = num(x['sessions'])
    if s is None:
        continue
    m = x['yearMonth']
    ga4[m]['total'] += s
    ga4[m][channel(x['sessionSourceMedium'])] += s

pur = collections.defaultdict(lambda: collections.Counter())
for x in rows('ga4-purchases-monthly.csv'):
    m = x['yearMonth']
    c = num(x['eventCount']) or 0.0
    pur[m]['total'] += c
    if x['sessionSourceMedium'].strip() == 'google / cpc':
        pur[m]['cpc'] += c

# ------------------------------------------------------- Google Business Profile
gbp = {x['yearMonth']: x for x in rows('gmb-monthly-metrics.csv')}

# ------------------------------------------------------------------ notes
REGIME_SHORT = {
    'A': 'conv-regime A (Begin checkout + 3 page-view actions primary)',
    'B': 'conv-regime B (Begin checkout + 2 bio pages + /whypnh primary)',
    'D': 'conv-regime D (Begin checkout primary only)',
    'E': 'conv-regime E (GA4 schedule_appointment + purchase primary; Begin checkout secondary)',
}
PMAX = {'2025|06', '2025|07', '2025|08'}
PRIOR_PAID = {'2023|03','2023|04','2023|05','2023|06','2023|07','2023|08','2023|09',
              '2024|02','2024|03','2024|04','2024|05','2024|06','2024|07','2024|08',
              '2024|09','2024|10','2024|11','2024|12','2025|01','2025|02','2025|03'}
DARK = {'2025|10', '2025|11', '2025|12', '2026|01', '2026|02', '2026|03'}
TAGASSIST = {'2025|06', '2026|04', '2026|05', '2026|06'}
ADSREF = {'2026|06', '2026|07', '2026|08'}


SPAM = {'2024|02': 'news.grets.store + static.seders.website + rida.tokyo',
        '2024|03': 'rida.tokyo',
        '2025|10': 'wake-up-network.com'}


def note_for(m, has_ads):
    n = []
    if m < '2025|06':
        n.append('no spend data: Google Ads account 7473953248 has no delivery before 2025-06')
    if m in PRIOR_PAID:
        n.append('GA4 shows google/cpc sessions with NO matching spend in this Ads account - paid search ran from an account not in this archive; cost and clicks for it are unrecoverable')
    if m in PMAX:
        n.append('Ads totals include Performance Max "Campaign #1"; its conversions were page-view actions in the thousands, so use the Leads-Search-1-only columns for any CPA')
    if m == '2025|09':
        n.append('Ads went dark 2025-08-27: campaign enabled but zero impressions all month; the 5 conversions Google shows for Sep 2025 are conversion-date spillover from August clicks, which is why click-date conversions here are 0')
    if m in DARK:
        n.append('DARK PERIOD: zero Ads delivery account-wide, verified zero spend not a reporting gap')
    if m == '2026|04':
        n.append('Ads restarted 2026-04-27; month is 4 serving days only')
    reg = lfl.get(m, {}).get('regimes') or set()
    for r in sorted(reg):
        if r.startswith('D->E'):
            n.append('SPLICE 2026-07-12: Begin checkout counted Jul 1-11 only, GA4 schedule_appointment Jul 13-31 only; as-reported conversions for this month are two partial months of two different metrics')
        else:
            n.append(REGIME_SHORT.get(r[0], r))
    if not reg and has_ads:
        n.append('no like-for-like conversion basis available')
    # what a GA4 "purchase" event actually means changes over the history
    if m < '2024|12':
        n.append('GA4 purchase events in this month are Squarespace store orders and unattributed events, NOT appointment bookings')
    elif m < '2026|06':
        n.append('GA4 purchase is a mix of Acuity scheduler pages and Squarespace store orders; not a clean booking count')
    else:
        n.append('GA4 purchase is predominantly Acuity scheduler; still overcounts real bookings by roughly 45% because one booking can fire up to three events')
    if m in SPAM:
        n.append('GA4 referral sessions inflated by bot/spam referrers (' + SPAM[m] + '); subtract before reading the referral column')
    if m in TAGASSIST:
        n.append('GA4 polluted by tagassistant.google.com self-referral (operator tag tests)')
    if m in ADSREF:
        n.append('GA4 polluted by ads.google.com self-referral (operator ad-preview clicks)')
    if m < '2025|03':
        n.append('Business Profile: no data, connector cannot reach before 2025-03-08')
    if m == '2025|03':
        n.append('Business Profile month partial: starts 2025-03-08')
    if m == '2026|09':
        n.append('PARTIAL MONTH: Ads/GA4 through 2026-09-08; Business Profile views populated only through 2026-09-04 and all action metrics still lagging, so left blank')
    return '; '.join(n)


# ------------------------------------------------------------------ assemble
months = sorted(set(ga4) | set(ads) | set(gbp) | set(pur) | DARK)

HEAD = ['month',
        'ads_spend_usd', 'ads_impressions', 'ads_clicks', 'ads_avg_cpc_usd',
        'ads_conversions_as_reported', 'ads_conversions_like_for_like', 'ads_cpa_like_for_like_usd',
        'ads_spend_search_campaign_usd', 'ads_conversions_lfl_search_campaign',
        'ads_cpa_lfl_search_campaign_usd',
        'ga4_sessions_total', 'ga4_sessions_paid_search', 'ga4_sessions_organic',
        'ga4_sessions_direct', 'ga4_sessions_referral',
        'ga4_purchase_events_total', 'ga4_purchase_events_google_cpc',
        'gbp_profile_views', 'gbp_actions_total', 'gbp_website_clicks',
        'gbp_direction_requests', 'gbp_phone_calls', 'gbp_bookings',
        'data_quality_note']

out = []
for m in months:
    row = {'month': m.replace('|', '-')}

    # --- ads
    has_ads = m in ads
    if has_ads:
        a = ads[m]
        row['ads_spend_usd'] = fmt(a['cost'], 2)
        row['ads_impressions'] = fmt(a['imp'])
        row['ads_clicks'] = fmt(a['clk'])
        row['ads_avg_cpc_usd'] = fmt(a['cost'] / a['clk'], 2) if a['clk'] else ''
        row['ads_conversions_as_reported'] = fmt(a['conv'], 2)
    elif m in DARK:
        # verified zero delivery, not missing data
        row['ads_spend_usd'] = '0.00'
        row['ads_impressions'] = '0'
        row['ads_clicks'] = '0'
        row['ads_avg_cpc_usd'] = ''
        row['ads_conversions_as_reported'] = '0'
    else:
        for k in ('ads_spend_usd', 'ads_impressions', 'ads_clicks', 'ads_avg_cpc_usd',
                  'ads_conversions_as_reported'):
            row[k] = ''

    l = lfl.get(m)
    if l and l['any']:
        row['ads_conversions_like_for_like'] = fmt(l['conv'], 2)
        row['ads_cpa_like_for_like_usd'] = fmt(l['cost'] / l['conv'], 2) if l['conv'] else ''
    elif m in DARK:
        row['ads_conversions_like_for_like'] = '0'
        row['ads_cpa_like_for_like_usd'] = ''
    else:
        row['ads_conversions_like_for_like'] = ''
        row['ads_cpa_like_for_like_usd'] = ''

    t = lfl_s.get(m)
    if t and t['any']:
        row['ads_spend_search_campaign_usd'] = fmt(t['cost'], 2)
        row['ads_conversions_lfl_search_campaign'] = fmt(t['conv'], 2)
        row['ads_cpa_lfl_search_campaign_usd'] = fmt(t['cost'] / t['conv'], 2) if t['conv'] else ''
    elif m in DARK:
        row['ads_spend_search_campaign_usd'] = '0.00'
        row['ads_conversions_lfl_search_campaign'] = '0'
        row['ads_cpa_lfl_search_campaign_usd'] = ''
    else:
        for k in ('ads_spend_search_campaign_usd', 'ads_conversions_lfl_search_campaign',
                  'ads_cpa_lfl_search_campaign_usd'):
            row[k] = ''

    # --- ga4
    g = ga4.get(m)
    if g:
        row['ga4_sessions_total'] = fmt(g['total'])
        row['ga4_sessions_paid_search'] = fmt(g['paid_search'])
        row['ga4_sessions_organic'] = fmt(g['organic'])
        row['ga4_sessions_direct'] = fmt(g['direct'])
        row['ga4_sessions_referral'] = fmt(g['referral'])
    else:
        for k in ('ga4_sessions_total', 'ga4_sessions_paid_search', 'ga4_sessions_organic',
                  'ga4_sessions_direct', 'ga4_sessions_referral'):
            row[k] = ''

    p = pur.get(m)
    if g:  # GA4 was collecting this month, so 0 purchases is a real zero
        row['ga4_purchase_events_total'] = fmt(p['total']) if p else '0'
        row['ga4_purchase_events_google_cpc'] = fmt(p['cpc']) if p else '0'
    else:
        row['ga4_purchase_events_total'] = ''
        row['ga4_purchase_events_google_cpc'] = ''

    # --- gbp
    b = gbp.get(m)
    partial_actions = (m == '2026|09')
    if b:
        row['gbp_profile_views'] = fmt(num(b['views_total']))
        if partial_actions:
            for k in ('gbp_actions_total', 'gbp_website_clicks', 'gbp_direction_requests',
                      'gbp_phone_calls', 'gbp_bookings'):
                row[k] = ''
        else:
            row['gbp_actions_total'] = fmt(num(b['actions_total']))
            row['gbp_website_clicks'] = fmt(num(b['actions_website']))
            row['gbp_direction_requests'] = fmt(num(b['actions_driving_directions']))
            row['gbp_phone_calls'] = fmt(num(b['actions_phone']))
            row['gbp_bookings'] = fmt(num(b['actions_bookings']))
    else:
        for k in ('gbp_profile_views', 'gbp_actions_total', 'gbp_website_clicks',
                  'gbp_direction_requests', 'gbp_phone_calls', 'gbp_bookings'):
            row[k] = ''

    row['data_quality_note'] = note_for(m, has_ads)
    out.append(row)

with open(P('master-monthly-channel-table.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=HEAD)
    w.writeheader()
    w.writerows(out)

print(f'wrote {len(out)} months, {months[0]} .. {months[-1]}')

# ------------------------------------------------------------------ totals
tot_cost = sum(a['cost'] for a in ads.values())
tot_clk = sum(a['clk'] for a in ads.values())
tot_imp = sum(a['imp'] for a in ads.values())
print(f'ads lifetime: ${tot_cost:.2f}, {int(tot_imp)} impr, {int(tot_clk)} clicks')
print('gbp lifetime views', sum(num(x["views_total"]) for x in rows("gmb-monthly-metrics.csv")))
print('gbp lifetime website clicks', sum(num(x["actions_website"]) for x in rows("gmb-monthly-metrics.csv")))
print('gbp lifetime bookings', sum(num(x["actions_bookings"]) for x in rows("gmb-monthly-metrics.csv")))
print('ga4 purchase lifetime', sum(c["total"] for c in pur.values()))
