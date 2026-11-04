# 06 · 真实参考文献及 DOI/PMID

---

## 0. 核验等级与一个必须先读的声明

### 本会话无法做 API 级核验

以下主机在本会话全部返回 **403 或 DNS 不解析**：

```
pubmed.ncbi.nlm.nih.gov        pmc.ncbi.nlm.nih.gov
eutils.ncbi.nlm.nih.gov        www.ebi.ac.uk  (Europe PMC)
api.crossref.org               clinicaltrials.gov
www.ncbi.nlm.nih.gov  (GEO)    scholar.google.com
alphafold.ebi.ac.uk            www.frontiersin.org
www.oaepublish.com             api.openalex.org
api.semanticscholar.org        doi.org
```

**后果**：本表的文献来自 WebSearch 返回的真实 pubmed/PMC 链接、DOI 与期刊页面，
但**没有一条经过数据库 API 的权威核对**。

### 核验等级定义

| 标记 | 含义 | 你该怎么做 |
|---|---|---|
| `SEARCH_SNIPPET` | 标题 / PMID / DOI 在本会话检索结果中**逐字出现过** | 可直接按号检索原文 |
| `TITLE_ONLY` | 见到标题，**未捕获** PMID 或 DOI | 需按标题检索补全 |
| `需核实` | 仅通过**二次引用**见到，未见原始条目 | **必须打开原文后才可引用** |
| `厂商/非同行评议` | 来自厂商页面、专利或新闻稿 | **不可作为科学依据引用** |

### 三条硬规则，本表严格执行

1. **凡未在检索结果中出现的文献，不提供任何 DOI/PMID 数字串。** 绝不猜测数字。
2. **多条文献标注 "authors not captured"** —— 看到了标题、期刊、常常也看到 DOI 或 PMID，
   但没看到完整作者列表，就不编造作者。
3. **你必须在基于任何一条文献建立论证之前，自己打开并读完它。**
   本表的标记说明的是"我能确认到什么程度"，**不是**该论文本身有多可靠。

---

## 1. 方案 A 的核心文献（HT-22 模型 + 检测干扰）

### 1.1 模型本身

| # | 文献 | 标记 |
|---|---|---|
| A1 | *Differentiation renders susceptibility to excitotoxicity in HT22 neurons*. **Neural Regeneration Research** 8(14), 2013. **PMID 25206424**; **DOI 10.3969/j.issn.1673-5374.2013.14.006** | `SEARCH_SNIPPET` |
| A2 | *Differentiation of HT22 neurons induces expression of NMDA receptor that mediates homocysteine cytotoxicity*. **Neurological Research** 34(1), 2011. **DOI 10.1179/1743132811Y.0000000057** | `SEARCH_SNIPPET` |
| A3 | *Transcriptomic analysis of glutamate-induced HT22 neurotoxicity as a model for screening anti-Alzheimer's drugs*. **Scientific Reports** 2023. **DOI 10.1038/s41598-023-34183-y** | `SEARCH_SNIPPET` |
| A4 | *γ-Oryzanol from Rice Bran Antagonizes Glutamate-Induced Excitotoxicity in an In Vitro Model of Differentiated HT-22 Cells*. 2024. **PMC11053564** | `SEARCH_SNIPPET` |
| A5 | *Mechanism of glutamate-induced neurotoxicity in HT22 mouse hippocampal cells*. authors not captured. | `TITLE_ONLY` |
| A6 | Mg²⁺-free 癫痫样模型依赖解除 NMDA 受体的 Mg²⁺ 阻断。**Scientific Reports** 2021. **DOI 10.1038/s41598-021-90486-y** | `SEARCH_SNIPPET` |
| A7 | HT-22 与原代海马神经元的差异（是否类似前体或成熟神经元尚不清楚）。**PLoS One**, **DOI 10.1371/journal.pone.0326401** | `SEARCH_SNIPPET` |

**A1 是方案 A 的全部靶心。** 其未分化 MK-801 臂：活力 26.19% → 38.72%，**P = 0.05**。

### 1.2 被误标为 "excitotoxicity" 的 HT-22 论文（审计样本示例）

| # | 文献 | 标记 |
|---|---|---|
| A8 | *Leptin Maintained Zinc Homeostasis Against Glutamate-Induced Excitotoxicity by Preventing Mitophagy-Mediated Mitochondrial Activation in HT22 Hippocampal Neuronal Cells*. **PMC5954240** | `SEARCH_SNIPPET` |
| A9 | *Reduction of Mitophagy-Related Oxidative Stress and Preservation of Mitochondria Function Using Melatonin Therapy in an HT22 Hippocampal Neuronal Cell Model of Glutamate-Induced Excitotoxicity*. **PMC6694460** | `SEARCH_SNIPPET` |
| A10 | *Neuroprotective Effect of Gallocatechin Gallate on Glutamate-Induced Oxidative Stress in Hippocampal HT22 Cells*. **PMC7961752** | `SEARCH_SNIPPET` |
| A11 | *Neuroprotective Effects of Tetrahydrocurcumin against Glutamate-Induced Oxidative Stress in Hippocampal HT22 Cells*. **PMC6983265** | `SEARCH_SNIPPET` |

