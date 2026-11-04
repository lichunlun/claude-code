# Chair-level verified cross-cutting findings (WebSearch-verified in session 2026-11-04)

## A. MR papers: NOT banned, but bar raised sharply  [VERIFIED]
- PLOS One editorial (Nov 2025): extra editorial screening since April 2024, mandatory STROBE-MR checklist;
  rejections by editorial staff increased, acceptances decreased. ~1800 MR submissions in 2024; 919 by Aug 2025.
  PMID 41252429 ; DOI 10.1371/journal.pone.0337199
- PLOS Genetics editorial (Jul 2025): "critical flaws ... in many MR studies, including numerous manuscripts
  submitted to PLOS Genetics". DOI 10.1371/journal.pgen.1011767
- Diabetologia editorial (Jul 2025) "Raising the bar...": acceptance rate for MR fell 24% -> 4% over 5 yrs.
  DOI 10.1007/s00125-025-06484-6
- Frontiers in Endocrinology retraction of MR immune-cells/diabetic nephropathy paper (PMC11880894).
- J Infect Dis editorial: retraction of an MR paper for IV assumption violation. (academic.oup.com/jid/article/232/3/525/8152352)
=> IMPLICATION FOR SCORING: naive two-sample MR = high overlap risk + real rejection risk. MR acceptable ONLY as
   cis-pQTL/eQTL drug-target MR + coloc that yields a bench-testable target.

## B. Bioinformatics-oncology signature genre: contaminated  [PARTIALLY VERIFIED]
- Could NOT verify an editorial that names TCGA/hub-gene papers as paper-mill product. Do not overclaim.
- DID verify two 2025 retractions of "XXX-related gene prognostic signature" papers:
  - Disease Markers, ferroptosis-related gene signature + HSF1, uterine carcinosarcoma, retracted Jul 2025
    (figure panel duplication + peer-review process concerns). PMC12303628
  - Oxid Med Cell Longev, pyroptosis-related gene signature in glioma, retracted Oct 2025
    (data validity; one author said they did not contribute). PMC12517977
- bioRxiv preprint 2025 (AI-based screening of cancer research publications, DOI 10.1101/2025.08.29.673016)
  — preprint, NOT peer reviewed; 433/3370 paper-mill papers were false negatives.
- Bibliometric study: oncology most affected field.
=> IMPLICATION: the genre carries guilt-by-association reputational risk. Say "saturated + reputational risk",
   NOT "journals have banned it".

## C. HT-22 model is systematically MISLABELED in the literature  [VERIFIED — potential topic]
- HT22 lack functional ionotropic glutamate receptors; glutamate kills them by GSH depletion =
  "oxidative glutamate toxicity" / "oxytosis", NOT receptor-mediated excitotoxicity.
- BUT: Neural Regen Res 2013 "Differentiation renders susceptibility to excitotoxicity in HT22 neurons"
  reports differentiated HT22 die by NMDA-receptor excitotoxicity while undifferentiated die by oxidative
  stress; and states it "remains unclear if HT22 cells are resistant to excitotoxicity because they do not
  express NMDA receptors". DOI 10.3969/j.issn.1673-5374.2013.14.006
- Many 2018-2023 papers nonetheless title their work "glutamate-induced excitotoxicity in HT22"
  (e.g. leptin/zinc PMC5954240 ; melatonin/mitophagy PMC6694460).
- Required glutamate is mM (non-physiological).
=> This is a genuine, documented, field-wide mislabeling + an unresolved question about differentiation state.
   Candidate topic category: "what does this model actually measure".

## D. oxytosis vs ferroptosis: live but LEANING-RESOLVED controversy  [VERIFIED]
- Front Neurosci 2018 review (PMC5920049) "Oxytosis/Ferroptosis-(Re-)Emerging Roles...": argues the two are
  "two names for the same death pathway". Oxytosis coined 2001 (glutamate oxidative death in neurons, studied
  almost exclusively in HT-22 for over a decade); ferroptosis named 2012 in tumor cells.
