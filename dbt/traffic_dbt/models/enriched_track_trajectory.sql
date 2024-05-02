-- models/enriched_track_trajectory.sql
with base_data as (
  select
    td.track_id,
    td.type,
    td.traveled_d as total_distance,
    td.avg_speed as track_avg_speed,
    traj.lat,
    traj.lon,
    traj.speed as instant_speed,
    traj.lon_acc,
    traj.lat_acc,
    traj.time
  from track_data td
  join trajectory_data traj on td.track_id = traj.track_id
),

aggregated_metrics as (
  select
    track_id,
    type,
    sum(total_distance) as sum_distance,
    avg(track_avg_speed) as avg_speed,
    max(instant_speed) as max_speed,
    min(instant_speed) as min_speed,
    avg(lon_acc) as avg_longitudinal_acc,
    avg(lat_acc) as avg_lateral_acc,
    max(lon_acc) as max_longitudinal_acc,
    max(lat_acc) as max_lateral_acc,
    min(lon_acc) as min_longitudinal_acc,
    min(lat_acc) as min_lateral_acc
  from base_data
  group by track_id, type
)

select
  *,
  sum_distance / nullif(avg_speed, 0) as estimated_travel_time_hours
from aggregated_metrics
