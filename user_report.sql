-- User details, latest login ( LL, PSL, SmartPrecedents, Draft, Smart Form), usage against the products for the past 12 months separately (All SMAPI and Aurora)
set define off;
-- UserDetails
SELECT DISTINCT
wu.user_signon_id,
wu.web_user_first_name,
wu.web_user_last_name,
us.wu_email,
wu.instnt_actv_cd,
wu.create_dt,
greatest(logins."'LexisLibrary'",logins."'LexisPSL'") as ALL_lst_login,
logins."'LexisLibrary'" as LL_lst_login,
logins."'LexisPSL'" as PSL_lst_login,
usg."'LexisLibrary'" as LL_past_12_mths,
usg."'LexisPSL'" as PSL_past_12_mths,
case when db_usg.wu_login_id  is null then 'Y' else '' end as "No Usage in db",
alert_12.act as "Alert 12 Months Usage",
alert.act as "Alert Usage since 2016",
wu.actv_ind
      
FROM pdl.gdw_web_user_curr wu
JOIN pdl.gdw_sub_acct_curr subacc  ON subacc.sub_acct_id = wu.sub_acct_id
JOIN pdl.gdw_web_user_signon us ON us.wu_login_id =  wu.user_signon_id
--  Usage pas 12 mths
LEFT JOIN  
    (SELECT * FROM
     ( SELECT
          ACC.accnt_legcy_id  AS ACC,
          prodfam.pf_name AS pf,
          wu.wu_login_id  AS login_id,
         SUM(fusg.act_count) AS act
      FROM
         law.f_src_usg_mn_a       fusg 
         JOIN  law.d_web_user      wu ON  fusg.wu_wid = wu.row_wid
         JOIN  law.d_usg_type      usgtp ON  fusg.usgtp_wid = usgtp.row_wid
         JOIN  law.d_fin_accnt_x   ACC ON fusg.fa_wid = ACC.row_wid
        JOIN   law.d_prod_family   prodfam ON fusg.pf_wid = prodfam.row_wid
      WHERE 1=1
          AND  usgtp.usgtp_subtype NOT IN ( 'COMMIT ADJ',  'PRINT LINES',  'WEB')
        and usgtp.usgtp_type not    in ('ADF', 'BROWSE',  'IMAGE', 'PRINT','Unspecified')
            AND ACC.accnt_legcy_id = 'SHAK5001'
            AND fusg.bu_pguid IN (   'UK',    'Unspecified'   ) 
            AND prodfam.pf_name  IN ('LexisLibrary','LexisPSL')--,'SmartForms','Smart Precedents')--,'Lexis Check & Draft','TolleyGuidance','TolleyLibrary',) --'Lexis Check & Draft','Smart Precedents',
            and fusg.dt_wid >= '20210401'-- and '20220406'
      GROUP BY
          prodfam.pf_name,
          ACC.accnt_legcy_id,
          wu.wu_login_id)
          PIVOT ( SUM(act)  FOR pf IN  ('LexisLibrary','LexisPSL'))) usg ON usg.login_id = wu.user_signon_id
          
-- last login/visit/download date across LL, PSL, Smart Precedents, Draft, Smart Forms
    LEFT JOIN
                (select * from 
(SELECT 
                wu.wu_login_id,
                prodfam.pf_name,
                MAX(fusg.LAST_USE_DT) AS lst_login_date                
            FROM
                law.f_src_usg_mn_a       fusg
                JOIN law.d_usg_type      usgty ON fusg.usgtp_wid = usgty.row_wid
                JOIN law.d_fin_accnt_x   finacc ON fusg.fa_wid = finacc.row_wid
                JOIN law.d_web_user      wu ON wu.row_wid = fusg.wu_wid
                JOIN law.d_prod_family   prodfam ON fusg.pf_wid = prodfam.row_wid
            WHERE
                1 = 1
                AND usgty.usgtp_type in ( 'Logins','Visits','Downloads')
                AND fusg.bu_pguid IN (   'UK', 'Unspecified')
                AND finacc.accnt_legcy_id = 'SHAK5001'
            GROUP BY
               prodfam.pf_name ,
              wu.wu_login_id)
              pivot (max(lst_login_date)for pf_name in ('LexisLibrary','LexisPSL'))) logins ON logins.wu_login_id = wu.user_signon_id
              
