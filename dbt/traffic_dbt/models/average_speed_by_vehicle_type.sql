-- models/average_speed_by_vehicle_type.sql
select
    type,
    avg(avg_speed) as average_speed
from
    track_data
group by
    type
