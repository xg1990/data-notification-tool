"""
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""
import os
import random
import string
import pytest

from dnt.core.config import Config

@pytest.fixture
def test_secret() -> str:
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(30))

@pytest.fixture
def test_config(test_secret):
    os.environ['SPECIAL_ENVVAR'] = test_secret
    fpath = os.path.join(os.path.dirname(__file__), "test_config.yml")
    config = Config(fpath)
    return config

@pytest.fixture
def test_config_fn():
    return os.path.join(os.path.dirname(__file__), "test_config.yml")
    