> 注意 A8/A9 用 "excitotoxicity"，A10/A11 用 "oxidative stress"——**描述的是同一个模型**。
> 这个标签分裂本身就是方案 A 第三阶段文献审计的量化对象。

### 1.3 检测干扰

| # | 文献 | 标记 |
|---|---|---|
| A12 | *Small Molecule Interferences in Resazurin and MTT-Based Metabolic Assays in the Absence of Cells*. 经 ResearchGate 325080341 见到；期刊/DOI 未捕获。MTT 19 种干扰物质、偏差 >3000%；resazurin 16 种、最大约 150%；**巯基与羧基为主要元凶** | `TITLE_ONLY` |
| A13 | *Limitations of the 3-(4,5-dimethylthiazol-2-yl)-2,5-diphenyl-2H-tetrazolium bromide (MTT) assay when compared to three commonly used cell enumeration assays*. **BMC Research Notes** 2015. **DOI 10.1186/s13104-015-1000-8** | `SEARCH_SNIPPET` |
| A14 | *Interference of Phenylethanoid Glycosides from Cistanche tubulosa with the MTT Assay*. **PMC6272201**。溯源至咖啡酰基团 | `SEARCH_SNIPPET` |
| A15 | *Advances in Cytotoxicity Testing: From In Vitro Assays to In Silico Models*. **PMC12653452**。resazurin 可被测试化合物荧光淬灭 | `SEARCH_SNIPPET` |
| A16 | Abcam CCK-8 / MTT 知识库页面：强还原性化合物直接还原四唑盐 → 假阳性；Zn/Mn 可非特异还原 WST-8 | **厂商/非同行评议** |
| A17 | elabscience《MTT vs LDH Assay》：LDH 为膜完整性读数，非还原型 | **厂商/非同行评议** |
| A18 | 某专利文件报告抗氧化剂 BME 干扰 WST-8 试剂 | **厂商/非同行评议（专利）** |

> **A16–A18 不可作为论文的科学依据引用**，只能作为"厂商自己都承认"的操作者提示，
> 且须在正文中注明其性质。方案 A 的价值恰在于把这些非同行评议的提示变成同行评议的数据。

### 1.4 自由基捕获抗氧化剂的化学（为什么 Fer-1 会干扰）

| # | 文献 | 标记 |
|---|---|---|
| A19 | *On the Mechanism of Cytoprotection by Ferrostatin-1 and Liproxstatin-1 and the Role of Lipid Peroxidation in Ferroptotic Cell Death*. **ACS Central Science** 2017. **DOI 10.1021/acscentsci.7b00028**; **PMC5364454**。「活性源于作为自由基捕获抗氧化剂的反应性，而非作为脂氧合酶抑制剂的效力」；Fer-1 代谢不稳定，不适体内 | `SEARCH_SNIPPET` |
| A20 | *Lipid-derived radical-trapping antioxidants suppress ferroptosis*. **PMC10960586** | `SEARCH_SNIPPET` |
| A21 | *A guide to using small molecule ferroptosis inhibitors*. **PMC12879747**。细节未能确认 | `TITLE_ONLY` |
| A22 | Armenta & Dixon, *Investigating Nonapoptotic Cell Death Using Chemical Biology Approaches*. 2020. **PMID 32220334**; **PMC7185180** | `SEARCH_SNIPPET` |

---

## 2. 方案 B 的核心文献（ISR 激酶归因）

