from __future__ import annotations  # для форвард-референций в типах
from typing import List, Optional
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, select, func
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column, joinedload


class BaseEntity(DeclarativeBase):
    __abstract__ = True

    @classmethod
    def query(cls):
        return select(cls).distinct()


class User(BaseEntity):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    student_id: Mapped[str] = mapped_column(String(10), nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=True)

    courses_taught: Mapped[List[Course]] = relationship("Course", back_populates="teacher")
    questions: Mapped[List[Question]] = relationship("Question", back_populates="user")
    enrollments: Mapped[List[Enrollment]] = relationship("Enrollment", back_populates="user")
    test_results: Mapped[List[TestResultsSummary]] = relationship("TestResultsSummary", back_populates="user")

    @classmethod
    def query(cls):
        return super().query().options(
            joinedload(User.courses_taught),
            joinedload(User.questions),
            joinedload(User.enrollments),
            joinedload(User.test_results)
        )


class Course(BaseEntity):
    __tablename__ = "course"

    course_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    teacher_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.user_id"), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    teacher: Mapped[Optional[User]] = relationship("User", back_populates="courses_taught")
    lessons: Mapped[List[Lesson]] = relationship("Lesson", back_populates="course")
    enrollments: Mapped[List[Enrollment]] = relationship("Enrollment", back_populates="course")
    test_results: Mapped[List[TestResultsSummary]] = relationship("TestResultsSummary", back_populates="course")

    @classmethod
    def query(cls):
        return super().query().options(
            joinedload(Course.teacher),
            joinedload(Course.lessons),
            joinedload(Course.enrollments),
            joinedload(Course.test_results)
        )


class Lesson(BaseEntity):
    __tablename__ = "lesson"

    lesson_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    conspect: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_file_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    course_id: Mapped[Optional[int]] = mapped_column(ForeignKey("course.course_id"), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())

    course: Mapped[Optional[Course]] = relationship("Course", back_populates="lessons")
    questions: Mapped[List[Question]] = relationship("Question", back_populates="lesson")

    @classmethod
    def query(cls):
        return super().query().options(
            joinedload(Lesson.course),
            joinedload(Lesson.questions)
        )


class Question(BaseEntity):
    __tablename__ = "questions"

    question_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    lesson_id: Mapped[Optional[int]] = mapped_column(ForeignKey("lesson.lesson_id"), nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.user_id"), nullable=True)

    lesson: Mapped[Optional[Lesson]] = relationship("Lesson", back_populates="questions")
    user: Mapped[Optional[User]] = relationship("User", back_populates="questions")
    answers: Mapped[List[Answer]] = relationship("Answer", back_populates="question")
    module_result: Mapped[Optional[ModuleResult]] = relationship("ModuleResult", back_populates="question", uselist=False)

    @classmethod
    def query(cls):
        return super().query().options(
            joinedload(Question.lesson),
            joinedload(Question.user),
            joinedload(Question.answers),
            joinedload(Question.module_result)
        )


class Answer(BaseEntity):
    __tablename__ = "answers"

    answer_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_correct: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    question_id: Mapped[Optional[int]] = mapped_column(ForeignKey("questions.question_id"), nullable=True)

    question: Mapped[Optional[Question]] = relationship("Question", back_populates="answers")

    @classmethod
    def query(cls):
        return super().query().options(
            joinedload(Answer.question).joinedload(Question.lesson),
            joinedload(Answer.question).joinedload(Question.user),
            joinedload(Answer.question).joinedload(Question.module_result)
        )


class Enrollment(BaseEntity):
    __tablename__ = "enrollment"

    course_id: Mapped[int] = mapped_column(ForeignKey("course.course_id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), primary_key=True)

    course: Mapped[Course] = relationship("Course", back_populates="enrollments")
    user: Mapped[User] = relationship("User", back_populates="enrollments")

    @classmethod
    def query(cls):
        return super().query().options(
            joinedload(Enrollment.course),
            joinedload(Enrollment.user)
        )


class ModuleResult(BaseEntity):
    __tablename__ = "module_results"

    question_id: Mapped[int] = mapped_column(ForeignKey("questions.question_id"), primary_key=True)
    result: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    question: Mapped[Question] = relationship("Question", back_populates="module_result")

    @classmethod
    def query(cls):
        return super().query().options(
            joinedload(ModuleResult.question).joinedload(Question.lesson),
            joinedload(ModuleResult.question).joinedload(Question.user),
            joinedload(ModuleResult.question).joinedload(Question.answers)
        )


class TestResultsSummary(BaseEntity):
    __tablename__ = "test_results_summary"

    test_result_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    course_id: Mapped[Optional[int]] = mapped_column(ForeignKey("course.course_id"), nullable=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.user_id"), nullable=True)
    summary_results: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    course: Mapped[Optional[Course]] = relationship("Course", back_populates="test_results")
    user: Mapped[Optional[User]] = relationship("User", back_populates="test_results")

    @classmethod
    def query(cls):
        return super().query().options(
            joinedload(TestResultsSummary.course),
            joinedload(TestResultsSummary.user)
        )
