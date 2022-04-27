import pandas as pd
import datetime as dt
import  numpy as np
import shutil


today = dt.datetime.today().strftime('%d%m%Y')

''' load dataframes '''
#initial email mapping might need to get external id as well
#for the latest email from elis list
# some old mappings are based on names
df_email_mapping = pd.read_csv('../file/user_email_for_report.csv')
df_wu_alias = pd.read_csv('../file/wu_alias/wu_alias.csv')
df_elis = pd.read_csv('../file/elis/elis.csv')
old_col =['User Signon Identifier','email_update','external_id','source_update']
new_col = ['User Signon Identifier','Email','External Id','Data Source']
#can't merge with user pool because it's wu_alias left join elis
#left join wu_alias on user id, left join elis on external id
def update(df = df_email_mapping):
    df_update = (df_email_mapping.fillna(0)
            .merge(df_wu_alias,how = 'left',left_on = 'User Signon Identifier',right_on='user_signon_id')
            .fillna(0)
            .assign(external_id = lambda x: np.where(x['Data Source']=='elis',x['External Id'],np.where(x['wa'].isin([0,'0']),x['External Id'],x['wa'])))
            .merge(df_elis,how='left',left_on='external_id',right_on='id')
            .rename(columns={'email_x':'email_gdw','email_y':'email_elis'})
            .fillna(0)
            .assign(email_update = lambda x: np.where(~x['email_elis'].isin([0,'0']),x['email_elis'],np.where(~x['email_gdw'].isin([0,'0']),x['email_gdw'],x['Email'])))
            .assign(source_update = lambda x: np.where(~x['email_elis'].isin([0,'0']),'elis',np.where(~x['email_gdw'].isin([0,'0']),'gdw',x['Data Source'])))
            .drop_duplicates()
            .reset_index()
            )[old_col].rename(columns={'email_update':'Email','external_id':'External Id','source_update':'Data Source'})
    df_update = (df_update.drop_duplicates()
            .reset_index())
    return df_update

df_updated_user_mapping = update()

shutil.move('../file/user_email_for_report.csv','../file/archive/user_email_for_report_before_updated_{}.csv'.format(today))
df_updated_user_mapping.to_csv('../file/user_email_for_report.csv',index=False)

        
