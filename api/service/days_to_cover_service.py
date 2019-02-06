import logging

class DaysToCoversService:

    def __init__(self, days_to_coverDao):
        self.logger = logging.getLogger(__name__)
        self.dao    = days_to_coverDao

    def find(self, start_date, end_date, security_id):
        return self.dao.find(start_date, end_date, security_id)
