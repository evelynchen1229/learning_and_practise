-- in the past three months
-- how many sessions have seen nav_favourite_toggle and nav_filter_toggle
-- in the past three months
-- how many sessions have seen people checking classes in collection
-- (collections_detail_open, collection_class_start)
-- in the past three months, for sessions just in the
-- explore screen / home screen, how many pages do people normally scroll
-- in the past three months, how many classes started from favourite,
-- filter and collection vs total class_start
--(class_start_collections)
SET timezone TO utc;
WITH user_pool AS (
    SELECT am.platform_account_id AS user_id
    FROM user_echen.account_mapping AS am
    WHERE am.platform NOT IN ('editor', 'creator')
        AND LOWER(am.platform) NOT LIKE '%test%'
        AND am.platform_account_id != '4769976666464260' --myself
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

, sessions_in_scope AS (
    SELECT DISTINCT
        tws.user_id
        , tws.session_id
        , tws.membership_status
    FROM total_workout_session AS tws
        LEFT JOIN tutorial_or_mulplay_invited_only AS tm
            ON tm.user_id = tws.user_id AND tws.session_id = tm.session_id
    WHERE tm.user_id IS NULL
)

-- total number of sessions when users play classes have seen users
-- clicked filter, favourites, and collections to view classes
, non_home_screen_session_detail AS (
    SELECT DISTINCT
        ae.user_id
        , ae.session_id
        , ae.event_type
        , sis.membership_status
        , CASE WHEN ae.event_type LIKE '%filter%' THEN 'filter_used'
            WHEN ae.event_type LIKE '%collections%' THEN 'collection_used'
            WHEN ae.event_type LIKE '%favourites%' THEN 'favourites_used'
            WHEN ae.event_type LIKE '%search%' THEN 'search_bar_used'
            ELSE ae.event_type
        END AS event_category
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

-- do people normally scroll down the pages
-- and how many pages do people normally scroll down
, home_screen_explore AS (
    SELECT DISTINCT
        hsos.user_id
        , hsos.session_id
        , ae.event_type
        , hsos.membership_status
    FROM home_screen_only_session AS hsos
        LEFT JOIN stg_amplitude.event AS ae
            ON hsos.session_id = ae.session_id
                AND hsos.user_id = ae.user_id
                AND ae.event_type LIKE 'nav_arrow%'
)

SELECT
    COUNT(DISTINCT user_id) AS number_of_unique_users
    , COUNT(DISTINCT user_id || '-' || session_id)
    AS number_of_real_sessions
    , membership_status
    , 'total_class start sessions' AS event_type
FROM sessions_in_scope
GROUP BY membership_status
UNION ALL
SELECT
    COUNT(DISTINCT user_id) AS number_of_unique_users
    , COUNT(DISTINCT user_id || '-' || session_id)
    AS number_of_sessions
    , membership_status
    , 'non home screen checked' AS event_type
FROM non_home_screen_session_detail
GROUP BY membership_status
UNION ALL
SELECT
    COUNT(DISTINCT user_id) AS number_of_unique_users
    , COUNT(DISTINCT user_id || '-' || session_id)
    AS number_of_sessions
    , membership_status
    , event_category AS event_type
FROM non_home_screen_session_detail
GROUP BY event_category, membership_status
UNION ALL
SELECT
    COUNT(DISTINCT user_id) AS number_of_unique_users
    , COUNT(DISTINCT user_id || '-' || session_id)
    AS number_of_sessions
    , membership_status
    , 'home screen checked only' AS event_type
FROM home_screen_only_session
GROUP BY membership_status
UNION ALL
SELECT
    COUNT(DISTINCT user_id) AS number_of_unique_users
    , COUNT(DISTINCT user_id || '-' || session_id)
    AS number_of_sessions
    , membership_status
    , CASE WHEN event_type IS NULL THEN 'first page home screen only'
        ELSE 'more pages checked from home screen'
    END AS event_type
FROM home_screen_explore
GROUP BY
    CASE WHEN event_type IS NULL THEN 'first page home screen only'
        ELSE 'more pages checked from home screen'
    END
    , membership_status
;
