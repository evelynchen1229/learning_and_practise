import cx_Oracle
import pandas as pd
import openpyxl
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.styles import Color, Fill
from openpyxl.cell import Cell
import os
import sys

# data connection to RECON
dsn_tns_recon = cx_Oracle.makedsn('psdb3119.lexisnexis.com', '1521', service_name='CUSTHUB.ispprod.lexisnexis.com')
conn_recon = cx_Oracle.connect(user='recon', password='Recon1121Z', dsn=dsn_tns_recon)

# SQL queries for usage threshold NPS data, as well as hub no email stats
sql_legal_usg = '''
-- legal customer for LL/PSL only, PSL > LL

select
*
from
        (
        select
                aa.secondary_sub_class as customer_group,
                s.sub_segment,
                s.value,
                s.market,
                case    when psl_live = 'Y' and nvl(psl_doc_views,0)>5 and nvl(psl_logins,0)>5 then 'LexisPSL'
                when library_live='Y' and nvl(ll_doc_views,0)>5 and nvl(ll_logins,0)>5 then 'LexisLibrary'
                else 'REMOVE'
                end as product_name,
                aa.accountname as mastername,
                aa.accountnumber as genesis_account,
                aa.psl_live,
                aa.PSL_MIN_STARTDATE,
                aa.psl_min_renewaldate,
                aa.LIBRARY_LIVE,
                aa.LIB_MIN_STARTDATE,
                aa.LIB_MIN_RENEWALDATE,
                usg.username,
                usg.email,
                usg.psl_logins,
                usg.psl_page_views,
                usg.psl_doc_views,
                usg.ll_logins as LIBRARY_LOGINS,
                usg.ll_page_views as LIBRARY_PAGEVIEWS,
                usg.ll_doc_views as LIBRARY_DOCVIEWS

        from  law.mv_nps_active_accounts@GBI_LAW aa
        join law.mv_nps_usg_legal@GBI_LAW usg on aa.accountnumber = usg.account
        left join lkp_segment      s on s.sec_sub_class = aa.secondary_sub_class
        where 1=1
            and nvl(s.sub_segment,'New') != 'REMOVE' -- for potential new segments
            and nvl(s.value,'New') not in ('Tax')
            and   ( nvl(psl_live,'N')!='N' or nvl(library_live,'N')!='N') 
        ) t
where 1=1
and product_name != 'REMOVE'

'''

sql_tax_usg = '''
-- tax customer for TG/TL, no hierarchy;both 4logins/6 docviews 
select
* 
 
from
        (
        select
                aa.secondary_sub_class as SEGMENT_UK,
                s.sub_segment,
                s.value,
                s.market,
                case   
                --only active TG
                  when tollguide_live='Y' and nvl(usg.tgu_doc_views,0)>5 and nvl(usg.tgu_logins,0)>3 and (nvl(tolley_live,'N')='N' or nvl(tl_doc_views,0)<6 or nvl(tl_logins,0)<4 )then 'TolleyGuidance'
                --only active TL
                  when tolley_live='Y' and nvl(tl_doc_views,0)>5 and nvl(tl_logins,0)>3 and (nvl(tollguide_live,'N')='N' or nvl(usg.tgu_doc_views,0)<6 or nvl(usg.tgu_logins,0)<4 )then 'TolleyLibrary'
                --both TG and TL
                  when tollguide_live='Y' and tolley_live='Y'and nvl(usg.tgu_doc_views,0)>5 and nvl(usg.tgu_logins,0)>3 and nvl(tl_doc_views,0)>5 and nvl(tl_logins,0)>3 then'TolleyGuidance_and_TolleyLibrary'
                else 'REMOVE'
                end as product_name,
                aa.accountname as mastername,
                aa.accountnumber as genesis_account,
                aa.tollguide_live AS GUIDANCE_LIVE ,
                aa.tgu_min_startdate  as GUIDANCE_MIN_START_DATE,
                aa.tgu_min_renewaldate as GUIDANCE_RENEWAL_DATE,
                aa.TOLLEY_LIVE, 
                aa.TOLLEY_MIN_STARTDATE, 
                aa.TOLLEY_MIN_RENEWALDATE,
                usg.username,
                usg.email,
                usg.tgu_logins as GUIDANCE_LOGINS,
                usg.tgu_doc_views as GUIDANCE_DOCVIEWS,
                usg.tgu_page_views as GUIDANCE_PAGEVIEWS,
                 usg.tl_logins as TOLLEY_LOGINS,
                usg.tl_page_views as TOLLEY_PAGEVIEWS,
                usg.tl_doc_views as TOLLEY_DOCVIEWS
        from  law.mv_nps_active_accounts@GBI_LAW aa
        join law.mv_nps_usg_tax@GBI_LAW usg on aa.accountnumber = usg.account
        left join  lkp_segment s on s.sec_sub_class = aa.secondary_sub_class 
        where 1=1
            and nvl(s.sub_segment,'New') != 'REMOVE' -- for potential new segments
            and nvl(s.value,'New')  in ('Tax','New','Public Sector') 
            and (NVL(aa.tollguide_live,'N') !='N'or nvl(tolley_live,'N')!='N' )
        ) t
where 1=1
and product_name != 'REMOVE'

'''

