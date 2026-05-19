from dishka import FromDishka
from dishka.integrations.faststream import inject as faststream_inject
from faststream.rabbit import RabbitRouter

from myapp.application.dto.profile import ProfileCreate
from myapp.application.interactor.create_profile import CreateProfileInteractor
from myapp.infrastructure.message.config import QueueConfig

router = RabbitRouter()


@router.subscriber(QueueConfig.user_created_queue)
@faststream_inject
async def handle_user_created(
    msg: dict,
    interactor: FromDishka[CreateProfileInteractor],
) -> None:
    await interactor.execute(ProfileCreate(user_id=msg["user_id"]))
