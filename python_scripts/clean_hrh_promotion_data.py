import pandas as pd


def process_promotion_data(input_file_path, output_file_path):
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

    # ID,Email,"Date of Promotion","Previous Cadre Name",
    # "Previous Rank Name","Current Cadre Name","Current Rank Name"
    df.columns = [
        "id",
        "email",
        "date_of_promotion",
        "previous_cadre_name",
        "previous_rank_name",
        "current_cadre_name",
        "current_rank_name",
    ]
    # Save the resulting DataFrame as a new CSV file
    df.to_csv(output_file_path, index=False)
    print(
        f"Processed CSV file saved at: {output_file_path}"
    )


process_promotion_data(
    input_file_path="data/downloads/export-hrh-promotion-data.csv",
    output_file_path="data/CSVs/cleaned_hrh_promotion_data.csv",
)
