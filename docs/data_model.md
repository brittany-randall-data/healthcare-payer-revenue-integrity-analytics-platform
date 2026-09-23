# Healthcare Payer Revenue Integrity Data Model

## Overview

The platform uses multiple related datasets to simulate healthcare provider, payer, enrollment, claims, and reimbursement workflows.

The data model is designed to support analysis of discrepancies between provider information, payer configuration, participation status, and reimbursement outcomes.

## Core Tables

### providers

Stores the authoritative provider profile used by the analytical platform.

Key fields:

- provider_id
- npi
- provider_name
- specialty
- taxonomy_code
- provider_type
- active_status

### provider_locations

Stores provider practice-location information.

Key fields:

- provider_id
- location_id
- location_name
- city
- state
- zip_code
- location_status

### payer_enrollment

Stores provider enrollment and participation information by payer and line of business.

Key fields:

- enrollment_id
- provider_id
- payer_name
- line_of_business
- enrollment_status
- effective_date
- termination_date
- panel_status
- payer_specialty
- payer_location_id

### claims

Stores synthetic claim and reimbursement outcomes used for revenue-integrity analysis.

Key fields:

- claim_id
- provider_id
- payer_name
- line_of_business
- service_date
- billed_amount
- paid_amount
- claim_status
- denial_reason

## Relationships

providers  
→ provider_locations through `provider_id`

providers  
→ payer_enrollment through `provider_id`

providers  
→ claims through `provider_id`

payer_enrollment  
→ claims through provider, payer, and line-of-business attributes

## Analytical Logic

The platform will compare records across these datasets to identify:

1. Provider specialty mismatches
2. Provider location mismatches
3. Missing payer enrollment
4. Inactive or terminated participation
5. Line-of-business participation gaps
6. Closed or inconsistent panel status
7. Claims associated with enrollment discrepancies
8. Potential reimbursement at risk

## Revenue Integrity Concept

A provider may appear correctly configured in one source while payer enrollment or claim data contains conflicting information.

The analytical workflow will identify these inconsistencies, classify the type of discrepancy, and evaluate whether the discrepancy is associated with reimbursement risk.

## Data Governance

All records used in this project will be synthetic or derived from public data.

No PHI, proprietary employer data, confidential payer records, or actual patient claim information will be used.