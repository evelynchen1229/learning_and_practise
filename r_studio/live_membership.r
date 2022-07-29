live_paid_members_weekly_monthly <- function(insert_week_start) {
  week_end <- insert_week_start + weeks(1) - days(1)
  subscriptions %>%
    filter(sub_type!='Free Trial', sub_type=='Monthly') %>%
    filter(as.Date(start_date) <= week_end,
           as.Date(end_date) >= insert_week_start) %>%
    summarise(active = n_distinct(ownerid)) %>%
    mutate(w_b = insert_week_start,
           week = insert_week_start %>% format('%y%U') %>% as.numeric()) |>
    select(w_b, week, active)
}
live_paid_members_weekly_monthly_subs_data <- seq(as.Date('2022-01-09'), Sys.Date(), '1 week') %>% map(live_paid_members_weekly_monthly) %>% bind_rows()
live_paid_members_weekly_annual <- function(insert_week_start) {
  week_end <- insert_week_start + weeks(1) - days(1)
  subscriptions %>%
    filter(sub_type!='Free Trial', sub_type=='Annual') %>%
    filter(as.Date(start_date) <= week_end,
           as.Date(end_date) >= insert_week_start) %>%
    summarise(active = n_distinct(ownerid)) %>%
    mutate(w_b = insert_week_start,
           week = insert_week_start %>% format('%y%U') %>% as.numeric()) |>
    select(w_b, week, active)
}
live_paid_members_weekly_annual_subs_data <- seq(as.Date('2022-01-09'), Sys.Date(), '1 week') %>% map(live_paid_members_weekly_annual) %>% bind_rows()
monthly_summary <-
live_paid_members_weekly_monthly_subs_data |>
  left_join(
    cohorts_excl_ft |> filter(sub_type=='Monthly') |>  group_by(week = cohort |> format('%y%U') |> as.numeric()) |>
      summarise(w_b = min(cohort),
                added = n())
  ) |>
  mutate(brought_forward = lag(active,1),
         churn = active-brought_forward-added)
annual_summary <-
  live_paid_members_weekly_annual_subs_data |>
  left_join(
    cohorts_excl_ft |> filter(sub_type=='Annual') |>  group_by(week = cohort |> format('%y%U') |> as.numeric()) |>
      summarise(w_b = min(cohort),
                added = n())
  ) |>
  mutate(brought_forward = lag(active,1),
         churn = active-brought_forward-added)
monthly_summary |> select(w_b, brought_forward, added, churn, active) |> arrange(desc(w_b)) |>  write_csv(paste0('monthly_subs_weekly_summary_', Sys.Date(),'.csv'))
annual_summary |>  select(w_b, brought_forward, added, churn, active) |> arrange(desc(w_b)) |>  write_csv(paste0('annual_subs_weekly_summary_', Sys.Date(),'.csv'))