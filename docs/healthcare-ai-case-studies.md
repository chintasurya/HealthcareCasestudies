# Healthcare AI + Knowledge Graph Case Studies

### MedGraph-style blueprints across healthcare domains (built to run on any cloud)

> **What this is:** a research catalog of build-ready case studies that follow the same pattern as
> **MedGraph** (public data → ETL → knowledge graph + vectors → GraphRAG / agentic layer → UI).
> Each one is also mapped onto our **Agentic Factory + data harness** (Salesforce Health Cloud /
> Marketing Cloud, a masked data context, Compliance Guardian, human gates).
>
> **Evidence labels used below:** `[Peer-reviewed]` journal or arXiv study · `[Gov]` regulator or NIH
> source · `[Vendor]` claim made by a vendor or consultancy, not independently checked.
> Treat `[Vendor]` numbers as directional only.

---

## 0. Contents

1. [What MedGraph actually is (the pattern to copy)](#1-what-medgraph-actually-is)
2. [How it maps onto our Agentic Factory](#2-mapping-medgraph-onto-the-agentic-factory)
3. [Healthcare domains to focus on (prioritized list)](#3-healthcare-domains-to-focus-on)
4. [Case studies, one per domain (17 blueprints)](#4-case-studies)
5. [Cloud-agnostic reference stack](#5-cloud-agnostic-reference-stack)
6. [Regulation and governance overlay per domain](#6-regulation-and-governance-overlay)
7. [Recommended portfolio: what to build first](#7-recommended-portfolio)
8. [How to keep finding case studies like this (LinkedIn and GitHub search strings)](#8-how-to-find-more-case-studies)
9. [Sources](#9-sources)

---

## 1. What MedGraph actually is

*(Taken from the MedGraph architecture image. The Medium article could not be fetched from this
environment because `medium.com` is not on the session's network allow-list.)*

| Layer | MedGraph choice | What it does |
|---|---|---|
| **Public data sources** | WHOCC ATC/DDD, NLM MeSH 2026, openFDA Labels, openFDA FAERS, ClinicalTrials.gov, RxNorm + ICD-10-CM | Free, authoritative, regularly refreshed reference data. **No PHI.** |
| **ETL (Python 3.12)** | `load_atc`, `load_mesh`, `ingest_openfda`, `ingest_faers`, `ingest_trials`, `load_rxnorm`, `load_icd`, `compute_similarity`, `embed_nodes` | Loads each source into the graph, resolves identities (RxNorm is the drug "spine"), computes drug-to-drug similarity and node embeddings |
| **Knowledge graph** | Neo4j: about 273K nodes, 302K relationships, 14 vector indexes | `Drug` sits in the middle, linked to ATC class, MeSH term, Label document, FAERS safety, Trials, RxNorm identity, ICD-10 disease |
| **Read and intelligence layer** | FastAPI REST, Graph Assistant (LangGraph, hosted API with Ollama fallback), React + Vite dashboard, Neo4j Browser, natural-language Q&A (GraphRAG) | Agent picks graph queries (Cypher) and/or vector search, then answers with citations |
| **Capabilities** | Graph-assisted search, drug safety, trial intelligence, similar-drug analytics, GraphRAG, agentic AI, ontology-driven design | |

**The reusable recipe:**

1. **Pick one "spine" entity** that everything joins to (MedGraph uses `Drug` keyed by RxNorm RxCUI).
2. **Use public, coded vocabularies as the ontology** (ATC, MeSH, ICD-10, RxNorm), not free text.
3. **Store both structure and meaning.** Graph edges hold facts. Vector indexes on nodes and documents hold meaning.
4. **Let an agent choose the retrieval path** (graph query, vector search, or both) and **cite** every answer back to its source node.
5. **Fall back to a local model** (Ollama) so the platform is not locked to one LLM vendor.

---

## 2. Mapping MedGraph onto the Agentic Factory

| MedGraph layer | Agentic Factory equivalent (our platform) | Gap or addition |
|---|---|---|
| Public data sources | **Context → Sources** (Jira, Confluence, Salesforce, Git, Copado, Drive) **+ GCP BigQuery (masked)** | Add **public healthcare reference data** (RxNorm, ICD-10, NPPES, CMS, openFDA) as a governed source |
| Python ETL | Cloud Workflows + Dispatcher (one agent task per step) | ETL jobs become registered **Tools** in the MCP gateway |
| Neo4j graph | **Spanner Graph (GQL)** knowledge graph | GQL (ISO/IEC 39075) and openCypher are close, so MedGraph queries port with little rework |
| Vector indexes | Cited retrieval (Graph API over MCP) | Add vector search over labels, SOPs and journeys for hybrid GraphRAG |
| LangGraph assistant | Codex engine + Registry (Tools, Skills, Templates) | Same pattern: the agent plans, calls tools, cites |
| No governance layer | **Harness Govern:** Change Guardian, Model Armor, Collibra masking + SDP, Compliance Guardian, human gates H1-H4, evaluation set, observability | **This is our differentiator.** MedGraph is a demo. We ship it governed |
| React dashboard | Salesforce LWC console, Approval page, Tableau review | Business users stay inside Salesforce |

**Positioning line:** *"MedGraph shows what a medical knowledge graph can answer. The Agentic
Factory shows how to let agents act on it inside a regulated enterprise, with minimum-data access,
masked aggregates and human gates."*

---

## 3. Healthcare domains to focus on

You named five domains: **Care Engagement, Medicines Manufacturing, Pharmacy, Medical Devices, IoT
Medical Devices.** These are the right core. The research suggests adding six more where knowledge
graphs and agents pay off and where Salesforce (Health Cloud, Life Sciences Cloud, Marketing Cloud,
Data Cloud) already has a foothold.

### 3.1 Domain list (prioritized)

| # | Domain | Segment (who buys) | Fit with our Salesforce + data-harness skills | Public data available | AI/KG value | Priority |
|---|---|---|---|---|---|---|
| 1 | **Care Engagement and Patient Experience** (care gaps, outreach, journeys, access, navigation) | Provider health systems, payers | ★★★★★ (what we build today) | High (CMS, CDC PLACES, SDOH, NPPES, Synthea) | High | **Tier 1** |
| 2 | **Pharmacy and Medication Management** (med rec, DDI, specialty pharmacy, adherence, prior auth) | Health systems, retail/specialty pharmacy, PBMs | ★★★★ | Very high (RxNorm, DailyMed, openFDA, CPIC) | Very high | **Tier 1** |
| 3 | **Life Sciences Commercial and Patient Services** (HCP engagement, hub services, MLR review) | Pharma and biotech brands | ★★★★★ (Life Sciences Cloud + Marketing Cloud) | High (NPPES, Open Payments, Part D Prescriber) | High | **Tier 1** |
| 4 | **Drug Safety / Pharmacovigilance** | Pharma, CROs, regulators | ★★★★ (adverse-event intake in Service Cloud) | Very high (FAERS, VAERS, labels) | Very high | **Tier 1** |
| 5 | **Medical Devices: Quality and Post-Market Surveillance** | MedTech manufacturers | ★★★★ (complaint handling in Service Cloud) | High (MAUDE, recalls, 510(k), GUDID) | High | **Tier 2** |
| 6 | **Connected / IoT Medical Devices (IoMT, RPM, virtual care)** | Health systems, device makers, RPM vendors | ★★★★ (Health Cloud care plans) | Medium (standards plus synthetic data) | High | **Tier 2** |
| 7 | **Clinical Research and Trials** (feasibility, site selection, recruitment) | Pharma, CROs, academic medical centers | ★★★★ (Life Sciences Cloud clinical) | Very high (ClinicalTrials.gov, AACT) | High | **Tier 2** |
| 8 | **Medicines Manufacturing and Quality (GMP)** | Pharma and CDMO manufacturing | ★★ (needs MES/QMS partners) | Medium (483s, warning letters, recalls) | Very high | **Tier 2** |
| 9 | **Pharma Supply Chain and Drug Shortages** | Manufacturers, distributors, hospital pharmacy | ★★★ | Medium (FDA shortages, NDC, DSCSA) | High | **Tier 3** |
| 10 | **Payer, Utilization Management and Revenue Cycle** (prior auth, denials, coverage policy) | Payers, provider revenue cycle | ★★★★ (Health Cloud UM) | High (LCD/NCD, CARC/RARC, NCCI) | Very high (CMS-0057-F deadline) | **Tier 2** |
| 11 | **Precision Medicine and Genomics** (pharmacogenomics, oncology) | Academic medical centers, oncology networks, labs | ★★ | High (ClinVar, CPIC, PharmGKB) | High | **Tier 3** |
| 12 | **Medical Device Cybersecurity and Clinical Asset Management** | Health system biomedical engineering, device makers | ★★★ (mirrors our Change Guardian) | High (CISA ICSMA, NVD, SBOM) | High | **Tier 3** |

**How to read it:** Tier 1 = build a demo now. Each reuses the Ascension Health Cloud / Marketing
patterns and has rich public data. Tier 2 = strong second wave. Tier 3 = niche or partner-led.

### 3.2 The value chain these domains cover

```
 Discover / Develop            Make / Supply            Market / Engage            Deliver Care              Pay
 ─────────────────────         ──────────────           ────────────────           ─────────────             ─────
 Precision medicine (11)  →    Manufacturing (8)   →    LS Commercial (3)    →     Care Engagement (1)  →    Payer / UM / RCM (10)
 Clinical trials (7)           Supply chain (9)         Patient services (3)       Pharmacy (2)
 Drug safety (4) ───────────── runs across the whole lifecycle ─────────────────── IoMT / RPM (6)
 Device quality (5) ─────────────────────────────────────────────────────────────  Device cyber (12)
```

---

## 4. Case studies

Every case study uses the same template so they can be compared and reused:

> **Problem** · **Users** · **Public data sources** · **Private / masked data** · **Graph model** ·
> **Agents** · **Salesforce surface** · **Guardrails** · **KPIs** · **Prior art / evidence**

---

### Domain 1: Care Engagement and Patient Experience

#### CS-01 · **CareGraph**: care-gap and patient-journey intelligence *(closest to our current build)*

- **Problem:** Health systems run many outreach campaigns (screenings, annual wellness visits,
  chronic care) but cannot explain *why* a cohort has a gap, *which* intervention works for whom,
  or whether outreach is fair across populations.
- **Users:** Population health managers, care coordinators, marketing ops, quality teams.
- **Public data:** CMS eCQM specs (eCQI Resource Center), CMS Care Compare, CDC PLACES
  (county and tract chronic disease prevalence), AHRQ SDOH Database, Area Deprivation Index, NPPES
  (providers), ICD-10-CM, LOINC, SNOMED CT (licence needed), Synthea for synthetic patients.
- **Private / masked data:** EHR care gaps, claims, Marketing Cloud engagement events. These are
  exposed to agents **only as masked BigQuery aggregates** (cohort counts, rates), never row-level PHI.
- **Graph model:**
  `(Measure)-[:REQUIRES]->(Service)`, `(Cohort)-[:HAS_GAP]->(Measure)`,
  `(Cohort)-[:LIVES_IN]->(Geography)-[:HAS_SDOH]->(SDOHFactor)`,
  `(Intervention)-[:TARGETS]->(Measure)`, `(Intervention)-[:USES_CHANNEL]->(Channel)`,
  `(Journey)-[:CONTAINS]->(Intervention)`, `(Provider)-[:PRACTICES_AT]->(Location)`.
- **Agents:**
  1. *Cohort Builder:* natural language to a masked cohort definition, returns counts only.
  2. *Gap Explainer:* GraphRAG over measure specs and SDOH ("why is colorectal screening low in zip X?").
  3. *Journey Designer:* drafts a Marketing Cloud journey (channel, cadence, content brief).
  4. *Compliance Guardian:* checks consent, TCPA and CAN-SPAM rules, PHI in content, and state health-data laws.
  5. *Outcome Evaluator:* compares gap closure across cohorts and flags equity gaps.
- **Salesforce surface:** Health Cloud care programs, Data Cloud segments, Marketing Cloud journeys, Tableau pre-send review.
- **KPIs:** Gap closure rate, appointment conversion, cost per closed gap, opt-out rate, equity gap (difference between top and bottom ADI decile).
- **Prior art:** Salesforce cites 27% better adherence and 29% faster case resolution for Health
  Cloud `[Vendor]`. No independent published case study was found, so **this is white space we can own.**

#### CS-02 · **AccessGraph**: patient access, price transparency and financial navigation

- **Problem:** Patients drop out when they cannot find the right provider, slot or price. Hospital
  price-transparency files are public but nearly unusable as-is.
- **Public data:** CMS Hospital Price Transparency machine-readable files, payer Transparency-in-Coverage
  files, HCPCS, CPT (AMA licence), NCCI edits, NPPES, CMS Doctors and Clinicians.
- **Graph model:** `(Service)-[:BILLED_AS]->(Code)`, `(Hospital)-[:CHARGES {payer, rate}]->(Code)`,
  `(Provider)-[:IN_NETWORK]->(Plan)`, `(Provider)-[:OFFERS]->(Service)`.
- **Agents:** Care Navigator (symptom or service to provider to slot), Price Estimator (shoppable-service
  bundle plus plan rates, with a disclaimer), Financial Assistance screener, Scheduling agent.
- **Salesforce surface:** Health Cloud Intelligent Appointment Management, Experience Cloud patient portal, Agentforce service agent.
- **KPIs:** Booking conversion, abandoned scheduling, estimate accuracy, call deflection.

#### CS-03 · **ReferralGraph**: network integrity and referral leakage

- **Problem:** Health systems lose revenue and care continuity when referrals leave the network.
- **Public data:** NPPES, CMS Medicare Physician and Other Practitioners (utilization by NPI), CMS
  Doctors and Clinicians (affiliations), Care Compare.
- **Private / masked data:** Referral orders and claims, aggregated by provider pair.
- **Graph model:** `(Provider)-[:REFERS_TO {count, specialty}]->(Provider)`, `(Provider)-[:AFFILIATED_WITH]->(System)`.
- **Agents:** Leakage Analyst (community detection and centrality), Physician Liaison briefing agent, Referral Router (in-network suggestion at order time).
- **Salesforce surface:** Health Cloud Provider Relationship Management, Tableau.
- **KPIs:** Leakage percentage, in-network referral rate, liaison visit ROI.

---

### Domain 2: Pharmacy and Medication Management

#### CS-04 · **RxSafeGraph**: medication reconciliation and interaction checking

- **Problem:** Medication lists are messy (free text, brand vs generic, duplicates). Plain LLMs miss
  interactions. A 2024 study found all four LLMs tested missed the metoprolol–verapamil interaction
  `[Peer-reviewed]`. **That is the argument for grounding answers in a graph.**
- **Public data:** RxNorm (the spine, as in MedGraph), DailyMed SPL labels, openFDA drug labels,
  FDA Orange Book, CPIC and PharmGKB (pharmacogenomics), FDA Table of Pharmacogenomic Biomarkers,
  ATC/DDD. AGS Beers Criteria needs a licence.
- **Graph model:** `(Product)-[:HAS_INGREDIENT]->(Ingredient)`, `(Ingredient)-[:INTERACTS_WITH {severity, mechanism, source}]->(Ingredient)`,
  `(Ingredient)-[:CONTRAINDICATED_IN]->(Condition)`, `(Gene)-[:AFFECTS_METABOLISM]->(Ingredient)`, `(Label)-[:WARNS]->(Reaction)`.
- **Agents:** Normalizer (free text to RxCUI; see RxMap), Reconciler (compares home, admission and
  discharge lists using FHIR `MedicationStatement`), Interaction Checker (**deterministic graph lookup
  first**, LLM only explains), Pharmacist Review gate, Patient Education writer (plain language, reading-level checked).
- **Salesforce surface:** Health Cloud medication management, care-plan tasks.
- **KPIs:** Discrepancies caught, pharmacist time per reconciliation, readmissions tied to adverse drug events.
- **Prior art:** Multi-agent prescription verification with knowledge graphs (arXiv 2409.03440)
  `[Peer-reviewed]`. RxMap, LLM-assisted RxNorm normalization (Johns Hopkins) `[Peer-reviewed]`.
  The way FHIR data is serialized changes LLM reconciliation accuracy (arXiv 2604.21076) `[Peer-reviewed]`.

#### CS-05 · **SpecialtyRx Hub**: benefits verification, prior authorization and adherence

- **Problem:** Specialty drugs need benefits investigation, prior authorization (PA), copay
  assistance and adherence support. Each step is a manual handoff. The **CMS Interoperability and
  Prior Authorization Final Rule (CMS-0057-F)** requires payers to stand up a FHIR Prior
  Authorization API with most requirements starting **1 January 2027**, so demand is peaking now.
- **Public data:** CMS Part D formulary files, Medicare Coverage Database (LCDs/NCDs), HL7 Da Vinci
  implementation guides (CRD, DTR, PAS), NCPDP SCRIPT ePA, DailyMed indications, manufacturer copay program rules.
- **Graph model:** `(Drug)-[:ON_FORMULARY {tier, PA, step}]->(Plan)`, `(Policy)-[:REQUIRES]->(Criterion)`,
  `(Criterion)-[:SATISFIED_BY]->(EvidenceType)`, `(Patient)-[:ENROLLED_IN]->(SupportProgram)`.
- **Agents:** Benefits Investigator, PA Packet Builder (maps chart evidence to each criterion and
  cites it), Appeal Drafter, Copay Program Matcher, Adherence Coach (refill-gap nudges through Marketing Cloud).
- **Salesforce surface:** Life Sciences Cloud patient services / Health Cloud, Agentforce, Marketing Cloud.
- **KPIs:** Time to therapy, PA first-pass approval rate, abandonment rate, proportion of days covered (PDC).
- **Prior art:** Availity + Humana + athenahealth end-to-end FHIR PA (non-AI) `[Vendor]`. HL7 commentary
  on agentic AI driving the CRD/DTR/PAS flow `[Gov/standards body]`. AI-written PA letters have strong
  clinical content but weak administrative scaffolding (arXiv 2603.29366) `[Peer-reviewed]`, which is the gap a graph of policy criteria fills.

---

### Domain 3: Life Sciences Commercial and Medical Affairs

#### CS-06 · **HCPGraph**: compliant HCP engagement and next-best-action

- **Problem:** Brand teams want a 360° view of healthcare professionals (HCPs) and next-best-action
  suggestions, but they must stay compliant (Sunshine Act, PhRMA Code, no off-label promotion).
- **Public data:** NPPES (NPI, taxonomy, address), CMS Open Payments (industry payments to HCPs;
  Program Year 2025 published June 2026), Medicare Part D Prescriber (by NPI and drug), CMS Doctors
  and Clinicians, ClinicalTrials.gov investigators, PubMed authorship, DailyMed approved indications.
  **NPI is the join key across all CMS datasets.**
- **Graph model:** `(HCP)-[:PRESCRIBES {volume}]->(Drug)`, `(HCP)-[:RECEIVED_PAYMENT {amount, nature}]->(Company)`,
  `(HCP)-[:INVESTIGATOR_ON]->(Trial)`, `(HCP)-[:AUTHORED]->(Publication)-[:ABOUT]->(Condition)`,
  `(Drug)-[:APPROVED_FOR]->(Indication)`.
- **Agents:** Pre-call Briefing agent, Next-Best-Action recommender, **MLR Pre-Review agent** (flags
  off-label claims against the approved label graph before Medical/Legal/Regulatory review), Medical
  Science Liaison insight summarizer.
- **Salesforce surface:** Life Sciences Cloud for Customer Engagement (GA since October 2025; Pfizer,
  Novartis and Fidia named as adopters `[Vendor]`), Marketing Cloud.
- **KPIs:** Call quality, MLR cycle time, content rejection rate, engagement lift.

---

### Domain 4: Drug Safety / Pharmacovigilance

#### CS-07 · **SignalGraph**: adverse-event intake and safety signal detection *(MedGraph's "Safety (FAERS)" node, grown into a full product)*

- **Problem:** Adverse events arrive through call centers, patient-support programs, social media
  and literature. Case processing is manual, and signal detection is slow.
- **Public data:** openFDA FAERS, VAERS (vaccines), DailyMed and openFDA labels (expected vs
  unexpected reactions), PubMed, WHO VigiAccess. MedDRA needs a licence.
- **Graph model:** MedGraph's `Case` pattern:
  `(Case)-[:INVOLVES]->(Drug)`, `(Case)-[:REPORTS]->(Reaction)`, `(Case)-[:OUTCOME]->(Outcome)`,
  `(Drug)-[:LABELED_REACTION]->(Reaction)`, `(Publication)-[:DESCRIBES]->(DrugReactionPair)`.
- **Agents:** AE Intake agent (detects adverse events in Service Cloud or patient-support conversations
  and builds the four minimum ICSR elements), Duplicate Detector (graph similarity), Signal Detector
  (**PRR/ROR disproportionality calculated in code, not by the LLM**), Literature Screener, Case Narrative drafter, Safety Physician gate.
- **Salesforce surface:** Service Cloud / Health Cloud for intake, handoff to the safety database (Argus, Veeva Vault Safety).
- **KPIs:** Missed AEs in support calls, case processing time, time to signal.
- **Prior art:** GraphRAG with a Llama 3 8B model reached near-perfect accuracy retrieving 19,520
  drug-to-side-effect links (arXiv 2507.13822) `[Peer-reviewed]`. An LLM-built knowledge graph of
  social-media side effects for semaglutide was validated against FAERS (arXiv 2504.04346) `[Peer-reviewed]`.
  Neo4j's tutorial builds an LLM agent over a FAERS graph `[Vendor]`.

---

### Domain 5: Medical Devices (quality and post-market surveillance)

#### CS-08 · **DeviceGraph**: complaint handling and post-market surveillance

- **Problem:** Device makers must triage complaints, decide whether each is FDA-reportable (MDR),
  code it with IMDRF terms, and produce EU MDR trend and PSUR reports. Coding is inconsistent and slow.
- **Public data:** openFDA device event (MAUDE), device recalls and enforcement, 510(k) and PMA,
  device classification and product codes, GUDID / AccessGUDID (UDI), IMDRF adverse-event codes, EUDAMED.
- **Graph model:** `(Device {UDI-DI})-[:HAS_PRODUCT_CODE]->(ProductCode)`, `(Device)-[:CLEARED_VIA]->(510k)-[:PREDICATE]->(510k)`,
  `(Event)-[:INVOLVES]->(Device)`, `(Event)-[:CODED_AS]->(IMDRFCode)`, `(Recall)-[:AFFECTS]->(Device)`.
- **Agents:** Complaint Intake (Service Cloud), Reportability Advisor (decision tree plus cited
  precedent; a human decides), IMDRF Coder, Trend Reporter (EU MDR Article 88), Competitive/Predicate Analyst (510(k) predicate chains).
- **Salesforce surface:** Service Cloud / Health Cloud case management, Tableau.
- **KPIs:** Complaint cycle time, late MDRs, coding consistency, trend detection lead time.
- **Prior art / caution:** A GPT-4 chatbot turns natural-language questions into openFDA MAUDE queries
  (SHTI 2024) `[Peer-reviewed]`. GPT-4 classified 4,459 colonoscopy MAUDE reports `[Peer-reviewed]`. A
  2026 preprint found an open reasoning model agreed with human IMDRF coding only about 59% of the time
  at Level 1 `[Peer-reviewed]`. **Lesson: graph context and human review are required.** Fewer than 23%
  of FDA recalls contain the UDI (AHRMM) `[Gov/industry]`, so entity resolution is a core ETL step.

---

### Domain 6: Connected / IoT Medical Devices (IoMT)

#### CS-09 · **VitalsGraph**: remote patient monitoring and virtual care

- **Problem:** Remote patient monitoring (RPM) produces a flood of readings. Care teams drown in
  alerts, and billing eligibility (days of data, minutes of management) is tracked by hand.
- **Standards and public data:** HL7 FHIR (`Device`, `Observation`), FHIR Personal Health Device IG,
  IEEE 11073, Bluetooth health device profiles, Open mHealth schemas, CMS RPM CPT codes (99453,
  99454, 99457, 99458, plus the CY2026 additions for shorter monitoring periods; check the current
  Physician Fee Schedule), clinical guidelines (for example ACC/AHA blood-pressure thresholds), Synthea for synthetic vitals.
- **Graph model:** `(Patient)-[:USES]->(Device)-[:PRODUCES]->(MetricSeries)`, `(CarePlan)-[:DEFINES]->(Threshold)`,
  `(Threshold)-[:ESCALATES_TO]->(CareTeamRole)`, `(MetricSeries)-[:SUMMARIZED_AS]->(DailySummary)`.
  Raw time series stay in a time-series store. **Only summaries go into the graph.**
- **Agents:** Triage (**rules plus anomaly ML decide; the LLM only explains**), Care Manager Daily
  Brief, Escalation Router, Billing Eligibility Tracker, Patient Coach (nudges through SMS or Marketing Cloud).
- **Salesforce surface:** Health Cloud care plans and timeline, Agentforce, MuleSoft or Data Cloud for device ingestion.
- **KPIs:** Alert volume per nurse, time to escalate, 30-day readmissions, billable-patient percentage, device adherence.
- **Prior art:** Modular RPM architecture with FHIR and IoMT validated in cardiac surgery (Bergamini et al. 2025) `[Peer-reviewed]`.
  Multi-agent RPM framework IoT4Health `[Peer-reviewed]`. Wearable-to-EHR FHIR integration `[Vendor]`.

#### CS-10 · **DeviceShield**: medical device cybersecurity and clinical asset graph

- **Problem:** Hospitals run thousands of networked devices (infusion pumps, imaging) with known
  vulnerabilities and no clear owner. This is the healthcare version of our **Change Guardian**: "who
  owns this asset and what breaks if we patch it?"
- **Public data:** CISA ICS Medical Advisories (ICSMA), NVD CVE and CPE, FDA premarket cybersecurity
  guidance and SBOM requirement (FD&C Act section 524B), MDS2 forms, GUDID, openFDA recalls.
- **Graph model:** `(Asset)-[:IS_MODEL]->(Device)-[:CONTAINS]->(SoftwareComponent)-[:HAS_VULN]->(CVE)`,
  `(Asset)-[:LOCATED_IN]->(Unit)-[:SERVES]->(PatientPopulation)`, `(Asset)-[:OWNED_BY]->(Team)`.
- **Agents:** Vulnerability-to-Asset Matcher, Clinical Impact Reasoner, Patch Plan drafter, Change Guardian approval gate.
- **KPIs:** Mean time to remediate, critical vulnerabilities on life-sustaining devices, unknown-owner assets.

---

### Domain 7: Clinical Research and Trials

#### CS-11 · **TrialGraph**: feasibility, site selection and recruitment

- **Problem:** About 80% of trials miss enrollment timelines (an often-cited industry figure).
  Eligibility criteria are free text, and site selection is based on relationships rather than data.
- **Public data:** ClinicalTrials.gov API v2, AACT (a Postgres copy of ClinicalTrials.gov), PubMed,
  NPPES, CDC PLACES (disease prevalence by geography), OMOP vocabularies (Athena), Synthea.
- **Graph model:** MedGraph's `Clinical Trials` node, extended:
  `(Trial)-[:HAS_CRITERION]->(Criterion)-[:MAPS_TO]->(Concept)`, `(Trial)-[:STUDIES]->(Condition)`,
  `(Trial)-[:RUN_AT]->(Site)-[:STAFFED_BY]->(Investigator)`, `(Geography)-[:PREVALENCE]->(Condition)`.
- **Agents:** Criteria Parser (free text to OMOP concept sets), Feasibility Counter (**returns masked counts
  only**, as in our data harness), Site Recommender, Diversity Planner, Recruitment Journey agent
  (consent-aware outreach in Marketing Cloud), Patient Matcher (TrialGPT-style, explains each criterion).
- **Salesforce surface:** Life Sciences Cloud clinical participant management, Marketing Cloud, Experience Cloud.
- **KPIs:** Screen-fail rate, time to first patient in, enrollment diversity, coordinator hours.
- **Prior art:** NIH's **TrialGPT** retrieves from ClinicalTrials.gov, matches criterion by criterion and
  ranks trials. It reported 87.3% matching accuracy and about 40% less screening time (Nature
  Communications 2024; code at ncbi-nlp/TrialGPT) `[Gov][Peer-reviewed]`. PRISM turns criteria into
  graph-structured questions over EHR data (arXiv 2404.15549) `[Peer-reviewed]`.

---

### Domain 8: Medicines Manufacturing and Quality (GMP)

#### CS-12 · **QualityGraph**: deviation, root cause and CAPA copilot

- **Problem:** Deviation investigations and corrective and preventive actions (CAPAs) take weeks.
  Similar past events are buried in quality-system text, and repeat findings lead to FDA 483 observations and warning letters.
- **Public data:** FDA Form 483 observations and warning letters (FDA Data Dashboard), openFDA drug
  enforcement (recalls), 21 CFR Parts 210, 211 and 11, ICH Q7, Q9(R1) and Q10, EU GMP Annex 11 and draft Annex 22 (AI).
- **Private data:** QMS (deviations, CAPAs, change controls), MES and eBMR, LIMS, SOPs.
- **Graph model:** `(Batch)-[:MADE_ON]->(Equipment)`, `(Batch)-[:USED]->(MaterialLot)-[:FROM]->(Supplier)`,
  `(Deviation)-[:OCCURRED_IN]->(Batch)`, `(Deviation)-[:ROOT_CAUSE]->(Cause)`, `(CAPA)-[:ADDRESSES]->(Cause)`,
  `(SOP)-[:GOVERNS]->(Step)`, `(Observation483)-[:CITES]->(Regulation)`.
- **Agents:** Deviation Triage (criticality), Similar Event Finder (graph plus vector), RCA Drafter
  (5-Whys and fishbone, with citations), CAPA Effectiveness Checker, Regulatory Citation agent
  ("which 483 themes match this?"), QA Approver gate (**AI drafts, qualified QA decides**, as ISPE guidance and draft Annex 22 require).
- **Guardrails:** GxP validation (GAMP 5 2nd edition, FDA Computer Software Assurance), Part 11 audit trail, frozen model versions per validated release.
- **KPIs:** Deviation closure time, repeat deviations, overdue CAPAs, right-first-time batches.
- **Prior art:** 40% shorter deviation closure time reported (McKinsey) `[Vendor]`. Microsoft Copilot
  deviation-investigation example (ISPE) `[Vendor]`. EY's case for bounded, traceable GenAI in GMP `[Vendor]`. 55% faster eBMR review `[Vendor]`.

#### CS-13 · **LabelGraph**: regulatory labeling and submission intelligence

- **Problem:** Safety labeling changes ripple across many products, markets and documents.
- **Public data:** DailyMed SPL (versioned), Drugs@FDA, FDA guidance documents, EMA EPARs, eCTD structure.
- **Agents:** Label Diff agent, Impact Analyzer (which products, markets and patient materials change),
  Health Authority Query Response drafter, Patient Material sync (back into Marketing Cloud content).
- **KPIs:** Label update cycle time, out-of-sync patient materials.

---

### Domain 9: Pharma Supply Chain and Drug Shortages

#### CS-14 · **SupplyGraph**: shortage early warning and therapeutic substitution

- **Problem:** Hospitals find out about shortages late and swap therapies by hand.
- **Public data:** openFDA drug shortages endpoint, NDC Directory, FDA establishment registrations,
  Orange Book (therapeutic equivalence), ATC + RxNorm (alternatives), DSCSA EPCIS serialization (from trading partners), openFDA recalls.
- **Graph model:** `(NDC)-[:PRODUCT_OF]->(Drug)`, `(NDC)-[:MANUFACTURED_AT]->(Facility)-[:IN_COUNTRY]->(Country)`,
  `(Drug)-[:EQUIVALENT_TO]->(Drug)`, `(Drug)-[:SAME_ATC_CLASS]->(Drug)`, `(Shortage)-[:AFFECTS]->(NDC)`.
- **Agents:** Shortage Early Warning (single-source facilities, recalls, warning letters), Substitute
  Finder (equivalence plus formulary plus label checks), P&T Committee brief writer, Clinician alert.
- **KPIs:** Days of warning before stock-out, substitution time, patients affected.
- **Prior art:** A 2025 knowledge graph of German drug-shortage drivers (Eberhardt et al., *International Journal of Production Research*) `[Peer-reviewed]`.
  USP Medicine Supply Map, a graph-based predictive model `[Gov/NGO]`. TraceLink claims 90-day prediction `[Vendor]`.

---

### Domain 10: Payer, Utilization Management and Revenue Cycle

#### CS-15 · **PolicyGraph**: coverage policy, denials and appeals

- **Problem:** Denials are rising. Coverage rules live in PDFs. Appeals are written from scratch.
- **Public data:** Medicare Coverage Database (LCD/NCD), CARC/RARC denial codes, NCCI edits, ICD-10-CM/PCS,
  HCPCS, payer medical policies (public PDFs), Da Vinci CRD/DTR/PAS. InterQual and MCG need licences.
- **Graph model:** `(Policy)-[:COVERS]->(Service)`, `(Policy)-[:REQUIRES]->(Criterion)`, `(Claim)-[:DENIED_WITH]->(CARC)`,
  `(CARC)-[:COMMON_ROOT_CAUSE]->(Cause)`, `(Code)-[:BUNDLES_WITH]->(Code)`.
- **Agents:** Denial Root-Cause Analyst, Appeal Letter drafter (cites policy criteria and chart evidence),
  Pre-bill Coding Validator, Prior Auth Requirement Discovery (CRD).
- **Salesforce surface:** Health Cloud Utilization Management, Service Cloud.
- **KPIs:** Denial rate, overturn rate, days in accounts receivable, PA turnaround (CMS-0057-F metrics are public reporting items).

---

### Domain 11: Precision Medicine and Genomics

#### CS-16 · **PGxGraph**: pharmacogenomics and oncology precision matching

- **Public data:** ClinVar, CPIC guidelines, PharmGKB, CIViC (open cancer variant evidence),
  FDA Pharmacogenomic Biomarkers table, ClinicalTrials.gov (biomarker trials), gnomAD. OncoKB needs a licence.
- **Graph model:** `(Variant)-[:IN_GENE]->(Gene)-[:AFFECTS]->(Drug)`, `(Variant)-[:EVIDENCE {level}]->(Therapy)`, `(Trial)-[:REQUIRES_BIOMARKER]->(Variant)`.
- **Agents:** PGx Alert Explainer, Tumor Board Prep agent, Biomarker Trial Matcher (reuses TrialGraph).
- **KPIs:** Actionable PGx results acted on, tumor board prep time, biomarker-trial referrals.

---

### Cross-domain capstone

#### CS-17 · **Enterprise Healthcare Knowledge Graph** (MedGraph plus everything above)

Combine the spines: **Drug (RxCUI)**, **Device (UDI-DI)**, **Provider (NPI)**, **Condition
(ICD-10/SNOMED)**, **Trial (NCT ID)**, **Facility (FEI/CCN)**, **Geography (FIPS)**. Each case study
above is one "view" over this shared graph, and that reuse is the business case for a platform.

---

## 5. Cloud-agnostic reference stack

Using open query languages (GQL and openCypher), open agent frameworks and an LLM gateway keeps every
case study portable.

| Layer | Google Cloud (Ascension today) | AWS | Azure | Open-source / any cloud |
|---|---|---|---|---|
| Graph database | Spanner Graph (GQL) | Neptune (openCypher) | Cosmos DB for Apache Gremlin | Neo4j (Aura on all 3 clouds), Memgraph |
| Vector search | Vertex AI Vector Search, AlloyDB pgvector | OpenSearch, Aurora pgvector | Azure AI Search | pgvector, Qdrant, Neo4j vector index |
| FHIR store | Cloud Healthcare API | AWS HealthLake | Azure Health Data Services | HAPI FHIR |
| Masked analytics | BigQuery + Sensitive Data Protection + Collibra | Redshift + Comprehend Medical + Lake Formation | Fabric/Synapse + Purview + Health De-identification | Microsoft Presidio, Apache Ranger |
| Orchestration | Cloud Workflows, Firestore checkpoints | Step Functions | Durable Functions, Logic Apps | Temporal, LangGraph checkpointers |
| Agent framework | Agent Development Kit, Codex | Bedrock Agents / AgentCore | Azure AI Foundry Agent Service | **LangGraph**, OpenAI Agents SDK, CrewAI |
| Tools protocol | MCP gateway | MCP | MCP | **MCP** (Model Context Protocol) |
| LLM access | Vertex AI (Gemini, Claude), Codex Enterprise | Bedrock (Claude, Llama, Nova) | Azure OpenAI, Foundry models | LiteLLM gateway, Ollama / vLLM for local fallback (as MedGraph does) |
| Guardrails | Model Armor | Bedrock Guardrails | Azure AI Content Safety | NeMo Guardrails, Guardrails AI |
| Evaluation / observability | Vertex AI evaluation, Cloud Trace | Bedrock evaluations, CloudWatch | Foundry evaluations | LangSmith, Arize Phoenix, Ragas, OpenTelemetry |
| Engagement surface | Salesforce Health Cloud / Life Sciences Cloud / Marketing Cloud / Data Cloud on every cloud | | | |

**Portability rules:**
1. Keep graph queries in **GQL or openCypher**. Avoid vendor-specific extensions in agent tools.
2. Put **every model call behind a gateway** so the model is a configuration setting.
3. Expose data **through MCP tools**, never direct database credentials to agents.
4. Keep the **ontology (codes and relationship types) in Git** as the contract. The database is an implementation detail.

---

## 6. Regulation and governance overlay

| Domain | Key rules the Compliance Guardian must encode | Human gate |
|---|---|---|
| Care engagement | HIPAA (minimum necessary, marketing rules), TCPA, CAN-SPAM, 42 CFR Part 2, state health-data laws (for example Washington's My Health My Data Act), ONC HTI-1 decision-support transparency | Pre-send review (Tableau), H1-H4 |
| Pharmacy | State pharmacy practice acts, FDA clinical decision support guidance (non-device CDS criteria), DEA rules for controlled substances | Pharmacist verification |
| Life sciences commercial | Sunshine Act / Open Payments, PhRMA Code, FDA rules on off-label promotion, OIG anti-kickback | MLR review |
| Pharmacovigilance | 21 CFR 314.80 / 600.80, ICH E2B(R3), EU GVP | Safety physician sign-off |
| Medical devices | 21 CFR 803 (MDR), 820 (QMSR, aligned to ISO 13485 since Feb 2026), EU MDR, ISO 14971, EU AI Act (high-risk AI in devices) | Regulatory/quality decision on reportability |
| IoMT / RPM | FDA SaMD and CDS guidance, CMS RPM billing rules, FDA cybersecurity (524B), HIPAA Security Rule | Clinician escalation decision |
| Clinical trials | 21 CFR 50/56 (consent, IRB), ICH E6(R3) GCP, IRB-approved recruitment materials | IRB-approved content, coordinator |
| Manufacturing | 21 CFR 210/211, Part 11, EU Annex 11 and draft Annex 22 (keeps generative AI out of critical GMP decisions), GAMP 5 / CSA | QA approval |
| Payer / RCM | CMS-0057-F, state prior-auth laws, CMS rules that adverse coverage determinations need clinician review | Clinician reviewer for any denial |

**Shared pattern across all of them (already in our harness):** agents see masked aggregates, AI drafts
and humans decide, every answer is cited to a graph node, and every change has a passport (audit trail).

---

## 7. Recommended portfolio

| Wave | Build | Why first | Reuses from Ascension work |
|---|---|---|---|
| **Wave 1 (now)** | **CS-01 CareGraph** | Direct continuation of our Health Cloud + Marketing work. No published competitor case study found | Masked data context, Compliance Guardian, Journey templates |
| | **CS-04 RxSafeGraph** | Closest to MedGraph (RxNorm spine), all public data, clear safety story ("graphs fix LLM misses") | Spanner Graph, cited retrieval |
| | **CS-06 HCPGraph** | Salesforce Life Sciences Cloud is new (GA October 2025), so pharma buyers are looking now | Marketing Cloud, MLR-style pre-send review |
| **Wave 2** | **CS-05 SpecialtyRx Hub** + **CS-15 PolicyGraph** | CMS-0057-F API deadline of January 2027 creates urgency | Agentforce, human gates |
| | **CS-07 SignalGraph** | Adverse-event capture is required in every patient-support program | Service Cloud intake |
| | **CS-09 VitalsGraph** | RPM growth, Health Cloud care plans | Care plans, escalation |
| | **CS-11 TrialGraph** | Strong public data and NIH TrialGPT precedent | Masked counts, Marketing Cloud recruitment |
| **Wave 3** | CS-08, CS-12, CS-14, CS-10, CS-16 | Need partners (QMS/MES vendors, biomedical engineering) or specialist data | Change Guardian (CS-10) |

**Suggested 6-week demo for Wave 1 (CareGraph + RxSafeGraph on one graph):**
1. Week 1: Ontology in Git (RxNorm, ICD-10, LOINC, eCQM, SDOH, NPPES). Synthea for 50K synthetic patients.
2. Week 2: ETL tools in the MCP gateway (`load_rxnorm`, `ingest_dailymed`, `load_places`, `load_nppes`, `load_ecqm`).
3. Week 3: Spanner Graph schema plus vector indexes on labels and measure specs. Masked aggregate views in BigQuery.
4. Week 4: Agents (Cohort Builder, Gap Explainer, Interaction Checker, Journey Designer) with citations.
5. Week 5: Compliance Guardian rules, Model Armor, evaluation set (100 golden questions with expected cited nodes).
6. Week 6: LWC console plus Tableau pre-send review. Record an end-to-end demo: question → cohort → journey → approval.

---

## 8. How to find more case studies

**LinkedIn search strings** (paste into LinkedIn search, filter by **Posts**, sort by **Latest**):

```
"knowledge graph" AND (healthcare OR pharma OR "life sciences") AND (GraphRAG OR LangGraph OR agentic)
"GraphRAG" AND (FAERS OR openFDA OR RxNorm OR "clinical trials")
("Health Cloud" OR Agentforce) AND ("case study" OR "go-live") AND (patient OR payer OR provider)
("Life Sciences Cloud" OR "Veeva") AND ("next best action" OR HCP) AND AI
("pharmacovigilance" OR "adverse event") AND (LLM OR "generative AI") AND (case study OR deployed)
("MAUDE" OR "post-market surveillance" OR "complaint handling") AND (LLM OR AI agent)
("remote patient monitoring" OR IoMT) AND (FHIR) AND (agent OR LLM)
("GMP" OR "deviation" OR "CAPA") AND ("generative AI" OR "AI agent") AND pharma
("prior authorization" OR "CMS-0057") AND (agentic OR "AI agent") AND FHIR
"Spanner Graph" OR "Neptune" OR "Neo4j" AND (hospital OR pharma OR medtech)
```

**People and pages worth following:** Neo4j Healthcare & Life Sciences, Google Cloud Healthcare & Life
Sciences, AWS for Health, Microsoft Health & Life Sciences, Salesforce Health, Databricks HLS, HL7
Da Vinci Project, NLM / NCBI (TrialGPT team), FDA Digital Health Center of Excellence.

**GitHub and arXiv searches:** `topic:knowledge-graph healthcare`, `GraphRAG medical`, `openFDA langgraph`,
`RxNorm neo4j`, `FHIR MCP server`, arXiv `cs.CL` + "pharmacovigilance" / "medical knowledge graph" / "clinical trial matching".

---

## 9. Sources

**Peer-reviewed / government**
- [NIH: AI algorithm (TrialGPT) matches volunteers to clinical trials](https://www.nih.gov/news-events/news-releases/nih-developed-ai-algorithm-matches-potential-volunteers-clinical-trials) · [TrialGPT code](https://github.com/ncbi-nlp/TrialGPT) · [NIH Record](https://nihrecord.nih.gov/2025/01/03/nih-developed-algorithm-matches-potential-volunteers-clinical-trials) · [BioXconomy summary](https://www.bioxconomy.com/clinical-and-research/ai-tech-trialgpt-can-cut-screening-time-by-40-says-nih)
- [PRISM: patient-trial matching with graph-structured criteria (arXiv 2404.15549)](https://arxiv.org/pdf/2404.15549)
- [RAG-based architectures for drug side-effect retrieval (GraphRAG, arXiv 2507.13822)](https://arxiv.org/abs/2507.13822v1)
- [Crowdsourced drug side-effect knowledge graph, semaglutide (arXiv 2504.04346)](https://arxiv.org/html/2504.04346v2)
- [LLM agent system for prescription verification (arXiv 2409.03440)](https://arxiv.org/pdf/2409.03440)
- [LLMs miss key drug interactions, proof-of-concept (ERCSP 2024)](https://doaj.org/article/e4f6c91c40cc4cddb8cf5736ea04cab5)
- [How FHIR serialization affects LLM medication reconciliation (arXiv 2604.21076)](https://arxiv.org/pdf/2604.21076)
- [RxMap: LLM-assisted medication normalization (Johns Hopkins)](https://pure.johnshopkins.edu/en/publications/rxmap-an-llm-assisted-tool-for-medication-normalization/)
- [AI-generated prior authorization letters (arXiv 2603.29366)](https://arxiv.org/pdf/2603.29366)
- [GPT-4 chatbot over openFDA / MAUDE (SHTI 2024)](https://ebooks.iospress.nl/pdf/doi/10.3233/SHTI240639) · [MAUDE IMDRF LLM benchmark preprint](https://eprints.dkit.ie/1049/1/maudepreproc-aiai26-preprint.pdf) · [SHTI 2025 MAUDE NLP](https://ebooks.iospress.nl/doi/10.3233/SHTI250076)
- [Post-market surveillance of digital therapeutics via MAUDE (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12136109/)
- [AHRMM UDI-DI recall impact summary](https://www.ahrmm.org/system/files/media/file/2021/09/UDI-DI-Recall-Impact-Executive-Summary.pdf)
- [Knowledge graphs for drug-shortage drivers (Eberhardt et al. 2025, IJPR)](https://ideas.repec.org/a/taf/tprsxx/v63y2025i19p7129-7152.html) · [KIT open copy](https://publikationen.bibliothek.kit.edu/1000181579)
- [Modular RPM architecture with FHIR/IoMT (Bergamini et al.)](https://boa.unimib.it/handle/10281/560131) · [IoT4Health multi-agent RPM (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5387113/)
- [HL7 News: agentic AI and Da Vinci burden-reduction APIs](https://hl7news.hl7.org/?p=1277)
- [Harvard ToolUniverse openFDA device tools](https://zitniklab.hms.harvard.edu/ToolUniverse/_modules/tooluniverse/openfda_device_tool.html)

**Vendor / industry (directional only)**
- [Salesforce Life Sciences Cloud for Customer Engagement availability](https://salesforce.com/news/stories/life-sciences-cloud-for-customer-engagement-availability) · [Agentforce for Healthcare & Life Sciences](https://www.salesforce.com/in/healthcare/)
- [Neo4j: knowledge-graph agent over FAERS with Llama 3.1 and LangChain](https://neo4j.com/blog/developer/knowledge-graph-llama-nvidia-langchain/)
- [ISPE: GenAI transforming deviation management](https://ispe.org/pharmaceutical-engineering/ispeak/how-generative-ai-transforming-deviation-management-lessons) · [McKinsey: GenAI in biopharma operations](https://mckinsey.com/industries/life-sciences/our-insights/gen-ai-a-game-changer-for-biopharma-operations) · [EY: AI in GMP](https://www.ey.com/en_ie/insights/ai/ai-in-gmp-creating-bounded-traceable-and-governed-workflows) · [CannyMinds eBMR](https://www.cannymindstech.com/ai-solutions/pharmaceutical)
- [Availity: end-to-end prior auth with FHIR APIs](https://www.availity.com/case-studies/end-to-end-prior-authorizations-using-fhir-apis/) · [CitiusTech Da Vinci ePA case study](https://citiustech.com/hubfs/citiustech-2024/industry-solutions/fhir-based-electronic-prior-authorization-epa/case-study/epa-davinci-burden-reduction-pa.pdf)
- [Open Payments + Part D join on NPI](https://ai-analytics.org/writing/cms-open-payments-part-d/) · [Open Payments 2026 overview](https://intuitionlabs.ai/articles/open-payments-2026-pharma-physician-payments)
- [TraceLink supply chain analytics](https://www.tracelink.com/agile-supply-chain/supply-chain-data-analytics) · [MedevIQ device intelligence](https://medeviq-app.pages.dev/)
- [Providence ambient AI study](https://www.aonl.org/news/Study-analyzes-impact-of-Providences-ambient-AI) · [Kaiser Permanente ambient AI rollout](https://www.beckershospitalreview.com/innovation/kaiser-permanente-expands-ai-scribes-across-40-hospitals-8-states.html)
- [Corti: medication reconciliation with AI agents](https://corti.ai/stories/how-to-automate-medication-reconciliation-with-ai-agents)

**Not reviewed:** the original [MedGraph Medium article](https://medium.com/@aiwithakashgoyal/building-medgraph-a-medical-intelligence-platform-using-neo4j-langgraph-and-graphrag-67dbbf29c194) could not be opened from this environment. Section 1 is based on its architecture image.
