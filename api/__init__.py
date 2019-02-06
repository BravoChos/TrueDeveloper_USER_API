import traceback
import decimal

from flask            import Flask, json
from flask_sqlalchemy import SQLAlchemy
###########################################################################
from flask_jwt_extended import JWTManager
from api.blacklist import BLACKLIST
###########################################################################
from api.model   import *
from api.service import *
from api.view    import create_endpoints

class MyJSONEncoder(json.JSONEncoder):

   def default(self, obj):
       if isinstance(obj, decimal.Decimal):
           # Convert decimal instances to strings.
           return str(obj)
       return super(MyJSONEncoder, self).default(obj)

class Services:
    pass

def create_app(config):
    app  = Flask(__name__)
    app.json_encoder = MyJSONEncoder

    ## App Config Settings
    app.debug                                     = config.DEBUG
    app.config['JWT_SECRET_KEY']                  = "some_secret_man"
    # code below is the original#################################################
    app.config['JWT_SECRETE_KEY']                 = config.JWT_SECRETE_KEY
    ##########################################################################
    app.config['JWT_AUTH_USERNAME_KEY']           = config.JWT_AUTH_USERNAME_KEY
    app.config['JWT_EXPIRATION_DELTA_IN_SECONDS'] = config.JWT_EXPIRATION_DELTA_IN_SECONDS
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SQLALCHEMY_DATABASE_URI']         = config.SQLALCHEMY_DATABASE_URI
################################################################################################
    app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
    jwt = JWTManager(app)
# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        return decrypted_token['jti'] in BLACKLIST
###############################################################################################

    ## Init DB
    db  = SQLAlchemy()
    db.init_app(app)
    db_engine = db.get_engine(app)

    ## DAOs
    securities_dao                      = SecuritiesDao(db_engine)
    loan_outstanding_percentages_dao    = LoanOutstandingPercentagesDao(db_engine)
    short_volume_percentages_dao        = ShortVolumePercentagesDao(db_engine)
    days_to_covers_dao                  = DaysToCoversDao(db_engine)
    short_outstanding_percentages_dao   = ShortOutstandingPercentagesDao(db_engine)
    premium_user_dao                    = PremiumUserDao(db_engine)

    ## Services
    services                                                    = Services()
    services.securities_service                                 = SecuritiesService(securities_dao)
    services.loan_outstanding_percentages_service               = LoanOutstandingPercentagesService(loan_outstanding_percentages_dao)
    services.short_volume_percentages_service                   = ShortVolumePercentagesService(short_volume_percentages_dao)
    services.days_to_covers_service                             = DaysToCoversService(days_to_covers_dao)
    services.short_outstanding_percentages_service              = ShortOutstandingPercentagesService(short_outstanding_percentages_dao)
    services.premium_user_service                               = PremiumUserService(premium_user_dao)
    ## End points
    app.register_blueprint(create_endpoints(services))

    return app
