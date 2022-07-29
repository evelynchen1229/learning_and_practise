import json
import boto3
import botocore
import requests
import datetime
import base64

current_time = datetime.datetime.now().strftime("%m-%d-%Y_ %H-%M-%S")
current_year = datetime.datetime.now().strftime("%Y")
current_month = datetime.datetime.now().strftime("%m")
current_day = datetime.datetime.now().strftime("%d")

def lambda_handler(event, context):
    SECRET = eval(get_secret())['secret']
    CRED = eval(get_secret())['cred']
    headers = {}
    params = {"access_token":CRED, "fields":"owner,sku,is_active,period_end_time,period_start_time,is_trial,cancellation_time","limit":1000}
    subscribers = []
    # default url sent to sqs
    #url = eval(event["Records"][0]["body"])['url']
    
    # for testing
    url = event['url']
    try:
        response = requests.get(url, headers=headers, params=params)
        print(response.status_code)
        print(response.request.url)
        if response.status_code == 200:
            response_json = response.json()
            print(response_json)
            subscribers.append(response_json)
            paging_dict = response_json["paging"]
            write_to_s3(subscribers)
            if "next" in paging_dict:
                next_url = paging_dict["next"]
                # send message to sqs
                # need real sqs queue
            #    client_sqs = boto3.client("sqs")
            #    response_sqs = client_sqs.send_message(
            #       
            #        QueueUrl = '',
            #        MessageBody = json.dumps({"url":next_url})
            #    )
            else:
                print("no next page",paging_dict)
    except requests.Timeout as timeout_exception:
        logging.error(f"The connection has timed out: {timeout_exception}")
    except requests.HTTPError as http_error:
        logging.error(f"The server returned an error: {http_error}")
    except requests.ConnectionError as connection_error:
        logging.error(f"Encountered a connection error: {connection_error}")
    return {'statusCode': 200,
        'body':json.dumps("one loop completed.")
    }

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

def fit_dictionary(item):
    new_dictionary = dict()
    new_dictionary["owner_Id"] = item["owner"]["id"]
    new_dictionary["sku"] = item["sku"]
    new_dictionary["is_active"] = item["is_active"]
    new_dictionary["is_trial"] = item["is_trial"]
    if 'period_end_time' in item:
        new_dictionary["period_end_time"] = item["period_end_time"]
    if 'period_start_time' in item:
        new_dictionary["period_start_time"] = item["period_start_time"]
    if 'cancellation_time' in item:
        new_dictionary["cancellation_time"] = item["cancellation_time"]
    new_dictionary["record_date"] =int(round(datetime.datetime.now().timestamp(), 0))
    return new_dictionary

def write_to_s3(item):
    new_data_item = []
    data_list = item[0]["data"]
    for data_item in data_list:
        #print(data_item)
        new_data_item.append(fit_dictionary(data_item))
        # load data to s3 bucket
    s3 = boto3.client("s3")
    s3.put_object(Bucket="qa-oculus-subscription",Key=f"{current_year}/{current_month}/{current_day}/subscriber_{current_time}.json",Body=json.dumps(new_data_item))
