

  create view "dev"."dbt_amplitude_test"."amplitude_device__dbt_tmp" as (
    WITH device AS (
  SELECT DISTINCT
    user_id
    , device_type
 FROM "dev"."dbt_amplitude_test"."stg_amplitude_device"
)

SELECT
  user_id
  , device_type
  , COUNT(user_id) OVER (PARTITION BY user_id) AS num_devices
FROM device
;
  ) ;
