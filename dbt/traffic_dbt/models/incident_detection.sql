-- models/incident_detection.sql
with speed_changes as (
  select
    track_id,
    time,
    speed,
    lon_acc,
    lat_acc,
    lag(speed) over (partition by track_id order by time) as previous_speed,
    speed - lag(speed) over (partition by track_id order by time) as speed_change
  from
    trajectory_data
)

select
  track_id,
  time,
  speed,
  lon_acc,
  lat_acc,
  previous_speed,
  speed_change
from
  speed_changes
where
  abs(speed_change) > 20  -- Threshold for speed change that might indicate an incident
