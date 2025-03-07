from dash import dcc, html
import plotly.express as px


def create_gender_pie_chart(
    values,
    names,
    hovertemplate,
    title="Patients by Gender",
    legend_title="Gender",
):
    # Create the pie chart using the specified parameters
    gender_pie_chart = dcc.Graph(
        figure=px.pie(
            values=values,
            names=names,
            color_discrete_sequence=[
                "#062d14",
                "#18a145",
            ],
        )
        .update_traces(hovertemplate=hovertemplate)
        .update_layout(
            showlegend=True,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            legend_title_text=legend_title,
            title={"text": f"<b><u>{title}</u></b>", "font": {"color": "#1E1E1E"}},
        ),
        config={"displayModeBar": False},
    )

    # Return the Div with the chart and the specified class
    return gender_pie_chart
