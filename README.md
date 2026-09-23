# Healthcare Payer Revenue Integrity Analytics Platform

An independent healthcare analytics engineering project designed to identify provider enrollment, payer configuration, participation, and reimbursement discrepancies that may create operational and revenue-cycle risk.

## Business Problem

Healthcare organizations rely on provider, payer, enrollment, specialty, location, and reimbursement data distributed across multiple systems. When these records do not align, organizations may experience provider participation gaps, billing delays, claim rejections, incorrect payer configuration, and missed reimbursement opportunities.

This project demonstrates a data-driven approach to identifying and analyzing these discrepancies using a modern analytics engineering workflow.

## Project Objectives

- Integrate provider, payer, enrollment, and reimbursement-related data into a structured analytical environment.
- Detect inconsistencies across provider participation, specialty, location, line of business, and enrollment records.
- Identify patterns that may indicate reimbursement or operational risk.
- Build reusable data-quality rules for validating payer and provider information.
- Translate technical findings into actionable healthcare business recommendations.

## Planned Architecture

Public / Synthetic Healthcare Data  
→ Python Data Ingestion & Cleaning  
→ Snowflake Data Warehouse  
→ dbt Transformation & Testing  
→ SQL Analytics  
→ Revenue Integrity Analysis  
→ Business Recommendations

## Technology Stack

- Python
- pandas
- SQL
- Snowflake
- dbt
- Git / GitLab

## Planned Analytical Areas

- Provider participation gaps
- Payer enrollment discrepancies
- Specialty and taxonomy inconsistencies
- Line-of-business configuration gaps
- Provider location discrepancies
- Enrollment-to-payment timing
- Claims and reimbursement risk patterns
- Data-quality and completeness monitoring

## Data Sources

This project will use publicly available and/or synthetic healthcare data. No protected health information (PHI), patient data, or proprietary employer data will be used.

## Repository Structure

The repository will contain:

- `data/` — source and synthetic datasets
- `src/` — Python ingestion and data-cleaning scripts
- `sql/` — analytical SQL queries
- `dbt/` — transformation models and data-quality tests
- `docs/` — architecture and project documentation
- `outputs/` — analytical results and visual outputs

## Project Status

🚧 **In Development**

Current phase: Project architecture and data-source design.

## Author

**Brittany Randall**  
Healthcare Data & Analytics | Decision Process Engineering | Payer & Revenue Operations