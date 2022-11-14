import os

from dnt.cli.main import main, validate
from click.testing import CliRunner


def test_validate(test_config):
    """CLI Tests"""
    runner = CliRunner()
    result = runner.invoke(validate, obj={'config': test_config})
    assert result.exit_code == 0
    assert result.output.startswith("test command")

def test_validate_from_main(test_config_fn):
    """CLI Tests"""
    runner = CliRunner()
    result = runner.invoke(main, ['-c', test_config_fn, 'validate'])
    assert result.exit_code == 0
    assert result.output.startswith("Invoking validate")
