''' THE BELOW FETCHES DATA FROM RECON (CHB), GCRM AND LAW. FILES ARE OUTPUTTED IN THE RAW DATA FOLDER
    AND ARE CONSEQUENTLY PROCESSED IN PANDAS
'''

print('import modules')
import cx_Oracle
import pandas as pd
import csv
import datetime as dt
from datetime import date
#import win32com.client
from pandas import ExcelWriter
#import os
import sys

today = date.today().strftime('%d_%m_%y')
print('connecting 12c_dataanalytics')
## CREDIT DAT FROM LAW
dsn_tns_base = cx_Oracle.makedsn('host', '1521', service_name='service')
conn_base = cx_Oracle.connect(user='username', password='password', dsn=dsn_tns_base)

# chambers
print('fetching chambers')
query_chamber = """
select distinct par_row_id customer,
attrib_02 chamber_name,
'Y' chamber_flag
from pdl.cuk_s_org_ext_xm
where sys_current_flg = 'Y'
and lower(attrib_02) like '%chamber%'
"""

df_chamber = pd.read_sql(query_chamber, con=conn_base)
#output_credit =  os.getcwd()+'\\Raw Data\\RAW_credit.csv'
output_chamber = sys.path[0] + f'\\Raw Data\\raw_chambers_{today}.csv'
df_chamber.to_csv(output_chamber, index=False)

#credit
period = input('Enter current period (YYYYMM): ')

query_cy_st = f"""
select distinct per_start_dt from law.d_period_dt where per_wid =  to_char(add_months(to_date({period},'yyyymm'),-11),'yyyymm') and calendar =  'Avatar 445'

"""
cy_st = pd.read_sql(query_cy_st, con=conn_base)
cy_yr_st = cy_st['PER_START_DT'][0].strftime('%Y-%m-%d')

query_py_st = f"""
select distinct per_start_dt from law.d_period_dt where per_wid =  to_char(add_months(to_date({period},'yyyymm'),-23),'yyyymm') and calendar =  'Avatar 445'

"""
py_st = pd.read_sql(query_py_st, con=conn_base)
py_yr_st = py_st['PER_START_DT'][0].strftime('%Y-%m-%d')

