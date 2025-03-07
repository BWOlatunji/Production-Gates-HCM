import pandas as pd
from datetime import datetime


def process_patients_data(input_file_path, output_file_path):
    """
    This function imports a CSV file, removes specified columns, converts the birthdate column to MM/DD/YYYY format,
    adds a new column 'age' calculated from the birthdate, and saves the resulting DataFrame as a new CSV file.

    :param input_file_path: Path to the input CSV file.
    :param output_file_path: Path to save the processed data as a CSV file.
    """
    # Import the CSV file into a DataFrame
    df = pd.read_csv(input_file_path)

    # Remove specified columns
    df = df.drop(
        columns=[
            "Patient Card Number",
            "Created At",
        ]
    )

    # Convert the birthdate column to datetime using the correct format (YYYY-MM-DD)
    df["Birth Date"] = pd.to_datetime(
        df["Birth Date"], format="%Y-%m-%d", errors="coerce"
    )

    # Create a new 'age' column based on the birth date
    current_date = datetime.now()  # Get the current date

    df["age"] = df["Birth Date"].apply(
        lambda birthdate: max(
            0,
            min(
                150,
                current_date.year
                - birthdate.year
                - (
                    (current_date.month, current_date.day)
                    < (birthdate.month, birthdate.day)
                ),
            ),
        )
        if pd.notnull(birthdate)
        else 0  # Replace None with 0
    )

    # Format the birth date as MM/DD/YYYY
    df["Birth Date"] = df["Birth Date"].dt.strftime("%m/%d/%Y")

    # Define age bins and corresponding labels for age groups
    bins = [
        0,
        4,
        9,
        19,
        29,
        39,
        49,
        59,
        150,
    ]  # Upper bound for 60+ is set to 150 as a safe maximum
    labels = ["0-4", "5-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60+"]

    # Add the age_group column to the DataFrame, forcing the labels to be strings
    df["age_group"] = pd.cut(
        df["age"], bins=bins, labels=labels, right=True, include_lowest=True
    ).astype(str)

    df.columns = [
        "patient_id",
        "patient_project_number",
        "gender",
        "marital_status",
        "birth_date",
        "state_name",
        "lga_name",
        "ward_name",
        "town_name",
        "facility_name",
        "is_caregiver",
        "age",
        "age_group",
    ]

    # Save the resulting DataFrame as a new CSV file and Parquet file
    df.to_csv(output_file_path, index=False)

    print(f"Processed CSV file saved at: {output_file_path}")


# Columns to remove from the data frame

process_patients_data(
    # Path to your input CSV file
    input_file_path="data/downloads/export-patients.csv",
    # Path to save the output CSV file
    output_file_path="data/CSVs/cleaned_patients_data.csv",
)
