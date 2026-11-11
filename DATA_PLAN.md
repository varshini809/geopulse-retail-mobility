# GeoPulse: Data Plan (Draft)

This file describes the data we plan to create and use in Week 1.
It is a plan only. Numbers below are targets, not results.

## Why we need mock data
Real phone location data is private and not available to us.
So we will create a mock (fake) dataset that looks like people
moving around a city during the day. No real person is in this data.

## Planned columns
| Column | Meaning | Example |
|---|---|---|
| device_id | Anonymous id of one phone | D0001 |
| latitude | Location north/south | 11.0168 |
| longitude | Location east/west | 76.9558 |
| timestamp | Date and time of the ping | 2026-11-12 08:15:00 |

## Planned extra tables
- stores: store_id, store_name, latitude, longitude
  (a small list of made-up store locations for the analysis)

## How the mock data should behave
- More pings in the morning (commute) and evening, fewer at night.
- Some devices pass near more than one store.
- Weekdays and weekends can look a little different.
- A fixed random seed is used, so the same data can be created again.

## Data checks we plan to run
- No empty values in any column.
- Latitude and longitude are inside the chosen city area.
- No duplicate rows (same device, same time).
- Timestamps are in correct order for each device.

## Output format
- Data saved as CSV, created by a Python script.
- Loaded into SQL tables for analysis.
- Power BI will read the final summary tables.

## Open questions for the team
- Which city area should the mock data use?
- How many devices and days are enough for a clear dashboard?
- Which SQL database will we use?
