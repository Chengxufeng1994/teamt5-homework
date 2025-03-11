from loguru import logger

from app.application.port.bus_api_client_port import BusAPIClient
from app.application.port.email_service_port import EmailService
from app.application.usecase.bus_usecase import BusUseCase, RegisterBusReminderModel
from app.domain.bus_realtime_near_stop_vo import BusRealTimeNearStop
from app.domain.bus_reminder_entity import BusReminder
from app.domain.bus_reminder_repository import BusReminderRepository
from app.domain.bus_stop_entity import BusStop


class BusService(BusUseCase):
    def __init__(
        self,
        bus_reminder_repository: BusReminderRepository,
        bus_api_client: BusAPIClient,
        email_service: EmailService,
    ) -> None:
        self.bus_reminder_repository = bus_reminder_repository
        self.bus_api_client = bus_api_client
        self.email_service = email_service

    async def get_bus_route_info(self, city: str, route_name: str) -> dict[int, list[BusStop]]:
        try:
            return await self.bus_api_client.get_bus_route_info(city, route_name)
        except Exception as e:
            logger.error(f'Error getting bus route info: {e}')
            raise

    async def get_bus_realtime_near_stop(
        self, city: str, route_name: str
    ) -> list[BusRealTimeNearStop]:
        try:
            return await self.bus_api_client.get_bus_realtime_near_stop(city, route_name)
        except Exception as e:
            logger.error(f'Error getting bus realtime near stop: {e}')
            raise

    async def check_bus_reminders(self) -> None:
        try:
            bus_reminders = await self.bus_reminder_repository.get_all()
            for reminder in bus_reminders:
                bus_realtime_list = await self.bus_api_client.get_bus_realtime_near_stop(
                    reminder.city, reminder.route_name
                )
                for bus in bus_realtime_list:
                    logger.info(bus)
                    if (
                        0 < reminder.stop_sequence - bus.stop_sequence <= 5
                        and bus.direction == reminder.direction
                    ):
                        # 發送通知
                        self.email_service.send_email(
                            reminder.recipient,
                            f'【提醒】{reminder.route_name} 即將到達 {reminder.stop_name}',
                            f'您的公車 {reminder.route_name} 即將到達您的目標站點，請準備上車！',
                        )
        except Exception as e:
            logger.error(f'Error checking bus reminders: {e}')
            raise

    async def register_bus_reminder(self, reminder_request: RegisterBusReminderModel) -> None:
        try:
            entity = BusReminder.create(**reminder_request.model_dump())
            await self.bus_reminder_repository.create(entity)
        except Exception as e:
            logger.error(f'Error registering bus reminder: {e}')
            raise
