from sqlalchemy.orm import Session
from data_access.models import CustomerSupport
from sqlalchemy import select, func
class CustomerSupportDAO:
    def get_customer_support_issues_by_category(self, db: Session):
        try:
            query = select(
                CustomerSupport.issue,
                func.count(CustomerSupport.id).label('count')
            ).group_by(CustomerSupport.issue)
            result = db.execute(query).fetchall()
            return [{"issue": row[0], "count": row.count} for row in result]
        except Exception as e:
            print(f"Error fetching customer support issues by category: {e}")
            return []

    def get_customer_support_issues(self, db: Session):
        return db.query(CustomerSupport).all()

    def get_customer_support_by_id(self, db: Session, issue_id):
        return db.query(CustomerSupport).filter(CustomerSupport.id == issue_id).first()

    def update_support_issue(self, db: Session, issue_id: int, issue_data: dict):
        db_issue = db.query(CustomerSupport).filter(CustomerSupport.id == issue_id).first()
        if db_issue:
            for key, value in issue_data.items():
                if hasattr(db_issue, key):
                    setattr(db_issue, key, value)
            db.commit()
            db.refresh(db_issue)
            return True
        return False
