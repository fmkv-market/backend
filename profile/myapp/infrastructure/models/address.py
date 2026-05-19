from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from myapp.infrastructure.database import Base


class AddressModel(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"), index=True)
    label: Mapped[str | None] = mapped_column(String(100), nullable=True)
    country: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))
    street: Mapped[str] = mapped_column(String(200))
    house: Mapped[str] = mapped_column(String(20))
    apartment: Mapped[str | None] = mapped_column(String(20), nullable=True)
    entrance: Mapped[str | None] = mapped_column(String(10), nullable=True)
    floor: Mapped[int | None] = mapped_column(Integer, nullable=True)
    intercom: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)

    profile: Mapped["ProfileModel"] = relationship("ProfileModel", back_populates="addresses")
