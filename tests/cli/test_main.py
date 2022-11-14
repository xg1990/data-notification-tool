import os

from dnt.cli.main import main
from click.testing import CliRunner, Result

__author__ = "xg1990"
__copyright__ = "xg1990"
__license__ = "MIT"


def test_main(test_config_fn) -> None:
    """CLI Tests"""
    runner: CliRunner = CliRunner()
    result: Result = runner.invoke(main, ['--config', test_config_fn])
    assert result.exit_code == 0
    assert result.output.startswith("Usage: main [OPTIONS] COMMAND [ARGS]")