- Cell Chem Biol 2020 review (S2451-9456(20)30426-8) "Using the Oxytosis/Ferroptosis Pathway to Understand and
  Treat Age-Associated Neurodegenerative Diseases".
- Element 2026 review, Daolin Tang & Rui Kang, "Ten controversies defining the boundaries of ferroptosis",
  published 4 Aug 2026, oaepublish.com/articles/element.2026.07 — lists as OPEN: whether mitochondria are
  essential; whether iron actively drives vs merely permits; **whether ferroptosis inducers are truly specific**;
  whether therapeutic targeting is feasible or overhyped. Grouped into mechanistic definition / regulatory
  control / experimental interpretation / translational relevance.
- Still disputed per reviews: role of calpains; which pathway drives neuronal loss in vivo.
- HT22 evidence for shared mechanism: Orai3 KD protects vs glutamate oxytosis; Orai1+Orai3 KD protect vs
  RSL3 ferroptosis (shared Ca2+ influx).
=> CAUTION: "is oxytosis = ferroptosis" is mostly settled in reviews. Do NOT sell it as wide open.
   The genuinely open sub-questions are the Tang/Kang four.

## E. Canonical ferroptosis TOOL COMPOUNDS are not clean  [VERIFIED — strong topic seed]
- erastin activates mitochondrial VDAC; (1S,3R)-RSL3 affects selenoproteins besides GPX4 (PMID 42442865 entry).
- RSL3 triggers gasdermin cleavage / pyroptosis in cancer cells — Sci Rep 2025,
  DOI 10.1038/s41598-025-11368-1. Authors: "these molecules however have off-target effects and cannot provide
  a comprehensive picture of overlapping pathways".
- Necrostatin-1 (nominal RIPK1 inhibitor) prevents ferroptosis RIPK1- and IDO-independently (PMC8469492).
- ETC inhibitors suppress erastin- but NOT RSL3- or EC359-induced ferroptosis (PMC10308161) => inducers
  diverge mechanistically.
- erastin irreversibly inhibits system xc- without cysteine modification of the transporter (PMC5772355).
=> TOPIC SEED: tool-compound specificity audit in a NEURONAL context. Cheap (viability + WB + plate-reader
   probes), conceptually real, negative result informative, directly addresses a Tang/Kang listed controversy.

## F. Negative/replication results DO have indexed venues  [VERIFIED]
- microPublication Biology: PubMed/PMC indexed since 2020 (Caltech Library announcement); FAQ states it accepts
  negative results, replications, and unpublished observations; reviewers assign category (new finding /
  negative result / replication); peer-reviewed report of findings from a single experiment; bioRxiv
  co-deposit allowed. NOTE: could not confirm a one-figure limit — student must read author guidelines.
- ReproSci (bioRxiv 2025, DOI 10.1101/2025.07.07.663442 / .663460): 1006 claims from 400 Drosophila-immunity
  papers; 61% of claims verified; among 45 experimentally tested "unchallenged" claims, 38/45 non-replicable.
  STATUS: PREPRINT, submitted for peer review Oct 2025 — cite as preprint only.
  Authors note "low motivation to publish negative or contradictory results".
=> Negative results are publishable but usually in a LOWER tier or a dedicated venue. Be honest with the student.

## G. Ferroptosis INHIBITOR tool caveats  [PARTIALLY VERIFIED]
- Fer-1 / Lip-1 act as radical-trapping antioxidants (RTAs), NOT lipoxygenase inhibitors: ACS Cent Sci,
  "On the Mechanism of Cytoprotection by Ferrostatin-1 and Liproxstatin-1...", DOI 10.1021/acscentsci.7b00028
  (PMC5364454). "activity likely derives from their reactivity as radical-trapping antioxidants rather than
  their potency as inhibitors of lipoxygenases".
- Fer-1 is metabolically unstable, not suited to in vivo use.
- A recent item titled "A guide to using small molecule ferroptosis inhibitors" (PMC12879747) appeared in
  search results; details NOT confirmed -> TITLE_ONLY, needs verification.
