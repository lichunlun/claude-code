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
