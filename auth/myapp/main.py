import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

from myapp.controllers.api import router
from myapp.infrastructure.ioc.dependencies import init_di

sys.path.append(str(Path(__file__).parent.parent))


def get_fastapi_app() -> FastAPI:
    fastapi_app = FastAPI()

    fastapi_app.include_router(router)

    return fastapi_app

app = get_fastapi_app()
init_di(app=app)


if __name__ == "__main__":
    uvicorn.run("myapp.main:app", host="0.0.0.0", reload=True, port=8000)
