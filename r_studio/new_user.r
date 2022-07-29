new_users <- dbGetQuery(con2,"
select 
 from_unixtime(first_login_unixtime::integer)::date as date, count(*)::integer
 from accounts.d_accounts
 group by 1 order by 1") |> as.tibble() |> mutate(date = date |> as.Date())
