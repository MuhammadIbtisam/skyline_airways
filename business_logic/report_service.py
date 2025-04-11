from data_access.flight_dao import FlightDAO
from data_access.customer_support_dao import CustomerSupportDAO
from sqlalchemy.orm import Session

class ReportService:
    def __init__(self):
        self.flight_dao = FlightDAO()
        self.customer_support_dao = CustomerSupportDAO()

    def get_flight_status_overview(self, db: Session):
        return self.flight_dao.get_flight_status_counts(db)

    def get_total_revenue_per_airline(self, db: Session):
        return self.flight_dao.get_total_revenue_per_airline(db)

    def get_passenger_traffic_by_route(self, db: Session):
        return self.flight_dao.get_passenger_traffic_by_route(db)

    def get_customer_support_issues_by_category(self, db: Session):
        return self.customer_support_dao.get_customer_support_issues_by_category(db)