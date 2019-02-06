import pytest

from api.model.dao.days_to_covers_dao       import DaysToCoversDao
from api.model.days_to_cover                import DaysToCover
from tests.test_database                    import test_database as db
from sqlalchemy                             import text
from decimal                                import *
from datetime                               import datetime
from flask                                  import Blueprint, jsonify, request


@pytest.fixture
def days_to_cover_dao():
    days_to_cover = DaysToCoversDao(db)
    return days_to_cover

def setup_module(module):
    ## Test data creation
    db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.execute(text(f"""
        INSERT INTO securities (id, market_id, ticker, name)
        VALUES('631', '1', '035420', 'NAVER')"""))
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
        VALUES (631, "2016-06-30", "0.35", "45035.0000", "126984.0000", "0.35", "31974850000.0000", "90774005550.0000" )"""))
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))

def teardown_module(module):
    ## Test data clean up
    db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.execute(text("TRUNCATE days_to_covers"))
    db.execute(text("TRUNCATE securities"))
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))

def test_days_to_cover_dao(days_to_cover_dao):
    days_to_covers = days_to_cover_dao.find("2016-06-30", "2016-06-31", 631)

    expected_date = datetime(2016,6,30).date()

    assert days_to_covers == [
        DaysToCover (
        security_id = 631,
        date = expected_date,
        days_to_cover_in_shares = Decimal("0.35"),
        short_outstanding_shares = Decimal("45035.0000"),
        twenty_days_moving_average_trading_volume= Decimal("126984.0000"),
        days_to_cover_in_amount= Decimal("0.35"),
        short_outstanding_amount= Decimal("31974850000.0000"),
        twenty_days_moving_average_trading_amount= Decimal("90774005550.0000")
        )
    ]

def test_days_to_cover_dao_fail(days_to_cover_dao):
    days_to_covers = days_to_cover_dao.find("2000-07-11", "3000-01-01", 999999)
    assert days_to_covers == []

def test_days_to_cover_dao_exception(days_to_cover_dao):
    with pytest.raises(Exception):
        days_to_cover_dao.find(None)
