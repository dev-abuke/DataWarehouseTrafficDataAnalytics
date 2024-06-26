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
    Round((sum(Cast(total_distance as numeric)) / 1000), 2) as total_distance_km,
    Round(avg(Cast(track_avg_speed as numeric)), 2) as avg_speed_kmh,
    Round(min(Cast(instant_speed as numeric)), 2) as min_speed_kmh,
    Round(max(Cast(instant_speed as numeric)), 2) as max_speed_kmh,
    Round(avg(Cast(lon_acc as numeric)), 2) as avg_longitudinal_acc_ms2,
    Round(avg(Cast(lat_acc as numeric)), 2) as avg_lateral_acc_ms2,
    Round(max(Cast(lon_acc as numeric)), 2) as max_longitudinal_acc_ms2,
    Round(max(Cast(lat_acc as numeric)), 2) as max_lateral_acc_ms2,
    Round(min(Cast(lon_acc as numeric)), 2) as min_longitudinal_acc_ms2,
    Round(min(Cast(lat_acc as numeric)), 2) as min_lateral_acc_ms2
  from base_data
  group by track_id, type
)

select
  *,
  Round(Cast((total_distance_km / nullif(avg_speed_kmh, 0)) as numeric), 2) as estimated_travel_time_hours
from aggregated_metrics
