from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.port.bus_api_client_port import BusAPIClient
from app.application.port.email_service_port import EmailService
from app.application.service.bus_service import BusService
from app.application.usecase.bus_usecase import BusUseCase
from app.config import Settings, get_settings
from app.domain.bus_reminder_repository import BusReminderRepository
from app.infrastructure.adapters.repositories.sqlalchemy.bus_reminder_repository import (
    SqlalchemyBusReminderRepository,
)
from app.infrastructure.adapters.smtp_email_service_adapter import SmtpEmailService
from app.infrastructure.adapters.tdx_bus_api_client import TDXBusAPIClient
from app.infrastructure.database import AsyncSessionLocal, get_db_session


def get_bus_reminder_repository(
    db: AsyncSession = Depends(get_db_session),
) -> BusReminderRepository:
    return SqlalchemyBusReminderRepository(db)


def get_bus_api_client_port(settings: Settings = Depends(get_settings)) -> BusAPIClient:
    return TDXBusAPIClient(
        app_id=settings.tdx_app_id, app_key=settings.tdx_app_key, auth_url=settings.tdx_auth_url
    )


def get_email_service(
    settings: Settings = Depends(get_settings),
) -> EmailService:
    return SmtpEmailService(
        host=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_username,
        password=settings.smtp_password,
    )


def get_bus_service(
    bus_reminder_repository: BusReminderRepository = Depends(get_bus_reminder_repository),
    bus_api_client: BusAPIClient = Depends(get_bus_api_client_port),
    email_service: EmailService = Depends(get_email_service),
) -> BusUseCase:
    return BusService(bus_reminder_repository, bus_api_client, email_service)


async def get_bus_service_manually() -> BusUseCase:
    settings = get_settings()
    db_session = AsyncSessionLocal()
    bus_reminder_repository = SqlalchemyBusReminderRepository(db_session)
    bus_api_client = TDXBusAPIClient(
        app_id=settings.tdx_app_id, app_key=settings.tdx_app_key, auth_url=settings.tdx_auth_url
    )
    email_service = SmtpEmailService(
        settings.smtp_host, settings.smtp_port, settings.smtp_username, settings.smtp_password
    )

    return BusService(bus_reminder_repository, bus_api_client, email_service)
