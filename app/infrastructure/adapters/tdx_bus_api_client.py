import aiohttp
from loguru import logger

from app.application.port.bus_api_client_port import BusAPIClient
from app.domain.bus_realtime_near_stop_vo import BusRealTimeNearStop
from app.domain.bus_stop_entity import BusStop


class TDXBusAPIClient(BusAPIClient):
    BASE_URL = 'https://tdx.transportdata.tw/api/basic'
    API_VERSION = 'v2'

    def __init__(self, app_id: str, app_key: str, auth_url: str) -> None:
        self.app_id = app_id
        self.app_key = app_key
        self.auth_url = auth_url
        self.access_token = None

    async def _get_access_token(self) -> None:
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'
        data_header = {
            'content-type': content_type,
            'grant_type': grant_type,
            'client_id': self.app_id,
            'client_secret': self.app_key,
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.auth_url, data=data_header) as response:
                    response.raise_for_status()
                    self.access_token = (await response.json())['access_token']
        except aiohttp.ClientError as e:
            logger.error(f'Error getting access token: {e}')
            raise

    async def _get_data_header(self) -> dict:
        if not self.access_token:
            await self._get_access_token()
        headers = {
            'authorization': 'Bearer ' + (self.access_token or ''),
        }
        return headers

    async def _fetch_data(self, endpoint: str, params: dict) -> list[dict]:
        headers = await self._get_data_header()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, params=params, headers=headers) as response:
                    response.raise_for_status()
                    data: list[dict] = await response.json()
                    return data
        except aiohttp.ClientError as e:
            logger.error(f'Error fetching data from {endpoint}: {e}')
            raise

    async def _get_bus_stop_of_route(self, city: str, route_name: str) -> list[dict]:
        url = self.BASE_URL + f'/v2/Bus/StopOfRoute/City/{city}/{route_name}'
        params = {
            # '$filter': (
            #     (
            #         f"contains(RouteName/En,'{route_name}') or "
            #         f"contains(RouteName/Zh_tw,'{route_name}')"
            #     )
            # ),
            '$format': 'JSON',
        }
        bus_stop_route_data = await self._fetch_data(url, params)
        return bus_stop_route_data[:2]

    async def _get_bus_eta(self, city: str, route_name: str) -> list[dict]:
        url = self.BASE_URL + f'/v2/Bus/EstimatedTimeOfArrival/City/{city}/{route_name}'
        params = {
            # '$filter': (
            #     (
            #         f"contains(RouteName/En,'{route_name}') or "
            #         f"contains(RouteName/Zh_tw,'{route_name}')"
            #     )
            # ),
            '$format': 'JSON',
        }
        bus_eta_data = await self._fetch_data(url, params)
        return bus_eta_data

    async def get_bus_realtime_near_stop(
        self, city: str, route_name: str
    ) -> list[BusRealTimeNearStop]:
        url = self.BASE_URL + f'/v2/Bus/RealTimeNearStop/City/{city}/{route_name}'
        params = {
            # '$filter': (
            #     (
            #         f"contains(RouteName/En,'{route_name}') or "
            #         f"contains(RouteName/Zh_tw,'{route_name}')"
            #     )
            # ),
            '$format': 'JSON',
        }
        bus_realtime_near_stop_data = await self._fetch_data(url, params)
        return [
            BusRealTimeNearStop.create(
                bus_realtime_near_stop.get('PlateNumb', ''),
                bus_realtime_near_stop.get('OperatorID', ''),
                bus_realtime_near_stop.get('OperatorNo', ''),
                bus_realtime_near_stop.get('RouteUID', ''),
                bus_realtime_near_stop.get('RouteID', ''),
                bus_realtime_near_stop.get('RouteName.Zh_tw', ''),
                bus_realtime_near_stop.get('SubRouteUID', ''),
                bus_realtime_near_stop.get('SubRouteID', ''),
                bus_realtime_near_stop.get('SubRouteName.Zh_tw', ''),
                bus_realtime_near_stop.get('Direction', ''),
                bus_realtime_near_stop.get('StopUID', ''),
                bus_realtime_near_stop.get('StopID', ''),
                bus_realtime_near_stop.get('StopName.Zh_tw', ''),
                bus_realtime_near_stop.get('StopSequence', -1),
                bus_realtime_near_stop.get('DutyStatus', -1),
                bus_realtime_near_stop.get('BusStatus', -1),
                bus_realtime_near_stop.get('A2EventType', -1),
                bus_realtime_near_stop.get('GPSTime', ''),
                bus_realtime_near_stop.get('TripStartTimeType', -1),
                bus_realtime_near_stop.get('TripStartTime', ''),
                bus_realtime_near_stop.get('SrcUpdateTime', ''),
                bus_realtime_near_stop.get('UpdateTime', ''),
            )
            for bus_realtime_near_stop in bus_realtime_near_stop_data
        ]

    async def get_bus_route_info(self, city: str, route_name: str) -> dict[int, list[BusStop]]:
        """取得指定公車路線的去程與回程站點資訊"""
        # 取得公車路線的去程與回程站點資訊
        bus_stop_route_data = await self._get_bus_stop_of_route(city, route_name)
        # 取得及時到站資訊
        bus_eta_data = await self._get_bus_eta(city, route_name)

        eta_lookup: dict[tuple, dict] = {
            (bus_eta['StopID'], bus_eta['Direction']): bus_eta for bus_eta in bus_eta_data
        }

        route_info: dict[int, list[BusStop]] = {
            0: [],
            1: [],
        }

        for bus_stop_route in bus_stop_route_data:
            direction = bus_stop_route['Direction']
            stops = bus_stop_route['Stops']
            route_id = bus_stop_route['RouteID']
            route_info[direction] = []

            for stop in stops:
                stop_id = stop['StopID']

                # 取得 ETA 資訊 (若無，則預設值)
                bus_eta = eta_lookup.get((stop_id, direction), {})
                estimate_time = bus_eta.get('EstimateTime', -1)
                stop_status = bus_eta.get('StopStatus', 0)

                bus_stop_entity = BusStop(
                    route_id=route_id,
                    station_id=stop['StationID'],
                    stop_uid=stop['StopUID'],
                    stop_id=stop['StopID'],
                    stop_name=stop['StopName']['Zh_tw'],
                    stop_boarding=stop['StopBoarding'],
                    stop_sequence=stop['StopSequence'],
                    location_city_code=stop['LocationCityCode'],
                    estimate_time=estimate_time,
                    stop_status=stop_status,
                )
                route_info[direction].append(bus_stop_entity)

        return route_info
