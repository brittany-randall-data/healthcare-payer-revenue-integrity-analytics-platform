-- Staging model for payer enrollment data
-- Standardizes payer enrollment and provider configuration data
-- for downstream revenue integrity analysis.

select
    enrollment_id,
    provider_id,
    payer_name,
    line_of_business,
    enrollment_status,
    effective_date,
    termination_date,
    panel_status,
    payer_specialty,
    payer_location_id
from {{ source('raw', 'payer_enrollment') }}