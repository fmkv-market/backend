import uuid

from sqlalchemy import func, UUID, CheckConstraint, and_, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import CITEXT

from myapp.application.services.addresses import AddressComponent, AddressLeaf, AddressComposite
from myapp.infrastructure.database import Base
from myapp.infrastructure.models import UserModel


class AddressModel(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    level: Mapped[str] = mapped_column(String)   # country/city/street/house
    value: Mapped[str] = mapped_column(String)

    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("addresses.id"), nullable=True
    )

    # Самореференция: один адрес содержит дочерние адреса
    children: Mapped[list["AddressModel"]] = relationship(
        "AddressModel",
        back_populates="parent",
        cascade="all, delete-orphan",
    )
    parent: Mapped["AddressModel" | None] = relationship(
        "AddressModel",
        back_populates="children",
        remote_side="AddressModel.id",
    )

    # Связь с пользователями
    users: Mapped[list[UserModel]] = relationship(
        "UserModel", back_populates="address"
    )

    def to_composite(self) -> AddressComponent:
        """
        Преобразует ORM-дерево в дерево Composite-объектов.
        Если нет детей — возвращает Leaf, иначе — Composite.
        """
        if not self.children:
            return AddressLeaf(level=self.level, value=self.value)

        node = AddressComposite(level=self.level, value=self.value)
        for child in self.children:
            node.add(child.to_composite())
        return node
