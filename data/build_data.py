"""Builds kosh-data.json: every figure carries a source id, an as-of date and a definition."""
import json
S = {}
def src(i, publisher, title, url, date, kind, sells=None):
    S[i] = dict(id=i, publisher=publisher, title=title, url=url, date=date, kind=kind, sells_services=sells)
src("S1","Nasscom-Zinnov","India GCC Landscape FY2026","https://zinnov.com/centers-of-excellence/zinnov-nasscom-india-gcc-landscape-2026-report/","2026-05","research","Zinnov sells GCC setup advisory")
src("S2","Business Today","India's GCC story hits 2030 target four years early","https://www.businesstoday.in/amp/technology/news/story/the-big-boom-how-indias-gcc-story-hits-2030-target-4-years-early-530265-2026-05-07","2026-05-07","news")
src("S3","KNN India","Govt targets 5,000 GCCs by 2030: FM at CII GCC Summit","https://knnindia.co.in/news/newsdetails/economy/govt-targets-5000-global-capability-centres-by-2030-fm-sitharaman","2026-07-10","government")
src("S4","Colliers via Outlook Business","Foreign firms rent 105 mn sq ft since 2022 for GCCs","https://www.outlookbusiness.com/news/foreign-firms-rent-105-mn-sq-ft-office-space-since-2022-to-establish-gccs-in-india-colliers","2026-07-24","broker","Colliers sells leasing advisory")
src("S5","Zinnov","5 shifts defining India's GCC story in 2025","https://zinnov.com/centers-of-excellence/5-shifts-defining-indias-global-capability-centers-gccs-story-in-2025-blog","2026-01-08","research","Zinnov sells GCC setup advisory")
src("S6","Vestian via The Week/PTI","GCC count and city split","https://www.theweek.in/wire-updates/business/2025/07/21/dcm52-biz-realty-gcc.html","2025-07-21","broker","Vestian sells workplace advisory")
src("S7","TeamLease via Storyboard18","India added 220 new GCCs in two years","https://www.storyboard18.com/how-it-works/india-added-220-new-gccs-in-2-years-sector-eyes-4-million-more-jobs-by-fy30-84071.htm","2025-11-12","staffing","TeamLease sells GCC staffing")
src("S8","ANSR via CXOToday","Emerging enterprises fuel India's GCC boom","https://cxotoday.com/press-release/emerging-enterprises-fuel-indias-gcc-boom-462000-professionals-14b-in-cumulative-revenue-new-ansr-report/","2025-11-25","research","ANSR sells GCC setup (BOT)")
src("S9","JLL via CXOToday","GCC expansion hits record 31 mn sq ft","https://cxotoday.com/research-whitepapers/indias-gcc-expansion-hits-record-31-million-sq-ft-with-metros-leading-growth-despite-tier-ii-emergence-jll/","2026-02-17","broker","JLL sells leasing advisory")
src("S10","CBRE","India Market Monitor Q2 2026","https://mktgdocs.cbre.com/2299/46818e44-7c68-4075-87d4-f55be26b98d0-598336659/India_Market_Monitor_Q2_2026_-.pdf","2026-07","broker","CBRE sells leasing advisory")
src("S11","CBRE via IANS","States target 1.18 million jobs, 1,380 new GCCs by 2031","https://ianslive.in/indian-states-target-118-million-jobs-1380-new-gccs-by-2031--20260814123137","2026-08-14","broker","CBRE sells leasing advisory")
src("S12","Siasat","New Telangana GCC policy to focus on AI, space, semiconductors","https://www.siasat.com/new-telangana-gcc-policy-to-focus-on-ai-space-semiconductors-3543873/","2026-09-17","news")
src("S13","South First","Karnataka launches India's first GCC policy","https://thesouthfirst.com/news/karnataka-launches-indias-first-gcc-policy-aiming-50-billion-economic-output-by-2029/","2024-09-27","news")
src("S14","law.asia","India GCC growth and state policies","https://law.asia/india-gcc-growth/","2025","legal")
src("S15","KPMG","Flash News: Maharashtra GCC Policy 2025","https://www.in.kpmg.com/taxflashnews/KPMG-Flash-News-Maharshtra-GCC-policy-2025.pdf","2025-10","advisory","KPMG sells GCC advisory")
src("S16","RSM India","Gujarat GCC Policy 2025-30","https://www.rsm.global/india/sites/default/files/media/publications/2025/Gujarat%20GCC%20Policy%202025_A%20Landmark%20Initiative%20to%20Attract%20Global%20Enterprises.pdf","2025-02","advisory","RSM sells advisory")
src("S17","Khaitan & Co","Uttar Pradesh releases its final GCC policy","https://www.khaitanco.com/thought-leadership/Uttar-Pradesh-releases-its-final-GCC-Policy","2025-05","legal")
src("S19","Mondaq / Khaitan","Rajasthan releases its GCC policy","https://webiis10.mondaq.com/india/employee-rights-labour-relations/1724116/impetus-to-gccs-in-india-rajasthan-releases-its-gcc-policy","2025","legal")
src("S20","Mondaq / Khaitan","Odisha releases its GCC policy","https://webiis10.mondaq.com/india/contracts-and-commercial-law/1749448/impetus-to-gccs-in-india-odisha-releases-its-gcc-policy","2025-12","legal")
src("S21","Drishti IAS","Madhya Pradesh GCC Policy 2025","https://www.drishtiias.com/state-pcs-current-affairs/madhya-pradesh-gcc-policy-2025","2025-02","news")
src("S22","Khaitan & Co","Andhra Pradesh IT and GCC Policy 4.0","https://khaitanco.com/thought-leadership/Impetus-to-GCCs-in-India-Andhra-Pradesh-Releases-its-IT-and-GCC-Policy","2024-12","legal")
src("S23","DT Next","TN Budget: payroll subsidies and IT parks","https://www.dtnext.in/amp/news/tamilnadu/tn-budget-from-payroll-subsidies-to-space-to-it-parks-the-big-budgetary-push-for-industries-768932","2024-02","news")
src("S24","Knight Frank via Siasat","Office rent in Hyderabad rises 10% in H1 2025","https://www.siasat.com/office-rent-in-hyderabad-sees-10-pc-rise-in-first-half-of-2025-3241549/","2025-07-03","broker","Knight Frank sells leasing advisory")
src("S25","The Realty Today (Propstack registration data)","Qualcomm leases 2.56 lakh sq ft at Bagmane Constellation","https://therealtytoday.com/news/commercial/semiconductor-giant-qualcomm-leases-256-lakh-sq-ft-at-bagmane-constellation-for-184-cr/","2025","registry")
src("S26","Zinnov","High-performer attrition in GCC India 2026","https://zinnov.com/global-talent/high-performer-attrition-gcc-india-2026-zinnov-blog/","2026-06","research","Zinnov sells GCC setup advisory")
src("S27","EY","GCC Pulse Survey, November 2025","https://www.ey.com/content/dam/ey-unified-site/ey-com/en-in/newsroom/2025/11/ey-global-capability-center-pulse-survey-november-2025.pdf","2025-11","survey","EY sells GCC advisory")
src("S28","Flexiple Talent Market","Salary medians by city (software engineer)","https://flexiple.com/market","2026-08","talent","Flexiple sells hiring and GCC setup")
src("S29","Vestian via The Realty Today","Office leasing reaches record 23.9 mn sq ft in Q2 2026","https://therealtytoday.com/news/market-insights/indias-office-leasing-reaches-record-239-mn-sq-ft-in-q2-2026-as-rentals-rise-vestian-report","2026-07-17","broker","Vestian sells workplace advisory")
src("S31","Business Standard","GCCs struggle to go beyond cost arbitrage in AI era","https://www.business-standard.com/technology/tech-news/gccs-struggle-to-go-beyond-cost-arbitrage-in-ai-era-shows-data-126071401063_1.html","2026-07-14","news")
src("S32","VJM Global","Cost of setting up a GCC in India","https://www.vjmglobal.com/blog/setting-up-gcc-cost-india-guide-gcc","2026","vendor","VJM Global sells setup services")
src("S33","Omnivoo","GCC India cost breakdown","https://www.omnivoo.com/blog/gcc-india-cost-breakdown","2026","vendor","Omnivoo sells EOR")
src("S34","Wisemonk","What transfers in a build-operate-transfer","https://www.wisemonk.io/blogs/what-transfers-build-operate-transfer-india","2026","vendor","Wisemonk sells EOR / BOT")
src("S35","Everest Group","GCC Setup PEAK Matrix 2025","https://www.everestgrp.com/report/egr-2025-34-r-7666","2025-11","research")
src("S36","AIM Research","Top GCC enablement service providers 2025","https://aimresearch.co/reports/top-gcc-enablement-service-providers-2025-india","2025-12","research")
src("S37","ANSR via BriefGlance","GCCs go mainstream: how small firms are reshaping India's talent hub","https://briefglance.com/articles/gccs-go-mainstream-how-small-firms-are-reshaping-indias-talent-hub","2026-07","research","ANSR sells GCC setup (BOT)")
src("S38","Ceipal","New GCCs in India 2024-2026","https://www.ceipal.com/resources/new-gccs-in-india-who-launched-whos-expanding-and-whos-coming-next-2024-2026","2026-03-23","vendor","Ceipal sells recruiting software")
src("S39","Flexiple","Upcoming Global Capability Centers in India","https://flexiple.com/global-capability-centers/upcoming-global-capability-centers-in-india","2026","talent","Flexiple sells hiring and GCC setup")
src("S40","Entrepreneur India (Nasscom-Zinnov)","Mid-market GCCs set to drive the next phase of growth","https://india.entrepreneur.com/technology/mid-market-gccs-set-to-drive-the-next-phase-of-growth/490546","2025-04","research","Zinnov sells GCC setup advisory")
src("S41","UNI","ANSR to set up 200 new GCCs in next five years","https://www.uniindia.com/ansr-to-set-up-200-new-gccs-in-next-5-year-globally-including-india/business-economy/news/3513828.html","2025","news")
src("S42","CXO Digital Pulse","Inductus and DST Gujarat sign MoU","https://www.cxodigitalpulse.com/inductus-group-and-dst-government-of-gujarat-signed-strategic-mou-to-position-gujarat-as-a-global-gcc-hub/","2026-04","news")
src("S43","Deloitte India","Deloitte India and Embark form a strategic alliance","https://www.deloitte.com/in/en/about/press-room/deloitte-india-and-embark-form-a-strategic-alliance.html","2025-08-06","press release")
src("S44","HDFC Sky","Quess Corp sets up new division for GCC market","https://hdfcsky.com/news/quess-corp-sets-up-new-business-division-for-targeting-gcc-market","2025-06-03","news")
src("S45","Elets","KDEM and GoodWorks target ₹5,000 crore GCC investment","https://egov.eletsonline.com/2026/08/kdem-goodworks-target-5000-crore-gcc-investment-in-karnataka/","2026-08-06","news")
src("S46","Cushman & Wakefield","Launch of GCC advisory practice","https://www.cushmanwakefield.com/en/india/news/2024/07/cushman-and-wakefield-launches-new-holistic-global-capability-center-advisory-practice","2024-07","press release")
src("S47","JLL","JLL India partners with Aeka Advisors","https://www.jll.com/en-in/newsroom/jll-india-partners-with-aeka-advisors-to-service-global","2025","press release")
src("S48","ThePrint","TeamLease and Invest UP partner for GCC talent","https://theprint.in/economy/teamlease-group-invest-up-partner-to-strengthen-talent-acquisition-for-gccs/2969616/","2026","news")
src("S49","Business Standard","Bhartiya Group launches GCC enablement venture","https://www.business-standard.com/companies/news/bhartiya-group-launches-new-venture-to-serve-as-gcc-enablement-platform-125042400523_1.html","2025-04-24","news")
src("S50","UNI","Keralam launches GCC Boilerplate","https://test.uniindia.com/keralam-launches-gcc-boilerplate-to-simplify-setup-of-global-capability-centres/south/news/3965723.html","2026-09-05","news")