sql_legal_nps = '''
-- legal customer for LL/PSL only, PSL > LL

select
t.* ,
   product_name  as productemail,
    case
        when product_name = 'LexisLibrary' and market = 'L' then 'LL_Legal'
        when product_name = 'LexisLibrary' and market = 'C' then 'LL_Corp'
        when product_name = 'LexisLibrary' and market = 'G' then 'LL_Pub'
        when product_name = 'LexisLibrary' and market = 'O' then 'LL_Legal'
        when product_name = 'LexisPSL' then 'LexisPSL'
     else product_name || ' ' || market
    end as Product
from
        (
        select
                c.contact_id,
                c.organisation_id,
                c.site_id,
                c.email_address as email,
                c.salutation as greeting,
                c.title as salutations,
                c.first_name as user_fn,
                c.surname as user_ln,
                c.job_title as title,
                c.phone_number as contact_phone,
                'UK' as country,
                c.country as region,
                '9' as language,
                aa.secondary_sub_class as customer_group,
                s.sub_segment,
                s.value,
                s.market,
                'Intl' as business,
                case    when psl_live = 'Y' and nvl(psl_doc_views,0)>5 and nvl(psl_logins,0)>5 then 'LexisPSL'
                when library_live='Y' and nvl(ll_doc_views,0)>5 and nvl(ll_logins,0)>5 then 'LexisLibrary'
                else 'REMOVE'
                end as product_name,
                c.contact_id as masternumber,
                aa.accountname as mastername,
                aa.accountnumber as genesis_account,
                aa.psl_live,
                aa.PSL_MIN_STARTDATE,
                aa.psl_min_renewaldate,
                aa.LIBRARY_LIVE,
                aa.LIB_MIN_STARTDATE,
                aa.LIB_MIN_RENEWALDATE,
                usg.username,
                c.suppress_email as exc_email,
                usg.psl_logins,
                usg.psl_page_views,
                usg.psl_doc_views,
                usg.ll_logins as LIBRARY_LOGINS,
                usg.ll_page_views as LIBRARY_PAGEVIEWS,
                usg.ll_doc_views as LIBRARY_DOCVIEWS,
                aa.repcode as rep_code,
                aa.full_name as rep_name,
                aa.salesteam as SALES_TERRITORY,
                aa.am_email as REP_EMAIL,
                aa.csname as csm_name,
                aa.cms_email as csm_email,
                row_number() over (partition by c.email_address order by c.contact_id desc) as rn
        from  law.mv_nps_active_accounts@GBI_LAW aa
        join law.mv_nps_usg_legal@GBI_LAW usg on aa.accountnumber = usg.account
        join vw_nps_contact_user_ids cui on cui.user_id=usg.username
        join vw_nps_contacts c on  c.contact_id= cui.contact_id
        left join lkp_segment s on s.sec_sub_class = aa.secondary_sub_class
        where
            c.email_address is not null
            and nvl(s.sub_segment,'New') != 'REMOVE' -- for potential new segments
            and nvl(s.value,'New') not in ('Tax')
            and   ( nvl(psl_live,'N')!='N' or nvl(library_live,'N')!='N') 
        ) t
where rn=1
and product_name != 'REMOVE'
'''

