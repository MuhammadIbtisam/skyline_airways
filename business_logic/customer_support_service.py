from data_access.flight_dao import FlightDAO
from data_access.customer_support_dao import CustomerSupportDAO
from sqlalchemy.orm import Session
from typing import List, Tuple, Optional

from data_access.models import CustomerSupport


class CustomerSupportService:
    def __init__(self):
        self.flight_dao = FlightDAO()
        self.customer_support_dao = CustomerSupportDAO()

    def get_flight_status_overview(self, db: Session):
        return self.flight_dao.get_flight_status_counts(db)

    def get_customer_support_issues(self, db: Session):
        try:
            issues = self.customer_support_dao.get_customer_support_issues(db)
            return issues, None
        except Exception as e:
            return None, f"Error fetching customer support issues: {e}"

    def get_support_issue_by_id(self, db: Session, issue_id: int):
        try:
            issue = self.customer_support_dao.get_customer_support_by_id(db, issue_id)
            return issue, None
        except Exception as e:
            return None, f"Error fetching support issue by ID: {e}"

    def update_support_issue(self, db: Session, issue_id: int, issue_data: dict):
        # return self.customer_support_dao.update_support_issue(db, issue_id, issue_data)
        try:
            success = self.customer_support_dao.update_support_issue(db, issue_id, issue_data)
            db.commit()
            return success, None
        except Exception as e:
            db.rollback()
            return False, f"Error updating support issue: {e}"
    #
    # def get_total_revenue_per_airline(self, db: Session):
    #     return self.flight_dao.get_total_revenue_per_airline(db)
    #
    # def get_passenger_traffic_by_route(self, db: Session):
    #     return self.flight_dao.get_passenger_traffic_by_route(db)
    #
    # def get_customer_support_issues_by_category(self, db: Session):
    #     return self.customer_support_dao.get_customer_support_issues_by_category(db)