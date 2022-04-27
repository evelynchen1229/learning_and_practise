'''This script is to flag top 200 law and ftse100 in the latest subscription list
'''

'''loading modules'''
import pandas as pd
import datetime as dt
from datetime import date
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, Color, Border
import numpy as np
import re
from sqlalchemy.engine import create_engine
import datetime as dt
from datetime import date
import os
import sys


name_suffix = ['company','bank','banking','ltd','.',',','limited','llp','plc','holdings','holding group',' - legal',' se',"int'l",'international','lnf - ',' uk']
today_yr = date.today().year
today_mth = date.today().month

existing_mapping_file = sys.path[0] + '\\mapping.xlsx'
account_base = sys.path[0] + '\\subscription.xlsx'
law_list = sys.path[0] + '\\top200law.xlsx'
df_mapping_law = pd.read_excel(existing_mapping_file,sheet_name='Lawyer200')
df_mapping_ftse = pd.read_excel(existing_mapping_file,sheet_name='FTSE100')
df_account_base = pd.read_excel(account_base)[['acc_num','acc_name','market_seg']].drop_duplicates().rename(columns={'acc_num':'account_number','acc_name':'account_name','market_seg':'segment'})
df_law_list = pd.read_excel(law_list)

DIALECT = 'oracle'
SQL_DRIVER = 'cx_oracle'
USERNAME = 'DATAANALYTICS' 
PASSWORD = 'DatPwd123Z' 
HOST = 'PSDB3684.LEXIS-NEXIS.COM'
PORT = 1521
SERVICE = 'GBIPRD1.ISPPROD.LEXISNEXIS.COM'
ENGINE_PATH_WIN_AUTH = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD +'@' + HOST + ':' + str(PORT) + '/?service_name=' + SERVICE
engine = create_engine(ENGINE_PATH_WIN_AUTH)

def quarter(mth):
    if mth == 0:
        return 'Q4'
    else:
        quarter_num = mth // 4 + 1
        return 'Q' + str(quarter_num)

def year(yr,mth):
    if mth == 0:
        return str(yr - 1)
    else:
        return str(yr)

def cleanup(df,col_name):
    name_value  = df[col_name].lower()
    for ns in name_suffix:
        if ns in name_value:
            name_value = name_value.replace(ns,'')
#    name_value = name_value.replace(' ','')
    name_value = name_value.strip()
    match = re.search(r'\([^()]*\)',name_value)
    if match:
        name_value = name_value.replace(match.group(),"")
    
    return name_value

def columnclean(df,col):
    df_clean = df.assign(cleaned_name = lambda x: x.apply(lambda x: cleanup(x, col_name = col),axis = 1))
    return df_clean


def mapping(df_subs,df_law,df_ftse):
    df_subs = (df_subs.merge(df_law,how='left',left_on=acct_cols[0],right_on=law_cols[0])
.merge(df_ftse,how='left',left_on = acct_cols[0],right_on = ftse_cols[0])
.loc[:,lambda x: ~x.columns.str.contains('_x|_y')]
    )
    return df_subs

def words(name ,first_word_only = 'N'):
    words_list = name.split(' ')
    if first_word_only == 'N':
        return words_list
    else:
        return words_list[0]



reporting_quarter = quarter(today_mth - 1)
reporting_year = year(today_yr, today_mth - 1)
ftse_list = sys.path[0] + f'\\{reporting_year}\\{reporting_year} {reporting_quarter}\\ftse100_{reporting_year}{reporting_quarter}.csv'
ftse_change =sys.path[0] + f'\\{reporting_year}\\{reporting_year} {reporting_quarter}\\ftse100_comparison.xlsx'
df_ftse_list = pd.read_csv(ftse_list)
df_ftse_old = pd.read_excel(ftse_change,sheet_name='ftse_drop_out')
df_ftse_new = pd.read_excel(ftse_change,sheet_name='ftse_new_code')
df_ftse_name_change = pd.read_excel(ftse_change,sheet_name= 'df_ftse_name_change')
'''1. mapping based on the existing mapping file'''

