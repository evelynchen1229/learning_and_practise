cohorts <-
  subscriptions %>%
  group_by(ownerid) %>% 
  slice(which.min(as.Date(start_date))) %>%
  mutate(free_cohort = start_date,
         free_cohort_month = start_date %>% as.Date() %>% round_date('month')
  ) %>%
  select(ownerid, free_cohort, free_cohort_month)


cohorts_excl_ft <-
  subscriptions %>% 
  filter(sub_type!='Free Trial') %>% 
  group_by(ownerid) %>% 
  slice(which.min(as.Date(start_date))) %>%
  mutate(cohort = start_date,
         cohort_month = start_date %>% as.Date() %>% round_date('month')
  ) %>%
  select(ownerid, cohort, cohort_month, sub_type)