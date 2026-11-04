# Topic-selection report: regulated cell death / stress / mitochondria / metabolism
### For a Chinese clinical-medicine undergraduate — HT-22 in hand, WB/qPCR/siRNA/transfection/plate-reader, strong R + GEO/TCGA, ¥20–80k, 6–12 months

---

## 0. Verification status and honest caveats (read first)

- Direct access to PubMed/PMC/Crossref/Europe PMC was blocked, as stated. I used **23 WebSearch calls** and then **hit the session WebSearch cap (200 per turn, shared across all agents in the turn)**. Two planned verification queries did not run (osmoprotectant/glycine cytoprotection literature; GEO accession hunting for HT-22 glutamate/ferroptosis datasets). Those gaps are marked inline.
- **No GEO accession appeared in any result**, so every topic below says "accession to be identified" and gives a search strategy instead. I did not invent one.
- Every reference below appeared in an actual search result this session. Where I only saw a title, or where a DOI was only derivable from a result URL slug, I say so. Where I am relying on background knowledge, I write **UNVERIFIED — needs verification** and give **no digit string**.
- Candidate count: **6 topics survive.** Topics 1, 2 and 5 are the ones I would actually defend at a committee. Topic 3 is the lowest-risk / lowest-ceiling option. Topics 4 and 6 are real but carry more execution risk. I have deliberately given you **zero** "compound X protects HT-22 via Nrf2/GPX4" designs.
- One cross-cutting feasibility fact to internalise: **nothing in topics 1–6 requires flow cytometry, Seahorse, MS, lipidomics, confocal, lentivirus or CRISPR.** They all require a **fluorescence-capable plate reader** (filters or monochromator) and preferably a basic fluorescence microscope. If the plate reader is absorbance-only, topics 1, 2, 4 and 6 lose their best readouts — that is the single biggest gating question to answer before committing.

---

# TOPIC 1 — (my top pick)

**1. `title_en`**
Is ferroptotic plasma-membrane rupture NINJ1-executed or osmotic in a NINJ1-low neuronal cell? Dissociating cell-death commitment from LDH release

**2. `core_question`**
In HT-22 cells, does loss (or gain) of NINJ1 change the *timing and size* of the ferroptotic plasma-membrane lesion — measured as SYTOX Green (~600 Da) influx versus LDH (~140 kDa) efflux in the same well — or is the lesion determined instead by osmotic/pore-size constraints that NINJ1 does not control?

**3. `hypothesis`**
Ferroptotic rupture is a *separable terminal step* from ferroptotic commitment. In cell types where NINJ1 is abundant (macrophages, fibroblasts) NINJ1 accelerates and enlarges the lesion; in a NINJ1-low neuronal cell the lesion is instead pore/osmotically limited, so LDH release is delayed relative to small-dye influx and relative to lipid peroxidation. Consequence: **LDH release — the field's default ferroptosis readout — reports rupture competence, not death commitment,** and NINJ1 modulation or osmotic support will produce "protection" by LDH that is absent by orthogonal readouts.

**4. `novelty_claim`**
New: (i) a direct adjudication between two published, mutually incompatible accounts of the *same* step — NINJ1 as "the executor of plasma membrane permeabilization in ferroptotic macrophages and fibroblasts" (Ramos 2024, EMBO J) versus "ferroptosis occurs through an osmotic mechanism and propagates independently of cell rupture" (Riegman 2020, Nat Cell Biol); (ii) the first test of either model in a cell type where NINJ1 is *not* enriched (Human Protein Atlas brain single-nucleus data place NINJ1 as "cell type enhanced (central nervous system macrophage)", not neuronal); (iii) a **size-exclusion osmoprotection series** (graded impermeant osmolytes) to estimate the functional lesion diameter, which neither paper did; (iv) an explicit readout-dissociation matrix.
Traps avoided: this is **not** a cell-line swap, because the prediction is that the dominant model *fails* in this cell type and a *competing published model* takes over — the discriminating measurement is specified in advance. It is not "two molecules in one axis". It is not DEG+enrichment. Both possible outcomes are informative, and the readout-dissociation data stand regardless of which model wins.

**5. `state_of_the_art` (verified)**
Ramos et al. (EMBO J 2024) identify NINJ1 as the executor of PMR in ferroptotic macrophages and fibroblasts, with NINJ1 oligomerising at the membrane, required for DAMP release and for early loss of membrane integrity, but **dispensable for lipid peroxidation, channel-mediated Ca²⁺ influx and cell swelling**. Riegman et al. (Nat Cell Biol 2020) report ferroptotic rupture is pore-mediated and osmotic, with propagation *upstream of* and independent of rupture, and — critically — propagation seen with erastin but **not** with direct GPX4 inhibition. A third, incompatible account (Chen/Wu/Chi, Cell Death Dis 2024) places NINJ1 *upstream*: NINJ1 knockdown protected against ferroptosis induced **only by xCT inhibitors**, not other FIN classes, via physical association with xCT, increased xCT stability and cystine uptake, and raised CoA; protection was abolished by blocking CoA or GSH synthesis. A 2024 bioRxiv preprint reports NINJ1 knockdown abolished erastin-induced rupture in HT-1080 but **not** RSL3-induced ferroptosis, and that NINJ1-mediated PMR is a two-step process requiring cell swelling. Nature 2025 adds that NINJ1 sets plasma-membrane fragility under mechanical strain. A 2026 Frontiers in Immunology review summarises the current compromise — NINJ1 dispensable for commitment, required for efficient PMR and release of large cytosolic proteins such as LDH.

**6. `specific_open_problem`**
Three published mechanisms (downstream executioner / osmotic pore / upstream xCT–CoA regulator) cannot all be right, the inducer-dependence pattern is unexplained, and **no study has tested any of them in a neuronal cell or in a cell type that is not NINJ1-enriched.** Nobody has measured whether the apparent "ferroptosis protection" produced by NINJ1 loss is protection at all, or only suppressed LDH efflux.

**7. `delta_vs_closest_paper`**
Closest paper: **Ramos et al., EMBO J 2024.** Exact differences: (a) they used NINJ1-high macrophages/fibroblasts and a lipid-hydroperoxide inducer (CuOOH); I use HT-22 with an xCT-inhibiting trigger (glutamate), erastin, and RSL3 side by side; (b) they used LDH and PI as concordant rupture readouts — I use them as *discordant* readouts in kinetic mode in the same well, which is the measurement that separates their model from Riegman's; (c) they did not vary extracellular osmotic support or osmolyte size; (d) they did not test sufficiency by overexpression in a NINJ1-low cell. Second-closest: **Chen/Chi, Cell Death Dis 2024** — they concluded upstream xCT/CoA regulation in cancer cells but did not measure rupture kinetics, so the two models were never pitted against each other with a readout that can tell them apart.

**8. `references`**
1. Ramos S, Hartenian E, Santos JC, Walch P, Broz P | NINJ1 induces plasma membrane rupture and release of damage-associated molecular pattern molecules during ferroptosis | EMBO J | 2024;43(7):1164–1186 | DOI 10.1038/s44318-024-00055-y; PMCID PMC10987646 | `SEARCH_SNIPPET` (PMID not captured)
2. Riegman M, et al. | Ferroptosis occurs through an osmotic mechanism and propagates independently of cell rupture | Nat Cell Biol | 2020;22(9):1042–1048 | PMID 32868903; DOI 10.1038/s41556-020-0565-1; PMCID PMC7644276 | `SEARCH_SNIPPET`
3. Chen SY, Wu J, Chi JT, et al. | NINJ1 regulates ferroptosis via xCT antiporter interaction and CoA modulation | Cell Death & Disease | 2024 | DOI 10.1038/s41419-024-07135-1; PMCID PMC11489787 (preprint PMC10925083) | `SEARCH_SNIPPET` (full author list not captured)
4. (authors not captured) | NINJ1 regulates plasma membrane fragility under mechanical strain | Nature | 2025 | DOI 10.1038/s41586-025-09222-5 (from result URL) | `SEARCH_SNIPPET`
5. (authors not captured) | Cell death and cell lysis are separable events during pyroptosis | Cell Death Discovery | 2017 | nature.com/articles/cddiscovery201770 — DOI not captured | `SEARCH_SNIPPET` *(the conceptual precedent: LDH release is a lysis readout routinely misread as a death readout; single-cell imaging separated the two; PI is 668 Da)*
6. (authors not captured) | NINJ1 mediated plasma membrane rupture is a two-step process requiring cell swelling | bioRxiv preprint | 2024 | DOI 10.1101/2024.10.29.620849 | `SEARCH_SNIPPET`
7. (authors not captured) | Membrane Dynamics and Cation Handling in Ferroptosis | Physiology | 2024 | DOI 10.1152/physiol.00029.2023 (from URL) | `SEARCH_SNIPPET` *(reports rapid Na⁺ influx / K⁺ efflux before rupture)*
8. (authors not captured) | Lipid peroxidation increases membrane tension, Piezo1 gating and cation permeability to execute ferroptosis | Current Biology | 2023 (bioRxiv 2022, DOI 10.1101/2022.10.31.514557) | DOI not captured | `SEARCH_SNIPPET`
9. Wang et al. | The structural, functional, and diagnostic significance of NINJ1 in ferroptosis-related diseases | FEBS Journal | 2026 | DOI 10.1111/febs.70258 (from URL) | `SEARCH_SNIPPET`
10. Human Protein Atlas, NINJ1 (ENSG00000131669) single-cell page | brain single-nucleus cluster specificity: "Cell type enhanced (central nervous system macrophage)" | database, accessed this session | `SEARCH_SNIPPET` *(feasibility evidence, not a paper)*
11. (authors not captured) | ATP2B3 Inhibition Alleviates Erastin-Induced Ferroptosis in HT-22 Cells through the P62-KEAP1-NRF2-HO-1 Pathway | 2023 | PMCID PMC10252295 | `SEARCH_SNIPPET` *(cited only as evidence that erastin works in HT-22 — the paper itself is an example of the saturated genre you are avoiding)*

