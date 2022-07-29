-- in the dbt_amplitude.amplitude_workouts table
-- class_length, multiplayer_mode, genre, is_tutorial, studio
-- class_name, class_id
-- shouldn't be null
-- Therefore return records where this isn't true to make the test fail
SELECT client_event_time
FROM dbt_amplitude.amplitude_workouts
WHERE class_length IS NULL
    OR multiplayer_mode IS NULL
    OR genre IS NULL
    OR is_tutorial IS NULL
    OR studio IS NULL
    OR class_name IS NULL
    OR class_id IS NULL