F = []
def fact(subject, metric, value, unit, source, as_of, definition="", note="", num=None):
    F.append(dict(id=f"F{len(F)+1}", subject=subject, metric=metric, value=value, unit=unit, num=num, source=source, as_of=as_of, definition=definition, note=note))

# India level
fact("india","GCC count",2117,"GCCs","S1","2026-03","Parent companies with an India GCC",num=2117)
fact("india","GCC count",1760,"GCCs (1,760+)","S5","2025-12","Calendar-year view",num=1760)
fact("india","GCC count",1800,"GCC centres (1,800+)","S7","2025-11","FY25 basis",num=1800)
fact("india","GCC count",1700,"GCCs (~1,700)","S6","2025-07","Broker count of occupiers",num=1700)
fact("india","GCC count",2100,"GCCs (2,100+)","S4","2025-12","Broker count",num=2100)
fact("india","GCC units",3728,"units","S1","2026-03","Physical centres; one company can run several",num=3728)
fact("india","GCC headcount",2.36,"million people","S1","2026-03",num=2.36)
fact("india","GCC revenue",98.4,"US$ billion","S1","2026-03","Cost-plus billing to parents",num=98.4)
fact("india","New GCCs per year",105,"~100-110 a year","S5","2025-12","Zinnov tracking, early 2024 to late 2025",num=105)
fact("india","New GCCs per year",100,"200+ in two years","S9","2026-02","JLL, two years to early 2026",num=100)
fact("india","New GCCs per year",110,"220+ from FY23 to FY25","S7","2025-11",num=110)
fact("india","New GCCs per year",365,"'nearly one a day'","S3","2026-07","Rhetorical, Finance Minister's speech",num=365)
fact("india","New GCC setups H1 2026",62,"setups","S37","2026-06",num=62)
fact("india","Share of H1 2026 setups under US$100M revenue",27,"%","S37","2026-06","17 of 62",num=27)
fact("india","Mid-market GCCs",583,"GCCs","S1","2026-03","US$100M-1B revenue parents",num=583)
fact("india","Mid-market GCCs",480,"GCCs (480+)","S40","2025-04","US$100M-1B revenue parents",num=480)
fact("india","GCC attrition 2025",9,"%","S27","2025-11","EY survey of GCCs",num=9)
fact("india","GCC attrition 2025",15.1,"%","S26","2026-06","Zinnov SIAH sample",num=15.1)
fact("india","GCC share of office leasing",42,"% (Q2 2026)","S10","2026-07","Top cities, CBRE definition",num=42)
fact("india","GCC share of office leasing",52,"% (Q2 2026)","S29","2026-07","Vestian definition",num=52)
fact("india","GCC share of office leasing",46,"% (H1 2026)","S4","2026-07","Top 7 cities, Colliers",num=46)
fact("india","GCC closures in 2025",25,"25+ closures","S31","2026-07","Neovay tracking",num=25)
fact("india","GCCs set up since 2021 that have plateaued",30,"% (~150 centres)","S31","2026-07","Embark / UnearthIQ",num=30)
fact("india","Setup time to first hires (EOR/BOT)","5-16","weeks","S33","2026","Vendor estimate",num=None)
fact("india","Setup time (own entity)","6-18","months","S33","2026","Vendor estimate",num=None)
fact("india","Setup time",'3-6',"months","S5","2026-01","Zinnov typical",num=None)
fact("india","EOR fee per employee per month",99,"US$ (from)","S34","2026","Vendor's own price",num=99)
fact("india","EOR fee per employee per month","199-599","US$","S33","2026","Vendor's own price range",num=None)
fact("india","Grade A office rent, tier-1 cities","50-100","₹ / sq ft / month","S32","2026","Vendor estimate",num=None)
fact("india","States with dedicated GCC policies",8,"states","S11","2026-08",num=8)
fact("india","New GCCs targeted by states by 2031",1380,"GCCs","S11","2026-08",num=1380)
fact("india","Government GCC ecosystem target 2030",5000,"GCCs","S3","2026-07",num=5000)

