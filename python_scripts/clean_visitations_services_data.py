import pandas as pd


def process_visitation_services_data(input_file_path, output_file_path):
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

    # Remove specified columns
    df = df.drop(
        columns=[
            "Created At",
        ]
    )
    df.columns = [
        "visitation_service_id",
        "visitation_id",
        "service_group_name",
        "service_name",
        "service_time",
        "health_care_worker_id_code",
    ]
    # Save the resulting DataFrame as a new CSV file
    df.to_csv(output_file_path, index=False)
    print(f"Processed CSV file saved at: {output_file_path}")


process_visitation_services_data(
    # Path to your input CSV file
    input_file_path="data/downloads/export-visitation-services.csv",
    # Path to save the output CSV file
    output_file_path="data/CSVs/cleaned_visitation_services_data.csv",
)
