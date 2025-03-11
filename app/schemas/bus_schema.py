from pydantic import BaseModel


class BusStopSchema(BaseModel):
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


class DirectionSchema(BaseModel):
    direction: int  # 0 或 1
    direction_name: str
    stops: list[BusStopSchema]


class BusRouteInfoResponse(BaseModel):
    city: str
    route_name: str
    outbound: DirectionSchema
    inbound: DirectionSchema


class BusReminderRequestSchema(BaseModel):
    city: str
    route_id: str
    route_name: str
    direction: int
    stop_id: str
    stop_name: str
    stop_sequence: int
    alert_method: str
    recipient: str
