# ssl patch
from gevent import monkey

monkey.patch_all()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from . import config
from . import models
from . import routers

origins = [
    "http://localhost:57805",
    "http://localhost:8080",
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if models.engine is not None:
        # Close the DB connection
        await models.close_session()


def create_app(settings=None):
    if not settings:
        settings = config.get_settings()

    app = FastAPI(lifespan=lifespan)
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # app.mount("/Static", StaticFiles(directory="./static"), name="Static")

    models.init_db(settings)

    routers.init_router(app)
    return app
