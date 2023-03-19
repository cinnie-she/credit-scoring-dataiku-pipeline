import dataiku
import pandas as pd
import numpy as np
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# Get data from dataiku
dataset = dataiku.Dataset("credit_risk_dataset_generated")
df = dataset.get_dataframe()

# shared storage


def SharedDataStorage():
    return html.Div(
        [
            dcc.Store(id="bins_settings"),
            dcc.Store(id="good_bad_def"),
            dcc.Store(id="binned_df"),
            dcc.Store(id="numerical_columns"),
            dcc.Store(id="categorical_columns"),
        ]
    )


###########################################################################
##################### Prepare Stylings Constants Here ####################
###########################################################################

colors = {
    "navbar-background": "#000055",
    "navbar-text": "#ffffff",
}

font_size = {
    "navbar": 16,
    "heading": 24,
    "section-heading": 18,
}

dimens = {
    "navbar-padding": 15,
    "navbar-background-padding": 12,
    "page-bottom-margin": 100,
    "heading-margin": 30,
    "table-column-width": 250,
    "panel-border-radius": 5,
}


###########################################################################
########################## Prepare Stylings Here ##########################
###########################################################################

# Navigation bar
navbar_container_style = {
    "backgroundColor": colors["navbar-background"],
    "padding": dimens["navbar-background-padding"],
    "paddingLeft": 0,
}
navbar_item_style = {
    "backgroundColor": colors["navbar-background"],
    "color": colors["navbar-text"],
    "padding": dimens["navbar-padding"],
    "textDecoration": "none",
    "fontSize": font_size["navbar"],
}

navbar_home_item_style = navbar_item_style.copy()
navbar_home_item_style["fontWeight"] = "bold"
navbar_home_item_style["fontSize"] = 18

# Heading
heading_style = {
    "fontSize": font_size["heading"],
    "fontWeight": "bold",
    "marginTop": dimens["heading-margin"],
    "textDecoration": "underline",
}

# Section Heading
section_heading_style = {
    "fontSize": font_size["section-heading"],
}
section_heading_inline_style = {
    "fontSize": font_size["section-heading"],
    "display": "inline",
}

# Good/Bad Definition Page
purple_panel_style = {
    "float": "left",
    "width": "30%",
    "backgroundColor": "#BCBCDA",
    "padding": "2%",
    "borderRadius": dimens["panel-border-radius"],
}
grey_panel_style = {
    "float": "left",
    "width": "60%",
    "padding": "2%",
    "marginLeft": "2%",
    "borderRadius": dimens["panel-border-radius"],
    "backgroundColor": "#DDDDDD",
}
white_panel_style = {
    "float": "left",
    "width": "58%",
    "padding": "2%",
    "marginRight": "2%",
    "borderRadius": dimens["panel-border-radius"],
    "border": "2px #DDDDDD solid",
    "backgroundColor": "#FFFFFF",
}
grey_full_width_panel_style = {
    "width": "96%",
    "padding": "2%",
    "borderRadius": dimens["panel-border-radius"],
    "backgroundColor": "#DDDDDD",
}
green_full_width_panel_style = {
    "width": "96%",
    "padding": "2%",
    "borderRadius": dimens["panel-border-radius"],
    "backgroundColor": "#C7DDB5",
}

###########################################################################
######################### Prepare Components Here #########################
###########################################################################


def NavBar():
    return html.Div(
        children=[
            dcc.Link("Home", href="home-page", style=navbar_home_item_style),
            dcc.Link(
                "Confirm Input Dataset",
                href="confirm-input-dataset-page",
                style=navbar_item_style,
            ),
            dcc.Link(
                "Good/Bad Definition", href="good-bad-def-page", style=navbar_item_style
            ),
            dcc.Link("Interactive Binning", href="ib-page",
                     style=navbar_item_style),
            dcc.Link(
                "Preview & Download Settings",
                href="preview-download-page",
                style=navbar_item_style,
            ),
        ],
        style=navbar_container_style,
    )


def Heading(title):
    return html.H1(title, style=heading_style)


def SectionHeading(title, inline=False):
    if inline == True:
        return html.H2(
            title,
            style=section_heading_inline_style,
        )
    else:
        return html.H2(
            title,
            style=section_heading_style,
        )


