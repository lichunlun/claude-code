# 数据库结构说明

- 引擎：SQLite（单文件 `data/research.db`），通过 SQLAlchemy 2.x ORM 访问；模型定义见 `rcc/models.py`。
- 每个连接开启 `PRAGMA foreign_keys=ON`、`busy_timeout=30000`；日志模式为默认的 DELETE（单文件，便于人工复制备份）。
- 时间戳：`created_at` / `updated_at` 为本地时间，由 ORM 自动维护。
- 状态类字段保存稳定的英文代码，界面显示中文标签（`rcc/constants.py`）。
- 升级策略：`create_all` 自动创建新表；`_add_missing_columns` 为旧库自动补充新增的可空列（只增不删，旧数据不受影响）；`app_meta.schema_version` 记录结构版本。

## 关系概览

```
projects ─┬─< project_milestones          (CASCADE)
          ├─< tasks                        (SET NULL)
          ├─< experiments ─< experiment_attachments (CASCADE)
          │        └── experiment_batches  (SET NULL)
          ├─< publications ─< publication_status_history (CASCADE)
          ├─< bioinformatics_jobs ─< bioinformatics_runs (CASCADE)
          ├─< calendar_events              (SET NULL)
          ├─< files_index                  (SET NULL)
          ├─< literature_notes             (SET NULL)
          ├─< ai_interactions              (SET NULL)
          └─<> literature  (经 project_literature 多对多，CASCADE)
literature ─< literature_notes (CASCADE)
literature ~ literature_fulltext (FTS5 虚拟表，按 literature_id 关联，删除文献时由服务层清理)
```

服务层另外**禁止删除仍有关联数据的项目**（提示改用归档），因此 SET NULL 只是兜底。

## 表清单

| 表 | 用途 | 关键字段 / 约束 |
|---|---|---|
| `projects` | 科研项目 | `name` 唯一；`status` ∈ Planning/Active/On Hold/Completed 或 NULL（待填写）；`progress` 0–100 或 NULL；`key_paths` 每行一个绝对路径；`source_note` 信息来源；`is_archived` |
| `project_milestones` | 里程碑 | `due_date` 可空；`status` ∈ Planned/In Progress/Blocked/Done |
| `tasks` | 跨项目任务 | `priority` ∈ Critical/High/Medium/Low；`status` ∈ Todo/In Progress/Blocked/Done/Cancelled；`due_date`、`estimated_hours`；`is_important`/`is_urgent` 为 NULL 时自动判断四象限；`started_at`/`completed_at` 由状态变更自动维护 |
| `literature` | 文献 | `doi` 唯一（规范化小写）、`pmid` 唯一、`file_hash`（SHA-256 查重）；`title` 可为 NULL（无法识别时）；`verification_status` ∈ Unverified/Partially Verified/Verified；`metadata_sources` JSON 记录每个字段的来源（pdf_xmp / pdf_info / pdf_text_page1 / manual / crossref / pubmed）与导入提示；`reading_status` ∈ Unread/Reading/Read/Key；`value_note`/`limitation_note` |
| `literature_notes` | 阅读笔记 | 类型、页码、可关联项目 |
| `project_literature` | 项目–文献多对多 | 复合主键；`relevance` 与项目的关系 |
| `literature_fulltext` | PDF 全文索引（FTS5） | `content`（每页一行）、`literature_id`、`page`；优先使用 trigram 分词器（支持中文与子串检索） |
| `experiment_batches` | 实验批次 | (`project_id`, `code`) 唯一 |
| `experiments` | 实验记录 | 目的、分组、模型、试剂、仪器、`parameters`（JSON 列表 name/value/unit）、`raw_data_path`（只读引用）、结果摘要、`outcome` ∈ Success/Partial/Failure/Pending Evaluation、失败原因、下一步 |
| `experiment_attachments` | 附件引用 | (`experiment_id`, `path`) 唯一；存在性、大小、修改时间、最近检测时间 |
| `publications` | 论文 | `status` ∈ Draft/Internal Review/Submitted/Editor Assigned/Under Review/Revision/Accepted/Published/Rejected/Transferred/Withdrawn/On Hold/Unconfirmed；各节点日期；投稿系统链接；文件路径 |
| `publication_status_history` | 状态历史 | 每次变更一行：from/to、事件日期、期刊、备注、`confirmed_by_user` |
| `bioinformatics_jobs` | 生信分析任务 | 语言、脚本/参数/工作目录/数据/输出路径、数据来源、`status` ∈ Pending/Running/Completed/Failed/Needs Verification、错误日志、结果摘要 |
| `bioinformatics_runs` | 运行与日志 | `source` ∈ manual/executed；命令（JSON）、脚本 SHA-256、退出码、日志路径与末尾内容、`confirmed_by_user` |
| `calendar_events` | 独立日程 | `event_type` ∈ exam/conference/milestone/goal/deadline/other；起止日期 |
| `files_index` | 文件索引 | `path` 唯一（绝对路径）；类别、存在性、大小、修改时间、最近检测时间 |
| `ai_settings` | 模型配置 | `provider_type` ∈ anthropic/openai_compatible；`key_storage` ∈ env/keyring/none；**只保存环境变量名，不保存 API Key** |
| `ai_interactions` | AI 调用留痕 | 授权范围、问题、发送字符数、回答、状态与错误 |
| `activity_logs` | 操作日志 | 对象类型/编号、动作（create/update/delete/status_change/import/verify/...）、摘要、变更详情 JSON |
| `app_meta` | 应用元数据 | `schema_version`、`seed_version`、最近备份时间、脚本执行开关、解释器路径等（不含任何密钥） |

## 主要索引

外键列（`project_id` 等）、`tasks.status/priority/due_date/completed_at`、`literature.year/pub_type/reading_status/file_hash`、`experiments.status/experiment_date`、`publications.status/revision_due_date`、`calendar_events.start_date`、`files_index.category`、`activity_logs.created_at` 以及 (`entity_type`, `entity_id`)。

## 直接查看数据

数据库是标准 SQLite 文件，可用 [DB Browser for SQLite](https://sqlitebrowser.org/) 只读打开查看；也可在应用“设置与备份”中导出为 Excel（每张表一个工作表）。请勿在应用运行时用其他工具写入数据库。
