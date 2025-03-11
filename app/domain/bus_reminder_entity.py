from dataclasses import dataclass


@dataclass
class BusReminder:
    id: int | None
    city: str
    route_id: str
    route_name: str
    direction: int
    stop_id: str
    stop_name: str
    stop_sequence: int
    alert_method: str
    recipient: str

    @staticmethod
    def create(
        city: str,
        route_id: str,
        route_name: str,
        direction: int,
        stop_id: str,
        stop_name: str,
        stop_sequence: int,
        alert_method: str,
        recipient: str,
    ) -> 'BusReminder':
        return BusReminder(
            id=None,
            city=city,
            route_id=route_id,
            route_name=route_name,
            direction=direction,
            stop_id=stop_id,
            stop_name=stop_name,
            stop_sequence=stop_sequence,
            alert_method=alert_method,
            recipient=recipient,
        )
