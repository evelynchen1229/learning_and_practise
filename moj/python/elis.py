import pandas as pd
import numpy as np

cols_1 = ['id','LN User']
cols =  ['id','userPrincipalName']
#new_cols = ['id','email']

df_elis_1 = pd.read_csv('../file/elis/2020-1-20.csv')
df_elis_2 = pd.read_csv('../file/elis/2020-8-25.csv')
df_elis_3 = pd.read_csv('../file/elis/2021-4-27.csv')

''' get the original mapping list based on LN User column in 2020-1-20 file'''
ln_user = df_elis_1[cols_1].drop_duplicates()[~df_elis_1['LN User'].isnull()]

''' for the same id, get the emails from the latest file '''
def email_update(df_old = df_elis_1,df_latest = df_elis_3):
    df_update = (df_old[cols].merge(df_latest[cols],how='left',on='id')
            .assign(email = lambda x: np.where(x['userPrincipalName_y'].isnull(),x['userPrincipalName_x'],x['userPrincipalName_y'])
                )
            .rename(columns={'email':'userPrincipalName'})
            )[cols]
    return df_update

df_elis_1_update = email_update(email_update(df_latest=df_elis_2))
df_elis_2_update = email_update(df_elis_2)
df_elis_3_update = email_update(df_elis_3)

df_elis = (pd.concat([df_elis_1_update,df_elis_2_update,df_elis_3_update]).drop_duplicates()
        .merge(ln_user,how='left',on='id')
        .rename(columns={'userPrincipalName':'email'})
        .drop_duplicates()
        )
df_elis['id'] = df_elis['id'].str.lower()
df_elis.to_csv('../file/elis/elis.csv',index=False)