def DataTable(df, id=""):
    return dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={
            "minWidth": dimens["table-column-width"],
            "width": dimens["table-column-width"],
            "maxWidth": dimens["table-column-width"],
        },
        sort_action="native",
        filter_action="native",
        css=[{"selector": ".show-hide", "rule": "display: none"}],
        id=id,
    )


def PredictorTypeListItem(var_name):
    return html.Div(
        [
            html.P(var_name, style={}),
            dcc.Dropdown(
                options=convert_column_list_to_dropdown_options(
                    ["numerical", "categorical"]
                ),
                value="numerical",
                clearable=False,
                searchable=False,
                style={"width": 150, "paddingLeft": 15},
            ),
        ],
        style={"display": "flex", "alignItems": "center", "margin": 8},
    )


def SaveButton(title, marginLeft=0, marginTop=0, id="", backgroundColor="#6668A9"):
    return html.Button(
        title,
        style={
            "marginLeft": marginLeft,
            "marginTop": marginTop,
            "backgroundColor": backgroundColor,
            "color": "#ffffff",
            "textTransform": "none",
        },
        id=id,
    )


def GoodBadDefNumericalListItem(var_list, idx=1, lower=0, upper=1):
    return html.Div(
        [
            html.P(str(idx) + ".", style={"float": "left", "marginRight": 5}),
            dcc.Dropdown(
                options=convert_column_list_to_dropdown_options(var_list),
                value=var_list[0],
                clearable=False,
                searchable=False,
                style={"width": 180},
            ),
            html.P(
                " :", style={"float": "left", "marginLeft": 5, "fontWeight": "bold"}
            ),
            dcc.Input(
                type="number",
                min=0,
                value=lower,
                id="",
                style={"width": 150, "float": "left", "marginLeft": 20},
            ),
            html.P(
                "(inclusive)",
                style={"float": "left", "marginLeft": 5, "marginBottom": 0},
            ),
            html.P(
                "一", style={"float": "left", "marginLeft": 10, "fontWeight": "bold"}
            ),
            dcc.Input(
                type="number",
                min=0,
                value=upper,
                id="",
                style={"width": 150, "float": "left", "marginLeft": 10},
            ),
            html.P(
                "(exclusive)  ",
                style={"float": "left", "marginLeft": 5, "marginBottom": 0},
            ),
            SaveButton("Remove", marginLeft=20, id={
                       'type': 'bad_numeric_def_rm_button', 'index': idx}),
        ],
        style={"display": "flex", "alignItems": "flex-end", "marginTop": 10},
    )


def GoodBadDefCategoricalListItem(var_list, idx=1, value=[]):
    return html.Div(
        [
            html.P(str(idx) + ".", style={"float": "left", "marginRight": 5}),
            dcc.Dropdown(
                options=convert_column_list_to_dropdown_options(var_list),
                value=var_list[0],
                clearable=False,
                searchable=False,
                style={"width": 180},
            ),
            html.P(
                " :", style={"float": "left", "marginLeft": 5, "fontWeight": "bold"}
            ),
            dcc.Dropdown(
                options=convert_column_list_to_dropdown_options(
                    value
                ),
                value=value,
                multi=True,
                style={"width": 500, "marginLeft": 10},
            ),
            SaveButton("Remove", marginLeft=20),
        ],
        style={"display": "flex", "alignItems": "flex-end", "marginTop": 10},
    )


###########################################################################
############################ Prepare Data Here ############################
###########################################################################
"""
Confirm Input Dataset Page
"""


def convert_column_list_to_dropdown_options(columns):
    options = list()
    for column_name in columns:
        options.append({"label": column_name, "value": column_name})
    return options


def generate_predictor_type_list(var_name_list):
    predictor_type_item_list = list()
    for var_name in var_name_list:
        predictor_type_item_list.append(PredictorTypeListItem(var_name))
    return predictor_type_item_list


"""
Good/Bad Definition Page
"""
# A class for validating user inputs for good bad definitions


class GoodBadDefValidator:
    # A method to validate if numerical definitions for bad/indeterminate has overlapped
    def validateIfNumericalDefOverlapped():
        return True
    # A method to validate if categorical definitions for bad/indeterminate has overlapped

    def validateIfCategoricalDefOverlapped():
        return True
    # A method to validate if all numerical definition range have upper bound > lower bound, if not, returns false

    def validateNumericalBounds(numeric_info_list):
        for numeric_info in numeric_info_list:
            a_range = [numeric_info["props"]["children"][3]['props']['value'],
                       numeric_info["props"]["children"][6]['props']['value']]
            if a_range[1] <= a_range[0]:
                return False
        return True


