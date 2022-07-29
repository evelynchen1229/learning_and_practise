SELECT *
  , {{ unpack_json('onboardingVersion', 'user_properties') }} 
        AS onboarding_version
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
  , {{unpack_json('quitReasonMultiplayerInvitation') }}
  AS class_quit_reason
  , {{unpack_json_no_null('timeElapsed')}} AS elapsed_time
  , {{ unpack_json_no_null('classLength') }} 
  AS class_length
FROM {{source ('amplitude','event')}} 
