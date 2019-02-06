import os
import sys
import logging

from datetime                       import timedelta
from flask_script                   import Manager
from api                            import create_app
from util.cryptography_service      import CryptographyService
from flask_twisted                  import Twisted
from twisted.python                 import log
from util.non_blocking_smtp_handler import NonBlockingSMTPHandler

class Config:
    pass

class StagingConfig(Config):
    def __init__(self, customer_master_key):
        self.cryptography_service = CryptographyService(customer_master_key)

    def get_config(self):
        import credentials 

        decrypt = self.cryptography_service.decrypt

        jwt_secrete_key    = decrypt(credentials.staging['encrypted_secrete_key']).decode()
        db_user_name       = decrypt(credentials.staging['encrypted_db_user_name']).decode()
        db_password        = decrypt(credentials.staging['encrypted_db_password']).decode()
        email_password     = decrypt(credentials.staging['encrypted_email_password']).decode()
        db_host            = os.environ['DB_HOST']
        database           = os.environ['DATABASE']

        config                                 = Config()
        config.DEBUG                           = True
        config.JWT_SECRETE_KEY                 = jwt_secrete_key
        config.JWT_AUTH_USERNAME_KEY           = 'email'
        config.JWT_EXPIRATION_DELTA_IN_SECONDS = 7 * 24 * 60 * 60
        config.SQLALCHEMY_TRACK_MODIFICATIONS  = False
        config.SQLALCHEMY_DATABASE_URI         = f"mysql://{db_user_name}:{db_password}@{db_host}:3306/{database}"
        config.EMAIL                           = 'info@trueshort.com'
        config.EMAIL_PASSWORD                  = email_password

        config.AKM_KEY_ARN = 'arn:aws:kms:ap-northeast-2:774685857155:key/a5ff2eec-197f-4b82-b264-283e72c1644b'

        return config

if __name__ == "__main__":
    env = os.environ['ENV']

    if env == 'STAGING':
        key_arn = 'arn:aws:kms:ap-northeast-2:774685857155:key/a5ff2eec-197f-4b82-b264-283e72c1644b'
        config  = StagingConfig(key_arn).get_config()
    else:
        from config import DevConfig
        config = DevConfig()

    app = create_app(config)

    if env != 'DEV':
        # For developement, use the default web server so we can 
        # leverage from auto re-loading, debug console, and etc
        twisted = Twisted(app)
        log.startLogging(sys.stdout)

    ## Configure logging
    if not app.debug:
        ## Set up the email logging setting
        mail_handler = NonBlockingSMTPHandler(
            mailhost    = ('smtp.gmail.com', 587),
            fromaddr    = config.EMAIL,
            toaddrs     = ['eun@trueshort.com'],
            subject     = 'Critical Error on API',
            credentials = (config.EMAIL, config.EMAIL_PASSWORD),
            secure      = ()
        )
        mail_handler.setLevel(logging.CRITICAL)
        app.logger.addHandler(mail_handler)

    app.logger.info(f"Running the app in {env} mode...")

    manager = Manager(app)
    manager.run()