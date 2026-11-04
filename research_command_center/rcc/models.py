"""SQLAlchemy ORM 数据模型。

设计要点：
- 每个领域一张主表，附属信息独立成表（笔记、附件、状态历史、运行日志……）。
- 外键：附属记录随主记录级联删除（CASCADE）；跨模块引用（如任务→项目）使用 SET NULL，
  服务层另外阻止删除仍有关联数据的项目，推荐“归档”。
- 文件只保存“绝对路径引用”，从不保存或修改原始文件内容。
- API Key 不入库：ai_settings 只记录环境变量名或系统密钥环条目名。
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def now() -> datetime:
    return datetime.now().replace(microsecond=0)


class Base(DeclarativeBase):
    def to_dict(self) -> dict[str, Any]:
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=now, onupdate=now, nullable=False)


# --------------------------------------------------------------------------- meta
class AppMeta(Base):
    __tablename__ = "app_meta"
    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[Optional[str]] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=now, onupdate=now)


# ----------------------------------------------------------------------- projects
class Project(TimestampMixin, Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(300), unique=True, nullable=False)
    research_direction: Mapped[Optional[str]] = mapped_column(Text)
    scientific_question: Mapped[Optional[str]] = mapped_column(Text)
    core_hypothesis: Mapped[Optional[str]] = mapped_column(Text)
    lead: Mapped[Optional[str]] = mapped_column(String(300))
    participants: Mapped[Optional[str]] = mapped_column(Text)
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    expected_end_date: Mapped[Optional[date]] = mapped_column(Date)
    status: Mapped[Optional[str]] = mapped_column(String(30), index=True)
    progress: Mapped[Optional[int]] = mapped_column(Integer)  # 0-100；NULL = 待填写
    key_paths: Mapped[Optional[str]] = mapped_column(Text)  # 每行一个路径
    current_stage: Mapped[Optional[str]] = mapped_column(Text)
    next_steps: Mapped[Optional[str]] = mapped_column(Text)
    main_risks: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    source_note: Mapped[Optional[str]] = mapped_column(Text)  # 信息来源说明
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    milestones: Mapped[list["ProjectMilestone"]] = relationship(
        back_populates="project", cascade="all, delete-orphan", passive_deletes=True
    )


class ProjectMilestone(TimestampMixin, Base):
    __tablename__ = "project_milestones"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    due_date: Mapped[Optional[date]] = mapped_column(Date, index=True)
    status: Mapped[str] = mapped_column(String(30), default="Planned", nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    note: Mapped[Optional[str]] = mapped_column(Text)
    project: Mapped[Project] = relationship(back_populates="milestones")


# -------------------------------------------------------------------------- tasks
class Task(TimestampMixin, Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    priority: Mapped[str] = mapped_column(String(20), default="Medium", nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), default="Todo", nullable=False, index=True)
    due_date: Mapped[Optional[date]] = mapped_column(Date, index=True)
    estimated_hours: Mapped[Optional[float]] = mapped_column(Float)
    # 四象限覆盖：NULL = 自动判断
    is_important: Mapped[Optional[bool]] = mapped_column(Boolean)
    is_urgent: Mapped[Optional[bool]] = mapped_column(Boolean)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, index=True)


# --------------------------------------------------------------------- literature
class Literature(TimestampMixin, Base):
    __tablename__ = "literature"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(Text)  # 无法识别时为 NULL（待核实）
    authors: Mapped[Optional[str]] = mapped_column(Text)  # “; ”分隔
    year: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    journal: Mapped[Optional[str]] = mapped_column(String(500))
    doi: Mapped[Optional[str]] = mapped_column(String(300), unique=True)  # 规范化小写
    pmid: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    pub_type: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    keywords: Mapped[Optional[str]] = mapped_column(Text)  # 逗号分隔
    research_tags: Mapped[Optional[str]] = mapped_column(Text)  # 研究方向标签，逗号分隔
    abstract: Mapped[Optional[str]] = mapped_column(Text)
    file_path: Mapped[Optional[str]] = mapped_column(Text)  # 原始 PDF 绝对路径（只读引用）
    file_hash: Mapped[Optional[str]] = mapped_column(String(64), index=True)
    file_size: Mapped[Optional[int]] = mapped_column(Integer)
    page_count: Mapped[Optional[int]] = mapped_column(Integer)
    is_uploaded_copy: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reading_status: Mapped[str] = mapped_column(String(20), default="Unread", nullable=False, index=True)
    value_note: Mapped[Optional[str]] = mapped_column(Text)  # 对项目的价值
    limitation_note: Mapped[Optional[str]] = mapped_column(Text)  # 局限
    verification_status: Mapped[str] = mapped_column(String(30), default="Unverified", nullable=False)
    metadata_sources: Mapped[Optional[str]] = mapped_column(Text)  # JSON：字段 → 来源
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    verification_note: Mapped[Optional[str]] = mapped_column(Text)
    fulltext_indexed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    notes: Mapped[list["LiteratureNote"]] = relationship(
        back_populates="literature", cascade="all, delete-orphan", passive_deletes=True
    )


class LiteratureNote(TimestampMixin, Base):
    __tablename__ = "literature_notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    literature_id: Mapped[int] = mapped_column(ForeignKey("literature.id", ondelete="CASCADE"), index=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), index=True)
    note_type: Mapped[Optional[str]] = mapped_column(String(50))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    page_ref: Mapped[Optional[str]] = mapped_column(String(50))
    literature: Mapped[Literature] = relationship(back_populates="notes")


class ProjectLiterature(Base):
    __tablename__ = "project_literature"
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True)
    literature_id: Mapped[int] = mapped_column(ForeignKey("literature.id", ondelete="CASCADE"), primary_key=True)
    relevance: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now, nullable=False)


# -------------------------------------------------------------------- experiments
class ExperimentBatch(TimestampMixin, Base):
    __tablename__ = "experiment_batches"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), index=True)
    code: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    __table_args__ = (UniqueConstraint("project_id", "code", name="uq_batch_project_code"),)


class Experiment(TimestampMixin, Base):
    __tablename__ = "experiments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), index=True)
    batch_id: Mapped[Optional[int]] = mapped_column(ForeignKey("experiment_batches.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    experiment_date: Mapped[Optional[date]] = mapped_column(Date, index=True)
    status: Mapped[str] = mapped_column(String(20), default="Planned", nullable=False, index=True)
    purpose: Mapped[Optional[str]] = mapped_column(Text)
    groups: Mapped[Optional[str]] = mapped_column(Text)
    model_system: Mapped[Optional[str]] = mapped_column(Text)  # 细胞或动物模型
    reagents: Mapped[Optional[str]] = mapped_column(Text)
    instruments: Mapped[Optional[str]] = mapped_column(Text)
    parameters: Mapped[Optional[str]] = mapped_column(Text)  # JSON 列表 [{name, value, unit}]
    raw_data_path: Mapped[Optional[str]] = mapped_column(Text)  # 主原始数据路径（只读引用）
    result_summary: Mapped[Optional[str]] = mapped_column(Text)
    outcome: Mapped[Optional[str]] = mapped_column(String(30))  # 成功/部分/失败/待评估
    failure_reason: Mapped[Optional[str]] = mapped_column(Text)
    next_experiment: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    attachments: Mapped[list["ExperimentAttachment"]] = relationship(
        back_populates="experiment", cascade="all, delete-orphan", passive_deletes=True
    )


class ExperimentAttachment(Base):
    __tablename__ = "experiment_attachments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    experiment_id: Mapped[int] = mapped_column(ForeignKey("experiments.id", ondelete="CASCADE"), index=True)
    path: Mapped[str] = mapped_column(Text, nullable=False)  # 绝对路径，只读引用
    kind: Mapped[Optional[str]] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(Text)
    exists_last_check: Mapped[Optional[bool]] = mapped_column(Boolean)
    file_size: Mapped[Optional[int]] = mapped_column(Integer)
    file_mtime: Mapped[Optional[datetime]] = mapped_column(DateTime)
    last_checked_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now, nullable=False)
    experiment: Mapped[Experiment] = relationship(back_populates="attachments")
    __table_args__ = (UniqueConstraint("experiment_id", "path", name="uq_attachment_path"),)


# ------------------------------------------------------------------- publications
class Publication(TimestampMixin, Base):
    __tablename__ = "publications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), index=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    author_order: Mapped[Optional[str]] = mapped_column(Text)
    first_author: Mapped[Optional[str]] = mapped_column(String(300))
    corresponding_author: Mapped[Optional[str]] = mapped_column(String(300))
    target_journal: Mapped[Optional[str]] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(30), default="Draft", nullable=False, index=True)
    planned_submission_date: Mapped[Optional[date]] = mapped_column(Date)  # 计划投稿期限
    submission_date: Mapped[Optional[date]] = mapped_column(Date)
    editor_assigned_date: Mapped[Optional[date]] = mapped_column(Date)
    under_review_date: Mapped[Optional[date]] = mapped_column(Date)  # 送外审日期
    revision_due_date: Mapped[Optional[date]] = mapped_column(Date, index=True)
    decision_date: Mapped[Optional[date]] = mapped_column(Date)  # 拒稿或接收日期
    published_date: Mapped[Optional[date]] = mapped_column(Date)
    submission_url: Mapped[Optional[str]] = mapped_column(Text)
    file_paths: Mapped[Optional[str]] = mapped_column(Text)  # 每行一个
    next_action: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    source_note: Mapped[Optional[str]] = mapped_column(Text)

    history: Mapped[list["PublicationStatusHistory"]] = relationship(
        back_populates="publication", cascade="all, delete-orphan", passive_deletes=True,
        order_by="PublicationStatusHistory.id",
    )


class PublicationStatusHistory(Base):
    """每一次状态变更都由用户手动确认，系统不会根据日期推断。"""
    __tablename__ = "publication_status_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    publication_id: Mapped[int] = mapped_column(ForeignKey("publications.id", ondelete="CASCADE"), index=True)
    from_status: Mapped[Optional[str]] = mapped_column(String(30))
    to_status: Mapped[str] = mapped_column(String(30), nullable=False)
    event_date: Mapped[Optional[date]] = mapped_column(Date)
    journal: Mapped[Optional[str]] = mapped_column(String(500))
    note: Mapped[Optional[str]] = mapped_column(Text)
    confirmed_by_user: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=now, nullable=False)
    publication: Mapped[Publication] = relationship(back_populates="history")


# ---------------------------------------------------------------- bioinformatics
class BioinformaticsJob(TimestampMixin, Base):
    __tablename__ = "bioinformatics_jobs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), index=True)
    name: Mapped[str] = mapped_column(String(500), nullable=False)
    purpose: Mapped[Optional[str]] = mapped_column(Text)
    language: Mapped[Optional[str]] = mapped_column(String(20))
    script_path: Mapped[Optional[str]] = mapped_column(Text)
    script_args: Mapped[Optional[str]] = mapped_column(Text)  # 每行一个参数
    working_dir: Mapped[Optional[str]] = mapped_column(Text)
    data_paths: Mapped[Optional[str]] = mapped_column(Text)  # 每行一个
    data_source: Mapped[Optional[str]] = mapped_column(Text)
    output_paths: Mapped[Optional[str]] = mapped_column(Text)  # 每行一个
    status: Mapped[str] = mapped_column(String(30), default="Pending", nullable=False, index=True)
    run_started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    run_finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    error_log: Mapped[Optional[str]] = mapped_column(Text)
    result_summary: Mapped[Optional[str]] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    runs: Mapped[list["BioinformaticsRun"]] = relationship(
        back_populates="job", cascade="all, delete-orphan", passive_deletes=True,
        order_by="BioinformaticsRun.id",
    )


class BioinformaticsRun(Base):
    """运行/日志记录：既可记录本系统执行的运行，也可手动登记在别处运行的结果。"""
    __tablename__ = "bioinformatics_runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("bioinformatics_jobs.id", ondelete="CASCADE"), index=True)
    source: Mapped[str] = mapped_column(String(20), default="manual", nullable=False)  # manual / executed
    command: Mapped[Optional[str]] = mapped_column(Text)  # JSON 列表
    script_sha256: Mapped[Optional[str]] = mapped_column(String(64))
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    exit_code: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[Optional[str]] = mapped_column(String(30))
    log_path: Mapped[Optional[str]] = mapped_column(Text)
    log_excerpt: Mapped[Optional[str]] = mapped_column(Text)
    note: Mapped[Optional[str]] = mapped_column(Text)
    pid: Mapped[Optional[int]] = mapped_column(Integer)
    confirmed_by_user: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now, nullable=False)
    job: Mapped[BioinformaticsJob] = relationship(back_populates="runs")


# ----------------------------------------------------------------------- calendar
class CalendarEvent(TimestampMixin, Base):
    __tablename__ = "calendar_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    event_type: Mapped[str] = mapped_column(String(30), default="other", nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    location: Mapped[Optional[str]] = mapped_column(String(500))
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


# -------------------------------------------------------------------------- files
class FileIndex(TimestampMixin, Base):
    __tablename__ = "files_index"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), index=True)
    path: Mapped[str] = mapped_column(Text, unique=True, nullable=False)  # 绝对路径
    file_name: Mapped[str] = mapped_column(String(500), nullable=False)
    extension: Mapped[Optional[str]] = mapped_column(String(30))
    category: Mapped[Optional[str]] = mapped_column(String(50), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    exists: Mapped[Optional[bool]] = mapped_column(Boolean)
    size_bytes: Mapped[Optional[int]] = mapped_column(Integer)
    modified_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    last_checked_at: Mapped[Optional[datetime]] = mapped_column(DateTime)


# ----------------------------------------------------------------------------- AI
class AISetting(TimestampMixin, Base):
    """模型配置。API Key 不保存在这里：只保存环境变量名，或系统密钥环中的条目名。"""
    __tablename__ = "ai_settings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    provider_type: Mapped[str] = mapped_column(String(30), nullable=False)  # anthropic / openai_compatible
    base_url: Mapped[Optional[str]] = mapped_column(Text)
    model: Mapped[str] = mapped_column(String(200), nullable=False)
    key_storage: Mapped[str] = mapped_column(String(20), default="env", nullable=False)  # env / keyring / none
    api_key_env_var: Mapped[Optional[str]] = mapped_column(String(100))
    max_tokens: Mapped[int] = mapped_column(Integer, default=8000, nullable=False)
    temperature: Mapped[Optional[float]] = mapped_column(Float)  # 仅 OpenAI 兼容接口使用
    effort: Mapped[Optional[str]] = mapped_column(String(20))  # 仅 Anthropic 使用，可空
    use_fallbacks: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class AIInteraction(Base):
    """AI 调用留痕：发送了什么范围的数据、得到了什么回答。"""
    __tablename__ = "ai_interactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"), index=True)
    profile_name: Mapped[Optional[str]] = mapped_column(String(100))
    model: Mapped[Optional[str]] = mapped_column(String(200))
    request_type: Mapped[Optional[str]] = mapped_column(String(50))
    context_scopes: Mapped[Optional[str]] = mapped_column(Text)  # JSON 列表
    question: Mapped[Optional[str]] = mapped_column(Text)
    context_chars: Mapped[Optional[int]] = mapped_column(Integer)
    response: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="ok", nullable=False)
    error: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now, nullable=False, index=True)


# ------------------------------------------------------------------ activity logs
class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False)
    entity_id: Mapped[Optional[int]] = mapped_column(Integer)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text)
    details: Mapped[Optional[str]] = mapped_column(Text)  # JSON
    created_at: Mapped[datetime] = mapped_column(DateTime, default=now, nullable=False, index=True)
    __table_args__ = (Index("ix_activity_entity", "entity_type", "entity_id"),)


ENTITY_MODELS = {
    "project": Project,
    "milestone": ProjectMilestone,
    "task": Task,
    "literature": Literature,
    "literature_note": LiteratureNote,
    "experiment": Experiment,
    "experiment_batch": ExperimentBatch,
    "experiment_attachment": ExperimentAttachment,
    "publication": Publication,
    "bioinformatics_job": BioinformaticsJob,
    "calendar_event": CalendarEvent,
    "file": FileIndex,
    "ai_setting": AISetting,
}
