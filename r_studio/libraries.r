library(tidyverse)
library(readr)
library(magrittr)
library(lubridate)
library(scales)
library(tidyverse)
library(googlesheets4)
library(readr)
library(magrittr)
library(gridExtra)
library(DBI)
library(rJava)
library(RJDBC)
library(magrittr) # needs to be run every time you start R and want to use %>%
library(dplyr)  


con2 <- dbConnect(
  RJDBC::JDBC("com.amazon.redshift.jdbc42.Driver",
              "/Users/evelynchen/Documents/redshift-jdbc42-2.1.0.9/redshift-jdbc42-2.1.0.9.jar"),
  "jdbc:redshift://redshift-cluster-1.ct0wmhwbmwm9.us-east-1.redshift.amazonaws.com:5439/dev", 
  "",#user_name
  ""# pw
)
