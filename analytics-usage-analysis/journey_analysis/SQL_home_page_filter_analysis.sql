/* in the past three months 
  - how many sessions have seen
	nav_favourite_toggle and nav_filter_toggle
  in the past three months
  - how many sessions have seen
	people checking classes in collection
  (collections_detail_open, collection_class_start)
  in the past three months
  - for sessions just in the explore screen / home screen
	how many pages do people normally scroll
  in the past three months
  , how many classes started from favourite, filter and collection vs total class_start
	-  (class_start_collections)
*/
SET timezone TO utc;
WITH user_pool AS (
    SELECT am.platform_account_id AS user_id
    FROM accounts.account_mapping AS am
    WHERE am.platform NOT IN ('editor', 'creator')
        AND LOWER(am.platform) NOT LIKE '%test%'
)

-- total number of sessions where users play classes in the last three months
, total_workout_session AS (
    SELECT DISTINCT
        aw.user_id
        , aw.session_id
    FROM workouts.f_workouts_amplitude AS aw
        INNER JOIN user_pool ON user_pool.user_id = aw.user_id
    WHERE aw.event_type = 'class_start'
        AND DATE(aw.client_event_time) >= TO_DATE('2022-04-01', 'yyyy-mm-dd')
)

-- total number of sessions when users play classes have seen users clicked
-- filter, favourites, and collections to view classes
, non_home_screen_session_detail AS (
    SELECT DISTINCT
        ae.user_id
        , ae.session_id
        , ae.event_type
        , ae.client_event_time
    FROM stg_amplitude.event AS ae
        INNER JOIN total_workout_session AS tws
            ON tws.session_id = ae.session_id
                AND ae.user_id = tws.user_id
    WHERE ae.event_type LIKE 'nav_filter%'
        OR ae.event_type LIKE '%collections%'
        OR ae.event_type = 'nav_toggle_favourites'
)

, home_screen_only_session AS (
    SELECT DISTINCT
        tws.user_id
        , tws.session_id
    FROM total_workout_session AS tws
        LEFT JOIN non_home_screen_session_detail AS nhss
            ON tws.session_id = nhss.session_id
                AND tws.user_id = nhss.user_id
    WHERE nhss.user_id IS NULL
)

-- do people normally scroll down the pages and how many pages do people normally scroll down
, home_screen_explore AS (
    SELECT DISTINCT
        hsos.user_id
        , hsos.session_id
        , ae.event_type
        , ae.client_event_time
    FROM home_screen_only_session AS hsos
        LEFT JOIN dbt_amplitude_test.amplitude_event AS ae
            ON hsos.session_id = ae.session_id
                AND hsos.user_id = ae.user_id
                AND ae.event_type LIKE 'nav_arrow%'
)

SELECT
    'total_class start sessions' AS event_type
    , COUNT(DISTINCT user_id) AS number_of_unique_users
    , COUNT(DISTINCT user_id || '-' || session_id) AS number_of_real_sessions
FROM total_workout_session
UNION ALL
SELECT
    'non home screen checked' AS event_type
    , COUNT(DISTINCT user_id) AS number_of_unique_users
    , COUNT(DISTINCT user_id || '-' || session_id) AS number_of_sessions
FROM non_home_screen_session_detail
UNION ALL
SELECT
    event_type
    , COUNT(DISTINCT user_id) AS number_of_unique_users
    , COUNT(DISTINCT user_id || '-' || session_id) AS number_of_sessions
FROM non_home_screen_session_detail
GROUP BY event_type
UNION ALL
SELECT
    'home screen checked only' AS event_type
    , COUNT(DISTINCT user_id) AS number_of_unique_users
    , COUNT(DISTINCT user_id || '-' || session_id) AS number_of_sessions
FROM home_screen_only_session
UNION ALL
SELECT
    CASE WHEN event_type IS NULL THEN 'first page home screen only'
        ELSE 'more pages checked from home screen'
    END AS event_type
    , COUNT(DISTINCT user_id) AS number_of_unique_users
    , COUNT(DISTINCT user_id || '-' || session_id) AS number_of_sessions
FROM home_screen_explore
GROUP BY
    CASE WHEN event_type IS NULL THEN 'first page home screen only'
        ELSE 'more pages checked from home screen'
    END
;
