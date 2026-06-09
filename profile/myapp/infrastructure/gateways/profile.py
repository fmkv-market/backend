from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from myapp.application.dto.profile import ProfileCreate, ProfileData, ProfileUpdate
from myapp.application.exception.profile import ProfileNotFoundException, ProfileAlreadyExistsException
from myapp.application.interface.profile import IProfileSaver, IProfileReader, IProfileUpdater, IProfileDeleter
from myapp.infrastructure.models.profile import ProfileModel


class ProfileGateway(IProfileSaver, IProfileReader, IProfileUpdater, IProfileDeleter):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, data: ProfileCreate) -> ProfileData:
        existing = await self._session.execute(
            select(ProfileModel).filter_by(user_id=data.user_id)
        )
        if existing.scalar_one_or_none() is not None:
            raise ProfileAlreadyExistsException
        profile = ProfileModel(**data.model_dump())
        self._session.add(profile)
        await self._session.commit()
        return ProfileData.map_to_domain_entity(profile)

    async def read_by_user_id(self, user_id: int) -> ProfileData:
        result = await self._session.execute(
            select(ProfileModel).filter_by(user_id=user_id)
        )
        try:
            profile = result.scalar_one()
        except NoResultFound:
            raise ProfileNotFoundException
        return ProfileData.map_to_domain_entity(profile)

    async def read_one(self, profile_id: int) -> ProfileData:
        result = await self._session.execute(
            select(ProfileModel).filter_by(id=profile_id)
        )
        try:
            profile = result.scalar_one()
        except NoResultFound:
            raise ProfileNotFoundException
        return ProfileData.map_to_domain_entity(profile)

    async def update(self, profile_id: int, data: ProfileUpdate) -> ProfileData:
        result = await self._session.execute(
            select(ProfileModel).filter_by(id=profile_id)
        )
        try:
            profile = result.scalar_one()
        except NoResultFound:
            raise ProfileNotFoundException
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(profile, field, value)
        await self._session.commit()
        return ProfileData.map_to_domain_entity(profile)

    async def delete_by_user_id(self, user_id: int) -> None:
        result = await self._session.execute(
            select(ProfileModel).filter_by(user_id=user_id)
        )
        profile = result.scalar_one_or_none()
        if profile is None:
            return
        await self._session.delete(profile)
        await self._session.commit()
