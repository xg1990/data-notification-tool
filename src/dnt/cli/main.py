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


def setup_logging(loglevel) -> None:
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


@click.group(invoke_without_command=True)
@click.option("-c", "--config", type=click.Path(exists=True))
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
    config: Config = ctx.obj
    click.echo("test command")
    print("config=", config)


@main.command()
@click.pass_context
def run(ctx) -> None:
    config: Config = ctx.obj['config']
    runner: Runner = Runner(config)
    runner.run_all()


if __name__ == "__main__":
    main()
