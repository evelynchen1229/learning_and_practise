import pandas as pd
import datetime
from datetime import date
import os
import sys


today = date.today().strftime('%d_%m_%y')
current_per = input('Current Year Period YYYYMM:')

fin = pd.read_excel(sys.path[0] + f'\\outputs\\financials_plutus_before_whitespace_{today}.xlsx')
terr = pd.read_excel(sys.path[0] + f'\\Lookup File\\Territory Extract.xlsx')

whitespace_prep = terr[['Customer Account Id','Customer Name','Status','Secondary Sub Class','Billing Name','Billing Legacy','Billing Status', 'Bill Repcode', 'Team', 'First Name', 'Last Name','CITY', 'ZIPCODE', 'COUNTRY','Reporting Region']]  

whitespace_prep_final = whitespace_prep.copy()
whitespace_prep_final['Billing Legacy'] = whitespace_prep_final['Billing Legacy'].astype('str')

fin_copy = fin[['CUSTOMER','ACCOUNT','ACCOUNTNAME']]

whitespace = (whitespace_prep_final.merge(fin_copy,how='left',left_on='Billing Legacy', right_on='ACCOUNT')
               .merge(fin_copy,how='left',left_on='Customer Account Id', right_on='CUSTOMER')
 .assign(null_account = lambda x: x['ACCOUNT_x'].isnull())
 .assign(null_customer = lambda x: x['CUSTOMER_y'].isnull())
 .assign(FULLNAME = lambda x: x['First Name'] + ' ' + x['Last Name'])
 .assign(UNIQUE_ID = lambda x: x['Customer Account Id'].astype('str') + x['Billing Legacy'].astype('str') + x['Billing Name'].astype('str') + x['Bill Repcode'].astype('str'))
                      )
                      
whitespace = (whitespace[(whitespace['null_account']== True) & (whitespace['null_customer']== True)
    & (~whitespace['Bill Repcode'].isin (['--','AMZZ','MIAA','MIAC'])) 
    & (~whitespace['Team'].isin(['Academic','MI-RK','MI-ES','Jordans','Miscellaneous','MK-MI','MLEX','MK-M1']))
#    & (~whitespace['Secondary Sub Class'].isin(['External Test'])) 
    & ((~whitespace['Team'].isin(['MI-MI'])) | (whitespace['Bill Repcode'].isin(['BDFW'])))  
    & (~whitespace['FULLNAME'].isin(['M LEX','Team RepCode','MLEX Account'])) # add MLEX Account assuming M LEX is trying to remove mlex account
    ]
               .drop(columns = ['CUSTOMER_x','ACCOUNT_x','ACCOUNTNAME_x','CUSTOMER_y','ACCOUNT_y','ACCOUNTNAME_y','First Name', 'Last Name','null_account', 'null_customer'])
               .drop_duplicates()
               .rename(columns = {'Customer Account Id':'CUSTOMER', 'Customer Name':'CUSTNAME', 'Status':'CUSTOMER_STATUS', 'Secondary Sub Class':'SEGMENT',
       'Billing Name':'ACCOUNTNAME', 'Billing Legacy':'ACCOUNT', 'Billing Status':'ACCOUNT_STATUS', 'Bill Repcode':'REPCODE',
       'Team':'TEAM', 'ZIPCODE':'POSTCODE', 'Reporting Region':'REGION'})
              )
whitespace[['LAW_CUSTOMER_STATUS','LBUMAXRENEWDATE','CUSTMAXRENEWDATE']] = None

whitespace[['LBU_SUBSCR','LBU_CAE_VAL','CUST_SUBSCR','CUST_CAE_VAL','CUST_CAE_P','LBU_CY_ON_AMT','LBU_CY_PR_AMT','LBU_CY_OA_AMT','LBU_CY_TOT','CUS_CY_ON_AMT','CUS_CY_PR_AMT','CUS_CY_OA_AMT','CUS_CY_TOT','LBU_PY_ON_AMT','LBU_PY_PR_AMT','LBU_PY_OA_AMT','LBU_PY_TOT','CUS_PY_ON_AMT','CUS_PY_PR_AMT','CUS_PY_OA_AMT','CUS_PY_TOT']]=0

whitespace[['CUS_HAS_CY_ONLINE_SPEND','CUS_HAS_PY_ONLINE_SPEND','CUST_ON_RENEWALFLG','LBU_ON_RENEWALFLG','LBU_MYD_FLG','EXCLDCLOSEDACCT']] = 'N'

whitespace['YRPER'] = current_per

cols = fin.columns
whitespace = whitespace[cols]
output = sys.path[0] + f'\\outputs\\whitespace_{today}.xlsx'
whitespace.to_excel(output,index=False)

financials = pd.concat([fin,whitespace])

financials.to_excel(sys.path[0] + f'\\outputs\\financials_plutus_with_whitespace_{today}.xlsx', index=False)
