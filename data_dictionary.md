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