import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px


def create_chart_column(chart_template):
    return html.Div(
        [
            html.Div(
                [chart_template],
                style={
                    "background-color": "#f8f9fa",  # Light background color for the container
                    # "padding": "20px",
                    "border-radius": "10px",  # Rounded corners
                    "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.2)",  # Box shadow effect
                },
            ),
        ],
        className="col-xs-10 col-sm-8 col-md-4 col-lg-4 col-xl-4",  # Correct Bootstrap classes for responsive layout
    )


# Bar chart for age group distribution
p_desired_order = ["0-4", "5-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60+"]
hovertemp = "<b>Age Group: </b> %{x} <br><b>Patient Count: </b> %{y} <br>"


def create_patients_age_group_bar_chart(
    age_group_count,
    title="Visitation by Age Group",
    height=400,  # Default height
    width=500,  # Default width, full container width
):
    age_group_chart = dcc.Graph(
        figure=px.bar(
            x=p_desired_order,
            y=[age_group_count.get(age_group, 0) for age_group in p_desired_order],
            color=p_desired_order,
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
            labels={
                "x": "",
                "y": "Count",
            },
        )
        .update_traces(hovertemplate=hovertemp)  # Apply custom hover template
        .update_layout(
            showlegend=False,  # Remove legend
            plot_bgcolor="rgba(0,0,0,0)",  # Remove background color of plot area
            paper_bgcolor="rgba(0,0,0,0)",  # Remove background color of entire figure
            title={
                "text": f"<b><u>{title}</u></b>",  # Bold and underline title
                "font": {"color": "#1E1E1E"},  # Set title color to green
            },
            height=height,  # Set the height dynamically
            width=width,  # Set the width dynamically
            margin={"t": 40, "b": 40},  # Adjust top and bottom margins for the title
        ),
        config={"displayModeBar": False},  # Disable Plotly menu bar
        style={
            "height": height,
            "width": width,
        },  # Apply the dynamic size to the container
    )

    return age_group_chart


def create_gender_pie_chart(
    values,
    names,
    hovertemplate,
    title="Patients by Gender",
    legend_title="Gender",
    height=400,  # Default height
    width=500,  # Default width
):
    # Create the pie chart using the specified parameters
    gender_pie_chart = dcc.Graph(
        figure=px.pie(
            values=values,
            names=names,
            color_discrete_sequence=[
                "#062d14",  # Color for the first slice
                "#18a145",  # Color for the second slice
            ],
        )
        .update_traces(hovertemplate=hovertemplate)
        .update_layout(
            showlegend=True,
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
            paper_bgcolor="rgba(0,0,0,0)",  # Transparent figure background
            legend_title_text=legend_title,
            title={"text": f"<b><u>{title}</u></b>", "font": {"color": "#1E1E1E"}},
            height=height,  # Set dynamic height
            width=width,  # Set dynamic width
        ),
        config={"displayModeBar": False},  # Disable Plotly mode bar
        style={
            "height": height,
            "width": width,
        },  # Apply dynamic height and width to the container
    )

    return gender_pie_chart


marital_status_colors = {
    "Single": "#062d14",
    "Married": "#15522a",
}


def create_marital_status_chart(
    marital_status_count,
    title="Patients by Marital Status",
    x_label="Marital Status",  # Default x-axis label
    y_label="Count",  # Default y-axis label
    height=400,  # Default height
    width=500,  # Default width
):
    # Create the bar chart using the specified marital status colors
    marital_status_chart = dcc.Graph(
        figure=px.bar(
            x=list(marital_status_colors.keys()),  # Marital status categories
            y=[
                marital_status_count.get(status, 0)
                for status in marital_status_colors.keys()
            ],  # Counts for each category
            color=list(marital_status_colors.keys()),  # Color mapping for categories
            color_discrete_map=marital_status_colors,  # Custom color map
            labels={"x": x_label, "y": y_label},  # Dynamic x and y axis labels
        )
        .update_traces(
            hovertemplate="<b>Status:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>"  # Custom hover template
        )
        .update_layout(
            showlegend=False,  # Hide legend
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent plot background
            paper_bgcolor="rgba(0,0,0,0)",  # Transparent figure background
            title={
                "text": f"<b><u>{title}</u></b>",
                "font": {"color": "#1E1E1E"},
            },  # Custom title style
            height=height,  # Set dynamic height
            width=width,  # Set dynamic width
        ),
        config={"displayModeBar": False},  # Disable Plotly mode bar
        style={
            "height": height,
            "width": width,
        },  # Apply dynamic height and width to the container
    )

    # Return the chart with the updated layout
    return marital_status_chart