# A class for obtaining user inputs from the section UI info
class GoodBadDefDecoder:
    # A method to translate section UI info to a list of numerical definition
    def getNumericDefListFromSection(self, numeric_info_list):
        numeric_list = list()  # initialization

        for numeric_info in numeric_info_list:
            single_def_dict = dict()
            column = numeric_info["props"]["children"][1]['props']['value']
            a_range = [numeric_info["props"]["children"][3]['props']['value'],
                       numeric_info["props"]["children"][6]['props']['value']]
            # The 2 bounds are valid, now check if any overlapping with previously saved data
            has_column_overlap = False
            for def_idx, saved_def in enumerate(numeric_list):
                if saved_def["column"] == column:
                    has_column_overlap = True
                    has_range_overlap = False
                    # Merge range to element list
                    for def_range_idx, def_range in enumerate(saved_def["ranges"]):
                        if a_range[0] <= def_range[0] and a_range[1] >= def_range[1]:
                            has_range_overlap = True
                            numeric_list[def_idx]["ranges"][def_range_idx] = [
                                a_range[0], a_range[1]]
                            break
                        elif a_range[0] <= def_range[0] and a_range[1] >= def_range[0] and a_range[1] <= def_range[1]:
                            has_range_overlap = True
                            numeric_list[def_idx]["ranges"][def_range_idx] = [
                                a_range[0], def_range[1]]
                            break
                        elif a_range[0] >= def_range[0] and a_range[0] <= def_range[1] and a_range[1] >= def_range[1]:
                            has_range_overlap = True
                            numeric_list[def_idx]["ranges"][def_range_idx] = [
                                def_range[0], a_range[1]]
                            break
                    if has_range_overlap == False:
                        numeric_list[def_idx]["ranges"].append(a_range)
                    break
            if has_column_overlap == False:
                single_def_dict["column"] = column
                single_def_dict["ranges"] = [a_range]
                numeric_list.append(single_def_dict)
        return numeric_list
    # A method to translate section UI info to a list of categorical definition

    def getCategoricalDefListFromSection(self, section):
        categoric_info_list = section[0]['props']['children'][4]['props']['children']
        categoric_list = list()  # initialization
        for categoric_info in categoric_info_list:
            single_def_dict = dict()
            column = categoric_info["props"]["children"][1]['props']['value']
            elements = categoric_info["props"]["children"][3]['props']['value']
            # Check if any overlapping with previously saved data
            has_overlap = False
            for saved_def in categoric_list:
                if saved_def["column"] == column:
                    has_overlap = True
                    # Append element to elements list if it is not existed yet
                    for element in elements:
                        if element not in saved_def["elements"]:
                            saved_def["elements"].append(element)
                    break
            if has_overlap == False:
                single_def_dict["column"] = column
                single_def_dict["elements"] = elements
                categoric_list.append(single_def_dict)
        return categoric_list


"""
Interactive Binning Page
"""


###########################################################################
######################### Setup Page Layouts Here #########################
###########################################################################


home_page_layout = html.Div(
    [
        NavBar(),
        Heading("Input Dataset"),
        html.P("Number of rows: " + str(df.shape[0])),
        html.P("Number of columns: " +
               str(df.shape[1]), style={"marginBottom": 30}),
        DataTable(df=df),
    ]
)


confirm_input_dataset_page_layout = html.Div(
    [
        NavBar(),
        Heading("Confirm Your Input Dataset"),
        html.Div(
            [
                SectionHeading("I. Select the columns you would like to bin:"),
                dcc.Dropdown(
                    options=convert_column_list_to_dropdown_options(
                        df.columns.to_list()
                    ),
                    value=df.columns.to_list(),
                    multi=True,
                    style={"marginBottom": 30},
                    id="predictor_var_dropdown",
                ),
            ],
            style={"marginTop": dimens["heading-margin"]},
        ),
        html.Div(
            [
                SectionHeading("II. Preview your dataset here:"),
                DataTable(
                    df=df,
                    id="input_dataset_preview_table",
                ),
            ]
        ),
        html.Div(
            [
                SectionHeading(
                    "III. Confirm the predictor type of the columns:"),
                html.Div(
                    id="select_predictor_type_list",
                ),
            ],
            style={"marginTop": 60},
        ),
        html.Div(
            [
                SectionHeading(
                    "IV. Save & Confirm your settings:", inline=True),
                SaveButton(
                    title="Save & Confirm Settings",
                    marginLeft=15,
                    id="confirm_predictor_var_button",
                ),
            ],
            style={
                "marginTop": 50,
                "clear": "left",
            },
        ),
        html.P("", id="confirm_input_dataset_error_msg",
               style={"color": "red", "marginTop": 10}),
        html.Div([], style={"height": 100}),
        html.P(id="text_bins_settings"),
        html.P(id="text_numerical_columns"),
        html.P(id="text_categorical_columns"),
    ]
)


