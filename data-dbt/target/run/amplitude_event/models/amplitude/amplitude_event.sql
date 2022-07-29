

  create view "dev"."dbt_amplitude_test"."amplitude_event__dbt_tmp" as (
    SELECT *
  , 
    (nullif(json_extract_path_text(user_properties,'onboardingVersion',true),null))
 
        AS onboarding_version
  , 
    (nullif(json_extract_path_text(event_properties,'multiplayerMode',true),null))
 
  AS multiplayer_mode
  , 
    (nullif(json_extract_path_text(event_properties,'genre',true),null))
 
  AS genre
  , 
    (nullif(json_extract_path_text(event_properties,'isTutorial',true),null))

  AS is_tutorial
  , 
    (nullif(json_extract_path_text(event_properties,'studio',true),null))
 
  AS studio
  , CASE WHEN 
    (nullif(json_extract_path_text(event_properties,'classDisplayName',true),null))
 = ''
      THEN 
    (nullif(json_extract_path_text(event_properties,'classDipslayName',true),null))

      ELSE 
    (nullif(json_extract_path_text(event_properties,'classDisplayName',true),null))

  END AS class_name
  , SPLIT_PART(
    (nullif(json_extract_path_text(event_properties,'classXRefId',true),null))
, '/StudioClass/', 2)
  AS class_id
  , 
    (nullif(json_extract_path_text(event_properties,'quitReasonMultiplayerInvitation',true),null))

  AS class_quit_reason
  , 
    (nullif(json_extract_path_text(event_properties,'timeElapsed',true),'') :: FLOAT)
 AS elapsed_time
  , 
    (nullif(json_extract_path_text(event_properties,'classLength',true),'') :: FLOAT)
 
  AS class_length
FROM "dev"."stg_amplitude"."event"
  ) ;
