SELECT DISTINCT
  user_id
  , session_id
  , {{unpack_json('device_type','user_properties')}}
  AS device_type
FROM {{source('amplitude','event')}}
WHERE event_type = 'app_server_env'
