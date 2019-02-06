import pytest

from sqlalchemy                             import text
from tests.conftest                         import client
from tests.test_database                    import test_database as db
from flask                                  import Blueprint, jsonify, request

def setup_module(module):
    ## Test data creation
    db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.execute(text(f"""
        INSERT INTO securities (id, market_id, ticker, name)
        VALUES(631, '1', '035420', 'NAVER')"""))
    db.execute(text(f"""
        INSERT INTO days_to_covers
            (security_id,
            date,
            days_to_cover_in_shares,
            short_outstanding_shares,
            twenty_days_moving_average_trading_volume,
            days_to_cover_in_amount,
            short_outstanding_amount,
            twenty_days_moving_average_trading_amount)
        VALUES (631, "2016-07-04", "0.39", "49425.0000", "127226.0000", "0.39", "35931975000.0000", "91136813750.0000" )"""))
    db.execute(text(f"""
        INSERT INTO days_to_covers
            (security_id,
            date,
            days_to_cover_in_shares,
            short_outstanding_shares,
            twenty_days_moving_average_trading_volume,
            days_to_cover_in_amount,
            short_outstanding_amount,
            twenty_days_moving_average_trading_amount)
        VALUES (631, "2016-07-05", "0.32", "41314.0000", "128596.2500", "0.34", "30985500000.0000", "92378772400.0000" )"""))
    db.execute(text(f"""
        INSERT INTO days_to_covers
            (security_id,
            date,
            days_to_cover_in_shares,
            short_outstanding_shares,
            twenty_days_moving_average_trading_volume,
            days_to_cover_in_amount,
            short_outstanding_amount,
            twenty_days_moving_average_trading_amount)
        VALUES (631, "2016-07-06", "0.31", "40332.0000", "129156.6500", "0.32", "30047340000.00000", "92924194100.0000" )"""))
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))

def teardown_module(module):
    ## Test data clean up
    db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.execute(text("TRUNCATE days_to_covers"))
    db.execute(text("TRUNCATE securities"))
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))

def test_loan_endpoint(client):
    rv = client.get('/days-to-covers/631?start_date=2016-07-04&end_date=2016-07-04')
    assert rv.status_code == 200
    assert rv.json == [
        {
            "date": "Mon, 04 Jul 2016 00:00:00 GMT",
            "days_to_cover_in_amount": "0.39",
            "days_to_cover_in_shares": "0.39",
            "security_id": 631,
            "short_outstanding_amount": "35931975000.0000",
            "short_outstanding_shares": "49425.0000",
            "twenty_days_moving_average_trading_amount": "91136813750.0000",
            "twenty_days_moving_average_trading_volume": "127226.0000"
        }]
def test_loan_endpoint_without_start_date(client):
    rv = client.get('/days-to-covers/631?end_date=2016-07-05')
    assert rv.status_code == 200
    assert rv.json == [
        {
            "date": "Mon, 04 Jul 2016 00:00:00 GMT",
            "days_to_cover_in_amount": "0.39",
            "days_to_cover_in_shares": "0.39",
            "security_id": 631,
            "short_outstanding_amount": "35931975000.0000",
            "short_outstanding_shares": "49425.0000",
            "twenty_days_moving_average_trading_amount": "91136813750.0000",
            "twenty_days_moving_average_trading_volume": "127226.0000"
        },
        {
            "date": "Tue, 05 Jul 2016 00:00:00 GMT",
            "days_to_cover_in_amount": "0.34",
            "days_to_cover_in_shares": "0.32",
            "security_id": 631,
            "short_outstanding_amount": "30985500000.0000",
            "short_outstanding_shares": "41314.0000",
            "twenty_days_moving_average_trading_amount": "92378772400.0000",
            "twenty_days_moving_average_trading_volume": "128596.2500"
        }]

def test_loan_endpoint_without_end_date(client):
    rv = client.get('/days-to-covers/631?start_date=2016-07-04')
    assert rv.status_code == 200
    assert rv.json == [
        {
            "date": "Mon, 04 Jul 2016 00:00:00 GMT",
            "days_to_cover_in_amount": "0.39",
            "days_to_cover_in_shares": "0.39",
            "security_id": 631,
            "short_outstanding_amount": "35931975000.0000",
            "short_outstanding_shares": "49425.0000",
            "twenty_days_moving_average_trading_amount": "91136813750.0000",
            "twenty_days_moving_average_trading_volume": "127226.0000"
      },
      {
            "date": "Tue, 05 Jul 2016 00:00:00 GMT",
            "days_to_cover_in_amount": "0.34",
            "days_to_cover_in_shares": "0.32",
            "security_id": 631,
            "short_outstanding_amount": "30985500000.0000",
            "short_outstanding_shares": "41314.0000",
            "twenty_days_moving_average_trading_amount": "92378772400.0000",
            "twenty_days_moving_average_trading_volume": "128596.2500"
      },
      {
            "date": "Wed, 06 Jul 2016 00:00:00 GMT",
            "days_to_cover_in_amount": "0.32",
            "days_to_cover_in_shares": "0.31",
            "security_id": 631,
            "short_outstanding_amount": "30047340000.0000",
            "short_outstanding_shares": "40332.0000",
            "twenty_days_moving_average_trading_amount": "92924194100.0000",
            "twenty_days_moving_average_trading_volume": "129156.6500"
      }]

def test_loan_with_unknown_security_id(client):
    rv = client.get('/days-to-covers/99999999')
    assert rv.status_code == 200
    assert rv.json == []

def test_loan_without_security_id(client):
    rv = client.get('/days-to-covers/not_number')
    assert rv.status_code == 400
