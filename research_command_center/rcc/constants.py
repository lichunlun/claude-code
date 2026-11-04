"""枚举值与中文显示标签。

数据库中保存稳定的英文代码，界面显示中文标签。这样未来接入 AI 或导出数据时语义稳定。
"""
from __future__ import annotations

PENDING = "待填写"
UNVERIFIED = "待核实"

# ---------- 项目 ----------
PROJECT_STATUSES = ["Planning", "Active", "On Hold", "Completed"]
PROJECT_STATUS_LABELS = {
    "Planning": "规划中",
    "Active": "进行中",
    "On Hold": "暂停",
    "Completed": "已完成",
}

MILESTONE_STATUSES = ["Planned", "In Progress", "Blocked", "Done"]
MILESTONE_STATUS_LABELS = {
    "Planned": "未开始",
    "In Progress": "进行中",
    "Blocked": "受阻",
    "Done": "已完成",
}

# ---------- 任务 ----------
TASK_PRIORITIES = ["Critical", "High", "Medium", "Low"]
TASK_PRIORITY_LABELS = {
    "Critical": "Critical · 关键",
    "High": "High · 高",
    "Medium": "Medium · 中",
    "Low": "Low · 低",
}
PRIORITY_WEIGHT = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}

TASK_STATUSES = ["Todo", "In Progress", "Blocked", "Done", "Cancelled"]
TASK_STATUS_LABELS = {
    "Todo": "待办",
    "In Progress": "进行中",
    "Blocked": "受阻",
    "Done": "已完成",
    "Cancelled": "已取消",
}
TASK_OPEN_STATUSES = ["Todo", "In Progress", "Blocked"]

# 四象限：紧急 = 截止日期在 N 天内（含逾期）；重要 = Critical/High（可手动覆盖）
URGENT_WITHIN_DAYS = 3
QUADRANTS = {
    "Q1": "重要且紧急",
    "Q2": "重要但不紧急",
    "Q3": "紧急但不重要",
    "Q4": "不重要且不紧急",
}

# ---------- 文献 ----------
LIT_TYPES = [
    "Review",
    "Original Article",
    "Meta-analysis",
    "Clinical Trial",
    "Systematic Review",
    "Case Report",
    "Preprint",
    "Editorial",
    "Other",
]
LIT_TYPE_LABELS = {
    "Review": "Review 综述",
    "Original Article": "Original Article 原创研究",
    "Meta-analysis": "Meta-analysis 荟萃分析",
    "Clinical Trial": "Clinical Trial 临床试验",
    "Systematic Review": "Systematic Review 系统综述",
    "Case Report": "Case Report 病例报告",
    "Preprint": "Preprint 预印本",
    "Editorial": "Editorial 社论/述评",
    "Other": "Other 其他",
}

READING_STATUSES = ["Unread", "Reading", "Read", "Key"]
READING_STATUS_LABELS = {
    "Unread": "未读",
    "Reading": "阅读中",
    "Read": "已读",
    "Key": "重点文献",
}

VERIFICATION_STATUSES = ["Unverified", "Partially Verified", "Verified"]
VERIFICATION_LABELS = {
    "Unverified": "待核实",
    "Partially Verified": "部分核实",
    "Verified": "已核实",
}

# 元数据来源标识（可追溯性）
SRC_PDF_XMP = "pdf_xmp"            # PDF 内嵌 XMP 元数据（出版商写入）
SRC_PDF_INFO = "pdf_info"          # PDF 文档信息字典
SRC_PDF_TEXT = "pdf_text_page1"    # PDF 第一页文本中的标识符
SRC_MANUAL = "manual"              # 用户手动录入
SRC_CROSSREF = "crossref"          # 用户触发的 Crossref 在线比对
SRC_PUBMED = "pubmed"              # 用户触发的 PubMed 在线比对
SOURCE_LABELS = {
    SRC_PDF_XMP: "PDF 内嵌 XMP 元数据",
    SRC_PDF_INFO: "PDF 文档属性",
    SRC_PDF_TEXT: "PDF 首页文本识别",
    SRC_MANUAL: "手动录入",
    SRC_CROSSREF: "Crossref 比对",
    SRC_PUBMED: "PubMed 比对",
}

NOTE_TYPES = ["摘要要点", "方法", "关键结果", "评论与质疑", "原文摘录", "其他"]

# ---------- 实验 ----------
EXPERIMENT_STATUSES = ["Planned", "In Progress", "Completed", "Failed", "Cancelled"]
EXPERIMENT_STATUS_LABELS = {
    "Planned": "待开展",
    "In Progress": "进行中",
    "Completed": "已完成",
    "Failed": "失败",
    "Cancelled": "已取消",
}
EXPERIMENT_PENDING_STATUSES = ["Planned", "In Progress"]

EXPERIMENT_OUTCOMES = ["Success", "Partial", "Failure", "Pending Evaluation"]
EXPERIMENT_OUTCOME_LABELS = {
    "Success": "成功",
    "Partial": "部分成功",
    "Failure": "失败",
    "Pending Evaluation": "待评估",
}

ATTACHMENT_KINDS = ["原始数据", "WB 图片", "测序文件", "实验图片", "分析结果", "实验记录本", "其他"]

