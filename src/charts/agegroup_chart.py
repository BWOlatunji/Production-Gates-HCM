from dash import dcc, html
import plotly.express as px

# Bar chart for age group distribution
desired_order = ["0-4", "5-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60+"]
hovertemp = "<b>Age Group: </b> %{x} <br><b>Patient Count: </b> %{y} <br>"


def create_patients_age_group_bar_chart(
    age_group_count,
    title="Visitation by Age Group",
):
    age_group_chart = dcc.Graph(
        figure=px.bar(
            x=desired_order,
            y=[age_group_count.get(age_group, 0) for age_group in desired_order],
            color=desired_order,
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
            # legend_title_text="Age Group",  # Custom legend title
            title={
                "text": f"<b><u>{title}</u></b>",  # Bold and underline title
                "font": {"color": "#1E1E1E"},  # Set title color to green
            },
        ),
        config={"displayModeBar": False},  # Disable Plotly menu bar
    )

    return age_group_chart