**9. `models_and_data`**
- HT-22 (in hand). Triggers: L-glutamate 2–10 mM (system xc⁻ inhibition — HT-22 lack ionotropic glutamate receptors, so death runs through xc⁻ → GSH depletion → lipid peroxidation), erastin, RSL3. The glutamate-vs-RSL3 contrast *is* the inducer-class contrast both NINJ1 papers disagree about.
- **Strongly recommended second line: HT-1080** ("needs to be obtained"; it is the field-standard ferroptosis line and the line used in the NINJ1 preprint, so it gives you a positive control for NINJ1-dependence). A NINJ1-high line (RAW 264.7 or NIH/3T3, "needs to be obtained") would make the paper substantially stronger as the comparator.
- Bioinformatics: NINJ1 expression across neural cell types — Human Protein Atlas (verified reachable), Allen Brain Cell Atlas, and mouse hippocampus snRNA-seq in GEO. **GEO accession to be identified** (search GEO for: hippocampus snRNA-seq mouse; HT22 glutamate RNA-seq; ferroptosis erastin RSL3 time-course RNA-seq). Deliverable: NINJ1 vs *Slc7a11*/*Gpx4*/*Acsl4* co-expression by cell type, to support the premise that neurons are NINJ1-low.

**10. `key_experiments`**
*Gate (weeks 1–3, go/no-go):* NINJ1 mRNA (qPCR) and protein (WB) in HT-22 vs a NINJ1-high comparator lysate. **If HT-22 NINJ1 is undetectable by WB, the knockdown arm is dead and the project pivots to the overexpression-sufficiency + osmotic arms — which is still a complete paper.** Decide here, not at month 6.
1. **The centrepiece — paired kinetic readout dissociation.** Same plate, kinetic mode: SYTOX Green influx (~600 Da; *plate reader only*, no flow) + LDH in supernatant at matched timepoints (*plate reader, absorbance*) + CCK-8 in parallel wells + ATP (colorimetric kit, *plate reader*; luminescent kit if available). Readout: time-to-50% for each. Prediction that discriminates the models: NINJ1 loss / osmotic support delays **LDH** without delaying **SYTOX** → rupture is a separable late, size-limited step.
2. **Upstream commitment is unchanged?** C11-BODIPY 581/591 ratiometric (*needs a plate reader with both FITC-like and TRITC-like filter sets, OR a fluorescence microscope with GFP+TRITC channels; flow cytometry preferred but NOT required*) and/or Liperfluo (single channel, plate reader fine); MDA/TBARS kit; GSH/GSSG kit (all *plate reader*). If peroxidation is unchanged while LDH is suppressed, the effect is at rupture.
3. **Loss of function:** NINJ1 siRNA (3 independent sequences, titrated to graded knockdown; in hand), knockdown verified by WB.
4. **Gain of function / sufficiency:** NINJ1 overexpression plasmid (transfection in hand) in HT-22 → does it accelerate LDH release without changing peroxidation? This is the arm that survives even if endogenous NINJ1 is near-zero.
5. **Size-exclusion osmoprotection.** Graded membrane-impermeant osmolytes (glycine ~75 Da; sucrose/raffinose; PEG 1000 / 4000 / 8000) at iso-osmotic matched concentrations, with a mannitol osmotic control. Estimates functional lesion diameter and tests Riegman's osmotic model directly. **Caveat: the osmoprotection/glycine-cytoprotection literature is UNVERIFIED in this session (search budget exhausted) — needs verification before you design doses, and run it as a piloted arm with its own osmolarity and vehicle controls.**
6. **xCT arm (tests the Chi model):** WB for SLC7A11/xCT ± NINJ1 siRNA; GSH kit as a cystine-uptake surrogate; qPCR for CoA-pathway genes (*Pank1/2*, *Ppcs*, *Ppcdc*); rescue with pantothenate. If NINJ1 knockdown raises xCT and GSH in HT-22 too, the upstream model generalises and you must report that.
7. **Bioinformatics arm:** cell-type NINJ1 expression (above) + a short, pre-registered audit of which readout(s) recent HT-22 ferroptosis papers used (LDH-only vs CCK-8-only vs orthogonal). Pure R work, uses the student's strength, and directly motivates the paper.
*Gating/equipment:* fluorescence plate reader **required**; fluorescence microscope strongly recommended; flow cytometry **not** required; no lentivirus, no CRISPR, no co-IP (do **not** try to replicate the NINJ1–xCT physical interaction — that needs co-IP you don't have; cite it, don't chase it).

**11. `expected_and_negative_results`**
Most likely: HT-22 express low NINJ1; knockdown has little effect; osmotic support and osmolyte size strongly modulate LDH without modulating SYTOX or peroxidation; NINJ1 overexpression confers rupture acceleration. That is a **positive result for the osmotic/pore model plus a limiting condition on the NINJ1 model** — publishable. If instead NINJ1 knockdown protects by *all* readouts including peroxidation and GSH, you have independently replicated the Chi upstream model in a neuronal cell — also publishable. **The negative result is publishable either way, because the readout-dissociation matrix is the deliverable, not the NINJ1 answer.** That is the main reason I rank this first.

**12. `difficulty_and_cost`**
Difficulty **3/5**. ≈**¥35–55k**: NINJ1 antibody (¥2–3k, validate carefully — this is the single highest-risk reagent), SLC7A11/GPX4/ACSL4/β-actin antibodies (¥6–10k), NINJ1 siRNA ×3 + controls (¥3–5k), NINJ1 expression plasmid (¥2–4k), RSL3 + erastin + Fer-1 (¥5–9k), C11-BODIPY (¥3–5k), SYTOX Green/PI (¥1k), LDH + GSH/GSSG + MDA + ATP kits (¥5–9k), transfection reagent + consumables + media/FBS (¥8–12k). Osmolytes are trivially cheap. **Must buy:** NINJ1 antibody, probes. **Should obtain:** HT-1080 and one NINJ1-high line. **Nothing needs outsourcing.**

**13. `timeline_months`** 9–11. M1: NINJ1 expression gate + plate-reader kinetic assay setup. M2–3: dose/time curves for glutamate/erastin/RSL3; readout dissociation baseline. M4–5: siRNA + overexpression. M6: osmoprotection series. M7: xCT/CoA arm + second cell line. M8: bioinformatics + readout audit. M9–11: figures, writing, revision.

**14. `target_journal_tier`** Solid specialty Q1–Q2, not a top-tier journal. Realistic: *Free Radical Biology and Medicine*; *Cell Death Discovery*; *Biochemical Pharmacology* or *Archives of Biochemistry and Biophysics*. *Redox Biology* only if the osmolyte-sizing data are clean and a second cell line is included. No acceptance promises.

**15. `reviewer_attacks`**
1. "One immortalised line; siRNA is partial; you cannot claim NINJ1 is dispensable without a knockout." → Counter with graded knockdown dose–response + overexpression sufficiency + a NINJ1-high comparator line, and phrase the claim as "not rate-limiting in this context", never "dispensable".
2. "Osmoprotectants are not clean — glycine has receptor/channel activity and PEG can seal membranes." → Multiple osmolyte chemistries, size series, iso-osmotic controls, and a frank limitations paragraph.
3. "Your readout dissociation may just be assay sensitivity, not biology." → Spike-in recovery for LDH, cell-number standard curves for every readout, and matched detection limits reported explicitly.

**16. `prelim_ratings`** novelty **H** · evidence-base **H** · overlap-risk **M** (the Broz and Chi labs are both active here; publish within 12 months or be scooped on the cancer-cell side — but the neuronal/NINJ1-low angle is unoccupied)

---

# TOPIC 2

**1. `title_en`**
Does the labile iron pool actually rise during neuronal ferroptosis? Decoupling iron-chelator protection from labile-iron dynamics, with a probe-leakage-controlled measurement

**2. `core_question`**
In HT-22 cells undergoing glutamate-, erastin- or RSL3-induced ferroptosis, does whole-cell labile Fe²⁺ increase before the point of commitment when measured by two orthogonal methods (live turn-on probe and leakage-immune lysate colorimetry), and does the protection afforded by iron chelation track that increase?

**3. `hypothesis`**
Labile iron does **not** rise appreciably before commitment in neuronal cells; apparent rises reported with live probes are confounded by permeability-dependent probe loss and by esterase-dependent loading; and chelator protection reflects iron's role as a **permissive catalytic cofactor** for peroxide decomposition rather than an expanding pool that acts as the trigger. Prediction: chelators protect across a window in which no LIP increase is measurable, and a *forced* LIP increase (ferric ammonium citrate) is not sufficient to kill without a peroxidation stimulus.

**4. `novelty_claim`**
New: the first independent test, in a non-cancer neuronal lineage, of the 2026 claim that "no significant increase in endogenous LIP occurs during ferroptosis"; and the first explicit quantification of **probe leakage as a source of error** in FerroOrange-type measurements during ferroptosis (the JBC paper itself flags that "changes in membrane permeability may cause probe leakage resulting in a misleading signal decline" but does not quantify it). Traps avoided: this is not a model transplant — it is an adjudication between a 2026 primary result and the entrenched neuro/oxytosis "iron accumulation" narrative, with a pre-specified orthogonal measurement and an explicit sufficiency test. No Nrf2. No natural product.

