#!/usr/bin/env python

import logging
from botocore.vendored import requests
import boto3

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def handler(event, context):
    print(event)
