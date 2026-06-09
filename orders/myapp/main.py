import sys

from pathlib import Path

import uvicorn
from faststream.asgi import AsgiFastStream
from faststream.rabbit import RabbitBroker, RabbitQueue

from myapp.controllers.message.subscriber import router as email_subscriber
from myapp.infrastructure.ioc.dependencies import init_di
from myapp.infrastructure.message.config import QueueConfig


sys.path.append(str(Path(__file__).parent.parent))
broker = RabbitBroker("amqp://guest:guest@rabbitmq:5672/")
broker.include_router(router=email_subscriber)
app = AsgiFastStream(broker)
container = init_di(app=app)


@app.after_startup
async def declare_smth() -> None:
    await broker.declare_queue(
        RabbitQueue(
            name=QueueConfig.email_queue,
        ),
    )



if __name__ == "__main__":
    uvicorn.run("myapp.main:app", host="0.0.0.0", reload=True, port=8004)
