import pandas as pd


class AttendanceSchema:
    EMPLOYEE_ID = "employee_id"
    DEPARTMENT = "department"
    DATE = "date"
    GENDER = "gender"
    DEPARTMENT_CODE = "department_code"
    CLOCKIN_TIME = "clockin_time"


def load_attendance_data() -> pd.DataFrame:
    # load the data from the CSV file
    attendance_data = pd.read_csv(
        "data/CSVs/cleaned_hrh_timecard_data.csv",
        dtype={
            AttendanceSchema.EMPLOYEE_ID: str,
            AttendanceSchema.DEPARTMENT: str,
            AttendanceSchema.GENDER: str,
            AttendanceSchema.DEPARTMENT_CODE: str,
        },
        parse_dates=[AttendanceSchema.DATE],
    )

    attendance_data[AttendanceSchema.CLOCKIN_TIME] = pd.to_datetime(
        attendance_data[AttendanceSchema.CLOCKIN_TIME], format="%H:%M:%S"
    ).dt.time
    # attendance_data[AttendanceSchema.CLOCKIN_TIME] = pd.to_datetime(
    #     attendance_data[AttendanceSchema.CLOCKIN_TIME], format="mixed"
    # ).dt.time

    return attendance_data
