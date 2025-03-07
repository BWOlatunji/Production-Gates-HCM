from dash import dcc, html
import plotly.express as px


marital_status_colors = {
    "Single": "#062d14",
    "Married": "#15522a",
}


def create_marital_status_chart(
    marital_status_count, title="Patients by Marital Status"
):
    # Create the bar chart using the specified marital status colors
    marital_status_chart = dcc.Graph(
        figure=px.bar(
            x=list(marital_status_colors.keys()),
            y=[
                marital_status_count.get(status, 0)
                for status in marital_status_colors.keys()
            ],
            color=list(marital_status_colors.keys()),
            color_discrete_map=marital_status_colors,
            labels={"x": "", "y": "Count"},
        )
        .update_traces(
            hovertemplate="<b>Status:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>"
        )
        .update_layout(
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            title={"text": f"<b><u>{title}</u></b>", "font": {"color": "#1E1E1E"}},
        ),
    )

    # Return the Div with the chart and the specified class
    return marital_status_chart
