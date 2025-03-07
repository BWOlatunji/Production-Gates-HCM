import pandas as pd
import numpy as np
from src.data import (
    patients_data,
    visitations_data,
)


# Handle inconsistent time formats
def parse_time(time_str):
    try:
        return pd.to_datetime(time_str, format="%H:%M").hour  # Standard case: HH:MM
    except ValueError:
        try:
            return pd.to_datetime(
                time_str, format="%H:%M:%S"
            ).hour  # If seconds are present
        except ValueError:
            return np.nan  # If neither works, return NaN


# Function to load and process data
def load_processed_data():
    # Load data
    patients_df = patients_data.load_patient_data()
    visitation_df = visitations_data.load_visitation_data()

    # Merge without repeating similar columns
    patients_visitation_df = pd.merge(
        patients_df.drop(
            columns=["state_name", "lga_name", "ward_name", "facility_name"]
        ),
        visitation_df.drop(columns=["patient_project_number"]),
        on="patient_id",
        how="inner",
    )
    # Convert date column
    patients_visitation_df["start_date"] = pd.to_datetime(
        patients_visitation_df["start_date"]
    )

    # Extract date parts
    patients_visitation_df["week_number"] = (
        patients_visitation_df["start_date"].dt.isocalendar().week
    )

    # Ensure all values are strings and strip any whitespace
    patients_visitation_df["time_in"] = (
        patients_visitation_df["time_in"].astype(str).str.strip()
    )

    # Apply function to extract hours
    patients_visitation_df["hour"] = patients_visitation_df["time_in"].apply(parse_time)

    # Drop NaN rows if necessary
    patients_visitation_df.dropna(subset=["hour"], inplace=True)

    patients_visitation_df["day_of_week"] = pd.to_datetime(
        patients_visitation_df["start_date"]
    ).dt.day_name()

    return patients_visitation_df