| # | 文献 | 标记 |
|---|---|---|
| B1 | Wolzak K, et al. (Scheper). *Neuron-specific translational control shift ensures proteostatic resilience during ER stress*. **EMBO J** 41(16):e110501, 2022. **PMID 35791631**; **DOI 10.15252/embj.2021110501**; **PMC9379547** | `SEARCH_SNIPPET` |
| B2 | Fessler E, et al. *A pathway coordinated by DELE1 relays mitochondrial stress to the cytosol*. **Nature** 579:433–437, 2020. **PMID 32132706**; **DOI 10.1038/s41586-020-2076-4** | `SEARCH_SNIPPET` |
| B3 | Guo X, et al. *Mitochondrial stress is relayed to the cytosol by an OMA1–DELE1–HRI pathway*. **Nature** 579:427–432, 2020. **DOI 10.1038/s41586-020-2078-2**（PMID 未捕获） | `SEARCH_SNIPPET` |
| B4 | Perea V, et al. (Wiseman). *Pharmacologic activation of a compensatory integrated stress response kinase promotes mitochondrial remodeling in PERK-deficient cells*. **Cell Chem Biol** 2023. **PMC10029010**（PMID/DOI 未捕获） | `SEARCH_SNIPPET` |
| B5 | Torrence ME, et al. (Manning). *The mTORC1-mediated activation of ATF4 promotes protein and glutathione synthesis downstream of growth signals*. **eLife** 10:article 63326, 2021 | `SEARCH_SNIPPET` |
| B6 | *mTORC1 Balances Cellular Amino Acid Supply with Demand for Protein Synthesis through Post-transcriptional Control of ATF4*. **Cell Reports** 2017. **PMID 28494858** | `SEARCH_SNIPPET` |
| B7 | Bravo-Jimenez, Sharma, Karimi-Abdolrezaee. *The integrated stress response in neurodegenerative diseases*. **Mol Neurodegener** 20(1):20, 2025. **DOI 10.1186/s13024-025-00811-6**; **PMC11837473** | `SEARCH_SNIPPET` |
| B8 | *Cytosolic retention of HtrA2 during mitochondrial protein import stress triggers the DELE1-HRI pathway*. ~2024. **PMC10981713** | `SEARCH_SNIPPET` |
| **B9** | **《PERK and GCN2 Contribute to eIF2α Phosphorylation and Cell Cycle Arrest after Activation of the Unfolded Protein Response Pathway》. Mol Biol Cell. DOI 10.1091/mbc.e05-03-0268。「GCN2 可能在 PERK 缺失时作为冗余的 eIF2α 激酶发挥作用」** | `SEARCH_SNIPPET` |
| B10 | *The dual role of ATF4 in neurons: from stress adaptation to therapeutic intervention*. **PMC13294100** | `SEARCH_SNIPPET` |
| B11 | *Deletion of the eIF2α Kinase GCN2 Fails to Rescue the Memory Decline Associated with Alzheimer's Disease*. **PMC3795630** | `SEARCH_SNIPPET` |
| B12 | *Translational control by eIF2α in neurons: Beyond the stress response*. Bellato, **Cytoskeleton** 2016. **DOI 10.1002/cm.21294** | `SEARCH_SNIPPET` |

> **B9 是方案 B 的设计约束来源。** 它决定了论文不能从单敲低的无效应中得出结论。

---

## 3. 方案 C 的核心文献（SCFD1）

| # | 文献 | 标记 |
|---|---|---|
| C1 | Iacoangeli A, … Jones AR. *SCFD1 expression quantitative trait loci in amyotrophic lateral sclerosis are differentially expressed*. **Brain Communications** 3(4):fcab236, 2021. **PMID 34708205**; **DOI 10.1093/braincomms/fcab236**; **PMC8545614** | `SEARCH_SNIPPET` |
| C2 | Borg R, Purkiss A, Cacciottolo R, Herrera P, Cauchi RJ. *Loss of amyotrophic lateral sclerosis risk factor SCFD1 causes motor dysfunction in Drosophila*. **Neurobiology of Aging** 2023. **PMID 36944290**; **DOI 10.1016/j.neurobiolaging.2023.02.005** | `SEARCH_SNIPPET` |
| C3 | Cauchi RJ. *SCFD1 in amyotrophic lateral sclerosis: reconciling a genetic association with in vivo functional analysis*. **Neural Regen Res** 19(6):1201–1202, 2024. **PMC11467948**（PMID 未捕获） | `SEARCH_SNIPPET` |
| **C4** | **SCFD1 耗竭 → ER 应激 → 自噬（哺乳动物细胞）。归属 Renna et al. 2011，仅经综述二次引用见到** | **`需核实`，不提供数字串** |
| **C5** | **SH-SY5Y 中 SCFD1 对神经毒素氧化应激有响应；表达升高抗凋亡，反义转染加速凋亡。来源为检索片段，期刊/年份未捕获** | **`需核实`，不提供数字串** |
| C6 | *Acetylation of SCFD1 regulates SNARE complex formation and autophagosome-lysosome fusion*. **PMC9809933**。U2OS 中 SCFD1 敲低使 LC3 与 SQSTM1/p62 显著升高 | `SEARCH_SNIPPET` |
| C7 | *Anaplasma phagocytophilum effector EgeA facilitates infection by hijacking TANGO1 and SCFD1 from ER–Golgi exit sites to pathogen-occupied inclusions*. **PNAS**. **DOI 10.1073/pnas.2405209121** | `SEARCH_SNIPPET` |
| C8 | *ALS/FTD-associated mutation in cyclin F inhibits ER-Golgi trafficking, inducing ER stress, ERAD and Golgi fragmentation*. ~2023. **PMC10665471** | `SEARCH_SNIPPET` |
| C9 | *C9orf72-Associated Dipeptide Repeat Expansions Perturb ER-Golgi Vesicular Trafficking, Inducing Golgi Fragmentation and ER Stress, in ALS/FTD*. ~2024. **PMC11584443** | `SEARCH_SNIPPET` |
| C10 | *Lack of an association between SCFD1 rs10139154 polymorphism and amyotrophic lateral sclerosis*. authors/journal/year 未捕获 | `TITLE_ONLY` |

