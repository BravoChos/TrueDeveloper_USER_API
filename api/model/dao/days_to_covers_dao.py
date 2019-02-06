from sqlalchemy                             import text
from .base_dao                              import BaseDao
from api.model.days_to_cover                import DaysToCover

class DaysToCoversDao(BaseDao):

    def find(self, start_date, end_date, security_id):
        sql = text(f"""
            SELECT
            *
            FROM days_to_covers as d
            WHERE d.date BETWEEN :start_date AND :end_date
            AND d.security_id = :security_id
        """)

        params     = {
            'start_date'  : start_date,
            'end_date'    : end_date,
            'security_id' : security_id
        }
        rows       = self.db.execute(sql, params).fetchall()
        days_to_covers = [DaysToCover.from_row(row) for row in rows]
        return days_to_covers
