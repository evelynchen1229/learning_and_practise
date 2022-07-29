WITH device AS (
  SELECT DISTINCT
    user_id
    , device_type
  FROM {{ref ('stg_amplitude_device')}}
  WHERE device_type IS NOT NULL
)

SELECT
  user_id
  , device_type
  , COUNT(user_id) OVER (PARTITION BY user_id) AS num_devices
FROM device
