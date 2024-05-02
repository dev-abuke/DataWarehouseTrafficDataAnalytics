-- models/geospatial_analysis.sql
select
    lat,
    lon,
    count(*) as count_points,
    avg(speed) as avg_speed
from
    {{ ref('trajectory_data') }}
group by
    lat, lon