- COULD NOT verify a source explicitly stating Fer-1/Lip-1 block non-ferroptotic deaths. That inference is
  mechanistically plausible (any lipid-peroxidation-dependent death) but is NOT established in a citable
  source from this session. DO NOT state it as fact.
- Armenta & Dixon, "Investigating Nonapoptotic Cell Death Using Chemical Biology Approaches", PMID 32220334
  (PMC7185180), 2020 -- closest thing to a tool-use methods reference.

## H. Epilepsy public datasets (GEO) -- accessions seen in search results  [SEARCH_SNIPPET]
- GSE63808  human hippocampus, pharmacoresistant TLE, microarray, ~150 samples (also ArrayExpress E-GEOD-63808)
- GSE127871 human hippocampal tissue RNA-seq, 12 intractable TLE patients
- GSE190451 human TLE hippocampus RNA-seq, 3 normal vs 3 TLE  (very small -- underpowered)
- GSE197015 kainic-acid mouse hippocampus RNA-seq
- GSE114701 miRNA, 20 TLE vs 20 control
- GSE44456, GSE28674, GSE104704, GSE7307, GSE163296, GSE11882 used in a 2025 8-dataset pooled analysis
  (287 samples: 110 normal, 177 TLE)
- GSE190452 = snRNA-seq of CORTEX, not hippocampus
- Springer 2025: "Identification of epileptic hippocampal sclerosis related genes through bulk and
  single-nucleus RNA sequencing datasets", DOI 10.1007/s00018-025-05959-4
=> ALL sample counts/platforms must be re-checked on the GEO page by the student. GEO was unreachable here.

## I. 2026 top-tier epilepsy mechanism paper (sets the bar / crowds the space)  [VERIFIED]
- "Enhanced Glycolysis-Driven Histone H3K18 Lactylation Regulates Epileptogenesis by Modulating the E3
  Ubiquitin Ligase COP1", Advanced Science, 29 May 2026, e16985, DOI 10.1002/advs.202516985, PMID 42210782.
  PKM2-driven glycolysis -> lactate -> H3K18la -> Cop1 transcription -> COP1 K48-ubiquitinates GABA-A
  receptor beta2 subunit -> proteasomal degradation -> reduced inhibition -> seizure susceptibility.
  PKM2 inhibition or Cop1 KO protective. Lactate + histone lactylation elevated in KA mice AND human
  epileptic brain tissue.
- Caveat found: Front Cell Neurosci 2024 review (DOI 10.3389/fncel.2024.1464169) concluded evidence was then
  INSUFFICIENT to confirm lactylation directly induces epilepsy via neuronal excitability.
- Review: "Lactylation in CNS disorders..." PMC11985781 ; "Role of Histone Lactylation in Neurological
  Disorders" PMC12386771. KAT2A writes H3K14la/H3K18la; HDAC1/HDAC3 are main delactylases.
=> IMPLICATION: epilepsy + lactylation is now OCCUPIED at high level by a 2026 Adv Sci paper. Any student
   topic here must not be a downstream echo of it. High overlap risk.

## J. CHAIR AUDIT HIT — the NLRP3 antibody-validation design ALREADY EXISTS (different tissue)  [VERIFIED]
Scout 1 proposed as its best-expected-value topic a "knockdown-validated reappraisal of neuronal
NLRP3/GSDMD detection" and rated overlap-risk LOW. My own audit contradicts that rating.

ALREADY PUBLISHED, same design, different tissue:
- "Issues with the Specificity of Immunological Reagents for NLRP3: Implications for Age-related Macular
  Degeneration", Scientific Reports 2017, DOI 10.1038/s41598-017-17634-1, PMC5764999.
  * Tested commercial anti-NLRP3 antibodies by WB, WT vs Nlrp3-knockout tissue.
  * Positive controls: mouse spleen, RAW264.7, THP-1.
  * Explicit stated aim: resolve "conflicting data published on AMD work" via reagent validation.
  * Result: "validated resources showed no NLRP3 expression in RPE in baseline, stimulated, healthy or
    diseased states"; concluded this "questions current interpretation of results reporting NLRP3
    expression and upregulation in AMD".
  * STRIKING DETAIL: for one antibody the band was NOT absent in knockout samples — it was HIGHER in the
    knockout tissue.

