from fastapi import APIRouter, Depends, HTTPException, status

from app.application.service.bus_factory import BusReminderFactory
from app.application.usecase.bus_usecase import BusUseCase
from app.dependencies import get_bus_service
from app.schemas.bus_schema import (
    BusReminderRequestSchema,
    BusRouteInfoResponse,
    BusStopSchema,
    DirectionSchema,
)
from app.schemas.common_schema import OkResponse

router = APIRouter(
    prefix='/bus',
    tags=['bus'],
)


async def bus_route_info_parameters(city: str = 'Taipei', route_name: str = '672') -> dict:
    return {'city': city, 'route_name': route_name}


def create_direction_schema(
    direction: int, direction_name: str, bus_route_info: dict
) -> DirectionSchema:
    stops = [BusStopSchema(**bus_stop.__dict__) for bus_stop in bus_route_info.get(direction, [])]
    return DirectionSchema(direction=direction, direction_name=direction_name, stops=stops)


@router.get('/routeinfo', response_model=BusRouteInfoResponse)
async def get_bus_route_info(
    bus_route_info_parameters: dict = Depends(bus_route_info_parameters),
    bus_service: BusUseCase = Depends(get_bus_service),
) -> BusRouteInfoResponse:
    city = bus_route_info_parameters['city']
    route_name = bus_route_info_parameters['route_name']
    if not city or not route_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='City and route name are required'
        )

    bus_route_info = await bus_service.get_bus_route_info(city, route_name)
    if not bus_route_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Bus route info not found'
        )

    return BusRouteInfoResponse(
        route_name=route_name,
        city=city,
        outbound=create_direction_schema(0, 'outbound', bus_route_info),
        inbound=create_direction_schema(1, 'inbound', bus_route_info),
    )


@router.post('/reminders', response_model=OkResponse)
async def register_bus_reminder(
    reminder_request: BusReminderRequestSchema,
    bus_service: BusUseCase = Depends(get_bus_service),
) -> OkResponse:
    bus_reminder_model = BusReminderFactory.to_application_model(reminder_request)
    await bus_service.register_bus_reminder(bus_reminder_model)
    return OkResponse()
