import pytest
from tests.conftest import client
from tests.test_database import test_database as db
from sqlalchemy import text

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

def test_ping(client):
    rv = client.get('/ping')
    assert rv.status_code == 200

def test_single_search_true(client):
    rv = client.get('/search/삼성전자')
    assert rv.status_code == 200
    assert rv.json == [
            {
                "id": 314,
                "english_name": "SamsungElectronics",
                "name": "삼성전자",
                "ticker": "005930"
            }
        ]

def test_multiple_search_true(client):
    rv = client.get('/search/삼성')
    assert rv.status_code == 200
    assert rv.json == [
            {
                "english_name": "SamsungFire&MarineInsurance",
                "id": 51,
                "name": "삼성화재",
                "ticker": "000810"
                }, {
                "id": 314,
                "english_name": "SamsungElectronics",
                "name": "삼성전자",
                "ticker": "005930"
            }
        ]

def test_wrongKeyword_search(client):
    rv = client.get('/search/!@$!@')
    assert rv.status_code == 200
    assert rv.json == []

def test_emptyKeyword_search(client):
    rv = client.get('/search')
    assert rv.status_code == 404
    assert rv.json == None
