import pandas as pd
import numpy as np
import datetime
from datetime import date
import os
import sys
# directory of raw data

today = date.today().strftime('%d_%m_%y')
#financials = pd.read_csv('Raw Data/Raw_Financial Base.csv')
#financials = pd.read_csv('./Raw Data/Raw_Financial_Base_plutus.csv')
financials = pd.read_excel(sys.path[0] + f'\\Raw Data\\raw_financials_column_clean_{today}.xlsx')

#credit = pd.read_csv('Raw Data/RAW_credit.csv')
credit = pd.read_excel(sys.path[0] + f'\\Raw Data\\raw_credit_{today}.xlsx')
#credit = pd.read_excel(r'./Raw Data/raw_credit_04_11_21.xlsx')

financial_cols = ['LBU_CY_ON_AMT','LBU_CY_OA_AMT','LBU_CY_PR_AMT','LBU_PY_ON_AMT','LBU_PY_OA_AMT','LBU_PY_PR_AMT','LBU_SUBSCR','LBU_CAE_VAL']

credit_cols = ['CREDIT_CY_ON','CREDIT_CY_OA','CREDIT_CY_PR','CREDIT_PY_ON','CREDIT_PY_OA','CREDIT_PY_PR','ACTIVE_SUBS_VALUE','CAE_SUBS_VALUE','ACCNT_LEGCY_ID']

new_cols = {'adj_lbu_cy_on_amt': financial_cols[0],
            'adj_lbu_cy_oa_amt': financial_cols[1],
            'adj_lbu_cy_pr_amt': financial_cols[2],
            'adj_lbu_py_on_amt': financial_cols[3],
            'adj_lbu_py_oa_amt': financial_cols[4],
            'adj_lbu_py_pr_amt': financial_cols[5],
            'adj_lbu_subscr': financial_cols[6],
            'adj_lbu_cae_val': financial_cols[7]}

financial_without_credit = (financials.merge(credit, how = 'left',left_on = 'ACCOUNT', right_on='ACCNT_LEGCY_ID')
        #.merge(cus_without_credit, how='left', left_on ='CUSTOMER', right_on ='CUSTOMER')

        # get adjusted lbu cy amount
        .assign(adj_lbu_cy_on_amt = lambda x: x[financial_cols[0]].fillna(0) - x[credit_cols[0]].fillna(0))
        .assign(adj_lbu_cy_oa_amt = lambda x: x[financial_cols[1]].fillna(0) - x[credit_cols[1]].fillna(0))
        .assign(adj_lbu_cy_pr_amt = lambda x: x[financial_cols[2]].fillna(0) - x[credit_cols[2]].fillna(0))

        # get adjusted lbu py amount
        .assign(adj_lbu_py_on_amt = lambda x: x[financial_cols[3]].fillna(0) - x[credit_cols[3]].fillna(0))
        .assign(adj_lbu_py_oa_amt = lambda x: x[financial_cols[4]].fillna(0) - x[credit_cols[4]].fillna(0))
        .assign(adj_lbu_py_pr_amt = lambda x: x[financial_cols[5]].fillna(0) - x[credit_cols[5]].fillna(0))

        # get adjusted lbu cae and active sub values
        .assign(adj_lbu_subscr = lambda x: x[financial_cols[6]].fillna(0) - x[credit_cols[6]].fillna(0))
        .assign(adj_lbu_cae_val = lambda x: x[financial_cols[7]].fillna(0) - x[credit_cols[7]].fillna(0))

         # get lbu total value for cy and py
        .assign(lbu_cy_tot = lambda x: x['adj_lbu_cy_on_amt'] + x['adj_lbu_cy_oa_amt'] + x['adj_lbu_cy_pr_amt'])
        .assign(lbu_py_tot = lambda x: x['adj_lbu_py_on_amt'] + x['adj_lbu_py_oa_amt'] + x['adj_lbu_py_pr_amt'])

        # get excldclosedacct flag
        .assign(excldclosedacct = lambda x: np.where((x['REPCODE'] == 'CL') & (x['lbu_py_tot'] == 0) & (x['lbu_cy_tot'] == 0),'Y','N'))

        # get cust level billing
        .assign(cust_subscr = lambda x: x.groupby('CUSTOMER').adj_lbu_subscr.transform('sum'))
        .assign(cust_cae_val = lambda x: x.groupby('CUSTOMER').adj_lbu_cae_val.transform('sum'))
        .assign(cust_cae_p = lambda x: x['cust_cae_val'] / x['cust_subscr'])

        .assign(cus_cy_on_amt = lambda x: x.groupby('CUSTOMER').adj_lbu_cy_on_amt.transform('sum'))
        .assign(cus_cy_oa_amt = lambda x: x.groupby('CUSTOMER').adj_lbu_cy_oa_amt.transform('sum'))
        .assign(cus_cy_pr_amt = lambda x: x.groupby('CUSTOMER').adj_lbu_cy_pr_amt.transform('sum'))
        .assign(cus_cy_tot = lambda x: x.groupby('CUSTOMER').lbu_cy_tot.transform('sum'))

        .assign(cus_py_on_amt = lambda x: x.groupby('CUSTOMER').adj_lbu_py_on_amt.transform('sum'))
        .assign(cus_py_oa_amt = lambda x: x.groupby('CUSTOMER').adj_lbu_py_oa_amt.transform('sum'))
        .assign(cus_py_pr_amt = lambda x: x.groupby('CUSTOMER').adj_lbu_py_pr_amt.transform('sum'))
        .assign(cus_py_tot = lambda x: x.groupby('CUSTOMER').lbu_py_tot.transform('sum'))

        .assign(cus_has_cy_online_spend = lambda x: np.where(x['cus_cy_on_amt'] > 0, 'Y', 'N'))
        .assign(cus_has_py_online_spend = lambda x: np.where(x['cus_py_on_amt'] > 0, 'Y', 'N'))

        # add unique id based on cust number and lbu number
        # Nov 21 addition: billing name and rep code
        .assign(unique_ID = lambda x: x['CUSTOMER'] + x['ACCOUNT'] + x['ACCOUNTNAME'] + x['REPCODE'])

        # drop orginal lbu spend and credit
        .drop(columns = financial_cols + credit_cols)
        .rename(columns = new_cols)

        )

