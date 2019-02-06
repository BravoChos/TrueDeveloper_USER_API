import logging

class PremiumUserService:

    def __init__(self, premium_user_dao):
        self.logger = logging.getLogger(__name__)
        self.dao    = premium_user_dao

    def get_hashed_password(self, username):
        return self.dao.get_hashed_password(username)

    def get_token(self, username):
        return self.dao.get_token(username)

    def register(self, username, hashed_password, account_level_id, quota_id):
        return self.dao.register(username, hashed_password, account_level_id, quota_id)

    def logout(self):
        return self.dao.logout()

    def refresh(self):
        return self.dao.refresh()

    def get_access_level_and_quota(self, user_id, endpoint_id):
        return self.dao.get_access_level_and_quota(user_id, endpoint_id)

    def update_account_level_table(self, user_id):
        return self.dao.update_account_level_table(user_id)

    def update_join_table(self, user_id, endpoint_id, current_count, expired_at_quota):
        return self.dao.update_join_table(user_id, endpoint_id, current_count, expired_at_quota)
