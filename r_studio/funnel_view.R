funnel_metrics <-
  downloads %>% filter(date>='2022-01-02') %>% group_by(week = date %>% format('%U')) %>% summarise(w_b = min(date) %>% as.Date(), downloads = sum(downloads)) %>%
  left_join(
    new_users %>% filter(date>='2022-01-02') %>% group_by(week = date %>% format('%U')) %>% summarise(users = sum(count))
  ) %>%
  left_join(
    cohorts %>% ungroup() %>% filter(free_cohort>='2022-01-02') %>% group_by(week = free_cohort %>% format('%U')) %>% summarise(freetrials = n())
  ) %>%
  left_join(
    cohorts_excl_ft %>% ungroup() %>% filter(cohort>='2022-01-02') %>% group_by(week = cohort %>% format('%U')) %>% summarise(memberships = n())
  )