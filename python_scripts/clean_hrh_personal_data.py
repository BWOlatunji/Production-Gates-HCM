import pandas as pd
from datetime import datetime


def process_personal_data(input_file, hq_file, output_file):
    # Import the CSV file into a DataFrame
    df = pd.read_csv(input_file)
    hq_df = pd.read_csv(hq_file)

    # Columns to remove from the data frame
    columns_to_remove = [
        "ID",
        "First Name",
        "Other Name",
        "Disability Name",
        "Marital Status",
        "Change Name Status",
        "Change Name",
        "Address",
        "BVN",
        "NIN",
        "Phone Number",
    ]

    # Remove specified columns
    df = df.drop(columns=columns_to_remove)

    # Convert the birthdate column to datetime and handle errors with NaT (Not a Time)
    df["Birth Date"] = pd.to_datetime(df["Birth Date"], errors="coerce")

    # Replace missing birth dates with a default date, e.g., '1900-01-01'
    df["Birth Date"] = df["Birth Date"].fillna(pd.Timestamp("1900-01-01"))

    # Calculate the age
    current_date = datetime.now()  # Get the current date
    df["age"] = df["Birth Date"].apply(
        lambda birthdate: current_date.year
        - birthdate.year
        - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))
    )

    # Replace missing or NaN ages with 0
    df["age"] = df["age"].fillna(0)

    # Define age bins and corresponding labels for age groups
    # Define bins and labels
    bins = [0, 19, 29, 39, 49, 59, 120]
    labels = ["< 20", "20-29", "30-39", "40-49", "50-59", "60+"]

    # Create the age_group column
    df["age_group"] = pd.cut(
        df["age"], bins=bins, labels=labels, right=True, include_lowest=True
    ).astype(str)

    df["Disability Status"] = df["Disability Status"].fillna(2)

    df = pd.merge(
        df,
        hq_df.drop(columns=["ID"]),
        left_on="Qualification",
        right_on="NAME",
        how="inner",
    ).drop(columns=["NAME"])

    # Reassign column names
    df.columns = [
        "gender",
        "birth_date",
        "email",
        "qualification",
        "specialization",
        "disability_status",
        "year_attended",
        "state_name",
        "lga_name",
        "ward_name",
        "state_of_origin_name",
        "lga_of_origin_name",
        "age",
        "age_group",
        "qualification_short_name",
    ]

    # Save the resulting DataFrame as a new CSV file
    df.to_csv(output_file, index=False)

    print(f"Processed CSV file saved at: {output_file}")


# Example usage
process_personal_data(
    input_file="data/downloads/export-hrh-personal-data.csv",
    hq_file="data/downloads/export-higher-qualifications.csv",
    output_file="data/CSVs/cleaned_hrh_personal_data.csv",
)
