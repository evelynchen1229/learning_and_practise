SELECT DISTINCT
  user_id
	, session_id
  , 
    (nullif(json_extract_path_text(user_properties,'onboardingVersion',true),null))

  AS onb_version
FROM "dev"."stg_amplitude"."event"
WHERE event_type = 'app_start'
  AND
    (nullif(json_extract_path_text(user_properties,'onb_version',true),null))
 IS NOT NULL