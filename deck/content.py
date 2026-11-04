"""Slide content for the Insight Global healthcare graph-platform deck.

Five platforms, one per domain. Each one is a knowledge graph built around a central
entity, with agents on top, and solves the whole set of problems in its domain.
Value figures are either sourced public evidence (source given) or a pilot target,
labelled as such. Graph stats are design counts, not data volumes.
"""

DECK_LABEL = "HEALTHCARE AI CASE STUDIES"
DECK_DATE = "NOVEMBER 2026"

CAPABILITIES = [
    ("Agentic AI & GenAI engineering",
     "Multi-agent workflows, RAG / GraphRAG, evaluation and guardrails, model-agnostic."),
    ("Knowledge graph & data engineering",
     "Healthcare ontologies (RxNorm, ICD-10, SNOMED, LOINC, NPI, UDI), ETL, vector search."),
    ("Salesforce for healthcare",
     "Health Cloud, Life Sciences Cloud, Marketing Cloud, Data Cloud, Agentforce, MuleSoft."),
    ("Multi-cloud delivery",
     "Google Cloud, AWS and Azure. The same design runs wherever the client already is."),
    ("Healthcare compliance & governance",
     "HIPAA, GxP / Part 11, FDA device and safety rules, consent, masking and audit trails."),
    ("Product & delivery",
     "Ideation workshops, architecture, proof of concept to production, change management."),
]

PROOF_POINT = ("We built a governed agentic delivery platform for a large US health system "
               "(Salesforce Health and Marketing Cloud, masked data context, compliance guardian, human approval gates).")

APPROACH_COLUMNS = [
    ("Data sources", "Public reference data + client systems (EHR, CRM, QMS, devices)", "database"),
    ("Python ETL", "Load, link, de-identify and embed; runs on any cloud", "workflow"),
    ("Knowledge graph", "One central entity, connected spokes, vector indexes", "network"),
    ("Graph assistant", "Specialist agents that plan, cite and hand off to people", "bot"),
    ("Experience", "Salesforce, dashboards, natural-language Q&A", "layout-dashboard"),
]
APPROACH_GOVERNANCE = "Governance built in: guardrails in and out · PHI masking & minimum-data access · human approval gates · evaluation sets · audit trail"
CLOUDS = ["Google Cloud", "AWS", "Azure", "Salesforce"]

ENGAGEMENT_STEPS = [
    ("Ideation workshop · 2 weeks", "Pick the graph and first modules, map data and stakeholders, agree success metrics."),
    ("Proof of concept · 6–8 weeks", "Working graph and agents on public and synthetic data, architecture signed off, sponsor demo."),
    ("Pilot · ~3 months", "Real users, governed client data, measured against the agreed KPIs."),
    ("Scale · ongoing", "Add modules and sites, then the next graph on the same platform."),
]

GOVERNANCE_LINE = "PHI masking · guardrails in & out · human approval · audit trail"

