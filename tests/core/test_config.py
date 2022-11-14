import os

from envyaml.envyaml import EnvYAML

from dnt.core.config import Config


def test_load_config():
    fpath = os.path.join(os.path.dirname(__file__), "..", "test_config.yml")
    config = Config(fpath)
    assert isinstance(config._config, EnvYAML)
