-- This query is for analysing where did the class_start land from
-- This is based on the previous event before class_start
WITH user_pool AS (
    SELECT am.platform_account_id AS user_id
    FROM user_echen.account_mapping AS am
    WHERE am.platform NOT IN ('editor', 'creator')
        AND LOWER(am.platform) NOT LIKE '%test%'
        -- inter user id (Evelyn) used for testing events
        AND am.platform_account_id != '4769976666464260'
)

, subscribers AS (
    SELECT
        sp.owner_id
        , sp.precise_period_start_time AS st
        , sp.precise_period_end_time AS et
    FROM subs.sub_periods AS sp
    WHERE sp.period_length > 7
)

, legacy_users AS (
    SELECT DISTINCT am.platform_account_id AS owner_id
    FROM accounts.f_content_authorisations AS fca
        INNER JOIN user_echen.account_mapping AS am
            ON fca.account_id = am.account_id
        LEFT JOIN subs.sub_periods AS sub
            ON sub.owner_id = am.platform_account_id
    WHERE fca.source_sku_name IN ('FITXRUSERS', 'EARLYFITXRUSERS', 'BOXVRUSERS')
        AND sub.owner_id IS NULL
)

, trial_users AS (
    SELECT
        sp.owner_id
        , sp.precise_period_start_time AS st
        , sp.precise_period_end_time AS et
    FROM subs.sub_periods AS sp
    WHERE sp.period_length = 7
)

, membership AS (
    SELECT
        owner_id
        , st
        , et
        , 'subscribers' AS sub_type
    FROM subscribers
    UNION ALL
    SELECT
        owner_id
        , st
        , et
        , 'trials' AS sub_type
    FROM trial_users
    UNION ALL
    SELECT
        owner_id
        , FROM_UNIXTIME(-1) AS st
        , SYSDATE AS et
        , 'legacy user' AS sub_type
    FROM legacy_users
)

-- total number of sessions where users play classes in the last three months
, total_workout_session AS (
    SELECT DISTINCT
        wa.user_id
        , wa.session_id
        , CASE WHEN sb.owner_id IS NULL THEN 'free'
            ELSE sb.sub_type END AS membership_status
        -- include different language for tutorial
        , CASE WHEN
            NULLIF(JSON_EXTRACT_PATH_TEXT(
                wa.event_properties, 'classDisplayName', true), null)
            LIKE 'tutori%' THEN 0
            WHEN
                NULLIF(JSON_EXTRACT_PATH_TEXT(
                    wa.event_properties, 'classDipslayName', true), null)
                LIKE 'tutori%' THEN 0
            WHEN
                NULLIF(JSON_EXTRACT_PATH_TEXT(
                    wa.event_properties, 'isTutorial', true), null)
                = 'true' THEN 0
            ELSE 1 END AS is_tutorial
        , CASE WHEN
            NULLIF(JSON_EXTRACT_PATH_TEXT(
                wa.event_properties, 'multiplayerMode', true), null)
            = 'MULTI_PLAYER'
            AND NULLIF(JSON_EXTRACT_PATH_TEXT(
                wa.event_properties, 'isHost', true), null)
            = 'false'
            THEN 0
            ELSE 1
        END AS is_multiplayer_invited
    FROM workouts.f_workouts_amplitude AS wa
        INNER JOIN user_pool ON user_pool.user_id = wa.user_id
        LEFT JOIN membership AS sb ON sb.owner_id = wa.user_id
            AND wa.client_event_time >= sb.st AND wa.client_event_time <= sb.et
    WHERE wa.event_type = 'class_start'
        AND DATE(wa.client_event_time) BETWEEN
        TO_DATE('2022-04-01', 'yyyy-mm-dd')
        AND TO_DATE('2022-06-30', 'yyyy-mm-dd')
)

, tutorial_or_mulplay_invited_only AS (
    SELECT
        user_id
        , session_id
        -- 0 THEN ONLY tutorial classes; >0 AT LEAST 1 non tutorial CLASS
        , SUM(is_tutorial) AS tutorial_only
        -- 0 THEN ONLY "passively" play classes
        , SUM(is_multiplayer_invited) AS multiplay_invited_only
    FROM total_workout_session
    GROUP BY user_id, session_id
    HAVING SUM(is_tutorial) = 0 OR SUM(is_tutorial) = 0
)

