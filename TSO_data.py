'Note: Teradata has migrated to Redshift'
print("import modules")
#import teradata
import psycopg2
import csv
import pandas as pd
import datetime as dt
import os
import shutil
import win32com.client as win32
from openpyxl import Workbook

print("move file to archive")
folder = r'\\Galileo\Public\Legal Intelligence\Customer Segmentation\BA\TSO Contact List Data'
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    dest = r'\\Galileo\Public\Legal Intelligence\Customer Segmentation\BA\TSO Contact List Data\TSO data archive'
    try:
        if os.path.isfile(file_path):
            shutil.move(file_path,dest)
           # os.unlink(file_path)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)

#print("connect to teradata")
print("connect to redshift")
#host,username,password = 'HOST','UID', 'PWD'
#udaExec = teradata.UdaExec (appName="test", version="1.0", logConsole=False)
#with udaExec.connect(method="odbc",system="TDP0", username="mutsomx",
#                            password="mutsomx14", driver="Teradata") as session:
#with udaExec.connect(method="odbc",system="TDP0", username="chenyx",
 #                           password="chenyx9", driver="Teradata") as session:

conn = psycopg2.connect(dbname= 'gdw', 
      host = 'prod-gdw-database.business.aws.lexisnexis.com', 
      port= '5439', 
      #user= 'chenyx', 
	  user = 'gopimeng',
      #password= '!Uf2KfxQ'
	  password = r'z%x4qbeX'
	  )