# Cities
C = [
 dict(id="bengaluru",name="Bengaluru",state="KA",tier=1),
 dict(id="hyderabad",name="Hyderabad",state="TG",tier=1),
 dict(id="pune",name="Pune",state="MH",tier=1),
 dict(id="chennai",name="Chennai",state="TN",tier=1),
 dict(id="ncr",name="Delhi NCR",state="HR",alt_state="UP",tier=1),
 dict(id="mumbai",name="Mumbai",state="MH",tier=1),
 dict(id="ahmedabad",name="Ahmedabad / GIFT City",state="GJ",tier=2),
 dict(id="kochi",name="Kochi",state="KL",tier=2),
]
fact("bengaluru","GCC count",487,"GCCs","S6","2025-07","Companies",num=487)
fact("bengaluru","GCC count",880,"centres (880+)","S5","2025-12","Units",num=880)
fact("bengaluru","GCC count",900,"units (900+)","S9","2026-02","Units",num=900)
fact("bengaluru","Share of GCC activity","34-39","%","S9","2026-02",num=36.5)
fact("bengaluru","Software engineer median salary",15.7,"₹ lakh / year","S28","2026-08","Median of disclosed pay",num=15.7)
fact("bengaluru","Office rent (single transaction)",113,"₹ / sq ft / month","S25","2025","Qualcomm, ORR, registered lease",num=113)
fact("bengaluru","ER&D voluntary attrition",14.3,"%","S26","2026-06",num=14.3)
fact("hyderabad","GCC count",273,"GCCs","S6","2025-07","Companies",num=273)
fact("hyderabad","GCC count",355,"centres (355+)","S5","2025-12","Units",num=355)
fact("hyderabad","GCC count",515,"GCCs","S12","2026-09","State government count",num=515)
fact("hyderabad","Share of GCC absorption Q2 2026",21,"%","S29","2026-07",num=21)
fact("hyderabad","Software engineer median salary",10.4,"₹ lakh / year","S28","2026-08","Median of disclosed pay",num=10.4)
fact("hyderabad","Office rent, SBD","70-95","₹ / sq ft / month","S24","2025-07",num=82.5)
fact("hyderabad","New GCCs in 2025-26",75,"centres","S12","2026-09","Highest of any state",num=75)
fact("pune","GCC count",178,"GCCs","S6","2025-07","Companies",num=178)
fact("pune","Share of GCC activity","15-20","%","S9","2026-02",num=17.5)
fact("pune","Software engineer median salary",9.5,"₹ lakh / year","S28","2026-08",num=9.5)
fact("chennai","GCC count",162,"GCCs","S6","2025-07","Companies",num=162)
fact("chennai","Software engineer median salary",7.6,"₹ lakh / year","S28","2026-08",num=7.6)
fact("chennai","ER&D voluntary attrition",8.2,"%","S26","2026-06",num=8.2)
fact("ncr","GCC count",272,"GCCs","S6","2025-07","Companies",num=272)
fact("ncr","Software engineer median salary",14.1,"₹ lakh / year","S28","2026-08","Delhi",num=14.1)
fact("mumbai","GCC count",207,"GCCs","S6","2025-07","Companies",num=207)
fact("mumbai","Software engineer median salary",9.7,"₹ lakh / year","S28","2026-08",num=9.7)
fact("ahmedabad","Rent reimbursement cap (Gujarat policy)",50,"₹ / sq ft / month","S16","2025-02","A policy cap, not a market rent",num=50)
fact("kochi","Kerala GCC framework","Boilerplate launched; policy in draft","","S50","2026-09",num=None)

