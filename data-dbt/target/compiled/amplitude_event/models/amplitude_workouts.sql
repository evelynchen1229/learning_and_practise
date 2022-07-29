

WITH workouts AS (
    SELECT
        client_event_time
        , device_id
        , id
        , server_upload_time
        , amplitude_id
        , event_type_id
        , user_id
        , project_name
        , amplitude_event_type
        , library
        , start_version
        , location_lng
        , location_lat
        , city
        , uuid
        , is_attribution_event
        , idfa
        , paying
        , ip_address
        , language
        , app
        , country
        , region
        , session_id
        , version_name
        , sample_rate
        , ad_id
        , os_version
        , event_type
        , dma
        , schema
        , client_upload_time
        , server_received_time
        , processed_time
        , event_time
        , user_creation_time
        , data
        , groups
        , _insert_id
        , group_properties
        , event_properties
        , user_properties
        , _fivetran_synced
        , 
    (nullif(json_extract_path_text(user_properties,'membership_status',true),null))
 
        AS membership_status
        , 
    (nullif(json_extract_path_text(user_properties,'onboardingVersion',true),null))
 
        AS onboarding_version
        , 
    (nullif(json_extract_path_text(event_properties,'classLength',true),null))
::FLOAT 
        AS class_length
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
    (nullif(json_extract_path_text(event_properties,'timeElapsed',true),null))
::FLOAT 
        AS elapsed_time
    FROM stg_amplitude.event
    WHERE event_type IN ('class_start', 'class_end', 'class_quit')
)

SELECT *
FROM workouts