, onboarding_sessions AS (
    SELECT DISTINCT
        event.user_id
        , event.session_id
    FROM stg_amplitude.event
        INNER JOIN user_pool
            ON user_pool.user_id = event.user_id
    WHERE event.event_type LIKE 'onb_%'
)

, sessions_in_scope AS (
    SELECT DISTINCT
        tws.user_id
        , tws.session_id
        , tws.membership_status
    FROM total_workout_session AS tws
        LEFT JOIN tutorial_or_mulplay_invited_only AS tm
            ON tm.user_id = tws.user_id AND tws.session_id = tm.session_id
        LEFT JOIN onboarding_sessions AS os
            ON os.user_id = tws.user_id AND os.session_id = tws.session_id
    WHERE tm.user_id IS NULL AND os.user_id IS NULL
)

-- total number of sessions when users play classes have seen users
-- clicked filter, favourites, and collections to view classes
, non_home_screen_session_detail AS (
    SELECT DISTINCT
        ae.user_id
        , ae.session_id
        , ae.event_type
        , sis.membership_status
    FROM stg_amplitude.event AS ae
        INNER JOIN sessions_in_scope AS sis
            ON sis.session_id = ae.session_id AND ae.user_id = sis.user_id
    WHERE ae.event_type LIKE 'nav_filter%'
        OR ae.event_type LIKE '%collections%'
        OR ae.event_type = 'nav_toggle_favourites'
        OR ae.event_type LIKE 'nav_search%'
)

, home_screen_only_session AS (
    SELECT DISTINCT
        sis.user_id
        , sis.session_id
        , sis.membership_status
    FROM sessions_in_scope AS sis
        LEFT JOIN non_home_screen_session_detail AS nhss
            ON sis.session_id = nhss.session_id
                AND sis.user_id = nhss.user_id
    WHERE nhss.user_id IS NULL
)