NOT yet done for neurons: two targeted searches returned NO paper reappraising neuronal NLRP3 in brain with
knockout-validated antibodies. Brain NLRP3 literature is microglia-centric (e.g. PMC9660492, Parkinson's SNc,
microglial NLRP3 knockdown acts on DA neurons INDIRECTLY via conditioned medium).

CONSEQUENCES — I am overriding Scout 1's ratings:
  (a) overlap-risk on the APPROACH: L -> M. The template is published and citable; a reviewer will know it.
  (b) trap-2 exposure ("mature method moved to a new tissue") is REAL and must be stated in the proposal,
      not hidden. Defensible framing: the contribution is not the method but the specific neuronal claim set
      plus two arms the 2017 paper lacks (quantitative cross-cell-type transcript abundance on one plate;
      human snRNA-seq cell-type assignment).
  (c) METHOD GAP: 2017 used genuine Nlrp3-KNOCKOUT tissue. The student has siRNA only. Partial knockdown is
      a strictly weaker specificity control, and the 2017 paper's own KO-higher-band result shows why.
      Must be conceded; mitigate with quantified knockdown efficiency + transcript-vs-band dose-response.
  (d) UPSIDE: the precedent proves the genre is publishable in a Sci Rep-tier venue, and supplies a
      ready-made validated-antibody strategy and positive-control panel.

## K. CHAIR AUDIT KILL — Scout 3's top-recommended topic has a BROKEN CENTRAL CONTROL  [VERIFIED]
Scout 3 (tumor/PTM) nominated as its "single top recommendation" a lactylation-arbitration study whose
decisive, near-free experiment was a **D-lactate control**: the argument being that D-lactate cannot generate
L-lactyl-CoA, so if D-lactate still raises the pan-Kla western signal, that signal is not L-lactylation.

That control does not work. Verified:
- Latham T et al., "Lactate, a product of glycolytic metabolism, inhibits histone deacetylase activity and
  promotes changes in gene expression", Nucleic Acids Research 40(11):4794-4803, 2012,
  DOI 10.1093/nar/gks066, PMID 22323521: **both** L- and D-lactate stimulate histone acetylation via HDAC
  inhibition. Latham also already matched doses "that had similar effects on histone H4 acetylation" when
  comparing lactate, TSA and butyrate -- i.e. the dose-matching idea has 2012 precedent.
- "L- and D-lactate enhance DNA repair and modulate the resistance of cervical carcinoma cells to anticancer
  drugs via histone deacetylase inhibition and hydroxycarboxylic acid receptor 1 activation",
  DOI 10.1186/s12964-015-0114-x, PMC4514991: **"D-lactate more potently inhibited cellular HDAC activity
  than L-lactate."**

WHY THIS IS FATAL TO THAT DESIGN: D-lactate is not an inert stereochemical control, it is a STRONGER HDAC
inhibitor than L-lactate. So a positive D-lactate result is uninterpretable -- it cannot distinguish
"the antibody signal is not L-lactylation" from "D-lactate inhibited HDACs harder". The one arm the scout
called "a near-free experiment with a binary interpretation" has no binary interpretation.

SECOND, INDEPENDENT PROBLEM with the same topic's dose-matched-HDACi arm: the predicted direction is
backwards. Search result: HDAC inhibitors "broadly decreased basal Kla levels and increased lysine
acetylation". The scout predicted dose-matched TSA would REPRODUCE the lactylation signal; the literature
says HDACi LOWERS Kla.

THIRD: the field contradicts itself on HDAC direction, which the student cannot resolve with WB/qPCR:
- "Class I histone deacetylases (HDAC1-3) are histone lysine delactylases", Science Advances,
  DOI 10.1126/sciadv.abi6696  -> HDACs are ERASERS.
