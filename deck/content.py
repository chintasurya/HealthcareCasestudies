"""Slide content for the Insight Global Healthcare AI case-study deck.

All copy lives here so it can be edited without touching layout code.
Value figures are either sourced industry evidence (source given) or a
pilot target, labelled as such. No invented results.
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

PROOF_POINT = ("Proof point: We built a governed agentic delivery platform for a large US health system "
               "(Salesforce Health and Marketing Cloud, masked data context, compliance guardian, human approval gates).")

APPROACH_COLUMNS = [
    ("Data sources", "Public reference data + client systems (EHR, CRM, QMS, devices)"),
    ("Ingest & govern", "ETL, de-identification, masking, consent, data quality"),
    ("Knowledge layer", "Knowledge graph + vector search + masked analytics"),
    ("AI agents", "Specialist agents that plan, cite and hand off to people"),
    ("Experience", "Salesforce, portals, Tableau, existing workflows"),
]
APPROACH_GOVERNANCE = "Governance built in: guardrails in and out · minimum-data access · human approval gates · evaluation sets · full audit trail"
CLOUDS = ["Google Cloud", "AWS", "Azure", "Salesforce"]

ENGAGEMENT_STEPS = [
    ("Ideation workshop · 2 weeks", "Pick the use case, map data and stakeholders, agree success metrics."),
    ("Proof of concept · 6–8 weeks", "Working agents on public and synthetic data, HLD signed off, demo to sponsors."),
    ("Pilot · ~3 months", "Real users, governed client data, measured against the agreed KPIs."),
    ("Scale · ongoing", "Roll out across sites and brands, add the next domain on the same platform."),
]

# --------------------------------------------------------------------------------------
# Sections and case studies
# --------------------------------------------------------------------------------------
SECTIONS = [
    {
        "num": "01",
        "title": "Care Engagement",
        "bg": "bg_section_navy.png",
        "accent": "cyan",
        "stage": "Engage & deliver care",
        "buyers": "Health systems, provider groups, health plans",
        "trigger": "Care gaps, low screening rates, no-shows, outreach that doesn't convert, patient leakage",
        "who": "CMO / CNO, VP Population Health, Patient Access, Marketing",
        "cases": [
            {
                "title": "Intelligent care-gap closure & patient journeys",
                "short": "Care-gap closure & journeys",
                "problem": "Health systems run many outreach campaigns but can't see why a group of patients has a care gap, "
                           "which intervention works for whom, or whether outreach is fair across communities.",
                "who": "Population health, care coordination, marketing ops, quality teams",
                "pains": [
                    "Care gaps and outreach live in separate systems",
                    "Same message to everyone, so low conversion and opt-outs",
                    "Privacy rules slow every new campaign",
                ],
                "facts": [
                    ("27%", "better patient adherence reported by Salesforce Health Cloud customers", "Salesforce (vendor-reported)"),
                ],
                "solution": [
                    "Cohort agent builds patient groups from plain-English questions and returns masked counts, never raw patient data",
                    "Gap explainer links quality measures, social drivers of health and access to explain each gap",
                    "Journey designer drafts personalized Marketing Cloud journeys by channel, timing and content",
                    "Compliance guardian checks consent, HIPAA and TCPA rules before anything is sent",
                ],
                "built_on": ["Health Cloud", "Marketing Cloud", "Data Cloud", "Tableau"],
                "hld": {
                    "sources": ["EHR care gaps & claims", "CMS quality measures", "CDC PLACES / SDOH", "Provider directory (NPPES)", "Engagement history"],
                    "ingest": ["FHIR & claims ETL", "PHI masking", "Consent & preferences", "Identity resolution"],
                    "knowledge": ["Knowledge graph: patient cohort · gap · measure · intervention · channel", "Vector index: measure specs, content", "Masked aggregates"],
                    "agents": ["Cohort builder", "Gap explainer", "Journey designer", "Compliance guardian", "Outcome evaluator"],
                    "experience": ["Health Cloud care programs", "Marketing Cloud journeys", "Tableau pre-send review"],
                },
                "value_headline": "Close more care gaps, with outreach that's personal, fair and compliant.",
                "stats": [
                    ("↑", "Gap-closure rate per campaign", "Pilot target"),
                    ("↓", "Days to launch a compliant campaign", "Pilot target"),
                    ("29%", "faster case resolution reported with Health Cloud", "Salesforce (vendor-reported)"),
                    ("100%", "of sends checked for consent and PHI before release", "Design guarantee"),
                ],
                "benefits": {
                    "Business": "Quality-measure revenue, fewer no-shows, better retention",
                    "Clinical": "Earlier screening and chronic-care follow-up",
                    "IT & data": "One governed data layer reused across campaigns",
                    "Compliance": "Minimum-data access, every send auditable",
                },
                "notes": {
                    "cut": True,
                    "talk": "This is closest to what our core team already delivers for a large US health system. "
                            "The point to land: agents work on masked aggregates, so marketing and population health can move fast without touching raw patient data.",
                    "questions": [
                        "How many outreach campaigns do you run a year, and how do you measure gap closure?",
                        "Which quality programs (HEDIS, Stars, value-based contracts) drive your priorities?",
                        "How long does privacy or compliance review take for a new campaign today?",
                    ],
                },
            },
            {
                "title": "Patient access & financial navigation agent",
                "short": "Access & financial navigation",
                "problem": "Patients drop out when they can't find the right provider, an open slot or a price they understand. "
                           "Price-transparency files are public but nearly impossible for patients to use.",
                "who": "Patient access centers, revenue cycle, digital front door teams",
                "pains": [
                    "Long call-center queues for simple scheduling and price questions",
                    "Estimates are slow, inconsistent or missing",
                    "Patients book outside the network",
                ],
                "facts": [
                    ("Since 2021", "US hospitals must publish machine-readable price files (CMS price transparency rule)", "CMS"),
                ],
                "solution": [
                    "Care navigator matches a symptom or service to the right in-network provider and open slot",
                    "Price estimator combines price-transparency files and plan rates into a plain-language estimate",
                    "Financial-assistance screener checks eligibility and starts the application",
                    "Agent hands complex cases to a human with the full context",
                ],
                "built_on": ["Health Cloud", "Experience Cloud", "Agentforce", "MuleSoft"],
                "hld": {
                    "sources": ["Scheduling system", "Hospital price files", "Payer rate files", "Provider directory", "Charity-care policy"],
                    "ingest": ["Rate-file parsing", "Code mapping (CPT / HCPCS)", "Network & plan rules", "Patient identity"],
                    "knowledge": ["Knowledge graph: service · code · provider · plan · location · rate", "Vector index: policies, FAQs", "Availability cache"],
                    "agents": ["Care navigator", "Price estimator", "Assistance screener", "Scheduling agent", "Human handoff"],
                    "experience": ["Patient portal & mobile", "Contact-center console", "SMS / chat"],
                },
                "value_headline": "Turn the digital front door into booked, in-network, financially clear visits.",
                "stats": [
                    ("↑", "Online booking conversion", "Pilot target"),
                    ("↓", "Calls per booked appointment", "Pilot target"),
                    ("↑", "In-network referrals kept", "Pilot target"),
                    ("24/7", "self-service scheduling and estimates", "Design capability"),
                ],
                "benefits": {
                    "Business": "More booked visits, less leakage, lower call volume",
                    "Clinical": "Patients reach the right care faster",
                    "IT & data": "Reuses directory and scheduling data already in place",
                    "Compliance": "Supports price-transparency and No Surprises Act goals",
                },
                "notes": {
                    "cut": False,
                    "talk": "A practical, fast-ROI use case. Most systems already have the data; what's missing is an agent that joins it up for the patient.",
                    "questions": [
                        "What share of appointments are booked online versus by phone?",
                        "How do patients get cost estimates today, and how accurate are they?",
                        "Do you track network leakage by service line?",
                    ],
                },
            },
        ],
    },
    {
        "num": "02",
        "title": "Life Sciences",
        "bg": "bg_section_magenta.png",
        "accent": "magenta",
        "stage": "Develop & commercialize",
        "buyers": "Pharma, biotech, CROs, academic medical centers",
        "trigger": "Launch planning, HCP engagement, slow MLR review, trial enrollment delays, site selection",
        "who": "Brand / commercial leads, Medical Affairs, Clinical Operations",
        "cases": [
            {
                "title": "Compliant HCP engagement & MLR pre-review",
                "short": "HCP engagement & MLR pre-review",
                "problem": "Brand teams want a 360° view of healthcare professionals (HCPs) and next-best-action guidance, "
                           "but every message must stay on-label and pass Medical-Legal-Regulatory (MLR) review, which takes weeks.",
                "who": "Brand and omnichannel teams, field reps, Medical Affairs, MLR reviewers",
                "pains": [
                    "HCP data is spread across CRM, claims and public sources",
                    "Generic content gets low engagement",
                    "MLR review is a bottleneck for every asset",
                ],
                "facts": [
                    ("$14.67B", "in industry payments to HCPs across 17M records published by CMS Open Payments (Program Year 2025)", "CMS via IntuitionLabs"),
                ],
                "solution": [
                    "HCP 360 links prescribing, payments, trials and publications by NPI",
                    "Pre-call briefing agent gives reps a one-page, compliant summary",
                    "Next-best-action agent suggests channel, content and timing",
                    "MLR pre-review agent flags off-label claims against the approved label before human review",
                ],
                "built_on": ["Life Sciences Cloud", "Marketing Cloud", "Data Cloud", "Agentforce"],
                "hld": {
                    "sources": ["CRM activity", "NPPES (NPI)", "CMS Open Payments", "Medicare Part D prescribers", "Approved labels (DailyMed)"],
                    "ingest": ["NPI identity resolution", "Claims & payments ETL", "Label parsing", "Consent & opt-outs"],
                    "knowledge": ["Knowledge graph: HCP · drug · indication · trial · publication · payment", "Vector index: content & claims library", "Engagement scores"],
                    "agents": ["Pre-call briefing", "Next-best-action", "MLR pre-review", "MSL insight summarizer"],
                    "experience": ["Life Sciences Cloud console", "Marketing Cloud", "MLR workflow (e.g. Veeva PromoMats)"],
                },
                "value_headline": "More relevant HCP engagement, and faster, safer content approval.",
                "stats": [
                    ("↓", "MLR cycle time per asset", "Pilot target"),
                    ("↓", "Content rejected for off-label claims", "Pilot target"),
                    ("↑", "HCP engagement rate", "Pilot target"),
                    ("Oct 2025", "Life Sciences Cloud for Customer Engagement went GA", "Salesforce"),
                ],
                "benefits": {
                    "Business": "Faster launches, better rep productivity",
                    "Clinical": "Accurate, on-label information reaches HCPs",
                    "IT & data": "One HCP graph across brands",
                    "Compliance": "Sunshine Act and PhRMA Code guardrails built in",
                },
                "notes": {
                    "cut": True,
                    "talk": "Life Sciences Cloud is new and pharma is actively rebuilding its commercial stack, so the timing is good. "
                            "Lead with MLR pre-review: it's a pain every brand team feels.",
                    "questions": [
                        "Are you moving from Veeva CRM to Salesforce Life Sciences Cloud, or evaluating it?",
                        "How long does an asset take to get through MLR today?",
                        "How do reps prepare for HCP calls?",
                    ],
                },
            },
            {
                "title": "Clinical trial feasibility & patient recruitment",
                "short": "Trial feasibility & recruitment",
                "problem": "Most trials miss enrollment timelines. Eligibility criteria are free text, sites are chosen on relationships, "
                           "and coordinators screen patients by hand.",
                "who": "Clinical operations, feasibility teams, site networks, CRO partners",
                "pains": [
                    "Manual chart screening against long criteria lists",
                    "Site selection not grounded in patient data",
                    "Under-representation of diverse patients",
                ],
                "facts": [
                    ("~40%", "less screening time with NIH's TrialGPT at matching accuracy close to experts (87.3%)", "NIH, Nature Communications 2024"),
                ],
                "solution": [
                    "Criteria parser turns free-text eligibility into coded concept sets",
                    "Feasibility agent returns masked patient counts by site and region",
                    "Site recommender ranks sites by patient pool, past performance and diversity",
                    "Patient matcher explains each criterion; recruitment journeys run with consent",
                ],
                "built_on": ["Life Sciences Cloud", "Marketing Cloud", "Experience Cloud"],
                "hld": {
                    "sources": ["ClinicalTrials.gov", "EHR / OMOP data (masked)", "CDC PLACES prevalence", "Investigator directory", "PubMed"],
                    "ingest": ["Criteria NLP to OMOP concepts", "De-identification", "Site & investigator linking", "Consent capture"],
                    "knowledge": ["Knowledge graph: trial · criterion · concept · site · investigator · region", "Vector index: protocols", "Masked counts"],
                    "agents": ["Criteria parser", "Feasibility counter", "Site recommender", "Patient matcher", "Recruitment journey"],
                    "experience": ["Feasibility dashboard", "Coordinator console", "Participant portal"],
                },
                "value_headline": "Find the right sites and patients faster, with every match explained.",
                "stats": [
                    ("~40%", "less clinician screening time (TrialGPT)", "NIH 2024"),
                    ("87.3%", "patient-to-trial matching accuracy (TrialGPT)", "NIH 2024"),
                    ("↓", "Time to first patient in", "Pilot target"),
                    ("↑", "Enrollment diversity", "Pilot target"),
                ],
                "benefits": {
                    "Business": "Shorter trials, earlier revenue, fewer rescue sites",
                    "Clinical": "More patients offered relevant trials",
                    "IT & data": "Reusable criteria and site graph across studies",
                    "Compliance": "Masked counts only; IRB-approved outreach",
                },
                "notes": {
                    "cut": False,
                    "talk": "Strong public evidence here (NIH TrialGPT), so this is easy to defend in front of a sponsor. "
                            "Also works for health systems that run research programs.",
                    "questions": [
                        "Which studies are behind on enrollment right now?",
                        "How are feasibility and site selection done today?",
                        "Do you have EHR data in OMOP or FHIR form for research?",
                    ],
                },
            },
        ],
    },
    {
        "num": "03",
        "title": "Pharmacy & Drug",
        "bg": "bg_section_gold.png",
        "accent": "yellow",
        "stage": "Dispense & manage medications",
        "buyers": "Health-system pharmacy, specialty pharmacy, PBMs, pharma patient-services hubs",
        "trigger": "Medication errors, prior-auth backlogs, CMS-0057-F, adherence, adverse-event capture",
        "who": "Chief Pharmacy Officer, VP Patient Services, Drug Safety",
        "cases": [
            {
                "title": "Medication reconciliation & interaction safety",
                "short": "Med reconciliation & interaction safety",
                "problem": "Medication lists are messy: free text, brand versus generic, duplicates. Pharmacists reconcile them by hand, "
                           "and general-purpose AI models miss dangerous interactions.",
                "who": "Hospital pharmacists, transitions-of-care nurses, ambulatory clinics",
                "pains": [
                    "Time-consuming reconciliation at admission and discharge",
                    "Interaction alerts are noisy, so real risks get missed",
                    "Adverse drug events drive readmissions",
                ],
                "facts": [
                    ("4 of 4", "AI models tested missed the metoprolol–verapamil interaction in a 2024 study, which is why answers must be grounded", "ERCSP 2024"),
                ],
                "solution": [
                    "Normalizer maps any free-text drug name to a standard drug code (RxNorm)",
                    "Reconciler compares home, admission and discharge lists and flags discrepancies",
                    "Interaction checker uses a curated drug knowledge graph first; AI only explains",
                    "Pharmacist approves; patient-friendly instructions generated at the right reading level",
                ],
                "built_on": ["Health Cloud", "EHR integration (FHIR)", "Agentforce"],
                "hld": {
                    "sources": ["EHR medication lists (FHIR)", "RxNorm", "FDA labels (DailyMed)", "Pharmacogenomics (CPIC)", "Pharmacy claims"],
                    "ingest": ["Drug-name normalization", "Label & interaction ETL", "Patient matching", "PHI controls"],
                    "knowledge": ["Knowledge graph: product · ingredient · interaction · condition · gene", "Vector index: label text", "Rules engine"],
                    "agents": ["Normalizer", "Reconciler", "Interaction checker", "Pharmacist review gate", "Patient educator"],
                    "experience": ["Pharmacist worklist", "EHR / Health Cloud", "Discharge instructions"],
                },
                "value_headline": "Safer medication lists in minutes, with every alert traceable to its source.",
                "stats": [
                    ("↓", "Pharmacist minutes per reconciliation", "Pilot target"),
                    ("↑", "Discrepancies caught before discharge", "Pilot target"),
                    ("↓", "Readmissions linked to adverse drug events", "Pilot target"),
                    ("100%", "of interaction answers cited to a source", "Design guarantee"),
                ],
                "benefits": {
                    "Business": "Fewer readmissions and penalties, pharmacist capacity freed",
                    "Clinical": "Fewer adverse drug events",
                    "IT & data": "Standard drug codes reused across apps",
                    "Compliance": "Human verification on every change",
                },
                "notes": {
                    "cut": True,
                    "talk": "The story: plain chatbots get drug interactions wrong; a graph of trusted drug data plus a pharmacist gate gets them right. "
                            "That is exactly our grounded-AI capability.",
                    "questions": [
                        "Who does medication reconciliation today, and how long does it take?",
                        "How noisy are your interaction alerts?",
                        "Are adverse drug events a readmission driver for you?",
                    ],
                },
            },
            {
                "title": "Specialty pharmacy hub: benefits, prior auth & adherence",
                "short": "Specialty Rx hub & prior auth",
                "problem": "Specialty drugs need benefits checks, prior authorization, copay help and adherence support. "
                           "Each step is a manual handoff, so patients wait weeks or abandon therapy.",
                "who": "Pharma patient-services hubs, specialty pharmacies, provider prior-auth teams",
                "pains": [
                    "Prior-auth packets assembled by hand from charts",
                    "Denials and appeals drafted from scratch",
                    "Adverse events in support calls can be missed",
                ],
                "facts": [
                    ("Jan 2027", "CMS-0057-F requires impacted payers to offer a FHIR prior-authorization API (most requirements from Jan 1, 2027)", "CMS Interoperability & Prior Authorization Final Rule"),
                ],
                "solution": [
                    "Benefits investigator checks coverage, formulary tier and requirements",
                    "Prior-auth builder maps chart evidence to each payer criterion, with citations",
                    "Appeal drafter and copay-program matcher remove manual rework",
                    "Adherence coach nudges refills; adverse-event detector flags safety reports in calls",
                ],
                "built_on": ["Life Sciences Cloud / Health Cloud", "Service Cloud", "Marketing Cloud", "Agentforce"],
                "hld": {
                    "sources": ["Payer formularies (CMS Part D)", "Coverage policies (LCD/NCD)", "Da Vinci FHIR APIs", "Patient-support calls", "Copay program rules"],
                    "ingest": ["Policy-to-criteria parsing", "Chart evidence extraction", "Call transcription", "PHI controls"],
                    "knowledge": ["Knowledge graph: drug · plan · policy · criterion · evidence · program", "Vector index: policies", "Case history"],
                    "agents": ["Benefits investigator", "Prior-auth builder", "Appeal drafter", "Adherence coach", "Adverse-event detector"],
                    "experience": ["Hub case console", "Provider portal", "Patient SMS / app"],
                },
                "value_headline": "Get patients on therapy faster and keep them there.",
                "stats": [
                    ("↓", "Days from prescription to first fill", "Pilot target"),
                    ("↑", "Prior-auth first-pass approval", "Pilot target"),
                    ("↑", "Proportion of days covered (adherence)", "Pilot target"),
                    ("Jan 2027", "CMS prior-authorization API deadline drives demand now", "CMS-0057-F"),
                ],
                "benefits": {
                    "Business": "Less abandonment, more patients on therapy",
                    "Clinical": "Faster access to specialty treatment",
                    "IT & data": "FHIR-ready for the CMS prior-auth APIs",
                    "Compliance": "Adverse events captured and routed to drug safety",
                },
                "notes": {
                    "cut": False,
                    "talk": "Timely because of the CMS prior-auth rule. Works for three buyer types: pharma hubs, specialty pharmacies and provider prior-auth teams.",
                    "questions": [
                        "How long from prescription to first fill for your specialty patients?",
                        "How many prior auths a month, and what's the first-pass approval rate?",
                        "How are adverse events in support calls captured today?",
                    ],
                },
            },
        ],
    },
    {
        "num": "04",
        "title": "Medical Devices & IoT",
        "bg": "bg_section_navy.png",
        "accent": "cyan",
        "stage": "Monitor devices & patients",
        "buyers": "MedTech manufacturers, health systems, remote-monitoring providers",
        "trigger": "Complaint backlogs, FDA / EU MDR reporting, recalls, remote monitoring programs, alert fatigue",
        "who": "VP Quality / Regulatory, Post-Market Surveillance, Virtual Care leaders",
        "cases": [
            {
                "title": "Complaint handling & post-market surveillance",
                "short": "Device complaints & surveillance",
                "problem": "Device makers must triage every complaint, decide whether it's reportable to FDA, code it consistently "
                           "and spot trends early. Today that's manual, slow and inconsistent.",
                "who": "Complaint handling, post-market surveillance, regulatory affairs, quality",
                "pains": [
                    "Complaint backlogs and late FDA reports",
                    "Inconsistent adverse-event coding",
                    "Trends spotted after a recall, not before",
                ],
                "facts": [
                    ("2M+", "medical device reports received by FDA each year (MAUDE)", "FDA"),
                ],
                "solution": [
                    "Intake agent structures complaints from calls, email and service records",
                    "Reportability advisor suggests the FDA / EU MDR decision with cited precedent; a person decides",
                    "Coding agent applies standard adverse-event codes (IMDRF)",
                    "Trend agent watches MAUDE, recalls and internal data for early signals",
                ],
                "built_on": ["Service Cloud", "Health Cloud", "Tableau"],
                "hld": {
                    "sources": ["Complaints & service cases", "FDA MAUDE & recalls", "510(k) / PMA records", "UDI database (GUDID)", "IMDRF code sets"],
                    "ingest": ["UDI entity resolution", "Narrative NLP", "Product-code mapping", "Quality-system sync"],
                    "knowledge": ["Knowledge graph: device · UDI · event · code · recall · predicate", "Vector index: narratives", "Trend statistics"],
                    "agents": ["Complaint intake", "Reportability advisor", "IMDRF coder", "Trend detector", "Regulatory reviewer gate"],
                    "experience": ["Service Cloud case console", "Quality system", "Tableau trend reports"],
                },
                "value_headline": "Faster, more consistent complaint handling and earlier safety signals.",
                "stats": [
                    ("↓", "Complaint cycle time", "Pilot target"),
                    ("0", "late FDA reports (goal)", "Pilot target"),
                    ("~59%", "agreement for an unaided AI model with human coding, which is why graph + human review matter", "2026 MAUDE study (preprint)"),
                    ("↑", "Trend detection lead time", "Pilot target"),
                ],
                "benefits": {
                    "Business": "Lower cost of quality, fewer surprise recalls",
                    "Clinical": "Patient-safety issues found earlier",
                    "IT & data": "One device graph linking UDI, complaints and recalls",
                    "Compliance": "21 CFR 803, EU MDR vigilance and audit trail",
                },
                "notes": {
                    "cut": True,
                    "talk": "Regulated, high-volume and text-heavy: a sweet spot for grounded AI. Be clear that people make the reportability decision; the AI prepares it.",
                    "questions": [
                        "How many complaints a month, and what's the current backlog?",
                        "Have you had late MDRs or FDA observations on complaint handling?",
                        "Is complaint intake in Salesforce or another system?",
                    ],
                },
            },
            {
                "title": "Remote patient monitoring & connected devices",
                "short": "Remote patient monitoring",
                "problem": "Connected devices create a flood of readings. Care teams drown in alerts, and billing rules "
                           "(days of data, minutes of care) are tracked by hand.",
                "who": "Virtual care and RPM programs, care managers, device and RPM vendors",
                "pains": [
                    "Alert fatigue hides the patients who need help",
                    "Device data isn't in the care team's workflow",
                    "Revenue lost when billing requirements aren't tracked",
                ],
                "facts": [
                    ("16 days", "of readings per 30-day period required for the core RPM billing code (CMS adds shorter-period codes for 2026)", "CMS Physician Fee Schedule"),
                ],
                "solution": [
                    "Devices stream into a standard FHIR format; only daily summaries go into the graph",
                    "Triage uses clinical rules and anomaly models to decide; AI writes the explanation",
                    "Care-manager daily brief and escalation routing to the right role",
                    "Billing tracker and patient coaching nudges keep programs on track",
                ],
                "built_on": ["Health Cloud", "MuleSoft / Data Cloud", "Agentforce", "Marketing Cloud"],
                "hld": {
                    "sources": ["Wearables & home devices", "Device clouds (BLE / IEEE 11073)", "EHR care plans", "Clinical thresholds", "Billing rules"],
                    "ingest": ["IoT gateway & FHIR mapping", "Time-series store", "Daily summaries", "Device-patient pairing"],
                    "knowledge": ["Knowledge graph: patient · device · metric · threshold · care plan · care team", "Anomaly models", "Billing ledger"],
                    "agents": ["Triage", "Care-manager brief", "Escalation router", "Billing tracker", "Patient coach"],
                    "experience": ["Health Cloud care timeline", "Nurse worklist", "Patient app / SMS"],
                },
                "value_headline": "Fewer, better alerts and a remote-monitoring program that pays for itself.",
                "stats": [
                    ("↓", "Alerts per nurse per day", "Pilot target"),
                    ("↓", "Time to escalate a high-risk reading", "Pilot target"),
                    ("↑", "Patients meeting billing requirements", "Pilot target"),
                    ("↓", "30-day readmissions in enrolled cohorts", "Pilot target"),
                ],
                "benefits": {
                    "Business": "Billable, scalable virtual-care revenue",
                    "Clinical": "Earlier intervention, fewer readmissions",
                    "IT & data": "Standards-based device integration (FHIR)",
                    "Compliance": "Clinician decides; FDA decision-support guidance respected",
                },
                "notes": {
                    "cut": False,
                    "talk": "The IoT story. The key design choice: rules and models make the clinical call, and AI explains, so it stays safe and auditable.",
                    "questions": [
                        "How many patients are in remote monitoring today, and with which devices?",
                        "How many alerts does a nurse handle per day?",
                        "Are you capturing all the RPM billing you're eligible for?",
                    ],
                },
            },
        ],
    },
    {
        "num": "05",
        "title": "Manufacturing & Supply Chain",
        "bg": "bg_section_magenta.png",
        "accent": "magenta",
        "stage": "Make & supply",
        "buyers": "Pharma and biotech manufacturing, CDMOs, distributors, hospital pharmacy",
        "trigger": "Deviation backlogs, FDA 483s / warning letters, CAPA overdue, drug shortages, supplier risk",
        "who": "VP Quality / QA, Site Heads, Supply Chain, Hospital Pharmacy Directors",
        "cases": [
            {
                "title": "GMP deviation & CAPA investigation copilot",
                "short": "Deviation & CAPA copilot",
                "problem": "Deviation investigations and corrective actions (CAPAs) take weeks. Similar past events are buried in quality records, "
                           "and repeat findings lead to FDA observations and warning letters.",
                "who": "QA investigators, site quality heads, manufacturing engineers",
                "pains": [
                    "Investigations start from a blank page",
                    "Repeat deviations because root causes aren't connected",
                    "Overdue CAPAs and inspection risk",
                ],
                "facts": [
                    ("40%", "reduction in deviation closure time reported in industry GenAI case studies", "McKinsey (vendor-reported)"),
                ],
                "solution": [
                    "Triage agent sets criticality and routes the deviation",
                    "Similar-event finder links batch, equipment, material lot and past root causes",
                    "Root-cause drafter writes the 5-Whys / fishbone with citations; QA decides",
                    "CAPA checker tracks effectiveness and matches FDA 483 themes",
                ],
                "built_on": ["Quality system (e.g. Veeva Vault QMS)", "MES / LIMS integration", "Any cloud"],
                "hld": {
                    "sources": ["Deviations, CAPAs, change controls", "MES / eBMR & LIMS", "SOPs", "FDA 483s & warning letters", "GMP regulations (21 CFR 210/211, ICH)"],
                    "ingest": ["Quality-record ETL", "Batch genealogy", "SOP chunking", "Validated, versioned pipelines"],
                    "knowledge": ["Knowledge graph: batch · equipment · lot · deviation · cause · CAPA · SOP", "Vector index: investigations", "Regulation library"],
                    "agents": ["Deviation triage", "Similar-event finder", "Root-cause drafter", "CAPA effectiveness", "QA approval gate"],
                    "experience": ["Quality system workflow", "Investigator workbench", "Quality dashboards"],
                },
                "value_headline": "Close investigations faster and stop repeat deviations, with QA always in control.",
                "stats": [
                    ("40%", "faster deviation closure reported in industry case studies", "McKinsey (vendor-reported)"),
                    ("↓", "Repeat deviations", "Pilot target"),
                    ("↓", "Overdue CAPAs", "Pilot target"),
                    ("100%", "of AI drafts approved by qualified QA (Part 11 audit trail)", "Design guarantee"),
                ],
                "benefits": {
                    "Business": "More right-first-time batches, less lost product",
                    "Clinical": "Consistent product quality for patients",
                    "IT & data": "Validated, versioned AI aligned to GAMP 5 / CSA",
                    "Compliance": "Inspection-ready; aligned to Part 11, Annex 11 and draft Annex 22 (AI)",
                },
                "notes": {
                    "cut": True,
                    "talk": "High value but highly regulated. Lead with control: AI drafts, qualified QA decides, every step is in the Part 11 audit trail.",
                    "questions": [
                        "How long does an average deviation investigation take to close?",
                        "Any recent 483 observations on investigations or CAPA?",
                        "Which quality system and MES do you run?",
                    ],
                },
            },
            {
                "title": "Drug shortage early warning & supply resilience",
                "short": "Shortage early warning",
                "problem": "Hospitals and manufacturers learn about shortages late. Finding a safe substitute and re-planning supply is manual and slow.",
                "who": "Hospital pharmacy and supply chain, manufacturer supply planning, distributors",
                "pains": [
                    "Little warning before stock-outs",
                    "Single-source suppliers and facilities are hidden risks",
                    "Therapeutic substitution decided under pressure",
                ],
                "facts": [
                    ("323", "active US drug shortages in Q1 2024, an all-time high", "ASHP"),
                ],
                "solution": [
                    "Early-warning agent watches FDA shortages, recalls, warning letters and supplier signals",
                    "Risk map links each product to manufacturer, facility and country",
                    "Substitute finder checks equivalence, formulary and label before suggesting options",
                    "Brief writer prepares Pharmacy & Therapeutics committee and clinician alerts",
                ],
                "built_on": ["Any cloud", "Tableau", "Health Cloud / Service Cloud alerts"],
                "hld": {
                    "sources": ["FDA drug shortages & recalls", "NDC directory", "Facility registrations", "Orange Book equivalence", "Inventory & purchasing"],
                    "ingest": ["NDC & facility linking", "Supplier signals", "Inventory sync", "Equivalence mapping"],
                    "knowledge": ["Knowledge graph: NDC · drug · manufacturer · facility · country · substitute", "Risk scores", "Formulary"],
                    "agents": ["Shortage early warning", "Supplier risk", "Substitute finder", "P&T brief writer", "Pharmacist approval"],
                    "experience": ["Supply dashboard", "Pharmacy alerts", "Clinician notifications"],
                },
                "value_headline": "See shortages coming and keep patients on safe therapy.",
                "stats": [
                    ("↑", "Days of warning before stock-out", "Pilot target"),
                    ("↓", "Time to approve a substitute", "Pilot target"),
                    ("↓", "Patients affected by stock-outs", "Pilot target"),
                    ("323", "active US shortages at the Q1 2024 peak", "ASHP"),
                ],
                "benefits": {
                    "Business": "Less emergency buying, lower waste",
                    "Clinical": "Continuity of care during shortages",
                    "IT & data": "Product-to-facility graph reused for supplier risk",
                    "Compliance": "Pharmacist approves every substitution",
                },
                "notes": {
                    "cut": False,
                    "talk": "Resonates with both hospitals and manufacturers. Mostly public data, so a proof of concept is fast.",
                    "questions": [
                        "How did the last major shortage affect you, and how early did you know?",
                        "How are substitutes approved today?",
                        "Do you track single-source suppliers and facilities?",
                    ],
                },
            },
        ],
    },
]
