downloads <- 
  read_sheet("https://docs.google.com/spreadsheets/d/1Y259k_s_zbVFoQ_EMFh4dBkOmre52JtMhY-Z5N0guX0/edit#gid=0",
                        sheet = 'downloads') %>%  
  as_tibble() %>% 
  mutate(date = date %>% as.Date())
