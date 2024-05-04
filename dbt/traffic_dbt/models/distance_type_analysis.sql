-- models/distance_type_analysis.sql
select
    type,
    Round((sum(Cast(traveled_d as numeric)) / 1000), 2) as total_distance_km
from
    track_data
group by
    type
