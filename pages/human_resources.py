import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data import hr_data_processing
from src.components import ids


# Define layout function
def layout():
    return html.Div(
        [
            dbc.Row(
                dbc.Col(
                    html.H4(
                        "Human Resources - Overview",
                        className="text-left my-4",
                    )
                )
            ),
            # html.Div(children=[ html.Div(
            #     dcc.Dropdown(
            #         id=ids.STATE_DROPDOWN,  # Using id constant here
            #         options=[
            #             {"label": state, "value": state}
            #             for state in states_df["state_name"].unique()
            #         ],
            #         placeholder="Select State",
            #         className="dropdown",
            #     ),
            # ),]),
            dbc.Row(
                [
                    # Column for main charts
                    dbc.Col(
                        [
                            # 1 - charts
                            dbc.Row(
                                [
                                    # employee-counts-by-qualification
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id=ids.EMPLOYEE_COUNT_BY_QUALIFICATION
                                                    )
                                                ],
                                                style={
                                                    "background-color": "#f8f9fa",  # Light background color for the container
                                                    "padding": "20px",
                                                    "border-radius": "10px",  # Rounded corners
                                                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                                                },
                                            ),
                                        ],
                                        xs=10,
                                        sm=8,
                                        md=6,
                                        lg=6,
                                        xl=6,
                                    ),
                                    # employee-distribution-by-age
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id=ids.EMPLOYEE_DISTRIBUTION_BY_AGE
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
                                        xs=10,
                                        sm=8,
                                        md=6,
                                        lg=6,
                                        xl=6,
                                    ),
                                ],
                                className="my-4",
                            ),
                            # 2 - charts
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id=ids.PERCENTAGE_DISTRIBUTION_BY_CADRE
                                                    )
                                                ],
                                                style={
                                                    "background-color": "#f8f9fa",  # Light background color for the container
                                                    "padding": "20px",
                                                    "border-radius": "10px",  # Rounded corners
                                                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                                                },
                                            ),
                                        ],
                                        xs=10,
                                        sm=8,
                                        md=12,
                                        lg=12,
                                        xl=12,
                                    ),
                                ]
                            ),
                            # 3 - charts
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.Div(
                                                [
                                                    dcc.Graph(
                                                        id=ids.EMPLOYEE_PERCENTAGE_BY_EMPLOYMENT_TYPE
                                                    ),
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
                                        xs=10,
                                        sm=8,
                                        md=12,
                                        lg=12,
                                        xl=12,
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
        # fluid=True,
    )


def register_callbacks(app):
    @app.callback(
        [
            Output(ids.EMPLOYEE_COUNT_BY_QUALIFICATION, "figure"),
            Output(ids.EMPLOYEE_DISTRIBUTION_BY_AGE, "figure"),
            Output(ids.EMPLOYEE_PERCENTAGE_BY_EMPLOYMENT_TYPE, "figure"),
            Output(ids.PERCENTAGE_DISTRIBUTION_BY_CADRE, "figure"),
        ],
        [Input("selected-filter-values", "data")],
    )
    def update_human_resources_page(dropdown_values):
        facility = dropdown_values.get("facility") if dropdown_values else None

        # Call load_processed_data
        data = hr_data_processing.load_hr_processed_data(facility)

        hr_qualification_counts = data["hr_qualification_counts"]
        hr_age_group_counts = data["hr_age_group_counts"]
        hr_employment_type_counts = data["hr_employment_type_counts"]
        hr_top_10_cadres_df = data["hr_top_10_cadres_df"]
        print(hr_age_group_counts.columns)
        print(hr_qualification_counts.columns)
        print(hr_employment_type_counts.columns)
        print(hr_top_10_cadres_df.columns)

        qualification_counts = hr_qualification_counts
        if qualification_counts.empty:
            return go.Figure().add_annotation(
                text="No data available", x=0.5, y=0.5, showarrow=False
            )

        # Sort the DataFrame by 'counts' in descending order
        qualification_counts = qualification_counts.sort_values(
            "counts", ascending=False
        )
        # Create the bar chart
        qcount_fig = px.bar(
            qualification_counts,
            x="counts",
            y="qualification_short_name",
            labels={
                "counts": "Employees",
                "qualification_short_name": "Qualification",
            },
            orientation="h",  # Horizontal bars
            color_discrete_sequence=["#18a145"],  # Set the desired color (green in this case)
            text="counts",  # Add text labels (counts) to the bars
        )

        # Apply custom hover template, add text labels, and clean up layout
        qcount_fig.update_traces(
            hovertemplate="<b>Qualification:</b> %{y}<br><b>Counts:</b> %{x}<extra></extra>",
            textposition="auto",  # Automatically position the text (inside or outside)
        )

        qcount_fig.update_layout(
            showlegend=False,  # Remove legend
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
            paper_bgcolor="rgba(0,0,0,0)",  # Transparent figure background
            title={
                "text": "<b><u>Employee by Qualification</u></b>",
                "font": {"color": "#1E1E1E"},
            },
        )


        age_group_counts = hr_age_group_counts
        if age_group_counts.empty:
            return go.Figure().add_annotation(
                text="No data available", x=0.5, y=0.5, showarrow=False
            )

        age_group_counts_fig = px.bar(
            age_group_counts,
            x="age_group",
            y="counts",
            labels={"counts": "Employee Count", "age_group": "Age Group"},
            color="age_group",  # Use 'age_group' column for color mapping
            # ["below 20", "20-29", "30-39", "40-49", "50-59", "60+"]
            color_discrete_map={
                "< 20": "#062d14",
                "20-29": "#15522a",
                "30-39": "#165e2e",
                "40-49": "#177e38",
                "50-59": "#18a145",
                "60+": "#25c258",
            },
        )
        # showing the plot without floating toolbar in Plotly
        # age_group_counts_fig.show(config={"displayModeBar": False})

        # Apply custom hover template and clean up layout
        age_group_counts_fig.update_traces(
            hovertemplate="<b>Age Group:</b> %{x}<br><b>Counts:</b> %{y}<extra></extra>"
        )
        age_group_counts_fig.update_layout(
            showlegend=False,  # Remove legend
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
            paper_bgcolor="rgba(0,0,0,0)",  # Transparent figure background
            title={
                "text": "<b><u>Employee Distribution by Age Group</u></b>",
                "font": {"color": "#1E1E1E"},
            },
        )

        employment_counts = hr_employment_type_counts

        # Sort by employment_type to ensure the order is consistent for bars and legend
        employment_counts = employment_counts.sort_values("employment_type")

        # Create a stacked bar chart with multiple segments for each employment type
        employment_counts_fig = go.Figure()

        # Define the colors for the employment types
        colors = [
            "#062d14",
            "#165e2e",
            "#18a145",
            "#4cdc7a",
        ]

        # Add a segment for each employment type in the stacked bar
        for i, row in employment_counts.iterrows():
            employment_counts_fig.add_trace(
                go.Bar(
                    x=[row["percentage"]],  # Percentage for this employment type
                    name=row["employment_type"],  # Employment type as the label
                    orientation="h",
                    hovertemplate=f"Employment Type: {row['employment_type']}<br>Count: {row['counts']}<br>Percentage: {row['percentage']:.2f}%<extra></extra>",
                    text=f"{row['employment_type']}: {row['percentage']:.2f}%",
                    textposition="none",  # Hide the text inside the bar
                    marker_color=colors[
                        i % len(colors)
                    ],  # Cycle through the defined colors
                )
            )

        # Update the layout for the figure
        employment_counts_fig.update_layout(
            title={
                "text": "<b><u>% Health Workers by Employment Type</u></b>",
                "font": {"color": "#1E1E1E"},
            },
            xaxis_title="",
            barmode="stack",  # Stack the bars horizontally
            showlegend=True,  # Show the legend for the employment types
            legend_title_text="Workers Group",  # Custom legend title
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis_title="",  # Remove the y-axis title
            height=200,  # Adjust the height of the chart here
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="top",  # Aligns the top of the legend box with the position defined by 'y'
                y=-0.6,  # Move the legend further down to add more space
                xanchor="center",  # Center the legend horizontally
                x=0.5,  # Position it at the center of the chart
            ),
        )

        # Optional: Customize y-axis ticks if needed
        employment_counts_fig.update_yaxes(
            tickmode="auto",  # Ensure tickmarks display correctly
            showline=True,  # Show the axis line
            zeroline=False,  # Disable the "zero" reference line
            showgrid=True,  # Optionally, show or hide the gridlines
        )

        top_10_cadres_df = hr_top_10_cadres_df

        # Create the treemap
        top_10_cadres_fig = px.treemap(
            top_10_cadres_df,
            path=["cadre_short_name"],  # The hierarchy of categories (only 'cadre' here)
            values="Total No. of Health Workers",  # The metric to represent the size of the treemap areas
            color="% Distribution",  # The column used to color the treemap
            color_continuous_scale="BuGn",  # Color scale for the treemap
        )

        # Remove grey background by setting plot and paper background to white (or transparent if you prefer)
        top_10_cadres_fig.update_layout(
            plot_bgcolor="white",  # Background color of the plot area
            paper_bgcolor="white",  # Background color of the entire figure
            title={
                "text": "<b><u>% Distribution of Health Workers by Cadre (Top 10)</u></b>",
                "font": {"color": "#1E1E1E"},
            },
        )

        # Update the hovertemplate to display both total workers and % distribution
        top_10_cadres_fig.update_traces(
            hovertemplate="<b>%{label}</b><br>Total Workers: %{value}<br>% Distribution: %{color:.2f}%<extra></extra>"
        )
        # fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

        return (
            qcount_fig,
            age_group_counts_fig,
            employment_counts_fig,
            top_10_cadres_fig,
        )
