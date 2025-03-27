import enum
from datetime import datetime
from decimal import Decimal
from xmlrpc.client import Boolean

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from database import Base

class Airline(Base):
    __tablename__ = "airlines"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False,  unique=True, index=True)
    country = Column(String, nullable=False, index=True)

class Aircraft(Base):
    __tablename__ = "aircrafts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    airline_id = Column(Integer, ForeignKey("airlines.id"), nullable=False)
    model = Column(String, nullable=False, index=True)
    capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

class CrewRoleEnum(enum.Enum):
    Admin = 'Admin'
    Pilot = 'Pilot'
    CoPilot = 'CoPilot'
    FlightAttendant = 'Flight Attendant'
    CustomerSupport = 'Customer Support'

class Crew(Base):
    __tablename__ = "crews"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True)
    phone = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False, enum=CrewRoleEnum, index=True)

class FlightStatusEnum(enum.Enum):
    Scheduled = 'Scheduled'
    Cancelled = 'Cancelled'
    Delayed = 'Delayed'
    Completed = 'Completed'

class Flight(Base):
    __tablename__ = "flights"
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String, nullable=False, unique=True, index=True)
    aircraft_id = Column(Integer, ForeignKey("aircrafts.id"), nullable=False)
    status = Column(String, default= FlightStatusEnum.Scheduled, enum=FlightStatusEnum, index=True)
    ticket_cost = Column(Decimal(10, 2), nullable=False)
    departure_from = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

class CrewFlight(Base):
    __tablename__ = "crew_flights"
    crew_id = Column(Integer, ForeignKey("crews.id"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)

class Passenger(Base):
    __tablename__ = "passengers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    email = Column(String, unique=True)
    phone = Column(String, nullable=False, unique=True)
    passport_number = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    nationality = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

class ReservationStatusEnum(enum.Enum):
    Confirmed = 'Confirmed'
    Cancelled = 'Cancelled'
    CheckedIn = 'Checked In'

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    passenger_id = Column(Integer, ForeignKey("passengers.id"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    seat_no = Column(String, nullable=False)
    status = Column(String, default= ReservationStatusEnum.Confirmed, enum=ReservationStatusEnum, index=True)
    booking_date = Column(DateTime, nullable=False)

class PaymentStatusEnum(enum.Enum):
    Pending = 'Pending'
    Confirmed = 'Confirmed'
    Rejected = 'Rejected'

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=False)
    amount = Column(Decimal(10, 2), nullable=False)
    payment_date = Column(DateTime, nullable=False, default=datetime.now)
    payment_method = Column(String, nullable=False)
    status = Column(String, default= PaymentStatusEnum.Pending, enum=PaymentStatusEnum, index=True)

class CustomerSupport(Base):
    __tablename__ = "customer_support"
    id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=False)
    issue = Column(String, nullable=False)
    resolution = Column(String, nullable=False)
    is_closed = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now)

class FlightAnalytic(Base):
    __tablename__ = "flight_analytics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    total_passengers = Column(Integer, nullable=False)
    revenue = Column(Decimal(10, 2), nullable=False)