import pandas as pd
import requests
from io import StringIO
from datetime import datetime

def download_and_combine_csvs(start_year=2024, provided_columns=None):
    """
    Downloads CSV files for each month starting from January 2024 to the current month,
    removes the first 5 rows and last 2 rows from each CSV, adds 'year', 'month', and 'date' columns,
    drops empty columns, and combines them into a single DataFrame.

    Args:
    - start_year (int): The starting year (default is 2024).
    - provided_columns (list): A list of column names to assign to the final DataFrame.

    Returns:
    - combined_df (pd.DataFrame): The combined DataFrame with all CSV files.
    """
    # Set up the current month and year
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Base URL of the endpoint
    base_url = "https://gombestate.payriteonline.ng/api/export-hrh-payroll-report-data/{month}/{year}"

    # Placeholder list to hold the dataframes
    df_list = []

    # Iterate through each month for the year 2024 up to the current month and year
    for year in range(start_year, current_year + 1):
        for month in range(1, 13):
            # If the year is the current year, don't fetch data beyond the current month
            if year == current_year and month > current_month:
                break

            # Construct the URL for each month
            url = base_url.format(month=month, year=year)

            # Download the CSV content
            response = requests.get(url)

            if response.status_code == 200:
                # Convert the CSV content into a pandas dataframe
                data = StringIO(response.text)
                df = pd.read_csv(data)

                # Remove the first 5 rows and last 2 rows
                df = df.iloc[5:-2]

                # Add 'year' and 'month' columns
                df["year"] = year
                df["month"] = month

                # Add 'date' column with the first day of the month (YYYY-MM-01 format)
                df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))
                
                # Remove S/No, Bank and Account number columns
                df = df.drop(df.columns[[0, 4, 5]], axis=1)

                # Append the dataframe to the list
                df_list.append(df)
            else:
                print(f"Failed to download data for {month}/{year}, status code: {response.status_code}")

    # Combine all dataframes
    combined_df = pd.concat(df_list, ignore_index=True)

    # Drop columns that are completely empty (i.e., all values are NaN)
    combined_df.dropna(axis=1, how="all", inplace=True)

    # Check the number of columns in the final combined dataframe
    print(f"Number of columns in combined dataframe after dropping empty columns: {len(combined_df.columns)}")
    print(f"Column names in combined dataframe: {combined_df.columns.tolist()}")

    # Assign provided column names to the combined dataframe
    if provided_columns:
        expected_columns = provided_columns + ["year", "month", "date"]

        # Check for a mismatch in column count
        if len(expected_columns) == len(combined_df.columns):
            combined_df.columns = expected_columns
        else:
            print(f"Warning: Column count mismatch. Provided {len(expected_columns)} column names, but dataframe has {len(combined_df.columns)} columns.")

            # Automatically assign default column names (col1, col2, col3, ...)
            default_columns = [f"col{i + 1}" for i in range(len(combined_df.columns))]
            combined_df.columns = default_columns
            print(f"Assigned default column names: {default_columns}")

    # Columns that are supposed to be numeric but might have commas
    numeric_columns = ["basic", "allowances", "gross", "deductions", "loans", "tax", "suspensions", "net_pay"]

    # Remove commas from numeric columns, then convert to numeric
    for col in numeric_columns:
        if combined_df[col].dtype == "object":  # Check if column is a string
            combined_df[col] = combined_df[col].str.replace(",", "")
        combined_df[col] = pd.to_numeric(combined_df[col], errors="coerce")  # Convert to float, forcing errors to NaN

    return combined_df

# Example usage:
column_names = [
    "psn", "grade_level", "ministry", "basic", "allowances", "gross", 
    "deductions", "loans", "tax", "suspensions", "net_pay"
]  # Replace with actual column names

final_df = download_and_combine_csvs(start_year=2024, provided_columns=column_names)

# Display the final dataframe
print(final_df)

# Optionally, save the final dataframe to a CSV
final_df.to_csv("data/CSVs/cleaned_hrh_payroll_data.csv", index=False)
