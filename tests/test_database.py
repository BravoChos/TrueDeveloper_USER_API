from sqlalchemy         import create_engine
from .test_config       import db

db_url = f"mysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
test_database = create_engine(db_url, encoding='utf-8', max_overflow=0)
