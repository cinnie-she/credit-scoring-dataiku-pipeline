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
            dcc.Link("Interactive Binning", href="ib-page", style=navbar_item_style),
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
        },
        id=id,
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


# Get the predictor variables in a dataframe
def get_predictor_var_list(columns):
    predictor_var_list = columns
    if "loan_status" in predictor_var_list:
        predictor_var_list.remove("loan_status")
    if "paid_past_due" in predictor_var_list:
        predictor_var_list.remove("paid_past_due")
    return predictor_var_list


# Get the response variables in a dataframe
def get_response_var_list(columns):
    response_var_list = list()
    if "loan_status" in columns:
        response_var_list.append("loan_status")
    if "paid_past_due" in columns:
        response_var_list.append("paid_past_due")
    return response_var_list


def generate_predictor_type_list(var_name_list):
    predictor_type_item_list = list()
    for var_name in var_name_list:
        predictor_type_item_list.append(PredictorTypeListItem(var_name))
    return predictor_type_item_list


"""
Good/Bad Definition Page
"""


def get_count_loan_status_default():
    return len(df[df["loan_status"] == 1])


def get_count_loan_status_non_default():
    return len(df[df["loan_status"] == 0])


def get_count_paid_past_due_good(lower_bound):
    return len(df.loc[(df["paid_past_due"] < lower_bound) & (df["loan_status"] == 0)])


def get_count_paid_past_due_bad(upper_bound):
    return len(
        df.loc[(df["paid_past_due"] > upper_bound) & (df["loan_status"] == 0)]
    ) + len(df[df["loan_status"] == 1])


def get_count_paid_past_due_indeterminate(indeterminate_range):
    filtered_default_df = df[df["loan_status"] == 0]
    filtered_upper_df = filtered_default_df[
        filtered_default_df["paid_past_due"] < indeterminate_range[1]
    ]
    filtered_df = filtered_upper_df[
        filtered_upper_df["paid_past_due"] > indeterminate_range[0]
    ]
    return len(filtered_df)


def compute_dataset_total_good_bad(
    def_column, good_weight, bad_weight, indeterminate_range=[60, 90]
):
    if def_column == "loan_status":
        good_bad_count = [
            good_weight * get_count_loan_status_non_default(),
            bad_weight * get_count_loan_status_default(),
        ]  # [good, bad]
        return good_bad_count
    else:
        good_count = get_count_paid_past_due_good(indeterminate_range[0])
        bad_count = get_count_paid_past_due_bad(indeterminate_range[1])
        return [good_weight * good_count, bad_weight * bad_count]


def compute_default_weight_of_good(indeterminate_range):
    good_count = get_count_paid_past_due_good(indeterminate_range[0])
    indeterminate_count = get_count_paid_past_due_indeterminate(indeterminate_range)
    if good_count != 0:
        default_weight = (indeterminate_count + good_count) / good_count
        return round(default_weight, 2)
    else:
        return 1  # avoid division by zero error


"""
Interactive Binning Page
"""


def get_list_of_total_count(var_df, unique_bin_name_list, good_bad_def):
    total_count_list = list()
    for unique_bin_name in unique_bin_name_list:
        bin_df = var_df[var_df.iloc[:, 0] == unique_bin_name]
        if (
            good_bad_def == None
        ):  # If-else statement put outside for loop would be better
            total_count_list.append(len(bin_df))
        else:
            good_bad_def_dict = json.loads(good_bad_def)
            if good_bad_def_dict["column"] == "loan_status":
                good_count = good_bad_def_dict["weights"]["good"] * len(
                    bin_df[bin_df["loan_status"] == 0]
                )
                bad_count = good_bad_def_dict["weights"]["bad"] * len(
                    bin_df[bin_df["loan_status"] == 1]
                )
                total_count_list.append(good_count + bad_count)
            else:
                good_count = good_bad_def_dict["weights"]["good"] * len(
                    bin_df.loc[
                        (
                            bin_df["paid_past_due"]
                            < good_bad_def_dict["indeterminate"][0]
                        )
                        & (bin_df["loan_status"] == 0)
                    ]
                )
                bad_count = good_bad_def_dict["weights"]["bad"] * (
                    len(
                        bin_df.loc[
                            (
                                bin_df["paid_past_due"]
                                > good_bad_def_dict["indeterminate"][1]
                            )
                            & (bin_df["loan_status"] == 0)
                        ]
                    )
                    + len(bin_df[bin_df["loan_status"] == 1])
                )
                total_count_list.append(good_count + bad_count)
    return total_count_list


