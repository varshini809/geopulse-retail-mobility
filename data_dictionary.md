# GeoPulse Data Dictionary

## Pings data

Each row represents one simulated GPS location ping. The data is mock data,
not the real location of a person.

| Column | Type | Meaning | Example | Check |
|---|---|---|---|---|
| `device_id` | Text | Anonymous ID for a simulated device | `D0001` | Must not be blank |
| `latitude` | Decimal number | North-south location in decimal degrees | `11.0168` | Must be between -90 and 90 |
| `longitude` | Decimal number | East-west location in decimal degrees | `76.9558` | Must be between -180 and 180 |
| `timestamp` | Date and time | Time when the simulated ping occurred | `2026-11-12 08:15:00` | Must be a valid time; should be ordered per device |

## Stores data

| Column | Type | Meaning | Example | Check |
|---|---|---|---|---|
| `store_id` | Text | ID for a made-up store location | `S001` | Must be unique and not blank |
| `store_name` | Text | Made-up store name | `Store 1` | Must not be blank |
| `latitude` | Decimal number | Store latitude in decimal degrees | `11.0168` | Must be between -90 and 90 |
| `longitude` | Decimal number | Store longitude in decimal degrees | `76.9558` | Must be between -180 and 180 |

The city boundary has not been chosen yet, so the coordinate checks only use
global limits for now. Update this dictionary if the final CSV has different
columns.

## Planned data behavior

These are dataset-generation targets, not confirmed results:

- Generate more pings during morning and evening commute periods, and fewer at night.
- Include some devices that pass near more than one store.
- Allow weekday and weekend patterns to differ.
- Use a fixed random seed so the mock dataset can be reproduced.

## gps_pings.csv

One row represents one GPS ping recorded for a device.

| Column | Type | Meaning | Example | Notes |
|---|---|---|---|---|
| `device_id` | Text | Identifier for the device that recorded the ping | `DEV_01538` | 2,000 unique device IDs in this sample |
| `latitude` | Decimal number | North-south coordinate in decimal degrees | `12.931232` | Sample range: 12.921472 to 12.993604 |
| `longitude` | Decimal number | East-west coordinate in decimal degrees | `77.623877` | Sample range: 77.590970 to 77.762222 |
| `timestamp` | Date/time text | Time the ping was recorded | `2026-11-12 00:00:14` | Format is `YYYY-MM-DD HH:MM:SS`; timezone is unspecified |

**Sample size:** 50,000 rows, with 25 pings per device, all dated 2026-11-12.

## stores.csv

One row represents one store location.

| Column | Type | Meaning | Example | Notes |
|---|---|---|---|---|
| `store_id` | Text | Identifier for the store | `STORE_A` | Unique in this sample |
| `store_name` | Text | Display name for the store | `Indiranagar Flagship (Existing)` | Text label |
| `lat` | Decimal number | Store latitude in decimal degrees | `12.9784` | Store latitude field |
| `lon` | Decimal number | Store longitude in decimal degrees | `77.6408` | Store longitude field |
| `status` | Text/category | Whether the store is existing or proposed | `existing` | Sample values: `existing`, `proposed` |

## Data quality note

The GPS sample contains 13 repeated `(device_id, timestamp)` pairs. These should be reviewed with the data provider before any rows are changed.