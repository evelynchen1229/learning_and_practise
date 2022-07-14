with cancel as
 
(SELECT 
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
                             and subrev.TRIAL_FLG = 'N'
                            
                            and p.postn_rep_cd !='--' 

                            and cust.cust_sub_class_2 not in ('Internal','External Test')
                            and subrev.sub_stat not IN ('Frozen','Pending','Held') 
                             -- subscriptions due to renew in december but didn't; either cancelled or complete without new sub; 
                            --flag for cancelled with new sub afterwards
                             and subrev.DT_RENEW between '01-NOV-20' and '30-NOV-20'


                        GROUP BY 
                             cust.integration_id, cust.accnt_name,
                            acc.accnt_legcy_id, 
                            acc.accnt_name,  
                            cust.cust_sub_class_2, 
                            prod.prod_famly, 
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
,

future_sub as (SELECT 
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
                            and subrev.sub_stat not IN ('Frozen','Pending','Held') 
                            and p.postn_rep_cd !='--' 
                            and cust.cust_sub_class_2 not in ('Internal','External Test')
                             and subrev.TRIAL_FLG = 'N'
                          and subrev.DT_RENEW >= '01-DEC-20' 
                           --and subrev.DT_RENEW between '01-DEC-20' and '31-DEC-20'
                            
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

cancel_sub as
(select cancel.*,
case when cancel.invoice is not null then cancel.invoice
else cancel.amount 
end as pre_value,
case when future_sub.sub_rev is not null then 'Y'
else 'N' end as Have_New_Subscription,
future_sub.sub_rev_ref future_sub,
future_sub.sub_stat future_sub_status,
   future_sub.dt_start future_start, 
future_sub.dt_end future_end, 
future_sub.canc_dt future_cancel, 
future_sub.amount future_amount,
future_sub.invoice future_invoice,
case when future_sub.invoice is not null then future_sub.invoice
else future_sub.amount 
end as future_value

from cancel
left join future_sub
on cancel.account = future_sub.account
and cancel.prod_cd = future_sub.prod_cd

where 
future_sub.sub_rev is null -- no following subs
or cancel.sub_stat = 'Cancelled' -- no matther whether there're future subs, return cancelled subs
or (cancel.sub_stat = 'Complete' and future_sub.sub_num != cancel.sub_num)
),

not_full_cancellation as
(select distinct complete.account
from future_sub complete -- get a list of accounts that have renewed the sub
join cancel
on cancel.sub_stat = 'Complete' 
and cancel.sub_num = complete.sub_num)

select cancel_sub.*
from cancel_sub
left join not_full_cancellation
on cancel_sub.account = not_full_cancellation.account
where 1=1 
and not_full_cancellation.account is null
and cancel_sub.prod_Name not like ('PWC INFORM:%')
--and cancel_sub.account = 'AINS5000'
;


/*
select cancel.*,complete.sub_rev_ref 
from (
select cancel.*,
case when cancel.invoice is not null then cancel.invoice
else cancel.amount 
end as pre_value,
case when future_sub.sub_rev is not null then 'Y'
else 'N' end as Have_New_Subscription,
future_sub.sub_rev_ref future_sub,
future_sub.sub_stat future_sub_status,
   future_sub.dt_start future_start, 
future_sub.dt_end future_end, 
future_sub.canc_dt future_cancel, 
future_sub.amount future_amount,
future_sub.invoice future_invoice,
case when future_sub.invoice is not null then future_sub.invoice
else future_sub.amount 
end as future_value

from cancel
left join future_sub
on cancel.account = future_sub.account
and cancel.prod_cd = future_sub.prod_cd

where 
future_sub.sub_rev is null -- no following subs
or cancel.sub_stat = 'Cancelled' -- no matther whether there're future subs, return cancelled subs
or (cancel.sub_stat = 'Complete' and future_sub.sub_num != cancel.sub_num)--might be new subs as well, but need to exclude those renewed but cancelled

 -- checking whtehr future renew data in dec 2020 as well
/*future_sub.sub_rev is not null
and future_sub.sub_rev_ref ! = cancel.sub_rev_ref*/

-- checking future renew subs are all cancelled
/*cancel.sub_stat = 'Complete'
and future_sub.sub_rev is not null
and future_sub.sub_rev_ref ! = cancel.sub_rev_ref*/

-- checking whether new sub can come after complete subs
/*future_sub.sub_rev is not null 
and cancel.sub_stat = 'Complete'
and future_sub.sub_num != cancel.sub_num*/
/*
order by cancel.account,cancel.SUB_REV_REF)cancel
--above gives cancellation at sub level
--jake needs full cancellation
-- to exclude accounts that had renews for other products
left join  
(select complete.account
from
future_sub complete -- get a list of accounts that have renewed the sub
join cancel
on cancel.sub_stat = 'Complete' 
and cancel.sub_num = complete.sub_num
--where complete.sub_rev_ref is null
where cancel.ACCOUNT = 'AINS5000'
;
*/