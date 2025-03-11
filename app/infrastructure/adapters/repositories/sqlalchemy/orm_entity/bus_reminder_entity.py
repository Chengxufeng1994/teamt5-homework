from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class BusReminder(Base):
    __tablename__ = 'bus_reminder'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    city: Mapped[str] = mapped_column(String, nullable=False)
    route_id: Mapped[str] = mapped_column(String, nullable=False)
    route_name: Mapped[str] = mapped_column(String, nullable=False)
    direction: Mapped[int] = mapped_column(Integer, nullable=False)
    stop_id: Mapped[str] = mapped_column(String, nullable=False)
    stop_name: Mapped[str] = mapped_column(String, nullable=False)
    stop_sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    alert_method: Mapped[str] = mapped_column(String, nullable=False)
    recipient: Mapped[str] = mapped_column(String, nullable=False)
