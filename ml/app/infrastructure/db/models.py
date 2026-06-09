from sqlalchemy import Float, String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class UserFeatures(Base):
    __tablename__ = "user_features"

    user_id: Mapped[str] = mapped_column(String(30), primary_key=True)  # String
    user_cart_update_turn_rate: Mapped[float] = mapped_column(Float, nullable=False)
    user_click_turn_rate: Mapped[float] = mapped_column(Float, nullable=False)
    user_conversion_rate: Mapped[float] = mapped_column(Float, nullable=False)


class ItemFeatures(Base):
    __tablename__ = "item_features"

    item_id: Mapped[str] = mapped_column(String(30), primary_key=True)  # String
    item_cart_update_turn_rate: Mapped[float] = mapped_column(Float, nullable=False)
    item_click_turn_rate: Mapped[float] = mapped_column(Float, nullable=False)
    item_conversion_rate: Mapped[float] = mapped_column(Float, nullable=False)


class UserItemFeatures(Base):
    __tablename__ = "user_item_features"

    user_id: Mapped[str] = mapped_column(String(30), primary_key=True)
    item_id: Mapped[str] = mapped_column(String(30), primary_key=True)
    u2i_cart_updates: Mapped[float] = mapped_column(Float, nullable=False)
    u2i_mean_time_between_cartupdates: Mapped[float] = mapped_column(Float, nullable=False)


class ItemCatalog(Base):
    __tablename__ = "item_catalog"

    item_id: Mapped[str] = mapped_column(String(30), primary_key=True)
    product_category: Mapped[str] = mapped_column(String, nullable=False)


class ItemEmbedding(Base):
    __tablename__ = "item_embeddings"

    item_id: Mapped[str] = mapped_column(String(30), primary_key=True)
    embedding: Mapped[list[float]] = mapped_column(ARRAY(Float), nullable=False)