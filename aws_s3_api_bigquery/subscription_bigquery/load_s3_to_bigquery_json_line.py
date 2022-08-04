import json
import jsonlines
import boto3
import botocore
import datetime
import base64
import os
from google.cloud import bigquery
import pytz

def load_s3_to_bigquery():

    # get process duration
    start = datetime.datetime.now()
    
    # get s3 file prefix 
    today = datetime.datetime.today()
    prefix = today.strftime('%Y/%m/%d') + '/subscriber'
    
    # connect to s3 bucket
    s3_client = boto3.client("s3")
    s3_bucket_name = 'qa-oculus-subscription'
    s3 =  boto3.resource("s3")
    my_bucket=s3.Bucket(s3_bucket_name)
    
    # connect to bigquery
    client = bigquery.Client()
    table_id = 'analytics-dev-356310.staging.stg_subscription'
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    job_config.autodetect = True

    # read each json file in the latest folder in the s3 bucket
    for file in my_bucket.objects.filter(Prefix = prefix):
        file_name=file.key
        # skip any existing jsonl files
        if file_name.find('.jsonl') == -1:
            print(file_name)
            # extract path name
            pathname, extension = os.path.splitext(file_name)
            new_file_name = f'{pathname}.jsonl'
    
            # convert json file to jsonl file
            # upload jsonl file to the s3 bucket
            obj = s3.Object(s3_bucket_name,file_name)
            data=obj.get()['Body'].read()
            json_data = json.loads(data)
            with jsonlines.open('subs.jsonl','w') as writer:
                writer.write_all(json_data)
            s3.Bucket(s3_bucket_name).upload_file('subs.jsonl',new_file_name)
            # load the jsonl file to bigquery
            with open('subs.jsonl','rb') as source_file:
                job = client.load_table_from_file(
                    source_file,
                    table_id,
                    job_config = job_config
                )
            job.result()

    # get process duration
    end = datetime.datetime.now()
    return end - start