def get_list_of_bad_count(var_df, unique_bin_name_list, good_bad_def):
    bad_count_list = list()
    for unique_bin_name in unique_bin_name_list:
        bin_df = var_df[var_df.iloc[:, 0] == unique_bin_name]
        if good_bad_def == None:  # use 'loan_status'
            bad_count = len(bin_df[bin_df["loan_status"] == 1])
            bad_count_list.append(bad_count)
        else:
            good_bad_def_dict = json.loads(good_bad_def)
            if good_bad_def_dict["column"] == "loan_status":
                bad_count = good_bad_def_dict["weights"]["bad"] * len(
                    bin_df[bin_df["loan_status"] == 1]
                )
                bad_count_list.append(bad_count)
            else:
                bad_count = good_bad_def_dict["weights"]["bad"] * (
                    len(
                        bin_df.loc[
                            (
                                bin_df["paid_past_due"]
                                > good_bad_def_dict["indeterminate"][1]
                            )
                            & (bin_df["loan_status"] == 0)
                        ]
                    )
                    + len(bin_df[bin_df["loan_status"] == 1])
                )
                bad_count_list.append(bad_count)
    return bad_count_list


# def get_list_of_woe(total_count_list, bad_count_list):
#     woe_list = list()
#     for i in range(len(total_count_list)):
#         if total_count_list[i] == 0:
#             bad_pct = 0
#         else:
#             bad_pct = bad_count_list[i] / total_count_list[i]
#         good_pct = 1 - bad_pct
#         if bad_pct == 0:
#             woe_list.append(None)
#         else:
#             woe_list.append(np.log(good_pct / bad_pct))
#     return woe_list


import plotly.graph_objects as go
from plotly.subplots import make_subplots


def generate_mixed_chart_fig(
    var_df=df[[df.columns[0], "loan_status"]], clicked_bar_index=None, good_bad_def=None
):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    good_marker_color = ["#8097e6"] * (len(var_df.iloc[:, 0].unique().tolist()))
    if clicked_bar_index is not None:
        good_marker_color[clicked_bar_index] = "#3961ee"

    bad_marker_color = ["#8bd58b"] * (len(var_df.iloc[:, 0].unique().tolist()))
    if clicked_bar_index is not None:
        bad_marker_color[clicked_bar_index] = "#55a755"

    unique_bins = sorted(var_df.iloc[:, 0].unique().tolist())
    total_count_list = get_list_of_total_count(var_df, unique_bins, good_bad_def)
    bad_count_list = get_list_of_bad_count(
        var_df,
        unique_bins,
        good_bad_def,
    )

    fig.add_trace(
        go.Bar(
            x=unique_bins,
            y=total_count_list,
            name="Good",
            marker_color=good_marker_color,
            offsetgroup=0,
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Bar(
            x=unique_bins,
            y=bad_count_list,  # TODO: need sum good & bad multplied by weights instead
            name="Bad",
            marker_color=bad_marker_color,
            offsetgroup=0,
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            mode="lines+markers",
            x=unique_bins,
            y=bad_count_list,
            # y=get_list_of_woe(total_count_list, bad_count_list),
            name="WOE",
            marker_color="red",
        ),
        secondary_y=True,
    )

    fig.update_layout(
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
        ),
        margin=go.layout.Margin(l=0, r=0, b=0, t=0),
    )

    # Set x-axis title
    fig.update_xaxes(title_text="Bins")

    # Set y-axes titles
    fig.update_yaxes(title_text="Bin Frequency", secondary_y=False)
    fig.update_yaxes(title_text="WOE", secondary_y=True)

    return fig


"""
All
"""