sql_tax_nps = '''
-- tax customer for TG/TL, no hierarchy;both 4logins/6 docviews
select
t.* ,
   product_name  as productemail,
    product_name   as Product
from
        (
        select
                c.contact_id,
                c.organisation_id,
                c.site_id,
                c.email_address as email,
                c.salutation as greeting,
                c.title as salutations,
                c.first_name as user_fn,
                c.surname as user_ln,
                c.job_title as title,
                c.phone_number as contact_phone,
                'UK' as country,
                c.country as region,
                '9' as language,
                aa.secondary_sub_class as SEGMENT_UK,
                s.sub_segment,
                s.value,
                s.market,
                'Intl' as business,
                case
                --only active TG
                  when tollguide_live='Y' and nvl(usg.tgu_doc_views,0)>5 and nvl(usg.tgu_logins,0)>3 and (nvl(tolley_live,'N')='N' or nvl(tl_doc_views,0)<6 or nvl(tl_logins,0)<4 )then 'TolleyGuidance'
                --only active TL
                  when tolley_live='Y' and nvl(tl_doc_views,0)>5 and nvl(tl_logins,0)>3 and (nvl(tollguide_live,'N')='N' or nvl(usg.tgu_doc_views,0)<6 or nvl(usg.tgu_logins,0)<4 )then 'TolleyLibrary'
                --both TG and TL
                  when tollguide_live='Y' and tolley_live='Y'and nvl(usg.tgu_doc_views,0)>5 and nvl(usg.tgu_logins,0)>3 and nvl(tl_doc_views,0)>5 and nvl(tl_logins,0)>3 then'TolleyGuidance_and_TolleyLibrary'
                else 'REMOVE'
                end as product_name,
                c.contact_id as masternumber,
                aa.accountname as mastername,
                aa.accountnumber as genesis_account,
                aa.tollguide_live AS GUIDANCE_LIVE ,
                aa.tgu_min_startdate  as GUIDANCE_MIN_START_DATE,
                aa.tgu_min_renewaldate as GUIDANCE_RENEWAL_DATE,
                aa.TOLLEY_LIVE,
                aa.TOLLEY_MIN_STARTDATE,
                aa.TOLLEY_MIN_RENEWALDATE,
                usg.username,
                c.suppress_email as exc_email,
                usg.tgu_logins as GUIDANCE_LOGINS,
                usg.tgu_doc_views as GUIDANCE_DOCVIEWS,
                usg.tgu_page_views as GUIDANCE_PAGEVIEWS,
                 usg.tl_logins as TOLLEY_LOGINS,
                usg.tl_page_views as TOLLEY_PAGEVIEWS,
                usg.tl_doc_views as TOLLEY_DOCVIEWS,
                aa.repcode as rep_code,
                aa.full_name as rep_name,
                aa.salesteam as SALES_TERRITORY,
                aa.am_email as REP_EMAIL,
                aa.csname as csm_name,
                aa.cms_email as csm_email,
                row_number() over (partition by c.email_address order by c.contact_id desc) as rn
        from  law.mv_nps_active_accounts@GBI_LAW aa
        join law.mv_nps_usg_tax@GBI_LAW usg on aa.accountnumber = usg .account
        join vw_nps_contact_user_ids cui on cui.user_id=usg.username
        join vw_nps_contacts c on  c.contact_id= cui.contact_id
        left join  lkp_segment    s on s.sec_sub_class = aa.secondary_sub_class
        where
            c.email_address is not null
            and nvl(s.sub_segment,'New') != 'REMOVE' -- for potential new segments
            and nvl(s.value,'New')  in ('Tax','New','Public Sector')  -- Jan suggested to keep it in since previous NPS had it 9 June 2021
            and (NVL(aa.tollguide_live,'N') !='N'or nvl(tolley_live,'N')!='N' )
        ) t
where rn=1
and product_name != 'REMOVE'
'''

