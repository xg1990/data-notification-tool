import yaml
import click
import logging
import sys

from dnt import __version__

__author__ = "xg1990"
__copyright__ = "xg1990"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def load_config(fpath: str) -> dict:
    with open(fpath) as fp:
        config = yaml.safe_load(fp)
    return config


@click.command()
def main():
    _logger.debug("Starting crazy calculations...")
    _logger.info("Script ends here")


if __name__ == "__main__":
    main()
