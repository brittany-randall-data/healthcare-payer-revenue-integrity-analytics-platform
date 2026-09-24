-- Healthcare Payer Revenue Integrity Analytics Platform
-- Snowflake RAW Layer
-- Creates the database, RAW schema, and source tables used by the platform.

CREATE DATABASE IF NOT EXISTS HEALTHCARE_REVENUE_INTEGRITY;

CREATE SCHEMA IF NOT EXISTS HEALTHCARE_REVENUE_INTEGRITY.RAW;

USE DATABASE HEALTHCARE_REVENUE_INTEGRITY;
USE SCHEMA RAW;


CREATE TABLE IF NOT EXISTS PROVIDERS (
    provider_id VARCHAR(10),
    npi VARCHAR(20),
    provider_name VARCHAR(100),
    specialty VARCHAR(100),
    taxonomy_code VARCHAR(20),
    provider_type VARCHAR(50),
    active_status VARCHAR(20)
);


CREATE TABLE IF NOT EXISTS PROVIDER_LOCATIONS (
    provider_id VARCHAR(10),
    location_id VARCHAR(10),
    location_name VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(10),
    zip_code VARCHAR(10),
    location_status VARCHAR(20)
);


CREATE TABLE IF NOT EXISTS PAYER_ENROLLMENT (
    enrollment_id VARCHAR(10),
    provider_id VARCHAR(10),
    payer_name VARCHAR(100),
    line_of_business VARCHAR(50),
    enrollment_status VARCHAR(20),
    effective_date DATE,
    termination_date DATE,
    panel_status VARCHAR(20),
    payer_specialty VARCHAR(100),
    payer_location_id VARCHAR(10)
);


CREATE TABLE IF NOT EXISTS CLAIMS (
    claim_id VARCHAR(10),
    provider_id VARCHAR(10),
    payer_name VARCHAR(100),
    line_of_business VARCHAR(50),
    service_date DATE,
    billed_amount NUMBER(10,2),
    paid_amount NUMBER(10,2),
    claim_status VARCHAR(20),
    denial_reason VARCHAR(200)
);