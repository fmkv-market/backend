from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from myapp.application.dto.address import AddressCreate, AddressData
from myapp.application.exception.address import AddressNotFoundException
from myapp.application.interface.address import IAddressGateway
from myapp.infrastructure.models.address import AddressModel


class AddressGateway(IAddressGateway):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, data: AddressCreate) -> AddressData:
        address = AddressModel(**data.model_dump())
        self._session.add(address)
        await self._session.commit()
        return AddressData.map_to_domain_entity(address)

    async def read_all_by_profile(self, profile_id: int) -> list[AddressData]:
        result = await self._session.execute(
            select(AddressModel).filter_by(profile_id=profile_id)
        )
        addresses = result.scalars().all()
        return [AddressData.map_to_domain_entity(a) for a in addresses]

    async def read_one(self, address_id: int) -> AddressData:
        result = await self._session.execute(
            select(AddressModel).filter_by(id=address_id)
        )
        try:
            address = result.scalar_one()
        except NoResultFound:
            raise AddressNotFoundException
        return AddressData.map_to_domain_entity(address)

    async def delete(self, address_id: int) -> None:
        result = await self._session.execute(
            select(AddressModel).filter_by(id=address_id)
        )
        try:
            address = result.scalar_one()
        except NoResultFound:
            raise AddressNotFoundException
        await self._session.delete(address)
        await self._session.commit()

    async def set_default(self, profile_id: int, address_id: int) -> None:
        await self._session.execute(
            update(AddressModel)
            .where(AddressModel.profile_id == profile_id)
            .values(is_default=False)
        )
        result = await self._session.execute(
            select(AddressModel).filter_by(id=address_id, profile_id=profile_id)
        )
        try:
            address = result.scalar_one()
        except NoResultFound:
            raise AddressNotFoundException
        address.is_default = True
        await self._session.commit()
