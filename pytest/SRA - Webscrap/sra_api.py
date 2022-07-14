import requests
import json
import pandas as pd
import cx_Oracle
import re
import time

class ApiSra:
    '''This class calls the SRA API'''

    def __init__(self, url, subkey):
        '''Add something useful'''
        self.url = url
        self.subkey = subkey
        self.api_data = ''
        self.df_api_data = ''
        self.target_connection = ''

    def call_api(self):
        '''Add something useful'''
        self.api_data = requests.get(self.url, headers={'Ocp-Apim-Subscription-Key': self.subkey}).json()
        self._save_api_data()

    def _save_api_data(self):
        '''Add something useful'''
        with open('api_data.json','w') as f:
            json.dump(self.api_data, f)
    
    def read_api_data_file(self):
        '''Add something useful'''
        with open('api_data.json','r') as f:
            self.api_data = json.load(f)

    def api_data_to_database(self):
        '''Add something useful'''
        # self.df_api_data = pd.read_json('api_data.json')
        self.df_api_data = pd.json_normalize(self.api_data, record_path=['Organisations'])
        self.df_api_data['Websites'] = self.df_api_data['Websites'].apply(lambda x: self._unpack(x))
        self.df_api_data['TradingNames'] = self.df_api_data['TradingNames'].apply(lambda x: self._unpack(x))
        self.df_api_data['PreviousNames'] = self.df_api_data['PreviousNames'].apply(lambda x: self._unpack(x))
        self.df_api_data['WorkArea'] = self.df_api_data['WorkArea'].apply(lambda x: self._unpack(x))

        # self.df_api_data['AuthorisationDate'] = self.df_api_data['AuthorisationDate'].apply(self.epoch_convert)
        # self.df_api_data['AuthorisationStatusDate'] = self.df_api_data['AuthorisationStatusDate'].apply(self.epoch_convert)
        #self.df_api_data['AuthorisationDate'] = pd.to_datetime(self.df_api_data['AuthorisationDate'])

        # self.df_api_data['AuthorisationDate'] = pd.to_datetime(self.df_api_data['AuthorisationDate'])
        # self.df_api_data['AuthorisationDate'] = self.df_api_data['AuthorisationDate'].apply(lambda x: x.strftime("%d-%b-%y"))
        

        self.df_api_data['AuthorisationDate'] = pd.to_datetime(self.df_api_data['AuthorisationDate'], errors='coerce').dt.strftime('%d-%b-%y')
        self.df_api_data['AuthorisationStatusDate'] = pd.to_datetime(self.df_api_data['AuthorisationStatusDate'], errors='coerce').dt.strftime('%d-%b-%y')


        self.df_api_data['Id'] = self.df_api_data['Id'].astype(int)
        self.df_api_data['SraNumber'] = self.df_api_data['SraNumber'].astype(int)
        self.df_api_data['NoOfOffices'] = self.df_api_data['NoOfOffices'].astype(int)

        self.df_api_data['PracticeName'] = self.df_api_data['PracticeName'].apply(lambda x: str(x).encode("ascii", "replace").decode("utf-8"))
        self.df_api_data['TradingNames'] = self.df_api_data['TradingNames'].apply(lambda x: str(x).encode("ascii", "replace").decode("utf-8"))
        self.df_api_data['PreviousNames'] = self.df_api_data['PreviousNames'].apply(lambda x: str(x).encode("ascii", "replace").decode("utf-8"))
        self.df_api_data['CompanyRegNo'] = self.df_api_data['CompanyRegNo'].apply(lambda x: str(x).encode("ascii", "replace").decode("utf-8"))
    

        print(self.df_api_data.info())



        self.df_api_data.to_csv('api_data.csv',encoding='utf-8',index=False)
        self.df_api_data = pd.read_csv('api_data.csv',encoding='utf-8')
        self.df_api_data.fillna('',inplace=True)



        # self.df_api_data.to_csv('test.csv')
        # insert_fields = '(ID, SRANUMBER, PRACTICENAME, AUTHORISATIONTYPE, AUTHORISATIONSTATUS, ORGANISATIONTYPE, AUTHORISATIONDATE, AUTHORISATIONSTATUSDATE, FREELANCEBASIS, REGULATOR, TRADINGNAMES, PREVIOUSNAMES, WORKAREA, WEBSITES, RESERVEDACTIVITES, COMPANYREGNO, CONSTITUTION, NOOFOFFICES, TYPE)'
        # insert_values = '(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19)'
        
        insert_fields = '(ID, SRANUMBER, PRACTICENAME, AUTHORISATIONTYPE, AUTHORISATIONSTATUS, ORGANISATIONTYPE, AUTHORISATIONDATE, AUTHORISATIONSTATUSDATE, FREELANCEBASIS, REGULATOR, TRADINGNAMES, PREVIOUSNAMES, WORKAREA, WEBSITES, RESERVEDACTIVITES, COMPANYREGNO, CONSTITUTION, NOOFOFFICES, TYPE)'
        insert_values = '(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19)'

        self.df_api_data.drop('Offices', axis=1, inplace=True)
        # rows_to_insert = list(map(tuple, self.df_api_data[['Id','SraNumber','PracticeName']].to_numpy(dtype=object)))

        rows_to_insert = list(map(tuple, self.df_api_data[['Id','SraNumber','PracticeName','AuthorisationType','AuthorisationStatus','OrganisationType','AuthorisationDate','AuthorisationStatusDate','FreelanceBasis','Regulator','TradingNames','PreviousNames','WorkArea','Websites','ReservedActivites','CompanyRegNo','Constitution','NoOfOffices','Type']].to_numpy(dtype=object)))
        

        # print(self.df_api_data[['Id','SraNumber']].to_numpy())
        # print(rows_to_insert)



        self._target_database_connection()

        cursor = self.target_connection.cursor()
        full_load_flg = cursor.execute("select full_load from pdl.web_harvest_cntrl where module = 'SRA API'").fetchall()
        cursor.close()

        print(full_load_flg)

        if full_load_flg[0][0]=='Y':
            cursor = self.target_connection.cursor()
            # cursor.execute("truncate table pdl.sra_practice")
            cursor.execute("update pdl.sra_practice set sys_current_flg='N' where sys_current_flg='Y' or sys_current_flg is null")
            cursor.close()
            self.target_connection.commit()
            
            cursor = self.target_connection.cursor()
            cursor.executemany("insert into pdl.sra_practice" + insert_fields + " values " + insert_values
                ,rows_to_insert)
            cursor.close()
            self.target_connection.commit()

            cursor = self.target_connection.cursor()
            cursor.execute("update pdl.sra_practice set sys_current_flg='Y', sys_loaded_dt=sysdate where sys_current_flg is null")
            cursor.close()
            self.target_connection.commit()

            cursor = self.target_connection.cursor()
            cursor.execute("update pdl.web_harvest_cntrl set full_load='N', LST_FULL_LOAD_DT=sysdate where module = 'SRA API'")
            cursor.close()
            self.target_connection.commit()



        self.target_connection.close()



    def _target_database_connection(self):
        '''Add something useful'''
        with open('config.json') as f:
            config_data = json.load(f)
        
        target_username = config_data['target_connection']['username']
        target_password = config_data['target_connection']['password']
        target_host = config_data['target_connection']['host']

        self.target_connection = cx_Oracle.connect(target_username, target_password, target_host)

    def _unpack(self, x):
        '''Add something useful'''
        try:
            iter(x)
        except TypeError:
            return ''
        else:
            return ' | '.join(x)
    
    def epoch_convert(self, epoc_date):
        try:
            print(epoc_date)
            epoc_date = re.findall('[0-9]+(?=-)', epoc_date)
            print(epoc_date)
            # return_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(epoc_date[0][:10])))
            return_date = time.strftime('%d-%b-%y', time.localtime(int(epoc_date[0][:10])))
            print(return_date)

        except Exception:
            # return_date = '1900-01-01 00:00:00'
            return_date = '01-Jan-50'
        finally:
            return return_date



        










