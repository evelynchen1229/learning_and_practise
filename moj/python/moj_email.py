
'''
automate the process to get elis user emails
1. whether a user is in the user_email_for_report
2. whether a user has elis email (based on wu alias)
3. whether a user has email from wu_alias
4. append latest wu_alias
5. append new mapping 
6. no emails are Unpsecified
7. email for mapped users are up to date
'''
#import wu_alias
#import user
#import elis
#import update
import pandas as pd
import datetime as dt
import  numpy as np
import shutil


today = dt.datetime.today().strftime('%d%m%Y')

''' load dataframes '''
df_moj_user = pd.read_csv('../file/moj_user.csv')
df_wu_alias = pd.read_csv('../file/wu_alias/wu_alias.csv')
df_elis = pd.read_csv('../file/elis/elis.csv')
df_email_mapping = pd.read_csv('../file/user_email_for_report.csv')

''' load existing mapping '''
mapped_users = df_email_mapping['User Signon Identifier'].to_list()

''' wu_alias left join elis user'''
user_info = (df_wu_alias.merge(df_elis,how = 'left',left_on='wa',right_on='id')
        .rename(columns = {'email_x':'email_gdw', 'email_y':'email_elis'})
        .fillna(0)
        )
#user_info.to_csv('../file/user_info.csv',index=False)
''' get user email mapping '''
#final structure should be user, external id if applicable, email
#final list always left join elis/rat/wa qeuery result for latest 
#email before starting new round of user email mapping
def user_email(user):
    if user in mapped_users: 
        pass
    else:
        return user 

user_list = []
for user in df_moj_user['User Signon Identifier'].to_list():
    user_id = user_email(user)
    if user_id is not None:
        user_list.append(user_id)

df_user_list = pd.DataFrame({'user_signon_id':user_list})

def new_user_email_mapping(df = df_user_list):
    df_new_mapping = (df
            .merge(user_info,how='left',on='user_signon_id')
            .fillna(0)
            .assign(email = lambda x: np.where(x['email_elis'] == 0,x['email_gdw'],x['email_elis']))
            .assign(source = lambda x: np.where(x['email_elis'] == 0,'gdw','elis')) 
            )
    df_new_mapping = (df_new_mapping[~df_new_mapping['email'].isin([0,'0'])]
        .rename(columns = {'user_signon_id' : 'User Signon Identifier','email': 'Email', 'wa':'External Id','source':'Data Source'})
        [['User Signon Identifier','Email','External Id','Data Source']]
        .drop_duplicates()
        .reset_index()
        )
    return df_new_mapping

df_user_new_mapping = new_user_email_mapping()

df_user_new_mapping.to_csv('../file/new_mapping.csv',index=False)

df_final_user_mapping = pd.concat([df_email_mapping,df_user_new_mapping]).drop_duplicates()
shutil.move('../file/user_email_for_report.csv','../file/archive/user_email_for_report_{}.csv'.format(today))
df_final_user_mapping.to_csv('../file/user_email_for_report.csv',index=False)