**5. `state_of_the_art` (verified)**
Ponnusamy et al. (J Biol Chem 2026) report that induction of ferroptosis did not cause any increase in the LIP in any colorectal cancer line tested; they measured at 4 h with FerroOrange because their TRX-PURO probe could not assess timepoints before 8 h, validated specificity with 50 µM deferoxamine, and flagged probe leakage during progression as a confound. A 2025 bioRxiv preprint reports the opposite direction in another context (polyamine depletion raises labile iron pools, FerroOrange used in cell-free assays). Organelle-targeted labile-Fe(II) probe cocktails exist for ferroptosis but require imaging. In the neuronal field, the oxytosis/ferroptosis literature (Maher group and others) treats iron-dependent lipid peroxidation downstream of xc⁻ blockade as settled, and HT-22 glutamate toxicity is routinely labelled an "in vitro ferroptosis model".

**6. `specific_open_problem`**
A central, textbook step — "intracellular labile iron rises and drives ferroptosis" — has now been directly contradicted in one lineage using the same probes the rest of the field relies on, and has **never been measured with a leakage-immune method in neurons**. It is also unknown whether chelator protection is quantitatively attributable to LIP at all.

**7. `delta_vs_closest_paper`**
Closest paper: **Ponnusamy et al., J Biol Chem 2026 (PMID 41819262).** Differences: (a) colorectal cancer lines vs neuronal HT-22, and an xc⁻-inhibiting trigger (glutamate) they did not use; (b) they used live probes at a single early timepoint; I add a **lysate-based ferrozine/colorimetric Fe²⁺ assay** at matched timepoints, which is immune to the leakage artefact they identify; (c) I add a **chelator-timing decoupling** experiment (add DFO at staggered times after trigger, map the window of rescuable commitment against the LIP time course) and a **sufficiency** arm (FAC ± a peroxidation stimulus), neither of which they report; (d) I add spike-recovery controls to quantify the leakage error they only flag qualitatively.

**8. `references`**
1. Ponnusamy V, Randall DR, Lee ZH, Das NK, Zhao L, Buscher K, Solanki S, Renslo AR, Hsu PP, Shah YM | Labile iron pool dynamics do not drive ferroptosis in colorectal cancer cells | J Biol Chem | 2026;302(5):111357 | PMID 41819262; DOI 10.1016/j.jbc.2026.111357; PMCID PMC13089158 | `SEARCH_SNIPPET`
2. same group | Labile iron pool dynamics do not drive ferroptosis potentiation in colorectal cancer cells | bioRxiv | 2025 | PMID 40631145; DOI 10.1101/2025.07.01.662602; PMCID PMC12236665 | `SEARCH_SNIPPET`
3. (authors not captured) | Polyamines buffer labile iron to suppress ferroptosis | bioRxiv | 2025 | DOI 10.1101/2025.06.30.662349 (from URL) | `SEARCH_SNIPPET`
4. Maher P and colleagues (full author list not captured) | Using the Oxytosis/Ferroptosis Pathway to Understand and Treat Age-Associated Neurodegenerative Diseases | Cell Chemical Biology | 2020 | DOI not captured | `SEARCH_SNIPPET`
5. (authors not captured) | The role of Ca²⁺ in cell death caused by oxidative glutamate toxicity and ferroptosis | (journal not captured) | PMCID PMC5682235 | `SEARCH_SNIPPET`
6. Hirayama and colleagues (author list not captured) | Organelle-specific analysis of labile Fe(II) during ferroptosis by using a cocktail of various colour organelle-targeted fluorescent probes | (journal/year not captured) | no PMID/DOI captured | `TITLE_ONLY`
7. (authors not captured) | The cell biology of ferroptosis | Nat Rev Mol Cell Biol | 2024 | DOI 10.1038/s41580-024-00703-5 (from URL) | `SEARCH_SNIPPET`
8. (authors not captured) | Crosstalk between Oxidative Stress and Ferroptosis/Oxytosis in Ischemic Stroke: Possible Targets and Molecular Mechanisms | 2021 | PMCID PMC8133868 | `SEARCH_SNIPPET`

**9. `models_and_data`** HT-22 (in hand). Triggers: glutamate, erastin, RSL3. Calibrators: FAC, ferrous ammonium sulfate, DFO, 2,2′-bipyridyl, ciclopirox olamine (second-chemotype chelator; "needs to be obtained", inexpensive). Bioinformatics arm is thin here — limit it to an honest expression check of iron-handling genes (*Fth1*, *Ftl1*, *Tfrc*, *Slc40a1*, *Ncoa4*, *Steap3*) by qPCR/WB plus a public neuronal ferroptosis dataset if one can be found. **GEO accession to be identified.**

**10. `key_experiments`**
1. **Orthogonal LIP time course.** FerroOrange live signal (*plate reader or fluorescence microscope; NO flow cytometry needed*) and, at the same timepoints from parallel wells, a **lysate ferrozine/colorimetric Fe²⁺ kit** (*plate reader, absorbance*), normalised to protein. Timepoints must straddle the commitment point, which you first define in experiment 3.
2. **Quantify the leakage artefact.** Load FerroOrange, then permeabilise a dose series (digitonin or saponin), measure signal loss versus LDH release — this gives an explicit calibration of how much apparent "signal decline" is leakage. Then spike known Fe²⁺ into lysates for recovery. This is the methodological core and is cheap.
3. **Commitment-window mapping (the decoupling experiment).** Add Fer-1 or DFO at 0, 2, 4, 6, 8, 10 h after trigger; score viability at a fixed endpoint. Compare the time-to-no-rescue against the LIP time course. If chelators still rescue in a window where LIP is flat, iron is not acting as an expanding pool.
4. **Sufficiency.** FAC dose series alone, versus FAC + a sub-lethal peroxidation stimulus, versus FAC + RSL3. Readouts: Liperfluo or C11-BODIPY (*plate reader with appropriate filters, or microscope*), MDA kit, SYTOX/PI, CCK-8 and LDH together.
5. **Chelator chemotype control.** DFO vs 2,2′-bipyridyl vs ciclopirox — if protection is chelation it should be chemotype-independent at equi-chelating doses; if DFO alone protects, suspect off-target radical scavenging.
6. WB for FTH1/TFRC/NCOA4 and qPCR to show the iron-regulatory response, so a flat LIP is not simply "nothing happened".
*Gating:* fluorescence plate reader **required** for FerroOrange and Liperfluo. Microscope strongly recommended to confirm probe localisation. Flow cytometry **not** needed.

**11. `expected_and_negative_results`** Most likely: flat or modestly changing whole-cell LIP, substantial quantified leakage artefact, chelator rescue extending beyond any LIP change, FAC insufficient alone. That reproduces the 2026 JBC conclusion in an independent lineage and adds the method — publishable. If LIP *does* rise robustly in HT-22, you have found a **cell-lineage limiting condition** on a 2026 Nature-family-adjacent claim, which is arguably the more interesting outcome. Both directions publishable. **Hard limitation you must concede in the paper:** whole-cell lysate Fe²⁺ cannot exclude a *local/organellar* rise. Do not overclaim; say "whole-cell labile iron".

**12. `difficulty_and_cost`** Difficulty **2–3/5**. ≈**¥25–40k**: FerroOrange (¥2–3k), Liperfluo and/or C11-BODIPY (¥3–6k), colorimetric Fe²⁺ kit ×2 brands (¥2–4k), chelators and FAC (¥1–2k), RSL3/erastin/Fer-1 (¥5–9k), MDA/GSH/LDH kits (¥4–7k), antibodies FTH1/TFRC/NCOA4 (¥5–8k), consumables (¥6–10k). Nothing outsourced. Cheapest of the mechanistic topics.

**13. `timeline_months`** 7–9.

**14. `target_journal_tier`** Q2 solid, Q1 specialty possible. Realistic: *Free Radical Biology and Medicine*; *Archives of Biochemistry and Biophysics*; *Neurochemistry International* or *Journal of Neurochemistry*. No promises.

**15. `reviewer_attacks`**
1. "Absence of a whole-cell LIP rise does not exclude a compartmentalised rise." → Concede explicitly in the title and abstract; cite the organelle-targeted-probe literature as the needed follow-up.
2. "FerroOrange is esterase- and viability-dependent — your flat signal may be probe failure." → That is exactly what experiment 2 is for; show spike-recovery and the permeabilisation calibration.
3. "This is a replication of a 2026 paper in a different cell line." → Lead with the method (leakage quantification) and the decoupling/sufficiency experiments, which are not in that paper. Be honest that independent replication is part of the value.

**16. `prelim_ratings`** novelty **M–H** · evidence-base **H** · overlap-risk **M** (the Shah/Renslo group will likely extend this themselves; the neuronal and methodological niche is open)

---

# TOPIC 3 — (safest, lowest ceiling)

**1. `title_en`**
Tetrazolium- and resazurin-based viability assays systematically misreport ferroptosis pharmacology: a quantified interference panel and a readout audit

**2. `core_question`**
Do the radical-trapping antioxidants, chelators and thiols used as standard ferroptosis controls (ferrostatin-1, liproxstatin-1, Trolox/α-tocopherol, NAC, deferoxamine, baicalein, zileuton, and a set of flavonoids claimed to be anti-ferroptotic) produce measurable WST-8/MTT/resazurin signal **in the complete absence of cells** at their exact published working concentrations, and does that inflate apparent cytoprotection relative to orthogonal, non-redox readouts?

