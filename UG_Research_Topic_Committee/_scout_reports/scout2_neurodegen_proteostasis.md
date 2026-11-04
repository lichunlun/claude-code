# Topic-selection committee report — neurodegeneration / neural injury / proteostasis

## PROCEDURAL NOTE (read before using this)
I ran **20 WebSearch calls**, then the turn's shared web-search budget (200 calls across all agents) was exhausted and further searches were refused. I did **not** reach the 20–35 I intended. Consequences:

- Every reference below appeared in one of my 20 search result sets. Nothing is invented.
- Where I could not capture a PMID or DOI, I say so and do **not** supply digits.
- **Three gating literature checks remain undone.** They must be completed before the student commits:
  1. Topic 3: has *ACSL4 knockdown in glutamate-treated HT-22* already been published? (searches refused)
  2. Topic 2: is there an existing *mammalian* SCFD1 knockdown/overexpression neuronal paper from the Cauchi group or others? (not searched)
  3. Topic 1: has anyone done a *kinase-resolved* ISR attribution in HT-22 disease models? (not searched directly)
- Today's date in this environment is **2026-11-04**, so "current frontier" below means late-2025/2026.

---

# TOPIC 1

**1. title_en**
Is it really ER stress? Kinase-resolved attribution of ATF4–CHOP induction in standard neuronal injury models

**2. core_question**
In HT-22 cells, is the ATF4/CHOP induction that the neuro-injury literature routinely attributes to PERK-dependent ER stress actually dependent on PERK and on eIF2α-Ser51 phosphorylation, or is it driven by HRI (EIF2AK1)/DELE1 or by eIF2α-phosphorylation-independent mTORC1–4E-BP control?

**3. hypothesis**
For at least two of the four canonical insults (glutamate/xCT block, OGD/reoxygenation, rotenone or MPP+, Aβ42 oligomers), ATF4/CHOP induction will be PERK-independent — HRI/DELE1-dependent for the mitochondrial insults and partly ISRIB-insensitive (i.e. eIF2α-independent, mTORC1-driven) for at least one — and will occur **without** IRE1-dependent XBP1 splicing, invalidating the "ER stress" label for those models.

**4. novelty_claim**
New: a per-stressor, kinase-resolved attribution map for the exact cell system the field uses, with an IRE1-specific discriminator (XBP1 splicing) that separates true ER stress from generic ISR. Avoids the "two molecules in one axis" trap because nothing is being paired — this is an epistasis/attribution experiment. Avoids the "transplant a mature mechanism" trap because the known mechanisms (PERK, HRI/DELE1, mTORC1–ATF4) are the *competing hypotheses being adjudicated*, not the conclusion. The output is a limiting condition on a very popular model ("ER stress drives neuronal injury").

**5. state_of_the_art**
Wolzak 2022 (EMBO J, PMID 35791631) showed PERK-null primary neurons retain translational attenuation during ER stress, with a rescaled, fully p-eIF2α-dependent ATF4 response mediated by HRI — i.e. neurons are unusual in kinase usage. Guo 2020 / Fessler 2020 (Nature) established OMA1–DELE1–HRI as the mitochondria→cytosol ISR relay; the HtrA2 paper (PMC10981713) and the DELE1 iron paper (Mol Cell 2023) show DELE1–HRI can fire OMA1-independently. Perea 2023 (Cell Chem Biol, PMC10029010) showed pharmacologic HRI (BtdCPU) and GCN2 (halofuginone) activation restores ER-stress resilience in PERK-deficient cells. Torrence 2021 (eLife 63326) and the 2017 mTORC1 paper (PMID 28494858) showed ATF4 can rise translationally via 4E-BPs with no eIF2α phosphorylation. The 2025 Mol Neurodegener ISR review (DOI 10.1186/s13024-025-00811-6) states that acutely inhibiting ISR under stress did not change outcome, implying the ISR may not be the operative driver at all in some models.

**6. specific_open_problem**
Thousands of neuronal injury papers report p-eIF2α + ATF4 + CHOP and conclude "PERK/ER stress." Nobody has, in one cell system and one set of blots, asked (a) which of the four eIF2α kinases is required per stressor, (b) whether ATF4 is even eIF2α-dependent, and (c) whether any IRE1-specific ER-stress marker moves.

**7. delta_vs_closest_paper**
Closest: **Wolzak 2022, EMBO J** (PMID 35791631). Difference: Wolzak used a *pure pharmacological ER stressor* (tunicamycin-class) in *PERK-knockout primary neurons* and asked whether neurons are resilient. This project uses *disease-model insults* in the *immortalized line the field actually publishes in*, tests *all four kinases plus DELE1/OMA1 plus the eIF2α-independent arm*, and adds an *IRE1-specific readout* Wolzak did not use as a discriminator. The claim is not "neurons are resilient" but "the published mechanistic label is frequently wrong."

**8. references**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | Wolzak K, et al. (Scheper) | Neuron-specific translational control shift ensures proteostatic resilience during ER stress | EMBO J 41(16):e110501 | 2022 | PMID 35791631; DOI 10.15252/embj.2021110501; PMC9379547 | SEARCH_SNIPPET |
| 2 | Fessler E, et al. | A pathway coordinated by DELE1 relays mitochondrial stress to the cytosol | Nature 579:433–437 | 2020 | PMID 32132706; DOI 10.1038/s41586-020-2076-4 | SEARCH_SNIPPET |
| 3 | Guo X, et al. | Mitochondrial stress is relayed to the cytosol by an OMA1–DELE1–HRI pathway | Nature 579:427–432 | 2020 | DOI 10.1038/s41586-020-2078-2 (PMID not captured) | SEARCH_SNIPPET |
| 4 | Perea V, et al. (Wiseman) | Pharmacologic activation of a compensatory integrated stress response kinase promotes mitochondrial remodeling in PERK-deficient cells | Cell Chem Biol | 2023 | PMC10029010 (PMID/DOI not captured) | SEARCH_SNIPPET |
| 5 | Torrence ME, et al. (Manning) | The mTORC1-mediated activation of ATF4 promotes protein and glutathione synthesis downstream of growth signals | eLife 10: article 63326 | 2021 | article 63326 (DOI/PMID not captured) | SEARCH_SNIPPET |
| 6 | authors not captured | mTORC1 Balances Cellular Amino Acid Supply with Demand for Protein Synthesis through Post-transcriptional Control of ATF4 | Cell Rep | 2017 | PMID 28494858 | SEARCH_SNIPPET |
| 7 | Bravo-Jimenez, Sharma, Karimi-Abdolrezaee | The integrated stress response in neurodegenerative diseases | Mol Neurodegener 20(1):20 | 2025 | DOI 10.1186/s13024-025-00811-6; PMC11837473 | SEARCH_SNIPPET |
| 8 | authors not captured | Cytosolic retention of HtrA2 during mitochondrial protein import stress triggers the DELE1-HRI pathway | journal not captured | ~2024 | PMC10981713 | SEARCH_SNIPPET |

**9. models_and_data**
HT-22 (in hand). Optional human cross-check in SH-SY5Y — **needs to be obtained**. Bioinformatics: **GSE174367** (verified: human prefrontal cortex snRNA-seq + snATAC-seq, late-stage AD, 191,890 nuclei; one reanalysis reports 8 control / 12 AD) and **GSE138852** (verified: Grubman entorhinal cortex, 6 control / 6 AD). **GSE147528** (frontal gyrus, AD progression) and **GSE157783** also appeared in results. Use these to ask whether the ATF4-target signature and EIF2AK1 vs EIF2AK3 expression localize to neurons or glia.

