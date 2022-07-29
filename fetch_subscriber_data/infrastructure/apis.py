import requests
import json
import logging
import botocore
import numpy as np
import datetime

logging.basicConfig(filename='test.log',level=logging.DEBUG)

SECRET = ''
CRED = ''


def get_subscriber_list():
    headers = {}
    # max limit 1525
    params = {"access_token":CRED, "fields":"owner,sku,is_active,period_end_time,period_start_time,is_trial,cancellation_time",'limit': 1000}
    subscribers = []
    url = 'https://graph.oculus.com/application/subscriptions'
    while True:
        try:
            response = requests.get(url, headers=headers, params=params)
            print(response.status_code)
            print(response.request.url)
            if response.status_code == 200:
                response_json = response.json()
                print(response_json)
                subscribers.append(response_json)
                paging_dict = response_json["paging"]
                if "next" in paging_dict:
                    url = paging_dict["next"]
                else:
                    break
            else:
                break;
            break
        except requests.Timeout as timeout_exception:
            logging.error(f"The connection has timed out: {timeout_exception}")
        except requests.HTTPError as http_error:
            logging.error(f"The server returned an error: {http_error}")
        except requests.ConnectionError as connection_error:
            logging.error(f"Encountered a connection error: {connection_error}")
    return subscribers
get_subscriber_list()
