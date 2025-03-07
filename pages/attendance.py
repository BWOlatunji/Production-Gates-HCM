import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.data import attendance_data_processing
from src.components import ids

# Load the CSV file
df = attendance_data_processing.load_processed_data()


# Custom color scale
custom_colorscale = [
    [0, "#f0fdf4"],  # Low values
    [0.5, '#4ddb7d'],  # Midpoint values
    [1, "#062d15"],  # High values
]


# Define layout function
def layout():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H4(
                        "HRH - Attendance Overview",
                        className="text-left my-4",
                    )
                )
            ),
            dbc.Row(
                [
                    # Column for main charts
                    dbc.Col(
                        [
                            # Dropdown for state, LGA, ward, and facility filters
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            # Year dropdown filter
                                            dcc.Dropdown(
                                                id=ids.YEAR_DROPDOWN,
                                                placeholder="Select Year",
                                                options=[
                                                    {
                                                        "label": year,
                                                        "value": year,
                                                    }
                                                    for year in df[
                                                        "date"
                                                    ].dt.year.unique()
                                                ],
                                                clearable=False,
                                            ),
                                        ],
                                        width=2,
                                    ),
                                    dbc.Col(
                                        [
                                            # Date range picker
                                            dcc.Dropdown(
                                                id=ids.MONTH_DROPDOWN,
                                                placeholder="Select Month",
                                                multi=True,
                                                options=[
                                                    {
                                                        "label": month,
                                                        "value": month,
                                                    }
                                                    for month in df["date"]
                                                    .dt.month_name(locale="English")
                                                    .unique()
                                                ],
                                                clearable=False,
                                            ),
                                        ],
                                        width=5,
                                    ),
                                    dbc.Col(
                                        width=1,
                                    ),
                                ],
                                className="mb-4",
                            ),
                            # 1 - charts
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    # Time series plot
                                                    dcc.Graph(
                                                        id=ids.ATTENDANCE_TIMESERIES_CHART
                                                    ),
                                                ],
                                                style={
                                                    "background-color": "#f8f9fa",  # Light background color for the container
                                                    "padding": "20px",
                                                    "border-radius": "10px",  # Rounded corners
                                                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                                                },
                                            ),
                                        ],
                                        width=12,
                                    ),
                                ]
                            ),
                            # 2 - charts
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    # Heatmap plot
                                                    dcc.Graph(id=ids.ATTENDANCE_HEATMAP)
                                                ],
                                                style={
                                                    "background-color": "#f8f9fa",  # Light background color for the container
                                                    "padding": "20px",
                                                    "border-radius": "10px",  # Rounded corners
                                                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                                                    # "height": "150px",  # Reduce the overall height of the container
                                                },
                                            ),
                                        ],
                                        width=12,
                                    ),
                                ],
                                className="my-4",
                            ),
                        ],
                        width=12,
                    ),
                ]
            ),
        ],
        fluid=True,
    )


def register_callbacks(app):
    # Callback to update charts based on selected year and date range
    @app.callback(
    [
        Output(ids.ATTENDANCE_TIMESERIES_CHART, "figure"),
        Output(ids.ATTENDANCE_HEATMAP, "figure"),
    ],
    [
        Input(ids.YEAR_DROPDOWN, "value"),
        Input(ids.MONTH_DROPDOWN, "value"),
        Input("selected-filter-values", "data"),
    ],
)
    def update_charts(selected_year, selected_month, dropdown_values):
        start_date = dropdown_values.get("date", {}).get("start_date")
        end_date = dropdown_values.get("date", {}).get("end_date")
        
        # Initially use the entire dataset
        filtered_df = df.copy()

        # Filter data based on the selected date range
        filtered_df = filtered_df[
            (filtered_df["date"] >= start_date) & (filtered_df["date"] <= end_date)
        ]

        if selected_year:
            # Filter data based on selected year
            filtered_df = filtered_df[filtered_df["date"].dt.year == selected_year]

        if selected_month:
            # Filter data based on selected month
            filtered_df = filtered_df[
                filtered_df["date"].dt.month_name(locale="English").isin(selected_month)
            ]

        # Prepare heatmap data (group by clockin_hour and weekday)
        heatmap_data = (
            filtered_df.groupby(["weekday", "clockin_hour"])["employee_id"]
            .nunique()
            .reset_index(name="employee_count")
        )

        # Pivot the data to create a matrix for the heatmap
        heatmap_data_pivot = heatmap_data.pivot(
            index="weekday", columns="clockin_hour", values="employee_count"
        )

        # Ensure weekdays are ordered correctly
        weekday_order = [
            "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
        ]
        heatmap_data_pivot = heatmap_data_pivot.reindex(weekday_order)

        # Create heatmap with custom color scale
        heatmap_fig = px.imshow(
            heatmap_data_pivot,
            labels=dict(x="Hour of Day", y="Weekday", color="Employee Count"),
            x=heatmap_data_pivot.columns,  # Use hours as the x-axis
            y=heatmap_data_pivot.index,  # Use weekdays as the y-axis
            title="Employee Count Heatmap (Hour vs Weekday)",
            aspect="auto",
            color_continuous_scale=custom_colorscale,  # Apply custom color scale
        )

        # Improve layout for heatmap
        heatmap_fig.update_layout(
            xaxis_title="Hour of Day",  # Update the x-axis title to represent hours
            yaxis_title="Weekday",  # Update the y-axis title to represent weekdays
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            title={
                "text": "<b><u>Employee Count Heatmap (Hour vs Weekday)</u></b>",
                "font": {"color": "#1E1E1E"},
            },
        )

        # Prepare time series data
        time_series_data = (
            filtered_df.groupby("date")["employee_id"]
            .nunique()
            .reset_index(name="employee_count")
        )

        # Create time series plot
        time_series_fig = px.line(
            time_series_data,
            x="date",
            y="employee_count",
            title="Employee Count Over Time",
            color_discrete_sequence=["green"],  # Change the line color here
        )

        # Improve layout for time series plot
        time_series_fig.update_layout(
            xaxis_title="", yaxis_title="Employee Count",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            title={
                "text": "<b><u>Employee Volume (Attendance) Over Time</u></b>",
                "font": {"color": "#1E1E1E"},
            },
        )

        return time_series_fig, heatmap_fig