> **C4 与 C5 是推翻 Scout「首个哺乳动物神经元研究」主张的两条关键证据，
> 但二者都只到 `需核实` 级别。** 你必须在开题前把它们找出来读完——
> 如果 C5 确实如检索片段所述，方案 C 的引言必须大幅改写。

---

## 4. 期刊政策与体裁饱和（影响投稿策略）

### 4.1 Mendelian randomization

| # | 文献/来源 | 标记 |
|---|---|---|
| P1 | *Expectations for Mendelian randomization research in PLOS One*. **PLOS One** 2025. **PMID 41252429**; **DOI 10.1371/journal.pone.0337199**。2024-04 起增编辑部筛查 + 强制 STROBE-MR；2024 年约 1800 篇投稿，2025 至 8 月 919 篇 | `SEARCH_SNIPPET` |
| P2 | *Expectations for papers performing Mendelian randomization analyses*. **PLOS Genetics** 2025. **DOI 10.1371/journal.pgen.1011767**。「许多 MR 研究存在关键缺陷」；**强烈建议提供生物学验证** | `SEARCH_SNIPPET` |
| P3 | *Raising the bar for publication of Mendelian randomisation studies in Diabetologia*. **Diabetologia** 2025. **DOI 10.1007/s00125-025-06484-6**。接受率 24% → 4% | `SEARCH_SNIPPET` |
| P4 | *Attention to the misuse of Mendelian randomisation in medical research*. **PMC11950933** | `SEARCH_SNIPPET` |
| P5 | *Mendelian Randomization and Infection: Pitfalls and Promises*. **J Infect Dis** 232(3):525 | `SEARCH_SNIPPET` |
| P6 | Retraction: *Mendelian randomization based on immune cells in diabetic nephropathy*. Frontiers in Endocrinology. **PMC11880894** | `SEARCH_SNIPPET` |
| P7 | Skin Research and Technology 于 2025 年 10 月同日撤回两篇 MR 论文（「同行评议不充分」、「不能被视为科学上可靠」、「缺乏生物学依据」） | `TITLE_ONLY`（经 Scout 5 检索） |
| P8 | *Challenges and future directions for Mendelian randomization*. **Nature Genetics** 2026 | `TITLE_ONLY` |
| P9 | European J Epidemiology：MR 投稿占比 2020 年 3.1% → 2024 年 13.0% | `TITLE_ONLY`（经 Scout 5） |

### 4.2 其他已饱和体裁

| # | 文献/来源 | 标记 |
|---|---|---|
| P10 | Suchak et al. **PLoS Biology 2025**：341 篇公式化 NHANES 论文；2014–2021 约 4 篇/年 → 2024 年 190 篇 | `TITLE_ONLY`（经 Scout 5） |
| P11 | *Science* 报道：2021 年后 NHANES 论文 92% 第一作者为中国单位（2021 前 8%）；Springer Nature 已撤回若干 | `TITLE_ONLY`（经 Scout 5） |
| P12 | Retraction Watch 2025-09-16：某期刊直接禁止药物安全数据库类论文 | `TITLE_ONLY`（经 Scout 5） |
| P13 | *Charting and Sidestepping the Pitfalls of Disproportionality Analysis*. **Drug Safety** 2025 | `TITLE_ONLY`（经 Scout 5） |
| P14 | Frontiers in Pharmacology 2025 评论：审查 35 篇网络药理学论文、另标 13 篇可疑；**盲对接被不当使用** | `TITLE_ONLY`（经 Scout 5） |
| P15 | 2025 年横断面研究：1143 篇论文工厂撤回中 **96.8% 全部作者为中国机构、76.9% 以医院为第一单位** | `TITLE_ONLY`（经 Scout 3） |
| P16 | *Revealing the Paper Mill Iceberg: AI-Based Screening of Cancer Research Publications*. **bioRxiv 2025**. **DOI 10.1101/2025.08.29.673016**。**预印本，未经同行评议**；3370 篇中 433 篇被漏判 | `SEARCH_SNIPPET` |
| P17 | RETRACTION: *Identification of Ferroptosis-Related Gene Prognostic Signature and HSF1...Uterine Carcinosarcoma*. Disease Markers, 2025-07 撤回。**PMC12303628** | `SEARCH_SNIPPET` |
| P18 | RETRACTION: *A Novel Prognostic Pyroptosis-Related Gene Signature...Gliomas*. Oxid Med Cell Longev, 2025-10 撤回。**PMC12517977** | `SEARCH_SNIPPET` |

### 4.3 阴性/重复结果的发表渠道

