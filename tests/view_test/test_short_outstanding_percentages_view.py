import pytest
from flask                                  import Blueprint, jsonify, request
from tests.conftest                         import client
from sqlalchemy                             import text
from tests.test_database                    import test_database as db
from flask                                  import Blueprint, jsonify, request

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
                        VALUES ('500', '2016-07-04', "100.00", "100.0000", "100.0000")"""))
    db.execute(text(f"""INSERT INTO short_outstanding_percentages 
                        (security_id,
                        date,
                        short_outstanding_percentage,
                        floating_shares,
                        short_outstanding_shares)
                        VALUES ('500', '2016-07-05', "100.00", "100.0000", "100.0000")"""))
    db.execute(text(f"""INSERT INTO short_outstanding_percentages 
                        (security_id,
                        date,
                        short_outstanding_percentage,
                        floating_shares,
                        short_outstanding_shares)
                        VALUES ('500', '2016-07-06', "100.00", "100.0000", "100.0000")"""))
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))

def teardown_module(module):
    ## Test data clean up
    db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.execute(text("TRUNCATE short_outstanding_percentages"))
    db.execute(text("TRUNCATE securities"))
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))

#test for 1
def test_short_out_with_all(client):
    rv = client.get('/short-outstanding-percentages/500?start_date=2016-07-04&end_date=2016-07-04')
    assert rv.status_code == 200
    assert rv.json == [{
                        "date": "Mon, 04 Jul 2016 00:00:00 GMT", 
                        "floating_shares": "100.0000", 
                        "security_id": 500, 
                        "short_outstanding_percentage": "100.00", 
                        "short_outstanding_shares": "100.0000"
                        }]

#test for 1
def test_short_out_endpoint_without_start_date(client):
    rv = client.get('/short-outstanding-percentages/500?end_date=2016-07-05')
    assert rv.status_code == 200
    assert rv.json == [{
                        "date": "Mon, 04 Jul 2016 00:00:00 GMT", 
                        "floating_shares": "100.0000", 
                        "security_id": 500, 
                        "short_outstanding_percentage": "100.00", 
                        "short_outstanding_shares": "100.0000"
                        },
                       {
                        "date": "Tue, 05 Jul 2016 00:00:00 GMT", 
                        "floating_shares": "100.0000", 
                        "security_id": 500, 
                        "short_outstanding_percentage": "100.00", 
                        "short_outstanding_shares": "100.0000"
                        }]

#test for 1
def test_short_out_endpoint_without_end_date(client):
    rv = client.get('/short-outstanding-percentages/500?start_date=2016-07-04')
    assert rv.json ==   [{
                        "date": "Mon, 04 Jul 2016 00:00:00 GMT", 
                        "floating_shares": "100.0000", 
                        "security_id": 500, 
                        "short_outstanding_percentage": "100.00", 
                        "short_outstanding_shares": "100.0000"
                        },
                        {
                        "date": "Tue, 05 Jul 2016 00:00:00 GMT", 
                        "floating_shares": "100.0000", 
                        "security_id": 500, 
                        "short_outstanding_percentage": "100.00", 
                        "short_outstanding_shares": "100.0000"
                        },
                        {
                        "date": "Wed, 06 Jul 2016 00:00:00 GMT", 
                        "floating_shares": "100.0000", 
                        "security_id": 500, 
                        "short_outstanding_percentage": "100.00", 
                        "short_outstanding_shares": "100.0000"
                        }]

#test for 1
def test_short_out_endpoint_without_dates(client):
    rv = client.get('/short-outstanding-percentages/500')
    assert rv.status_code == 200
    assert rv.json == [{
                        "date": "Mon, 04 Jul 2016 00:00:00 GMT", 
                        "floating_shares": "100.0000", 
                        "security_id": 500, 
                        "short_outstanding_percentage": "100.00", 
                        "short_outstanding_shares": "100.0000"
                        },
                        {
                        "date": "Tue, 05 Jul 2016 00:00:00 GMT", 
                        "floating_shares": "100.0000", 
                        "security_id": 500, 
                        "short_outstanding_percentage": "100.00", 
                        "short_outstanding_shares": "100.0000"
                        },
                        {
                        "date": "Wed, 06 Jul 2016 00:00:00 GMT", 
                        "floating_shares": "100.0000", 
                        "security_id": 500, 
                        "short_outstanding_percentage": "100.00", 
                        "short_outstanding_shares": "100.0000"
                        }]

#test for 0
def test_short_out_with_unknown_security_id(client):
    rv = client.get('/short-outstanding-percentages/99999999')
    assert rv.status_code == 200
    assert rv.json == []

#test for -1
def test_short_out_without_security_id(client):
    rv = client.get('/short-outstanding-percentages/test')
    assert rv.status_code == 400
