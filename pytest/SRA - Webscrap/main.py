import json

from requests import api
from sra_api import ApiSra
from sra_webscrap import ScrapSRA


with open('config.json') as config_file:
    config_data = json.load(config_file)

api_url = config_data['api_details']['url']
api_subkey = config_data['api_details']['subkey']

api_call = ApiSra(api_url, api_subkey)

#api_call.call_api()
api_call.read_api_data_file()
api_call.api_data_to_database()

# print(api_call.df_api_data.head())

scrap = ScrapSRA()
scrap.fetch_sra_organisations()
scrap.download_sites()
scrap.close_database_connection()