good_bad_def_page_layout = html.Div(
    [
        NavBar(),
        Heading("Define Good & Bad Definitions"),
        # Define Bad Definition
        SectionHeading("I. Define Bad Definition"),
        html.Div(
            [
                html.Ul(
                    [
                        html.Li("Numerical Variables", style={"fontSize": 16}),
                        html.Ol(
                            [],
                            style={"listStyleType": "lower-roman",
                                   "fontSize": 16},
                            id="bad_numeric_def_list",
                        ),
                        SaveButton(
                            "Add",
                            marginTop=0,
                            marginLeft=30,
                            id="add_bad_numeric_def_button",
                        ),
                        html.Li(
                            "Categorical Variables",
                            style={"fontSize": 16, "marginTop": 15},
                        ),
                        html.Ol(
                            [],
                            style={"listStyleType": "lower-roman",
                                   "fontSize": 16},
                            id="bad_categoric_def_list",
                        ),
                        SaveButton(
                            "Add",
                            marginTop=0,
                            marginLeft=30,
                            id="add_bad_categoric_def_button",
                        ),
                    ],
                    style={"listStyleType": "disc"},
                ),
                html.Div(
                    [
                        html.P(
                            "Weight of bad", style={"float": "left", "marginRight": 10}
                        ),
                        dcc.Input(
                            type="number", min=0, value=1, id="weight_of_bad_input"
                        ),
                    ],
                    style={
                        "marginTop": 15,
                        "display": "flex",
                        "alignItems": "flex-end",
                    },
                ),
            ],
            style={"marginLeft": 10},
            id="define_bad_def_section",
        ),
        html.Div([], style={"height": 50}),
        # Define Indeterminate Definition
        SectionHeading("II. Define Indeterminate Definition"),
        html.Div(
            [
                html.Ul(
                    [
                        html.Li("Numerical Variables", style={"fontSize": 16}),
                        html.Ol(
                            [],
                            style={"listStyleType": "lower-roman",
                                   "fontSize": 16},
                            id="indeterminate_numeric_def_list",
                        ),
                        SaveButton(
                            "Add",
                            marginTop=0,
                            marginLeft=30,
                            id="add_indeterminate_numeric_def_button",
                        ),
                        html.Li(
                            "Categorical Variables",
                            style={"fontSize": 16, "marginTop": 15},
                        ),
                        html.Ol(
                            [],
                            style={"listStyleType": "lower-roman",
                                   "fontSize": 16},
                            id="indeterminate_categoric_def_list",
                        ),
                        SaveButton(
                            "Add",
                            marginTop=0,
                            marginLeft=30,
                            id="add_indeterminate_categoric_def_button",
                        ),
                    ],
                    style={"listStyleType": "disc"},
                ),
            ],
            style={"marginLeft": 10},
            id="define_indeterminate_def_section",
        ),
        html.Div([], style={"height": 50}),
        # Define Good Definition
        SectionHeading("III. Define Good Definition"),
        html.P(
            "Weight of good", style={"marginTop": 8, "float": "left", "marginRight": 10}
        ),
        dcc.Input(type="number", min=0, value=1, id="weight_of_good_input"),
        html.Div([], style={"height": 50}),
        # Confirm Definitions
        SectionHeading("IV. Confirm the Definitions: ", inline=True),
        SaveButton("Confirm", marginLeft=15, id="confirm_good_bad_def_button"),
        html.P("", id="good_bad_def_error_msg",
               style={"color": "red", "marginTop": 10}),
        html.Div([], style={"height": 50}),
        # Show Statistics
        html.Div([], id="good_bad_stat_section"),
        # Debug
        html.P("", id="test_good_bad_def"),
    ]
)


