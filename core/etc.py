import os
import sys

import importlib

import warnings
import logging
import click

logging.basicConfig(level=logging.WARN)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


K_LEFT = 0
K_RIGHT = 1
K_UP = 2

DRIVERS = [
    'piradio.lcd.raspi_lcd',
    'piradio.lcd.fake_lcd',
    'piradio.lcd.web_lcd'
]

@click.command()
@click.option("--als-max-iter", default=10, type=int)
@click.option("--keras-hidden-units", default=20, type=int)
@click.option("--max-row-limit", default=100000, type=int)
def workflow(als_max_iter, keras_hidden_units, max_row_limit):

if __name__ == "__main__":
    warnings.filterwarnings("ignore")

    try:
        _DRIVERS.append(importlib.import_module(drv))
        logging.info('Loaded LCD driver %s', drv)
    except OSError:
        logging.warning('Failed to load LCD driver %s', drv)