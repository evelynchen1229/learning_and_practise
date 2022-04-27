import pandas as pd
import numpy as np
import datetime
from datetime import date
import os
import sys
# directory of raw data


today = date.today().strftime('%d_%m_%y')
financials = pd.read_excel(sys.path[0] + f'\\Raw Data\\raw_plutus_financial_base_{today}.xlsx')
#financials = pd.read_excel(r'./Raw Data/raw_plutus_financial_base_04_11_21.xlsx')

financials = (financials.assign(final_cust = lambda x: np.where(x['REAL_CUSTOMER'].isnull(),x['CUSTOMER'],x['REAL_CUSTOMER'])
                                    )
                   .assign(final_seg = lambda x: np.where((x['REAL_CUSTOMER'].isnull()) | (x['REAL_SEGMENT'] == 'Unspecified'),x['SEGMENT'],x['REAL_SEGMENT'])
                                    )
                   .assign(final_law_cust_status= lambda x: np.where(x['REAL_CUSTOMER'].isnull(),x['LAW_CUSTOMER_STATUS'],x['REAL_CUST_STATUS'])
                                    )
                  
                   .rename(columns = {'CUSTOMER':'PLU_CUSTOMER','SEGMENT':'PLU_SEGMENT','final_cust':'CUSTOMER','final_seg':'SEGMENT','LAW_CUSTOMER_STATUS':'PLU_LAW_CUSTOMER_STATUS','final_law_cust_status':'LAW_CUSTOMER_STATUS'})
                   .drop(columns = ['REAL_CUSTOMER','PLU_CUSTOMER','PLU_SEGMENT','REAL_CUST_STATUS','REAL_CUST_STATUS','PLU_LAW_CUSTOMER_STATUS','REAL_SEGMENT'])
)
# no need for NEXIS_FLG
cols = ['CUSTOMER'
        #,'FINANCIAL_CUSTOMER'
        ,'CUSTNAME', 'CUSTOMER_STATUS','LAW_CUSTOMER_STATUS','SEGMENT', 'ACCOUNT_STATUS', 'ACCOUNT',
       'ACCOUNTNAME', 'TEAM', 'REPCODE', 'FULLNAME',  'CITY',
       'POSTCODE', 'REGION', 'COUNTRY', 'LBU_SUBSCR', 'LBU_CAE_VAL',
       'CUST_ON_RENEWALFLG', 'LBU_ON_RENEWALFLG', 'LBU_MYD_FLG',
       'LBUMAXRENEWDATE', 'CUSTMAXRENEWDATE', 'LBU_CY_ON_AMT', 'LBU_CY_PR_AMT',
       'LBU_CY_OA_AMT', 'LBU_PY_ON_AMT', 'LBU_PY_PR_AMT', 'LBU_PY_OA_AMT',
       'YRPER' ]

financials_column_clean = financials[cols]

financials_column_clean.to_excel(sys.path[0] + f'\\Raw Data\\raw_financials_column_clean_{today}.xlsx',index=False)

