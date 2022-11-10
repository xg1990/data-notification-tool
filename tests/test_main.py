import os

from dnt.main import main, load_config
from click.testing import CliRunner

__author__ = "xg1990"
__copyright__ = "xg1990"
__license__ = "MIT"


def test_main():
    """CLI Tests"""
    runner = CliRunner()
    result = runner.invoke(main)
    assert result.exit_code == 0
    assert result.output == ""


def test_load_config():
    fpath = os.path.join(os.path.dirname(__file__), 'test_config.yml')
    config = load_config(fpath)
    assert isinstance(config, dict)
