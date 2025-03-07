import pandas as pd


def process_visitation_services_data(input_file_path, output_file_path):
    """
    This function imports a CSV file, removes specified columns, converts the birthdate column to MM/DD/YYYY format,
    adds a new column 'age' calculated from the birthdate, and saves the resulting DataFrame as a new CSV file.

    :param input_file_path: Path to the input CSV file.
    :param output_file_path: Path to save the processed data as a CSV file.
    :param parquet_output_file_path: Path to save the processed data as a Parquet file.
    :param columns_to_remove: List of columns to be removed.
    """
    # Import the CSV file into a DataFrame
    df = pd.read_csv(
        input_file_path,
    )

    # Remove specified columns
    df = df.drop(
        columns=[
            "JSON Value",
            "Created At",
        ]
    )
    df.columns = [
        "visitation_service_detail_id",
        "visitation_service_id",
        "description",
    ]
    # Save the resulting DataFrame as a new CSV file
    df.to_csv(output_file_path, index=False)
    print(f"Processed CSV files saved at: {output_file_path}")


process_visitation_services_data(
    # Path to your input CSV file
    input_file_path="data/downloads/export-visitation-service-details.csv",
    # Path to save the output CSV file
    output_file_path="data/CSVs/cleaned_visitation_services_details_data.csv",
)
