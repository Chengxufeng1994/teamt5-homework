from datetime import datetime

from loguru import logger

from app.dependencies import get_bus_service_manually


async def bus_reminder_job() -> None:
    logger.info(f'🚍 Checking bus schedule at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    try:
        bus_service = await get_bus_service_manually()
        await bus_service.check_bus_reminders()
    except Exception as e:
        logger.error(f'Error in bus_reminder_job: {e}')
