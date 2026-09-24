-- Healthcare Payer Revenue Integrity Analytics Platform
-- Snowflake Revenue Integrity Analytics Layer
-- Reconciles provider, payer enrollment, location, and claims data
-- to identify configuration exceptions and quantify synthetic billed
-- charges associated with denied claims.

USE DATABASE HEALTHCARE_REVENUE_INTEGRITY;

CREATE SCHEMA IF NOT EXISTS ANALYTICS;

USE SCHEMA ANALYTICS;


-- ============================================================
-- 1. PROVIDER CONFIGURATION EXCEPTIONS
-- ============================================================

CREATE OR REPLACE VIEW ANALYTICS.PROVIDER_CONFIGURATION_EXCEPTIONS AS

SELECT
    p.provider_id,
    p.provider_name,
    p.specialty AS master_specialty,
    pe.payer_name,
    pe.line_of_business,
    pe.enrollment_status,
    pe.payer_specialty,
    pe.panel_status,
    pl.location_status,
    p.active_status AS provider_status,

    ARRAY_TO_STRING(
        ARRAY_COMPACT(
            ARRAY_CONSTRUCT(
                IFF(
                    p.specialty <> pe.payer_specialty,
                    'SPECIALTY_MISMATCH',
                    NULL
                ),

                IFF(
                    pe.enrollment_status = 'Pending',
                    'PENDING_ENROLLMENT',
                    NULL
                ),

                IFF(
                    pe.enrollment_status = 'Terminated',
                    'TERMINATED_ENROLLMENT',
                    NULL
                ),

                IFF(
                    pe.panel_status = 'Closed',
                    'CLOSED_PANEL',
                    NULL
                ),

                IFF(
                    pl.location_status = 'Inactive',
                    'INACTIVE_LOCATION',
                    NULL
                ),

                IFF(
                    p.active_status = 'Inactive'
                    AND pe.enrollment_status = 'Active',
                    'INACTIVE_PROVIDER_ACTIVE_ENROLLMENT',
                    NULL
                )
            )
        ),
        ' | '
    ) AS exception_types

FROM RAW.PROVIDERS p

LEFT JOIN RAW.PAYER_ENROLLMENT pe
    ON p.provider_id = pe.provider_id

LEFT JOIN RAW.PROVIDER_LOCATIONS pl
    ON p.provider_id = pl.provider_id
    AND pe.payer_location_id = pl.location_id;


-- ============================================================
-- 2. REVENUE INTEGRITY EXCEPTION ANALYSIS
-- ============================================================

CREATE OR REPLACE VIEW ANALYTICS.REVENUE_INTEGRITY_EXCEPTIONS AS

SELECT
    e.provider_id,
    e.provider_name,
    e.exception_types,
    COUNT(c.claim_id) AS total_claims,
    COUNT_IF(c.claim_status = 'Denied') AS denied_claims,

    SUM(
        CASE
            WHEN c.claim_status = 'Denied'
            THEN c.billed_amount
            ELSE 0
        END
    ) AS potential_revenue_at_risk

FROM ANALYTICS.PROVIDER_CONFIGURATION_EXCEPTIONS e

LEFT JOIN RAW.CLAIMS c
    ON e.provider_id = c.provider_id

WHERE e.exception_types <> ''

GROUP BY
    e.provider_id,
    e.provider_name,
    e.exception_types;


-- ============================================================
-- 3. VALIDATION SUMMARY
-- Expected synthetic results:
-- 6 provider-level configuration exceptions
-- 10 denied claims
-- $5,630 in synthetic billed charges potentially at risk
-- ============================================================

SELECT
    COUNT(*) AS provider_exceptions,
    SUM(denied_claims) AS denied_claims,
    SUM(potential_revenue_at_risk) AS potential_revenue_at_risk
FROM ANALYTICS.REVENUE_INTEGRITY_EXCEPTIONS;


-- ============================================================
-- 4. PRIORITIZED EXCEPTION REPORT
-- ============================================================

SELECT
    provider_id,
    provider_name,
    exception_types,
    total_claims,
    denied_claims,
    potential_revenue_at_risk
FROM ANALYTICS.REVENUE_INTEGRITY_EXCEPTIONS
ORDER BY potential_revenue_at_risk DESC;