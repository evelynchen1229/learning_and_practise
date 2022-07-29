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
        , {{ unpack_json('membership_status', 'user_properties') }} 
        AS membership_status
        , {{ unpack_json('onboardingVersion', 'user_properties') }} 
        AS onboarding_version
        , {{ unpack_json('classLength') }}::FLOAT 
        AS class_length
        , {{ unpack_json('multiplayerMode') }} 
        AS multiplayer_mode
        , {{ unpack_json('genre') }} 
        AS genre
        , {{ unpack_json('isTutorial') }}
        AS is_tutorial
        , {{ unpack_json('studio') }} 
        AS studio
        , CASE WHEN {{ unpack_json('classDisplayName') }} = ''
            THEN {{ unpack_json('classDipslayName') }}
            ELSE {{ unpack_json('classDisplayName') }}
        END AS class_name
        , SPLIT_PART({{ unpack_json('classXRefId') }}, '/StudioClass/', 2)
        AS class_id
        , {{ unpack_json('timeElapsed') }}::FLOAT 
        AS elapsed_time
        , {{unpack_json('quitReasonMultiplayerInvitation') }}
        AS class_quit_reason
    FROM {{source ('amplitude','event')}} 
    WHERE event_type IN ('class_start', 'class_end', 'class_quit','class_finish','class_start_collections','class_end_collections','class_restarted','class_replayed')
)

SELECT *
FROM workouts 
