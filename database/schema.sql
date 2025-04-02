create table if not exists Airlines (
    id integer primary key Autoincrement,
    name text unique not null,
    country text not null
);

create index if not exists name_airlines on Airlines (name)
create index if not exists country_airlines on Airlines (country)

create table if not exists Aircrafts (
    id integer primary key autoincrement,
    airline_id integer not null,
    model text not null,
    capacity integer not null,
    created_at text not null default current_timestamp,
    foreign key (airline_id) references Airlines(id)
);

create index if not exists model_aircrafts on Aircrafts (model);

create table if not exists Crews (
    id integer primary key autoincrement,
    first_name text not null,
    last_name text not null,
    email text unique,
    phone text not null unique,
    role text not null check(role in ('Admin', 'Pilot', 'CoPilot', 'Flight Attendant', 'Customer Support'))
);

create index if not exists role_crews on Crews (role);

create table if not exists Flights (
    id integer primary key autoincrement,
    number text not null unique,
    aircraft_id integer not null,
    status text default 'Scheduled' check(status in ('Scheduled', 'Cancelled', 'Delayed', 'Completed')),
    ticket_cost decimal(10,2) not null,
    departure_from text not null,
    destination text not null,
    departure_time text not null,
    arrival_time text not null,
    created_at text not null default current_timestamp,
    updated_at text not null default current_timestamp,
    foreign key (aircraft_id) references Aircrafts(id)
);

create index if not exists number_flights on Flights (number);
create index if not exists status_flights on Flights (status);

create table if not exists CrewFlights (
    crew_id integer not null,
    flight_id integer not null,
    primary key (crew_id, flight_id),
    foreign key (crew_id) references Crews(id),
    foreign key (flight_id) references Flights(id)
);

create table if not exists Passengers (
    id integer primary key autoincrement,
    first_name text not null,
    last_name text not null,
    email text unique,
    phone text not null unique,
    passport_number text not null,
    dob text not null,
    nationality text not null,
    created_at text not null default current_timestamp
);

create index if not exists first_name_passengers on Passengers (first_name);
create index if not exists last_name_passengers on Passengers (last_name);
create index if not exists nationality_passengers on Passengers (nationality);

create table if not exists Reservations (
    id integer primary key autoincrement,
    passenger_id integer not null,
    flight_id integer not null,
    seat_no text not null,
    status text default 'Confirmed' check(status in ('Confirmed', 'Cancelled', 'Checked In')),
    booking_date text not null,
    foreign key (passenger_id) references Passengers(id),
    foreign key (flight_id) references Flights(id)
);

create index if not exists status_reservations on Reservations (status);

create table if not exists Payments (
    id integer primary key autoincrement,
    reservation_id integer not null,
    amount decimal(10,2) not null,
    payment_date text not null default current_timestamp,
    payment_method text not null,
    status text default 'Pending' check(status in ('Pending', 'Confirmed', 'Rejected')),
    foreign key (reservation_id) references Reservations(id)
);

create index if not exists status_payments on Payments (status);

create table if not exists CustomerSupport (
    id integer primary key autoincrement,
    reservation_id integer not null,
    issue text not null,
    resolution text not null,
    is_closed boolean default 0,
    created_at text not null default current_timestamp,
    updated_at text not null default current_timestamp,
    foreign key (reservation_id) references Reservations(id)
);

create table if not exists FlightAnalytics (
    id integer primary key autoincrement,
    flight_id integer not null,
    total_passengers integer not null,
    revenue decimal(10,2) not null,
    foreign key (flight_id) references Flights(id)
);