- "Class I histone deacetylases catalyze lysine lactylation", JBC 2025, PMC11888385 (note: scout cited
  PMC12624779 for the same title; two PMC ids seen, must be checked) -> HDACs are WRITERS, and
  "HDAC-catalyzed Kla formation is the dominant mechanism of overall lysine lactylation".

VERDICT: the lactylation-arbitration topic drops from Scout 3's #1 to NOT RECOMMENDED for this student.
Novelty override: H -> M. Feasibility override: the decisive controls are not decisive.
The salvageable residue is the antibody peptide-competition arm alone, which is too thin for an
Original Article on its own.

LESSON TO CARRY INTO FILE 04: a cheap control is only decisive if it is clean. Three of five scouts
proposed "arbitration" topics; arbitration only works where the discriminating reagent is itself unconfounded.

## L. CHAIR AUDIT PASS (with a designed-around caveat) — the ISR/ER-stress attribution topic survives  [VERIFIED]
Scout 2's Topic 1 ("Is it really ER stress? kinase-resolved attribution of ATF4-CHOP in neuronal injury
models"). Targeted search found NO study doing this attribution, and nothing on the "mislabeled" claim.
The gap is real.

Supporting facts verified:
- Four eIF2a kinases (HRI, PERK, GCN2, PKR) converge on p-eIF2a; GCN2 = amino-acid scarcity, PKR = viral,
  HRI = heme deficiency. ER stress is "primarily orchestrated by PERK".
- CHOP induction was PERK-dependent in a cell-line study.
- Review on ATF4 in neurons: PMC13294100, "The dual role of ATF4 in neurons: from stress adaptation to
  therapeutic intervention".
- Seizure-related review states the PERK-eIF2a-ATF4 response is "predominantly maladaptive".

THE CAVEAT THAT MUST BE DESIGNED AROUND — KINASE REDUNDANCY:
- Verified: "PERK and GCN2 Contribute to eIF2alpha Phosphorylation and Cell Cycle Arrest after Activation of
  the Unfolded Protein Response Pathway", Mol Biol Cell, DOI 10.1091/mbc.e05-03-0268 — the authors
  "suggested GCN2 might function as the redundant eIF2alpha kinase during UPR activation when PERK is absent."
=> A single-kinase siRNA showing NO effect is therefore UNINTERPRETABLE (could be compensation, not
   independence). This is NOT fatal, unlike the D-lactate problem, because:
   (a) the POSITIVE direction stays interpretable — if HRI/DELE1 knockdown abolishes ATF4 where the field
       assumed PERK, redundancy does not explain that away;
   (b) double knockdowns (PERK+GCN2) and the ISRIB / GSK2606414 pharmacological arms give orthogonal
       evidence;
   (c) Xbp1-splicing RT-PCR is an IRE1-specific discriminator independent of the kinase question entirely,
       and is nearly free.
=> DESIGN REQUIREMENT: the paper must be built on positive reassignment + Xbp1 discriminator, NOT on
   absence-of-effect from single knockdowns. Pre-register that asymmetry.

## M. Note on GCN2 in a neurodegeneration model  [SEARCH_SNIPPET]
- "Deletion of the eIF2a Kinase GCN2 Fails to Rescue the Memory Decline Associated with Alzheimer's Disease",
  PMC3795630 — a published negative in exactly this family of questions, i.e. the genre is publishable.

## N. CHAIR AUDIT PASS — viability-assay interference in ferroptosis pharmacology is a REAL, UNFILLED gap
##    with a documented mechanism and a free decisive control  [VERIFIED]
Scout 4's Topic 3. Targeted search found NO study testing ferrostatin-1 (or other RTA ferroptosis inhibitors)
against MTT / CCK-8(WST-8) / resazurin / LDH side by side. Gap confirmed.

