from myapp.application.dto.address import AddressCreate, AddressData
from myapp.application.interface.address import IAddressGateway
from myapp.application.interface.profile import IProfileReader


class AddAddressInteractor:
    def __init__(self, gateway: IAddressGateway, reader: IProfileReader) -> None:
        self._gateway = gateway
        self._reader = reader

    async def execute(self, user_id: int, data: AddressCreate) -> AddressData:
        profile = await self._reader.read_by_user_id(user_id)
        data_with_profile = data.model_copy(update={"profile_id": profile.id})
        return await self._gateway.save(data_with_profile)


class GetAddressesInteractor:
    def __init__(self, gateway: IAddressGateway, reader: IProfileReader) -> None:
        self._gateway = gateway
        self._reader = reader

    async def execute(self, user_id: int) -> list[AddressData]:
        profile = await self._reader.read_by_user_id(user_id)
        return await self._gateway.read_all_by_profile(profile.id)


class DeleteAddressInteractor:
    def __init__(self, gateway: IAddressGateway) -> None:
        self._gateway = gateway

    async def execute(self, address_id: int) -> None:
        await self._gateway.delete(address_id)


class SetDefaultAddressInteractor:
    def __init__(self, gateway: IAddressGateway, reader: IProfileReader) -> None:
        self._gateway = gateway
        self._reader = reader

    async def execute(self, user_id: int, address_id: int) -> None:
        profile = await self._reader.read_by_user_id(user_id)
        await self._gateway.set_default(profile.id, address_id)
