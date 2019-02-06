import pytest
from flask                                  import Blueprint, jsonify, request
from tests.conftest                         import client
from sqlalchemy                             import text
from tests.test_database                    import test_database as db

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
                         VALUES ('500', '2016-07-04', "100.00", "100.0000", "100.0000", "100.00", "100.00", "100.0000", "100.0000", "100.0000", "100.0000", "100.0000")"""))
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
                         VALUES ('500', '2016-07-05', "100.00", "100.0000", "100.0000", "100.00", "100.00", "100.0000", "100.0000", "100.0000", "100.0000", "100.0000")"""))
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
                         VALUES ('500', '2016-07-06', "100.00", "100.0000", "100.0000", "100.00", "100.00", "100.0000", "100.0000", "100.0000", "100.0000", "100.0000")"""))    
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))


def teardown_module(module):
    ## Test data clean up
    db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.execute(text("TRUNCATE loan_utilization_percentages"))
    db.execute(text("TRUNCATE securities"))
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))

def test_loan_endpoint(client):
    rv = client.get('/loan-outstanding-percentages/500?start_date=2016-07-04&end_date=2016-07-04')
    assert rv.status_code == 200
    assert rv.json == [{'all_outstanding_shares': '100.0000',
                        'date': 'Mon, 04 Jul 2016 00:00:00 GMT',
                        'floating_shares': '100.0000',
                        'loan_outstanding_amount': '100.0000',
                        'loan_outstanding_shares': '100.0000',
                        'loan_utilization_percentage': '100.00',
                        'loan_utilization_percentage_amount': '100.00', 
                        'loan_utilization_percentage_shares': '100.00', 
                        'market_cap': '100.0000',
                        'prev_valid_free_floats': '100.0000', 
                        'prev_valid_outstanding_shares': '100.0000',
                        'security_id': 500}]

def test_loan_endpoint_without_start_date(client):
    rv = client.get('/loan-outstanding-percentages/500?end_date=2016-07-05')
    assert rv.status_code == 200
    assert rv.json == [{'all_outstanding_shares': '100.0000',
                        'date': 'Mon, 04 Jul 2016 00:00:00 GMT',
                        'floating_shares': '100.0000',
                        'loan_outstanding_amount': '100.0000',
                        'loan_outstanding_shares': '100.0000',
                        'loan_utilization_percentage': '100.00',
                        'loan_utilization_percentage_amount': '100.00',
                        'loan_utilization_percentage_shares': '100.00',
                        'market_cap': '100.0000',
                        'prev_valid_free_floats': '100.0000',
                        'prev_valid_outstanding_shares': '100.0000',
                        'security_id': 500},
                       {'all_outstanding_shares': '100.0000',
                        'date': 'Tue, 05 Jul 2016 00:00:00 GMT',
                        'floating_shares': '100.0000',
                        'loan_outstanding_amount': '100.0000',
                        'loan_outstanding_shares': '100.0000',
                        'loan_utilization_percentage': '100.00',
                        'loan_utilization_percentage_amount': '100.00',
                        'loan_utilization_percentage_shares': '100.00',
                        'market_cap': '100.0000',
                        'prev_valid_free_floats': '100.0000',
                        'prev_valid_outstanding_shares': '100.0000',
                        'security_id': 500}]

def test_loan_endpoint_without_end_date(client):
    rv = client.get('/loan-outstanding-percentages/500?start_date=2016-07-04')
    assert rv.json ==   [{'all_outstanding_shares': '100.0000',
                        'date': 'Mon, 04 Jul 2016 00:00:00 GMT',
                        'floating_shares': '100.0000',
                        'loan_outstanding_amount': '100.0000',
                        'loan_outstanding_shares': '100.0000',
                        'loan_utilization_percentage': '100.00',
                        'loan_utilization_percentage_amount': '100.00',
                        'loan_utilization_percentage_shares': '100.00',
                        'market_cap': '100.0000',
                        'prev_valid_free_floats': '100.0000',
                        'prev_valid_outstanding_shares': '100.0000',
                        'security_id': 500},
                        {'all_outstanding_shares': '100.0000',
                        'date': 'Tue, 05 Jul 2016 00:00:00 GMT',
                        'floating_shares': '100.0000',
                        'loan_outstanding_amount': '100.0000',
                        'loan_outstanding_shares': '100.0000',
                        'loan_utilization_percentage': '100.00',
                        'loan_utilization_percentage_amount': '100.00',
                        'loan_utilization_percentage_shares': '100.00',
                        'market_cap': '100.0000',
                        'prev_valid_free_floats': '100.0000',
                        'prev_valid_outstanding_shares': '100.0000',
                        'security_id': 500},
                        {'all_outstanding_shares': '100.0000',
                        'date': 'Wed, 06 Jul 2016 00:00:00 GMT',
                        'floating_shares': '100.0000',
                        'loan_outstanding_amount': '100.0000',
                        'loan_outstanding_shares': '100.0000',
                        'loan_utilization_percentage': '100.00',
                        'loan_utilization_percentage_amount': '100.00',
                        'loan_utilization_percentage_shares': '100.00',
                        'market_cap': '100.0000',
                        'prev_valid_free_floats': '100.0000',
                        'prev_valid_outstanding_shares': '100.0000',
                        'security_id': 500}]

def test_loan_endpoint_without_date(client):
    rv = client.get('/loan-outstanding-percentages/500')
    assert rv.status_code == 200
    assert rv.json == [{'all_outstanding_shares': '100.0000',
                        'date': 'Mon, 04 Jul 2016 00:00:00 GMT',
                        'floating_shares': '100.0000',
                        'loan_outstanding_amount': '100.0000',
                        'loan_outstanding_shares': '100.0000',
                        'loan_utilization_percentage': '100.00',
                        'loan_utilization_percentage_amount': '100.00',
                        'loan_utilization_percentage_shares': '100.00',
                        'market_cap': '100.0000',
                        'prev_valid_free_floats': '100.0000',
                        'prev_valid_outstanding_shares': '100.0000',
                        'security_id': 500},
                        {'all_outstanding_shares': '100.0000',
                        'date': 'Tue, 05 Jul 2016 00:00:00 GMT',
                        'floating_shares': '100.0000',
                        'loan_outstanding_amount': '100.0000',
                        'loan_outstanding_shares': '100.0000',
                        'loan_utilization_percentage': '100.00',
                        'loan_utilization_percentage_amount': '100.00',
                        'loan_utilization_percentage_shares': '100.00',
                        'market_cap': '100.0000',
                        'prev_valid_free_floats': '100.0000',
                        'prev_valid_outstanding_shares': '100.0000',
                        'security_id': 500},
                        {'all_outstanding_shares': '100.0000',
                        'date': 'Wed, 06 Jul 2016 00:00:00 GMT',
                        'floating_shares': '100.0000',
                        'loan_outstanding_amount': '100.0000',
                        'loan_outstanding_shares': '100.0000',
                        'loan_utilization_percentage': '100.00',
                        'loan_utilization_percentage_amount': '100.00',
                        'loan_utilization_percentage_shares': '100.00',
                        'market_cap': '100.0000',
                        'prev_valid_free_floats': '100.0000',
                        'prev_valid_outstanding_shares': '100.0000',
                        'security_id': 500}]

def test_loan_with_unknown_security_id(client):
    rv = client.get('/loan-outstanding-percentages/99999999')
    assert rv.status_code == 200
    assert rv.json == []

def test_loan_without_security_id(client):
    rv = client.get('/loan-outstanding-percentages/not_number')
    assert rv.status_code == 400

