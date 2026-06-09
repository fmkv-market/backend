from dishka import FromDishka
from dishka.integrations.faststream import inject as faststream_inject
from faststream.rabbit import RabbitRouter

from myapp.application.dto.profile import ProfileCreate
from myapp.application.interactor.create_profile import CreateProfileInteractor
from myapp.application.interactor.delete_profile import DeleteProfileInteractor
from myapp.infrastructure.message.config import QueueConfig

router = RabbitRouter()


@router.subscriber(QueueConfig.user_created_queue)
@faststream_inject
async def handle_user_created(
    msg: dict,
    interactor: FromDishka[CreateProfileInteractor],
) -> None:
    await interactor.execute(
        ProfileCreate(
            user_id=msg["user_id"],
            first_name=msg.get("first_name"),
            last_name=msg.get("last_name"),
        )
    )


@router.subscriber(QueueConfig.user_deleted_queue)
@faststream_inject
async def handle_user_deleted(
    msg: dict,
    interactor: FromDishka[DeleteProfileInteractor],
) -> None:
    await interactor.by_user_id(msg["user_id"])
