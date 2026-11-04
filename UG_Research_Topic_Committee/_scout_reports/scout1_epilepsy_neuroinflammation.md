# Topic-selection committee report: epilepsy / neuroinflammation / neuroimmunology

**Process note:** 19 productive WebSearch calls. The session's shared web-search budget was exhausted before I could run ~6 planned confirmatory lookups (author lists for two papers, a bEnd.3 BBB feasibility check, a P2RX7 single-cell expression check, and the human-hippocampus snRNA-seq accession hunt). Everything below is tagged for verification status, and the gaps are flagged as such rather than filled from memory. Nothing is fabricated; where I could not capture a PMID/DOI I say so and give no digits.

**Headline judgment up front.** This domain offers an undergraduate with these resources *almost no path* to a competitive mechanism paper — the mechanism race now requires conditional knockouts, EEG telemetry, and in vivo imaging (see landscape). But it offers two unusually good paths that most labs will not take: (1) **validity audits** of assumptions the field has built on without testing, and (2) **public human genetics**, which in epilepsy neuroimmunology is strikingly underused relative to how crowded the rodent literature is. All five surviving topics sit in those two lanes. I killed every topic that required the student to compete on mechanism.

I deliver **5 topics**, not 6. A sixth (brain-endothelial vs neuronal IL-1β competence head-to-head) did not survive as a standalone: the decisive in vivo experiment was already published (endothelial *Il1r1* conditional knockout attenuates seizures, Mol Neurobiol 2024, PMID 38087170), and what remains needs Transwell/TEER infrastructure I could not verify the student has. I folded its useful part into Topic 1 as an optional arm.

---

## A universal feasibility constraint the student must accept before reading further

HT-22 is an immortalized mouse hippocampal line that **cannot fire action potentials and, undifferentiated, lacks functional NMDA receptors** (Sci Rep 2023, DOI 10.1038/s41598-023-34183-y; PMID 25206424 shows NMDAR characteristics appear only after differentiation). Three consequences, which I apply to every wet topic below:

- There is **no such thing as an "in vitro epilepsy model" in HT-22**. The published HT-22 "epilepsy" papers all use glutamate or kainate excitotoxicity as a surrogate (Heliyon 2023; Neurochem Res 2025, DOI 10.1007/s11064-025-04372-4). The Mg²⁺-free epileptiform model is **mechanistically unusable** in undifferentiated HT-22, because that model works by relieving the Mg²⁺ block of NMDA receptors (Sci Rep 2021, DOI 10.1038/s41598-021-90486-y) — receptors these cells do not have. The student must call their challenge "excitotoxic/injury stress," not "seizure," in the title and abstract, or a competent reviewer will reject on that alone.
- HT-22 is useful here precisely for **expression-competence and antibody-specificity questions**, which do not require electrical activity. That is why all three wet topics are framed that way.
- HT-22 also differs substantially from primary hippocampal neurons (PLoS One, DOI 10.1371/journal.pone.0326401, notes it is unclear whether HT-22 resemble progenitors or mature neurons). Every claim must be worded as being about "a hippocampal neuronal line," with a public-data arm carrying the generalization.

---

# TOPIC 1 — IL-1 receptor accessory protein isoform ratio as the gate on direct IL-1β action on hippocampal neurons

**1. title_en**
"Seizure-associated reconfiguration of neuronal IL-1 receptor accessory protein isoforms (AcP vs AcPb): a candidate gate on direct interleukin-1β signalling in hippocampal neurons"

**2. core_question**
Does excitotoxic/epileptogenic stress shift the neuronal *Il1rap* isoform ratio away from the CNS-restricted AcPb isoform toward canonical AcP, and does that shift determine which IL-1β signalling branch (p38/Src vs NF-κB) a hippocampal neuron can execute?

**3. hypothesis**
Hippocampal neurons are constitutively AcPb-dominant, which permits non-transcriptional IL-1β signalling (Src/p38) but not canonical NF-κB signalling. Epileptogenic stress raises the AcP:AcPb ratio, converting neurons into partial canonical IL-1 responders — and this ratio, not IL-1R1 abundance, is the rate-limiting variable in "direct neuronal IL-1β action."