# --------------------------------------------------------------------------------------
PLATFORMS = [
    # ---------------------------------------------------------------- CareGraph
    {
        "name": "CareGraph",
        "domain": "Care Engagement",
        "accent": "cyan",
        "icon": "heart-pulse",
        "tagline": "Care Engagement Intelligence Platform",
        "subtitle": "Connecting patients, care gaps, providers, access and outreach with a knowledge graph",
        "headline": "Care teams can't see, or act on, the whole patient journey",
        "problem": "Care gaps, scheduling, referrals, costs and outreach sit in separate systems. Health systems run many campaigns "
                   "but can't tell why a gap exists, what works for whom, or whether outreach is fair.",
        "who": "Population health, patient access, care coordination, marketing, quality",
        "problems": [
            ("clipboard-check", "Care gaps stay open", "Screenings and chronic-care follow-ups are missed"),
            ("megaphone", "One-size-fits-all outreach", "Low conversion and high opt-outs"),
            ("calendar-check", "Hard to get an appointment", "Long queues and abandoned scheduling"),
            ("route", "Referral leakage", "Patients leave the network"),
            ("badge-dollar-sign", "Cost confusion", "No clear estimates or financial help"),
            ("lock", "Privacy slows everything", "Each campaign waits on compliance review"),
        ],
        "definition": "One knowledge graph of the patient journey, with agents that find gaps, design outreach and book care, using masked data.",
        "modules": [
            ("Cohort & gap intelligence", "explains every gap by measure, community and access"),
            ("Journey designer", "personalized Marketing Cloud journeys"),
            ("Access navigator", "right provider, right slot, clear estimate"),
            ("Referral integrity", "keeps referrals in network"),
            ("Compliance guardian", "consent, HIPAA and TCPA checked before send"),
        ],
        "built_on": ["Health Cloud", "Marketing Cloud", "Data Cloud", "Agentforce", "Tableau"],
        "center": ("Patient", "user-round"),
        "spokes": [
            ("Care gaps", "clipboard-check"), ("Providers", "stethoscope"), ("Appointments", "calendar-check"),
            ("Referrals", "route"), ("Community (SDOH)", "house-heart"), ("Journeys", "megaphone"),
            ("Consent", "shield-check"), ("Costs", "badge-dollar-sign"),
        ],
        "stats": [("10", "Entity types"), ("18", "Relationships"), ("6", "Vector indexes")],
        "sources": [
            ("EHR / FHIR", "Encounters, problems, care gaps", "hospital"),
            ("CMS quality measures", "eCQM specifications", "file-text"),
            ("CDC PLACES + SDOH", "Community health by census tract", "map-pin"),
            ("NPPES", "Provider identity (NPI)", "stethoscope"),
            ("Price transparency", "Hospital & payer rate files", "badge-dollar-sign"),
            ("Engagement data", "Marketing Cloud, contact center", "message-square"),
        ],
        "etl": [
            ("database", ["load_fhir", "load_ecqm"]),
            ("map-pin", ["load_places", "load_nppes"]),
            ("badge-dollar-sign", ["ingest_rates", "ingest_engagement"]),
            ("lock", ["mask_phi", "embed_nodes"]),
        ],
        "agents": ["Cohort builder", "Gap explainer", "Journey designer", "Access navigator", "Compliance guardian"],
        "outputs": [("Health Cloud console", "layout-dashboard"), ("Marketing Cloud journeys", "megaphone"),
                    ("Natural-language Q&A", "message-square")],
        "capabilities": [
            ("Care-gap closure", "clipboard-check"), ("Personalized journeys", "megaphone"), ("Patient access", "calendar-check"),
            ("Referral integrity", "route"), ("Equity analytics", "scale"), ("GraphRAG Q&A", "network"), ("Agentic AI", "bot"),
        ],
        "value_headline": "Close more care gaps, book more visits and keep patients in network, with every send compliant.",
        "value_stats": [
            ("↑", "Care-gap closure rate per campaign", "Pilot target"),
            ("↓", "Calls per booked appointment", "Pilot target"),
            ("29%", "faster case resolution reported with Health Cloud", "Salesforce (vendor-reported)"),
            ("100%", "of outreach checked for consent and PHI before send", "Design guarantee"),
        ],
        "benefits": {
            "Business": "Quality-program revenue, more booked visits, less leakage",
            "Clinical": "Earlier screening and chronic-care follow-up",
            "IT & data": "One governed patient graph reused by every team",
            "Compliance": "Minimum-data access; every send auditable",
        },
        "talk": "Closest to what our core team already delivers for a large US health system. Land the point that agents work on masked "
                "aggregates, so marketing, access and population health move fast without touching raw patient data.",
        "questions": [
            "How do you measure care-gap closure today, and which quality programs drive it?",
            "What share of appointments are booked online versus by phone?",
            "How long does compliance review take for a new campaign?",
        ],
        "trigger": "Care gaps, low screening rates, no-shows, outreach that doesn't convert, network leakage, price questions",
        "who_to_talk": "CMO / CNO, VP Population Health, Patient Access, Marketing",
    },
    # ---------------------------------------------------------------- TherapyGraph
    {
        "name": "TherapyGraph",
        "domain": "Life Sciences",
        "accent": "magenta",
        "icon": "flask-conical",
        "tagline": "Life Sciences Intelligence Platform",
        "subtitle": "Connecting therapies, HCPs, trials, evidence and content with a knowledge graph",
        "headline": "Commercial, medical and clinical teams work from different pictures",
        "problem": "HCP data, trial data, publications and approved content live in separate systems. Brands struggle to personalize "
                   "compliantly, MLR review takes weeks, and trials miss enrollment targets.",
        "who": "Brand and omnichannel teams, Medical Affairs, MLR, Clinical Operations",
        "problems": [
            ("users", "Fragmented HCP view", "CRM, claims and public data never meet"),
            ("file-search", "Slow MLR review", "Every asset waits weeks for approval"),
            ("shield-alert", "Off-label risk", "Claims drift from the approved label"),
            ("flask-conical", "Trial enrollment delays", "Criteria are free text; screening is manual"),
            ("map-pin", "Site selection by gut feel", "Not grounded in patient data"),
            ("message-square", "Field insights get lost", "MSL notes never reach strategy"),
        ],
        "definition": "One graph of each therapy's world (HCPs, evidence, trials and content) with agents for engagement, review and recruitment.",
        "modules": [
            ("HCP 360 & next-best-action", "channel, content and timing per HCP"),
            ("MLR pre-review", "flags off-label claims before human review"),
            ("Trial feasibility & sites", "masked patient counts by site and region"),
            ("Patient matching & recruitment", "every criterion explained, consent-aware outreach"),
            ("Medical-affairs insight", "summarizes field and literature signals"),
        ],
        "built_on": ["Life Sciences Cloud", "Marketing Cloud", "Data Cloud", "Agentforce"],
        "center": ("Therapy", "pill"),
        "spokes": [
            ("HCPs", "stethoscope"), ("Label & indications", "file-text"), ("Clinical trials", "flask-conical"),
            ("Sites & investigators", "hospital"), ("Publications", "book-open"), ("Open Payments", "badge-dollar-sign"),
            ("Content & claims", "megaphone"), ("Patient programs", "users"),
        ],
        "stats": [("11", "Entity types"), ("20", "Relationships"), ("7", "Vector indexes")],
        "sources": [
            ("NPPES", "HCP identity (NPI)", "stethoscope"),
            ("CMS Open Payments", "Industry payments to HCPs", "badge-dollar-sign"),
            ("Medicare Part D", "Prescribing by NPI and drug", "pill"),
            ("ClinicalTrials.gov", "Trials, criteria, sites", "flask-conical"),
            ("DailyMed labels", "Approved indications & claims", "file-text"),
            ("PubMed", "Publications & authors", "book-open"),
        ],
        "etl": [
            ("database", ["load_nppes", "load_open_payments"]),
            ("pill", ["load_partd", "load_labels"]),
            ("flask-conical", ["ingest_trials", "load_pubmed"]),
            ("network", ["resolve_npi", "embed_nodes"]),
        ],
        "agents": ["Pre-call briefing", "Next-best-action", "MLR pre-review", "Trial feasibility", "Patient matcher"],
        "outputs": [("Life Sciences Cloud console", "layout-dashboard"), ("Marketing Cloud", "megaphone"),
                    ("Natural-language Q&A", "message-square")],
        "capabilities": [
            ("HCP 360", "users"), ("Next-best-action", "target"), ("MLR pre-review", "file-search"),
            ("Trial feasibility", "flask-conical"), ("Patient recruitment", "user-round"), ("GraphRAG Q&A", "network"),
            ("Agentic AI", "bot"),
        ],
        "value_headline": "More relevant HCP engagement, faster content approval and trials that enroll on time.",
        "value_stats": [
            ("~40%", "less trial screening time with NIH's TrialGPT approach", "NIH, Nature Communications 2024"),
            ("↓", "MLR cycle time per asset", "Pilot target"),
            ("↑", "HCP engagement rate", "Pilot target"),
            ("$14.67B", "in HCP payments in CMS Open Payments (PY2025), linkable by NPI", "CMS via IntuitionLabs"),
        ],
        "benefits": {
            "Business": "Faster launches, rep productivity, shorter trials",
            "Clinical": "Accurate, on-label information; more patients reach trials",
            "IT & data": "One therapy graph shared by commercial, medical and clinical",
            "Compliance": "Sunshine Act and PhRMA Code guardrails built in",
        },
        "talk": "Salesforce Life Sciences Cloud went GA in October 2025 and pharma is rebuilding its commercial stack, so timing is good. "
                "TherapyGraph is the one graph that commercial, medical and clinical teams can all use.",
        "questions": [
            "Are you moving to, or evaluating, Salesforce Life Sciences Cloud?",
            "How long does an asset take to get through MLR today?",
            "Which studies are behind on enrollment, and how are sites chosen?",
        ],
        "trigger": "Launch planning, HCP engagement, slow MLR review, trial enrollment delays, site selection",
        "who_to_talk": "Brand / commercial leads, Medical Affairs, Clinical Operations",
    },
    # ---------------------------------------------------------------- RxGraph
    {
        "name": "RxGraph",
        "domain": "Pharmacy & Drug",
        "accent": "yellow",
        "icon": "pill",
        "tagline": "Pharmacy & Medication Intelligence Platform",
        "subtitle": "Connecting medications, interactions, coverage, safety and supply with a knowledge graph",
        "headline": "Medication decisions depend on data scattered across many systems",
        "problem": "Medication lists are messy, interaction alerts are noisy, prior auth is manual, adherence slips and shortages hit "
                   "without warning. General-purpose AI models also miss dangerous interactions.",
        "who": "Health-system and specialty pharmacy, PBMs, pharma patient-services hubs, drug safety",
        "problems": [
            ("clipboard-check", "Messy medication lists", "Reconciled by hand at admission and discharge"),
            ("triangle-alert", "Missed interactions", "Noisy alerts hide real risks"),
            ("file-text", "Prior-auth backlogs", "Packets assembled from charts by hand"),
            ("bell", "Poor adherence", "Refill gaps go unnoticed"),
            ("siren", "Missed adverse events", "Safety reports lost in support calls"),
            ("package", "Shortages", "Substitutes chosen under pressure"),
        ],
        "definition": "One graph of every medication (ingredients, interactions, coverage, safety and supply) with agents that reconcile, check, authorize and substitute.",
        "modules": [
            ("Medication reconciliation", "free text to standard codes, discrepancies flagged"),
            ("Interaction & PGx safety", "graph lookup first; AI only explains"),
            ("Benefits & prior auth", "evidence mapped to payer criteria (CMS-0057-F ready)"),
            ("Adherence & adverse events", "refill nudges and safety-report capture"),
            ("Shortage substitution", "equivalent options checked against formulary"),
        ],
        "built_on": ["Health Cloud", "Service Cloud", "Agentforce", "EHR (FHIR)"],
        "center": ("Medication", "pill"),
        "spokes": [
            ("Ingredients & ATC", "flask-conical"), ("Interactions", "triangle-alert"), ("Labels", "file-text"),
            ("Pharmaco-genomics", "dna"), ("Formulary & coverage", "scale"), ("Prior-auth criteria", "clipboard-check"),
            ("Adverse events", "siren"), ("NDC & shortages", "package"),
        ],
        "stats": [("12", "Entity types"), ("22", "Relationships"), ("6", "Vector indexes")],
        "sources": [
            ("RxNorm", "Drug identity (RxCUI)", "pill"),
            ("DailyMed / openFDA", "Labels, indications, warnings", "file-text"),
            ("openFDA FAERS", "Adverse event reports", "siren"),
            ("CPIC / PharmGKB", "Gene–drug guidance", "dna"),
            ("CMS Part D & LCD/NCD", "Formulary & coverage rules", "scale"),
            ("FDA shortages & NDC", "Supply status", "package"),
        ],
        "etl": [
            ("database", ["load_rxnorm", "load_labels"]),
            ("siren", ["ingest_faers", "load_cpic"]),
            ("scale", ["load_formulary", "load_policies"]),
            ("package", ["ingest_shortages", "embed_nodes"]),
        ],
        "agents": ["Reconciler", "Interaction checker", "Prior-auth builder", "Adherence coach", "Substitute finder"],
        "outputs": [("Pharmacist worklist", "clipboard-check"), ("Health Cloud / EHR", "layout-dashboard"),
                    ("Natural-language Q&A", "message-square")],
        "capabilities": [
            ("Med reconciliation", "clipboard-check"), ("Interaction safety", "shield-check"), ("Prior auth", "file-text"),
            ("Adherence", "bell"), ("Adverse events", "siren"), ("Shortage substitution", "package"), ("GraphRAG Q&A", "network"),
        ],
        "value_headline": "Safer medication lists, faster access to therapy and fewer surprises from shortages.",
        "value_stats": [
            ("4 of 4", "AI models tested missed a known interaction, so answers must be grounded", "ERCSP 2024"),
            ("↓", "Pharmacist minutes per reconciliation", "Pilot target"),
            ("↑", "Prior-auth first-pass approval", "Pilot target"),
            ("Jan 2027", "CMS prior-authorization API deadline (CMS-0057-F)", "CMS"),
        ],
        "benefits": {
            "Business": "Fewer readmissions, faster time to therapy, less waste",
            "Clinical": "Fewer adverse drug events, continuity during shortages",
            "IT & data": "Standard drug codes and FHIR-ready prior-auth APIs",
            "Compliance": "Pharmacist approves every change; adverse events routed to safety",
        },
        "talk": "Plain chatbots get drug interactions wrong; a graph of trusted drug data plus a pharmacist gate gets them right. "
                "The prior-auth deadline in January 2027 makes this urgent for payers, pharmacies and pharma hubs.",
        "questions": [
            "Who does medication reconciliation today, and how long does it take?",
            "How many prior auths a month, and what's the first-pass approval rate?",
            "How did the last major shortage affect you, and how early did you know?",
        ],
        "trigger": "Medication errors, noisy alerts, prior-auth backlogs, CMS-0057-F, adherence, adverse events, shortages",
        "who_to_talk": "Chief Pharmacy Officer, VP Patient Services, Drug Safety",
    },
    # ---------------------------------------------------------------- DeviceGraph
    {
        "name": "DeviceGraph",
        "domain": "Medical Devices & IoT",
        "accent": "purple",
        "icon": "cpu",
        "tagline": "Medical Device & IoT Intelligence Platform",
        "subtitle": "Connecting devices, patients, telemetry, complaints, recalls and security with a knowledge graph",
        "headline": "Device data is everywhere, but nobody sees the whole picture",
        "problem": "Remote-monitoring readings flood care teams, complaints pile up against tight FDA deadlines, recalls are hard to trace "
                   "to patients, and connected devices carry known vulnerabilities.",
        "who": "MedTech quality & regulatory, virtual care / RPM programs, biomedical engineering",
        "problems": [
            ("bell", "Alert fatigue", "Too many readings, too few real signals"),
            ("clipboard-check", "Complaint backlogs", "Manual triage and inconsistent coding"),
            ("siren", "Late FDA reports", "Reportability decided under time pressure"),
            ("search", "Recall traceability", "Which patients have the affected device?"),
            ("shield-alert", "Device vulnerabilities", "Known CVEs on connected devices"),
            ("badge-dollar-sign", "RPM billing missed", "Data-day and minute rules tracked by hand"),
        ],
        "definition": "One graph that follows every device (UDI) from patient and telemetry to complaints, recalls and vulnerabilities, with agents for triage, reporting and remediation.",
        "modules": [
            ("Remote-monitoring triage", "rules and models decide; AI explains"),
            ("Complaint & reportability", "intake, IMDRF coding, FDA / EU MDR advice"),
            ("Recall & UDI tracing", "device to patient in one query"),
            ("Post-market trends", "early signals from MAUDE and internal data"),
            ("Device cybersecurity", "CVE-to-asset matching and patch plans"),
        ],
        "built_on": ["Health Cloud", "Service Cloud", "MuleSoft", "Tableau"],
        "center": ("Device (UDI)", "cpu"),
        "spokes": [
            ("Patients", "user-round"), ("Telemetry", "activity"), ("Care plans", "heart-pulse"),
            ("Complaints", "message-square"), ("MAUDE events", "siren"), ("Recalls", "triangle-alert"),
            ("510(k) / PMA", "file-text"), ("Vulnera-bilities", "shield-alert"),
        ],
        "stats": [("12", "Entity types"), ("21", "Relationships"), ("5", "Vector indexes")],
        "sources": [
            ("Device telemetry", "Wearables & home devices (FHIR)", "watch"),
            ("FDA GUDID", "UDI device identity", "database"),
            ("FDA MAUDE", "Device adverse events", "siren"),
            ("FDA recalls & 510(k)", "Recalls, clearances, predicates", "file-text"),
            ("CISA ICSMA & NVD", "Device vulnerabilities", "shield-alert"),
            ("Complaints & service", "Service Cloud cases", "message-square"),
        ],
        "etl": [
            ("wifi", ["ingest_telemetry", "to_fhir"]),
            ("database", ["load_gudid", "ingest_maude"]),
            ("file-text", ["load_recalls", "load_510k"]),
            ("shield-alert", ["load_cves", "embed_nodes"]),
        ],
        "agents": ["RPM triage", "Complaint intake", "Reportability advisor", "Trend detector", "Patch planner"],
        "outputs": [("Care team console", "layout-dashboard"), ("Quality & regulatory", "clipboard-check"),
                    ("Natural-language Q&A", "message-square")],
        "capabilities": [
            ("Remote monitoring", "activity"), ("Complaint handling", "clipboard-check"), ("FDA reporting", "siren"),
            ("Recall tracing", "search"), ("Cybersecurity", "shield-check"), ("GraphRAG Q&A", "network"), ("Agentic AI", "bot"),
        ],
        "value_headline": "Fewer, better alerts, faster complaint handling and devices you can trace and secure.",
        "value_stats": [
            ("2M+", "medical device reports FDA receives each year (MAUDE)", "FDA"),
            ("↓", "Alerts per nurse per day", "Pilot target"),
            ("↓", "Complaint cycle time and late FDA reports", "Pilot target"),
            ("↓", "Time to remediate critical device vulnerabilities", "Pilot target"),
        ],
        "benefits": {
            "Business": "Billable virtual care, lower cost of quality, fewer surprise recalls",
            "Clinical": "Earlier intervention and safety issues found sooner",
            "IT & data": "Standards-based device integration (FHIR, UDI)",
            "Compliance": "21 CFR 803, EU MDR vigilance; people make every reportability call",
        },
        "talk": "The IoT story and the device-quality story in one graph. Key design choice: rules and models make the clinical call and "
                "people make the reportability call; AI prepares and explains, so it stays safe and auditable.",
        "questions": [
            "How many patients are in remote monitoring, and how many alerts does a nurse handle per day?",
            "How many complaints a month, and any late MDRs or FDA observations?",
            "Can you trace a recalled device to the patients who have it today?",
        ],
        "trigger": "Remote monitoring programs, alert fatigue, complaint backlogs, FDA / EU MDR reporting, recalls, device security",
        "who_to_talk": "VP Quality / Regulatory, Post-Market Surveillance, Virtual Care, Biomed / CISO",
    },
    # ---------------------------------------------------------------- ChainGraph
    {
        "name": "ChainGraph",
        "domain": "Manufacturing & Supply Chain",
        "accent": "green",
        "icon": "factory",
        "tagline": "Manufacturing & Supply Chain Intelligence Platform",
        "subtitle": "Connecting suppliers, plants, batches, quality and distribution with a knowledge graph",
        "headline": "From supplier to patient, the chain is only visible in pieces",
        "problem": "Supplier risks are hidden, deviation investigations take weeks, repeat findings lead to FDA 483s, and shortages are "
                   "discovered too late to plan around.",
        "who": "Pharma & biotech manufacturing, CDMOs, quality, supply chain, distributors",
        "problems": [
            ("truck", "Hidden supplier risk", "Single-source materials and facilities"),
            ("search", "Slow investigations", "Deviations start from a blank page"),
            ("workflow", "Repeat deviations", "Root causes never connected; CAPAs overdue"),
            ("clipboard-check", "Batch review bottleneck", "eBMR review delays release"),
            ("file-search", "Inspection findings", "Repeat FDA 483 themes"),
            ("package", "Late shortage warning", "Stock-outs discovered too late"),
        ],
        "definition": "One graph of the product chain (supplier, material, plant, batch, distribution) with agents for quality, risk and shortage planning.",
        "modules": [
            ("Supplier & material risk", "single-source and facility risk map"),
            ("Deviation & CAPA copilot", "similar events, root cause and CAPA drafts"),
            ("Batch-record review", "exceptions flagged before QA release"),
            ("Inspection readiness", "matches findings to FDA 483 themes"),
            ("Shortage early warning", "supply signals and substitution plans"),
        ],
        "built_on": ["Quality system (e.g. Veeva Vault QMS)", "MES / LIMS / ERP", "Tableau", "Any cloud"],
        "center": ("Product lot", "boxes"),
        "spokes": [
            ("Suppliers", "truck"), ("Materials & lots", "package"), ("Plants & equipment", "factory"),
            ("Batch records", "test-tube"), ("Deviations & CAPA", "triangle-alert"), ("SOPs & 483s", "scale"),
            ("Distribution", "route"), ("Demand & shortages", "gauge"),
        ],
        "stats": [("13", "Entity types"), ("24", "Relationships"), ("6", "Vector indexes")],
        "sources": [
            ("ERP & suppliers", "Suppliers, materials, orders", "truck"),
            ("MES / eBMR & LIMS", "Batches, equipment, tests", "factory"),
            ("Quality system (QMS)", "Deviations, CAPAs, changes", "clipboard-check"),
            ("FDA 483s & letters", "Inspection findings", "file-search"),
            ("FDA shortages & recalls", "Market supply signals (NDC)", "package"),
            ("DSCSA / distribution", "Serialization & inventory", "route"),
        ],
        "etl": [
            ("truck", ["load_erp", "load_suppliers"]),
            ("factory", ["ingest_mes", "ingest_lims"]),
            ("clipboard-check", ["load_qms", "load_483s"]),
            ("package", ["ingest_shortages", "embed_nodes"]),
        ],
        "agents": ["Supplier risk", "Deviation triage", "Root-cause drafter", "CAPA checker", "Shortage early warning"],
        "outputs": [("Quality workbench", "clipboard-check"), ("Supply dashboard", "layout-dashboard"),
                    ("Natural-language Q&A", "message-square")],
        "capabilities": [
            ("Supplier risk", "truck"), ("Deviation & CAPA", "workflow"), ("Batch review", "clipboard-check"),
            ("Inspection readiness", "file-search"), ("Shortage warning", "package"), ("GraphRAG Q&A", "network"),
            ("Agentic AI", "bot"),
        ],
        "value_headline": "Close investigations faster, stop repeat deviations and see shortages coming, with QA always in control.",
        "value_stats": [
            ("40%", "faster deviation closure reported in industry GenAI case studies", "McKinsey (vendor-reported)"),
            ("323", "active US drug shortages at the Q1 2024 peak", "ASHP"),
            ("↓", "Repeat deviations and overdue CAPAs", "Pilot target"),
            ("↑", "Days of warning before a stock-out", "Pilot target"),
        ],
        "benefits": {
            "Business": "Right-first-time batches, less lost product, less emergency buying",
            "Clinical": "Consistent quality and continuity of supply for patients",
            "IT & data": "Validated, versioned pipelines (GAMP 5 / CSA)",
            "Compliance": "QA approves every AI draft; Part 11 audit trail",
        },
        "talk": "High value and highly regulated. Lead with control: AI drafts, qualified QA decides, every step sits in the Part 11 audit trail. "
                "The supply-chain half uses mostly public data, so a proof of concept is fast.",
        "questions": [
            "How long does an average deviation investigation take to close?",
            "Any recent 483 observations on investigations or CAPA?",
            "Do you track single-source suppliers and facilities for your key products?",
        ],
        "trigger": "Deviation backlogs, FDA 483s / warning letters, overdue CAPAs, supplier risk, drug shortages",
        "who_to_talk": "VP Quality / QA, Site Heads, Supply Chain, Hospital Pharmacy Directors",
    },
]
