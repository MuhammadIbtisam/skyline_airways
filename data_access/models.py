# I am handling ORM in one module
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.orm import relationship
from database.db_connection import Base
from datetime import datetime


class Airline(Base):
    __tablename__ = "Airlines"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, unique=True, nullable=False)
    country = Column(String, nullable=False)
    aircrafts = relationship("Aircraft", back_populates="airline")

class Aircraft(Base):
    __tablename__ = "Aircrafts"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    airline_id = Column(Integer, ForeignKey("Airlines.id"), nullable=False)
    model = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    airline = relationship("Airline", back_populates="aircrafts")
    flights = relationship("Flight", back_populates="aircraft")

class Crew(Base):
    __tablename__ = "Crews"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True)
    phone = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    flights = relationship("Flight", secondary="CrewFlights", back_populates="crews")
    user = relationship("User", back_populates="crew", uselist=False)

class Flight(Base):
    __tablename__ = "Flights"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    number = Column(String, unique=True, nullable=False)
    aircraft_id = Column(Integer, ForeignKey("Aircrafts.id"), nullable=False)
    status = Column(String, default='Scheduled')
    ticket_cost = Column(Numeric(10, 2), nullable=False)
    departure_from = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    departure_time = Column(String, nullable=False)
    arrival_time = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    aircraft = relationship("Aircraft", back_populates="flights")
    crews = relationship("Crew", secondary="CrewFlights", back_populates="flights")
    reservations = relationship("Reservation", back_populates="flight")
    tickets = relationship("Ticket", back_populates="flight")
    analytics = relationship("FlightAnalytic", back_populates="flight")

class CrewFlight(Base):
    __tablename__ = "CrewFlights"
    crew_id = Column(Integer, ForeignKey("Crews.id"), primary_key=True)
    flight_id = Column(Integer, ForeignKey("Flights.id"), primary_key=True)

class Passenger(Base):
    __tablename__ = "Passengers"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True)
    phone = Column(String, unique=True, nullable=False)
    passport_number = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    nationality = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    reservations = relationship("Reservation", back_populates="passenger")
    user = relationship("User", back_populates="passenger", uselist=False)

class Reservation(Base):
    __tablename__ = "Reservations"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    passenger_id = Column(Integer, ForeignKey("Passengers.id"), nullable=False)
    flight_id = Column(Integer, ForeignKey("Flights.id"), nullable=False)
    seat_no = Column(String, nullable=False)
    status = Column(String, default='Confirmed')
    booking_date = Column(String, nullable=False)
    passenger = relationship("Passenger", back_populates="reservations")
    flight = relationship("Flight", back_populates="reservations")
    tickets = relationship("Ticket", back_populates="reservation")
    payment = relationship("Payment", back_populates="reservation", uselist=False)
    customer_support_entry = relationship("CustomerSupport", back_populates="reservation", uselist=False) # One-to-one

class Ticket(Base):
    __tablename__ = "Tickets"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    reservation_id = Column(Integer, ForeignKey("Reservations.id"), nullable=False)
    flight_id = Column(Integer, ForeignKey("Flights.id"), nullable=False)
    ticket_number = Column(String, unique=True, nullable=False)
    _class = Column("class", String, nullable=False) # Use _class to avoid keyword conflict
    price = Column(Numeric(10, 2), nullable=False)
    status = Column(String, default='Valid')
    issued_at = Column(DateTime, default=datetime.utcnow)
    reservation = relationship("Reservation", back_populates="tickets")
    flight = relationship("Flight", back_populates="tickets")

class Payment(Base):
    __tablename__ = "Payments"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    reservation_id = Column(Integer, ForeignKey("Reservations.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(String, nullable=False)
    status = Column(String, default='Pending')
    reservation = relationship("Reservation", back_populates="payment")

class CustomerSupport(Base):
    __tablename__ = "CustomerSupport"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    reservation_id = Column(Integer, ForeignKey("Reservations.id"), nullable=False)
    issue = Column(String, nullable=False)
    resolution = Column(String, nullable=False)
    is_closed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reservation = relationship("Reservation", back_populates="customer_support_entry")

class FlightAnalytic(Base):
    __tablename__ = "FlightAnalytics"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    flight_id = Column(Integer, ForeignKey("Flights.id"), nullable=False)
    total_passengers = Column(Integer, nullable=False)
    revenue = Column(Numeric(10, 2), nullable=False)
    flight = relationship("Flight", back_populates="analytics")


# class User:
#     __tablename__ = 'Users'
#     id = Column(Integer, primary_key=True, autoincrement=True, index=True)
#     username = Column(String, unique=True, nullable=False)
#     hashed_password = Column(String, nullable=False)
#     role = Column(String, nullable=False)
#     crew_id = Column(Integer, ForeignKey("Crews.id"), unique=True)
#     passenger_id = Column(Integer, ForeignKey("Passengers.id"), unique=True)
#
#     crew = relationship("Crew", back_populates="user", uselist=False)
#     passenger = relationship("Passenger", back_populates="user", uselist=False)
#
#     __table_args__ = (
#         CheckConstraint("role IN ('Admin', 'Pilot', 'CoPilot', 'Flight Attendant', 'Customer Support', 'Passenger')",
#                         name="check_user_role"),
#     )


class User(Base):
    __tablename__ = 'users' # Correct tablename to lowercase as in your schema
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    crew_id = Column(Integer, ForeignKey("Crews.id"), unique=True, nullable=True) # Allow nullable
    passenger_id = Column(Integer, ForeignKey("Passengers.id"), unique=True, nullable=True) # Allow nullable

    crew = relationship("Crew", back_populates="user", uselist=False)
    passenger = relationship("Passenger", back_populates="user", uselist=False)

    __table_args__ = (
        CheckConstraint("role IN ('Admin', 'Pilot', 'CoPilot', 'Flight Attendant', 'Customer Support', 'Passenger')",
                        name="check_user_role"),
    )
