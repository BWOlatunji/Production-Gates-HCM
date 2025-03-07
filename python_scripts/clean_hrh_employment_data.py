import pandas as pd
from datetime import datetime


def process_employment_data(input_csv_path, cadre_csv_path, output_csv_path):
    # Read the CSV file
    df = pd.read_csv(input_csv_path)
    cadre_df = pd.read_csv(cadre_csv_path)
    # 1. Convert "Date of Appointment" to a date format
    df["Date of Appointment"] = pd.to_datetime(
        df["Date of Appointment"], errors="coerce"
    )

    # 2. Replace missing values in "Have Promotion" column with 0
    df["Have Promotion"] = df["Have Promotion"].fillna(0)

    # 3. Remove "ID", "Have Employment", "LGA", and "Pending License Status" columns
    columns_to_drop = ["ID", "Have Employment", "LGA", "Pending License Status"]
    df = df.drop(columns=columns_to_drop)

    # 4. Replace missing values in "Have Training" column with 0
    df["Have Training"] = df["Have Training"].fillna(0)

    # 5. Add a column for the number of years the employee has been employed to date
    current_date = pd.to_datetime(datetime.now().date())
    df["Years Employed"] = (current_date - df["Date of Appointment"]).dt.days // 365

    df = pd.merge(
        df, cadre_df.drop(columns=["ID"]), left_on="Cadre", right_on="NAME", how="inner"
    ).drop(columns=["NAME"])

    # modify column names
    # Email,"PSN Number",Cadre,Rank,"Date of Appointment","Have Promotion","Staff Category","Facility Stationed",
    # "Staff Location","Staff Role in Facility","Employment Type","Have License","Have Training",

    df.columns = [
        "email",
        "psn_number",
        "cadre",
        "rank",
        "date_of_appointment",
        "have_promotion",
        "staff_category",
        "facility_stationed",
        "staff_location",
        "staff_role_in_facility",
        "employment_type",
        "have_license",
        "have_training",
        "years_employed",
        "cadre_short_name",
    ]
    # 6. Save the cleaned data as CSV
    df.to_csv(output_csv_path, index=False)
    print("Processed CSV file saved successfully.")


# Usage:
process_employment_data(
    input_csv_path="data/downloads/export-hrh-employment-data.csv",
    cadre_csv_path="data/downloads/export-cadres.csv",
    output_csv_path="data/CSVs/cleaned_hrh_employment_data.csv",
)
