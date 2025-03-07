# import dash
# from dash import dcc, html, Input, Output
# import dash_bootstrap_components as dbc
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go

# from src.data.visitation_data_processing import load_processed_data
# from src.charts.gender_pie_chart import create_gender_pie_chart
# from src.charts.agegroup_chart import create_patients_age_group_bar_chart
# from src.charts.marital_status_bar_charts import create_marital_status_chart

from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go


def layout():
    return html.Div(
        [
            html.H3("Visitation Dashboard"),
            dcc.Graph(id="visitation-chart"),  # Placeholder for a chart
            html.Div(id="visitation-details"),  # Placeholder for details
            html.Div(id="visitation-dates"),  # Div to show the selected date range
        ]
    )


def register_callbacks(app):
    @app.callback(
        [
            Output("visitation-chart", "figure"),
            Output("visitation-details", "children"),
            Output("visitation-dates", "children"),
        ],  # Output for date range
        [Input("selected-dropdown-values", "data")],
    )
    def update_visitation_page(dropdown_values):
        facility = dropdown_values.get("facility") if dropdown_values else None
        start_date = dropdown_values.get("date", {}).get("start_date")
        end_date = dropdown_values.get("date", {}).get("end_date")

        if facility:
            chart_title = f"Visitation Data for Facility: {facility}"
            fig = {
                "data": [
                    {
                        "x": [1, 2, 3],
                        "y": [
                            facility.count("a"),
                            facility.count("b"),
                            facility.count("c"),
                        ],
                    }
                ],
                "layout": {"title": chart_title},
            }
            details = f"Showing data for facility: {facility}"
        else:
            fig = {
                "data": [{"x": [1, 2, 3], "y": [4, 1, 2]}],
                "layout": {"title": "Visitation Data (Default)"},
            }
            details = "No facility selected. Showing default data."

        # Display the selected date range
        date_range = (
            f"Selected Date Range: {start_date} to {end_date}"
            if start_date and end_date
            else "No date range selected."
        )

        return fig, details, date_range
