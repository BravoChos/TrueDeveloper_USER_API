import pytest
from api.service.securities_service import SecuritiesService
from api.model.dao.securities_dao import SecuritiesDao
from api.model.security import Security
from tests.test_database import test_database as db
from sqlalchemy import text

@pytest.fixture
def securities_service():
    search = SecuritiesService(SecuritiesDao(db))
    return search

def setup_module(module):
    db.execute(text(f"""
        INSERT INTO securities (id, name, ticker, english_name, market_id)
        VALUES (314,"삼성전자", "005930", "SamsungElectronics", 1)
    """))
    db.execute(text(f"""
        INSERT INTO securities (id, name, ticker, english_name, market_id)
        VALUES (51,"삼성화재", "000810", "SamsungFire&MarineInsurance", 1)
    """))

def teardown_module(module):
    ## Test data clean up
    db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.execute(text("TRUNCATE securities"))
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))

def test_singleResult_service_search(securities_service):
    securities = securities_service.search('삼성전자')

    for s in securities:
        s.id = None

    assert securities == [
        Security(id = None, english_name = "SamsungElectronics", name = "삼성전자", ticker = "005930")
    ]

def test_multipleResult_service_search(securities_service):
    securities = securities_service.search('삼성')

    for s in securities:
        s.id = None

    print("what is securities :", securities)
    assert securities == [
        Security(id = None, english_name = "SamsungFire&MarineInsurance", name = "삼성화재", ticker = "000810"),
        Security(id = None, english_name = "SamsungElectronics", name = "삼성전자", ticker = "005930"),
    ]

def test_wrongKeyword_search(securities_service):
    securities = securities_service.search('!@#!$%')
    print("what is securities :", securities)
    assert len(securities) == 0

def test_emptyKeyword_search(securities_service):
    securities = securities_service.search('')
    assert len(securities) == 0
