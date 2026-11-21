# GeoPulse: Power BI Dashboard Plan (Draft)

Owner: Varshini (team lead, Power BI)
Status: plan only. The dashboard is not built yet, because the
mock data is still being created in Week 1.

## Goal of the dashboard
Help a store planner see when and where people walk near stores,
and check if a new store could take visitors from an old store.

## Planned data inputs
- pings table: device_id, latitude, longitude, timestamp
- stores table: store_id, store_name, latitude, longitude
- Summary tables made with SQL and Python (visitors per store per hour)

## Planned cards (KPIs)
- Total unique devices
- Total pings
- Average pings per device
- Peak hour of the day
- Share of devices that visit more than one store

## Planned charts
- Column chart: visitors by hour of the day
- Bar chart: visitors per store
- Donut chart: morning, afternoon and evening share
- Table: store name, unique visitors, peak hour
- Map visual: ping locations around the stores

## Planned filters and navigation
- Slicers: store and date
- Left navigation bar with icons linked to bookmarks
- Pages: Overview, Store Traffic, Overlap Between Stores

## Design rules
- One colour theme with light and dark shades.
- Clear names for every measure (no "Count of ...").
- Use the real date field for the time axis.

## Open questions
- Which map visual will we use in Power BI?
- Will the data be loaded from CSV files or from the SQL database?
- Which stores will we compare for the overlap page?