**3. `hypothesis`**
A substantial fraction of commonly used ferroptosis "rescue" compounds directly reduce tetrazolium/resazurin dyes or interfere with the electron mediator at working concentrations, and ferroptosis itself alters cellular NAD(P)H and dehydrogenase capacity; together these shift apparent EC50/IC50 values and in some cases manufacture protection that does not exist by PI/SYTOX, LDH or direct nuclei counting.

**4. `novelty_claim`**
New: a **quantified, compound-by-compound, concentration-matched interference panel** for the modern ferroptosis toolkit, plus a "false-protection index" that converts chemical interference into the error it causes in a realistic HT-22 protection experiment, plus a **systematic audit of which readouts the recent HT-22/neuronal ferroptosis literature actually used**. Trap avoided: this is an assay/reagent-artefact exposure with a cleaner method — explicitly one of the real-novelty categories — not a mechanism claim. There is precedent for this genre succeeding in this exact field: Shah/Shchepinov/Pratt (ACS Cent Sci 2018) showed LOX inhibitors act as off-target radical-trapping antioxidants, which reframed the role of lipoxygenases in ferroptosis.

**5. `state_of_the_art` (verified, with an important honesty caveat)**
The chemistry is acknowledged but, in this session's searches, **only in vendor documentation, not in a dedicated peer-reviewed study of ferroptosis reagents**. Sigma-Aldrich's CCK-8 datasheet states "WST-8 may react with reducing agents to generate WST-8 formazan". Lumiprobe's protocol states reducing agents and antioxidants present in the sample confound results and must be removed. A technical guide recommends compound+reagent-without-cells wells and flags ascorbate, DTT and thiol-rich media as causes of non-enzymatic reduction, and notes polyphenols and flavonoids reduce these dyes with no cells present. Meanwhile ferrostatin-1 is characterised as a highly effective radical-trapping antioxidant, and the published genre routinely uses CCK-8 as the primary readout with Fer-1 as the rescue control. **My searches found no study that directly tested whether ferrostatin-1 or liproxstatin-1 reduce WST-8/MTT in cell-free controls** — that is the gap.

**6. `specific_open_problem`**
An artefact that vendors warn about has never, to my verified knowledge, been systematically quantified for the ferroptosis toolkit, in a field where CCK-8-only viability data support thousands of mechanistic claims.

**7. `delta_vs_closest_paper`**
Closest paper: **Shah R, Shchepinov MS, Pratt DA, "Resolving the Role of Lipoxygenases in the Initiation and Execution of Ferroptosis", ACS Cent Sci 2018;4(3):387–396.** That work exposed an off-target *pharmacological* artefact (LOX inhibitors acting as RTAs in cells). My proposal exposes an off-target *analytical* artefact (the same class of compounds acting on the detection chemistry), which is a different failure mode, at a different step, and affects a far broader set of papers. Second-closest precedent for publishability of this genre: the 2021 *Scientific Reports* work showing limited specificity of pan-acylation antibodies.

**8. `references`**
1. Shah R, Shchepinov MS, Pratt DA | Resolving the Role of Lipoxygenases in the Initiation and Execution of Ferroptosis | ACS Central Science | 2018;4(3):387–396 | DOI 10.1021/acscentsci.7b00589 (from result URL) | `SEARCH_SNIPPET`
2. (authors not captured) | On the Mechanism of Cytoprotection by Ferrostatin-1 and Liproxstatin-1 and the Role of Lipid Peroxidation in Ferroptotic Cell Death | ACS Central Science | 2017 | DOI 10.1021/acscentsci.7b00028 (from result URL) | `SEARCH_SNIPPET`
3. Conrad M (and colleague; list not captured) | Lipoxygenases — Killers against Their Will? | ACS Central Science | 2018;4(3):312 | PMID 29632874; PMCID PMC5879469 | `SEARCH_SNIPPET`
4. (authors not captured) | The chemical basis of ferroptosis | Nature Chemical Biology | 2019 | DOI 10.1038/s41589-019-0408-1 (from URL) | `SEARCH_SNIPPET`
5. (authors not captured) | Programmed cell death detection methods: a systematic review and a categorical comparison | Apoptosis | 2022 | DOI 10.1007/s10495-022-01735-y (from URL) | `SEARCH_SNIPPET` *(notes LDH release occurs at a late stage in ferroptosis/oxidative death once the membrane is disrupted)*
6. (authors not captured) | Epigenetics Identifier screens reveal regulators of chromatin acylation and limited specificity of acylation antibodies | Scientific Reports | 2021 | PMCID PMC8211816 | `SEARCH_SNIPPET` *(genre precedent: reagent-specificity papers do publish)*
7. (authors not captured) | Lipid-derived radical-trapping antioxidants suppress ferroptosis | (journal/year not captured) | PMCID PMC10960586 | `SEARCH_SNIPPET`
8. Sigma-Aldrich | Cell Counting Kit-8 product datasheet (96992) | manufacturer document, accessed this session | "WST-8 may react with reducing agents to generate WST-8 formazan" | `SEARCH_SNIPPET` *(vendor document, not a paper — cite as such)*
9. Lumiprobe | CCK-8 cell viability assay protocol | manufacturer document, accessed this session | `SEARCH_SNIPPET` *(vendor document)*

**9. `models_and_data`** HT-22 (in hand) with glutamate, erastin, RSL3. Cell-free interference plates. Second line (e.g. HT-1080) desirable but optional. Audit arm: a structured, pre-registered literature-coding exercise in R — this is the only "bioinformatics" component and it is meta-research, not omics. No GEO data needed.

**10. `key_experiments`**
1. **Cell-free interference matrix** (*plate reader, absorbance only*): WST-8/CCK-8, MTT, and resazurin, each × full concentration series of Fer-1, Lip-1, Trolox, α-tocopherol, NAC, GSH, DFO, 2,2′-bipyridyl, baicalein, zileuton, plus 4–6 flavonoids/natural products the literature calls anti-ferroptotic (quercetin, baicalin, luteolin, etc.). Complete medium ± FBS ± phenol red, 37 °C, matched incubation times. Output: ΔOD attributable to chemistry alone.
2. **Protection-inflation experiment.** Run a textbook HT-22 glutamate protection curve for each compound with **five readouts in parallel**: CCK-8, MTT, resazurin, LDH release, and SYTOX Green/PI influx (*plate reader*), plus Calcein-AM/PI or Hoechst nuclei counting (*microscope*). Compute an EC50 shift and a "false-protection index" per compound.
3. **Metabolic-state confound, independent of chemistry.** Show that ferroptotic and sub-lethal stress conditions change CCK-8 signal per surviving cell: normalise CCK-8 to counted nuclei or to total protein (BCA) across the time course. Add NADH/NAD⁺ and NADPH kit measurements (*plate reader*) to tie the shift to reductive capacity.
4. **The cleaner method.** Propose and validate a minimal orthogonal panel (real-time SYTOX kinetics + LDH + nuclei count) with limits of detection, dynamic range, and a spike-recovery control, and show it recovers the "true" pharmacology for the worst-offending compounds.
5. **Readout audit** (R): code a defined sample of recent HT-22 / neuronal ferroptosis papers for readout type and presence/absence of a cell-free control. Report the frequency. Pre-specify inclusion criteria and publish the coding sheet.
*Gating:* absorbance plate reader is enough for most of it; **fluorescence plate reader required** for SYTOX/Calcein; microscope for nuclei counting. No flow cytometry, no specialist equipment.

**11. `expected_and_negative_results`** Likely: strong interference from thiols (NAC, GSH) and flavonoids; weaker but non-zero from Fer-1/Lip-1; a quantifiable metabolic-state confound that is probably larger than the chemical one. If **no** compound interferes meaningfully, the paper becomes a validation study — "CCK-8 is fit for purpose in ferroptosis within these bounds" — which is thinner but still publishable, and the metabolic-state and audit arms survive either way. Lowest scientific risk of all six; also the lowest ceiling.

**12. `difficulty_and_cost`** Difficulty **1–2/5**. ≈**¥15–30k**: CCK-8/MTT/resazurin (¥2–4k), the compound panel (¥6–12k, dominated by RSL3 and Lip-1), SYTOX/Calcein/PI (¥1–2k), LDH + NAD(P)H kits (¥3–5k), consumables (¥5–8k). Nothing outsourced. **This is the one that fits ¥20k.**

**13. `timeline_months`** 5–7 — the only option with real slack for an undergraduate's first paper.

**14. `target_journal_tier`** Methods/analytical Q2–Q3, or a redox specialty journal. Realistic: *Analytical Biochemistry*; *Journal of Pharmacological and Toxicological Methods* or *SLAS Discovery*; *Free Radical Biology and Medicine* (as a "methodological considerations" piece) or *Cell Biology and Toxicology*. No promises.

**15. `reviewer_attacks`**
1. "Known for thirty years; vendors already warn about it." → The honest answer: the chemistry is known, the **magnitude in this specific toolkit and the downstream error in real conclusions are not**, and the audit shows the warning is widely ignored. Say this in the cover letter, do not pretend to discover the phenomenon.
2. "Straw man — good labs already use orthogonal readouts." → The audit is the rebuttal; pre-register it so it cannot be dismissed as cherry-picking.
3. "Cell-free interference at concentrations nobody uses." → Match published working concentrations exactly and cite the source for each.

**16. `prelim_ratings`** novelty **M** · evidence-base **M** (the key gap is supported mainly by vendor documents; I could not verify a peer-reviewed precedent for the specific test) · overlap-risk **L**

---

# TOPIC 4

