insert into Users (username, hashed_password, role, crew_id, passenger_id)
VALUES
    ('admin', '$2b$12$So9uvP3xeYjB9x/85tYHwe6krnfvdYbwu8p46kk0hBZDeeWoHWphG', 'Admin', NULL, NULL), -- Password: password
    ('pilot1', '$2b$12$So9uvP3xeYjB9x/85tYHwe6krnfvdYbwu8p46kk0hBZDeeWoHWphG', 'Pilot', 1, NULL),     -- Password: password (Crew ID 1: Michael Smith)
    ('copilot1', '$2b$12$So9uvP3xeYjB9x/85tYHwe6krnfvdYbwu8p46kk0hBZDeeWoHWphG', 'CoPilot', 2, NULL),  -- Password: password (Crew ID 2: Sarah Johnson)
    ('attendant1', '$2b$12$So9uvP3xeYjB9x/85tYHwe6krnfvdYbwu8p46kk0hBZDeeWoHWphG', 'Flight Attendant', 3, NULL), -- Password: password (Crew ID 3: David Brown)
    ('support1', '$2b$12$So9uvP3xeYjB9x/85tYHwe6krnfvdYbwu8p46kk0hBZDeeWoHWphG', 'Customer Support', 5, NULL), -- Password: password (Crew ID 5: Chris Davis)
    ('passenger1', '$2b$12$So9uvP3xeYjB9x/85tYHwe6krnfvdYbwu8p46kk0hBZDeeWoHWphG', 'Passenger', NULL, 1), -- Password: password (Passenger ID 1: Alice Johnson)
    ('passenger2', '$2b$12$So9uvP3xeYjB9x/85tYHwe6krnfvdYbwu8p46kk0hBZDeeWoHWphG', 'Passenger', NULL, 2); -- Password: password (Passenger ID 2: Bob Smith)

insert into Airlines (name, country)
values ('American Airlines', 'USA'),
       ('British Airways', 'UK'),
       ('Emirates', 'UAE'),
       ('Qatar Airways', 'Qatar'),
       ('Singapore Airlines', 'Singapore'),
       ('Lufthansa', 'Germany'),
       ('Air France', 'France'),
       ('Turkish Airlines', 'Turkey'),
       ('Cathay Pacific', 'Hong Kong'),
       ('Japan Airlines', 'Japan'),
       ('Etihad Airways', 'UAE'),
       ('Korean Air', 'South Korea'),
       ('Air Canada', 'Canada'),
       ('Thai Airways', 'Thailand'),
       ('Qantas Airways', 'Australia');

insert into Aircrafts (airline_id, model, capacity)
values (1, 'Boeing 737', 180),
       (2, 'Airbus A320', 160),
        (3, 'Boeing 737', 180),
       (3, 'Boeing 777', 396),
       (4, 'Airbus A380', 850),
       (5, 'Boeing 787 Dreamliner', 296),
       (6, 'Airbus A350', 440),
       (7, 'Boeing 767', 375),
       (8, 'Embraer E190', 114),
       (9, 'Bombardier CRJ900', 90),
       (10, 'ATR 72', 78),
       (11, 'Boeing 747', 660),
       (12, 'Boeing 757', 228),
       (13, 'Airbus A321', 185),
       (13, 'Boeing 767', 375),
       (14, 'Airbus A330', 277),
       (15, 'Boeing 767', 375),
       (15, 'Boeing 737 MAX', 200);

