from sqlalchemy import (
    TIMESTAMP,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Boolean,
)
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, server_default="")
    surname = Column(String, nullable=False, server_default="")
    verification_code = Column(Integer, unique=True)
    password = Column(String, nullable=False)
    profile_image = Column(
        String,
        nullable=False,
        server_default="https://mykaleidoscope.ru/x/uploads/posts/2023-05/1684818829_mykaleidoscope-ru-p-strizhka-stasa-pekhi-pinterest-69.jpg",
    )
    weight = Column(Float)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    title = Column(String, nullable=False)
    additional_info = Column(String, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    ended_at = Column(TIMESTAMP(timezone=True))
    average_time_resting = Column(Integer, nullable=True)


class IndividualExercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, nullable=False, primary_key=True)
    workout_id = Column(Integer, ForeignKey("workouts.id", ondelete="SET NULL"))
    title = Column(String, nullable=False)


class Set(Base):
    __tablename__ = "set"

    id = Column(Integer, nullable=False, primary_key=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="SET NULL"))
    weight = Column(Float, server_default="0")
    units = Column(Boolean, nullable=False, server_default="False")
    repetitions = Column(Integer, nullable=False, server_default="1")
    performed_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
