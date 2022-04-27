'''THE BELOW TAKES THE DATA OUTPUTTED BY Base_Data_Fetch.py AND WRANGLES IT TO PRODUCE
THE FINAL FILE READY FOR SUBMISSION INTO THE ALLOCATION CODE STARTED BY MAILA MUTSO IN 2019
'''


import pandas as pd
import os
import sys

import datetime
from datetime import date
today = date.today().strftime('%d_%m_%y')

# SEGMENT LOOKUP
# SECOND VALUE WILL BE USED FOR THE ALLOCATION LOGIC
# THIRD VALUE WILL BE USED FOR FE ASSIGNMENT
seg = [['Other Public Sector','Public Sector','Legal'],
['Other Tax (Legal)','Tax','Tax'],
['Large Corporate Legal','Inhouse Legal','Legal'],
['Other Tax (Corporate)','Inhouse Tax','Tax'],
['Small Law','Small Law','Legal'],
['Export','Export','Legal/Tax'],
['General Practice','General Practice','Legal'],
['Other Academic','Academic','Legal'],
['Trade','Trade',''],
['Bar','Bar','Legal'],
['Consumer-led','Consumer-Led','Legal'],
['Mid Law','Ireland','Tax/Legal'],
['Top Tier','Top Tier','Legal'],
['Full Service Commercial','Full Service Commercial','Legal'],
['BIS Academic','Academic','Legal'],
['Large Tax (Legal)','Tax','Tax'],
['BIS Corporate Non Legal','Inhouse Legal','Legal'],
['Unassigned','Unassigned',''],
['BIS Corporate Legal','Inhouse Legal','Legal'],
['BIS Government','Public Sector','Legal'],
['Solo','Small Law','Legal'],
['Large Tax (Corporate)','Inhouse Tax','Tax'],
['Small Corporate Legal','Inhouse Legal','Legal'],
['Large Tax - Corporate','Inhouse Tax','Tax'],
['Large Tax - Legal','Tax','Tax'],
['Other Tax','Tax','Tax'],
['Other Tax - Corporate','Inhouse Tax','Tax'],
['Other Tax - Legal','Tax','Tax'],
['Unassigned'],
['Solo Tax','Tax','Tax'],
['Mid Tax','Tax','Tax'],
['Top Tier Tax','Top Tier','Tax'],
]

seg_lu = pd.DataFrame(seg, columns = ['Sec_subclass','Segment','FE'])

# directory of lookup files
#dir_lkp = os.getcwd()+'\\Lookup Files\\'
# directory of raw data
#dir_raw = os.getcwd()+'\\Raw Data\\'

### FUNCTIONS: FE ASSIGNMENT LOGIC, FLAG TO ASCERTAIN IF BD ACCOUNT CAN BE ALLOCATED ##############
# fee earners assignment logic
def fe_num(x):
       if x['FE'] == 'Legal':
              return x['Legal_FE']
       elif x['FE'] == 'Tax':
              return x['Tax_FE']
       else:
              if pd.isnull(x['Legal_FE']):
                     return x['Tax_FE']
              else:
                     return x['Legal_FE']

# can we allocate to BD flag
#def BD_allocatable(x):
#    lst_1 = ['Consumer-Led','Consumer-led','Small Law','Solo','General Practice','Large Corporate Legal','Small Corporate Legal', 'Large Tax (Legal)', 'Mid Tax', 'Other Tax (Legal)', 'Solo Tax','Other Tax - Legal','Large Tax - Legal']
#    lst_2 = ['Other Academic', 'Bar', 'Large Tax (Corporate)','Large Tax - Corporate', 'Other Tax (Corporate)','Other Tax - Corporate', 'Other Public Sector','Mid Law','Ireland','BIS Academic','BIS Corporate Non Legal']
#
#    if x['SEGMENT'] in ['Trade','Export','Full Service Commercial','Top Tier']:
#       return 'N/A'
#    if 'BD' in x['TEAM']:
#        if x['CUS_CY_PR_AMT'] > 0.0:
#            return 'Y'
#        if x['SEGMENT'] in lst_1 and pd.notnull(x['FeeEarnerNum']) and  pd.notnull(x['Marketable Contact Flag']):
#            return 'Y'
#        if x['SEGMENT'] in lst_2 and  pd.notnull(x['Marketable Contact Flag']):
#            return 'Y'
#        else:
#            return 'N'
#    return 'N/A'
def BD_allocatable(x):
    lst_1 = ['Consumer-Led','Consumer-led','Small Law','Solo','General Practice','Large Corporate Legal','Small Corporate Legal', 'Large Tax (Legal)', 'Mid Tax', 'Other Tax (Legal)', 'Solo Tax','Other Tax - Legal','Large Tax - Legal']
    lst_2 = ['Other Academic', 'Bar', 'Large Tax (Corporate)','Large Tax - Corporate', 'Other Tax (Corporate)','Other Tax - Corporate', 'Other Public Sector','Mid Law','Ireland','BIS Academic','BIS Corporate Non Legal']

