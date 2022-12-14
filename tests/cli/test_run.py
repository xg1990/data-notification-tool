import os

from dnt.cli.main import main, run, validate
from click.testing import CliRunner


def test_run(test_config, test_secret):
    """CLI Tests"""
    runner = CliRunner()
    result = runner.invoke(run, obj={"config": test_config})
    assert result.exit_code == 0
    assert result.output.startswith(
        "MESSAGE FROM DBT CONSOLE DUMMY SERVICE [test_action]"
    )
    assert f"test message from {test_secret}" in result.output
