import pytest
import os
from envyaml import EnvYAML
from dnt.core.config import Config


def test_load_config():
    fpath = os.path.join(os.path.dirname(__file__), "..", "test_config.yml")
    config = Config(fpath)
    assert isinstance(config._config, EnvYAML)
    assert isinstance(config.sources, dict)
    assert isinstance(config.destinations, dict)
    assert isinstance(config.formatters, dict)
    assert isinstance(config.filterers, dict)
    assert isinstance(config.message_groups, dict)
    assert isinstance(config.jobs, dict)

def test_set_up_services():
    fpath = os.path.join(os.path.dirname(__file__), "..", "test_config.yml")
    config = Config(fpath)
    config._set_up_services()
    assert "sqlite_in_memory" in config.sources
    assert "console" in config.destinations
    assert "new_formatter.TimeStringFormatter" in config.formatters
    assert "new_filterer.DevFilterer" in config.filterers

def test_validate():
    fpath = os.path.join(os.path.dirname(__file__), "..", "test_config.yml")
    config = Config(fpath)
    assert config.validate() is True
