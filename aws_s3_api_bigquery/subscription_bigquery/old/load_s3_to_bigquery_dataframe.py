import json
import jsonlines
import boto3
import botocore
import datetime
import base64
import os
from google.cloud import bigquery
import pytz
import pandas as pd

def load_s3_to_bigquery():

    # get process duration
    start = datetime.datetime.now()
    
    # get s3 file prefix 
    today = datetime.datetime.today()
#    prefix = today.strftime('%Y/%m/%d') + '/subscriber'
    prefix = '2022/07/28/subscriber'
    
    # connect to s3 bucket
    s3_client = boto3.client("s3")
    s3_bucket_name = 'qa-oculus-subscription'
    s3 =  boto3.resource("s3")
    my_bucket=s3.Bucket(s3_bucket_name)
    
    # connect to bigquery
    client = bigquery.Client()
    table_id = 'regal-muse-354710.staging.stg_subscription'
    job_config = bigquery.LoadJobConfig(
        # Optionally, set the write disposition. BigQuery appends loaded rows
        # to an existing table by default, but with WRITE_TRUNCATE write
        # disposition it replaces the table with the loaded data.
        schema=[
            bigquery.SchemaField("owner_id", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("sku", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("is_active", "BOOLEAN", mode="NULLABLE"),
            bigquery.SchemaField("period_start_time", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("period_end_time", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("cancellation_time", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("is_trial", "BOOLEAN", mode="NULLABLE"),
            bigquery.SchemaField("recorded_date", "DATE", mode="NULLABLE"),
        ]
    )

    # read each json file in the latest folder in the s3 bucket
    for file in my_bucket.objects.filter(Prefix = prefix):
        file_name=file.key
        new_key = []
        new_value = []
        record = []
        # skip any existing jsonl files
        if file_name.find('.jsonl') == -1:
            print(file_name)
            # extract path name
            obj = s3.Object(s3_bucket_name,file_name)
            data=obj.get()['Body'].read()
            json_data = json.loads(data)
            for d in json_data:
                d_value = list(d.values())
                d_value[0] = int(d_value[0]['id'])
                d_value.append(today)

                d_key = list(d.keys())
                d_key[0] = 'owner_id'
                d_key.append('recorded_date')

                subs_dict = dict(zip(d_key, d_value))

                for key in subs_dict.keys():
                    if 'time' in key:
                        subs_dict[key] = pd.to_datetime(subs_dict[key])
                if 'period_start_time' not in subs_dict.keys():
                    subs_dict['period_start_time'] = pd.NaT
                elif 'period_end_time' not in subs_dict.keys():
                    subs_dict['period_end_time'] = pd.NaT
                elif 'cancellation_time' not in subs_dict.keys():
                    subs_dict['cancellation_time'] = pd.NaT
                else:
                    pass
                record.append(subs_dict)

        dataframe = pd.DataFrame(
            record,
            # In the loaded table, the column order reflects the order of the
            # columns in the DataFrame.
            columns=[
                "owner_id",
                "sku",
                "is_active",
                "period_start_time",
                "period_end_time",
                "cancellation_time",
                "is_trial",
                "recorded_date",
            ],
        )
        job = client.load_table_from_dataframe(
            dataframe, table_id, job_config = job_config
        )
        job.result()

    # get process duration
    end = datetime.datetime.now()
    return end - start

if __name__ == '__main__':
    load_s3_to_bigquery()
