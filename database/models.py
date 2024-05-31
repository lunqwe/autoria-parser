from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.config import Base


class Card(Base):
    __tablename__ = 'cards'
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(nullable=True)
    title: Mapped[str] = mapped_column(nullable=True)
    price_usd: Mapped[int] = mapped_column(nullable=True)
    odometer: Mapped[int] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    phone_number: Mapped[int] = mapped_column(nullable=True)
    image_url: Mapped[str] = mapped_column(nullable=True)
    images_count: Mapped[int] = mapped_column(nullable=True)
    car_number: Mapped[str] = mapped_column(nullable=True)
    car_vin: Mapped[str] = mapped_column(nullable=True)
    datetime_found: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    

        
        