# N0v 21 change:
    if x['SEGMENT'] in ['Trade','Export','Full Service Commercial','Top Tier'] or x['TEAM'] in ['ST-F1','TE-F1'] :
        return 'N/A'
    # print spend between 0 and 3k, Y regardless of marketable contacts and FE
    # over 3k will be allocated to AM anyway
    if x['CUS_CY_PR_AMT'] > 0  :
        return 'Y'
    elif pd.isnull(x['Marketable Contact Flag']):
        return 'N'
    elif x['SEGMENT'] in lst_1 and pd.isnull(x['FeeEarnerNum']) :
        return 'N'
    return 'Y'


########## LOAD FILES ############

# Manually Mapped legacy to new nexis customers
#mapping = pd.read_csv(dir_lkp+'Customer Mapping_manually mapped.csv')
mapping = pd.read_csv(sys.path[0] + '\\Lookup File\\Customer Mapping.csv')
# base financial data
#financials = pd.read_csv(dir_raw+'Raw_Financial Base.csv',encoding='windows-1252')
financials = pd.read_excel(sys.path[0] + f'\\outputs\\financials_plutus_after_pn_{today}.xlsx')#,encoding='windows-1252')
#financials = pd.read_excel('./outputs/financials_plutus_after_pn_05_11_21.xlsx')#,encoding='windows-1252')
#Whitespace
#whitespace = pd.read_csv(dir_raw+'WHITESPACE DATA_1712.csv')
#whitespace = pd.read_excel('./outputs/whitespace_{0}.xlsx'.format(today))
# Marketable Contacts
#marketable = pd.read_csv(dir_raw+'MARKETABLE CONTACTS.csv')
# Hub data
hub = pd.read_csv(sys.path[0] + f'\\Raw Data\\raw_hub_{today}.csv')
#hub = pd.read_csv('./Raw Data/raw_fe_marketable_strategy_05_11_21.csv')
#base nexis data
#nexis = pd.read_csv(dir_raw+'Raw_Nexis Billings.csv')
nexis = pd.read_csv(sys.path[0] + '\\Raw Data\\raw_nexis_billing_{today}.csv')
#nexis = pd.read_csv('./Raw Data/raw_nexis_billing_05_11_21.csv')
#current territory file
#territory = pd.read_excel(dir_lkp+'Territory Extract 2020 Year End.xlsx')
territory = pd.read_excel(sys.path[0] + '\\Lookup File\\Territory Extract.xlsx')
#chamber flag
chamber = pd.read_csv(sys.path[0] + f'\\Raw Data\\raw_chambers_{today}.csv')
#chamber = pd.read_csv('./Raw Data/raw_chambers_05_11_21.csv')


######## TRANSFORMATIONS #############

# appending whitespace, hub info, chamber flag to the base financials
financials =(financials
              .merge(hub, how = 'left', left_on = 'CUSTOMER',right_on = 'CUSTOMER')
              .merge(chamber, how = 'left', left_on = 'CUSTOMER',right_on = 'CUSTOMER')
             # .rename(columns={'CUSTOMER_x':'CUSTOMER_hub','CUSTOMER_y':'CUSTOMER_chamber'})
              )

# taking Consortia accounts from the territory file
# applying group concat due to duplicate consortia
consortia = (territory[['Customer Account Id','Consortium']].drop_duplicates()
            .loc[~pd.isnull(territory['Consortium'])]
            .groupby('Customer Account Id').apply(lambda x: ','.join(x.Consortium))
            .reset_index()
            .rename(columns = {0 : 'Consortium'})
              )

