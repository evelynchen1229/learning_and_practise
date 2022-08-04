''' THE FOLLOWING TAKES THE BASE DATA AND CREATES TWO NEW COLUMNS WHICH WILL CONTAIN THE NEWLY ASSIGNED TEAM
    AND THE REASON FOR ASSIGNMENT.
    - THE RULES REFLECT THE STANDARD THRESHOLDS IN THE FILE PROVIDED BY SALESOPS
    - THE EXCEPTION OVERRIDE THE RULES

    FILE IS THEN FORMATTED AND SAVED
'''
# Nov 2021 new rules requested
# Nov 21 BD list needs changing - need to add BD-F3


import pandas as pd
import xlsxwriter
import datetime as dt
import os
import sys




### RULES ###

def topTierAlloc(segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    if segment == 'Top Tier' or previousTeam == 'ST-F1':
        return 'ST-F1'


def fullServiceAlloc(segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    if segment == 'Full Service Commercial' or previousTeam == 'ST-F1':
        return 'ST-F1'

def tradeAlloc(segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    if segment == 'Trade' or previousTeam == 'TE-F1':
        return 'TE-F1'

def exportAlloc(segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    if segment == 'Export' or previousTeam == 'TE-F1':
        return 'TE-F1'

def generalPracticeAlloc(segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    BDlist = ['BD-P1', 'BD-T1', 'BD-T2', 'BD-F1', 'BD-F3']
    
    if segment == 'General Practice':
        
        if currentSpend > 15000:
            return 'AM-F2'

        if currentSpend > 3000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'N':
            # Nov 21 change
            return 'AM-T3'
        if currentSpend > 5000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'Y':
            # Nov 21 change
            return 'AM-T3'
        if currentSpend >= 0 and currentSpend <= 15000 and nexisAccount == 'Y':
            # Nov 21 change
            return 'AM-T3'

        if currentSpend > 0 and currentSpend <= 5000 and nexisAccount == 'N' and onlineSub == 'Y' :
            return 'AM-T2'

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' :
            # Nov 21 change
            return 'BD-F1'

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' and previousTeam in BDlist:
            return previousTeam





def consumerLedAlloc(segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    
    BDlist = ['BD-P1', 'BD-T1', 'BD-T2', 'BD-F1', 'BD-F3']
    if segment == 'Consumer-Led':

        if currentSpend > 15000:
            return 'AM-F2'

        if currentSpend > 3000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'N':
            # Nov 21 change
            return 'AM-T3'
        if currentSpend > 5000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'Y':
            # Nov 21 change
            return 'AM-T3'
        if currentSpend >= 0 and currentSpend <= 15000 and nexisAccount == 'Y':
            # Nov 21 change
            return 'AM-T3'

        if currentSpend > 0 and currentSpend <= 5000 and nexisAccount == 'N' and onlineSub == 'Y' :
            return 'AM-T2'
            
        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' :
            # Nov 21 change
            return 'BD-F1'

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' and previousTeam in BDlist:
            return previousTeam




def smallLawAlloc(segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    BDlist = ['BD-P1', 'BD-T1', 'BD-T2', 'BD-F1', 'BD-F3']
    if segment == 'Small Law':

        if currentSpend > 15000:
            return 'AM-F2'

        if currentSpend > 3000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'N':
            return 'AM-T1'
        if currentSpend > 5000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'Y':
            return 'AM-T1'        
        if currentSpend >= 0 and currentSpend <= 15000 and nexisAccount == 'Y':
            return 'AM-T1'

        if currentSpend > 0 and currentSpend <= 5000 and nexisAccount == 'N' and onlineSub == 'Y' :
            return 'AM-T2'

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' and FEnum > 5:
            # Nov 21 change
            return 'BD-F1'

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' and FEnum >= 1 and FEnum<= 5:
            return 'BD-T1 or BD-T2'

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' and previousTeam in BDlist:
            return previousTeam

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N':
            return '0 FE'


def academicAlloc(segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    BDlist = ['BD-P1', 'BD-T1', 'BD-T2', 'BD-F1', 'BD-F3']
    if segment == 'Academic':

        if currentSpend > 15000:
            return 'AM-F3'

        if currentSpend > 3000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'N':
            return 'AM-T3'
        if currentSpend >= 0 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'Y': 
            return 'AM-T3'
        if currentSpend >= 0 and currentSpend <= 15000 and nexisAccount == 'Y':
            return 'AM-T3'

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' and FEnum > 2:
            # requested in Nov 2021
            return 'New BD Team'

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N':
            return 'BD-T2'




def barAlloc(segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    if segment == 'Bar':

        if currentSpend > 15000:
            return 'AM-F1'

        if currentSpend > 3000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'N':
            return 'AM-T3'
        if currentSpend > 0 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'Y':  
            return 'AM-T3'
        if currentSpend >= 0 and currentSpend <= 15000 and nexisAccount == 'Y':
            return 'AM-T3'

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' and FEnum > 2:
            # Nov 21 change
            return 'New BD Team'

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N':
            return 'BD-T2'


def irelandAlloc(segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    if segment == 'Ireland':

        if currentSpend > 15000:
            return 'AM-F3'

        if currentSpend > 0 and currentSpend <= 5000 and nexisAccount == 'N' and onlineSub == 'Y':
            return 'AM-T2'

        if currentSpend > 3000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'N':
            return 'AM-T3'
        if currentSpend > 5000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'Y':
            return 'AM-T3'
        if currentSpend >= 0 and currentSpend <= 15000 and nexisAccount == 'Y':
            return 'AM-T3'

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N':
            return 'BD-T1'


def publicSectorAlloc(segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    BDlist = ['BD-P1', 'BD-T1', 'BD-T2', 'BD-F1', 'BD-F3']
    if segment == 'Public Sector':

        if currentSpend > 15000 and nexisAccount == 'N' and onlineSub == 'N':
            return 'AM-F1'
        if currentSpend > 15000 and nexisAccount == 'N' and onlineSub == 'Y':
            return 'AM-F1'
        if currentSpend > 15000 and nexisAccount == 'Y' and onlineSub == 'Y':
            return 'AM-F1'

        if currentSpend > 3000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'N':
            # Nov 21 change
            return 'AM-T3'

        if currentSpend > 0 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'Y':
            # Nov 21 change
            return 'AM-T3'


        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' and FEnum > 2:
            # Nov 21 change 
            return 'New BD Team'
        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N':
            return 'BD-T2'



def inhouseLegalAlloc(segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    BDlist = ['BD-P1', 'BD-T1', 'BD-T2', 'BD-F1', 'BD-F3']
    if segment == 'Inhouse Legal':
        if currentSpend > 15000:
            return 'AM-F1'

        if currentSpend > 0 and currentSpend <= 5000 and nexisAccount == 'N' and onlineSub == 'Y':
            return 'AM-T2'

        if currentSpend > 3000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'N':
            # Nov 21 change
            return 'AM-T1'
        if currentSpend > 5000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'Y':
            # Nov 21 change
            return 'AM-T1'
        if currentSpend >= 0 and currentSpend <= 15000 and nexisAccount == 'Y':
            return 'AM-T3'
   
        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' and FEnum > 2:
            # Nov 21 change 
            return 'New BD Team'
        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' and FEnum >= 1 and FEnum<= 2:
            return 'BD-T2'


        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' and previousTeam in BDlist:
            return previousTeam 

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N':
            # return '0 FE'
            return 'BD-T2'


        

def inhouseTaxAlloc(segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    BDlist = ['BD-P1', 'BD-T1', 'BD-T2', 'BD-F1', 'BD-F3']
    if segment == 'Inhouse Tax':


        # Nov 21 change
        if currentSpend > 15000 and nexisAccount == 'N' and onlineSub == 'Y':
            return 'AM-F1'

        # Nov 21 change
        if currentSpend > 15000 and nexisAccount == 'N' and onlineSub == 'N':
            return 'AM-F1'

        if currentSpend > 12000 and nexisAccount == 'Y' and onlineSub == 'Y':
            return 'AM-F1'

        # Nov 21 change
        if currentSpend > 0 and currentSpend <= 4000 and nexisAccount == 'N' and onlineSub == 'Y':
            return 'AM-T2'

        # Nov 21 change
        if currentSpend > 3000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'N':
            return 'AM-T3'

        # Nov 21 change
        if currentSpend > 4000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'Y':
            return 'AM-T3'



        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' and FEnum > 3:
            return 'BD-F1'

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N':
            return 'BD-T1'



def taxAlloc(segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    BDlist = ['BD-P1', 'BD-T1', 'BD-T2', 'BD-F1', 'BD-F3']
    if segment == 'Tax':

        # Nov 21 change
        if currentSpend > 15000 and nexisAccount == 'N' and onlineSub == 'N':
            return 'AM-F1'
        # Nov 21 change
        if currentSpend > 15000 and nexisAccount == 'N' and onlineSub == 'Y':
            return 'AM-F1'

        # Nov 21 change
        if currentSpend > 0 and currentSpend <= 4000 and nexisAccount == 'N' and onlineSub == 'Y':
            return 'AM-T2'

        # Nov 21 change
        if currentSpend > 3000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'N':
            return 'AM-T3'
        # Nov 21 change
        if currentSpend > 4000 and currentSpend <= 15000 and nexisAccount == 'N' and onlineSub == 'Y':
            return 'AM-T3'

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' and FEnum > 3:
            return 'BD-F1'
        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' and FEnum >= 1 and FEnum<= 3:
            return 'BD-T1'

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N' and previousTeam in BDlist:
            return previousTeam

        if currentSpend <= 3000 and nexisAccount == 'N' and onlineSub == 'N':
            return '0 FE'



### EXCEPTIONS ###

# Nov 21 change: no need the belwo exception
#def BDAlloc(originalAlloc, segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
#    BDlist = [ 'BD-P1', 'BD-T1', 'BD-T2', 'BD-F1', 'BD-F3'] #'BD-CH'
#    AMlist = ['AM-T1', 'AM-T2', 'AM-T3', 'AM-F1', 'AM-F2', 'AM-F3']
#    if previousTeam in BDlist and onlineSub =='Y' and originalAlloc in AMlist:
#        return previousTeam
#    
def BD_alloc_flg(originalAlloc, segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    if 'BD' in previousTeam and BDallocatable == 'N':
        return previousTeam

def winBack(originalAlloc, segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    AMlist = ['AM-F1', 'AM-F2', 'AM-F3']
    if previousTeam in AMlist and onlineSub == 'N' and PYflg == 'Y':
        return previousTeam

def winBackFlg(onlineSub, previousTeam,PYflg):
    AMlist = ['AM-F1', 'AM-F2', 'AM-F3', 'AM-T1','AM-T2','AM-T3']
    if previousTeam in AMlist and onlineSub == 'N' and PYflg == 'Y':
        return 'Y'

# Nov 21 change: remove BD from cae exceptions 
def cae_subs(originalAlloc, segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
    if float(cae) > 0.5 and 'BD' not in previousTeam:
        return previousTeam




def getNewTeam( row ):
    segment = row['Segment']
    currentSpend = float(row['CurrYr_Tot_with_Nexis'])
    nexisAccount = row['Has_Nexis_Account']
    previousTeam = row['TEAM']
    renewableONspend = row['CUST_ON_RENEWALFLG']
    onlineSub = row['Cust_ON_or_Nexis']
    FEnum = row['FeeEarnerNum']
    PYflg = row['CUS_HAS_PY_ONLINE_SPEND']
    BDallocatable = row['BD Allocatable']
    cae = row['CUST_CAE_P']

    ruleFns = [ #winBack,
                #nexisAlloc,
                topTierAlloc, 
                fullServiceAlloc,
                tradeAlloc,
                exportAlloc,
                generalPracticeAlloc,
                consumerLedAlloc,
                smallLawAlloc,
                academicAlloc,
                barAlloc,
                irelandAlloc,
                publicSectorAlloc,
                inhouseLegalAlloc,
                inhouseTaxAlloc,
                taxAlloc
                 ]
    additionalRules = [winBack, cae_subs]


    for ruleFn in ruleFns:
        originalAlloc = None
        if ruleFn(segment, currentSpend, nexisAccount, onlineSub, previousTeam,renewableONspend,FEnum,PYflg,BDallocatable,cae):
            originalAlloc = ruleFn(segment, currentSpend, nexisAccount, onlineSub, previousTeam,renewableONspend,FEnum,PYflg,BDallocatable,cae)
            for additionalRule in additionalRules:
                if additionalRule(originalAlloc, segment, currentSpend, nexisAccount, onlineSub, previousTeam,renewableONspend,FEnum,PYflg,BDallocatable,cae):
                    return additionalRule(originalAlloc, segment, currentSpend, nexisAccount, onlineSub, previousTeam,renewableONspend,FEnum,PYflg,BDallocatable,cae)
            return originalAlloc
#        elif BD_alloc_flg(originalAlloc, segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
 #           return BD_alloc_flg(originalAlloc, segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae)
        elif winBack(originalAlloc, segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
            return winBack(originalAlloc, segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae)
        elif cae_subs(originalAlloc, segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae):
            return cae_subs(originalAlloc, segment, currentSpend, nexisAccount, onlineSub, previousTeam, renewableONspend,FEnum,PYflg,BDallocatable,cae)
    return 'n/a'

def addFlg(row):
    PYflg = row['CUS_HAS_PY_ONLINE_SPEND']
    previousTeam = row['TEAM']
    onlineSub = row['Cust_ON_or_Nexis'] #Cust_ON_RenewalFlg
    
    ruleFns = [winBackFlg]

    for ruleFn in ruleFns:
        if ruleFn(onlineSub, previousTeam,PYflg):
            return ruleFn(onlineSub, previousTeam,PYflg)
            
    return 'N'


### OUTCOME COLUMN - 2021 ADDITION###

def outcome(x):

    #Nov 21
    # for non BD team, cae exception applies so new team will be caused by cae exception
    # for BD team, cae exception doesn't apply, will move to AM team due to spend
    if x['CUST_CAE_P'] > 0.5 and 'BD' not in str(x['Team']): # and  x['BD Allocatable'] != 'N':
        return 'CAE'

    elif str(x['New Team']) in ['AM-T1','AM-T3'] and x['Has_Nexis_Account'] == 'Y' and float(x['CurrYr_Tot_with_Nexis']) <= 5000:
        return 'Nexis (where allocated out of T2 as cannot have Nexis)'
    
    # Dec 21 change:

    elif 'AM-T2' in str(x['New Team']) :
        if  x['Winback flag'] == 'N':
            return 'Spend (CORT)'
        else:
            return 'Winback (CORT)'

    elif 'AM-T' in str(x['New Team']) :
        if  x['Winback flag'] == 'N':
            return 'Spend (Desk)'
        else:
            return 'Winback (Desk)'


    elif 'ST-F1' in  str(x['New Team']):
        return 'Strategic'

    # Nov 21 - for my information, can be deleted later
    elif 'TE-F1' in str(x['New Team']):
        return 'Trade and Export'
    elif 'Reg-Comp' in str(x['HP_Segment_2_Desc']):
        return 'Reg-Comp segment'
    elif 'Internal' in str(x['HP_Segment_2_Desc']):
        return 'Internal segment'

    elif 'AM-F3' in  str(x['New Team']) and x['Segment']=='Ireland':
        return 'Ireland'

    elif 'AM-F' in str(x['New Team']):
        if x['Winback flag'] == 'N':
            return 'Spend (Field)'
        else:
            return 'Winback (Field)'

    elif 'BD' in  str(x['New Team']):
        if x['BD Allocatable'] == 'N':
            if pd.notnull(x['Marketable Contact Flag']) and x['HP_Segment_2_Desc'] in ['Consumer-Led','Consumer-led','Small Law','Solo','General Practice','Large Corporate Legal','Small Corporate Legal', 'Large Tax (Legal)', 'Mid Tax', 'Other Tax (Legal)', 'Solo Tax','Other Tax - Legal','Large Tax - Legal']:
                # Nov 21
                if x['Winback flag'] == 'Y' :
                    return 'Winback (Desk); Cannot Allocate - Marketable contacts available but missing FE (BD)' 
                return 'Cannot Allocate - Marketable contacts available but missing FE (BD)'
            elif pd.isnull(x['Marketable Contact Flag']):
                if x['Winback flag'] == 'Y' :
                    return 'Winback (Desk); Cannot Allocate - Missing Marketable contacts (BD)' 
                return 'Cannot Allocate - Missing Marketable contacts (BD)'
#        elif pd.isnull(x['BD Allocatable']) and x['Winback flag'] == 'Y':
        elif x['Winback flag'] == 'Y':
            return 'Winback (Desk)'
        elif pd.isnull(x['FeeEarnerNum']):
            return 'Missing Fee Earner (BD)'
        elif x['CurrYr_Tot_with_Nexis'] > 0 and x['Cust_ON_or_Nexis'] == 'N':
            return 'No Online Renewals (BD)'
        elif x['CurrYr_Tot_with_Nexis'] <= 0 and x['Cust_ON_or_Nexis'] == 'N':
            return 'No Spend BD'

# Nov 21: delete bd allocatable flag if new team is not BD team or 0 FE; previous team is not BD and new team is not n/a 
def bd_allocatable(x):
    if '0 FE' in str(x['New Team']) or 'BD' in str(x['New Team']):
        return x['BD Allocatable']
    elif 'BD' in str(x['TEAM']) and 'n/a' in str(x['New Team']):
        return x['BD Allocatable']
    return None

today = dt.datetime.today().strftime('%Y%m%d')
today_src = dt.datetime.today().strftime('%d_%m_%y')
#read base data (whatever that is)
#src = str(input('Enter File Path of Base Data: '))
#src = src.replace('"','').replace('\\', '/')
src = sys.path[0] + f'\\outputs\\Base Data Clean_{today_src}.xlsx'
df = pd.read_excel(src)
print( "*" * 80 )
print( "applying categorisation rules ..." )

df['New Team'] = df.apply(lambda row: getNewTeam(row), axis=1)
df['Winback flag'] = df.apply(lambda row: addFlg(row), axis=1)
df['adj_bd_allocatable'] = df.apply(lambda x: bd_allocatable(x), axis=1)


print( "*" * 80 )
print( "exporting data ...")

print( df.groupby('New Team').count()['TEAM'])

df = (df.drop(columns = ['BD Allocatable'])
        .rename(columns = {'TEAM':'Team','REPCODE': 'RepCode','FULLNAME':'FullName','SEGMENT':'HP_Segment_2_Desc','Customer_id':'OC_ROW_ID','CUSTNAME':'OC_NAME','ACCOUNT':'AccountNumber','ACCOUNTNAME':'AccountName','LBUMAXRENEWDATE':'LBUmaxRenewDate','CUSTMAXRENEWDATE':'CustMaxRenewDate', 'adj_bd_allocatable':'BD Allocatable'})
        )
df['outcome'] = df.apply(lambda x: outcome(x), axis=1)
df = df[['UNIQUE_ID','Hub Org ID','Team','RepCode', 'FullName', 'HP_Segment_2_Desc',  'Segment','OC_ROW_ID', 'OC_NAME','CITY', 'POSTCODE', 'REGION','COUNTRY','AccountNumber', 'AccountName','FeeEarnerNum','Legal_FE', 'Tax_FE', 'Consortium','CHAMBER_FLAG','LBU_CY_TOT','LBU_CY_ON_AMT', 'CUS_CY_TOT', 'CurrYr_Tot_with_Nexis','CUS_CY_ON_AMT', 'LBU_PY_TOT','LBU_PY_ON_AMT', 'CUS_PY_TOT','CUS_PY_ON_AMT','Winback flag','FTSE350', 'PRIVATE100', 'Marketable Contact Flag','BD Allocatable','LBU_ON_RENEWALFLG', 'CUST_ON_RENEWALFLG','New Team','outcome','CUSTOMER_STATUS','ACCOUNT_STATUS',  'LBUmaxRenewDate','CustMaxRenewDate','LBU_CY_PR_AMT', 'LBU_CY_OA_AMT', 'CUS_CY_PR_AMT', 'CUS_CY_OA_AMT', 'LBU_PY_PR_AMT', 'LBU_PY_OA_AMT', 'CUS_PY_PR_AMT', 'CUS_PY_OA_AMT', 'YRPER', 'LBU_SUBSCR', 'LBU_CAE_VAL', 'CUST_SUBSCR',  'CUST_CAE_VAL', 'CUST_CAE_P',  'CUS_HAS_CY_ONLINE_SPEND','Has_Nexis_Account', 'Nexis Spend','LBU_MLEX_GBP', 'LBU_LAW360_GBP','LBU_Premium_News_Spend','CUS_MLEX_GBP', 'CUS_LAW360_GBP','CUS_Premium_News_Spend','CUS_HAS_PY_ONLINE_SPEND','Cust_ON_or_Nexis','LBU_MYD_FLG', 'Matching pool','Reporting Country','Reporting Region','4th_level_segment']]

#df.columns
## FORMATTING ##
## date columns
for col in [ 'LBUmaxRenewDate','CustMaxRenewDate']:
    df[col] = df[col].astype('datetime64[ns]')
    df[col] = [d.strftime('%d/%m/%Y') if not pd.isnull(d) else '' for d in df[col]]



output_file = sys.path[0] + f"\\outputs\\Allocations_{today}.xlsx"
column_list = df.columns
writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

#fix formats - bold headings
df.to_excel(writer, sheet_name = 'Allocations', startrow = 1, header = False, index = False)

workbook  = writer.book
worksheet = writer.sheets['Allocations']

for idx, val in enumerate(column_list):
    worksheet.write(0, idx, val)

#fix formats - expand all columns with data
for idx, col in enumerate(df):  # loop through all columns
    series = df[col]
    max_len = max((
        series.astype(str).map(len).max(),  # len of largest item
        len(str(series.name))  # len of column name/header
        )) + 3  # adding a little extra space
    worksheet.set_column(idx, idx, max_len)  # set column width

writer.save()