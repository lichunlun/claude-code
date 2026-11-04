# Topic-Selection Committee Report
### Chinese clinical-medicine undergraduate · one original SCI paper · 6–12 months
### Reviewer: tumor biology / TME / epigenetics & PTM

---

## 0. Methodological note on this report

I ran 28 WebSearch queries; 24 returned results before the session's search budget was exhausted. Every reference below appeared in an actual result in this session and is tagged. Two late candidates could **not** be verified and are therefore **not offered as topics**: (a) a "human-genetics prediction → cells" topic built on DNPH1 as an MR-nominated breast-cancer risk protein plus its PARPi/hmdU biology — the MR hit `DNPH1` appeared verbatim in a result, but I could not verify the direction of effect or the PARPi link, so it is listed under rejected/deferred ideas, not as a topic; (b) the author list of the Genome Biology YTHDF rebuttal (title, journal, DOI verified; authors not captured).

**Blunt framing before the topics.** Classic oncology mechanism discovery is a *bad* fit for this student: no co-IP, no mass spectrometry, no lentivirus, no CRISPR lines, no ChIP, no flow cytometry. Every "we discovered that X modifies Y to drive cancer Z" project needs at least three of those. But there is one genre where WB + qPCR + siRNA + transfection + viability is not a compromise — it is *exactly the right toolkit*: **arbitration of contradictory published claims about PTM writers/erasers and RNA-modification readers.** Those disputes are being fought with precisely these assays. This is where I am steering the student. Separately, HT-22 is close to worthless for most oncology, but it is a genuine asset for exactly one thing: being the *neuronal partner* in a tumour–neuron experiment. Two topics exploit each of those facts.

---

# TOPIC 1

**1. `title_en`**
Which enzyme actually writes histone lysine lactylation in a glycolytic cancer cell? A reagent-matched, same-cell-line arbitration of six competing "lactyltransferase" claims

**2. `core_question`**
In a single cancer cell line under defined glycolytic load, does siRNA depletion of EP300/CREBBP, KAT7(HBO1), AARS1, AARS2, or HDAC1/2/3 (singly and as HDAC1+2+3) reduce global pan-Kla and the specific marks the cancer literature actually blots (H3K18la, H3K9la, H4K12la) — and is the enzyme requirement the same at basal state and under high glycolytic flux?

**3. `hypothesis`**
The six published "writer" claims are not alternative truths but **condition-dependent and partly reagent-dependent**. Specifically: at basal state in a cancer line, no single acetyltransferase knockdown will move global pan-Kla (reproducing the 2025 JBC result in a new cell type), whereas HDAC1/2/3 triple knockdown will; but under imposed high glycolytic flux the site-specific marks (H3K18la) will become EP300-dependent while global pan-Kla stays HDAC-dependent. I.e. "global pan-Kla" and "H3K18la" have *different* writers, and the field's habit of treating them interchangeably is the source of the contradiction.

**4. `novelty_claim`**
New: the first head-to-head, same-cell, same-antibody-lot comparison of all claimed writers, with glycolytic load as an explicit variable and global-vs-site-specific marks separated. Traps avoided: this is not two molecules jammed into an axis, not a mechanism transplanted to a new cancer type, and not DEG+correlation. It is a **reagent-independent re-test of widely cited but mutually contradictory claims** — one of the explicitly sanctioned novelty categories. It also avoids the "a few WB bands → complete causal pathway" trap by inverting the logic: the WBs are the *endpoint being adjudicated*, not evidence for a downstream story.

**5. `state_of_the_art`**
Six mutually incompatible writer claims now exist. p300/CBP (Nature 2019, `SEARCH_SNIPPET`); HBO1/KAT7, preferentially H3K9la (Nat Commun 2024, `SEARCH_SNIPPET`); AARS1 as a lactate sensor/lactyltransferase acting on p53 (Cell 2024, `SEARCH_SNIPPET`) and on YAP in gastric cancer (JCI 2024, `SEARCH_SNIPPET`); AARS1+AARS2 as *global* lactyltransferases regulating cGAS (Nature 2024, `SEARCH_SNIPPET`); non-enzymatic transfer from lactoylglutathione (Cell Chem Biol 2019, `SEARCH_SNIPPET`); and most disruptively, class I HDACs as *writers* (J Biol Chem 2025, `SEARCH_SNIPPET`) — the same enzymes earlier reported as *delactylases* (Sci Adv, `SEARCH_SNIPPET`). The 2025 JBC paper reports that in HEK293T, siRNA against AARS1/AARS2 did **not** change global Kla, siRNA against CBP/p300/HBO1 did **not** change Kla, GLO1 knockdown did **not** change Kla, and HDAC1/2/3 triple knockdown produced the strongest effect — and that its result contradicts the earlier delactylase experiment, which it attributes to knockdown efficiency. A 2025 Nature Cell Biology review and a 2026 Molecules review both treat the writer identity as unsettled.

**6. `specific_open_problem`**
The field's most consequential negative result (JBC 2025) was obtained in **HEK293T at basal lactate**, a non-cancer, non-glycolytic-stressed line — i.e. precisely *not* the condition under which the cancer lactylation literature makes its claims. Nobody has asked whether the Cell/Nature AARS1/AARS2 and the Nature-2019 p300 requirements reappear when glycolytic flux is high, nor whether global pan-Kla and H3K18la have different writer dependencies. Knockdown efficiency — the explanation JBC itself invokes for the contradiction — has never been systematically quantified and matched across the competing experiments.

**7. `delta_vs_closest_paper`**
Closest paper: **"Class I histone deacetylases catalyze lysine lactylation," J Biol Chem 2025 (PII S0021-9258(25)02453-6; preprint bioRxiv 10.1101/2025.02.25.640220).** Exact differences: (i) that work is in HEK293T; this is in a cancer line where the disputed claims were made; (ii) that work tests basal Kla only; this makes glycolytic load (glucose concentration, Na-L-lactate, oxamate, 2-DG) an independent variable; (iii) that work reads global pan-Kla; this separates global pan-Kla from H3K18la/H3K9la/H4K12la, which is what the cancer papers actually report; (iv) that work does not quantify and match knockdown efficiency across enzymes, which is the hypothesis it offers for the contradiction; (v) this adds a second antibody vendor to test reagent-independence.

**8. `references`**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | Zhang D, Tang Z, Huang H, … Zhao Y | Metabolic regulation of gene expression by histone lactylation | Nature 574(7779):575–580 | 2019 | PMID 31645732; doi 10.1038/s41586-019-1678-1; PMC6818755 | `SEARCH_SNIPPET` |
| 2 | Gonzatti MB et al. (first author per result) | Class I histone deacetylases catalyze lysine lactylation | J Biol Chem | 2025 | PII S0021-9258(25)02453-6; PMC12624779; preprint doi 10.1101/2025.02.25.640220 | `SEARCH_SNIPPET` |
| 3 | Moreno-Yruela C et al. | Class I histone deacetylases (HDAC1–3) are histone lysine delactylases | Science Advances | result describes it as 2021 — confirm year | doi 10.1126/sciadv.abi6696 | `SEARCH_SNIPPET` |
| 4 | Li et al. | AARS1 and AARS2 sense l-lactate to regulate cGAS as global lysine lactyltransferases | Nature 634(8036) | 2024 | doi 10.1038/s41586-024-07992-y | `SEARCH_SNIPPET` |
| 5 | Zong et al. | Alanyl-tRNA synthetase, AARS1, is a lactate sensor and lactyltransferase that lactylates p53 and contributes to tumorigenesis | Cell | 2024 | PII S0092-8674(24)00397-0 | `SEARCH_SNIPPET` |
| 6 | — (authors not captured) | HBO1 catalyzes lysine lactylation and mediates histone H3K9la to regulate gene transcription | Nat Commun 15(1):3561 | 2024 | PMID 38670996; doi 10.1038/s41467-024-47900-6; PMC11053077 | `SEARCH_SNIPPET` |
| 7 | Gaffney et al. | Non-enzymatic Lysine Lactoylation of Glycolytic Enzymes | Cell Chem Biol | 2019 | no PMID/DOI captured | `SEARCH_SNIPPET` |
| 8 | — | Emerging roles of lysine lactyltransferases and lactylation | Nat Cell Biol | 2025 | doi 10.1038/s41556-025-01635-8 | `SEARCH_SNIPPET` |
| 9 | — | Lysine Lactylation Writers: Enzymatic Versus Non-Enzymatic Mechanisms, Isomer Specificity, and Therapeutic Implications | Molecules 31(21):3902 | 2026 | mdpi.com/1420-3049/31/21/3902 | `SEARCH_SNIPPET` |
| 10 | — | The alanyl-tRNA synthetase AARS1 moonlights as a lactyltransferase to promote YAP signaling in gastric cancer | J Clin Invest | 2024 | jci.org/articles/view/174587; PMC11093599 | `SEARCH_SNIPPET` |

**9. `models_and_data`**
Cell lines: HT-22 (in hand, serves as the non-cancer comparator — a legitimate second cell type at zero cost) **plus one cancer line that must be obtained**. Recommended: HepG2 or a line matching a specific disputed paper (e.g. a PDAC line for the Mol Cancer 2024 glycolysis↔lactylation feedback claim, doi 10.1186/s12943-024-02008-9, `SEARCH_SNIPPET`). Obtain from a Chinese cell bank; **STR authentication is mandatory and must be budgeted** — reviewers of an arbitration paper will attack cell identity first. Public data: GEO **GSE239656** (appeared in a result alongside the HBO1 paper, `SEARCH_SNIPPET`) can be re-analysed to ask whether HBO1-dependent H3K9la sites overlap the genes the other writer papers claim; any further accessions "to be identified."

