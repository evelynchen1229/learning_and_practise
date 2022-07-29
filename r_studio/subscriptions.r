

unique_periodstarts <- dbGetQuery(con2, "
select distinct
 ownerid,
 email,
 periodstarttime::date as start_date,
 periodendtime::date as end_date,
 max(from_unixtime(recorddate))::date as latest_record
from subscribers
left join accounts.account_mapping mapping on mapping.platform_account_id = subscribers.ownerid
left join accounts.d_profiles profiles on profiles.account_id = mapping.account_id
group by 1, 2, 3, 4") %>% as.tibble() %>%
  mutate(start_date = start_date %>% as.Date(),
         end_date = end_date %>% as.Date(),
         latest_record = latest_record %>% as.Date())


subscriptions <-
  unique_periodstarts %>%
  filter(!is.na(start_date)) %>%
  group_by(ownerid, start_date) %>%
  slice(which.min(latest_record)) %>% ungroup() %>%
  arrange(ownerid, start_date) %>%
  group_by(ownerid) %>%
  mutate(sub_n = row_number()) %>%
  ungroup() %>%
  mutate(duration = difftime(end_date, start_date, units = 'days') %>% as.numeric(),
         sub_type = case_when(duration <10 ~ 'Free Trial', duration <40 ~ 'Monthly', 1==1 ~ 'Annual'))
