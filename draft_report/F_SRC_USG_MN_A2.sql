select sum(F_USG.ACT_COUNT) as actv_count,
D_DS.DS_NAME,
F_USG.DT_WID,
    -- count(distinct case  when F_USG.WU_WID > 0 then F_USG.WU_WID end ) as user_count,
     D_DT.YR_MTH ,
     D_ACC.ACCNT_NAME,
     D_ACC_X.ACCNT_LEGCY_ID as legacy_acc,
     --D_USGSRC.USGSRC_TYPE,
     --D_USGSRC.USGSRC_VER ,
     D_WU.WU_EMAIL ,
     concat(concat(D_WU.FST_NAME, ' '), D_WU.LST_NAME) as user_name,
     D_WU.WU_LOGIN_ID 
 --    D_ACC.ROW_WID as c11
from 
     LAW.D_PROD_FAMILY D_PF /* Dim_ProductFamily */ ,
     LAW.D_WEB_USER D_WU /* Dim_WebUser */ ,
     LAW.D_USG_TYPE D_USGTYPE /* Dim_UsageType */ ,
     LAW.D_USG_SRC D_USGSRC /* Dim_UsageSource */ ,
     LAW.D_FIN_ACCNT D_ACC /* Dim_FinancialAccount */ ,
     LAW.D_FIN_ACCNT_X D_ACC_X /* Dim_FinancialAccount_Legacy */ ,
     LAW.D_DATE D_DT /* Dim_Date_Month */ ,
     LAW.F_SRC_USG_MN_A F_USG, /* Fact_SourceUsage_Month_Agg */ 
    --LAW.F_SRC_USG F_USG,
   LAW.D_DATA_SRC D_DS
where  ( D_USGSRC.USGSRC_TYPE not in ('Unspecified') and D_PF.ROW_WID = F_USG.PF_WID and D_USGTYPE.ROW_WID = F_USG.USGTP_WID and D_ACC_X.ROW_WID = F_USG.FA_WID and D_DT.ROW_WID = F_USG.DT_WID 
and D_ACC.ROW_WID = D_ACC_X.ROW_WID and D_ACC.ROW_WID = F_USG.FA_WID and D_DS.ROW_WID = F_USG.DS_WID
and D_PF.PF_NAME like 'Lexis Check % Draft' and D_USGTYPE.USGTP_TYPE = 'Views' and D_ACC_X.ACCNT_LEGCY_ID = 'CAME5023' and D_WU.ROW_WID = F_USG.WU_WID and F_USG.USGSRC_WID = D_USGSRC.ROW_WID and (F_USG.BU_PGUID in ('UK', 'Unspecified')) and D_DT.YR_MTH = '2018 / 06'  and D_WU.WU_LOGIN_ID in ('DASG@473952') ) 
group by D_DT.YR_MTH, D_ACC.ACCNT_NAME,-- F_USG.DATASOURCE_NUM_ID,
D_DS.DS_NAME,
--D_ACC.ROW_WID,
D_ACC_X.ACCNT_LEGCY_ID, 
D_WU.WU_EMAIL, D_WU.WU_LOGIN_ID,
F_USG.DT_WID,
--D_USGSRC.USGSRC_VER, D_USGSRC.USGSRC_TYPE,
concat(concat(D_WU.FST_NAME, ' '), D_WU.LST_NAME);
