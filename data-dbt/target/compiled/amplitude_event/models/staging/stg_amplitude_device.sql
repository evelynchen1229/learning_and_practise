SELECT DISTINCT
  user_id
  , session_id
  , 
    (nullif(json_extract_path_text(user_properties,'device_type',true),null))

  AS device_type
FROM "dev"."stg_amplitude"."event"
WHERE event_type = 'app_server_env'