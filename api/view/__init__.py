import logging

from flask import Blueprint, jsonify, request, abort
import bcrypt
####################################################################
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    fresh_jwt_required,
    jwt_refresh_token_required,
    jwt_optional,
    get_jwt_identity
)
import time, datetime
#####################################################################
def create_endpoints(services):
    endpoint = Blueprint('simple_page', __name__) ##what does this Blueprint do?

    @endpoint.route("/ping")
    def ping():
        return "pong"

    @endpoint.route("/search/<keyword>", methods=['GET'])
    @jwt_required
    def search(keyword):
        endpoint_id = 1
        access_level = 3
        user_id = get_jwt_identity()
        # user_id = 1
        ts = time.time() #ts = time in seconds
        st = datetime.datetime.fromtimestamp(ts) #st = standard time

        result = services.premium_user_service.get_access_level_and_quota(user_id, endpoint_id)
        level_in_number = result["level_in_number"]
        expired_at_account_level = result["expired_at_account_level"]
        expired_at_quota = result["expired_at_quota"]
        count_limit = result["count_limit"]
        current_count = result["current_count"]

        #1. check account_level
        if level_in_number < access_level:
            return jsonify({"message": "Invalid Credentials. Please Upgrade The Account Level!"}), 401
        #2. check account_level period
        if expired_at_account_level < st:
            #  uptates account_level to None!!!
            services.premium_user_service.update_account_level_table(user_id)
            return jsonify({"message": "Service Period Expired. Please renew your status!"}), 401
        #3. check quota period ?60*60*24
        if expired_at_quota < st:
            expired_at_quota = datetime.datetime.fromtimestamp(ts+40).strftime('%Y-%m-%d %H:%M:%S')
            current_count = 0
            # services.premium_user_service.update_join_table(user_id, endpoint_id, current_count, expired_at_quota)
        #4. check quota allowance
        elif count_limit <= current_count:
            return jsonify({"message": "Exceeded Quota Allowance. Please try our service tomorrow!"}), 401

        services.premium_user_service.update_join_table(user_id, endpoint_id, current_count+1, expired_at_quota)
        securities = services.securities_service.search(keyword)
        return jsonify([security.to_json() for security in securities])

    @endpoint.route("/loan-outstanding-percentages/<security_id>", methods=['GET'])
    # @jwt_required
    def find_loan_outstanding_percentages(security_id):
        endpoint_id = 3
        access_level = 2
        # user_id = get_jwt_identity()
        user_id = 1
        ts = time.time() #ts = time in seconds
        st = datetime.datetime.fromtimestamp(ts) #st = standard time

        result = services.premium_user_service.get_access_level_and_quota(user_id, endpoint_id)
        level_in_number = result["level_in_number"]
        expired_at_account_level = result["expired_at_account_level"]
        expired_at_quota = result["expired_at_quota"]
        count_limit = result["count_limit"]
        current_count = result["current_count"]

        #1. check account_level
        if level_in_number < access_level:
            return jsonify({"message": "Invalid Credentials. Please Upgrade The Account Level!"}), 401
        #2. check account_level period
        if expired_at_account_level < st:
            # uptates account_level to None!!!
            services.premium_user_service.update_account_level_table(user_id)
            return jsonify({"message": "Service Period Expired. Please renew your status!"}), 401
        #3. check quota period
        if expired_at_quota < st:  #60*60*24
            expired_at_quota = datetime.datetime.fromtimestamp(ts+9).strftime('%Y-%m-%d %H:%M:%S')
            current_count = 0
        #4. check quota allowance
        elif count_limit <= current_count:
            return jsonify({"message": "Exceeded Quota Allowance. Please try our service tomorrow!"}), 401
        services.premium_user_service.update_join_table(user_id, endpoint_id, current_count+1, expired_at_quota)

        if not security_id.isdigit():
            return "", 400

        start_date = request.args.get("start_date", "1800-01-01")
        end_date = request.args.get("end_date", "2200-01-01")
        loans = services.loan_outstanding_percentages_service.find(start_date, end_date, security_id)
        return jsonify([loan.to_json() for loan in loans])

    @endpoint.route("/short-outstanding-percentages/<security_id>", methods=['GET'])
    @jwt_required
    def find_short_outstanding_percentages(security_id):
        endpoint_id = 5
        access_level = 1
        user_id = get_jwt_identity()
        ts = time.time() #ts = time in seconds
        st = datetime.datetime.fromtimestamp(ts) #st = standard time

        result = services.premium_user_service.get_access_level_and_quota(user_id, endpoint_id)
        level_in_number = result["level_in_number"]
        expired_at_account_level = result["expired_at_account_level"]
        expired_at_quota = result["expired_at_quota"]
        count_limit = result["count_limit"]
        current_count = result["current_count"]

        #1. check account_level
        if level_in_number < access_level:
            return jsonify({"message": "Invalid Account Level. Please Upgrade!"}), 401
        #2. check account_level period
        if expired_at_account_level < st:
            # uptates account_level to None!!!
            services.premium_user_service.update_account_level_table(user_id)
            return jsonify({"message": "Service Period Expired. Please Renew Account!"}), 401
        #3. check quota period
        if expired_at_quota < st:
            expired_at_quota = datetime.datetime.fromtimestamp(ts+60*60*24).strftime('%Y-%m-%d %H:%M:%S')
            current_count = 0
        #4. check quota allowance
        elif count_limit <= current_count:
            return jsonify({"message": "Exceeded Quota Allowance. Please try our service tomorrow!"}), 401
        services.premium_user_service.update_join_table(user_id, endpoint_id, current_count+1, expired_at_quota)

        if not security_id.isdigit():
            return "", 400

        start_date = request.args.get("start_date", "1800-01-01")
        end_date = request.args.get("end_date", "2200-01-01")
        short_outs = services.short_outstanding_percentages_service.find(start_date, end_date, security_id)
        return jsonify([short_out.to_json() for short_out in short_outs])

    @endpoint.route("/short-volume-percentages/<security_id>", methods=['GET'])
    @jwt_required
    def find_short_volume_percentages(security_id):
        endpoint_id = 4
        access_level = 2
        user_id = get_jwt_identity()
        ts = time.time() #ts = time in seconds
        st = datetime.datetime.fromtimestamp(ts) #st = standard time

        result = services.premium_user_service.get_access_level_and_quota(user_id, endpoint_id)
        level_in_number = result["level_in_number"]
        expired_at_account_level = result["expired_at_account_level"]
        expired_at_quota = result["expired_at_quota"]
        count_limit = result["count_limit"]
        current_count = result["current_count"]

        #1. check account_level
        if level_in_number < access_level:
            return jsonify({"message": "Invalid Credentials. Please Upgrade The Account Level!"}), 401
        #2. check account_level period
        if expired_at_account_level < st:
            # uptates account_level to None!!!
            services.premium_user_service.update_account_level_table(user_id)
            return jsonify({"message": "Service Period Expired. Please renew your status!"}), 401
        #3. check quota period
        if expired_at_quota < st:
            expired_at_quota = datetime.datetime.fromtimestamp(ts+60*60*24).strftime('%Y-%m-%d %H:%M:%S')
            current_count = 0
        #4. check quota allowance
        elif count_limit <= current_count:
            return jsonify({"message": "Exceeded Quota Allowance. Please try our service tomorrow!"}), 401
        services.premium_user_service.update_join_table(user_id, endpoint_id, current_count + 1, expired_at_quota)

        if not security_id.isdigit():
            return "", 400

        start_date = request.args.get("start_date", "1800-01-01")
        end_date = request.args.get("end_date", "2200-01-01")
        shortVolumes = services.short_volume_percentages_service.find(start_date, end_date, security_id)
        return jsonify([shortVolume.to_json() for shortVolume in shortVolumes])

    @endpoint.route("/days-to-covers/<security_id>", methods=['GET'])
    @jwt_required
    def find_days_to_covers(security_id):
        endpoint_id = 2
        access_level = 3
        user_id = get_jwt_identity()
        ts = time.time() #ts = time in seconds
        st = datetime.datetime.fromtimestamp(ts) #st = standard time

        result = services.premium_user_service.get_access_level_and_quota(user_id, endpoint_id)
        level_in_number = result["level_in_number"]
        expired_at_account_level = result["expired_at_account_level"]
        expired_at_quota = result["expired_at_quota"]
        count_limit = result["count_limit"]
        current_count = result["current_count"]

        #1. check account_level
        if level_in_number < access_level:
            return jsonify({"message": "Invalid Credentials. Please Upgrade The Account Level!"}), 401
        #2. check account_level period
        if expired_at_account_level < st:
            # uptates account_level to None!!!
            services.premium_user_service.update_account_level_table(user_id)
            return jsonify({"message": "Service Period Expired. Please renew your status!"}), 401
        #3. check quota period
        if expired_at_quota < st:
            expired_at_quota = datetime.datetime.fromtimestamp(ts+60*60*24).strftime('%Y-%m-%d %H:%M:%S')
            current_count = 0
        #4. check quota allowance
        elif count_limit <= current_count:
            return jsonify({"message": "Exceeded Quota Allowance. Please try our service tomorrow!"}), 401
        services.premium_user_service.update_join_table(user_id, endpoint_id, current_count+1, expired_at_quota)

        if not security_id.isdigit():
            return "", 400

        start_date = request.args.get("start_date", "1800-01-01")
        end_date = request.args.get("end_date", "2200-01-01")
        days_to_covers = services.days_to_covers_service.find(start_date, end_date, security_id)
        return jsonify([days_to_cover.to_json() for days_to_cover in days_to_covers])

    @endpoint.route("/login", methods=['GET'])
    def login_premium_user():

        username = request.headers['username']
        password = request.headers['password'].encode('utf-8')

        if username == None or password == None:
            return {"message": "username and password cannot be left blank!"}

        hashed_password = services.premium_user_service.get_hashed_password(username)
        if bcrypt.checkpw(password, hashed_password[0].encode('utf-8')):
            result = services.premium_user_service.get_token(username)
            return jsonify(result), 200
        else:
            return jsonify({"message": "You have entered wrong password!"})

    @endpoint.route("/register", methods=['GET'])
    def register_premium_user():
        username = request.headers['username']
        password = request.headers['password'].encode('utf-8')
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        account_level_id = request.headers['account_level_id']
        quota_id = request.headers['quota_id']

        if username == None or hashed_password == None:
            return jsonify({"message": "username and password cannot be left blank!"})

        user_register = services.premium_user_service.register(username, hashed_password, account_level_id, quota_id)
        return jsonify(user_register)

    @endpoint.route("/logout", methods=['POST'])
    @jwt_required
    def logout_premium_user():
        result = services.premium_user_service.logout()
        return jsonify(result)

    @endpoint.route("/refresh", methods=['POST'])
    @jwt_refresh_token_required
    def refresh_premium_user_token():
        result = services.premium_user_service.refresh()
        return jsonify(result)

    return endpoint
