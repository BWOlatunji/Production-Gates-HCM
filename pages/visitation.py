import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data import visitation_data_processing
from src.components import ids

patients_visitation_df = visitation_data_processing.load_processed_data()


# Define layout function
def layout():
    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    html.H4(
                        "Visitation Trends and Planning",
                        className="text-left my-4",
                    )
                )
            ),
            dbc.Row(
                [
                    # Column for main charts
                    dbc.Col(
                        [
                            # 1- charts
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id=ids.VS_GENDER_PIE_CHART
                                                    ),  # Disable mode bar controls
                                                ],
                                                style={
                                                    "background-color": "#f8f9fa",  # Light background color for the container
                                                    "padding": "10px",
                                                    "border-radius": "10px",  # Rounded corners
                                                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                                                },
                                            ),
                                        ],
                                        xs=10,
                                        sm=8,
                                        md=4,
                                        lg=4,
                                        xl=4,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id=ids.VISITATION_BY_AGE_GROUP_BARCHART
                                                    ),
                                                ],
                                                style={
                                                    "background-color": "#f8f9fa",  # Light background color for the container
                                                    "padding": "10px",
                                                    "border-radius": "10px",  # Rounded corners
                                                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                                                },
                                            ),
                                        ],
                                        xs=10,
                                        sm=8,
                                        md=4,
                                        lg=4,
                                        xl=4,
                                    ),
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id=ids.VS_MARITAL_STATUS_BARCHART
                                                    ),
                                                ],
                                                style={
                                                    "background-color": "#f8f9fa",  # Light background color for the container
                                                    "padding": "10px",
                                                    "border-radius": "10px",  # Rounded corners
                                                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                                                },
                                            ),
                                        ],
                                        xs=10,
                                        sm=8,
                                        md=4,
                                        lg=4,
                                        xl=4,
                                    ),
                                ],
                                className="my-4",
                            ),
                            # 2 - heatmap
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id=ids.VS_HOURLY_TRAFFIC_HEATMAP
                                                    ),
                                                ],
                                                style={
                                                    "background-color": "#f8f9fa",  # Light background color for the container
                                                    "padding": "10px",
                                                    "border-radius": "10px",  # Rounded corners
                                                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                                                },
                                            ),
                                        ]
                                    )
                                ],
                                className="my-4",
                            ),
                            # 3 - time series
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id=ids.VISITATIONS_OVER_TIME_CHART
                                                    ),
                                                ],
                                                style={
                                                    "background-color": "#f8f9fa",  # Light background color for the container
                                                    "padding": "10px",
                                                    "border-radius": "10px",  # Rounded corners
                                                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                                                },
                                            ),
                                        ]
                                    )
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
    @app.callback(
        [
            Output(ids.VS_GENDER_PIE_CHART, "figure"),
            Output(ids.VS_MARITAL_STATUS_BARCHART, "figure"),
            Output(ids.VISITATION_BY_AGE_GROUP_BARCHART, "figure"),
            Output(ids.VS_HOURLY_TRAFFIC_HEATMAP, "figure"),
            Output(ids.VISITATIONS_OVER_TIME_CHART, "figure"),
        ],
        [Input("selected-filter-values", "data")],
    )
    def update_charts(dropdown_values):
        """Updates all charts based on selected filters."""
        selected_facilities = (
            dropdown_values.get("facility") if dropdown_values else None
        )
        start_date = dropdown_values.get("date", {}).get("start_date")
        end_date = dropdown_values.get("date", {}).get("end_date")
        # Convert dates
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filter data
        filtered_df = patients_visitation_df[
            (patients_visitation_df["start_date"] >= pd.to_datetime(start_date))
            & (patients_visitation_df["start_date"] <= pd.to_datetime(end_date))
        ]

        # Apply facility filter
        if selected_facilities:
            filtered_df = filtered_df[
                filtered_df["facility_name"].isin(selected_facilities)
            ]

        # **Handle empty dataset**
        if filtered_df.empty:
            empty_fig = px.scatter(title="No Data Available")
            return empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

        # ** Gender Pie Chart**
        # gender_fig = px.pie(
        #     filtered_df,
        #     names="gender",
        #     hole=0.4,
        #     color_discrete_sequence=[
        #         "#062d14",
        #         "#18a145",
        #     ],  # Custom colors
        # )

        # # Remove background and legend
        # gender_fig.update_layout(
        #     plot_bgcolor="rgba(0,0,0,0)",
        #     paper_bgcolor="rgba(0,0,0,0)",
        #     showlegend=True,
        #     legend_title_text="Gender",  # Custom legend title
        #     title={
        #         "text": "<b><u>Patients by Gender</u></b>",
        #         "font": {"color": "#1E1E1E"},
        #     },
        # )

        gender_fig = px.pie(
            filtered_df,
            names="gender",
            hole=0.3,
            color_discrete_sequence=[
                "#062d14",
                "#18a145",
            ],  # Custom colors
        )

        # Remove background, move legend to bottom, and increase chart size
        gender_fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            legend_title_text="Gender",  # Custom legend title
            title={
                "text": "<b><u>Patients by Gender</u></b>",
                "font": {"color": "#1E1E1E"},
            },
            width=300,  # Adjust width to increase size
            # height=500,  # Adjust height to increase size
            legend=dict(
                orientation="h",  # Horizontal orientation
                yanchor="bottom",  # Align vertically at the bottom
                y=-0.2,  # Place the legend slightly below the chart
                xanchor="center",  # Align horizontally at the center
                x=0.5,  # Position the legend at the center
            ),
        )

        # Customize hover template
        gender_fig.update_traces(hovertemplate="%{label}: %{percent}")

        # ** Marital Status Bar Chart (Fixed)**
        if "marital_status" in filtered_df.columns:
            marital_status_counts = (
                filtered_df["marital_status"]
                .fillna("Unknown")
                .value_counts()
                .reset_index()
            )
            marital_status_counts.columns = ["marital_status", "count"]

            marital_fig = px.bar(
                marital_status_counts,
                x="marital_status",
                y="count",
                labels={"marital_status": "Marital Status", "count": "Count"},
                color="marital_status",
                color_discrete_sequence=[
                    "#062d14",
                    "#18a145",
                ],
            )

            marital_fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
                legend_title_text="Marital Status",  # Custom legend title
                title={
                    "text": "<b><u>Patients by Marital Status</u></b>",
                    "font": {"color": "#1E1E1E"},
                },
            )

            marital_fig.update_traces(
                hovertemplate="Marital Status: %{x} <br>Count: %{y}"
            )
        else:
            marital_fig = px.bar(title="Marital Status Data Not Available")

        # ** Visitation Count by Age Group**
        # Define the correct order of age groups
        desired_order = [
            "0-4",
            "5-9",
            "10-19",
            "20-29",
            "30-39",
            "40-49",
            "50-59",
            "60+",
        ]

        # Create a dictionary of age group counts with missing groups set to zero
        age_group_counts = filtered_df["age_group"].value_counts().to_dict()
        age_group_counts = {age: age_group_counts.get(age, 0) for age in desired_order}

        # Create the bar chart
        visitation_age_fig = px.bar(
            x=list(age_group_counts.keys()),  # Ensure correct order
            y=list(age_group_counts.values()),
            color=list(age_group_counts.keys()),
            color_discrete_map={
                "0-4": "#062d14",
                "5-9": "#15522a",
                "10-19": "#165e2e",
                "20-29": "#177e38",
                "30-39": "#18a145",
                "40-49": "#25c258",
                "50-59": "#4cdc7a",
                "60+": "#88eda7",
            },
            labels={"x": "Age Group", "y": "Visit Count"},
        )

        # Apply custom hover template and clean up layout
        visitation_age_fig.update_traces(
            hovertemplate="<b>Age Group:</b> %{x}<br><b>Visits:</b> %{y}<extra></extra>"
        )
        visitation_age_fig.update_layout(
            showlegend=False,  # Remove legend
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
            paper_bgcolor="rgba(0,0,0,0)",  # Transparent figure background
            title={
                "text": "<b><u>Visitation by Age Group</u></b>",
                "font": {"color": "#1E1E1E"},
            },
        )

        # ** heatmap showing visitation count by hour of the day and day of the week.

        """Updates the heatmap showing visitation count by hour of the day and day of the week."""

        # Add hour and weekday name columns
        filtered_df["hour"] = pd.to_datetime(
            filtered_df["time_in"], errors="coerce"
        ).dt.hour
        filtered_df["weekday"] = pd.to_datetime(
            filtered_df["start_date"], errors="coerce"
        ).dt.day_name()

        # Ensure the weekdays are ordered correctly
        weekday_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        # Group by weekday and hour to get counts
        heatmap_data = (
            filtered_df.groupby(["weekday", "hour"]).size().reset_index(name="count")
        )

        # Pivot the data for heatmap (weekday as rows, hour as columns)
        pivot_df = heatmap_data.pivot(
            index="weekday", columns="hour", values="count"
        ).reindex(weekday_order)

        # Create heatmap using go.Heatmap for more control
        heatmap_fig = go.Figure(
            data=go.Heatmap(
                z=pivot_df.values,
                x=pivot_df.columns,
                y=pivot_df.index,
                colorscale=[
                    [0, "#f0fdf4"],  # Low values
                    [0.5, "#4ddb7d"],  # Midpoint values
                    [1, "#062d15"],  # High values
                ],
                hovertemplate="Hour: %{x}<br>Weekday: %{y}<br>Count: %{z}",
                hoverinfo="x+y+z",  # Exclude trace name from hover information
                name="",  # Set name to empty to remove "trace 0"
            )
        )
        # Update layout for better hourly view
        heatmap_fig.update_layout(
            title={
                "text": "<b><u>Visitation Traffic (Time and Day of the Week)</u></b>",
                "font": {"color": "#1E1E1E"},
            },
            xaxis_title="Hour of Day (0-23)",
            yaxis_title="Weekday",
            xaxis=dict(tickmode="linear", dtick=1),
        )

        # Count rows for each visit_date
        visitations_over_time = (
            filtered_df.groupby("start_date")
            .size()
            .reset_index(name="visitation_count")
        )

        # Create the line chart
        visitations_over_time_fig = px.line(
            visitations_over_time,
            x="start_date",
            y="visitation_count",
            labels={"start_date": "Date", "visitation_count": "Total Visitations"},
            color_discrete_sequence=["green"],  # Change the line color here
        )

        # Improve layout
        visitations_over_time_fig.update_layout(
            xaxis_title="Date", yaxis_title="Total Visitations"
        )
        # Remove background and legend
        visitations_over_time_fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            title={
                "text": "<b><u>Visitation Volume Over Time</u></b>",
                "font": {"color": "#1E1E1E"},
            },
        )

        return (
            gender_fig,
            marital_fig,
            visitation_age_fig,
            heatmap_fig,
            visitations_over_time_fig,
        )
