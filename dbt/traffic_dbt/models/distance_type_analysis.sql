-- models/distance_type_analysis.sql
select
    track_id,
    type,
    sum(traveled_d) as total_distance
from
    track_data
group by
    track_id, type
