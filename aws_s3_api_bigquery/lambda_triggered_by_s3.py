import json
import datetime
import urllib
import boto3
import pandas as pd
from google.cloud import bigquery
import pytz

current_year = datetime.datetime.now().strftime("%Y")
current_month = datetime.datetime.now().strftime("%m")
current_day = datetime.datetime.now().strftime("%d")
today = datetime.date.today()
s3 = boto3.client("s3")

def lambda_handler(event, context):
    print(event)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding = "utf-8")
    try:
        response = s3.get_object(Bucket = bucket, Key = key)
        text = response['Body'].read().decode()
    except Exception as e:
        print(e)
        raise(e)ata = json.loads(text)
     # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
