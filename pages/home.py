import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from src.data.home_data_processing import load_and_process_data

# from src.charts.gender_pie_chart import create_gender_pie_chart
# from src.charts.agegroup_chart import create_patients_age_group_bar_chart
# from src.charts.marital_status_bar_chart import create_marital_status_chart
from src.charts import helper_charts

# get processed data
data = load_and_process_data()

# Extract data
male_patients = data["male_patients"]
female_patients = data["female_patients"]
patients_age_group = data["patients_age_group"]
visitations_age_group = data["visitations_age_group"]
patients_marital_status_count = data["patients_marital_status_count"]
visitations_marital_status_count = data["visitations_marital_status_count"]
v_male_patients = data["v_male_patients"]
v_female_patients = data["v_female_patients"]
formatted_total_patients = data["formatted_total_patients"]
total_lgas = data["total_lgas"]
total_wards = 11  # data["total_wards"]
total_facilities = data["total_facilities"]
formatted_male_percentage = data["formatted_male_percentage"]
formatted_female_percentage = data["formatted_female_percentage"]
formatted_single_patients = data["formatted_single_patients"]
formatted_married_patients = data["formatted_married_patients"]
formatted_total_employees = data["formatted_total_employees"]
formatted_disability_status_percentage = data["formatted_disability_status_percentage"]


# Define custom colors for marital statuses
marital_status_colors = {
    "Single": "#062d14",
    "Married": "#15522a",
}

# Register this page in Dash's page registry
dash.register_page(__name__, path="/")


def create_kpi_card(card_value, card_text):
    return dbc.Col(
        html.Div(
            className="kpi-card",
            children=[
                html.Span(card_value, className="card-value"),
                html.Span(card_text, className="card-text"),
            ],
        ),
    )


# Define layout function
def layout():
    return html.Div(
        [
            dbc.Row(
                dbc.Col(
                    html.H5(
                        "Human Resources for Health Overview",
                        className="text-left my-4",
                    ),
                    width={"size": 10},
                )
            ),
            # KPI Cards
            html.Div(
                id="kpi-container",
                children=dbc.Row(
                    [
                        create_kpi_card(
                            card_value=formatted_total_patients,
                            card_text="Patients",
                        ),
                        create_kpi_card(
                            card_value=total_lgas,
                            card_text="LGAs",
                        ),
                        create_kpi_card(
                            card_value=total_wards,
                            card_text="Wards",
                        ),
                        create_kpi_card(
                            card_value=total_facilities,
                            card_text="Facilities",
                        ),
                        create_kpi_card(
                            card_value=formatted_total_employees,
                            card_text="HRH",
                        ),
                        create_kpi_card(
                            card_value=formatted_total_employees,
                            card_text="HRH",
                        ),
                    ],
                    className="g-1",  # add spacing between columns
                ),
            ),
            ## Registration title
            html.Div(
                html.H5(
                    "Registration Overview",
                    className="text-left my-3",
                )
            ),
            # Registration charts
            dbc.Row(
                [
                    # REGISTRATION - GENDER
                    helper_charts.create_chart_column(
                        helper_charts.create_gender_pie_chart(
                            values=[
                                male_patients,
                                female_patients,
                            ],
                            names=[
                                "Male",
                                "Female",
                            ],
                            hovertemplate="<b>Gender: </b> %{label}<br><b>Count: </b> %{value}<br><b>Percentage: </b> %{percent:.2%}<extra></extra>",
                            title="Patients by Gender",
                            legend_title="Gender",
                            height=300,  # Default height
                            width=300,  # Default width
                        )
                    ),
                    # REGISTRATION - AGE GROUP
                    helper_charts.create_chart_column(
                        helper_charts.create_patients_age_group_bar_chart(
                            age_group_count=patients_age_group,
                            title="Patients by Age Group",
                            height=300,  # Default height
                            width=300,  # Default width, full container width
                        )
                    ),
                    # REGISTRATION - MARITAL STATUS
                    helper_charts.create_chart_column(
                        helper_charts.create_marital_status_chart(
                            marital_status_count=patients_marital_status_count,
                            title="Patients by Marital Status",
                            x_label="Marital Status",  # Default x-axis label
                            y_label="Count",  # Default y-axis label
                            height=300,  # Default height
                            width=300,  # Default width
                        )
                    ),
                ]
            ),
            ## Visitation title
            html.Div(
                html.H5(
                    "Visitation Overview",
                    className="text-left my-3",
                )
            ),
            # Charts 2 - Visitation
            dbc.Row(
                [
                    # Pie chart for gender
                    helper_charts.create_chart_column(
                        helper_charts.create_gender_pie_chart(
                            values=[
                                v_male_patients,
                                v_female_patients,
                            ],
                            names=[
                                "Male",
                                "Female",
                            ],
                            hovertemplate="<b>Gender: </b> %{label}<br><b>Count: </b> %{value}<br><b>Percentage: </b> %{percent:.2%}<extra></extra>",
                            title="Visitations by Gender",
                            legend_title="Gender",
                            height=300,  # Default height
                            width=300,  # Default width
                        )
                    ),
                    # Bar chart for patient age group distribution for registered patients and those who come for visitation
                    helper_charts.create_chart_column(
                        helper_charts.create_patients_age_group_bar_chart(
                            age_group_count=visitations_age_group,
                            title="Visitations by Age Group",
                            height=300,  # Default height
                            width=300,  # Default width, full container width
                        )
                    ),
                    # VISITATION - MARITAL STATUS
                    helper_charts.create_chart_column(
                        helper_charts.create_marital_status_chart(
                            marital_status_count=visitations_marital_status_count,
                            title="Visitations by Marital Status",
                            x_label="",  # Default x-axis label
                            y_label="Count",  # Default y-axis label
                            height=300,  # Default height
                            width=300,  # Default width
                        )
                    ),
                ]
            ),
        ],
    )
