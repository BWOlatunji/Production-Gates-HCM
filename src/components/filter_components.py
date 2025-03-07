import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import datetime
import pandas as pd
from . import ids


today = datetime.date.today()
start_date = "2023-01-01"
end_date = today


def create_location_dropdowns(app, states_df, lgas_df, wards_df, facilities_df):
    # Create the filter controls row
    location_dropdowns = html.Div(
        style={"display": "flex", "flex-direction": "column", "gap": "12px"},
       children = [
            html.Div(
                dcc.Dropdown(
                    id=ids.STATE_DROPDOWN,  # Using id constant here
                    options=[
                        {"label": state, "value": state}
                        for state in states_df["state_name"].unique()
                    ],
                    placeholder="Select State",
                    className="dropdown",
                ),
            ),
            html.Div(
                dcc.Dropdown(
                    id=ids.LGA_DROPDOWN,  # Using id constant here
                    placeholder="Select LGA",
                    className="dropdown",
                ),
            ),
            html.Div(
                dcc.Dropdown(
                    id=ids.WARD_DROPDOWN,  # Using id constant here
                    placeholder="Select Ward",
                    className="dropdown",
                ),
            ),
            html.Div(
                dcc.Dropdown(
                    id=ids.FACILITY_DROPDOWN,  # Add constant for facility dropdown
                    placeholder="Select Facility",
                    multi=True,
                    style={"width": "100%"},
                    className="dropdown",
                ),
            ),
            html.Div(
                dcc.DatePickerRange(
                    id=ids.DATE_PICKER_RANGE,
                    start_date=start_date,
                    end_date=end_date,
                    display_format="YYYY-MM-DD",
                )
            ),
            dcc.Store(id="filtered_lgas"),  # In-memory cache for filtered LGAs
            dcc.Store(id="filtered_wards"),  # In-memory cache for filtered Wards
        ]
    )

    # Callback to update LGAs based on selected state
    @app.callback(
        [
            Output(ids.LGA_DROPDOWN, "options"),
            Output(ids.LGA_DROPDOWN, "value"),
            Output("filtered_lgas", "data"),
        ],
        Input(ids.STATE_DROPDOWN, "value"),
    )
    def update_lga_options(selected_state):
        try:
            if selected_state:
                # Cache the filtered LGAs in memory
                state_id = states_df.loc[
                    states_df["state_name"] == selected_state, "state_id"
                ].values[0]
                lgas_in_state = lgas_df[lgas_df["state_id"] == state_id]
                lga_options = [
                    {"label": lga, "value": lga}
                    for lga in lgas_in_state["lga_name"].unique()
                ]
                return lga_options, None, lgas_in_state.to_dict("records")
        except IndexError:
            return [], None, None  # Handle case where state_id doesn't exist

        return [], None, None  # Return empty if no state selected

    # Callback to update Wards based on selected LGA
    @app.callback(
        [
            Output(ids.WARD_DROPDOWN, "options"),
            Output(ids.WARD_DROPDOWN, "value"),
            Output("filtered_wards", "data"),
        ],
        Input(ids.LGA_DROPDOWN, "value"),
        State("filtered_lgas", "data"),  # Use cached LGAs
    )
    def update_ward_options(selected_lga, filtered_lgas):
        try:
            if selected_lga and filtered_lgas:
                lgas_in_state = pd.DataFrame(filtered_lgas)  # Retrieve cached LGAs
                lga_id = lgas_in_state.loc[
                    lgas_in_state["lga_name"] == selected_lga, "lga_id"
                ].values[0]
                wards_in_lga = wards_df[wards_df["lga_id"] == lga_id]
                ward_options = [
                    {"label": ward, "value": ward}
                    for ward in wards_in_lga["ward_name"].unique()
                ]
                return ward_options, None, wards_in_lga.to_dict("records")
        except IndexError:
            return [], None, None  # Handle case where lga_id doesn't exist

        return [], None, None  # Return empty if no LGA selected

    # Callback to update Facilities based on selected Ward
    @app.callback(
        [
            Output(ids.FACILITY_DROPDOWN, "options"),
            Output(ids.FACILITY_DROPDOWN, "value"),
        ],
        Input(ids.WARD_DROPDOWN, "value"),
        State("filtered_wards", "data"),  # Use cached Wards
    )
    def update_facility_options(selected_ward, filtered_wards):
        try:
            if selected_ward and filtered_wards:
                wards_in_lga = pd.DataFrame(filtered_wards)  # Retrieve cached Wards
                ward_id = wards_in_lga.loc[
                    wards_in_lga["ward_name"] == selected_ward, "ward_id"
                ].values[0]
                facilities_in_ward = facilities_df[facilities_df["ward_id"] == ward_id]
                facility_options = [
                    {"label": facility, "value": facility}
                    for facility in facilities_in_ward["facility_name"].unique()
                ]
                return facility_options, None
        except IndexError:
            return [], None  # Handle case where ward_id doesn't exist

        return [], None  # Return empty if no Ward selected

    # 🏽 **Date Picker Range callback**
    @app.callback(
        [
            Output(ids.DATE_PICKER_RANGE, "start_date"),
            Output(ids.DATE_PICKER_RANGE, "end_date"),
        ],
        [
            Input(ids.DATE_PICKER_RANGE, "start_date"),
            Input(ids.DATE_PICKER_RANGE, "end_date"),
        ],
    )
    def update_date_picker_range(selected_start_date, selected_end_date):
        # Return the selected start and end dates
        return selected_start_date, selected_end_date

    # Return the row containing the filters
    return location_dropdowns