| # | 文献/来源 | 标记 |
|---|---|---|
| P19 | microPublication Biology FAQ 与 Caltech Library 公告：自 2020 年起 PubMed/PMC 收录；接受阴性结果、重复研究与未发表观察；审稿人指定类别；允许同时存 bioRxiv。**篇幅/图数限制未能确认** | `SEARCH_SNIPPET` + 部分未确认 |
| P20 | ReproSci. *Assessing the Replicability of Scientific Claims in Drosophila Immunity Through an Analysis of 400 Publications*. **bioRxiv 2025**. **DOI 10.1101/2025.07.07.663442**（另见 .663460）。**预印本**；1006 条主张，61% 已验证；45 条"未被挑战"主张中 **38/45 不可重复** | `SEARCH_SNIPPET` |

### 4.4 统计遗传学方法校准（若做方案 C 的公共数据臂必读）

| # | 文献 | 标记 |
|---|---|---|
| P21 | Tambets et al. **HGG Advances 2024**：精细定位 pQTL 指派给**最近的蛋白编码基因**优于所测每一种共定位方法（71.9% 精确率 / 76.9% 召回，coloc.susie 为 45.1% 精确率）；MR + 多个条件独立共定位 QTL 达 81% 精确率但召回坍缩至 7.1% | `TITLE_ONLY`（经 Scout 5） |
| P22 | Eldjarn et al. **Nature 2023**：Olink 与 SomaScan 相关性仅中等；2024 年 Author Correction **推翻**其原精确率主张 | `TITLE_ONLY`（经 Scout 5） |
| P23 | *Rare variant associations with plasma protein levels in the UK Biobank*. **Nature** 2023. **DOI 10.1038/s41586-023-06547-x** | `SEARCH_SNIPPET` |
| P24 | *Large-scale plasma proteomics comparisons through genetics and disease associations*. **Nature** 2023. **DOI 10.1038/s41586-023-06563-x** | `SEARCH_SNIPPET` |
| P25 | Zhao JH et al. *Genetics of circulating inflammatory proteins identifies drivers of immune-mediated disease risk and therapeutic targets*. **Nature Immunology** 2023. **DOI 10.1038/s41590-023-01588-w** | `SEARCH_SNIPPET` |
| P26 | scDRS. *Polygenic enrichment distinguishes disease associations of individual cells in single-cell RNA-seq data*. **Nature Genetics** 2022. **DOI 10.1038/s41588-022-01167-z** | `SEARCH_SNIPPET` |

---

## 5. 被击落课题的关键文献（供你理解查新逻辑）

### 5.1 乳酸化仲裁（击落来源，见 `04` §7）

| # | 文献 | 标记 |
|---|---|---|
| K1 | Latham T, Mackay L, Sproul D, et al. *Lactate, a product of glycolytic metabolism, inhibits histone deacetylase activity and promotes changes in gene expression*. **Nucleic Acids Research** 40(11):4794–4803, 2012. **DOI 10.1093/nar/gks066**; **PMID 22323521**。**L- 与 D-乳酸均**经抑制 HDAC 促进乙酰化；已做过剂量匹配 | `SEARCH_SNIPPET` |
| K2 | *L- and D-lactate enhance DNA repair and modulate the resistance of cervical carcinoma cells to anticancer drugs via histone deacetylase inhibition and hydroxycarboxylic acid receptor 1 activation*. **DOI 10.1186/s12964-015-0114-x**; **PMC4514991**。**「D-乳酸对细胞 HDAC 活性的抑制比 L-乳酸更强」** | `SEARCH_SNIPPET` |
| K3 | *Class I histone deacetylases (HDAC1–3) are histone lysine delactylases*. **Science Advances**. **DOI 10.1126/sciadv.abi6696** → HDAC 是**擦除酶** | `SEARCH_SNIPPET` |
| K4 | Gonzatti MB et al. *Class I histone deacetylases catalyze lysine lactylation*. **JBC 2025**。**PMC11888385**（Scout 为同一标题引用 PMC12624779——**两个 PMC 号，必须核实**） → HDAC 是**书写酶** | `SEARCH_SNIPPET`，**号码冲突未解决** |
| K5 | Zhang D et al. *Metabolic regulation of gene expression by histone lactylation*. **Nature** 574(7779):575–580, 2019. **PMID 31645732**; **DOI 10.1038/s41586-019-1678-1** | `SEARCH_SNIPPET` |
| K6 | Zhang D, Gao J, Zhu Z, … Zhao Y. *Lysine l-lactylation is the dominant lactylation isomer induced by glycolysis*. **Nature Chemical Biology** 21:91–99. **DOI 10.1038/s41589-024-01680-8** | `SEARCH_SNIPPET` |
| K7 | *Both L-lactyl and D-lactyl enantiomers modify histones in mouse testis*. **bioRxiv 预印本** 2025. **DOI 10.1101/2025.10.09.681385**; **PMC13380202**。报告 H3K18/H3K79 以 **D**-乳酰化为主；总化学计量仅 0.01–0.44%，而乙酰化达 25–35% | `SEARCH_SNIPPET`，**预印本** |
| K8 | *Epigenetics Identifier screens reveal regulators of chromatin acylation and limited specificity of acylation antibodies*. **Scientific Reports** 2021. **DOI 10.1038/s41598-021-91359-0**; **PMC8211816** | `SEARCH_SNIPPET` |
| K9 | An YJ et al. *Lactate as a major epigenetic carbon source for histone acetylation via nuclear LDH metabolism*. **Exp Mol Med** 55:2238–2247, 2023. **DOI 10.1038/s12276-023-01095-w**; **PMC10618192** | `SEARCH_SNIPPET` |

