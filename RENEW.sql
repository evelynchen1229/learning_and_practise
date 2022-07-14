with renew as (SELECT 
                            cust.integration_id     AS customer, cust.accnt_name as customer_name,
                            acc.accnt_legcy_id      AS account, 
                            acc.accnt_name, 
                            cust.cust_sub_class_2   AS segment, 
                            prod.prod_famly         AS prodfam, 
                            prod.prod_cd, 
                            PROD.PROD_NAME, 
                            prod.prod_medium_cd, 
                              subrev.dt_start, 
                            subrev.dt_end, 
                            subrev.canc_dt, 
                              subrev.sub_stat ,
                              subrev.DT_RENEW,
                                subrev.TRIAL_FLG , 
                            gens.sys_delete_flg, 
                            subrev.SUB_NUM,
subrev.SUB_REV,
subrev.SUB_REV_REF,
subrev.CAE_DATE,
subrev.CAE_FLG,
                            SUM(fsub.doc_amt) AS amount, 
                            sum(finv.doc_amt) as invoice 
                        FROM 
                            law.f_subscr_rev    fsub  
                            JOIN law.d_customer_x    cust ON fsub.cus_wid = cust.row_wid 
                            JOIN law.d_product       prod ON fsub.prod_wid = prod.row_wid 
                            JOIN law.d_subscr_rev    subrev ON subrev.row_wid = fsub.row_wid 
                            JOIN law.d_fin_accnt_x   acc ON acc.row_wid = fsub.fa_wid 
                            INNER JOIN law.d_position  p ON p.row_wid = acc.pos_pr_wid 
                            left join LAW.f_invoice_ln finv on subrev.row_wid = finv.subr_wid 
                            join pdl.gen_s_line gens on gens.sys_pguid = subrev.pguid and gens.sys_current_flg = 'Y' 
                        WHERE 
                            1 = 1 
                            AND fsub.delete_flg = 'N' 
                            AND  fsub.bu_pguid = 'UK' 
                            and prod.prod_famly  in ('Tolley Library','Tax Library')
                           -- and prod.prod_cd = 'TOLM03'
                           -- and  acc.accnt_legcy_id = 'CVRO5000'
                            and subrev.DT_RENEW between '01-DEC-20' and '31-DEC-20'
                            and subrev.TRIAL_FLG = 'N'
                           --and subrev.sub_stat IN ('Complete at End',  'Active','Cancel At End') 
                            

                         

                            and p.postn_rep_cd !='--' 

                            and cust.cust_sub_class_2 not in ('Internal','External Test')
                            

                         

                        GROUP BY 
                             cust.integration_id, cust.accnt_name,
                            acc.accnt_legcy_id, 
                            acc.accnt_name, 
                            cust.cust_sub_class_2, 
                            prod.prod_famly, 
                            subrev.CAE_DATE,
subrev.CAE_FLG,
                            prod.prod_cd, 
                            PROD.PROD_NAME, 
                            prod.prod_medium_cd, 
                            gens.sys_delete_flg, 
                            subrev.dt_start, 
                            subrev.dt_end, 
                            subrev.canc_dt, 
                              subrev.sub_stat , 
                               subrev.TRIAL_FLG,
                               subrev.DT_RENEW,
                                  subrev.SUB_NUM,
subrev.SUB_REV,
subrev.SUB_REV_REF
order by   acc.accnt_legcy_id,subrev.SUB_REV_REF),

active as (SELECT 
                            cust.integration_id     AS customer, cust.accnt_name as customer_name,
                            acc.accnt_legcy_id      AS account, 
                            acc.accnt_name, 
                            cust.cust_sub_class_2   AS segment, 
                            prod.prod_famly         AS prodfam, 
                            prod.prod_cd, 
                            PROD.PROD_NAME, 
                            prod.prod_medium_cd, 
                              subrev.dt_start, 
                            subrev.dt_end, 
                            subrev.canc_dt, 
                              subrev.sub_stat ,
                              subrev.DT_RENEW,
                                subrev.TRIAL_FLG , 
                            gens.sys_delete_flg, 
                            subrev.SUB_NUM,
subrev.SUB_REV,
subrev.SUB_REV_REF,
subrev.CAE_DATE,
subrev.CAE_FLG,
                            SUM(fsub.doc_amt) AS amount, 
                            sum(finv.doc_amt) as invoice 
                        FROM 
                            law.f_subscr_rev    fsub  
                            JOIN law.d_customer_x    cust ON fsub.cus_wid = cust.row_wid 
                            JOIN law.d_product       prod ON fsub.prod_wid = prod.row_wid 
                            JOIN law.d_subscr_rev    subrev ON subrev.row_wid = fsub.row_wid 
                            JOIN law.d_fin_accnt_x   acc ON acc.row_wid = fsub.fa_wid 
                            INNER JOIN law.d_position  p ON p.row_wid = acc.pos_pr_wid 
                            left join LAW.f_invoice_ln finv on subrev.row_wid = finv.subr_wid 
                            join pdl.gen_s_line gens on gens.sys_pguid = subrev.pguid and gens.sys_current_flg = 'Y' 
                        WHERE 
                            1 = 1 
                            AND fsub.delete_flg = 'N' 
                            AND  fsub.bu_pguid = 'UK' 
                            and prod.prod_famly  in ('Tolley Library','Tax Library')
                           -- and prod.prod_cd = 'TOLM03'
                           -- and  acc.accnt_legcy_id = 'CVRO5000'
                           -- and subrev.DT_RENEW between '01-DEC-20' and '31-DEC-20'
                           and subrev.sub_stat IN ('Complete at End',  'Active','Cancel At End') 
                           and subrev.TRIAL_FLG = 'N'
                             and p.postn_rep_cd !='--' 
                            and cust.cust_sub_class_2 not in ('Internal','External Test')
                        GROUP BY 
                             cust.integration_id, cust.accnt_name,
                            acc.accnt_legcy_id, 
                            acc.accnt_name, 
                            cust.cust_sub_class_2, 
                            prod.prod_famly, 
                            subrev.CAE_DATE,
subrev.CAE_FLG,
                            prod.prod_cd, 
                            PROD.PROD_NAME, 
                            prod.prod_medium_cd, 
                            gens.sys_delete_flg, 
                            subrev.dt_start, 
                            subrev.dt_end, 
                            subrev.canc_dt, 
                              subrev.sub_stat , 
                               subrev.TRIAL_FLG,
                               subrev.DT_RENEW,
                                  subrev.SUB_NUM,
subrev.SUB_REV,
subrev.SUB_REV_REF
order by   acc.accnt_legcy_id,subrev.SUB_REV_REF)

select uplift.*,
case when nvl(uplift.pre_value ,0) = 0 then '100%'
else round(((uplift.current_value - uplift.pre_value)/uplift.pre_value)*100,2) || '%' 
end as uplift_percentage
from(
select active.*,
case when active.invoice is not null then active.invoice
else active.amount 
end as current_value,
renew.dt_renew as pre_renew_date,
renew.TRIAL_FLG as pre_TRIAL_FLG,
renew.sub_stat as pre_sub_stat,
renew.invoice as pre_invoice,
renew.amount  as pre_sub_amount,
case when renew.invoice is not null then renew.invoice
else renew.amount 
end as pre_value
from active
join renew on renew.account = active.account
and renew.prod_cd = active.prod_cd
and renew.SUB_num = active.sub_num --should remove new subscriptions

where (case when active.invoice is not null then active.invoice
else active.amount end) > (case when renew.invoice is not null then renew.invoice
else renew.amount end) 
)uplift
order by uplift.account,uplift.SUB_REV_REF;
                               
                       
