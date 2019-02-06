from sqlalchemy                             import text
from .base_dao                              import BaseDao
from api.model.short_volume_percentage      import ShortVolumePercentage

class ShortVolumePercentagesDao(BaseDao):

    def find(self, start_date, end_date, security_id):
        sql = text(f"""
            SELECT
            *
            FROM short_volume_percentages as s
            WHERE s.date BETWEEN :start_date AND :end_date
            AND s.security_id = :security_id
        """)

        params     = {
            'start_date'  : start_date,
            'end_date'    : end_date,
            'security_id' : security_id
        }
        rows                            = self.db.execute(sql, params).fetchall()
        short_volume_percentages        = [ShortVolumePercentage.from_row(row) for row in rows]
        return short_volume_percentages
