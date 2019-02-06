import pytest

from decimal                                                    import *
from sqlalchemy                                                 import text
from api.model.dao.short_volume_percentages_dao                 import ShortVolumePercentagesDao
from api.model.short_volume_percentage                          import ShortVolumePercentage
from api.service.short_volume_percentages_service               import ShortVolumePercentagesService
from tests.test_database                                        import test_database as db
from flask                                                      import Blueprint, jsonify, request
from datetime                                                   import datetime

@pytest.fixture
def short_volume_service():
    short_volume_service = ShortVolumePercentagesService(ShortVolumePercentagesDao(db))
    return short_volume_service

def setup_module(module):
    ## Test data creation
    db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.execute(text(f"""INSERT INTO securities
                        (id, market_id, ticker, name)
                        VALUES('500', '1', '014820', '동원시스템즈')"""))
    db.execute(text(f"""INSERT INTO short_volume_percentages 
                        (
                            security_id,
                            date,
                            short_volume_percentage,
                            short_volume,
                            trading_volume   
                        )
                         VALUES (500, '2016-07-04', '50.00', '50.0000', '50.0000')"""))
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))

def teardown_module(module):
    ## Test data clean up
    db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.execute(text("TRUNCATE short_volume_percentages"))
    db.execute(text("TRUNCATE securities"))
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))

def test_short_volume_service(short_volume_service):
    short_volumes_service = short_volume_service.find("2016-07-04", "2016-07-04", 500)

    expected_date = datetime(2016,7,4).date()

    assert short_volumes_service == [
        ShortVolumePercentage (
        security_id=500,
        date=expected_date,
        short_volume_percentage=Decimal(50.00),
        short_volume=Decimal(50.0000),
        trading_volume=Decimal(50.0000)
        )
    ]


def test_short_volume_service_fail(short_volume_service):
    short_volumes_service = short_volume_service.find("2000-07-11", "3000-01-01", 999999)
    assert short_volumes_service == []

def test_short_volume_service_exception(short_volume_service):
    with pytest.raises(Exception):
        short_volumes_service.find(None)