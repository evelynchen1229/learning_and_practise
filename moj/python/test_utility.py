import pandas as pd
''' load dataframe '''
df_wu_alias = pd.read_csv('../file/wu_alias/wu_alias.csv')

def cell_value(parameter,lkp_col='user_signon_id',result_col = 'wa',df=df_wu_alias):
    index = df[df[lkp_col]==parameter].index
    value = df[result_col].values[index][0]
    return value 
