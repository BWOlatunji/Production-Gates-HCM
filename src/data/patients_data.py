import pandas as pd


class PatientSchema:
    PATIENT_ID = "patient_id"
    PATIENT_PROJECT_NUMBER = "patient_project_number"
    GENDER = "gender"
    MARITAL_STATUS = "marital_status"
    BIRTHDATE = "birth_date"
    STATE_NAME = "state_name"
    LGA_NAME = "lga_name"
    WARD_NAME = "ward_name"
    TOWN_NAME = "town_name"
    FACILITY_NAME = "facility_name"
    IS_CAREGIVER = "is_caregiver"
    AGE = "age"
    AGE_GROUP = "age_group"


def load_patient_data() -> pd.DataFrame:
    # load the data from the CSV file
    patient_data = pd.read_csv(
        "data/CSVs/cleaned_patients_data.csv",
        dtype={
            PatientSchema.PATIENT_ID: str,
            PatientSchema.PATIENT_PROJECT_NUMBER: str,
            PatientSchema.GENDER: str,
            PatientSchema.MARITAL_STATUS: str,
            PatientSchema.STATE_NAME: str,
            PatientSchema.LGA_NAME: str,
            PatientSchema.WARD_NAME: str,
            PatientSchema.TOWN_NAME: str,
            PatientSchema.FACILITY_NAME: str,
            PatientSchema.IS_CAREGIVER: str,
            PatientSchema.AGE: int,
            PatientSchema.AGE_GROUP: str,
        },
        parse_dates=[PatientSchema.BIRTHDATE],
    )

    return patient_data