**10. `key_experiments`**
*Bench (all within current techniques):* (a) siRNA panel — EP300, CREBBP, KAT7, AARS1, AARS2, HDAC1, HDAC2, HDAC3, HDAC1+2+3; ≥2 independent siRNAs per gene; knockdown quantified by both qPCR and WB and **reported as % residual protein for every sample** (this is the study's key methodological contribution). (b) Each knockdown × 2–3 metabolic conditions (5 mM vs 25 mM glucose; ± 20 mM Na-L-lactate; ± 20 mM oxamate). (c) WB panel: pan-Kla, H3K18la, H3K9la, H4K12la, pan-Kac, H3K18ac, total H3, total H4 — loading normalised to total H3, not to GAPDH. (d) Same key conditions repeated with a **second antibody vendor** for reagent-independence. (e) Functional coupling: qPCR of the specific target genes the disputed papers nominate, to test whether gene output tracks the writer whose loss removes the mark. (f) Rescue by transfection of a WT and catalytically-dead construct for whichever enzyme scores (transfection is in hand; plasmids cheap).
*Bioinformatics:* re-analysis of GSE239656 (and any further accessions located) for overlap between writer-dependent sites and the loci claimed by competing papers. This is a mechanistic overlap test, not DEG+enrichment.
*Gating requirements, flagged:* histone-PTM mass spectrometry is **not** required for the core claim but **one outsourced targeted histone-PTM LC-MS/MS run** on 2–3 decisive conditions would roughly double the paper's tier. Treat as optional add-on (see cost). ChIP/CUT&RUN not needed and should not be attempted.

**11. `expected_and_negative_results`**
Both outcomes are publishable, and this is the central design virtue. If no acetyltransferase knockdown moves pan-Kla while HDAC1/2/3 does, the student has independently reproduced and generalised the most disruptive 2025 result into cancer cells — valuable. If EP300 dependence *reappears* under glycolytic load, the student has defined the limiting condition that reconciles Nature 2019 with JBC 2025 — more valuable. If global and site-specific marks dissociate, that alone explains much of the literature's incoherence. There is no branch of this experiment that yields nothing. **The one genuinely unpublishable outcome is technical failure of knockdown**, which is why knockdown efficiency must be the first milestone, not an afterthought.

**12. `difficulty_and_cost`**
Difficulty **3/5**. Estimate **¥35,000–60,000**. Must buy: one cancer line + STR authentication (~¥2,500–4,000); antibody panel incl. a duplicate-vendor subset (~¥18,000–28,000 — this is the dominant cost; PTM Bio in Hangzhou is the de facto standard and the student should buy the *same catalogue numbers* used by the disputed papers); siRNA panel (~¥6,000–10,000); reagents and plasticware (~¥6,000–10,000). Optional outsourced targeted histone-PTM LC-MS/MS: **+¥8,000–20,000**, which would push the total to the upper end of the stated budget — flag to the supervisor before committing. No mouse work. No flow, no ChIP, no lentivirus.

**13. `timeline_months`**
8–11. Months 1–2 obtain/authenticate line, validate antibodies and siRNA efficiency. Months 3–6 the knockdown × condition matrix. Months 7–8 second-vendor replication and rescue. Months 9–11 bioinformatics, writing, revision. A bioRxiv preprint at ~month 8 is advisable — arbitration studies are scoopable.

**14. `target_journal_tier`**
Tier 2 society-journal biochemistry. Realistic: **Journal of Biological Chemistry** (natural home — it published the contradicting paper), **Epigenetics & Chromatin**, **Biochemical Journal**. With the MS add-on, **Life Science Alliance** or **Journal of Molecular Cell Biology** become arguable. No acceptance can be promised. I specifically advise *against* OA megajournals here: a verified 2025 study found paper-mill retractions concentrate in high-open-access, mid-quartile, high-volume medicine journals, and publishing an arbitration study in such a venue destroys much of its credibility value.

**15. `reviewer_attacks`**
1. "siRNA is incomplete and HDACs are redundant — your negatives are knockdown failures." Pre-empted by mandatory quantitative residual-protein reporting and by the triple-knockdown arm; this is the exact criticism JBC 2025 levelled at its predecessor, so the student must not repeat it.
2. "Pan-Kla antibodies are not specific, so your entire readout is uninterpretable." Partly true and partly the point; mitigate with the second-vendor arm and by citing the documented limited specificity of acylation antibodies (Sci Rep 2021, `SEARCH_SNIPPET`). Topic 2 attacks this head-on and the two topics should not both be attempted.
3. "One cell line, no mass spectrometry, no in vivo." Honest answer: scope is deliberately one cell line plus HT-22 as a second cell type; MS is offered as an optional arm. This attack will cap the journal tier and the student should accept that trade.

**16. `prelim_ratings`**
Novelty **H** (high for the genre — it adjudicates a live, dated dispute). Evidence-base **H** (10 verified references, including flatly contradictory primaries). Overlap-risk **M** (the field is hot; someone will do this, hence the preprint advice).

---

# TOPIC 2

**1. `title_en`**
Is it lactylation at all? Discriminating histone lactylation from HDAC inhibition and from lactate-derived acetyl-CoA as the mechanism by which lactate remodels cancer-cell chromatin

**2. `core_question`**
When a cancer cell is exposed to lactate at the doses used throughout the lactylation literature, is the resulting chromatin change attributable to L-lactylation, or is it quantitatively reproduced by lactate's HDAC-inhibitory activity and by lactate serving as a carbon source for histone acetylation — and does the pan-Kla/H3K18la antibody signal survive stereochemical and acyl-peptide competition controls?

**3. `hypothesis`**
A substantial fraction of the published "lactate → histone lactylation → gene X" signal is a composite artefact: (i) **D-lactate**, which cannot generate L-lactyl-CoA and is not an AARS substrate, will reproduce much of the pan-Kla WB increase, implying the antibody signal is not L-lactylation; (ii) an HDAC inhibitor dose-titrated to match lactate's acetylation increase will reproduce the "lactylation" signal without any lactate; (iii) the transcriptional output attributed to lactylation will track H3K18**ac** more tightly than H3K18**la**.

**4. `novelty_claim`**
New: the first explicit *discriminating measurement* between three co-occurring, individually published routes from lactate to chromatin, using cheap stereochemical and dose-matching controls that the field has not applied together. Traps avoided: not an axis, not a transplant, not a model swap, no docking, no DEG+correlation. It belongs to two sanctioned categories at once — **a measurement that discriminates competing explanations** and **a reagent-independent re-test of a widely cited but shaky claim**. The D-lactate control in particular is a near-free experiment with a binary interpretation.

**5. `state_of_the_art`**
Three routes are each independently published and never compared. Route 1, L-lactylation: Nature 2019 (`SEARCH_SNIPPET`); and Nat Chem Biol 2024/2025 established that K_L-la, not K_D-la or carboxyethyl-lysine (Kce), is the dominant glycolysis-induced histone isomer, reporting >100-fold higher anti-L-lactyllysine affinity for L- over D-lactylated BSA (`SEARCH_SNIPPET`). Route 2, HDAC inhibition: lactate inhibits HDAC activity and changes gene expression (Nucleic Acids Res 2012, `SEARCH_SNIPPET`); this mechanism is load-bearing in the CD8 T-cell stemness paper, which attributes lactate's effect to HDAC inhibition raising H3K27ac at the *Tcf7* super-enhancer (Nat Commun 2022, `SEARCH_SNIPPET`). Route 3, carbon source: ¹³C₃-lactate labels histone H4 to ~60% via nucleus-localised LDHA, and lactate raises histone **acetylation** (Exp Mol Med 2023, `SEARCH_SNIPPET`). On the antibody side, pan-acylation antibodies have documented limited specificity, with acetylation's vast overabundance as the suspected off-target source and batch-to-batch variability (Sci Rep 2021, `SEARCH_SNIPPET`); the 2025 JBC preprint reports the pan-Kla antibody also reacts with carboxyethyl-lysine (`SEARCH_SNIPPET`); a 2025 study found histone lactylation stoichiometry of only ~0.01–0.44% versus up to 25–35% for acetylation at some N-terminal lysines, and reported predominantly **D**-lactylation at H3K18 and H3K79 in mouse testis (`SEARCH_SNIPPET`); and 2025 reviews state that low abundance makes it hard to distinguish a primary regulatory function from a secondary metabolic consequence (`SEARCH_SNIPPET`).

**6. `specific_open_problem`**
Essentially the whole cancer lactylation literature establishes "lactate raises H3K18la" by sodium-lactate treatment plus a pan-Kla or H3K18la Western blot, and infers a transcriptional mechanism. **The three alternative routes are never excluded in the same experiment.** No published study has, in one system: matched sodium load and osmolarity, separated lactic acid from the pH-neutral anion, compared L- versus D-lactate at equal dose, dose-matched an HDAC inhibitor to lactate's own acetylation effect, and run acyl-peptide competition on the detecting antibody. The stoichiometry data make the question urgent: a mark present at 0.01–0.44% is being asked to explain transcriptional changes while a 25–35% mark moves in the same experiment and is not measured.

**7. `delta_vs_closest_paper`**
Closest paper: **An YJ et al., "Lactate as a major epigenetic carbon source for histone acetylation via nuclear LDH metabolism," Exp Mol Med 55:2238–2247 (2023), doi 10.1038/s12276-023-01095-w.** That paper proves route 3 exists (¹³C tracing into H4 acetylation) but does **not** compare it against lactylation, does not test antibody specificity, does not use D-lactate, and does not dose-match an HDAC inhibitor. The delta is the arbitration itself: An et al. add a third mechanism to the pile; this study asks which one carries the signal, using isotope-free, undergraduate-feasible discriminators.

**8. `references`**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | An YJ et al. | Lactate as a major epigenetic carbon source for histone acetylation via nuclear LDH metabolism | Exp Mol Med 55:2238–2247 | 2023 | doi 10.1038/s12276-023-01095-w; PMC10618192 | `SEARCH_SNIPPET` |
| 2 | Latham T, Mackay L, Sproul D, et al. | Lactate, a product of glycolytic metabolism, inhibits histone deacetylase activity and promotes changes in gene expression | Nucleic Acids Res 40(11):4794–4803 | 2012 | doi 10.1093/nar/gks066 | `SEARCH_SNIPPET` |
| 3 | Zhang D, Gao J, Zhu Z, … Dai L, Li L, Zhao Y | Lysine l-lactylation is the dominant lactylation isomer induced by glycolysis | Nat Chem Biol 21:91–99 | 2024 online / 2025 print | doi 10.1038/s41589-024-01680-8 (PMID not captured) | `SEARCH_SNIPPET` |
| 4 | — | Both L-lactyl and D-lactyl enantiomers modify histones in mouse testis | bioRxiv (preprint) | 2025 | doi 10.1101/2025.10.09.681385; PMC13380202 | `SEARCH_SNIPPET` |
| 5 | — | Epigenetics Identifier screens reveal regulators of chromatin acylation and limited specificity of acylation antibodies | Sci Rep | 2021 | doi 10.1038/s41598-021-91359-0; PMC8211816 | `SEARCH_SNIPPET` |
| 6 | Zhang D et al. | Metabolic regulation of gene expression by histone lactylation | Nature 574(7779):575–580 | 2019 | PMID 31645732; doi 10.1038/s41586-019-1678-1 | `SEARCH_SNIPPET` |
| 7 | Gonzatti MB et al. | Class I histone deacetylases catalyze lysine lactylation | J Biol Chem | 2025 | PII S0021-9258(25)02453-6; PMC12624779 | `SEARCH_SNIPPET` |
| 8 | — | Lactate increases stemness of CD8+ T cells to augment anti-tumor immunity | Nat Commun | 2022 | doi 10.1038/s41467-022-32521-8; PMC9448806 | `SEARCH_SNIPPET` |
| 9 | — | Lactylation in health and disease: physiological or pathological? | Theranostics 15(5):1787 | 2025 | thno.org/v15p1787 (DOI not captured) | `SEARCH_SNIPPET` |
| 10 | — | Lactylation: a Passing Fad or the Future of Posttranslational Modification | Inflammation | 2022 | doi 10.1007/s10753-022-01637-w | `SEARCH_SNIPPET` |
| 11 | — | Lactate as a Chemical Modification on Proteins and Metabolites | Annu Rev Biochem | year not captured | doi 10.1146/annurev-biochem-051024-015746 | `SEARCH_SNIPPET` |
| 12 | — | Biochemistry and regulation of histone lysine l-lactylation | (journal not captured) | — | PMC12920031 | `SEARCH_SNIPPET` |

**9. `models_and_data`**
HT-22 (in hand) + **one cancer line to be obtained**, STR-authenticated. A macrophage line (RAW264.7 or THP-1, **to be obtained**) is an optional third arm because the original Nature 2019 lactate→H3K18la→*Arg1* experiment was in macrophages, making it the single most-cited claim to re-test. Public data: accessions to be identified — the bioinformatics component here is deliberately thin and the student should not pad it.

**10. `key_experiments`**
*Bench (all in-hand techniques):* (a) **Dose- and ion-matched treatment panel** at a single lactate concentration used in the literature: Na-L-lactate, Na-D-lactate, Na-acetate, NaCl (Na⁺/osmolarity control), lactic acid (pH-dropped), and a pH-matched medium control. (b) Same panel ± oxamate, ± 2-DG, ± LDHA/LDHB siRNA to separate exogenous from glycolytic lactate. (c) **Dose-matching arm:** titrate TSA (and NaBu) to the exact H3 acetylation increase lactate produces, then ask whether pan-Kla/H3K18la follows. (d) **Antibody-specificity arm:** dot blot of synthetic L-lactyl-K18, D-lactyl-K18, acetyl-K18 and (if obtainable) carboxyethyl-K18 peptides; then pre-absorption competition of each antibody with each peptide before blotting lysates; repeat with a second vendor's antibody. (e) **Transcriptional coupling:** qPCR of the genes claimed to be lactylation-driven across the whole panel, then ask by simple correlation whether gene output tracks H3K18la or H3K18ac. (f) Nuclear-versus-cytoplasmic LDHA fractionation by WB (no confocal needed) to test route 3's prerequisite.
*Gating requirements, flagged:* chiral LC-MS/MS is the definitive isomer assay and is **not available**; the student substitutes the D-versus-L functional dissociation plus peptide competition, and must state this limitation in the paper. One outsourced targeted histone-PTM LC-MS/MS run on 3–4 decisive conditions is the single highest-value optional purchase. Carboxyethyl-lysine peptide may require custom synthesis — price it early, and drop that arm if quoted above ~¥3,000.

**11. `expected_and_negative_results`**
Fully symmetric. If D-lactate reproduces the signal, or if dose-matched TSA reproduces it, the student has shown that a standard experiment in hundreds of cancer papers does not establish what it is claimed to establish — a high-value result. If the signal is L-lactate-specific, peptide-competition-clean, dissociable from acetylation, and tracks H3K18la rather than H3K18ac, the student has supplied the specificity validation the field has been criticised for lacking — also publishable, and arguably more welcome. The only non-result is if the cancer line simply shows no chromatin response to lactate; mitigate by validating responsiveness in month 2 before committing, and by keeping the macrophage arm as a positive control condition drawn from the original paper.

**12. `difficulty_and_cost`**
Difficulty **3/5**. Estimate **¥30,000–55,000**. Must buy: cancer line + STR (~¥2,500–4,000); antibody panel across two vendors (~¥15,000–25,000); synthetic modified peptides, 3–4 species (~¥4,000–10,000, the Kce peptide being the wildcard); small-molecule panel incl. Na-D-lactate, TSA, NaBu, oxamate, 2-DG (~¥3,000–6,000); siRNA (~¥2,000–4,000); consumables (~¥5,000–8,000). Optional outsourced targeted histone-PTM MS **+¥8,000–20,000**. No mouse work; a xenograft would add nothing to this question and I recommend refusing it if offered.

**13. `timeline_months`**
7–10. This is the fastest of the six because the treatment panel is cheap and parallel. Months 1–2 line acquisition, responsiveness validation, antibody/peptide procurement. Months 3–5 treatment panel and dose-matching. Months 6–7 peptide competition and second-vendor replication. Months 8–10 write-up.

**14. `target_journal_tier`**
Tier 2 society biochemistry / epigenetics. Realistic: **Journal of Biological Chemistry**, **Epigenetics & Chromatin**, **FEBS Journal** or **FEBS Letters**. A clean positive-for-artefact result with the optional MS arm could reach **Life Science Alliance**. No promises. Same warning as Topic 1 against OA megajournals.

**15. `reviewer_attacks`**
1. "Without chiral mass spectrometry you cannot claim anything about isomers." Correct, and the student must concede it in writing. The defensible claim is narrower and still strong: *the antibody signal routinely interpreted as L-lactylation is reproduced by a treatment that cannot generate L-lactyl-CoA.*
2. "D-lactate is metabolised differently and may raise intracellular L-lactate, so your control is not clean." Real objection; mitigate by measuring medium and intracellular L-lactate with a cheap colorimetric kit in every condition and reporting it.
3. "This is a negative/technical paper, not a biological discovery." The honest rebuttal is that the field's own 2025 reviews name specificity and supraphysiological lactate doses as its limiting problems. Expect this attack to cap the tier.

**16. `prelim_ratings`**
Novelty **H**. Evidence-base **H** (12 verified refs; the contradictions are documented, not inferred). Overlap-risk **M–H** — a well-resourced lab could do this in three months, so speed and an early preprint matter. **This is my single top recommendation**, narrowly over Topic 1, because its decisive controls are cheaper, its timeline is shortest, and its result is interpretable even if the antibodies behave badly.

> **Do not attempt Topics 1 and 2 together.** They share reagents and would read as one diluted paper. Topic 2 first; Topic 1 is the natural follow-up for a master's project.

---

# TOPIC 3

**1. `title_en`**
Paralog compensation as the unmeasured variable in m6A reader biology: does YTHDF1-specific regulation of oncogene translation survive when YTHDF2/3 upregulation is prevented?

**2. `core_question`**
In a cancer cell line, does single-siRNA knockdown of YTHDF1 lower the protein-to-mRNA ratio of published YTHDF1 "translational targets" — and is any apparent YTHDF1 specificity abolished, or instead revealed, once compensatory upregulation of YTHDF2 and YTHDF3 is measured and blocked by co-knockdown?

**3. `hypothesis`**
Single YTHDF knockdowns induce measurable compensatory upregulation of the other two paralogs; this compensation is the hidden variable generating the contradictory literature. Prediction: single YTHDF1 knockdown will change target mRNA abundance (consistent with the redundant-decay model) with little change in protein/mRNA ratio, and apparent "YTHDF1-specific translational control" will shrink or vanish once paralog levels are accounted for.

**4. `novelty_claim`**
New: paralog compensation is explicitly invoked in the genetics literature as the explanation for redundancy, yet it is essentially never *measured* in the cancer papers that claim reader-specific mechanisms. This tests an **assumed-but-unmeasured step** and uses protein/mRNA ratio as a **measurement that discriminates** the decay model from the translation model — two sanctioned categories. Traps avoided: not a new axis, not a cancer-type transplant, no signature-building. It does not claim to discover a reader–target relationship; it tests whether a class of published claims is robust to a control nobody runs.

**5. `state_of_the_art`**
The unified model (Cell 2020, Zaccara & Jaffrey, `SEARCH_SNIPPET`) holds that YTHDF1/2/3 bind the same m6A sites and redundantly drive decay. It was challenged in Genome Biology 2023 (`SEARCH_SNIPPET`, authors not captured), which argued the 2020 analysis grouped RNAs by m6A status rather than by individual-protein binding, reported that YTHDF1 promotes target translation, and reported distinct protein partners and higher-order structures for YTHDF1 versus YTHDF2. Zaccara & Jaffrey defended the model in RNA 2024 (`SEARCH_SNIPPET`), noting that *Ythdf1* or *Ythdf3* loss can be compensated by the other readers whereas *Ythdf2* loss cannot, and proposing that side-by-side YTHDF1/YTHDF2 ribosome profiling would settle it. Independent genetics supports redundancy: single conditional knockout of *Ythdf1*, *Ythdf2* or *Ythdf3* had no effect on cortical neurogenesis while the triple knockout extended it (`SEARCH_SNIPPET`); structural work reports essentially identical m6A-RNA interactions across the three (`SEARCH_SNIPPET`). Meanwhile the cancer literature continues to publish YTHDF1-specific translational mechanisms (e.g. a YTHDF1–cyclin B1 translation axis in KRAS/TP53 co-mutant lung adenocarcinoma, `SEARCH_SNIPPET`), and at least one paper reports YTHDF1 driving *degradation* via AGO2 and phase separation (`SEARCH_SNIPPET`) — i.e. the opposite function.

**6. `specific_open_problem`**
The dispute has been fought almost entirely over **reanalysis of the same sequencing datasets**, with both camps arguing about how to compute translation efficiency. Compensation is named as the mechanism of redundancy but is treated as a background assumption rather than a measured quantity. Nobody has asked the cheap bench question: in a cancer line, what happens to YTHDF2/3 protein when YTHDF1 is knocked down, and does controlling for that change the answer? Nor has anyone tested whether the *specific* targets nominated by cancer papers behave as the unified model predicts.

**7. `delta_vs_closest_paper`**
Closest paper: **Zaccara S, Jaffrey SR, "Understanding the redundant functions of the m6A-binding YTHDF proteins," RNA (2024), PMC11019742, doi 10.1261/rna.079988.124 (DOI inferred from the article identifier `rna.079988.124` in the URL — verify).** That is a commentary arguing from existing sequencing data and proposing ribosome profiling as the arbiter. The delta: this study answers an adjacent question the commentary does not address, with assays the student actually owns — paralog protein/mRNA compensation quantified in every knockdown, target-level protein/mRNA ratios, and actinomycin-D mRNA stability chases on the *specific transcripts the cancer literature nominates*. It substitutes a cheap, direct measurement for the ribosome profiling neither camp has run side by side.

**8. `references`**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | Zaccara S, Jaffrey SR | A Unified Model for the Function of YTHDF Proteins in Regulating m6A-Modified mRNA | Cell | 2020 | PMID/DOI not captured | `SEARCH_SNIPPET` |
| 2 | — (authors not captured) | The mechanism underlying redundant functions of the YTHDF proteins | Genome Biology | 2023 | doi 10.1186/s13059-023-02862-8; preprint doi 10.1101/2022.05.05.490669 | `SEARCH_SNIPPET` |
| 3 | Zaccara S, Jaffrey SR | Understanding the redundant functions of the m6A-binding YTHDF proteins | RNA | 2024 | PMC11019742; article id rna.079988.124 | `SEARCH_SNIPPET` |
| 4 | — | m6A regulation of cortical and retinal neurogenesis is mediated by the redundant m6A readers YTHDFs | (journal not captured) | — | PMC9418916 | `SEARCH_SNIPPET` |
| 5 | — | YTHDF1 promotes mRNA degradation via YTHDF1–AGO2 interaction and phase separation | (journal not captured) | — | PMC8780909 | `SEARCH_SNIPPET` |
| 6 | — (authors not captured) | N6-methyladenosine Modulates Messenger RNA Translation Efficiency | Cell | 2015 | PII S0092-8674(15)00562-0 | `SEARCH_SNIPPET` (title/journal/year/PII verbatim; authors not captured) |
| 7 | — | YTHDF1 Promotes Cyclin B1 Translation through m6A Modulation and Contributes to the Poor Prognosis of Lung Adenocarcinoma with KRAS/TP53 Co-Mutation | (journal not captured) | — | PMC8305181 | `SEARCH_SNIPPET` |
| 8 | — | Structural and Dynamic Insights into Redundant Function of YTHDF Proteins | J Chem Inf Model | — | doi 10.1021/acs.jcim.0c01029 | `SEARCH_SNIPPET` |
| 9 | — | Context-dependent functional compensation between Ythdf m6A readers | bioRxiv (preprint) | 2020 | doi 10.1101/2020.06.03.131441 | `SEARCH_SNIPPET` |

Nine verified references; sufficient, though several lack captured author lists and the student must complete the metadata on PubMed.

**9. `models_and_data`**
**One cancer line must be obtained** — strongly prefer the exact line used by whichever YTHDF1-specific cancer paper the student chooses as the test case, so the re-test is reagent-matched. HT-22 is a usable second cell type at no cost and is defensible here because YTHDF redundancy has been studied in neural development. Public data: accessions to be identified; the planned bioinformatics is a re-analysis of published YTHDF knockdown RNA-seq/ribosome-profiling sets computing translation efficiency **both** ways the two camps compute it, to demonstrate that the analysis choice drives the conclusion. That is a methodological result, not DEG+enrichment.

**10. `key_experiments`**
*Bench (all in hand):* (a) siRNA matrix — YTHDF1, YTHDF2, YTHDF3 singly; all three pairwise; triple; ≥2 siRNAs per gene. (b) **In every single condition, measure all three paralogs by qPCR and WB** — the compensation measurement, and the study's core contribution. (c) For 3–5 published YTHDF1 "translational targets," measure mRNA (qPCR) and protein (WB) and compute protein/mRNA ratio. (d) Actinomycin-D chase with qPCR time-course for mRNA half-life of the same targets. (e) Viability/proliferation across the matrix, to test whether the phenotype reported for single YTHDF1 knockdown requires YTHDF1 specifically or any reader. (f) Optional rescue by transfection of YTHDF1 and YTHDF2 constructs into the triple knockdown — tests interchangeability directly and is the strongest single experiment if the plasmids can be sourced cheaply.
*Gating requirements, flagged:* ribosome profiling and polysome fractionation are **unavailable**; protein/mRNA ratio is a legitimate but weaker proxy and must be labelled as such. m6A mapping is unavailable and not needed. No luciferase reporters (gating) — avoid designs that require them.

**11. `expected_and_negative_results`**
Symmetric and publishable either way. Substantial compensation plus loss of YTHDF1 specificity → a general methodological warning for a very large cancer literature. No compensation and preserved YTHDF1 specificity → direct support for the Genome Biology position using an independent assay, and a point Zaccara & Jaffrey's own commentary would have to address. Weakest outcome: compensation present but protein/mRNA ratios too noisy to call — mitigate by choosing targets with large published effect sizes and by running enough biological replicates (≥4) from the start.

**12. `difficulty_and_cost`**
Difficulty **2–3/5** — the cheapest and technically safest of the six. Estimate **¥25,000–45,000**. Must buy: cancer line + STR (~¥2,500–4,000); antibodies for YTHDF1/2/3 and 3–5 target proteins (~¥10,000–18,000); siRNA matrix (~¥5,000–9,000); actinomycin D, consumables, qPCR reagents (~¥6,000–10,000); optional plasmids (~¥1,500–4,000). No mouse work, no MS, no sequencing generation.

**13. `timeline_months`**
6–9. The shortest-risk path of the six and the right choice if the student's supervisor wants a near-certain publication rather than maximum impact.

**14. `target_journal_tier`**
Tier 2 RNA-biology / molecular biology. Realistic: **RNA**, **RNA Biology**, **Journal of Molecular Biology**. *Nucleic Acids Research* is out of reach without ribosome profiling. No promises.

**15. `reviewer_attacks`**
1. "Protein/mRNA ratio is not translation efficiency; you need ribosome profiling." Unavoidable and must be conceded; it caps the tier.
2. "Knockdown, not knockout — residual reader protein explains your negatives." Pre-empt with quantified residual protein and the triple-knockdown arm.
3. "This re-litigates a settled debate." Rebuttal: both camps published position papers in 2023 and 2024 and the 2024 commentary explicitly names the experiment still missing, so it is not settled.

**16. `prelim_ratings`**
Novelty **M–H** (the compensation measurement is genuinely new; the framing must carry the rest). Evidence-base **H**. Overlap-risk **M**.

---

# TOPIC 4

**1. `title_en`**
Testing the untested step of the glioma–neuron symbiosis hypothesis: does neuronal lactate consumption actually spare glucose for glioma cells?

**2. `core_question`**
In a glucose-limited co-culture, does a neuronal cell line's uptake of glioma-derived lactate measurably increase glucose availability to, and glycolytic/growth output of, the glioma cells — and is that benefit abolished when neuronal monocarboxylate transport is blocked?

**3. `hypothesis`**
The glucose-sparing step is real but small and strongly dependent on glucose scarcity: under glucose restriction, MCT-dependent neuronal lactate consumption will produce a measurable increase in glioma glucose availability and proliferation, and blocking neuronal MCT uptake will abolish it; under standard 25 mM glucose the effect will be undetectable. I.e. the hypothesis is correct in principle but its magnitude is conditional, which constrains the proposed therapeutic claim that MCT1+MCT2 should be co-targeted.

**4. `novelty_claim`**
New: the first direct experimental test of the central metabolic step of a hypothesis published in 2025 and explicitly presented as untested. This is **defining a limiting condition that constrains a popular model** — and the model is only months old, so the student is not entering a crowded field. Traps avoided: it is not a mechanism transplant, not an axis, not bioinformatics-plus-validation. It also uses HT-22 for the one role HT-22 can legitimately play — the neuronal lactate consumer — rather than pretending it is a tumour model.

**5. `state_of_the_art`**
"Glioma neuron symbiosis: a hypothesis" (PMID 41098857, PMC12518321, `SEARCH_SNIPPET`) and its companion mechanistic-considerations paper (PMC13194419, `SEARCH_SNIPPET`) propose that lactate moves from glioma (MCT4, possibly MCT2) to neuron (MCT1), that neurons burn it and thereby spare glucose for the "hexose-hungry" glioma, and that effective MCT inhibitors should therefore target MCT1 and MCT2 together. The search result characterised this explicitly as a hypothesis, with statements such as "neurons regularly benefit from the endless supply of glioma-produced lactate" and "similarly to astrocytes, glioma cells could supply neurons with lactate." The supporting background is solid: lactate shuttling from glia to neurons via MCT1/4 and MCT2 is established (PMID 33132853, `SEARCH_SNIPPET`), and glioma lactate is demonstrably consumed by other cells in the microenvironment — a 2026 review reports glioma-derived lactate taken up by macrophages via MCT1 under hypoxia (`SEARCH_SNIPPET`). Separately, lactate is established as a driver of glioma biology: CBX3-regulated histone lactylation remodels glioblastoma immunity (JCI 2024, `SEARCH_SNIPPET`); H3K9 lactylation confers temozolomide resistance (PMC11109612, `SEARCH_SNIPPET`); H4K8 lactylation tracks malignant progression (Theranostics, `SEARCH_SNIPPET`).

**6. `specific_open_problem`**
The hypothesis' load-bearing step — that neuronal lactate consumption *returns a measurable glucose benefit to the tumour* — has never been measured in any system. The literature documents lactate transfer in one direction and infers the economic consequence. Whether the spared glucose is quantitatively sufficient to matter, and at what ambient glucose concentration, is entirely open; the therapeutic recommendation (co-target MCT1 and MCT2) rests on it.

**7. `delta_vs_closest_paper`**
Closest papers: the two 2025 glioma–neuron symbiosis papers themselves (PMC12518321 / PMC13194419). They are hypothesis and commentary with no new experiments on this step. The delta is total: this is the first measurement. The contrast case in the literature — glioma lactate consumed by macrophages via MCT1 — tests a different recipient cell and does not address glucose sparing.

**8. `references`**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | — (authors not captured) | Glioma neuron symbiosis: a hypothesis | (journal not captured) | 2025 | PMID 41098857; PMC12518321 | `SEARCH_SNIPPET` |
| 2 | — | The glioma neuron symbiosis hypothesis — cellular and molecular mechanistic considerations | (journal not captured) | 2025/2026 | PMC13194419 | `SEARCH_SNIPPET` |
| 3 | — | Lactate Transporters Mediate Glia-Neuron Metabolic Crosstalk in Homeostasis and Disease | (journal not captured) | 2020 | PMID 33132853 | `SEARCH_SNIPPET` |
| 4 | — | Lactate reprograms glioblastoma immunity through CBX3-regulated histone lactylation | J Clin Invest | 2024 | jci.org/articles/view/176851; PMC11563687 | `SEARCH_SNIPPET` |
| 5 | — | Histone H3K9 Lactylation Confers Temozolomide Resistance in Glioblastoma via LUC7L2-Mediated MLH1 Intron Retention | (journal not captured) | — | PMC11109612 | `SEARCH_SNIPPET` |
| 6 | — | Lactate Induces the Expressions of MCT1 and HCAR1 to Promote Tumor Growth and Progression in Glioblastoma | (journal not captured) | — | PMC9097945 | `SEARCH_SNIPPET` |
| 7 | — | Histone H4K8 lactylation promotes glioblastoma progression by inducing NUPR1-mediated autophagosome–lysosome fusion | Theranostics 16:4427 | — | thno.org/v16p4427 | `SEARCH_SNIPPET` |
| 8 | — | MCT2 Expression and Lactate Influx in Anorexigenic and Orexigenic Neurons of the Arcuate Nucleus | (journal not captured) | — | PMC3637215 | `SEARCH_SNIPPET` |

Eight verified; adequate, but author/journal metadata must be completed from PubMed.

**9. `models_and_data`**
HT-22 (in hand) as the neuronal consumer. **One glioma line must be obtained** — U87MG or U251 are the realistic choices; note that U87's provenance is itself contested in the literature and STR authentication is non-negotiable here. Transwell co-culture (cheap inserts) rather than direct mixing, so the two populations stay separable for lysis. No public dataset is central; TCGA/CGGA could be used only to check whether MCT/LDH expression patterns are consistent with the model, and the student should keep that strictly secondary so the paper is not mistaken for a bioinformatics paper.

**10. `key_experiments`**
*Bench (in hand plus cheap kits):* (a) Baseline characterisation: glucose consumed and lactate produced/consumed per cell per hour for HT-22 and the glioma line in monoculture at 2.5, 5 and 25 mM glucose, using colorimetric glucose and lactate kits. **This is the make-or-break experiment and must come first** — if HT-22 is a net lactate producer rather than consumer, the project stops at month 3 with a cheap, honest answer. (b) Transwell co-culture at matched total cell number, measuring medium glucose and lactate over time; the test is whether glioma-side glucose availability is higher than in a glioma-only control at equal cell density. (c) Blockade arm: knock down MCT2 (*Slc16a7*) in HT-22 by siRNA (in hand), and separately use the cheap pan-MCT inhibitor α-cyano-4-hydroxycinnamate; prediction is loss of the benefit. (d) Glioma output readouts: viability/proliferation (in hand), plus WB for phospho-S6 and phospho-AKT as nutrient-sensing readouts, plus pan-Kla as a lactate-exposure readout. (e) Reciprocal control: HT-22 viability and pan-Kla under glioma-conditioned medium, to document the neuronal side of the exchange.
*Gating requirements, flagged:* ¹³C isotope tracing is the definitive assay for carbon transfer and is **unavailable** (outsourced metabolomics with tracing is well above this budget) — the student substitutes mass-balance arithmetic from the colorimetric kits and must state the limitation. Seahorse unavailable. No animal work.

**11. `expected_and_negative_results`**
A clean negative — no measurable glucose sparing at any glucose concentration — **is publishable**, because the hypothesis is recent, explicit, prominent, and carries a therapeutic recommendation. That is the main reason this topic survives committee. The risk is a *third* outcome: HT-22 behaves as a glycolytic proliferating cell rather than a lactate-consuming neuron, which would make the result uninformative about real neurons. In that case the honest paper is small and the student should pivot. I rate that risk as substantial — see attacks.

**12. `difficulty_and_cost`**
Difficulty **3–4/5**. Estimate **¥25,000–45,000**. Must buy: glioma line + STR (~¥2,500–4,000); glucose and lactate colorimetric kits in quantity (~¥4,000–8,000 — this is a high-replicate study); transwell inserts (~¥3,000–6,000); MCT2 siRNA and CHC (~¥2,000–4,000); antibodies for MCT1/MCT2/MCT4, LDHA/B, pS6, pAKT, pan-Kla (~¥10,000–18,000); consumables (~¥4,000–6,000). Difficulty is driven by assay precision, not by expensive equipment: medium metabolite differences will be small and the student needs tight cell-number normalisation and many replicates.

**13. `timeline_months`**
8–12. Month 3 is a hard go/no-go gate on the HT-22 lactate-consumption result.

**14. `target_journal_tier`**
Tier 2–3 neuro-oncology / neurochemistry. Realistic: **Journal of Neuro-Oncology**, **Neuro-Oncology Advances**, **Journal of Neurochemistry**. A clean negative might also suit **ASN Neuro**. No promises.

**15. `reviewer_attacks`**
1. **"HT-22 is not a neuron."** The strongest and most likely fatal objection — HT-22 is an immortalised proliferating line, is highly glycolytic, and lacks mature neuronal phenotype without differentiation. Mitigation: differentiate HT-22 before assay and document marker induction by WB/qPCR; frame conclusions about "a neuronal cell line," never "neurons"; concede that primary neurons are required for the definitive test. The student must accept that this caps the paper.
2. "Without isotope tracing you have not shown carbon transfer." Conceded; mass balance plus MCT blockade is the fallback.
3. "Transwell co-culture at non-physiological glucose does not model peritumoural brain." Conceded; the glucose-dependence curve is the honest answer.

**16. `prelim_ratings`**
Novelty **H** (direct test of a months-old, explicitly untested hypothesis). Evidence-base **M** (the hypothesis papers are prominent but the surrounding primary evidence for this specific step is thin, and several of my references lack captured author/journal metadata). Overlap-risk **L** (very few groups will bother testing someone else's hypothesis paper). **Feasibility risk H** — this is the topic most likely to fail for reagent reasons, and I rank it fourth for that reason alone.

---

# TOPIC 5

**1. `title_en`**
Which tumour-derived signal dominates Schwann cell repair-phenotype induction? A head-to-head blockade arbitration of PGE2, extracellular-vesicle IL-8/CCL2, and TGF-β

**2. `core_question`**
When a Schwann cell line is exposed to pancreatic-cancer-conditioned medium, which single blockade — COX-2/EP-receptor, IL-8/CXCR1-2, TGF-β receptor, or EV-release inhibition — abolishes induction of the repair markers (c-JUN, NGFR/p75, SOX2, loss of myelin-program genes) and the associated migratory phenotype, and are their contributions additive or dominated by one pathway?

**3. `hypothesis`**
The three published inducers are not independent: PGE2 is the proximal dominant signal, and the apparent EV/IL-8 and TGF-β contributions will prove largely non-additive with COX-2 blockade, because they converge on the same c-JUN-dependent repair program. Prediction: COX-2/EP blockade alone will abolish most marker induction; adding IL-8 or TGF-β blockade on top will add little.

**4. `novelty_claim`**
New: a dose-controlled, same-system comparison of three separately published inducers of one phenotype, testing dominance versus additivity. This is **defining a limiting condition that constrains a popular model** — the model being "tumours induce repair Schwann cells, therefore block it." Traps avoided: not a new axis, not a model swap, not scRNA-seq re-description. It explicitly does not claim to discover a new inducer; it asks which of the known ones carries the signal, which is the question the therapeutic literature needs answered and has not asked.

**5. `state_of_the_art`**
Schwann cell dedifferentiation to a repair phenotype — increased neurotrophic factor secretion, increased proliferation and migration, elongated Büngner-band-like morphology — is now central to perineural invasion in PDAC (Front Pharmacol 2025, doi 10.3389/fphar.2025.1540027, `SEARCH_SNIPPET`). Three inducers are published independently: tumour-secreted PGE2 acting on Schwann cell EP receptors (Signal Transduct Target Ther, doi 10.1038/s41392-026-02648-x, `SEARCH_SNIPPET`); tumour extracellular vesicles via IL-8 (PMID 37425927, `SEARCH_SNIPPET`) and via IL-8/CCL2 (In Vitro Models 2025, doi 10.1007/s44164-025-00083-w, `SEARCH_SNIPPET`); and TGF-β from CAFs and macrophages. A 2025 Cancer Cell study using integrated single-cell and spatial transcriptomics resolved distinct Schwann subsets in invaded nerves, including a Büngner-band-like repair subset and a distinct TGFBI⁺ subset promoting neural invasion (PII S1535-6108(25)00270-3, `SEARCH_SNIPPET`). A downstream loop is also described: Schwann-derived CCL2 recruits macrophages that release cathepsin B to degrade the perineurium, with macrophage GDNF promoting invasion.

**6. `specific_open_problem`**
Which inducer dominates in vivo is explicitly unsettled, and the candidate interventions (PTGES/PGE2 blockade, IL-6R, CCR2, L1CAM) are all preclinical with no evidence that blocking Schwann reprogramming alone reduces invasion. Nor is it known how the transcriptomically defined subsets map onto the in vitro phenotype. The cheapest unasked question is the dominance question: all three inducers have only ever been tested one at a time, in different systems, at uncontrolled doses.

**7. `delta_vs_closest_paper`**
Closest paper: **"Prostaglandin E2-driven dedifferentiation of Schwann cells leads to perineural invasion in pancreatic ductal adenocarcinoma," Signal Transduct Target Ther, doi 10.1038/s41392-026-02648-x.** It establishes PGE2 as sufficient and necessary *within its own system* but does not compare it against EV/IL-8 or TGF-β, and does not test additivity. The delta is the combinatorial blockade matrix in one system with one conditioned medium and one marker panel — the comparison the field has not run.

**8. `references`**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | — | Prostaglandin E2-driven dedifferentiation of Schwann cells leads to perineural invasion in pancreatic ductal adenocarcinoma | Signal Transduct Target Ther | 2026 | doi 10.1038/s41392-026-02648-x | `SEARCH_SNIPPET` |
| 2 | — | Pancreatic Tumor-Derived Extracellular Vesicles Stimulate Schwann Cell Phenotype Indicative of Perineural Invasion via IL-8 Signaling | (journal not captured) | 2023 | PMID 37425927 | `SEARCH_SNIPPET` |
| 3 | — | Pancreatic cancer extracellular vesicles stimulate Schwann cell activation and perineural invasion in vitro via IL-8/CCL2 | In Vitro Models | 2025 | doi 10.1007/s44164-025-00083-w | `SEARCH_SNIPPET` |
| 4 | — | Integrated single-cell and spatial transcriptomics uncover distinct cellular subtypes involved in neural invasion in pancreatic cancer | Cancer Cell | 2025 | PII S1535-6108(25)00270-3 | `SEARCH_SNIPPET` |
| 5 | — | The supporting role of Schwann cells in perineural invasion of pancreatic ductal adenocarcinoma | Front Pharmacol | 2025 | doi 10.3389/fphar.2025.1540027 | `SEARCH_SNIPPET` |
| 6 | — | Increased nerve density adversely affects outcome in colorectal cancer and denervation suppresses tumor growth | J Transl Med | 2025 | doi 10.1186/s12967-025-06104-2 | `SEARCH_SNIPPET` |
| 7 | — | Tumor-infiltrating nerves: unraveling the role of cancer neuroscience in tumorigenesis, disease progression, and emerging therapies | (journal not captured) | 2025 | PMC12214194 | `SEARCH_SNIPPET` |

Seven verified; above the five-reference bar but with thin author metadata.

**9. `models_and_data`**
**Two lines must be obtained:** a PDAC line (PANC-1 or BxPC-3) and a Schwann cell line. A rat Schwann line is the cheap, widely available option in China; the student must verify availability and STR/species authentication before committing, and must concede the rat-line species mismatch with human tumour-conditioned medium in the paper. HT-22 is **not** appropriate here — it is a central nervous system neuronal line and has no role in a peripheral-nerve invasion model; I would reject any design that smuggled it in. Public data: the Cancer Cell 2025 study's accession is "to be identified" and could be mined to check whether the student's in vitro marker panel matches the repair subset signature — a legitimate, bounded bioinformatics component.

**10. `key_experiments`**
*Bench (in hand):* (a) Conditioned-medium dose-response to establish a submaximal induction dose — essential, because blockade experiments at saturating dose cannot show dominance. (b) Blockade matrix: COX-2 inhibitor (celecoxib) or EP2/EP4 antagonist; IL-8/CXCR1-2 blockade; TGF-β receptor inhibitor (SB431542, cheap); EV-release inhibition (GW4869) — each alone, all pairwise, all three. (c) Readouts by WB and qPCR: c-JUN, NGFR/p75, SOX2, GFAP, S100B, plus secreted GDNF and NGF transcripts. (d) Phenotype: wound-healing and transwell migration (in hand). (e) Add-back: recombinant PGE2, IL-8 and TGF-β alone and combined into plain medium, to test sufficiency at matched potency.
*Gating requirements, flagged:* proper EV isolation requires ultracentrifugation (**unavailable**); GW4869-mediated release inhibition plus 100 kDa ultrafiltration of conditioned medium is the substitute and is weaker — the student must concede this and must **not** claim to have isolated exosomes. Recombinant cytokines and EP antagonists are the budget risk. Co-culture with DRG neurons and any in vivo sciatic-nerve invasion model are out of scope.

**11. `expected_and_negative_results`**
A dominance result (PGE2 explains most of it) is a useful constraint on therapeutic strategy. A strict-additivity result is also informative — it would mean no single blockade will work, which matters for the drug-development claims. The weak outcome is partial, noisy, non-separable effects, which is a real possibility with conditioned medium; mitigate with the submaximal-dose design and the recombinant add-back arm, which is interpretable even if the blockade arm is messy.

**12. `difficulty_and_cost`**
Difficulty **3–4/5**. Estimate **¥35,000–65,000** — the most expensive of the six. Must buy: two cell lines + STR (~¥5,000–8,000); antibody panel (~¥14,000–22,000); recombinant PGE2, IL-8, TGF-β (~¥5,000–10,000); inhibitors incl. EP antagonists, which are the pricey item (~¥6,000–14,000); IL-8 neutralising antibody or CXCR1-2 antagonist (~¥3,000–8,000); consumables (~¥5,000–8,000). **This may exceed ¥60,000 and should be flagged to the supervisor up front.**

**13. `timeline_months`**
9–12. Two new lines to establish, a dose-response to build, and a 15-condition matrix — this is the tightest fit to the 12-month ceiling and I would not recommend it if the deadline is firm.

**14. `target_journal_tier`**
Tier 2–3 cancer cell biology. Realistic: **Experimental Cell Research**, **Molecular Carcinogenesis**, **Journal of Neuro-Oncology**. No promises. I advise against Frontiers/MDPI venues here for the reasons given in the landscape.

**15. `reviewer_attacks`**
1. "In vitro only, no nerve, no animal — you cannot speak about perineural invasion." Largely valid; the paper must claim only the Schwann-phenotype-induction question.
2. "A rat Schwann line responding to human tumour medium is not a model." Must be conceded explicitly.
3. "GW4869 plus ultrafiltration is not EV depletion." Conceded; the EV arm is the weakest and should be presented as exploratory.

**16. `prelim_ratings`**
Novelty **M** (an arbitration, but of in vitro inducers rather than of a controversy with stakes as high as Topics 1–2). Evidence-base **M–H**. Overlap-risk **M–H** — this is a hot, well-funded field with many Chinese PDAC labs, and an undergraduate will be outrun. I rank it fifth.

---

# TOPIC 6

**1. `title_en`**
Dose sufficiency as the missing test in exosomal microRNA signalling: can the miRNA copy number vesicles can plausibly deliver change a target protein at all?

**2. `core_question`**
If a recipient cancer cell receives a synthetic miRNA mimic titrated down to the intracellular copy number that extracellular vesicles could realistically deliver, does the target protein claimed in the published literature change — or does target repression require doses orders of magnitude above what vesicle stoichiometry permits?

**3. `hypothesis`**
Target repression will require mimic doses one to three orders of magnitude above the EV-deliverable copy number, implying that a large body of "tumour-derived exosomal miR-X transfers to recipient cell Y and represses target Z" conclusions are quantitatively unsupported by their own transfer mechanism and are instead driven by co-transferred protein, by bulk-dose transfection artefacts, or by endogenous miRNA induction in the recipient.

**4. `novelty_claim`**
New: the decisive arm of this study requires **no vesicles at all** — it is a dose-response of a synthetic mimic against a published target, which converts a famously hard quantitative objection into a cheap, in-hand experiment. This is a **reagent-independent re-test of a widely cited but shaky claim** plus a **measurement that discriminates competing explanations**. Traps avoided: it is the exact inverse of the "we found miRNA X regulates Y in cancer Z" trap — it tests whether that entire sentence form is dose-plausible.

**5. `state_of_the_art`**
The quantitative objection is old, specific, and never resolved. Chevillet et al. (PNAS 2014, PMID 25267620, `SEARCH_SNIPPET`) measured a mean of 0.00825 ± 0.02 miRNA molecules per exosome across six sources — roughly one copy per 121 exosomes, ranging from one per 9 to one per 47,162 — across preparations spanning two orders of magnitude in concentration (6.06 × 10⁷ to 7.79 × 10⁹ exosomes/µL), and concluded that current mechanistic models for exosome-mediated miRNA communication may need to be revised. Counter-evidence exists but is inconsistent: a neural stem cell study reported at least 10 copies per exosome (PLoS One 2016, `SEARCH_SNIPPET`); a 2022 review argued that functional low-level transfer does not fit conventional reductionist stoichiometric concepts (`SEARCH_SNIPPET`); single-vesicle TIRF work argues qPCR cannot determine precise stoichiometry (`SEARCH_SNIPPET`). Reported stoichiometry across studies spans 10⁻⁵ to ~10 copies per vesicle — a 10⁶-fold disagreement.

**6. `specific_open_problem`**
The debate has been conducted entirely on the **supply** side — how many copies are in a vesicle — using methods that disagree by six orders of magnitude. The **demand** side has never been measured: nobody has asked what intracellular copy number is actually required to move a specific published target protein in a specific recipient cell. Until that number exists, the stoichiometric objection cannot be settled either way, and it is cheap to obtain.

**7. `delta_vs_closest_paper`**
Closest paper: **Chevillet et al., PNAS 111(41):14888–14893 (2014), PMID 25267620, doi 10.1073/pnas.1408301111.** It quantifies supply and leaves the functional threshold unaddressed. The delta: this study measures the demand threshold directly, in a cancer line, against a target protein nominated by a specific published exosomal-miRNA paper, and then compares the two numbers. No study I located does this.
**Required pre-check before committing:** I could not verify in this session that the dose-sufficiency arm has not already been published. The student must run a dedicated literature search on EV-miRNA functional dose thresholds before starting, and abandon the topic if it has.

**8. `references`**
| # | authors (short) | title | journal | year | PMID / DOI | verification |
|---|---|---|---|---|---|---|
| 1 | Chevillet et al. | Quantitative and stoichiometric analysis of the microRNA content of exosomes | PNAS 111(41):14888–14893 | 2014 | PMID 25267620; doi 10.1073/pnas.1408301111 | `SEARCH_SNIPPET` |
| 2 | — | Investigation of Content, Stoichiometry and Transfer of miRNA from Human Neural Stem Cell Line Derived Exosomes | PLoS One | 2016 | doi 10.1371/journal.pone.0146353; PMC4713432 | `SEARCH_SNIPPET` |
| 3 | — | Exosome Carrier Effects; Resistance to Digestion in Phagolysosomes May Assist Transfers to Targeted Cells; II Transfers of miRNAs Are Better Analyzed via Systems Approach as They Do Not Fit Conventional Reductionist Stoichiometric Concepts | Int J Mol Sci | 2022 | doi 10.3390/ijms23116192 | `SEARCH_SNIPPET` |
| 4 | — | Total internal reflection-based single-vesicle in situ quantitative and stoichiometric analysis of tumor-derived exosomal microRNAs for diagnosis and treatment monitoring | Theranostics 9:4494 | — | thno.org/v09p4494 | `SEARCH_SNIPPET` |
| 5 | — | Quantification of Exosomes | (journal not captured) | 2016 | PMC5039048 | `SEARCH_SNIPPET` |
| 6 | — | Exosomal microRNAs (exomiRs): Small molecules with a big role in cancer | (journal not captured) | 2018 | PMC5831981 | `SEARCH_SNIPPET` |

Six verified; meets the bar, but this is the **thinnest evidence base of the six topics** and most of it predates 2017, which is itself a warning that the field has moved on without resolving the objection.

**9. `models_and_data`**
**One cancer line must be obtained** — ideally the exact donor/recipient pair from a specific published exosomal-miRNA paper so the re-test is matched. Choosing a target protein with a large, repeatedly reported effect size is essential. Public data: not central; accessions to be identified if the student wants to check target-expression context.

**10. `key_experiments`**
*Bench, decisive arm (all in hand):* (a) Absolute quantification of the chosen miRNA by qPCR against a synthetic oligonucleotide standard curve — gives copies per µg RNA and, with a cell count, copies per cell. (b) **Mimic dose-response spanning ~5 logs**, from a few copies-per-cell equivalent up to the conventional 50 nM, reading out target protein by WB and target mRNA by qPCR; the output is the threshold dose. (c) Calibration of delivered copy number using a labelled mimic to bound transfection efficiency — this is the key uncertainty and must be bounded, not assumed. (d) Endogenous-induction control: measure whether the recipient's own copy number of that miRNA rises after conditioned-medium exposure, which is an alternative explanation for apparent transfer.
*Supply arm, gated and optional:* EV preparation requires ultracentrifugation (**unavailable**); polymer-precipitation kits are cheap but are specifically distrusted by EV reviewers. Particle counting requires nanoparticle tracking analysis, which must be **outsourced** (~¥300–800/sample in China). **Recommendation: build the paper on the demand arm and cite published supply numbers.** Attempting the supply arm with kit preps will invite rejection.

**11. `expected_and_negative_results`**
If the threshold dose is far above EV-deliverable copy numbers, the result is a general quantitative constraint on a very large literature — high value. If the target moves at near-single-copy-per-cell doses, that is a genuine surprise supporting low-stoichiometry signalling and is equally publishable. The failure mode is not a negative result but an uninterpretable one: if delivered copy number cannot be bounded, the whole comparison collapses. That is why (c) is load-bearing and must be validated in month 2.

**12. `difficulty_and_cost`**
Difficulty **4/5** — highest of the six, because the central number depends on a delivery-efficiency estimate the student's toolkit bounds only loosely. Estimate **¥30,000–60,000**. Must buy: cancer line + STR (~¥2,500–4,000); synthetic mimics, labelled mimic and oligo standards (~¥4,000–8,000); target and control antibodies (~¥8,000–14,000); qPCR reagents at high replicate count (~¥6,000–10,000); outsourced NTA if the supply arm is attempted (~¥3,000–8,000); consumables (~¥5,000–8,000).

**13. `timeline_months`**
9–12. Tight, and the month-2 delivery-calibration gate is unforgiving.

**14. `target_journal_tier`**
Tier 2–3. Realistic: **Journal of Extracellular Vesicles and Circulating Nucleic Acids**, **Journal of Cellular and Molecular Medicine**, **FEBS Open Bio**. *Journal of Extracellular Vesicles* is likely out of reach without a credible supply arm. No promises.

**15. `reviewer_attacks`**
1. "Transfection delivery is nothing like vesicle fusion — your dose comparison is apples to oranges (endosomal routing, RISC loading)." The most serious objection; the student can only bound it and must present the threshold as an order-of-magnitude estimate.
2. "You did not isolate EVs properly / at all." Unavoidable if the supply arm is skipped; turn it into a design choice and cite published stoichiometry.
3. "One miRNA, one target, one cell line — you cannot generalise to a literature." Fair; do not over-claim in the title or abstract.

**16. `prelim_ratings`**
Novelty **H**. Evidence-base **M–L** (six refs, mostly 2014–2016, and an unverified prior-art risk). Overlap-risk **L**. **Feasibility risk H.** I rank it sixth and include it because its novelty type is excellent — but I would only green-light it if Topics 1–3 are unavailable, and only after the prior-art pre-check.

---

# `domain_landscape`

**The real 2023–2026 frontier, as my searches found it.** The most active genuinely unsettled area intersecting this student's resources is **lactate-driven chromatin chemistry**, and it is unsettled in an unusually productive way: the primary literature now contains flat, dated contradictions rather than vague gaps. Since the founding Nature 2019 paper, six different mechanisms have been published for how a lactyl group reaches a lysine — p300/CBP, HBO1/KAT7 (Nat Commun 2024), AARS1 (Cell 2024), AARS1+AARS2 (Nature 2024), non-enzymatic transfer from lactoylglutathione (Cell Chem Biol 2019), and class I HDACs acting as *writers* (**J Biol Chem 2025**) — the last directly inverting an earlier report of the same enzymes as *delactylases*. The 2025 JBC paper reports that in HEK293T, knockdown of AARS1/AARS2, of CBP/p300/HBO1, and of GLO1 all failed to change global Kla, and that the pan-Kla antibody also detects carboxyethyl-lysine. Meanwhile **Nat Chem Biol 2024/2025** established L-lactyl as the dominant glycolysis-induced isomer, and an **October 2025 preprint** reported predominantly *D*-lactylation at H3K18 and H3K79 in mouse testis with total histone lactylation stoichiometry of only 0.01–0.44% against 25–35% for acetylation. A **2025 Theranostics** review states outright that these low levels make it hard to tell whether lactylation is regulatory or a metabolic by-product; a **2025 Nature Cell Biology** review and a **2026 Molecules** review both treat writer identity as open. Add two fully independent, separately published routes from lactate to chromatin — HDAC inhibition (Nucleic Acids Res 2012; load-bearing in the **Nat Commun 2022** CD8 T-cell stemness paper) and lactate as the carbon source for histone acetylation via nuclear LDHA (**Exp Mol Med 2023**, ~60% ¹³C incorporation into H4) — and the field's standard experiment, sodium lactate plus a pan-Kla blot, no longer licenses its standard conclusion. That gap is the opportunity in Topics 1 and 2. A parallel, equally arbitrable contradiction exists in m6A reader biology (Cell 2020 unified model vs Genome Biology 2023 rebuttal vs RNA 2024 defence), which is Topic 3. **Cancer neuroscience** is the other live frontier — 2025–2026 brought a Cancer Cell single-cell/spatial dissection of PDAC neural invasion, a Signal Transduct Target Ther paper on PGE2-driven Schwann dedifferentiation, a J Transl Med 2025 colorectal denervation study, and an explicitly untested **glioma–neuron symbiosis hypothesis (PMID 41098857)** — but it is capital-intensive and the undergraduate's entry point is narrow.

**The saturation and paper-mill problem, stated plainly.** I will not hand this student a prognostic signature, a risk model, a hub gene with two Westerns, or a nomogram, and the student should understand *why* beyond "it's crowded." A 2025 cross-sectional study found paper-mill retractions concentrate in journals with a specific profile — high open-access share, mid-quartile impact factor, high volume of citable items, medicine and health categories — and that of 1,143 paper-mill retractions, 96.8% had all listed authors at Chinese institutions and 76.9% listed a hospital as primary affiliation. A Chinese clinical-medicine undergraduate submitting a TCGA signature paper to a mid-quartile OA oncology journal is submitting into the exact demographic and venue profile editors now screen hardest; one cancer journal alone has over 100 paper-mill retractions, and a 2025 bioRxiv preprint reports AI screening of cancer publications at 0.91 accuracy while arguing detected papers are a fraction of the true prevalence. **Mendelian randomization is now in the same position**, which matters because this student is willing to learn MR: PLOS One began pre-screening MR submissions in April 2024 and reports a high rejection rate; PLOS Genetics states such manuscripts are "almost invariably rejected during editorial review"; Scientific Reports requires STROBE-MR; JCEM says it will reject without review. A standalone two-sample MR paper is close to unpublishable in a reputable venue. Public data is still usable here — but only, as in Topics 1 and 3, to answer a mechanistic or methodological question that does not reduce to DEG plus correlation plus enrichment.

**Honest read on undergraduate opportunity.** Narrow but real. The student cannot do discovery-mode oncology — no co-IP, MS, ChIP, flow, lentivirus or CRISPR means no new mechanism can be built. But PTM and RNA-modification *arbitration* turns on siRNA efficiency, antibody specificity, dose controls and careful Westerns, which is precisely what this student has. The decisive advantage is structural: in Topics 1–3 **both answers are results**, so there is no branch that yields an unpublishable year. Two further practical notes. First, outsourced RNA-seq in China is now roughly ¥600–1,200 per sample, so 6–12 samples sit inside this budget; that is worth knowing, but none of my six topics needs it, and adding it would pull them back toward the genre to avoid. Second, these are scoopable projects — a funded lab could do Topic 2 in three months. A bioRxiv preprint around month 8 is not optional.

**My recommendation: Topic 2, with Topic 3 as the low-risk alternative.** Topic 2 has the cheapest decisive controls, the shortest timeline, and an interpretable result in every branch. Topic 3 is the safest route to a publication if the supervisor wants near-certainty over impact. Topic 1 is the best follow-on. Do not attempt Topics 1 and 2 together. Do not do mouse work for any of these — a xenograft would add 4–6 months and ¥15,000–40,000 and would not strengthen a single one of these arguments.

---

# `rejected_ideas`

1. **"LncRNA/circRNA/miR-X regulates target Y in cancer Z."** The explicitly named trap and the single most paper-mill-associated genre in oncology; a student from the exact author profile that 96.8% of paper-mill retractions share should not go near it.
2. **TCGA/GEO prognostic signature, risk model, nomogram or hub-gene screen with validating Westerns.** Ruled out by the committee's own brief and by the retraction-profile evidence above; also unvalidatable with this student's toolkit.
3. **Standalone two-sample Mendelian randomization of a metabolite, protein or exposure against cancer risk.** PLOS Genetics states these are almost invariably rejected at editorial review and PLOS One pre-screens them; it would also contain no mechanism.
4. **"Lactylation of protein X promotes cancer Y via pathway Z."** The field's current mass-production format; requires PTM mass spectrometry, site-mutant rescue and co-IP (all gating), and adds nothing while the writer, eraser, isomer and antibody questions in Topics 1–2 remain open.
5. **FTO m6A-versus-m6Am substrate re-test** (Mauer FEBS Lett 2018 vs Mol Cell 2018, PMID 30197295). Genuinely unresolved and a tempting arbitration, but the only affordable readouts (m6A dot blot or ELISA) are far too noisy to adjudicate it; it needs LC-MS/MS of nucleosides, which is gating.
6. **TAK-981/subasumstat mechanism — global SUMO loss versus a specific IFN-linked response**, where a CLL T-cell study reports IFNAR-independence against an NK-cell preprint's IFN-dependence. Real controversy, but the decisive readouts are interferon induction in primary immune cells, requiring flow cytometry and primary cell culture; the drug is also costly.
7. **Lactic-acid-versus-lactate-anion arbitration in CD8 T cells** (Nat Commun 2022 stemness vs the suppressive consensus, with a preprint proposing acidosis as the confound). An excellent question, and the acid/anion confound is the right discriminator — but it needs primary T cells, cytokine readouts and flow cytometry. The chromatin half of it survives as Topic 2.
8. **GPR81/HCAR1 receptor arm versus intracellular lactylation as the carrier of lactate's transcriptional effect.** Feasible with siGPR81 plus MCT blockade and worth doing, but it overlaps Topic 2's control structure so heavily that running both would produce one diluted paper rather than two.
9. **scRNA-seq re-analysis defining a new TAM or Schwann or CAF subset.** Descriptive, saturated, and the student cannot validate a subset without flow cytometry or spatial methods; the Cancer Cell 2025 PDAC study shows what a properly resourced version looks like.
10. **Molecular docking of a natural compound onto a lactylation enzyme, with claimed mechanism.** No causal content; an explicitly listed trap.
11. **DNPH1 as an MR-nominated breast-cancer risk protein tested in cells (deferred, not rejected).** This would have been a genuine "specific prediction from human genetics nobody tested in cells." `DNPH1` appeared verbatim in a result as one of five proteins with a potential causal role in breast cancer risk (CD160, DNPH1, LAYN, LRRC37A2, TLR1), but my search budget ran out before I could verify the direction of effect or the reported PARP-inhibitor/hmdU connection. **Status: `UNVERIFIED`, needs verification — no DOI or PMID given, no digits guessed.** If the student wants a human-genetics-to-cells topic, this is the one worth two hours of searching; the design would be siDNPH1 plus a PARP inhibitor with viability and γH2AX readouts, all within current techniques.
