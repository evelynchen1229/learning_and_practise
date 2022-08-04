from load_subscribers_to_s3 import get_subscribers
from load_s3_to_bigquery import load_s3_to_bigquery

if __name__ == '__main__':
    get_subscribers()
    load_s3_to_bigquery()
