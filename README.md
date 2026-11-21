## geopulse-retail-mobility

## Week 1: Data checks and dictionary

- `data_checks.py` uses pandas to check mock GPS ping data for missing values,
  duplicates, invalid coordinates, and timestamp issues.
- `data_dictionary.md` describes the planned ping and store data columns.
- The planned ping columns are `device_id`, `latitude`, `longitude`, and
  `timestamp`.

### Run the checks

After `pings.csv` is added to this folder, run:

## Data status

- The project will use synthetic GPS pings; no real phone location data is used.
- The ping and store CSV files are pending.
- The city area for validating coordinates has not been selected yet.
- The checks and dictionary are based on the draft schema. Data validation results
  will be added after the CSV files are available.