def compute_binned_dataset(bins_settings_list):
    binned_df = df[df.columns.to_list()]

    for predictor_var_info in bins_settings_list:
        new_col_name = predictor_var_info["column"] + "_binned"
        if predictor_var_info["bins"] == "none":
            binned_df[new_col_name] = df[predictor_var_info["column"]]
        elif predictor_var_info["bins"] == "equal width":
            pass
            # binned_df[new_col_name] = generate_binned_col_with_equal_width_algo(predictor_var_info)
        elif predictor_var_info["bins"] == "equal frequency":
            pass
            # binned_df[new_col_name] = generate_binned_col_with_equal_frequency_algo(predictor_var_info)
        else:
            pass
            # binned_df[new_col_name] = generate_binned_col_with_custom_binning(predictor_var_info)

    return binned_df


###########################################################################
######################### Setup Page Layouts Here #########################
###########################################################################


home_page_layout = html.Div(
    [
        NavBar(),
        Heading("Input Dataset"),
        html.P("Number of rows: " + str(df.shape[0])),
        html.P("Number of columns: " + str(df.shape[1]), style={"marginBottom": 30}),
        DataTable(df=df),
    ]
)


confirm_input_dataset_page_layout = html.Div(
    [
        NavBar(),
        Heading("Confirm Your Input Dataset"),
        html.P(
            "The response variables found in your dataset includes: "
            + str(get_response_var_list(df.columns.to_list()))
        ),
        html.Div(
            [
                SectionHeading("I. Select the columns you would like to bin:"),
                dcc.Dropdown(
                    options=convert_column_list_to_dropdown_options(
                        get_predictor_var_list(df.columns.to_list())
                    ),
                    value=get_predictor_var_list(df.columns.to_list()),
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
                    df=df[get_predictor_var_list(df.columns.to_list())],
                    id="input_dataset_preview_table",
                ),
            ]
        ),
        html.Div(
            [
                SectionHeading("III. Confirm the predictor type of the columns:"),
                html.Div(
                    generate_predictor_type_list(df.columns.to_list()),
                    id="select_predictor_type_list",
                ),
            ],
            style={"marginTop": 60},
        ),
        html.Div(
            [
                SectionHeading("IV. Save & Confirm your settings:", inline=True),
                SaveButton(
                    title="Save & Confirm Settings",
                    marginLeft=15,
                    id="confirm_predictor_var_button",
                ),
            ],
            style={
                "marginTop": 50,
                "marginBottom": dimens["page-bottom-margin"],
                "clear": "left",
            },
        ),
        html.P(id="text"),
    ]
)


good_bad_def_page_layout = html.Div(
    [
        NavBar(),
        Heading("Define Good & Bad Definitions"),
        html.Div(
            [
                html.Div(
                    [
                        SectionHeading("I. Provide your good & bad definitions"),
                        dcc.Dropdown(
                            options=convert_column_list_to_dropdown_options(
                                get_response_var_list(df.columns.to_list())
                            ),
                            value="loan_status",
                            clearable=False,
                            searchable=False,
                            style={"marginBottom": 30},
                            id="good_bad_def_dropdown",
                        ),
                        html.P("Weight of good"),
                        dcc.Input(
                            type="number", min=0, value=1, id="weight_of_good_input"
                        ),
                        html.P("Weight of bad", style={"marginTop": 8}),
                        dcc.Input(
                            type="number", min=0, value=1, id="weight_of_bad_input"
                        ),
                        html.Div(
                            [
                                html.P(
                                    "Select the range of indeterminate samples:",
                                    style={"marginTop": 40},
                                ),
                                dcc.RangeSlider(
                                    min=0,
                                    max=120,
                                    step=1,
                                    value=[60, 90],
                                    marks={
                                        i: "{}".format(i) for i in range(0, 121, 10)
                                    },
                                    tooltip={"placement": "bottom"},
                                    id="indeterminate_range_slider",
                                ),
                            ],
                            id="select_indeterminate_range_section",
                            style={"display": "none"},
                        ),
                        SaveButton(
                            title="Save & Confirm Definitions",
                            marginTop=55,
                            id="confirm_good_bad_def_button",
                        ),
                    ],
                    style=purple_panel_style,
                ),
                html.Div(
                    [
                        SectionHeading(
                            "II. Preview the good & bad distribution of your dataset",
                        ),
                        dcc.Graph(
                            figure={
                                "data": [
                                    {
                                        "x": ["Good", "Bad"],
                                        "y": [
                                            get_count_loan_status_non_default(),
                                            get_count_loan_status_default(),
                                        ],
                                        "type": "bar",
                                        "marker": {"color": "#6B87AB"},
                                    },
                                ],
                                "layout": {"title": "Good & Bad Count"},
                            },
                            id="dataset_total_good_bad_histogram",
                        ),
                    ],
                    style=grey_panel_style,
                ),
            ],
            style={"overflow": "hidden", "marginBottom": dimens["page-bottom-margin"]},
        ),
        html.P(id="text3"),
    ]
)


