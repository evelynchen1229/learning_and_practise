import pandas as pd
import numpy as np
import openpyxl
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.styles import Color, Fill
from openpyxl.cell import Cell
import os
import sys

# get dataframes ready
# for tax customers
output_tax_usg =  sys.path[0]+'\\3. Raw Data\\NPS-Tax_Usage.xlsx'
tax_usg = pd.read_excel(output_tax_usg)

output_tax_nps = sys.path[0]+'\\3. Raw Data\\NPS-Tax.xlsx'
tax_nps = pd.read_excel(output_tax_nps)

output_tax_email = sys.path[0]+'\\3. Raw Data\\tax_hub_no_email.xlsx'
tax_nps_null_email = pd.read_excel(output_tax_email)

# for legal customers
output_legal_usg =  sys.path[0]+'\\3. Raw Data\\NPS-Legal_Usage.xlsx'
legal_usg = pd.read_excel(output_legal_usg)

output_legal_nps = sys.path[0]+'\\3. Raw Data\\NPS-Legal.xlsx'
legal_nps = pd.read_excel(output_legal_nps)

output_legal_email = sys.path[0]+'\\3. Raw Data\\legal_hub_no_email.xlsx'
legal_nps_null_email = pd.read_excel(output_legal_email)

# funnel view and summary
funnel_file = sys.path[0]+'\\3. Raw Data\\funnel_view_and_summary.xlsx'
funnel_view = pd.read_excel(funnel_file,'Funnel_View')
summary_view = pd.read_excel(funnel_file,'No_Contacts')

# final dataset
output_final = sys.path[0]+'\\3. Raw Data\\final_data_set.xlsx'
final_dataset = pd.read_excel(output_final)

print('running checks  1 / 7 ...')
# check 1: funnel view final figures equals summary view figures
print('Funnel View stats equals to #contacts per product in the final file: \n', funnel_view['No_users_PWC_exclusion'] == summary_view['number_of_contacts'])

print('running checks  2 / 7 ...')
# check 2: double check whether any contacts have both null and not null email entries in hub
# expect to see distinct count of contact_ID by email addresses to be 1
duplication_check = (pd.concat([tax_nps,legal_nps,tax_nps_null_email ,legal_nps_null_email])
                     [['CONTACT_ID','EMAIL']]
                     .drop_duplicates()
                     .groupby(['CONTACT_ID'])['EMAIL'].count()
                     .reset_index()
                     ['EMAIL'].unique()
                    )
if duplication_check[0] == 1:
    print('One contact has one email record in the customer hub: PASS')
else:
    print('One contact has one email record in the customer hub: FAIL')

print('running checks  3 / 7 ...')
# check 3:  number of emails per contact - check whether there are any users with more than one email in the dataset
# expect to have 1 as result
no_of_email_per_user = final_dataset.groupby('USERNAME')['EMAIL'].nunique().reset_index()['EMAIL'].unique()
if no_of_email_per_user[0] == 1:
    print("One email per contact: PASS")
else:
    print("One email per contact: FAIL")

print('running checks  4 / 7 ...')
# check 4: # number of survey sent out per contact per product - expect to see 1 as result
no_of_survey_per_contact_per_prod = final_dataset.groupby(['product','USERNAME'])['EMAIL'].count().reset_index()['EMAIL'].unique()
if no_of_survey_per_contact_per_prod[0] == 1:
    print("One email per contact per product: PASS")
else:
    print("One email per contact per product: FAIL")

print('running checks  5 / 7 ...')
# check 5: tolleyguidance_and_tolleylibrary split to tolley guidance and tolley library correctly
num_combined = (final_dataset
        .loc[lambda x: x['PRODUCT'].str.contains('_and_')]
        .groupby('product')['PRODUCT'].count()
        )
print('tolleyguidance_and_tolleylibrary split to tolley guidance and tolley library correctly:\n',num_combined[0] == num_combined[1])

print('running checks  6 / 7 ...')
# check 6:  potential exclusion - check with Kev whether need to exclude the related accounts
NAME_INTERNAL = ['GRAT','AUTH','STUD','LEXI','LEGA','BUTT','EXTE','HAMM']
potential_exclusion = (pd.concat([legal_nps,tax_nps])
                       .loc[lambda x: x['GENESIS_ACCOUNT'].str.contains('|'.join(NAME_INTERNAL))]
                       .groupby(['GENESIS_ACCOUNT','MASTERNAME','REP_CODE','REP_NAME','SALES_TERRITORY'])['USERNAME'].count()
                       .reset_index()
                      )

print('potential accounts to be excluded: ',potential_exclusion)

print('running checks  7 / 7 ...')
# check 7: straightward accounts and email exclusion have been applied as expected
engagement_file = sys.path[0]+'\\engagement.txt'
with open(engagement_file) as f:
        lines = f.readlines()
        accnt_engagement = [line.strip() for line in lines]
        f.close()
