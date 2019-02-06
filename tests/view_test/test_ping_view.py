import pytest
from flask               import Blueprint, jsonify, request
from tests.conftest      import client

def test_ping(client):
    rv = client.get('/ping')
    assert rv.status_code == 200
