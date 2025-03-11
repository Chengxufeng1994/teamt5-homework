from app.domain.bus_reminder_entity import BusReminder as BusReminderModel
from app.domain.bus_reminder_repository import BusReminderRepository
from app.infrastructure.adapters.repositories.sqlalchemy.orm_entity.bus_reminder_entity import (
    BusReminder,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class SqlalchemyBusReminderRepository(BusReminderRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, model: BusReminderModel) -> None:
        entity = BusReminder(
            city=model.city,
            route_id=model.route_id,
            route_name=model.route_name,
            direction=model.direction,
            stop_id=model.stop_id,
            stop_name=model.stop_name,
            stop_sequence=model.stop_sequence,
            alert_method=model.alert_method,
            recipient=model.recipient,
        )

        async with self.db:
            try:
                self.db.add(entity)
                await self.db.flush()
                await self.db.commit()
            except Exception as e:
                await self.db.rollback()
                raise e

    async def get_all(self) -> list[BusReminderModel]:
        stmt = select(BusReminder)
        result = await self.db.execute(stmt)
        reminders = result.scalars().all()

        return [
            BusReminderModel(
                id=elem.id,
                city=elem.city,
                route_id=elem.route_id,
                route_name=elem.route_name,
                direction=elem.direction,
                stop_id=elem.stop_id,
                stop_name=elem.stop_name,
                stop_sequence=elem.stop_sequence,
                alert_method=elem.alert_method,
                recipient=elem.recipient,
            )
            for elem in reminders
        ]
