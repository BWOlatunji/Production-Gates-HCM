import pandas as pd


def process_timecard_data(input_excel_path, output_csv_path):
    # Step 1: Load the Excel sheet, skipping the first row which is empty
    df = pd.read_excel(input_excel_path, header=1)

    # Step 2: Clean up column names by removing any leading/trailing spaces
    df.columns = df.columns.str.strip()

    # Check the columns to ensure "Time" exists
    # print("Columns in the dataset:", df.columns)

    if "Time" not in df.columns:
        raise KeyError("The required column 'Time' is missing in the dataset")

    # Step 3: Define a function to extract the first time value from the "Time" column
    def extract_first_time(time_str):
        if pd.isna(time_str):
            return None  # If time is missing, return None
        time_values = time_str.split(",")  # Split the time values by commas
        first_time = time_values[
            0
        ].strip()  # Take the first time and remove any extra spaces
        try:
            # Convert the first time to a valid time format (with hours, minutes, and seconds)
            first_time_parsed = pd.to_datetime(
                first_time, format="%H:%M:%S", errors="coerce"
            )
            if pd.isna(first_time_parsed):
                return None  # Return None if the time can't be parsed
            return first_time_parsed.strftime(
                "%H:%M:%S"
            )  # Return the time as a string in the format 'HH:MM:SS'
        except ValueError:
            return None  # Return None if there's any issue parsing the time

    # Step 4: Create a new column "Extracted Time" with the first extracted time value
    df["Extracted Time"] = df["Time"].apply(extract_first_time)

    # Drop the 'Time' and 'Times' columns
    df.drop(["First Name", "Last Name", "Times", "Time"], axis="columns", inplace=True)
    df.columns = [
        "employee_id",
        "department",
        "date",
        "gender",
        "department_code",
        "clockin_time",
    ]
    # Step 5: Save the cleaned data as CSV, keeping both the old and new columns
    df.to_csv(output_csv_path, index=False)
    print(
        f"Processed CSV file saved at: {output_csv_path}"
    )

# Usage:
process_timecard_data(
    input_excel_path="data/downloads/Time Card_20250117031909_export.xlsx",
    output_csv_path="data/CSVs/cleaned_hrh_timecard_data.csv",
)