interactive_binning_page_layout = html.Div(
    [
        NavBar(),
        Heading("Interactive Binning Interface"),
        html.P(id="text_omg"),
        html.Div(
            [
                html.Div(
                    [
                        SectionHeading("I. Select a predictor variable to bin"),
                        dcc.Dropdown(
                            options=convert_column_list_to_dropdown_options(
                                get_predictor_var_list(df.columns.to_list())
                            ),
                            value=df.columns.to_list()[0],
                            style={"marginBottom": 30},
                            clearable=False,
                            searchable=False,
                            id="predictor_var_ib_dropdown",
                        ),
                    ],
                    style=purple_panel_style,
                ),
                html.Div(
                    [
                        SectionHeading(
                            "II. Select the automated binning algorithm for initial binning"
                        ),
                        dcc.Dropdown(
                            options=[
                                {"label": "No Binnings", "value": "none"},
                                {"label": "Equal Width", "value": "equal width"},
                                {
                                    "label": "Equal Frequency",
                                    "value": "equal frequency",
                                },
                                {
                                    "label": "Import Settings",
                                    "value": "import settings",
                                },
                            ],
                            value="none",
                            clearable=False,
                            searchable=False,
                            style={"marginBottom": 20, "width": "60%"},
                            id="auto_bin_algo_dropdown",
                        ),
                        html.Div(
                            children=[
                                dcc.RadioItems(
                                    options=[
                                        {"label": "Width", "value": "width"},
                                        {
                                            "label": "Number of Bins",
                                            "value": "number of bins",
                                        },
                                    ],
                                    value="width",
                                    inline=True,
                                    id="equal_width_radio_button",
                                ),
                                html.Div([], style={"height": 25}),
                                html.Div(
                                    [
                                        html.Div(
                                            [],
                                            style={
                                                "display": "inline",
                                                "marginLeft": 5,
                                            },
                                        ),
                                        html.P("Width:", style={"display": "inline"}),
                                        dcc.Input(
                                            type="number",
                                            value=1,
                                            min=1,
                                            style={"marginLeft": 10},
                                        ),
                                    ],
                                    id="equal_width_width_input_section",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [],
                                            style={
                                                "display": "inline",
                                                "marginLeft": 5,
                                            },
                                        ),
                                        html.P(
                                            "Number of Bins:",
                                            style={"display": "inline"},
                                        ),
                                        dcc.Input(
                                            type="number",
                                            value=10,
                                            min=1,
                                            style={"marginLeft": 10},
                                        ),
                                    ],
                                    id="equal_width_num_bin_input_section",
                                    style={"display": "none"},
                                ),
                            ],
                            id="equal_width_input_section",
                            style={"display": "none"},
                        ),
                        html.Div(
                            children=[
                                dcc.RadioItems(
                                    options=[
                                        {"label": "Frequency", "value": "frequency"},
                                        {
                                            "label": "Number of Bins",
                                            "value": "number of bins",
                                        },
                                    ],
                                    value="frequency",
                                    inline=True,
                                    id="equal_freq_radio_button",
                                ),
                                html.Div([], style={"height": 25}),
                                html.Div(
                                    [
                                        html.Div(
                                            [],
                                            style={
                                                "display": "inline",
                                                "marginLeft": 5,
                                            },
                                        ),
                                        html.P(
                                            "Frequency:", style={"display": "inline"}
                                        ),
                                        dcc.Input(
                                            type="number",
                                            value=1000,
                                            min=1,
                                            style={"marginLeft": 10},
                                        ),
                                    ],
                                    id="equal_freq_freq_input_section",
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [],
                                            style={
                                                "display": "inline",
                                                "marginLeft": 5,
                                            },
                                        ),
                                        html.P(
                                            "Number of Bins:",
                                            style={"display": "inline"},
                                        ),
                                        dcc.Input(
                                            type="number",
                                            value=10,
                                            min=1,
                                            style={"marginLeft": 10},
                                        ),
                                    ],
                                    id="equal_freq_num_bin_input_section",
                                    style={"display": "none"},
                                ),
                            ],
                            id="equal_frequency_input_section",
                            style={"display": "none"},
                        ),
                        html.Div(
                            children=[
                                html.Div(
                                    [], style={"display": "inline", "marginLeft": 5}
                                ),
                                html.P("Upload a file: ", style={"display": "inline"}),
                                SaveButton(
                                    "Upload", marginLeft=10, backgroundColor="#8097e6"
                                ),
                            ],
                            id="import_settings_input_section",
                            style={"display": "none"},
                        ),
                        html.Div([], style={"marginBottom": 25}),
                        SaveButton("Refresh"),
                        html.P(
                            style={"marginTop": 20},
                            id="auto_bin_algo_description",
                        ),
                    ],
                    style=grey_panel_style,
                ),
            ]
        ),
        html.Div([], style={"width": "100%", "height": 25, "clear": "left"}),
        html.Div(
            [
                html.Div(
                    [
                        SectionHeading("III. Perform Interactive Binning"),
                        dcc.Graph(
                            figure=generate_mixed_chart_fig(),
                            id="mixed_chart",
                        ),
                    ],
                    style=white_panel_style,
                ),
                html.Div(
                    [
                        # html.P("Split/Add bin: Click on the bar representing the bin you would like to split > choose the split point > click the 'split' button"),
                        # html.P("Remove bin: Click on the bar representing the bin you would like to remove > click on 'Remove' button"),
                        # html.P("Adjust bin boundaries: Click on the bar to be adjusted > adjust through slider > click on 'Adjust' button"),
                        html.P("Bin Name: ", id="selected_bin_name"),
                        html.P("Bin Index: ", id="selected_bin_index"),
                        html.P("Bin Count: ", id="selected_bin_count"),
                        html.Div(
                            [],
                            style={
                                "width": "100%",
                                "height": 0,
                                "border": "1px solid black",
                            },
                        ),
                        SectionHeading("Rename Selected Bin"),
                        SaveButton(title="Rename"),
                        SectionHeading("Split Selected Bin"),
                        SaveButton(title="Split"),
                        SectionHeading("Merge Selected Bins"),
                        SaveButton(title="Merge"),
                        SectionHeading("Remove Selected Bin(s)"),
                        SaveButton(title="Remove"),
                    ],
                    style=purple_panel_style,
                ),
            ]
        ),
        html.Div([], style={"width": "100%", "height": 25, "clear": "left"}),
        html.Div(
            [
                SectionHeading("IV. Monitor Bins Performance (Before)"),
            ],
            style=grey_full_width_panel_style,
        ),
        html.Div([], style={"width": "100%", "height": 25, "clear": "left"}),
        html.Div(
            [
                SectionHeading("V. Monitor Bins Performance (After)"),
            ],
            style=green_full_width_panel_style,
        ),
        SectionHeading(
            "VI. Save & Confirm Your Bins Settings for the Chosen Predictor Variable:",
            inline=True,
        ),
        SaveButton(
            title="Save & Confirm Interactive Binning",
            marginLeft=15,
            marginTop=55,
            id="confirm_ib_button",
        ),
        html.Div(style={"height": 100}),
    ]
)


