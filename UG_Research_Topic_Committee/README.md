# 本科生原创课题选题委员会

为一名临床医学本科生寻找「真正可做、具备独立科学贡献、能经受同行评审」的原创研究课题。
最终目标是 **1 个**推荐课题，而不是 15 个看起来新颖的题目。

最后更新：2026-11-04

---

## 怎么读这批文件

**只有 20 分钟**，读两个：

1. **`04_Innovation_Audit.md` §0** —— 本次工作最重要的一条结论
2. **`08_Final_Recommendation.md`** —— 最终推荐与理由

**有一小时**，按这个顺序：

| 文件 | 内容 |
|---|---|
| `01_Literature_Landscape.md` | 研究前沿与文献地图；哪些方向已饱和到不值得进入 |
| `02_15_Candidate_Topics.md` | 15 个候选课题、量化评分、每个课题的查新裁决 |
| `03_Top3_Research_Proposals.md` | 最终三个完整方案（A 稳妥 / B 创新 / C 长期），含三阶段设计、分组、对照、统计、Figure 规划 |
| `04_Innovation_Audit.md` | **核心文件。** 创新性查新；四个被击落课题的完整记录 |
| `05_Experimental_Roadmap.md` | 技术路线、10 个月月度排期、预算明细、风险登记表 |
| `06_Reference_List.md` | 全部参考文献，逐条标注可核验等级 |
| `07_Reviewer_Critique.md` | 四位期刊审稿人视角的模拟严格审稿与异议 |
| `08_Final_Recommendation.md` | 最终唯一推荐 |

原始材料：`_scout_reports/`（五个独立领域 Agent 的完整报告，2275 行，
每个课题按 16 项逐条写满）；`_WIP_chair_verified_notes.md`（主席层面核实记录，A–R 共 18 组）。

---

## 本次工作最重要的一条结论

五个独立领域 Agent 共产出 **29 个候选课题**。随后对其中 **7 个**做了独立的"对抗性查新"
——不去找支持它新颖的证据，而是专门去找**已经做过它的那篇论文**。

**7 个里有 4 个的创新性主张被实质性损坏或摧毁。而这 4 个，每一个都是由该领域的专家 Agent
以"创新性：高"或"我的首选推荐"的身份提交上来的。**

| 裁决 | 课题 | 原因 |
|---|---|---|
| ❌ 彻底击落 | 乳酸化仲裁 | 核心的 D-乳酸对照本身被混杂：D-乳酸抑制 HDAC **比 L-乳酸更强** |
| ⚠️ 近乎击落 | 不稳定铁池 | 2026 年 JBC 已回答，**连 Scout 当作创新点的"探针渗漏对照"都已被该文提出** |
| ⚠️ 部分击落 | SCFD1 | "首个哺乳动物神经元研究"被证伪：SH-SY5Y 中已有敲低+过表达双向结果 |
| ⚠️ 降级 | 神经元 NLRP3 审计 | 同一设计已发表于视网膜色素上皮，且先例用真正基因敲除，学生只有 siRNA |

含义：

> 一个刚刚读完某领域文献的专家，对"这件事有没有人做过"的自我判断，可靠性大约是一半。
> 唯一可靠的做法，是针对那个**具体的决定性实验**去反向检索它的前期工作。

**推论**：剩下 8 个未经独立查新的课题必须假定带有同等风险，已被排除在最终三选之外。
`04_Innovation_Audit.md` §8 给了可自行执行的查新 5 步法。

---

## 最终推荐

> **把 C01（HT-22 分化态）作为主干，把 C02（活力检测干扰）折叠进来作为第二条轴线，合成一篇论文。**
>
> *What the HT-22 glutamate model actually measures: differentiation state and viability
> readout as unreported determinants of apparent neuroprotective pharmacology*

这个结论**与五个 Scout 中任何一个的首选推荐都不同**。两条轴线在一个点上相交，
而这个交点从未被人问过：

- 那个被广泛沿用的"分化 HT-22 兴奋毒性"模型，全部依据是 **2013 年一篇未被独立重复的论文**
  （PMID 25206424），其关键对照臂统计学**边缘**（活力 26.19% → 38.72%，**P = 0.05**），
  且该文自己的评述指出**两种检测之间存在不一致**。
- 该文用来保护未分化细胞的试剂是 **DTT —— 一个巯基试剂**。而巯基是 MTT 类还原型检测的
  **头号干扰基团**（无细胞研究中 MTT 偏差超过 3000%）。
- **那么：那个边缘的 P = 0.05，有多少是读数伪影？**

