from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc

from app.config import get_settings

settings = get_settings()


def get_scheduler() -> BackgroundScheduler:
    jobstores = {'default': SQLAlchemyJobStore(url=f'sqlite:///{settings.database_name}')}
    executors = {'default': ThreadPoolExecutor(20), 'processpool': ProcessPoolExecutor(5)}
    job_defaults = {'coalesce': False, 'max_instances': 3}
    scheduler = BackgroundScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults,
        timezone=utc,
    )
    return scheduler


def get_async_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    return scheduler
