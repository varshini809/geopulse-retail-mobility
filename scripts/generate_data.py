import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Ensure output directory exists
os.makedirs("data", exist_ok=True)

# Set random seed so results are reproducible
np.random.seed(42)
random.seed(42)

# ---------------------------------------------------------
# 1. CREATE STORE LOCATIONS (Centered around Bengaluru, India)
# ---------------------------------------------------------
stores_data = [
    {
        "store_id": "STORE_A",
        "store_name": "Indiranagar Flagship (Existing)",
        "lat": 12.9784,
        "lon": 77.6408,
        "status": "existing",
    },
    {
        "store_id": "STORE_B",
        "store_name": "5th Street Proposed (Candidate)",
        "lat": 12.9802,  # Very close (~350m away) -> will cause cannibalization!
        "lon": 77.6435,
        "status": "proposed",
    },
    {
        "store_id": "STORE_C",
        "store_name": "Koramangala Hub (Existing)",
        "lat": 12.9352,
        "lon": 77.6245,
        "status": "existing",
    },
    {
        "store_id": "STORE_D",
        "store_name": "MG Road Central (Existing)",
        "lat": 12.9756,
        "lon": 77.6066,
        "status": "existing",
    },
    {
        "store_id": "STORE_E",
        "store_name": "Whitefield Tech Park (Candidate)",
        "lat": 12.9698,  # Far away -> zero cannibalization with Store A
        "lon": 77.7499,
        "status": "proposed",
    },
]

stores_df = pd.DataFrame(stores_data)
stores_df.to_csv("data/stores.csv", index=False)
print(f"[SUCCESS] Generated {len(stores_df)} stores -> data/stores.csv")


# ---------------------------------------------------------
# 2. GENERATE REALISTIC MOBILE GPS PINGS
# ---------------------------------------------------------
def generate_pings(num_devices=2000, pings_per_device=25):
  records = []
  base_date = datetime(2026, 11, 12, 0, 0, 0)

  # Weighted hours: heavy morning (8-10 AM) and evening (5-8 PM) commuter spikes
  hours = list(range(24))
  hour_weights = [
      0.005,
      0.005,
      0.005,
      0.005,
      0.01,
      0.02,
      0.04,
      0.07,
      0.11,
      0.10,
      0.06,
      0.05,
      0.06,
      0.05,
      0.04,
      0.05,
      0.07,
      0.09,
      0.08,
      0.05,
      0.02,
      0.01,
      0.005,
      0.005,
  ]

  for i in range(1, num_devices + 1):
    device_id = f"DEV_{i:05d}"

    # Assign each device a primary "home/office neighborhood" near one of the stores
    home_store = random.choice(stores_data)

    for _ in range(pings_per_device):
      # Pick hour based on commuter traffic distribution
      hour = random.choices(hours, weights=hour_weights, k=1)[0]
      minute = random.randint(0, 59)
      second = random.randint(0, 59)
      timestamp = base_date + timedelta(
          hours=hour, minutes=minute, seconds=second
      )

      # Scatter GPS coordinates around the store (~0.004 degrees is roughly ~400-450 meters)
      # 70% of pings cluster near the device's primary zone; 30% roam to another zone
      target_store = (
          home_store
          if random.random() < 0.70
          else random.choice(stores_data)
      )

      lat = target_store["lat"] + np.random.normal(0, 0.0035)
      lon = target_store["lon"] + np.random.normal(0, 0.0035)

      records.append({
          "device_id": device_id,
          "latitude": round(lat, 6),
          "longitude": round(lon, 6),
          "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
      })

  df = pd.DataFrame(records)
  # Sort chronologically like a real streaming/batch log
  df = df.sort_values("timestamp").reset_index(drop=True)
  return df


print("Generating 50,000 synthetic GPS pings...")
pings_df = generate_pings(num_devices=2000, pings_per_device=25)
pings_df.to_csv("data/gps_pings.csv", index=False)
print(
    f"[SUCCESS] Generated {len(pings_df)} GPS pings -> data/gps_pings.csv"
)
print("\nSample output:")
print(pings_df.head())