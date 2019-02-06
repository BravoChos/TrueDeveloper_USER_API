import logging

class SecuritiesService:

    def __init__(self, securities_dao):
        self.logger = logging.getLogger(__name__)
        self.dao    = securities_dao

    def search(self, keyword):
        return self.dao.search(keyword)
