from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import func, TIMESTAMP, ForeignKey

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[Optional[str]]
    password_hash: Mapped[Optional[str]]
    created_on: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        server_default=func.now()
    )
    
class Driver(Base):
    __tablename__ = "drivers"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str]
    aadhaar_no: Mapped[str]
    car_no_plate: Mapped[str]
    
class DriverProfile(Base):
    __tablename__ = "driver_profiles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id", ondelete="CASCADE"))
    first_name: Mapped[str]
    last_name: Mapped[str]
    pan_card_no: Mapped[str]
    drivers_license: Mapped[str]
    home_address: Mapped[str]
    last_booking: Mapped[str] = mapped_column(ForeignKey("bookings.id", ondelete="CASCADE"))
    aadhaar_no: Mapped[str]
    car_no_plate: Mapped[str]
    
class Passenger(Base):
    __tablename__ = "passengers"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str]
    aadhaar_no: Mapped[str]
    
class PassengerProfile(Base):
    __tablename__ = "passenger_profiles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    passenger_id: Mapped[int] = mapped_column(ForeignKey("passengers.id", ondelete="CASCADE"))
    first_name: Mapped[str]
    last_name: Mapped[str]
    last_visited: Mapped[str]
    last_booking: Mapped[str]
    updated_on:  Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        server_default=func.now()
    )

    
class Booking(Base):
    __tablename__ = "bookings"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey("drivers.id", ondelete="CASCADE"))
    passenger_id: Mapped[int] = mapped_column(ForeignKey("passengers.id", ondelete="CASCADE"))
    pickup_point: Mapped[str]
    destination: Mapped[str]
    booking_progress: Mapped[str]
    last_updated: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=False),
        server_default=func.now()
    )