ACCOUNTS_EXCLUDED = accnt_engagement + ['EMMS5003','KNIG5010','KNIG5103','KNIG5104','PRIC5129','LEXI5081','WILL5016','WEST5276','WBIR5000','WALK5098','VALE5035','UKGL5000','TRAN5024','THEC6838','THEC5067','TENO5005','SURR5028','STHC5001','SSTA5006','SSTA5005','SOUT6633','SIGS5000','RWGO5000','ROYA5211','RMJA5001','RGKA5001','REED5133','REED0020','PUBL5023','PTEM5000','PSLT5000','PSLS5000','PRIS5017','POLI5001','PHUN5000','PENN5015','PAUL5020','PARR5019','OFFI5316','OFFI5309','NTHW5002','NOTT5048','NDAL5000','MRRI5005','MROD5001','MINI5354','MINI5341','MINI5276','MHAY5002','MATT5103','MANA5042','LUTO5027','LORD5061','LOND6472','LNTE5000','LNBT5001','LNBT5000','LEXI5396','LEXI5390','LEXI5386','LEXI5377','LEXI5365','LEXI5352','LEXI5335','LEXI5329','LEXI5318','LEXI5286','LEXI5278','LEXI5275','LEXI5264','LEXI5239','LEXI5202','LEXI5161','LEXI5126','LEXI5107','LEXI5092','LEXI5008','LEIC5040','LEGA6495','LDJH5000','LANC5039','KNOW5038','KING5475','JUST5047','JUST5022','JUDI5046','JUDG5086','JUDG5084','JUDG5082','JUDG5081','JUDG5080','JUDG5077','JUDG5024','JUDG5011','JUDG0021','JSCA5001','JOHN5599','JOHN5584','JMIL5007','JHRE5004','JDRA5000','JAME5753','JAME5750','INTE5697','HOWA5063','HONM5083','HONM5069','HONM5058','HONM5046','HONM5038','HONM5037','HONM5012','HONJ5005','HMPA5000','HMCO5003','HISH5132','HISH5131','HISH5129','HISH5127','HISH5126','HISH5125','HISH5122','HISH5121','HISH5120','HISH5118','HISH5110','HISH5109','HISH5108','HISH5107','HISH5106','HISH5105','HISH5102','HISH5101','HISH5099','HISH5097','HISH5094','HISH5092','HISH5087','HISH5084','HISH5083','HISH5080','HISH5078','HISH5076','HISH5067','HISH5055','HISH5054','HISH5046','HISH5044','HISH5042','HISH5030','HISH5029','HISH5028','HISH5027','HISH5024','HISH5022','HISH5020','HISH5015','HISH5009','HISH5007','HHJU5000','HERH5006','HERH5004','HERH5001','HENR5091','HCLT5002','HAMM0028','HAM19945','HAM19153','GRAT7646','GRAT5001','GOSN5000','GMCG0001','GLYN5000','GLPT5000','EXTE5005','EDWA5157','EBEN5001','DORS5025','DIST5060','DIST5045','DIST5036','DIST5020','DIST5016','DIST5011','DIST5007','DIST5006','DIST5005','COUR6017','COMP5248','CLIF5132','CLER0069','CHRI5524','CHRI5098','CHAI0013','CBLO5000','CARO5151','BUTT5073','BUTT5020','BLEV5003','BJLA5000','BEAS5004','BAKE5016','AUTH5003','AUDI5004','ATHE5020','ASIM5004','ARMY5003','APGH5001','AMBU5000','AJSE5000','5THB0001','LNIN5001','TREV5076']
EMAIL_EXCLUDED = ['francesca.hutcheson@dykeyaxley.co.uk']


accnt_email_exclusion = (final_dataset
                       .loc[lambda x: (x['GENESIS_ACCOUNT'].isin(ACCOUNTS_EXCLUDED) | x['EMAIL'].isin(EMAIL_EXCLUDED))]
                      )

if accnt_email_exclusion.empty:
    print("Set of accounts and email have been excluded as expected: PASS")
else:
    print("Set of accounts and email have been excluded as expected: FAIL")

potential_pwc = (final_dataset
.loc[lambda x: (x['GENESIS_ACCOUNT'].str.contains('PRIC') | x['MASTERNAME'].str.contains('pricewaterhousecoopers', case = False) | x['EMAIL'].str.contains('pwc.com',case = False))]
.groupby(['GENESIS_ACCOUNT','MASTERNAME','REP_CODE','REP_NAME','SALES_TERRITORY','EMAIL'])['USERNAME'].count()
.reset_index()
                      )
print('potential pwc accounts: ',potential_pwc)