### 5.2 不稳定铁池（击落来源，见 `04` §5）

| # | 文献 | 标记 |
|---|---|---|
| K10 | *Labile iron pool dynamics do not drive ferroptosis in colorectal cancer cells*. **Journal of Biological Chemistry** 2026. PII **S0021-9258(26)00227-9**; **PMC13089158**; **PMID 41819262**(经 Scout 4)。预印本 **DOI 10.1101/2025.07.01.662602** | `SEARCH_SNIPPET`（两条独立路径命中） |
| K11 | *A guide to ferroptosis, the biological rust of cellular membranes*. Veeckmans et al., **FEBS Journal** 2024. **DOI 10.1111/febs.16993** | `SEARCH_SNIPPET` |
| K12 | Dojindo F374 / Goryo FerroOrange 产品页：仅检测不稳定 Fe²⁺；无法定量 Fe³⁺ 或铁蛋白结合铁 | **厂商/非同行评议** |

### 5.3 NLRP3 抗体审计（降级来源，见 `04` §6）

| # | 文献 | 标记 |
|---|---|---|
| K13 | *Issues with the Specificity of Immunological Reagents for NLRP3: Implications for Age-related Macular Degeneration*. **Scientific Reports** 2017. **DOI 10.1038/s41598-017-17634-1**; **PMC5764999**。WT vs *Nlrp3*-KO 验证；**其中一个抗体的条带在敲除样本中更强** | `SEARCH_SNIPPET` |
| K14 | *NLRP3 inflammasome is expressed and functional in mouse brain microglia but not in astrocytes*. **PLoS ONE**. **DOI 10.1371/journal.pone.0130624** | `SEARCH_SNIPPET` |
| K15 | *Targeting microglial NLRP3 in the SNc region as a promising disease-modifying therapy for Parkinson's disease*. **PMC9660492**。微胶质 NLRP3 敲低经条件培养基**间接**作用于多巴胺神经元 | `SEARCH_SNIPPET` |

---

## 6. 铁死亡边界争议与工具化合物（横向背景）

| # | 文献 | 标记 |
|---|---|---|
| F1 | Daolin Tang & Rui Kang. *Ten controversies defining the boundaries of ferroptosis*. **Element**, 2026-08-04. oaepublish.com/articles/element.2026.07。列为开放：线粒体是否必需；**铁是驱动还是许可**；**诱导剂是否真正特异**；治疗靶向是否被过度炒作 | `SEARCH_SNIPPET`（期刊页不可达） |
| F2 | *Oxytosis/Ferroptosis—(Re-)Emerging Roles for Oxidative Stress-Dependent Non-apoptotic Cell Death in Diseases of the Central Nervous System*. **Frontiers in Neuroscience** 2018. **PMC5920049**。主张两者是「同一死亡通路的两个名字」 | `SEARCH_SNIPPET` |
| F3 | *Using the Oxytosis/Ferroptosis Pathway to Understand and Treat Age-Associated Neurodegenerative Diseases*. **Cell Chemical Biology** 2020. PII **S2451-9456(20)30426-8** | `SEARCH_SNIPPET` |
| F4 | *Potent ferroptosis agent RSL3 induces cleavage of Pyroptosis-Specific gasdermins in Cancer cells*. **Scientific Reports** 2025. **DOI 10.1038/s41598-025-11368-1**。「这些分子具有脱靶效应，无法提供重叠通路的全貌」 | `SEARCH_SNIPPET` |
| F5 | *Ferroptosis induction via genetic approaches – CRISPR/Cas9-based disruption on key anti-ferroptotic genes*. **PMID 42442865**。erastin 激活线粒体 VDAC；(1S,3R)-RSL3 影响 GPX4 之外的硒蛋白 | `SEARCH_SNIPPET` |
| F6 | *Necrostatin-1 Prevents Ferroptosis in a RIPK1- and IDO-Independent Manner in Hepatocellular Carcinoma*. **PMC8469492** | `SEARCH_SNIPPET` |
| F7 | *The LIFR-targeting small molecules EC330/EC359 are potent ferroptosis inducers*. **PMC10308161**。ETC 抑制剂压制 erastin 诱导但压不住 RSL3 诱导 | `SEARCH_SNIPPET` |
| F8 | *The ferroptosis inducer erastin irreversibly inhibits system xc− and synergizes with cisplatin...*. **PMC5772355** | `SEARCH_SNIPPET` |
| F9 | *Ferroptosis inhibitors: past, present and future*. Zhang L, Luo YL, Xiang Y, Bai XY, Qiang RR, Zhang X, Yang YL, Liu XL. **Frontiers in Pharmacology** 15, 2024-05. **DOI 10.3389/fphar.2024.1407335** | `SEARCH_SNIPPET` |
| F10 | *Ferroptosis: when metabolism meets cell death*. **Physiological Reviews**. **DOI 10.1152/physrev.00031.2024** | `SEARCH_SNIPPET` |