# ---------- 投稿 ----------
PUB_PIPELINE = [
    "Draft",
    "Internal Review",
    "Submitted",
    "Editor Assigned",
    "Under Review",
    "Revision",
    "Accepted",
    "Published",
]
PUB_SIDE_STATUSES = ["Rejected", "Transferred", "Withdrawn", "On Hold"]
PUB_UNCONFIRMED = "Unconfirmed"
PUB_STATUSES = PUB_PIPELINE + PUB_SIDE_STATUSES + [PUB_UNCONFIRMED]
PUB_STATUS_LABELS = {
    "Draft": "Draft · 草稿",
    "Internal Review": "Internal Review · 内部审阅",
    "Submitted": "Submitted · 已投稿",
    "Editor Assigned": "Editor Assigned · 编辑已分配",
    "Under Review": "Under Review · 外审中",
    "Revision": "Revision · 修改中",
    "Accepted": "Accepted · 已接收",
    "Published": "Published · 已发表",
    "Rejected": "Rejected · 拒稿",
    "Transferred": "Transferred · 转投",
    "Withdrawn": "Withdrawn · 撤稿",
    "On Hold": "On Hold · 暂停投稿",
    "Unconfirmed": "状态待确认",
}
# 首页“正在投稿”的口径
PUB_IN_SUBMISSION = ["Submitted", "Editor Assigned", "Under Review", "Revision"]

# ---------- 生信分析 ----------
BIO_LANGUAGES = ["R", "Python", "Shell", "Other"]
BIO_STATUSES = ["Pending", "Running", "Completed", "Failed", "Needs Verification"]
BIO_STATUS_LABELS = {
    "Pending": "Pending · 待运行",
    "Running": "Running · 运行中",
    "Completed": "Completed · 已完成",
    "Failed": "Failed · 失败",
    "Needs Verification": "Needs Verification · 待核验",
}
RUNNABLE_EXTENSIONS = {"R": {".r"}, "Python": {".py"}}

# ---------- 日历 ----------
EVENT_TYPES = ["exam", "conference", "milestone", "goal", "deadline", "other"]
EVENT_TYPE_LABELS = {
    "exam": "考试",
    "conference": "会议",
    "milestone": "里程碑",
    "goal": "个人科研目标",
    "deadline": "截止日期",
    "other": "其他",
}
# 聚合视图中的事件来源
CAL_SOURCE_LABELS = {
    "event": "日程",
    "task": "任务截止",
    "experiment": "实验",
    "publication": "投稿/修改期限",
    "project": "项目节点",
    "milestone": "项目里程碑",
    "bioinfo": "分析任务",
}

# ---------- 文件 ----------
FILE_CATEGORIES = [
    "PDF 文献",
    "Word 文档",
    "数据表格",
    "R 脚本",
    "Python 脚本",
    "演示文稿",
    "实验图片",
    "测序/组学数据",
    "统计分析结果",
    "文本笔记",
    "其他",
]
EXTENSION_CATEGORY = {
    ".pdf": "PDF 文献",
    ".doc": "Word 文档",
    ".docx": "Word 文档",
    ".xls": "数据表格",
    ".xlsx": "数据表格",
    ".csv": "数据表格",
    ".tsv": "数据表格",
    ".r": "R 脚本",
    ".rmd": "R 脚本",
    ".qmd": "R 脚本",
    ".py": "Python 脚本",
    ".ipynb": "Python 脚本",
    ".ppt": "演示文稿",
    ".pptx": "演示文稿",
    ".png": "实验图片",
    ".jpg": "实验图片",
    ".jpeg": "实验图片",
    ".tif": "实验图片",
    ".tiff": "实验图片",
    ".bmp": "实验图片",
    ".gif": "实验图片",
    ".scn": "实验图片",
    ".fastq": "测序/组学数据",
    ".fq": "测序/组学数据",
    ".bam": "测序/组学数据",
    ".sam": "测序/组学数据",
    ".vcf": "测序/组学数据",
    ".fasta": "测序/组学数据",
    ".fa": "测序/组学数据",
    ".h5ad": "测序/组学数据",
    ".rds": "统计分析结果",
    ".rdata": "统计分析结果",
    ".pzfx": "统计分析结果",
    ".sav": "统计分析结果",
    ".jmp": "统计分析结果",
    ".md": "文本笔记",
    ".txt": "文本笔记",
}

LABELS = {
    "project_status": PROJECT_STATUS_LABELS,
    "milestone_status": MILESTONE_STATUS_LABELS,
    "task_priority": TASK_PRIORITY_LABELS,
    "task_status": TASK_STATUS_LABELS,
    "lit_type": LIT_TYPE_LABELS,
    "reading_status": READING_STATUS_LABELS,
    "verification": VERIFICATION_LABELS,
    "experiment_status": EXPERIMENT_STATUS_LABELS,
    "experiment_outcome": EXPERIMENT_OUTCOME_LABELS,
    "pub_status": PUB_STATUS_LABELS,
    "bio_status": BIO_STATUS_LABELS,
    "event_type": EVENT_TYPE_LABELS,
    "cal_source": CAL_SOURCE_LABELS,
}


def label(kind: str, code: str | None, empty: str = PENDING) -> str:
    """把代码转换为中文标签；空值显示“待填写”。"""
    if code is None or code == "":
        return empty
    return LABELS.get(kind, {}).get(code, str(code))
