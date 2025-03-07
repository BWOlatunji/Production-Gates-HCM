import pandas as pd
from src.data import attendance_data


# Function to load and process data
def load_processed_data():
    attendance_df = attendance_data.load_attendance_data()
    # Extract hour from clockin_time
    attendance_df["clockin_hour"] = pd.to_datetime(
        attendance_df["clockin_time"], format="%H:%M:%S"
    ).dt.hour

    # Extract day of the week from the date
    attendance_df["weekday"] = attendance_df["date"].dt.day_name()
    # print(attendance_df.columns)
    return attendance_df
