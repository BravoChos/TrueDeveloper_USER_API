from sqlalchemy                             import text
from .base_dao                              import BaseDao
from api.model.loan_outstanding_percentage  import LoanOutstandingPercentage

class LoanOutstandingPercentagesDao(BaseDao):

    def find(self, start_date, end_date, security_id):
        sql = text(f"""
            SELECT
            *
            FROM loan_utilization_percentages as l
            WHERE l.date BETWEEN :start_date AND :end_date
            AND l.security_id = :security_id
        """)

        params     = {
            'start_date'  : start_date,
            'end_date'    : end_date,
            'security_id' : security_id
        }
        rows                         = self.db.execute(sql, params).fetchall()
        loan_outstanding_percentages = [LoanOutstandingPercentage.from_row(row) for row in rows]
        return loan_outstanding_percentages