interactive_binning_page_layout = html.Div([
    NavBar(),
    Heading("Interactive Binning Interface"),
])


preview_download_page_layout = html.Div(
    [
        NavBar(),
        Heading("Preview & Download Bins Settings"),
    ]
)

###########################################################################
#################### Implement Callback Functions Here ####################
###########################################################################

"""
Confirm Input Dataset Page:
Hide columns in confirm input dataset page when user add/delete 
columns they would like to bin
"""


@app.callback(
    Output("input_dataset_preview_table", "hidden_columns"),
    Input("predictor_var_dropdown", "value"),
)
def hide_confirm_input_dataset_column_on_dropdown_change(predictor_var_dropdown_values):
    hide_columns = df.columns.to_list()
    hide_columns = [
        x for x in hide_columns if x not in predictor_var_dropdown_values]
    return hide_columns


"""
Confirm Input Dataset Page:
Generate a list of options for user to confirm the predictor type of the columns
whenever the user changes the columns selected to be bin in Section 1
"""


@app.callback(
    Output("select_predictor_type_list", "children"),
    Input("predictor_var_dropdown", "value"),
)
def update_confirm_predictor_type_list(predictor_var_dropdown_values):
    return generate_predictor_type_list(predictor_var_dropdown_values)


"""
Confirm Input Dataset Page:
When confirm button is clicked in confirm input dataset page, this function saves the initial bins 
settings to shared storage
"""


@app.callback(
    [
        Output("bins_settings", "data"),
        Output("numerical_columns", "data"),
        Output("categorical_columns", "data"),
    ],
    Input("confirm_predictor_var_button", "n_clicks"),
    [
        State("predictor_var_dropdown", "value"),
        State("select_predictor_type_list", "children"),
        State("bins_settings", "data"),
        State("numerical_columns", "data"),
        State("categorical_columns", "data"),
    ],
)
def save_initial_bin_settings_to_shared_storage(
    n_clicks, predictor_var_dropdown_values, predictor_type, original_bins_settings_data, original_numerical_col_data, original_categorical_col_data
):
    # Check if any non-numerical column marked as numerical, if yes, save the original data
    for i in range(len(predictor_type)):
        pred = predictor_var_dropdown_values[i]
        pred_var_type = predictor_type[i]["props"]["children"][1]["props"]["value"]
        # invalid user input, return original data
        if df[pred].dtype == "object" and pred_var_type == "numerical":
            return original_bins_settings_data, original_numerical_col_data, original_categorical_col_data

    bins_settings = {"variable": []}  # initialization
    numerical_columns = list()  # initialization
    categorical_columns = list()  # initialization

    # User input is valid, prepare data to save to storage
    for i in range(len(predictor_type)):
        pred = predictor_var_dropdown_values[i]
        pred_var_type = predictor_type[i]["props"]["children"][1]["props"]["value"]
        bins_settings["variable"].append(
            {
                "column": pred,
                "type": pred_var_type,
                "infoVal": -1,
                "bins": "none",
            }
        )
        if (pred_var_type == 'numerical'):
            numerical_columns.append(pred)
        else:
            categorical_columns.append(pred)

    return json.dumps(bins_settings), json.dumps(numerical_columns), json.dumps(categorical_columns)


"""
Confirm Input Dataset Page:
When user click on confirm button, if user input is invalid,
show error message
"""


@app.callback(
    Output("confirm_input_dataset_error_msg", "children"),
    Input("confirm_predictor_var_button", "n_clicks"),
    [
        State("predictor_var_dropdown", "value"),
        State("select_predictor_type_list", "children"),
    ],
)
def show_confirm_input_datset_error_msg(n_clicks, predictor_var_dropdown_values, predictor_type):
    # Check if any non-numerical column marked as numerical, if yes, save the original data
    for i in range(len(predictor_type)):
        pred = predictor_var_dropdown_values[i]
        pred_var_type = predictor_type[i]["props"]["children"][1]["props"]["value"]
        # invalid user input, return original data
        if df[pred].dtype == "object" and pred_var_type == "numerical":
            return "Error: some columns having categorical type is defined as numerical."
    return ""


"""
Good/Bad Definition Page:
Press add button to add a new definition row in bad numeric section
"""


