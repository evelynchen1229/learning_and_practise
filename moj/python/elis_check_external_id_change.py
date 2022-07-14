import pandas as pd
import numpy as np


df_elis = pd.read_csv('../file/elis/elis.csv')

df = df_elis.groupby('email')['id'].transform('count').reset_index()
print(df[df['id']==2])
print(df_elis.iloc[[5618,8348,6559,9167]][['id','email']])
