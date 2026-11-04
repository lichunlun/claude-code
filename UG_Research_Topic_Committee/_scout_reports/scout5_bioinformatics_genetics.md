# Topic-Selection Committee Report
## Computational biology / statistical genetics seat

**Scope note / limits of verification.** Direct access to PubMed, PMC, eutils, Crossref, ClinicalTrials.gov, GEO and OpenGWAS was blocked in this session, so nothing below was confirmed by querying a database. Everything is grounded in 48 actual WebSearch calls; my search budget was then exhausted, so four planned verification searches did not run (SEA-AD's named vulnerable neuronal subtypes; a GEO accession for HT-22/glutamate RNA-seq; DepMap ferroptosis co-dependency specifics; STROBE-MR adherence audits). Those gaps are flagged in-line. **No GEO accession appeared verbatim in any result, so I give none.** Every reference carries a `verification` tag; `UNVERIFIED` items carry no digit strings.

---

# TOPIC 1

**1. `title_en`**
Orthogonal bench validation of neuron-prioritized Alzheimer's risk genes: does knockdown of a computationally nominated neuronal target alter hippocampal neuronal vulnerability to oxidative and ferroptotic death?

**2. `core_question`**
For a pre-specified, published-but-functionally-unvalidated AD risk gene nominated as acting in excitatory neurons, does siRNA knockdown in HT-22 cells shift viability under glutamate/erastin/RSL3 challenge in the direction predicted by the risk allele's eQTL effect?

**3. `hypothesis`**
At least one neuron-prioritized AD gene is a cell-intrinsic modifier of neuronal oxidative/ferroptotic death, such that knockdown moves HT-22 EC50 for the stressor in the direction predicted by the risk-increasing allele's effect on expression; genes prioritized purely by coloc+MR+literature (no orthogonal evidence) will validate at a markedly lower rate than genes with convergent single-cell eQTL and expression evidence.

**4. `novelty_claim`**
New: a *pre-registered, directional* bench test of a named computational prediction, with the direction fixed before the experiment by the eQTL sign. The fake-novelty trap it avoids is "yet another bioinformatics nomination paper": the deliverable is not a gene list but a confirmation/refutation of someone else's list. It also avoids the "hub gene" trap because candidate selection is driven by genetic evidence (coloc direction), not by differential-expression rank, and because the experiment can falsify the prediction. Crucially, Uffelmann et al. (Nature 2026) state in their own peer-review file that 43 of their prioritized genes (34%) rest *solely* on coloc + MR + literature with no orthogonal validation, and that they performed no functional validation — that sentence is the paper's premise.

**5. `state_of_the_art`**
AD heritability is microglia-dominated (Nott 2019 Science; Bellenguez 2022; the 2026 consensus meta-analysis reports enrichment in microglial genes). Cell-type-resolved eQTL resources now exist and are open (Bryois 2022 Nat Neurosci — 8 brain cell types, 7,607 eGenes, 46% cell-type-specific, full summary statistics on Zenodo; Fujita 2024 Nat Genet — 424 ROSMAP donors, ~1.5M nuclei, 81 subtypes; de Klein 2023 MetaBrain). A 2025 cell-type TWAS preprint reports 223 cell-type-specific AD risk genes, 91 independent, of which 7 are excitatory-neuron-specific (ARL4A, RAB8B, HEXIM1 named) and 4 inhibitory-neuron-specific (SNX22, FMNL1, FOSB named). Uffelmann 2026 (Nature) reports ~118–127 loci and finds that neuronal cell-type associations drop to only nominal significance after adjusting for average differential expression across cell types.

**6. `specific_open_problem`**
Nobody has tested whether *any* neuron-assigned AD risk gene is a cell-intrinsic determinant of neuronal death vulnerability. The 2025–2026 papers that assign AD genes to neurons explicitly decline to do functional work, and the one paper that does functional validation on brain eQTL colocalization (EGFR, via CRISPRi) did not use neuron-specific eQTLs. The neuronal AD signal is therefore simultaneously (a) repeatedly reported and (b) suspected by its own discoverers of being secondary to microglial signal.

**7. `delta_vs_closest_paper`**
Closest real papers: **Uffelmann et al., Nature 2026** (nominates neuronal genes, explicitly performs no functional validation) and the **Nature Communications 2025 integrative systems-biology paper** that knocked down MEPCE and HNRNPA2B1 in flies and human iPSCs. Delta vs Uffelmann: the student supplies the missing orthogonal functional evidence for one named gene, with a pre-specified direction. Delta vs the Nat Commun paper: their phenotype was tau-mediated neurotoxicity in flies/iPSCs (resources the student does not have); the student's phenotype is oxidative/ferroptotic vulnerability in a mouse hippocampal line, which is a *different and independently interesting* axis, and their candidate selection was not neuron-eQTL-driven.

**8. `references`**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | Uffelmann E, Wightman DP, Bahrami S, Shadrin AA, Fominykh V, Ojima T, Jiang C, Benner C, et al. | Alzheimer's disease genetics converges on microglial and neuronal dysregulation | Nature | 2026 (online 28 Oct) | PMID 42951976; DOI 10.1038/s41586-026-11206-y | SEARCH_SNIPPET |
| 2 | Bryois J, et al. | Cell-type-specific cis-eQTLs in eight human brain cell types identify novel risk genes for psychiatric and neurological disorders | Nature Neuroscience 25(8):1104–1112 | 2022 | PMID 35915177; DOI 10.1038/s41593-022-01128-z; data Zenodo DOI 10.5281/zenodo.5543734 | SEARCH_SNIPPET |
| 3 | Fujita M, Gao Z, et al. | Cell subtype-specific effects of genetic variation in the Alzheimer's disease brain | Nature Genetics 56(4):605–614 | 2024 | PMID 38514782; DOI 10.1038/s41588-024-01685-y | SEARCH_SNIPPET |
| 4 | Bellenguez C, Küçükali F, Jansen IE, et al. | New insights into the genetic etiology of Alzheimer's disease and related dementias | Nature Genetics 54(4):412–436 | 2022 | DOI 10.1038/s41588-022-01024-z; sumstats GWAS Catalog **GCST90027158** | SEARCH_SNIPPET |
| 5 | Nott A, et al. | Brain cell type–specific enhancer–promoter interactome maps and disease-risk association | Science 366:1134–1139 | 2019 | PMID/DOI not captured — needs verification | TITLE_ONLY |
| 6 | Tambets R, Kolde A, Kolberg P, Love MI, Alasoo K | Extensive co-regulation of neighboring genes complicates the use of eQTLs in target gene prioritization | HGG Advances | 2024 | PMID 39210598; DOI 10.1016/j.xhgg.2024.100348 | SEARCH_SNIPPET |
| 7 | (first author not captured) | Cell-type-specific transcriptomic-wide association studies detected 91 independent risk genes for Alzheimer's disease dementia | medRxiv **preprint** | 2025 | DOI 10.1101/2025.05.27.25328452 | SEARCH_SNIPPET (preprint) |
| 8 | (authors not captured) | An integrative systems-biology approach defines mechanisms of Alzheimer's disease neurodegeneration | Nature Communications | 2025 | DOI 10.1038/s41467-025-59654-w | SEARCH_SNIPPET |
| 9 | Gabitto MI, et al. | Integrated multimodal cell atlas of Alzheimer's disease (SEA-AD) | Nature Neuroscience | 2024 | DOI 10.1038/s41593-024-01774-5 | SEARCH_SNIPPET |

**9. `models_and_data`**
- **AD GWAS**: Bellenguez 2022, GWAS Catalog **GCST90027158** (this accession appeared verbatim in results; open). Wightman 2021 (DOI 10.1038/s41588-021-00921-z) is hosted on the NIAGADS FTP and — critically — includes a variant *excluding 23andMe and UK Biobank*, i.e. a proxy-light outcome for sensitivity analysis. The 2026 consensus meta-analysis (DOI 10.1038/s41588-026-02583-1) reports 56 loci detected specifically in clinically diagnosed cases; its summary-statistics access route was **not** confirmed in my searches — needs verification.
- **Cell-type eQTL**: Bryois 2022 full summary statistics on Zenodo (DOI 10.5281/zenodo.5543734) — open, laptop-sized, the single best entry point. Fujita 2024 (ROSMAP snRNA-eQTL) — access route not confirmed; ROSMAP generally requires an AD Knowledge Portal / Synapse data-use agreement. MetaBrain at metabrain.nl (de Klein 2023), open per the paper's data-availability statement.
- **Single-cell expression**: SEA-AD processed snRNA-seq is open on the AWS Open Data Registry (bucket name **sea-ad-single-cell-profiling** appeared in results); raw FASTQ is controlled-access via Sage Bionetworks / AD Knowledge Portal. Also mirrored on CZ CELLxGENE, but CELLxGENE's own page warns its copy has reduced metadata and fewer genes — use the AWS copy.
- **Mouse orthology / HT-22 expression**: the student must confirm the candidate is expressed in HT-22 by qPCR before committing. There is no public HT-22 expression atlas I verified; a glutamate-treated HT-22 RNA-seq dataset exists behind *Scientific Reports* 2023 (DOI 10.1038/s41598-023-34183-y) but **no accession appeared in my results — accession to be identified by the student in GEO**.
- **NOT available**: UK Biobank individual-level data; any human patient material.

**10. `key_experiments`**
*Computational (R, laptop-feasible):*
1. Harmonize AD GWAS (`MungeSumstats`) and the Bryois Zenodo cell-type eQTL files.
2. Colocalization per locus with `coloc` (`coloc.abf` plus `coloc.susie` for multiple causal variants); report PP(H4) and the *direction* of the eQTL effect for the risk-increasing allele. Follow with `susieR` fine-mapping.
3. cis-MR per candidate gene with `TwoSampleMR` / `MendelianRandomization` using *conditionally independent* cis instruments only — and explicitly report the Tambets 2024 benchmark as the prior on precision (see reviewer attacks).
4. Cell-type restriction: `Seurat`/`anndata` + `scDRS` or MAGMA-style enrichment on SEA-AD to confirm excitatory-neuron expression and to check the gene is not simply microglia-expressed. (I did **not** verify which of scDRS/CELLECT is best supported in 2026 — student should check.)
5. Final candidate selection by a written, pre-registered rule: neuron-specific coloc PP(H4) > 0.8, mouse ortholog exists, expressed in HT-22 by qPCR, directional prediction unambiguous. Register on OSF *before* the wet lab.

*Wet lab (all within the student's stated techniques):*
6. qPCR to confirm candidate expression in HT-22; siRNA (3 independent duplexes + scrambled NC) with Lipofectamine; knockdown confirmed by qPCR **and** Western blot (precedent: HT-22 siRNA at 40 nM with Lipofectamine 2000 is standard in this model).
7. Dose–response viability (CCK-8/MTT) under three mechanistically distinct stressors: glutamate (system xc− block), erastin (xCT inhibition), RSL3 (direct GPX4 inhibition), plus H2O2 as a *non-ferroptotic* specificity control. Report EC50 shift, not just one concentration.
8. Mechanism readouts on a plate reader: TBARS/MDA, GSH/GSSG, intracellular Fe2+; Western blot for GPX4, SLC7A11/xCT, ACSL4, FSP1/AIFM2.
9. Rescue specificity: ferrostatin-1 / liproxstatin-1 should abolish the effect if it is ferroptotic.

*Gating requirements and substitutes:*
- **Flow cytometry (not assumed available)** — needed for conventional C11-BODIPY 581/591 lipid-ROS. **Substitute:** C11-BODIPY read on a fluorescence microplate reader is explicitly listed as a valid readout, and a Heliyon 2024 review recommends pairing C11-BODIPY with an MDA kit rather than relying on either alone. This substitution must be stated in Methods, not hidden.
- **Confocal (not assumed)** — substitute: plate-reader kinetics plus ordinary fluorescence microscopy if available.
- **Lentivirus/CRISPR (not assumed)** — siRNA only; this is a real limitation (transient, partial, off-target) and the three-duplex design is the mitigation.
- **Rescue by overexpression** would need a plasmid and ideally a siRNA-resistant construct — flag as optional stretch requiring transfection-grade plasmid purchase.

**11. `expected_and_negative_results`**
Most likely outcome: **1 of 3–4 tested candidates shows a reproducible EC50 shift, the rest do not.** That is a publishable result *as a validation-rate paper* ("n of N neuron-prioritized AD genes are cell-intrinsic modifiers of oxidative vulnerability"), because the claim being tested was pre-specified and named. A fully negative result is publishable but only in a venue that accepts confirmatory/negative work — eNeuro explicitly lists "Negative Results" and "Confirmation" as article types, with the requirement that negative-results papers test the hypothesis by multiple experimental approaches and use rigorous positive and negative controls. Build those controls in from day one or the negative result is unpublishable.

**12. `difficulty_and_cost`**
Difficulty **4/5**. Estimated ¥25,000–50,000 (my estimate; I did not search Chinese reagent pricing): siRNA synthesis ¥1,500–3,000; transfection reagent ¥2,000–3,500; antibody panel (GPX4, xCT, ACSL4, FSP1, loading control) ¥10,000–20,000 — the dominant line item; WB consumables ¥3,000–6,000; CCK-8 ¥1,000–2,000; MDA/GSH/Fe2+ kits ¥1,500–4,500; compounds (erastin, RSL3, ferrostatin-1, liproxstatin-1) ¥4,000–10,000, with RSL3 and liproxstatin-1 the expensive ones; C11-BODIPY ¥3,000–5,000; culture consumables ¥500–1,000/month. **Add an APC of ¥10,000–30,000+** for most realistic open-access targets — budget it explicitly or target a subscription journal.
Compute: steps 1–3 run comfortably on a laptop (16 GB). Step 4 does **not** — SEA-AD h5ad files are large; the student must subset to excitatory neurons on a server or use pseudobulk matrices. Do **not** attempt to mirror deCODE or UKB-PPP wholesale: the deCODE download page lists a plasma-proteomics comparison entry at 19.7 TB. Fetch per-protein/per-locus files only.

**13. `timeline_months`**
Computational candidate selection and pre-registration: months 1–3. Expression confirmation + siRNA optimization: months 3–5. Main experiments with three biological replicates: months 5–9. Writing and submission: months 9–12. **Honest assessment: this is a 12-month project with no slack, and realistically 14–18 months if siRNA knockdown efficiency is poor on the first candidate.** It is the highest-ceiling, highest-risk option here.

**14. `target_journal_tier`**
Tier: solid specialty, not top-tier. Realistic: *Free Radical Biology and Medicine*; *Journal of Neurochemistry*; *Cell Death & Disease* (harder); *Molecular Neurobiology*. *Redox Biology* is a stretch. No acceptance can be promised. Honest warning: if the paper reads as "bioinformatics + one cell line," several journals will desk-reject; the framing must lead with the falsification of a named published prediction, not with the pipeline.

**15. `reviewer_attacks`**
1. **"Your colocalization does not identify the causal gene."** This is lethal and well-evidenced: Tambets et al. (HGG Advances 2024) found that assigning fine-mapped pQTLs to the *closest protein-coding gene* beat every colocalization method tested (71.9% precision / 76.9% recall), while coloc.susie achieved only 45.1% precision at 46.3% recall; combining MR with multiple conditionally distinct colocalizing QTLs reached 81% precision but 7.1% recall. You must quote this against yourself and justify your candidate on convergent evidence, not coloc alone.
2. **"HT-22 is a mouse immortalized line, not a human neuron, and the AD signal is microglial."** Uffelmann 2026's own analysis shows neuronal associations falling to nominal significance after adjustment, and Nott 2019 placed sporadic AD variants largely in microglial enhancers. You cannot claim to model AD; you can only claim to test cell-intrinsic neuronal vulnerability.
3. **"A transient siRNA phenotype under a pharmacological stressor is not the GWAS mechanism."** True. The honest claim is a necessary-condition test, not a mechanism. Pre-register the direction so you cannot be accused of post-hoc sign fitting.

**16. `prelim_ratings`**
Novelty **H** · Evidence-base **H** · Overlap-risk **M** (several well-resourced labs are circling these gene lists; a 2025 CRISPRi/EGFR paper and the Nat Commun 2025 fly/iPSC paper show the genre is live).

---

# TOPIC 2

**1. `title_en`**
How robust are plasma-proteome Mendelian randomization targets for Alzheimer's disease? A systematic robustness audit across outcome definitions, proteomic platforms, epitope artefacts and colocalization frameworks.

**2. `core_question`**
Of the plasma proteins nominated as causal AD targets by the 2024–2026 proteome-wide MR literature, what fraction survives (a) substitution of the outcome GWAS for a clinically-diagnosed-only definition, (b) substitution of the proteomic platform (SomaScan ↔ Olink), (c) removal of coding-variant instruments that may act through epitope effects, and (d) colocalization under a multiple-causal-variant framework?

**3. `hypothesis`**
A substantial minority of published AD protein targets are platform- or outcome-definition-contingent; the subset surviving all four stress tests will be small and will be dominated by the proteins already reported by multiple independent groups (GRN, CR1, PILRA), while single-paper nominations will largely fail.

**4. `novelty_claim`**
New: the first head-to-head robustness audit of a *named, enumerable* MR target literature, producing a tiered, annotated target list plus a quantified flip rate. Avoids the "naive MR" trap completely — this is not a new MR of a new exposure; it is an adjudication of an existing body of claims, which is exactly what PLOS Genetics' 2025 MR policy and the Frontiers in Endocrinology 2024 editorial on derivative open-database studies are asking for. It also avoids the "sensitivity-analysis theatre" trap: the four stress tests are chosen because each has a documented mechanism of failure, not because they are conventional.

**5. `state_of_the_art`**
At least five 2025 papers ran proteome-wide MR + colocalization for AD and converged only partially. Yu, Jiang, Zhou & Zhao (J Alzheimers Dis 2025) found 9 proteins in deCODE and 17 in UKB-PPP, with only BCAM, CD55, CR1 and GRN in both and coloc supporting GRN and CR1. A J Transl Med 2025 paper scanning 1,916 proteins nominated BLNK, CD2AP, GRN, PILRA and PILRB. A Brain 2025 paper reported 169 significant protein–disease associations at 5% FDR from 13,377 tested, with 18 proteins supported by plasma pQTL plus brain eQTL colocalization. A Brain and Behavior 2025 paper using 91 inflammatory proteins prioritized MMP1 and CCL4. A fifth prioritized BIN1, Siglec-3, GSTP1, SERPINF2 and GRN. Meanwhile Eldjarn et al. (Nature 2023) found only modest correlation between Olink and SomaScan despite similar cis-pQTL counts (2,101 vs 2,120), with worked examples (CD58/multiple sclerosis) where the platform changes the conclusion — and that paper itself required a 2024 Author Correction that *reversed* its precision claim.

**6. `specific_open_problem`**
Every one of those papers used a different outcome GWAS, a different platform, and a different coloc method, and none audited the others. Nobody has quantified how much of the AD protein-target literature is an artefact of those three choices. Separately, no published AD proteome-MR paper I found re-tested its targets against the 2026 consensus ADRD meta-analysis, which reports 56 loci detected *specifically* in clinically diagnosed cases and flags 18 loci (15 novel) as requiring external validation.

**7. `delta_vs_closest_paper`**
Closest real paper: **Yu, Jiang, Zhou & Zhao, J Alzheimers Dis 2025** (DOI 10.1177/13872877251344572) — the only one that already compared deCODE against UKB-PPP and reported the shrinkage (26 nominations → 4 shared → 2 colocalizing). Delta: they compared platforms for their *own* analysis, on one outcome GWAS, with one coloc method. The student audits *the whole published set* of nominations, adds two tests they did not perform (coding-variant/epitope exclusion; clinical-only vs proxy-included outcome), and uses a multiple-causal-variant coloc framework benchmarked against the Tambets precision ceiling.

**8. `references`**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | Yu K, Jiang R, Zhou D, Zhao Z | Therapeutic targets for Alzheimer's disease: proteome-wide Mendelian randomization and colocalization analyses | Journal of Alzheimer's Disease | 2025 | DOI 10.1177/13872877251344572 | SEARCH_SNIPPET |
| 2 | (authors not captured) | Biomarker identification for Alzheimer's disease through integration of comprehensive Mendelian randomization and proteomics data | Journal of Translational Medicine | 2025 | PMID 40050982; DOI 10.1186/s12967-025-06317-5 | SEARCH_SNIPPET |
| 3 | Eldjarn GH, Ferkingstad E, et al. | Large-scale plasma proteomics comparisons through genetics and disease associations | Nature 622:348–358 (+ Author Correction 2024, PMC11153164) | 2023 | PMID 37794188; DOI 10.1038/s41586-023-06563-x | SEARCH_SNIPPET |
| 4 | Sun BB, Chiou J, Traylor M, et al. | Plasma proteomic associations with genetics and health in the UK Biobank | Nature 622:329–338 | 2023 | DOI 10.1038/s41586-023-06592-6 | SEARCH_SNIPPET |
| 5 | Ferkingstad E, et al. | Large-scale integration of the plasma proteome with genetics and disease | Nature Genetics 53(12):1712–1721 | 2021 | PMID 34857953; DOI 10.1038/s41588-021-00978-w | SEARCH_SNIPPET |
| 6 | Tambets R, Kolde A, Kolberg P, Love MI, Alasoo K | Extensive co-regulation of neighboring genes complicates the use of eQTLs in target gene prioritization | HGG Advances | 2024 | PMID 39210598; DOI 10.1016/j.xhgg.2024.100348 | SEARCH_SNIPPET |
| 7 | Bellenguez C, Lambert J-C, et al. (508 contributors per Alzforum) | Consensus meta-analysis of genome-wide association studies for Alzheimer's disease and related dementias | Nature Genetics 58:1214–1225 | 2026 | PMID 41282675; DOI 10.1038/s41588-026-02583-1 | SEARCH_SNIPPET |
| 8 | (authors not captured) | Epitope effect prevalence in affinity-based pQTL studies | bioRxiv **preprint** | 2025 | DOI 10.1101/2025.06.20.660695 | SEARCH_SNIPPET (preprint) |
| 9 | (authors not captured) | Expectations for papers performing Mendelian randomization analyses | PLOS Genetics | 2025 | DOI 10.1371/journal.pgen.1011767 (PMC12270091) | SEARCH_SNIPPET |
| 10 | (authors not captured) | Benchmarking Bayesian colocalization methods in validating Mendelian randomization-based target discoveries from circulating proteins for cardiometabolic diseases | bioRxiv / published | 2024 / 2026 | DOI 10.1101/2024.10.14.617627; PMID 42613742 | SEARCH_SNIPPET |
| 11 | (authors not captured) | Mendelian randomization identifies proteins involved in neurodegenerative diseases | Brain 148(7):2412 | 2025 | DOI not captured — needs verification | SEARCH_SNIPPET |

**9. `models_and_data`**
All open, no credentialing:
- **deCODE SomaScan pQTL** summary data at decode.com/summarydata (Ferkingstad 2021: 35,559 Icelanders, 4,719 proteins, 18,084 pQTLs). Download per-protein only — the page lists a companion comparison dataset at 19.7 TB.
- **UKB-PPP Olink pQTL** summary statistics at ukb-ppp.gwas.eu and on the AWS Open Data Registry (registry.opendata.aws/ukbppp), per-protein files plus annotation metadata. Underlying NPX measures require UK Biobank approval — **not needed and not available to this student**; summary statistics are sufficient and are the realistic route.
- **Rare-variant pQTL** (Dhindsa 2023, Nature 622:339–347, DOI 10.1038/s41586-023-06547-x) via azphewas.com — useful as an orthogonal check that a cis signal reflects real abundance.
- **AD outcome GWAS**: Bellenguez 2022 (**GCST90027158**, open); Wightman 2021 (NIAGADS, including the *excluding 23andMe and UKBB* version — this is the key proxy-light comparator); the 2026 consensus meta-analysis (access route **needs verification**).
- **Brain eQTL for orthogonal support**: Bryois 2022 (Zenodo DOI 10.5281/zenodo.5543734), MetaBrain (metabrain.nl).
- Practical note: OpenGWAS now **requires authentication** (API key in `OPENGWAS_JWT`) and enforces per-user allowances; several GitHub issues document breakage and quota exhaustion. Do not build the project around OpenGWAS API calls — download flat summary-statistics files instead.

**10. `key_experiments`**
Purely computational; R; laptop-feasible throughout.
1. **Define the audited set reproducibly.** A pre-registered search of 2023–2026 proteome-wide/cis-pQTL MR papers with AD or ADRD as outcome; extract every nominated protein with its reported platform, instrument set, outcome GWAS, MR method and coloc evidence. This is the paper's backbone — treat it as a systematic review with PRISMA-style flow and a published extraction sheet.
2. **Re-instrument from scratch.** Cis window ±500 kb (or ±100 kb; pre-specify), LD clumping with a 1000 Genomes EUR reference via `ieugwasr`/`plinkbinr`, F-statistics and I² reported per instrument. `TwoSampleMR` + `MendelianRandomization` (IVW, Wald ratio for single-SNP, MR-Egger, weighted median), `MRPRESSO` where k is adequate. Steiger directionality where defensible.
3. **Stress test A — outcome definition.** Re-run every target against Bellenguez 2022, Wightman 2021 (full and excluding 23andMe+UKBB), and the 2026 consensus (all-cases and clinically-diagnosed stratum if obtainable). Report sign flips and significance flips, not just a table of p-values.
4. **Stress test B — platform.** Re-run each target with deCODE and with UKB-PPP instruments; quantify concordance of effect direction and magnitude.
5. **Stress test C — epitope artefact.** Re-run excluding cis instruments in or near coding sequence; cross-check whether the cis-pQTL has a concordant cis-eQTL. A 2025 preprint estimates missense-mediated epitope effects affect ≤12% of cis-pQTLs — so the expected yield is modest, and you should say so rather than overclaim.
6. **Stress test D — colocalization.** `coloc` (`coloc.abf` and `coloc.susie`), `susieR` fine-mapping; consider SharePro, which the cardiometabolic benchmark found most often supported significant MR associations. Report PP(H4) and, explicitly, the Tambets precision benchmark as the calibration prior.
7. **Deliverable.** A four-tier annotated target list, a quantified flip rate per stress test, and an open GitHub repository + OSF pre-registration. Visualization with `ggplot2`/`forestploter`.
- **Gating:** none. No wet lab, no money, no credentialing. This is the only topic here with essentially zero material cost.
- **Skill gating (real):** this needs genuine statistical-genetics care, not package-calling. The student will need a supervisor or collaborator who can referee instrument selection and LD handling, or the audit will itself be attackable.

**11. `expected_and_negative_results`**
A "negative" result — most targets survive — is *also* a strong paper, because it would be the first evidence that the AD proteome-MR literature is more robust than its critics assume. The design is symmetric, which is exactly why it is defensible. The likely real outcome is heterogeneous: a handful of multiply-replicated proteins survive everything, and a long tail of single-paper nominations does not.

**12. `difficulty_and_cost`**
Difficulty **3/5** computationally but **4/5** in statistical judgement. Cost ≈ **¥0–3,000** (storage; possibly a cheap cloud VM for bulk downloads). APC ¥0–20,000 depending on venue. **Runs on a laptop** provided downloads are per-protein and per-locus; budget ~200–500 GB of disk if auditing ~50–100 proteins across two platforms and four outcome GWAS.

**13. `timeline_months`**
Months 1–2 systematic identification and extraction; months 2–5 re-instrumentation and the four stress tests; month 6 sensitivity/robustness checks and repository; months 6–8 writing and submission. **Realistically completable in 8 months.** This is the most schedule-reliable of the three strongest options.

**14. `target_journal_tier`**
Tier: good specialty / methodological. Realistic: *HGG Advances* (the Tambets paper's own home — a strong fit); *Genetic Epidemiology*; *Alzheimer's Research & Therapy*; *BMC Medical Research Methodology*. Stretch: *International Journal of Epidemiology*, *European Journal of Epidemiology*. **Honest warnings:** PLOS One has run editorial screening of MR submissions since late 2023 with a high rejection rate; PLOS Genetics' 2025 policy says poorly performed MR papers are "almost invariably rejected during editorial review" and *strongly encourages biological validation* — so pitch this as meta-research/adjudication, never as "an MR study." A Frontiers in Endocrinology editorial has already labelled open-database MR studies "derivative."

**15. `reviewer_attacks`**
1. **"Your re-analysis is itself an MR, and inherits the same assumptions."** Correct and unavoidable. Pre-empt it: the claim is relative (concordance across specifications), not absolute (which protein is causal). Never write "we confirm X is causal."
2. **"Colocalization is not a validation step."** Tambets 2024 is the weapon here and it cuts both ways; your tiering must be presented as a ranking of robustness, not of truth, and you must report the ~45–50% precision ceiling for coloc-based prioritization.
3. **"Discordance between platforms reflects biology (different epitopes, different isoforms, different proteoforms), not error."** This is the strongest objection. You must engage it, including the Eldjarn Author Correction which reversed the original platform-precision claim — a reviewer who knows the field will check whether you cited the corrected version.
4. (Additional, often fatal) **"Sample overlap between pQTL and GWAS cohorts inflates your statistics,"** since UKB-PPP participants are UK Biobank participants and Bellenguez/Wightman both include UK Biobank. Quantify or stratify; do not ignore.

**16. `prelim_ratings`**
Novelty **M–H** (the design is novel; the ingredients are not) · Evidence-base **H** · Overlap-risk **M** (an audit like this is an obvious move for a methods group; publish fast and pre-register early to establish priority).

---

# TOPIC 3

**1. `title_en`**
Differentiation state determines the death mechanism in the HT-22 glutamate model: a literature audit and a controlled head-to-head re-test of oxytosis versus NMDA-receptor-mediated excitotoxicity.

**2. `core_question`**
In the same laboratory, same passage and same assay, does HT-22 differentiation state switch glutamate-induced death from a ferroptosis-inhibitor-sensitive, NMDA-antagonist-insensitive mechanism to an MK-801/memantine-sensitive one — and what fraction of the published HT-22/glutamate literature reports the differentiation state and pharmacological controls needed to know which mechanism it studied?

**3. `hypothesis`**
Undifferentiated HT-22 glutamate death is rescued by ferrostatin-1/liproxstatin-1 but not by MK-801 or memantine; differentiated HT-22 acquire an additional NMDA-antagonist-sensitive component; and a large majority of published HT-22/glutamate papers do not report differentiation state or include the pharmacological control that would discriminate the two, with a measurable subset explicitly mislabelling the mechanism as "excitotoxicity."

**4. `novelty_claim`**
New: the discrepancy itself is in the literature but has never been adjudicated, and no one has quantified how often the HT-22/glutamate model is used without the methodological information needed to interpret it. Avoids every trap on your list: it is not a signature paper, not an MR, not a database-mining paper, and the novelty is not "a new gene" but a correction to how a widely used model is reported. The hypothesis is pre-specified and symmetric — both outcomes change practice.

**5. `state_of_the_art`**
The canonical position, traceable to Maher & Davis (1996, cited inside later papers), is that HT-22 cells "do not express active ionotropic glutamate receptors and are not subject to excitotoxicity," so glutamate kills by blocking cystine import through system xc−, depleting glutathione, inhibiting GPX4 and activating 12/15-lipoxygenase, with calcium entry downstream of ROS rather than upstream — the "oxytosis" pathway (Maher's Cell Chemical Biology review; "From Oxytosis to Ferroptosis" review). Ferrostatin-1 protects HT-22 from this oxidative toxicity (Neural Regeneration Research 2020). **Against this**, a 2013 Neural Regeneration Research paper states that "it has almost become consensus that HT22 cells do not possess excitatory properties because of the lack of NMDA receptors," then reports that *differentiated* HT-22 express NMDA receptors and die by NMDA-mediated excitotoxicity blocked by MK-801 and memantine, while undifferentiated cells die by oxidative stress — concluding that "it still remains unclear if HT22 cells are resistant to excitotoxicity because they do not express NMDA receptors." A companion study reports NMDA-receptor induction on differentiation mediating homocysteine cytotoxicity, and differentiated HT-22 are now also promoted as a screening model in their own right.

**6. `specific_open_problem`**
Two mutually exclusive mechanistic accounts of the same model coexist, separated by a variable (differentiation) that most papers do not report. Nobody has run the discriminating experiment with both pharmacological arms side by side and modern ferroptosis readouts, and nobody has audited the literature for whether its mechanistic labels are supportable. Meanwhile a 2022 Brain Sciences systematic review of glutamate neurotoxicity (4,060 records screened, 71 included, 23 in vitro) found that risk-of-bias problems were concentrated in poor reporting of blinding, randomization and allocation concealment — i.e. the reporting-quality problem in this literature is already documented at the review level but has never been pinned to this specific, consequential methodological variable.

**7. `delta_vs_closest_paper`**
Closest real paper: **"Differentiation renders susceptibility to excitotoxicity in HT22 neurons," Neural Regeneration Research 8(14), 2013.** Delta: (a) they showed differentiated cells are MK-801/memantine-sensitive; they did not test ferroptosis inhibitors, did not measure GSH/MDA/GPX4/xCT, and did not quantify how the field reports differentiation state; (b) the student adds the ferroptosis arm (ferrostatin-1, liproxstatin-1, ACSL4/GPX4/xCT Western blots) and the orthogonal stressors (erastin, RSL3) that let you say *which* pathway each state uses, not merely which drug blocks it; (c) the student adds a systematic reporting audit, converting a single-lab discrepancy into a field-level methodological finding with a reporting checklist as the deliverable.

**8. `references`**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | (authors not captured) | Differentiation renders susceptibility to excitotoxicity in HT22 neurons | Neural Regeneration Research 8(14) | 2013 | DOI 10.3969/j.issn.1673-5374.2013.14.006 | SEARCH_SNIPPET |
| 2 | Maher P & Davis JB | (cited within later papers as the source of "HT22 do not express active ionotropic glutamate receptors and are not subject to excitotoxicity") | — | 1996 | no PMID/DOI captured — **needs verification** | UNVERIFIED (citation seen only inside another paper's text) |
| 3 | Maher P, et al. | Using the oxytosis/ferroptosis pathway to understand and treat age-associated neurodegenerative diseases | Cell Chemical Biology | 2020 | PMC7749085; article ID S2451-9456(20)30426-8 | SEARCH_SNIPPET |
| 4 | (authors not captured) | From oxytosis to ferroptosis: 10 years of research on oxidative cell death | — | ~2023 | PMC10620435 | SEARCH_SNIPPET |
| 5 | (authors not captured) | Ferrostatin-1 protects HT-22 cells from oxidative toxicity | Neural Regeneration Research 15(3) | 2020 | DOI/PMID not captured — needs verification | TITLE_ONLY |
| 6 | (authors not captured) | Differentiation of HT22 neurons induces expression of NMDA receptor that mediates homocysteine cytotoxicity | — | ~2011 | not captured — needs verification | TITLE_ONLY |
| 7 | AL-Nasser MN, Mellor IR, Carter WG | Is L-glutamate toxic to neurons and thereby contributes to neuronal loss and neurodegeneration? A systematic review | Brain Sciences | 2022 | PMC9139234 | SEARCH_SNIPPET |
| 8 | (authors not captured) | The role of Ca2+ in cell death caused by oxidative glutamate toxicity and ferroptosis | — | 2017 | PMID 28545724 | SEARCH_SNIPPET |
| 9 | (authors not captured) | Differentiated HT22 cells as a novel model for in vitro screening of serotonin reuptake inhibitors | — | ~2023 | PMC9871236 | SEARCH_SNIPPET |
| 10 | (authors not captured) | The application of approaches in detecting ferroptosis | Heliyon 10:e23507 | 2024 | article S2405-8440(23)10715-8 | SEARCH_SNIPPET |
| 11 | (authors not captured) | Cellular protection using Flt3 and PI3Kα inhibitors demonstrates multiple mechanisms of oxidative glutamate toxicity | Nature Communications | 2014 | DOI 10.1038/ncomms4672 | SEARCH_SNIPPET |

**9. `models_and_data`**
- **Cells in hand:** HT-22, described as a subclone of the HT-4 line immortalized with a temperature-sensitive SV40 T antigen, derived from mouse hippocampus (Morimoto and Koshland, 1990, cited on vendor data sheets — **UNVERIFIED, needs checking**). Note: HT-22 is sold by several vendors (Sigma-Aldrich SCC129, Cytion, AcceGen, AMSBIO) and a Sigma data sheet states only species verification (mouse origin; negative for rat and Chinese hamster), **not** identity against a reference profile. My searches found **no** ICLAC misidentification entry and no Cellosaurus record I can quote. Because differentiation protocols and passage history vary between labs, the paper must report vendor, lot, passage range, STR/species status and the exact differentiation protocol — that reporting discipline is part of the contribution.
- **Literature corpus for the audit:** PubMed/Europe PMC search for HT-22 + glutamate. **I could not query PubMed in this session**, so the corpus size is unknown; the student should expect several hundred papers and should pre-specify a sampling frame (e.g. all papers in a defined window, or a random sample of 150 with a documented seed).
- No public omics data are strictly required. If the student wants a transcriptomic layer, a glutamate-treated HT-22 RNA-seq study exists (*Scientific Reports* 2023, DOI 10.1038/s41598-023-34183-y) but **no accession appeared in my results — accession to be identified by the student in GEO.**

**10. `key_experiments`**
*Computational / meta-research (laptop, free):*
1. Pre-registered systematic audit (OSF) with explicit inclusion criteria and a published extraction form. Extract per paper: differentiation state reported (yes/no/what protocol), glutamate concentration and exposure time, mechanistic label used in title/abstract ("excitotoxicity" / "oxidative" / "ferroptosis" / unspecified), pharmacological controls present (NMDA antagonist? ferroptosis inhibitor? antioxidant?), viability assay, replication structure. Two independent extractors on a 20% subsample with a reported kappa — this is cheap and makes the audit credible.
2. Analysis in R (`tidyverse`, `meta`/`metafor` only if effect sizes are extractable — more likely report descriptive proportions with Wilson CIs). Deliverable: an HT-22 reporting checklist.

*Wet lab (entirely within the student's techniques):*
3. Two arms: undifferentiated and differentiated HT-22, differentiated by the protocol specified in the 2013 NRR paper (student must read it; **I could not retrieve the protocol details**).
4. Full glutamate dose–response in both arms (CCK-8/MTT), with EC50 and 95% CI, ≥3 independent biological replicates on separate days, blinded plate reading where possible.
5. Pharmacological dissection, factorial: ± MK-801, ± memantine, ± ferrostatin-1, ± liproxstatin-1, ± N-acetylcysteine. Each inhibitor validated with a positive control (ferrostatin-1 vs RSL3; MK-801 vs an NMDA-responsive comparator if one is available — if not, state the limitation).
6. Mechanism readouts on a plate reader: GSH/GSSG, TBARS/MDA, Fe2+; Western blot for GPX4, SLC7A11/xCT, ACSL4, and NMDA-receptor subunits (GRIN1/GluN1, GRIN2B) to test whether differentiation actually induces receptor protein. qPCR for the same.
7. Orthogonal stressors in both arms: erastin (xCT), RSL3 (GPX4), H2O2 (non-ferroptotic). If the differentiated arm is NMDA-sensitive, its erastin/RSL3 EC50 should be unchanged — that is the discriminating prediction.
- **Gating:** flow cytometry not required (plate-reader MDA/GSH plus C11-BODIPY on a fluorescence plate reader; the Heliyon review recommends pairing C11-BODIPY with MDA). Electrophysiology would be the definitive receptor-function test and is **not available** — this is a real limitation: the student can show receptor *protein* but not receptor *current*, and must say so. Calcium imaging would help and needs only a plate reader with Fluo-4 (optional, cheap).

**11. `expected_and_negative_results`**
Three informative outcomes, all publishable: (a) differentiation switches the mechanism → resolves the discrepancy and the audit shows the field has been conflating two models; (b) differentiation does *not* switch the mechanism → refutes the 2013 report, which is a clean confirmatory-failure paper with direct practical consequences; (c) both mechanisms coexist in both states → the model is less clean than either camp claims, which is itself worth reporting. eNeuro's "Negative Results" and "Confirmation" article types exist precisely for (b), with the stated requirement of multiple experimental approaches and rigorous positive and negative controls — design to that bar from the start.

**12. `difficulty_and_cost`**
Difficulty **2–3/5** — the lowest-risk topic here and the best match to the student's actual assets. Estimated **¥15,000–30,000**: MK-801 and memantine are inexpensive (~¥500–1,500 each); ferrostatin-1 ~¥1,000–2,500; liproxstatin-1 and RSL3 are the costly items (~¥2,000–5,000 each); erastin ~¥1,000–2,000; antibody panel (GPX4, xCT, ACSL4, GluN1, GluN2B, loading control) ¥12,000–24,000 — again the dominant cost, and the NMDA-subunit antibodies are the ones most likely to disappoint, so buy from a supplier with published HT-22 or mouse-brain validation; kits ¥1,500–4,500; CCK-8 and consumables ¥3,000–5,000. The audit costs ¥0. **Fully laptop-feasible on the computational side.**

**13. `timeline_months`**
Audit: months 1–3 (can run in parallel with cell culture setup). Differentiation protocol establishment: months 2–4 (budget real time here — this is the main technical risk). Main factorial experiments: months 4–8. Writing/submission: months 8–10. **Comfortably achievable in 10 months.**

**14. `target_journal_tier`**
Tier: solid specialty / methods. Realistic: *eNeuro* (explicitly accepts Confirmation and Negative Results); *Journal of Neuroscience Methods*; *Neurochemistry International*; *Free Radical Biology and Medicine*; *ALTEX* or *Toxicology in Vitro* if framed as a model-validation paper. *Neural Regeneration Research* is a natural home given both prior papers appeared there, which is both an advantage (editorial familiarity) and a conflict-of-narrative risk. No acceptance promises.

**15. `reviewer_attacks`**
1. **"Your audit is a reporting-quality survey, not science, and your sample is arbitrary."** Pre-register the sampling frame, report inter-rater agreement, and lead with the experiment rather than the audit.
2. **"You showed receptor protein by Western blot but not functional NMDA receptors — your 'excitotoxicity' arm is unproven."** This is the strongest attack and you cannot fully answer it without electrophysiology or calcium imaging. Add Fluo-4 calcium measurement (cheap, plate reader) and state the limitation explicitly; do not claim functional receptors from a blot.
3. **"One lab, one cell stock, one differentiation protocol — the discrepancy might be clonal drift, not differentiation."** Partly mitigable by reporting passage, vendor and lot, and by testing two independently sourced HT-22 stocks if obtainable. Flag as a limitation.
4. (Commonly fatal in this literature) **"Your glutamate concentrations and timepoints are not matched between arms, so you compared different insult severities."** Match on fraction-of-maximal-effect, not on millimolar concentration, and pre-specify that.

**16. `prelim_ratings`**
Novelty **M** · Evidence-base **H** · Overlap-risk **L** (nobody is racing to do this; it is unglamorous and therefore safe).

---

# TOPIC 4

**1. `title_en`**
Does transcriptomic signature reversal actually predict neuroprotection? A pre-registered calibration test of LINCS-nominated compounds in a hippocampal neuronal oxidative-stress model.

**2. `core_question`**
Across a pre-registered set of compounds spanning the full range of connectivity scores against an excitatory-neuron Alzheimer's expression signature, does the connectivity score predict the magnitude of protection in glutamate- and erastin-challenged HT-22 cells?

**3. `hypothesis`**
Connectivity score will show weak-to-null rank correlation with measured protection; strong reversers will not protect at a higher rate than connectivity-neutral compounds matched on chemical class and solubility. (The honest prior is that the method is poorly calibrated.)

**4. `novelty_claim`**
New: the design tests the *method*, not a compound. Almost every signature-reversal repurposing paper tests only its top hits and reports the winners — a design that cannot estimate the method's predictive value. Including connectivity-neutral and anti-correlated controls, and pre-registering the primary endpoint as a rank correlation rather than "compound X protects," converts a drug-discovery fishing trip into a calibration study. This directly avoids the trap of "we nominated 5 compounds and one worked," which is unpublishable as novelty and uninterpretable as evidence.

**5. `state_of_the_art`**
Signature reversal is well established as a method, with L1000CDS2 providing a search engine over characteristic-direction LINCS L1000 signatures, and connectivity scores running from −1 (complete reversal) to +1. The flagship AD application is Taubes et al. (Nature Aging 2021): APOE4-specific signatures from 213 brain tissue samples were queried against >1,300 FDA-approved drugs, nominating bumetanide, which was then validated in APOE4/4 human neurons, APOE4 knock-in mice, and two EHR databases covering >5 million people. Methodologically, connectivity scores from CMap 1.0 are reported to be enriched at zero and to correlate poorly with IC50, and an oncology validation study established the "test top candidates in cell lines" workflow. Expert reaction to bumetanide was mixed: NIA's Jean Yuan considered it trial-worthy; Jeffrey Cummings was unconvinced.

**6. `specific_open_problem`**
No study I found estimates the *calibration* of signature reversal for neuroprotection — i.e. the relationship between connectivity score and measured effect across the score range, with negative controls. The field reports hit rates among top-ranked compounds only, which is a selected sample. My searches also found no systematic review of experimental validation rates for LINCS-based AD predictions.

**7. `delta_vs_closest_paper`**
Closest real paper: **Taubes et al., Nature Aging 2021, DOI 10.1038/s43587-021-00122-7.** Delta: (a) they used a bulk, APOE4-stratified brain signature; the student uses a cell-type-resolved excitatory-neuron signature from SEA-AD, which matches the test system's cell type; (b) they tested their top hit; the student tests a stratified sample across the score range including connectivity-neutral controls; (c) their endpoint was "does bumetanide work"; the student's pre-registered endpoint is "does the score predict." Their resources (iPSC neurons, APOE4-KI mice, 5M-patient EHR) are unavailable to this student, which is precisely why competing on compound discovery would be hopeless and competing on method calibration is viable. Note an Author Correction to the Taubes paper exists; cite the corrected version.

**8. `references`**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | Taubes A, et al. | Experimental and real-world evidence supporting the computational repurposing of bumetanide for APOE4-related Alzheimer's disease | Nature Aging 1:932–947 (+ Author Correction) | 2021 | DOI 10.1038/s43587-021-00122-7 | SEARCH_SNIPPET |
| 2 | Gabitto MI, et al. | Integrated multimodal cell atlas of Alzheimer's disease (SEA-AD) | Nature Neuroscience | 2024 | DOI 10.1038/s41593-024-01774-5 | SEARCH_SNIPPET |
| 3 | (authors not captured) | Reconciling multiple connectivity scores for drug repurposing | Briefings in Bioinformatics 22(6):bbab161 | 2021 | DOI not captured — needs verification | SEARCH_SNIPPET |
| 4 | (authors not captured) | Validation of transcriptome signature reversion for drug repurposing in oncology | — | 2023 | PMC9851289 | SEARCH_SNIPPET |
| 5 | (authors not captured) | Transcriptomic analysis of glutamate-induced HT22 neurotoxicity as a model for screening anti-Alzheimer's drugs | Scientific Reports | 2023 | DOI 10.1038/s41598-023-34183-y | SEARCH_SNIPPET |
| 6 | Maher P, et al. | Using the oxytosis/ferroptosis pathway to understand and treat age-associated neurodegenerative diseases | Cell Chemical Biology | 2020 | PMC7749085 | SEARCH_SNIPPET |
| 7 | (authors not captured) | The application of approaches in detecting ferroptosis | Heliyon 10:e23507 | 2024 | S2405-8440(23)10715-8 | SEARCH_SNIPPET |

**9. `models_and_data`**
- **Disease signature:** SEA-AD processed snRNA-seq, open on the AWS Open Data Registry (bucket **sea-ad-single-cell-profiling**); as of June 2026, processed snRNA-seq with cell-type assignments from eleven brain regions is downloadable. Use the AWS copy, not CELLxGENE's reduced version.
- **LINCS L1000 / CMap:** signatures are distributed through clue.io and LINCS resources, and L1000CDS2 provides a query engine. **I did not verify current access terms, registration requirements or GEO accessions for L1000 in this session — the student must check, and no accession is given here.**
- **Compounds:** must be purchasable in China and soluble in DMSO at usable concentrations. Pre-screen for this *before* pre-registering the compound list, or the design will collapse on procurement.
- **Model:** HT-22 with glutamate and erastin. Note the honest mismatch: a mouse immortalized line is not an excitatory cortical neuron, so a reversal signature derived from human excitatory neurons is being tested in a system that does not express that signature. This must be stated as the central limitation, and ideally the student should verify by qPCR that a handful of signature genes behave as expected in HT-22 under stress.

**10. `key_experiments`**
*Computational:*
1. Pseudobulk differential expression within excitatory-neuron subtypes (SEA-AD) using `DESeq2` or `limma`-voom on pseudobulk counts (preferred over single-cell DE, which inflates false positives); `Seurat`/`anndata` for handling. Pathway context with `clusterProfiler`/`fgsea`.
2. Characteristic-direction signature; query LINCS; compute connectivity scores; stratify compounds into score bins (strong reverser / neutral / mimicker).
3. Pre-register (OSF) before any compound purchase: the compound list with its bin assignment, the primary endpoint (Spearman rho between connectivity score and maximal protection), the sample size, and the analysis plan. **This pre-registration is the paper's main methodological asset.**

*Wet lab:*
4. 8–12 compounds, blinded to bin by a colleague where possible, tested over 5-point dose–response in glutamate-challenged HT-22 (CCK-8), ≥3 independent replicates; the same panel in erastin-challenged cells; H2O2 as a non-ferroptotic specificity arm.
5. For any compound that protects: mechanism follow-up with MDA/GSH, Western blot for GPX4/xCT/ACSL4, and qPCR for a small panel of signature genes to test whether the compound actually reverses the signature in this system (this is the step that distinguishes a real result from a nonspecific antioxidant).
6. Cytotoxicity-only control: confirm apparent "protection" is not assay interference — CCK-8/MTT are reduction-based and many antioxidants and polyphenols interfere directly. **Run a cell-free absorbance control for every compound.** Reviewers kill papers on this.
- **Gating:** no flow, no confocal, no lentivirus required. A plate reader is essential. A second, non-metabolic viability readout (LDH release, or crystal violet) is strongly advised and is cheap — treat as near-mandatory.

**11. `expected_and_negative_results`**
The most likely outcome — **null or weak correlation** — is the publishable result, and it is the reason to do the study. This only works if the paper is framed, written and (ideally) registered as a calibration study from the outset. If framed as drug discovery, a null result is unpublishable. Be clear-eyed: some reviewers and editors will still read a null calibration study as a failed screen. This is the topic with the widest spread between "well-received" and "desk-rejected."

**12. `difficulty_and_cost`**
Difficulty **3–4/5**. Estimated **¥20,000–45,000**: 8–12 compounds at ¥500–3,000 each (¥6,000–25,000); CCK-8 plus a second viability assay ¥3,000–6,000; kits ¥1,500–4,500; antibodies ¥6,000–15,000 if mechanism follow-up is needed; consumables ¥3,000–5,000. Compute: SEA-AD pseudobulk needs more than a typical laptop for the full object — subset to excitatory neurons on a server or work from pre-computed pseudobulk if available; the LINCS query and all statistics run on a laptop.

**13. `timeline_months`**
Months 1–3 signature derivation, LINCS query, pre-registration, procurement; months 3–8 dose–response panels; months 8–10 mechanism follow-up on any hits; months 10–13 writing. **Realistically 13 months**, i.e. at the outer edge of the window.

**14. `target_journal_tier`**
Tier: specialty / methodological. Realistic: *Briefings in Bioinformatics* (if the calibration framing is strong); *SLAS Discovery*; *Journal of Neurochemistry*; *Frontiers in Pharmacology* (lower prestige, faster). *Nature Aging* and similar are out of reach. Honest note: a null calibration study is harder to place than a positive screen, and APCs at the plausible venues are substantial.

**15. `reviewer_attacks`**
1. **"Your test system does not express the signature you reversed."** The deepest objection; partly answerable with the qPCR signature-gene check, never fully.
2. **"Your negative-control compounds are not matched on anything that matters (lipophilicity, radical-trapping capacity, generic cytotoxicity), so your 'calibration' is confounded."** Matching strategy must be pre-specified and defended; this is where the design lives or dies.
3. **"CCK-8 interference."** Guaranteed to be raised. The cell-free control and a second non-metabolic readout are non-negotiable.
4. **"n = 8–12 compounds gives you no power to estimate a correlation."** Compute and report the detectable effect size honestly; consider framing as an estimate with a wide CI rather than a hypothesis test.

**16. `prelim_ratings`**
Novelty **M–H** (the framing is the novelty) · Evidence-base **M** · Overlap-risk **L**.

---

# TOPIC 5

**1. `title_en`**
Is FSP1 required for vitamin K–mediated protection of hippocampal neurons? A discriminating test of the non-canonical vitamin K cycle in oxidative glutamate toxicity.

**2. `core_question`**
Does siRNA knockdown of Aifm2/FSP1 abolish menaquinone-4 protection of HT-22 cells against glutamate- and erastin-induced death, as the FSP1-dependent non-canonical vitamin K cycle predicts, or does protection persist, indicating FSP1-independent radical trapping in neurons?

**3. `hypothesis`**
If vitamin K protection in neurons is FSP1-dependent, Aifm2 knockdown will shift the MK-4 protection curve rightward and reduce maximal protection against all ferroptotic stressors; if MK-4 acts largely as a direct lipophilic radical-trapping antioxidant at the concentrations used in neuronal models, protection will be largely preserved. The two outcomes are mutually exclusive on the primary endpoint.

**4. `novelty_claim`**
New: a direct loss-of-function test, in a neuronal system, of a mechanistic claim established in non-neuronal cells. The reported neuronal result (MK-4 protects HT-22 against sulfasalazine, glutamate and FIN56, described as inducing ferroptosis "via mechanisms distinct from RSL3") is *suggestive* of a stressor-independent, possibly FSP1-independent mechanism, but the requirement test was not run. This avoids the fake-novelty trap of "compound X protects HT-22 cells," of which there are hundreds, because the claim is about a *requirement*, not a protection, and the experiment can come out either way.

**5. `state_of_the_art`**
Mishima et al. (Nature 2022) established that fully reduced vitamin K (hydroquinone) is a potent lipophilic antioxidant that blocks lipid peroxidation and ferroptosis, and that FSP1 is the long-sought warfarin-resistant vitamin K reductase, resolving a question open for over half a century; vitamin K inhibited ferroptosis at lower concentrations than vitamin E. A subsequent neuronal study reports MK-4 protection in HT-22 against several ferroptosis inducers including ones acting by mechanisms distinct from RSL3. FSP1 biology continues to develop, including a 2025 report of FSP1-mediated lipid-droplet quality control preventing neutral lipid peroxidation. Separately, ferroptosis is known to be heterogeneous: an ALOX5-mediated, ACSL4-independent route has been described in Huntington's disease models, and ACSL4 is described as necessary for lipid peroxidation downstream of POR and ALOX, with ACSL4 inhibition alleviating RSL3-induced oxidative stress in HT-22 (reported in a 2026 Frontiers in Pharmacology paper whose primary focus is diabetic/depressive models, so its HT-22 data are indirect).

**6. `specific_open_problem`**
Whether the FSP1–vitamin K axis is the operative mechanism of vitamin K neuroprotection has not been tested by FSP1 loss of function in neurons. This matters practically: vitamin K is cheap, oral and widely available, and "vitamin K protects neurons" claims are accumulating without a mechanism test.

**7. `delta_vs_closest_paper`**
Closest real papers: **Mishima et al., Nature 2022 (DOI 10.1038/s41586-022-05022-3)** — established the FSP1 requirement, but not in neurons and not with these stressors; and **"Vitamin K suppression of ferroptosis in neuronal model systems" (PMC12725873)** — showed protection in HT-22 across stressors but, per the available snippet, did not perform FSP1 loss of function. Delta: the student supplies exactly the missing factorial (±Aifm2 siRNA × ±MK-4 × stressor identity). **Caveat the committee must note: I could not read the full text of PMC12725873, so there is a real possibility it already contains an FSP1 knockdown arm. The student must verify this before committing — this is the single highest-priority verification step for this topic, and if the arm is present, this topic dies.**

**8. `references`**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | Mishima E, et al. | A non-canonical vitamin K cycle is a potent ferroptosis suppressor | Nature 608:778–783 | 2022 | DOI 10.1038/s41586-022-05022-3 | SEARCH_SNIPPET |
| 2 | (authors not captured) | Vitamin K suppression of ferroptosis in neuronal model systems | — | ~2025/2026 | PMC12725873 | SEARCH_SNIPPET |
| 3 | (authors not captured) | FSP1-mediated lipid droplet quality control prevents neutral lipid peroxidation and ferroptosis | — | 2025 | PMID 41162632 | SEARCH_SNIPPET |
| 4 | (authors not captured) | ALOX5-mediated ferroptosis acts as a distinct cell death pathway upon oxidative stress in Huntington's disease | Genes & Development 37(5–6):204 | 2023 | DOI not captured — needs verification | SEARCH_SNIPPET |
| 5 | Maher P, et al. | Using the oxytosis/ferroptosis pathway to understand and treat age-associated neurodegenerative diseases | Cell Chemical Biology | 2020 | PMC7749085 | SEARCH_SNIPPET |
| 6 | (authors not captured) | From oxytosis to ferroptosis: 10 years of research on oxidative cell death | — | ~2023 | PMC10620435 | SEARCH_SNIPPET |
| 7 | (authors not captured) | Ferrostatin-1 protects HT-22 cells from oxidative toxicity | Neural Regeneration Research 15(3) | 2020 | not captured — needs verification | TITLE_ONLY |
| 8 | (authors not captured) | The application of approaches in detecting ferroptosis | Heliyon 10:e23507 | 2024 | S2405-8440(23)10715-8 | SEARCH_SNIPPET |
| 9 | (authors not captured) | Cofilin1 oxidation links oxidative distress to mitochondrial demise and neuronal cell death | Cell Death & Disease | 2021 | DOI 10.1038/s41419-021-04242-1 | SEARCH_SNIPPET |

**9. `models_and_data`**
- HT-22 in hand. MK-4 (menaquinone-4) and phylloquinone are inexpensive and readily available; warfarin is a useful orthogonal tool (FSP1-mediated reduction is warfarin-resistant, so warfarin should *not* abolish MK-4 protection if FSP1 is the reductase — a cheap, strong internal control).
- siRNA against mouse *Aifm2*, three duplexes plus NC.
- Public data (small, supporting role only): AIFM2/FSP1 and GPX4 expression across human brain cell types from SEA-AD (open, AWS) to argue neuronal relevance; DepMap co-essentiality to nominate one additional partner gene to knock down (**note: my search did not find a published DepMap co-essentiality analysis of ferroptosis regulators, and co-essentiality is framed in a Nature Reviews MCB 2023 tools article as a pathway-grouping method — treat this as exploratory, and remember HT-22 is mouse and not in DepMap**).
- No credentialing, no patient samples, no animals required.

**10. `key_experiments`**
1. Confirm Aifm2 expression in HT-22 (qPCR, Western blot) — **do this first; if FSP1 is not expressed, the topic ends here.**
2. Establish MK-4 protection curves against glutamate, erastin, RSL3 and FIN56 (if affordable) in wild-type HT-22; ferrostatin-1 as positive control, H2O2 as specificity arm.
3. Primary experiment: 2 × 2 × stressor factorial — Aifm2 siRNA vs NC siRNA × MK-4 vs vehicle × each stressor. Primary endpoint: change in MK-4 EC50 and maximal protection on Aifm2 knockdown, pre-specified. Three independent biological replicates minimum; knockdown confirmed by qPCR and Western blot in every experiment.
4. Orthogonal pharmacology: MK-4 ± warfarin (prediction: no loss of protection, since FSP1-mediated reduction is warfarin-resistant); vitamin E or ferrostatin-1 as FSP1-independent comparators (prediction: protection unaffected by Aifm2 knockdown).
5. Mechanism readouts: TBARS/MDA, GSH/GSSG, Fe2+, C11-BODIPY on a plate reader; Western blot for GPX4, xCT, ACSL4, FSP1.
6. Optional stretch (**gated**): overexpression rescue with an Aifm2 construct, requiring plasmid purchase and transfection optimization — strengthens the paper considerably if achievable.
- **Gating:** flow cytometry not needed (plate-reader substitutes as above). Co-IP, mass spec, Seahorse not needed. Lentivirus/CRISPR not needed. This topic is the best-matched to the student's exact toolkit.

**11. `expected_and_negative_results`**
Both outcomes are publishable and interesting: FSP1-dependence extends a Nature finding into neurons; FSP1-independence says vitamin K's neuronal effect is direct radical trapping, which has clear implications for dose and for the many "vitamin K is neuroprotective" claims. The risk is not the direction of the result — it is a *partial* result (modest, noisy shift), which is the most likely outcome and the hardest to publish. Mitigate with adequate replication and pre-specified effect-size thresholds.

**12. `difficulty_and_cost`**
Difficulty **2–3/5** — technically the most tractable, scientifically the narrowest. Estimated **¥20,000–35,000**: siRNA ¥1,500–3,000; transfection reagent ¥2,000–3,500; MK-4 and warfarin ¥500–1,500; FSP1/AIFM2, GPX4, xCT, ACSL4 antibodies ¥10,000–20,000; RSL3/erastin/FIN56/ferrostatin-1 ¥5,000–12,000 (FIN56 and RSL3 are the expensive ones — drop FIN56 if the budget is tight); kits and consumables ¥4,000–8,000. Computation is trivial and laptop-only.

**13. `timeline_months`**
Months 1–2 expression confirmation and siRNA optimization; months 2–3 MK-4 protection curves; months 3–7 factorial experiments; months 7–9 writing. **Achievable in 9 months.** The fastest route to a finished paper.

**14. `target_journal_tier`**
Tier: solid specialty. Realistic: *Free Radical Biology and Medicine*; *Neurochemistry International*; *Cell Death Discovery*; *Biochemical and Biophysical Research Communications* (low tier but fast). *Redox Biology* is a genuine stretch and would require the overexpression rescue. No promises.

**15. `reviewer_attacks`**
1. **"MK-4 concentrations are supraphysiological, so FSP1-independence is a concentration artefact."** Must run a full concentration range and discuss achievable brain concentrations honestly.
2. **"Partial siRNA knockdown cannot establish a requirement."** Report knockdown efficiency at protein level in every experiment; if efficiency is below ~70%, the negative result is uninterpretable. This is the main technical risk.
3. **"One immortalized mouse line; FSP1 dependence is known to be cell-type- and lipid-context-dependent, and a 2025 paper ties FSP1 to lipid-droplet biology."** Cannot be fully answered; acknowledge and limit the claim to this model.

**16. `prelim_ratings`**
Novelty **M** · Evidence-base **H** · Overlap-risk **H** — ferroptosis/FSP1 is a crowded, fast-moving field with well-funded labs; a six-month delay could see this scooped, and the possibility that PMC12725873 already contains the knockdown arm must be checked first.

---

# TOPIC 6

**1. `title_en`**
Do published "hub genes" replicate? A matched-null replication audit of GEO-derived hub-gene signatures in a single neurological disease.

**2. `core_question`**
In independent GEO datasets for the same disease, do hub genes nominated by published bioinformatics re-analyses replicate in direction and significance more often than expression- and variance-matched random gene sets drawn from the same data?

**3. `hypothesis`**
Published hub-gene lists will show low cross-paper overlap and will not replicate meaningfully better than matched random gene sets, because standard hub-gene pipelines select genes on properties (high expression, high variance, high connectivity) that make them appear "significant" in any dataset.

**4. `novelty_claim`**
New: the **matched-null comparison**. Existing criticism of hub-gene papers is editorial and rhetorical; it has not been quantified against the only null that matters. Papers that "validate" hub genes in a second GEO dataset almost never ask whether random genes matched on expression and variance would validate equally well — and if they would, the entire genre produces no information. The deliverable is a replication rate, a quantified null, and a minimal protocol. This avoids the hub-gene trap by *being about* the hub-gene trap.

**5. `state_of_the_art`**
The genre is enormous and formulaic: LASSO-Cox or WGCNA-derived gene selection, a nomogram, and "validation" in a second public cohort, with authors themselves conceding that data were only derived from publicly available datasets and that accuracy should be further assessed in clinical samples. Documented parallels in adjacent literatures: Suchak et al. (PLoS Biol 2025) identified 341 formulaic single-factor NHANES papers, rising from roughly 4/year in 2014–2021 to 190 in 2024 alone, with failure to account for multifactorial relationships and false-discovery risk, and selective extraction of data; a companion PLOS Biology Primer by Byrne and Stender proposes practical detection steps; *Science* reported that 92% of post-2021 NHANES papers had a first author at a Chinese institution versus 8% before 2021, and that Springer Nature has retracted a number of NHANES papers. On the reanalysis-feasibility side, a 2026 bioRxiv audit of 3,631 bulk Illumina GEO series with at least 25 samples concluded that uniform reanalysis is unavailable for most published human disease RNA-seq, and that usable coverage rather than raw-read deposition is the main constraint — with a companion Zenodo deposit noting that 24 series an Entrez query could not resolve are contradicted by the primary GEO record and 39 records carry no "Raw data" status line at all, i.e. a single programmatic lookup is not reliable evidence that data are missing.

**6. `specific_open_problem`**
Nobody has measured the information content of the hub-gene genre. The 2026 GEO audit measured *reprocessability*; it did not measure whether published results replicate. Editorials assert the genre is worthless; no one has shown it.

**7. `delta_vs_closest_paper`**
Closest real papers: **Suchak et al., PLoS Biol 2025 (DOI 10.1371/journal.pbio.3003152)** — quantified the *volume and design flaws* of a formulaic genre but did not attempt replication; and the **2026 bioRxiv GEO reprocessability audit** — quantified whether data *can* be reanalyzed but not whether findings hold. Delta: the student actually re-runs the analyses and compares against a matched null, producing a replication rate rather than a count of papers or a data-availability statistic.

**8. `references`**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | Suchak T, Aliu AE, Harrison C, Zwiggelaar R, Geifman N, Spick M | Explosion of formulaic research articles, including inappropriate study designs and false discoveries, based on the NHANES US national health database | PLoS Biology 23(5):e3003152 | 2025 | PMID 40338847; DOI 10.1371/journal.pbio.3003152 | SEARCH_SNIPPET |
| 2 | Byrne JA, Stender (initials not captured) | More science friction for less science fiction (Primer) | PLoS Biology | 2025 | DOI 10.1371/journal.pbio.3003167 | SEARCH_SNIPPET |
| 3 | (authors not captured) | Most published human disease RNA-seq cannot be uniformly reanalyzed: a population-scale audit of reprocessability in the Gene Expression Omnibus | bioRxiv **preprint** (+ Zenodo record 21817531) | 2026 | bioRxiv ID 2026.08.05.742891 (DOI prefix in result was non-standard — **needs verification**) | SEARCH_SNIPPET (preprint) |
| 4 | (authors not captured) | Papermills as another challenge to research integrity and trust in science | — | 2025 | PMC11907274 | SEARCH_SNIPPET |
| 5 | (news) | Low-quality papers are surging by exploiting public data sets and AI | Science (news) | 2025 | no DOI (news item) | SEARCH_SNIPPET |
| 6 | (authors not captured) | The proliferation of derivative and redundant studies in endocrinology due to the application of Mendelian randomisation and other methods to open databases | Frontiers in Endocrinology (editorial) | 2024 | PMC11197397 | SEARCH_SNIPPET |
| 7 | (authors not captured) | Expectations for papers performing Mendelian randomization analyses | PLOS Genetics | 2025 | DOI 10.1371/journal.pgen.1011767 | SEARCH_SNIPPET |
| 8 | Oransky I / Retraction Watch (staff) | Exclusive: Journal bans drug safety database papers as they flood the literature | Retraction Watch (16 Sep 2025) | 2025 | no DOI | SEARCH_SNIPPET |

**9. `models_and_data`**
- **GEO** for the chosen disease. **No accession appeared in any of my search results, so none is given: accessions to be identified by the student in GEO.** Choose one disease with many published hub-gene papers and at least 4–6 independent series with ≥20 samples per group. Expect to rely on processed matrices rather than raw reads, given the 2026 reprocessability finding, and pre-specify how you handle platform heterogeneity.
- **The audited papers:** identified by a pre-registered search. **My searches could not query PubMed, so corpus size is unknown.** Pre-specify a sampling frame and seed.
- Everything open; no credentialing; no money.

**10. `key_experiments`**
1. Pre-registered systematic identification and extraction of hub-gene lists (OSF), with dual extraction on a subsample and reported agreement.
2. Independent re-analysis: `GEOquery` to retrieve series, `limma` for microarray and `DESeq2`/`edgeR` for counts, with `sva`/`ComBat` for batch where appropriate and a pre-specified decision rule for platform handling.
3. **The matched null (the core of the paper):** for each published hub-gene list of size *k*, draw ≥1,000 random gene sets of the same size matched on mean expression decile and variance decile; compute the same replication statistic (fraction with concordant direction and nominal significance) for the published list and for the null distribution; report an empirical p-value per paper and the distribution across papers.
4. Secondary analyses: pairwise Jaccard overlap between papers' lists; whether hub-gene status is predicted simply by expression level or connectivity; whether papers' own "validation" datasets overlap their discovery datasets (a common undisclosed problem).
5. `WGCNA` and `clusterProfiler` re-runs where needed to reproduce the original pipelines faithfully.
6. Deliverable: replication rate, matched-null benchmark, a minimal reporting/analysis protocol, and a fully open repository. All R, all laptop-feasible.
- **Gating:** none technically. The real gate is **social**: a Chinese undergraduate publishing an audit of a genre dominated by Chinese-affiliated authors carries reputational and supervisory risk. Mitigate by auditing *the genre, not the authors*: analyze papers in aggregate, do not name individual papers in the text, deposit the (necessarily identifiable) extraction sheet with a clear statement that no judgement about individual authors is intended, and secure explicit supervisor buy-in before starting. If the supervisor is uncomfortable, choose a different topic — this one is not worth a conflict.

**11. `expected_and_negative_results`**
If published hub genes *do* replicate above the matched null, that is a genuinely surprising and highly publishable defence of the genre. Either direction is informative, which is what makes it a real study rather than a polemic.

**12. `difficulty_and_cost`**
Difficulty **2–3/5**. Cost **≈¥0** plus APC. Fully laptop-feasible (16 GB is enough for processed matrices; raw-read reprocessing would not be, and the 2026 audit suggests you should not attempt it).

**13. `timeline_months`**
Months 1–2 pre-registration and corpus assembly; months 2–5 re-analysis and null construction; months 5–6 secondary analyses; months 6–8 writing. **Achievable in 8 months; the cheapest and most schedule-certain option on this list.**

**14. `target_journal_tier`**
Tier: methodological / meta-research, modest prestige but real. Realistic: *BMC Medical Research Methodology*; *PeerJ*; *Research Integrity and Peer Review*; *Briefings in Bioinformatics* (stretch, if the matched-null method is presented as a contribution); *Journal of Clinical Epidemiology* (stretch). Honest: this will not be a high-impact-factor paper, but it is the kind of paper that gets cited by editorials and survives scrutiny — which is worth more for a student's record than a Q2 signature paper that may later be questioned.

**15. `reviewer_attacks`**
1. **"Your matched null is not matched on the right thing"** (connectivity, module membership, pathway membership). Pre-specify several matching schemes and report sensitivity to all of them.
2. **"Replication failure reflects biological and technical heterogeneity between cohorts, not analytic error."** Partly true and partly the point; the matched null is the answer, since random genes face the same heterogeneity. Make that argument explicitly and early.
3. **"You cannot faithfully reproduce pipelines that were not fully reported."** Correct — report how many papers were un-reproducible and treat that as a finding, citing the 2026 GEO reprocessability audit.
4. (Non-statistical but real) **"This is a critique, not research."** The matched-null quantification is the defence; lead with the method, not the complaint.

**16. `prelim_ratings`**
Novelty **M–H** · Evidence-base **H** · Overlap-risk **M** (meta-research groups are actively working this seam — Byrne and colleagues in particular — so move quickly and pre-register).

---

# `domain_landscape` (2023–2026)

The decisive change since roughly 2023 is that *access to data stopped being the scarce resource*, and so analysis volume stopped being evidence of contribution. The result is a documented collapse in the credibility of several formerly attractive genres, and it is specific enough to name.

**Mendelian randomization.** The method is sound; the literature built on it is not. The European Journal of Epidemiology reports MR papers rising from 3.1% of its submissions in 2020 to 13.0% in 2024. PLOS One has run dedicated editorial screening of MR submissions since late 2023 and rejects a high proportion. In July 2025 PLOS Genetics published formal expectations stating that it receives many poorly performed MR studies which are "almost invariably rejected during editorial review," and — the sentence that should shape this student's choice — that it **strongly encourages authors to provide some sort of biological validation of their MR findings**. PLOS Medicine requires STROBE-MR with a completed checklist. Frontiers in Endocrinology published a 2024 editorial on the proliferation of derivative and redundant open-database studies and told authors it would no longer consider bibliometric studies at all. Retractions are individual rather than en masse, but they are explicit: Skin Research and Technology retracted two MR papers on the same day in October 2025, stating that the articles were accepted after an insufficient peer-review process, that the findings "cannot be regarded as scientifically sound," and that the papers lacked the biological rationale to justify MR; Frontiers in Endocrinology retracted an immune-cell MR paper in February 2025. Nature Genetics published "Challenges and future directions for Mendelian randomization" in 2026. **Conclusion: a naive two-sample MR is now a liability, not a credential.** MR survives only as cis-instrumented target work with colocalization and orthogonal validation, or as adjudication of existing claims.

**NHANES.** Suchak et al. (PLoS Biol 2025) is the definitive document: 341 formulaic single-exposure papers, rising from roughly 4/year in 2014–2021 to 190 in 2024 alone, characterized by failure to account for multifactorial relationships, failure to account for false-discovery risk, and selective extraction of data rather than use of the full resource. *Science* reported that 92% of post-2021 papers had a China-affiliated first author (versus 8% before 2021) and that Springer Nature has retracted a number of them. A Dove Press editorial reports a 1,244% rise in sleep-focused NHANES papers, from 9 in 2015 to 121. **This genre is closed.**

**TCGA signatures and hub genes.** My searches returned dozens of 2025 LASSO-Cox-plus-nomogram papers and *no* editorial defending them; their own limitations sections concede that data came only from public repositories and that accuracy must be assessed in clinical samples the authors do not have. I did not find a formal journal ban, so I will not claim one — but the pattern (many near-identical papers, no external cohorts, self-acknowledged non-validation) is the same pattern that produced the NHANES intervention.

**Pharmacovigilance disproportionality.** Retraction Watch reported on 16 September 2025 that a journal has banned drug-safety-database papers outright because they were flooding the literature, noting that FAERS accounts for a large share of the spike and that many papers stack multiple redundant statistics; Drug Safety published "Charting and Sidestepping the Pitfalls of Disproportionality Analysis" in 2025, and a separate piece is titled "The Rising Misuse of Pharmacovigilance Reporting Systems: A Threat to Evidence-Based Medicine." **Also closed.**

**Network pharmacology / network toxicology plus docking.** A 2025 Frontiers in Pharmacology commentary reviewed 35 papers, flagged 13 more as suspicious, and concluded that blind docking has been inappropriately used in most network pharmacology analyses, with ligands docked to different protein domains rather than a shared active site. The genre's own papers concede that docking scores neglect pharmacokinetics and need molecular-dynamics follow-up.

**What still commands respect.** Three things. First, **triangulation with a bench endpoint** — this is now explicit journal policy at PLOS Genetics, not merely taste. Second, **honest methodological work on prioritization**: Tambets et al. (HGG Advances 2024) showed that assigning fine-mapped pQTLs to the nearest protein-coding gene outperformed every colocalization method tested (71.9% precision, 76.9% recall, versus coloc.susie at 45.1% precision), and that MR plus multiple conditionally distinct colocalizing QTLs reached 81% precision only by collapsing recall to 7.1%. That single paper should be read by this student before anything else; it is both the best available calibration prior and the sharpest weapon reviewers will use. Third, **data resources are genuinely excellent and genuinely open**: deCODE SomaScan pQTLs, UKB-PPP Olink pQTLs (summary statistics on AWS Open Data and ukb-ppp.gwas.eu, with individual NPX behind UK Biobank approval that this student does not need), Bryois cell-type brain eQTLs with full summary statistics on Zenodo, MetaBrain, SEA-AD processed snRNA-seq on AWS, Bellenguez's AD GWAS at GWAS Catalog **GCST90027158**, Wightman's NIAGADS files including a version excluding 23andMe and UK Biobank, and as of 2026 a consensus ADRD meta-analysis (Nature Genetics 58:1214–1225) reporting 91 loci with 56 detected specifically in clinically diagnosed cases and 18 loci flagged as needing external validation. There is also a crucial honest caution: Eldjarn et al. (Nature 2023) found only modest Olink–SomaScan correlation and required a 2024 Author Correction that *reversed* its own precision claim, and a 2025 preprint estimates missense-mediated epitope effects affect ≤12% of cis-pQTLs. The data are good; the measurement layer is not transparent.

**Where an undergraduate with R can genuinely contribute.** Not by adding a nomination to a pile of nominations. By (a) being the person who actually tests a named published prediction at the bench — the field's own flagship papers now admit in their peer-review files that they performed no functional validation and that a third of their prioritized genes lack orthogonal support; (b) by auditing a specific, enumerable body of claims against stress tests with documented failure mechanisms; or (c) by building the null that a genre never built for itself. All three are achievable with a laptop, one mouse cell line, Western blots and siRNA. None requires money the student does not have. The scarce resource now is not data or compute — it is a question whose answer could come out either way.

---

# `rejected_ideas`

1. **Generic two-sample MR of exposure X → neurological outcome Y via IEU OpenGWAS.** Saturated to the point of desk rejection at PLOS One and PLOS Genetics, retractions ongoing for exactly this design, and OpenGWAS now requires authentication with per-user allowances that break reproducible pipelines.
2. **NHANES single-exposure association study (any exposure, any outcome).** Suchak et al. documented 190 such papers in 2024 alone; Springer Nature is retracting them; the design cannot support its own conclusions.
3. **TCGA/GEO prognostic signature plus nomogram (ferroptosis-, cuproptosis-, disulfidptosis-, autophagy- or senescence-"related genes").** Saturated, paper-milled, and reviewers now demand independent clinical cohorts the student cannot obtain.
4. **FAERS/openFDA disproportionality analysis.** At least one journal banned the genre outright in September 2025; multiple 2025 editorials call it misused.
5. **Network pharmacology or network toxicology plus molecular docking of a TCM formula or environmental toxicant.** A 2025 commentary found blind docking misapplied in most such analyses; the design generates no falsifiable prediction.
6. **Gut microbiome MR on a neurological outcome.** The weakest instruments in the entire MR literature — microbiome GWAS yield very few genome-wide significant variants — combined with the most saturated topic space.
7. **MIMIC-IV observational study of delirium or sepsis-associated encephalopathy.** Credentialing is genuinely achievable (see tooling note), but the design space is as crowded as NHANES, confounding is unmanageable without strong clinical-epidemiology supervision, and the student's comparative advantage (a neuronal cell model) goes unused.
8. **Virtual screening / AlphaFold-docking paper nominating natural compounds against GPX4, ACSL4 or similar.** A docking score is not a mechanism and does not discriminate between hypotheses; increasingly desk-rejected, and the student's wet lab could test such predictions but the predictions themselves carry no information.
9. **Bibliometric analysis of any field.** Frontiers in Endocrinology stated it will no longer consider bibliometric studies; other journals are following.
10. **Anything requiring UK Biobank individual-level data, patient samples, or a biobank.** Not available. Summary-statistics routes exist for the genetics and are sufficient; the clinical routes are not.

---

# `tooling_note`

**AlphaFold, structure analysis and molecular docking.** Available in principle, and almost certainly not worth using here. A docking score is a ranking heuristic, not evidence of binding, and certainly not evidence of mechanism; the 2025 Frontiers in Pharmacology review found blind docking inappropriately applied in most network pharmacology analyses, with ligands placed in different protein domains rather than a common active site, and papers in the genre themselves concede that scores neglect pharmacokinetics. The one circumstance in which structure work would earn its place in these topics is a **discriminating** prediction: for example, if the student's candidate gene (Topic 1) has a coding risk variant, AlphaMissense or structural analysis could predict loss versus gain of function, which maps onto *opposite* siRNA and overexpression predictions — then the structure work has done work. The TMEM106B literature is a good illustration of when structure matters: the risk haplotype contains both a cis-eQTL effect and the missense variant rs3173615 (S185T), recent work argues the missense variant is the primary causal driver, and the risk T185 variant selectively increases the fibril core — a structural claim with a testable consequence. Note also that deep-learning variant predictors are known to be weaker in intrinsically disordered regions and that benchmark circularity is a live concern, so a prediction should never be the paper's load-bearing claim. **Verdict: use structure only to generate a discriminating prediction you will then test; never as a figure that substitutes for an experiment.**

**MIMIC-IV credentialing.** Technically easy and genuinely obtainable: PhysioNet's FAQ states that credentialing plus CITI training-report approval typically takes 1–2 weeks (the relevant CITI course is "Data or Specimens Only Research," a shorter module than full human-subjects training), with a separate data-use agreement signed per MIMIC dataset. A Georgia Tech student-competition page estimates several business days and warns about delays. So the barrier is low. **But the verdict is: not worth it for this student on this timeline.** The access is cheap; the *supervision* for credible ICU epidemiology is not, and the student has no comparative advantage there. Their competitive asset is the dry-to-wet bridge, and MIMIC gives them nothing to bridge to.

**NHANES.** Free, no credentialing, and that is precisely the problem — the barrier to entry is zero, so the genre has no information left in it. **Verdict: do not touch it**, with one narrow exception: if the student wanted a meta-research project, NHANES is the best-documented example of genre collapse and Suchak et al. (PLoS Biol 2025) is a usable template. But do not add an association paper to that pile.

**Practical tooling notes worth acting on.** (i) Do **not** build any project around OpenGWAS API calls — authentication is now required, allowances are enforced, and GitHub issues document repeated breakage; download flat summary-statistics files instead. (ii) Do **not** attempt to mirror plasma-proteomics resources wholesale — deCODE's download page lists a companion comparison dataset at 19.7 TB. Fetch per-protein and per-locus. (iii) SEA-AD's full snRNA-seq objects will not fit comfortably on a laptop; use the AWS Open Data copy (not the reduced CELLxGENE version), and subset or pseudobulk. (iv) For ferroptosis readouts without flow cytometry, C11-BODIPY 581/591 is explicitly readable on a fluorescence microplate reader, and the standard recommendation is to pair it with an MDA/TBARS kit rather than rely on either alone — state the substitution in Methods. (v) Budget the article processing charge explicitly (¥10,000–30,000+ at most plausible open-access venues); it is frequently larger than the reagent budget and is the most common reason a finished undergraduate paper does not get submitted.

---

# Committee recommendation (ranked by probability of one publishable SCI Original Article within 6–12 months)

1. **Topic 3** (HT-22 model adjudication: audit + controlled re-test) — best match to the student's actual assets, lowest technical risk, cheapest, both outcomes publishable, overlap risk low. **This is my first choice.**
2. **Topic 2** (AD proteome-MR robustness audit) — zero material cost, strongest venue fit (*HGG Advances*), 8-month timeline, but demands real statistical-genetics supervision.
3. **Topic 6** (hub-gene matched-null replication audit) — cheapest and most schedule-certain, modest venue, but carries a social/supervisory gate that must be cleared first.
4. **Topic 5** (FSP1 requirement for vitamin K neuroprotection) — fastest to a finished paper and the best-matched toolkit, but **verify first** whether PMC12725873 already contains the FSP1 knockdown arm, and accept high scoop risk.
5. **Topic 1** (neuron-prioritized AD gene at the bench) — highest ceiling and the best story, but realistically 14–18 months and dependent on siRNA working on the first candidate.
6. **Topic 4** (LINCS calibration test) — intellectually the most interesting framing, but the widest spread between enthusiastic acceptance and desk rejection, and the most likely to produce a result the student cannot place.

**On whether a purely computational paper can be a credible Original Article: yes — but only in the audit, adjudication or methods genre, and only with a pre-registered protocol and an open repository.** A purely computational paper that *nominates* (genes, proteins, drugs, signatures) is now presumed worthless until validated, and PLOS Genetics has written that presumption into policy. A purely computational paper that *tests* — that could have come out the other way and tells the field something it must act on — is a perfectly respectable Original Article. Topics 2 and 6 are of the second kind. Nothing on this list is of the first.

**Verification tasks the student must complete before committing (I could not do these with network access blocked):** (a) read PMC12725873 in full to check for an FSP1 knockdown arm (kills or confirms Topic 5); (b) retrieve the 2013 Neural Regeneration Research differentiation protocol (Topic 3); (c) confirm the access route for the 2026 consensus ADRD summary statistics (Topic 2); (d) identify GEO accessions for every dataset used (Topics 4, 6) — **I have given none because none appeared verbatim in my results**; (e) confirm the Nott 2019 DOI/PMID, the Maher & Davis 1996 citation, the Brain 2025 MR paper DOI, and the authorship of the Alzheimer's Research & Therapy 2022 GWAS-versus-GWAX paper, all of which I saw only as titles or as citations inside other papers.
