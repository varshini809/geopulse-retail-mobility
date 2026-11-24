-- =====================================================
-- GeoPulse: Retail Cannibalization Risk Analysis
-- Date: 20 November 2026
-- =====================================================

-- Purpose:
-- Analyze proximity and overlapping GPS devices between
-- proposed and existing retail store locations.
--
-- Important:
-- These metrics indicate potential cannibalization risk.
-- They do not prove actual customer loss or lost revenue.

USE DATABASE GEOPULSE_DB;
USE SCHEMA RAW_DATA;


-- STEP 1: Calculate distances between proposed and existing stores

SELECT
    proposed.STORE_ID AS PROPOSED_STORE_ID,
    proposed.STORE_NAME AS PROPOSED_STORE_NAME,
    existing.STORE_ID AS EXISTING_STORE_ID,
    existing.STORE_NAME AS EXISTING_STORE_NAME,
    ROUND(
        ST_DISTANCE(proposed.LOCATION, existing.LOCATION),
        2
    ) AS DISTANCE_METERS
FROM STORES proposed
CROSS JOIN STORES existing
WHERE LOWER(proposed.STATUS) = 'proposed'
  AND LOWER(existing.STATUS) = 'existing'
ORDER BY DISTANCE_METERS ASC;


-- STEP 2: Classify potential risk based on 500-meter proximity

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
  AND LOWER(existing.STATUS) = 'existing'
ORDER BY DISTANCE_METERS ASC;


-- STEP 3: Calculate overlapping GPS devices

WITH DEVICE_PROXIMITY AS (
    SELECT DISTINCT
        g.DEVICE_ID,
        s.STORE_ID,
        s.STATUS
    FROM GPS_PINGS g
    JOIN STORES s
        ON ST_DWITHIN(g.LOCATION, s.LOCATION, 500)
    WHERE g.DEVICE_ID IS NOT NULL
),

OVERLAPPING_DEVICES AS (
    SELECT
        proposed.STORE_ID AS PROPOSED_STORE_ID,
        existing.STORE_ID AS EXISTING_STORE_ID,
        COUNT(DISTINCT proposed.DEVICE_ID) AS SHARED_DEVICES
    FROM DEVICE_PROXIMITY proposed
    JOIN DEVICE_PROXIMITY existing
        ON proposed.DEVICE_ID = existing.DEVICE_ID
    WHERE LOWER(proposed.STATUS) = 'proposed'
      AND LOWER(existing.STATUS) = 'existing'
    GROUP BY
        proposed.STORE_ID,
        existing.STORE_ID
)

SELECT
    p.STORE_ID AS PROPOSED_STORE_ID,
    p.STORE_NAME AS PROPOSED_STORE_NAME,
    e.STORE_ID AS EXISTING_STORE_ID,
    e.STORE_NAME AS EXISTING_STORE_NAME,
    COALESCE(o.SHARED_DEVICES, 0) AS SHARED_DEVICES
FROM STORES p
CROSS JOIN STORES e
LEFT JOIN OVERLAPPING_DEVICES o
    ON p.STORE_ID = o.PROPOSED_STORE_ID
   AND e.STORE_ID = o.EXISTING_STORE_ID
WHERE LOWER(p.STATUS) = 'proposed'
  AND LOWER(e.STATUS) = 'existing'
ORDER BY SHARED_DEVICES DESC;