import pandas as pd


class DataSchema:
    EMAIL = "email"
    PSN_NUMBER = "psn_number"
    CADRE = "cadre"
    RANK = "rank"
    DATE_OF_APPOINTMENT = "date_of_appointment"
    HAVE_PROMOTION = "have_promotion"
    STAFF_CATEGORY = "staff_category"
    FACILITY_STATIONED = "facility_stationed"
    STAFF_LOCATION = "staff_location"
    STAFF_ROLE_IN_FACILITY = "staff_role_in_facility"
    EMPLOYMENT_TYPE = "employment_type"
    HAVE_LICENSE = "have_license"
    HAVE_TRAINING = "have_training"
    YEAR_EMPLOYED = "years_employed"
    CADRE_SHORTNAME = "cadre_short_name"


def load_employment_data() -> pd.DataFrame:
    # load the data from the CSV file
    employment_data = pd.read_csv(
        "data/CSVs/cleaned_hrh_employment_data.csv",
        dtype={
            DataSchema.EMAIL:str,
            DataSchema.PSN_NUMBER: str,
            DataSchema.CADRE: str,
            DataSchema.RANK: str,
            DataSchema.HAVE_PROMOTION: int,
            DataSchema.STAFF_CATEGORY: str,
            DataSchema.FACILITY_STATIONED: str,
            DataSchema.STAFF_LOCATION: str,
            DataSchema.STAFF_ROLE_IN_FACILITY: str,
            DataSchema.EMPLOYMENT_TYPE: str,
            DataSchema.HAVE_LICENSE: float,
            DataSchema.HAVE_TRAINING: float,
            DataSchema.YEAR_EMPLOYED: float,
            DataSchema.CADRE_SHORTNAME: str,
        },
        parse_dates=[DataSchema.DATE_OF_APPOINTMENT],
    )

    
    return employment_data
# print(load_employment_data().dtypes)