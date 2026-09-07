# Leads-Search-1: Monday working session guide

For: Monday 2026-09-07, 10:00 Central. Campaign: Leads-Search-1 (ID 22767146837), Google Ads account 7473953248.
Data: Supermetrics pull on 2026-09-06, last 90 days (2026-06-08 to 2026-09-06) unless noted. Full findings are in `leads-search-1-optimization-review-2026-09-06.md` in this folder.

## Ground rules for this session

- Budget stays where it is. You adjust it in real time from clinician load. Nothing below touches budget.
- Bidding stays click-based. The API reports Manual CPC; you describe it as Maximize Clicks. Either way, bid adjustments (device, schedule, location) still apply, and primary versus secondary conversion status does not change delivery. Conversion changes are for your data only.
- Everything here is reversible in the Ads interface. Estimated total time: about 75 minutes.
- Every negative proposed below was checked against the 430 negatives already on the campaign and against every active keyword. None duplicates an existing negative; none blocks an active keyword.

Order of work: 1 conversion reporting decision, 2 negatives, 3 pauses, 4 match types, 5 bid adjustments, 6 ads, 7 columns and cadence, 8 Acuity intake question. Sections 2 to 7 involve no patient data of any kind.

---

## 1. Conversion reporting: decide before you touch it (5 minutes)

Today the "Conversions" column counts a page load of /schedule-an-appointment twice: once as "Begin checkout (Page load ...)" and once as "PNH2 (web) schedule_appointment". Neither is a booking, and the Acuity addendum shows that bookings cannot be attributed in Google Ads without sending scheduling events to Google, which is the compliance question you raised. So this section is now a decision, not a to-do:

- Option A, hold. Change nothing in Conversions on Monday. Ask your compliance advisor whether the scheduling-page and bio-page conversion actions, and Acuity's Google Analytics integration, should stay. Under click-based bidding none of them affect delivery.
- Option B, tidy only. If you want the column to read sensibly while you wait: Goals > Conversions > Summary > "Begin checkout (Page load ...)" > Edit settings > Secondary. That removes the double count and sends Google nothing new. Do not import additional GA4 events (the earlier draft suggested importing the contact-form event; that is withdrawn pending the same advice).
- Option C, cleanup, if the advisor says stop. Acuity > Integrations > Google Analytics > disconnect. Google Ads > Conversions > pause the two "PNH2 (web)" imports, the "Begin checkout" action, and the three "Page view" actions. Keep the Google tag on marketing pages only.

The scorecard that replaces all of this is the monthly Acuity export plus the intake question in section 8.

GA4 hygiene, 3 minutes, safe under every option: Admin > Data streams > PNH2 web stream > Configure tag settings > List unwanted referrals > add `ads.google.com` and `tagassistant.google.com`. They are your own test clicks showing up as purchase sources.

---

## 2. Negative keywords to add (15 minutes)

Your Sept 1 list already blocks 111 of the 331 clicked queries ($164). What follows are the gaps that still spent money. Add at the campaign level (Keywords > Negative keywords > + > Campaign > Leads-Search-1). Match type is in brackets; remember negatives do not match plurals or close variants, so singular and plural are listed separately where it matters.

### 2a. Prescription and conventional-only intent (NDs in Minnesota cannot prescribe; these searchers cannot be served)

| Negative | Evidence (90 days) |
|---|---|
| "contraception", "contraceptive", "contraceptives", "the pill" [phrase] | "contraceptives for females" $4.51, "best contraception for 40 year old" $1.28, "i want to go on the pill" $0.49. All from `hormone doctor near me` broad. |
| "estrogen patches", "estrogen replacement", "hormone replacement", "hormone therapy", "hrt" [phrase] | "where to get estrogen patches", "estrogen replacement options" $2.70, "female hormone therapy near me" $3.56, "weight gain and hormone replacement therapy" $2.91, "best hormone replacement therapy for women". About $12. |
| "medication", "medications" [phrase] | "natural medication for adhd" $3.61, "best thyroid medication for weight loss" $2.33. |
| "primary care", "primary doctor", "primary doctors", "primary physician", "primary physicians" [phrase] | Six "best primary doctors/physicians near me" queries, $6.90. "primary care" conflicts with the keyword `male primary care doctors near me`, which is on the pause list below; pause that keyword first. |

