import pandas as pd
from pathlib import Path

# Locate project directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Define dataset paths
GPS_FILE = DATA_DIR / "gps_pings.csv"
STORES_FILE = DATA_DIR / "stores.csv"


def validate_dataset(file_path, required_columns, dataset_name):

    print(f"\n========== {dataset_name} VALIDATION ==========")

    # Check whether file exists
    if not file_path.exists():
        print("ERROR: File not found!")
        return False

    # Load dataset
    df = pd.read_csv(file_path)

    print(f"Total Records: {len(df)}")

    # Check required columns
    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        print(f"Missing Columns: {missing_columns}")
        return False

    print("Schema: Valid")

    # Check missing values
    missing_values = df.isnull().sum().sum()
    print(f"Missing Values: {missing_values}")

    # Check duplicate records
    duplicates = df.duplicated().sum()
    print(f"Duplicate Records: {duplicates}")

    # Validate coordinates
    if "latitude" in df.columns:
        invalid_lat = (~df["latitude"].between(-90, 90)).sum()
    elif "lat" in df.columns:
        invalid_lat = (~df["lat"].between(-90, 90)).sum()
    else:
        invalid_lat = 0

    if "longitude" in df.columns:
        invalid_lon = (~df["longitude"].between(-180, 180)).sum()
    elif "lon" in df.columns:
        invalid_lon = (~df["lon"].between(-180, 180)).sum()
    else:
        invalid_lon = 0

    print(f"Invalid Latitude: {invalid_lat}")
    print(f"Invalid Longitude: {invalid_lon}")

    # Validate timestamps
    if "timestamp" in df.columns:
        invalid_timestamps = pd.to_datetime(
            df["timestamp"], errors="coerce"
        ).isnull().sum()

        print(f"Invalid Timestamps: {invalid_timestamps}")

    print("==============================================")

    return (
        missing_values == 0
        and duplicates == 0
        and invalid_lat == 0
        and invalid_lon == 0
        and ("timestamp" not in df.columns or invalid_timestamps == 0)
    )


def main():

    gps_columns = [
        "device_id",
        "latitude",
        "longitude",
        "timestamp"
    ]

    store_columns = [
        "store_id",
        "store_name",
        "lat",
        "lon",
        "status"
    ]

    gps_valid = validate_dataset(
        GPS_FILE, gps_columns, "GPS PINGS"
    )

    stores_valid = validate_dataset(
        STORES_FILE, store_columns, "STORES"
    )

    print("\n========== FINAL VALIDATION ==========")

    if gps_valid and stores_valid:
        print("STATUS: SUCCESS")
        print("Both datasets passed validation.")
    else:
        print("STATUS: FAILED")
        print("Please check the dataset errors.")

    print("======================================")


if __name__ == "__main__":
    main()