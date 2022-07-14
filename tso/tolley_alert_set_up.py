import pandas as pd
import cx_Oracle
import datetime
from datetime import timedelta
from datetime import date
import os
import sys
import openpyxl
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.styles import Color, Fill
from openpyxl.cell import Cell
import warnings
warnings.simplefilter("ignore")

yr = int(date.today().strftime('%Y'))
mth = int(date.today().strftime('%m'))


'''connect to PQS'''
'''need to change the host and change to ldap'''
#dsn_tns = cx_Oracle.makedsn('PSDB1c863-VIP.LEXIS-NEXIS.COM',
                            #'1521', service_name='olsprod55-scan.lexisnexis.com')
#conn = cx_Oracle.connect(user='PQS_READ',
                         #password='PQS_READ', dsn=dsn_tns)

query = '''SELECT     
  ALERTS.OWNER_BILLGROUP     
, ALERTS.MASTER_BILLGROUP     
, ALERTS.BILLGROUP_NAME     
, ALERTS.BILLGROUP_STATUS     
, OWNERSTATUS.OWNER_STATUS_DESC     
, ALERTS.PRIMARY_MARKET     
, ALERTS.USER_TYPE     
, ALERTS.BILL_PLAN     
, ALERTS.WEB_ID     
, ALERTS.LEXIS_ID     
, ALERTS.USER_FIRST_NAME     
, ALERTS.USER_LAST_NAME     
, ALERTS.USER_FULL_NAME     
, ALERTS.ALERT_KEY     
, ALERTS.ALERT_NAME     
, ALERTS.ALERT_CREATION_DATE     
, ALERTS.ALERT_STATUS     
, ALERTSTATUS.ALERT_STATUS_DESC     
, ALERTS.PRODUCT_ID     
, PRODID.PRODUCT_NAME     
, ALERTS.SUB_PRODUCT_ID     
, SUBPRODID.SUB_PRODUCT_NAME     
, ALERTS.MENU     
, ALERTS.LIBRARY     
, ALERTS.FILES     
, ALERTS.RUN_SCHEDULE     
, SCHEDULEID.RUN_SCHEDULE_DESC     
, ALERTS.RUN_DAY     
, ALERTS.RUN_HOUR     
, ALERTS.RUN_MINUTE     
, ALERTS.TIME_ZONE_ID     
, ALERTS.START_HRLY     
, ALERTS.END_HRLY     
, ALERTS.DST_FLAG     
, ALERTS.DELIVERY_SWITCH     
, ALERTS.DELIVERY_DESTINATION_TYPE     
, DELDES.DEL_DEST_DESC     
, ALERTS.DELIVERY_EMAIL_ADDRESS     
, ALERTS.NOTIFICATION_SWITCH     
, ALERTS.NOTIFICATION_EMAIL_ADDRESS     
, ALERTS.CLIENT_ID     
, ALERTS.SEARCH_TEXT     
 FROM     
  (SELECT     
    SUBSTR(OWNERGROUP,1,6)                                  AS OWNER_BILLGROUP     
  , SUBSTR(UINFO.BGRP.MASTBGRP,1,6)                         AS MASTER_BILLGROUP     
  , UINFO.BGRP.BGRP_DESC                                    AS BILLGROUP_NAME     
  , OWNERSTATUS                                             AS BILLGROUP_STATUS     
  , UINFO.BGRP.PRIMMKT_KEY_PRIMARY_MKT_GRP                  AS PRIMARY_MARKET     
  , UINFO.BGRP.BGRP_IND_USER_TYPE                           AS USER_TYPE     
  , UINFO.BGRP.BILL_PLAN_NEW                                AS BILL_PLAN     
  , SUBSTR(OWNERID,7,30)                                    AS WEB_ID     
  , SUBSTR(OWNERID,1,6)                                     AS LEXIS_ID     
  , UINFO.WEB_USERS.FIRST_NAME                              AS USER_FIRST_NAME     
  , UINFO.WEB_USERS.NAME                                    AS USER_LAST_NAME     
  , UINFO.WEB_USERS.NAME||', '||UINFO.WEB_USERS.FIRST_NAME  AS USER_FULL_NAME     
  , PROFILE.PROFILEKEY                                      AS ALERT_KEY     
  , DESCRIPTIVENAME                                         AS ALERT_NAME     
  , SAVEDATE                                                AS ALERT_CREATION_DATE     
  , SCHEDSTATUS                                             AS ALERT_STATUS     
  , OWNER.PRIMARYPRODID                                     AS PRODUCT_ID     
  , OWNER.HIERARCHPRODID                                    AS SUB_PRODUCT_ID     
  , MENU                                                    AS MENU     
  , LIBRARY                                                 AS LIBRARY     
  , FILELIST                                                AS FILES     
  , PERIODICITY                                             AS RUN_SCHEDULE     
  , SCHEDULE.RUNDAY                                         AS RUN_DAY     
  , SCHEDULE.RUNHOUR                                        AS RUN_HOUR     
  , SCHEDULE.RUNMINUTE                                      AS RUN_MINUTE     
  , SCHEDULE.TIMEZONEID                                     AS TIME_ZONE_ID     
  , SCHEDULE.STARTHOURLY                                    AS START_HRLY     
  , SCHEDULE.ENDHOURLY                                      AS END_HRLY     
  , SCHEDULE.DAYLIGHTSAVINGSFLAG                            AS DST_FLAG     
  , DELIVERY.DELIVERYSWITCH                                 AS DELIVERY_SWITCH     
  , DELIVERY.DESTINATIONTYPE                                AS DELIVERY_DESTINATION_TYPE     
  , DELIVERY.EMAILAdDRESS                                   AS DELIVERY_EMAIL_ADDRESS     
  , ALERT.DELIVERYSWITCH                                    AS NOTIFICATION_SWITCH     
  , ALERT.EMAILADDRESS                                      AS NOTIFICATION_EMAIL_ADDRESS     
  , QUERY.CLIENTID                                          AS CLIENT_ID     
  , QUERY.SEARCHTEXT                                        AS SEARCH_TEXT     
  FROM  PROFILE     
  JOIN  ALERT     
  ON    PROFILE.PROFILEKEY = ALERT.PROFILEKEY     
  JOIN  DELIVERY     
  ON    PROFILE.PROFILEKEY = DELIVERY.PROFILEKEY     
  JOIN  OWNER     
  ON    PROFILE.OWNERKEY = OWNER.OWNERKEY     
  JOIN  QUERY     
  ON    PROFILE.PROFILEKEY = QUERY.PROFILEKEY     
  JOIN  SCHEDULE     
  ON    PROFILE.PROFILEKEY = SCHEDULE.PROFILEKEY     
  JOIN  UINFO.WEB_USERS@UINFO     
  ON    SUBSTR(OWNERID,7,30) = UINFO.WEB_USERS.WEBID_LOGIN     
  JOIN  UINFO.BGRP@UINFO     
  ON    OWNERGROUP = UINFO.BGRP.BGRP_ID_BGRP_KEY) ALERTS     
LEFT JOIN     
  (SELECT 1 AS PRODUCT_ID, 'Corp Web' AS PRODUCT_NAME FROM DUAL UNION ALL     
  SELECT 2, 'Legal Web' FROM DUAL UNION ALL     
  SELECT 3, 'Schools/Colleges' FROM DUAL UNION ALL     
  SELECT 4, 'Company Quick Check' FROM DUAL UNION ALL     
  SELECT 5, 'NBC Research' FROM DUAL UNION ALL     
  SELECT 6, 'Congressional Compass' FROM DUAL UNION ALL     
  SELECT 7, 'GIS Compass' FROM DUAL UNION ALL     
  SELECT 8, 'Lexis.com' FROM DUAL UNION ALL     
  SELECT 9, 'Sales Requestor' FROM DUAL UNION ALL     
  SELECT 10, 'Statistical Compass' FROM DUAL UNION ALL     
  SELECT 11, 'Lawyer Locater' FROM DUAL UNION ALL     
  SELECT 12, 'Power Invoice' FROM DUAL UNION ALL     
  SELECT 13, 'Nexis.com' FROM DUAL UNION ALL     
  SELECT 14, 'American Bar Assoc' FROM DUAL UNION ALL     
  SELECT 31, 'LN Europe - LN Professional' FROM DUAL UNION ALL     
  SELECT 34, 'LN Europe - LN Alert Personal' FROM DUAL UNION ALL     
  SELECT 35, 'LN Europe -- LN Alert' FROM DUAL UNION ALL     
  SELECT 37, 'LN Direct Advance' FROM DUAL UNION ALL     
  SELECT 40, 'LN Europe -- LN Executive' FROM DUAL UNION ALL     
  SELECT 50, 'Political Universe' FROM DUAL UNION ALL     
  SELECT 58, 'Generic XML Gateway' FROM DUAL UNION ALL     
  SELECT 69, 'Rosetta' FROM DUAL UNION ALL     
  SELECT 74, 'Practice Area Pages' FROM DUAL UNION ALL     
  SELECT 75, 'LNU for Development Professionals' FROM DUAL UNION ALL     
  SELECT 210, 'OLD LN Intranet Publisher' FROM DUAL UNION ALL     
  SELECT 230, 'LN Web Publisher' FROM DUAL UNION ALL     
  SELECT 231, 'LN Intranet Publisher' FROM DUAL UNION ALL     
  SELECT 255, 'CUI XML Gateway' FROM DUAL UNION ALL     
  SELECT 23100, 'Science Direct' FROM DUAL) PRODID     
ON ALERTS.PRODUCT_ID = PRODID.PRODUCT_ID     
LEFT JOIN     
  (SELECT 6 AS PRODUCT_ID, 774 AS SUB_PRODUCT_ID,'LexisNexis Academic Adaptation' AS SUB_PRODUCT_NAME from DUAL UNION ALL     
  SELECT 8, 481,'Research' from DUAL UNION ALL     
  SELECT 14, 522,'LexisNexis Dossier' from DUAL UNION ALL     
  SELECT 14, 797,'Prospect Portfolio' from DUAL UNION ALL     
  SELECT 51, 759,'Web Services Kit - Rosetta' from DUAL UNION ALL     
  SELECT 69, 481,'Rosetta' from DUAL UNION ALL     
  SELECT 69, 644,'Australia Legal' from DUAL UNION ALL     
  SELECT 69, 645,'Canada Legal' from DUAL UNION ALL     
  SELECT 69, 646,'France Legal' from DUAL UNION ALL     
  SELECT 69, 648,'Germany Legal' from DUAL UNION ALL     
  SELECT 69, 652,'New Zealand Legal' from DUAL UNION ALL     
  SELECT 69, 654,'Lexis Library' from DUAL UNION ALL     
  SELECT 69, 758,'Nexis' from DUAL UNION ALL     
  SELECT 69, 762,'Austria Legal' from DUAL UNION ALL     
  SELECT 69, 811,'Lexis PSL' from DUAL UNION ALL     
  SELECT 69, 817,'Nexis Direct' from DUAL UNION ALL     
  SELECT 69, 830,'India Legal' from DUAL UNION ALL     
  SELECT 69, 831,'Malaysia Legal' from DUAL UNION ALL     
  SELECT 69, 842,'Web Product Targeting Specific Content A' from DUAL UNION ALL     
  SELECT 69, 845,'Tolley Guidance' from DUAL UNION ALL     
  SELECT 69, 846,'Practical Guidance AU' from DUAL UNION ALL     
  SELECT 69, 847,'Practical Guidance NZ' from DUAL UNION ALL     
  SELECT 69, 866,'Quicklaw Practice Advisor' from DUAL UNION ALL     
  SELECT 69, 880,'Asia Practical Guidance' from DUAL UNION ALL     
  SELECT 74, 764,'LexisNexis Insurance Compliance' from DUAL UNION ALL     
  SELECT 74, 765,'LexisNexis Tax Center' from DUAL UNION ALL     
  SELECT 78, 780,'Total Patent' from DUAL UNION ALL     
  SELECT 79, 865,'Nexis Analyzer' from DUAL UNION ALL     
  SELECT 231, 664,'LNP Editor' from DUAL UNION ALL     
  SELECT 231, 870,'LNP Express Editor' from DUAL UNION ALL     
  SELECT 720, 723,'LexisNexis Portal Component: Enduser' from DUAL UNION ALL     
  SELECT 720, 724,'LexisNexis Portal Component: Admin' from DUAL UNION ALL     
  SELECT 838, 840,'Lexis Diligence' from DUAL) SUBPRODID     
ON ALERTS.PRODUCT_ID = SUBPRODID.PRODUCT_ID     
AND ALERTS.SUB_PRODUCT_ID = SUBPRODID.SUB_PRODUCT_ID     
LEFT JOIN      
  (SELECT 1 AS RUN_SCHEDULE_ID, 'On Demand' AS RUN_SCHEDULE_DESC FROM DUAL UNION ALL     
  SELECT 2, 'Intra-day Business Days' FROM DUAL UNION ALL     
  SELECT 3, 'Daily' FROM DUAL UNION ALL     
  SELECT 4, 'Business Days' FROM DUAL UNION ALL     
  SELECT 5, 'Weekly' FROM DUAL UNION ALL     
  SELECT 6, 'Monthly' FROM DUAL UNION ALL     
  SELECT 7, 'Intra-day daily' FROM DUAL UNION ALL     
  SELECT 8, 'Saved Search' FROM DUAL UNION ALL     
  SELECT 10, 'Bi-Weekly' FROM DUAL) SCHEDULEID     
ON ALERTS.RUN_SCHEDULE = SCHEDULEID.RUN_SCHEDULE_ID     
LEFT JOIN     
  (SELECT 1 AS OWNER_STATUS_ID, 'Active' AS OWNER_STATUS_DESC FROM DUAL UNION ALL     
  SELECT 2, 'Locked' FROM DUAL UNION ALL     
  SELECT 3, 'Expired' FROM DUAL) OWNERSTATUS     
ON ALERTS.BILLGROUP_STATUS = OWNERSTATUS.OWNER_STATUS_ID     
LEFT JOIN     
  (SELECT 1 AS ALERT_STATUS_ID, 'Active' AS ALERT_STATUS_DESC FROM DUAL UNION ALL     
  SELECT 2, 'Locked' FROM DUAL UNION ALL     
  SELECT 3, 'Expired' FROM DUAL UNION ALL     
  SELECT 4, 'Deleted' FROM DUAL UNION ALL     
  SELECT 5, 'Suspended' FROM DUAL) ALERTSTATUS     
ON ALERTS.ALERT_STATUS = ALERTSTATUS.ALERT_STATUS_ID     
LEFT JOIN     
  (SELECT 0 AS DEL_DEST_ID, 'Email' AS DEL_DEST_DESC FROM DUAL UNION ALL     
  SELECT 1, 'Enhanced Email' FROM DUAL UNION ALL     
  SELECT 2, 'Fax' FROM DUAL UNION ALL     
  SELECT 3, 'SAP' FROM DUAL UNION ALL     
  SELECT 4, 'Download' FROM DUAL UNION ALL     
  SELECT 5, 'Attached Print' FROM DUAL UNION ALL     
  SELECT 6, 'n/a' FROM DUAL UNION ALL     
  SELECT 7, 'n/a' FROM DUAL UNION ALL     
  SELECT 8, 'Web Download' FROM DUAL UNION ALL     
  SELECT 9, 'FTP' FROM DUAL) DELDES     
ON ALERTS.DELIVERY_DESTINATION_TYPE = DELDES.DEL_DEST_ID     
     
WHERE 1=1     
    
and SUBPRODID.SUB_PRODUCT_NAME = 'Web Product Targeting Specific Content A'
'''

