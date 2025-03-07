import pandas as pd


class DataSchema:
    GENDER = "gender"
    BIRTHDATE = "birth_date"
    EMAIL = "email"
    QUALIFICATION = "qualification"
    SPECIALIZATION = "specialization"
    DISABILITY_STATUS = "disability_status"
    YEAR_ATTENDED = "year_attended"
    STATE = "state_name"
    LGA = "lga_name"
    WARD = "ward_name"
    STATE_OF_ORIGIN = "state_of_origin_name"
    LGA_OF_ORIGIN = "lga_of_origin_name"
    AGE = "age"
    AGE_GROUP = "age_group"
    QUALIFICATION_SHORTNAME = "qualification_short_name"


def load_personal_data() -> pd.DataFrame:
    # load the data from the CSV file

    hr_personal_data = pd.read_csv(
        "data/CSVs/cleaned_hrh_personal_data.csv",
        dtype={
            DataSchema.GENDER: str,
            DataSchema.EMAIL: str,
            DataSchema.QUALIFICATION: str,
            DataSchema.SPECIALIZATION: str,
            DataSchema.DISABILITY_STATUS: float,
            DataSchema.YEAR_ATTENDED: str,
            DataSchema.STATE: str,
            DataSchema.LGA: str,
            DataSchema.WARD: str,
            DataSchema.STATE_OF_ORIGIN: str,
            DataSchema.LGA_OF_ORIGIN: str,
            DataSchema.AGE: int,
            DataSchema.AGE_GROUP: str,
            DataSchema.QUALIFICATION_SHORTNAME: str,
        },
        # parse_dates=[DataSchema.BIRTHDATE],
    )
    hr_personal_data[DataSchema.BIRTHDATE] = pd.to_datetime(
        hr_personal_data[DataSchema.BIRTHDATE], errors="coerce"
    )

    return hr_personal_data

