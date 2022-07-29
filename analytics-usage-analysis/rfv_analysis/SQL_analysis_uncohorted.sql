SET timezone TO utc;
WITH
-- a user pool for users starting a class in May
user_pool AS (
    SELECT
        wa.user_id
        , MIN(DATE(wa.client_event_time)) AS first_class_play_date
    FROM workouts.f_workouts_amplitude AS wa
        INNER JOIN user_echen.account_mapping AS am
            ON wa.user_id = am.platform_account_id
    WHERE wa.event_type = 'class_start'
        AND am.platform NOT IN ('editor', 'creator')
        AND LOWER(am.platform) NOT LIKE '%test%'
    GROUP BY wa.user_id
    HAVING MIN(DATE(wa.client_event_time)) BETWEEN
        TO_DATE('2022-05-01', 'yyyy/mm/dd')
        AND TO_DATE('2022-05-31', 'yyyy/mm/dd')
)

, class_play AS (
    SELECT
        wa.user_id
        , COUNT(DISTINCT DATE(wa.client_event_time)) AS active_days
    FROM workouts.f_workouts_amplitude AS wa
         INNER JOIN user_pool AS up ON up.user_id = wa.user_id
    WHERE wa.event_type = 'class_start'
    GROUP BY wa.user_id
)

, class_play_frequency AS (
    SELECT
        wa.user_id
        , DATE_PART(WEEK, DATE(wa.client_event_time)) AS class_play_week
        , COUNT(DISTINCT DATE(wa.client_event_time)) AS active_days
    FROM workouts.f_workouts_amplitude AS wa
        INNER JOIN user_pool AS up ON up.user_id = wa.user_id
    WHERE wa.event_type = 'class_start'
    GROUP BY wa.user_id, DATE_PART(WEEK, DATE(wa.client_event_time))
)

, class_played_time AS (
    SELECT
        wa.user_id
        , SUM(DECODE(JSON_EXTRACT_PATH_TEXT(
            wa.event_properties, 'timeElapsed', true), '', null
            , JSON_EXTRACT_PATH_TEXT(
                wa.event_properties, 'timeElapsed', true))::FLOAT)
        AS rough_time_elapsed
    FROM workouts.f_workouts_amplitude AS wa
        INNER JOIN user_pool AS up ON up.user_id = wa.user_id
    WHERE wa.event_type != 'class_start'
        AND DATE(wa.client_event_time) >= TO_DATE('2022-05-01', 'yyyy/mm/dd')
    GROUP BY wa.user_id
)

-- recency
/*SELECT
    active_days
    , COUNT(user_id) AS number_of_users
FROM class_play
GROUP BY active_days
ORDER BY 2 DESC
;
-- frequency
SELECT
    active_days AS class_play_days_per_week
    , COUNTt(user_id) AS frequency
FROM class_play_frequency
GROUP BY class_play_days_per_week
ORDER BY 2 DESC
;*/
-- volume
/*SELECT
    event_type
    , ROUND(SUM(rough_time_elapsed) / 60, 0) AS elapse_time_min
FROM class_played_time
GROUP BY 1
ORDER BY 2 DESC
;*/

SELECT DISTINCT
    cp.user_id
    , cp.active_days AS total_active_days
    , SUM(pf.active_days) OVER (
        PARTITION BY pf.user_id) / COUNT(pf.class_play_week) OVER
    (PARTITION BY pf.user_id) AS average_days_per_week
    , ROUND(pt.rough_time_elapsed / 60, 0) AS total_elapse_time_min
FROM class_play AS cp
    INNER JOIN class_play_frequency AS pf ON pf.user_id = cp.user_id
    INNER JOIN class_played_time AS pt ON pt.user_id = cp.user_id
;
