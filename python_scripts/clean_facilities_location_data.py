import pandas as pd


def clean_facilities_location_data(
    state_csv_path, lga_csv_path, ward_csv_path, facilities_csv_path, state_latlon_path
):
    # Read the CSV file
    states_df = pd.read_csv(state_csv_path)
    lgas_df = pd.read_csv(lga_csv_path)
    wards_df = pd.read_csv(ward_csv_path)
    facilities_df = pd.read_csv(facilities_csv_path)
    state_latlon_df = pd.read_csv(state_latlon_path)

    # Convert 'Name' column to uppercase
    state_latlon_df["Name"] = state_latlon_df["Name"].str.upper()

    # merge states_df with state_latlon_df
    states_df = pd.merge(
        states_df, state_latlon_df, left_on="NAME", right_on="Name", how="inner"
    )
    states_df = states_df.drop(columns=["Name"])

    # states
    states_df.columns = [
        "state_id",
        "state_name",
        "latitude",
        "longitude",
    ]

    lgas_df.columns = ["lga_id", "lga_name", "state_id"]
    wards_df.columns = ["ward_id", "ward_name", "lga_id"]
    facilities_df.columns = [
        "facility_id",
        "facility_name",
        "facility_short_name",
        "address",
        "ward_id",
        "town_id",
    ]

    # facilities_locations_data = (
    #     facilities_df.merge(wards_df, on="ward_id", how="left")
    #     .merge(lgas_df, on="lga_id", how="left")
    #     .merge(states_df, on="state_id", how="left")
    # )

    # Save the cleaned data as CSV
    states_df.to_csv("data/CSVs/cleaned_states_data.csv", index=False)
    lgas_df.to_csv("data/CSVs/cleaned_lgas_data.csv", index=False)
    wards_df.to_csv("data/CSVs/cleaned_wards_data.csv", index=False)
    facilities_df.to_csv("data/CSVs/cleaned_facilities_data.csv", index=False)
    # facilities_locations_data.to_csv(
    #     "data/CSVs/cleaned_facilities_location_data.csv", index=False
    # )

    print("Processed CSV file saved successfully.")


# Usage:
clean_facilities_location_data(
    state_csv_path="data/downloads/export-states.csv",
    lga_csv_path="data/downloads/export-lgas.csv",
    ward_csv_path="data/downloads/export-wards.csv",
    facilities_csv_path="data/downloads/export-facilities.csv",
    state_latlon_path="data/downloads/Nig States LatLong.csv",
)