sql_legal_nps_no_email = '''

-- legal customer for LL/PSL only, PSL > LL

select
t.* ,
   product_name  as productemail,
    case
        when product_name = 'LexisLibrary' and market = 'L' then 'LL_Legal'
        when product_name = 'LexisLibrary' and market = 'C' then 'LL_Corp'
        when product_name = 'LexisLibrary' and market = 'G' then 'LL_Pub'
        when product_name = 'LexisLibrary' and market = 'O' then 'LL_Legal'
        when product_name = 'LexisPSL' then 'LexisPSL'
     else product_name || ' ' || market
    end as Product
from
        (
        select
                c.contact_id,
                c.organisation_id,
                c.site_id,
                c.email_address as email,
                c.salutation as greeting,
                c.title as salutations,
                c.first_name as user_fn,
                c.surname as user_ln,
                c.job_title as title,
                c.phone_number as contact_phone,
                'UK' as country,
                c.country as region,
                '9' as language,
                aa.secondary_sub_class as customer_group,
                s.sub_segment,
                s.value,
                s.market,
                'Intl' as business,
                case    when psl_live = 'Y' and nvl(psl_doc_views,0)>5 and nvl(psl_logins,0)>5 then 'LexisPSL'
                when library_live='Y' and nvl(ll_doc_views,0)>5 and nvl(ll_logins,0)>5 then 'LexisLibrary'
                else 'REMOVE'
                end as product_name,
                c.contact_id as masternumber,
                aa.accountname as mastername,
                aa.accountnumber as genesis_account,
                aa.psl_live,
                aa.PSL_MIN_STARTDATE,
                aa.psl_min_renewaldate,
                aa.LIBRARY_LIVE,
                aa.LIB_MIN_STARTDATE,
                aa.LIB_MIN_RENEWALDATE,
                usg.username,
                c.suppress_email as exc_email,
                usg.psl_logins,
                usg.psl_page_views,
                usg.psl_doc_views,
                usg.ll_logins as LIBRARY_LOGINS,
                usg.ll_page_views as LIBRARY_PAGEVIEWS,
                usg.ll_doc_views as LIBRARY_DOCVIEWS,
                aa.repcode as rep_code,
                aa.full_name as rep_name,
                aa.salesteam as SALES_TERRITORY,
                aa.am_email as REP_EMAIL,
                aa.csname as csm_name,
                aa.cms_email as csm_email,
                row_number() over (partition by c.email_address order by c.contact_id desc) as rn
        from  law.mv_nps_active_accounts@GBI_LAW aa
        join law.mv_nps_usg_legal@GBI_LAW usg on aa.accountnumber = usg.account
        join vw_nps_contact_user_ids cui on cui.user_id=usg.username
        join vw_nps_contacts c on  c.contact_id= cui.contact_id
        left join lkp_segment s on s.sec_sub_class = aa.secondary_sub_class
        where
            c.email_address is null
            and nvl(s.sub_segment,'New') != 'REMOVE' -- for potential new segments
            and nvl(s.value,'New') not in ('Tax')
            and   ( nvl(psl_live,'N')!='N' or nvl(library_live,'N')!='N') 
        ) t
where rn=1
and product_name != 'REMOVE'

'''

