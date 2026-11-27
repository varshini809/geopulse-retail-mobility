# GeoPulse: Planned Power BI Measures (Draft)

Owner: Varshini (team lead, Power BI)
Status: DRAFT. Not tested yet, because the dataset is not loaded in Power BI.
Table and column names below are assumptions from our data plan.
They will be changed to match the real tables.

## Assumed tables
- pings: device_id, latitude, longitude, timestamp
- store_visits: store_name, device_id, timestamp (pings inside a store area)

## Calculated columns (pings table)
Hour of the day, used for the hourly chart:
```
Hour of Day = HOUR(pings[timestamp])
```
Part of the day, used for the donut chart:
```
Part of Day =
SWITCH(
    TRUE(),
    pings[Hour of Day] >= 5 && pings[Hour of Day] < 12, "Morning",
    pings[Hour of Day] >= 12 && pings[Hour of Day] < 17, "Afternoon",
    "Evening / Night"
)
```

## Planned measures (cards)
```
Total Pings = COUNTROWS(pings)

Total Unique Devices = DISTINCTCOUNT(pings[device_id])

Avg Pings per Device = DIVIDE([Total Pings], [Total Unique Devices])

Peak Hour =
MAXX(
    TOPN(1, VALUES(pings[Hour of Day]), [Total Pings]),
    pings[Hour of Day]
)
```

## Planned measures (store pages)
```
Unique Visitors per Store = DISTINCTCOUNT(store_visits[device_id])
```
This measure is used with the store name on the axis and the
store slicer, so each store shows its own visitors.

## Why these measures
- Total Pings and Total Unique Devices show the size of the data.
- Avg Pings per Device checks that the mock data looks realistic.
- Peak Hour shows the busiest time of the day.
- Unique Visitors per Store compares the stores.

## To check after the data is loaded
- Each measure gives a sensible number on a small sample.
- The hourly chart shows morning and evening peaks.
- Measure names are clear (no "Count of ...").