**1. `title_en`**
Is NAD⁺ depletion necessary or sufficient for parthanatos? A necessity/sufficiency dissection in a neuronal cell line

**2. `core_question`**
In HT-22 cells, does restoring NAD⁺ (NMN/NR/exogenous NAD⁺) to pre-stress levels prevent PARP1-dependent death, and does an equivalent, kinetically matched NAD⁺ depletion produced without PARP1 hyperactivation (NAMPT inhibition) kill the same cells?

**3. `hypothesis`**
NAD⁺ depletion is **neither sufficient nor rate-limiting** for parthanatos in neuronal cells; the proximate determinant is PAR-dependent ATP collapse (and AIF relocalisation), so NAD⁺ restoration that does not prevent PAR accumulation will fail to rescue, and matched NAD⁺ depletion without PAR will not kill.

**4. `novelty_claim`**
New: a dedicated **2×2 necessity/sufficiency design with the assumed intermediate actually measured at every arm**, in a neuronal context, including the PARG-inhibitor arm that a 2026 preprint says uncouples NAD⁺ depletion from ATP depletion. Trap avoided: this does not jam two molecules into an axis or chase a new name — it directly measures a step ("PARP1 kills by consuming NAD⁺") that almost every parthanatos paper asserts and almost none measures alongside a matched-depletion control.

**5. `state_of_the_art` (verified)**
Reviews state that PARP1 activation is insufficient to account for parthanatos, that profound NAD⁺ depletion in the absence of PARP1 hyperactivation was insufficient to induce parthanatos, and that there are no reports yet confirming that PARP1-dependent parthanatos entirely depends on mitochondrial NAD⁺ depletion — while simultaneously noting that adding NAD⁺ or overexpressing NAD⁺-generating enzymes avoids PARP1-dependent death. A 2026 bioRxiv preprint reports that PARG inhibition uncoupled NAD⁺ depletion from ATP depletion, that PAR hydrolysis is required for ATP depletion, and that parthanatos does not necessarily correlate with NAD⁺ depletion. In axons, NAD⁺ falling to ~11% of control produced no cell death or degeneration, and FK866 delays rather than causes degeneration — while FK866 does kill some non-neuronal cells (CLL) by NAD⁺ then ATP loss, and a 2025 PNAS paper describes a SARM1-independent program coupling NAD⁺ depletion to BAX activation and APAF1 degradation. Separately, the MIF-nuclease ("PAAN") executioner step is contested: a 2023 J Med Chem paper states that in their hands the nuclease activity could not be unambiguously assigned to MIF, raising bacterial contamination.

**6. `specific_open_problem`**
The canonical causal chain PARP1 → NAD⁺ depletion → death has been asserted for two decades, questioned in reviews, challenged in a 2026 preprint, and never resolved with a matched-depletion sufficiency control plus direct NAD⁺ measurement in the same cells — least of all in neurons.

**7. `delta_vs_closest_paper`**
Closest work: the **2026 bioRxiv PARG preprint** ("PARG activity is required for cell death by parthanatos"). Differences: (a) it is a preprint in (as far as I could verify) non-neuronal cells; (b) it approaches the question through PAR turnover, whereas I approach it through a **dose- and rate-matched NAD⁺-depletion sufficiency arm** (FK866 ± nicotinamide, titrated to reproduce the parthanatos NAD⁺ trajectory), which it does not report; (c) I pair this with measured restoration (NMN/NR) rather than assumed restoration. The result is an independent test of the same conclusion by a different route, plus the neuronal context.

**8. `references`**
1. (authors not captured) | Molecular Mechanisms of Parthanatos and Its Role in Diverse Diseases | Int J Mol Sci | 2022;23(13):7292 | PMCID PMC9266317; DOI 10.3390/ijms23137292 (from publisher URL) | `SEARCH_SNIPPET`
2. (authors not captured) | PARG activity is required for cell death by parthanatos | bioRxiv preprint | 2026 | biorxiv.org/content/10.64898/2026.05.12.724507v1 | `SEARCH_SNIPPET` *(preprint, not peer-reviewed)*
3. (authors not captured) | SARM1 is an essential component of neuronal Parthanatos | (journal not captured; ~2025) | PMCID PMC12132571 | `SEARCH_SNIPPET`
4. (authors not captured) | A metabolic cell death program downstream of SARM1 couples NAD⁺ depletion to BAX activation and APAF1 degradation | PNAS | 2025 | DOI 10.1073/pnas.2522444122 (from URL) | `SEARCH_SNIPPET`
5. (authors not captured) | NMNAT1 inhibits axon degeneration via blockade of SARM1-mediated NAD⁺ depletion | eLife | 2016; article 19749 | DOI not captured | `SEARCH_SNIPPET`
6. (authors not captured) | A rise in NAD precursor nicotinamide mononucleotide (NMN) after injury promotes axon degeneration | Cell Death & Differentiation | 2014 | nature.com/articles/cdd2014164 — DOI not captured | `SEARCH_SNIPPET`
7. Park H, et al. | PAAN/MIF nuclease inhibition prevents neurodegeneration in Parkinson's disease | Cell | 2022 | PMCID PMC9149120; DOI 10.1016/j.cell.2022.04.020 (derived from result URL) | `SEARCH_SNIPPET`
8. (authors not captured) | Allosteric Inhibitors of Macrophage Migration Inhibitory Factor … | J Med Chem | 2023 | DOI 10.1021/acs.jmedchem.3c00397 (from URL) | `SEARCH_SNIPPET` *(the failed-replication statement about MIF nuclease activity)*
9. (authors not captured) | Targeting PAAN/MIF nuclease activity in parthanatos-associated brain diseases | (journal not captured) | PMID 39929577 | `SEARCH_SNIPPET`
10. (authors not captured) | On-target effect of FK866, a nicotinamide phosphoribosyl transferase inhibitor, by apoptosis-mediated death in chronic lymphocytic leukemia cells | 2014 | PMID 25172933 | `SEARCH_SNIPPET`

**9. `models_and_data`** HT-22 (in hand). Parthanatos triggers: MNNG, or H₂O₂, or high-dose glutamate — **you must first establish which gives PARP1-dependent, PAR-positive, caspase-independent death in HT-22; do not assume it.** Tools: PJ34 or olaparib (PARP inhibition), PARG inhibitor PDD00017273 ("needs to be obtained"), FK866, nicotinamide, NMN/NR, Z-VAD-FMK, siRNA against *Parp1* and *Aifm1*. Bioinformatics arm is minor; keep it to NAD-pathway gene expression. **GEO accession to be identified.**

**10. `key_experiments`**
1. **Establish the model (gate, M1–2):** dose/time for the chosen trigger; PAR accumulation by WB (anti-PAR antibody — budget for it, and validate); PARP1 siRNA and PJ34 dependence; caspase-3/7 activity kit (*plate reader*) to show caspase-independence; AIF in nuclear vs cytosolic fractions by WB. **If HT-22 do not give clean PAR-dependent death, stop and switch topic.**
2. **Necessity:** NMN / NR / exogenous NAD⁺ dose series → measure NAD⁺ and NADH with a colorimetric/fluorometric kit (*plate reader*) to confirm restoration, measure ATP (*plate reader*), then score death (SYTOX/PI + LDH + CCK-8). Report rescue as a function of **measured** NAD⁺ restoration, not of dose.
3. **Sufficiency (the key arm):** titrate FK866 ± nicotinamide to reproduce, as closely as possible, the magnitude *and rate* of the NAD⁺ fall seen in parthanatos. Then ask whether cells die. Overlay time courses explicitly.
4. **Uncoupling:** PARG inhibitor ± trigger; measure PAR (WB), NAD⁺, ATP, death. Tests the 2026 preprint's claim in a neuronal cell.
5. **Executioner arm (optional, cheap):** *Mif* siRNA ± trigger, with the explicit caveat that MIF nuclease activity is contested. **Do not attempt recombinant nuclease assays** — that is what the J Med Chem group disputed and it needs protein biochemistry you do not have.
*Gating:* fluorescence plate reader for SYTOX and caspase/ATP fluorometric kits (colorimetric ATP alternatives exist); anti-PAR antibody is the critical reagent; **no flow cytometry, no Seahorse**. Honest limitation: colorimetric kits report **total** NAD⁺ pools, not free or compartmental NAD⁺ — the sensor literature is explicit that these are not interchangeable, and you cannot fix this without a genetically encoded sensor (which needs imaging you may not have).

**11. `expected_and_negative_results`** Likely: matched FK866 depletion does not kill; NMN restores measured NAD⁺ but rescues only partially; PARG inhibition separates NAD⁺ from ATP. That is a clean negative on the canonical chain and is publishable. If NMN fully rescues and FK866 kills, you have *supported* the dogma with the first direct measurement — true but harder to place, and the paper gets thinner. Asymmetric risk; this is why it ranks fourth.

**12. `difficulty_and_cost`** Difficulty **3/5**. ≈**¥35–55k**: anti-PAR antibody (¥3–5k), PARP1/AIF/MIF antibodies (¥6–9k), FK866 (¥1–2k), PARG inhibitor (¥2–4k), NMN/NR/NAD⁺ (¥2–3k), MNNG/H₂O₂ (cheap), siRNAs (¥4–6k), NAD⁺/NADH + ATP + caspase-3/7 + LDH kits (¥6–10k), consumables (¥8–12k).

**13. `timeline_months`** 9–11, with a hard gate at month 2.

**14. `target_journal_tier`** Q2 specialty. Realistic: *Biochemical and Biophysical Research Communications*; *Apoptosis* or *Molecular and Cellular Biochemistry*; *Neurochemistry International*. No promises.

