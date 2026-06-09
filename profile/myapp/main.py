import sys
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from faststream.rabbit import RabbitBroker, RabbitQueue
import dishka_faststream as faststream_integration

from myapp.controllers.api import router
from myapp.controllers.message.subscriber import router as message_router
from myapp.infrastructure.ioc.dependencies import init_di
from myapp.infrastructure.message.config import QueueConfig

sys.path.append(str(Path(__file__).parent.parent))

broker = RabbitBroker("amqp://guest:guest@rabbitmq:5672/")
broker.include_router(message_router)


def get_fastapi_app(lifespan) -> FastAPI:
    fastapi_app = FastAPI(lifespan=lifespan)
    fastapi_app.include_router(router)
    return fastapi_app


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.start()
    await broker.declare_queue(RabbitQueue(name=QueueConfig.user_created_queue))
    await broker.declare_queue(RabbitQueue(name=QueueConfig.user_deleted_queue))
    yield
    await broker.stop()


app = get_fastapi_app(lifespan=lifespan)
container = init_di(app=app, broker=broker)
faststream_integration.setup_dishka(container, broker=broker)

if __name__ == "__main__":
    uvicorn.run("myapp.main:app", host="0.0.0.0", reload=True, port=8004)