### 2b. Conventional specialists and clinics you are not

| Negative | Evidence |
|---|---|
| "dermatology", "dermatologist", "cardiologist", "rheumatologist", "gastroenterologist", "gi doctor", "geriatric", "allergist" [phrase] | "integrative dermatology near me" x2 $3.61, "natural cardiologist near me" $2.31, "integrative rheumatologist" $2.32, "free gi doctor near me" $3.80, "best female geriatric doctors" $2.27, "pediatric allergist" and "pediatrician allergist" $4.08. Note: allergist blocks the conventional specialty, not "kids allergies" queries. |
| "fertility clinic", "fertility clinics", "fertility treatment", "fertility treatments", "naprotechnology" [phrase] | "fertility clinic minneapolis", "fertility clinic maple grove mn", "fertility clinic near me near me", "fertility treatment options" $4.47, "fertility treatment near me", "naprotechnology doctor near me". About $15. IVF and NaPro seekers, not naturopathic fertility support. Your `natural fertility specialist` keyword is unaffected. |
| "pediatric clinic", "pediatric clinics", "pediatric office", "pediatric offices", "independent pediatrician" [phrase] | "pediatric clinic(s) near me" x2 $4.17, "pediatric offices near me" $2.09, "independent pediatrician near me" $1.88. Generic pediatrician shopping. |
| "regenerative" [phrase] | "regenerative medicine providers near me" $1.69. |
| "nurse", "public health", "specialty center" [phrase] | "enema nurse near me", "ramsey county public health center", "lakeville specialty center suite 250". |
| "testosterone test" [phrase] | "testosterone test" $4.62 (lab-shopping). Does not touch `naturopath for low testosterone` or `low testosterone natural treatment`. |

### 2c. Competitor and institution names not yet on the list

| Negative | Evidence |
|---|---|
| "hennepin clinic" [phrase] | $2.18 |
| "ways to well" [phrase] | $2.31 |
| "wholesome health" [phrase] | $1.55 |
| "south lake pediatrics" [phrase] | 4 impressions, no click yet |
| "restore hyper" [phrase] | "restore hyper wellness" 10 impressions; your existing "restore wellness" negative does not catch it because "hyper" sits between the words |

### 2d. Generic single queries, exact match only (safe: exact negatives do not touch longer keywords like `functional medicine doctors near me`)