sql_tax_nps_no_email = '''
-- tax customer for TG/TL, no hierarchy;both 4logins/6 docviews
select
t.* ,
   product_name  as productemail,
    product_name   as Product
from
        (
        select
                c.contact_id,
                c.organisation_id,
                c.site_id,
                c.email_address as email,
                c.salutation as greeting,
                c.title as salutations,
                c.first_name as user_fn,
                c.surname as user_ln,
                c.job_title as title,
                c.phone_number as contact_phone,
                'UK' as country,
                c.country as region,
                '9' as language,
                aa.secondary_sub_class as SEGMENT_UK,
                s.sub_segment,
                s.value,
                s.market,
                'Intl' as business,
                case
                --only active TG
                  when tollguide_live='Y' and nvl(usg.tgu_doc_views,0)>5 and nvl(usg.tgu_logins,0)>3 and (nvl(tolley_live,'N')='N' or nvl(tl_doc_views,0)<6 or nvl(tl_logins,0)<4 )then 'TolleyGuidance'
                --only active TL
                  when tolley_live='Y' and nvl(tl_doc_views,0)>5 and nvl(tl_logins,0)>3 and (nvl(tollguide_live,'N')='N' or nvl(usg.tgu_doc_views,0)<6 or nvl(usg.tgu_logins,0)<4 )then 'TolleyLibrary'
                --both TG and TL
                  when tollguide_live='Y' and tolley_live='Y'and nvl(usg.tgu_doc_views,0)>5 and nvl(usg.tgu_logins,0)>3 and nvl(tl_doc_views,0)>5 and nvl(tl_logins,0)>3 then'TolleyGuidance_and_TolleyLibrary'
                else 'REMOVE'
                end as product_name,
                c.contact_id as masternumber,
                aa.accountname as mastername,
                aa.accountnumber as genesis_account,
                aa.tollguide_live AS GUIDANCE_LIVE ,
                aa.tgu_min_startdate  as GUIDANCE_MIN_START_DATE,
                aa.tgu_min_renewaldate as GUIDANCE_RENEWAL_DATE,
                aa.TOLLEY_LIVE,
                aa.TOLLEY_MIN_STARTDATE,
                aa.TOLLEY_MIN_RENEWALDATE,
                usg.username,
                c.suppress_email as exc_email,
                usg.tgu_logins as GUIDANCE_LOGINS,
                usg.tgu_doc_views as GUIDANCE_DOCVIEWS,
                usg.tgu_page_views as GUIDANCE_PAGEVIEWS,
                 usg.tl_logins as TOLLEY_LOGINS,
                usg.tl_page_views as TOLLEY_PAGEVIEWS,
                usg.tl_doc_views as TOLLEY_DOCVIEWS,
                aa.repcode as rep_code,
                aa.full_name as rep_name,
                aa.salesteam as SALES_TERRITORY,
                aa.am_email as REP_EMAIL,
                aa.csname as csm_name,
                aa.cms_email as csm_email,
                row_number() over (partition by c.email_address order by c.contact_id desc) as rn
        from  law.mv_nps_active_accounts@GBI_LAW aa
        join law.mv_nps_usg_tax@GBI_LAW usg on aa.accountnumber = usg .account
        join vw_nps_contact_user_ids cui on cui.user_id=usg.username
        join vw_nps_contacts c on  c.contact_id= cui.contact_id
        left join  lkp_segment    s on s.sec_sub_class = aa.secondary_sub_class
        where
            c.email_address is null
            and nvl(s.sub_segment,'New') != 'REMOVE' -- for potential new segments
            and nvl(s.value,'New')  in ('Tax','New','Public Sector')  -- Jan suggested to keep it in since previous NPS had it 9 June 2021
            and (NVL(aa.tollguide_live,'N') !='N'or nvl(tolley_live,'N')!='N' )
        ) t
where rn=1
and product_name != 'REMOVE'
'''

# read sql and save to excel files
# for tax customers
print('generating raw data file 1 / 6 ...')
tax_usg = pd.read_sql(sql_tax_usg, con=conn_recon)
output_tax_usg =  sys.path[0]+'\\3. Raw Data\\NPS-Tax_Usage.xlsx'
tax_usg.to_excel(output_tax_usg, index = False)

print('generating raw data file 2 / 6 ...')
tax_nps = pd.read_sql(sql_tax_nps, con=conn_recon)
output_tax_nps = sys.path[0]+'\\3. Raw Data\\NPS-Tax.xlsx'
tax_nps.to_excel(output_tax_nps, index = False)

print('generating raw data file 3 / 6 ...')
tax_nps_null_email = pd.read_sql(sql_tax_nps_no_email, con=conn_recon)
output_tax_email = sys.path[0]+'\\3. Raw Data\\tax_hub_no_email.xlsx'
tax_nps_null_email.to_excel(output_tax_email, index = False)

# for legal customers
print('generating raw data file 4 / 6 ...')
legal_usg = pd.read_sql(sql_legal_usg, con=conn_recon)
output_legal_usg =  sys.path[0]+'\\3. Raw Data\\NPS-Legal_Usage.xlsx'
legal_usg.to_excel(output_legal_usg, index = False)

print('generating raw data file 5 / 6 ...')
legal_nps = pd.read_sql(sql_legal_nps, con=conn_recon)
output_legal_nps = sys.path[0]+'\\3. Raw Data\\NPS-Legal.xlsx'
legal_nps.to_excel(output_legal_nps, index = False)

print('generating raw data file 6 / 6 ...')
legal_nps_null_email = pd.read_sql(sql_legal_nps_no_email, con=conn_recon)
output_legal_email = sys.path[0]+'\\3. Raw Data\\legal_hub_no_email.xlsx'
legal_nps_null_email.to_excel(output_legal_email, index = False)


conn_recon.close()
