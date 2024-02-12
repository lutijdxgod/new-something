from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, ForeignKey  # , JSON
from sqlalchemy.dialects.postgresql import ARRAY
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
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