acct_cols = df_account_base.columns
ftse_cols = df_mapping_ftse.columns
law_cols = df_mapping_law.columns

df_mapping = mapping(df_account_base,df_mapping_law,df_mapping_ftse)

'''2. for unmapped accounts, check any new pairs need adding in'''
'''possibly safe to exclude university, chambers, academic, public, chambers / bar segment as they are unlikely to be in top 200 law list or ftse100'''
''' assumption for getting unmapped accounts is that most law firms don't go public and ftse100 so far hasn't had any big law firm, therefore instead of an or logic, and logic is used to filter for unmapped accounts'''

df_unmapped = (df_mapping
.assign(unmapped_law = lambda x: np.where(x['UK 200'].fillna(0) == 0,'Y','N'))
.assign(unmapped_ftse = lambda x: np.where(x['FTSE100'].fillna(0) == 0, 'Y', 'N'))
.loc[lambda x : (x['unmapped_law'] == 'Y') & (x['unmapped_ftse'] == 'Y') & (~(x['segment'].isin(['Bar','Other Public Sector','Other Academic'])| (x['account_name'].str.contains('University|College|Universiteit|Universita|Universit|LexisNexis'))))]
.assign(cleaned_name = lambda x: x.apply(lambda x: cleanup(x,col_name ='account_name'),axis = 1))
)

#--- for law200---
#df_unmapped.to_excel('./account_unmapped.xlsx',index=False)
df_law_list_cleaned = columnclean(df_law_list,'M&A and other names')

'''checking any potential law200 pairs to be added to the mapping file
method used for checking is just a left join based on the cleaned name
'''
df_unmapped_checking = (df_unmapped[['account_number','account_name','cleaned_name']]
.merge(df_law_list_cleaned,how='left',on='cleaned_name')
)
df_potential_new_pair = df_unmapped_checking.loc[lambda x: pd.isna(x['Firm']) == False]

# need to double check any accounts named "Stephensons" as the real top200 Stephensons is stephensons solicitor and it doesn't have office in BRIERLEY HILL
stephensons = df_potential_new_pair.loc[lambda x: x['cleaned_name'] == 'stephensons']
stephensons_acc_num = ','.join([ "'" + x + "'" for x in stephensons['account_number'].to_list()])


conn_base=engine.connect()

query = f'''
select 
cd.customer_account account,
        addrs.addr_4 AS city
        from
pdl.gen_r_customer_delivery cd 
LEFT JOIN pdl.gen_r_names_addresses addrs ON addrs.address_ptr = cd.address_ptr AND addrs.sys_current_flg = 'Y'
where cd.SYS_CURRENT_FLG = 'Y' 
and cd.customer_account in ({stephensons_acc_num})

'''
stephensons_check = pd.read_sql(query, con=conn_base)
conn_base.close()

wrong_stephensons_acct = stephensons_check.loc[lambda x: x['city'].str.upper() == 'BRIERLEY HILL']['account'].to_list()

# the below dataframe would be the potential pair after excluding wrong pairs for stephensons
double_check = (df_potential_new_pair
.loc[lambda x: ~x['account_number'].isin(wrong_stephensons_acct)]
.rename(columns={'account_number':'ACC_NUM','account_name':'ACC_NAME','Rank':'UK 200 Rank','Firm':'UK 200'})
)
print (double_check)

checking = input("Do you want to add any pair to Laywer200 mapping? Y / N")
if 'y' in checking.lower():
    df_new_mapping_law = df_mapping_law.append(double_check[df_mapping_law.columns])
elif checking in ['N','No','no','n','']:
    df_new_mapping_law = df_mapping_law
else:
    specify_account = input('''If you just want to add specific pair to Laywer200 mapping, please specify the account number. 
    If multiple account numbers will be added, please use space to separate them.''')
    specified_accouts = specify_account.split(' ')
    df_new_mapping_law = df_mapping_law.append(double_check.loc[lambda x: x['ACC_NUM'].isin(specified_accouts)][df_mapping_law.columns])

