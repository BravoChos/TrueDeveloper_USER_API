import logging

class BaseDao:
    def __init__(self, db):
        self.db     = db
        self.logger = logging.getLogger(__name__)
