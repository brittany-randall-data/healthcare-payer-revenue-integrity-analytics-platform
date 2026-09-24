# Healthcare Payer Revenue Integrity Analytics Platform

An independent healthcare analytics engineering portfolio project designed to identify payer and provider configuration discrepancies that may contribute to reimbursement risk and preventable claim denials.

## Live Analytics Application

### Payer Revenue Integrity Command Center

**Live Application:**  
https://payer-revenue-integrity.streamlit.app

The deployed Streamlit command center provides an executive-facing view of provider configuration exceptions, denied claims, and associated synthetic billed charges potentially at risk.

The application dynamically reads the generated revenue-integrity exception analysis and presents:

- **6 providers requiring configuration review**
- **10 denied claims associated with identified exceptions**
- **$5,630 in synthetic billed charges potentially at risk**
- **8 configuration exception flags**
- Provider-level revenue exposure ranking
- Prioritized provider review queue
- Human-readable configuration exception categories
- Analytics architecture and data-flow summary

---

## Business Problem

Healthcare organizations maintain provider, payer enrollment, location, and claims information across multiple systems.

When those systems disagree, configuration issues such as specialty mismatches, incomplete enrollment, terminated participation, closed panels, inactive locations, or provider-status discrepancies can create reimbursement and operational risk.

This project demonstrates how those data sources can be integrated, validated, transformed, reconciled, and presented through a modern healthcare analytics engineering workflow.

## Business Question

Can provider, payer, claims, and enrollment data be integrated to identify reimbursement risk, provider-configuration anomalies, and potentially preventable payment failures before they become larger revenue-cycle problems?

## Project Architecture

**Synthetic Healthcare Data**  
→ **Python Validation & Exception Analysis**  
→ **Snowflake RAW Data Warehouse**  
→ **SQL Reconciliation & Analytics Views**  
→ **dbt Transformation & Data Quality Testing**  
→ **Revenue Integrity Analytics**  
→ **Streamlit Command Center**

## Technology Stack

- Python
- pandas
- SQL
- Snowflake
- dbt
- Streamlit
- Altair
- Git
- GitLab
- GitHub

## Data

The project uses entirely synthetic healthcare data created specifically for portfolio demonstration.

The relational dataset includes:

- Provider master data
- Provider locations
- Payer enrollment and participation data
- Claims and reimbursement data

**No patient information, PHI, employer data, or proprietary healthcare organization data is used.**

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

A Snowflake warehouse was implemented with separate **RAW** and **ANALYTICS** layers.

The RAW layer contains:

- `PROVIDERS`
- `PROVIDER_LOCATIONS`
- `PAYER_ENROLLMENT`
- `CLAIMS`

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

The completed dbt build successfully executed **4 Snowflake view models and 20 automated data tests with 24/24 resources completed successfully and zero errors**.

## Revenue Integrity Findings

The synthetic analysis identified:

- **6 provider-level configuration exceptions**
- **10 denied claims associated with those exceptions**
- **$5,630 in synthetic billed charges potentially at risk**
- **8 total configuration exception flags**

Detected exception categories include:

- Specialty mismatch
- Pending enrollment
- Terminated enrollment
- Closed payer panel
- Inactive provider location
- Inactive provider with active payer enrollment

The **$5,630** represents synthetic billed charges associated with denied claims and identified configuration exceptions. It does **not** represent recovered revenue, confirmed lost revenue, or guaranteed recoverable revenue.

## Payer Revenue Integrity Command Center

The analytics layer is delivered through a deployed Streamlit application designed to translate technical findings into an executive-facing decision tool.

The command center includes:

### Executive KPIs
- Providers requiring review
- Denied claims
- Synthetic billed charges potentially at risk
- Total configuration exception flags

### Revenue Exposure Analysis
Providers are ranked by synthetic billed charges associated with denied claims to highlight where review may be prioritized.

### Priority Review Queue
The application presents provider, payer, line-of-business, configuration exception, denied-claim, and financial-exposure information in a consolidated review queue.

Machine-oriented exception codes are transformed into human-readable business labels to improve usability for operational stakeholders.

### Live Application

https://payer-revenue-integrity.streamlit.app

## Repository Structure

- `data/` — synthetic source datasets
- `src/` — Python validation and revenue-integrity analysis
- `sql/` — Snowflake warehouse and analytics SQL
- `dbt/` — dbt transformation models, source definitions, and automated data-quality tests
- `outputs/` — generated revenue-integrity exception analysis
- `docs/` — project documentation and data model
- `dashboard.py` — deployed Streamlit Payer Revenue Integrity Command Center

## Project Status

### Completed

- Synthetic relational healthcare dataset
- Python validation pipeline
- Revenue-integrity exception analysis
- Snowflake RAW data warehouse
- Snowflake SQL reconciliation
- Reusable Snowflake analytics views
- dbt staging transformation layer
- Automated dbt data-quality testing
- Executive revenue-integrity dashboard
- Priority provider review queue
- Streamlit analytics application
- Public Streamlit deployment
- Git/GitLab version control
- Public GitHub portfolio repository

### Potential Future Enhancements

- Exception severity and prioritization scoring
- Expanded payer-location reconciliation rules
- Additional analytical models
- Expanded payer and line-of-business filtering

## Portfolio Data Disclaimer

This project is an independent portfolio demonstration built entirely with synthetic healthcare data.

No patient information, PHI, employer data, proprietary healthcare organization data, or confidential payer information is included.

Financial amounts are synthetic and are used solely to demonstrate analytics engineering, reconciliation, data-quality, and revenue-integrity concepts.

## Author

**Brittany S. Randall**  
**M.S. Data Analytics – Decision Process Engineering**
