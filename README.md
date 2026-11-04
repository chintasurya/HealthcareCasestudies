# Healthcare Case Studies

Research on case studies that follow the **MedGraph** pattern (public data → knowledge graph +
vectors → GraphRAG / agents) across healthcare domains, mapped onto the Agentic Factory
(Salesforce Health Cloud / Marketing Cloud + governed data harness). Every case study is designed
to run on any cloud.

**Main document:** [`docs/healthcare-ai-case-studies.md`](docs/healthcare-ai-case-studies.md)

## Domains covered

| Tier | Domain | Case studies |
|---|---|---|
| 1 | Care Engagement and Patient Experience | CS-01 CareGraph, CS-02 AccessGraph, CS-03 ReferralGraph |
| 1 | Pharmacy and Medication Management | CS-04 RxSafeGraph, CS-05 SpecialtyRx Hub |
| 1 | Life Sciences Commercial and Medical Affairs | CS-06 HCPGraph |
| 1 | Drug Safety / Pharmacovigilance | CS-07 SignalGraph |
| 2 | Medical Devices: Quality and Post-Market | CS-08 DeviceGraph |
| 2 | Connected / IoT Medical Devices (IoMT, RPM) | CS-09 VitalsGraph, CS-10 DeviceShield |
| 2 | Clinical Research and Trials | CS-11 TrialGraph |
| 2 | Medicines Manufacturing and Quality (GMP) | CS-12 QualityGraph, CS-13 LabelGraph |
| 2 | Payer, Utilization Management and Revenue Cycle | CS-15 PolicyGraph |
| 3 | Pharma Supply Chain and Drug Shortages | CS-14 SupplyGraph |
| 3 | Precision Medicine and Genomics | CS-16 PGxGraph |
| — | Cross-domain capstone | CS-17 Enterprise Healthcare Knowledge Graph |

## Capabilities deck (Insight Global template)

- **Deck:** [`deck/IG_Healthcare_AI_Case_Studies.pptx`](deck/IG_Healthcare_AI_Case_Studies.pptx) (23 slides, speaker notes with talk track and discovery questions)
- **Preview:** [`deck/IG_Healthcare_AI_Case_Studies_preview.pdf`](deck/IG_Healthcare_AI_Case_Studies_preview.pdf) (rendered with a substitute font; the .pptx uses Trenda IG Text)
- Five knowledge-graph platforms, one per domain, each in 3 slides (problem & solution → architecture → value):
  **CareGraph** (Care Engagement), **TherapyGraph** (Life Sciences), **RxGraph** (Pharmacy & Drug),
  **DeviceGraph** (Medical Devices & IoT), **ChainGraph** (Manufacturing & Supply Chain)
- Icons: [Lucide](https://lucide.dev) (ISC license), rendered to PNG in `deck/assets/icons/`
- Edit copy in `deck/content.py`, then rebuild:

```bash
python3 deck/extract_assets.py /path/to/PowerPoint_Template.pdf
python3 deck/build_deck.py --icons /path/to/node_modules/lucide-static/icons
```
