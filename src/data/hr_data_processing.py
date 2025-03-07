# data_processing.py
import pandas as pd
from src.data import (
    hr_personal_data,
    employment_data,
)


# Function to load and process data
def load_hr_processed_data(facility=None):
    # Load data
    hr_personal_df = hr_personal_data.load_personal_data()
    employment_df = employment_data.load_employment_data()

    merged_df = pd.merge(hr_personal_df, employment_df, on="email", how="inner")

    # Apply filters only if facility is not None
    if facility:
        merged_df = merged_df[merged_df["facility_stationed"].isin(facility)]

    # Calculate percentages
    total_employees = len(hr_personal_df)
    formatted_total_employees = "{:,}".format(total_employees)

    # Registration - Gender
    male_employees = hr_personal_df.query('gender in ["male", "Male"]').shape[0]
    female_employees = hr_personal_df.query('gender in ["female", "Female"]').shape[0]

    male_percentage = (
        (male_employees / total_employees) * 100 if total_employees > 0 else 0
    )
    formatted_male_percentage = "{:.2f}".format(male_percentage)
    female_percentage = (
        (female_employees / total_employees) * 100 if total_employees > 0 else 0
    )
    formatted_female_percentage = "{:.2f}".format(female_percentage)

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

    merged_df = pd.merge(hr_personal_df, employment_df, on="email", how="inner")

    def prepare_employee_counts_by_qualification(df, facility=None):
        # Apply filters based on the dropdown selections
        filtered_df = df.copy()
        if facility:
            # filtered_df = filtered_df[filtered_df["facility_stationed"] == facility]
            # Since facility is a list (multi-select), use .isin() to filter
            filtered_df = filtered_df[filtered_df["facility_stationed"].isin(facility)]

        # Group by qualification and count
        qualification_counts = (
            filtered_df.groupby("qualification_short_name")
            .size()
            .reset_index(name="counts")
        )

        return qualification_counts

    hr_qualification_counts = prepare_employee_counts_by_qualification(
        merged_df, facility
    )

    def prepare_employee_distribution_by_age_group(df, facility=None):
        # Apply filters
        filtered_df = df.copy()
        if facility:
            # filtered_df = filtered_df[filtered_df["facility_stationed"] == facility]
            # Since facility is a list (multi-select), use .isin() to filter
            filtered_df = filtered_df[filtered_df["facility_stationed"].isin(facility)]

        # Define age group order
        # ["below 20", "20-29", "30-39", "40-49", "50-59", "60+"]
        age_group_order = ["< 20", "20-29", "30-39", "40-49", "50-59", "60+"]

        # Group by age group and count
        age_group_counts = (
            filtered_df.groupby("age_group").size().reset_index(name="counts")
        )

        # Ensure proper ordering of age groups
        age_group_counts["age_group"] = pd.Categorical(
            age_group_counts["age_group"], categories=age_group_order, ordered=True
        )
        age_group_counts = age_group_counts.sort_values("age_group")

        return age_group_counts

    hr_age_group_counts = prepare_employee_distribution_by_age_group(
        merged_df, facility
    )

    def prepare_percentage_distribution_by_cadre(df, facility=None):
        # Apply filters
        filtered_df = df.copy()
        if facility:
            # filtered_df = filtered_df[filtered_df["facility_stationed"] == facility]
            # Since facility is a list (multi-select), use .isin() to filter
            filtered_df = filtered_df[filtered_df["facility_stationed"].isin(facility)]

        # Group by cadre and count
        cadre_counts = (
            filtered_df.groupby("cadre_short_name").size().reset_index(name="counts")
        )

        # Calculate percentage
        cadre_counts["percentage"] = (
            cadre_counts["counts"] / cadre_counts["counts"].sum()
        ) * 100

        return cadre_counts

    hr_cadre_counts = prepare_percentage_distribution_by_cadre(merged_df, facility)

    def prepare_employee_percentage_by_employment_type(df, facility=None):
        # Apply filters
        filtered_df = df.copy()
        if facility:
            # Since facility is a list (multi-select), use .isin() to filter
            filtered_df = filtered_df[filtered_df["facility_stationed"].isin(facility)]

        # Group by employment type and count
        employment_type_counts = (
            filtered_df.groupby("employment_type").size().reset_index(name="counts")
        )

        # Calculate percentage
        employment_type_counts["percentage"] = (
            employment_type_counts["counts"] / employment_type_counts["counts"].sum()
        ) * 100

        # Sort alphabetically by employment type
        employment_type_counts = employment_type_counts.sort_values(
            by="employment_type", ascending=False
        )

        return employment_type_counts

    hr_employment_type_counts = prepare_employee_percentage_by_employment_type(
        merged_df, facility
    )

    def prepare_emp_count_stackedbar(df, facility=None):
        # Apply filters
        filtered_df = df.copy()
        if facility:
            # filtered_df = filtered_df[filtered_df["facility_stationed"] == facility]
            # Since facility is a list (multi-select), use .isin() to filter
            filtered_df = filtered_df[filtered_df["facility_stationed"].isin(facility)]
        # Calculate the percentage of health workers by employment type
        employment_counts = (
            filtered_df.groupby("employment_type")["email"].count().reset_index()
        )
        employment_counts.columns = ["employment_type", "total_workers"]

        # Calculate percentage
        employment_counts["percent_health_workers"] = (
            employment_counts["total_workers"]
            / employment_counts["total_workers"].sum()
        ) * 100
        return employment_counts

    hr_emp_count_stackedbar = prepare_emp_count_stackedbar(merged_df, facility)

    def prepare_cadre_treemap_data(df, facility=None):
        # Apply filters
        filtered_df = df.copy()
        if facility:
            # Since facility is a list (multi-select), use .isin() to filter
            filtered_df = filtered_df[filtered_df["facility_stationed"].isin(facility)]

        # Clean and check for missing values in 'cadre'
        filtered_df["cadre"] = filtered_df["cadre"].fillna("Unknown")

        # Create a mock total number of health workers for demonstration purposes
        filtered_df["Total No. of Health Workers"] = filtered_df.groupby(
            "cadre_short_name"
        )["cadre_short_name"].transform("count")

        # Calculate percentage distribution of health workers by cadre
        total_health_workers = filtered_df["Total No. of Health Workers"].sum()
        filtered_df["% Distribution"] = (
            filtered_df["Total No. of Health Workers"] / total_health_workers
        ) * 100

        # Group the data by 'cadre' and calculate the total number of health workers
        top_10_cadres_df = (
            filtered_df.groupby("cadre_short_name")
            .agg({"Total No. of Health Workers": "sum"})
            .reset_index()
        )

        # Recalculate the % Distribution after grouping to avoid mean aggregation issues
        top_10_cadres_df["% Distribution"] = (
            (top_10_cadres_df["Total No. of Health Workers"] / total_health_workers)
            * 100
        ).round(2)  # Ensure the result is rounded to two decimal places

        # Sort by 'Total No. of Health Workers' and take the top 10 cadres
        top_10_cadres_df = top_10_cadres_df.sort_values(
            by="Total No. of Health Workers", ascending=False
        ).head(10)

        return top_10_cadres_df

    hr_top_10_cadres_df = prepare_cadre_treemap_data(merged_df, facility)
    # print(hr_top_10_cadres_df)
    return {
        "formatted_total_employees": formatted_total_employees,
        "formatted_male_percentage": formatted_male_percentage,
        "formatted_female_percentage": formatted_female_percentage,
        "formatted_disability_status_percentage": formatted_disability_status_percentage,
        "hr_qualification_counts": hr_qualification_counts,
        "hr_age_group_counts": hr_age_group_counts,
        "hr_cadre_counts": hr_cadre_counts,
        "hr_employment_type_counts": hr_employment_type_counts,
        "hr_emp_count_stackedbar": hr_emp_count_stackedbar,
        "hr_top_10_cadres_df": hr_top_10_cadres_df,
    }
