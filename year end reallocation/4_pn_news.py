# fields needed: lbu_cy_oa_value,mlex value, l360 value, lbu_tot_cy, cus_oa_cy, cy_tot
import pandas as pd
import numpy as np
import os
import sys

import datetime
from datetime import date

today = date.today().strftime('%d_%m_%y')
l360=['L360','L360 PULSE','L360 - IP']

financials_before_pn = pd.read_excel(sys.path[0] + f'\\outputs\\financials_plutus_with_whitespace_{today}.xlsx')

pn_news =(pd.read_excel(sys.path[0] + '\\Lookup File\\Premium News - Renewals Tracker.xlsx')
       .rename(columns={'Billing acct to Map to in Allocation detail sheet':'ACCOUNT',
                           'iKnow Customer Account Number':'CUSTOMER'})
       .assign(mlex_gbp = lambda x: round(x['MLex Spend']/1.28,2))
       # Fran said to just use L360 Spend column for the toal amount
       .assign(l360_gbp = lambda x: round((x['L360 Spend'].fillna(0))/1.28,2))
#       .assign(l360_gbp = lambda x: round((x['L360 Billing frequency x '].fillna(0))/1.28,2))
)

df_mlex = pn_news.loc[pn_news['Type (mlex/L360)']=='Mlex'][['CUSTOMER','ACCOUNT','mlex_gbp']].groupby(['ACCOUNT','CUSTOMER'])['mlex_gbp'].sum().reset_index()

df_l360 = pn_news.loc[lambda x: x['Type (mlex/L360)'].isin(l360)][['CUSTOMER','ACCOUNT','l360_gbp']].groupby(['ACCOUNT','CUSTOMER'])['l360_gbp'].sum().reset_index()

df_mlex_cus = df_mlex.groupby('CUSTOMER')['mlex_gbp'].sum().reset_index()
df_l360_cus = df_l360.groupby('CUSTOMER')['l360_gbp'].sum().reset_index()

df_after_pn = (financials_before_pn.merge(df_mlex[['ACCOUNT','mlex_gbp']], how='left',on='ACCOUNT')
        .merge(df_l360[['ACCOUNT','l360_gbp']],how='left',on='ACCOUNT')
        .merge(df_mlex_cus,how='left',left_on='CUSTOMER', right_on = 'CUSTOMER')
        .merge(df_l360_cus,how='left',left_on='CUSTOMER', right_on = 'CUSTOMER') 
        .assign(adj_lbu_cy_oa=lambda x: x['LBU_CY_OA_AMT'].fillna(0) + x['mlex_gbp_x'].fillna(0) + x['l360_gbp_x'].fillna(0))
        .assign(adj_lbu_tot=lambda x: x['LBU_CY_TOT'].fillna(0) + x['mlex_gbp_x'].fillna(0) + x['l360_gbp_x'].fillna(0))
        .assign(adj_cus_oa = lambda x: x['mlex_gbp_y'].fillna(0)+x['l360_gbp_y'].fillna(0)+x['CUS_CY_OA_AMT'].fillna(0))
        .assign(adj_cus_tot = lambda x: x['mlex_gbp_y'].fillna(0)+x['l360_gbp_y'].fillna(0)+x['CUS_CY_TOT'].fillna(0))
        #.drop(columns = ['CUSTOMER_y','CUSTOMER'])
        .rename(columns = {'mlex_gbp_x':'LBU_MLEX_GBP','mlex_gbp_y':'CUS_MLEX_GBP','l360_gbp_x':'LBU_LAW360_GBP','l360_gbp_y':'CUS_LAW360_GBP',
            'LBU_CY_OA_AMT':'LAW_LBU_CY_OA_AMT','LBU_CY_TOT':'LAW_LBU_CY_TOT','CUS_CY_OA_AMT':'LAW_CUS_CY_OA_AMT',
            'CUS_CY_TOT':'LAW_CUS_CY_TOT',
            'adj_lbu_cy_oa':'LBU_CY_OA_AMT','adj_lbu_tot':'LBU_CY_TOT','adj_cus_oa':'CUS_CY_OA_AMT','adj_cus_tot':'CUS_CY_TOT'})
        .assign(LBU_Premium_News_Spend = lambda x: x['LBU_MLEX_GBP'].fillna(0) + x['LBU_LAW360_GBP'].fillna(0))
        .assign(CUS_Premium_News_Spend = lambda x: x['CUS_MLEX_GBP'].fillna(0) + x['CUS_LAW360_GBP'].fillna(0))
              )
col = ['UNIQUE_ID','CUSTOMER',  'CUSTNAME', 'CUSTOMER_STATUS',
       'SEGMENT', 'ACCOUNTNAME',  'ACCOUNT','ACCOUNT_STATUS',
       'REPCODE', 'TEAM', 'FULLNAME', 'CITY', 'POSTCODE',
       'REGION', 'COUNTRY', 'LAW_CUSTOMER_STATUS', 
       'LBU_SUBSCR', 'LBU_CAE_VAL', 'CUST_SUBSCR', 'CUST_CAE_VAL', 'CUST_CAE_P', 
       'CUS_HAS_CY_ONLINE_SPEND','CUS_HAS_PY_ONLINE_SPEND',
       'CUST_ON_RENEWALFLG', 'LBU_ON_RENEWALFLG',
       'LBU_MYD_FLG', 'LBUMAXRENEWDATE', 'CUSTMAXRENEWDATE',
        'LBU_CY_ON_AMT', 'LBU_CY_PR_AMT','LBU_CY_OA_AMT', 'LBU_CY_TOT',
       'CUS_CY_ON_AMT','CUS_CY_PR_AMT','CUS_CY_OA_AMT','CUS_CY_TOT',
       'LBU_PY_ON_AMT', 'LBU_PY_PR_AMT', 'LBU_PY_OA_AMT', 'LBU_PY_TOT',
       'CUS_PY_ON_AMT', 'CUS_PY_PR_AMT', 'CUS_PY_OA_AMT', 'CUS_PY_TOT',
       'YRPER','EXCLDCLOSEDACCT',
        #'FINANCIAL_CUSTOMER',
        'LAW_LBU_CY_OA_AMT', 'LBU_Premium_News_Spend','LBU_MLEX_GBP', 'LBU_LAW360_GBP','LAW_LBU_CY_TOT',
       'LAW_CUS_CY_OA_AMT', 'CUS_Premium_News_Spend','CUS_MLEX_GBP', 'CUS_LAW360_GBP','LAW_CUS_CY_TOT'    
       ]
df_after_pn = df_after_pn[col]

output = sys.path[0] + f'\\outputs\\financials_plutus_after_pn_{today}.xlsx'
df_after_pn.to_excel(output,index=False)
