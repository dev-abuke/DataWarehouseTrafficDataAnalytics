-- models/operational_efficiency.sql
select
    a.track_id,
    a.type,
    a.traveled_d,
    p.avg_speed,
    p.avg_longitudinal_acceleration,
    p.avg_lateral_acceleration,
    case
        when p.avg_speed > 0 then (a.traveled_d / 1000) / p.avg_speed
        else null
    end as efficiency_score
from
    track_data a
join
    {{ ref('vehicle_performance') }} p on a.track_id = p.track_id
