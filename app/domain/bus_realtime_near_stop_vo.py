from dataclasses import dataclass
from datetime import datetime


@dataclass
class BusRealTimeNearStop:
    plate_numb: str
    operator_id: str
    operator_no: str
    route_uid: str
    route_id: str
    route_name: str
    sub_route_uid: str
    sub_route_id: str
    sub_route_name: str
    direction: str
    stop_uid: str
    stop_id: str
    stop_name: str
    stop_sequence: int
    duty_status: int
    bus_status: int
    a2_event_type: int
    gps_time: datetime
    trip_start_time_type: int
    trip_start_time: datetime
    src_update_time: datetime
    update_time: datetime

    @staticmethod
    def create(
        plate_numb: str,
        operator_id: str,
        operator_no: str,
        route_uid: str,
        route_id: str,
        route_name: str,
        sub_route_uid: str,
        sub_route_id: str,
        sub_route_name: str,
        direction: str,
        stop_uid: str,
        stop_id: str,
        stop_name: str,
        stop_sequence: int,
        duty_status: int,
        bus_status: int,
        a2_event_type: int,
        gps_time: datetime,
        trip_start_time_type: int,
        trip_start_time: datetime,
        src_update_time: datetime,
        update_time: datetime,
    ) -> 'BusRealTimeNearStop':
        return BusRealTimeNearStop(
            plate_numb=plate_numb,
            operator_id=operator_id,
            operator_no=operator_no,
            route_uid=route_uid,
            route_id=route_id,
            route_name=route_name,
            sub_route_uid=sub_route_uid,
            sub_route_id=sub_route_id,
            sub_route_name=sub_route_name,
            direction=direction,
            stop_uid=stop_uid,
            stop_id=stop_id,
            stop_name=stop_name,
            stop_sequence=stop_sequence,
            duty_status=duty_status,
            bus_status=bus_status,
            a2_event_type=a2_event_type,
            gps_time=gps_time,
            trip_start_time_type=trip_start_time_type,
            trip_start_time=trip_start_time,
            src_update_time=src_update_time,
            update_time=update_time,
        )
