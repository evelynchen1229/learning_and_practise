-- Use the `ref` function to select from other models

select *
from "dev"."dbt_amplitude_test"."my_first_dbt_model"
where id = 1