# States and incentive rules (structured for the eligibility check)
ST = [
 dict(id="KA",name="Karnataka",status="Policy 2024-29 (draft text verified; final amounts not verified)",source="S13",extra_sources=["S14"],
      rules=dict(),
      incentives=["Rent reimbursement up to 50%","R&D grants up to ₹50 crore","EPF support","45-day approvals","'Beyond Bengaluru' package for locations outside Bengaluru"],
      watch="Final notified amounts not verified."),
 dict(id="TG",name="Telangana",status="No notified GCC policy; draft in preparation (Sep 2026)",source="S12",rules=dict(no_policy=True),
      incentives=["Targeted support for frontier tech (AI, semiconductors, space, quantum) expected in the new policy"],
      watch="Nothing to claim today. Negotiate case by case."),
 dict(id="MH",name="Maharashtra",status="GCC Policy 2025 (operating guidelines pending, Nov 2025)",source="S15",
      rules=dict(excluded_functions=["bpo","call centre","sales"]),
      incentives=["Capex subsidy 20% of fixed capital, capped ₹10-100 crore by size","Or rent support 10% (Mumbai/Pune) / 20% (elsewhere) for 5 years","Payroll 40% (Mumbai/Pune) / 50% for 3 years, up to ₹50k per employee and ₹5 crore per unit","Stamp duty 50-100%, electricity duty 100% for 10 years"],
      watch="BPO, call centres and pure sales units are excluded. Guidelines pending."),
 dict(id="GJ",name="Gujarat",status="GCC Policy 2025-30 (effective Feb 2025)",source="S16",rules=dict(min_employees=50),
      incentives=["Capex 20% (infra) / 30% (IT), up to ₹50 crore","Opex 15% for 5 years; rent capped at ₹50/sq ft/month","₹50k per male / ₹60k per female employee","EPF 75% (men) / 100% (women) for 5 years"],
      watch="Minimum 50 employees."),
 dict(id="UP",name="Uttar Pradesh",status="GCC Policy 2024 (notified May 2025)",source="S17",
      rules=dict(min_employees_noida=200, min_employees_other=100),
      incentives=["Land subsidy 30-50%, 100% stamp duty","5% interest subsidy","Opex, payroll, EPF and recruitment subsidies"],
      watch="Thresholds: ₹20 crore or 200 staff in Noida/Ghaziabad; ₹15 crore or 100 staff elsewhere."),
 dict(id="RJ",name="Rajasthan",status="GCC Policy 2025 (to Mar 2029)",source="S19",
      rules=dict(ownership=["own"], first_n=10),
      incentives=["Capex 30% up to ₹10 crore","Lease 50% up to ₹1 crore","First 10 large GCCs: 30% salary reimbursement for 3 years"],
      watch="Wholly owned units only: BOT and JV setups are excluded. The richest incentives go to the first 10 GCCs."),
 dict(id="OD",name="Odisha",status="GCC Policy 2025 (from Dec 2025)",source="S20",
      rules=dict(min_employees=50, parent_rank=["g2000","f1000"]),
      incentives=["Capex 30%","Co-working up to ₹6,000 per seat per month","Recruitment ₹30-40k per hire","EPF/ESI 100% for 5 years"],
      watch="Parent must be Fortune 1000 or Forbes G2000, with 50+ staff."),
 dict(id="TN",name="Tamil Nadu",status="No standalone policy; payroll subsidy scheme to Mar 2027 (Budget Feb 2024)",source="S23",
      rules=dict(dated=True),
      incentives=["Payroll subsidy 30% / 20% / 10% over 3 years for new roles above ₹1 lakh a month","Land incentives up to 50%","'GCC One' fast-track desk"],
      watch="Scheme figures date from Feb 2024. Only roles paying over ₹1 lakh a month qualify."),
 dict(id="HR",name="Haryana",status="GCC Policy 2025",source="S14",rules=dict(),
      incentives=["Land subsidy 30-50%","Capex up to ₹25 crore","Payroll / EPF and stamp duty support"],
      watch="Amounts reported only in secondary coverage."),
 dict(id="KL",name="Kerala",status="Draft policy; 'Keralam GCC Boilerplate' launched Sep 2026",source="S50",rules=dict(no_policy=True),
      incentives=["Single framework to simplify setup"],watch="Incentive amounts not published."),
 dict(id="MP",name="Madhya Pradesh",status="GCC Policy 2025",source="S21",rules=dict(),incentives=["Capex, payroll, upskilling and R&D support"],watch="Amounts not published."),
 dict(id="AP",name="Andhra Pradesh",status="IT & GCC Policy 4.0 (2024-29)",source="S22",rules=dict(),incentives=["Capital, rental, recruitment and power incentives"],watch="Operating guidelines to follow; amounts not published."),
]

