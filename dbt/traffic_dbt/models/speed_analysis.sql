-- models/speed_analysis.sql
select
    time as hour,
    avg(speed) as average_speed,
    max(speed) as max_speed,
    min(speed) as min_speed
from
    trajectory_data
group by
    hour
order by
    hour