, class_block AS (
    SELECT
        event.user_id
        , event.session_id
        , hsos.membership_status
        , event.event_type
        , event.event_properties
        , event.client_event_time
        , SUM(CASE WHEN event_type = 'class_start' THEN 1 else 0 end)
            OVER (PARTITION BY event.user_id, event.session_id
                ORDER BY event.client_event_time ASC ROWS UNBOUNDED PRECEDING) AS block
    FROM stg_amplitude.event
        INNER JOIN non_home_screen_session_detail AS nhss
            ON nhss.user_id = event.user_id AND nhss.session_id = event.session_id
    -- INNER JOIN sessions_in_scope AS sis ON sis.user_id = event.user_id AND sis.session_id = event.session_id
    -- INNER JOIN home_screen_only_session AS hsos ON event.user_id = hsos.user_id AND event.session_id = hsos.session_id
    WHERE 
    /*(event_type LIKE 'nav_filter_%'
    OR event_type LIKE '%collections%'
    OR event_type in('nav_toggle_favourites','class_start','class_quit','class_end','nav_bar_home_main','nav_home_main','nav_explore','class_finish','nav_start_multiplayer_class','nav_multiplayer_join_lobby')
    )
    */
        event_type NOT LIKE 'startup%'
        AND event_type NOT LIKE 'app_%'
        AND event_type NOT LIKE '%profile%'
        AND event_type NOT LIKE '%load%'
        AND event_type NOT LIKE 'polling%'
        --AND event_type NOT LIKE 'nav_arrow%'
        AND event_type NOT LIKE 'upsell%'
        AND event_type NOT LIKE '%setting%'
        AND event_type NOT LIKE '%help%'
        AND event_type NOT LIKE '%_env%'
        AND event_type NOT LIKE '%membership%'
        AND event_type NOT LIKE '%trial%'
        AND event_type NOT LIKE '%stats%'
        AND event_type NOT LIKE '%account%'
        AND event_type NOT LIKE 'how%'
        AND event_type NOT LIKE 'what%'
        AND event_type NOT LIKE 'review%'
        AND event_type NOT LIKE '%_result%_screen%'
        AND event_type NOT LIKE '%share%'
        AND event_type NOT LIKE '%email%'
        AND event_type NOT LIKE '%ghost%'
        AND event_type NOT LIKE '%subscription%'
        AND event_type NOT LIKE 'onb_results%'
        AND event_type NOT LIKE '%multiplay%'
        AND event_type NOT LIKE 'milestones_%'
        AND event_type NOT LIKE 'nav_legacy_%'
        AND event_type NOT IN ('nav_legacy_pop_up_90reminder_close','environment_selected','lobby_solo_play_toggle_on','lobby_squats_toggle_off','nav_music_volume','lobby_solo_play_toggle_off'
        ,'nav_class_select','class_start_delayed','onb_results_video_play','wu_toggle_is_on','nav_bar_stats','pause_voice_toggle_off','nav_multiplayer_toggle_microphone','ctr_favourite','nav_squats_on','nav_squats_off'
        ,'nav_favourited','nav_remove_favourited','nav_streak_selection','nav_multiplayer_toggle_users_microphone','pause_voice_toggle_on','nav_focusmode_on','generic_error','onb_results_video_close','ctr_rate_class','onb_video_skip','onb_video_end'
        ,'onb_terms_and_cond','onb_remind_me_later','nav_focusmode_off','onb_video_start','onb_new_user','onb_terms_accept','nav_legacy_pop_up_expired_close','nav_bar_achievements','nav_leaderboard_continue')
        AND NOT (NULLIF(json_extract_path_text(event_properties,'multiplayerMode',true),NULL) = 'MULTI_PLAYER'
                AND NULLIF(json_extract_path_text(event_properties,'isHost',true),NULL) = 'false'
                )
        -- exclude tutorial classes
        AND NOT (NULLIF(json_extract_path_text(event_properties,'classDisplayName',true),NULL) LIKE 'tutori%'
            OR NULLIF(json_extract_path_text(event_properties,'classDipslayName',true),NULL) LIKE 'tutori%'
            OR NULLIF(json_extract_path_text(event_properties,'isTutorial',true),NULL) = 'true'
        )
        AND NULLIF(json_extract_path_text(event_properties,'studio',true),NULL) NOT IN ('WarmUp','CoolDown')
        AND date(event.client_event_time) BETWEEN TO_DATE('2022-06-01', 'yyyy-mm-dd') AND TO_DATE('2022-06-30', 'yyyy-mm-dd')
    ORDER BY user_id,session_id, client_event_time 
)
, location_usage AS (
	SELECT
		class_block.user_id || '-' ||class_block.session_id || '-' || class_block.block AS block_id
		, class_block.user_id
		, class_block.session_id
		, class_block.block
		, class_block.membership_status
		, class_block.event_type
		, class_block.event_properties
		, class_block.client_event_time
		, RANK () over(PARTITION BY class_block.user_id
		, class_block.session_id
		, class_block.block
ORDER BY client_event_time desc) AS row_num
FROM class_block
--WHERE USER_id=4242534702514316 and session_id =  1654037281000
--order by class_block.user_id, class_block.session_id , class_block.client_event_time
)

, favourites_toggles AS (
	SELECT
		block_id
		, event_type
		, COUNT(event_type) % 2 number_of_favourites_toggles
		, MIN(row_num) toggle_stage
	FROM location_usage
	WHERE event_type = 'nav_toggle_favourites'
	GROUP BY block_id,event_type
)

, last_block AS (
SELECT user_id
, session_id
, MAX(block_id) last_block
FROM location_usage
GROUP BY user_id
, session_id
)

