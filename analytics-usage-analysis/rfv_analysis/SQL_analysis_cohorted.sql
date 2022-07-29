-- weekly view by cohorts instead of natrual calendar
SET timezone TO utc;
WITH
-- a user pool showing users who started their first class in May
-- (including tutorial classes)
-- not editors, creators, or test paltforms
-- five users had class_quit in 2021 which didn't have class_start associated
user_pool AS (
    SELECT
        wa.user_id
        , MIN(DATE(wa.client_event_time)) AS first_class_play_date
    FROM dbt_amplitude.amplitude_workouts AS wa
        INNER JOIN user_echen.account_mapping AS am
            ON wa.user_id = am.platform_account_id
    WHERE wa.event_type = 'class_start'
        AND am.platform NOT IN ('editor', 'creator')
        AND LOWER(am.platform) NOT LIKE '%test%'
        -- exception:
        -- below users have class_end date
        -- earlier than their first class_start date
        AND wa.user_id NOT IN ('4594009870614420', '3997484303703512'
            , '5001758036535301', '4077093452313223', '4249103761818757')
        --AND DATE(client_event_time) <= (DATE(sysdate) - 7)
        AND DATE(wa.client_event_time)
        <= (TO_DATE('2022-06-23', 'yyyy-mm-dd') - 7)
    GROUP BY wa.user_id
    -- HAVING MIN(date(client_event_time))
    -- BETWEEN TO_DATE('2022-05-01', 'yyyy/mm/dd') AND DATE(sysdate) - 7
    HAVING MIN(DATE(wa.client_event_time))
        BETWEEN TO_DATE('2022-05-01', 'yyyy/mm/dd')
        AND TO_DATE('2022-06-23', 'yyyy-mm-dd') - 7
)

, class_played_time AS (
    SELECT
        wa.user_id
        , DATE(wa.client_event_time) AS class_play_date
        , SUM(wa.elapsed_time) / 60 AS rough_time_elapsed_minutes
    FROM dbt_amplitude.amplitude_workouts AS wa
        INNER JOIN user_pool AS up ON up.user_id = wa.user_id
    WHERE wa.event_type != 'class_start'
        AND LOWER(wa.class_name) != 'tutorial'
        --AND DATE(wa.client_event_time) < DATE(sysdate)
        AND DATE(wa.client_event_time) < TO_DATE('2022-06-23', 'yyyy-mm-dd')
    GROUP BY wa.user_id, DATE(wa.client_event_time)
)

-- daily view of number of classes played
-- , unique classes played, time spent in classes
-- non tutorial classes
SELECT
    up.user_id
    , up.first_class_play_date
    , DATE(wa.client_event_time) AS class_play_date
    , (DATEDIFF(DAY, up.first_class_play_date
        , DATE(wa.client_event_time)) / 7 + 1) AS week_number
    , DATEDIFF(DAY, up.first_class_play_date
        , DATE(wa.client_event_time)) AS day_number
    , ROUND(cpt.rough_time_elapsed_minutes, 2) AS rough_time_elapsed_minutes
    , COUNT(wa.class_id) AS number_of_classes_started
    , COUNT(DISTINCT wa.class_id) AS unique_number_of_classes_started
FROM user_pool AS up
    INNER JOIN dbt_amplitude.amplitude_workouts AS wa
        ON wa.user_id = up.user_id
    LEFT JOIN class_played_time AS cpt
        ON cpt.user_id = wa.user_id
            AND cpt.class_play_date = DATE(wa.client_event_time)
WHERE wa.event_type = 'class_start'
    AND LOWER(wa.class_name) != 'tutorial'
    --AND DATE(wa.client_event_time) < DATE(sysdate)
    AND DATE(wa.client_event_time) < TO_DATE('2022-06-23', 'yyyy-mm-dd')
GROUP BY
    up.user_id
    , up.first_class_play_date
    , DATE(wa.client_event_time)
    , cpt.rough_time_elapsed_minutes
    , (DATEDIFF(DAY, up.first_class_play_date
        , DATE(wa.client_event_time)) / 7 + 1)
    , DATEDIFF(DAY, up.first_class_play_date
        , DATE(wa.client_event_time))
;
