import pandas as pd


class DataSchema:
    STATE_ID = "state_id"
    STATE_NAME = "state_name"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    LGA_ID = "lga_id"
    LGA_NAME = "lga_name"
    WARD_ID = "ward_id"
    WARD_NAME = "ward_name"
    FACILITY_ID = "facility_id"
    FACILITY_NAME = "facility_name"
    FACILITY_SHORTNAME = "facility_short_name"
    ADDRESS = "address"
    TOWN_ID = "town_id"


# Function to load data from CSV files and return them as data frames
def load_facility_location_data():
    states_data = pd.read_csv(
        "data/CSVs/cleaned_states_data.csv",
        dtype={
            DataSchema.STATE_ID: int,
            DataSchema.STATE_NAME: str,
            DataSchema.LATITUDE: float,
            DataSchema.LONGITUDE: float,
        },
    )
    lgas_data = pd.read_csv(
        "data/CSVs/cleaned_lgas_data.csv",
        dtype={
            DataSchema.LGA_ID: int,
            DataSchema.LGA_NAME: str,
            DataSchema.STATE_ID: int,
        },
    )
    wards_data = pd.read_csv(
        "data/CSVs/cleaned_wards_data.csv",
        dtype={
            DataSchema.WARD_ID: int,
            DataSchema.WARD_NAME: str,
            DataSchema.LGA_ID: int,
        },
    )
    facilities_data = pd.read_csv(
        "data/CSVs/cleaned_facilities_data.csv",
        # facility_id,facility_name,facility_short_name,address,ward_id,town_id
        dtype={
            DataSchema.FACILITY_ID: int,
            DataSchema.FACILITY_NAME: str,
            DataSchema.FACILITY_SHORTNAME: str,
            DataSchema.ADDRESS: str,
            DataSchema.WARD_ID: int,
            DataSchema.TOWN_ID: int,
        },
    )

    return states_data, lgas_data, wards_data, facilities_data