# exclude closed accounts
financials = financial_without_credit[financial_without_credit['excldclosedacct'] == 'N']
financials.columns = map(str.upper, financials.columns)
# no need for nexis_flg column
cols = ['UNIQUE_ID','CUSTOMER', 'CUSTNAME', 'CUSTOMER_STATUS',
         'SEGMENT', 'ACCOUNTNAME',  'ACCOUNT','ACCOUNT_STATUS',
        'REPCODE','TEAM', 'FULLNAME', 'CITY', 'POSTCODE','REGION', 'COUNTRY',
        'LAW_CUSTOMER_STATUS', 
        'LBU_SUBSCR', 'LBU_CAE_VAL', 'CUST_SUBSCR', 'CUST_CAE_VAL', 'CUST_CAE_P',       
         'CUS_HAS_CY_ONLINE_SPEND', 'CUS_HAS_PY_ONLINE_SPEND',
        'CUST_ON_RENEWALFLG', 'LBU_ON_RENEWALFLG',
      'LBU_MYD_FLG', 'LBUMAXRENEWDATE', 'CUSTMAXRENEWDATE',
        'LBU_CY_ON_AMT', 'LBU_CY_PR_AMT','LBU_CY_OA_AMT', 'LBU_CY_TOT', 
        'CUS_CY_ON_AMT', 'CUS_CY_PR_AMT',       'CUS_CY_OA_AMT', 'CUS_CY_TOT',
        'LBU_PY_ON_AMT', 'LBU_PY_PR_AMT', 'LBU_PY_OA_AMT', 'LBU_PY_TOT',
        'CUS_PY_ON_AMT','CUS_PY_PR_AMT', 'CUS_PY_OA_AMT', 'CUS_PY_TOT',
        'YRPER', 'EXCLDCLOSEDACCT'
      #  'FINANCIAL_CUSTOMER'       
      ]
financials = financials[cols]

output = sys.path[0] + f'\\outputs\\financials_plutus_before_whitespace_{today}.xlsx'
financials.to_excel(output,index=False)


