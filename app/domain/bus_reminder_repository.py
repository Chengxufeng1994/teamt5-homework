from abc import ABC, abstractmethod

from app.domain.bus_reminder_entity import BusReminder


class BusReminderRepository(ABC):
    @abstractmethod
    async def create(self, reminder: BusReminder) -> None:
        pass

    @abstractmethod
    async def get_all(self) -> list[BusReminder]:
        pass
