import pandas as pd
import numpy as np
import os
import sys

cs_data = sys.path[0] + '\\CS BASE DATA.xlsx'
pn_news = sys.path[0] + '\\Premium News - Renewals Tracker.xlsx'
cs_am = sys.path[0] + '\\CSM to AM Allocations_final_working.xlsx'

df_cs = pd.read_excel(cs_data)
cs_am_mapping = pd.read_excel(cs_am,'Sheet1')[['CSM','Adjusted CSLOGIN','REPCODE']]


# premium news 
df_pn=(pd.read_excel(pn_news)
       .rename(columns={'Billing acct to Map to in Allocation detail sheet':'ACCOUNT',
                           'iKnow Customer Account Number':'CUSTOMER'})
       .assign(mlex_gbp = lambda x: round(x['MLex Spend']/1.38,2))
       .assign(l360_gbp = lambda x: round((x['L360 Spend'].fillna(0))/1.38,2))

)
Mlex = ['Mlex','MLex']
l360=['L360','L360 PULSE','L360 - IP']

col_name = {'mlex_gbp_x':'MLex Spend £',
        'l360_gbp_x':'L360 Spend £',
        'mlex_gbp_y':'cus_mlex_spend_£',
        'l360_gbp_y':'cus_l360_spend_£',
        'Premium_News_Spend_Flag':'Premium News Spend Flag',
        'all_billing':'All Billing Account ON Spend',
        'adj_cus':'Adjusted Period End Customer ON Spend',
        'adj_cs':'Adjusted CS Allocation',
        'adj_cslogin': 'Adjusted CSLOGIN Allocation',
        'adj_csname' : 'Adjusted CSNAME Allocation'

      }

new_cols = ['CUSTOMER','CUSTNAME','ACCOUNT','ACCOUNTNAME','POSTCODE','POSTCODE_AREA','CITY','COUNTRY','FULLNAME','REPCODE','TEAM','CSTEAM','CSLOGIN','adj_cslogin','CSNAME','CSM','adj_csname','SEGMENT','NEW_BIZ_DEALS','Premium_News_Spend_Flag','LBU_ON_SPEND','mlex_gbp_x','l360_gbp_x','all_billing','CUST_ON_SPEND','adj_cus','MYD_FLG','MYD_YR','MYD_TRM','DT_END','CAE_FLG','RISK_LVL','PR_ONLY_RISK','LAST_TRAINED']
final_cols = ['CUSTOMER','CUSTNAME','ACCOUNT','ACCOUNTNAME','POSTCODE','POSTCODE_AREA','CITY','COUNTRY','FULLNAME','REPCODE','TEAM','CSTEAM','Adjusted CS Allocation','CSLOGIN','CSM','Adjusted CSLOGIN Allocation','CSNAME','Adjusted CSNAME Allocation','SEGMENT','NEW_BIZ_DEALS','Premium News Spend Flag','LBU_ON_SPEND','MLex Spend £','L360 Spend £','All Billing Account ON Spend','CUST_ON_SPEND','Adjusted Period End Customer ON Spend','MYD_FLG','MYD_YR','MYD_TRM','DT_END','CAE_FLG','RISK_LVL','PR_ONLY_RISK','LAST_TRAINED']



df_mlex = df_pn.loc[df_pn['Type (mlex/L360)'].isin(Mlex)][['CUSTOMER','ACCOUNT','mlex_gbp']].groupby(['ACCOUNT','CUSTOMER'])['mlex_gbp'].sum().reset_index()
df_l360 = df_pn.loc[lambda x: x['Type (mlex/L360)'].isin(l360)][['CUSTOMER','ACCOUNT','l360_gbp']].groupby(['ACCOUNT','CUSTOMER'])['l360_gbp'].sum().reset_index()
df_mlex_cus = df_mlex.groupby('CUSTOMER')['mlex_gbp'].sum().reset_index()
df_l360_cus = df_l360.groupby('CUSTOMER')['l360_gbp'].sum().reset_index()


