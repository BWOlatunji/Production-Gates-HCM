# data processing
import pandas as pd
from src.data import (
    # employment_data,
    hr_personal_data,
    patients_data,
    visitations_data,
    facilities_location_data,
)


# Function to load and process data
def load_and_process_data():
    # Load data
    patients_df = patients_data.load_patient_data()
    visitation_df = visitations_data.load_visitation_data()
    hr_personal_df = hr_personal_data.load_personal_data()
    # employment_df = employment_data.load_employment_data()
    states_df, lgas_df, wards_df, facilities_df = (
        facilities_location_data.load_facility_location_data()
    )

    # Merged DataFrame
    patients_visitation_df = pd.merge(
        visitation_df, patients_df, left_on="patient_id", right_on="patient_id"
    )

    # patients data
    patients_age_group = patients_df["age_group"].value_counts()

    patients_marital_status_count = patients_df["marital_status"].value_counts()

    visitations_age_group = patients_visitation_df["age_group"].value_counts()
    visitations_marital_status_count = patients_visitation_df[
        "marital_status"
    ].value_counts()

    # Calculate percentages
    total_patients = len(patients_df)
    formatted_total_patients = "{:,}".format(total_patients)

    total_lgas = 1  # len(lgas_df)
    total_wards = len(wards_df)
    total_facilities = 24  # len(facilities_df)

    # Registration - Gender
    male_patients = patients_df.query('gender in ["male", "Male"]').shape[0]
    female_patients = patients_df.query('gender in ["female", "Female"]').shape[0]

    male_percentage = (
        (male_patients / total_patients) * 100 if total_patients > 0 else 0
    )
    formatted_male_percentage = "{:.2f}".format(male_percentage)

    female_percentage = (
        (female_patients / total_patients) * 100 if total_patients > 0 else 0
    )
    formatted_female_percentage = "{:.2f}".format(female_percentage)

    # Visitation - Gender
    v_male_patients = patients_visitation_df.query('gender in ["male", "Male"]').shape[
        0
    ]
    v_female_patients = patients_visitation_df.query(
        'gender in ["female", "Female"]'
    ).shape[0]

    # marital status
    married_patients = patients_df.query(
        'marital_status in ["married", "Married"]'
    ).shape[0]
    single_patients = patients_df.query(
        'marital_status in  ["single", "Single"]'
    ).shape[0]

    formatted_single_patients = "{:,}".format(single_patients)
    formatted_married_patients = "{:,}".format(married_patients)

    total_employees = len(hr_personal_df)
    formatted_total_employees = "{:,}".format(total_employees)

    # Personal - Disability
    disability_status_employees = hr_personal_df.query(
        "disability_status in [1, 1]"
    ).shape[0]

    disability_status_percentage = (
        (disability_status_employees / total_employees) * 100
        if total_employees > 0
        else 0
    )
    formatted_disability_status_percentage = "{:.2f}".format(
        disability_status_percentage
    )

    # Create a dictionary of age group counts with missing groups set to zero
    # age_group_counts = filtered_df["age_group"].value_counts().to_dict()
    # age_group_counts = {age: age_group_counts.get(age, 0) for age in desired_order}

    return {
        "male_patients": male_patients,
        "female_patients": female_patients,
        "patients_age_group": patients_age_group,
        "visitations_age_group": visitations_age_group,
        "patients_marital_status_count": patients_marital_status_count,
        "visitations_marital_status_count": visitations_marital_status_count,
        "v_male_patients": v_male_patients,
        "v_female_patients": v_female_patients,
        "formatted_total_patients": formatted_total_patients,
        "total_lgas": total_lgas,
        "total_wards": total_wards,
        "total_facilities": total_facilities,
        "formatted_male_percentage": formatted_male_percentage,
        "formatted_female_percentage": formatted_female_percentage,
        "formatted_single_patients": formatted_single_patients,
        "formatted_married_patients": formatted_married_patients,
        "formatted_total_employees": formatted_total_employees,
        "formatted_disability_status_percentage": formatted_disability_status_percentage,
    }
