from sqlalchemy         import text
from .base_dao          import BaseDao
from api.model.security import Security

class SecuritiesDao(BaseDao):

    def search(self, keyword):
        # If keyword is empty, then return an empty list
        if not keyword: return []

        sql  = text(f"""
            SELECT 
                s.id,
                s.name,
                s.english_name,
                s.ticker
            FROM securities as s
            WHERE (replace(s.name, ' ', '') LIKE :keyword or s.ticker LIKE :keyword)
            AND   s.active = 1
            ORDER BY s.id
        """)

        params     = { 'keyword' : keyword + "%", }
        rows       = self.db.execute(sql, params).fetchall()
        securities = [Security.from_row(row) for row  in rows]

        return securities