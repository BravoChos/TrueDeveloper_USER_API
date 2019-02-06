from sqlalchemy                             import text
from .base_dao                              import BaseDao
from api.model.premium_user                 import PremiumUser
from api.blacklist import BLACKLIST
#################################################################
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_raw_jwt
)
import time, datetime
###############################################################

class PremiumUserDao(BaseDao):
    def get_hashed_password(self, username):
        sql = text(f"""
            SELECT
            hashed_password
            FROM premium_user as p
            WHERE p.username = :username
        """)

        params = {
            'username': username
        }
        hashed_password      = self.db.execute(sql, params).fetchone() #or fetchall()
        return hashed_password

    def get_token(self, username):
        sql = text(f"""
            SELECT
            *
            FROM premium_user as p
            WHERE p.username = :username
        """)
        params = {
            'username': username
        }
        premium_user      = self.db.execute(sql, params).fetchone() #or fetchall()
        access_token = create_access_token(identity=premium_user[0], fresh=True)
        refresh_token = create_refresh_token(premium_user[0])
        username = premium_user[1]
        return {
                   'access_token': access_token,
                   'refresh_token': refresh_token,
                   'username':  username
               }, 200

    def register(self, username, hashed_password, account_level_id, quota_id):
        # check wheather username is valid
        sql = text(f"""
            SELECT
            *
            FROM premium_user as p
            WHERE p.username = :username
        """)
        params = {
            'username': username
        }
        premium_user      = self.db.execute(sql, params).fetchone()
        if premium_user:
            return {"message": "A user with that username already exists"}, 400
        # insert user information into premium_user table
        sql2 = text(f"""
            INSERT INTO premium_user ( username, hashed_password, account_level_id )
            VALUES(:username, :hashed_password, :account_level_id)""")
        params2 = {
            'username': username,
            'hashed_password': hashed_password,
            'account_level_id': account_level_id
        }
        self.db.execute(sql2, params2)
        # get registered user_id value to insert in join table
        sql_for_user_id = text(f"""
            SELECT
            id
            FROM premium_user as p
            WHERE p.username = :username
        """)
        params = {
            'username': username
        }
        # get_user_id is form of subset...hmmm
        get_User_Id = self.db.execute(sql_for_user_id, params).fetchone() #it doent work when using fetchall..
        # insert user information into join premium_user_quota_endpoint
        sql3 = text(f"""
            INSERT INTO premium_user_quota_endpoint ( user_id, quota_id, endpoint_id,
            current_count, expired_at_quota, expired_at_account_level, renewed_at_for_service )
            VALUES( :user_id, :quota_id, :endpoint_id, :current_count, :expired_at_quota,
            :expired_at_account_level, :renewed_at_for_service)""")
        user_id = get_User_Id[0]
        current_count = 0
        #ts represents current time in second
        ts = time.time()
        #strickly spearking we need to get each period value from account_level and quota table
        #and then convert those values in sec to proceed the following process.
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')  # vs. datetime.datetime.utcnow()
        # expired_at_quota = datetime.datetime.fromtimestamp(ts+(60*60*24)).strftime('%Y-%m-%d %H:%M:%S')  (60*60*24*30)
        # (60*60*24) (40)
        expired_at_quota = datetime.datetime.fromtimestamp(ts+(30)).strftime('%Y-%m-%d %H:%M:%S')
        # (60*60*24*30)
        expired_at_account_level = datetime.datetime.fromtimestamp(ts+60).strftime('%Y-%m-%d %H:%M:%S')
        renewed_at_for_service = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        endpoint_row = [1,2,3,4,5]
        for endpoint_id in endpoint_row:
            params3 = {
                'user_id' : user_id,
                'quota_id' : quota_id,
                'endpoint_id': endpoint_id,
                'current_count': current_count,
                'expired_at_quota': expired_at_quota,
                'expired_at_account_level': expired_at_account_level,
                'renewed_at_for_service': renewed_at_for_service
            }
            self.db.execute(sql3, params3)

        return {"message": "New User registered successfully."}, 201

    def logout(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200

    def refresh(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity = current_user, fresh = False)
        return {'access_token': new_token}, 200

    def get_access_level_and_quota(self, user_id, endpoint_id):
        sql4 = text(f"""
            SELECT
            level_in_number, current_count, count_limit, expired_at_quota, expired_at_account_level
            FROM premium_user_quota_endpoint as p
            INNER JOIN quota_level as q ON p.quota_id = q.id
            INNER JOIN premium_user as u ON p.user_id = u.id
            INNER JOIN account_level as l ON u.account_level_id = l.id
            WHERE user_id = :user_id and endpoint_id = :endpoint_id;
            """)
        params4 = {
            'endpoint_id': endpoint_id,
            'user_id': user_id
        }
        result = self.db.execute(sql4, params4).fetchone()
        return {"level_in_number": result[0], "expired_at_account_level": result[4], "expired_at_quota": result[3], "current_count":result[1], "count_limit":result[2]}

    def update_account_level_table(self, user_id):
        sql_update_al = text(f"""
            UPDATE premium_user
            SET
            account_level_id = 4
            WHERE id = :user_id;""")
        params_update_al = {
            'user_id': user_id,
        }
        self.db.execute(sql_update_al, params_update_al)
        print("update account_level table successfully")

    def update_join_table(self, user_id, endpoint_id, current_count, expired_at_quota):
        sql_update_join = text(f"""
            UPDATE premium_user_quota_endpoint
            SET
            current_count    = :current_count,
            expired_at_quota = CAST(:expired_at_quota as datetime)
            WHERE user_id = :user_id and endpoint_id = :endpoint_id;""")
        params_update_join = {
            'user_id': user_id,
            'endpoint_id': endpoint_id,
            'current_count': current_count,
            'expired_at_quota': expired_at_quota
        }
        self.db.execute(sql_update_join, params_update_join)
        print("update join table successfully")