print('credit query')
query_credit = """
with sales_ops_product AS
(
        SELECT
            prod.row_wid,
            prod.prod_cd,
            prod.prod_famly,
            prod.prod_name,
            CASE
                WHEN prod.fin_report_cd != 'Unspecified' THEN 'ON'
                WHEN prod.fin_report_cd = 'Unspecified' AND
                prod.prod_medium_cd IN ('MC', 'PR','CD','DI') THEN 'PR'
                WHEN prod.fin_report_cd = 'Unspecified' AND
                prod.prod_medium_cd = 'OA' THEN 'OA'
                WHEN prod.fin_report_cd = 'Unspecified' AND
                prod.prod_medium_cd = 'ON' AND
                (
                --Product Code Detail Criteria
                (prod.prod_cd LIKE 'LEGM%' OR
                prod.prod_cd LIKE 'PSLC%' OR
                prod.prod_cd LIKE 'PSLD%' OR
                prod.prod_cd LIKE 'TSO%' OR
                prod.prod_cd LIKE 'TOLG%' OR
                prod.prod_cd LIKE 'TOLL%' OR
                prod.prod_cd LIKE 'MELM%')
                OR prod.prod_cd IN ('BXSUBS','IHSUBS','VASUBS','VCSUBS','VRSUBS','VVSUBS','WASUBS','WCSUBS','WDSUBS','WESUBS', --webinars
                'WFSUBS','WISUBS','WJSUBS','WNSUBS','WOSUBS','WPSUBS','WRSUBS','WSSUBS','WTSUBS','WUA','WVSUBS','WWSUBS','WXSUBS')
                -- Product Family Criteria
                OR (prod.spr_product_family IN ('LexisLibrary','Core', 'SmartForms', 'Middle East Online','LexisSmart', 'PSL/LPA','LexisPSL'))) THEN 'ON'
            ELSE 'OA'
            END AS salesops_medcodeclass
        FROM law.d_product prod
        WHERE 1=1
            AND (prod.spr_exclusion !='Y')
),
 credit as (
 select accnt_legcy_id,
  sum(CAE_sub) CAE_subs_value,
  sum(active_sub) active_subs_value,
  sum(CY_ON) Credit_CY_ON,
  sum(CY_PR) Credit_CY_PR,
  sum(CY_OA) Credit_CY_OA,
  sum(PY_ON) Credit_PY_ON,
  sum(PY_PR) Credit_PY_PR,
  sum(PY_OA) Credit_PY_OA
  from
  (select credit.accnt_legcy_id,salesops_medcodeclass,fy,SUB_STAT,
  case when salesops_medcodeclass='ON' and fy='cy' then "Invoice Amount" end as CY_ON,
  case when salesops_medcodeclass='PR' and fy='cy' then "Invoice Amount" end as CY_PR,
  case when salesops_medcodeclass='OA' and fy='cy' then "Invoice Amount" end as CY_OA,
  case when salesops_medcodeclass='ON' and fy='py' then "Invoice Amount" end as PY_ON,
  case when salesops_medcodeclass='PR' and fy='py' then "Invoice Amount" end as PY_PR,
  case when salesops_medcodeclass='OA' and fy='py' then "Invoice Amount" end as PY_OA,
  case when salesops_medcodeclass='ON' and SUB_STAT = 'Cancel At End' then "Invoice Amount" end as CAE_sub,
  case when salesops_medcodeclass='ON' and SUB_STAT in ('Active','Cancel At End','Complete at End') then "Invoice Amount" end as active_sub
from(
SELECT
  INV.ROW_WID, acc.ACCNT_LEGCY_ID,prod.prod_cd,sop.salesops_medcodeclass,sub.SUB_STAT,
  INV.INTEGRATION_ID AS "Invoice Line", INV.ORIG_INV_NUM AS "Original Invoice #", INV.DT_INV "Invoice Date",
  F.DOC_AMT AS "Invoice Amount", ORIG.INTEGRATION_ID AS "Original Invoice", ORIG.DT_INV AS "Original Invoice Date",
  case when INV.DT_INV between TO_DATE('{0}', 'YYYY-MM-DD') and (to_date ('{1}','YYYY-MM-DD')-1)
  AND ORIG.DT_INV < TO_DATE('{0}', 'YYYY-MM-DD') then 'py'
  when  INV.DT_INV >= TO_DATE('{1}', 'YYYY-MM-DD') 
  AND ORIG.DT_INV < TO_DATE('{1}', 'YYYY-MM-DD') 
  then 'cy'
  else 'exclude'
  end as fy
FROM
  law.D_INVOICE_LN INV
  INNER JOIN law.F_INVOICE_LN F ON F.ROW_WID = INV.ROW_WID
  INNER JOIN law.D_INVOICE ORIG ON ORIG.ROW_WID = F.IN_ORIG_WID --  if doesn't work, ETL lookup must be incorrect use ORIG.INTEGRATION_ID = INV.ORIG_INV_NUM as a work around
  inner join law.d_fin_accnt_x acc on acc.row_wid = f.fa_wid
  inner join law.d_product prod on prod.row_wid = f.prod_wid
  inner join sales_ops_product sop ON sop.row_wid=prod.row_wid
  left join law.D_SUBSCR_REV sub on sub.row_wid = f.subr_wid
WHERE
  INV.DELETE_FLG = 'N' -- Invoice has not been deleted
  AND INV.DATASOURCE_NUM_ID = 10 -- Only Invoices from Genesis
  AND INV.ORIG_INV_NUM IS NOT NULL
  AND INV.ORIG_INV_NUM <> '         ' -- Looks like Genesis has this value instead of NULL
 /* AND INV.DT_INV >= TO_DATE('2021-01-01', 'YYYY-MM-DD') -- Need to change this to whatever date we are going to use - likely first day of avatar year
  AND ORIG.DT_INV < TO_DATE('2021-01-01', 'YYYY-MM-DD') -- Need to change this to whatever date we are going to use - likely first day of avatar year
  */
  AND INV.DT_INV >= TO_DATE('{0}', 'YYYY-MM-DD') -- invoice date after avatar py start date 
  AND ORIG.DT_INV < TO_DATE('{1}', 'YYYY-MM-DD') -- original invoice earlier than avatar cy start date

  AND F.DOC_AMT < 0 -- Only Credits
  --and ACC.accnt_legcy_id = 'AGBA5003'
  --exclude Law360 and Mlex
  and prod.prod_cd not in ('L360UK','L360IP','L360P','L360US','MLEXMI','MLEXSB')
  and not (prod.prod_name like 'LAW360%' or prod.prod_name like 'MLEX%')
  ORDER BY INV.DT_INV, INV.INTEGRATION_ID)credit
  where credit.fy != 'exclude'
)
  group by accnt_legcy_id
)
select *
from credit

""".format(py_yr_st,cy_yr_st)
df_credit = pd.read_sql(query_credit, con=conn_base)
#output_credit =  os.getcwd()+'\\Raw Data\\RAW_credit.csv'
output_credit = sys.path[0] + f'\\Raw Data\raw_credit_{today}.xlsx'
df_credit.to_excel(output_credit, index=False)
print('credit done')