# Conflicts: same subject+metric, materially different values
CONFLICTS = [
 dict(id="X1",question="How many GCCs are in India?",facts=["F1","F2","F3","F4","F5","F6"],why="Mostly definitions and dates. Nasscom-Zinnov counts 2,117 parent companies and 3,728 physical centres in the same report. Brokers count office occupiers. Zinnov's own number jumps from 1,760+ (end-2025) to 2,117 (Mar 2026), which looks like a scope change, not a quarter of growth."),
 dict(id="X2",question="How many new GCCs open each year?",facts=["F9","F10","F11","F12","F13"],why="Research firms land near 100-110 a year. The Finance Minister's 'nearly one a day' is a speech line, not a count."),
 dict(id="X3",question="What is GCC attrition?",facts=["F17","F18"],why="Different samples. EY surveys GCC leaders; Zinnov tracks talent data. Plan for the higher figure in AI and cloud roles."),
 dict(id="X4",question="What share of office leasing do GCCs take?",facts=["F19","F20","F21"],why="Each broker uses its own city set and decides differently whether flex seats used by GCCs count as GCC leasing."),
 dict(id="X5",question="How many GCCs are in Bengaluru?",facts=["F33","F34","F35"],why="487 counts companies; 880+ and 900+ count centres."),
 dict(id="X6",question="How many GCCs are in Hyderabad?",facts=["F40","F41","F42"],why="The state government counts 515; Zinnov counts 355+ centres at end-2025. Different dates and different definitions of a GCC."),
 dict(id="X7",question="What does an EOR cost per employee?",facts=["F27","F28"],why="Both are vendors quoting their own prices. The gap is what an entrant has to negotiate blind."),
 dict(id="X8",question="How long does setup take?",facts=["F24","F25","F26"],why="It depends on the model: EOR/BOT gets first hires in weeks, your own entity takes months. Every figure here comes from a firm that sells setup."),
 dict(id="X9",question="How many mid-market GCCs are there?",facts=["F15","F16"],why="Two vintages of the same series: 480+ (Apr 2025) and 583 (Mar 2026)."),
]

