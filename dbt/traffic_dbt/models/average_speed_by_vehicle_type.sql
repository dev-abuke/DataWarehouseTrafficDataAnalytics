-- models/average_speed_by_vehicle_type.sql
select
    type,
    avg(speed) as average_speed
from
    {{ ref('trajectory_data') }}
group by
    type
