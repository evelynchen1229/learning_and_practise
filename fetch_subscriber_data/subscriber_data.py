from infrastructure.apis import get_subscriber_list
from infrastructure.config import NEW_ITEM
#import boto3
import datetime
import json
from json import JSONEncoder
from botocore.config import Config
import copy
import numpy as np

def format_dictionary(object_list):
    for item in object_list:
        data_list = item["data"]
        for data_item in data_list:
            new_data_item = fit_dictionary(data_item)

def fit_dictionary(item):
    new_dictionary = copy.deepcopy(NEW_ITEM)
    new_dictionary["owner_Id"] = item["owner"]["id"]
    new_dictionary["SKU"] = item["sku"]
    new_dictionary["is_active"] = item["is_active"]
    new_dictionary["is_trial"] = item["is_trial"]
    if 'period_end_time' in item:
        new_dictionary["periodEndTime"] = item['period_end_time']
    if 'period_start_time' in item:
        new_dictionary["periodStartTime"] = item["period_start_time"]
    if 'cancellation_time' in item:
        new_dictionary["cancellationTime"] = item["cancellation_time"]
    new_dictionary["record_date"] = int(np.round(datetime.datetime.now().timestamp(), 0))
    print(new_dictionary)
    return new_dictionary


if __name__ == '__main__':
    subscriber_list = get_subscriber_list()
    format_dictionary(subscriber_list)

