import os

from click.testing import CliRunner, Result

from dnt.cli.main import main

__author__ = "xg1990"
__copyright__ = "xg1990"
__license__ = "MIT"


def test_main(test_config_fn) -> None:
    """CLI Tests"""
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(main, ["--config", test_config_fn])
    assert result.exit_code == 0
    assert result.output.startswith("Usage: main [OPTIONS] COMMAND [ARGS]")


def test_main_without_config() -> None:
    """CLI Tests"""
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(main)
    assert result.exit_code == 2
    assert result.output.startswith("Usage: main [OPTIONS] COMMAND [ARGS]")