**15. `reviewer_attacks`**
1. "FK866-matched depletion is not equivalent — rate, compartment and subcellular site differ." → Strongest attack; overlay rates, concede compartmentation, and limit the claim to "total cellular NAD⁺ depletion of this magnitude and rate is not sufficient".
2. "Total-pool colorimetric kits cannot address free/mitochondrial NAD⁺." → Concede; cite the sensor literature; frame as the needed follow-up.
3. "Is this parthanatos at all in HT-22?" → Experiment 1 exists precisely to answer this, with PAR, PARP1-dependence, caspase-independence and AIF relocalisation all shown.

**16. `prelim_ratings`** novelty **H** · evidence-base **M** (key challenges are preprints and review assertions) · overlap-risk **M**

---

# TOPIC 5 — (best fit to the student's bioinformatics strength)

**1. `title_en`**
A prediction from Parkinson's disease genetics, untested in cells: does *partial* GCH1 hypofunction — not knockout — sensitise neuronal cells to ferroptosis?

**2. `core_question`**
Does reducing GCH1 to roughly heterozygous-loss levels (graded siRNA titration and pharmacological inhibition), as opposed to the near-complete loss used in all published ferroptosis work, sensitise HT-22 cells to lipid peroxidation and ferroptotic death — and is that sensitisation reversed by sepiapterin?

**3. `hypothesis`**
The GCH1/BH4 ferroptosis-suppression axis is **non-linear and has substantial reserve**: a ~50% reduction in GCH1, which is what PD-associated deleterious variants plausibly produce, does **not** sensitise under basal conditions but does so only when a second constraint is imposed (GPX4 inhibition, cysteine limitation, or PUFA loading). If true, the popular "GCH1 variants → ferroptosis → PD" narrative requires a second hit and is not a single-gene dose effect.

**4. `novelty_claim`**
New: a **gene-dose-faithful** test of a human-genetics prediction. Every published GCH1-ferroptosis experiment I could verify uses CRISPR activation/loss-of-function screens or strong knockdown; the human genetic signal is a **rare heterozygous deleterious-variant burden** (1.2% vs 0.1% in cases vs controls in a two-cohort Chinese study), which is a very different perturbation. Testing dose, non-linearity and reserve — plus a second-hit requirement — is the specific prediction nobody has made in cells. Traps avoided: not a mechanism transplant (the direction of the prediction is that the simple model *fails*); not docking; not DEG+enrichment; the bioinformatics (eQTL/colocalisation, and optionally MR) is used to *generate a falsifiable cell prediction*, not as the result itself.

**5. `state_of_the_art` (verified)**
Kraft et al. (ACS Cent Sci 2020) report that BH4/BH2 synthesis by GCH1-expressing cells causes lipid remodeling, suppressing ferroptosis by selectively preventing depletion of phospholipids with two polyunsaturated acyl tails, and conclude the protection is independent of GPX4; GCH1 was identified both in a CRISPR-activation screen as a ferroptosis suppressor and in a CRISPR loss-of-function screen as an enhancer. On the genetics side, a two-cohort case-control study found a significant burden of GCH1 deleterious variants in early-onset or familial PD versus controls (1.2% vs 0.1%, P < 0.0001) and linked them to earlier age at onset; a separate study found a rare-variant burden in *SYT11*, *FGF20* and *GCH1* associated with PD after Bonferroni correction. Reduced plasma BH4 has been reported in late-onset sporadic PD. Crucially, reviews note that **only a few studies examined rare GCH1 variants in PD, with conflicting results** — so the genetics must be presented carefully, not oversold. GCH1 also appears in neuronal ferroptosis work in ALS models (SPY1/GCH1/TFR1).

**6. `specific_open_problem`**
Two literatures point at the same gene from opposite ends — human PD genetics and ferroptosis cell biology — and nobody has asked the obvious quantitative question: **is the cellular phenotype dose-sensitive in the range human genetics actually implicates?** Without that, the "GCH1 → ferroptosis → PD" story is an assumption.

**7. `delta_vs_closest_paper`**
Closest paper: **Kraft VAN et al., ACS Cent Sci 2020.** Differences: (a) they manipulated GCH1 at the extremes (overexpression and screen-level loss) in cancer cells; I titrate to a human-genetics-relevant partial loss in a neuronal line; (b) they established the mechanism, I test its **dose–response, reserve and second-hit requirement**, which they did not address; (c) I add the human-genetics arm (brain eQTL/colocalisation with PD GWAS) that connects the cell measurement to the variant burden; (d) I use HT-22, where the GCH1 axis has not, as far as I verified, been tested at all.

**8. `references`**
1. Kraft VAN, et al. | GTP Cyclohydrolase 1/Tetrahydrobiopterin Counteract Ferroptosis through Lipid Remodeling | ACS Central Science | 2020 | DOI 10.1021/acscentsci.9b01063 (from result URL) | `SEARCH_SNIPPET` (full author list not captured)
2. (authors not captured) | GCH1 variants contribute to the risk and earlier age-at-onset of Parkinson's disease: a two-cohort case-control study | 2020 | PMCID PMC7401216 | `SEARCH_SNIPPET`
3. (authors not captured) | Common and rare GCH1 variants are associated with Parkinson disease | ~2018 | no PMID/DOI captured | `TITLE_ONLY`
4. (authors not captured) | SPY1 inhibits neuronal ferroptosis in amyotrophic lateral sclerosis by reducing lipid peroxidation through regulation of GCH1 and TFR1 | ~2023 | PMCID PMC9950139 | `SEARCH_SNIPPET`
5. (authors not captured) | Crucial neuroprotective roles of the metabolite BH4 in dopaminergic neurons | bioRxiv preprint | 2023 | DOI 10.1101/2023.05.08.539795 (from URL) | `SEARCH_SNIPPET`
6. Wang et al. | Pharmacological Inhibition of Ferroptosis as a Therapeutic Target for Neurodegenerative Diseases and Strokes | Advanced Science | 2023 | DOI 10.1002/advs.202300325; PMCID PMC10460905 | `SEARCH_SNIPPET`
7. (authors not captured) | The molecular mechanism of ferroptosis and its relationship with Parkinson's disease | Brain Research Bulletin (ScienceDirect S0361923024001242) | 2024 | DOI not captured | `SEARCH_SNIPPET`
8. (authors not captured) | The cell biology of ferroptosis | Nat Rev Mol Cell Biol | 2024 | DOI 10.1038/s41580-024-00703-5 (from URL) | `SEARCH_SNIPPET`

