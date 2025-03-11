from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.domain.bus_realtime_near_stop_vo import BusRealTimeNearStop
from app.domain.bus_stop_entity import BusStop


class RegisterBusReminderModel(BaseModel):
    city: str
    route_id: str
    route_name: str
    direction: int
    stop_id: str
    stop_name: str
    stop_sequence: int
    alert_method: str
    recipient: str


class BusUseCase(ABC):
    @abstractmethod
    async def get_bus_route_info(self, city: str, route_name: str) -> dict[int, list[BusStop]]:
        """
        獲取指定城市和路線名稱的公車路線資訊。

        :param city: 城市名稱
        :param route_name: 路線名稱
        :return: 包含公車站點資訊的字典
        """
        pass

    @abstractmethod
    async def get_bus_realtime_near_stop(
        self, city: str, route_name: str
    ) -> list[BusRealTimeNearStop]:
        """
        獲取指定城市和路線名稱的即時公車到站資訊。

        :param city: 城市名稱
        :param route_name: 路線名稱
        :return: 包含即時公車到站資訊的列表
        """
        pass

    @abstractmethod
    async def register_bus_reminder(self, reminder_request: RegisterBusReminderModel) -> None:
        """
        註冊公車提醒。

        :param reminder_request: 公車提醒請求模型
        """
        pass

    @abstractmethod
    async def check_bus_reminders(self) -> None:
        """
        檢查公車提醒並發送通知。
        """
        pass
