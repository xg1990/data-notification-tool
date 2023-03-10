import logging
import sys
from turtle import pd

import click
import yaml

from dnt import __version__
from dnt.core.config import Config
from dnt.core.runner import Runner

__author__ = "xg1990"
__copyright__ = "xg1990"
__license__ = "MIT"

_logger: logging.Logger = logging.getLogger(__name__)


def setup_logging(loglevel: int) -> None:
    """
    Setup basic logging.

    Args:
        loglevel (int): minimum loglevel for emitting messages
    
    Returns:
        None
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


@click.group(invoke_without_command=True)
@click.option("-c", "--config", required=True, type=click.Path(exists=True))
@click.pass_context
def main(ctx, config) -> None:
    ctx.ensure_object(dict)
    ctx.obj["config"] = Config(config)
    # _logger.debug("Starting crazy calculations...")
    # _logger.info("Script ends here")
    if ctx.invoked_subcommand is None:
        click.echo(main.get_help(ctx))
    else:
        click.echo(f"Invoking {ctx.invoked_subcommand}")


@main.command()
@click.pass_context
def validate(ctx) -> None:
    """
    Validate config file.
    """
    config: Config = ctx.obj["config"]
    click.echo("Validating...")
    print("Config file is good to go:", config.validate())


@main.command()
@click.pass_context
@click.argument("jobs", nargs=-1)
def run(ctx, jobs) -> None:
    """
    Run jobs.
    """
    config: Config = ctx.obj["config"]
    runner: Runner = Runner(config)
    click.echo("Running jobs...")
    runner.run_all(list(jobs))


if __name__ == "__main__":
    main()
