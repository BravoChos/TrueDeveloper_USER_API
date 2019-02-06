import pytest

from api                     import create_app
from .test_config            import DevConfig

@pytest.fixture
def client():
    config = DevConfig()
    app = create_app(config)
    app.config['TESTING'] = True

    client = app.test_client()
    
    yield client
