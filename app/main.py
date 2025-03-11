import sys
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from app.bus_reminder_job import bus_reminder_job
from app.config import get_settings
from app.infrastructure.adapters.repositories.sqlalchemy.orm_entity.bus_reminder_entity import (  # noqa: F401
    BusReminder,
)
from app.infrastructure.database import Base, get_async_engine
from app.infrastructure.scheduler import get_async_scheduler
from app.routers.bus_router import router as bus_router

logger.remove()
logger.add(
    sys.stdout,
    format='{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} | {message}',
    level='INFO',
)
logger.add('app.log', rotation='10 MB', level='DEBUG')


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    scheduler = get_async_scheduler()
    scheduler.add_job(
        bus_reminder_job,
        'interval',
        seconds=30,
        id='bus_reminder_job',
        replace_existing=True,
        coalesce=True,
    )

    if not scheduler.running:
        scheduler.start()

    engine = get_async_engine()
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
    finally:
        job = scheduler.get_job('bus_reminder_job')
        if job:
            scheduler.remove_job('bus_reminder_job')
        scheduler.shutdown(wait=False)
        await engine.dispose()


env = get_settings()

app = FastAPI(
    title=env.app_name,
    version=env.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    max_age=-1,
)

app.include_router(bus_router)