---

## 7. 癫痫与神经炎症（若改选 C07/C09/C11/C12 需要）

| # | 文献 | 标记 |
|---|---|---|
| E1 | ILAE Consortium on Complex Epilepsies. *GWAS meta-analysis of over 29,000 people with epilepsy identifies 26 risk loci and subtype-specific genetic architecture*. **Nature Genetics** 2023. **DOI 10.1038/s41588-023-01485-w**; **PMC10484785**。神经元富集、无胶质富集 | `SEARCH_SNIPPET` |
| E2 | *Localization of brain neuronal IL-1R1 reveals specific neural circuitries responsive to immune signaling*. **J Neuroinflammation** 2024. **PMID 39563437**; **DOI 10.1186/s12974-024-03287-1** | `SEARCH_SNIPPET` |
| E3 | Srinivasan D, Yen JH, Joseph DJ, Friedman W. *Cell type-specific interleukin-1β signaling in the CNS*. **J Neurosci** 24(29):6482–6488, 2004. **PMID 15269258**; **DOI 10.1523/JNEUROSCI.5712-03.2004**。神经元无 NF-κB 激活、无可检出 TRAF6 | `SEARCH_SNIPPET` |
| E4 | Smith DE et al. *A central nervous system-restricted isoform of the interleukin-1 receptor accessory protein modulates neuronal responses to interleukin-1*. **Immunity** 30(6):817–831, 2009 | `SEARCH_SNIPPET`（PMID/DOI 未捕获） |
| E5 | *Neuron-specific effects of interleukin-1β are mediated by a novel isoform of the IL-1 receptor accessory protein*. **J Neurosci** 31(49):18048, 2011. **PMID 22159118** | `SEARCH_SNIPPET` |
| E6 | *Synapse-specific IL-1 receptor subunit reconfiguration augments vulnerability to IL-1β in the aged hippocampus*. **PNAS** 2015. **DOI 10.1073/pnas.1514486112** | `SEARCH_SNIPPET` |
| E7 | *Conditional knockout of IL-1R1 in endothelial cells attenuates seizures and neurodegeneration...*. **Mol Neurobiol** 2024. **PMID 38087170**; **DOI 10.1007/s12035-023-03842-6** | `SEARCH_SNIPPET` |
| E8 | Vezzani group. *Powerful anticonvulsant action of IL-1 receptor antagonist on intracerebral injection and astrocytic overexpression in mice*. **PNAS** 2000. **DOI 10.1073/pnas.190206797** | `SEARCH_SNIPPET` |
| E9 | Illes P, Khan TM, Rubini P. *Neuronal P2X7 receptors revisited: do they really exist?* **J Neurosci** 37(30):7049, 2017（对立论文见同期 37(30):7063） | `SEARCH_SNIPPET` |
| E10 | *A functional P2X7 splice variant with an alternative transmembrane domain 1 escapes gene inactivation in P2X7 knock-out mice*. **JBC** 2009. **PMID 19546214**; **PMC2757983** | `SEARCH_SNIPPET` |
| E11 | *Enhanced Glycolysis-Driven Histone H3K18 Lactylation Regulates Epileptogenesis by Modulating the E3 Ubiquitin Ligase COP1*. **Advanced Science** 2026-05-29, e16985. **DOI 10.1002/advs.202516985**; **PMID 42210782** | `SEARCH_SNIPPET` |
| E12 | cGAS 介导 I 型干扰素驱动药物难治性癫痫进展。**Nature Neuroscience** 2026. **PMID 41676493**; **DOI 10.1038/s41593-026-02384-z** | `SEARCH_SNIPPET` |
| E13 | 神经元 mtDNA 经 p-MLKL 渗漏激活微胶质 cGAS–STING。**PNAS** 2026. **DOI 10.1073/pnas.2522313123** | `SEARCH_SNIPPET` |
| E14 | Jeong et al. C1q 中和减弱补体介导突触清除与癫痫样活动。**Epilepsia** 2026. **DOI 10.1111/epi.18678** | `SEARCH_SNIPPET` |
| E15 | Mushunuri A et al. *Genetic risk factor identification for common epilepsies guided by integrative omics data analysis*. **Epilepsia** 67(3):1406–1420, 2026. **PMID 41319129**; **DOI 10.1111/epi.70021**; **PMC13007835** | `SEARCH_SNIPPET` |
| E16 | Andersen MS et al. *Heritability enrichment implicates microglia in Parkinson's disease pathogenesis*. **Annals of Neurology** 2021. **DOI 10.1002/ana.26032** | `SEARCH_SNIPPET` |
| E17 | *HDAC1 promotes hippocampal neuronal pyroptosis in epileptic mice through the miR-15a-5p/caspase-1 axis*. **Neurochemical Research** 2025. **DOI 10.1007/s11064-025-04372-4** | `SEARCH_SNIPPET` |
| E18 | 癫痫中内皮 claudin-5 的因果性实验。**Nature Communications** 2022. **DOI 10.1038/s41467-022-29657-y** | `SEARCH_SNIPPET` |

