import json
import boto3
import botocore
import requests
import datetime
import base64
import logging

limit = 1000
fields_list = ['owner','sku','is_active','period_end_time','period_start_time','is_trial','cancellation_time']
fields = ','.join(fields_list)
headers = {}
url = 'https://graph.oculus.com/application/subscriptions'
logging.basicConfig(filename='test.log',level=logging.DEBUG)

def get_secret():

    secret_name = "qa/oculus/subscription/api/token"
    region_name = "eu-west-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    secret = get_secret_value_response['SecretString']

    return secret

def write_to_s3(item,year,month,day,time):
    new_data_item = []
    data_list = item[0]["data"]
    for data_item in data_list:
        new_data_item.append(data_item)
    s3 = boto3.client("s3")
    s3.put_object(Bucket="qa-oculus-subscription",Key=f"{year}/{month}/{day}/subscriber_{time}.json",Body=json.dumps(new_data_item))

api_token = eval(get_secret())['api_token']
params = {"access_token":api_token, "fields":fields,"limit":limit}
def get_subscribers(urls = url, header = headers, param = params):
    now = datetime.datetime.now()
    n = 0
    while True:
        try:
            current_time = datetime.datetime.now().strftime("%m-%d-%Y_ %H-%M-%S")
            current_year = datetime.datetime.now().strftime("%Y")
            current_month = datetime.datetime.now().strftime("%m")
            current_day = datetime.datetime.now().strftime("%d")
            subscribers = []
            response = requests.get(urls, headers=header, params=param)
            if response.status_code == 200:
                response_json = response.json()
                subscribers.append(response_json)
#                write_to_s3(subscribers,current_year,current_month,current_day,current_time)
                paging_dict = response_json["paging"]
                if "next" in paging_dict:
                    urls = paging_dict["next"]
                    n += 1
                    print (n)
                else:
                    end_time = datetime.datetime.now()
                    print('process duration:',end_time - now)
                    break
            else:
                print(response.status_code)
                logging.error(f"Response status code is not 200: {response.status_code}")
                logging.error(f"error reason:{response.reason}")
                print(response.raise_for_status())
                break
        except requests.Timeout as timeout_exception:
            logging.error(f"The connection has timed out: {timeout_exception}")
        except requests.HTTPError as http_error:
            logging.error(f"The server returned an error: {http_error}")
        except requests.ConnectionError as connection_error:
            logging.error(f"Encountered a connection error: {connection_error}")
    return subscribers

#if __name__ == '__main__':
#    get_subscribers()