insert into Tickets (reservation_id, flight_id, ticket_number, class, price, status, issued_at)
values (1, 1, 'AA101-2025-0001', 'Economy', 250.00, 'Valid', '2025-03-25 10:00:00'),
       (2, 1, 'AA101-2025-0002', 'Business', 250.00, 'Valid', '2025-03-26 11:00:00'),
       (3, 2, 'BA202-2025-0003', 'Economy', 150.00, 'Cancelled', '2025-03-20 09:00:00'),
       (4, 2, 'BA202-2025-0004', 'Economy', 150.00, 'Valid', '2025-03-21 10:00:00'),
       (5, 3, 'EK303-2025-0005', 'Business', 1200.00, 'Valid', '2025-03-22 12:00:00'),
       (6, 3, 'EK303-2025-0006', 'First Class', 1200.00, 'Valid', '2025-03-22 12:30:00'),
       (7, 4, 'QR404-2025-0007', 'Economy', 1800.00, 'Cancelled', '2025-03-18 08:00:00'),
       (8, 4, 'QR404-2025-0008', 'Business', 1800.00, 'Valid', '2025-03-19 09:00:00'),
       (9, 5, 'SQ505-2025-0009', 'Economy', 900.00, 'Valid', '2025-03-23 13:00:00'),
       (10, 5, 'SQ505-2025-0010', 'Economy', 900.00, 'Valid', '2025-03-24 14:00:00'),
       (11, 6, 'LH606-2025-0011', 'Economy', 1100.00, 'Cancelled', '2025-03-17 10:00:00'),
       (12, 6, 'LH606-2025-0012', 'Business', 1100.00, 'Valid', '2025-03-18 11:00:00'),
       (13, 7, 'AF707-2025-0013', 'First Class', 950.00, 'Valid', '2025-03-20 12:00:00'),
       (14, 7, 'AF707-2025-0014', 'Business', 950.00, 'Valid', '2025-03-21 13:00:00'),
       (15, 8, 'TK808-2025-0015', 'Economy', 1300.00, 'Cancelled', '2025-03-22 09:00:00'),
       (16, 8, 'TK808-2025-0016', 'Business', 1300.00, 'Valid', '2025-03-23 10:00:00'),
       (17, 9, 'CX909-2025-0017', 'First Class', 1400.00, 'Valid', '2025-03-24 11:00:00'),
       (18, 9, 'CX909-2025-0018', 'Economy', 1400.00, 'Valid', '2025-03-25 12:00:00'),
       (19, 10, 'JL101-2025-0019', 'Economy', 600.00, 'Cancelled', '2025-03-26 08:00:00'),
       (20, 10, 'JL101-2025-0020', 'Business', 600.00, 'Valid', '2025-03-27 09:00:00');

insert into Crews (first_name, last_name, email, phone, role)
values ('Michael', 'Smith', 'michael.smith@example.com', '1112223333', 'Pilot'),
       ('Sarah', 'Johnson', 'sarah.johnson@example.com', '2223334444', 'CoPilot'),
       ('David', 'Brown', 'david.brown@example.com', '3334445555', 'Flight Attendant'),
       ('Emma', 'Williams', 'emma.williams@example.com', '4445556666', 'Flight Attendant'),
       ('Chris', 'Davis', 'chris.davis@example.com', '5556667777', 'Customer Support'),
       ('Olivia', 'Taylor', 'olivia.taylor@example.com', '6667778888', 'Pilot'),
       ('James', 'Miller', 'james.miller@example.com', '7778889999', 'CoPilot'),
       ('Ethan', 'Anderson', 'ethan.anderson@example.com', '8889990000', 'Flight Attendant'),
       ('Sophia', 'White', 'sophia.white@example.com', '9990001111', 'Flight Attendant'),
       ('Liam', 'Martin', 'liam.martin@example.com', '0001112222', 'Customer Support'),
       ('Henry', 'Clark', 'henry.clark@example.com', '1112223334', 'Admin'),
       ('Isabella', 'Moore', 'isabella.moore@example.com', '2223334445', 'Pilot'),
       ('Lucas', 'Walker', 'lucas.walker@example.com', '3334445556', 'CoPilot'),
       ('Charlotte', 'Young', 'charlotte.young@example.com', '4445556667', 'Flight Attendant'),
       ('Benjamin', 'Hall', 'benjamin.hall@example.com', '5556667778', 'Customer Support');

