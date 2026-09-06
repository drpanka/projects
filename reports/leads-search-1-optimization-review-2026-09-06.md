# Leads-Search-1 optimization review

Date: 2026-09-06. Source: Supermetrics (Google Ads account 7473953248, GA4 property PNH2 353828960). Window: last 90 days unless noted. Timezone: America/Chicago.

## Bottom line

The campaign is buying cheap visits to the scheduling page, but the number Google Ads reports as "conversions" is a page load, counted twice. Booking-level evidence is thin: GA4 attributes 4 Acuity bookings and 25 contact-form leads to paid search on $1,372 of spend. The campaign is also throttled hard: it loses 82 to 90 percent of eligible impressions to budget. The two fixes that matter most cost nothing: repoint the primary conversion goals at bookings and contact leads, and stop broad match from spending a third of the budget on off-target queries.

## Campaign snapshot

| Metric (90 days) | Value |
|---|---|
| Impressions | 12,871 |
| Clicks | 663 |
| Cost | $1,371.81 |
| CTR | 5.2% |
| Avg CPC | $2.07 |
| Ads-reported conversions | 69 (cost/conv $19.88) |
| Search impression share | 10% |
| Lost IS to budget | 82 to 90% |
| Lost IS to rank | 7 to 12% |

Settings: Search only, search partners on, Manual CPC, $10/day (spend ran $25 to $36/day in early August, so the budget was cut around Aug 20 and edited again Sept 5). Geo: 22-mile radius around Hopkins plus six geo targets, presence-only. Ad schedule: Mon to Fri 7:00 to 20:00, Sat 7:00 to 14:00, Sun 8:00 to 20:00. About 460 campaign negatives.

Weekly trend since July: spend fell from about $220 to $240 per week (16 and 6 conversions) to $67 to $88 per week (1 conversion each). Conversion rate also fell: July 14.9%, August 7.0%, September 2.5%.

## What "conversions" actually are

Primary conversion actions counted in the 69:

| Action | Type | 90-day count |
|---|---|---|
| Begin checkout (page load /schedule-an-appointment) | page load, many per click | 18 |
| PNH2 (web) schedule_appointment | GA4 event, fires on the same page | 50 |
| PNH2 (web) purchase (Acuity booking) | GA4 purchase | 1 |
| Intro Call Click, Lead form Submit, Calls from ads | | 0 |

Both of the first two count the same page view. Neither is a booking.

GA4 funnel for google / cpc, last 90 days:

| Step | Sessions |
|---|---|
| Sessions | 700 |
| Reached /schedule-an-appointment | 83 |
| Contact form submitted (generate_lead on /contact) | 25 |
| Acuity booking (purchase on /schedule/0081d9d2/...) | 4 |

Real economics: about $47 per contact-form lead and about $343 per attributed booking. The contact-form lead is not imported into Google Ads at all.

Note: GA4 shows 8 purchases with source "ads.google.com / referral". Those are clicks from inside the Ads interface (previews or final URL checks), not customers. Exclude them from any booking count.

## Where the money goes

Search terms (Google shows terms for $672 of the $1,372):

| Bucket | Share of visible spend |
|---|---|
| On-target (naturopath, functional, hormone, pediatric, etc.) | 45% |
| Off-target (ED, prostate, birth control, primary care, pediatrician near me, institutions, symptom questions) | 37% |
| Other / ambiguous | 17% |

Off-target share by ad group: Men's Health 88%, Pediatrics 75%, Functional 37%, Women's 30%, Core 23%, Geo 6%.

Ad groups:

| Ad group | Cost | Conv (page loads) | Cost/conv |
|---|---|---|---|
| Functional & Integrative Medicine | $512 | 17 | $30.10 |
| Women's Health & Hormones | $452 | 20 | $22.61 |
| Naturopath Near Me - Core | $122 | 10 | $12.18 |
| Geo-Qualified | $113 | 8.5 | $13.28 |
| Pediatrics | $88 | 7 | $12.58 |
| Men's Health | $61 | 6.5 | $9.43 |

Men's Health looks cheapest, but its "conversions" come from queries like "erectile dysfunction treatment". That is the clearest case where booking data is needed before trusting the number.

Keywords with $10+ spend and zero conversions: functional medicine for hormones ($42), naturopaths in my area ($24), female naturopath ($23), functional integrative doctor ($14), naturopath for hormones ($11), integrative medicine doctors in my area ($17, top-of-page CPC $29.55). Removed keywords already cleaned up another $100 or so.

Starved winners: "naturopathic doctor near me" exact has a 23% CTR and only 52 impressions (12% impression share). Broad keywords consume the budget before exact ones get to serve.

Devices: mobile is 80% of spend at $22.03 per conversion; desktop $14.61.

Search partners: 12% of spend at $10.01 per conversion versus $22.85 on Google search. Leave partners on.

Day of week: Friday $55.03 per conversion (4 on $220), Sunday $31.93; Saturday $12.41, Tuesday $13.59, Wednesday $15.02.

Hour: 10:00 to 17:00 is 56% of spend at $20 to $81 per conversion; 06:00 to 09:00 runs $10 to $16; 18:00 to 19:00 runs $8 to $11.

