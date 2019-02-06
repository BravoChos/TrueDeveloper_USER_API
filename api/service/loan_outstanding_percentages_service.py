import logging

class LoanOutstandingPercentagesService:

    def __init__(self, loan_outstanding_percentages_dao):
        self.logger = logging.getLogger(__name__)
        self.dao    = loan_outstanding_percentages_dao

    def find(self, start_date, end_date, security_id):
        return self.dao.find(start_date, end_date, security_id)