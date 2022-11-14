"""
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""
import os
import pytest

from dnt.core.config import Config


@pytest.fixture
def test_config():
    fpath = os.path.join(os.path.dirname(__file__), "test_config.yml")
    config = Config(fpath)
    return config

@pytest.fixture
def test_config_fn():
    return os.path.join(os.path.dirname(__file__), "test_config.yml")
    