GCCS = [
 dict(name="Costco",sector="Retail",city="hyderabad",status="Announced",detail="Technology, research and digital operations; 1,000+ professionals initial target",source="S38",as_of="2026-03"),
 dict(name="Eli Lilly",sector="Pharma",city="hyderabad",status="Announced",detail="AI, automation, software engineering; up to 1,500 people by 2026-27",source="S38",as_of="2026-03"),
 dict(name="Sanofi",sector="Pharma",city="hyderabad",status="Expanding",detail="€400 million investment; 2,600+ employees by 2026",source="S38",as_of="2026-03"),
 dict(name="HCA Healthcare",sector="Healthcare",city="hyderabad",status="Announced",detail="Hospital operations and healthcare technology; US$75 million investment",source="S38",as_of="2026-03"),
 dict(name="L'Oréal",sector="Consumer goods",city="hyderabad",status="Announced",detail="One of its largest global GCCs",source="S38",as_of="2026-03"),
 dict(name="Johnson & Johnson",sector="Healthcare",city="hyderabad",status="Announced",detail="Global healthcare operations, digital and enterprise support",source="S38",as_of="2026-03"),
 dict(name="Western Union (2nd centre)",sector="Financial services",city="hyderabad",status="Announced",detail="Platform engineering; BOT model with HCLTech; 400+ professionals",source="S39",as_of="2026"),
 dict(name="Qualcomm",sector="Semiconductors",city="bengaluru",status="Leased",detail="2.56 lakh sq ft at Bagmane Constellation, ORR, at ₹113/sq ft/month",source="S25",as_of="2025"),
]