preview_download_page_layout = html.Div(
    [
        NavBar(),
        Heading("Preview & Download Bins Settings"),
        SectionHeading("I. Preview Output Dataset"),
        DataTable(df, id="preview_binned_df"),
        html.Div(style={"height": 25}),
        SectionHeading("II. Preview Summary Statistics Table"),
        html.P("TBC"),
        html.Div(style={"height": 25}),
        SectionHeading("III. Preview Mixed Chart"),
        html.P("TBC"),
        html.Div(style={"height": 25}),
        SectionHeading("IV. Download Bins Settings", inline=True),
        SaveButton(
            title="Download Bins Settings:",
            marginLeft=15,
            id="download_bin_settings_button",
        ),
        dcc.Download(id="download_json"),
        html.Div(style={"height": 25}),
        html.P(
            "After downloading, import the json file into the Dataiku project... XXX"
        ),
        html.Div(style={"height": 100}),
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
    hide_columns = get_predictor_var_list(df.columns.to_list())
    hide_columns = [x for x in hide_columns if x not in predictor_var_dropdown_values]
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
    Output("bins_settings", "data"),
    Input("confirm_predictor_var_button", "n_clicks"),
    [
        State("predictor_var_dropdown", "value"),
        State("select_predictor_type_list", "children"),
    ],
)
def save_initial_bin_settings_to_shared_storage(
    n_clicks, predictor_var_dropdown_values, predictor_type
):
    bins_settings = {"variable": []}  # initialization
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
    return json.dumps(bins_settings)


"""
Good/Bad Definition Page:
When the confirm button is clicked in good/bad definition page, this function saves 
the definitions defined by the users in json format to the shared storage
"""


@app.callback(
    Output("good_bad_def", "data"),
    Input("confirm_good_bad_def_button", "n_clicks"),
    [
        State("good_bad_def_dropdown", "value"),
        State("weight_of_good_input", "value"),
        State("weight_of_bad_input", "value"),
        State("indeterminate_range_slider", "value"),
    ],
)
def save_good_bad_definition_to_shared_storage(
    n_clicks, def_column, good_weight, bad_weight, indeterminate_range
):
    good_bad_def = {
        "column": def_column,
        "weights": {"good": good_weight, "bad": bad_weight},
        "indeterminate": indeterminate_range,
    }
    return json.dumps(good_bad_def)


"""
Good/Bad Definition Page:
When the confirm button is clicked in good/bad definition page, this function 
computes the good & bad count of the whole dataset, and updates the historgram
"""


@app.callback(
    Output("dataset_total_good_bad_histogram", "figure"),
    Input("confirm_good_bad_def_button", "n_clicks"),
    [
        State("good_bad_def_dropdown", "value"),
        State("weight_of_good_input", "value"),
        State("weight_of_bad_input", "value"),
        State("indeterminate_range_slider", "value"),
    ],
)
def update_dataset_total_good_bad_histogram(
    n_clicks, def_column, good_weight, bad_weight, indeterminate_range
):
    good_bad_count = compute_dataset_total_good_bad(
        def_column, good_weight, bad_weight, indeterminate_range
    )
    fig = {
        "data": [
            {
                "x": ["Good", "Bad"],
                "y": good_bad_count,
                "type": "bar",
                "marker": {"color": "#6B87AB"},
            },
        ],
        "layout": {"title": "Good & Bad Count"},
    }
    return fig


"""
Good/Bad Definition Page:
When the user chose 'paid_past_due' column for the definition of good and bad,
automatically computes the weight of good, and updates the default value of the 
input box
"""


@app.callback(
    Output("weight_of_good_input", "value"),
    [
        Input("good_bad_def_dropdown", "value"),
        Input("indeterminate_range_slider", "value"),
    ],
    State("weight_of_good_input", "value"),
)
def update_default_weight_of_good_for_paid_past_due(
    def_column, indeterminate_range, good_weight
):
    if def_column == "paid_past_due":
        default_good_weight = compute_default_weight_of_good(indeterminate_range)
        return default_good_weight
    else:
        return good_weight  # do not update anything


"""
Good/Bad Definition Page:
When the user chose 'paid_past_due' column for the definition of good and bad,
automatically show the range slider, otherwise, hide the slider
"""


@app.callback(
    Output("select_indeterminate_range_section", "style"),
    Input("good_bad_def_dropdown", "value"),
)
def show_or_hide_indeterminate_range_slider(def_column):
    if def_column == "loan_status":
        return {"display": "none"}
    else:
        return {}


"""
Interactive Binning Page:
Render the data stored in shared storage about the predictor variables to be 
binned (which is set by user in the confirm input dataset page),
the options available in the dropdown showing the predictor variable can be binned in the Interactive 
Binning page is updated
"""


@app.callback(
    Output("predictor_var_ib_dropdown", "options"),
    Input("bins_settings", "data"),
)
def update_ib_predictor_var_dropdown(data):
    data_dict = json.loads(data)
    data_list = data_dict["variable"]
    col_to_be_binned_list = list()

    for pred_info in data_list:
        col_to_be_binned_list.append(pred_info["column"])

    return convert_column_list_to_dropdown_options(col_to_be_binned_list)


"""
Interactive Binning Page:
Update automated binning input section UI based on 
dropdown value
"""


@app.callback(
    [
        Output("equal_width_input_section", "style"),
        Output("equal_frequency_input_section", "style"),
        Output("import_settings_input_section", "style"),
    ],
    Input("auto_bin_algo_dropdown", "value"),
)
def update_auto_bin_input_section_UI(auto_bin_algo):
    if auto_bin_algo == "none":
        return {"display": "none"}, {"display": "none"}, {"display": "none"}
    elif auto_bin_algo == "equal width":
        return {}, {"display": "none"}, {"display": "none"}
    elif auto_bin_algo == "equal frequency":
        return {"display": "none"}, {}, {"display": "none"}
    else:
        return {"display": "none"}, {"display": "none"}, {}


"""
Interactive Binning Page:
Update user clicked bin's information
"""


@app.callback(
    [
        Output("selected_bin_name", "children"),
        Output("selected_bin_index", "children"),
        Output("selected_bin_count", "children"),
    ],
    Input("mixed_chart", "clickData"),
)
def update_clicked_bar_info(data):
    if data is not None and data["points"][0]["curveNumber"] != 2:
        return (
            "Bin Name: " + str(data["points"][0]["x"]),
            "Bin Index: " + str(data["points"][0]["pointIndex"]),
            "Bin Count: " + str(data["points"][0]["y"]),
        )
    else:
        return "Bin Name: ", "Bin Index: ", "Bin Count: "


"""
Interactive Binning Page:
Update the color of the bar clicked by the user
"""


@app.callback(
    Output("mixed_chart", "figure"),
    [
        Input("mixed_chart", "clickData"),
        Input("predictor_var_ib_dropdown", "value"),
    ],
    State("good_bad_def", "data"),
)
def update_bar_selected_color(data, var_to_bin, good_bad_def_data):
    if good_bad_def_data == None:
        var_df = df[
            [var_to_bin, "loan_status"]
        ]  # TODO: var_to_bin need to check null too
    else:
        good_bad_def = json.loads(good_bad_def_data)
        if good_bad_def["column"] == "loan_status":
            var_df = df[[var_to_bin, "loan_status"]]
        else:
            var_df = df[[var_to_bin, "loan_status", "paid_past_due"]]

    clicked_bar_index = None

    if data is not None and data["points"][0]["curveNumber"] != 2:
        clicked_bar_index = data["points"][0]["pointIndex"]

    return generate_mixed_chart_fig(
        var_df=var_df,
        clicked_bar_index=clicked_bar_index,
        good_bad_def=good_bad_def_data,
    )


"""
Interactive Binning Page:
Update automated binning input section UI based on 
dropdown value
"""


@app.callback(
    Output("auto_bin_input_section", "children"),
    Input("auto_bin_algo_dropdown", "value"),
)
def update_auto_bin_input_section_UI(auto_bin_algo):
    if auto_bin_algo == "none":
        return []
    elif auto_bin_algo == "equal width":
        return [
            dcc.RadioItems(
                options=["width", "number of bins"], value="width", inline=True
            )
        ]
    elif auto_bin_algo == "equal frequency":
        return [
            dcc.RadioItems(
                options=["frequency", "number of bins"], value="frequency", inline=True
            )
        ]
    else:
        return [
            html.P("Upload a file: ", style={"display": "inline"}),
            SaveButton("Upload", marginLeft=10, backgroundColor="#8097e6"),
        ]


"""
Interactive Binning Page:
Update the input area of equal width automated binning 
algorithm based on the radio button value
"""


@app.callback(
    [
        Output("equal_width_width_input_section", "style"),
        Output("equal_width_num_bin_input_section", "style"),
    ],
    Input("equal_width_radio_button", "value"),
)
def update_equal_freq_input_section(method):
    if method == "width":
        return {}, {"display": "none"}
    else:  # method == "number of bins"
        return {"display": "none"}, {}


"""
Interactive Binning Page:
Update the input area of equal frequency automated binning 
algorithm based on the radio button value
"""


@app.callback(
    [
        Output("equal_freq_freq_input_section", "style"),
        Output("equal_freq_num_bin_input_section", "style"),
    ],
    Input("equal_freq_radio_button", "value"),
)
def update_equal_freq_input_section(method):
    if method == "frequency":
        return {}, {"display": "none"}
    else:  # method == "number of bins"
        return {"display": "none"}, {}


"""
Preview & Download Settings:
update binned dataframe for preview
"""


@app.callback(
    Output("preview_binned_df", "data"),
    Input("binned_df", "data"),
)
def update_preview_output_dataset(data):
    adict = json.loads(data)
    binned_df = pd.DataFrame.from_dict(adict)
    return binned_df.to_dict("records")


@app.callback(
    Output("preview_binned_df", "columns"),
    Input("binned_df", "data"),
)
def update_preview_output_dataset2(data):
    adict = json.loads(data)
    binned_df = pd.DataFrame.from_dict(adict)
    return [{"name": i, "id": i} for i in binned_df.columns]


"""
Preview & Download Settings:
export bins settings as json file
"""


@app.callback(
    Output("download_json", "data"),
    Input("download_bin_settings_button", "n_clicks"),
    State("bins_settings", "data"),
    prevent_initial_call=True,
)
def export_bin_settings(n_clicks, bins_settings_data):
    return dict(content=bins_settings_data, filename="bins_settings.json")


"""
All:
When bins_settings in shared storage is changed, re-bin
all var based on the new settings, and save the binned dataframe
to shared storage
"""


@app.callback(
    Output("binned_df", "data"),
    Input("bins_settings", "data"),
)
def bin_df_and_save_to_shared_storage(bins_settings_data):
    bins_settings_dict = json.loads(bins_settings_data)
    bins_settings_list = bins_settings_dict["variable"]

    binned_df = compute_binned_dataset(bins_settings_list)

    return json.dumps(binned_df.to_dict())


###########################################################################
############################ Debugging Purpose ############################
###########################################################################

# Get bins settings
@app.callback(
    Output("text", "children"),
    Input("bins_settings", "data"),
)
def update_bins_settings(data):
    adict = json.loads(data)
    alist = adict["variable"]
    return str(alist)


# Get good/bad definitions
@app.callback(
    Output("text3", "children"),
    Input("good_bad_def", "data"),
)
def update_good_bad_def(data):
    return data


# get good bad def column in ib page
@app.callback(
    Output("text_omg", "children"),
    Input("mixed_chart", "clickData"),
    [
        State("good_bad_def", "data"),
        State("predictor_var_ib_dropdown", "value"),
    ],
)
def hi(data, good_bad_def_data, var_to_bin):
    if good_bad_def_data == None:
        return "none"
    else:
        good_bad_def = json.loads(good_bad_def_data)
        if good_bad_def["column"] == "loan_status":
            return "loan_status"
        else:
            return "paid_past_due"


###########################################################################
############ Not important for our development after this line ############
###########################################################################

"""
Setup web application layout & callbacks for navigation (can ignore this part)
"""
# base styling
app.config.external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

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
