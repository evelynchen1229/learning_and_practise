import pandas as pd
import numpy as np
import os
import sys
import openpyxl
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.styles import Color, Fill
from openpyxl.cell import Cell  
import datetime as dt
from datetime import date

'''get data frames ready for comparison'''
curr_mth = int(date.today().strftime('%m'))
pre_mth = dt.datetime.strptime(str(curr_mth-1),'%m').strftime('%B')
curr_yr = date.today().strftime('%Y')
main_folder = r'\\Galileo\Public\Legal Intelligence\Customer Segmentation\BA\CS Allocation Reports'
current_month = sys.path[0] + '\\CS PRIORITY DATA.xlsx'
previous_month = main_folder + f'\\{pre_mth} {curr_yr}\\CS PRIORITY DATA.xlsx'

cols = ['CUSTOMER','CUSTNAME','ACCOUNT','ACCOUNTNAME','FULLNAME','REPCODE','TEAM','CSTEAM','ADJUSTED CS ALLOCATION','CSLOGIN','ADJUSTED CSLOGIN ALLOCATION','CSNAME','ADJUSTED CSNAME ALLOCATION','BP_>£5K','BP_£3-5K','BP_IH','BP_OTHER','BP_ACCT','ACCT_RISK_DRIVER','ACCT_HIGH_GROWTH_DRIVER','ACCT_STRATEGIC_DRIVER','ACCT_NEW_BIZ_DRIVER','ACCT_SPENDING_DRIVER','ACCT_PN_DRIVER','ACCNT_PRIORITY','CUS_SPENDING_DRIVER','CUS_PRIORITY']
final_cols = ['CUSTOMER_PREV','CUSTNAME_PREV','ACCOUNT','ACCOUNTNAME_PREV','FULLNAME_PREV','REPCODE_PREV','TEAM_PREV','CSTEAM_PREV','ADJUSTED CS ALLOCATION_PREV','CSLOGIN_PREV','ADJUSTED CSLOGIN ALLOCATION_PREV','CSNAME_PREV','ADJUSTED CSNAME ALLOCATION_PREV','CUSTOMER_CURR','CUSTNAME_CURR','ACCOUNTNAME_CURR','FULLNAME_CURR','REPCODE_CURR','TEAM_CURR','CSTEAM_CURR','ADJUSTED CS ALLOCATION_CURR','CSLOGIN_CURR','ADJUSTED CSLOGIN ALLOCATION_CURR','CSNAME_CURR','ADJUSTED CSNAME ALLOCATION_CURR','BP_OVER_5K_MOVEMENT','BP_3_5K_MOVEMENT','BP_IH_MOVEMENT','BP_OTHER_MOVEMENT','BP_ACCT_MOVEMENT','ACCNT_RISK_DRIVER_MOVEMENT','ACCNT_HIGH_GROWTH_DRIVER_MOVEMENT','ACCNT_STRATEGIC_DRIVER_MOVEMENT','ACCNT_NEW_BIZ_DRIVER_MOVEMENT','ACCNT_SPENDING_DRIVER_MOVEMENT','ACCNT_PN_DRIVER_MOVEMENT','ACCNT_OVERALL_PRIORITY_MOVEMENT','ACCNT_DROP_OUT_OF_THE_REPORT_AS_A_WHOLE','CUS_SPENDING_DRIVER_MOVEMENT','CUS_OVERALL_PRIORITY_MOVEMENT']
cs_current = pd.read_excel(current_month,sheet_name='Report')[cols]
cs_previous = pd.read_excel(previous_month,sheet_name = 'Report')[cols]

def spend_movement(x,level='account'):
    if level == 'account':
        if x['ACCT_SPENDING_DRIVER_prev'] == 'High':
            if x['ACCT_SPENDING_DRIVER_curr'] == 'Medium':
                return 'Moved from High to Medium'
            return 'Moved from High to Low'
        elif x['ACCT_SPENDING_DRIVER_prev'] == 'Medium':
            if x['ACCT_SPENDING_DRIVER_curr'] == 'High':
                return 'Moved from Medium to High'
            return 'Moved from Medium to Low'
        else:
            if x['ACCT_SPENDING_DRIVER_curr'] == 'High':
                return 'Moved from Low to High'
            return 'Moved from Low to Medium'
    elif level == 'customer':
        if x['CUS_SPENDING_DRIVER_prev'] == 'High':
            if x['CUS_SPENDING_DRIVER_curr'] == 'Medium':
                return 'Moved from High to Medium'
            return 'Moved from High to Low'
        elif x['CUS_SPENDING_DRIVER_prev'] == 'Medium':
            if x['CUS_SPENDING_DRIVER_curr'] == 'High':
                return 'Moved from Medium to High'
            return 'Moved from Medium to Low'
        else:
            if x['CUS_SPENDING_DRIVER_curr'] == 'High':
                return 'Moved from Low to High'
            return 'Moved from Low to Medium'

