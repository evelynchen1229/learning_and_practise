import pandas as pd
from datetime import date
import sys

# check published ACV period
from sqlalchemy.engine import create_engine
DIALECT = 'oracle'
SQL_DRIVER = 'cx_oracle'
USERNAME = 'DATAANALYTICS' 
PASSWORD = 'DatPwd123Z' 
HOST = 'PSDB3684.LEXIS-NEXIS.COM'
PORT = 1521
SERVICE = 'GBIPRD1.ISPPROD.LEXISNEXIS.COM'
ENGINE_PATH_WIN_AUTH = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD +'@' + HOST + ':' + str(PORT) + '/?service_name=' + SERVICE

engine = create_engine(ENGINE_PATH_WIN_AUTH)
conn_base=engine.connect()
query = '''
SELECT MAX(F.PER_WID) FROM LAW.F_FIN_ACV F INNER JOIN LAW.D_FIN_ACV D ON D.ROW_WID = F.ROW_WID WHERE D.STATUS = 'PUBLISHED' AND D.SUBDOMAIN_NAME = 'ACV'
'''
df_period = pd.read_sql(query, con=conn_base)
conn_base.close()
latest_acv_period = df_period.iloc[0].to_list()[0]

today = date.today().strftime('%Y%m')

# if the current month is January,expected reporting period would be December of last year
if today[-2:] == '01': 
    reporing_period = int(str(date.today().year - 1) + '12')
else:
    reporting_period = int(today) - 1

print('Reporting period:',reporting_period)

proceed = True

# if the current month is January, should double check with Sarah and Jacqui for any updated high growth and csm to am file they'd like us to use
# also, remember to use the latest exchange rate 
if today[-2:] == '01':
    print('Please remeber to update the exchange rate when it is ready for the Premium News spend.')
    high_growth_file = input('Have you got any latest high growth file from Sarah? Yes / No\n')
    csm_to_am = input('Have you checked with Jacqui regarding to any csm to am mapping she would like us to use? Yes / No\n')
    if high_growth_file not in ['Yes','yes','y','Y']:
        print('Please check with Sarah for high growth file first.')
        proceed = False
    elif csm_to_am not in ['Yes','yes','y','Y']:
        print('Please check with Jacqui for any potential cm to am mapping first just in case. If there is any new file, please make sure you have AM repcode and CSM Login ready for the report.')
        proceed = False
else:
    pass

if proceed == True and latest_acv_period == reporting_period:  
    print('Please remember to verify Nexis customer mapping with Deb once the latest GCRM report is ready.')  
    pn_checking = input('Have you checked Premium News? Yes / No\n')
    fx_update = input('Is the latest exchange rate being used? Yes / No\n')
    if pn_checking not in ['Yes','yes','y','Y']:
        print('Premium News data is not ready yet. Please prepare Premiums News first.')
    elif fx_update not in ['Yes','yes','y','Y']:
        print('Please use the latest foreign exchange rate.')
    else:
        import CS_GET_DATA    
        # check 1: whether there's duplication in the financial data - expect to see 1 - no duplication for accounts 
        cs_data = sys.path[0] + '\\CS BASE DATA.xlsx'
        df_base = pd.read_excel(cs_data)
        acct_dup_test = (df_base
            .groupby('ACCOUNT')['LBU_ON_SPEND'].count()
            .reset_index())['LBU_ON_SPEND'].max()
        acct_dup_test = 1
        print('No duplication in the financial base:',acct_dup_test == 1)
        
        if acct_dup_test == 1:
            import CS_Premium_News
            # check 3: whether all the tests have passed - account level spend equals to customer level spend after adding premium news     
            tests_checking = input('Have all the tests passed? Yes / No\n')
            if tests_checking in ['Yes','yes','y','Y']:
                import CS_Priority_Bucket
              #  import CS_Comparison
                print('All done!')
            else:
                print('After adding Premium News spend, account level and customer level spend do not add up. Please investigate.')
        else:
            print('There is duplication in the financial base data. Please investigate.')

else:
    print(f'ACV is not ready. The latest ACV period is {latest_acv_period} while the reporting period needed is {reporting_period}.')
