import cx_Oracle
import pandas as pd
import csv
import datetime as dt
from datetime import date
#import win32com.client
from pandas import ExcelWriter
import os
import sys
from sqlalchemy.engine import create_engine
DIALECT = 'oracle'
SQL_DRIVER = 'cx_oracle'
USERNAME = 'username' 
PASSWORD = 'password' 
HOST = 'host'
PORT = 1521
SERVICE = 'service'
ENGINE_PATH_WIN_AUTH = DIALECT + '+' + SQL_DRIVER + '://' + USERNAME + ':' + PASSWORD +'@' + HOST + ':' + str(PORT) + '/?service_name=' + SERVICE

engine = create_engine(ENGINE_PATH_WIN_AUTH)
conn_base=engine.connect()

today = int(date.today().strftime('%Y%m'))
#period = input('enter period')#YYYYMM
period = str(today - 1)
query_base = """
/* CS CURRENT ALLOCATION REPORT
This query fetches allocation and active subscription details for each account allocated to a CS Team.
The report provides a detailed follow-up for the accounts allocated via the CS Proposed Allocations report

04.06.20 - RT: changed logic to only look at ACV value, upon David Smith request
 
FORMATS:
:reporting_year: YYYY - used to fetch invoiced values for the year
:reporting_period: YYYYMM - used to fetch ACV period end values for the reporting period
*/
 
/*CS details - Currently allocated Sales and CS Teams */
WITH cs_details AS
(SELECT DISTINCT
          alloc.team team,
          alloc.repcode repcode,
          alloc.fullname fullname,
          alloc.segment SEGMENT,
          alloc.customer customer,
          alloc.custname custname,
          alloc.city,
          alloc.postcode,
          alloc.region,
          alloc.country,
          alloc.account,
          alloc.accountname,
          alloc.accstatus,
          csalloc.cslogin,
          csalloc.csname,
          csalloc.csteam
    FROM 
    (select distinct
                    case when  c.provider_customer_key <> BA.PAR_OU_ID then CA.ROW_ID else c.provider_customer_key end as customer,
                    case when c.provider_customer_key <> BA.PAR_OU_ID then  CA.NAME else c.customer end as custname,
                    a.provider_account_key account,
                    a.account_name accountname,
                    fa_accnt.account_status accstatus,
                    c.customer_segment segment,
                    fa_accnt.team as team,
                    fa_accnt.repcode repcode,
                    fa_accnt.fullname fullname,
                    addrs.addr_5 AS region,
                    addrs.addr_4 AS city,
                    addrs.post_code_r AS postcode,
                    addrs.addr_6 AS country,
                     CASE  WHEN 
                     (
                        CASE
                            WHEN  fa_accnt.repcode = 'CL' THEN NULL  ELSE  fa_accnt.repcode  END
                            ) IS NOT NULL 
                        THEN 
                            COUNT(DISTINCT (CASE WHEN  fa_accnt.repcode = 'CL' THEN NULL ELSE  fa_accnt.repcode END)) OVER (PARTITION BY c.provider_customer_key)
                             END AS custrepcount
                from pdl.plu_vw_account a
                join pdl.plu_vw_customer c on a.customer_id = c.customer_id
                INNER JOIN pdl.CUK_S_ORG_EXT CUST on CUST.ROW_ID = c.provider_customer_key AND CUST.SYS_CURRENT_FLG = 'Y'
                INNER JOIN pdl.CUK_S_ORG_EXT_XM XM ON a.provider_account_key = XM.ATTRIB_02 AND XM.SYS_CURRENT_FLG = 'Y'
                INNER JOIN pdl.CUK_S_ORG_EXT BA ON BA.ROW_ID = XM.PAR_ROW_ID AND BA.SYS_CURRENT_FLG = 'Y' and BA.X_LNUK_PR_LEGACY_ID = XM.ROW_ID
                INNER JOIN pdl.CUK_S_ORG_EXT CA ON CA.ROW_ID = BA.PAR_OU_ID AND CA.SYS_CURRENT_FLG = 'Y'
                LEFT JOIN pdl.gen_r_customer_delivery cd ON cd.customer_account = a.provider_account_key and cd.SYS_CURRENT_FLG = 'Y' 
                LEFT JOIN pdl.gen_r_names_addresses addrs ON addrs.address_ptr = cd.address_ptr AND addrs.sys_current_flg = 'Y'
                 left JOIN (
                                    SELECT
                                        xaccnt.accnt_legcy_id,
                                        p.postn_rep_cd as repcode,
                                        p.postn_team            AS team,
                                        p.emp_name              AS fullname,
                                         xaccnt.ACCNT_STAT as account_status
                                    FROM
                                        law.f_fin_accnt     faccnt
                                        INNER JOIN law.d_fin_accnt_x   xaccnt ON faccnt.row_wid = xaccnt.row_wid
                                        INNER JOIN law.d_position      p ON p.row_wid = xaccnt.pos_pr_wid
                                ) fa_accnt ON a.provider_account_key = fa_accnt.accnt_legcy_id
                                
               -- left join law.d_customer_x xcust on xcust.integration_id = c.provider_customer_key
                    where  1=1 
                       -- and fa_accnt.repcode   not in ('MIAA', 'MIAC')
                       -- and fa_accnt.fullname not in ('M LEX', 'Team RepCode')
                       -- Evelyn: added in March 2022
                        and fa_accnt.team not in ('MI-MI','MI-ES','Miscellaneous')
                        and fa_accnt.repcode is not null
    
    ) alloc
            LEFT JOIN (select distinct
                acc.accnt_legcy_id as accnum,
                pos.emp_login as cslogin,
                pos.emp_name as csname,
                case when pos.postn_team = 'Online Training' then 'CSD'
                when pos.postn_team = 'Training' then 'CSF'
                -- Evelyn: added in Mar 2022 upon Sarah's request
                when pos.emp_login = 'HOPWOODJ' then 'CSF'
                else pos.postn_team end as csteam
            from
                law.f_fin_accnt facc
                inner join law.d_fin_accnt_x   acc  on facc.row_wid = acc.row_wid
                inner join law.d_position  pos on pos.row_wid = facc.pos_pas_wid and  pos.row_wid = acc.pos_pas_wid
            where 1=1
                  --and pos.actv_flg = 'Y'
                  --temporary
                and (pos.actv_flg = 'Y' or acc.accnt_legcy_id in ('CLIF5177','BRIC5021','SIMM5106','REYN5056','SHEL5068','TREA5014','LOND6248','GOOD5031','NORW5024','LOND5225','SHER5390','3VER5003','MONC5011','MAES5002','OFCO5028','MISS7069','THEC8664','MRMA5278','THEI5077','HOME5219','UNIV8042','HAUS5013','QUAD5033','LOND2334','FOOD5025','CAFC5024','GOVE5075','WEAT0005','THEU5026','HIGH5282','HAUS5012','MIDD5192','KING5681','HAUS5014','REYN5064','LBHA0021','SUPR5081','UNIV7647','UNIV5165','RLAT5000','2DRJ5000','OFCO5026','CLER5038','TWOE5000','UNIV6931','2KIN5002','LOND5137','SHER5010','AWHA5003','FALK5027','EMBA5000','RAYD5004','CHAM5250','MEDI5111','MONO5000','GRAN0028','PUMP5001','PENS5064','BANQ5005','INTE6581','LOND5358','THAM5066','INST5083','BLOU5001','BRIT5260','BIRK0002','LOND5148','CHBR5000','PORT5020','CURR5003','HAUS5007','NEVE5002','COUN5257','LEED5024','HENR5042','DIAG5027','ADMI5010','GEOF5036','HODG5014','JUDG5069','SEDG5026','ESSE5223','SELB5016','SHEL5302','AMIF5004','LAND5195','CLOI5003','FIVE5015','MILT5010','IVOR5004','UNIV5838','RJWA5002','POLY5008','JOEL5000','BRIT5433','GREE5069','ERSK5001','ALIS5014','SCHL0047','GERA5013','SERJ5000','DBRA5001','BRIC5008','JONA5024','THEO5050','UNIV5228','GRAY5003','ELEC5032','HEAL5115','UNIV6938','7BED5002','UNIV5116','FINA5267','PUMP5003','29BE5000','CROW5370','DEVE5004','PHIL5038','ATYR5000','CHAM5181','INNS5006','JOHN5379','EYTO5000','HARD5016','MATR5004','ATTW5016','PATR5017','MONC5000','CHAM5004','ACCO5010','HARV5006','FIEL5043','WJOH5001','KING5332','MBUR5000','GRBR5005','LIBR5076','LOND5135','9GOU5000','ENTE5007','PCRA5000','LIBR5097','OLDS5003','WILB0004','CHAR5137','NING5000','LHUT5000','LIBR5073','IMIL5002','ALPR5001','COMC5000','LAWS5030','DOUG5017','FOUN5000','NEVI5029','ASGR5009','CHAM5001','HOUS5017','BLAC5326','MICH5040','FINA5014','MIDD5014','INNE5031','GRAY5017','LOGI5020','WEIL5000','REYN5006','LINC5000','SIMM5022','BPPL5005','CLIF5020','COLL5143','TREA5003','THEC5067'
))
                  and facc.delete_flg = 'N'
                  and acc.accnt_legcy_id <> 'Unspecified') csalloc
              ON csalloc.accnum = alloc.account
            WHERE 1 = 1),
 
/* Last trained date for the account.  Session - Inhouse, Undertake Training, Status = Done*/
cs_last_trained AS
(SELECT  
        DISTINCT ACC.accnt_legcy_id AS ACCOUNT,
        LAST_VALUE(dt.dt) OVER (PARTITION BY  ACC.accnt_legcy_id ORDER BY  dt.dt ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) last_trained
FROM     law.f_activity FACT
          JOIN law.d_activity act ON act.row_wid     = FACT.row_wid
          JOIN  law.d_position pos ON  pos.row_wid     = FACT.pos_pr_wid
          JOIN  law.d_fin_accnt_x ACC ON  ACC.row_wid = FACT.fa_wid
          JOIN  law.d_date dt ON dt.row_wid      = FACT.dt_start_wid
WHERE 1=1
           AND pos.postn_team in ( 'Online Training' , 'Training')
          AND FACT.delete_flg = 'N'
          AND FACT.bu_pguid IN ('UK', 'Unspecified')
          AND act.act_type like 'Sess%'
         -- AND ACC.accnt_legcy_id = 'GATE5009'
          AND  act.act_status = 'Done'
          AND  (act.act_name like 'Under%' or act.act_name like 'under%' or act.act_name like  'Train Users%' )
          AND act.act_format NOT IN ('Introduction Meeting','Meeting')),
           
         
/* Multi-year deal, MYD Details and CAE flags - taking values associated to the subscription ending soonest for each account*/
MYD AS
(SELECT
        ACCOUNT,
        myd_flg,
        myd_yr,
        myd_trm,
        cae_flg,
        dt_end
 FROM
        (SELECT DISTINCT
                ACC.accnt_legcy_id   AS ACCOUNT,
                subrev.myd_flg,
                subrev.myd_yr,
                subrev.myd_trm,
                subrev.cae_flg,
                subrev.dt_end,
                row_number() OVER(PARTITION BY ACC.accnt_legcy_id ORDER BY subrev.dt_end) AS earliest_ending
        FROM
                law.f_invoice_ln    inv
                 JOIN law.d_product       prod ON inv.prod_wid = prod.row_wid
                 JOIN law.d_subscr_rev    subrev ON subrev.row_wid = inv.subr_wid
                 JOIN law.d_fin_accnt_x   ACC ON ACC.row_wid = inv.fa_wid
                 JOIN (
                            SELECT distinct
                                prod.prod_cd,
                                CASE
                                    WHEN prod.fin_report_cd != 'Unspecified' THEN 'ON'
                                    WHEN prod.fin_report_cd = 'Unspecified' AND prod.prod_medium_cd = 'ON'
                                         AND (
                                            --Product Code Detail Criteria
                                              ( prod.prod_cd LIKE 'LEGM%'
                                                     OR prod.prod_cd LIKE 'PSLC%'
                                                     OR prod.prod_cd LIKE 'PSLD%'
                                                     OR prod.prod_cd LIKE 'TSO%'
                                                     OR prod.prod_cd LIKE 'TOLG%'
                                                     OR prod.prod_cd LIKE 'TOLL%'
                                                     OR prod.prod_cd LIKE 'MELM%' )
                                                       OR prod.prod_cd in ('BXSUBS','IHSUBS','VASUBS','VCSUBS','VRSUBS','VVSUBS','WASUBS','WCSUBS','WDSUBS','WESUBS', --webinars
                    'WFSUBS','WISUBS','WJSUBS','WNSUBS','WOSUBS','WPSUBS','WRSUBS','WSSUBS','WTSUBS','WUA','WVSUBS','WWSUBS','WXSUBS')
             
                                             -- Product Family Criteria
                                                    OR ( spr_products.spr_product_family IN ('LexisLibrary','Core', 'Smart Forms', 'Middle East Online'/*, 'Lexis Smart Bespoke'*/, 'PSL/LPA','LexisPSL'  ) ) )
                                    THEN     'ON' ELSE   'OA'  END AS salesops_medcodeclass
                             FROM law.d_product prod
                             INNER JOIN
                                (SELECT
                                    TRIM(provider_product_key) AS prod_code,
                                    spr_product_family
                                FROM
                                    pdl.plu_vw_product
                                WHERE nvl(spr_exclusion,'N') !='Y'
                                ) spr_products ON spr_products.prod_code = prod.prod_cd)
                                 sales_ops_spr ON sales_ops_spr.prod_cd = prod.prod_cd
            WHERE
                    1 = 1
                    AND inv.delete_flg = 'N'
                    AND ( inv.bu_pguid IN ( 'UK',  'Unspecified') )
                    and sales_ops_spr.salesops_medcodeclass = 'ON'
                    AND subrev.sub_stat in ('Active', 'Cancel At End', 'Complete at End')
                    AND subrev.delete_flg = 'N')
 WHERE earliest_ending = 1),
  
/* ACV value -  not filtering for salesops medcode class as
none of the excluded product codes appear in ACV*/
ACV AS
(SELECT
        customer,
        lbu_acc,
        PERIOD,
        SUM(period_end_value) AS lbu_period_end_value
FROM
          (SELECT
                cus.integration_id      AS customer,
                fa.accnt_legcy_id             AS lbu_acc,
                acv.per_wid                   AS PERIOD,
                prod.prod_cd                  AS product_code,
                prod.prod_famly               AS prod_family,
                prod.prod_medium_cd           AS prod_medium_code,
                SUM( acv.doc_period_end_val*rate.exch_rate)  AS period_end_value
          FROM law.f_fin_acv acv
                   JOIN law.d_fin_accnt_x fa ON acv.fa_wid = fa.row_wid
                   JOIN law.d_product prod ON prod.row_wid = acv.prod_wid
                   JOIN law.d_customer_x cus ON acv.cus_wid =cus.row_wid
                   JOIN law.d_fx_rate_m     rate ON acv.fx_wid = rate.fx_wid
          WHERE 1 =1
                 AND acv.per_wid = {0}
                 AND  rate.exch_cd =  'PLU - Annual'
                 AND rate.curcy_cd_to = 'GBP'
          GROUP BY
                cus.integration_id,
                fa.accnt_legcy_id,
                acv.per_wid,
                prod.prod_cd,
                prod.prod_famly,
                prod.prod_medium_cd
          ) acv
WHERE 1=1
GROUP BY
        customer,
          lbu_acc,
          PERIOD),

-- Jan 22 change
/* New Business 
roll up to account level: if an account only has New Bisiness acv records, then New Business; 
if an account has both New Business and othe ytd_class acv records, then New Product Family;
otherwise blank*/
nb as (select customer,lbu_acc,
case when nb > 0  and exist >0 then 'New Product Family'
when nb > 0 and exist = 0 then 'New Business'
end new_biz_deals
from(
select customer,lbu_acc,
sum(new_biz) nb,
sum(existing) exist
from(
SELECT
                cus.integration_id   AS customer,
                fa.accnt_legcy_id    AS lbu_acc,
                case when dacv.ytd_class = 'New Business'  then 1 else 0 end new_biz,
                case when dacv.ytd_class != 'New Business' then 1 else 0 end existing
            FROM
                law.f_fin_acv       acv
                INNER JOIN law.d_fin_accnt_x   fa ON acv.fa_wid = fa.row_wid
                INNER JOIN law.d_product       prod ON prod.row_wid = acv.prod_wid
                INNER JOIN law.d_customer_x    cus ON acv.cus_wid = cus.row_wid
                INNER JOIN law.d_fin_acv dacv on acv.row_wid = dacv.row_wid
            WHERE
                1 = 1
                AND acv.per_wid = {0}            
                and fa.accnt_legcy_id != 'Unspecified'
                and prod.prod_cd not in ('MLEXMI','MLEXSB','L360UK','L360IP','L360P') -- because the premium news tracker file has LAW360 IP and LAW360 PUlse as types as well
)
group by customer,lbu_acc

) ),
 
/*RISK Level - requested by Sarah in May 2022
roll up at account level -  High at account level if there's at least one High active risk; Low risk if there's no high active risk agreements
used to be just flag of Y and N based on whether there's  agreement with active risk status
*/
RISK as
(SELECT
    ACCOUNT,
   -- CASE WHEN SUM(risk_num) > 0 THEN 'High' ELSE 'Low' END AS risk_lvl
   -- new change in Apr 2022: flag print only risk
    CASE WHEN SUM(risk_num) > 0 and sum(online_prod) > 0 THEN 'High' 
    when SUM(risk_num) = 0 and sum(online_prod) > 0 then 'Low'
    ELSE '' END AS risk_lvl,
    case when sum(online_prod) > 0 then '' else 'Y' end as PR_only_risk
FROM
    (SELECT
                    ACC.accnt_legcy_id   AS ACCOUNT,
                    ACC.accnt_name       AS accountname,
                    PER.yr_num,
                    prod.prod_cd,
                    prod.fin_report_cd,
                    prod.prod_medium_cd,
                    prod.prod_famly,
                    agrrev.risk_level,
                    agrrev.risk_status,
                    agrrev.risk_reason,
                    -- new change in Mar 2022: active high risk will be shown as high, all active risk agreements are low then low
                    CASE WHEN agrrev.risk_level = 'High' THEN 1 ELSE 0 END AS risk_num,
                    -- new change in Apr 2022: flag print only risk
                    case when prod.prod_medium_cd = 'ON' then 1 else 0 end as online_prod
        FROM
                law.f_invoice_ln    inv
                 JOIN law.d_product       prod ON inv.prod_wid = prod.row_wid
                 JOIN law.d_subscr_rev    subrev ON subrev.row_wid = inv.subr_wid
                 JOIN law.d_fin_accnt_x   ACC ON ACC.row_wid = inv.fa_wid
                 JOIN law.d_period_dt     PER ON inv.dt_inv_wid = PER.per_dt_wid
                 JOIN law.d_agree_rev     agrrev ON agrrev.row_wid = inv.agr_wid
                 JOIN
                        (SELECT
                            TRIM(provider_product_key) AS prod_code, spr_product_family
                        FROM pdl.plu_vw_product
                        WHERE nvl(spr_exclusion,'N') !='Y' ) spr_prod ON spr_prod.prod_code = prod.prod_cd
        WHERE
                1 = 1
                AND inv.delete_flg = 'N'
                AND ( inv.bu_pguid IN ( 'UK',  'Unspecified') )
                AND PER.calendar = 'Avatar 445'
                --AND acc.accnt_legcy_id = 'LAWR5017'
                AND subrev.sub_stat IN ('Active', 'Cancel At End', 'Complete at End')
               -- AND prod.prod_medium_cd = 'ON'
                AND subrev.delete_flg = 'N'
                 -- only get active risk for the flag
                and agrrev.risk_status = 'Active') risk
GROUP BY ACCOUNT
       )
 
SELECT det.*
FROM
        (SELECT
                cd.customer,
                cd.custname,
                cd.ACCOUNT,
                cd.accountname,
             --   cd.accstatus,
                cd.postcode,
                case when trim(cd.country) = 'UK' then REGEXP_SUBSTR( cd.postcode, '[[:alpha:]]+') end AS postcode_area,
                cd.city,
                cd.country,
                cd.fullname,
                cd.repcode,
                cd.team,
                cd.csteam,
                cd.cslogin,
                cd.csname,
                cd.SEGMENT,
                nb.new_biz_deals,
                NVL(SUM(acv.lbu_period_end_value) over (partition by cd.customer),0) as cust_on_spend,                        
                nvl(SUM(acv.lbu_period_end_value),0) AS lbu_on_spend,
                myd.myd_flg,
                myd.myd_yr,
                myd.myd_trm,
                myd.dt_end,
                myd.cae_flg,
            --    myd.sub_stat,
                risk.risk_lvl,
                risk.PR_only_risk,
                clt.last_trained
        FROM cs_details cd
                LEFT JOIN cs_last_trained  clt ON clt.ACCOUNT =  cd.ACCOUNT
                LEFT JOIN myd ON myd.ACCOUNT = cd.ACCOUNT
                LEFT JOIN acv ON acv.lbu_acc = cd.ACCOUNT AND acv.customer = cd.customer
                LEFT JOIN nb ON nb.lbu_acc = cd.ACCOUNT AND nb.customer = cd.customer
                LEFT JOIN risk ON cd.ACCOUNT = risk.ACCOUNT
                --where cd.account = 'BARB5025'
                --where   cd.customer = '1-114UD3P'
        GROUP BY
                cd.customer,
                cd.custname,
                cd.ACCOUNT,
                cd.accountname,
           --     cd.accstatus,
                cd.postcode,
                cd.city,
                cd.country,
                cd.fullname,
                cd.repcode,
                cd.team,
                cd.csteam,
                cd.cslogin,
                cd.csname,
                cd.SEGMENT,
                myd.myd_flg,
                myd.myd_yr,
                myd.myd_trm,
                myd.cae_flg,
           --     myd.sub_stat,
                myd.dt_end,
                clt.last_trained,
               acv.lbu_period_end_value,
               nb.new_biz_deals,
               risk.risk_lvl,risk.PR_only_risk) det
where 1=1
-- Excluding Closed rep codes, accoutns with no team cs assigned
-- ACV doesn't see cancellations until the following month -> by excluding null MYD we exclude cancellations (not excluding as of Jan 21 upon David's request...)
--     det.repcode != 'CL'
--and det.csteam is not null
-- and det.lbu_on_spend != 0
--  and det.myd_flg is not null
-- and det.ACCOUNT = 'DOUG5164'
   
""".format(period)
df_base = pd.read_sql(query_base, con=conn_base)
df_base.columns = df_base.columns.str.strip().str.upper()


output_base =  sys.path[0]+'\\CS BASE DATA.xlsx'
df_base.to_excel(output_base, index=False)
conn_base.close()

# test : expect to see 1 - no duplication for accounts 
cs_data = sys.path[0] + '\\CS BASE DATA.xlsx'
df_base = pd.read_excel(cs_data)
acct_dup_test = (df_base
        .groupby('ACCOUNT')['LBU_ON_SPEND'].count()
        .reset_index())['LBU_ON_SPEND'].max()
print('No duplication in the financial base:',acct_dup_test == 1)