> ⚠️ **VX-765 / NCT01501383 的试验状态**：检索片段与一份**企业新闻稿**指出 Phase 2b 已终止，
> 且一份 AlzDiscovery 摘要称结果从未在同行评议期刊发表。
> **ClinicalTrials.gov 在本会话不可达，该状态未经注册库直查。引用前必须自行核实。**

---

## 8. GEO 数据集编号（**全部需自行上 GEO 复核**）

GEO 在本会话不可达。以下编号仅为检索结果中出现过，**样本数与平台均未经核对**。

| 编号 | 检索片段所述内容 |
|---|---|
| GSE63808 | 人海马，药物难治性 TLE，微阵列，约 150 样本（= ArrayExpress E-GEOD-63808） |
| GSE127871 | 人海马 RNA-seq，12 例难治性 TLE |
| GSE190451 | 人 TLE 海马 RNA-seq，3 对照 vs 3 TLE（**样本极小**） |
| GSE190452 | **皮层** snRNA-seq，**不是海马** |
| GSE197015 | 红藻氨酸小鼠海马 RNA-seq |
| GSE241219 | 小鼠匹罗卡品 SE，CA1 bulk RNA-seq，6/12/24/36/72 h |
| GSE213393 | 小鼠齿状回，红藻氨酸 vs 生理盐水 |
| GSE114701 | miRNA，20 TLE vs 20 对照 |
| GSE122228 | 杏仁核内红藻氨酸，微阵列 |
| GSE174367 | 人前额叶 snRNA-seq + snATAC-seq，晚期 AD，191,890 核 |
| GSE138852 | Grubman 内嗅皮层，6 对照 / 6 AD |
| GSE147528 / GSE157783 | AD 进程相关 |
| GSE107011 | 免疫细胞 / PBMC 谱 |
| GSE285372 | 红藻氨酸后 1 h 海马染色质 Fos 结合 |
| GCST90027158 | Bellenguez AD GWAS（GWAS Catalog） |

另：*Identification of epileptic hippocampal sclerosis related genes through bulk and single-nucleus
RNA sequencing datasets*. 2025. **DOI 10.1007/s00018-025-05959-4** `SEARCH_SNIPPET`

---

## 9. 本表的已知缺陷清单

逐条列出，以免你误以为本表完整：

1. **零条 API 级核验。** 全部来自 WebSearch 片段。
2. **K4 存在两个冲突的 PMC 号**（PMC11888385 vs PMC12624779），未能判定。
3. **C4、C5 仅到 `需核实` 级**，但它们是推翻方案 C 原创新性主张的关键证据
   —— 必须优先解决。
4. **A12 期刊与 DOI 未捕获**，但它是方案 A 轴线二的主要机制依据。
5. **A16–A18、K12 为厂商/专利来源**，不可作为科学依据引用。
6. **K7、P16、P20 为预印本**，必须按预印本引用。
7. **ClinicalTrials.gov 所有试验状态未经核查。**
8. **全部 GEO 编号的样本数与平台未经核对。**
9. **"Fer-1/Lip-1 是否阻断非铁死亡性死亡"找不到可引用出处**
   —— 机制上合理但本会话无出处，**不得当作事实陈述**。
10. 多条文献的作者列表缺失（标为 authors not captured），**刻意不编造**。

> **若需要 API 级核验与 GEO 样本数确认**，需在云环境设置中放开
> `pubmed.ncbi.nlm.nih.gov`、`pmc.ncbi.nlm.nih.gov`、`eutils.ncbi.nlm.nih.gov`、
> `www.ebi.ac.uk`、`api.crossref.org`、`clinicaltrials.gov`、`www.ncbi.nlm.nih.gov`
> （会话标题栏云环境菜单 → Edit → Network access → Allowed domains，保留"允许包管理器"勾选），
> **并开启新会话**——中途放开对已启动的会话不生效。
