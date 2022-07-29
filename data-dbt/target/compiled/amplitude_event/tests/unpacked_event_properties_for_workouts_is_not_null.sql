-- in the dbt_amplitude.amplitude_workouts table
-- class_length, multiplayer_mode, genre, is_tutorial, studio
-- class_name, class_id, elapsed_time
-- shouldn't be null for class_end and class_quit
-- Therefore return records where this isn't true to make the test fail
SELECT COUNT(client_event_time)
FROM dbt_amplitude.amplitude_workouts
WHERE (class_length IS NULL
    OR multiplayer_mode IS NULL
    OR genre IS NULL
    OR is_tutorial IS NULL
    OR studio IS NULL
    OR class_name IS NULL
    OR class_id IS NULL
    OR elapsed_time IS NULL
    )
    AND event_type != 'class_start'