**9. `models_and_data`**
- Cells: HT-22 (in hand). Optional second line SH-SY5Y ("needs to be obtained") — but note SH-SY5Y+ferroptosis is exactly the saturated genre, so use it only as a replication line, never as the story.
- Tools: *Gch1* siRNA (graded — this is the whole point), DAHP (GCH1 inhibitor, cheap), sepiapterin (rescue, bypasses GCH1 via the salvage pathway), BH4 if affordable; second-hit stressors RSL3, cystine-free medium, arachidonic acid loading; Fer-1 as the ferroptosis control.
- **Bioinformatics (the student's strength, and a genuine component):** GCH1 brain eQTL from GTEx + PD GWAS summary statistics → **colocalisation (coloc in R)**; optionally MR using GCH1 brain-eQTL or pQTL instruments on PD, with the standard sensitivity analyses and an honest statement that a single-gene cis-MR is weak evidence. Also: GCH1/BH4-pathway expression across brain cell types and in PD substantia nigra datasets. **GEO/GWAS accessions to be identified** (search GEO for PD substantia nigra expression datasets; PD GWAS summary stats via the standard consortium portals). Do **not** make the MR the paper's headline — it is the prediction generator.

**10. `key_experiments`**
1. **Dose–response (the core).** Graded *Gch1* knockdown (siRNA concentration series and/or pooled-vs-single siRNA) calibrated by qPCR **and** WB to achieve ~30%, ~50%, ~70%, ~90% loss. Then viability (CCK-8 + LDH + SYTOX, *plate reader*) and lipid peroxidation (C11-BODIPY ratio — *plate reader with both filter sets or fluorescence microscope; flow preferred, not required* — plus Liperfluo and an MDA kit) under: basal, RSL3, cystine-free, and AA-loaded conditions. Output: a dose × stressor sensitisation surface. **Plot GCH1 protein level, not siRNA dose, on the x-axis** — reviewers will demand it.
2. **Pharmacological mirror.** DAHP dose series, same readouts. Agreement between genetic and pharmacological partial loss is the internal control.
3. **Pathway specificity.** Sepiapterin rescue (bypasses GCH1) must reverse the phenotype; folate/BH2 controls; and show the effect is **not** simply NOS-dependent (HT-22 NOS expression by qPCR; a NOS inhibitor arm).
4. **Mechanism consistency, within means.** Kraft's mechanism is phospholipid remodeling — you cannot do lipidomics. Substitute: AA vs oleate loading (does MUFA competition phenocopy BH4 rescue?), ACSL4 WB, and GPX4-independence (does GCH1 knockdown sensitise *on top of* RSL3, i.e. is it additive?). State plainly that lipidomic confirmation is out of scope.
5. **Human-genetics arm:** coloc/MR as above, plus GCH1 expression in PD brain datasets.
*Gating:* fluorescence plate reader required; **BH4 quantification requires HPLC — you do not have it.** Either outsource (~¥3–8k for a small sample set, confirm with a local analytical facility) or omit and rely on sepiapterin/DAHP logic, conceding the gap. Flag this to the student before they commit.

**11. `expected_and_negative_results`** Likely: no basal sensitisation at ~50% loss; clear sensitisation at ~50% loss **plus** a second hit; full sensitisation only below ~25% remaining. That is a **reserve/second-hit model** — a limiting condition on a popular narrative, and genuinely useful. If partial loss sensitises linearly and basally, the simple model is supported and strengthened, which is also publishable. The riskiest outcome is a flat, uninformative result across all doses and stressors; mitigate by establishing the DAHP positive control early.

**12. `difficulty_and_cost`** Difficulty **3/5**. ≈**¥35–60k**: GCH1 antibody (¥2–4k; validate — this is a real risk), siRNAs ×3 + controls (¥4–6k), sepiapterin (¥2–5k), DAHP (¥1k), RSL3/Fer-1 (¥4–7k), arachidonic acid/oleate (¥1k), C11-BODIPY + Liperfluo (¥5–8k), kits GSH/MDA/LDH (¥4–6k), consumables (¥8–12k), **optional BH4 HPLC outsourcing ¥3–8k**. Bioinformatics costs nothing but time.

**13. `timeline_months`** 9–12. The bioinformatics arm can run in parallel from month 1, which suits this student unusually well.

**14. `target_journal_tier`** Q1–Q2 specialty if the dose–response is clean and the genetics arm is rigorous. Realistic: *Free Radical Biology and Medicine*; *Journal of Neurochemistry* or *Neurobiology of Disease*; *Cell Death Discovery*. No promises.

**15. `reviewer_attacks`**
1. "siRNA titration does not model a coding variant — express the variants." → Partly fair. Counter: present it as a gene-dose experiment, not a variant experiment; be explicit in the title ("hypofunction", not "variants"); if budget allows, add WT vs one reported variant construct by transfection.
2. "No BH4 measurement, so you have not shown the mechanism is BH4." → Either outsource HPLC or concede and rest on sepiapterin rescue plus DAHP concordance.
3. "The GCH1–PD rare-variant association is inconsistent across cohorts." → Present the conflicting evidence honestly in the introduction; do not let the coloc/MR carry more weight than it can bear.

**16. `prelim_ratings`** novelty **H** · evidence-base **M–H** (ferroptosis side solid; genetics side genuinely mixed) · overlap-risk **L–M**

---

# TOPIC 6

**1. `title_en`**
One transporter, two deaths: mapping the cystine-flux and glucose window that separates ferroptosis from "disulfidptosis" in a single cell type

**2. `core_question`**
In HT-22 cells, is the boundary between ferroptosis and disulfide-stress death set by SLC7A11 *expression level* (as the disulfidptosis model holds) or simply by **net cystine flux relative to NADPH supply**, such that matching flux abolishes the apparent dependence on SLC7A11 abundance?

**3. `hypothesis`**
The two "distinct" death modalities are two ends of one continuous cystine-flux axis. A 2D titration of extracellular cystine × glucose will produce a continuous landscape in which low flux gives GSH depletion and iron-dependent lipid peroxidation (Fer-1/DFO-rescuable), high flux with low glucose gives NADPH exhaustion and protein disulfide accumulation (reducing-agent-rescuable), and SLC7A11 overexpression only *shifts* the boundary rather than creating a new modality.

**4. `novelty_claim`**
New: the first within-one-cell-type quantitative flux map of the ferroptosis/disulfidptosis boundary, with modality assignment by a pre-specified orthogonal rescue panel rather than by nomenclature. It directly addresses a counterexample noted in the critical reviews — that in SLC7A11-low cells, adding extra cystine also depleted NADPH, produced actin disulfides and caused death — which undermines SLC7A11 abundance as the deciding factor. Traps avoided: this is **not** a cell-line transplant of disulfidptosis and not a TCGA signature paper; the deliverable is a limiting condition that constrains a naming-driven literature, and the design treats "disulfidptosis" critically, as instructed.

**5. `state_of_the_art` (verified)**
Liu et al. (Nat Cell Biol 2023) established that in SLC7A11-high cells under glucose starvation, continued cystine import draws down NADPH, producing disulfide bonds in actin cytoskeletal proteins and F-actin collapse. Critical reviews now flag that some studies lack direct evidence for the core features; that evidence standards should require cystine/SLC7A11 dependence, NADPH or GSH impairment, abnormal disulfide accumulation, actin collapse, mechanism-relevant rescue, and exclusion of competing RCD pathways; that it is unclear why disulfide stress occurs preferentially in actin-associated proteins; and that in SLC7A11-low 786-O cells, extra cystine also depleted NADPH and produced actin disulfides and death. ER-stress manipulation also modulates the phenotype in both directions. On the other side of the axis, HT-22 glutamate toxicity runs through xc⁻ inhibition → GSH depletion → lipid peroxidation, and the transsulfuration literature shows cysteine supply can be rerouted via NRF2/CBS to confer ferroptosis resistance.

**6. `specific_open_problem`**
Whether "disulfidptosis" is a distinct modality or the high-flux arm of a single cystine-handling axis has never been tested by titrating flux in one cell type with matched readouts. The field is generating TCGA "disulfidptosis signatures" on top of an untested dichotomy.

**7. `delta_vs_closest_paper`**
Closest paper: **Liu X, et al., Nat Cell Biol 2023.** Differences: (a) they compared SLC7A11-high versus -low cells; I hold the cell constant and titrate **flux** in two dimensions (cystine × glucose), with SLC7A11 overexpression as a *boundary-shifting* perturbation rather than a modality switch; (b) they did not place ferroptosis and disulfide-stress death on a common axis with a shared rescue panel; (c) neuronal cells, where xc⁻ biology is best characterised and where the opposite perturbation (glutamate) is the canonical death trigger, have not been used.

**8. `references`**
1. Liu X, et al. | Actin cytoskeleton vulnerability to disulfide stress mediates disulfidptosis | Nat Cell Biol | 2023 | PMCID PMC10027392 | `SEARCH_SNIPPET` (full author list not captured)
2. (authors not captured) | Disulfidptosis: Six Riddles Necessitating Solutions | 2024 | PMCID PMC10845294 | `SEARCH_SNIPPET`
3. (authors not captured) | Disulfidptosis: Mechanisms, evidence boundaries, and translational opportunities | 2025 | PMCID PMC13393014 | `SEARCH_SNIPPET`
4. (authors not captured) | Disulfidptosis: disulfide stress–induced cell death | Trends in Cell Biology | 2023 | ScienceDirect S0962892423001411; DOI not captured | `SEARCH_SNIPPET`
5. (authors not captured) | Inhibition of Endoplasmic Reticulum Stress Cooperates with SLC7A11 to Promote Disulfidptosis and Suppress Tumor Growth upon Glucose Limitation | 2025 | PMCID PMC11831432 | `SEARCH_SNIPPET`
6. (authors not captured) | The effect of disulfidptosis induced by glucose starvation in SLC7A11high ovarian cancer cells | 2025 | PMCID PMC12719518 | `SEARCH_SNIPPET`
7. (authors not captured) | Activation of the reverse transsulfuration pathway through NRF2/CBS confers erastin-induced ferroptosis resistance | Br J Cancer | 2020 | DOI 10.1038/s41416-019-0660-x; PMCID PMC7052275 | `SEARCH_SNIPPET`
8. Maher P and colleagues | Using the Oxytosis/Ferroptosis Pathway to Understand and Treat Age-Associated Neurodegenerative Diseases | Cell Chem Biol | 2020 | DOI not captured | `SEARCH_SNIPPET`

**9. `models_and_data`** HT-22 (in hand) ± SLC7A11 overexpression by transfection (in hand). Media: custom cystine and glucose titrations (cystine-free DMEM "needs to be obtained"; inexpensive). Rescue panel: Fer-1, DFO (ferroptosis arm); 2-mercaptoethanol, TCEP or DTT, NAC, and glucose/galactose restoration (disulfide arm); Z-VAD-FMK and necrostatin-1 as exclusion controls. No omics needed. **GEO accession to be identified** if a transcriptomic cross-check is wanted; it is optional here.

**10. `key_experiments`**
1. **The 2D landscape.** 6×6 matrix of extracellular cystine × glucose, viability by CCK-8 **and** LDH **and** SYTOX (*plate reader*), 96-well, several time points. Output: an isobologram-style death surface. Repeat in SLC7A11-overexpressing cells — does the surface shift or change shape?
2. **Modality assignment by rescue panel**, applied across the whole surface, not just at two corners. A continuous shift in which rescue works where defines the axis.
3. **Non-reducing vs reducing SDS-PAGE** for actin and cytoskeletal disulfide oligomers (student has WB — no new equipment). **Critical technical point:** block free thiols in the lysis buffer (NEM or iodoacetamide) or you will generate artefactual disulfides during lysis; include an oxidant-free control and a diamide positive control. Reviewers will ask about exactly this.
4. **The limiting metabolite.** NADPH/NADP⁺ and GSH/GSSG kits (*plate reader*) across the surface; test whether supplying glucose, or NADPH-sparing conditions, moves the boundary as predicted.
5. **Transsulfuration bypass.** Homocysteine or cystathionine supplementation ± a CTH/CBS inhibitor; qPCR/WB for *Cbs*/*Cth*. Tests whether HT-22 have a functional bypass that sets the low-flux edge of the window.
6. WB for SLC7A11 to confirm overexpression levels and to plot phenotype against protein, not plasmid dose.
*Gating:* fluorescence plate reader for SYTOX; everything else is absorbance kits and WB. **No flow cytometry, no actin imaging required** — but note that the absence of F-actin imaging is the main thing reviewers will want, so a basic phalloidin stain on the fluorescence microscope (if available) would materially strengthen the paper. Flag microscope availability as a soft dependency.

**11. `expected_and_negative_results`** Likely: a continuous surface with a flux-determined boundary, and SLC7A11 overexpression shifting rather than redefining it. That is a limiting-condition result that constrains a fast-growing nomenclature literature — publishable. If the two deaths are genuinely discontinuous and SLC7A11-abundance-dependent, that *validates* the disulfidptosis model in a new lineage and is still publishable, though less interesting. Either way the quantitative map is the deliverable.

**12. `difficulty_and_cost`** Difficulty **3/5**. ≈**¥30–50k**: SLC7A11 plasmid (¥2–4k), SLC7A11/GPX4/actin antibodies (¥5–8k), custom/cystine-free media and glucose-free DMEM (¥3–5k), NADPH and GSH/GSSG kits (¥4–7k), reducing agents/NEM/diamide (¥1–2k), Fer-1/DFO/inhibitors (¥4–6k), SYTOX/LDH (¥2–3k), consumables (¥8–12k). Media formulation work is the hidden time cost, not the money.

**13. `timeline_months`** 8–10.

**14. `target_journal_tier`** Q2, Q1 specialty if the map is clean. Realistic: *Free Radical Biology and Medicine*; *Biochemical Pharmacology* or *Archives of Biochemistry and Biophysics*; *Cell Death Discovery*. No promises.

**15. `reviewer_attacks`**
1. "Without lipidomics or proteomics you cannot claim these are one axis." → Frame the claim phenomenologically and pharmacologically; say what would be needed to go further.
2. "Non-reducing gels are prone to lysis-induced artefactual oxidation." → Thiol-blocking lysis, oxidant-free and diamide controls, and report them in the main figures, not the supplement.
3. "SLC7A11 overexpression in HT-22 is non-physiological, so your window is an artefact of expression level." → Report measured protein levels, use at least two expression levels, and present the flux interpretation as the primary claim.

**16. `prelim_ratings`** novelty **M–H** · evidence-base **M** · overlap-risk **M** (the disulfidptosis literature is expanding very fast, mostly with low-value signature papers — the critical/quantitative niche is less crowded but the clock is running)

---

# `domain_landscape` (2023–2026 frontier; ~540 words)

The honest state of this field in late 2026 is that the *discovery* phase of regulated cell death has given way to a *consolidation and correction* phase, and the correction phase is where an undergraduate can still contribute.

Three genuinely live fronts emerged from my searches. **First, the terminal step of lytic death.** NINJ1 went from unknown to "the executioner of plasma membrane rupture" in about three years, and the ferroptosis extension (Ramos et al., EMBO J 2024) is now in open conflict with Riegman's osmotic/pore model (Nat Cell Biol 2020) and with a third account placing NINJ1 *upstream* at xCT with CoA involvement (Cell Death Dis 2024). A 2024 preprint adds that NINJ1-dependence is inducer-specific (erastin yes, RSL3 no), and Nature 2025 adds mechanical-strain-dependent membrane fragility. The 2026 reviews (FEBS J, Biochem Soc Trans, Front Immunol) paper over the disagreement with "dispensable for commitment, required for efficient rupture" — which, if taken seriously, means the field's default readout (LDH release) is a rupture assay, not a death assay. Nobody has tested any of this in a neuronal or NINJ1-low cell. This is the single best opening I found.

**Second, central assumptions are being directly measured for the first time, and some are failing.** The most striking 2026 paper I found is Ponnusamy et al. (J Biol Chem 2026, PMID 41819262): the labile iron pool does **not** rise during ferroptosis in colorectal cancer cells. A 2025 preprint pushes in the opposite direction via polyamines. In parthanatos, reviews now state that NAD⁺ depletion without PARP1 hyperactivation is insufficient, a 2026 preprint uncouples NAD⁺ from ATP depletion, and the MIF/"PAAN" nuclease executioner failed to replicate in a 2023 J Med Chem study. In ferroptosis chemistry, the Pratt group's demonstration that lipoxygenase inhibitors act as off-target radical-trapping antioxidants remains the template for how a reagent-artefact paper reshapes a field.

**Third, reagent and assay specificity is becoming a legitimate publishable topic.** Pan-acyl antibody specificity has been challenged (Sci Rep 2021), a 2025 preprint questions the widely used H3K18la antibody, and vendor documentation openly states that WST-8 reacts with reducing agents — a warning the ferroptosis literature largely ignores.

**What is saturated junk.** Essentially all of: natural product + Nrf2/HO-1 + HT-22 or SH-SY5Y; "compound protects via GPX4/AMPK/mTOR"; cuproptosis and disulfidptosis TCGA signature papers (the underlying biology has acknowledged holes — elesclomol's FDX1 dependence collapses above ~40 nM, Cu-elesclomol oxidises ascorbate to H₂O₂, and SLC7A11-low cells also show the disulfidptosis phenotype); and the exploding lactate/lactylation-meets-ferroptosis literature, where I found a 2026 review conceding that lactate has "contrasting regulatory effects" in normal versus tumour cells — a polite way of saying the primary results contradict each other. Mendelian randomisation of serum iron or ferritin on neurodegeneration is similarly flooded.

**Undergraduate opportunity, honestly.** It is real but narrow. It lies in *measurement*, not in new molecules: adjudicating a two-paper disagreement with a readout that can tell them apart; measuring a step everyone assumes; or quantifying an artefact. These designs are cheap, need no flow cytometry or omics, publish in Q1–Q2 specialty journals rather than top-tier, and — crucially — remain publishable when the result is negative. The corresponding disadvantage is that correction papers get hostile reviews and need unusually tight controls. A student who cannot tolerate three rounds of methodological nitpicking should take Topic 3.

---

# `rejected_ideas`

1. **ALDH2 rs671 → 4-HNE accumulation → ferroptosis in neurons.** Tempting (rs671 is a high-frequency East Asian functional variant with excellent human genetics), but npj Parkinsons Dis 2025 already published ALDH2/rs671/ferroptosis in dopaminergic neurons via PRDX6, and a 2026 J Cell Mol Med paper covers ALDH2-ferroptosis in I/R — the remaining delta is a cell-type swap.
2. **Cuproptosis or disulfidptosis gene-signature prognostic model in TCGA.** This is the DEG+correlation+enrichment genre explicitly forbidden; it is built on an untested dichotomy and would add nothing.
3. **Lactylation of a metabolic enzyme regulating ferroptosis in HT-22.** The 2024–2026 output here is enormous and mutually contradictory; worse, the pan-Kla and H3K18la antibodies the whole design depends on have unresolved specificity problems, so the student would be building on a reagent that may not work.
4. **Any "natural compound protects HT-22 from glutamate/erastin via Nrf2/HO-1".** Forbidden by the brief and scientifically worthless; my own searches returned at least four such papers unprompted (salidroside, oxysophocarpine, GIP, and others), which is the clearest possible evidence of saturation.
5. **Adjudicating whether MIF really has nuclease activity ("PAAN").** A genuinely live controversy (J Med Chem 2023 could not assign the activity unambiguously and raised bacterial contamination), but resolving it requires recombinant protein expression, purification and in vitro nuclease assays — none of which the student has.
6. **DHODH vs FSP1 (brequinar off-target) adjudication.** A real published Nature exchange, but the decisive measurements are FSP1 NADH-oxidase activity assays and CoQ measurements; without those, the student would only reproduce viability curves and could not settle anything.
7. **Cytosolic mtDNA by digitonin fractionation is an artefact.** A near-miss: the gap is real (a protocol paper states the assays are not standardised, raising the risk of artefacts, and names both under- and over-digitonin failure modes), and qPCR-based mtDNA quantification is in the student's hands. Rejected because the strongest version needs single-cell or spike-in validation to be convincing, and journals would likely treat it as a protocol note rather than an original article — poor return for 9 months.
8. **ATF4 is pro- or anti-ferroptotic.** The contradiction is real and well documented (J Hepatol 2023 and Cell Metab 2022 protective; PERK-eIF2α-ATF4 and ATF4-CHAC1 studies pro-ferroptotic), but the resolution almost certainly lies in stress intensity and duration across tissues, which means a convincing study needs multiple cell types and time-resolved proteomics — out of scope, and a single-cell-line answer would just add a ninth contradictory paper.
9. **"Mitochondria are required for cysteine-deprivation but not GPX4-inhibition ferroptosis."** A real and still-contested claim (Gao et al., Mol Cell), but the clean test needs mtDNA-depleted/ρ⁰ cells or respirometry, and a 2024 VDAC1 study already complicates the clean separation.

---

## Committee recommendation

If the student has a **fluorescence plate reader**: pursue **Topic 1**, with **Topic 2** as the fallback if the NINJ1 antibody or HT-22 NINJ1 expression gate fails at month 1. If their bioinformatics ambition is the priority and they want a project with a parallel computational arm: **Topic 5**. If the budget is at the ¥20k floor, or if they need near-certainty of a publication within 7 months: **Topic 3**, understanding that the ceiling is a methods journal.

Two things to settle before any commitment: (1) does the plate reader do fluorescence, and with which filter sets; (2) can a second cell line (HT-1080 strongly preferred) be obtained. Both answers change the ranking.

**Verification ledger:** 23 WebSearch queries executed; the session cap was then reached, so the osmoprotectant literature (Topic 1, experiment 5) and all GEO accession hunting remain **unverified** and are marked as such. No reference above was written from memory alone; items I could not confirm in a result are tagged `TITLE_ONLY` or stated as UNVERIFIED with no digits.