But the MECHANISM for why it would matter IS documented:
- Cell-free interference study, "Small Molecule Interferences in Resazurin and MTT-Based Metabolic Assays in
  the Absence of Cells" (seen via ResearchGate 325080341; journal/DOI not captured -> TITLE_ONLY):
  MTT showed 19 interfering species with deviations **above 3000%**; resazurin 16 species, largest ~150%.
  **Thiol and carboxylic acid groups were the main culprits.**
- CCK-8/WST-8: strongly reducing compounds directly reduce the tetrazolium salt -> FALSE POSITIVES; metal
  ions (Zn, Mn) non-specifically reduce WST-8. (Abcam knowledge-center page — VENDOR SOURCE, not peer
  reviewed; use only as a practitioner note.) A patent-sourced comparison reported the antioxidant BME
  interfered with WST-8 — PATENT SOURCE, treat cautiously.
- Natural-product case: MTT readout conflicted with CCK-8 and other assays for Cistanche phenylethanoid
  glycosides, traced to caffeyl groups. PMC6272201.
- Resazurin: subject to fluorescence quenching by test compounds; FCS is an interferent.
- "Limitations of the MTT assay when compared to three commonly used cell enumeration assays",
  BMC Res Notes, DOI 10.1186/s13104-015-1000-8.
- LDH is membrane-integrity, NOT reduction-based -> the orthogonal readout. Recommended control found:
  spike purified LDH into compound-containing medium to confirm recovery.

WHY THIS IS A STRONG CANDIDATE:
 (a) The decisive control is FREE and cell-free: medium + compound + dye, no cells. If Fer-1 reduces the dye
     without cells, every CCK-8-based "Fer-1 rescued viability" datapoint in the field is inflated by an
     unknown amount.
 (b) Blast radius is enormous — CCK-8/MTT + Fer-1 is the near-universal readout of the ferroptosis
     protection literature.
 (c) It needs NO gated equipment, NO new cell line, and the student already owns every assay.
 (d) It connects directly to chair finding E and to Tang & Kang 2026's listed controversy on inducer/tool
     specificity.
 (e) Fer-1 is an aromatic amine RTA (chair finding G) — a reducing agent by design. The prior is strong.
RISK: it is a methods paper. Ceiling is limited (see F: venues exist but are lower tier). Reviewer attack
"this is technical, not biological" is guaranteed and must be answered by quantifying how much published
effect size it would move, not just by showing interference exists.

## O. CHAIR AUDIT — STRONGEST FIND OF THE WHOLE EXERCISE
##    A widely-reused HT-22 model rests on ONE unreplicated paper with a BORDERLINE arm  [VERIFIED]
Scout 5's Topic 3 independently converged on chair finding C. My targeted audit then found something
neither of us had: the claim's entire evidential base, and its weakness.

THE SINGLE SOURCE:
- "Differentiation renders susceptibility to excitotoxicity in HT22 neurons", Neural Regeneration Research
  8(14), 2013. PMID 25206424. DOI 10.3969/j.issn.1673-5374.2013.14.006.
  * Differentiated HT22 were more glutamate-sensitive: EC50 "reducing approximately two orders of magnitude".
  * MK-801 and memantine protected DIFFERENTIATED cells, no effect on undifferentiated.
  * Dithiothreitol protected UNDIFFERENTIATED cells, less effective in differentiated.
  * "Tissues from mice brain and differentiated HT22 cells possessed NMDA receptors, whereas undifferentiated
    HT22 cells and the negative control showed no NMDA receptor characteristics."

THE WEAKNESS (this is the opening):
- The undifferentiated MK-801 arm was BORDERLINE: viability 26.19% -> 38.72%, **P = 0.05**.
- A review of the same work notes a "minor inconsistency between the two assays".
- **NO independent head-to-head replication exists.** Targeted search returned none.
- Only partial, different-insult support: a 2011 Neurological Research homocysteine paper found the same
  undifferentiated-resistant / differentiated-sensitive pattern, attributed to differential NMDA receptor
  expression (tandfonline 10.1179/1743132811Y.0000000057).
- MEANWHILE the model is now being USED as established: e.g. "gamma-Oryzanol from Rice Bran Antagonizes
  Glutamate-Induced Excitotoxicity in an In Vitro Model of Differentiated HT-22 Cells", 2024, PMC11053564.
  That paper applies the model rather than testing it.