query ="""
    select
 LBU_ACCT_ID
--, USER_SIGNON_ID
, min(USER_FULL_NAME)  as USER_FULL_NAME
, min(web_user_last_name) AS LAST_NAME
, min(web_user_first_name) AS FIRST_NAME
, EMAIL_ADDRESS
, max(begin_dt) AS CONTENT_ST_DTE
, max(end_dt) as MaxContentEndDate
--, min(cc_intrnl_user_ind) cc_intrnl_user_ind
--, min(platform_cd)  platform_cd
, MIN(USR_CR_DT) AS minUsr_CreatedDte
, Max(web_id_cancel_dt) as minUsr_CancelDate



FROM (
SELECT	 CON_WEB_GRP.web_user_grp_id
		, CON_WEB_GRP.content_id
		, CON_WEB_GRP.actv_ind as WEBGRP_ACTV
		, CON_WEB_GRP.create_dt as WEBGRP_CR_DT
		, CON_WEB_GRP.inactv_dt as WEBGRP_INACTV_DT
		, CON_WEB_GRP.dw_gen_ind
	--	, SUBCON_CUR.content_id
		, SUBCON_CUR.content_descr
		, SUBCON_CUR.web_subscrp_id
		, SUBCON_CUR.web_prdct_cd
		, SUBCON_CUR.web_prdct_grp_cd
		, SUBCON_CUR.content_name
		, SUBCON_CUR.begin_dt
		, SUBCON_CUR.end_dt
		, SUBCON_CUR.promo_mkt_id
		, SUBCON_CUR.content_promo_type_cd
		, SUBCON_CUR.max_user_nbr
		, SUBCON_CUR.content_type_cd
		, SUBCON_CUR.local_content_id
		, SUBCON_CUR.actv_ind as SUBCON_ACTV
		, SUBCON_CUR.create_dt as SUBCON_CR_DT
		, SUBCON_CUR.inactv_dt as SUBCON_INACTV
		, SUBCON_CUR.dw_mod_dt
--		, CON_SRC_PKG.content_id
		, CON_SRC_PKG.src_pkg_content_id
		, CON_SRC_PKG.actv_ind as CON_SCRPK_ACTV

	--	, PKG_CUR.src_pkg_content_id
		, PKG_CUR.src_pkg_name
		, PKG_CUR.src_pkg_descr
		, PKG_CUR.local_pkg_id


		, WUWB_GRP.web_user_id
--		, WUWB_GRP.web_user_grp_id

		, grp.web_user_grp_name
		, grp.web_subscr_org_cd
		, grp.actv_ind as GRP_ACTV


	, CMU.LBU_ACCT_ID
	, CMU.user_signon_id
	, CMU.USER_FULL_NAME
	, CMU.web_user_last_name
	, CMU.web_user_first_name
	, CMU.create_dt as USR_CR_DT
	, CMU.web_id_cancel_dt
	, CMU.actv_ind as USR_ACTV
	, CMU.EMAIL_ADDRESS
	, CMU.cc_intrnl_user_ind
	, CMU.platform_cd

FROM	BI.content_subscrp_web_user_grp CON_WEB_GRP

INNER JOIN BI.content_subscrp_curr SUBCON_CUR
ON CON_WEB_GRP.content_id = SUBCON_CUR.content_id

inner join BI.content_subscrp_src_pkg CON_SRC_PKG
ON CON_WEB_GRP.content_id = CON_SRC_PKG.content_id

inner join 	BI.src_pkg_curr PKG_CUR
on CON_SRC_PKG.src_pkg_content_id = PKG_CUR.src_pkg_content_id

inner join BI.web_user_web_user_grp WUWB_GRP
ON  CON_WEB_GRP.web_user_grp_id=WUWB_GRP.web_user_grp_id

INNER JOIN           BI.web_user_grp grp
ON CON_WEB_GRP.web_user_grp_id = grp.web_user_grp_id


INNER  JOIN 	(

																											SELECT DISTINCT
																											  USR.WEB_USER_ID
																											, ACU.LBU_ACCT_ID
																											, UPPER(USR.user_signon_id) AS user_signon_id
																											,UPPER(USR.WEB_USER_FIRST_NAME) || ' ' || UPPER(USR.WEB_USER_LAST_NAME) AS USER_FULL_NAME
																											,UPPER(USR.WEB_USER_FIRST_NAME) AS WEB_USER_FIRST_NAME
																											,UPPER(USR.WEB_USER_LAST_NAME) AS WEB_USER_LAST_NAME
																											, USR.create_dt
																											, USR. web_id_cancel_dt
																											, USR.actv_ind
																											, USEM.CMUNCT_MTHD_CD
																											, USEM.EMAIL_ADDRESS
																											, SUB_EXT.platform_cd
																											, USR.cc_intrnl_user_ind
																											FROM
																											BI.WEB_USER_CURR 			USR

																											LEFT JOIN	(select   TCO.WEB_USER_ID
																																				, TCO.CMUNCT_MTHD_CD
																																				, UPPER(TCO.CMUNCT_MTHD_VALUE) AS EMAIL_ADDRESS
																																			FROM bi_pi.WEB_USER_CMUNCT_MTHD		TCO  -- Communication Methods View (to Get Emails and Telephone)
																																			WHERE 1=1
																																				AND TCO.CMUNCT_MTHD_CD IN ('07') -- Email 07 -- TELEPHONE 09
																																				--all records have 'N' indication 06 Dec 2021
																																				-- above bug seems to be fixed 04 Jan 2022
																																				AND TCO.ACTV_IND = 'Y'
																																				AND TCO.CMUNCT_MTHD_VALUE NOT IN ('null')
																																				--and TCO.WEB_USER_ID='24,582,544'
																																				)  USEM

																											ON	 USR.WEB_USER_ID = USEM.WEB_USER_ID
																											INNER JOIN	BI.SUB_ACCT_CURR 			ACU
																											ON	USR.SUB_ACCT_ID = ACU.SUB_ACCT_ID
																											inner join BI.Sub_Acct_Extn_Online_curr SUB_EXT
																													on ACU.sub_acct_id =  SUB_EXT.sub_acct_id
																											WHERE 1=1
																											--and USR.cc_intrnl_user_ind<>'Y' -- Remove Internal Users
																											and SUB_EXT.platform_cd <> 'INTERNAL' -- Remove Internal Accounts
																											  --and USR.WEB_USER_ID='24,582,544'

			) CMU
ON	WUWB_GRP.web_user_id		=	CMU.WEB_USER_ID


INNER JOIN BI.web_user_online_subscrp_curr ATTRGRP_SUB_CURR
ON SUBCON_CUR.web_subscrp_id = ATTRGRP_SUB_CURR.web_subscrp_id
and WUWB_GRP.web_user_id= ATTRGRP_SUB_CURR.web_user_id

WHERE 1=1

 and SUBCON_CUR.end_dt >= current_date -- Only Active Content Sub -- Menu Code
 and SUBCON_CUR.content_promo_type_cd IN ('NA') -- No promotion code Menu content i.e. trials

AND	CMU.WEB_ID_CANCEL_DT >= CURRENT_DATE -- Only Active Users

AND PKG_CUR.local_pkg_id In (
'TSO', -- No Users against this prodcut
'TSOAO'
--'TSE', -- CD Subscription -- Print Product
--'TSAAMW' -- CD Subscription -- Print Product
)   -- For the Local Menu Code ID's for Tolley Seminars
AND CMU.EMAIL_ADDRESS is not null


-- Testing SQL
--AND CMU.LBU_ACCT_ID IN ('HORW5011')
--'BERK5141')
--AND CMU.EMAIL_ADDRESS='IMRAN@BERKELEYACCOUNTANTS.CO.UK'

---AND content_id='2491832'
-- AND CON_WEB_GRP.web_user_grp_id='592006'
 --'590778'


 ) SUB_QRY


 group by   LBU_ACCT_ID
, EMAIL_ADDRESS   """
print("load result to dataframe")
df = pd.read_sql(query,conn)
today = dt.datetime.today().strftime('%d%m%Y')
output_file = r'\\Galileo\Public\Legal Intelligence\Customer Segmentation\BA\TSO Contact List Data\TSO_DATA_{}.csv'.format(
        today)
print("save result to csv")
df.to_csv(output_file, index=False, encoding='utf-8-sig')
#session.close()
conn.close()

#df.workbook=easy_getOptions().setPasswordToOpen("password")
#workbook.easy_getOptions().setPasswordToOpen("password")

print("send email")
outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
# mail.To = 'evelyn.chen@lexisnexis.co.uk'
mail.To = 'joel.falken-smith@lexisnexis.co.uk'
#mail.CC = 'maila.muts0@lexisnexis.co.uk'
mail.CC = 'maila.mutso@lexisnexis.co.uk;jemini.amrat@lexisnexis.co.uk;Greeshma.GopiMenon@lexisnexis.co.uk'
mail.Subject = 'TSO raw data'
mail.Body = 'Please find attached the latest TSO data'
mail.HTMLBody = '<p>Hello Joel,</p><p>Please find attached the latest TSO data.</p><p>Thanks,<br>Evelyn</p>'
attachment  = output_file
mail.Attachments.Add(attachment)
mail.Send()

