SELECT DISTINCT
  user_id
  , session_id
  , SPLIT_PART({{unpack_json('id')}}, '/PlayerProfile/', 2)
  AS profile_id
FROM stg_amplitude.event e 
WHERE event_type = 'profile_updated'
