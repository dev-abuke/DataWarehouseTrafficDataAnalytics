-- models/vehicle_performance_analysis.sql
select
    track_id,
    avg(speed) as avg_speed,
    avg(lon_acc) as avg_longitudinal_acceleration,
    avg(lat_acc) as avg_lateral_acceleration
from
    {{ ref('trajectory_data') }}
group by
    track_id
