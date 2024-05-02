-- models/operational_efficiency.sql
select
    a.track_id,
    a.type,
    a.total_distance,
    p.avg_speed,
    p.avg_longitudinal_acceleration,
    p.avg_lateral_acceleration,
    case
        when p.avg_speed > 0 then a.total_distance / p.avg_speed
        else null
    end as efficiency_score
from
    {{ ref('distance_type_analysis') }} a
join
    {{ ref('vehicle_performance') }} p on distance_type_analysis.track_id = vehicle_performance.track_id