df_final = (df_cs.merge(df_mlex[['ACCOUNT','mlex_gbp']], how='left',on='ACCOUNT')
    .merge(df_l360[['ACCOUNT','l360_gbp']],how='left',on='ACCOUNT')
    .merge(df_mlex_cus,how='left',on='CUSTOMER')
    .merge(df_l360_cus,how='left',on='CUSTOMER')  
    .merge(cs_am_mapping,how='left',on='REPCODE')
    .assign(all_billing=lambda x: x['LBU_ON_SPEND'].fillna(0) + x['mlex_gbp_x'].fillna(0) + x['l360_gbp_x'].fillna(0))
    .assign(adj_cus = lambda x: x['mlex_gbp_y'].fillna(0)+x['l360_gbp_y'].fillna(0)+x['CUST_ON_SPEND'].fillna(0))     
    .assign(Premium_News_Spend_Flag= lambda x: np.where(pd.notnull(x['mlex_gbp_x']),'Y',np.where(pd.notnull(x['l360_gbp_x']),'Y','N')))    
    .assign(adj_cslogin = lambda x: np.where( (x['all_billing'] == 0) | (x['TEAM'] == 'AM-T2'), 'SELFSERVE', np.where(pd.notnull(x['Adjusted CSLOGIN']), x['Adjusted CSLOGIN'],x['CSLOGIN'])))
    .assign(adj_csname = lambda x: np.where(x['adj_cslogin'] == 'SELFSERVE','SELFSERVE SELFSERVE',np.where(pd.notnull(x['CSM']), x['CSM'],x['CSNAME'])))
        )

# test : expect to see all True - pn lbu sum equals cus sum
mlex_test = round(df_final['mlex_gbp_x'].sum(),0) == round(df_final[['CUSTOMER','mlex_gbp_y']].drop_duplicates().iloc[:,1].sum(),0)
l360_test = round(df_final['l360_gbp_x'].sum(),0) == round(df_final[['CUSTOMER','l360_gbp_y']].drop_duplicates().iloc[:,1].sum(),0)

# final stage - put everything together
# all lbu level sum equals to cus sum
final_test = round(df_final['all_billing'].sum(),0) == round(df_final[['CUSTOMER','adj_cus']].drop_duplicates().iloc[:,1].sum(),0)

print(mlex_test,l360_test,final_test)
print('mlex_test:','acct:',round(df_final['mlex_gbp_x'].sum(),0),'cus:',round(df_final[['CUSTOMER','mlex_gbp_y']].drop_duplicates().iloc[:,1].sum(),0))
print('l360 test:','acct:',round(df_final['l360_gbp_x'].sum(),0),'cus:',round(df_final[['CUSTOMER','l360_gbp_y']].drop_duplicates().iloc[:,1].sum(),0))

# put recommended CS Team
def newteam(x):
    if x['all_billing'] == 0:
            return 'SELFSERVE'
    elif x['TEAM'] == 'AM-T2':
            return 'SELFSERVE'
    elif x['TEAM'] in ['AM-F1','AM-F2','AM-F3','ST-F1']:
            return 'CSF'
    elif x['TEAM'] in ['AM-T1','AM-T3','TE-F1','TE-T1']:
            return 'CSD'
    elif x['adj_cus'] >= 15000:
        return 'CSF'
    elif 5000 <= x['adj_cus'] <15000:
        return  'CSD'
    else: 
        return 'CORT'



df_final = (df_final.drop(columns = ['mlex_gbp_y','l360_gbp_y'])[new_cols]
        .assign(adj_cs = lambda x: x.apply(lambda x: newteam(x),axis=1))
        .rename(columns = col_name)
        )[final_cols]
df_final.columns = df_final.columns.str.strip().str.upper()
output_base =  sys.path[0]+'\\CS PN DATA.xlsx'

df_final.to_excel(output_base,index=False)