它也是唯一一个**不赌生物学效应存在**的方案——它测的是方法学依赖性本身，
所以无论结果朝哪个方向走，都有一篇论文。

三个检查点都落在能承受损失的时候：
**第 1 周**一个不含细胞的实验（几百元）告诉你一半是否存在；
**第 8 周**书面停止判定；
**第 7 个月**看 Figure 5 能否用一句话说完——不能，就拆开。

---

## 可运行代码

| 文件 | 用途 | 状态 |
|---|---|---|
| `code/score_topics.py` | 课题评分引擎 | ✅ **已跑通，`--selftest` 7/7** |
| `code/analyze_assay_matrix.py` | 方案 A 主统计分析 | ✅ **已跑通，`--selftest` 14/14** |
| `code/score_topics.R` | 同上，R 版 | ⚠️ **未执行**（本环境装不上 R） |
| `code/analyze_assay_matrix.R` | 同上，R 版 | ⚠️ **未执行**（本环境装不上 R） |

```bash
python3 code/score_topics.py --selftest
python3 code/score_topics.py data/topic_scores.csv

python3 code/analyze_assay_matrix.py --selftest
python3 code/analyze_assay_matrix.py --demo              # 模拟数据跑完整报告
python3 code/analyze_assay_matrix.py data/assay_matrix.csv --dose-response
```

两个 R 脚本是 Python 版的移植，但**从未被执行过**（apt 装不上 R）。
首次使用请先跑 `--selftest`，它应当打印出与 Python 版相同数量的 PASS。
若不一致，以 Python 版为基准。

### 评分引擎强制分离四件事

```
p_exec      = P(实验能物理完成)
p_paper     = P(无论结果如何，能拼成一篇论文)
p_accept    = P(该论文被 SCI 期刊接收)
p_published = p_exec × p_paper × p_accept        ← 三个顺序闸门，乘积必然更小
科学价值     = 单独一列，不参与乘法
```

全部数字都是**主观判断，不是测量值**；被记录下来是为了可被质疑，而不是为了被相信。
`p_published` 是全表最不可靠的数字——用于课题间**相互比较**，绝不当成成功率预测。
脚本还会计算 `rank_divergence`（真实概率排名 − 量表排名），暴露"分数虚高"与"赌注更好"的不一致。

### 统计脚本做的三件容易手算错的事

1. **把交互项作为主要输出**，而非主效应——"效应量随读数改变"本身就是结果。
2. **强制报告效应量与 95% CI**，不只报 P 值。
3. **按 `experiment` 聚合生物学重复**；同一板的复孔被误当作 n 时直接报错。

脚本还会在**交互项不显著但效应量差异很大**时打印功效警告——
三因素交互项的功效需求远高于主效应，n=4 下这是"检验不足"而非"阴性结果"，这是最易误判之处。

---

## 两个真实环境限制

**1. 文献数据库直连全部被网络策略拦截。**
`pubmed.ncbi.nlm.nih.gov`、`pmc.ncbi.nlm.nih.gov`、`eutils`、`www.ebi.ac.uk`、
`api.crossref.org`、`clinicaltrials.gov`、GEO、`scholar.google.com`、`www.frontiersin.org`、
`oaepublish.com` 均返回 403 或 DNS 不解析。

后果：文献为"检索可见"而非"API 核验"；**所有 GEO 编号的样本数与平台需你本人复核**；
ClinicalTrials.gov 的试验状态核查未能执行。
`06_Reference_List.md` §0 给出三级核验标记，§9 列出 10 条已知缺陷。

若需 API 级核验：在云环境设置放开上述域名（会话标题栏云环境菜单 → Edit → Network access
→ Allowed domains，保留"允许包管理器"勾选），**并开新会话**——中途放开对已启动会话不生效。

**2. WebSearch 配额为每回合 200 次，由回合内所有 Agent 共享。**
5 个 Scout 各跑 19–48 次将其耗尽，各自均有 2–6 项计划中的核验检索未能执行（已在各报告内标注）。
这也是为什么只有 7 个课题完成了独立查新。

---

## 目录

```
01–08_*.md              八份交付物
README.md               本文件
_WIP_chair_verified_notes.md   主席核实记录 A–R
_scout_reports/         五个领域 Agent 的原始报告
code/                   可运行脚本（Python 已验证，R 未验证）
data/                   评分 CSV 输入与排序输出
```

本目录之外的 `A_revised_*.docx`、`B_revised_*.docx`、`修改说明.md` 属于另一项既有工作，
本任务未作任何改动。
