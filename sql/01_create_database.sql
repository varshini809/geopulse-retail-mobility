-- =====================================================
-- GeoPulse: Snowflake Database Setup
-- Purpose: Create database, schema, tables and stage
-- =====================================================

-- 1. Create the GeoPulse database
CREATE DATABASE IF NOT EXISTS GEOPULSE_DB;

-- 2. Create schema for raw data
CREATE SCHEMA IF NOT EXISTS GEOPULSE_DB.RAW_DATA;

-- 3. Create GPS_PINGS table
CREATE TABLE IF NOT EXISTS GEOPULSE_DB.RAW_DATA.GPS_PINGS (
    DEVICE_ID VARCHAR(50),
    LATITUDE FLOAT,
    LONGITUDE FLOAT,
    TIMESTAMP TIMESTAMP_NTZ,
    LOCATION GEOGRAPHY
);

-- 4. Create STORES table
CREATE TABLE IF NOT EXISTS GEOPULSE_DB.RAW_DATA.STORES (
    STORE_ID VARCHAR(50),
    STORE_NAME VARCHAR(100),
    LAT FLOAT,
    LON FLOAT,
    STATUS VARCHAR(20),
    LOCATION GEOGRAPHY
);

-- 5. Create internal Snowflake stage
CREATE STAGE IF NOT EXISTS GEOPULSE_DB.RAW_DATA.GEOPULSE_STAGE;