Geo: Minneapolis $344 for 17.5 conversions. Zero-conversion cities with $25+: Little Canada $45, Maple Grove $37, Shakopee $33, Bloomington $27, Eagan $25. Hopkins itself: $17, 98 impressions.

Ads: Men's Health enabled RSA is rated Poor; the paused Men's RSA had a 15.5% CTR versus 6.4%. Women's, Core and Pediatrics RSAs are Average. Functional and Core keywords land on the homepage; several quality scores are 4 to 6 with "below average" ad relevance.

Landing pages (GA4, google / cpc): homepage 70% engaged, women's 60%, pediatrics 61%, /mens-health 33% engaged with a 67% bounce rate.

## Optimizations, ranked

Order: highest impact and easiest first, hardest and lowest payoff last.

### Tier 1: do now, under an hour each

1. Fix conversion goals. Set "PNH2 (web) purchase" as primary. Mark "generate_lead" as a key event in GA4, import it, set primary. Demote "Begin checkout (page load)" and "PNH2 (web) schedule_appointment" to secondary. Everything downstream (bidding, budget, the Acuity comparison) depends on this.
2. Cut off-target queries. Add negatives for the ED and prostate cluster still leaking (treatment, products, pills, cure, ncbi, uptodate), "pediatrician(s) near me", "pediatric clinic(s)", "primary care", "primary doctor(s)", "contraceptive(s)", "estrogen patches", "doctors near me", "clinic(s) near me", "test" phrases (food sensitivity test, testosterone test), and the institution names seen (HCMC, Ramsey County, Bluestone, Oak Street, MNGI, M Health). Better still, convert every Men's Health keyword from broad to phrase.
3. Pause the zero-conversion keywords listed above. Frees about $100 per quarter of budget for terms that convert.
4. Bid adjustments (Manual CPC allows these): Friday -30%, Sunday -20%; 10:00 to 17:00 -20%; 06:00 to 09:00 and 18:00 to 20:00 +15%; mobile -15%; Little Canada, Maple Grove, Shakopee, Bloomington, Eagan -30% (or shrink the radius from 22 to about 15 miles and rely on telehealth copy for the rest).
5. Re-enable the paused Men's Health RSA and rewrite the Poor-rated one. Add a second RSA in Women's, Core and Pediatrics.
6. Restore budget to $20 to $25/day after step 1. The campaign is 85 to 90 percent budget-limited, and conversions fell almost linearly with the August cut. If cash is the constraint, keep $10 and let steps 2 to 4 concentrate it.

### Tier 2: a few hours, solid payoff

7. Restructure match types. Move core broad keywords to phrase, keep three to five broad keywords at most. Or split into two campaigns: Core (exact and phrase) at $15/day and Broad discovery at $5/day, so high-intent exact terms are never starved.
8. Close the Acuity loop for reporting (see next section).
9. Build a dedicated Functional Medicine landing page and fix /mens-health. This raises quality score, lowers rank-lost share and CPC.
10. Switch to Maximize Conversions only after step 1 and only once primary conversions exceed about 15 per month. Google's current recommendation would optimize toward page views.
11. Re-enable a brand defense campaign at $2 to $3/day (PNHdefense is paused).

### Tier 3: harder, lower or slower payoff

12. Offline conversion import from Acuity by email (enhanced conversions for leads) so Google can bid toward bookings, not page views. Requires enabling enhanced conversions and a scheduled Google Sheets upload.
13. Call tracking. "Calls from ads" logged 1 in 90 days and Clicks to call 1. CallRail has a Supermetrics connector if calls turn out to matter.
14. Retry Performance Max or broad match with target CPA, but only after three months of booking-level conversion data.
15. RSA pinning experiments, sitelink and image refresh. Marginal at this budget.

## Getting Acuity data into the picture

What already exists: the scheduler runs on the site's own domain under /schedule/0081d9d2/, so GA4 already records Acuity bookings as purchase events with the paid-search session attached. "PNH2 (web) purchase" is already imported into Google Ads. Google Ads shows 1 and GA4 shows 4 because of attribution window and modeling differences, plus the 8 self-referral test bookings noted above.

Steps:

1. Acuity, 30 minutes. Export appointments for the last 90 days (date, appointment type, new versus returning, paid amount, email). Add an intake question "How did you hear about us?" with a "Google ad" option.
2. Google Sheets, 30 minutes. Paste the export into a sheet with one row per booking. Authorize the Google Sheets connector in Supermetrics (currently not connected). Bookings can then be joined by week to Ads spend to produce cost per new patient, which is the number that confirms or refutes the campaign.
3. Google Ads, 1 to 2 hours (Tier 3 item 12). Turn on enhanced conversions for leads, then schedule a Google Sheets import of bookings keyed by email and booking time. This lets Google optimize toward real bookings.

## Data caveats

Google hides low-volume search terms, so the term-level analysis covers 49 percent of spend. Conversion counts per keyword and city are small; treat single-digit differences as directional. The site could not be fetched from this environment, so the Acuity embed was inferred from GA4 page paths rather than page source.
