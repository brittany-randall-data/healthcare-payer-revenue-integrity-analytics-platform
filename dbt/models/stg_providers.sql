-- Staging model for provider master data
-- Standardizes the RAW.PROVIDERS source for downstream dbt models.

select
    provider_id,
    npi,
    provider_name,
    specialty,
    taxonomy_code,
    provider_type,
    active_status
from {{ source('raw', 'providers') }}