**10. key_experiments**
Bench (all within the student's list):
- siRNA matrix: *Eif2ak3*(PERK), *Eif2ak1*(HRI), *Eif2ak2*(PKR), *Eif2ak4*(GCN2), *Dele1*, *Oma1* × 4 stressors (glutamate 2–5 mM; OGD/reoxygenation; rotenone or MPP+; Aβ42 oligomer or corticosterone). WB: p-eIF2α(S51), total eIF2α, ATF4, CHOP, ATF3, loading control.
- qPCR: *Ddit3, Trib3, Chac1, Atf3, Asns* (ISR) vs *Hspa5, Herpud1, Edem1* (ER-specific). **Xbp1 splicing by RT-PCR + agarose gel** — the key IRE1-specific discriminator, costs essentially nothing and needs no kit.
- Pharmacologic discriminators: ISRIB (if ATF4 is ISRIB-insensitive → eIF2α-independent), GSK2606414 (PERK), Torin1/rapamycin (mTORC1 arm), thapsigargin/tunicamycin as positive controls.
- Optional extension that sharpens it: low-dose anisomycin as a ribosome-collision/ribotoxic-stress positive control plus *Zak* siRNA, to test whether some "ER stress" is really ribotoxic stress.
Bioinformatics: cell-type-resolved ATF4-target scoring in GSE174367/GSE138852 (R/Seurat, pseudobulk per cell type, limma/edgeR).
**Gating flags:** translation-rate measurement (SUnSET) needs an anti-puromycin antibody (~¥3–4k; optional, not load-bearing). Polysome profiling, proteomics, ribosome profiling: not available, **not required**. No co-IP or luciferase reporter needed.

**11. expected_and_negative_results**
Expected: at least two stressors show PERK-independent, HRI/DELE1-dependent ATF4 with no XBP1 splicing. Negative result (PERK dominates everywhere, XBP1 splices) is **publishable** as a rigor/validation paper in a mid-tier specialty journal, and is genuinely useful — it would license the field's existing interpretation for the first time. Partial result (one stressor reassigned) is the most likely and is publishable.

**12. difficulty_and_cost**
Difficulty **3/5**. ~¥35–50k. Buy: 5–6 antibodies (p-eIF2α is the expensive one), 6 siRNAs ×2 sequences each, ISRIB, GSK2606414, Torin1, tunicamycin/thapsigargin, qPCR master mix, plasticware. Nothing outsourced.

**13. timeline_months** 7–9 (bench 5–6, bioinformatics 1–2 in parallel, writing 1–2).

**14. target_journal_tier**
Solid specialty/mechanistic tier (roughly IF 3–6), not top-tier. Realistic venues: *Journal of Neurochemistry*, *Neurochemistry International*, *Cell Stress and Chaperones*. If the reassignment is clean and includes a functional rescue: *Neurobiology of Disease* or *Cell Death & Disease* are reachable but not promised.

**15. reviewer_attacks**
(i) "HT-22 is an SV40-immortalized line lacking ionotropic glutamate receptors — irrelevant to neurons." (ii) "Incomplete siRNA knockdown plus kinase compensation makes negative dependence uninterpretable" — must show knockdown efficiency per experiment and use two sequences. (iii) "This is methodological housekeeping, not new biology" — must deliver at least one positive reassignment plus a functional consequence (viability rescue by the correct kinase knockdown).

**16. prelim_ratings** novelty **M–H**; evidence-base **H**; overlap-risk **M**.

---

# TOPIC 2

**1. title_en**
Gain or loss? A dose-resolved test of the top ALS eQTL gene SCFD1 in neuronal cells

**2. core_question**
Does a GWAS/eQTL-sized (20–40%) reduction of SCFD1 in neuronal cells produce measurable secretory-pathway stress and reduced viability, or does a phenotype appear only near complete loss — and does SCFD1 **over**expression (the direction reported in ALS motor cortex) phenocopy or oppose knockdown?

**3. hypothesis**
SCFD1 has a steep threshold: ≤40% knockdown is phenotypically silent for UPR markers and viability, while >60% knockdown induces XBP1 splicing, BiP/CHOP and a chaperone-transcript decrease mirroring the *Drosophila* result; overexpression does **not** phenocopy, i.e. the risk mechanism is loss-of-function and the elevated SCFD1 seen in ALS cortex is compensatory or secondary.

**4. novelty_claim**
New: the first mammalian neuronal dose–response for SCFD1, built specifically to adjudicate a controversy that has been stated in print. Avoids the "human-genetics-to-cells transplant" trap because the test is directional and quantitative — it is not "knock down a GWAS gene and run enrichment," it is "does the eQTL-sized perturbation do anything, and in which direction." This is exactly the category "a specific prediction from human genetics nobody tested in cells" plus "defining a limiting condition."

**5. state_of_the_art**
SCFD1 (Sec1/Munc18-like; ER→Golgi and Golgi→ER transport, partners Syntaxin 5 and the COG complex) is the only gene reaching genome-wide significance for mediating ALS risk through eQTLs (Iacoangeli 2021, PMID 34708205). In that study rs8005942 showed **opposite** genotype–expression directions in controls vs ALS; SCFD1 was **increased** in ALS motor cortex in rarer-genotype homozygotes and this correlated with **shorter** survival; SCFD1 eQTLs acted as a trans-eQTL hotspot. Borg 2023 (PMID 36944290) showed fly *Slh* knockdown causes climbing/flight deficits at mild knockdown and NMJ defects plus lethality at strong knockdown, with chaperone genes downregulated. Cauchi 2024 (*Neural Regen Res* 19(6):1201–1202) argues explicitly that a gain-of-function role "does not appear to concur with the in vivo data, which suggests just the opposite." A negative association replication also exists ("Lack of an association between SCFD1 rs10139154 polymorphism and amyotrophic lateral sclerosis").

**6. specific_open_problem**
There is no mammalian neuronal SCFD1 perturbation study at all in what I found — no dose–response, no overexpression arm, and no measurement of whether the fly chaperone-downregulation signature is conserved. The human genetic and the animal functional data point in opposite directions and the field has said so.

**7. delta_vs_closest_paper**
Closest: **Borg et al. 2023, Neurobiol Aging** (PMID 36944290). Difference: that paper is *Drosophila*, RNAi only, no overexpression, no graded dose series calibrated to eQTL effect size, and no mammalian neuronal readout. This project supplies the mammalian neuronal dose–response **and** the opposite-direction arm, which is the specific thing needed to resolve the GOF/LOF dispute Cauchi 2024 raised.

**8. references**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | Iacoangeli A, … Jones AR | SCFD1 expression quantitative trait loci in amyotrophic lateral sclerosis are differentially expressed | Brain Commun 3(4):fcab236 | 2021 | PMID 34708205; DOI 10.1093/braincomms/fcab236; PMC8545614 | SEARCH_SNIPPET |
| 2 | Borg R, Purkiss A, Cacciottolo R, Herrera P, Cauchi RJ | Loss of amyotrophic lateral sclerosis risk factor SCFD1 causes motor dysfunction in Drosophila | Neurobiol Aging | 2023 | PMID 36944290; DOI 10.1016/j.neurobiolaging.2023.02.005 | SEARCH_SNIPPET |
| 3 | Cauchi RJ | SCFD1 in amyotrophic lateral sclerosis: reconciling a genetic association with in vivo functional analysis | Neural Regen Res 19(6):1201–1202 | 2024 | PMC11467948 (PMID not captured) | SEARCH_SNIPPET |
| 4 | authors not captured | ALS/FTD-associated mutation in cyclin F inhibits ER-Golgi trafficking, inducing ER stress, ERAD and Golgi fragmentation | journal not captured | ~2023 | PMC10665471 | SEARCH_SNIPPET |
| 5 | authors not captured | C9orf72-Associated Dipeptide Repeat Expansions Perturb ER-Golgi Vesicular Trafficking, Inducing Golgi Fragmentation and ER Stress, in ALS/FTD | journal not captured | ~2024 | PMC11584443 | SEARCH_SNIPPET |
| 6 | authors not captured | Lack of an association between SCFD1 rs10139154 polymorphism and amyotrophic lateral sclerosis | journal not captured | not captured | none captured | TITLE_ONLY |
| 7 | authors not captured | Genome-Wide Gene-Set Analysis Approaches in Amyotrophic Lateral Sclerosis | J Pers Med 12(11):1932 | 2022 | none captured | TITLE_ONLY |

**9. models_and_data**
HT-22 (in hand; mouse *Scfd1* is the conserved-function arm). **SH-SY5Y needs to be obtained** and is strongly advised, because the eQTL is human. Human genetics: ALS GWAS summary statistics and GTEx/brain eQTL — **accession to be identified** (I verified no accession). Post-mortem ALS cortex expression data — **accession to be identified**.

**10. key_experiments**
- Graded siRNA titration (and/or two siRNAs at several concentrations) to hit ~20/40/60/80% knockdown, verified per well by qPCR **and** WB. This titration *is* the experiment; do not skip the calibration.
- Overexpression arm: SCFD1 plasmid (purchase/synthesis ~¥2–4k), transfection (in hand).
- Readouts: Xbp1 splicing RT-PCR (cheap, IRE1-specific), BiP/HSPA5, CHOP, ATF4 by WB+qPCR; the fly-derived chaperone panel (*Hspa5, Hspa8, Dnajb1, Hsp90b1*) by qPCR as a cross-species conservation test; GM130/golgin-97/TGN46 by WB; CCK-8 viability and LDH.
- Cheap secretion/Golgi-function substitute (avoids gated assays): electrophoretic mobility shift of an endogenous heavily glycosylated protein (e.g. LAMP1) on WB as a Golgi-processing readout, rather than a RUSH or luciferase-secretion reporter.
**Gating flags:** Golgi fragmentation ideally needs immunofluorescence — "possibly negotiable" per the student's resources; if unavailable, WB of Golgi proteins plus the glycosylation shift is a defensible substitute and should be stated as a limitation. Gaussia/SEAP secretion reporters are luciferase-class — **gated**, substitute as above. Co-IP with Syntaxin 5 — **gated**, omit. iPSC motor neurons — out of reach, omit.

**11. expected_and_negative_results**
Expected: a threshold well above eQTL effect size, i.e. partial loss is tolerated. That is a *strong* negative-with-teeth result: it says the SCFD1 GWAS signal is unlikely to act through simple haploinsufficiency-style trafficking stress in neurons, and constrains the field's default interpretation. Publishable either way. The worst outcome is a flat no-effect at all doses with a weak overexpression arm — mitigate by including a positive control (brefeldin A) in every plate.

**12. difficulty_and_cost**
Difficulty **3/5**. ~¥30–45k (+¥5–10k if SH-SY5Y added). Buy: SCFD1 antibody — **availability/validation risk for mouse, check before committing**; SCFD1 plasmid; siRNAs; UPR antibody set; qPCR reagents.

**13. timeline_months** 8–11.

**14. target_journal_tier**
Specialty genetics/neurobiology tier. Realistic: *Neurobiology of Aging* (published the fly paper; editorially receptive to the follow-up), *Journal of Neurochemistry*, *Molecular Neurobiology*. *Human Molecular Genetics* is a stretch and would need the human-cell arm.

**15. reviewer_attacks**
(i) "Mouse line, human eQTL — the dose calibration is not transferable." (ii) "No neurons, no motor neurons, no patient material." (iii) "Absence of phenotype at low knockdown may just be assay insensitivity" — pre-register a positive control and report assay sensitivity explicitly.

**16. prelim_ratings** novelty **H**; evidence-base **H**; overlap-risk **M** (the Cauchi group is clearly working toward mammalian data — this is a race; the 12-month clock matters).

---

# TOPIC 3

**1. title_en**
Oxytosis is not canonical ferroptosis: does glutamate/xCT-block death in HT-22 require ACSL4?

**2. core_question**
Is glutamate-induced HT-22 death ACSL4-dependent (canonical ferroptosis execution) or ACSL4-independent and ALOX12/15- and AIF-dependent (classical oxytosis), and does it differ from RSL3/GPX4-inhibitor death in the same cells?

**3. hypothesis**
Glutamate (system x_c^- block, mechanistically equivalent to erastin/cystine deprivation) kills HT-22 largely **independently** of ACSL4, whereas RSL3 killing in the same cells is ACSL4-dependent; glutamate death instead requires ALOX12/15 and AIF nuclear translocation. If so, the very large literature claiming "compound X rescues glutamate-induced ferroptosis via Nrf2/GPX4/ACSL4" has mis-assigned the executioner.

**4. novelty_claim**
New: a within-model, side-by-side dependency test that discriminates two competing explanations for the same phenotype, using the single most-used neuronal death model in the field. Avoids the "swap the drug/model" trap because no new compound is introduced — the manipulated variables are the executioner genes. Avoids "DEG + correlation" entirely. It adjudicates a controversy that the field's own champions concede is unresolved in vivo for lack of discriminating markers.

**5. state_of_the_art**
Maher/Lewerenz and colleagues have argued oxytosis and ferroptosis should be treated as "two names for the same cell death pathway" (Front Neurosci 2018, PMC5920049; Cell Chem Biol 2020, pii S2451-9456(20)30426-8), while conceding it has "proven extremely difficult to unequivocally assign which of these pathways is responsible for neuronal loss" because no established markers distinguish them. HT-22 lacks ionotropic glutamate receptors, so glutamate toxicity there is x_c^- blockade, not excitotoxicity. Doll 2017 (Nat Chem Biol, DOI 10.1038/nchembio.2239) established ACSL4 as a ferroptosis-sensitivity determinant. Critically, a review in my results reported that **ACSL4 was required for GPX4-inhibitor-induced ferroptosis but not for erastin- or cysteine-deprivation-induced ferroptosis** — I could not identify the primary paper for that claim before the search budget ran out, and it must be tracked down. ALOX12 supports an explicitly ACSL4-independent route. Seiler 2008 (Cell Metab 8:237–248, DOI 10.1016/j.cmet.2008.07.005) established the GPX4 → 12/15-LOX → AIF axis.

**6. specific_open_problem**
Whether the canonical ferroptosis executioner module is required for the canonical neuronal oxidative-glutamate death has, as far as my (incomplete) searching showed, never been tested head-to-head in HT-22 with inducer-matched controls — despite hundreds of papers assuming it.

**7. delta_vs_closest_paper**
Closest: **Maher/Lewerenz, Cell Chem Biol 2020** (review, "Using the Oxytosis/Ferroptosis Pathway to Understand and Treat Age-Associated Neurodegenerative Diseases"). Difference: that is a unification *argument* from shared features (GSH depletion, lipid peroxidation, caspase independence). This project supplies the genetic-requirement test the argument lacks, with the inducer as an explicit variable. A second closest is Seiler 2008, which established the 12/15-LOX/AIF arm but predates ACSL4 and never compared inducers.

**8. references**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | Lewerenz J, …, Maher P (full list not captured) | Oxytosis/Ferroptosis—(Re-)Emerging Roles for Oxidative Stress-Dependent Non-apoptotic Cell Death in Diseases of the Central Nervous System | Front Neurosci | 2018 | PMC5920049 | SEARCH_SNIPPET |
| 2 | authors not captured (Maher group) | Using the Oxytosis/Ferroptosis Pathway to Understand and Treat Age-Associated Neurodegenerative Diseases | Cell Chem Biol, pii S2451-9456(20)30426-8 | 2020 | none captured | SEARCH_SNIPPET |
| 3 | Seiler A, et al. | Glutathione Peroxidase 4 Senses and Translates Oxidative Stress into 12/15-Lipoxygenase Dependent- and AIF-Mediated Cell Death | Cell Metab 8(3):237–248 | 2008 | DOI 10.1016/j.cmet.2008.07.005 (PMID explicitly not found in search) | SEARCH_SNIPPET |
| 4 | authors not captured (Doll/Conrad) | ACSL4 dictates ferroptosis sensitivity by shaping cellular lipid composition | Nat Chem Biol | 2017 | DOI 10.1038/nchembio.2239 (from article URL) | SEARCH_SNIPPET |
| 5 | authors not captured | Origins of nervous tissue susceptibility to ferroptosis | journal not captured | ~2023 | PMC10308196 | SEARCH_SNIPPET |
| 6 | authors not captured | ACSL4 and the lipoxygenases 15/15B are pivotal for ferroptosis induced by iron and PUFA dyshomeostasis in dopaminergic neurons | Free Radic Biol Med, pii S0891584922011121 | 2022 | none captured | SEARCH_SNIPPET |
| 7 | authors not captured | Inhibition of VDAC1 Protects Against Glutamate-Induced Oxytosis and Mitochondrial Fragmentation in Hippocampal HT22 Cells | journal not captured | ~2024 | PMC11469849 | SEARCH_SNIPPET |
| 8 | authors not captured | Reduced Sulfation Enhanced Oxytosis and Ferroptosis in Mouse Hippocampal HT22 Cells | journal not captured | ~2020 | PMC7022473 | SEARCH_SNIPPET |

**9. models_and_data**
HT-22 only (in hand). No public dataset required; optionally a public lipidomics/transcriptomics reanalysis — **accession to be identified**.

**10. key_experiments**
- siRNA: *Acsl4*, *Alox12*, *Alox15*, *Aifm1*, *Gpx4* (positive control), two sequences each.
- Inducer panel as the second variable: glutamate (x_c^- block) | erastin | cystine-free medium | RSL3 (GPX4 inhibitor) | H2O2.
- Readouts, all in-hand or cheap kits: CCK-8 and LDH viability; WB for ACSL4, GPX4, AIF (plus cytosolic/nuclear fractionation, which needs only buffers), PARP1, 4-HNE adducts; MDA and GSH colorimetric kits; C11-BODIPY lipid peroxidation read on a **plate reader** (flow cytometry would be better but is **gated** — plate-reader ratio is an accepted substitute); rescue pharmacology with ferrostatin-1, liproxstatin-1, baicalein (12-LOX), deferoxamine, z-VAD.
**Gating flags:** flow cytometry **not available** — use plate-reader C11-BODIPY and state the limitation. Lipidomics/mass spectrometry **not available**; outsourcing oxidized-phospholipid lipidomics is expensive (well above the budget for a useful n) and is **not required** for the genetic-dependency claim — say so explicitly in the paper's limitations.

**11. expected_and_negative_results**
Expected: ACSL4 knockdown protects against RSL3 but not glutamate; ALOX12/15 and AIF knockdown protect against glutamate. Negative result (ACSL4 required for both) is **publishable** and valuable — it would be the first genetic validation of the unification hypothesis in the field's own model, and it would legitimize a large existing literature. Either outcome is a paper.

**12. difficulty_and_cost**
Difficulty **2/5** — the cheapest and most certain to finish. ~¥30–40k. Buy: 5 siRNA pairs; ACSL4, GPX4, 4-HNE, AIF, PARP1 antibodies; RSL3, erastin, Fer-1, Lip-1, baicalein, DFO; MDA/GSH kits; C11-BODIPY.

**13. timeline_months** 6–8.

**14. target_journal_tier**
Redox/cell-death specialty tier. Realistic: *Free Radical Biology and Medicine*, *Cell Death Discovery*, *Neurochemistry International*. *Redox Biology* is a stretch and would need the inducer panel to be complete and n≥4.

**15. reviewer_attacks**
(i) **"Already known / already done"** — this is the real danger and the gating literature check above must be done first. (ii) "Knockdown is not knockout; residual ACSL4 suffices" — must show >80% protein loss and include a double knockdown. (iii) "Without oxidized-lipid mass spectrometry you cannot call anything ferroptosis" — pre-empt by framing the claim as *executioner-gene requirement*, not lipid identity.

**16. prelim_ratings** novelty **M**; evidence-base **H**; overlap-risk **H** (must be verified before committing).

---

# TOPIC 4

**1. title_en**
Does neuronal "Golgi stress" exist? Arm-resolved test of the GASE/TFE3 and CREB3–ARF4 programs in neuronal cells

**2. core_question**
In neuronal cells, do insults reported to cause Golgi fragmentation in ALS/FTD and injury models actually activate a transcriptional Golgi stress response (GASE/TFE3 targets, CREB3→ARF4, HSP47), or is the fragmentation transcriptionally silent — and is ARF4 the common node?

**3. hypothesis**
Neuronal cells engage the CREB3–ARF4 arm selectively (consistent with the one existing neuronal data point) while the TFE3/GASE arm, defined in HeLa/HEK293, is weak or absent; several insults that fragment the Golgi induce **no** Golgi-stress transcription at all, and part of what is currently read as Golgi stress is PERK/ATF4 bleed-through.

**4. novelty_claim**
New: the first arm-resolved, cell-type-specific survey of the mammalian Golgi stress response in neuronal cells, with an explicit ISR-subtraction design. Avoids the "transplant a mature mechanism to a new disease" trap because the question is *whether the response exists in this cell type and which arm*, with a pre-specified discriminator (GASE targets vs ATF4 targets under PERK knockdown) — and the known confound is built into the design: a Golgi stressor used throughout the field (monensin) was reported to act via PERK/ATF4, so ISR subtraction is mandatory, not decorative.

**5. state_of_the_art**
The mammalian Golgi stress response comprises TFE3/GASE (targets include GCP60/ACBD3, GM130, giantin; vesicular-transport targets STX3A, WIPI49, RAB20; MLX is a GASE repressor), HSP47 (anti-apoptotic) and CREB3→S1P/S2P cleavage→ARF4 (pro-apoptotic) arms (Taniguchi & Yoshida, Cell Struct Funct 42(1), 2017). Monensin, a standard Golgi stressor, was reported to act via the PERK/ATF4 pathway (Mol Biol Cell 2018, DOI 10.1091/mbc.E17-11-0693). The only neuronal data I found is Shirai 2023 (PMID 37606396): CHMP2B-T104N accumulates in the Golgi in N1E-115 cells, selectively upregulates the Arf4 arm, and Arf4 siRNA rescues process elongation. A 2024 review ("Emerging Evidence of Golgi Stress Signaling for Neuropathies," Neurol Int 16(2):24, PMC10961782) frames the area as emerging. Recent additions: a PGSE proteoglycan arm (PMC11926408) and PI4P dysregulation at the trans-Golgi as an activator (J Biol Chem, pii S0021925824025778); plus a 2025/2026 review of ER and Golgi stress in secretion (PMID 42098616, PMC13359550). Golgi fragmentation is repeatedly reported in ALS/FTD models (cyclin F, PMC10665471; C9orf72 DPRs, PMC11584443) **without** transcriptional-response measurement.

**6. specific_open_problem**
Golgi fragmentation is inferred to mean "Golgi stress" from morphology alone in the neurodegeneration literature. Whether the transcriptional program fires in neurons, which arm, and how much of the apparent signal is ISR contamination, is unmeasured.

**7. delta_vs_closest_paper**
Closest: **Shirai et al. 2023, Neurol Int** (PMID 37606396). Difference: that paper tested one mutation (CHMP2B-T104N) in one line (N1E-115), found the Arf4 arm up, and stopped. This project tests **multiple disease-relevant insults against multiple canonical Golgi stressors across all three arms with ISR subtraction**, i.e. it asks whether the Arf4 result generalizes or was mutation-specific, and whether the field's morphology-based inference is ever valid.

**8. references**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | Shirai et al. | FTD/ALS Type 7-Associated Thr104Asn Mutation of CHMP2B Blunts Neuronal Process Elongation, and Is Recovered by Knockdown of Arf4, the Golgi Stress Regulator | Neurol Int 15(3):63 | 2023 | PMID 37606396; PMC10443297 | SEARCH_SNIPPET |
| 2 | Taniguchi M, Yoshida H (authors not fully captured) | TFE3, HSP47, and CREB3 Pathways of the Mammalian Golgi Stress Response | Cell Struct Funct 42(1) | 2017 | none captured | SEARCH_SNIPPET |
| 3 | authors not captured | Emerging Evidence of Golgi Stress Signaling for Neuropathies | Neurol Int 16(2):24 | 2024 | PMC10961782; DOI 10.3390/... (not captured) | SEARCH_SNIPPET |
| 4 | authors not captured | Targeted protein unfolding uncovers a Golgi-specific transcriptional stress response | Mol Biol Cell | 2018 | DOI 10.1091/mbc.E17-11-0693 | SEARCH_SNIPPET |
| 5 | authors not captured | PGSE Is a Novel Enhancer Regulating the Proteoglycan Pathway of the Mammalian Golgi Stress Response | journal not captured | 2025 | PMC11926408 | SEARCH_SNIPPET |
| 6 | authors not captured | Dysregulation of PI4P in the trans Golgi regions activates the mammalian Golgi stress response | J Biol Chem, pii S0021925824025778 | 2024/2025 | none captured | SEARCH_SNIPPET |
| 7 | authors not captured | Endoplasmic reticulum and Golgi stress signaling-mediated regulation of protein secretion | journal not captured | 2025/2026 | PMID 42098616; PMC13359550 | SEARCH_SNIPPET |
| 8 | authors not captured | Golgi stress response reprograms cysteine metabolism to confer cytoprotection in Huntington's disease | journal not captured | ~2018 | PMC5789946 | SEARCH_SNIPPET |

**9. models_and_data**
HT-22 (in hand). N1E-115 (the line in the only neuronal precedent) — **needs to be obtained**, cheap and worth it for direct comparability. No dataset required; optional public RNA-seq reanalysis — **accession to be identified**.

**10. key_experiments**
- Stressor panel: monensin, nigericin, brefeldin A (ER–Golgi control), plus disease-relevant insults (OGD/R, glutamate, proteasome inhibition, α-syn or DPR expression if constructs are obtainable).
- qPCR panel: *Acbd3/Gcp60, Golga2, Golgb1, Arf4, Serpinh1/Hsp47, Tfe3, Creb3, Mlx, Stx3a, Rab20* vs ISR panel *Ddit3, Trib3, Chac1, Atf4*; plus Xbp1 splicing RT-PCR.
- **ISR subtraction (the design's key move):** repeat under *Eif2ak3*/PERK siDNA knockdown; GASE/ARF4 targets that persist are genuinely Golgi-stress, those that vanish were ATF4 bleed-through.
- siRNA *Tfe3*, *Creb3*, *Arf4* + viability and (if IF available) process/Golgi morphology.
- WB: ARF4, GM130, HSP47, TFE3 (mobility shift as the dephosphorylation proxy).
**Gating flags:** TFE3 nuclear translocation is best shown by IF or nuclear/cytosolic fractionation — fractionation is cheap and in reach; IF is "possibly negotiable." HyT36-style targeted unfolding reagents are likely unobtainable — omit, use monensin/nigericin. No MS, no ChIP needed. ARF4 and HSP47 antibody availability must be checked first.

**11. expected_and_negative_results**
Expected: a partly ISR-contaminated picture with ARF4 as the robust neuronal node. Negative result (no Golgi-stress transcription in neuronal cells under any disease insult) is **publishable and arguably more interesting** — it would mean the morphology-based "Golgi stress" claims in the ALS/AD literature are unsupported.

**12. difficulty_and_cost**
Difficulty **2.5/5**. ~¥25–40k. Buy: monensin/nigericin/BFA, 4–5 antibodies (ARF4, HSP47, TFE3 availability risk), 3–4 siRNAs, qPCR primers and reagents.

**13. timeline_months** 7–9.

**14. target_journal_tier**
Specialty/organelle-biology tier. Realistic: *Neurochemistry International*, *Cell Structure and Function*, *Journal of Neurochemistry*. *Neurology International* published the precedent paper but is low-tier; use only as a fallback.

**15. reviewer_attacks**
(i) "Golgi stress response is defined by specific reporters you do not have (GASE-luciferase)" — luciferase reporters are **gated**; must defend endogenous-target qPCR as the readout. (ii) "Negative result = failed experiment" — must include a cell type where the arm *does* fire (HeLa/HEK293 side-by-side, HEK293 **needs to be obtained**) to prove assay competence. (iii) "Monensin is not a specific Golgi stressor" — this is correct and is why the ISR-subtraction arm exists; foreground it.

**16. prelim_ratings** novelty **M–H**; evidence-base **M**; overlap-risk **L–M** (small field, mostly a few Japanese groups).

---

# TOPIC 5

**1. title_en**
Is UFM1 conjugation a rate-limiting node for neuronal ER proteostasis?

**2. core_question**
Do disease-relevant ER and translational stressors change RPL26 UFMylation flux in neuronal cells, and is partial loss of UBA5 or UFL1 — at the level implied by patient hypomorphic variants — sufficient to trigger an ISR/ER-stress program and reduce viability?

**3. hypothesis**
Neuronal cells run high constitutive RPL26 UFMylation at the ER; partial UBA5/UFL1 loss is sufficient (unlike in non-neuronal cells, where compensation is expected) to raise p-eIF2α/ATF4/CHOP and sensitize to translocation stress, identifying ER-ribosome quality control — rather than ER-phagy or general autophagy — as the neuronally limiting UFM1 function.

**4. novelty_claim**
New: a neuronal dose–requirement test for the newest-described UFM1 function (release of 60S from ER translocons), motivated by human recessive neurological genetics. Avoids the "transplant a mechanism" trap because the question is *which of several known UFM1 functions is the neuronally limiting one*, which is a discrimination, not a relabelling. Avoids "two molecules in an axis" because no partner is being proposed.

**5. state_of_the_art**
UFM1 is activated by UBA5 and conjugated with high selectivity to RPL26 K132/K134 on 60S subunits docked at the ER membrane (PNAS 2019, DOI 10.1073/pnas.1816202116); RPL26 UFMylation is essential for ER-localized ribosome-associated quality control (PNAS 2023, DOI 10.1073/pnas.2220340120); the UFM1 E3 ligase recognizes and releases 60S ribosomes from ER translocons (Nature 2024, DOI 10.1038/s41586-024-07093-w, PMC10937380). Loss of UFMylation genes strongly induces ER stress, and UFM1 genes are UPR targets. Human genetics: UBA5 variants cause recessive cerebellar ataxia; UFC1 variants cause early-onset encephalopathy with progressive microcephaly. A 2025 review reports altered UFMylation components in excitatory neurons and reduced RPL26 immunoreactivity in AD neurons (Mol Neurodegener, DOI 10.1186/s13024-025-00855-8); a 2025 Nat Rev Mol Cell Biol review (DOI 10.1038/s41580-025-00944-y) synthesizes the mechanism.

**6. specific_open_problem**
Everything neuronal in this field is association or inference. There is no neuronal measurement of UFMylation flux under stress, and no test of whether the pathway is limiting at patient-relevant partial loss rather than at knockout.

**7. delta_vs_closest_paper**
Closest: **"The UFM1 E3 ligase recognizes and releases 60S ribosomes from ER translocons," Nature 2024** (DOI 10.1038/s41586-024-07093-w). Difference: that work defines the biochemistry in non-neuronal systems at full loss-of-function. This project asks the orthogonal question — flux under neuronal disease stress, and sufficiency at partial loss — which is the question the human genetics actually poses and which no paper I found addresses.

**8. references**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | authors not captured | The UFM1 E3 ligase recognizes and releases 60S ribosomes from ER translocons | Nature | 2024 | DOI 10.1038/s41586-024-07093-w; PMC10937380 | SEARCH_SNIPPET |
| 2 | authors not captured | RPL26/uL24 UFMylation is essential for ribosome-associated quality control at the endoplasmic reticulum | PNAS | 2023 | DOI 10.1073/pnas.2220340120 | SEARCH_SNIPPET |
| 3 | authors not captured | Ribosomal protein RPL26 is the principal target of UFMylation | PNAS | 2019 | DOI 10.1073/pnas.1816202116 | SEARCH_SNIPPET |
| 4 | authors not captured | The many connections of UFMylation with Alzheimer's disease: a comprehensive review | Mol Neurodegener | 2025 | DOI 10.1186/s13024-025-00855-8 | SEARCH_SNIPPET |
| 5 | authors not captured | The mechanistic basis and cellular functions of UFMylation | Nat Rev Mol Cell Biol | 2025 | DOI 10.1038/s41580-025-00944-y | SEARCH_SNIPPET |
| 6 | authors not captured | UFM1 at the endoplasmic reticulum: linking ER stress, ribosome quality control, and ER-phagy | journal not captured | 2025 | PMC12687425 | SEARCH_SNIPPET |
| 7 | authors not captured | UFMylation: A Potential Modification for Neurological Diseases | journal not captured | 2025 | PMC12174942 | SEARCH_SNIPPET |

**9. models_and_data**
HT-22 (in hand). Human cross-check in SH-SY5Y — **needs to be obtained**. No dataset strictly required; optional snRNA-seq check of UFM1-pathway gene expression by cell type in **GSE174367** / **GSE138852** (both verified accessions).

**10. key_experiments**
- WB of the UFM1 conjugate ladder and the UFMylated-RPL26 shifted band under stress: tunicamycin, thapsigargin, glutamate, low-dose anisomycin (collision inducer, very cheap), emetine, DTT.
- siRNA: *Uba5*, *Ufl1*, *Ddrgk1/Ufbp1*, *Ufsp2* (de-UFMylase; expect the opposite shift), at graded doses.
- Readouts: p-eIF2α, ATF4, CHOP; Xbp1 splicing RT-PCR; *Hspa5/Herpud1* qPCR; CCK-8; plus p-p38/p-JNK as a ribotoxic-stress indicator.
**Gating flags:** this topic's single biggest risk is **antibody performance** — anti-UFM1 and the RPL26 shift must be validated in mouse cells, and UFSP2 knockdown is the correct specificity control. Budget a validation month and a fallback. Polysome profiling and co-IP are **gated** and should be designed out, not outsourced (outsourced polysome/ribosome profiling is far above ¥80k for a useful n). Proteomics not required.

**11. expected_and_negative_results**
Expected: measurable flux change plus sufficiency at partial loss. Negative result (no neuronal flux change; full compensation at partial loss) is **publishable but weaker** — it argues the UBA5/UFC1 neurological phenotypes do not run through ER-RQC in this cell type, which is a useful constraint but a harder sell. This is the topic with the worst negative-result value.

**12. difficulty_and_cost**
Difficulty **3.5/5**. ~¥35–55k, of which ¥12–16k is antibodies alone. Buy: UFM1, RPL26, UBA5, DDRGK1 antibodies; 4 siRNAs; anisomycin, emetine, tunicamycin, thapsigargin.

**13. timeline_months** 9–12 (do not attempt in 6).

**14. target_journal_tier**
Specialty biochemistry/neurochemistry tier. Realistic: *Journal of Neurochemistry*, *Cell Stress and Chaperones*, *FEBS Letters* / *Biochemical Journal*.

**15. reviewer_attacks**
(i) "UFMylation band shifts are notoriously artefact-prone — show UFSP2 and UBA5 controls and a conjugation-dead rescue." (ii) "Without polysome or ribosome-profiling data you cannot claim an ER-RQC defect." (iii) "A cell line is the wrong model for a recessive neurodevelopmental disease."

**16. prelim_ratings** novelty **M–H**; evidence-base **M**; overlap-risk **M** (fast field, well-funded labs; the 2024 Nature group will keep moving).

---

# TOPIC 6

**1. title_en**
Repair-pathway choice at damaged lysosomes in neuronal cells: PITT, ESCRT, or neither?

**2. core_question**
When lysosomes are damaged in neuronal cells, is membrane repair carried by the ESCRT-independent PITT route, by ESCRT (including the newly described TFG–TSG101/LASER step), or by neither — and does blocking the dominant route sensitize neuronal cells to lysosomotropic and proteotoxic injury?

**3. hypothesis**
Neuronal cells depend predominantly on the PITT route and are relatively insensitive to loss of ESCRT components; consequently, the ESCRT-centric model built from non-neuronal cells over-predicts neuronal vulnerability, and the HSP-gene TFG acts in neurons through a narrower window than in glia.

**4. novelty_claim**
New: a cell-type-resolved genetic requirement test for lysosome repair in neuronal cells, directly adjudicating a claim made in a 2025 preprint, with viability as the functional endpoint. Avoids fake novelty because it is a head-to-head requirement test between two live competing models, not a transplant. Human-genetics anchor: TFG mutations cause hereditary spastic paraplegia and were reported to impair lysosomal ESCRT recruitment.

**5. state_of_the_art**
The LASER pathway (Nature 2026, DOI 10.1038/s41586-026-10604-6, PMC13442042) reports TFG binding TSG101 to drive sequential ESCRT-I→III assembly, that HSP-causing TFG mutations impair oligomerization and resealing, and — notably — that "even healthy neurons undergo constitutive, albeit transient, lysosomal permeabilization." A 2025 preprint (PMC13487023) reports that astrocytes preferentially recruit ESCRT while neurons preferentially engage the ESCRT-independent PITT pathway, with both recruiting TAX1BP1 and p62. A 2026 Nat Cell Biology paper adds DFCP1-containing ER microdomains as a repair route (DOI 10.1038/s41556-026-02062-z). Reviews from 2025 frame ESCRT-dependent and PITT routes as parallel.

**6. specific_open_problem**
The neuron-vs-glia repair-pathway claim exists only as a preprint and only as a recruitment (imaging) observation. There is no genetic requirement test and no functional (survival) consequence in neuronal cells.

**7. delta_vs_closest_paper**
Closest: **"Astrocytes mobilize a broader repertoire of lysosomal repair mechanisms than neurons," bioRxiv 2025 / PMC13487023** (preprint). Difference: that work shows *recruitment preference* by imaging. This project tests *requirement* by knockdown of PITT components (PI4K2A, OSBP/ORP family) versus ESCRT components (CHMP4B, TSG101, ALIX) versus TFG, with survival and lysosomal-integrity endpoints — i.e. it converts a correlation into a dependency, which the preprint does not do.

**8. references**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | authors not captured | LASER couples damage sensing to ESCRT assembly for lysosome repair | Nature | 2026 | DOI 10.1038/s41586-026-10604-6; PMC13442042 | SEARCH_SNIPPET |
| 2 | authors not captured | Astrocytes mobilize a broader repertoire of lysosomal repair mechanisms than neurons | bioRxiv (preprint) | 2025 | PMC13487023; preprint 2025.09.07.674666 | SEARCH_SNIPPET |
| 3 | authors not captured | DFCP1-containing ER microdomains mediate lysosomal membrane repair | Nat Cell Biol | 2026 | DOI 10.1038/s41556-026-02062-z | SEARCH_SNIPPET |
| 4 | authors not captured | Key Mechanisms in Lysosome Stability, Degradation and Repair (title possibly truncated) | Mol Cell Biol (Taylor & Francis) | 2025 | DOI 10.1080/10985549.2025.2494762 | SEARCH_SNIPPET |
| 5 | authors not captured | (lysosome damage/repair review) | Front Cell Death | 2025 | DOI 10.3389/fceld.2025.1669955 | TITLE_ONLY |
| 6 | authors not captured | Pathways to Repair or Remove Lysosomes Damaged by Extracellular Fine Particles | Springer book chapter | 2024 | DOI 10.1007/978-981-97-7067-0_13 | SEARCH_SNIPPET |
| 7 | authors not captured | Mechanisms and functions of lysosomal lipid homeostasis | Cell Chem Biol, pii S2451-9456(25)00035-2 | 2025 | none captured | TITLE_ONLY |

**9. models_and_data**
HT-22 (in hand); an astrocyte or non-neuronal comparator line — **needs to be obtained**. No dataset required.

**10. key_experiments**
- Damage: LLOMe (cheap), plus a proteotoxic arm (proteasome inhibition, or α-syn/tau fibril-free aggregate stress if available).
- siRNA: PITT arm (*Pi4k2a*, *Osbp*, *Osbpl9/11*); ESCRT arm (*Chmp4b*, *Tsg101*, *Pdcd6ip*/ALIX); *Tfg*; *Tax1bp1*, *Sqstm1*.
- Readouts avoiding gated methods: cathepsin B release into cytosol by WB after digitonin fractionation; LysoTracker/acridine orange on a **plate reader**; TFEB-target qPCR (*Ctsd, Lamp1, Sqstm1, Mcoln1*) as a damage-response proxy; CCK-8/LDH.
**Gating flags:** the field's standard readout is galectin-3/8 puncta by **immunofluorescence** — "possibly negotiable" for this student; without it the paper is materially weaker, so confirm microscope access **before** choosing this topic. Live confocal, super-resolution, FRAP: **not available**, design out. Lentivirus/CRISPR: **not available** — siRNA only, which limits durable depletion.

**11. expected_and_negative_results**
Expected: PITT-arm knockdown sensitizes, ESCRT-arm knockdown does not. Negative result (both or neither required) is publishable only in a low tier, because the claim being tested is new and a null is hard to distinguish from insufficient knockdown.

**12. difficulty_and_cost**
Difficulty **4/5**. ~¥40–60k. Buy: LLOMe, 8–9 siRNAs, galectin-3, LAMP1, cathepsin B, CHMP4B, p62, TAX1BP1 antibodies.

**13. timeline_months** 10–12+, realistically beyond 12.

**14. target_journal_tier**
Organelle/cell-biology specialty tier. Realistic: *Autophagy Reports*, *Journal of Cellular Physiology*, *Biochimica et Biophysica Acta – Molecular Cell Research*. Higher tiers are occupied by the groups that own this question.

**15. reviewer_attacks**
(i) "Your repair readouts are indirect; galectin puncta kinetics are the standard and you have none/few." (ii) "siRNA depletion is too shallow and too brief for a repair-kinetics question." (iii) "This is a one-line extension of an existing preprint."

**16. prelim_ratings** novelty **M–H**; evidence-base **M**; overlap-risk **H**.

---

## Committee recommendation (ranking)
1. **Topic 3** — highest probability of a finished, publishable paper inside 12 months; cheapest; only one real risk (prior art), which must be checked first.
2. **Topic 1** — best novelty-to-feasibility ratio; no gated technique is load-bearing.
3. **Topic 2** — highest genuine novelty, but it is a race against the group that owns the gene, and it needs a plasmid plus ideally a human line.
4. **Topic 4** — safest intellectual territory (uncrowded), moderate payoff, needs antibody availability confirmed.
5. **Topic 5** — good question, antibody risk could consume the whole year.
6. **Topic 6** — frontier and genuinely interesting, but imaging-dependent and racing Nature-level labs. Do not pick this if a publication in 12 months is required.

**Topics 1 and 6 should not both be run** by one student — nor should Topic 1 be expanded to absorb the ribotoxic-stress arm as a full second axis; keep that as a bounded extension.

---

## domain_landscape (2023–2026 frontier; ~540 words)

**What is crowded to the point of worthlessness.** Compound-rescues-HT-22-from-glutamate-via-Nrf2/HO-1/GPX4 is a template, not a research question: my searches alone surfaced gastrodin (2020), salidroside (2022) and isoliensinine (2024) running the identical design. OGD/R plus a non-coding-RNA–target axis plus Nrf2/NF-κB is the same template with a different insult. Standalone Mendelian randomization in neurodegeneration has become a production line. "DEG + enrichment on a public AD snRNA-seq dataset" is now routinely desk-rejected. An undergraduate entering any of these spends a year to produce something uncitable.

**What is crowded but still competitive at the top only.** TDP-43 condensate biology moved decisively in 2025 with the Cell paper on intra-condensate demixing inside stress granules generating pathological aggregates — a model that explicitly supersedes the older "stress granules are protective" position but does not settle it (a 2022 Nat Commun paper reports stress-induced TDP-43 mobility loss independent of granules, and a 2024 PDI preprint reports granule disassembly blocking aggregation). This is live and important, and it requires FRAP, live confocal and engineered variants — out of reach. Lysosome-membrane repair is the hottest organelle-QC area right now: LASER (TFG–TSG101→ESCRT, Nature 2026) and DFCP1/ER-microdomain repair (Nat Cell Biol 2026), with a 2025 preprint claiming neurons prefer PITT and astrocytes ESCRT. Fascinating, imaging-bound, and dominated by large labs. Programmed axon degeneration is in flux: the NMN/NAD⁺-ratio allosteric model for SARM1 (Figley 2021) is being challenged by 2024–2025 preprints proposing a NAD⁺-dependent liquid-to-solid transition, and base-exchange "inhibitors" turn out to activate SARM1 in vivo — but adjudicating any of it needs NMN/NAD⁺ mass spectrometry and axons, so it is not an undergraduate project.

**Where there is real, unoccupied room.** Three places. (1) **Attribution, not discovery.** The ISR is now known to be kinase-plural in neurons — Wolzak 2022 showed PERK-null neurons keep translational control via HRI; Perea 2023 showed HRI/GCN2 activators substitute for PERK; Torrence 2021 showed ATF4 can rise with no eIF2α phosphorylation at all; and the 2025 Mol Neurodegener review notes acute ISR inhibition sometimes changes nothing. Meanwhile the applied literature still writes "PERK/ER stress" from three bands. Nobody has done the per-stressor attribution. (2) **Organelle stress responses that were never tested in neurons.** The Golgi stress response (TFE3/GASE, HSP47, CREB3–ARF4) was built in HeLa/HEK293; the sole neuronal data point is one Arf4 result in N1E-115 (2023), while ALS/FTD papers infer "Golgi stress" from fragmentation alone. New arms are still being found (PGSE, 2025; PI4P, 2024). (3) **Human genetics with no cell biology.** SCFD1 is the only genome-wide-significant eQTL-mediated ALS gene, its direction of effect is openly contested in print (Cauchi 2024 vs the eQTL data), and there appears to be no mammalian neuronal perturbation study at all.

**Honest read on undergraduate opportunity.** It is narrow but real, and it lies entirely in *adjudication and attribution*, not discovery. An undergraduate with Western blot, qPCR, siRNA and one cell line cannot out-discover a funded lab, but can settle a question a funded lab has no incentive to settle. The binding constraint is not the budget — it is that the good projects all require admitting, in print, that a popular interpretation may be wrong, and defending a possible negative result. Topics 1, 3 and 4 are structured so the negative result is still a paper. Topics 5 and 6 are not, and that is why they rank last.

**2025–2026 papers I actually found:** LASER (Nature 2026); DFCP1 lysosome repair (Nat Cell Biol 2026); ATF4→mTOR suppression→PUMA in PD models (Cell Reports, 2026 pii, bioRxiv 2025); ISR in neurodegeneration review (Mol Neurodegener 2025); UFMylation mechanism review (Nat Rev Mol Cell Biol 2025) and UFMylation–AD review (Mol Neurodegener 2025); TDP-43 intra-condensate demixing (Cell 2025); DLK modular injury transcription (PLoS Genet, Dec 2025); SARM1 inhibition-to-activation review (Trends Pharmacol Sci 2025) plus 2025 base-exchange and parthanatos preprints; mitochondrial protein import stress (Phil Trans R Soc B 2025; bioRxiv 2026); RQC reviews (Exp Mol Med 2025; J Gerontol 2025); PGSE Golgi stress arm (2025); ER/Golgi stress and secretion (PMID 42098616); astrocyte-vs-neuron lysosome repair preprint (2025).

---

## rejected_ideas

1. **"Natural compound X protects HT-22 from glutamate-induced ferroptosis via Nrf2/HO-1/GPX4."** Pure drug swap on a template already run by gastrodin, salidroside and isoliensinine among hundreds — zero novelty by the committee's own definition.
2. **OGD/R in HT-22 + a lncRNA/miRNA–mRNA axis + Nrf2 or NF-κB.** Two well-studied molecules jammed into one axis; the single most saturated design in the cell-model neuro literature.
3. **Standalone Mendelian randomization of plasma proteins or metabolites against AD/PD/ALS.** Method-only output, no new biology, and increasingly desk-rejected; the student's MR skill is better spent as one supporting panel inside Topic 2.
4. **Adjudicating the SARM1 NMN/NAD⁺-ratio controversy.** Requires LC-MS/MS quantification of NMN and NAD⁺ (outsourced metabolomics far exceeds ¥80k at usable n), the key 2024–2025 challenges are still preprints, and HT-22 has no axon to score.
5. **Any iPSC-neuron, organoid or CRISPR-knock-in version of the above.** Explicitly out of reach on cost, time and culture skill; proposing it wastes the year.
6. **TDP-43 cryptic-exon biology (STMN2/UNC13A).** The causal intronic elements are primate-specific, so a mouse line cannot report the field's flagship readout, and the human side is owned by large consortia.
7. **Molecular docking of a compound to a proteostasis target, then "mechanism" from docking score plus a few Western blots.** Fake mechanism; publishable only in venues that will damage the student's record.
8. **Adjudicating PINK1/Parkin-independent basal mitophagy.** Requires mito-QC or mt-Keima reporters, flow cytometry and live imaging — all gated — and the central claim is an in vivo one that no cell line can test.
9. **Single-cell reanalysis of a public AD dataset producing DEGs, correlations and GO/KEGG with no wet validation.** The archetypal fake-novelty pattern; it would not survive review at any journal worth targeting.

---

## Sources
- [SARM1 metabolic sensor (Figley 2021), PubMed](https://pubmed.ncbi.nlm.nih.gov/33657413/) · [SARM1 base-exchange inhibitors activate SARM1 (preprint)](https://www.biorxiv.org/content/10.1101/2025.04.22.649875v1.full) · [SARM1 liquid-to-solid transition (preprint)](https://www.biorxiv.org/content/10.1101/2024.11.19.624255v1.full) · [Targeting SARM1 (Trends Pharmacol Sci 2025)](https://www.cell.com/trends/pharmacological-sciences/fulltext/S0165-6147(25)00219-6) · [SARM1 in neuronal parthanatos](https://pmc.ncbi.nlm.nih.gov/articles/PMC13285980/)
- [OMA1–DELE1–HRI (Guo 2020, Nature)](https://www.nature.com/articles/s41586-020-2078-2) · [DELE1 pathway (Fessler 2020), PubMed](https://pubmed.ncbi.nlm.nih.gov/32132706/) · [DELE1 iron-responsive pathway (Mol Cell 2023)](https://www.sciencedirect.com/science/article/pii/S1097276523004136) · [HtrA2 and import stress → DELE1-HRI](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10981713/)
- [Wolzak 2022, EMBO J](https://www.embopress.org/doi/full/10.15252/embj.2021110501) · [Perea 2023, Cell Chem Biol](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10029010/) · [ISR in neurodegenerative diseases (Mol Neurodegener 2025)](https://link.springer.com/article/10.1186/s13024-025-00811-6) · [ATF4 suppresses mTOR in PD models (Cell Reports)](https://www.cell.com/cell-reports/fulltext/S2211-1247(26)00910-1?rss=yes) · [ATF4 in neurons under mitochondrial stress](https://pmc.ncbi.nlm.nih.gov/articles/PMC13316428/)
- [mTORC1–ATF4 (eLife 63326)](https://elifesciences.org/articles/63326) · [mTORC1 post-transcriptional ATF4 control, PubMed](https://pubmed.ncbi.nlm.nih.gov/28494858/)
- [SCFD1 Drosophila (Borg 2023), PubMed](https://pubmed.ncbi.nlm.nih.gov/36944290/) · [SCFD1 eQTL in ALS (Brain Commun 2021)](https://academic.oup.com/braincomms/article/3/4/fcab236/6383134) · [SCFD1: reconciling genetics with in vivo function (Cauchi 2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11467948) · [Cyclin F and ER-Golgi trafficking](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10665471/) · [C9orf72 DPRs perturb ER-Golgi trafficking](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11584443/)
- [TFE3/HSP47/CREB3 Golgi stress response](https://www.jstage.jst.go.jp/article/csf/42/1/42_16023/_html/-char/en) · [CHMP2B T104N / Arf4 (Shirai 2023)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10443297/) · [Golgi stress signaling for neuropathies (2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10961782) · [Targeted protein unfolding uncovers Golgi-specific transcriptional stress response](https://www.molbiolcell.org/doi/10.1091/mbc.E17-11-0693) · [PGSE enhancer (2025)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11926408/) · [PI4P and the Golgi stress response](https://www.sciencedirect.com/science/article/pii/S0021925824025778) · [ER and Golgi stress in protein secretion, PubMed](https://pubmed.ncbi.nlm.nih.gov/42098616/)
- [UFM1 E3 ligase releases 60S from ER translocons (Nature 2024)](https://www.nature.com/articles/s41586-024-07093-w) · [RPL26 UFMylation and ER-RQC (PNAS 2023)](https://www.pnas.org/doi/10.1073/pnas.2220340120) · [RPL26 is the principal UFMylation target (PNAS 2019)](https://www.pnas.org/doi/10.1073/pnas.1816202116) · [UFMylation and Alzheimer's (2025)](https://molecularneurodegeneration.biomedcentral.com/articles/10.1186/s13024-025-00855-8) · [Mechanistic basis of UFMylation (Nat Rev Mol Cell Biol 2025)](https://www.nature.com/articles/s41580-025-00944-y)
- [Oxytosis/Ferroptosis in CNS disease (Front Neurosci 2018)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5920049/) · [Using the oxytosis/ferroptosis pathway (Cell Chem Biol 2020)](https://www.cell.com/cell-chemical-biology/fulltext/S2451-9456(20)30426-8) · [ACSL4 dictates ferroptosis sensitivity (Nat Chem Biol 2017)](https://www.nature.com/articles/nchembio.2239) · [Origins of nervous tissue susceptibility to ferroptosis](https://pmc.ncbi.nlm.nih.gov/articles/PMC10308196/) · [ACSL4 and 15-LOX in dopaminergic neuron ferroptosis](https://www.sciencedirect.com/science/article/abs/pii/S0891584922011121) · [VDAC1 inhibition and HT22 oxytosis](https://pmc.ncbi.nlm.nih.gov/articles/PMC11469849/) · [Reduced sulfation enhances oxytosis and ferroptosis in HT22](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7022473/) · [HT-22 line (Sigma SCC129)](https://sigmaaldrich.com/SL/en/product/mm/scc129)
- [LASER couples damage sensing to ESCRT (Nature 2026)](https://www.nature.com/articles/s41586-026-10604-6) · [Astrocytes vs neurons lysosomal repair (preprint)](https://pmc.ncbi.nlm.nih.gov/articles/PMC13487023/) · [DFCP1 ER microdomains in lysosomal repair (Nat Cell Biol 2026)](https://www.nature.com/articles/s41556-026-02062-z) · [Lysosome stability/degradation/repair review (2025)](https://www.tandfonline.com/doi/pdf/10.1080/10985549.2025.2494762)
- [TDP-43 intra-condensate demixing (Cell 2025)](https://www.cell.com/cell/fulltext/S0092-8674(25)00509-4) · [Alzforum coverage](https://www.alzforum.org/news/research-news/stress-granules-does-demixing-seed-tdp-43-aggregation) · [TDP-43 mobility loss independent of stress granules (Nat Commun 2022)](https://www.nature.com/articles/s41467-022-32939-0)
- [NEMF mutations impair RQC (Nat Commun 2020)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7494853/) · [GTPBP1 resolves paused ribosomes](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7665888/) · [RQC and neurological disorders (2025)](https://academic.oup.com/biomedgerontology/article/80/4/glae304/7932361) · [Quality control at stalled ribosomes (Exp Mol Med 2025)](https://www.nature.com/articles/s12276-025-01623-w) · [poly-GR ribotoxic stress response (Sci Signal)](https://www.science.org/doi/10.1126/scisignal.adl1030) · [ZNF598 titrates poly(GR) (NAR 2021)](https://academic.oup.com/nar/article/49/19/11294/6374173)
- [NMNAT2 MAPK turnover (Walker 2017), Addgene/PubMed 28095293](https://addgene.org/browse/pubmed/28095293) · [PAM/MYCBP2 SCF degrades NMNAT2 (PubMed 29997255)](https://www.pubmed.gov/29997255/) · [Nmnat2 localization and stability (PLoS Biol 2013)](https://journals.plos.org/plosbiology/article?id=10.1371%2Fjournal.pbio.1001539)
- [DLK modular injury response (PLoS Genet 2025)](https://journals.plos.org/plosgenetics/article?id=10.1371%2Fjournal.pgen.1011969) · [DLK required for retrograde injury signaling (Neuron 2012)](https://www.cell.com/neuron/fulltext/S0896-6273(12)00425-4)
- [Mitochondrial import stress and α-synuclein](https://pmc.ncbi.nlm.nih.gov/articles/PMC12393598/) · [Proteostasis via mitochondrial protein import (Phil Trans R Soc B 2025)](https://doi.org/10.1098/rstb.2025.0271)
- [GEO GSE174367](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE174367) · [AD snRNA-seq reanalysis context](https://pmc.ncbi.nlm.nih.gov/articles/PMC9093608/)
- [Protein folding and proteostasis review (2025)](https://www.nature.com/articles/s41392-025-02439-w) · [Proteostasis in the ageing neuron](https://www.sciencedirect.com/science/article/pii/S1568163726000656)

**Follow-up needed:** the student (or a follow-up session) should run the three gating prior-art searches listed at the top before committing to Topic 3, 2 or 1. If more searching is wanted, a new message after this reply can continue it, or `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` can be raised.