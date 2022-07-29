SELECT DISTINCT
  user_id
	, session_id
  , {{unpack_json('onboardingVersion','user_properties')}}
  AS onb_version
FROM {{source('amplitude','event')}}
WHERE event_type = 'app_start'
  AND{{unpack_json('onb_version','user_properties')}} IS NOT NULL
