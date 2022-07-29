select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      -- in the dbt_amplitude.amplitude_workouts table
-- elapsed_time shouldn't be null for
-- class_end and class_quit
-- Therefore return records where this isn't true to make the test fail
SELECT client_event_time
FROM dbt_amplitude.amplitude_workouts
WHERE elapsed_time IS NULL
    AND event_type != 'class_start'
      
    ) dbt_internal_test