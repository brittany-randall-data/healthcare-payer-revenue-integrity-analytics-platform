# Healthcare Payer Revenue Integrity Analytics Platform

An independent healthcare analytics engineering portfolio project designed to identify payer and provider configuration discrepancies that may contribute to reimbursement risk and preventable claim denials.

## Business Problem

Healthcare organizations maintain provider, payer enrollment, location, and claims information across multiple systems. When those systems disagree, configuration issues such as specialty mismatches, incomplete enrollment, terminated participation, closed panels, inactive locations, or provider-status discrepancies can create reimbursement and operational risk.

This project demonstrates how those data sources can be integrated and systematically analyzed using a modern analytics engineering workflow.

## Business Question

Can provider, payer, claims, and enrollment data be integrated to identify reimbursement risk, provider-configuration anomalies, and potentially preventable payment failures before they become larger revenue-cycle problems?

## Project Architecture

Synthetic Healthcare Data  
→ Python Validation & Exception Analysis  
→ Snowflake RAW Data Warehouse  
→ SQL Reconciliation & Analytics Views  
→ dbt Transformation & Data Quality Testing  
→ Revenue Integrity Analysis

## Technology Stack

- Python
- pandas
- SQL
- Snowflake
- dbt
- Git / GitLab

## Data

The project uses entirely synthetic healthcare data created specifically for portfolio demonstration.

The relational dataset includes:

- Provider master data
- Provider locations
- Payer enrollment and participation data
- Claims and reimbursement data

No patient information, PHI, employer data, or proprietary healthcare organization data is used.

## Python Validation and Exception Analysis

Python validation scripts were developed to:

- Validate required columns and source structure
- Detect duplicate records
- Validate referential integrity across datasets
- Identify invalid financial values
- Reconcile provider, payer enrollment, and location information
- Flag provider-configuration exceptions
- Associate configuration exceptions with denied claims

## Snowflake Data Warehouse

A Snowflake warehouse was implemented with separate RAW and ANALYTICS layers.

The RAW layer contains:

- PROVIDERS
- PROVIDER_LOCATIONS
- PAYER_ENROLLMENT
- CLAIMS

Reusable SQL analytics views reconcile provider master, payer enrollment, provider location, and claims data to identify configuration discrepancies and quantify associated denied billed charges.

## dbt Transformation and Testing

A dbt project was implemented and connected directly to Snowflake.

Staging models were created for:

- Providers
- Provider locations
- Payer enrollment
- Claims

Automated dbt data-quality tests validate:

- Required values
- Provider identifiers
- NPI identifiers
- Expected provider status values
- Expected enrollment status values
- Expected location status values
- Expected claim status values

The completed dbt pipeline successfully executed **4 Snowflake view models and 20 automated data tests with 24/24 passing and zero errors**.

## Revenue Integrity Findings

The synthetic analysis identified:

- **6 provider-level configuration exceptions**
- **10 denied claims associated with those exceptions**
- **$5,630 in synthetic billed charges potentially at risk**

Detected exception categories include:

- Specialty mismatch
- Pending enrollment
- Terminated enrollment
- Closed payer panel
- Inactive provider location
- Inactive provider with active payer enrollment

The $5,630 represents synthetic billed charges associated with identified configuration exceptions. It does not represent recovered revenue or guaranteed recoverable revenue.

## Repository Structure

- `data/` — synthetic source datasets
- `src/` — Python validation and revenue-integrity analysis
- `sql/` — Snowflake warehouse and analytics SQL
- `dbt/` — dbt transformation models, source definitions, and automated data-quality tests
- `outputs/` — generated revenue-integrity exception analysis
- `docs/` — project documentation and data model

## Project Status

### Completed

- Synthetic relational healthcare dataset
- Python validation pipeline
- Revenue-integrity exception analysis
- Snowflake RAW warehouse
- Snowflake SQL reconciliation
- Reusable Snowflake analytics views
- dbt staging transformation layer
- Automated dbt data-quality testing
- Git/GitLab version control

### Future Enhancements

- Executive visualization/dashboard
- Exception severity and prioritization framework
- Expanded payer-location reconciliation rules
- Additional analytical models

## Author

**Brittany Randall**  
M.S. Data Analytics – Decision Process Engineering