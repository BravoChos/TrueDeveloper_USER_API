import pytest

from sqlalchemy                                             import text
from api.model.dao.loan_outstanding_percentages_dao         import LoanOutstandingPercentagesDao
from tests.test_database                                    import test_database as db
from api.service.loan_outstanding_percentages_service       import LoanOutstandingPercentagesService
from api.model.loan_outstanding_percentage                  import LoanOutstandingPercentage
from decimal                                                import *
from datetime                                               import datetime

@pytest.fixture
def loan_service():
    loan_outstanding_percentage_services = LoanOutstandingPercentagesService(LoanOutstandingPercentagesDao(db))
    return loan_outstanding_percentage_services

def setup_module(module):
    ## Test data creation
    db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.execute(text(f"""INSERT INTO securities
                        (id, market_id, ticker, name)
                        VALUES('500', '1', '014820', '동원시스템즈')"""))
    db.execute(text(f"""INSERT INTO loan_utilization_percentages 
                        (security_id,
                         date,
                         loan_utilization_percentage,
                         loan_outstanding_shares,
                         floating_shares,
                         loan_utilization_percentage_shares,
                         loan_utilization_percentage_amount,
                         all_outstanding_shares,
                         prev_valid_free_floats,
                         prev_valid_outstanding_shares,
                         market_cap,
                         loan_outstanding_amount)
                         VALUES (500, '2016-07-04', "100.00", "100.0000", "100.0000", "100.00", "100.00", "100.0000", "100.0000", "100.0000", "100.0000", "100.0000")"""))
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))

def teardown_module(module):
    ## Test data clean up
    db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.execute(text("TRUNCATE loan_utilization_percentages"))
    db.execute(text("TRUNCATE securities"))
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))

def test_loan_service(loan_service):
    loanServices = loan_service.find("2016-07-04", "2016-07-04", 500)

    expected_date = datetime(2016,7,4).date()

    assert loanServices == [
                            LoanOutstandingPercentage (
                            security_id=500,
                            date=expected_date,
                            loan_utilization_percentage=  Decimal('100.00'),
                            loan_outstanding_shares=Decimal('100.0000'),
                            floating_shares=Decimal('100.0000'),
                            loan_utilization_percentage_shares=Decimal('100.00'),
                            loan_utilization_percentage_amount=Decimal('100.00'),
                            all_outstanding_shares=Decimal('100.0000'),
                            prev_valid_free_floats=Decimal('100.0000'),
                            prev_valid_outstanding_shares=Decimal('100.0000'),
                            market_cap=Decimal('100.0000'),
                            loan_outstanding_amount=Decimal('100.0000')
                                )
                           ]

def test_loan_service_failure(loan_service):
    loanServices = loan_service.find('1900-01-01', '3000-01-01', 99999)
    assert loanServices == []

def test_loan_service_exception(loan_service):
    with pytest.raises(Exception):
        loan_service.find(None)

