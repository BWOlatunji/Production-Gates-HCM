import pandas as pd


def process_license_data(input_file_path, output_file_path):
    """
    This function imports a CSV file, removes specified columns, converts the birthdate column to MM/DD/YYYY format,
    adds a new column 'age' calculated from the birthdate, and saves the resulting DataFrame as a new CSV file.

    :param input_file_path: Path to the input CSV file.
    :param output_file_path: Path to save the processed data as a CSV file.
    """
    # Import the CSV file into a DataFrame
    df = pd.read_csv(
        input_file_path,
    )

    df["Licence Name"] = df["Licence Name"].astype(str)

    columns_to_drop = ["ID"]
    df = df.drop(columns=columns_to_drop)
    # ID,Email,"Licence Name","Issue Date","Expire Date",
    # "Issuing Agency Name","Licence Status Name"
    df.columns = [
        "email",
        "license_name",
        "issue_date",
        "expire_date",
        "issuing_agency_name",
        "license_status_name",
    ]
    # Save the resulting DataFrame as a new CSV file
    df.to_csv(output_file_path, index=False)
    print(
        f"Processed CSV file saved at: {output_file_path}"
    )


process_license_data(
    input_file_path="data/downloads/export-hrh-license-data.csv",
    output_file_path="data/CSVs/cleaned_hrh_license_data.csv",
)
