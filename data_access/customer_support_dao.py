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

