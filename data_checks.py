import pandas as pd

# Read the mock GPS pings CSV
pings = pd.read_csv("pings.csv")

required_columns = {"device_id", "latitude", "longitude", "timestamp"}

# Check that all planned columns are present
missing_columns = required_columns - set(pings.columns)
if missing_columns:
    print("Missing columns:", missing_columns)
else:
    print("All required columns are present")

# Check for blank or missing cells
print("\nMissing values by column:")
print(pings.isna().sum())

# Check duplicate rows and repeated device/timestamp pairs
print("\nExact duplicate rows:", pings.duplicated().sum())
print(
    "Repeated device/timestamp pairs:",
    pings.duplicated(subset=["device_id", "timestamp"]).sum()
)

# Check that timestamps can be read as dates and times
pings["timestamp"] = pd.to_datetime(pings["timestamp"], errors="coerce")
print("\nInvalid timestamps:", pings["timestamp"].isna().sum())

# Check latitude and longitude are numeric and within global coordinate limits
pings["latitude"] = pd.to_numeric(pings["latitude"], errors="coerce")
pings["longitude"] = pd.to_numeric(pings["longitude"], errors="coerce")

bad_coordinates = (
    pings["latitude"].isna()
    | ~pings["latitude"].between(-90, 90)
    | pings["longitude"].isna()
    | ~pings["longitude"].between(-180, 180)
)
print("Invalid coordinates:", bad_coordinates.sum())

# Check timestamps are in order within each device's rows
out_of_order = (
    pings.groupby("device_id")["timestamp"]
    .apply(lambda times: not times.is_monotonic_increasing)
)
print("Devices with timestamps out of order:", out_of_order.sum())