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