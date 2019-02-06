import logging

class ShortVolumePercentagesService:

    def __init__(self, short_volume_percentages_dao):
        self.logger = logging.getLogger(__name__)
        self.dao    = short_volume_percentages_dao

    def find(self, start_date, end_date, security_id):
        return self.dao.find(start_date, end_date, security_id)