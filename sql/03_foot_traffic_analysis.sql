-- =====================================================
-- GeoPulse: Retail Foot Traffic Analysis
-- Date: 19 November 2026
-- =====================================================

-- Purpose:
-- Analyze GPS activity within 500 meters of retail stores.
-- GPS proximity does not confirm actual store visits.

USE DATABASE GEOPULSE_DB;
USE SCHEMA RAW_DATA;

-- STEP 1: Calculate distances between GPS pings and stores

SELECT
    g.DEVICE_ID,
    s.STORE_ID,
    s.STORE_NAME,
    ROUND(
        ST_DISTANCE(g.LOCATION, s.LOCATION),
        2
    ) AS DISTANCE_METERS
FROM GPS_PINGS g
CROSS JOIN STORES s
WHERE g.LOCATION IS NOT NULL
  AND s.LOCATION IS NOT NULL
LIMIT 10;


-- STEP 2: Count GPS pings within 500 meters of each store

SELECT
    s.STORE_ID,
    s.STORE_NAME,
    s.STATUS,
    COUNT(g.DEVICE_ID) AS TOTAL_GPS_PINGS
FROM STORES s
LEFT JOIN GPS_PINGS g
    ON ST_DWITHIN(s.LOCATION, g.LOCATION, 500)
GROUP BY
    s.STORE_ID,
    s.STORE_NAME,
    s.STATUS
ORDER BY TOTAL_GPS_PINGS DESC;


-- STEP 3: Count unique devices near each store

SELECT
    s.STORE_ID,
    s.STORE_NAME,
    s.STATUS,
    COUNT(g.DEVICE_ID) AS TOTAL_GPS_PINGS,
    COUNT(DISTINCT g.DEVICE_ID) AS UNIQUE_DEVICES
FROM STORES s
LEFT JOIN GPS_PINGS g
    ON ST_DWITHIN(s.LOCATION, g.LOCATION, 500)
GROUP BY
    s.STORE_ID,
    s.STORE_NAME,
    s.STATUS
ORDER BY UNIQUE_DEVICES DESC;