WHY THIS IS THE BEST TOPIC-A CANDIDATE IN THE POOL:
 (a) It is a replication-plus-extension of a load-bearing claim, not a model swap. The student's own cell
     line IS the correct material -- for once HT-22 is an asset, not an apology.
 (b) Decisive both ways. Replicates -> the field's differentiated-HT22 excitotoxicity model is finally
     validated (useful, citable). Fails to replicate -> a downstream literature is built on sand.
 (c) Cheap: differentiation protocol + MK-801 + memantine + DTT + qPCR/WB for GluN1/GluN2A/GluN2B.
     No gated equipment. (Patch-clamp would be the gold standard and is NOT available -- must be conceded;
     receptor-level claims must rest on transcript/protein + pharmacology, not on current.)
 (d) It directly serves chair finding C: the field-wide "excitotoxicity" mislabeling of HT-22 work.
 (e) Negative-result value is high and the paper exists either way.
RISKS: (i) differentiation protocol reproducibility is itself the main execution risk -- the 2013 protocol
must be followed exactly and reported in full; (ii) "this is just a replication" reviewer attack -- answer by
adding the receptor-expression panel and the mislabeling audit as new contributions; (iii) a single-lab
replication cannot settle a field -- do not overclaim.

## P. CHAIR AUDIT PARTIAL-KILL — C04 (SCFD1): scout's novelty claim is OVERSTATED  [VERIFIED]
Scout 2 claimed for its Topic 2: "There is no mammalian neuronal SCFD1 perturbation study at all in what I
found -- no dose-response, no overexpression arm, and no measurement of whether the fly chaperone-
downregulation signature is conserved." My audit contradicts the first two clauses.

PRIOR ART THAT EXISTS (all SEARCH_SNIPPET unless noted):
1. "depletion of SCFD1 in mammalian cells induces an ER stress response that leads to autophagy"
   -- attributed to Renna et al. 2011, reached via a SECONDARY citation in a review; I did not open the
   primary. TITLE_ONLY / needs verification. This is precisely the hypothesised readout, already published
   in mammalian cells.
2. **IN SH-SY5Y** (the very line the scout advised the student to obtain): SCFD1 expression "significantly
   responds to neurotoxin-induced oxidative stress, where increased expression exhibited anti-apoptotic
   effects, and SCFD1-antisense transfected cells accelerated apoptosis." -> a neuronal-like line with BOTH
   a knockdown and an overexpression arm, already reporting a protective direction. This substantially
   pre-empts the scout's "overexpression arm" novelty.
3. SCFD1 knockdown in U2OS: LC3 and SQSTM1/p62 "dramatically higher" -- autophagy readout already done.
   "Acetylation of SCFD1 regulates SNARE complex formation and autophagosome-lysosome fusion", PMC9809933.
4. A conflicting/negative result exists: SCFD1 knockdown in HeLa "did not disrupt SEC31 ER localization".
5. TANGO1 + SCFD1 "prevent ER congestion and stress by facilitating transport of bulky or unfolded proteins
   at ERES" (PNAS, DOI 10.1073/pnas.2405209121 is the Anaplasma effector paper that hijacks both).

WHAT ACTUALLY SURVIVES AS NOVEL: only the **eQTL-calibrated graded dose-response** (is a 20-40% reduction,
the size the human eQTL actually produces, phenotypically silent?) plus the explicit GOF-vs-LOF adjudication
framing of the Iacoangeli-vs-Cauchi dispute. That is narrower than claimed but is still a real, unanswered,
and well-posed question.

OVERRIDES: novelty_rating H -> M. novelty score 9 -> 7. confidence low -> high (now audited).
evidence_rating H -> H (unchanged; the dispute is genuinely documented in print).
VERDICT: keep as a candidate, but it can no longer be sold as "the first mammalian neuronal study", and it
is NOT the highest-novelty option in the pool. Any proposal must cite items 1-3 above in its own
state-of-the-art and narrow its claim accordingly.