PROVIDERS = [
 dict(name="ANSR",category="Setup & BOT",claim="Says it has set up 170 GCCs; plans 200 more in five years. MoU with Tamil Nadu.",source="S41"),
 dict(name="Bhartiya Converge",category="Real estate & enablement",claim="Launched in Apr 2025 as a GCC enablement platform.",source="S49"),
 dict(name="Cushman & Wakefield",category="Real estate",claim="GCC advisory practice offering services à la carte.",source="S46"),
 dict(name="Deloitte India + Embark",category="Advisory + operations",claim="Alliance (Aug 2025): Deloitte on strategy, entity and tax; Embark on facilities and operations. Targets mid-market firms.",source="S43"),
 dict(name="GoodWorks (Sansovi)",category="GCC-as-a-service",claim="MoU with KDEM (Karnataka, Aug 2026) targeting 50 new GCCs.",source="S45"),
 dict(name="Inductus",category="Setup & BOT",claim="BOT, company-owned partner-operated and modular models. MoU with Gujarat DST (Apr 2026) for mid-sized MNCs.",source="S42"),
 dict(name="JLL + Aeka Advisors",category="Real estate + advisory",claim="Partnership to serve global companies setting up GCCs.",source="S47"),
 dict(name="Quess (Origint)",category="Staffing & workplace",claim="Division launched Jun 2025: workforce, workplace and workload as a service.",source="S44"),
 dict(name="TeamLease",category="Staffing",claim="Partnership with Invest UP on GCC talent.",source="S48"),
 dict(name="Wisemonk",category="EOR",claim="EOR from US$99 per employee per month (its own published price).",source="S34"),
 dict(name="Zinnov",category="Advisory & research",claim="Publishes the Nasscom-Zinnov GCC landscape and sells setup advisory.",source="S1"),
]

