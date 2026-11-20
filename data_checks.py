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

# Blank or null cells
blank_cells = frame.astype("string").apply(
    lambda column: column.str.strip().eq("")
)
missing_cells = frame.isna() | blank_cells

print("Blank or null cells:", int(missing_cells.sum().sum()))

# Completely duplicated rows
print("Exact duplicate rows:", int(frame.duplicated().sum()))

# Repeated device and timestamp pairs
keys = frame[["device_id", "timestamp"]].astype("string")
keys = keys.apply(lambda column: column.str.strip())
valid_keys = (
    keys["device_id"].notna()
    & keys["timestamp"].notna()
    & keys["device_id"].ne("")
    & keys["timestamp"].ne("")
)

duplicate_pairs = keys.loc[valid_keys].duplicated().sum()
print("Repeated device/timestamp pairs:", int(duplicate_pairs))

# Parse timestamps and count invalid or missing values
timestamps = pd.to_datetime(frame["timestamp"], errors="coerce")
invalid_timestamps = timestamps.isna()
print("Invalid timestamps:", int(invalid_timestamps.sum()))

# Check that timestamps are in order for each device
ordered_rows = frame.loc[
    ~invalid_timestamps & frame["device_id"].notna(),
    ["device_id"]
].copy()
ordered_rows["timestamp"] = timestamps.loc[ordered_rows.index]

out_of_order = ordered_rows.groupby("device_id")["timestamp"].apply(
    lambda times: not times.is_monotonic_increasing
)
print("Devices with timestamps out of order:", int(out_of_order.sum()))

# Check that coordinates are numeric and within global limits
latitude = pd.to_numeric(frame["latitude"], errors="coerce")
longitude = pd.to_numeric(frame["longitude"], errors="coerce")

invalid_coordinates = (
    latitude.isna()
    | ~latitude.between(-90, 90)
    | longitude.isna()
    | ~longitude.between(-180, 180)
)
print("Invalid coordinates:", int(invalid_coordinates.sum()))