## Q. CHAIR AUDIT NEAR-KILL — C06 (labile iron pool) was answered in 2026, probe-leakage insight included
##    [VERIFIED]
Scout 4's Topic 2: "Does the labile iron pool actually rise during neuronal ferroptosis? Decoupling
iron-chelator protection from labile-iron dynamics, with a probe-leakage-controlled measurement."

ALREADY PUBLISHED:
- "Labile iron pool dynamics do not drive ferroptosis in colorectal cancer cells", Journal of Biological
  Chemistry, article PII S0021-9258(26)00227-9, PMC13089158. Preprint version: bioRxiv
  DOI 10.1101/2025.07.01.662602 ("...do not drive ferroptosis potentiation...").
  * Finding: "no significant increase in endogenous LIP occurs during ferroptosis"; the LIP "does not expand
    upon pharmacological initiated ferroptosis, despite the potentiating effect of exogenous iron
    supplementation." => iron permissive, not driver. That IS the scout's hypothesis.
  * They already diagnose WHY older measurements mislead: Calcein-AM and PhenGreen SK are chelator/quenching
    probes needing a second competing chelator, so signal depends on probe concentration, extent of ester
    hydrolysis, intracellular sequestration, and relative Fe2+/Fe3+ affinities.
  * They already use FerroOrange (reactivity-based, vendor states no chelating ability) as the fix.
  * **They already state the probe-leakage caveat the scout offered as its novelty:** "as ferroptosis
    progresses in the cell, changes in membrane permeability may cause probe leakage resulting in a
    misleading signal decline."
- Context: FEBS J 2024 review "A guide to ferroptosis, the biological rust of cellular membranes",
  DOI 10.1111/febs.16993 -- notes many proposed ferroptosis biomarkers are context-dependent and
  "considered as rather bystander effects of ferroptosis."
- FerroOrange vendor limits: detects only labile Fe2+; cannot quantify Fe3+ or ferritin/haemoglobin-bound iron
  (Dojindo F374 / Goryo). VENDOR SOURCE.

WHAT WOULD BE LEFT: only "repeat it in a neuronal cell type". That is pseudo-novelty trap 3 verbatim
(changing only the cell line). The limitation the JBC authors concede -- limited cell lines and inducers
(RSL3, JKE, IKE), no independent replication -- is a legitimate opening for a REPLICATION paper, but it is
not the mechanistic contribution the scout described, and it would have to be sold honestly as replication.

OVERRIDES: novelty 8 -> 4; novelty_rating H -> L; overlap_risk M -> H; confidence low -> high.
VERDICT: NOT RECOMMENDED as proposed. Eligible only as an explicitly-labelled replication-in-a-second-
lineage study, which has a much lower ceiling.

## R. META-FINDING — THE AUDIT ATTRITION RATE IS THE REAL RESULT OF THIS EXERCISE
Independent adversarial audit was run on 7 of the candidate topics. Outcomes:
  PASS, strong          C01 (audit O)
  PASS                  C02 (audit N)
  PASS with caveat      C03 (audit L)
  PARTIAL KILL          C04 (audit P) -- novelty claim overstated, prior art in SH-SY5Y and mammalian cells
  NEAR KILL             C06 (audit Q) -- answered in 2026 JBC, including the proposed novel control
  DOWNGRADE             C11 (audit J) -- identical design published in another tissue
  KILL                  lactylation arbitration, scout3-T2 (audit K) -- central control is confounded
=> 4 of 7 audited topics had their novelty claim materially damaged or destroyed. Every one of those four
   was presented by its own domain scout with a confident novelty rating of H or "my top recommendation".
=> The 8 remaining un-audited topics must therefore be presumed to carry a comparable risk. They are NOT
   eligible for the final three, and the student must not act on any of them before the same audit is run.
=> This is the single most important finding to hand the student: novelty self-assessment by a domain expert
   who has just read the field is not reliable. Only an adversarial search for the specific prior art is.
