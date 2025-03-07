import pandas as pd


class VisitationSchema:
    VISITATION_ID = "visitation_id"
    PATIENT_ID = "patient_id"
    PATIENT_PROJECT_NUMBER = "patient_project_number"
    FACILITY_NAME = "facility_name"
    START_DATE = "start_date"
    END_DATE = "end_date"
    TIME_IN = "time_in"
    TIME_OUT = "time_out"


def load_visitation_data() -> pd.DataFrame:
    # load the data from the CSV file
    visitation_data = pd.read_csv(
        "data/CSVs/cleaned_visitations_data.csv",
        dtype={
            VisitationSchema.VISITATION_ID: int,
            VisitationSchema.PATIENT_ID: str,
            VisitationSchema.PATIENT_PROJECT_NUMBER: str,
            VisitationSchema.FACILITY_NAME: str,
        },
        parse_dates=[VisitationSchema.START_DATE, VisitationSchema.END_DATE],
    )

    # Convert TIME_IN and TIME_OUT columns to time format
    visitation_data[VisitationSchema.TIME_IN] = pd.to_datetime(
        visitation_data[VisitationSchema.TIME_IN], format="mixed"
    ).dt.time

    # visitation_data[VisitationSchema.TIME_OUT] = pd.to_datetime(
    #     visitation_data[VisitationSchema.TIME_OUT], format="%H:%M:%S"
    # ).dt.time
    visitation_data[VisitationSchema.TIME_OUT] = pd.to_datetime(
        visitation_data[VisitationSchema.TIME_OUT], format="mixed"
    ).dt.time

    return visitation_data
