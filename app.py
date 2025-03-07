import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# Import the components for different pages
from pages import human_resources, visitation, attendance
from src.components import filter_components, ids

from src.data import (
    facilities_location_data as fld,
)

# Load the data
states_df, lgas_df, wards_df, facilities_df = fld.load_facility_location_data()


external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

# Initialize the Dash app
app = dash.Dash(
    __name__,
    use_pages=True,  # Enables multi-page support
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, external_stylesheets],
)

# Define the Sidebar (with example dropdowns)
sidebar = filter_components.create_location_dropdowns(
    app, states_df, lgas_df, wards_df, facilities_df
)

# Registering pages after the app is instantiated
dash.register_page("visitation", path="/visitation", layout=visitation.layout)
dash.register_page(
    "human_resources", path="/human_resources", layout=human_resources.layout
)
dash.register_page("attendance", path="/attendance", layout=attendance.layout)

# Define the Navbar using NavbarSimple
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dcc.Link("Home", href="/", className="nav-link")),
        dbc.NavItem(
            dcc.Link("Human Resources", href="/human_resources", className="nav-link")
        ),
        dbc.NavItem(dcc.Link("Attendance", href="/attendance", className="nav-link")),
        dbc.NavItem(dcc.Link("Visitation", href="/visitation", className="nav-link")),
        dbc.NavItem(dcc.Link("Payroll", href="/payroll", className="nav-link")),
    ],
    color="#15522b",
    dark=True,
    fluid=True,
    sticky="top",
    brand_external_link=False,
    style={
        "padding-left": "10px",
        "padding-right": "10px",
    },
)

# Combined Header and Navbar Row
header_navbar = dbc.Row(
    [
        # Logo Column
        dbc.Col(
            html.Img(
                src="/assets/logo.jpg",
                height="40px",
            ),
            width="auto",
        ),
        # Title Column
        # Title Column with Bootstrap Responsive Font Classes
        dbc.Col(
            html.P(
                "Tracking Health Worker Productivity Dashboard",
                className="text-primary mb-0 fs-md-3 fs-lg-4",  # Adjust font size for different breakpoints
            ),
            width=True,
            style={"display": "flex", "align-items": "center"},  # Align text vertically
        ),
        # Navbar Column
        dbc.Col(
            navbar,
            width="auto",
            style={
                "display": "flex",
                "align-items": "center",
            },  # Align navbar vertically
        ),
    ],
    justify="between",
    align="center",
)

# Define the Footer
footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    [
                        html.Div("Powered By: "),
                        html.A(
                            href="https://hcm.ng/rite/",
                            children=[
                                html.Img(
                                    alt="HCM",
                                    src="/assets/logo banner_cropped.png",
                                    style={"width": "150px", "height": "auto"},
                                )
                            ],
                        ),
                    ],
                    className="d-flex justify-content-center align-items-center gap-2",
                ),
            )
        ],
    ),
    className="footer p-3",
    fluid=True,
)


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


# App layout
app.layout = html.Div(
    [
        # Header
        # Navigation Bar
        dbc.Row(
            [
                html.Div(
                    id="header_navbar",
                    children=header_navbar,
                )
            ]
        ),
        # Sidebar and Content
        dbc.Row(
            [
                # Collapsible Sidebar
                dbc.Col(
                    id="collapsible-sidebar",
                    children=dbc.Card(
                        [
                            dbc.CardHeader(
                                id="card-header",
                                children=[
                                    html.Div(
                                        html.H5("Filters", style={"margin": "0"}),
                                        style={"padding-right": "5px", "margin": "0px"},
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "<<",
                                                id="sidebar-toggle",
                                                n_clicks=0,
                                                className="btn-primary",
                                            ),
                                        ]
                                    ),
                                ],
                                # className="d-flex flex-row-reverse",
                                className="d-flex p-2",
                                style={"justify-content": "space-between"},
                            ),
                            dbc.Collapse(
                                dbc.CardBody(
                                    [
                                        sidebar,
                                    ],
                                ),
                                id="collapse-sidebar",
                                is_open=True,
                            ),
                        ]
                    ),
                    xs=12,
                    sm=12,
                    md=3,
                    lg=3,
                    xl=3,
                ),
                # Main Content with spaces between columns
                dbc.Col(
                    [
                        dash.page_container,  # This dynamically loads page content
                    ],
                    xs=12,
                    sm=12,
                    md=9,
                    lg=9,
                    xl=9,
                ),
            ],
            className="mt-3",
            style={"padding": "8px 8px 8px 8px"},
        ),
        # Footer
        dbc.Row([footer]),
        dcc.Store(id="selected-filter-values"),  # Store to hold dropdown values
    ],
)


# Callbacks
@app.callback(
    Output("collapse-sidebar", "is_open"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("collapse-sidebar", "is_open")],
)
def toggle_sidebar(n, is_open):
    if n:
        return not is_open
    return is_open


# Callback to store dropdown values in dcc.Store
@app.callback(
    Output("selected-filter-values", "data"),  # Store the values in dcc.Store
    [
        Input(ids.STATE_DROPDOWN, "value"),
        Input(ids.LGA_DROPDOWN, "value"),
        Input(ids.WARD_DROPDOWN, "value"),
        Input(ids.FACILITY_DROPDOWN, "value"),
        Input(ids.DATE_PICKER_RANGE, "start_date"),  # Capture the start_date input
        Input(ids.DATE_PICKER_RANGE, "end_date"),  # Capture the end_date input
    ],
)
def store_selected_filters(state, lga, ward, facility, start_date, end_date):
    # Store all selected dropdown values and date range as a dictionary
    return {
        "state": state,
        "lga": lga,
        "ward": ward,
        "facility": facility,
        "date": {"start_date": start_date, "end_date": end_date},  # Store date range
    }


# Register callbacks for each page
human_resources.register_callbacks(app)
visitation.register_callbacks(app)
attendance.register_callbacks(app)


if __name__ == "__main__":
    app.run_server(debug=True)