-- No usage ever recorded in db?
LEFT JOIN 
   ( SELECT 
                wu.wu_login_id
            FROM
                law.f_src_usg_MN_A      fusg
                --JOIN law.d_date          dt ON fusg.dt_wid = dt.row_wid
                JOIN law.d_usg_type      usgty ON fusg.usgtp_wid = usgty.row_wid
                JOIN law.d_fin_accnt_x   finacc ON fusg.fa_wid = finacc.row_wid
                JOIN law.d_web_user      wu ON wu.row_wid = fusg.wu_wid
            
            WHERE
                1 = 1
                AND  usgty.usgtp_subtype NOT IN ( 'COMMIT ADJ',  'PRINT LINES',   'WEB')
          and usgty.usgtp_type not    in ('ADF', 'BROWSE',  'IMAGE', 'PRINT','Unspecified')

                AND fusg.bu_pguid IN (   'UK', 'Unspecified')
                AND finacc.accnt_legcy_id = 'SHAK5001'
               
            GROUP BY
            wu.wu_login_id) db_usg on db_usg.wu_login_id = wu.user_signon_id
            
-- alert usage in the past 12m
LEFT JOIN 
   ( SELECT 
                wu.wu_login_id,
                SUM(fusg.act_count) AS act
            FROM
                law.f_src_usg_MN_A      fusg
                --JOIN law.d_date          dt ON fusg.dt_wid = dt.row_wid
                JOIN law.d_usg_type      usgty ON fusg.usgtp_wid = usgty.row_wid
                JOIN law.d_fin_accnt_x   finacc ON fusg.fa_wid = finacc.row_wid
                JOIN law.d_web_user      wu ON wu.row_wid = fusg.wu_wid
            
            WHERE
                1 = 1
                AND  usgty.usgtp_subtype NOT IN ( 'COMMIT ADJ',  'PRINT LINES',   'WEB')
            AND usgty.usgtp_type  IN ('ALERT')
                AND fusg.bu_pguid IN (   'UK', 'Unspecified')
                AND finacc.accnt_legcy_id = 'SHAK5001'
                and fusg.dt_wid >= '20210401'-- and '20220406'
               
            GROUP BY
            wu.wu_login_id) alert_12 on alert_12.wu_login_id = wu.user_signon_id
-- alert usage since 2016
LEFT JOIN 
   ( SELECT 
                wu.wu_login_id,
                SUM(fusg.act_count) AS act
            FROM
                law.f_src_usg_MN_A      fusg
                --JOIN law.d_date          dt ON fusg.dt_wid = dt.row_wid
                JOIN law.d_usg_type      usgty ON fusg.usgtp_wid = usgty.row_wid
                JOIN law.d_fin_accnt_x   finacc ON fusg.fa_wid = finacc.row_wid
                JOIN law.d_web_user      wu ON wu.row_wid = fusg.wu_wid
            
            WHERE
                1 = 1
                AND  usgty.usgtp_subtype NOT IN ( 'COMMIT ADJ',  'PRINT LINES',   'WEB')
            AND usgty.usgtp_type  IN ('ALERT')
                AND fusg.bu_pguid IN (   'UK', 'Unspecified')
                AND finacc.accnt_legcy_id = 'SHAK5001'
               
            GROUP BY
            wu.wu_login_id) alert on alert.wu_login_id = wu.user_signon_id
WHERE 
    wu.sys_delete_flg= 'N'
    AND wu.sys_current_flg = 'Y'
    AND subacc.sys_current_flg='Y'
    AND subacc.sys_delete_flg = 'N'
    AND subacc.lbu_acct_id = 'SHAK5001'
    and us.sys_current_flg = 'Y'
    AND wu.actv_ind = 'Y'
    ;