print('financial base')



# BASE DATA FROM LAW - query might need to be updated, comments in the SQL file in the folder
# cust_det is using law customer because fair amount of plutus customer id and segments are not the same as in iknow or s_org_ext table
# for law cus table, there are 22 accounts in Oct 2021 still have no customer associated, but some can be found in s_org_ext table and seg can be found in territory file
# financial base excludes law 360 and Mlex products for now as not all the billings are shown and will add this premium news billing from Finance team
# AMZZ rep code should be treated as -- rep code
# Nov 2021: requested to add internal segment due to some trade and export accounts being in this segment;
# Nov 2021: requested to add BDFW rep code as it's currently excluded due to MI-MI team
# Nov 2021: requeted to remove flag for nexis_flg; it's been phased off
query_base = """

with cust_det as
        (select distinct
        real_cust.oc_row_id real_customer,
        real_cust.segment real_segment,
        real_cust.cus_status real_cust_status,

        c.provider_customer_key customer ,
        c.customer custname,
        c.status as cust_status,
        xcust.accnt_stat as law_customer_status,
        a.provider_account_key account,
        a.account_name accountname,
        fa_accnt.account_status,
        c.customer_segment SEGMENT,
        fa_accnt.team,
        fa_accnt.repcode repcode,
        fa_accnt.fullname fullname,
        addrs.addr_5 AS region,
        addrs.addr_4 AS city,
        addrs.post_code_r AS postcode,
        addrs.addr_6 AS country
        from pdl.plu_vw_account a
        join pdl.plu_vw_customer c on a.customer_id = c.customer_id
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
                        
        left join law.d_customer_x xcust on xcust.integration_id = c.provider_customer_key
        left join (
            select distinct
            o.par_ou_id as oc_row_id,
            o.row_id as fa_row_id,
            x.attrib_02 as fa_num,
            cus.cust_sub_class_2 segment,
            cus.accnt_stat cus_status
            from pdl.cuk_s_org_ext o
            join pdl.cuk_s_org_ext_xm x
            on x.par_row_id = o.row_id and o.x_lnuk_pr_legacy_id = x.row_id
            left join law.d_customer_x cus on cus.integration_id = o.par_ou_id
            where
            o.bu_id = '1-EOYEBK'
            and o.ou_type_cd = 'Billing'
            and o.sys_current_flg = 'Y'
            and not (cus.bu_pguid = 'USA' and x.attrib_02 in ('TRIN5132','ADEL5025'))
        )real_cust on real_cust.fa_num =  a.provider_account_key

        where  1=1
        -- AMZZ does not need to be included.
        -- THere's only one BA on it and it's for 'Internal Training Account'
        -- so to be treated the same as rep code '--'
        and fa_accnt.repcode   not in ('MIAA', 'MIAC','AMZZ','--')
        and fa_accnt.fullname not in ('M LEX', 'Team RepCode')
        and (fa_accnt.team != 'MI-MI' or fa_accnt.repcode like 'BD%') --make sure BDFW is included 
        -- Kev said can exclude below sales teams, Fran mentioned accounts under Jordans or MI-ES would stay with existing owners anyway, so no need to pull in reallocation
        and fa_accnt.team not in ('MI-RK','Miscellaneous','MI-ES','Academic','Jordans','MK-M1','MLEX','United Kingdom')
        -- account TRIN5132 has one cus id 1-114PA5J, but this cus has two records in the d_cus_x table
        -- one is from USA bu
        and not (xcust.bu_pguid = 'USA' and a.provider_account_key in ('TRIN5132','ADEL5025'))
        -- ROLL0198 has two records due to two account names for the same account number
        --and fa_accnt.accnt_name != 'Rolls Royce - Training Centre, Derby'

        --and not   (fa_accnt.repcode   ='--' or  c.customer_segment like '%Internal%')

           ) ,

sales_ops_product as
(
        SELECT
            prod.row_wid,
            prod.prod_cd,
            prod.prod_famly,
            prod.prod_name,
        CASE
            WHEN prod.fin_report_cd != 'Unspecified' THEN 'ON'
            WHEN prod.fin_report_cd = 'Unspecified' AND
            prod.prod_medium_cd IN ('MC', 'PR','CD','DI') THEN 'PR'
            WHEN prod.fin_report_cd = 'Unspecified' AND
            prod.prod_medium_cd = 'OA' THEN 'OA'
            WHEN prod.fin_report_cd = 'Unspecified' AND
            prod.prod_medium_cd = 'ON' AND
            (
            --Product Code Detail Criteria
            (prod.prod_cd LIKE 'LEGM%' OR
            prod.prod_cd LIKE 'PSLC%' OR
            prod.prod_cd LIKE 'PSLD%' OR
            prod.prod_cd LIKE 'TSO%' OR
            prod.prod_cd LIKE 'TOLG%' OR
            prod.prod_cd LIKE 'TOLL%' OR
            prod.prod_cd LIKE 'MELM%')
            OR prod.prod_cd in ('BXSUBS','IHSUBS','VASUBS','VCSUBS','VRSUBS','VVSUBS','WASUBS','WCSUBS','WDSUBS','WESUBS', --webinars
            'WFSUBS','WISUBS','WJSUBS','WNSUBS','WOSUBS','WPSUBS','WRSUBS','WSSUBS','WTSUBS','WUA','WVSUBS','WWSUBS','WXSUBS')
            -- Product Family Criteria
            OR (prod.SPR_PRODUCT_FAMILY IN ('LexisLibrary','Core', 'SmartForms', 'Middle East Online','LexisSmart', 'PSL/LPA','LexisPSL'))) THEN 'ON'
        ELSE 'OA'
        END AS salesops_medcodeclass
        FROM law.D_PRODUCT PROD
        WHERE 1=1
        -- since no need any more nexis product code as it's phased out, this exception filter might not be needed
        -- shouldn't affect rules as these two prod would be OA products anyway and 0 spending found
       -- and (prod.spr_exclusion !='Y' or prod.prod_cd in ('WAENX', 'FTACA'))
       and prod.spr_exclusion != 'Y'
),

financials as
        (SELECT
                --customer,
                account,
                accountname,
                NVL(SUM(case when FY = 'CY' and salesops_medcodeclass = 'ON' THEN amt end),0) as CY_ON_AMT,
                NVL(SUM(case when FY = 'CY' and salesops_medcodeclass = 'PR' THEN amt end),0) as CY_PR_AMT,
                NVL(SUM(case when FY = 'CY' and salesops_medcodeclass = 'OA' THEN amt end),0) as CY_OA_AMT,

                NVL(SUM(case when FY = 'PY' and salesops_medcodeclass = 'ON' THEN amt end),0) as PY_ON_AMT,
                NVL(SUM(case when FY = 'PY' and salesops_medcodeclass = 'PR' THEN amt end),0) as PY_PR_AMT,
                NVL(SUM(case when FY = 'PY' and salesops_medcodeclass = 'OA' THEN amt end),0) as PY_OA_AMT,

                sum(case when salesops_medcodeclass = 'ON' then active_subs_value end) as active_subs_value,
                sum(case when salesops_medcodeclass = 'ON' then CAE_subs_value end) as CAE_subs_value,
                max(case when salesops_medcodeclass = 'ON' then  dt_renew end) as max_dt_renew,
                max(CASE WHEN myd_flg = 'Y' and dt_renew > yr_st  then 1 else 0 end) as myd_flg,
                max(CASE WHEN  salesops_medcodeclass = 'ON'  and nvl(dt_renew, to_date('1900-01-01','YYYY-MM-DD'))  > yr_st  then 1 else 0 end) as LBU_renewal_flg

                --sum(nexis_flag) as Maila_nexis_flag
         FROM
                (SELECT
                    sub_inv.integration_id as customer,
                    sub_inv.accnt_legcy_id as account,
                    sub_inv.accnt_name as accountname,
                    sub_inv.per_wid,
                    sub_inv.prod_cd,
                    case when sub_inv.per_wid  >= to_char(add_months(to_date({0},'yyyymm'),-11),'yyyymm') then 'CY' else 'PY' END AS FY,
                    -- AS WE HAVE A BESPOKE FY, THE START OF THE YEAR IS THE START OF THE PERIOD IDENTIFIED AS THE STARTING PERIOD FOR THE CY
                    case when sub_inv.per_wid >= to_char(add_months(to_date({0},'yyyymm'),-23),'yyyymm') then (select distinct per_start_dt from law.d_period_dt where per_wid =  to_char(add_months(to_date({0},'yyyymm'),-11),'yyyymm') and calendar =  'Avatar 445') end as yr_st,
                    case when sub_inv.sub_stat  in ('Active','Cancel At End','Complete at End') then  sub_inv.amt end as active_subs_value,
                    case when sub_inv.sub_stat  in ('Cancel At End') then  amt end as CAE_subs_value,
                    case when sub_inv.sub_stat  in ('Active','Cancel At End','Complete at End','Pending','Frozen') then   sub_inv.dt_renew end as dt_renew,
                    sub_inv.myd_flg,
                    --case when sub_inv.prod_cd in ('WAENX', 'FTACA') then 1 else 0 end as nexis_flag,
                    sub_inv.salesops_medcodeclass,
                    sub_inv.f_row_wid,
                    sub_inv.amt
              -- SUB_INV -- ALL SUBS WITHOUT AN INVOICE UNIONED TO THE INVOICE DATA
              -- THE 'INVOICE' DATE OF THE SUBSCRIPTION WITH NO INVOICE HAS BEEN ARBITRARILY SET TO 30 DAYS BEFORE THE SUB START DATE
                FROM
                ( select
                        cust.integration_id,
                        dacc.accnt_legcy_id,
                        dacc.accnt_name,
                        per.per_wid,
                        prod.prod_cd,
                        prod.prod_famly,
                        prod.prod_name,
                        dsub.sub_stat,
                        dsub.dt_start,
                        dsub.dt_end,
                        dsub.canc_dt,
                        dsub.cae_date,
                        dsub.DT_RENEW,
                        dsub.myd_flg,
                        sop.salesops_medcodeclass,
                        fsub.row_wid as f_row_wid,
                        fsub.doc_amt AS amt,
                        'SUB' as src
                    from
                        law.f_subscr_rev fsub
                        join law.d_subscr_rev    dsub on dsub.row_wid = fsub.row_wid
                        join law.d_product prod on prod.row_wid = fsub.prod_wid
                        join sales_ops_product sop on sop.row_wid=prod.row_wid
                        join law.d_fin_accnt_x dacc on dacc.row_wid=fsub.fa_wid
                        JOIN law.d_customer_x cust  ON fsub.cus_wid = cust.row_wid
                        LEFT join law.f_invoice_ln inv on   dsub.row_wid = inv.subr_wid
                        -- the alleged invoice date should be 30 days before the end of the sub, but i decided 30 days before the start of the sub...
                        JOIN law.d_period_dt per ON to_char(to_date(fsub.dt_start_wid,'yyyymmdd') - 30,'yyyymmdd') = per.per_dt_wid
                        join pdl.gen_s_line gens on gens.sys_pguid = dsub.pguid and gens.sys_current_flg = 'Y'
                    where 1=1
                        and per.calendar = 'Avatar 445'
                        and dsub.bu_pguid = 'UK'
                        and fsub.dt_start_wid != 0
                        --  EXCLUDING RECORDS WITH  AN INVOICE
                        and inv.row_wid is null
                        and nvl(gens.sys_delete_flg,'N')!='Y'
                        and  case when dsub.grts_rsn = 'Trial Request' and fsub.doc_amt <= 0 then 1 else 0 end != 1
                        and per.per_wid between to_char(add_months(to_date({0},'yyyymm'),-23),'yyyymm')  AND {0}
                        --exclude Mlex and Law360 products
                        and prod.prod_cd not in ('L360UK','L360IP','L360P','L360US','MLEXMI','MLEXSB')
                        and not (prod.prod_name like 'LAW360%' or prod.prod_name like 'MLEX%')

                 UNION ALL
                 -- INVOICE DATA
                 SELECT
                    cust.integration_id,
                    acc.accnt_legcy_id,
                    acc.accnt_name,
                    per.per_wid,
                    prod.prod_cd,
                     prod.prod_famly,
                    prod.prod_name,
                    subrev.sub_stat,
                    subrev.dt_start,
                    subrev.dt_end,
                    subrev.canc_dt,
                    subrev.cae_date,
                    subrev.DT_RENEW,
                    subrev.myd_flg,
                    sop.salesops_medcodeclass,
                    inv.row_wid as f_row_wid,
                    inv.doc_amt AS amt,
                    'INV' as src
                FROM law.f_invoice_ln inv
                INNER JOIN law.d_customer_x cust  ON inv.cus_wid = cust.row_wid
                INNER JOIN law.d_product prod ON inv.prod_wid = prod.row_wid
                join sales_ops_product sop on sop.row_wid=prod.row_wid
                inner JOIN law.d_subscr_rev subrev ON subrev.row_wid = inv.subr_wid
                INNER JOIN law.d_fin_accnt_x acc ON acc.row_wid = inv.fa_wid
                INNER JOIN law.d_period_dt per ON inv.dt_inv_wid = per.per_dt_wid
                --join law.d_product prod on inv.prod_wid = prod.row_wid
                WHERE 1 = 1
                        AND inv.delete_flg = 'N'
                        AND (inv.bu_pguid IN ('UK', 'Unspecified'))
                        AND per.calendar = 'Avatar 445'
                        and  case when subrev.grts_rsn = 'Trial Request' and inv.doc_amt <= 0 then 1 else 0 end != 1
                        and per.per_wid between to_char(add_months(to_date({0},'yyyymm'),-23),'yyyymm')  AND {0}
                        --exclude Law360 and Mlex products
                        and prod.prod_cd not in ('L360UK','L360IP','L360P','L360US','MLEXMI','MLEXSB')
                        and not (prod.prod_name like 'LAW360%' or prod.prod_name like 'MLEX%')
                        ) sub_inv

                        WHERE 1=1
                        -- below accounts have two cus ids and the filtered one has no billings
                        and sub_inv.integration_id ||sub_inv.accnt_legcy_id not in ('1-1GRXKWECJCH5005','1-1CO6S6QFNZG5000','1-1FHCKNQHATT5031','1-25W8-3056PINK5021','1-25W8-4062ROSS5014','1-FCDB-2670TUGH5007')
                )
             group by
                --customer,
                account,
                accountname
    )

    select * from
          (-- cus level spendings could be calculated later on once credit has been removed
          select
                cust_det.real_customer,
                cust_det.customer,
                cust_det.custname,
               -- financials.customer financial_customer,
                cust_det.cust_status as customer_status,
                cust_det.real_cust_status,
                cust_det.law_customer_status,
                cust_det.account_status as account_status,
                cust_det.account,
                cust_det.accountname,
                cust_det.team,
                cust_det.repcode,
                cust_det.fullname,
                cust_det.real_segment,
                cust_det.segment,
                cust_det.city,
                cust_det.postcode,
                cust_det.region,
                cust_det.country,
                sum(financials.active_subs_value) AS LBU_Subscr,
                sum(CAE_subs_value) as LBU_CAE_VAL,
                /*
                SUM(sum(financials.active_subs_value)) over (partition by  CUST_DET.CUSTOMER) as Cust_Subscr,
                SUM(sum(CAE_subs_value)) OVER   (partition by  CUST_DET.CUSTOMER) as CUST_CAE_VAL,
                NULLIF(SUM(sum(CAE_subs_value)) OVER   (partition by  CUST_DET.CUSTOMER),0) /   SUM(sum(financials.active_subs_value)) over (partition by  CUST_DET.CUSTOMER) AS Cust_CAE_p,
               case when  nvl(SUM(SUM(CY_ON_AMT)) OVER (partition by  CUST_DET.CUSTOMER),0) > 0 then 'Y' else 'N' end AS CUS_HAS_CY_ONLINE_SPEND,
               case when  nvl(SUM(SUM(PY_ON_AMT)) OVER (partition by  CUST_DET.CUSTOMER),0) >  0 then 'Y' else 'N' end AS CUS_HAS_PY_ONLINE_SPEND,
               */
                case when  nvl(SUM(SUM(LBU_renewal_flg)) OVER (partition by  CUST_DET.CUSTOMER),0) > 0 then 'Y' else 'N' end AS Cust_ON_RenewalFlg ,
                case when  nvl(SUM(financials.LBU_renewal_flg) ,0) > 0 then 'Y' else 'N' end AS LBU_ON_RenewalFlg ,

              -- case when sum(Maila_nexis_flag) > 0 then 'Y' else 'N' end as nexis_flg,
                case   WHEN SUM(myd_flg) > 0  then 'Y' else 'N' end AS  LBU_MYD_FLG,
                max(financials.max_dt_renew) as LBUmaxRenewDate,
               max(max(financials.max_dt_renew)) OVER (partition by  CUST_DET.CUSTOMER) as CustMaxRenewDate,
                -- CURRENT YEAR LBU
                NVL(SUM(financials.CY_ON_AMT),0) AS LBU_CY_ON_AMT,
                NVL(SUM(financials.CY_PR_AMT),0) AS LBU_CY_PR_AMT,
                NVL(SUM( financials.CY_OA_AMT),0) AS LBU_CY_OA_AMT,
               -- NVL( SUM(financials.CY_ON_AMT) + SUM(financials.CY_PR_AMT) + SUM( financials.CY_OA_AMT),0) AS LBU_CY_TOT,
                /*
                -- CURRENT YEAR CUST
                NVL(SUM(SUM(financials.CY_ON_AMT)) OVER (PARTITION BY CUST_DET.CUSTOMER),0) AS CUS_CY_ON_AMT,
                NVL(SUM(SUM(financials.CY_PR_AMT)) OVER (PARTITION BY CUST_DET.CUSTOMER),0) AS CUS_CY_PR_AMT,
                NVL(SUM(SUM( financials.CY_OA_AMT)) OVER (PARTITION BY CUST_DET.CUSTOMER),0) AS CUS_CY_OA_AMT,
                NVL(SUM(SUM(financials.CY_ON_AMT)) OVER (PARTITION BY CUST_DET.CUSTOMER) + SUM(SUM(financials.CY_PR_AMT))  OVER (PARTITION BY CUST_DET.CUSTOMER) + SUM(SUM( financials.CY_OA_AMT))  OVER (PARTITION BY CUST_DET.CUSTOMER),0) AS CUS_CY_TOT,
*/
                -- PREVIOUS YEAR LBU
                NVL(SUM(financials.PY_ON_AMT),0) AS LBU_PY_ON_AMT,
                NVL(SUM(financials.PY_PR_AMT),0) AS LBU_PY_PR_AMT,
                NVL(SUM( financials.PY_OA_AMT),0) AS LBU_PY_OA_AMT,
                --NVL( SUM(financials.PY_ON_AMT) + SUM(financials.PY_PR_AMT) + SUM( financials.PY_OA_AMT),0) AS LBU_PY_TOT,
                /*
                -- PREVIOUS YEAR CUST
                NVL(SUM(SUM(financials.PY_ON_AMT))  OVER (PARTITION BY CUST_DET.CUSTOMER),0) AS CUS_PY_ON_AMT,
                NVL(SUM(SUM(financials.PY_PR_AMT))  OVER (PARTITION BY CUST_DET.CUSTOMER),0) AS CUS_PY_PR_AMT,
                NVL(SUM(SUM( financials.PY_OA_AMT))  OVER (PARTITION BY CUST_DET.CUSTOMER),0) AS CUS_PY_OA_AMT,
                NVL(SUM(SUM(financials.PY_ON_AMT)) OVER (PARTITION BY CUST_DET.CUSTOMER) + SUM(SUM(financials.PY_PR_AMT))  OVER (PARTITION BY CUST_DET.CUSTOMER) + SUM(SUM( financials.PY_OA_AMT))  OVER (PARTITION BY CUST_DET.CUSTOMER),0) AS CUS_PY_TOT,
*/
                {0} as YrPer
/*
                -- NEED TO EXCLUDE CL REPCODES WITH NO SPEND AT CUST LEVEL IN PREVIOUS YEAR
                -- Nov 21 a few accounts have CL and 0 previous year spend, but have cy_pr_spend
                CASE WHEN cust_det.repcode = 'CL' AND   (NVL( SUM(financials.PY_ON_AMT) + SUM(financials.PY_PR_AMT) + SUM( financials.PY_OA_AMT),0) ) = 0 THEN 'Y' ELSE 'N' END AS excldclosedacct
*/
        from     cust_det
        -- financials.customer are mostly real_customer but 8 accounts have law_d_cus_x integration id
        left join financials on financials.account = cust_det.account --and financials.customer = cust_det.customer
        GROUP BY
                cust_det.real_customer,
                cust_det.customer,
                cust_det.custname,
                --financials.customer,
                cust_det.account,
                 cust_det.region,
                cust_det.accountname,
                cust_det.team,
                cust_det.repcode,
                cust_det.fullname,
               
                cust_det.segment,
                cust_det.city,
                cust_det.postcode,
                cust_det.country,
                cust_det.real_cust_status,
                cust_det.cust_status,
                 cust_det.law_customer_status,
                  cust_det.account_status,
                cust_det.real_segment
        )
            --where excldclosedacct = 'N'
""".format(period)
df_base = pd.read_sql(query_base, con=conn_base)
#output_base =  os.getcwd()+'\\Raw Data\\Raw_Financial_Base_plutus.csv'
output_base = sys.path[0] + f'\\Raw Data\\raw_plutus_financial_base_{today}.xlsx'
df_base.to_excel(output_base, index=False)


conn_base.close()

print('financial base done')