, filter_location_usage AS (
    SELECT
        class_block.user_id || '-' ||class_block.session_id || '-' || class_block.block AS block_id
        , class_block.user_id
        , class_block.session_id
        , class_block.block
        , class_block.membership_status
        , class_block.event_type
        , class_block.event_properties
        , class_block.client_event_time
        , RANK () over(PARTITION BY class_block.user_id
        , class_block.session_id
        , class_block.block
        ORDER BY client_event_time asc) AS first_event_row_num
        , RANK () over(PARTITION BY class_block.user_id
        , class_block.session_id
        , class_block.block
        ORDER BY client_event_time desc) AS last_event_row_num
    FROM class_block
    --JOIN non_home_screen_session_detail nhss ON nhss.user_id = class_block.user_id AND nhss.session_id = class_block.session_id
    -- get first class
    WHERE block IN (0,1)
        AND 
         ( event_type LIKE 'nav_filter%'
        OR event_type LIKE '%collections%'
        OR event_type = 'nav_toggle_favourites'
        OR event_type LIKE 'nav_search%'
        OR event_type like '%class_%'
        OR event_type IN ('nav_explore','nav_bar_home_main')
        OR event_type LIKE 'nav_arrow%'
        ) 
        AND event_type != 'class_paused'
    --AND NOT (event_type = 'nav_filter_toggle' AND nullif(json_extract_path_text(event_properties,'Studio',true),'') IN ('CoolDown','WarmUp'))
)
, filter_time_gap AS (
    SELECT DISTINCT
        user_id
        , session_id
        , client_event_time - LAG(client_event_time) OVER (PARTITION BY user_id, session_id ORDER BY block) AS time_gap
    FROM filter_location_usage
    WHERE first_event_row_num = 1
    ORDER BY user_id, session_id, client_event_time
)

, class_completion AS (
    SELECT DISTINCT
        user_id
        , session_id
        , event_type
        , RANK () OVER (PARTITION BY user_id, session_id
    ORDER BY client_event_time desc) AS last_event_row_num
    FROM filter_location_usage
    WHERE block = 1
        AND event_type IN ('class_start','class_quit','class_end','class_finish')
)

, filter_analysis AS (
    SELECT DISTINCT
        flu.user_id
        , flu.session_id
        , flu.membership_status
        , flu.block_id
        , flu.event_type
        , CASE WHEN flu.first_event_row_num = 1 AND flu.last_event_row_num = 1 THEN 'only_event'
            WHEN flu.first_event_row_num = 1 THEN 'first_event'
        ELSE 'last_event'
        END event_order
        , ftg.time_gap
        , ft.number_of_favourites_toggles
        , cc.event_type class_completion
    FROM filter_location_usage flu
        INNER JOIN filter_time_gap ftg ON ftg.user_id = flu.user_id AND ftg.session_id = flu.session_id AND time_gap IS NOT NULL
        INNER JOIN class_completion cc ON cc.user_id = flu.user_id AND cc.session_id = flu.session_id AND cc.last_event_row_num = 1
        LEFT JOIN favourites_toggles ft ON ft.block_id = flu.block_id AND ft.event_type = flu.event_type 
    WHERE block = 0
    AND (flu.first_event_row_num = 1 OR flu.last_event_row_num = 1)
    /*AND ((flu.user_id = 1563177783806269
    AND flu.session_id = 1654103833000)
    OR (flu.user_id = 2041449079318175
    AND flu.session_id = 1654089636000)
    )*/
    ORDER BY user_id, session_id
)

-- find previous event before class_start
SELECT 
    lu.membership_status
    , lu.event_type
    ,count(lu.event_type) number_of_records
    --, number_of_favourites_toggles
    , CASE WHEN lb.last_block IS NULL THEN 'N' ELSE 'Y' END AS last_block
FROM location_usage lu
--LEFT JOIN favourites_toggles ft ON lu.block_id = ft.block_id AND lu.event_type = ft.event_type AND ft.toggle_stage = 1
LEFT JOIN last_block lb ON lb.last_block = lu.block_id
WHERE row_num = 1
GROUP BY lu.event_type--, number_of_favourites_toggles
,CASE WHEN lb.last_block IS NULL THEN 'N' ELSE 'Y' END
,lu.membership_status
UNION ALL 
SELECT 
    lu.membership_status
     ,'total_class_starts' AS event_type
    ,count(lu.event_type) number_of_records
    --, NULL number_of_favourites_toggles
    , 'N' AS last_block
FROM location_usage lu
WHERE event_type = 'class_start'
GROUP BY membership_status
,lu.event_type
;