def overall_movement(x,level='account'):
    if level == 'account':
        if x['ACCNT_PRIORITY_prev'] == 'High':
            if x['ACCNT_PRIORITY_curr'] == 'Medium':
                return 'Moved from High to Medium'
            return 'Moved from High to Low'
        elif x['ACCNT_PRIORITY_prev'] == 'Medium':
            if x['ACCNT_PRIORITY_curr'] == 'High':
                return 'Moved from Medium to High'
            return 'Moved from Medium to Low'
        else:
            if x['ACCNT_PRIORITY_curr'] == 'High':
                return 'Moved from Low to High'
            return 'Moved from Low to Medium'
    elif level =='customer':
        if x['CUS_PRIORITY_prev'] == 'High':
            if x['CUS_PRIORITY_curr'] == 'Medium':
                return 'Moved from High to Medium'
            return 'Moved from High to Low'
        elif x['CUS_PRIORITY_prev'] == 'Medium':
            if x['ACCNT_PRIORITY_curr'] == 'High':
                return 'Moved from Medium to High'
            return 'Moved from Medium to Low'
        else:
            if x['CUS_PRIORITY_curr'] == 'High':
                return 'Moved from Low to High'
            return 'Moved from Low to Medium'

       
df_comparison = (cs_previous
.merge(cs_current,how='left',on='ACCOUNT',suffixes=('_prev','_curr'))
.loc[lambda x: ((x['CUS_SPENDING_DRIVER_prev'].fillna(0) != x['CUS_SPENDING_DRIVER_curr'].fillna(0)) | (x['CUS_PRIORITY_prev'].fillna(0) != x['CUS_PRIORITY_curr'].fillna(0)) | (x['BP_>£5K_prev'].fillna(0) != x['BP_>£5K_curr'].fillna(0)) | (x['BP_£3-5K_prev'].fillna(0) != x['BP_£3-5K_curr'].fillna(0)) | (x['BP_IH_prev'].fillna(0) != x['BP_IH_curr'].fillna(0)) | (x['BP_OTHER_prev'].fillna(0) != x['BP_OTHER_curr'].fillna(0)) | (x['BP_ACCT_prev'].fillna(0) != x['BP_ACCT_curr'].fillna(0)) | (x['ACCT_RISK_DRIVER_prev'].fillna(0) != x['ACCT_RISK_DRIVER_curr'].fillna(0)) | (x['ACCT_HIGH_GROWTH_DRIVER_prev'].fillna(0) != x['ACCT_HIGH_GROWTH_DRIVER_curr'].fillna(0)) | (x['ACCT_STRATEGIC_DRIVER_prev'].fillna(0) != x['ACCT_STRATEGIC_DRIVER_curr'].fillna(0)) | (x['ACCT_NEW_BIZ_DRIVER_prev'].fillna(0) != x['ACCT_NEW_BIZ_DRIVER_curr'].fillna(0)) | (x['ACCT_SPENDING_DRIVER_prev'].fillna(0) != x['ACCT_SPENDING_DRIVER_curr'].fillna(0)) | (x['ACCT_PN_DRIVER_prev'].fillna(0) != x['ACCT_PN_DRIVER_curr'].fillna(0)) | (x['ACCNT_PRIORITY_prev'].fillna(0) != x['ACCNT_PRIORITY_curr'].fillna(0)) | (pd.isna(x['CUSTOMER_curr'])))]
.assign(BP_over_5K_movement = lambda x: np.where(x['BP_>£5K_prev'].fillna(0)==x['BP_>£5K_curr'].fillna(0),'',np.where(x['BP_>£5K_prev'].fillna(0)==0,'Moved to High Priority Band','Droped out of High Priority Band')))
.assign(BP_3_5K_movement = lambda x: np.where(x['BP_£3-5K_prev'].fillna(0)==x['BP_£3-5K_curr'].fillna(0),'',np.where(x['BP_£3-5K_prev'].fillna(0)==0,'Moved to High Priority Band','Droped out of High Priority Band')))
.assign(BP_IH_movement = lambda x: np.where(x['BP_IH_prev'].fillna(0)==x['BP_IH_curr'].fillna(0),'',np.where(x['BP_IH_prev'].fillna(0)==0,'Moved to High Priority Band','Droped out of High Priority Band')))
.assign(BP_OTHER_movement = lambda x: np.where(x['BP_OTHER_prev'].fillna(0)==x['BP_OTHER_curr'].fillna(0),'',np.where(x['BP_OTHER_prev'].fillna(0)==0,'Moved to High Priority Band','Droped out of High Priority Band')))
.assign(BP_ACCT_movement = lambda x: np.where(x['BP_ACCT_prev'].fillna(0)==x['BP_ACCT_curr'].fillna(0),'',np.where(x['BP_ACCT_prev'].fillna(0)==0,'Moved to High Priority Band','Droped out of High Priority Band')))
.assign(accnt_risk_driver_movement = lambda x: np.where(x['ACCT_RISK_DRIVER_prev'].fillna(0)==x['ACCT_RISK_DRIVER_curr'].fillna(0),'',np.where(x['ACCT_RISK_DRIVER_prev'].fillna(0)==0,'Moved to High Priority Band','Droped out of High Priority Band')))
.assign(accnt_high_growth_driver_movement = lambda x: np.where(x['ACCT_HIGH_GROWTH_DRIVER_prev'].fillna(0)==x['ACCT_HIGH_GROWTH_DRIVER_curr'].fillna(0),'',np.where(x['ACCT_HIGH_GROWTH_DRIVER_prev'].fillna(0)==0,'Moved to High Priority Band','Droped out of High Priority Band')))
.assign(accnt_strategic_driver_movement = lambda x: np.where(x['ACCT_STRATEGIC_DRIVER_prev'].fillna(0)==x['ACCT_STRATEGIC_DRIVER_curr'].fillna(0),'',np.where(x['ACCT_STRATEGIC_DRIVER_prev'].fillna(0)==0,'Moved to High Priority Band','Droped out of High Priority Band')))
.assign(accnt_new_biz_driver_movement = lambda x: np.where(x['ACCT_NEW_BIZ_DRIVER_prev'].fillna(0)==x['ACCT_NEW_BIZ_DRIVER_curr'].fillna(0),'',np.where(x['ACCT_NEW_BIZ_DRIVER_prev'].fillna(0)==0,'Moved to High Priority Band','Droped out of High Priority Band')))
.assign(accnt_spending_driver_movement = lambda x: np.where(x['ACCT_SPENDING_DRIVER_prev'].fillna(0)==x['ACCT_SPENDING_DRIVER_curr'].fillna(0),'',x.apply(lambda x: spend_movement(x),axis=1)))
.assign(accnt_pn_driver_movement = lambda x: np.where(x['ACCT_PN_DRIVER_prev'].fillna(0)==x['ACCT_PN_DRIVER_curr'].fillna(0),'',np.where(x['ACCT_PN_DRIVER_prev'].fillna(0)==0,'Moved to High Priority Band','Droped out of High Priority Band')))
.assign(accnt_overall_priority_movement = lambda x: np.where(x['ACCNT_PRIORITY_prev'].fillna(0)==x['ACCNT_PRIORITY_curr'].fillna(0),'',x.apply(lambda x: overall_movement(x),axis=1) ))
.assign(accnt_drop_out_of_the_report_as_a_whole = lambda x: np.where(x['CUSTOMER_curr'].fillna(0)==0,'Y',''))
.assign(cus_spending_driver_movement = lambda x: np.where(x['CUS_SPENDING_DRIVER_prev'].fillna(0)==x['CUS_SPENDING_DRIVER_curr'].fillna(0),'',x.apply(lambda x: spend_movement(x,'customer'),axis=1)))
.assign(cus_overall_priority_movement = lambda x: np.where(x['CUS_PRIORITY_prev'].fillna(0)==x['CUS_PRIORITY_curr'].fillna(0),'',x.apply(lambda x: overall_movement(x,'customer'),axis=1) ))
)

df_comparison.columns = df_comparison.columns.str.strip().str.upper()
output = sys.path[0] + '\\ CS PRIORITY MOVEMENT.xlsx'
df_comparison[final_cols].to_excel(output,index=False)







