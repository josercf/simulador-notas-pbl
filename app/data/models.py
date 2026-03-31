from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.database import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    modules: Mapped[list[Module]] = relationship(back_populates="course", cascade="all, delete-orphan")


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    course: Mapped[Course] = relationship(back_populates="modules")
    classrooms: Mapped[list[Classroom]] = relationship(back_populates="module", cascade="all, delete-orphan")


class Classroom(Base):
    __tablename__ = "classrooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id"))
    total_sprints: Mapped[int] = mapped_column(Integer, default=10)
    weeks_per_sprint: Mapped[int] = mapped_column(Integer, default=2)
    module: Mapped[Module] = relationship(back_populates="classrooms")
    students: Mapped[list[Student]] = relationship(back_populates="classroom", cascade="all, delete-orphan")
    groups: Mapped[list[Group]] = relationship(back_populates="classroom", cascade="all, delete-orphan")


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    classroom: Mapped[Classroom] = relationship(back_populates="groups")
    students: Mapped[list[Student]] = relationship(back_populates="group")


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    profile: Mapped[str] = mapped_column(String(40))
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    group_id: Mapped[int | None] = mapped_column(ForeignKey("groups.id"), nullable=True)
    classroom: Mapped[Classroom] = relationship(back_populates="students")
    group: Mapped[Group | None] = relationship(back_populates="students")


class Sprint(Base):
    __tablename__ = "sprints"

    id: Mapped[int] = mapped_column(primary_key=True)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    sprint_number: Mapped[int] = mapped_column(Integer)
    __table_args__ = (UniqueConstraint("classroom_id", "sprint_number", name="uix_classroom_sprint"),)


class Week(Base):
    __tablename__ = "weeks"

    id: Mapped[int] = mapped_column(primary_key=True)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    sprint_number: Mapped[int] = mapped_column(Integer)
    week_number: Mapped[int] = mapped_column(Integer)


class AssessmentItem(Base):
    __tablename__ = "assessment_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    item_type: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(120))
    max_points: Mapped[float] = mapped_column(Float)
    weight: Mapped[float] = mapped_column(Float)


class Artifact(Base):
    __tablename__ = "artifacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    sprint_number: Mapped[int] = mapped_column(Integer)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))
    group_grade: Mapped[float] = mapped_column(Float)


class WeightedActivity(Base):
    __tablename__ = "weighted_activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    week_number: Mapped[int] = mapped_column(Integer)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    grade: Mapped[float] = mapped_column(Float)


class Exam(Base):
    __tablename__ = "exams"

    id: Mapped[int] = mapped_column(primary_key=True)
    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    grade: Mapped[float] = mapped_column(Float)


class StudentContribution(Base):
    __tablename__ = "student_contributions"

    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("simulation_runs.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    sprint_number: Mapped[int] = mapped_column(Integer)
    factor: Mapped[float] = mapped_column(Float)


class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    scenario_name: Mapped[str] = mapped_column(String(40))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    results: Mapped[list[ScenarioResult]] = relationship(back_populates="run", cascade="all, delete-orphan")


class ScenarioResult(Base):
    __tablename__ = "scenario_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    run_id: Mapped[int] = mapped_column(ForeignKey("simulation_runs.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    sprint_number: Mapped[int] = mapped_column(Integer)
    artifact_grade: Mapped[float] = mapped_column(Float)
    activity_grade: Mapped[float] = mapped_column(Float)
    cumulative_grade: Mapped[float] = mapped_column(Float)
    projected_final_grade: Mapped[float] = mapped_column(Float)
    risk_level: Mapped[str] = mapped_column(String(20))
    run: Mapped[SimulationRun] = relationship(back_populates="results")
