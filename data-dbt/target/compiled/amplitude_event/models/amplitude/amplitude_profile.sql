SELECT DISTINCT
  user_id
  , session_id
  , SPLIT_PART(
    (nullif(json_extract_path_text(event_properties,'id',true),null))
, '/PlayerProfile/', 2)
  AS profile_id
FROM stg_amplitude.event e 
WHERE event_type = 'profile_updated'