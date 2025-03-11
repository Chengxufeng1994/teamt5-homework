from app.application.usecase.bus_usecase import RegisterBusReminderModel
from app.schemas.bus_schema import BusReminderRequestSchema


class BusReminderFactory:
    @staticmethod
    def to_application_model(
        reminder_request: BusReminderRequestSchema,
    ) -> RegisterBusReminderModel:
        return RegisterBusReminderModel(**reminder_request.model_dump())