@app.callback(
    Output("bad_numeric_def_list", "children"),
    Input("add_bad_numeric_def_button", "n_clicks"),
    [
        State("bad_numeric_def_list", "children"),
        State("numerical_columns", "data"),
    ],
)
def add_bad_numeric_section_row(n_clicks, def_list, numeric_col_data):
    new_idx = len(def_list)+1
    new_row = GoodBadDefNumericalListItem(
        var_list=json.loads(numeric_col_data), idx=new_idx)
    def_list.append(new_row)
    return def_list


"""
Good/Bad Definition Page:
Press add button to add a new definition row in bad categorical section
"""


@app.callback(
    Output("bad_categoric_def_list", "children"),
    Input("add_bad_categoric_def_button", "n_clicks"),
    [
        State("bad_categoric_def_list", "children"),
        State("categorical_columns", "data"),
    ]
)
def add_bad_categoric_section_row(n_clicks, def_list, categoric_col_data):
    new_idx = len(def_list)+1
    new_row = GoodBadDefCategoricalListItem(var_list=json.loads(
        categoric_col_data), idx=new_idx, value=["own", "rent", "mortgage"])
    def_list.append(new_row)
    return def_list


"""
Good/Bad Definition Page:
Press add button to add a new definition row in bad numeric section
"""


@app.callback(
    Output("indeterminate_numeric_def_list", "children"),
    Input("add_indeterminate_numeric_def_button", "n_clicks"),
    [
        State("indeterminate_numeric_def_list", "children"),
        State("numerical_columns", "data"),
    ],
)
def add_bad_numeric_section_row(n_clicks, def_list, numeric_col_data):
    new_idx = len(def_list)+1
    new_row = GoodBadDefNumericalListItem(
        var_list=json.loads(numeric_col_data), idx=new_idx)
    def_list.append(new_row)
    return def_list


"""
Good/Bad Definition Page:
Press add button to add a new definition row in indeterminate categorical section
"""


@app.callback(
    Output("indeterminate_categoric_def_list", "children"),
    Input("add_indeterminate_categoric_def_button", "n_clicks"),
    [
        State("indeterminate_categoric_def_list", "children"),
        State("categorical_columns", "data"),
    ]
)
def add_bad_categoric_section_row(n_clicks, def_list, categoric_col_data):
    new_idx = len(def_list)+1
    new_row = GoodBadDefCategoricalListItem(var_list=json.loads(
        categoric_col_data), idx=new_idx, value=["own", "rent", "mortgage"])
    def_list.append(new_row)
    return def_list


"""
Good/Bad Definition Page:
Press confirm button to save good bad defintiion to shared storage
"""


@app.callback(
    Output("good_bad_def", "data"),
    Input("confirm_good_bad_def_button", "n_clicks"),
    [
        State("define_bad_def_section", "children"),
        State("define_indeterminate_def_section", "children"),
        State("weight_of_bad_input", "value"),
        State("weight_of_good_input", "value"),
        State("good_bad_def", "data"),
    ],
)
def save_good_bad_def_to_shared_storage(n_clicks, bad_def_sec, indeterminate_def_sec, bad_weight, good_weight, original_def_data):
    # Validate user input, if invalid, return original definition
    bad_numeric_info_list = bad_def_sec[0]['props']['children'][1]['props']['children']
    indeterminate_numeric_info_list = indeterminate_def_sec[
        0]['props']['children'][1]['props']['children']
    if not GoodBadDefValidator.validateNumericalBounds(bad_numeric_info_list) or not GoodBadDefValidator.validateNumericalBounds(indeterminate_numeric_info_list):
        return original_def_data

    # User input is valid, prepare data and save to storage
    # Initialize the data
    good_bad_def = {
        "bad": {
            "numerical": [],
            "categorical": [],
            "weight": bad_weight,
        },
        "indeterminate": {
            "numerical": [],
            "categorical": [],
        },
        "good": {
            "weight": good_weight,
        }
    }
    decoder = GoodBadDefDecoder()
    # Update data
    good_bad_def["bad"]["numerical"] = decoder.getNumericDefListFromSection(
        numeric_info_list=bad_numeric_info_list)
    good_bad_def["indeterminate"]["numerical"] = decoder.getNumericDefListFromSection(
        numeric_info_list=indeterminate_numeric_info_list)
    good_bad_def["bad"]["categorical"] = decoder.getCategoricalDefListFromSection(
        section=bad_def_sec)
    good_bad_def["indeterminate"]["categorical"] = decoder.getCategoricalDefListFromSection(
        section=indeterminate_def_sec)

    return json.dumps(good_bad_def)