insert into Flights (number, aircraft_id, departure_from, destination, ticket_cost, departure_time, arrival_time)
values ('AA101', 1, 'New York', 'Los Angeles', 250.00, '2025-04-10 07:00:00', '2025-04-10 10:30:00'),
       ('BA202', 2, 'London', 'Paris', 150.00, '2025-04-12 09:15:00', '2025-04-12 10:45:00'),
       ('EK303', 3, 'Dubai', 'Sydney', 1200.00, '2025-04-15 21:30:00', '2025-04-16 06:15:00'),
       ('QR404', 4, 'Doha', 'New York', 1800.00, '2025-04-18 02:00:00', '2025-04-18 14:30:00'),
       ('SQ505', 5, 'Singapore', 'Tokyo', 900.00, '2025-04-20 11:45:00', '2025-04-20 18:10:00'),
       ('LH606', 6, 'Frankfurt', 'Bangkok', 1100.00, '2025-04-22 13:20:00', '2025-04-23 06:00:00'),
       ('AF707', 7, 'Paris', 'Dubai', 950.00, '2025-04-24 22:00:00', '2025-04-25 06:30:00'),
       ('TK808', 8, 'Istanbul', 'New York', 1300.00, '2025-04-26 16:15:00', '2025-04-26 23:50:00'),
       ('CX909', 9, 'Hong Kong', 'San Francisco', 1400.00, '2025-04-28 01:00:00', '2025-04-28 10:30:00'),
       ('JL101', 10, 'Tokyo', 'Seoul', 600.00, '2025-04-30 12:30:00', '2025-04-30 14:50:00');

insert into CrewFlights (crew_id, flight_id)
values (1, 1),
       (2, 1),
       (3, 1),
       (4, 1),
       (5, 1),
       (6, 2),
       (7, 2),
       (8, 2),
       (9, 2),
       (10, 2),
       (11, 3),
       (12, 3),
       (13, 3),
       (14, 3),
       (15, 3),
       (1, 4),
       (2, 4),
       (3, 4),
       (4, 4),
       (6, 5),
       (7, 5),
       (8, 5),
       (9, 5),
       (12, 6),
       (13, 6),
       (14, 6),
       (1, 7),
       (3, 7),
       (4, 7),
       (6, 8),
       (7, 8),
       (8, 8),
       (12, 9),
       (13, 9),
       (14, 9),
       (1, 10),
       (2, 10),
       (3, 10),
       (4, 10);

insert into Passengers (first_name, last_name, email, phone, passport_number, dob, nationality)
values ('Alice', 'Johnson', 'alice.johnson@example.com', '1234567890', 'P12345678', '1990-05-15', 'USA'),
       ('Bob', 'Smith', 'bob.smith@example.com', '2345678901', 'P23456789', '1985-08-22', 'Canada'),
       ('Charlie', 'Brown', 'charlie.brown@example.com', '3456789012', 'P34567890', '1992-02-10', 'UK'),
       ('David', 'Williams', 'david.williams@example.com', '4567890123', 'P45678901', '1988-11-30', 'Australia'),
       ('Emma', 'Davis', 'emma.davis@example.com', '5678901234', 'P56789012', '1995-09-25', 'Germany'),
       ('Frank', 'Miller', 'frank.miller@example.com', '6789012345', 'P67890123', '1983-07-17', 'France'),
       ('Grace', 'Taylor', 'grace.taylor@example.com', '7890123456', 'P78901234', '1997-03-05', 'Spain'),
       ('Henry', 'Anderson', 'henry.anderson@example.com', '8901234567', 'P89012345', '1991-12-12', 'Italy'),
       ('Ivy', 'White', 'ivy.white@example.com', '9012345678', 'P90123456', '1986-06-28', 'Netherlands'),
       ('Jack', 'Martin', 'jack.martin@example.com', '0123456789', 'P01234567', '1999-04-14', 'Sweden'),
       ('Katherine', 'Moore', 'katherine.moore@example.com', '1112223333', 'P11122333', '1984-10-08', 'Switzerland'),
       ('Liam', 'Walker', 'liam.walker@example.com', '2223334444', 'P22233444', '1993-01-19', 'Norway'),
       ('Mia', 'Young', 'mia.young@example.com', '3334445555', 'P33344555', '1996-07-21', 'Denmark'),
       ('Noah', 'Hall', 'noah.hall@example.com', '4445556666', 'P44455666', '1989-05-09', 'Brazil'),
       ('Olivia', 'Clark', 'olivia.clark@example.com', '5556667777', 'P55566777', '2000-02-27', 'Argentina'),
       ('Peter', 'Lewis', 'peter.lewis@example.com', '6667778888', 'P66677888', '1994-11-11', 'Mexico'),
       ('Quinn', 'Harris', 'quinn.harris@example.com', '7778889999', 'P77788999', '1982-03-16', 'Japan'),
       ('Rachel', 'King', 'rachel.king@example.com', '8889990000', 'P88899000', '1987-09-03', 'China'),
       ('Samuel', 'Scott', 'samuel.scott@example.com', '9990001111', 'P99900111', '1998-12-29', 'India'),
       ('Tina', 'Nelson', 'tina.nelson@example.com', '0001112222', 'P00011222', '1990-06-07', 'South Korea');