#alert = pd.read_sql(query,con=conn)
#conn.close()

'''get raw data from the shared folder'''
alert_data = sys.path[0] + '\\pqs_raw.xlsx'
alert = pd.read_excel(alert_data,engine="openpyxl")

'''Get a list of users with active alert created since 2018'''
alert.to_pickle(sys.path[0]+'\\alert_raw.pkl')
alert_raw = pd.read_pickle(sys.path[0]+'\\alert_raw.pkl')
df_criteria = alert_raw[alert_raw['ALERT_STATUS_DESC']=='Active'].groupby('WEB_ID')['ALERT_CREATION_DATE'].min().reset_index()

df_criteria['ALERT_CREATION_DATE'] = pd.to_datetime(df_criteria['ALERT_CREATION_DATE']).dt.date

# create date between 2018 and the end of previous month
user_list = df_criteria['WEB_ID'][(df_criteria['ALERT_CREATION_DATE']>=datetime.date(2018,1,1)) & (df_criteria['ALERT_CREATION_DATE']<datetime.date(yr,mth,1))].to_list()

'''Get all the alert for the above users and save to csv'''
alert_report = alert_raw[alert_raw['WEB_ID'].isin(user_list)]
alert_report.to_csv(sys.path[0]+'\\alert_report.csv',index=False)

'''Get No.users by week and month, week commencing on Sundays and export to csv'''
# create date between 2018 and the end of previous month
df_report = df_criteria[(df_criteria['ALERT_CREATION_DATE']>=datetime.date(2018,1,1)) & (df_criteria['ALERT_CREATION_DATE']<datetime.date(yr,mth,1))].copy()
df_report['month'] = pd.to_datetime(df_report['ALERT_CREATION_DATE']).dt.month
df_report['year'] = pd.to_datetime(df_report['ALERT_CREATION_DATE']).dt.year
df_report['YR_MN'] = df_report['ALERT_CREATION_DATE'].apply(lambda x: x.strftime('%Y-%m'))
df_report['Sunday_wc'] = df_report['ALERT_CREATION_DATE'].apply(lambda x: x - timedelta(days = x.weekday()+1))

week_summary = df_report.groupby('Sunday_wc')['WEB_ID'].nunique().reset_index()
week_summary.to_csv(sys.path[0]+'\\week_summary.csv',index=False)

month_summary = df_report.groupby('YR_MN')['WEB_ID'].nunique().reset_index()
month_summary.to_csv(sys.path[0]+'\\month_summary.csv',index=False)
