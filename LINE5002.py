import pandas as pd
import numpy as np
import os
import sys
import openpyxl
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.styles import Color, Fill
from openpyxl.cell import Cell

#cs_data = sys.path[0] + '\\CS PROPOSED DATA New Business.xlsx'
source_data = 'LINE5002_Source.xlsx'
trial_module = ['Personal Injury','Tax','Arbitration','TMT','Information Law','EU Law','International Trade']

# get cleaned PA - without leading space
df_source_raw = pd.read_excel(source_data)
df_source = (df_source_raw.assign(cleaned_pa = lambda x: x['Practice Area'].str.strip()))[['CSI','cleaned_pa']].drop_duplicates()

# step one - flag unique or overlap
df_unique = (df_source
.groupby(['CSI'])['cleaned_pa'].count().reset_index()
.rename(columns={'cleaned_pa':'csi_count'})
)

df_mapping = (df_source.merge(df_unique,how='inner',on='CSI')
.assign(unique_or_overlap = lambda x: np.where(x['csi_count']==1,'Unique','Overlap'))
.assign(adj_pa = lambda x: np.where(x['cleaned_pa'].isin(trial_module),'Trial Modules',x['cleaned_pa']))
)

#print(df_mapping)
#df_mapping.to_csv('practice area mapping.csv',index=False)

# step two - for overlap sources, indicate overlapped source

df_overlap = (df_mapping[['CSI','adj_pa']][df_mapping['unique_or_overlap'] == 'Overlap']
.drop_duplicates()
.groupby (['CSI'])['adj_pa'].apply('/ '.join).reset_index()
.assign(unique_or_overlap='Overlap')
)

# step three - concat unique source and overlapped source
df_final = pd.concat([df_mapping[['CSI','cleaned_pa','unique_or_overlap']][df_mapping['unique_or_overlap'] == 'Unique'].rename(columns={'cleaned_pa':'adj_pa'}),df_overlap])

print(df_final)
df_final.to_csv('practice area for reporting.csv',index = False)