# taking hub org id and reporting countr/region from the territory file
reporting_country = territory[['Customer Account Id','Hub Org ID','Reporting Country','Reporting Region']].drop_duplicates()

# merging the nexis financial data with the customers manually mapped (get legacy integration id from new cust)
nexis_mapped=(nexis
              .merge(mapping, how = 'left', left_on = 'CUSTOMER', right_on = 'ACCNT_NUM')
              # value grouped by legacy integration id and new customer
              .groupby(['INTEGRATION_ID','CUSTOMER'])[['SUM(VALUE_DOC)']].sum()
              .rename(columns = {'SUM(VALUE_DOC)': 'value'})
              # assign the total value for the legacy customer
              .assign(subtotal = lambda x: x.groupby('INTEGRATION_ID').value.transform('sum')).reset_index()
              # group concat the new customer, to capture multiple nexis customers for one legacy cust, comma separated
              .groupby(['INTEGRATION_ID','subtotal']).apply(lambda x: ','.join(x.CUSTOMER))
              .reset_index()
              .rename(columns = {0: 'CUSTOMER'})
                     )
nexis_mapped['subtotal'] = pd.to_numeric(nexis_mapped['subtotal'],errors='coerce')

# putting all together
tog = (financials
       #merge bespoke customer mapping
       .merge(nexis_mapped, how = 'left', left_on = 'CUSTOMER', right_on = 'INTEGRATION_ID' )
       #drop unnecessary cust mapping columns
       .drop(columns = (['INTEGRATION_ID']))
       #top 100 flag
       #.assign(Top100 = financials[['CUSTOMER']].apply(lambda x: 'Y' if x['CUSTOMER'] in top100 else 'N', axis =1))
       #rename according to Maila's file
       .rename(columns = {'subtotal': 'Nexis Spend', 'CUSTOMER_y' : 'Matching pool', 'CUSTOMER_x':'Customer_id'})
       #merging Kev's segments
       .merge(seg_lu, how = 'left', left_on = 'SEGMENT', right_on = 'Sec_subclass')
       # drop the extra subclass columns
       .drop(columns = 'Sec_subclass' )
       #merging relevant territory columns
       .merge(consortia , how = 'left', left_on = 'Customer_id', right_on = 'Customer Account Id')
       .drop(columns =(['Customer Account Id']))           
       #merging territory file to get hub org id and reporting country
       .merge(reporting_country,how='left',left_on='Customer_id',right_on='Customer Account Id')
       .drop(columns='Customer Account Id')
       )

# CurrYr_Tot_with_Nexis - cust total + nexis spend
tog= tog.assign(CurrYr_Tot_with_Nexis = tog['CUS_CY_TOT'].fillna(0) + tog['Nexis Spend'].fillna(0))

# nexis_mike - flags if the Nexis Spend is not NaN
tog = tog.assign(nexis_mike = tog[['Nexis Spend']].apply(lambda x: 'N' if pd.isnull(x['Nexis Spend'])   else 'Y' , axis = 1))

#Has_Nexis_Account - flags if the customer has the LAW nexis flag ('WAENX', 'FTACA') or Mike Nexis Spend
#Nov 2021: no need for nexis flag any more, just Mike Nexis Spend
tog = tog.rename(columns={'nexis_mike' :'Has_Nexis_Account'} )

# Cust_ON_or_Nexis - Y if cust has ON renewals or Nexis
tog = tog.assign( Cust_ON_or_Nexis= tog[['CUST_ON_RENEWALFLG','Has_Nexis_Account']].apply(lambda x: 'Y' if (x['Has_Nexis_Account'] == 'Y' or x['CUST_ON_RENEWALFLG'] == 'Y') else 'N', axis = 1))


### APPLYING FUNCTIONS FROM THE TOP
#FE number - apply function
tog['FeeEarnerNum'] = tog.apply(lambda x: fe_num(x), axis=1)
#Can the customer be allocated to BD?
tog['BD Allocatable'] = tog.apply(lambda x: BD_allocatable(x), axis=1)



#### EXPORT #####
tog.to_excel(sys.path[0] + f'\\outputs\\Base Data Clean_{today}.xlsx', index = False)



