## Project Status

🚧 **In Development**

### Completed

- Designed a synthetic relational healthcare dataset spanning provider master, location, payer enrollment, and claims data.
- Built a Python data-validation pipeline to verify required fields, duplicate keys, referential integrity, and claim financial logic.
- Built a cross-source revenue integrity analysis pipeline that reconciles provider, location, payer enrollment, specialty, panel, and claims information.
- Implemented automated business rules to detect specialty mismatches, pending or terminated enrollment, closed panels, inactive locations, and provider-status inconsistencies.
- Linked provider configuration exceptions to denied claims and generated a prioritized exception report.
- Identified 10 synthetic denied claims associated with configuration exceptions, representing $5,630 in synthetic billed charges potentially at risk.

### Current Analytical Results

The initial synthetic dataset produced six provider-level exception records associated with 10 denied claims.

| Exception Category | Example Risk |
| --- | --- |
| Specialty mismatch | Provider specialty differs from payer configuration |
| Pending enrollment | Claims occur before payer enrollment is active |
| Terminated enrollment | Claims associated with terminated payer participation |
| Closed panel | Provider configuration may prevent appropriate member assignment |
| Inactive location | Enrollment or claims activity associated with an inactive practice location |
| Provider-status inconsistency | Active payer enrollment associated with an inactive provider record |

> **Note:** All results are generated from synthetic data. The $5,630 figure represents synthetic billed charges associated with detected exceptions and does not represent actual recovered revenue.

### Next Phase

- Implement analytical warehouse structures in Snowflake.
- Recreate core reconciliation logic using SQL.
- Build dbt transformation models and automated data-quality tests.
- Develop analytical models for provider participation gaps and revenue-integrity monitoring.
- Create executive-facing visualizations and recommendations.



## Snowflake Analytics Warehouse

The project includes a Snowflake analytics warehouse that integrates synthetic provider, payer enrollment, provider location, and claims data.

### RAW Layer

Four source datasets are loaded into the `RAW` schema:

- `PROVIDERS`
- `PROVIDER_LOCATIONS`
- `PAYER_ENROLLMENT`
- `CLAIMS`

The raw layer preserves the source-level healthcare data used for reconciliation and downstream analysis.

### Revenue Integrity Analytics

SQL transformations reconcile provider master data with payer enrollment and location configuration to identify potential revenue-integrity exceptions, including:

- Specialty mismatches
- Pending payer enrollment
- Terminated payer enrollment
- Closed provider panels
- Inactive practice locations
- Active payer enrollment for inactive providers

The resulting provider-level exceptions are joined to synthetic claims data to evaluate denied claims associated with configuration discrepancies.

### Validated Snowflake Results

The current synthetic dataset produces:

- **6 provider-level configuration exceptions**
- **10 denied claims associated with those exceptions**
- **$5,630 in synthetic billed charges potentially at risk**

The $5,630 represents synthetic billed charges associated with denied claims and identified configuration exceptions. It does not represent recovered revenue or guaranteed recoverable revenue.

### Snowflake SQL

Reproducible Snowflake SQL is available in the [`sql/`](sql/) directory:

- `01_create_raw_layer.sql` — database, schema, and source-table definitions
- `02_revenue_integrity_analytics.sql` — cross-source reconciliation, exception detection, claims aggregation, and validation queries