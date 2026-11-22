-- =====================================================
-- GeoPulse: Reusable Analytics Views
-- Date: 23 November 2026
-- =====================================================

-- Purpose:
-- Create reusable Snowflake views for store-level
-- mobility analytics and potential cannibalization risk.
--
-- Prerequisites:
-- GPS_PINGS and STORES tables must contain processed
-- geographic locations.

USE DATABASE GEOPULSE_DB;
USE SCHEMA RAW_DATA;


-- =====================================================
-- VIEW 1: STORE FOOT TRAFFIC ANALYSIS
-- =====================================================

CREATE OR REPLACE VIEW STORE_FOOT_TRAFFIC_VIEW AS

SELECT
    s.STORE_ID,
    s.STORE_NAME,
    s.STATUS,

    COUNT(g.DEVICE_ID) AS TOTAL_GPS_PINGS,

    COUNT(DISTINCT g.DEVICE_ID) AS UNIQUE_DEVICES,

    ROUND(
        COUNT(g.DEVICE_ID) * 1.0 /
        NULLIF(COUNT(DISTINCT g.DEVICE_ID), 0),
        2
    ) AS AVG_PINGS_PER_DEVICE

FROM STORES s

LEFT JOIN GPS_PINGS g
    ON ST_DWITHIN(s.LOCATION, g.LOCATION, 500)

GROUP BY
    s.STORE_ID,
    s.STORE_NAME,
    s.STATUS;


-- =====================================================
-- VIEW 2: CANNIBALIZATION RISK ANALYSIS
-- =====================================================

CREATE OR REPLACE VIEW CANNIBALIZATION_RISK_VIEW AS

SELECT
    proposed.STORE_ID AS PROPOSED_STORE_ID,
    proposed.STORE_NAME AS PROPOSED_STORE_NAME,

    existing.STORE_ID AS EXISTING_STORE_ID,
    existing.STORE_NAME AS EXISTING_STORE_NAME,

    ROUND(
        ST_DISTANCE(proposed.LOCATION, existing.LOCATION),
        2
    ) AS DISTANCE_METERS,

    CASE
        WHEN ST_DWITHIN(
            proposed.LOCATION,
            existing.LOCATION,
            500
        )
        THEN 'POTENTIAL RISK'
        ELSE 'LOW PROXIMITY RISK'
    END AS CANNIBALIZATION_RISK

FROM STORES proposed

CROSS JOIN STORES existing

WHERE LOWER(proposed.STATUS) = 'proposed'
  AND LOWER(existing.STATUS) = 'existing';


-- =====================================================
-- VALIDATION QUERIES
-- =====================================================

-- Expected: 5 stores
SELECT *
FROM STORE_FOOT_TRAFFIC_VIEW
ORDER BY UNIQUE_DEVICES DESC;

-- Expected: 6 proposed-to-existing store comparisons
SELECT *
FROM CANNIBALIZATION_RISK_VIEW
ORDER BY DISTANCE_METERS ASC;