"""
Good/Bad Definition Page:
Show error message when:
(1) some upper bound < lower bound for bad & indeterminate numerical variables
(2) overlapping between numerical definitions for bad & indeterminate
(3) overlapping between categorical definitions for bad & indeterminate
"""


@app.callback(
    Output("good_bad_def_error_msg", "children"),
    Input("confirm_good_bad_def_button", "n_clicks"),
    [
        State("define_bad_def_section", "children"),
        State("define_indeterminate_def_section", "children"),
    ],
)
def show_good_bad_def_error_msg(n_clicks, bad_def_sec, indeterminate_def_sec):
    error_msg = ""

    bad_numeric_info_list = bad_def_sec[0]['props']['children'][1]['props']['children']
    indeterminate_numeric_info_list = indeterminate_def_sec[
        0]['props']['children'][1]['props']['children']
    if not GoodBadDefValidator.validateNumericalBounds(bad_numeric_info_list):
        error_msg += "Error: Some of the numerical range(s) for bad definition has lower bound >= upper bound which is invalid.\t"
    if not GoodBadDefValidator.validateNumericalBounds(indeterminate_numeric_info_list):
        error_msg += "Error: Some of the numerical range(s) for indeterminate definition has lower bound >= upper bound which is invalid.\t"

    return error_msg


"""
Good/Bad Definition Page:
Show statistics & bar chart to show total good/indeterminate/bad
in the whole dataset after the user clicked on the confirm button
"""

###########################################################################
############################ Debugging Purpose ############################
###########################################################################
# Get bins settings


@app.callback(
    Output("text_bins_settings", "children"),
    Input("bins_settings", "data"),
)
def update_bins_settings(data):
    adict = json.loads(data)
    alist = adict["variable"]
    return "bins settings = " + str(alist)

# Get numerical columns


@app.callback(
    Output("text_numerical_columns", "children"),
    Input("numerical_columns", "data"),
)
def update_numerical_columns(data):
    alist = json.loads(data)
    return "numerical columns = " + str(alist)

# Get categorical columns


@app.callback(
    Output("text_categorical_columns", "children"),
    Input("categorical_columns", "data"),
)
def update_categorical_columns(data):
    alist = json.loads(data)
    return "categorical columns = " + str(alist)

# Get good bad definition


@app.callback(
    Output("test_good_bad_def", "children"),
    Input("good_bad_def", "data"),
)
def update_good_bad_def_text(data):
    return "good bad def = " + str(json.loads(data))

###########################################################################
############ Not important for our development after this line ############
###########################################################################


"""
Setup web application layout & callbacks for navigation (can ignore this part)
"""
# base styling
app.config.external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css"]

# handle routing & page content
url_bar_and_content_div = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="root-url", style={"display": "none"}),
        html.Div(id="first-loading", style={"display": "none"}),
        html.Div(id="page-content"),
        SharedDataStorage(),
    ]
)

# index layout
app.layout = url_bar_and_content_div

# "complete" layout, need at least Dash 1.12
app.validation_layout = html.Div(
    [
        url_bar_and_content_div,
        NavBar(),
        home_page_layout,
        confirm_input_dataset_page_layout,
        good_bad_def_page_layout,
        interactive_binning_page_layout,
        preview_download_page_layout,
    ]
)

# The following callback is used to dynamically instantiate the root-url


@app.callback(
    [
        Output("root-url", "children"),
        Output("first-loading", "children"),
    ],
    Input("url", "pathname"),
    State("first-loading", "children"),
)
def update_root_url(pathname, first_loading):
    if first_loading is None:
        return pathname, True
    else:
        raise PreventUpdate


# This is the callback doing the routing
@app.callback(
    Output("page-content", "children"),
    [
        Input("root-url", "children"),
        Input("url", "pathname"),
    ],
)
def display_page(root_url, pathname):
    if root_url + "home-page" == pathname:
        return home_page_layout
    elif root_url + "confirm-input-dataset-page" == pathname:
        return confirm_input_dataset_page_layout
    elif root_url + "good-bad-def-page" == pathname:
        return good_bad_def_page_layout
    elif root_url + "ib-page" == pathname:
        return interactive_binning_page_layout
    elif root_url + "preview-download-page" == pathname:
        return preview_download_page_layout
    elif root_url == pathname:
        return home_page_layout
    else:
        return "404"
