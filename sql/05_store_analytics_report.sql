-- =====================================================
-- GeoPulse: Store-Level Analytics Report
-- Date: 22 November 2026
-- =====================================================

-- Purpose:
-- Compare GPS activity around existing and proposed stores.
-- A nearby GPS observation does not confirm a store visit.

USE DATABASE GEOPULSE_DB;
USE SCHEMA RAW_DATA;

-- Store-level mobility analytics within a 500-meter radius

SELECT
    s.STORE_ID,
    s.STORE_NAME,
    s.STATUS,

    -- Total GPS observations near each store
    COUNT(g.DEVICE_ID) AS TOTAL_GPS_PINGS,

    -- Number of distinct nearby devices
    COUNT(DISTINCT g.DEVICE_ID) AS UNIQUE_DEVICES,

    -- Average GPS observations per nearby device
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
    s.STATUS

ORDER BY UNIQUE_DEVICES DESC;