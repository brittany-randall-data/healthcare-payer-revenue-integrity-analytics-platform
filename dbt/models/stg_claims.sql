-- Staging model for synthetic claims data
-- Standardizes claims and reimbursement fields
-- for downstream revenue integrity analysis.

select
    claim_id,
    provider_id,
    payer_name,
    line_of_business,
    service_date,
    billed_amount,
    paid_amount,
    claim_status,
    denial_reason
from {{ source('raw', 'claims') }}