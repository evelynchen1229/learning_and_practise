import json
import jsonlines
from google.cloud import bigquery
import pytz
import pandas as pd
import datetime

#client = bigquery.Client()
#table_id = 'regal-muse-354710.staging.stg_subscription'
#file_name = 'subscriber.json'
#job_config = bigquery.LoadJobConfig()
#    # Optionally, set the write disposition. BigQuery appends loaded rows
#    # to an existing table by default, but with WRITE_TRUNCATE write
#    # disposition it replaces the table with the loaded data.
#    write_disposition="WRITE_TRUNCATE",
#)
#job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
#job_config.autodetect = True
#
#with open(f'{file_name}','r+') as f:
#    data = json.load(f)
#
#with jsonlines.open('subscriber.jsonl','w') as writer:
#    writer.write_all(data)
#with open('subscriber.jsonl','rb') as source_file:
#    job = client.load_table_from_file(
#        source_file,
#        table_id,
#        job_config = job_config
#    )
#
#job.result()
#

file_name = 'subscriber.json'
new_key = []
new_value = []
record = []
today = datetime.date.today()
print(today)

with open(f'{file_name}','r+') as f:
    data = json.load(f)
    for d in data:
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


client = bigquery.Client()
table_id = 'regal-muse-354710.staging.stg_subscription'
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

job = client.load_table_from_dataframe(
    dataframe, table_id, job_config=job_config
)  # Make an API request.
job.result()  # Wait for the job to complete.

