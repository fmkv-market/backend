from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates

from myapp.infrastructure.database import Base


class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True)
    parent_id: Mapped[str] = mapped_column(ForeignKey("categories.id"), nullable=True)