insert into Reservations (passenger_id, flight_id, seat_no, status, booking_date)
values (1, 1, '12A', 'Confirmed', '2025-03-25'),
       (2, 1, '14C', 'Confirmed', '2025-03-26'),
       (3, 2, '5B', 'Cancelled', '2025-03-20'),
       (4, 2, '7D', 'Confirmed', '2025-03-21'),
       (5, 3, '9E', 'Checked In', '2025-03-22'),
       (6, 3, '3F', 'Confirmed', '2025-03-22'),
       (7, 4, '2A', 'Cancelled', '2025-03-18'),
       (8, 4, '15B', 'Confirmed', '2025-03-19'),
       (9, 5, '8C', 'Checked In', '2025-03-23'),
       (10, 5, '16D', 'Confirmed', '2025-03-24'),
       (11, 6, '10E', 'Cancelled', '2025-03-17'),
       (12, 6, '4F', 'Confirmed', '2025-03-18'),
       (13, 7, '6A', 'Checked In', '2025-03-20'),
       (14, 7, '18B', 'Confirmed', '2025-03-21'),
       (15, 8, '11C', 'Cancelled', '2025-03-22'),
       (16, 8, '20D', 'Confirmed', '2025-03-23'),
       (17, 9, '13E', 'Checked In', '2025-03-24'),
       (18, 9, '21F', 'Confirmed', '2025-03-25'),
       (19, 10, '22A', 'Cancelled', '2025-03-26'),
       (20, 10, '23B', 'Confirmed', '2025-03-27');

insert into Payments (reservation_id, amount,payment_date, payment_method, status)
values (1, 200.00, '2025-03-25', 'Credit Card', 'Confirmed'),
       (2, 200.00, '2025-03-26', 'Debit Card', 'Confirmed'),
       (3, 180.00, '2025-03-20', 'PayPal', 'Rejected'),
       (4, 180.00, '2025-03-21', 'Credit Card', 'Confirmed'),
       (5, 220.00, '2025-03-22', 'Bank Transfer', 'Confirmed'),
       (6, 220.00, '2025-03-22', 'Credit Card', 'Confirmed'),
       (7, 175.00, '2025-03-18', 'Cash', 'Rejected'),
       (8, 175.00, '2025-03-19', 'Credit Card', 'Confirmed'),
       (9, 250.00, '2025-03-23', 'Debit Card', 'Confirmed'),
       (10, 250.00, '2025-03-24', 'Credit Card', 'Confirmed'),
       (11, 190.00, '2025-03-17', 'Bank Transfer', 'Rejected'),
       (12, 190.00, '2025-03-18', 'Credit Card', 'Confirmed'),
       (13, 210.00, '2025-03-20', 'PayPal', 'Confirmed'),
       (14, 210.00, '2025-03-21', 'Credit Card', 'Confirmed'),
       (15, 230.00, '2025-03-22', 'Debit Card', 'Rejected'),
       (16, 230.00, '2025-03-23', 'Credit Card', 'Confirmed'),
       (17, 240.00, '2025-03-24', 'Cash', 'Confirmed'),
       (18, 240.00, '2025-03-25', 'Credit Card', 'Confirmed'),
       (19, 260.00, '2025-03-26', 'Bank Transfer', 'Rejected'),
       (20, 260.00, '2025-03-27', 'Credit Card', 'Confirmed');

insert into CustomerSupport (reservation_id, issue, resolution, is_closed)
values (3, 'Flight cancellation request', 'Refund processed', 1),
       (5, 'Seat change request', 'Upgraded to business class', 1),
       (2, 'Lost baggage', 'Filed a claim, tracking in progress', 0);
