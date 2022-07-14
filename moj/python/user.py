import pandas as pd

df_library = pd.read_excel('../file/moj_base_data.xlsx',sheet_name = 'LL BI Data',skiprows = lambda x: x in [0,1])['User Signon Identifier'].drop_duplicates()
df_psl = pd.read_excel('../file/moj_base_data.xlsx',sheet_name = 'PSL BI Data',skiprows = lambda x: x in [0,1])['User Signon Identifier'].drop_duplicates() 

df_user = pd.concat([df_library,df_psl]).drop_duplicates()

df_user.to_csv('../file/moj_user.csv',index=False)
