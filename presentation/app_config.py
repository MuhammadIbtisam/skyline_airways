# presentation/app_config.py
import tkinter as tk
from data_access.db_connect import create_session
from business_logic.flight_service import FlightService
# from business_logic.aircraft_service import AircraftService
# from business_logic.airline_service import AirlineService
# from business_logic.crew_service import CrewService
# from business_logic.customer_support_service import CustomerSupportService
# from business_logic.passenger_service import PassengerService
# from business_logic.payment_service import PaymentService
# from business_logic.reservation_service import ReservationService
# from business_logic.flight_analytic_service import FlightAnalyticService

class AppConfig:
    def __init__(self):
        # self.root = tk.Tk()
        # self.root.title("Airline Reservation System") # This title might not be the one you want for your main app
        self.db_session = create_session()

        # Initialize Business Logic Services
        self.flight_service = FlightService(self.db_session)
        # self.aircraft_service = AircraftService(self.db_session)
        # self.airline_service = AirlineService(self.db_session)
        # self.crew_service = CrewService(self.db_session)
        # self.customer_support_service = CustomerSupportService(self.db_session)
        # self.passenger_service = PassengerService(self.db_session)
        # self.payment_service = PaymentService(self.db_session)
        # self.reservation_service = ReservationService(self.db_session)
        # self.flight_analytic_service = FlightAnalyticService(self.db_session)

    def get_root(self) -> tk.Tk:
        return self.root

    def get_db_session(self):
        return self.db_session

    def get_flight_service(self):
        return self.flight_service

    # def get_aircraft_service(self):
    #     return self.aircraft_service
    #
    # def get_airline_service(self):
    #     return self.airline_service
    #
    # def get_crew_service(self):
    #     return self.crew_service
    #
    # def get_customer_support_service(self):
    #     return self.customer_support_service
    #
    # def get_passenger_service(self):
    #     return self.passenger_service
    #
    # def get_payment_service(self):
    #     return self.payment_service
    #
    # def get_reservation_service(self):
    #     return self.reservation_service
    #
    # def get_flight_analytic_service(self):
    #     return self.flight_analytic_service

    def run(self):
        self.root.mainloop()

# Remove this block to prevent automatic execution on import
# if __name__ == '__main__':
#     config = AppConfig()
#     config.run()