wb = openpyxl.load_workbook(existing_mapping_file)
writer = pd.ExcelWriter(existing_mapping_file, engine='openpyxl')
writer.book = wb
del wb['Lawyer200']
df_new_mapping_law.to_excel(writer,sheet_name='Lawyer200',index=False)
writer.save()


''' produce a file with unmapped accounts for manual check'''
df_law_unmapped_accounts = df_unmapped_checking.loc[lambda x: pd.isna(x['Firm']) == True]
df_law_unmapped_accounts.to_excel(sys.path[0] + '\\unmapped_accounts.xlsx',index=False)

# --- ftse100 ---
df_ftse_list_cleaned = columnclean(df_ftse_list,'Name')

def ftsepair(acct_name,ftse_name,df_account = df_unmapped,df_ftse=df_ftse_list_cleaned):
    acct_num = df_account['account_number'][df_account['cleaned_name'] == acct_name].values[0]
    acct = df_account['account_name'][df_account['cleaned_name'] == acct_name].values[0]
    ftse = df_ftse['Name'][df_ftse['cleaned_name'] == ftse_name].values[0].upper()
    ftse_code = df_ftse['Code'][df_ftse['cleaned_name'] == ftse_name].values[0]
    print('Account Name:',acct,'\nFTSE Company:',ftse)
    add_pair = input('Would you like to add this pair? Y / N')
    if 'y' in add_pair.lower():
        pair_info = {'ACC_NUM':acct_num,'ACC_NAME':acct,'FTSE100':ftse,'FTSE100 Code':ftse_code}
        df_ftse_pair = pd.DataFrame(data=pair_info,index=[0])
    else:
        df_ftse_pair = pd.DataFrame()
        
        
    return df_ftse_pair

# for unmapped ftse100 companies
unmapped_names = df_unmapped['cleaned_name'].to_list()
ftse_cleaned_name = df_ftse_list_cleaned['cleaned_name'].to_list()
for fn in ftse_cleaned_name:
    for un in unmapped_names:
        if len(words(fn)) == 1  and fn in words(un):
            df_ftse_new_pair = ftsepair(un,fn)
            df_mapping_ftse = df_mapping_ftse.append(df_ftse_new_pair)
        elif len(words(un)) == 1 and un in words(fn):
            df_ftse_new_pair = ftsepair(un,fn)
            df_mapping_ftse = df_mapping_ftse.append(df_ftse_new_pair)
        elif len(words(fn)) > 1 and len(words(fn)) <= len(words(un))  and fn in un:
            df_ftse_new_pair = ftsepair(un,fn)
            df_mapping_ftse = df_mapping_ftse.append(df_ftse_new_pair)
        elif len(words(un)) > 1 and len(words(fn)) >= len(words(un))  and un in fn:
            df_ftse_new_pair = ftsepair(un,fn)
            df_mapping_ftse = df_mapping_ftse.append(df_ftse_new_pair)
        else:
            pass

'''remove mappings that have dropped out of lists and update name for name  / code change'''
old_ftse_code = df_ftse_old['Code'].to_list()

df_new_mapping_ftse = (df_mapping_ftse.merge(df_ftse_name_change,how='left',left_on = 'FTSE100 Code',right_on = 'Code_prev')
.assign(adj_code = lambda x:  np.where(pd.isna(x['Code_curr']) == False,x['Code_curr'],x['FTSE100 Code']))
.assign(adj_name = lambda x:np.where(pd.isna(x['Code_curr']) == False,x['Name_curr'].str.upper(),x['FTSE100']))
.rename(columns={'FTSE100':'old FTSE','FTSE100 Code':'old Code','adj_code':'FTSE100 Code','adj_name':'FTSE100'})
)[['ACC_NUM','ACC_NAME','FTSE100','FTSE100 Code','Comment']]

df_new_mapping_ftse['Comment'] = df_new_mapping_ftse['Comment'].apply(lambda x: np.where(x in old_ftse_code,'Old',''))
del wb['FTSE100']
df_new_mapping_ftse.to_excel(writer,sheet_name='FTSE100',index=False)
writer.save()
wb.save(existing_mapping_file)