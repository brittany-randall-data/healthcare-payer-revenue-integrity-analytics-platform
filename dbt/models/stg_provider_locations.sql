-- Staging model for provider location data
-- Standardizes synthetic provider practice locations
-- for downstream revenue integrity analysis.

select
    provider_id,
    location_id,
    location_name,
    city,
    state,
    zip_code,
    location_status
from {{ source('raw', 'provider_locations') }}