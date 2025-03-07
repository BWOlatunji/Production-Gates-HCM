import pandas as pd


def process_training_data(input_file, output_file):
    # Import the CSV file into a DataFrame
    df = pd.read_csv(input_file)
    # add new column names
    df.columns = [
        "id",
        "email",
        "profile_id",
        "institution_name",
        "course_of_study",
        "course_of_study_name",
        "certificate_type",
        "certificate_type_name",
        "certificate_name",
        "start_date",
        "end_date",
        "sponsor_type",
        "sponsor_type_name",
        "training_status",
        "training_type",
        "training_status_name",
        "training_type_name",
        "relevance",
    ]
    # Save the resulting DataFrame as a new CSV file
    df.to_csv(output_file, index=False)
    print(f"Processed CSV file saved at: {output_file}")


process_training_data(
    input_file="data/downloads/export-hrh-training-data.csv",
    output_file="data/CSVs/cleaned_hrh_training_data.csv",
)