ASSUMPTIONS = dict(
  sqft_per_seat=dict(value=100,label="100 sq ft per seat (Kosh planning assumption, not sourced)"),
  statutory_load=dict(value=0.125,label="Statutory benefits add 10-15% to salary (vendor estimate, S32); midpoint 12.5%",source="S32"),
  salary_proxy=dict(label="Software engineer median used as the average cost per head. Real mixes vary a lot by role and seniority.",source="S28"),
  rent_fallback=dict(low=50,high=100,label="Grade A tier-1 rent ₹50-100/sq ft/month (vendor estimate, S32) where no city figure exists",source="S32"),
  inr_per_usd=dict(value=88,label="₹88 per US$ (Kosh planning rate)"),
)
out = dict(meta=dict(name="Kosh dataset",version="0.1",as_of="2026-10-13",note="Prototype dataset compiled from public sources. Every figure carries a source and date. Not investment, legal or tax advice."),
           sources=list(S.values()), facts=F, cities=C, states=ST, conflicts=CONFLICTS, gccs=GCCS, providers=PROVIDERS, assumptions=ASSUMPTIONS)
# integrity checks
ids={f["id"] for f in F}
for f in F: assert f["source"] in S, f
for x in CONFLICTS:
    for fid in x["facts"]: assert fid in ids, (x["id"],fid)
    subj={next(f for f in F if f["id"]==fid)["metric"] for fid in x["facts"]}
for s in ST: assert s["source"] in S
for g in GCCS+PROVIDERS: assert g["source"] in S
import os; json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"kosh-data.json"),"w"), ensure_ascii=False, indent=1)
print(len(S),"sources",len(F),"facts",len(CONFLICTS),"conflicts")
for x in CONFLICTS: print(x["id"],[ (next(f for f in F if f["id"]==i)["subject"],next(f for f in F if f["id"]==i)["metric"]) for i in x["facts"]])
