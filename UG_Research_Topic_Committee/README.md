# 本科生原创课题选题委员会 — 工作目录

> **状态：进行中（阶段一未完成）。本目录尚不包含任务要求的 8 份交付物。**
> 最后更新：2026-11-04

## 这是什么

为一名临床医学本科生寻找「真正可做、具备独立科学贡献、能经受同行评审」的原创研究课题。
最终目标是 **1 个** 推荐课题，而不是 15 个看起来新颖的题目。

## 目前进度

| 阶段 | 状态 | 说明 |
|---|---|---|
| 1. 五领域并行文献侦察 | 进行中 | 5 个独立 Agent 后台运行，结果未返回 |
| 2. 独立对抗性创新性查新 | **受阻** | 本回合 WebSearch 配额（200 次/回合，所有 Agent 共享）已被阶段一耗尽 |
| 3. 15 候选评分 + 选出 Top3 | 未开始 | |
| 4. 模拟严格审稿 | 未开始 | |
| 5. 撰写 8 份交付物 | 未开始 | |

## 已完成的实质内容

### `code/score_topics.py` / `code/score_topics.R`
评分引擎。同一套 100 分制权重、同一个 CSV 输入，两种语言各一份实现。

设计上强制把四件常被混为一谈的事分开：

```
p_exec   = P(实验能物理完成)
p_paper  = P(无论结果如何，能拼成一篇论文)
p_accept = P(该论文被 SCI 期刊接收)
p_published = p_exec × p_paper × p_accept     ← 三个顺序闸门，乘积必然小于任一单项
科学价值 = 单独一列，不参与乘法
```

脚本会对越界输入直接报错而非静默排序，并标记阻断性红旗（高重合风险 / 证据薄弱 / 低置信度）。
`p_published` 是三个主观概率的乘积，因此是全表最不可靠的数字——用于课题之间**相互比较**，
绝不可当作成功率预测。

```bash
python3 code/score_topics.py --selftest        # 7/7 通过
python3 code/score_topics.py data/topic_scores.csv
Rscript  code/score_topics.R  data/topic_scores.csv
```

R 在准备这批交付物的环境中不可用，因此实际跑出评分的是 Python 版；两版读同一 CSV、
应给出相同结果。

### `_WIP_chair_verified_notes.md`
主席层面亲自核实的 9 组横向事实（A–I）。每条都标注了可核验等级，**凡本会话检索中未出现的，
一律标为未核实且不给出 DOI/PMID 数字串**。其中三条会直接改变选题方向：

- **A** — MR 论文未被禁投，但门槛剧变（Diabetologia 的 MR 接受率五年内 24% → 4%）。
- **C** — HT-22 被全领域系统性误标：该细胞缺乏功能性离子型谷氨酸受体，谷氨酸经耗竭 GSH 致死，
  但大量论文仍以 "excitotoxicity" 为题；且分化状态可能改变机制，该问题文献明言「仍不清楚」。
- **E** — 铁死亡工具化合物并不干净（erastin 激活 VDAC；RSL3 影响其他硒蛋白并触发焦亡），
  而 Tang & Kang 2026 已将「诱导剂是否真正具有特异性」列为未决争议。

另有一条反向警告（**I**）：癫痫 + 乳酸化已被 2026 年 *Advanced Science* 一篇论文占据，
该方向下游重合风险高。

## 两个真实环境限制（必须记录，否则后续会误判）

**1. 文献数据库直连全部被网络策略拦截。**
`pubmed.ncbi.nlm.nih.gov`、`pmc.ncbi.nlm.nih.gov`、`eutils`、`www.ebi.ac.uk`、
`api.crossref.org`、`clinicaltrials.gov`、GEO、`scholar.google.com`、`alphafold.ebi.ac.uk`、
`www.frontiersin.org`、`oaepublish.com` 均返回 403 或 DNS 不解析。

后果：可通过 WebSearch 得到真实 PMID 链接与 DOI，但**无法逐条调 API 做权威核验**，
也无法打开 GEO 页面确认样本数与平台。所有 GSE 编号均标为「检索可见、需本人上 GEO 复核」。

**2. WebSearch 配额为每回合 200 次，由该回合内所有 Agent 共享。**
5 个侦察 Agent 已将其耗尽，导致阶段二的查新无法在同一回合内执行。
后续应**串行、限流**派发审计 Agent。

## 目录约定

```
code/    可运行脚本
data/    评分 CSV 输入与排序后输出
```

本目录之外的 `A_revised_*.docx`、`B_revised_*.docx`、`修改说明.md` 属于另一项既有工作，
本任务未作任何改动。
