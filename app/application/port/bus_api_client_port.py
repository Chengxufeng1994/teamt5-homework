from abc import ABC, abstractmethod

from app.domain.bus_realtime_near_stop_vo import BusRealTimeNearStop
from app.domain.bus_stop_entity import BusStop


class BusAPIClient(ABC):
    @abstractmethod
    async def get_bus_route_info(self, city: str, route_name: str) -> dict[int, list[BusStop]]:
        pass

    @abstractmethod
    async def get_bus_realtime_near_stop(
        self, city: str, route_name: str
    ) -> list[BusRealTimeNearStop]:
        pass