[doctors near me], [doctor near me], [clinics near me], [clinic near me], [i need a doctor], [physicians], [chronic], [poop], [hopkins clinic], [wellness near me], [health wellness], [healthy lifestyle habits], [medical examination], [medical treatments], [men's health], [women clinic near me], [women's clinic near me], [top rated doctors near me], [finding a doctor near me], [non traditional doctors near me], [free children clinic near me], [low acth], [games day men's health near me], [pediatrician near me], [pediatricians near me]

Evidence: "hopkins clinic" $8.52 for one click, "chronic" $8.14 for one click, the rest $0.60 to $3.25 each. Together about $35 with 3 page-load conversions and no visible booking.

### 2e. Informational modifiers

| Negative | Evidence |
|---|---|
| "treatment options", "treatment for", "treatments for" [phrase] | "menopause treatment options" x2, "natural treatment for inflammation", "holistic treatment for high blood pressure", "natural treatments for gad", "treatment for prostate". Do not add the bare word "treatment": it would block your own `enlarged prostate natural treatment`, `low testosterone natural treatment` and `natural prostate treatment near me`. |
| "signs of", "products", "diet", "habits" [phrase] | "signs of early menopause", "longevity products", "hormone balance diet", "heather stone diet", "healthy lifestyle habits". |
| "sex drive", "kegel", "lump" [phrase] | "estrogen and sex drive", "kegel exercises for frequent urination", "lump in neck thyroid". |
| "para", "medico", "médico", "chequeo" [phrase] | Spanish queries still leaking past "clinica", "ginecologo", "cerca de mi": "chequeo médico general para mujeres" $1.32. |

### 2f. Judgment calls (your decision; not added to the count above)

- "vaccine", "vaccines", "anti vax": "anti vax pediatricians near me" and "pediatricians near me that don t require vaccines" (one page-load conversion). Decide based on whether you want that conversation.
- "weight loss": "naturopath for weight loss near me" and "ideal health and weight". Block only if weight loss is not a service you want to sell from ads.
- "mental health": "naturopathic doctor specializing in mental health". Same logic.
- "online": "medicine and doctors online". You do offer telehealth, so leave it unless it keeps spending.

Expected effect: the visible leakage these close is about $110 per quarter at current spend, roughly 8 percent of budget, plus whatever the hidden low-volume terms share. More important, the match-type changes in step 4 close the structural leak that produces new junk every week.

---

## 3. Keywords to pause (10 minutes)

All figures are 90-day, enabled keywords only. Conversions here are page loads, not bookings.

### Women's Health & Hormones

| Keyword | Match | Cost | Clicks | Conv | Why |
|---|---|---|---|---|---|
| functional medicine for hormones | Broad | $42.00 | 18 | 0 | Highest zero-result spend in the campaign. Matched menopause treatment options, GLP-1, thyroid medication for weight loss, "dutch complete", "hashimoto's". |
| female naturopath | Broad | $23.15 | 9 | 0 | Matched hot flashes at night, menopause treatment, holistic osteoporosis. `female naturopath near me` (kept) covers the real intent. |
| naturopath for hormones | Broad | $11.28 | 5 | 0 | Matched female hormone therapy, estrogen and sex drive, premenopausal symptoms. `naturopath for hormone imbalance` (kept, 2 conv) is the better version. |
| functional medicine hormones | Broad | $7.59 | 5 | 0 | Matched estrogen after 65, weight gain and HRT. Duplicate of the first row. |

### Functional & Integrative Medicine

| Keyword | Match | Cost | Clicks | Conv | Why |
|---|---|---|---|---|---|
| integrative medicine doctors in my area | Broad | $16.81 | 8 | 0.02 | Top-of-page CPC is $29.55, the most expensive auction in the campaign, for "finding a doctor near me" and "integrative dermatology". |
| functional integrative doctor | Broad | $14.44 | 9 | 0 | Matched "best primary doctors near me", "wholesome health". |
| functional doctor in my area | Broad | $10.25 | 7 | 1 | Matched best primary doctors, fibromyalgia doctor, nrt testing, "medical treatments". |
| functional medicine doctors in my area | Broad | $7.23 | 3 | 0 | Matched "free gi doctor near me". |
| functional medicine practitioner in my area | Broad | 0 impressions | | | Same "in my area" pattern; pause before it starts. |

Pattern: every "in my area" keyword is a broad-match duplicate of a "near me" keyword you already run, and Google reads "in my area" as generic doctor shopping. The "near me" versions stay.

### Naturopath Near Me - Core

| Keyword | Match | Cost | Clicks | Conv | Why |
|---|---|---|---|---|---|
| naturopaths in my area | Broad | $23.95 | 10 | 0 | Same "in my area" problem. Matched "holistic health ulcerative colitis". |
| naturalist dr near me | Broad | $0 | 0 | 0 | 166 impressions, zero clicks. A 0 percent CTR drags the ad group's expected CTR and quality score. "Naturalist" is not what searchers mean. |
| natural healing doctors near me | Broad | $0 | 0 | 0 | 33 impressions, zero clicks. Same reason. |

### Men's Health

You rebuilt this group on Sept 1 around prostate, low testosterone and athletic performance. Keep those. Pause the generic "men's doctor" family: with broad match, Google treats "men's doctor near me" as ED, prostate-cancer and primary-care intent, and 88 percent of this group's visible spend went there.

| Keyword | Match | Cost | Clicks | Conv | Why |
|---|---|---|---|---|---|
| male medical clinic near me | Broad | $7.23 | 4 | 0 | testosterone test, prostate cancer treatment, prostate cancer test |
| male primary care doctors near me | Broad | $4.68 | 2 | 0 | Primary care by definition. Must go before the "primary care" negative. |
| gents specialist doctor near me | Broad | $2.96 | 4 | 2 | Both conversions were "best treatment for enlarged prostate" and "erectile dysfunction treatment"; the second is now blocked, the first is covered by your new prostate keywords. |
| male doctor near me | Broad | $2.06 | 1 | 1 | The one conversion was "men's health doctors near me", which `men's health naturopath` (kept) also matches. |
| men's specialist doctor near me | Broad | $2.02 | 4 | 0 | girth enlargement, ED sign up, blood flow |
| male health doctors near me | Broad | $2.02 | 2 | 0.5 | "problem with keeping a hard on" |
| men's health doctor near me | Broad | $0.47 | 2 | 0 | "instant ed cure" |
| men health clinic near me | Broad | $0.29 | 1 | 0 | "best over the counter ed treatment" |
| men's clinic near me, men's doctor near me, best mens doctor near me, men's physician near me, male health doctor near me, male clinic near me, best male doctor near me | Broad | under $1 each | | | Same family, same intent; pause for a clean group. |
| naturopath for erectile dysfunction | Broad | | | | Your own negatives ("ed", "erectile") now block it, so it can only show "blocked" status. Pause to keep the group readable. |

Keep in Men's Health: men's health naturopath, naturopath for men, naturopath for men's health, holistic doctor for men near me, adrenal fatigue doctor near me (2 conv on $9.75), naturopath for low testosterone, naturopath for testosterone, natural testosterone doctor near me, low testosterone natural treatment, naturopath for prostate, naturopath for prostate health, enlarged prostate natural treatment, natural prostate treatment near me, naturopath for athletic performance, men's hormone doctor near me.

### Pediatrics and Geo-Qualified

Nothing to pause. Two Pediatrics keywords have impressions and no clicks (`pediatric holistic doctor near me` 132, `natural pediatrician near me` 51). They are on-target; watch them for another 30 days.

Total paused: about $180 of 90-day spend, or 13 percent, that produced 4.5 page-load conversions and no visible booking.

---

## 4. Match type changes: broad to phrase (15 minutes)

Why: with click-based bidding, broad match has no conversion signal to steer it, so it drifts to whatever is cheap. Phrase match keeps the meaning of the keyword in the query. Budget-lost impression share is 82 to 90 percent, so the volume drop from narrowing is absorbed: the same $10 simply goes to better queries.

How: Keywords > select the keyword > Edit > Change match types > Phrase. Google creates a new keyword and removes the old one, so 90-day history on those rows resets. That is expected.

### Do these first (biggest leaks)

| Ad group | Keyword | 90-day cost | What broad pulled in |
|---|---|---|---|
| Women's | hormone doctor near me | $74.54 | contraceptives, estrogen patches, fertility clinic, low acth, hormone therapy, preventive screenings, "i want to go on the pill" |
| Women's | women's health naturopath | $105.71 | perimenopause symptoms, menopause symptoms, pcos treatment, fertility clinic x2, obgyns near me, m health, Spanish query |
| Functional | functional medicine | $113.99 | holistic medicine, what is functional medicine, food sensitivity test, doctors near me, bioresonance, high blood pressure, longevity products, pituitary healing frequency |
| Functional | functional medicine near me | $91.77 | best primary care physicians, biocharger, enema nurse, ways to well, ramsey county, ulcerative colitis, stomach pain |
| Functional | functional medicine doctors near me | $43.22 | dr silvia hugec, family practice physician, rheumatologist, lakeville specialty center, medical examination, geriatric, hcmc, physicians |
| Pediatrics | pediatric holistic doctor | $41.06 | pediatric clinics, anti vax, free children clinic, independent pediatrician, pediatric offices, rebecca doege |
| Pediatrics | holistic pediatricians near me | $36.51 | health partners, pediatric allergist, functional medicine pediatric, pediatricians who don't require vaccines |
| Core | alternative medicine near me | $27.32 | belief code, chakra tune up, poop, adhd medication, hennepin clinic, community health center, pppd, "medicine and doctors online" |

### Then the rest of Women's and Functional broad keywords

Women's: women's hormone specialist near me, female naturopath near me, naturopath for hormone imbalance, fertility naturopath near me, naturopath for fertility, naturopath for menopause, naturopath for pcos, naturopath for thyroid, women's naturopath, natural thyroid doctor near me, natural hormone doctors near me, holistic thyroid doctors near me, holistic hormone doctor near me, Hashimoto's naturopath.

Functional: functional integrative medicine near me, functional medicine clinic near me, functional medicine practitioner, functional medical doctors, best functional doctors near me, best functional doctor near me, functional medicine practice near me, integrative physician near me.

Men's (the ones you keep): all of them to phrase except `adrenal fatigue doctor near me`, which converted twice on $9.75 and can stay broad for now.

### Leave as broad

Core: naturopathic practitioner near me (4 conv on $12.03), holistic dr near me (2 conv on $4.71), naturopathic dr near me, best naturopath near me, best naturopathic doctor near me, naturopathic family medicine, naturopath for allergies, natural practitioner near me. These are naturopath-specific enough that broad stays on-topic.
Pediatrics: pediatric naturopath near me (2 conv on $10.48), pediatric naturopath, natural pediatrician near me, pediatric holistic doctor near me.

---

## 5. Bid adjustments (10 minutes)

These apply under Manual CPC and under Maximize Clicks. Percentages are starting points sized to the 90-day gaps; revisit after 30 days.

### Ad schedule (Campaign > Ad schedule; the rows already exist, add the modifier)

| Day | Row | Modifier | 90-day basis |
|---|---|---|---|
| Mon to Thu | 07:00 to 10:00 | +15% | 06:00 to 09:00 cost per page-load conversion $10 to $16 |
| Mon to Thu | 10:00 to 15:00 | -20% | 10:00 to 15:00 is 47% of spend at $20 to $81 per conversion |
| Mon to Thu | 15:00 to 17:00 | -10% | $43 to $67 per conversion |
| Mon to Thu | 17:00 to 20:00 | +15% | 18:00 to 19:00 ran $8 to $11 per conversion |
| Friday | all four rows | -30%, -35%, -30%, -10% | Friday: 4 conversions on $220, $55 each, worst day |
| Saturday | 07:00 to 14:00 | +10% | 16 conversions on $199, $12.41 each, best day |
| Sunday | 08:00 to 20:00 | -20% | 6 conversions on $192, $31.93 each |

### Devices (Campaign > Devices)

Mobile -15%. Mobile is 80 percent of spend at $22.03 per conversion; desktop is $14.61 with a 14.2 percent conversion rate versus 9.4. Do not touch tablets (13 clicks).

### Locations (Campaign > Locations)

The campaign targets a 22-mile radius plus six geo targets. To set a city adjustment the city must be added as its own target inside the radius: Locations > + > enter city > Target > then set the bid adjustment in the table.

| City | Adjustment | 90-day basis |
|---|---|---|
| Little Canada | -30% | $45.10, 29 clicks, 0 conversions |
| Maple Grove | -30% | $37.11, 15 clicks, 0 |
| Shakopee | -30% | $32.86, 15 clicks, 0 |
| Bloomington | -30% | $27.04, 14 clicks, 0 |
| Eagan | -30% | $25.24, 13 clicks, 0 |
| Lakeville | -30% | $17.00, 9 clicks, 0 (and "lakeville" is already a negative keyword) |
| Eden Prairie | +10% | $31.50, 3 conversions, $10.50 each |
| Plymouth | +10% | $62.70, 5 conversions, $12.54 each |
| Hopkins | +10% | only $16.83 spent at home; 98 impressions |

Alternative if you would rather not manage city rows: shrink the radius from 22 to 15 miles. That drops Little Canada, Shakopee, Eagan, Lakeville and most of Maple Grove in one move, and telehealth copy still covers the rest of the state.

---

## 6. Ads (10 minutes)

| Ad group | Ad ID | Action | Why |
|---|---|---|---|
| Men's Health | 817157424693 (paused) | Enable | While it ran: 15.5% CTR, 32 clicks on $31.56, 2 conversions. The enabled ad (812601575949) is rated Poor with 6.4% CTR. Run both for two weeks, then pause the weaker. |
| Men's Health | 812601575949 (enabled) | Edit headlines | Poor rating. It has 15 headlines but several restate "labs" and "numbers". Add two or three that name the new keyword themes: "Natural Prostate Support", "Low Testosterone, Naturally", "Men's Naturopathic Doctor". |
| Women's | 817264858229 (paused, Poor) | Leave paused | 4.7% CTR versus 5.5% on the live ad. |
| Functional | 817264881560 (paused, Pending) | Leave paused | Higher CTR (5.85% vs 4.45%) but $63 per conversion versus $23. |
| Geo-Qualified | 817157599125 (paused) | Leave paused | 1.66% CTR. |
| Women's, Core, Pediatrics | | Optional: add a second RSA | Women's ad is Average strength on your biggest group. If you write one, lead with "Dr. Haley Panka, ND" and "Perimenopause & Menopause", which are the headlines that map to the converting keywords. |

Sitelinks and callouts are fine. Three sitelinks point to /schedule-an-appointment, which is what you want.

---

## 7. Columns and a weekly cadence (5 minutes)

Set once at Campaigns > Columns > Modify:

- Conversions, All conv., Cost / conv., Conv. rate, plus Segment > Conversions > Conversion action when you want the split.
- Search impr. share, Search lost IS (budget), Search lost IS (rank).
- At the keyword level add Quality Score, Exp. CTR, Ad relevance, Landing page exp.

Weekly, 15 minutes: Keywords > Search terms > last 7 days > sort by cost. Add exact negatives for anything generic, phrase negatives for anything conventional. Then Keywords > sort by cost, pause anything at $15 with zero conversions over 60 days.

What "better" looks like after 30 days at the same budget: search-term junk share under 15 percent (from 37), click-through rate above 6 percent (from 5.2), and, in the monthly Acuity export, more intro calls and first appointments per $100 of spend than the June-to-August baseline (1.7 and 0.9 per $100 in high-spend weeks).

---

## 8. Acuity: intake question and monthly export

The export you sent is joined to spend in `leads-search-1-acuity-addendum-2026-09-07.md`. Two things going forward:

1. Acuity > Intake Forms > add "How did you hear about us?" with options Google ad, Google search, referral from a friend or clinician, social media, other. Required on the Introductory Phone Call type. This is the attribution method that keeps every byte inside Acuity.
2. Monthly, export the same de-identified appointment report (date scheduled, type, calendar, price, paid, scheduled by, plus the intake answer). I report intro calls and first appointments per $100 of spend, and the share of new patients naming a Google ad.

Confirm appointment type ID 41826455 under Appointment Types; the evidence says it is the Introductory Phone Call.

---

## Where things stand (clean stop)

Done: 90-day pull across Google Ads and GA4, review report, this guide, and the Acuity join in the addendum.
Yours: sections 2 to 6 in the Ads interface, section 7 once, section 8 in Acuity, section 1 after a word with your compliance advisor.
Mine after: monthly Acuity join, then a second pass on match types and bids with booking data instead of page loads.
