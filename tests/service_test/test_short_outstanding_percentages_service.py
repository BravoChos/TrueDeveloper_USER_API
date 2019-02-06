import pytest

from sqlalchemy                                             import text
from api.model.dao.short_outstanding_percentages_dao        import ShortOutstandingPercentagesDao
from tests.test_database                                    import test_database as db
from api.service.short_outstanding_percentages_service      import ShortOutstandingPercentagesService
from decimal                                                import Decimal
from datetime                                               import datetime
from api.model.short_outstanding_percentage                 import ShortOutstandingPercentage


@pytest.fixture
def short_out_service():
    short_out_service = ShortOutstandingPercentagesService(ShortOutstandingPercentagesDao(db))
    return short_out_service

def setup_module(module):
    ## Test data creation
    db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.execute(text(f"""INSERT INTO securities      
                        (id, market_id, ticker, name)
                        VALUES('500', '1', '014820', '템즈')"""))
    db.execute(text(f"""INSERT INTO short_outstanding_percentages 
                        (security_id,
                         date,
                         short_outstanding_percentage,
                         floating_shares,
                         short_outstanding_shares)
                         VALUES ('500', '2016-07-04', "100.00", "100.0000", "100.00")"""))
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))

def teardown_module(module):
    ## Test data clean up
    db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.execute(text("TRUNCATE short_outstanding_percentages"))
    db.execute(text("TRUNCATE securities"))
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))

#test for 1
def test_short_out_service(short_out_service):
    short_outs = short_out_service.find("2016-07-04", "2016-07-04", 500)

    expected_date = datetime(2016,7,4).date()

    assert short_outs == [
        ShortOutstandingPercentage (
        security_id=500,
        date=expected_date,
        short_outstanding_percentage= Decimal('100.00'),
        floating_shares=Decimal('100.0000'),
        short_outstanding_shares=Decimal('100.00'),
        )
    ]

#test for 0
def test_short_out_service_fail(short_out_service):
    short_outs = short_out_service.find("2000-07-11", "3000-01-01", 999999)
    assert short_outs == []

#test for -1
def test_short_out_service_exception(short_out_service):
    with pytest.raises(Exception):
        short_out_dao.find(None)