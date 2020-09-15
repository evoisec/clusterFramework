import os
import sys

import importlib

import warnings
import logging
import click

# key boilerplate wiring
#CLI options/parameters
#Logging
#Error Handling - exceptions & assertions

logging.basicConfig(level=logging.WARN)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Constants
K_LEFT = 0
K_RIGHT = 1
K_UP = 2

DRIVERS = [
    'piradio.lcd.raspi_lcd',
    'piradio.lcd.fake_lcd',
    'piradio.lcd.web_lcd'
]

# _func_name, var_name

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


import json
import kfp
from kfp import components
from kfp import dsl
import os
import subprocess

diagnose_me_op = components.load_component_from_url(
    'https://raw.githubusercontent.com/kubeflow/pipelines/566dddfdfc0a6a725b6e50ea85e73d8d5578bbb9/components/diagnostics/diagnose_me/component.yaml')

confusion_matrix_op = components.load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/1.0.0/components/local/confusion_matrix/component.yaml')

roc_op = components.load_component_from_url('https://raw.githubusercontent.com/kubeflow/pipelines/1.0.0/components/local/roc/component.yaml')

dataproc_create_cluster_op = components.load_component_from_url(
    'https://raw.githubusercontent.com/kubeflow/pipelines/38771da09094640cd2786a4b5130b26ea140f864/components/gcp/dataproc/create_cluster/component.yaml')

dataproc_delete_cluster_op = components.load_component_from_url(
    'https://raw.githubusercontent.com/kubeflow/pipelines/38771da09094640cd2786a4b5130b26ea140f864/components/gcp/dataproc/delete_cluster/component.yaml')
