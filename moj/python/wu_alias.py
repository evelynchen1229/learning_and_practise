
import psycopg2
import csv
import pandas as pd
import datetime as dt
import shutil

'''connect to gdw and get email and wu_alias'''
print('connect to redshift in DBeaver')
conn = psycopg2.connect(dbname= 'gdw', 
      host = 'prod-gdw-database.business.aws.lexisnexis.com', 
      port= '5439', 
      user= 'chenyx', 
      password= '!Uf2KfxQ')
query ="""
select distinct wu.user_signon_id,al.web_user_alias_id wa
--,trim(wu.web_user_first_name) web_user_first_name,trim(wu.web_user_last_name) web_user_last_name
,usem.cmunct_mthd_value as email
from bi.web_user_curr wu
left join bi.sub_acct_curr sac on sac.sub_acct_id = wu.sub_acct_id 
left join bi.web_user_alias al on al.web_user_id = wu.web_user_id and al.inst_id = '1001099'
left join 
(select web_user_id, cmunct_mthd_cd, cmunct_mthd_value
from bi_pi.web_user_cmunct_mthd
where cmunct_mthd_cd = '07'
and actv_ind = 'Y'
and cmunct_mthd_value is not null) USEM on wu.web_user_id = usem.web_user_id
where (sac.lbu_acct_id = 'THEC5067' or wu.user_signon_id like '%@476006' or wu.user_signon_id like '%@DCA')
and wu.lbu_id = 'UK'
"""
print("load result to dataframe")

df_wu_alias_latest = pd.read_sql(query,conn)
conn.close()

today = dt.datetime.today().strftime('%d%m%Y')
output_file = r'../file/wu_alias/wu_alias_{}.csv'.format(today)

print("save result to csv")
df_wu_alias_latest.to_csv(output_file, index=False, encoding='utf-8-sig')


df_wu_alias = pd.read_csv('../file/wu_alias/wu_alias.csv')

#df_wu_alias_latest = pd.read_csv(r'../file/wu_alias/wu_alias_{}.csv'.format(today))

df_wu_alias_final = (pd.concat([df_wu_alias,df_wu_alias_latest])
        .drop_duplicates()
        .fillna(0)
        .assign(fre = lambda x: x.groupby('user_signon_id')['wa'].transform('count'))
        )
df_wu_alias_final.drop(index= df_wu_alias_final.index[(df_wu_alias_final['fre'] > 1) & (df_wu_alias_final['email'] == 0)], axis = 0, inplace = True)
df_wu_alias_final.drop(columns='fre',inplace=True)
df_wu_alias_final['wa'] = df_wu_alias_final['wa'].str.lower()


shutil.move('../file/wu_alias/wu_alias.csv','../file/wu_alias/archive/wu_alias.csv')
df_wu_alias_final.to_csv('../file/wu_alias/wu_alias.csv',index = False)
