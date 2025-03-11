from dataclasses import dataclass


@dataclass
class BusStop:
    route_id: str
    station_id: str
    stop_uid: str
    stop_id: str
    stop_name: str
    stop_boarding: int
    stop_sequence: int
    location_city_code: str
    estimate_time: int
    stop_status: int
