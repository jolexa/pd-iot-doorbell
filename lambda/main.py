#!/usr/bin/env python

import os
import logging
from threading import Thread
import json

from botocore.vendored import requests
import boto3

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def find_pd_details():
    ssm = boto3.client('ssm')
    # Get all the parameters found in the path
    res = ssm.get_parameters_by_path(
        Path=os.environ.get('SSM_PATH', '/pd-iot-doorbell'),
        WithDecryption=True)

    parameters = res['Parameters']
    # No built in paginator
    while res.get('NextToken'):
        res = ssm.get_parameters_by_path(
            Path=os.environ.get('SSM_PATH', '/pd-iot-doorbell'),
            WithDecryption=True,
            NextToken=res.get('NextToken')
        )
        parameters.extend(res['Parameters'])

    for secret in parameters:
        os.environ[secret.get('Name').split('/')[-1]] = secret.get('Value')

def handler(event, context):
    logger.debug(event)
    secret_thread = Thread(target=find_pd_details)
    secret_thread.start()  # background

    # This is a demonstration of how you could extract the click type, SINGLE,
    # LONG, DOUBLE, to do different things. For this function, just do the same
    # thing for every clicktype
    logger.debug("The event was a '{}' click".format(event['clickType']))

    # Define the payload
    # https://v2.developer.pagerduty.com/v2/docs/send-an-event-events-api-v2
    pd_cef = {
        "event_action": "trigger",
        "payload": {
            "summary": "Someone is at the door!",
            "severity": "info",
            "source": "iotbutton",
            "custom_details" : {}
            }
        }
    pd_cef['payload']['custom_details']['batteryVoltage'] = event['batteryVoltage']
    pd_cef['payload']['custom_details']['clickType'] = event['clickType']

    secret_thread.join()
    pd_cef['routing_key'] = str(os.environ['service_key'])

    # Trigger an event
    #r = requests.post('https://events.pagerduty.com/generic/2010-04-15/create_event.json',
    r = requests.post('https://events.pagerduty.com/v2/enqueue',
            data=json.dumps(pd_cef))
    logger.debug(r.json())

if __name__== "__main__":
    event = {'serialNumber': '123456789', 'batteryVoltage': '1614mV', 'clickType': 'SINGLE'}
    context = {}
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-2'
    handler(event, context)
