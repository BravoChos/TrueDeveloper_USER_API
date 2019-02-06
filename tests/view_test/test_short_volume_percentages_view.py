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
    db.execute(text(f"""INSERT INTO short_volume_percentages 
                        (
                            security_id,
                            date,
                            short_volume_percentage,
                            short_volume,
                            trading_volume   
                        )
                         VALUES (500, '2016-07-05', '50.00', '50.0000', '50.0000')"""))
    db.execute(text(f"""INSERT INTO short_volume_percentages 
                        (
                            security_id,
                            date,
                            short_volume_percentage,
                            short_volume,
                            trading_volume   
                        )
                         VALUES (500, '2016-07-06', '50.00', '50.0000', '50.0000')"""))
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))


def teardown_module(module):
    ## Test data clean up
    db.execute(text("SET FOREIGN_KEY_CHECKS=0"))
    db.execute(text("TRUNCATE short_volume_percentages"))
    db.execute(text("TRUNCATE securities"))
    db.execute(text("SET FOREIGN_KEY_CHECKS=1"))

def test_short_volume_endpoint(client):
    rv = client.get('/short-volume-percentages/500?start_date=2016-07-04&end_date=2016-07-04')
    assert rv.status_code == 200
    assert rv.json == [{'date': 'Mon, 04 Jul 2016 00:00:00 GMT',
                        'security_id': 500,
                        'short_volume': '50.0000',
                        'short_volume_percentage': '50.00',
                        'trading_volume': '50.0000'}]

def test_short_volume_endpoint_without_start_date(client):
    rv = client.get('/short-volume-percentages/500?end_date=2016-07-05')
    assert rv.status_code == 200
    assert rv.json == [{'date': 'Mon, 04 Jul 2016 00:00:00 GMT',
                        'security_id': 500,
                        'short_volume': '50.0000',
                        'short_volume_percentage': '50.00',
                        'trading_volume': '50.0000'},
                        {'date': 'Tue, 05 Jul 2016 00:00:00 GMT',
                        'security_id': 500,
                        'short_volume': '50.0000',
                        'short_volume_percentage': '50.00',
                        'trading_volume': '50.0000'}]

def test_short_volume_endpoint_without_end_date(client):
    rv = client.get('/short-volume-percentages/500?start_date=2016-07-05')
    assert rv.json ==   [{'date': 'Tue, 05 Jul 2016 00:00:00 GMT',
                        'security_id': 500,
                        'short_volume': '50.0000',
                        'short_volume_percentage': '50.00',
                        'trading_volume': '50.0000'},
                        {'date': 'Wed, 06 Jul 2016 00:00:00 GMT',
                        'security_id': 500,
                        'short_volume': '50.0000',
                        'short_volume_percentage': '50.00',
                        'trading_volume': '50.0000'}]


def test_short_volume_endpoint_without_date(client):
    rv = client.get('/short-volume-percentages/500')
    assert rv.status_code == 200
    assert rv.json == [{'date': 'Mon, 04 Jul 2016 00:00:00 GMT',
                        'security_id': 500,
                        'short_volume': '50.0000',
                        'short_volume_percentage': '50.00',
                        'trading_volume': '50.0000'},
                        {'date': 'Tue, 05 Jul 2016 00:00:00 GMT',
                        'security_id': 500,
                        'short_volume': '50.0000',
                        'short_volume_percentage': '50.00',
                        'trading_volume': '50.0000'},
                        {'date': 'Wed, 06 Jul 2016 00:00:00 GMT',
                        'security_id': 500,
                        'short_volume': '50.0000',
                        'short_volume_percentage': '50.00',
                        'trading_volume': '50.0000'}]

def test_short_volume_with_unknown_security_id(client):
    rv = client.get('/short-volume-percentages/99999999')
    assert rv.status_code == 200
    assert rv.json == []

def test_short_volume_without_security_id(client):
    rv = client.get('/short-volume-percentages/not_number')
    assert rv.status_code == 400