**4. novelty_claim**
This adjudicates a flat contradiction between two large literatures that cite each other without resolving it. The epilepsy/neuroinflammation field asserts IL-1β acts directly on neurons to drive hyperexcitability (Viviani 2003 Src/NR2B; Vezzani's IL-1Ra anticonvulsant work, PNAS 2000). The IL-1 signalling field has shown neurons **cannot** run canonical IL-1 signalling: no NF-κB activation, no detectable TRAF6 (J Neurosci 2004, PMID 15269258), and the 2024 IL-1R1 mapping paper reports IL-1 induces NF-κB in IL-1R1⁺ *non-neuronal* cells but **not** in IL-1R1⁺ neurons (PMID 39563437). The reconciling variable — the AcP:AcPb ratio — is known to be modifiable (it shifts with ageing and increases IL-1β vulnerability, PNAS 2015, DOI 10.1073/pnas.1514486112) but **has never been measured in epilepsy or seizure models**; my searches returned no study linking AcPb to seizure susceptibility or epileptogenesis.
- Avoids trap 1 (two famous molecules in an "axis"): the object is the isoform ratio of a *single* gene as a switch, not a linear X→Y→Z chain.
- Avoids trap 3 (only changing the model): the readout itself is new to this disease area, not the model.
- Avoids trap 6 (WB bands = pathway): the decisive experiment is isoform-selective knockdown dissociating two downstream branches, not band intensity.
- **Honest exposure: trap 2.** "Mechanism known in ageing, now tested in epilepsy" is a fair reviewer framing. The defence must be that the paper's claim is the *resolution of a named contradiction* with a prespecified falsifiable negative, and that the branch-dissociation siRNA experiment is new in any tissue. If the student cannot hold that framing, this topic degrades to trap 2 and should not be attempted.

**5. state_of_the_art**
AcPb is a CNS-restricted *Il1rap* splice isoform that binds IL-1 and IL-1R1 but cannot mediate canonical IL-1 responses (Immunity 2009, Smith DE et al.); OMIM 602626 records that it skips exon 12 and includes a novel exon 12b encoding a different cytoplasmic C-terminus. AcPb-only knockout mice are deficient in IL-1β regulation of p-Src in neurons (J Neurosci 2011, PMID 22159118) — i.e. the Src branch that the epilepsy field invokes *requires* AcPb. Neurons use p38/CREB, not NF-κB, in response to IL-1β, and lack detectable TRAF6 (PMID 15269258). Ageing shifts the synaptic ratio toward AcP and increases IL-1β sensitivity (PNAS 2015). Dentate granule neurons are the dominant neuronal IL-1R1 site and exclusively express AcPb (PMID 39563437). Meanwhile, IL-1R1 deletion restricted to *endothelium* is sufficient to attenuate seizures (PMID 38087170), and caspase-1 inhibition (VX-765) passed safety but did not show sufficient efficacy in treatment-resistant epilepsy, with the Phase 2b trial terminated.

**6. specific_open_problem**
Nobody has measured the *Il1rap* exon-12 vs exon-12b isoform ratio in any seizure model or epileptic tissue, and nobody has shown that selectively removing AcPb (versus total IL1RAP) redirects a neuron's IL-1β response between branches.

**7. delta_vs_closest_paper**
Closest: **"Localization of brain neuronal IL-1R1 reveals specific neural circuitries responsive to immune signaling," J Neuroinflammation 2024 (PMID 39563437).** That paper maps *where* neuronal IL-1R1 is and shows neurons fail to mount NF-κB responses — it establishes the puzzle. It does not (a) quantify the AcP:AcPb ratio, (b) test whether that ratio is dynamic under injury/epileptogenic stress, or (c) perform isoform-selective loss-of-function to assign branch usage. This project does all three and is situated in epilepsy, which that paper does not address.

**8. references**
1. ILAE Consortium on Complex Epilepsies | GWAS meta-analysis of over 29,000 people with epilepsy identifies 26 risk loci and subtype-specific genetic architecture | Nature Genetics | 2023 | DOI 10.1038/s41588-023-01485-w; PMC10484785 | `SEARCH_SNIPPET`
2. authors not captured | Localization of brain neuronal IL-1R1 reveals specific neural circuitries responsive to immune signaling | Journal of Neuroinflammation | 2024 | PMID 39563437; DOI 10.1186/s12974-024-03287-1 | `SEARCH_SNIPPET`
3. Srinivasan D, Yen JH, Joseph DJ, Friedman W | Cell type-specific interleukin-1β signaling in the CNS | Journal of Neuroscience 24(29):6482–6488 | 2004 | PMID 15269258; DOI 10.1523/JNEUROSCI.5712-03.2004 | `SEARCH_SNIPPET`
4. Smith DE et al. | A central nervous system-restricted isoform of the interleukin-1 receptor accessory protein modulates neuronal responses to interleukin-1 | Immunity 30(6):817–831 | 2009 | PMID/DOI not captured | `SEARCH_SNIPPET`
5. authors not captured | Neuron-specific effects of interleukin-1β are mediated by a novel isoform of the IL-1 receptor accessory protein | Journal of Neuroscience 31(49):18048 | 2011 | PMID 22159118 | `SEARCH_SNIPPET`
6. authors not captured | Synapse-specific IL-1 receptor subunit reconfiguration augments vulnerability to IL-1β in the aged hippocampus | PNAS | 2015 | DOI 10.1073/pnas.1514486112 | `SEARCH_SNIPPET`
7. authors not captured | Conditional knockout of IL-1R1 in endothelial cells attenuates seizures and neurodegeneration via inhibiting neuroinflammation mediated by Nrf2/HO-1/NLRP3 signaling in status epilepticus model | Molecular Neurobiology | 2024 | PMID 38087170; DOI 10.1007/s12035-023-03842-6 | `SEARCH_SNIPPET`
8. authors not captured (Vezzani group) | Powerful anticonvulsant action of IL-1 receptor antagonist on intracerebral injection and astrocytic overexpression in mice | PNAS | 2000 | DOI 10.1073/pnas.190206797 | `SEARCH_SNIPPET`
9. Viviani B et al. | Interleukin-1β enhances NMDA receptor-mediated intracellular calcium increase through activation of the Src family of kinases | Journal of Neuroscience | 2003 | PMID/DOI not captured | `SEARCH_SNIPPET` (title seen verbatim)
10. — | OMIM entry 602626, IL1RAP (records exon 12 / exon 12b isoform structure) | OMIM | n.d. | MIM 602626 | `SEARCH_SNIPPET`
11. authors not captured | Interleukin-1R3 mediates interleukin-1-induced potassium current increase through fast activation of Akt kinase | PNAS | year not captured | DOI 10.1073/pnas.1205207109 | `SEARCH_SNIPPET`
12. authors not captured | IL-1β and HMGB1 in epileptogenesis: recent advances and clinical translation | journal not captured (2025 review) | 2025 | PMC12566638 | `SEARCH_SNIPPET`

**9. models_and_data**
- Cells: HT-22 (in hand), undifferentiated and differentiated side by side. Optional second cell: **bEnd.3** brain endothelial line as the AcP-dominant / NF-κB-competent positive control (**needs to be obtained**; this is the salvaged part of the dropped sixth topic).
- Public data: **GSE241219** (mouse pilocarpine status epilepticus, CA1 bulk RNA-seq, 6/12/24/36/72 h — ideal for junction-level isoform work because it is RNA-seq, not array); **GSE213393** (mouse dentate gyrus, kainate vs saline); **GSE99577**; **GSE122228** (intra-amygdala kainate, microarray — usable only if the array has exon-discriminating probes, likely not); **GSE63808** (human pharmacoresistant TLE hippocampus, bulk); **GSE190452** and **GSE140393** (human TLE cortex snRNA-seq, for cell-type assignment of *IL1R1*/*IL1RAP*). A human *hippocampus* snRNA-seq accession is "to be identified" — my searches found the studies (an AES abstract; a 2025 bioRxiv hippocampal-sclerosis preprint) but no accession.

**10. key_experiments**
Bench (all within the stated toolkit):
- **Week 1–2 go/no-go, non-negotiable:** qPCR for *Il1r1*, total *Il1rap*, exon-12 and exon-12b junction-specific amplicons in HT-22. If *Il1r1* is absent or near-undetectable, **stop and switch topics** — do not build a paper on a receptor-null cell.
- Isoform-specific qPCR assays: forward primer in the shared exon 11, reverse primers in exon 12 vs exon 12b. Validate by sequencing the amplicons (outsourced Sanger, trivial cost).
- Challenge series: glutamate and kainate excitotoxic stress ± IL-1β; time course. Readouts: isoform ratio (qPCR), p-p38/p38, p-Src/Src, p-p65/p65, IκBα (WB); NF-κB target genes *Nfkbia, Ccl2, Il6, Tnf* (qPCR).
- **Decisive experiment:** siRNA knockdown of (a) total *Il1rap*, (b) exon-12b-selective, (c) *Il1r1*, (d) non-targeting. Prediction: AcPb-selective knockdown abolishes the IL-1β→p-Src response while leaving/unmasking the p38 or NF-κB arm; total knockdown abolishes both.
- Viability/CCK-8 to test whether IL-1β modifies excitotoxic death and whether that modification is AcPb-dependent.
Bioinformatics:
- Junction-level quantification of *Il1rap* exon 12 vs 12b in GSE241219 and GSE213393 across the epileptogenesis time course (download SRA fastqs; quantify with salmon/kallisto against an isoform-aware index, or count junction-spanning reads directly with STAR/regtools).
- Cell-type assignment of *IL1R1*/*IL1RAP* in GSE190452 / GSE140393 to show which human cell types could carry the signal.
Gating requirements:
- **Isoform-selective siRNA**: must be custom-designed against exon 12b; cheap but requires careful design and a validated knockdown. Substitute if it fails: antisense/morpholino is not cheaper — instead fall back to overexpression-free pharmacological branch dissection (PP2/SB203580) plus total-*Il1rap* knockdown, which weakens but does not kill the paper.
- **Phospho-antibodies** (p-Src Y416/Y418, p-p38, p-p65): purchasable, moderate cost; each needs a stimulation-positive control.
- **No luciferase NF-κB reporter** — plasmid sourcing is a declared constraint. Use endogenous target-gene qPCR plus p-p65 WB instead. This is adequate and I recommend it over sourcing reporters.
- **SRA download + compute**: tens of GB and an isoform-aware aligner. Needs a workstation or a university cluster, or ~¥1–2k of cloud. Flag as a real, often-underestimated requirement.
- Animal arm (optional, strengthens a lot): 4–6 mice/timepoint, pilocarpine or kainate, hippocampal qPCR for the isoform ratio. Requires negotiated animal access + ethics approval; adds ~3 months.

**11. expected_and_negative_results**
- Positive: ratio shifts toward AcP after stress/epileptogenesis; AcPb-selective knockdown dissociates branches. This is a clean mechanistic paper with real translational reading (it would explain why global IL-1 blockade helps in some settings and why caspase-1 inhibition did not deliver).
- Negative A (ratio does not change): still publishable as a constraint — "the AcP:AcPb ratio is not the gate; neuronal IL-1 responsiveness in epileptogenesis must be set elsewhere." Modest but real, and it closes a plausible hypothesis.
- Negative B (HT-22 express no *Il1r1*): **not publishable as a paper.** This is why the week-2 go/no-go exists.
- Negative C (branch dissociation fails): weakest outcome; the paper becomes descriptive. Mitigate by keeping the public-data isoform arm strong enough to stand largely on its own.

**12. difficulty_and_cost**
Difficulty **4/5**. Roughly **¥35,000–60,000** without animals; **¥55,000–80,000** with a small mouse arm. Must buy: recombinant mouse IL-1β, custom siRNAs (4 targets × 3 duplexes), 6–8 antibodies including 3 phospho, transfection reagent, qPCR primers + sequencing validation, CCK-8. Must obtain: bEnd.3 (optional). Must outsource: Sanger sequencing of amplicons (trivial); nothing else.

**13. timeline_months** 9–12 (8 if the animal arm is dropped and the bioinformatics arm starts in month 1 in parallel).

**14. target_journal_tier**
Solid specialty-to-upper-specialty neuroscience/neuroimmunology, roughly IF 3–9, where mechanism rigor beats model breadth. Realistic: **Journal of Neuroinflammation** (ambitious but it is the natural home for cell-type-resolved IL-1 biology), **Journal of Neurochemistry**, **Experimental Neurology**. Fallbacks: **Molecular Neurobiology**, **Frontiers in Cellular Neuroscience**. No acceptance can be promised; the IL-1 signalling community reviews hard.

**15. reviewer_attacks**
1. "HT-22 is not a hippocampal neuron, and your 'epileptogenic stress' is glutamate toxicity." — Partly unanswerable. Must be pre-empted in the title/abstract, with the public-data and (ideally) mouse-tissue arms carrying generalization.
2. "You show a transcript ratio; you have not shown protein, surface localization, or complex stoichiometry." — Fair. AcP vs AcPb are hard to resolve by WB. Honest limitation statement required; a partial answer is that the siRNA branch dissociation is a functional, not correlative, assay.
3. "The ageing paper already showed the ratio is modifiable; this is the same idea in a new disease." — The trap-2 attack. Only the contradiction-resolution framing plus the branch-dissociation result defeats it.

**16. prelim_ratings**
Novelty **H** · evidence-base **H** (the contradiction is documented on both sides by strong papers) · overlap-risk **M** (the 2024 IL-1R1 group and the AcPb originators could do this quickly if they thought of it; the epilepsy angle is what protects the student)

---

# TOPIC 2 — Is "neuronal NLRP3/GSDMD pyroptosis" in seizure models an antibody artifact?

**1. title_en**
"Knockdown-validated reappraisal of neuronal inflammasome and gasdermin-D detection in hippocampal neuronal cultures used as seizure injury models"

**2. core_question**
Are *Nlrp3*, *Pycard*, *Casp1* and *Gsdmd* expressed in a hippocampal neuronal line at levels compatible with functional inflammasome assembly, and are the NLRP3 and GSDMD-N western-blot bands reported throughout the HT-22 seizure-injury literature sensitive to target-specific knockdown?

**3. hypothesis**
The "neuronal inflammasome" signal in cell-line seizure models is substantially an antibody-specificity and priming artifact: transcript levels are orders of magnitude below myeloid reference cells, and a measurable fraction of the published bands will prove knockdown-insensitive.

**4. novelty_claim**
This is a validity audit of one of the most-published claims in Chinese and international epilepsy cell biology, using the one control that literature systematically omits. The field's own methodologists state the problem plainly: without genetic knockout/knockdown controls it is not possible to evaluate NLRP3 expression from antibody-based methods alone (bioRxiv 2025, 2025.08.13.669639). And the 2026 literature now openly conflicts — a 2026 Frontiers in Cell and Developmental Biology paper (DOI 10.3389/fcell.2026.1793636; title not captured in my search) reports GSDMD cleavage occurring mainly in **astrocytes**, not neurons, while the HT-22 papers attribute it to neurons.
- Avoids trap 4 (pure database mining): there is a decisive bench arm.
- Avoids trap 6 (a few WB bands claiming a pathway): the project's whole premise is that WB bands without knockdown controls mean nothing — it is the inverse of that trap.
- Avoids trap 3 (only changing the model): it deliberately **replicates the published models exactly** and changes only the controls.

**5. state_of_the_art**
A dense recent literature reports neuronal NLRP3/caspase-1/GSDMD-N induction in HT-22 and in rodent seizure models and claims causality from knockdown of upstream regulators: SREBP1 (Heliyon 2023), HDAC1/miR-15a-5p/caspase-1 (Neurochem Res 2025, DOI 10.1007/s11064-025-04372-4), IRAK4/NF-κB/NLRP3 (Exp Neurol), JC124 (Cell Commun Signal 2025, DOI 10.1186/s12964-025-02239-3), baicalein (eNeuro 2024, ENEURO.0319-24.2024), plus *Gsdmd* knockdown in kainate TLE (PMID 36921736) and NLRP3–mitophagy work (Sci Rep 2025, DOI 10.1038/s41598-025-01087-y). Against this: NLRP3 components are functional in mouse brain microglia but not astrocytes (PLoS One, DOI 10.1371/journal.pone.0130624); reviews note basal neuronal *Nlrp3* is low or absent in public transcriptomic datasets, a point conceded even by a paper arguing *for* neuronal NLRP3 (Brain 2023;146(7):2989); and the human translation of this axis underperformed — VX-765 (caspase-1 inhibitor) was well tolerated but did not show sufficient efficacy, with Phase 2b (NCT01501383) terminated.

**6. specific_open_problem**
No published HT-22 inflammasome paper I found reports an NLRP3- or GSDMD-targeted knockdown as an antibody-specificity control, and none reports neuronal transcript abundance against a myeloid reference on a common scale. So the field has no measurement that distinguishes "neurons assemble inflammasomes" from "antibodies cross-react in neuronal lysates."

**7. delta_vs_closest_paper**
Closest: **"HDAC1 promotes hippocampal neuronal pyroptosis in epileptic mice through the miR-15a-5p/caspase-1 axis," Neurochemical Research 2025 (DOI 10.1007/s11064-025-04372-4).** It runs cleaved-caspase-1 and GSDMD-N blots in kainate-treated HT-22 and infers neuronal pyroptosis. It does not test whether those bands are *Casp1*- or *Gsdmd*-siRNA-sensitive, does not quantify transcript abundance against a myeloid comparator, and does not test antibody concordance across clones. This project holds its model constant and supplies exactly those missing controls.

**8. references**
1. authors not captured | Clarifying the priming requirement and activator specificity for the NLRP3 inflammasome in human keratinocytes in vitro | bioRxiv (**preprint**) | 2025 | bioRxiv 2025.08.13.669639 | `SEARCH_SNIPPET`
2. authors not captured | NLRP3 inflammasome is expressed and functional in mouse brain microglia but not in astrocytes | PLoS ONE | year not captured | DOI 10.1371/journal.pone.0130624 | `SEARCH_SNIPPET`
3. authors not captured | Neuronal NLRP3 inflammasome mediates spreading depolarization-evoked trigeminovascular activation | Brain 146(7):2989 | 2023 | PMID/DOI not captured | `SEARCH_SNIPPET`
4. authors not captured | SREBP1 deficiency diminishes glutamate-mediated HT22 cell damage and hippocampal neuronal pyroptosis induced by status epilepticus | Heliyon | 2023 | PMID/DOI not captured (article ID S2405-8440(23)11153-4) | `SEARCH_SNIPPET`
5. authors not captured | HDAC1 promotes hippocampal neuronal pyroptosis in epileptic mice through the miR-15a-5p/caspase-1 axis | Neurochemical Research | 2025 | DOI 10.1007/s11064-025-04372-4 | `SEARCH_SNIPPET`
6. authors not captured | GSDMD knockdown exacerbates hippocampal damage and seizure susceptibility by crosstalk between pyroptosis and apoptosis in kainic acid-induced temporal lobe epilepsy | journal not captured | 2023 | PMID 36921736 | `SEARCH_SNIPPET`
7. authors not captured | JC124 confers multimodal neuroprotection in epilepsy by suppressing NLRP3 inflammasome activation: evidence from animal and human neuronal models | Cell Communication and Signaling | 2025 | DOI 10.1186/s12964-025-02239-3 | `SEARCH_SNIPPET`
8. authors not captured | title not captured | Frontiers in Cell and Developmental Biology | 2026 | DOI 10.3389/fcell.2026.1793636 | `SEARCH_SNIPPET` — **title unverified**; cited only for the reported astrocyte-dominant GSDMD cleavage. Must be read in full before citing.
9. — | Vertex announces completion of Phase 2 study of VX-765 in people with epilepsy (company release); Phase 2b NCT01501383 listed as terminated | corporate press release / registry | year not captured | NCT01501383 | `SEARCH_SNIPPET` — **not peer-reviewed**; the AlzDiscovery summary in my results notes the trial results were never published in a peer-reviewed venue.
10. authors not captured | Transcriptomic analysis of glutamate-induced HT22 neurotoxicity as a model for screening anti-Alzheimer's drugs | Scientific Reports | 2023 | DOI 10.1038/s41598-023-34183-y | `SEARCH_SNIPPET`

**9. models_and_data**
- HT-22 (in hand). **Myeloid reference cell needed** — BV-2 or RAW264.7 (**needs to be obtained**; both are cheap and widely shared in Chinese institutions).
- Public data: **GSE241219**, **GSE213393**, **GSE122228**, **GSE63808** for tissue-level abundance; **GSE190452** / **GSE140393** human TLE snRNA-seq for cell-type assignment of *NLRP3*, *CASP1*, *GSDMD*, *PYCARD*; **GSE285372** (Fos binding in hippocampal chromatin 1 h after kainate) only if a chromatin-accessibility angle is wanted.

**10. key_experiments**
- Side-by-side relative qPCR (common standard curve, same plate) of *Nlrp3, Pycard, Casp1, Casp11, Gsdmd, Il1b, Il18* in HT-22 vs BV-2/RAW264.7, resting and after canonical priming (LPS) ± nigericin. This single figure is the paper's spine.
- Exact replication of two published HT-22 protocols (glutamate; kainate), then WB for NLRP3 and GSDMD with **two or three different commercial clones** per target, run on the same lysates.
- **Decisive:** siRNA against *Nlrp3* and *Gsdmd* in HT-22, then ask whether each band loses intensity proportionally to transcript knockdown. A band that survives ≥70% transcript knockdown is not the target.
- IL-1β/IL-18 release by **commercial ELISA** (explicitly the cheap substitute for any mass-spectrometry or secretome approach) — functional inflammasome output, or its absence.
- LDH release + CCK-8 to characterize the death modality without claiming pyroptosis from bands alone.
- Bioinformatics: cell-type-resolved expression of the inflammasome module in human TLE snRNA-seq; deconvolution of bulk mouse seizure datasets to test whether the tissue-level induction tracks myeloid fraction rather than neuronal expression.

Gating requirements:
- **Flow cytometry is NOT available** — so no ASC-speck flow quantification. Substitute: ELISA for IL-1β/IL-18 release plus LDH; and, if basic IF is negotiated, ASC speck counting by conventional fluorescence microscopy (no confocal needed for speck presence/absence).
- Nigericin and LPS: cheap. ELISA kits: moderate.
- No CRISPR knockout required; siRNA is the declared and sufficient tool here, and I would argue it is the right one — the point is to apply the control the field already accepts.

**11. expected_and_negative_results**
- "Negative" (bands not knockdown-sensitive, transcripts 2–4 logs below myeloid): **this is the publishable result**, and the most valuable one — a direct constraint on a large body of work and on a therapeutic rationale that already underperformed in humans.
- "Positive" (bands knockdown-sensitive, real transcripts present): also publishable and genuinely useful — it would be the first properly validated demonstration of neuronal inflammasome competence in this model, and would strengthen the field.
- This symmetry is the topic's main strength: **both outcomes are papers.** That is rare and is the single biggest argument for choosing it.
- Real risk: a "mixed" result (one antibody specific, one not) is messier to publish but still lands in a methods-friendly venue.

**12. difficulty_and_cost**
Difficulty **3/5** — the lowest-risk wet topic here. **¥25,000–45,000**. Must buy: 4–6 antibodies (deliberately redundant clones), siRNAs for 2 targets, LPS/nigericin, IL-1β and IL-18 ELISA kits, LDH kit, qPCR reagents. Must obtain: BV-2 or RAW264.7. Nothing needs outsourcing.

**13. timeline_months** 6–9. The fastest route to a submittable manuscript among all five.

**14. target_journal_tier**
Methods/rigor-friendly specialty journals, roughly IF 2.5–5, that will publish a negative or validation result. Realistic: **eNeuro** (explicitly receptive to negative and replication findings — my first choice), **Journal of Neuroscience Methods**, **Epilepsy Research**. Fallbacks: **IBRO Neuroscience Reports**, **ASN Neuro**, **Frontiers in Cellular Neuroscience**.

**15. reviewer_attacks**
1. "Absence of evidence in an immortalized line says nothing about neurons in vivo." — The strongest attack. Answer: the claim is explicitly scoped to the *model system that the target literature itself uses*, plus the public-data cell-type arm. Do not over-claim about in vivo neurons.
2. "Your antibodies/priming conditions were wrong — NLRP3 needs priming you did not provide." — Pre-empt by including a full LPS±nigericin priming matrix and by running the myeloid control in parallel on the same plate/blot.
3. "This is criticism, not discovery." — Partially valid; mitigate by making the quantitative cross-cell-type expression atlas and the human snRNA-seq cell-type assignment genuinely new contributions, not just rebuttals. Choose a journal whose scope embraces validation.

**16. prelim_ratings**
Novelty **M–H** (methodological rather than conceptual, but it adjudicates a live conflict) · evidence-base **H** · overlap-risk **L** (almost nobody is incentivized to publish this, which is precisely why it is open)

---

# TOPIC 3 — Neuronal P2X7: splice-variant-resolved, knockdown-validated adjudication

**1. title_en**
"Does a hippocampal neuronal line express functional P2X7? Splice-variant-resolved transcript analysis and knockdown-validated protein detection, with human single-cell cross-reference"

**2. core_question**
In a hippocampal neuronal line, is there knockdown-sensitive P2X7 protein, which *P2rx7* splice variants are present, and is there a BzATP-evoked functional response attributable to P2X7?

**3. hypothesis**
Neuronal P2X7 immunoreactivity in hippocampal neuronal preparations is largely antibody-derived rather than receptor-derived; where genuine transcript exists it is the escape variant P2X7k rather than canonical P2X7a, which would explain a decade of irreconcilable knockout results.

**4. novelty_claim**
This is a named, explicitly unresolved controversy with a point–counterpoint published in the same issue of the Journal of Neuroscience (Illes, Khan & Rubini, "Neuronal P2X7 receptors revisited: do they really exist?", J Neurosci 2017;37(30):7049, versus the companion paper at 37(30):7063), and the resolution hinges on a measurement nobody has done in one preparation: variant-resolved transcript quantification **plus** knockdown-validated protein detection **plus** a functional readout. The mechanistic crux is documented — the original GSK knockout retained *P2rx7-k* (JBC 2009, PMID 19546214), a new 2025 constitutive knockout line was needed to remove *P2rx7-a/-b/-c/-k* together (Purinergic Signalling 2025, DOI 10.1007/s11302-025-10074-x), and antibodies reportedly cannot distinguish P2X7k from full-length protein. There is direct epilepsy stakes: P2X7 antagonism reduces spontaneous seizures and gliosis in experimental TLE (J Neurosci 2016;36(22):5920) and is under active consideration as adjunctive therapy for drug-refractory epilepsy.
- Avoids trap 1, trap 3, trap 5 outright.
- Avoids trap 6 by making band identity the question, not the evidence.

**5. state_of_the_art**
P2X7 protein is elevated in hippocampal subfields of epileptic mice and in resected hippocampus from drug-resistant TLE patients; five days of JNJ-47965567 reduced spontaneous seizures with effects outlasting brain drug exposure (J Neurosci 2016;36(22):5920), and JNJ-54175446 had anti-seizure effects in the intra-amygdala kainate model (PMC10800975). Against neuronal localization: the Illes group argues neuroactive P2X7 sits on astrocytes and oligodendrocytes; P2X7-EGFP and conditional humanized mouse approaches (PMC5432476) have been used to dissect CNS *P2rx7* cellular distribution; available tools lack specific agonists and some antagonists lack specificity. The original P2X7k characterization explicitly reported a nonspecific brain band distinguishable from true P2X7 only by PNGase F deglycosylation behaviour (PMID 19546214) — a cheap trick the field mostly dropped.

**6. specific_open_problem**
No study I found reports, in a single neuronal preparation, (a) variant-specific *P2rx7* qPCR, (b) siRNA-validated western blot with more than one antibody clone, and (c) a BzATP functional readout. That triad is the measurement that would settle whether neuronal P2X7 is real in cultured hippocampal neurons.

**7. delta_vs_closest_paper**
Closest: **Illes P, Khan TM, Rubini P, "Neuronal P2X7 receptors revisited: do they really exist?", J Neurosci 2017;37(30):7049.** That is a review/opinion piece arguing the negative case from the existing literature; it generates no new data. This project generates the specific missing data in a defined preparation and adds a human single-cell cross-reference the 2017 debate could not use.

**8. references**
1. Illes P, Khan TM, Rubini P | Neuronal P2X7 receptors revisited: do they really exist? | Journal of Neuroscience 37(30):7049 | 2017 | PMID/DOI not captured | `SEARCH_SNIPPET`
2. authors not captured | Neuronal P2X7 receptor: involvement in neuronal physiology and pathology (companion/counterpoint) | Journal of Neuroscience 37(30):7063 | 2017 | PMID/DOI not captured | `SEARCH_SNIPPET`
3. authors not captured | A functional P2X7 splice variant with an alternative transmembrane domain 1 escapes gene inactivation in P2X7 knock-out mice | Journal of Biological Chemistry | 2009 | PMID 19546214; PMC2757983 | `SEARCH_SNIPPET`
4. authors not captured | Establishment and behavioural characterization of a novel constitutive P2X7 receptor knockout mouse line | Purinergic Signalling | 2025 | DOI 10.1007/s11302-025-10074-x | `SEARCH_SNIPPET`
5. authors not captured | Transient P2X7 receptor antagonism produces lasting reductions in spontaneous seizures and gliosis in experimental temporal lobe epilepsy | Journal of Neuroscience 36(22):5920 | 2016 | PMID/DOI not captured | `SEARCH_SNIPPET`
6. authors not captured | Splice variants of the P2X7 receptor reveal differential agonist dependence and functional coupling with pannexin-1 | Journal of Cell Science 125(16):3776 | 2012 | PMID/DOI not captured | `SEARCH_SNIPPET`
7. authors not captured | Genetically dissecting P2rx7 expression within the central nervous system using conditional humanized mice | journal not captured | year not captured | PMC5432476 | `SEARCH_SNIPPET`
8. authors not captured | Anti-seizure effects of JNJ-54175446 in the intra-amygdala kainic acid model of drug-resistant temporal lobe epilepsy in mice | journal not captured | 2023 | PMC10800975 | `SEARCH_SNIPPET`
9. authors not captured | The purinergic P2X7 receptor as a target for adjunctive treatment for drug-refractory epilepsy | journal not captured | year not captured | PMC11241490 | `SEARCH_SNIPPET`

**9. models_and_data**
- HT-22 (in hand) — but see the risk note. A second neuronal line (**N2a or SH-SY5Y, needs to be obtained**) is strongly advised so the finding is not single-line. Myeloid positive control (BV-2/RAW264.7, **needs to be obtained**) is mandatory.
- Public data: **GSE190452**, **GSE140393** for human *P2RX7* cell-type assignment; **GSE241219**/**GSE213393** for mouse *P2rx7* induction after status epilepticus. A dedicated check of *P2RX7* neuronal expression in single-cell data was one of the searches the budget cut off — treat that as an unverified assumption to test first.

**10. key_experiments**
- Variant-specific qPCR for *P2rx7-a*, *-b*, *-c*, *-k* (primer sets exploiting the alternative exon 1/TM1, as defined by the JBC 2009 and J Cell Sci 2012 work), HT-22 vs myeloid control.
- WB with 2–3 antibody clones ± *P2rx7* siRNA; include **PNGase F deglycosylation** to reproduce the original band-identity test — cheap, decisive, and largely abandoned by the field.
- Functional: BzATP concentration–response on viability (CCK-8/LDH) ± A438079 or Brilliant Blue G (cheap antagonists). **YO-PRO-1 or ethidium dye uptake** for large-pore formation if a fluorescence plate reader or standard fluorescence microscope is available.
Gating requirements:
- **Patch-clamp unavailable** — so no current measurement. The honest consequence: the paper can establish expression and dye-uptake/viability pharmacology but **cannot claim channel function**. This must be stated as a limitation, and it caps the topic's ceiling. A collaborator's rig would raise it substantially; worth asking.
- **JNJ-47965567/JNJ-54175446 are impractical** (cost/availability). Use A438079 and BBG and say so.
- PNGase F: inexpensive. Dye-uptake assay: needs a fluorescence reader — verify availability before committing.

**11. expected_and_negative_results**
- Negative (no knockdown-sensitive protein, no functional response): a clean contribution to a named controversy, publishable, and useful to a therapeutic programme.
- Positive, variant-resolved (P2X7k present and functional): more interesting and would support the counterpoint camp.
- **Main risk, stated plainly:** if HT-22 turn out to be *P2rx7*-null, the result is thin, because there is no existing claim of neuronal P2X7 in HT-22 for the student to adjudicate — my searches found no HT-22 P2X7 paper at all. The topic then becomes "one line lacks P2X7," which is weak. Mitigate by (a) checking single-cell/public data for neuronal *P2RX7* **before** committing, and (b) including a second neuronal line.

**12. difficulty_and_cost**
Difficulty **4/5**. **¥30,000–50,000**. Must buy: 2–3 P2X7 antibodies, siRNA, BzATP, A438079/BBG, PNGase F, dye-uptake probe, qPCR primers for 4 variants. Must obtain: a second neuronal line + myeloid control. Must check first: fluorescence plate reader.

**13. timeline_months** 8–11.

**14. target_journal_tier**
Purinergic/neuroscience specialty, roughly IF 2.5–5. Realistic: **Purinergic Signalling** (the controversy's home journal — the natural venue), **eNeuro**, **Journal of Neurochemistry**. Fallbacks: **Frontiers in Cellular Neuroscience**, **Neurochemical Research**.

**15. reviewer_attacks**
1. "Without electrophysiology you have not tested function." — Largely correct; must be conceded and scoped.
2. "A transformed line is the wrong preparation for this controversy — the debate is about neurons in tissue." — Serious. Partially answered by the second line and the public-data arm; fully answered only by primary neurons, which are "possible but must be obtained."
3. "Your siRNA knockdown is incomplete, so a surviving band is not proof of nonspecificity." — Must pre-empt with quantified knockdown efficiency, multiple duplexes, and a dose–response between transcript level and band intensity.

**16. prelim_ratings**
Novelty **M–H** · evidence-base **H** · overlap-risk **M** (established purinergic labs have the tools and the motive; the 2025 knockout-line paper suggests the field is actively re-tooling)

---

# TOPIC 4 — Does human genetic risk for epilepsy act in glial or immune cell *states*?

**1. title_en**
"Cell-state-resolved heritability analysis of common epilepsies: testing whether genetic risk acts in reactive glial and peripheral immune populations"

**2. core_question**
Is common-variant heritability for generalized and all-epilepsy enriched in *activated/reactive* glial and peripheral immune cell states — as opposed to the resting glial cell types already tested — when benchmarked against Alzheimer's, multiple sclerosis and Parkinson's disease as positive controls?

**3. hypothesis**
Epilepsy's genetic signal is neuron-restricted even at cell-*state* resolution, meaning the neuroinflammation observed in epileptic tissue is predominantly a consequence of seizures rather than an inherited cause — in sharp contrast to the neurodegenerative diseases where microglial enrichment is robust.

**4. novelty_claim**
The ILAE 2023 GWAS reported enrichment in excitatory and inhibitory neurons and **not** in astrocytes, oligodendrocytes or microglia — but it tested *resting* cell-type references with MAGMA/FUMA. The field's standing defence is precisely that GWAS cell-type analyses look at resting cells and would miss risk acting in stimulus-dependent states. That defence has never been tested in epilepsy. Using cell-state-resolved scoring (scDRS, Nature Genetics 2022, DOI 10.1038/s41588-022-01167-z; and specifically-expressed-gene heritability enrichment) over reactive astrocyte, disease-associated microglia and peripheral immune subsets, with cross-disease positive controls, converts a vague hand-wave into a falsifiable test.
- Avoids trap 4 (pure database mining: no DEG + correlation + enrichment here — the design is a prespecified hypothesis test with positive controls and a defined null).
- Avoids trap 2: it does not import a mechanism; it tests whether one exists.
- This is the "measurement that distinguishes two competing explanations" category: inflammation-as-cause vs inflammation-as-consequence.

**5. state_of_the_art**
ILAE 2023 (29,944 cases / 52,538 controls; 26 loci, 19 GGE-specific, 29 implicated genes) found neuronal but not glial enrichment, and explicitly contrasted epilepsy with Alzheimer's and multiple sclerosis, where microglia are implicated. Focal epilepsy yielded no genome-wide-significant loci — a hard power ceiling. Drug-resistant epilepsy GWAS (eBioMedicine 2025, PMID 40240269) found no significant loci when epilepsy types were combined. For the positive controls: neurodegenerative heritability is enriched at microglial chromatin contact sites (PLoS Genetics, DOI 10.1371/journal.pgen.1011407) and microglial open chromatin is the strongest enrichment in Parkinson's disease (Ann Neurol 2021, Andersen et al., DOI 10.1002/ana.26032). A 2026 Epilepsia integrative-omics paper (Mushunuri et al., DOI 10.1111/epi.70021) extended ILAE data with TWAS and a methylation-QTL framework (ME-MAGMA), reporting 897 FDR-corrected candidates dominated by ion channels — not a cell-state analysis.

**6. specific_open_problem**
Whether epilepsy's glial null survives when the annotations are (a) reactive/disease-associated glial states rather than resting cell types, (b) derived from *epileptic* human tissue rather than healthy reference atlases, and (c) extended to peripheral immune subsets — and how its effect sizes compare to diseases where the microglial signal is real.

**7. delta_vs_closest_paper**
Closest: **ILAE Consortium, Nature Genetics 2023 (DOI 10.1038/s41588-023-01485-w).** It reports a glial null using resting-cell-type references and a single family of methods, as one sub-analysis of a large GWAS paper. This project makes that null the primary object, tests it against the specific alternative hypothesis that would rescue the inflammation model (state- rather than type-specific action), uses epilepsy-tissue-derived annotations, and calibrates with three disease positive controls — none of which ILAE 2023 did.

**8. references**
1. ILAE Consortium on Complex Epilepsies | GWAS meta-analysis of over 29,000 people with epilepsy identifies 26 risk loci and subtype-specific genetic architecture | Nature Genetics | 2023 | DOI 10.1038/s41588-023-01485-w; PMC10484785 | `SEARCH_SNIPPET`
2. authors not captured | Polygenic enrichment distinguishes disease associations of individual cells in single-cell RNA-seq data (scDRS) | Nature Genetics | 2022 | DOI 10.1038/s41588-022-01167-z | `SEARCH_SNIPPET`
3. Mushunuri A et al. | Genetic risk factor identification for common epilepsies guided by integrative omics data analysis | Epilepsia 67(3):1406–1420 | 2026 | PMID 41319129; DOI 10.1111/epi.70021; PMC13007835 | `SEARCH_SNIPPET`
4. authors not captured | Genome-wide association meta-analyses of drug-resistant epilepsy | eBioMedicine | 2025 | PMID 40240269 | `SEARCH_SNIPPET`
5. authors not captured | Genetic risk for neurodegenerative conditions is linked to disease-specific microglial pathways | PLoS Genetics | year not captured | DOI 10.1371/journal.pgen.1011407; PMC12017514 | `SEARCH_SNIPPET`
6. Andersen MS et al. | Heritability enrichment implicates microglia in Parkinson's disease pathogenesis | Annals of Neurology | 2021 | DOI 10.1002/ana.26032 | `SEARCH_SNIPPET`
7. authors not captured | Heritability enrichment of specifically expressed genes identifies disease-relevant tissues and cell types (LDSC-SEG) | journal not captured | year not captured | PMID/DOI not captured | `TITLE_ONLY`
8. authors not captured | Single-nucleus transcriptomics reveals cell type-specific remodeling and epilepsy-associated microglia | journal not captured | 2025 | PMC13521094 | `SEARCH_SNIPPET`
9. Pai et al. (per search result) | High-resolution transcriptomics informs glial pathology in human temporal lobe epilepsy | Acta Neuropathologica Communications | 2022 | DOI 10.1186/s40478-022-01453-1 | `SEARCH_SNIPPET`

**9. models_and_data**
No cells. GWAS summary statistics: ILAE 2023 epilepsy (all-epilepsy, GGE, focal) — ILAE consortium data availability; positive-control GWAS for AD/MS/PD via public repositories (the EBI GWAS summary statistics FTP appeared in my results as a standard source). Single-cell/annotation sources: **GSE190452**, **GSE140393** (human TLE cortex snRNA-seq), **PMC13521094**'s epilepsy-associated microglia dataset (accession to be identified), **GSE241219** / **GSE213393** (mouse seizure, for reactive-state signature derivation), plus a healthy human brain reference atlas (Allen Brain Map cell-types RNA-seq appeared in my results). Peripheral immune reference: **GSE107011** (immune cell / PBMC profiling, appeared in my results) — suitability to be confirmed.

**10. key_experiments**
Entirely R/bioinformatics, fully within declared strengths:
- Derive reactive-state gene programmes (reactive astrocyte, disease-associated/epilepsy-associated microglia, interferon-response states) from epilepsy snRNA-seq rather than importing AD-derived signatures.
- Run scDRS over human TLE snRNA-seq with epilepsy GWAS, and specifically-expressed-gene heritability enrichment over state annotations.
- Run the identical pipeline on AD, MS and PD GWAS as positive controls, and on a non-brain trait as a negative control.
- **Pre-specify and report power**: simulate detectable enrichment given epilepsy's h²_SNP and sample size. Without this the paper is indefensible, because "no signal" and "no power" are otherwise indistinguishable. Restrict primary analyses to GGE and all-epilepsy; treat focal epilepsy as exploratory only, since it has no genome-wide hits.
- Sensitivity: multiple gene-mapping windows, MAGMA gene-set sizes, and both method families; report concordance.
Gating requirements: **none in equipment.** Needs a workstation with adequate RAM for snRNA-seq objects (or ~¥0–2k cloud). The real gating requirement is **statistical discipline** — this topic is only publishable if the negative is rigorously bounded.

**11. expected_and_negative_results**
- The expected result *is* the "negative," and here that is the point: a well-powered, positive-control-calibrated demonstration that inherited epilepsy risk does not act through glial or immune states, with the direct implication that anti-inflammatory strategies in epilepsy target a consequence, not a cause. That reading has real translational weight given that caspase-1 inhibition did not deliver in humans.
- If enrichment *is* found in a reactive state, that is a notable positive and a strong paper.
- Genuine publication risk: some editors treat null bioinformatics as unpublishable. The positive-control design and the explicit power analysis are what make it publishable; without them, don't attempt it.

**12. difficulty_and_cost**
Difficulty **3/5** conceptually, **4/5** in statistical rigor. **¥0–3,000** (compute only). Nothing to buy or outsource. This is by far the cheapest topic and the only one with essentially zero procurement risk.

**13. timeline_months** 4–7. Could be submitted first and run in parallel with a wet topic — this is a legitimate strategy for a student who needs one publication in 6–12 months.

**14. target_journal_tier**
Clinical-epilepsy and neuroimmunology specialty, roughly IF 3–7, with a stretch option. Realistic: **Epilepsia Open**, **Seizure**, **Journal of Neuroinflammation**. Stretch: **Epilepsia** or **Brain Communications** if the power analysis is airtight. Fallback: **Frontiers in Neurology**.

**15. reviewer_attacks**
1. "This is a power problem dressed up as a biological finding." — The central attack. Only a prespecified power analysis and three positive controls answer it.
2. "ILAE 2023 already reported no glial enrichment." — Must be answered in the first paragraph by naming exactly what was *not* tested (states, epilepsy-derived annotations, immune subsets, cross-disease calibration).
3. "Common-variant architecture says nothing about acquired epilepsy, where inflammation is most invoked." — Fundamentally valid and must be conceded explicitly: the paper constrains the *inherited* contribution, not post-insult epileptogenesis. Over-claiming here would be fatal.

**16. prelim_ratings**
Novelty **M–H** · evidence-base **H** · overlap-risk **M–H** (statistical-genetics groups can execute this in weeks; the Mushunuri 2026 group is already working this data. Speed matters — this is the topic most likely to be scooped if the student is slow)

---

# TOPIC 5 — Adjudicating the contradictory Mendelian randomization literature on inflammation and epilepsy

**1. title_en**
"Do causal claims linking circulating inflammatory proteins to epilepsy survive cis-instrument restriction and colocalization? A systematic re-analysis"

**2. core_question**
Of the inflammatory-protein and immune-cell "causal effects on epilepsy" reported across the 2023–2025 Mendelian randomization literature, how many survive restriction to cis instruments, formal colocalization, correction for the full multiple-testing burden, and replication across epilepsy GWAS and subtypes?

**3. hypothesis**
Most published MR hits in this literature are artifacts of trans-pleiotropy, unaccounted multiple testing across hundreds of exposures, and non-replication across cohorts; few or none will colocalize, and the apparent abundance of "causal inflammatory drivers of epilepsy" is a false-discovery phenomenon.

**4. novelty_claim**
This literature is internally inconsistent in a documented way: different papers nominate different and largely non-overlapping proteins and immune traits (IL-5 and IL-1 receptor antagonist for focal epilepsy; M-CSF and RANTES for generalized; CD64 on monocytes with VEGF-A/IL-13/CCL23/LIF-R/CXCL11/OPG as mediators; a separate preprint reporting no causal relationship at all). A 2025 plasma-proteome MR applying a PP.H4 > 0.8 colocalization threshold found its best epilepsy signal (ACVRL1, PP.H4 = 0.747) *fall short* of it. The decisive step — cis-only instruments plus colocalization plus honest multiplicity — is what most of these papers skipped, and no one has applied it systematically across the whole claim set.
- Avoids trap 4: this is not DEG + enrichment; it is a prespecified replication/adjudication study with a stated decision rule.
- This is squarely the "limiting condition that constrains a popular model" category.

**5. state_of_the_art**
Multiple 2023–2025 MR studies report inflammation–epilepsy causal effects: bidirectional MR of 41 cytokines; immune-cell MR with metabolite mediation (Sci Rep 2024, DOI 10.1038/s41598-024-70370-1); circulating inflammatory cytokines and proteins as epilepsy drivers/targets (Epilepsy & Behavior 2024, PMID 38823075); IL6R-blockade-proxy MR (World J Psychiatry, DOI 10.5498/wjp.v14.i8.1244); a 2025 plasma-proteome MR with colocalization (PMC12716302); and a Research Square preprint reporting no reverse causal relationship. The reference exposure resource is the Olink inflammation pQTL meta-analysis (Zhao et al., Nature Immunology 2023, DOI 10.1038/s41590-023-01588-w: 180 primary pQTL signals, 59 cis and 121 trans, across 91 proteins), with UKB-PPP (~2,900 plasma proteins, 14,287 pQTLs, ~67% with cis associations) and deCODE summary data publicly hosted. Crucially, epilepsy's own genetics points to neurons, not immune cells (ILAE 2023) — so a null here would be *consistent* rather than isolated.

**6. specific_open_problem**
Nobody has taken the published claim set as the unit of analysis and asked, with harmonized instruments and a prespecified colocalization decision rule, which claims are robust. The literature is therefore growing without a convergence mechanism.

**7. delta_vs_closest_paper**
Closest: **"Assessing the causal relationship between the plasma proteome and epilepsy: a Mendelian randomization study" (2025, PMC12716302).** It runs a proteome-wide MR with colocalization but reports its own fresh scan; it does not systematically re-test the previously published claims, does not harmonize instruments across the prior studies' heterogeneous exposure sources, and does not quantify how much of the prior literature survives. This project's unit of analysis is the prior claim set, not a new scan.

**8. references**
1. authors not captured | Assessing the impact of circulating inflammatory cytokines and proteins as drivers and therapeutic targets in epilepsy: a Mendelian randomization study | Epilepsy & Behavior | 2024 | PMID 38823075 | `SEARCH_SNIPPET`
2. authors not captured | Causal relationship between immune cells and epilepsy mediated by metabolites analyzed through Mendelian randomization | Scientific Reports | 2024 | DOI 10.1038/s41598-024-70370-1 | `SEARCH_SNIPPET`
3. authors not captured | Assessing the causal relationship between the plasma proteome and epilepsy: a Mendelian randomization study | journal not captured | 2025 | PMC12716302 | `SEARCH_SNIPPET`
4. Zhao JH et al. | Genetics of circulating inflammatory proteins identifies drivers of immune-mediated disease risk and therapeutic targets | Nature Immunology | 2023 | DOI 10.1038/s41590-023-01588-w | `SEARCH_SNIPPET`
5. authors not captured | Exploring the role of interleukin-6 receptor blockade in epilepsy and associated neuropsychiatric conditions through a Mendelian randomization study | World Journal of Psychiatry 14(8):1244 | 2024 | DOI 10.5498/wjp.v14.i8.1244 | `SEARCH_SNIPPET`
6. authors not captured | Exploring causal correlations between systemic inflammatory cytokines and epilepsy: a bidirectional Mendelian randomization study | journal not captured (article ID S1059131123002935) | 2023 | PMID/DOI not captured | `SEARCH_SNIPPET`
7. ILAE Consortium on Complex Epilepsies | GWAS meta-analysis of over 29,000 people with epilepsy identifies 26 risk loci and subtype-specific genetic architecture | Nature Genetics | 2023 | DOI 10.1038/s41588-023-01485-w | `SEARCH_SNIPPET`
8. authors not captured | Rare variant associations with plasma protein levels in the UK Biobank | Nature | 2023 | DOI 10.1038/s41586-023-06547-x | `SEARCH_SNIPPET`
9. authors not captured | Large-scale plasma proteomics comparisons through genetics and disease associations | Nature | 2023 | DOI 10.1038/s41586-023-06563-x | `SEARCH_SNIPPET`

**9. models_and_data**
No cells. Exposures: Olink inflammation pQTL meta-analysis (Nat Immunol 2023), UKB-PPP (via the AstraZeneca pQTL portal, which appeared in my results as the hosting site; **access terms must be checked** — some uses require approval), deCODE summary data (Olink 2,931 and SomaScan 4,907 assays, publicly hosted per my results), and the immune-cell-trait GWAS used by the prior papers. Outcomes: ILAE 2023 all-epilepsy / GGE / focal; FinnGen as the replication cohort (FinnGen R10 appeared in my results as used by a prior preprint). Tissue QTL for triangulation: brain eQTL resources — **MetaBrain and GTEx brain were NOT confirmed reachable in my searches** (that lookup was cut off by the budget), so treat brain-eQTL availability as "to be confirmed."

**10. key_experiments**
- Systematically extract every reported inflammation→epilepsy causal claim from the 2023–2025 papers into a structured claim table (exposure, instrument source, effect, p, replication status).
- Re-instrument each exposure with **cis-only** variants, harmonized LD reference, F-statistic and Steiger filtering.
- Re-estimate with IVW/MR-Egger/weighted median; apply the correct multiplicity burden for the *original* exposure panel size, not the subset reported.
- **Colocalization** (coloc, prespecified PP.H4 ≥ 0.8) at every cis locus against epilepsy GWAS — the step whose absence most inflates this literature.
- Replication across epilepsy GWAS/subtypes and in FinnGen; report a survival table.
- Optional triangulation: do surviving proteins show brain-tissue expression consistent with a CNS mechanism (contingent on brain-eQTL access).
Gating requirements: **none in equipment.** UKB-PPP access terms are the only real gate — if restricted, fall back to the fully public Olink inflammation meta-analysis and deCODE data, which is sufficient for the core question.

**11. expected_and_negative_results**
- Expected: few or no claims survive. Published as a survival table plus a methodological diagnosis, this is a genuinely useful, citable contribution — and it coheres with the genetic architecture reported by ILAE 2023.
- If a small number *do* survive cis + coloc + replication, that is arguably the better outcome: it produces a short, credible, prioritized target list where the field currently has noise.
- Risk: some journals will treat this as a Letter/Comment rather than an Article. Framing it as a prespecified systematic replication study with a registered protocol (OSF) materially improves the odds.

**12. difficulty_and_cost**
Difficulty **3/5**. **¥0–2,000**. Nothing to buy. Main cost is the student's time and the care needed to avoid the same errors being critiqued.

**13. timeline_months** 4–6.

**14. target_journal_tier**
Epilepsy specialty and genetic-epidemiology-literate venues, roughly IF 2.5–6. Realistic: **Seizure**, **Epilepsy & Behavior** (notably, the venue that published one of the papers being re-examined — an advantage, not a conflict), **Epilepsia Open**. Stretch: **European Journal of Epidemiology** or **Brain Communications** if framed as a methodological case study.

**15. reviewer_attacks**
1. "Null MR results reflect weak instruments and epilepsy's modest GWAS power, not absence of effect." — Must be answered with instrument strength reporting and explicit minimum-detectable-effect calculations per exposure.
2. "This is a critique of other people's work, not new science." — Mitigate with prespecification, a transparent claim-extraction protocol, and a constructive deliverable (a prioritized surviving-target list and a reusable pipeline).
3. "Plasma protein levels are poor proxies for brain exposure, so neither the original claims nor your refutation is informative." — The deepest attack, and it cuts both ways. Address it head-on as a limitation of the whole literature — which is itself part of the paper's contribution.

**16. prelim_ratings**
Novelty **M** · evidence-base **H** · overlap-risk **M–H** (MR papers in this space appear monthly; a 2025 paper already added colocalization, and I found a public GitHub project computing cis-pQTL/ILAE-2023 epilepsy MR with null results for IL6R, IL-10, CXCL9 and M-CSF. The space is filling fast.)

---

# domain_landscape

The 2023–2026 frontier in epilepsy neuroimmunology has shifted from "inflammation accompanies seizures" to two harder questions: **which cell, and which state**. The nucleic-acid-sensing axis is the clearest example and it moved extremely fast. In 2026, cGAS-mediated type I interferon signalling was reported to drive disease progression in drug-refractory epilepsy, with microglia-specific *Cgas* deletion reducing seizure activity and conditioned medium from PTZ-treated neurons activating microglial TBK1 only in *Cgas*⁺/⁺ cells (Nature Neuroscience 2026, PMID 41676493, DOI 10.1038/s41593-026-02384-z); a PNAS 2026 paper reported neuronal mtDNA leakage via p-MLKL being taken up by microglia to activate cGAS–STING (DOI 10.1073/pnas.2522313123); and a Neurochemical Research 2026 paper placed STING-driven microglial polarization downstream of status epilepticus (DOI 10.1007/s11064-026-04734-6). Complement moved similarly: C1q neutralization during epileptogenesis attenuated complement-mediated synaptic elimination and epileptiform activity (Jeong et al., Epilepsia 2026, DOI 10.1111/epi.18678). An astrocyte-specific monoacylglycerol-lipase deletion reduced seizure susceptibility where neuron-specific deletion did not (bioRxiv 2026, preprint). Two 2026 Frontiers in Immunology reviews reframe epilepsy as a disease of "inflammatory places" and foreground CCR2⁺ monocytes and microglial over-pruning of inhibitory synapses. Meningeal and skull-marrow immunity is being mapped (Cell Death & Disease 2025, DOI 10.1038/s41419-025-07336-2) but, per my searches, **not yet connected to seizures** — genuinely open, and genuinely out of reach without in vivo labelling.

**Crowded to the point of futility:** NLRP3/pyroptosis/ferroptosis in rodent seizure models with a cell-line arm; microglial M1/M2 polarization; lncRNA/miRNA/target "axes"; and Mendelian randomization of circulating cytokines or immune-cell traits against epilepsy, where at least six mutually inconsistent papers appeared in 2023–2025. A student entering any of these competes with hundreds of better-resourced groups on identical questions.

**Genuinely open, and I would stake the committee's credibility on these:** (1) *Which cell actually receives the cytokine signal.* IL-1R1 deletion restricted to endothelium is sufficient to attenuate seizures (PMID 38087170), while neurons express IL-1R1 yet fail to mount NF-κB responses and lack detectable TRAF6 (PMID 39563437; PMID 15269258) — so the field's foundational "IL-1β acts directly on neurons" claim rests on a receptor complex nobody has characterized in this disease. (2) *Whether neurons have functional inflammasomes or P2X7 at all* — both are live, named controversies sustained by unvalidated antibodies. (3) *Why human translation failed.* VX-765 was well tolerated but did not show sufficient efficacy, and Phase 2b was terminated, against uniformly positive rodent data. Nobody has published a serious reconciliation. Anakinra in FIRES remains case-series-level, with a 2025 review explicitly calling for a platform trial (Adv Sci 2025, DOI 10.1002/advs.202509668) and one 2025 case report showing anakinra working with *normal* IL-1β levels (PMID 42367793) — i.e. even the biomarker logic is unsettled. (4) *Whether human genetics supports causal inflammation at all*: ILAE 2023 says neurons, not glia.

**Honest read on where an undergraduate can contribute.** Not in mechanism. The current frontier requires conditional knockouts, EEG telemetry, microglia-specific deletion and in vivo imaging — every one of which is outside the stated resources, and no substitution saves them. The exploitable asymmetry is **rigor**: this field's cell-line and antibody practices are weak, the incentive to audit them is near zero, and the controls required (siRNA, redundant antibody clones, cross-cell-type qPCR) are exactly what this student already has. The second asymmetry is **public human genetics**, which is free, underused in epilepsy neuroimmunology relative to the rodent literature, and matched to a student strong in R. Topics 1–3 exploit the first; Topics 4–5 exploit the second. If forced to pick one, I would recommend **Topic 2** on expected value — it is the only topic where both the positive and the negative outcome is a paper, it is the cheapest wet project, and it has the lowest overlap risk — with **Topic 4** run in parallel as cheap insurance.

# rejected_ideas

1. **Any "lncRNA X / miR-Y / target Z axis in epilepsy."** Trap 1 by definition. The search space is already saturated (e.g. an ILF3-AS1/miR-212 hippocampal epilepsy paper surfaced unprompted in my results). No new principle is possible.
2. **A new NLRP3/ferroptosis/pyroptosis inhibitor or natural product in HT-22 glutamate injury + a kainate mouse.** Already done repeatedly and recently: SREBP1 (Heliyon 2023), HDAC1/miR-15a-5p/caspase-1 (Neurochem Res 2025), IRAK4/NF-κB/NLRP3 (Exp Neurol), JC124 (Cell Commun Signal 2025), baicalein (eNeuro 2024). Changing only the molecule is trap 3.
3. **cGAS–STING in epilepsy.** Scooped decisively in 2026 by Nature Neuroscience (PMID 41676493) and PNAS (DOI 10.1073/pnas.2522313123), both with genetic deletion and human tissue. No undergraduate-feasible increment remains.
4. **A fresh Mendelian randomization scan of cytokines or immune-cell traits against epilepsy.** Saturated — Sci Rep 2024, Epilepsy & Behavior 2024 (PMID 38823075), World J Psychiatry 2024, a 2025 plasma-proteome MR (PMC12716302), plus a public GitHub project already computing cis-pQTL/ILAE-2023 MR with null results. Only the *adjudication* framing (Topic 5) survives.
5. **Molecular docking of a natural compound onto NLRP3 or TLR4, then HT-22 validation.** Trap 5 verbatim. A binding score is not a mechanism, and reviewers in this space now reject it reflexively.
6. **HMGB1 disulfide isoform as an epilepsy biomarker.** The foundational work exists (JCI 2017, "Molecular isoforms of high-mobility group box 1 are mechanistic biomarkers for epilepsy," jci.org/articles/view/92001) and isoform discrimination requires mass spectrometry plus a human serum cohort with longitudinal seizure outcomes. Commercial ELISA cannot distinguish redox isoforms, which is the entire point — so no cheap substitute exists. Gating requirement is fatal here, not negotiable.
7. **Claudin-5 / blood–brain barrier causality in epilepsy.** The decisive experiment is published: endothelial claudin-5 manipulation and conditional knockout, with spontaneous seizures and ictal EEG (Nature Communications 2022, DOI 10.1038/s41467-022-29657-y). Replicating it needs endothelial-specific Cre lines and EEG. A 2025 claudin-5-binding small molecule paper is a drug-delivery study, not a causality study — and also out of reach.
8. **C1q/C3-mediated microglial pruning of inhibitory synapses in epilepsy.** Just addressed in Epilepsia 2026 (Jeong et al., DOI 10.1111/epi.18678). The interesting residual — a C1q-independent C3 route and a parallel MerTK/phosphatidylserine pathway, both flagged in a 2025 review (PMC13458259) — requires engulfment assays, flow cytometry and in vivo work. Excellent question, wrong resources.
9. **A Mg²⁺-free "in vitro epilepsy model" in HT-22.** Mechanistically invalid: the model works by relieving the Mg²⁺ block of NMDA receptors (Sci Rep 2021, DOI 10.1038/s41598-021-90486-y), and undifferentiated HT-22 lack functional NMDA receptors (Sci Rep 2023, DOI 10.1038/s41598-023-34183-y; PMID 25206424). Any paper doing this is unpublishable in a journal with a competent reviewer.
10. **Skull bone marrow / meningeal immune trafficking in epilepsy.** Genuinely open — my searches found no study tracing skull-marrow or meningeal immune cells to seizure generation — but it requires in vivo cell labelling, flow cytometry and surgery. Flagging it as the best question in the domain that this student cannot touch.
11. **Standalone brain-endothelial vs neuronal IL-1β competence head-to-head** (the dropped sixth topic). The decisive in vivo result exists (PMID 38087170), and the in vitro version needs Transwell/TEER infrastructure I could not verify. Folded into Topic 1 as an optional bEnd.3 control arm.

**Final caveat on verification.** Several references above carry `authors not captured` or `PMID/DOI not captured`. That is deliberate — I saw the title, journal, and often the DOI or PMID verbatim in search results, but not the full author list, and I will not invent one. One reference (DOI 10.3389/fcell.2026.1793636) has an **unverified title** and must be read in full before being cited. The student must retrieve and read every reference before building a proposal on it; my tags indicate how much of each citation I could actually confirm, not how reliable the underlying paper is.