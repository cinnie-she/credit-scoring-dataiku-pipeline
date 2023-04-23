import dataiku
import pandas as pd
import numpy as np
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from decimal import Decimal

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
            dcc.Store(id="temp_col_bins_settings"),
            dcc.Store(id="temp_binned_col"),
            dcc.Store(id="temp_chart_info"),
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
section_heading_center_style = {
    "fontSize": font_size["section-heading"],
    "textAlign": "center",
    "fontWeight": "bold",
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


def SectionHeading(title, inline=False, center=False, bold=False):
    if inline == True:
        return html.H2(
            title,
            style=section_heading_inline_style,
        )
    if center == True and bold == True:
        return html.H2(
            title,
            style=section_heading_center_style,
        )
    return html.H2(
        title,
        style=section_heading_style,
    )


def DataTable(df, id="", width=dimens["table-column-width"]):
    return dash_table.DataTable(
        data=df.to_dict("records"),
        columns=[{"name": i, "id": i} for i in df.columns],
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={
            "minWidth": width,
            "width": width,
            "maxWidth": width+30,
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


def SaveButton(title, inline=False, marginLeft=0, marginTop=0, id="", backgroundColor="#6668A9", width=0):
    if width == 0:
        if inline == True:
            return html.Button(
                title,
                style={
                    "marginLeft": marginLeft,
                    "marginTop": marginTop,
                    "backgroundColor": backgroundColor,
                    "color": "#ffffff",
                    "textTransform": "none",
                    "float": "left",
                },
                id=id,
            )
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
    else:
        if inline == True:
            return html.Button(
                title,
                style={
                    "marginLeft": marginLeft,
                    "marginTop": marginTop,
                    "backgroundColor": backgroundColor,
                    "color": "#ffffff",
                    "textTransform": "none",
                    "float": "left",
                    "width": width,
                    "paddingLeft": 5,
                    "paddingRight": 5,
                },
                id=id,
            )
        return html.Button(
            title,
            style={
                "marginLeft": marginLeft,
                "marginTop": marginTop,
                "backgroundColor": backgroundColor,
                "color": "#ffffff",
                "textTransform": "none",
                "width": width,
                "paddingLeft": 5,
                "paddingRight": 5,
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
    def validate_if_numerical_def_overlapped(self, bad_numeric_list, indeterminate_numeric_list):
        for bad_numeric_def in bad_numeric_list:
            column = bad_numeric_def["column"]
            for indeterminate_numeric_def in indeterminate_numeric_list:
                # found matching column definition
                if indeterminate_numeric_def["column"] == column:
                    # Check if any overlapping definition
                    for bad_range in bad_numeric_def["ranges"]:
                        for indeterminate_range in indeterminate_numeric_def["ranges"]:
                            if bad_range[0] < indeterminate_range[0] and bad_range[1] > indeterminate_range[0]:
                                return False
                            if bad_range[0] < indeterminate_range[1] and bad_range[1] > indeterminate_range[1]:
                                return False
                            if bad_range[0] == indeterminate_range[0] and bad_range[1] <= indeterminate_range[1]:
                                return False
                            if bad_range[1] == indeterminate_range[1] and bad_range[0] >= indeterminate_range[0]:
                                return False
                    break
        return True

    # A method to validate if categorical definitions for bad/indeterminate has overlapped
    def validate_if_categorical_def_overlapped(self, bad_categoric_list, indeterminate_categoric_list):
        for bad_categoric_def in bad_categoric_list:
            column = bad_categoric_def["column"]
            for indeterminate_categoric_def in indeterminate_categoric_list:
                # found matching column definition
                if indeterminate_categoric_def["column"] == column:
                    # Check if any overlapping definition
                    for element in bad_categoric_def["elements"]:
                        if element in indeterminate_categoric_def["elements"]:
                            return False
                    break
        return True

    # A method to validate if all numerical definition range have upper bound > lower bound, if not, returns false
    def validate_numerical_bounds(self, numeric_info_list):
        for numeric_info in numeric_info_list:
            a_range = [numeric_info[1], numeric_info[2]]
            try:
                if a_range[1] <= a_range[0]:
                    return False
            except:
                return False
        return True


# A class for merging overlapping good bad definition ranges/elements for the same type (bad or indeterminate)
class GoodBadDefDecoder:
    # A method to translate numerical definition ranges defined by user (with/without overlapping) info to a list of numerical definition (no overlapping)
    @staticmethod
    def get_numeric_def_list_from_section(numeric_info_list):
        numeric_list = list()  # initialization

        for numeric_info in numeric_info_list:
            single_def_dict = dict()
            column = numeric_info[0]
            a_range = [numeric_info[1], numeric_info[2]]
            # The 2 bounds are valid, now check if any overlapping with previously saved data
            has_column_overlap = False
            for def_idx, saved_def in enumerate(numeric_list):
                if saved_def["column"] == column:
                    has_column_overlap = True
                    has_range_overlap = False
                    overlapped_def_range_idxes = list()
                    # Merge range to element list
                    for def_range_idx, def_range in enumerate(saved_def["ranges"]):
                        if len(overlapped_def_range_idxes) != 0:
                            a_range = numeric_list[def_idx]["ranges"][overlapped_def_range_idxes[0]]

                        if a_range[0] <= def_range[0] and a_range[1] >= def_range[1]:
                            has_range_overlap = True
                            numeric_list[def_idx]["ranges"][def_range_idx] = [
                                a_range[0], a_range[1]]
                            overlapped_def_range_idxes.insert(0, def_range_idx)
                        elif def_range[0] <= a_range[0] and def_range[1] >= a_range[1]:
                            has_range_overlap = True
                        elif a_range[0] <= def_range[0] and a_range[1] >= def_range[0] and a_range[1] <= def_range[1]:
                            has_range_overlap = True
                            numeric_list[def_idx]["ranges"][def_range_idx] = [
                                a_range[0], def_range[1]]
                            overlapped_def_range_idxes.insert(0, def_range_idx)
                        elif a_range[0] >= def_range[0] and a_range[0] <= def_range[1] and a_range[1] >= def_range[1]:
                            has_range_overlap = True
                            numeric_list[def_idx]["ranges"][def_range_idx] = [
                                def_range[0], a_range[1]]
                            overlapped_def_range_idxes.insert(0, def_range_idx)
                    if len(overlapped_def_range_idxes) != 0:
                        del overlapped_def_range_idxes[0]
                        for i in sorted(overlapped_def_range_idxes, reverse=True):
                            del numeric_list[def_idx]["ranges"][i]
                    if has_range_overlap == False:
                        numeric_list[def_idx]["ranges"].append(a_range)
                    break
            if has_column_overlap == False:
                single_def_dict["column"] = column
                single_def_dict["ranges"] = [a_range]
                numeric_list.append(single_def_dict)

        for idx in range(len(numeric_list)):
            numeric_list[idx]["ranges"] = GoodBadDefDecoder.sort_numerical_def_ranges(
                numeric_list[idx]["ranges"])

        return numeric_list

    # A method to sort a list of numerical def e.g., from [[15, 20], [1, 10], [13, 14]] to [[1, 10], [13, 14], [15, 20]].
    @staticmethod
    def sort_numerical_def_ranges(numeric_def_r):
        sorted_def_ranges = list()
        for r in numeric_def_r:
            has_appended = False
            for idx in range(len(sorted_def_ranges)):
                if r[0] < sorted_def_ranges[idx][0]:
                    sorted_def_ranges.insert(idx, r)
                    has_appended = True
                    break
            if has_appended == False:
                sorted_def_ranges.append(r)
        return sorted_def_ranges

    # A method to translate categorical definition elements defined by user (with/without overlapping) info to a list of categorical definition (no overlapping)
    @staticmethod
    def get_categorical_def_list_from_section(categoric_info_list):
        categoric_list = list()  # initialization
        for categoric_info in categoric_info_list:
            single_def_dict = dict()
            column = categoric_info[0]
            elements = categoric_info[1]
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


# A class for counting the number of good and bad samples/population in the column
class GoodBadCounter:
    # A method to get the number of sample bad, sample indeterminate, sample good, population good, and population bad
    @staticmethod
    def get_statistics(dframe, good_bad_def):
        new_dframe, sample_bad_count = GoodBadCounter.count_sample_bad(
            dframe, good_bad_def["bad"])
        sample_indeterminate_count = GoodBadCounter.count_sample_indeterminate(
            new_dframe, good_bad_def["indeterminate"])
        sample_good_count = GoodBadCounter.count_sample_good(
            dframe, sample_bad_count, sample_indeterminate_count)
        good_weight = good_bad_def["good"]["weight"]
        bad_weight = good_bad_def["bad"]["weight"]
        population_good_count = GoodBadCounter.get_population_good(
            sample_good_count, good_weight)
        population_bad_count = GoodBadCounter.get_population_bad(
            sample_bad_count, bad_weight)
        return (sample_bad_count, sample_indeterminate_count, sample_good_count, good_weight, bad_weight, population_good_count, population_bad_count)

    # A method to count the number of sample bad
    @staticmethod
    def count_sample_bad(dframe, bad_defs):
        bad_count = 0
        for bad_numeric_def in bad_defs["numerical"]:
            # count number of rows if dframe row is in bad_numeric_def range, and add to bad_count
            for a_range in bad_numeric_def["ranges"]:
                bad_count += len(dframe[(dframe[bad_numeric_def["column"]] >= a_range[0]) & (
                    dframe[bad_numeric_def["column"]] < a_range[1])])
                # delete rows if dframe row is in bad_numeric_def range
                dframe = dframe.drop(dframe[(dframe[bad_numeric_def["column"]] >= a_range[0]) & (
                    dframe[bad_numeric_def["column"]] < a_range[1])].index)

        for bad_categoric_def in bad_defs["categorical"]:
            # count number of rows if dframe row is having any one of the bad_categoric_def elements value
            for element in bad_categoric_def["elements"]:
                bad_count += len(dframe[(dframe[bad_categoric_def["column"]] == element)])
                # delete rows if dframe row has value 'element'
                dframe = dframe.drop(
                    dframe[(dframe[bad_categoric_def["column"]] == element)].index)

        return (dframe, bad_count)

    # A method to count the number of sample indeterminate
    @staticmethod
    def count_sample_indeterminate(dframe, indeterminate_defs):
        indeterminate_count = 0
        for indeterminate_numeric_def in indeterminate_defs["numerical"]:
            # count number of rows if dframe row is in indeterminate_numeric_def range, and add to indeterminate_count
            for a_range in indeterminate_numeric_def["ranges"]:
                indeterminate_count += len(dframe[(dframe[indeterminate_numeric_def["column"]] >= a_range[0]) & (
                    dframe[indeterminate_numeric_def["column"]] < a_range[1])])
                # delete rows if dframe row is in indeterminate_numeric_def range
                dframe = dframe.drop(dframe[(dframe[indeterminate_numeric_def["column"]] >= a_range[0]) & (
                    dframe[indeterminate_numeric_def["column"]] < a_range[1])].index)

        for indeterminate_categoric_def in indeterminate_defs["categorical"]:
            # count number of rows if dframe row is having any one of the indeterminate_categoric_def elements value
            for element in indeterminate_categoric_def["elements"]:
                indeterminate_count += len(
                    dframe[(dframe[indeterminate_categoric_def["column"]] == element)])
                # delete rows if dframe row has value 'element'
                dframe = dframe.drop(
                    dframe[(dframe[indeterminate_categoric_def["column"]] == element)].index)

        return indeterminate_count

    # A method to count the number of sample good
    @staticmethod
    def count_sample_good(dframe, sample_bad_count, sample_indeterminate_count):
        return (len(dframe) - sample_bad_count - sample_indeterminate_count)

    # A method to count the number of population good
    @staticmethod
    def get_population_good(sample_good_count, good_weight):
        return sample_good_count * good_weight

    # A method to count the number of population bad
    @staticmethod
    def get_population_bad(sample_bad_count, bad_weight):
        return sample_bad_count * bad_weight


"""
Interactive Binning Page
"""
# A class to calculate statistical values for displaying the mixed chart & statistical tables


class StatCalculator:
    def __init__(self, df, col_bins_settings, good_bad_def) -> None:
        # for binning & good bad calculation, need whole df (OR only columns to be binned & columns involved in good bad def)
        self.df = df
        self.col_bins_settings = col_bins_settings  # for binning
        self.good_bad_def = good_bad_def  # for good bad calculation

    # Output - a dataframe representing the summary statistics table of the column
    def compute_summary_stat_table(self):
        if len(self.df) == 0 or self.col_bins_settings == None or self.good_bad_def == None:
            return None
        """
        1. Binning
        """
        col_to_bin = self.col_bins_settings["column"]  # get the name of column to be binned

        col_df = self.df.loc[:, [col_to_bin]]  # get a single column

        # perform binning
        _, binned_series = BinningMachine.perform_binning_on_col(
            col_df, self.col_bins_settings)
        self.df.insert(loc=0, column=col_to_bin+"_binned", value=binned_series)

        """
        2. Compute Summary Statistic Table
        """
        # Initialize an empty dictionary for storing information of each rows of the summary table (i.e., each bin)
        summary_dict = dict()
        # Create a list which stores summary table' column names
        summary_table_col_name_list = ["Bin", "Good", "Bad", "Odds",
                                       "Total", "Good%", "Bad%", "Total%", "Info_Odds", "WOE", "MC"]

        # Get and save a list of unique bin_name
        bin_name_list = self.df.iloc[:, 0].unique().tolist()

        # Get total good & bad
        _, _, _, _, _, total_good_count, total_bad_count = GoodBadCounter.get_statistics(
            self.df, self.good_bad_def)

        # For each bin_name in the list (i.e. loop nbin times)
        for bin_name in bin_name_list:
            # Get a DataFrame which filtered out rows that does not belong to the bin
            bin_df = self.df.loc[self.df.iloc[:, 0] == bin_name]
            # Call compute_bin_stats(var_df : pd.DataFrame, total_num_records : Integer, bin_name : String) and save as bin_stats_list
            bin_stats_list = self.__compute_bin_stats__(
                bin_df, bin_name, total_good_count, total_bad_count)
            # Add an element in the dictionary, with bin_name as the key, and bin_stats_list as the value
            summary_dict[bin_name] = bin_stats_list

        # Create a pd.DataFrame object using the created dictionary
        var_summary_df = pd.DataFrame.from_dict(
            summary_dict, orient='index', columns=summary_table_col_name_list)

        # Call compute_var_stats(var_df: pd.DataFrame, var_summary_df : pd.DataFrame, total_num_records : Integer) and save the list
        var_stats_list = self.__compute_var_stats__(
            var_summary_df, total_good_count, total_bad_count)

        # Create a dictionary using "all" as the key, and the list created as the value
        all_summary_series = pd.Series(
            var_stats_list, index=summary_table_col_name_list)

        # Append the dictionary as a row to the pd.DataFrame created
        var_summary_df = var_summary_df.append(
            all_summary_series, ignore_index=True)

        # format df
        for col in ['Odds', 'Info_Odds', 'WOE', 'MC']:
            var_summary_df[col] = var_summary_df[col].apply(
                lambda x: 0 if (x != None and abs(x) < 0.001) else x)
            var_summary_df[col] = var_summary_df[col].apply(
                lambda x: round(x, 4) if (x != None) else x)

        for col in ['Good%', 'Bad%', 'Total%']:
            var_summary_df[col] = var_summary_df[col].apply(
                lambda x: round(x, 4) if (x != None) else x)

        return var_summary_df

    def __compute_bin_stats__(self, bin_df, bin_name, total_good, total_bad):
        # Initialize an empty list (e.g., bin_stats_list) for storing the statistics for a bin
        bin_stats_list = list()

        # Compute bin good & bad count
        _, _, _, _, _, good, bad = GoodBadCounter.get_statistics(
            bin_df, self.good_bad_def)
        # Compute bin total count
        total = good + bad
        # Call compute_pct(value : Integer, total_value : Integer) and save the returned value (i.e., good%)
        good_pct = self.compute_pct(good, total_good)
        # Call compute_pct(value : Integer, total_value : Integer) and save the returned value (i.e., bad%)
        bad_pct = self.compute_pct(bad, total_bad)
        # Call compute_pct(value : Integer, total_value : Integer) and save the returned value (i.e., total%)
        total_pct = self.compute_pct(total, total_good + total_bad)
        # Call compute_odds(good_pct : Float, bad_pct : Float) and save the returned value
        odds = self.compute_odds(good, bad)
        info_odds = self.compute_info_odds(good_pct, bad_pct)
        # Call compute_woe(df : pd.DataFrame) using df and save the returned value
        woe = self.compute_woe(info_odds)
        # Call compute_info_val(good_pct : Float, bad_pct : Float, woe : Float) and save the returned value
        mc = self.compute_mc(good_pct, bad_pct, woe)

        # Append all statistics to the bin_stats_list in order
        bin_stats_row = [bin_name, good, bad, odds, total, good_pct *
                         100, bad_pct*100, total_pct*100, info_odds, woe, mc]
        bin_stats_list.extend(bin_stats_row)

        # Return list
        return bin_stats_list

    def __compute_var_stats__(self, var_summary_df, total_good, total_bad):
        # Create an empty list for storing the statistics for the whole dataset
        var_stats_list = list()

        # Call compute_good(df : pd.DataFrame) using df and save the returned value
        good = total_good
        # Call compute_bad(df : pd.DataFrame) using df and save the returned value
        bad = total_bad
        # Call compute_total(df : pd.DataFrame) using df and save the returned value
        total = good + bad
        # Call compute_pct(value : Integer, total_value : Integer) and save the returned value (i.e., good%)
        good_pct = self.compute_pct(good, total_good)
        # Call compute_pct(value : Integer, total_value : Integer) and save the returned value (i.e., bad%)
        bad_pct = self.compute_pct(bad, total_bad)
        # Call compute_pct(value : Integer, total_value : Integer) and save the returned value (i.e., total%)
        total_pct = 1
        # Call compute_odds(good_pct : Float, bad_pct : Float) and save the returned value
        odds = self.compute_odds(good, bad)
        info_odds = None
        # Empty woe
        woe = None
        # Sum up the MC column and save the value = InfoVal
        mc = var_summary_df.MC.sum()

        # Append all statistics to the empty list in order
        var_stats_list = ["Total", good, bad, odds, total, good_pct *
                          100, bad_pct*100, total_pct*100, info_odds, woe, mc]
        # Return list
        return var_stats_list

    @staticmethod
    def compute_pct(value, total_value):
        if total_value == 0:
            return None
        else:
            return (value/total_value)

    @staticmethod
    def compute_odds(good, bad):
        if bad == 0:
            return None
        else:
            return (good/bad)

    @staticmethod
    def compute_info_odds(good_pct, bad_pct):
        if bad_pct == 0:
            return None
        else:
            return (good_pct/bad_pct)

    @staticmethod
    def compute_woe(info_odds):
        if info_odds == None or info_odds <= 0:
            return None
        else:
            return np.log(info_odds)

    @staticmethod
    def compute_mc(good_pct, bad_pct, woe):
        if woe == None:
            return 0
        else:
            return (good_pct - bad_pct)*woe


def get_list_of_total_count(temp_df, binned_col, unique_bin_name_list, good_bad_def):
    total_count_list = list()

    for unique_bin_name in unique_bin_name_list:
        if good_bad_def == None:  # If-else statement put outside for loop would be better
            total_count_list.append(0)  # good bad def not defined, so no count
        else:
            bin_df = temp_df[temp_df[binned_col] == unique_bin_name]
            # Get total good & bad
            _, _, _, _, _, total_good_count, total_bad_count = GoodBadCounter.get_statistics(
                bin_df, good_bad_def)
            total_count_list.append(total_good_count+total_bad_count)
    return total_count_list


def get_list_of_bad_count(temp_df, binned_col, unique_bin_name_list, good_bad_def):
    bad_count_list = list()
    for unique_bin_name in unique_bin_name_list:
        if good_bad_def == None:  # good bad def not defined, so no count
            bad_count_list.append(0)
        else:
            bin_df = temp_df[temp_df[binned_col] == unique_bin_name]
            _, _, _, _, _, _, total_bad_count = GoodBadCounter.get_statistics(
                bin_df, good_bad_def)
            bad_count_list.append(total_bad_count)
    return bad_count_list


def get_list_of_woe(temp_df, binned_col, unique_bin_name_list, good_bad_def):
    woe_list = list()
    for unique_bin_name in unique_bin_name_list:
        if good_bad_def == None:
            woe_list.append(0)
        else:
            bin_df = temp_df[temp_df[binned_col] == unique_bin_name]
            _, _, _, _, _, total_good, total_bad = GoodBadCounter.get_statistics(
                df, good_bad_def)
            _, _, _, _, _, good, bad = GoodBadCounter.get_statistics(
                bin_df, good_bad_def)
            good_pct = StatCalculator.compute_pct(good, total_good)
            bad_pct = StatCalculator.compute_pct(bad, total_bad)
            info_odds = StatCalculator.compute_info_odds(good_pct, bad_pct)
            woe = StatCalculator.compute_woe(info_odds)
            woe_list.append(woe)
    return woe_list


def generate_mixed_chart_fig(
    unique_bins=[], total_count_list=[], bad_count_list=[], woe_list=[], clicked_bar_index=None, selected_bars_index_set=None
):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    num_bins = len(unique_bins)

    good_marker_color = ["#8097e6"] * num_bins
    if selected_bars_index_set is not None and len(selected_bars_index_set) != 0:
        for idx in selected_bars_index_set:
            good_marker_color[idx] = "#3961ee"
    elif clicked_bar_index is not None:
        good_marker_color[clicked_bar_index] = "#3961ee"

    bad_marker_color = ["#8bd58b"] * num_bins
    if selected_bars_index_set is not None and len(selected_bars_index_set) != 0:
        for idx in selected_bars_index_set:
            bad_marker_color[idx] = "#55a755"
    elif clicked_bar_index is not None:
        bad_marker_color[clicked_bar_index] = "#55a755"

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
            y=woe_list,
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


def get_str_from_ranges(ranges):
        if not isinstance(ranges, list):
            return -1
        if len(ranges) == 0:
            return '[]'
        
        ranges = GoodBadDefDecoder.sort_numerical_def_ranges(ranges)
        
        ranges_str = "["
        ranges_str = f"{ranges_str}[{ranges[0][0]}, {ranges[0][1]})"
        for idx in range(1, len(ranges)):
            ranges_str = f"{ranges_str}, [{ranges[idx][0]}, {ranges[idx][1]})"
        ranges_str += "]"
        return ranges_str  


# A class for performing binning based on bins settings
class BinningMachine:
    # Perform equal width binning based on a specified width (for numerical column only)
    @staticmethod
    def perform_eq_width_binning_by_width(col_df, width):
        if len(col_df) == 0:
            return (-1, -1)
        if col_df.isna().all().all():
            return (-1, pd.Series([None for _ in range(len(col_df))]))
        # Cannot be categorical type
        if not pd.api.types.is_numeric_dtype(col_df.iloc[:, 0]):
            return (-1, -1)
        # width cannot be non-numeric
        if not (isinstance(width, int) or isinstance(width, float)) or width <= 0:
            return (-1, -1)

        min = col_df.min()
        max = col_df.max()
        num_bins = int(np.ceil((max - min) / width)) + 1

        bin_edges = list()
        for i in range(num_bins):
            bin_edges.append(
                float(Decimal(str(float(min))) + Decimal(str(width)) * i))

        bin_ranges = [
            [edge, float(Decimal(str(edge))+Decimal(str(width)))] for edge in bin_edges]

        binned_result = list()
        for _, row in col_df.iterrows():
            val = row.iloc[0]
            if np.isnan(val):
                binned_result.append(None)

            for bin_range in bin_ranges:
                if val >= bin_range[0] and val < bin_range[1]:
                    binned_result.append(f"[{bin_range[0]}, {bin_range[1]})")
                    break
        
        def_li = list()
        for r in bin_ranges:
            def_li.append({"name": get_str_from_ranges([r]), "ranges": [r]})
        
        return (def_li, pd.Series(binned_result))

    # A method to perform equal width binning based on a specified number of bins
    @staticmethod
    def perform_eq_width_binning_by_num_bins(col_df, num_bins):
        if len(col_df) == 0:
            return (-1, -1)
        if col_df.isna().all().all():
            return (-1, pd.Series([None for _ in range(len(col_df))]))
        # Cannot be categorical type
        if not pd.api.types.is_numeric_dtype(col_df.iloc[:, 0]):
            return (-1, -1)
        if not isinstance(num_bins, int) or num_bins <= 0:
            return (-1, -1)

        min = col_df.min()
        max = col_df.max()
        width = (float(max) - float(min)) / num_bins
        add_to_last_width = Decimal(str(width * 0.01))  # to include max value

        bin_edges = list()
        for i in range(num_bins):
            bin_edges.append(
                float(Decimal(str(float(min))) + Decimal(str(width)) * i))

        bin_ranges = [
            [edge, float(Decimal(str(edge))+Decimal(str(width)))] for edge in bin_edges]
        bin_ranges[len(bin_ranges)-1][1] = float(Decimal(str(add_to_last_width)
                                                         ) + Decimal(str(bin_ranges[len(bin_ranges)-1][1])))

        binned_result = list()
        for _, row in col_df.iterrows():
            val = row.iloc[0]
            if np.isnan(val):
                binned_result.append(None)
            for bin_range in bin_ranges:
                if val >= bin_range[0] and val < bin_range[1]:
                    binned_result.append(f"[{bin_range[0]}, {bin_range[1]})")
                    break
                
        def_li = list()
        for r in bin_ranges:
            def_li.append({"name": get_str_from_ranges([r]), "ranges": [r]})
        
        return (def_li, pd.Series(binned_result))

    # A method to perform equal frequency binning based on a specified frequency
    @staticmethod
    def perform_eq_freq_binning_by_freq(col_df, freq):
        if len(col_df) == 0:
            return (-1, -1)
        if col_df.isna().all().all():
            return (-1, pd.Series([None for _ in range(len(col_df))]))
        # Cannot be categorical type
        if not pd.api.types.is_numeric_dtype(col_df.iloc[:, 0]):
            return (-1, -1)
        if not isinstance(freq, int) or freq <= 0 or freq > len(col_df):
            return (-1, -1)

        num_bins = int(np.ceil(len(col_df)/freq))
        # print(num_bins)
        # if num_bins == 1:
        #     print(type(col_df.iloc[:, 0]))
        #     return col_df.iloc[:, 0]

        # bin the col_df
        interval_li = pd.qcut(
            col_df.iloc[:, 0], num_bins, duplicates="drop").to_list()

        if all(not isinstance(x, pd._libs.interval.Interval) for x in interval_li):
            interval_li = [pd.Interval(float(col_df.iloc[0:1, 0]), float(
                col_df.iloc[0:1, 0])+1) for _ in interval_li]

        # convert to the format we want
        binned_result = list()
        for idx in range(len(interval_li)):
            if not isinstance(interval_li[idx], pd._libs.interval.Interval):
                binned_result.append(None)
            else:
                binned_result.append(
                    f"[{interval_li[idx].left}, {interval_li[idx].right})")

        def_set = set()
        for idx in range(len(interval_li)):
            if isinstance(interval_li[idx], pd._libs.interval.Interval):
                def_set.add((interval_li[idx].left, interval_li[idx].right))
        bin_ranges = list(def_set)
        
        def_li = list()
        for r in bin_ranges:
            def_li.append({"name": get_str_from_ranges([[r[0], r[1]]]), "ranges": [[r[0], r[1]]]})
        
        return (def_li, pd.Series(binned_result))

    # A method to perform equal-frequency binning based on a specified number of bins
    @staticmethod
    def perform_eq_freq_binning_by_num_bins(col_df, num_bins):
        if len(col_df) == 0:
            return (-1, -1)
        if col_df.isna().all().all():
            return (-1, pd.Series([None for _ in range(len(col_df))]))
        # Cannot be categorical type
        if not pd.api.types.is_numeric_dtype(col_df.iloc[:, 0]):
            return (-1, -1)
        if not isinstance(num_bins, int) or num_bins <= 0:
            return (-1, -1)

        interval_li = pd.qcut(
            col_df.iloc[:, 0], num_bins, duplicates="drop").to_list()

        if all(not isinstance(x, pd._libs.interval.Interval) for x in interval_li):
            interval_li = [pd.Interval(float(col_df.iloc[0:1, 0]), float(
                col_df.iloc[0:1, 0])+1) for _ in interval_li]

        # convert to the format we want
        binned_result = list()
        for idx in range(len(interval_li)):
            if not isinstance(interval_li[idx], pd._libs.interval.Interval):
                binned_result.append(None)
            else:
                binned_result.append(
                    f"[{interval_li[idx].left}, {interval_li[idx].right})")

        def_set = set()
        for idx in range(len(interval_li)):
            if isinstance(interval_li[idx], pd._libs.interval.Interval):
                def_set.add((interval_li[idx].left, interval_li[idx].right))
        bin_ranges = list(def_set)
        
        def_li = list()
        for r in bin_ranges:
            def_li.append({"name": get_str_from_ranges([[r[0], r[1]]]), "ranges": [[r[0], r[1]]]})
        
        return (def_li, pd.Series(binned_result))

    # A method to perform custom binning for a categorical column
    @staticmethod
    def perform_categorical_custom_binning(col_df, bins_settings):
        if len(col_df) == 0:
            return (-1, -1)

        binned_result = list()

        for _, row in col_df.iterrows():
            val = row.iloc[0]
            has_assigned_bin = False
            for bin in bins_settings:
                if val in bin["elements"]:
                    binned_result.append(bin["name"])
                    has_assigned_bin = True
                    break
            if has_assigned_bin == False:  # does not belongs to any bin
                binned_result.append(None)

        return (bins_settings, pd.Series(binned_result))

    # A method to perform custom binning for a numerical column
    @staticmethod
    def perform_numerical_custom_binning(col_df, bins_settings):
        if len(col_df) == 0:
            return (-1, -1)

        binned_result = list()

        for _, row in col_df.iterrows():
            val = row.iloc[0]
            has_assigned_bin = False
            for bin in bins_settings:
                for r in bin["ranges"]:
                    if val >= r[0] and val < r[1]:
                        binned_result.append(bin["name"])
                        has_assigned_bin = True
                        break

            if has_assigned_bin == False:  # does not belongs to any bin
                binned_result.append(None)

        return (bins_settings, pd.Series(binned_result))

    # A method to perform binning (equal-width/equal-frequency/custom) for a single column (either categorical or numerical)
    @staticmethod
    def perform_binning_on_col(col_df, col_bins_settings):
        """
        col_bins_settings is in the form of: 
        {
            "column": "person_income",
            "type": "numerical",
            "info_val": 0.11,
            "bins": [
                {
                    "name": "0-9999, 30000-39999",
                    "ranges": [[0, 9999], [30000, 39999]],
                },
                {
                    "name": "20000-29999",
                    "ranges": [[20000, 29999]],
                },
            ],
        }
        """
        if col_bins_settings["bins"] == "none":
            if len(col_df) == 0:
                return (-1, -1)
            unique_bin = col_df.iloc[:, 0].unique().tolist()
            if col_bins_settings["type"] == "numerical":
                def_li = list()
                for bin in unique_bin:
                    def_li.append({"name": str(bin), "ranges": [[bin, bin+0.0000001]]})
                return BinningMachine.perform_numerical_custom_binning(col_df, def_li)
            else:
                def_li = list()
                for bin in unique_bin:
                    def_li.append({"name": str(bin), "elements": [bin]})
                return BinningMachine.perform_categorical_custom_binning(col_df, def_li)
        elif isinstance(col_bins_settings["bins"], dict):  # auto binning
            if col_bins_settings["bins"]["algo"] == "equal width":
                if col_bins_settings["bins"]["method"] == "width":
                    if col_bins_settings["type"] == "numerical":
                        return BinningMachine.perform_eq_width_binning_by_width(col_df, col_bins_settings["bins"]["value"])
                    else:
                        return (-1, -1)
                else:  # by num of bins
                    if col_bins_settings["type"] == "numerical":
                        return BinningMachine.perform_eq_width_binning_by_num_bins(col_df, col_bins_settings["bins"]["value"])
                    else:
                        return (-1, -1)
            else:  # equal frequency
                if col_bins_settings["bins"]["method"] == "freq":
                    if col_bins_settings["type"] == "numerical":
                        return BinningMachine.perform_eq_freq_binning_by_freq(col_df, col_bins_settings["bins"]["value"])
                    else:
                        return (-1, -1)
                else:  # by num of bins
                    if col_bins_settings["type"] == "numerical":
                        return BinningMachine.perform_eq_freq_binning_by_num_bins(col_df, col_bins_settings["bins"]["value"])
                    else:
                        return (-1, -1)
        else:  # custom binning
            if col_bins_settings["type"] == "numerical":
                return BinningMachine.perform_numerical_custom_binning(col_df, col_bins_settings["bins"])
            else:
                return BinningMachine.perform_categorical_custom_binning(col_df, col_bins_settings["bins"])

    # A method that perform binning (equal-width/equal-frequency/custom) for the whole dataframe (can contain numerical/categorical columns)
    @staticmethod
    def perform_binning_on_whole_df(dframe, bins_settings_list):
        if len(dframe) == 0:
            return dframe

        for col in dframe.columns:
            col_df = dframe.loc[:, [col]]

            # Find col_bins_settings
            col_bins_settings = None
            for bins_settings in bins_settings_list:
                if bins_settings["column"] == col:
                    col_bins_settings = bins_settings
                    break

            # if no bins settings for the column, skip it
            if col_bins_settings == None:
                continue

            _, binned_series = BinningMachine.perform_binning_on_col(
                col_df, col_bins_settings)
            if not isinstance(binned_series, pd.Series):  # error occurs
                return -1

            binned_col_name = col + "_binned"
            dframe[binned_col_name] = binned_series

        return dframe

def generate_categoric_old_div_children(old_bin_list=[], dtype=None):
    if dtype == None: 
        return []
    if len(old_bin_list) == 0:
        return []
    
    if dtype == "categorical":
        s = "Element"
    else:
        s = "Range"
    
    idx = 1
    old_element_list = list()
    for old_bin in old_bin_list:
        old_element_list.append(
            html.Div([
                html.Div([html.P("(" + str(idx) + ") ")], style={"width": "10%", "float": "left", "fontSize": 14}),
                html.Div([html.P("Old Bin Name: " + old_bin[0]), html.P("Old Bin " + s + "(s): " + old_bin[1])], style={"float": "left", "width": "85%", "fontSize": 14}),
            ])
        )
        idx += 1
        
    return old_element_list


def generate_categoric_new_div_children(new_bin_list=[], dtype=None):
    if dtype == None: 
        return []
    if len(new_bin_list) == 0:
        return []
    
    if dtype == "categorical":
        s = "Element"
    else:
        s = "Range"
    
    idx = 1
    new_element_list = list()
    for new_bin in new_bin_list:
        new_element_list.append(
            html.Div([
                html.Div([html.P("(" + str(idx) + ") ")], style={"width": "10%", "float": "left", "fontSize": 14}),
                html.Div([html.P("New Bin Name: " + new_bin[0]), html.P("New Bin "+ s + "(s): " + new_bin[1])], style={"float": "left", "width": "85%", "fontSize": 14}),
            ]),
        )
        idx += 1
    
    return new_element_list


def generate_bin_changes_div_children(old_bin_list=[], new_bin_list=[], dtype=None):
    if dtype == None:
        return []
    if old_bin_list == -1 or new_bin_list == -1:
        return [html.P("Error: The name has already been used.", style={"color": "red", "fontSize": 14})]
    if old_bin_list == -2 or new_bin_list == -2:
        return [html.P("Error: The new name is the same as the old one.", style={"color": "red", "fontSize": 14})]
    if old_bin_list == -3 or new_bin_list == -3:
        return [html.P("Error: Please select element(s) from the dropdown menu.", style={"color": "red", "fontSize": 14})]
    if old_bin_list == -4 or new_bin_list == -4:
        return [html.P("Error: All elements of the bin has been included, no splitting could be performed.", style={"color": "red", "fontSize": 14})]
    
    children = list()
    
    children.append(html.P("Preview Changes:", style={"fontWeight": "bold", "textDecoration": "underline"}))
    
    if len(old_bin_list) != 0:
        old_element_list = generate_categoric_old_div_children(old_bin_list=old_bin_list, dtype=dtype)
        children.append(html.P("Old Bin(s):", style={"fontWeight": "bold", "fontSize": 14}))
        children.append(html.Div(old_element_list))
    
    if len(new_bin_list) != 0:
        children.append(html.P("Will be changed to:", style={"fontWeight": "bold", "fontSize": 14}))
        new_element_list = generate_categoric_new_div_children(new_bin_list, dtype=dtype)
        children.append(html.Div(new_element_list))
    else:
        children.append(html.P("No changes."))

    return children


def generate_selected_bin_info_div_children(temp_chart_info, temp_col_bins_settings, click_data, dtype):
    if click_data is not None:
        children = list()
        points = click_data["points"]
        bin_defs = temp_col_bins_settings["bins"]
        selected_bin_names = set()
        
        for point in points:
            bin_name = point["x"]
            if bin_name in selected_bin_names:
                continue
            else:
                selected_bin_names.add(bin_name)
            
            if dtype == "categorical":
                bin_elements = None
                for bin_def in bin_defs:
                    if bin_def["name"] == bin_name:
                        bin_elements = bin_def["elements"]
            else:
                bin_ranges = None
                for bin_def in bin_defs:
                    if bin_def["name"] == bin_name:
                        bin_ranges = bin_def["ranges"]
                        
            bin_idx = point["pointIndex"]
            bin_bad_count = temp_chart_info["bad_count_list"][bin_idx]
            bin_gd_count = temp_chart_info["total_count_list"][bin_idx] - bin_bad_count
            bin_woe = temp_chart_info["woe_list"][bin_idx]
            children.append(html.P("Bin Name: " + str(bin_name), style={"fontSize": 14}))
            
            if dtype == "categorical":
                children.append(html.P("Bin Element(s): " + str(bin_elements), style={"fontSize": 14}))
            else:
                children.append(html.P("Bin Range(s): " + get_str_from_ranges(bin_ranges), style={"fontSize": 14}))
            
            children.append(html.P("Population Good Count: " + str(bin_gd_count), style={"fontSize": 14}))
            children.append(html.P("Population Bad Count: " + str(bin_bad_count), style={"fontSize": 14}))
            children.append(html.P("Bin WOE: " + "{:.4f}".format(bin_woe), style={"fontSize": 14}))
            if len(points) > 1:
                children.append(html.Hr(style={"marginTop": 8, "marginBottom": 8, "marginLeft": 0, "marginRight": 0}))
        
        return children
    else:
        return [
            html.P("Bin Name:", style={"fontSize": 14}),
            html.P("Bin Element(s): ", style={"fontSize": 14}),
            html.P("Population Good Count:", style={"fontSize": 14}),
            html.P("Population Bad Count: ", style={"fontSize": 14}),
            html.P("Bin WOE: ", style={"fontSize": 14}),
        ]

    
# A class for handling interactive binning logics
class InteractiveBinningMachine:
    @staticmethod
    def categoric_create_new_bin(new_bin_name, new_bin_element_li, temp_col_bins_settings):
        if len(new_bin_element_li) == 0:
            return (temp_col_bins_settings, -3, -3)
        
        if InteractiveBinningMachine.validate_new_name(new_bin_name, temp_col_bins_settings) == False:
            return (temp_col_bins_settings, -1, -1)
        
        old_bin_list = list()
        new_bin_list = list()
        
        bin_to_remove_idx_li = list()
        # for all bins, remove overlapped elements with new_bin_element_li
        for idx in range(len(temp_col_bins_settings["bins"])):
            intersaction = set(temp_col_bins_settings["bins"][idx]["elements"]) & set(new_bin_element_li)
            if bool(intersaction) == True:
                old_bin_list.append([temp_col_bins_settings["bins"][idx]["name"], str(temp_col_bins_settings["bins"][idx]["elements"])])
                intersaction_li = list(intersaction)
                temp_col_bins_settings["bins"][idx]["elements"] = [x for x in temp_col_bins_settings["bins"][idx]["elements"] if x not in intersaction_li]
            
                if len(temp_col_bins_settings["bins"][idx]["elements"]) == 0:
                    bin_to_remove_idx_li.append(idx)
                else:
                    new_bin_list.append([temp_col_bins_settings["bins"][idx]["name"], str(temp_col_bins_settings["bins"][idx]["elements"])])
        
        for idx in sorted(bin_to_remove_idx_li, reverse=True):
            del temp_col_bins_settings["bins"][idx]
        
        # add the new bin to bins settings
        if new_bin_name == "" or new_bin_name == None:
            new_bin_name = str(new_bin_element_li)
            
        if InteractiveBinningMachine.validate_new_name(new_bin_name, temp_col_bins_settings) == False:
            return (temp_col_bins_settings, -1, -1)
            
        new_bin = {
            "name": new_bin_name,
            "elements": new_bin_element_li
        }
        
        new_bin_list.append([new_bin_name, str(new_bin_element_li)])
        
        temp_col_bins_settings["bins"].append(new_bin)
        
        return (temp_col_bins_settings, old_bin_list, new_bin_list)
        
    @staticmethod
    def categoric_add_elements(selected_bin_name, new_bin_name, elements_to_add_li, temp_col_bins_settings):
        if len(elements_to_add_li) == 0:
            return (temp_col_bins_settings, -3, -3)
        
        if InteractiveBinningMachine.validate_new_name(new_bin_name, temp_col_bins_settings, selected_bin_name=selected_bin_name) == False:
            return (temp_col_bins_settings, -1, -1)
        
        old_bin_list = list()
        new_bin_list = list()
        
        bin_to_remove_idx_li = list()
        # for all bins, remove overlapped elements with new_bin_element_li
        for idx in range(len(temp_col_bins_settings["bins"])):
            intersaction = set(temp_col_bins_settings["bins"][idx]["elements"]) & set(elements_to_add_li)
            if bool(intersaction) == True:
                old_bin_list.append([temp_col_bins_settings["bins"][idx]["name"], str(temp_col_bins_settings["bins"][idx]["elements"])])
                intersaction_li = list(intersaction)
                temp_col_bins_settings["bins"][idx]["elements"] = [x for x in temp_col_bins_settings["bins"][idx]["elements"] if x not in intersaction_li]
            
                if len(temp_col_bins_settings["bins"][idx]["elements"]) == 0:
                    bin_to_remove_idx_li.append(idx)
                else:
                    new_bin_list.append([temp_col_bins_settings["bins"][idx]["name"], str(temp_col_bins_settings["bins"][idx]["elements"])])
            
            elif temp_col_bins_settings["bins"][idx]["name"] == selected_bin_name:
                old_bin_list.append([temp_col_bins_settings["bins"][idx]["name"], str(temp_col_bins_settings["bins"][idx]["elements"])])
                # Add elements to the selected bin
                for element in elements_to_add_li:
                    temp_col_bins_settings["bins"][idx]["elements"].append(element)
                if new_bin_name != "" and new_bin_name != None:
                    temp_col_bins_settings["bins"][idx]["name"] = new_bin_name
                new_bin_list.append([temp_col_bins_settings["bins"][idx]["name"], str(temp_col_bins_settings["bins"][idx]["elements"])])
        
        for idx in sorted(bin_to_remove_idx_li, reverse=True):
            del temp_col_bins_settings["bins"][idx]
          
        return (temp_col_bins_settings, old_bin_list, new_bin_list)
    
    @staticmethod
    def categoric_split_bin(selected_bin_name, new_bin_name, elements_to_split_out_li, temp_col_bins_settings):
        if len(elements_to_split_out_li) == 0:
            return (temp_col_bins_settings, -3, -3)
        
        if InteractiveBinningMachine.validate_new_name(new_bin_name, temp_col_bins_settings, selected_bin_name=selected_bin_name) == False:
            return (temp_col_bins_settings, -1, -1)
        
        old_bin_list = list()
        new_bin_list = list()
        
        for idx in range(len(temp_col_bins_settings["bins"])):
            if temp_col_bins_settings["bins"][idx]["name"] == selected_bin_name:
                if set(temp_col_bins_settings["bins"][idx]["elements"]) == set(elements_to_split_out_li):
                    return (temp_col_bins_settings, -4, -4)
                old_bin_list.append([temp_col_bins_settings["bins"][idx]["name"], str(temp_col_bins_settings["bins"][idx]["elements"])])
                # Remove user indicated elements from selected bin
                temp_col_bins_settings["bins"][idx]["elements"] = [x for x in temp_col_bins_settings["bins"][idx]["elements"] if x not in elements_to_split_out_li]
                new_bin_list.append([temp_col_bins_settings["bins"][idx]["name"], str(temp_col_bins_settings["bins"][idx]["elements"])])
                break
            
        if new_bin_name == "" or new_bin_name == None:
            new_bin_name = str(elements_to_split_out_li)
            
        new_bin = {
            "name": new_bin_name,
            "elements": elements_to_split_out_li,
        }
        
        temp_col_bins_settings["bins"].append(new_bin)
        
        new_bin_list.append([new_bin_name, str(elements_to_split_out_li)])
        
        return (temp_col_bins_settings, old_bin_list, new_bin_list)
        
                
    
    @staticmethod
    def categoric_rename_bin(selected_bin_name, new_bin_name, temp_col_bins_settings):
        if selected_bin_name == new_bin_name:
            return (temp_col_bins_settings, -2, -2)
        
        if InteractiveBinningMachine.validate_new_name(new_bin_name, temp_col_bins_settings) == False:
            return (temp_col_bins_settings, -1, -1)
        
        old_bin_list = list()
        new_bin_list = list()
        
        for idx in range(len(temp_col_bins_settings["bins"])):
            if temp_col_bins_settings["bins"][idx]["name"] == selected_bin_name:
                old_bin_list.append([temp_col_bins_settings["bins"][idx]["name"], str(temp_col_bins_settings["bins"][idx]["elements"])])
                
                if new_bin_name == "" or new_bin_name == None:
                    new_bin_name = str(temp_col_bins_settings["bins"][idx]["elements"])
                
                if InteractiveBinningMachine.validate_new_name(new_bin_name, temp_col_bins_settings) == False:
                    return (temp_col_bins_settings, -1, -1)
                
                temp_col_bins_settings["bins"][idx]["name"] = new_bin_name
                new_bin_list.append([temp_col_bins_settings["bins"][idx]["name"], str(temp_col_bins_settings["bins"][idx]["elements"])])
                break
                
        return (temp_col_bins_settings, old_bin_list, new_bin_list)
     
    @staticmethod
    def categoric_merge_bins(selected_bin_name_li, new_bin_name, temp_col_bins_settings):
        new_bin_element_list = list()
        bin_to_remove_idx_li = list()
        # Add elements to bin if it is one of the selected bins
        for idx in range(len(temp_col_bins_settings["bins"])):
            if temp_col_bins_settings["bins"][idx]["name"] in selected_bin_name_li:
                for element in temp_col_bins_settings["bins"][idx]["elements"]:
                    new_bin_element_list.append(element)
                bin_to_remove_idx_li.append(idx)
        
        for idx in sorted(bin_to_remove_idx_li, reverse=True):
            del temp_col_bins_settings["bins"][idx]
           
        if new_bin_name == "" or new_bin_name == None:
            new_bin_name = str(new_bin_element_list)
            
        if InteractiveBinningMachine.validate_new_name(new_bin_name, temp_col_bins_settings) == False:
            return (temp_col_bins_settings, -1, -1)
        
        new_bin = {
            "name": new_bin_name,
            "elements": new_bin_element_list,
        }
        
        temp_col_bins_settings["bins"].append(new_bin)
        
        new_bin_list = [[new_bin_name, str(new_bin_element_list)]]
        
        return (temp_col_bins_settings, [], new_bin_list)
        
        
    @staticmethod
    def validate_new_name(new_name, temp_col_bins_settings, selected_bin_name=None):
        # Return false if name has already been use. otherwise, return True
        if selected_bin_name == None:
            for bin_def in temp_col_bins_settings["bins"]:
                if bin_def["name"] == new_name:
                    return False
            return True
        else:
            if selected_bin_name == new_name:
                return True
            for bin_def in temp_col_bins_settings["bins"]:
                if bin_def["name"] == new_name:
                    return False
            return True
    
    
            
"""
All
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
        html.Div(style={"height": 100}),
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
                        SaveButton("Remove", marginLeft=10,
                                   id="bad_numeric_def_remove_button"),
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
                        SaveButton("Remove", marginLeft=10,
                                   id="bad_categoric_def_remove_button"),
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
                        SaveButton("Remove", marginLeft=10,
                                   id="indeterminate_numeric_def_remove_button"),
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
                        SaveButton("Remove", marginLeft=10,
                                   id="indeterminate_categoric_def_remove_button"),
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
        html.Div([], style={"height": 50, "clear": "left"}),
        # Debug
        html.Div([], style={"height": 100}),
        html.P("", id="test_good_bad_def"),
    ]
)


interactive_binning_page_layout = html.Div([
    NavBar(),
    Heading("Interactive Binning Interface"),
    html.P(id="ib_show_bins_settings_text"),  # debug
    html.P(id="ib_show_good_bad_def_text"),  # debug

    html.Div(
        [
            html.P(
                "Note: Binning & generating statistical tables may take some time, please wait patiently if applicable."),
            html.Div(
                [
                    SectionHeading(
                        "I. Select a predictor variable to bin"),
                    dcc.Dropdown(
                        options=convert_column_list_to_dropdown_options(
                            df.columns.to_list()
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
                        ],
                        value="none",
                        clearable=False,
                        searchable=False,
                        style={"marginBottom": 20, "width": 250},
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
                                    html.P("Width:", style={
                                        "display": "inline"}),
                                    dcc.Input(
                                        type="number",
                                        value=1,
                                        min=1,
                                        style={"marginLeft": 10},
                                        id="equal_width_width_input",
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
                                        id="equal_width_num_bin_input",
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
                                    {"label": "Frequency",
                                     "value": "frequency"},
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
                                        id="equal_freq_freq_input",
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
                                        id="equal_freq_num_bin_input",
                                    ),
                                ],
                                id="equal_freq_num_bin_input_section",
                                style={"display": "none"},
                            ),
                        ],
                        id="equal_frequency_input_section",
                        style={"display": "none"},
                    ),
                    html.Div([], style={"marginBottom": 25}),
                    SaveButton("Refresh", id="auto_bin_refresh_button"),
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
                    html.P(
                        "Tips 1: If you would like to de-select the bar(s), simply click on the WOE line.", style={"marginTop": 20}),
                    html.P(
                        "Tips 2: You could use the 'Box Select' or 'Lasso Select' tools on the top right corner to select multiple bars."),
                ],
                style=white_panel_style,
            ),
            # Categorical Create New Bin Control Panel
            html.Div([
                html.Div(
                    [
                        SectionHeading("Create a New Bin",
                                       center=True, bold=True),
                        html.P("Instructions", style={"fontWeight": "bold"}),
                        html.Ul([
                            html.Li("Enter the name of the new bin in the text input area", style={
                                    "fontSize": 14}),
                            html.Li("Select the elements from the dropdown menu that you would like to include in the bin", style={
                                    "fontSize": 14}),
                            html.Li("Click the ‘Create New Bin’ button to preview changes on the bins settings", style={
                                    "fontSize": 14}),
                            html.Li("The selected elements which overlaps with the old bins settings will be automatically removed from the other bins", style={
                                    "fontSize": 14}),
                            html.Li("Once you consider the binning is fine, click the ‘Submit’ button to update the mixed chart & the statistical tables", style={
                                    "fontSize": 14}),
                        ], style={"listStyleType": "square", "lineHeight": "97%"}),
                        html.P("Enter the new bin name: ",
                               style={"fontWeight": "bold"}),
                        dcc.Input(style={"marginBottom": 10},
                                  id="categoric_create_new_bin_name_input"),
                        html.P("Select elements to be included in the new bin:", style={
                               "fontWeight": "bold"}),
                        dcc.Dropdown(
                            options=convert_column_list_to_dropdown_options(
                                ["OWN", "RENT", "MORTGAGE", "OTHERS"]),  # dummy
                            value=[],
                            multi=True,
                            style={"marginBottom": 13},
                            id="categoric_create_new_bin_dropdown",
                        ),
                        SaveButton("Create New Bin",
                                   id="categoric_create_new_bin_button"),
                        html.Div(style={"height": 13}),
                        html.Div([
                            html.Div([], id="categoric_create_new_bin_changes_div"),
                            html.Div([
                                SaveButton(
                                    "Submit", inline=True, id="categoric_create_new_bin_submit_button"),
                                SaveButton("Hide Details", inline=True, backgroundColor="#8097E6",
                                           marginLeft=5, id="categoric_create_new_bin_hide_details_button"),
                                html.Div(style={"height": 13, "clear": "both"}),
                                html.P("*Note: Submitting the changes only updates the mixed chart & the statistical tables, it DOES NOT save the bins settings until you click the ‘Confirm Binning’ button in Section V.",
                                       style={"lineHeight": "99%", "fontSize": 14}),
                            ], id="categoric_create_new_bin_submit_div"),
                        ], id="categoric_create_new_bin_preview_changes_div", style={"display": "none"}),
                    ],
                    style={
                        "float": "left",
                        "width": "30%",
                        "backgroundColor": "#BCBCDA",
                        "padding": "2%",
                        "borderRadius": dimens["panel-border-radius"],
                    },
                ),
            ], id="categorical_create_new_bin_control_panel", style={"display": "none"}),
            # Categorical Add Elements Control Panel
            html.Div([
                html.Div([
                    SaveButton("Add Elements", inline=True, width="12%"),
                    SaveButton("Split Bin", inline=True,
                               width="9%", marginLeft="0.5%", id="categoric_add_elements_panel_to_split_button"),
                    SaveButton("Rename Bin", inline=True,
                               width="12%", marginLeft="0.5%", id="categoric_add_elements_panel_to_rename_button"),
                ]),
                html.Div(
                    [
                        SectionHeading("Add Elements to the Bin",
                                       center=True, bold=True),
                        html.P("Instructions", style={"fontWeight": "bold"}),
                        html.Ul([
                            html.Li("Enter the new bin name in the text input area, if it is empty, the bin name will remain the same", style={
                                    "fontSize": 14}),
                            html.Li("Select the elements to be added in the new bin from the dropdown menu", style={
                                    "fontSize": 14}),
                            html.Li("Click the ‘Add Elements’ button to preview changes on the bins settings", style={
                                    "fontSize": 14}),
                            html.Li("The selected elements which overlaps with the old bins settings will be automatically removed from the other bins", style={
                                    "fontSize": 14}),
                            html.Li("Once you consider the binning is fine, click the ‘Submit’ button to update the mixed chart & the statistical tables", style={
                                    "fontSize": 14}),
                        ], style={"listStyleType": "square", "lineHeight": "97%"}),
                        html.P("Selected Bin Info: ", style={
                               "fontWeight": "bold"}),
                        # TODO: extract this out
                        html.Div(id="categoric_add_elements_panel_selected_bin_info"),

                        html.P("Enter the new bin name: ",
                               style={"fontWeight": "bold"}),
                        dcc.Input(style={"marginBottom": 10}, id="categoric_add_elements_panel_name_input"),
                        html.P("Select elements to be added into the bin:",
                               style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            options=convert_column_list_to_dropdown_options(
                                ["OWN", "OTHERS"]),  # dummy
                            value=[],
                            multi=True,
                            style={"marginBottom": 13},
                            id="categoric_add_elements_panel_dropdown",
                        ),
                        SaveButton("Add Elements", id="categoric_add_elements_panel_add_button"),
                        html.Div(style={"height": 13}),
                        html.Div([
                            html.Div([], id="categoric_add_elements_panel_changes_div"),
                            html.Div([
                                SaveButton("Submit", inline=True, id="categoric_add_elements_panel_submit_button"),
                                SaveButton("Hide Details", inline=True,
                                           backgroundColor="#8097E6", marginLeft=5, id="categoric_add_elements_panel_hide_details_button"),
                                html.Div(style={"height": 13, "clear": "both"}),
                                html.P("*Note: Submitting the changes only updates the mixed chart & the statistical tables, it DOES NOT save the bins settings until you click the ‘Confirm Binning’ button in Section V.",
                                       style={"lineHeight": "99%", "fontSize": 14}),
                            ], id="categoric_add_elements_panel_submit_div"),
                        ], id="categoric_add_elements_panel_preview_changes_div", style={"display": "none"}),
                    ],
                    style={
                        "marginTop": 13,
                        "float": "left",
                        "width": "30%",
                        "backgroundColor": "#BCBCDA",
                        "padding": "2%",
                        "borderRadius": dimens["panel-border-radius"],
                    },
                ),
            ], id="categorical_add_elements_control_panel", style={"display": "none"}),
            # Categorical Split Bin Control Panel
            html.Div([
                html.Div([
                    SaveButton("Add Elements", inline=True, width="12%", id="categoric_split_panel_add_elements_nav_button"),
                    SaveButton("Split Bin", inline=True,
                               width="9%", marginLeft="0.5%"),
                    SaveButton("Rename Bin", inline=True,
                               width="12%", marginLeft="0.5%", id="categoric_split_panel_rename_nav_button"),
                ]),
                html.Div(
                    [
                        SectionHeading("Split an Existing Bin",
                                       center=True, bold=True),
                        html.P("Instructions", style={"fontWeight": "bold"}),
                        html.Ul([
                            html.Li("Enter the new bin name in the text input area, if it is empty, the elements included in the bin will be used as the bin name", style={
                                    "fontSize": 14}),
                            html.Li("Select the elements to be split out from the old bin", style={
                                    "fontSize": 14}),
                            html.Li("Click the ‘Split Bin’ button to preview changes on the bins settings", style={
                                    "fontSize": 14}),
                            html.Li("Once you consider the binning is fine, click the ‘Submit’ button to update the mixed chart & the statistical tables", style={
                                    "fontSize": 14}),
                        ], style={"listStyleType": "square", "lineHeight": "97%"}),
                        html.P("Selected Bin Info: ", style={
                               "fontWeight": "bold"}),
                        # TODO: extract this out
                        html.Div(id="categoric_split_panel_selected_bin_info"),

                        html.P("Enter the new bin name: ",
                               style={"fontWeight": "bold"}),
                        dcc.Input(style={"marginBottom": 10}, id="categoric_split_panel_new_bin_name_input"),
                        html.P("Select elements to be split out from the bin:", style={
                               "fontWeight": "bold"}),
                        dcc.Dropdown(
                            options=convert_column_list_to_dropdown_options(
                                ["OWN", "OTHERS"]),  # dummy
                            value=[],
                            multi=True,
                            style={"marginBottom": 13},
                            id="categoric_split_panel_dropdown",
                        ),
                        SaveButton("Split Bin", id="categoric_split_panel_split_button"),
                        html.Div(style={"height": 13}),
                        html.Div([
                            html.Div([], id="categoric_split_panel_changes_div"),
                            html.Div([
                                SaveButton("Submit", inline=True, id="categoric_split_panel_submit_button"),
                                SaveButton("Hide Details", inline=True,
                                           backgroundColor="#8097E6", marginLeft=5, id="categoric_split_panel_hide_details_button"),
                                html.Div(style={"height": 13, "clear": "both"}),
                                html.P("*Note: Submitting the changes only updates the mixed chart & the statistical tables, it DOES NOT save the bins settings until you click the ‘Confirm Binning’ button in Section V.",
                                       style={"lineHeight": "99%", "fontSize": 14}),
                            ], id="categoric_split_panel_submit_div"),
                        ], id="categoric_split_panel_preview_changes_div", style={"display": "none"}),
                    ],
                    style={
                        "marginTop": 13,
                        "float": "left",
                        "width": "30%",
                        "backgroundColor": "#BCBCDA",
                        "padding": "2%",
                        "borderRadius": dimens["panel-border-radius"],

                    },

                ),
            ], id="categorical_split_bin_control_panel", style={"display": "none"}),

            # Categorical Rename Bin Control Panel
            html.Div([
                html.Div([
                    SaveButton("Add Elements", inline=True, width="12%", id="categoric_rename_panel_add_elements_nav_button"),
                    SaveButton("Split Bin", inline=True,
                               width="9%", marginLeft="0.5%", id="categoric_rename_panel_split_nav_button"),
                    SaveButton("Rename Bin", inline=True,
                               width="12%", marginLeft="0.5%"),
                ]),
                html.Div(
                    [
                        SectionHeading("Rename Bin", center=True, bold=True),
                        html.P("Instructions", style={"fontWeight": "bold"}),
                        html.Ul([
                            html.Li("Enter the new bin name in the text input area", style={
                                    "fontSize": 14}),
                            html.Li("Click the ‘Rename Bin’ button to preview changes on the bins settings", style={
                                    "fontSize": 14}),
                            html.Li("If nothing is entered in the input when the 'Rename Bin' button is clicked, the bin element(s) would be used as the new bin name", style={
                                    "fontSize": 14}),
                            html.Li("Once you consider the binning is fine, click the ‘Submit’ button to update the mixed chart & the statistical tables", style={
                                    "fontSize": 14}),
                        ], style={"listStyleType": "square", "lineHeight": "97%"}),
                        html.P("Selected Bin Info: ", style={
                               "fontWeight": "bold"}),
                        # TODO: extract this out
                        html.Div(id="categoric_rename_panel_selected_bin_info"),

                        html.P("Enter the new bin name: ",
                               style={"fontWeight": "bold"}),
                        dcc.Input(style={"marginBottom": 10}, id="categoric_rename_panel_new_bin_name_input"),
                        SaveButton("Rename Bin", id="categoric_rename_panel_rename_button"),
                        html.Div(style={"height": 13}),
                        html.Div([
                            html.Div([], id="categoric_rename_panel_changes_div"),
                            html.Div([
                                SaveButton("Submit", inline=True, id="categoric_rename_panel_submit_button"),
                                SaveButton("Hide Details", inline=True,
                                           backgroundColor="#8097E6", marginLeft=5, id="categoric_rename_panel_hide_details_button"),
                                html.Div(style={"height": 13, "clear": "both"}),
                                html.P("*Note: Submitting the changes only updates the mixed chart & the statistical tables, it DOES NOT save the bins settings until you click the ‘Confirm Binning’ button in Section V.",
                                       style={"lineHeight": "99%", "fontSize": 14}),
                            ], id="categoric_rename_panel_submit_div"),
                        ], id="categoric_rename_panel_preview_changes_div", style={"display": "none"})
                    ],
                    style={
                        "marginTop": 13,
                        "float": "left",
                        "width": "30%",
                        "backgroundColor": "#BCBCDA",
                        "padding": "2%",
                        "borderRadius": dimens["panel-border-radius"],

                    },

                ),
            ], id="categorical_rename_bin_control_panel", style={"display": "none"}),

            # Categorical Merge Bins Control Panel
            html.Div([
                html.Div(
                    [
                        SectionHeading("Merge Bins", center=True, bold=True),
                        html.P("Instructions", style={"fontWeight": "bold"}),
                        html.Ul([
                            html.Li("Enter the new bin name in the text input area", style={
                                    "fontSize": 14}),
                            html.Li("Click the ‘Merge Bins’ button to preview changes on the bins settings", style={
                                    "fontSize": 14}),
                            html.Li("Once you consider the binning is fine, click the ‘Submit’ button to update the mixed chart & the statistical tables", style={
                                    "fontSize": 14}),
                        ], style={"listStyleType": "square", "lineHeight": "97%"}),
                        # TODO: extract this out
                        html.P("Selected Bin Info: ", style={"fontWeight": "bold"}),
                        html.Div([], id="categoric_merge_panel_selected_bin_info_div"),

                        html.P("Enter the new bin name: ",
                               style={"fontWeight": "bold"}),
                        dcc.Input(style={"marginBottom": 10}, id="categoric_merge_panel_new_bin_name_input"),
                        SaveButton("Merge Bins", id="categoric_merge_panel_merge_button"),
                        html.Div(style={"height": 13}),
                        html.Div([
                            html.Div([], id="categoric_merge_panel_changes_div"),
                            html.P(id="test_preview"),
                            html.Div([
                                SaveButton("Submit", inline=True, id="categoric_merge_panel_submit_button"),
                                SaveButton("Hide Details", inline=True,
                                           backgroundColor="#8097E6", marginLeft=5, id="categoric_merge_panel_hide_details_button"),
                                html.Div(style={"height": 13, "clear": "both"}),
                                html.P("*Note: Submitting the changes only updates the mixed chart & the statistical tables, it DOES NOT save the bins settings until you click the ‘Confirm Binning’ button in Section V.",
                                       style={"lineHeight": "99%", "fontSize": 14}),
                            ], id="categoric_merge_panel_submit_div"),
                        ], id="categoric_merge_bin_panel_preview_changes_div", style={"display": "none"}),
                    ],
                    style={
                        "float": "left",
                        "width": "30%",
                        "backgroundColor": "#BCBCDA",
                        "padding": "2%",
                        "borderRadius": dimens["panel-border-radius"],

                    },

                ),
            ], id="categorical_merge_bins_control_panel", style={"display": "none"}),

            # Numerical Create New Bin Control Panel
            html.Div([
                html.Div(
                    [
                        SectionHeading("Create a New Bin",
                                       center=True, bold=True),
                        html.P("Instructions", style={"fontWeight": "bold"}),
                        html.Ul([
                            html.Li("Enter the name of the new bin in the text input area", style={
                                    "fontSize": 14}),
                            html.Li("Indicate the ranges that you would like to include in the bin", style={
                                    "fontSize": 14}),
                            html.Li("Click the ‘Create New Bin’ button to preview changes on the bins settings", style={
                                    "fontSize": 14}),
                            html.Li("The indicated ranges which overlaps with the old bins settings will be automatically removed from the other bins", style={
                                    "fontSize": 14}),
                            html.Li("Once you consider the binning is fine, click the ‘Submit’ button to update the mixed chart & the statistical tables", style={
                                    "fontSize": 14}),
                        ], style={"listStyleType": "square", "lineHeight": "97%"}),
                        html.P("Enter the new bin name: ",
                               style={"fontWeight": "bold"}),
                        dcc.Input(style={"marginBottom": 10}, id="numeric_create_new_bin_panel_new_bin_name_input"),
                        html.P("Indicate the ranges to be included in the new bin:", style={
                               "fontWeight": "bold"}),
                        
                        html.Ol([], style={"fontSize": 14}, id="numeric_create_new_bin_panel_range_list"),
                        html.Div([], style={"height": 10, "clear": "both"}),
                        
                        SaveButton("Add", inline=True, id="numeric_create_new_bin_panel_add_button"),
                        SaveButton("Remove", inline=True, marginLeft=8, id="numeric_create_new_bin_panel_remove_button"),
                        html.Div([], style={"clear": "both", "height": 8}),
                        SaveButton("Create New Bin", id="numeric_create_new_bin_panel_create_new_bin_button"),
                        html.Div(style={"height": 13}),
                        html.Div([
                            html.Div([], id="numeric_create_new_bin_panel_changes_div"),
                            SaveButton("Submit", inline=True, id="numeric_create_new_bin_panel_submit_button"),
                            SaveButton("Hide Details", inline=True,
                                       backgroundColor="#8097E6", marginLeft=5, id="numeric_create_new_bin_hide_details_button"),
                            html.Div(style={"height": 13, "clear": "both"}),
                            html.P("*Note: Submitting the changes only updates the mixed chart & the statistical tables, it DOES NOT save the bins settings until you click the ‘Confirm Binning’ button in Section V.",
                                   style={"lineHeight": "99%", "fontSize": 14}),
                        ], id="numeric_create_new_bin_preview_changes_div", style={"display": "none"}),
                        
                    ],
                    style={
                        "float": "left",
                        "width": "30%",
                        "backgroundColor": "#BCBCDA",
                        "padding": "2%",
                        "borderRadius": dimens["panel-border-radius"],
                    },

                ),
            ], id="numerical_create_new_bin_control_panel", style={"display": "none"}),

            # Numerical Adjust Cutpoints Control Panel
            html.Div([
                html.Div([
                    SaveButton("Adjust Cutpoints", inline=True, width="16.5%"),
                    SaveButton("Rename Bin", inline=True,
                               width="16.5%", marginLeft="1%", id="numeric_adjust_cutpoints_panel_rename_nav_button"),
                ]),
                html.Div(
                    [
                        SectionHeading(
                            "Adjust Cutpoints of the Bin", center=True, bold=True),
                        html.P("Instructions", style={"fontWeight": "bold"}),
                        html.Ul([
                            html.Li("Enter the new bin name in the text input area, if it is empty, the bin name will remain the same", style={
                                    "fontSize": 14}),
                            html.Li("Indicate the ranges that you would like to remains in the selected bin", style={
                                    "fontSize": 14}),
                            html.Li("Any ranges in the selected bin not being indicated would be split out as a new bin", style={
                                    "fontSize": 14}),
                            html.Li("The indicated ranges which overlaps with the old bins settings will be automatically removed from the other bins", style={
                                    "fontSize": 14}),
                            html.Li("Once you consider the binning is fine, click the ‘Submit’ button to update the mixed chart & the statistical tables", style={
                                    "fontSize": 14}),
                        ], style={"listStyleType": "square", "lineHeight": "97%"}),
                        html.P("Selected Bin Info: ", style={
                               "fontWeight": "bold"}),
                        # TODO: extract this out
                        html.Div([], id="numeric_adjust_cutpoints_panel_selected_bin_info_div"),

                        html.P("Enter the new bin name: ",
                               style={"fontWeight": "bold"}),
                        dcc.Input(style={"marginBottom": 10}, id="numeric_adjust_cutpoints_panel_new_bin_name_input"),
                        html.P("Indicate the range(s) to be added into the bin:", style={
                               "fontWeight": "bold"}),
                        
                        html.Ol([], style={"fontSize": 14}, id="numeric_adjust_cutpoints_panel_range_list"),
                        html.Div([], style={"height": 10, "clear": "both"}),
                        
                        # TODO!! --> Add dynamic range list
                        SaveButton("Add", inline=True, id="numeric_adjust_cutpoints_panel_add_button"),
                        SaveButton("Remove", inline=True, marginLeft=8, id="numeric_adjust_cutpoints_panel_remove_button"),
                        html.Div([], style={"clear": "both", "height": 8}),
                        SaveButton("Adjust Cutpoints", id="numeric_adjust_cutpoints_panel_adjust_cutpoints_button"),
                        html.Div(style={"height": 13}),
                        html.Div([
                            html.Div([], id="numeric_adjust_cutpoints_panel_changes_div"),
                            SaveButton("Submit", inline=True, id="numeric_adjust_cutpoints_panel_submit_button"),
                            SaveButton("Hide Details", inline=True,
                                       backgroundColor="#8097E6", marginLeft=5, id="numeric_adjust_cutpoints_panel_hide_details_button"),
                            html.Div(style={"height": 13, "clear": "both"}),
                            html.P("*Note: Submitting the changes only updates the mixed chart & the statistical tables, it DOES NOT save the bins settings until you click the ‘Confirm Binning’ button in Section V.",
                                   style={"lineHeight": "99%", "fontSize": 14}),
                        ], id="numeric_adjust_cutpoints_panel_preview_changes_div", style={"display": "none"}),
                    ],
                    style={
                        "marginTop": 13,
                        "float": "left",
                        "width": "30%",
                        "backgroundColor": "#BCBCDA",
                        "padding": "2%",
                        "borderRadius": dimens["panel-border-radius"],
                    },

                ),
            ], id="numerical_adjust_cutpoints_control_panel", style={"display": "none"}),

            # Numerical Rename Bin Control Panel
            html.Div([
                html.Div([
                    SaveButton("Adjust Cutpoints", inline=True, width="16.5%", id="numeric_rename_panel_adjust_cutpoints_nav_button"),
                    SaveButton("Rename Bin", inline=True,
                               width="16.5%", marginLeft="1%"),
                ]),
                html.Div(
                    [
                        SectionHeading("Rename Bin", center=True, bold=True),
                        html.P("Instructions", style={"fontWeight": "bold"}),
                        html.Ul([
                            html.Li("Enter the new bin name in the text input area", style={
                                    "fontSize": 14}),
                            html.Li("Click the ‘Rename Bin’ button to preview changes on the bins settings", style={
                                    "fontSize": 14}),
                            html.Li("If nothing is entered in the input when the 'Rename Bin' button is clicked, the bin range(s) would be used as the new bin name", style={
                                    "fontSize": 14}),
                            html.Li("Once you consider the binning is fine, click the ‘Submit’ button to update the mixed chart & the statistical tables", style={
                                    "fontSize": 14}),
                        ], style={"listStyleType": "square", "lineHeight": "97%"}),
                        html.P("Selected Bin Info: ", style={
                               "fontWeight": "bold"}),
                        # TODO: extract this out
                        html.Div([], id="numeric_rename_panel_selected_bin_info_div"),

                        html.P("Enter the new bin name: ",
                               style={"fontWeight": "bold"}),
                        dcc.Input(style={"marginBottom": 10}, id="numeric_rename_panel_new_bin_name_input"),
                        SaveButton("Rename Bin", id="numeric_rename_panel_rename_button"),
                        html.Div(style={"height": 13}),
                        html.Div([
                            html.Div([], id="numeric_rename_panel_changes_div"),
                            SaveButton("Submit", inline=True),
                            SaveButton("Hide Details", inline=True,
                                       backgroundColor="#8097E6", marginLeft=5, id="numeric_rename_panel_hide_details_button"),
                            html.Div(style={"height": 13, "clear": "both"}),
                            html.P("*Note: Submitting the changes only updates the mixed chart & the statistical tables, it DOES NOT save the bins settings until you click the ‘Confirm Binning’ button in Section V.",
                                   style={"lineHeight": "99%", "fontSize": 14}),
                        ], id="numeric_rename_panel_preview_changes_div", style={"display": "none"}),
                    ],
                    style={
                        "marginTop": 13,
                        "float": "left",
                        "width": "30%",
                        "backgroundColor": "#BCBCDA",
                        "padding": "2%",
                        "borderRadius": dimens["panel-border-radius"],

                    },

                ),
            ], id="numerical_rename_bin_control_panel", style={"display": "none"}),

            # Numerical Merge Bins Control Panel
            html.Div([
                html.Div(
                    [
                        SectionHeading("Merge Bins", center=True, bold=True),
                        html.P("Instructions", style={"fontWeight": "bold"}),
                        html.Ul([
                            html.Li("Enter the new bin name in the text input area", style={
                                    "fontSize": 14}),
                            html.Li("Click the ‘Merge Bins’ button to preview changes on the bins settings", style={
                                    "fontSize": 14}),
                            html.Li("Once you consider the binning is fine, click the ‘Submit’ button to update the mixed chart & the statistical tables", style={
                                    "fontSize": 14}),
                        ], style={"listStyleType": "square", "lineHeight": "97%"}),
                        # TODO: extract this out
                        html.P("Selected Bin Info: ", style={
                               "fontWeight": "bold"}),
                        html.Div([], id="numeric_merge_panel_selected_bin_info_div"),
                        html.P("Enter the new bin name: ",
                               style={"fontWeight": "bold"}),
                        dcc.Input(style={"marginBottom": 10}, id="numeric_merge_panel_new_bin_name_input"),

                        SaveButton("Merge Bins", id="numeric_merge_panel_merge_button"),
                        html.Div(style={"height": 13}),
                        html.Div([
                            html.Div([], id="numeric_merge_panel_changes_div"),
                            SaveButton("Submit", inline=True),
                            SaveButton("Hide Details", inline=True,
                                       backgroundColor="#8097E6", marginLeft=5, id="numeric_merge_panel_hide_details_button"),
                            html.Div(style={"height": 13, "clear": "both"}),
                            html.P("*Note: Submitting the changes only updates the mixed chart & the statistical tables, it DOES NOT save the bins settings until you click the ‘Confirm Binning’ button in Section V.",
                                   style={"lineHeight": "99%", "fontSize": 14}),
                        ], id="numeric_merge_panel_preview_changes_div", style={"display": "none"}),
                    ],
                    style={
                        "float": "left",
                        "width": "30%",
                        "backgroundColor": "#BCBCDA",
                        "padding": "2%",
                        "borderRadius": dimens["panel-border-radius"],
                    },

                ),
            ], id="numerical_merge_bins_control_panel", style={"display": "none"}),
        ]
    ),
    html.P(id="test_select"),
    html.P(id="test_click"),
    html.Div([], style={"width": "100%", "height": 25, "clear": "left"}),
    html.Div(
        [
            SectionHeading("IV. Monitor Bins Performance (Before)"),
            html.Div([], id="stat_table_before"),
        ],
        style=grey_full_width_panel_style,
    ),
    html.Div([], style={"width": "100%", "height": 25, "clear": "left"}),
    html.Div(
        [
            SectionHeading("V. Monitor Bins Performance (After)"),
            html.Div([], id="stat_table_after"),
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
])


preview_download_page_layout = html.Div(
    [
        NavBar(),
        Heading("Preview & Download Bins Settings"),

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
Good/Bad Definition:
Add/Remove definition from bad numerical list
"""


@app.callback(
    Output("bad_numeric_def_list", "children"),
    [
        Input("add_bad_numeric_def_button", "n_clicks"),
        Input("bad_numeric_def_remove_button", "n_clicks"),
    ],
    [
        State("numerical_columns", "data"),
        State({"index": ALL, "type": "bad_numerical_lower"}, "value"),
        State({"index": ALL, "type": "bad_numerical_upper"}, "value"),
        State({"index": ALL, "type": "bad_numerical_column"}, "value"),
        State({"index": ALL, "type": "bad_numerical_checkbox"}, "value"),
    ],
)
def edit_bad_numeric_def_list(add_clicks, remove_clicks_list, numeric_col_data, lower_list, upper_list, column_list, checkbox_list):
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    adding = len([i for i in triggered if i ==
                 "add_bad_numeric_def_button.n_clicks"])
    removing = len([i for i in triggered if i ==
                   "bad_numeric_def_remove_button.n_clicks"])
    new_spec = [
        (column, lower, upper, selected) for column, lower, upper, selected in zip(column_list, lower_list, upper_list, checkbox_list)
        if not (removing and selected)
    ]
    if adding:
        new_spec.append((json.loads(numeric_col_data)[0], 0, 1, []))
    new_list = [
        html.Div(
            [
                html.P(str(idx+1) + ".",
                       style={"float": "left", "marginRight": 5}),
                dcc.Dropdown(
                    options=convert_column_list_to_dropdown_options(
                        json.loads(numeric_col_data)),
                    value=column,
                    clearable=False,
                    searchable=False,
                    style={"width": 180},
                    id={"index": idx, "type": "bad_numerical_column"},
                ),
                html.P(
                    " :", style={"float": "left", "marginLeft": 5, "fontWeight": "bold"}
                ),
                dcc.Input(
                    type="number",
                    min=0,
                    value=lower,
                    id={"index": idx, "type": "bad_numerical_lower"},
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
                    id={"index": idx, "type": "bad_numerical_upper"},
                    style={"width": 150, "float": "left", "marginLeft": 10},
                ),
                html.P(
                    "(exclusive)  ",
                    style={"float": "left", "marginLeft": 5, "marginBottom": 0},
                ),
                dcc.Checklist(
                    id={"index": idx, "type": "bad_numerical_checkbox"},
                    options=[{"label": "", "value": "selected"}],
                    value=selected,
                    style={"display": "inline", "marginLeft": 15},
                ),
            ],
            style={"display": "flex", "alignItems": "flex-end", "marginTop": 10},
        )
        for idx, (column, lower, upper, selected) in enumerate(new_spec)
    ]
    return new_list


"""
Good/Bad Definition:
Add/Remove definition from indeterminate numerical list
"""


@app.callback(
    Output("indeterminate_numeric_def_list", "children"),
    [
        Input("add_indeterminate_numeric_def_button", "n_clicks"),
        Input("indeterminate_numeric_def_remove_button", "n_clicks"),
    ],
    [
        State("numerical_columns", "data"),
        State({"index": ALL, "type": "indeterminate_numerical_lower"}, "value"),
        State({"index": ALL, "type": "indeterminate_numerical_upper"}, "value"),
        State({"index": ALL, "type": "indeterminate_numerical_column"}, "value"),
        State({"index": ALL, "type": "indeterminate_numerical_checkbox"}, "value"),
    ],
)
def edit_indeterminate_numeric_def_list(add_clicks, remove_clicks_list, numeric_col_data, lower_list, upper_list, column_list, checkbox_list):
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    adding = len([i for i in triggered if i ==
                 "add_indeterminate_numeric_def_button.n_clicks"])
    removing = len([i for i in triggered if i ==
                   "indeterminate_numeric_def_remove_button.n_clicks"])
    new_spec = [
        (column, lower, upper, selected) for column, lower, upper, selected in zip(column_list, lower_list, upper_list, checkbox_list)
        if not (removing and selected)
    ]
    if adding:
        new_spec.append((json.loads(numeric_col_data)[0], 0, 1, []))
    new_list = [
        html.Div(
            [
                html.P(str(idx+1) + ".",
                       style={"float": "left", "marginRight": 5}),
                dcc.Dropdown(
                    options=convert_column_list_to_dropdown_options(
                        json.loads(numeric_col_data)),
                    value=column,
                    clearable=False,
                    searchable=False,
                    style={"width": 180},
                    id={"index": idx, "type": "indeterminate_numerical_column"},
                ),
                html.P(
                    " :", style={"float": "left", "marginLeft": 5, "fontWeight": "bold"}
                ),
                dcc.Input(
                    type="number",
                    min=0,
                    value=lower,
                    id={"index": idx, "type": "indeterminate_numerical_lower"},
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
                    id={"index": idx, "type": "indeterminate_numerical_upper"},
                    style={"width": 150, "float": "left", "marginLeft": 10},
                ),
                html.P(
                    "(exclusive)  ",
                    style={"float": "left", "marginLeft": 5, "marginBottom": 0},
                ),
                dcc.Checklist(
                    id={"index": idx, "type": "indeterminate_numerical_checkbox"},
                    options=[{"label": "", "value": "selected"}],
                    value=selected,
                    style={"display": "inline", "marginLeft": 15},
                ),
            ],
            style={"display": "flex", "alignItems": "flex-end", "marginTop": 10},
        )
        for idx, (column, lower, upper, selected) in enumerate(new_spec)
    ]
    return new_list


"""
Good/Bad Definition:
Add/Remove definition from bad categorical list
"""


@app.callback(
    Output("bad_categoric_def_list", "children"),
    [
        Input("add_bad_categoric_def_button", "n_clicks"),
        Input("bad_categoric_def_remove_button", "n_clicks"),
    ],
    [
        State("categorical_columns", "data"),
        State({"index": ALL, "type": "bad_categorical_element"}, "value"),
        State({"index": ALL, "type": "bad_categorical_column"}, "value"),
        State({"index": ALL, "type": "bad_categorical_checkbox"}, "value"),
    ],
)
def edit_bad_categoric_def_list(add_clicks, remove_clicks_list, categoric_col_data, elements_list, column_list, checkbox_list):
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    adding = len([i for i in triggered if i ==
                 "add_bad_categoric_def_button.n_clicks"])
    removing = len([i for i in triggered if i ==
                   "bad_categoric_def_remove_button.n_clicks"])
    new_spec = [
        (column, elements, selected) for column, elements, selected in zip(column_list, elements_list, checkbox_list)
        if not (removing and selected)
    ]
    if adding:
        new_spec.append((json.loads(categoric_col_data)[0], [], []))
    new_list = [
        html.Div([
            html.P(str(idx+1) + ".",
                   style={"float": "left", "marginRight": 5}),
            dcc.Dropdown(
                options=convert_column_list_to_dropdown_options(
                    json.loads(categoric_col_data)),
                value=column,
                clearable=False,
                searchable=False,
                style={"width": 180},
                id={"index": idx, "type": "bad_categorical_column"},
            ),
            html.P(
                " :", style={"float": "left", "marginLeft": 5, "fontWeight": "bold", "marginRight": 10}
            ),
            dcc.Dropdown(
                options=convert_column_list_to_dropdown_options(
                    df[column].unique()),
                value=elements,
                multi=True,
                style={"width": 500},
                id={"index": idx, "type": "bad_categorical_element"},
            ),
            dcc.Checklist(
                id={"index": idx, "type": "bad_categorical_checkbox"},
                options=[{"label": "", "value": "selected"}],
                value=selected,
                style={"display": "inline", "marginLeft": 15},
            )
        ], style={"display": "flex", "alignItems": "flex-end", "marginTop": 10})
        for idx, (column, elements, selected) in enumerate(new_spec)
    ]
    return new_list


"""
Good/Bad Definition:
Add/Remove definition from indeterminate categorical list
"""


@app.callback(
    Output("indeterminate_categoric_def_list", "children"),
    [
        Input("add_indeterminate_categoric_def_button", "n_clicks"),
        Input("indeterminate_categoric_def_remove_button", "n_clicks"),
    ],
    [
        State("categorical_columns", "data"),
        State({"index": ALL, "type": "indeterminate_categorical_element"}, "value"),
        State({"index": ALL, "type": "indeterminate_categorical_column"}, "value"),
        State({"index": ALL, "type": "indeterminate_categorical_checkbox"}, "value"),
    ],
)
def edit_indeterminate_categoric_def_list(add_clicks, remove_clicks_list, categoric_col_data, elements_list, column_list, checkbox_list):
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    adding = len([i for i in triggered if i ==
                 "add_indeterminate_categoric_def_button.n_clicks"])
    removing = len([i for i in triggered if i ==
                   "indeterminate_categoric_def_remove_button.n_clicks"])
    new_spec = [
        (column, elements, selected) for column, elements, selected in zip(column_list, elements_list, checkbox_list)
        if not (removing and selected)
    ]
    if adding:
        new_spec.append((json.loads(categoric_col_data)[0], [], []))
    new_list = [
        html.Div([
            html.P(str(idx+1) + ".",
                   style={"float": "left", "marginRight": 5}),
            dcc.Dropdown(
                options=convert_column_list_to_dropdown_options(
                    json.loads(categoric_col_data)),
                value=column,
                clearable=False,
                searchable=False,
                style={"width": 180},
                id={"index": idx, "type": "indeterminate_categorical_column"},
            ),
            html.P(
                " :", style={"float": "left", "marginLeft": 5, "fontWeight": "bold", "marginRight": 10}
            ),
            dcc.Dropdown(
                options=convert_column_list_to_dropdown_options(
                    df[column].unique()),
                value=elements,
                multi=True,
                style={"width": 500},
                id={"index": idx, "type": "indeterminate_categorical_element"},
            ),
            dcc.Checklist(
                id={"index": idx, "type": "indeterminate_categorical_checkbox"},
                options=[{"label": "", "value": "selected"}],
                value=selected,
                style={"display": "inline", "marginLeft": 15},
            )
        ], style={"display": "flex", "alignItems": "flex-end", "marginTop": 10})
        for idx, (column, elements, selected) in enumerate(new_spec)
    ]
    return new_list


"""
Good/Bad Definition:
Change categorical multi-value dropdown based on changes in column choice for
bad categorical definitions
"""


@app.callback(
    [
        Output({"index": MATCH, "type": "bad_categorical_element"}, "options"),
        Output({"index": MATCH, "type": "bad_categorical_element"}, "value"),
    ],
    Input({"index": MATCH, "type": "bad_categorical_column"}, "value"),
    State({"index": MATCH, "type": "bad_categorical_element"}, "value"),
)
def update_multi_value_dropdown_bad_categorical(column, elements):
    options = convert_column_list_to_dropdown_options(df[column].unique())
    value = elements
    for element in elements:
        if element not in df[column].unique():
            value = []
            break
    return [options, value]


"""
Good/Bad Definition:
Change categorical multi-value dropdown based on changes in column choice for
indeterminate categorical definitions
"""


@app.callback(
    [
        Output(
            {"index": MATCH, "type": "indeterminate_categorical_element"}, "options"),
        Output({"index": MATCH, "type": "indeterminate_categorical_element"}, "value"),
    ],
    Input({"index": MATCH, "type": "indeterminate_categorical_column"}, "value"),
    State({"index": MATCH, "type": "indeterminate_categorical_element"}, "value"),
)
def update_multi_value_dropdown_bad_categorical(column, elements):
    options = convert_column_list_to_dropdown_options(df[column].unique())
    value = elements
    for element in elements:
        if element not in df[column].unique():
            value = []
            break
    return [options, value]


"""
Good/Bad Definition
Save good bad definition to storage when confirm button is clicked
"""


@app.callback(
    Output("good_bad_def", "data"),
    Input("confirm_good_bad_def_button", "n_clicks"),
    [
        State({"index": ALL, "type": "bad_numerical_column"}, "value"),
        State({"index": ALL, "type": "bad_numerical_lower"}, "value"),
        State({"index": ALL, "type": "bad_numerical_upper"}, "value"),
        State({"index": ALL, "type": "indeterminate_numerical_column"}, "value"),
        State({"index": ALL, "type": "indeterminate_numerical_lower"}, "value"),
        State({"index": ALL, "type": "indeterminate_numerical_upper"}, "value"),
        State({"index": ALL, "type": "bad_categorical_column"}, "value"),
        State({"index": ALL, "type": "bad_categorical_element"}, "value"),
        State({"index": ALL, "type": "indeterminate_categorical_column"}, "value"),
        State({"index": ALL, "type": "indeterminate_categorical_element"}, "value"),
        State("weight_of_bad_input", "value"),
        State("weight_of_good_input", "value"),
    ],
)
def save_good_bad_def_to_storage(n_clicks, bad_numerical_column_list, bad_numerical_lower_list, bad_numerical_upper_list, indeterminate_numerical_column_list, indeterminate_numerical_lower_list, indeterminate_numerical_upper_list, bad_categorical_column_list, bad_categorical_element_list, indeterminate_categorical_column_list, indeterminate_categorical_element_list, bad_weight, good_weight):
    validator = GoodBadDefValidator()

    # Validate if weights are numeric & non-negative
    if bad_weight == None or good_weight == None:
        raisePreventUpdate

    # Validate numerical boundaries of user input, if invalid, return original definition
    bad_numeric_info_list = tuple(zip(
        bad_numerical_column_list, bad_numerical_lower_list, bad_numerical_upper_list))
    indeterminate_numeric_info_list = tuple(zip(
        indeterminate_numerical_column_list, indeterminate_numerical_lower_list, indeterminate_numerical_upper_list))
    if not validator.validate_numerical_bounds(bad_numeric_info_list) or not validator.validate_numerical_bounds(indeterminate_numeric_info_list):
        raise PreventUpdate

    # Numerical boundaries of user input are valid, prepare data here
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

    bad_categorical_info_list = zip(
        bad_categorical_column_list, bad_categorical_element_list)
    indeterminate_categorical_info_list = zip(
        indeterminate_categorical_column_list, indeterminate_categorical_element_list)

    # Update data
    good_bad_def["bad"]["numerical"] = GoodBadDefDecoder.get_numeric_def_list_from_section(
        numeric_info_list=bad_numeric_info_list)
    good_bad_def["indeterminate"]["numerical"] = GoodBadDefDecoder.get_numeric_def_list_from_section(
        numeric_info_list=indeterminate_numeric_info_list)
    good_bad_def["bad"]["categorical"] = GoodBadDefDecoder.get_categorical_def_list_from_section(
        categoric_info_list=bad_categorical_info_list)
    good_bad_def["indeterminate"]["categorical"] = GoodBadDefDecoder.get_categorical_def_list_from_section(
        categoric_info_list=indeterminate_categorical_info_list)

    # Validate if there's overlapping between bad & indeterminate
    if not validator.validate_if_numerical_def_overlapped(good_bad_def["bad"]["numerical"], good_bad_def["indeterminate"]["numerical"]):
        raise PreventUpdate
    if not validator.validate_if_categorical_def_overlapped(good_bad_def["bad"]["categorical"], good_bad_def["indeterminate"]["categorical"]):
        raise PreventUpdate

    # If no definitions defined, do not update
    if len(good_bad_def["bad"]["numerical"]) == 0 and len(good_bad_def["indeterminate"]["numerical"]) == 0 and len(good_bad_def["bad"]["categorical"]) == 0 and len(good_bad_def["indeterminate"]["categorical"]) == 0:
        raise PreventUpdate

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
        State({"index": ALL, "type": "bad_numerical_column"}, "value"),
        State({"index": ALL, "type": "bad_numerical_lower"}, "value"),
        State({"index": ALL, "type": "bad_numerical_upper"}, "value"),
        State({"index": ALL, "type": "indeterminate_numerical_column"}, "value"),
        State({"index": ALL, "type": "indeterminate_numerical_lower"}, "value"),
        State({"index": ALL, "type": "indeterminate_numerical_upper"}, "value"),
        State({"index": ALL, "type": "bad_categorical_column"}, "value"),
        State({"index": ALL, "type": "bad_categorical_element"}, "value"),
        State({"index": ALL, "type": "indeterminate_categorical_column"}, "value"),
        State({"index": ALL, "type": "indeterminate_categorical_element"}, "value"),
        State("weight_of_bad_input", "value"),
        State("weight_of_good_input", "value"),
    ],
    prevent_initial_call=True,
)
def show_good_bad_def_error_msg(n_clicks, bad_numerical_column_list, bad_numerical_lower_list, bad_numerical_upper_list, indeterminate_numerical_column_list, indeterminate_numerical_lower_list, indeterminate_numerical_upper_list, bad_categorical_column_list, bad_categorical_element_list, indeterminate_categorical_column_list, indeterminate_categorical_element_list, bad_weight, good_weight):
    error_msg = ""

    # Validate if weights are numeric & non-negative
    if bad_weight == None or good_weight == None:
        error_msg += "Error (Invalid User Input): Weights have to be a non-negative number.\t"

    has_bound_error = False
    validator = GoodBadDefValidator()

    bad_numeric_info_list = tuple(zip(
        bad_numerical_column_list, bad_numerical_lower_list, bad_numerical_upper_list))
    indeterminate_numeric_info_list = tuple(zip(
        indeterminate_numerical_column_list, indeterminate_numerical_lower_list, indeterminate_numerical_upper_list))

    if not validator.validate_numerical_bounds(bad_numeric_info_list):
        has_bound_error = True
        error_msg += "Error (Invalid User Input): Some of the numerical range(s) for bad definition has lower bound >= upper bound which is invalid.\t"
    if not validator.validate_numerical_bounds(indeterminate_numeric_info_list):
        has_bound_error = True
        error_msg += "Error (Invalid User Input): Some of the numerical range(s) for indeterminate definition has lower bound >= upper bound which is invalid.\t"

    bad_categorical_info_list = zip(
        bad_categorical_column_list, bad_categorical_element_list)
    indeterminate_categorical_info_list = zip(
        indeterminate_categorical_column_list, indeterminate_categorical_element_list)

    bad_numeric_list = GoodBadDefDecoder.get_numeric_def_list_from_section(
        numeric_info_list=bad_numeric_info_list)
    indeterminate_numeric_list = GoodBadDefDecoder.get_numeric_def_list_from_section(
        numeric_info_list=indeterminate_numeric_info_list)

    if not has_bound_error and not validator.validate_if_numerical_def_overlapped(bad_numeric_list, indeterminate_numeric_list):
        error_msg += "Error (Invalid User Input): Some of the numerical definitions of bad & indeterminate have overlapped.\t"

    bad_categoric_list = GoodBadDefDecoder.get_categorical_def_list_from_section(
        categoric_info_list=bad_categorical_info_list)
    indeterminate_categoric_list = GoodBadDefDecoder.get_categorical_def_list_from_section(
        categoric_info_list=indeterminate_categorical_info_list)
    if not validator.validate_if_categorical_def_overlapped(bad_categoric_list, indeterminate_categoric_list):
        error_msg += "Error (Invalid User Input): Some of the categorical definitions of bad & indeterminate have overlapped.\t"

    if len(bad_numeric_list) == 0 and len(indeterminate_numeric_list) == 0 and len(bad_categoric_list) == 0 and len(indeterminate_categoric_list) == 0:
        error_msg += "Error: Definitions should not be empty."

    return error_msg


"""
Good/Bad Definition Page:
Show statistics & bar chart to show total good/indeterminate/bad
in the whole dataset after the user clicked on the confirm button
"""


@app.callback(
    Output("good_bad_stat_section", "children"),
    Input("good_bad_def", "data"),
)
def show_good_bad_stats_and_bar_chart(good_bad_def_data):
    # Get good bad definitions
    good_bad_def = json.loads(good_bad_def_data)

    # Check if there's definition defined, if not, return nothing
    if len(good_bad_def["bad"]["numerical"]) == 0 and len(good_bad_def["bad"]["categorical"]) == 0 and len(good_bad_def["indeterminate"]["numerical"]) == 0 and len(good_bad_def["bad"]["categorical"]) == 0 and len(good_bad_def["indeterminate"]["categorical"]) == 0:
        return []

    # Compute statistics
    sample_bad_count, sample_indeterminate_count, sample_good_count, good_weight, bad_weight, population_good_count, population_bad_count = GoodBadCounter.get_statistics(
        df, good_bad_def)

    # Prepare bar chart
    fig = {
        "data": [
            {
                "x": ["Good", "Bad"],
                "y": [population_good_count, population_bad_count],
                "type": "bar",
                "marker": {"color": "#6B87AB"},
            },
        ],
        "layout": {"title": "Total Population Good & Bad Counts"},
    }

    # Return layout
    return html.Div([
        SectionHeading("V. Monitor Total Good Bad Counts in the Dataset"),
        html.Div([
            html.P("Sample Good Count: " + str(sample_good_count)),
            html.P("Sample Indeterminate Count: " +
                   str(sample_indeterminate_count)),
            html.P("Sample Bad Count: " + str(sample_bad_count)),
            html.Div([], style={"height": 8}),
            html.P("Weight of Good: " + str(good_weight)),
            html.P("Weight of Bad: " + str(bad_weight)),
            html.Div([], style={"height": 8}),
            html.P("Population Good Count: " +
                   str(int(population_good_count))),
            html.P("Population Bad Count: " + str(int(population_bad_count))),
        ], style=purple_panel_style),
        html.Div([
            dcc.Graph(figure=fig),
        ], style=grey_panel_style),
    ])


"""
Interactive Binning Page:
Render the data stored in shared storage about the predictor variables to be 
binned (which is set by user in the confirm input dataset page),
the options available in the dropdown showing the predictor variable can be binned in the Interactive 
Binning page is updated
"""


@app.callback(
    [
        Output("predictor_var_ib_dropdown", "options"),
        Output("predictor_var_ib_dropdown", "value"),
    ],
    [
        Input("numerical_columns", "data"),
        Input("categorical_columns", "data"),
    ]
)
def update_ib_predictor_var_dropdown(numerical_col, categorical_col):
    var_to_be_bin_list = json.loads(
        numerical_col) + json.loads(categorical_col)
    return [convert_column_list_to_dropdown_options(var_to_be_bin_list), var_to_be_bin_list[0]]


"""
Interactive Binning Page:
Reset automated binning panel based on variable to 
be binned
"""


@app.callback(
    [
        Output("auto_bin_algo_dropdown", "value"),
        Output("auto_bin_algo_dropdown", "options"),
        Output("equal_width_radio_button", "value"),
        Output("equal_width_width_input", "value"),
        Output("equal_width_num_bin_input", "value"),
        Output("equal_freq_radio_button", "value"),
        Output("equal_freq_freq_input", "value"),
        Output("equal_freq_num_bin_input", "value"),
    ],
    Input("predictor_var_ib_dropdown", "value"),
    State("bins_settings", "data"),
)
def update_auto_bin_panel_on_bin_var_change(var_to_bin, bins_settings_data):
    bins_settings_dict = json.loads(bins_settings_data)
    bins_settings_list = bins_settings_dict["variable"]
    dtype = None
    for var in bins_settings_list:
        if var["column"] == var_to_bin:
            dtype = var["type"]

    if dtype == "categorical":
        options = [
            {"label": "No Binnings", "value": "none"},
        ]
        return ["none", options, "width", 1, 10, "frequency", 1000, 10]
    else:
        options = [
            {"label": "No Binnings", "value": "none"},
            {"label": "Equal Width", "value": "equal width"},
            {
                "label": "Equal Frequency",
                "value": "equal frequency",
            },
        ]
        return ["none", options, "width", 1, 10, "frequency", 1000, 10]


"""
Interactive Binning Page:
Update automated binning input section UI based on 
automated binning algorithm dropdown value
"""


@app.callback(
    [
        Output("equal_width_input_section", "style"),
        Output("equal_frequency_input_section", "style"),
    ],
    Input("auto_bin_algo_dropdown", "value"),
)
def update_auto_bin_input_section_UI(auto_bin_algo):
    if auto_bin_algo == "none":
        return {"display": "none"}, {"display": "none"}
    elif auto_bin_algo == "equal width":
        return {}, {"display": "none"}
    else:  # equal frequency
        return {"display": "none"}, {}


"""
Interactive Binning Page:
Change the automated binning algorithm description based on 
the user-selected algorithm
"""


@app.callback(
    dash.dependencies.Output("auto_bin_algo_description", "children"),
    dash.dependencies.Input("auto_bin_algo_dropdown", "value"),
)
def update_auto_bin_algo_description(selected_algo):
    if selected_algo == "none":
        return "*Regards each unique value in the dataset as a bin"
    elif selected_algo == "equal width":
        return "*Divides the range of value with predetermined width OR into predetermined number of equal width bins"
    else:  # equal frequency
        return "*Divides the data into a predetermined number of bins containing approximately the same number of observations"


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
Interactive Binning Page:
Initialize temp_bins_settings when user 
- Select predictor var to bin
- Update temp_bins_settings when user clicks on 
refresh button in automated binning panel
- Click categoric create new bin submit button
- Click categoric add elements submit button
- Click categoric split bin submit button [TBC]
- Click categoric rename bin submit button
- Click categoric merge bins submit button
"""


@app.callback(
    [
        Output("temp_col_bins_settings", "data"),
        Output("temp_binned_col", "data"),
    ],
    [
        Input("predictor_var_ib_dropdown", "value"),
        Input("auto_bin_refresh_button", "n_clicks"),
        Input("categoric_create_new_bin_submit_button", "n_clicks"),
        Input("categoric_rename_panel_submit_button", "n_clicks"),
        Input("categoric_add_elements_panel_submit_button", "n_clicks"),
        Input("categoric_merge_panel_submit_button", "n_clicks"),
        Input("categoric_split_panel_submit_button", "n_clicks"),
    ],
    [
        State("bins_settings", "data"),
        State("auto_bin_algo_dropdown", "value"),
        State("equal_width_radio_button", "value"),
        State("equal_width_width_input", "value"),
        State("equal_width_num_bin_input", "value"),
        State("equal_freq_radio_button", "value"),
        State("equal_freq_freq_input", "value"),
        State("equal_freq_num_bin_input", "value"),
        State("temp_col_bins_settings", "data"),
        State("categoric_create_new_bin_name_input", "value"),
        State("categoric_create_new_bin_dropdown", "value"),
        State("categoric_rename_panel_new_bin_name_input", "value"),
        State("mixed_chart", "clickData"),
        State("categoric_add_elements_panel_name_input", "value"),
        State("categoric_add_elements_panel_dropdown", "value"),
        State("categoric_merge_panel_new_bin_name_input", "value"),
        State("mixed_chart", "selectedData"),
        State("categoric_split_panel_new_bin_name_input", "value"),
        State("categoric_split_panel_dropdown", "value"),
    ],
)
def update_temp_bins_settings(var_to_bin, n_clicks, n_clicks2, n_clicks3, n_clicks4, n_clicks5, n_clicks6, bins_settings_data, auto_bin_algo, equal_width_method, width, ew_num_bins, equal_freq_method, freq, ef_num_bins, temp_col_bins_settings_data, categoric_create_new_bin_name_input, categoric_create_new_bin_dropdown, categoric_rename_panel_new_bin_name_input, click_data, categoric_add_elements_panel_name_input, categoric_add_elements_panel_dropdown, categoric_merge_panel_new_bin_name_input, selected_data, categoric_split_panel_new_bin_name_input, categoric_split_panel_dropdown):
    triggered = dash.callback_context.triggered
    
    if triggered[0]['prop_id'] == "categoric_create_new_bin_submit_button.n_clicks":
        temp_col_bins_settings = json.loads(temp_col_bins_settings_data)
        
        new_settings, _, __ = InteractiveBinningMachine.categoric_create_new_bin(new_bin_name=categoric_create_new_bin_name_input, new_bin_element_li=categoric_create_new_bin_dropdown, temp_col_bins_settings=temp_col_bins_settings)

        def_li, binned_series = BinningMachine.perform_binning_on_col(
        df.loc[:, [new_settings["column"]]], new_settings)
        temp_df = df.copy()
        temp_df['binned_col'] = binned_series.values
        
        return [json.dumps(new_settings), json.dumps(temp_df.to_dict())]
        
    if triggered[0]['prop_id'] == "categoric_rename_panel_submit_button.n_clicks":
        temp_col_bins_settings = json.loads(temp_col_bins_settings_data)
        
        new_settings, _, __ = InteractiveBinningMachine.categoric_rename_bin(selected_bin_name=click_data["points"][0]["x"], new_bin_name=categoric_rename_panel_new_bin_name_input, temp_col_bins_settings=temp_col_bins_settings)
        
        def_li, binned_series = BinningMachine.perform_binning_on_col(
        df.loc[:, [new_settings["column"]]], new_settings)
        temp_df = df.copy()
        temp_df['binned_col'] = binned_series.values
        
        return [json.dumps(new_settings), json.dumps(temp_df.to_dict())]
    
    if triggered[0]['prop_id'] == "categoric_add_elements_panel_submit_button.n_clicks":
        temp_col_bins_settings = json.loads(temp_col_bins_settings_data)
        
        new_settings, _, __ = InteractiveBinningMachine.categoric_add_elements(selected_bin_name=click_data["points"][0]["x"], new_bin_name=categoric_add_elements_panel_name_input, elements_to_add_li=categoric_add_elements_panel_dropdown, temp_col_bins_settings=temp_col_bins_settings)
        
        def_li, binned_series = BinningMachine.perform_binning_on_col(
        df.loc[:, [new_settings["column"]]], new_settings)
        temp_df = df.copy()
        temp_df['binned_col'] = binned_series.values
        
        return [json.dumps(new_settings), json.dumps(temp_df.to_dict())]
    
    if triggered[0]['prop_id'] == "categoric_merge_panel_submit_button.n_clicks":
        temp_col_bins_settings = json.loads(temp_col_bins_settings_data)
    
        selected_bin_name_set = set()
        for point in selected_data["points"]:
            selected_bin_name_set.add(point["x"])
        selected_bin_name_li = list(selected_bin_name_set)

        new_settings, _, __ = InteractiveBinningMachine.categoric_merge_bins(selected_bin_name_li=selected_bin_name_li, new_bin_name=categoric_merge_panel_new_bin_name_input, temp_col_bins_settings=temp_col_bins_settings)
    
        def_li, binned_series = BinningMachine.perform_binning_on_col(
        df.loc[:, [new_settings["column"]]], new_settings)
        temp_df = df.copy()
        temp_df['binned_col'] = binned_series.values
        
        return [json.dumps(new_settings), json.dumps(temp_df.to_dict())]
    
    if triggered[0]['prop_id'] == "categoric_split_panel_submit_button.n_clicks":
        temp_col_bins_settings = json.loads(temp_col_bins_settings_data)
    
        new_settings, _, __ = InteractiveBinningMachine.categoric_split_bin(selected_bin_name=click_data["points"][0]["x"], new_bin_name=categoric_split_panel_new_bin_name_input, elements_to_split_out_li=categoric_split_panel_dropdown, temp_col_bins_settings=temp_col_bins_settings)
    
        def_li, binned_series = BinningMachine.perform_binning_on_col(
        df.loc[:, [new_settings["column"]]], new_settings)
        temp_df = df.copy()
        temp_df['binned_col'] = binned_series.values
        
        return [json.dumps(new_settings), json.dumps(temp_df.to_dict())]
    
    bins_settings_dict = json.loads(bins_settings_data)
    bins_settings_list = bins_settings_dict["variable"]
    col_bins_settings = None
    for var in bins_settings_list:
        if var["column"] == var_to_bin:
            col_bins_settings = var
            break

    if triggered[0]['prop_id'] == 'auto_bin_refresh_button.n_clicks':
        if auto_bin_algo == "equal width":
            if equal_width_method == "width":
                col_bins_settings["bins"] = {
                    "algo": "equal width",
                    "method": "width",
                    "value": width,
                }
            else:
                col_bins_settings["bins"] = {
                    "algo": "equal width",
                    "method": "num_bins",
                    "value": ew_num_bins,
                }
        elif auto_bin_algo == "equal frequency":
            if equal_freq_method == "freq":
                col_bins_settings["bins"] = {
                    "algo": "equal frequency",
                    "method": "freq",
                    "value": freq,
                }
            else:
                col_bins_settings["bins"] = {
                    "algo": "equal frequency",
                    "method": "num_bins",
                    "value": ef_num_bins,
                }
        else:  # none
            col_bins_settings["bins"] = "none"

    def_li, binned_series = BinningMachine.perform_binning_on_col(
        df.loc[:, [col_bins_settings["column"]]], col_bins_settings)
    temp_df = df.copy()
    temp_df['binned_col'] = binned_series.values
    
    col_bins_settings["bins"] = def_li
        
    return [json.dumps(col_bins_settings), json.dumps(temp_df.to_dict())]





"""
Interactive Binning Page:
Save chart info including unique_bins, total_count_list,
bad_count_list, and woe_list into storage when temp_binned_col
is updated
"""


@app.callback(
    Output("temp_chart_info", "data"),
    Input("temp_binned_col", "data"),
    State("good_bad_def", "data"),
)
def save_temp_chart_info(temp_binned_col_data, good_bad_def_data):
    temp_binned_col_dict = json.loads(temp_binned_col_data)
    temp_df = pd.DataFrame(temp_binned_col_dict)

    good_bad_def = json.loads(good_bad_def_data)

    unique_bins = sorted(temp_df['binned_col'].unique().tolist())
    total_count_list = get_list_of_total_count(
        temp_df, 'binned_col', unique_bins, good_bad_def)
    bad_count_list = get_list_of_bad_count(
        temp_df,
        'binned_col',
        unique_bins,
        good_bad_def,
    )
    woe_list = get_list_of_woe(
        temp_df, 'binned_col', unique_bins, good_bad_def)

    temp_chart_info_dict = {
        "unique_bins": unique_bins,
        "total_count_list": total_count_list,
        "bad_count_list": bad_count_list,
        "woe_list": woe_list,
    }

    return json.dumps(temp_chart_info_dict)


"""
Interactive Binning Page:
Update mixed chart when user changes the variable 
to be binned
"""


@app.callback(
    Output("mixed_chart", "figure"),
    [
        Input("temp_chart_info", "data"),
        Input("mixed_chart", "clickData"),
        Input("mixed_chart", "selectedData"),
    ],
    [
        State("good_bad_def", "data"),
        State("auto_bin_algo_dropdown", "value"),
        State("equal_width_radio_button", "value"),
        State("equal_width_width_input", "value"),
        State("equal_width_num_bin_input", "value"),
        State("equal_freq_radio_button", "value"),
        State("equal_freq_freq_input", "value"),
        State("equal_freq_num_bin_input", "value"),
    ],
)
def update_mixed_chart_on_var_to_bin_change(temp_chart_info_data, click_data, selected_data, good_bad_def_data, auto_bin_algo, equal_width_method, width, ew_num_bins, equal_freq_method, freq, ef_num_bins):
    triggered = dash.callback_context.triggered

    temp_chart_info = json.loads(temp_chart_info_data)

    clicked_bar_index = None
    selected_bars_index_set = set()

    if click_data is not None and click_data["points"][0]["curveNumber"] != 2:
        clicked_bar_index = click_data["points"][0]["pointIndex"]

    if selected_data is not None:
        for point in selected_data['points']:
            if point['curveNumber'] != 2:
                selected_bars_index_set.add(point['pointIndex'])

    # Clear click data if new graph data is generated
    if triggered[0]['prop_id'] == 'temp_chart_info.data' or (click_data is not None and click_data["points"][0]["curveNumber"] == 2):
        clicked_bar_index = None
        selected_bars_index_set = None

    return generate_mixed_chart_fig(unique_bins=temp_chart_info['unique_bins'], total_count_list=temp_chart_info['total_count_list'], bad_count_list=temp_chart_info['bad_count_list'], woe_list=temp_chart_info['woe_list'], clicked_bar_index=clicked_bar_index, selected_bars_index_set=selected_bars_index_set)


@app.callback(
    [
        Output("mixed_chart", "clickData"),
        Output("mixed_chart", "selectedData"),
    ],
    [
        Input("mixed_chart", "clickData"),
        Input("mixed_chart", "selectedData"),
        Input("predictor_var_ib_dropdown", "value"),
    ],
)
def erase_click_data(click_data, selected_data, var_to_bin):
    if click_data is not None and click_data["points"][0]["curveNumber"] == 2:
        click_data = None
        selected_data = None
    if selected_data is not None:
        click_data = None

    triggered = dash.callback_context.triggered
    if triggered[0]['prop_id'] == 'mixed_chart.clickData':
        selected_data = None
    if triggered[0]['prop_id'] == 'predictor_var_ib_dropdown.value':
        click_data = None
        selected_data = None

    return [click_data, selected_data]


"""
Interactive Binning Page:
Update statistical table (before & after) when user
changes the variable to be binned
"""


@app.callback(
    [
        Output("stat_table_before", "children"),
        Output("stat_table_after", "children"),
    ],
    Input("temp_col_bins_settings", "data"),
    [
        State("good_bad_def", "data"),
        State("stat_table_after", "children"),
    ]
)
def update_stat_tables_on_var_to_bin_change(temp_col_bins_settings_data, good_bad_def_data, stat_table_after):
    col_bins_settings = json.loads(temp_col_bins_settings_data)

    good_bad_def = json.loads(good_bad_def_data)

    stat_cal = StatCalculator(df.copy(), col_bins_settings, good_bad_def)
    stat_df = stat_cal.compute_summary_stat_table()

    return [stat_table_after, [DataTable(stat_df, width=70)]]


"""
Interactive Binning Page:
Update the control panel UI when user changes the 
variable to be binned
"""


@app.callback(
    [
        Output("categorical_create_new_bin_control_panel", "style"),
        Output("categorical_add_elements_control_panel", "style"),
        Output("categorical_split_bin_control_panel", "style"),
        Output("categorical_rename_bin_control_panel", "style"),
        Output("categorical_merge_bins_control_panel", "style"),
        Output("numerical_create_new_bin_control_panel", "style"),
        Output("numerical_adjust_cutpoints_control_panel", "style"),
        Output("numerical_rename_bin_control_panel", "style"),
        Output("numerical_merge_bins_control_panel", "style"),
    ],
    [
        Input("mixed_chart", "clickData"),
        Input("mixed_chart", "selectedData"),
        Input("predictor_var_ib_dropdown", "value"),
        Input("categoric_add_elements_panel_to_split_button", "n_clicks"),
        Input("categoric_add_elements_panel_to_rename_button", "n_clicks"),
        Input("categoric_split_panel_add_elements_nav_button", "n_clicks"),
        Input("categoric_split_panel_rename_nav_button", "n_clicks"),
        Input("categoric_rename_panel_add_elements_nav_button", "n_clicks"),
        Input("categoric_rename_panel_split_nav_button", "n_clicks"),
        Input("numeric_adjust_cutpoints_panel_rename_nav_button", "n_clicks"),
        Input("numeric_rename_panel_adjust_cutpoints_nav_button", "n_clicks"),
    ],
    State("bins_settings", "data"),
)
def update_control_panel_on_var_to_bin_change(click_data, selected_data, var_to_bin, n_clicks, n_clicks2, n_clicks3, n_clicks4, n_clicks5, n_clicks6, n_clicks7, n_clicks8, bins_settings_data):
    triggered = dash.callback_context.triggered

    if triggered[0]['prop_id'] == 'categoric_add_elements_panel_to_split_button.n_clicks':
        return [{"display": "none"}, {"display": "none"}, {}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}]
    if triggered[0]['prop_id'] == 'categoric_add_elements_panel_to_rename_button.n_clicks':
        return [{"display": "none"}, {"display": "none"}, {"display": "none"}, {}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}]
    if triggered[0]['prop_id'] == 'categoric_split_panel_add_elements_nav_button.n_clicks':
        return [{"display": "none"}, {}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}]
    if triggered[0]['prop_id'] == 'categoric_split_panel_rename_nav_button.n_clicks':
        return [{"display": "none"}, {"display": "none"}, {"display": "none"}, {}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}]
    if triggered[0]['prop_id'] == 'categoric_rename_panel_add_elements_nav_button.n_clicks':
        return [{"display": "none"}, {}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}]
    if triggered[0]['prop_id'] == 'categoric_rename_panel_split_nav_button.n_clicks':
        return [{"display": "none"}, {"display": "none"}, {}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}]
    if triggered[0]['prop_id'] == 'numeric_adjust_cutpoints_panel_rename_nav_button.n_clicks':
        return [{"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {}, {"display": "none"}]
    if triggered[0]['prop_id'] == 'numeric_rename_panel_adjust_cutpoints_nav_button.n_clicks':
        return [{"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {}, {"display": "none"}, {"display": "none"}]
    
    bins_settings_dict = json.loads(bins_settings_data)
    bins_settings_list = bins_settings_dict["variable"]
    col_bins_settings = None
    for var in bins_settings_list:
        if var["column"] == var_to_bin:
            col_bins_settings = var
            break

    if col_bins_settings["type"] == "numerical":
        if click_data == None and selected_data == None:
            # Create New Bin
            return [{"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {}, {"display": "none"}, {"display": "none"}, {"display": "none"}]
        elif click_data != None and selected_data == None:
            # Adjust Cutpoints
            return [{"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {}, {"display": "none"}, {"display": "none"}]
        else:
            return [{"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {}]
    else:
        if click_data == None and selected_data == None:
            # Create New Bin
            return [{}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}]
        elif click_data != None and selected_data == None:
            # Add Elements
            return [{"display": "none"}, {}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}]
        else:
            return [{"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {}, {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "none"}]


"""
Interactive Binning Page:
Update categorical create new bin control panel's dropdown 
options and value when user changes the var to bin in predictor
variable dropdown
"""


@app.callback(
    [
        Output("categoric_create_new_bin_dropdown", "options"),
        Output("categoric_create_new_bin_dropdown", "value"),
    ],
    Input("predictor_var_ib_dropdown", "value"),
)
def update_categoric_create_new_bin_dropdown(var_to_bin):
    unique_val_list = sorted(df[var_to_bin].unique().tolist())
    return [convert_column_list_to_dropdown_options(unique_val_list), unique_val_list]


"""
Interactive Binning Page:
Show/Hide categorical create new bin control panel preview changes 
when user clicks on the 'create new bin' button
"""


@app.callback(
    Output("categoric_create_new_bin_preview_changes_div", "style"),
    [
        Input("categoric_create_new_bin_button", "n_clicks"),
        Input("categoric_create_new_bin_hide_details_button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def show_categoric_create_new_bin_preview_changes_div(n_clicks, n_clicks2):
    triggered = dash.callback_context.triggered

    if triggered[0]['prop_id'] == "categoric_create_new_bin_button.n_clicks":
        return {}
    else:
        return {"display": "none"}

    
"""
Interactive Binning Page:
Update categoric create new bin preview changes info
when user clicks on the 'Create New Bin' button
"""
@app.callback(
    [
        Output("categoric_create_new_bin_changes_div", "children"),
        Output("categoric_create_new_bin_submit_div", "style"),
    ],
    Input("categoric_create_new_bin_button", "n_clicks"),
    [
        State("categoric_create_new_bin_name_input", "value"),
        State("categoric_create_new_bin_dropdown", "value"),
        State("temp_col_bins_settings", "data"),
    ],
)
def update_categoric_create_new_bin_preview_changes_info(n_clicks, new_name, bin_element_list, temp_col_bins_settings_data):
    col_bin_settings = json.loads(temp_col_bins_settings_data)
    
    _, old_bin_list, new_bin_list = InteractiveBinningMachine.categoric_create_new_bin(new_bin_name=new_name, new_bin_element_li=bin_element_list, temp_col_bins_settings=col_bin_settings)
    
    style = {}
    if not isinstance(old_bin_list, list) or not isinstance(new_bin_list, list):
        style = {"display": "none"}
    
    return [generate_bin_changes_div_children(old_bin_list=old_bin_list, new_bin_list=new_bin_list, dtype="categorical"), style]


"""
Interactive Binning Page:
Update categoric add elements preview changes info
when user clicks on the 'Add Elements' button
"""
@app.callback(
    [
        Output("categoric_add_elements_panel_changes_div", "children"),
        Output("categoric_add_elements_panel_submit_div", "style"),
    ],
    Input("categoric_add_elements_panel_add_button", "n_clicks"),
    [
        State("categoric_add_elements_panel_name_input", "value"),
        State("categoric_add_elements_panel_dropdown", "value"),
        State("temp_col_bins_settings", "data"),
        State("mixed_chart", "clickData"),
    ],
)
def update_categoric_add_elements_panel_preview_changes_info(n_clicks, new_name, bin_element_list, temp_col_bins_settings_data, click_data):
    col_bin_settings = json.loads(temp_col_bins_settings_data)
    
    _, old_bin_list, new_bin_list = InteractiveBinningMachine.categoric_add_elements(selected_bin_name=click_data["points"][0]["x"], new_bin_name=new_name, elements_to_add_li=bin_element_list, temp_col_bins_settings=col_bin_settings)
    
    style = {}
    if not isinstance(old_bin_list, list) or not isinstance(new_bin_list, list):
        style = {"display": "none"}
    
    return [generate_bin_changes_div_children(old_bin_list=old_bin_list, new_bin_list=new_bin_list, dtype="categorical"), style]

"""
Interactive Binning Page:
Update categoric split preview changes info
when user clicks on the 'Split Bin' button
"""
@app.callback(
    [
        Output("categoric_split_panel_changes_div", "children"),
        Output("categoric_split_panel_submit_div", "style"),
    ],
    Input("categoric_split_panel_split_button", "n_clicks"),
    [
        State("categoric_split_panel_new_bin_name_input", "value"),
        State("categoric_split_panel_dropdown", "value"),
        State("temp_col_bins_settings", "data"),
        State("mixed_chart", "clickData"),
    ],
)
def update_categoric_create_new_bin_preview_changes_info(n_clicks, new_name, bin_element_list, temp_col_bins_settings_data, click_data):
    col_bin_settings = json.loads(temp_col_bins_settings_data)
    
    _, old_bin_list, new_bin_list = InteractiveBinningMachine.categoric_split_bin(selected_bin_name=click_data["points"][0]["x"], new_bin_name=new_name, elements_to_split_out_li=bin_element_list, temp_col_bins_settings=col_bin_settings)
    
    style = {}
    if not isinstance(old_bin_list, list) or not isinstance(new_bin_list, list):
        style = {"display": "none"}
    
    return [generate_bin_changes_div_children(old_bin_list=old_bin_list, new_bin_list=new_bin_list, dtype="categorical"), style]

"""
Interactive Binning Page:
Update categoric merge preview changes info
when user clicks on the 'Merge Bins' button
"""
@app.callback(
    [
        Output("categoric_merge_panel_changes_div", "children"),
        Output("categoric_merge_panel_submit_div", "style"),
    ],
    Input("categoric_merge_panel_merge_button", "n_clicks"),
    [
        State("categoric_merge_panel_new_bin_name_input", "value"),
        State("temp_col_bins_settings", "data"),
        State("mixed_chart", "selectedData"),
    ],
)
def update_categoric_create_new_bin_preview_changes_info(n_clicks, new_name, temp_col_bins_settings_data, selected_data):
    col_bin_settings = json.loads(temp_col_bins_settings_data)
    
    selected_bin_name_set = set()
    for point in selected_data["points"]:
        selected_bin_name_set.add(point["x"])
    selected_bin_name_li = list(selected_bin_name_set)
    
    _, old_bin_list, new_bin_list = InteractiveBinningMachine.categoric_merge_bins(selected_bin_name_li=selected_bin_name_li, new_bin_name=new_name, temp_col_bins_settings=col_bin_settings)
    
    style = {}
    if not isinstance(old_bin_list, list) or not isinstance(new_bin_list, list):
        style = {"display": "none"}
    
    return [generate_bin_changes_div_children(old_bin_list=old_bin_list, new_bin_list=new_bin_list, dtype="categorical"), style]


"""
Interactive Binning Page:
Update numeric create new bin preview changes info
when user clicks on the 'Create New Bin' button
"""
@app.callback(
    Output("numeric_create_new_bin_panel_changes_div", "children"),
    Input("numeric_create_new_bin_panel_create_new_bin_button", "n_clicks"),
    [
        State("numeric_create_new_bin_panel_new_bin_name_input", "value"),
        State("predictor_var_ib_dropdown", "value"),
        State("temp_col_bins_settings", "data"),
    ],
)
def update_numeric_create_new_bin_preview_changes_info(n_clicks, new_name, var_to_bin, temp_col_bins_settings_data):
    col_bin_settings = json.loads(temp_col_bins_settings_data)
    
    #col_bin_list = None
    # If it is no binning OR automated binning, have to translate it to list
    #if isinstance(col_bins_settings["bins"], dict) == True or col_bins_settings["bins"] == "none":
    #    col_bin_list = BinningMachine.convert_auto_bin_def_to_custom_def(col_bins_settings["bins"])
    
    #old_bin_list, new_bin_list = InteractiveBinningMachine.get_categoric_create_new_bin_changes(new_name, bin_element_list, var_to_bin, col_bin_settings)
    
    return generate_bin_changes_div_children(old_bin_list=[["0-20", "[[0, 20)]"], ["30-50", "[[30, 50)]"]], new_bin_list=[["0-50", "[[0, 50)]"]], dtype="numerical")


"""
Interactive Binning Page:
Update numeric adjust cutpoints preview changes info
when user clicks on the 'Adjust Cutpoints' button
"""
@app.callback(
    Output("numeric_adjust_cutpoints_panel_changes_div", "children"),
    Input("numeric_adjust_cutpoints_panel_adjust_cutpoints_button", "n_clicks"),
    [
        State("numeric_adjust_cutpoints_panel_new_bin_name_input", "value"),
        State("predictor_var_ib_dropdown", "value"),
        State("temp_col_bins_settings", "data"),
    ],
)
def update_numeric_create_new_bin_preview_changes_info(n_clicks, new_name, var_to_bin, temp_col_bins_settings_data):
    col_bin_settings = json.loads(temp_col_bins_settings_data)
    
    #col_bin_list = None
    # If it is no binning OR automated binning, have to translate it to list
    #if isinstance(col_bins_settings["bins"], dict) == True or col_bins_settings["bins"] == "none":
    #    col_bin_list = BinningMachine.convert_auto_bin_def_to_custom_def(col_bins_settings["bins"])
    
    #old_bin_list, new_bin_list = InteractiveBinningMachine.get_categoric_create_new_bin_changes(new_name, bin_element_list, var_to_bin, col_bin_settings)
    
    return generate_bin_changes_div_children(old_bin_list=[["0-20", "[[0, 20)]"], ["30-50", "[[30, 50)]"]], new_bin_list=[["0-50", "[[0, 50)]"]], dtype="numerical")


"""
Interactive Binning Page:
Update numeric rename preview changes info
when user clicks on the 'Rename Bin' button
"""
@app.callback(
    Output("numeric_rename_panel_changes_div", "children"),
    Input("numeric_rename_panel_rename_button", "n_clicks"),
    [
        State("numeric_rename_panel_new_bin_name_input", "value"),
        State("predictor_var_ib_dropdown", "value"),
        State("temp_col_bins_settings", "data"),
    ],
)
def update_numeric_create_new_bin_preview_changes_info(n_clicks, new_name, var_to_bin, temp_col_bins_settings_data):
    col_bin_settings = json.loads(temp_col_bins_settings_data)
    
    #col_bin_list = None
    # If it is no binning OR automated binning, have to translate it to list
    #if isinstance(col_bins_settings["bins"], dict) == True or col_bins_settings["bins"] == "none":
    #    col_bin_list = BinningMachine.convert_auto_bin_def_to_custom_def(col_bins_settings["bins"])
    
    #old_bin_list, new_bin_list = InteractiveBinningMachine.get_categoric_create_new_bin_changes(new_name, bin_element_list, var_to_bin, col_bin_settings)
    
    return generate_bin_changes_div_children(old_bin_list=[["0-20", "[[0, 20)]"], ["30-50", "[[30, 50)]"]], new_bin_list=[["0-50", "[[0, 50)]"]], dtype="numerical")

"""
Interactive Binning Page:
Update numeric merge preview changes info
when user clicks on the 'Merge Bins' button
"""
@app.callback(
    Output("numeric_merge_panel_changes_div", "children"),
    Input("numeric_merge_panel_merge_button", "n_clicks"),
    [
        State("numeric_merge_panel_new_bin_name_input", "value"),
        State("predictor_var_ib_dropdown", "value"),
        State("temp_col_bins_settings", "data"),
    ],
)
def update_numeric_create_new_bin_preview_changes_info(n_clicks, new_name, var_to_bin, temp_col_bins_settings_data):
    col_bin_settings = json.loads(temp_col_bins_settings_data)
    
    #col_bin_list = None
    # If it is no binning OR automated binning, have to translate it to list
    #if isinstance(col_bins_settings["bins"], dict) == True or col_bins_settings["bins"] == "none":
    #    col_bin_list = BinningMachine.convert_auto_bin_def_to_custom_def(col_bins_settings["bins"])
    
    #old_bin_list, new_bin_list = InteractiveBinningMachine.get_categoric_create_new_bin_changes(new_name, bin_element_list, var_to_bin, col_bin_settings)
    
    return generate_bin_changes_div_children(old_bin_list=[], new_bin_list=[["0-50", "[[0, 50)]"]], dtype="numerical")


"""
Interactive Binning Page:
Update categoric rename preview changes info
when user clicks on the 'Rename Bin' button
"""
@app.callback(
    [
        Output("categoric_rename_panel_changes_div", "children"),
        Output("categoric_rename_panel_submit_div", "style"),
    ],
    Input("categoric_rename_panel_rename_button", "n_clicks"),
    [
        State("categoric_rename_panel_new_bin_name_input", "value"),
        State("temp_col_bins_settings", "data"),
        State("mixed_chart", "clickData"),
    ],
)
def update_categoric_create_new_bin_preview_changes_info(n_clicks, new_name, temp_col_bins_settings_data, click_data):
    col_bin_settings = json.loads(temp_col_bins_settings_data)
    
    _, old_bin_list, new_bin_list = InteractiveBinningMachine.categoric_rename_bin(selected_bin_name=click_data["points"][0]["x"], new_bin_name=new_name, temp_col_bins_settings=col_bin_settings)
    
    style = {}
    if not isinstance(old_bin_list, list) or not isinstance(new_bin_list, list):
        style = {"display": "none"}
    
    return [generate_bin_changes_div_children(old_bin_list=old_bin_list, new_bin_list=new_bin_list, dtype="categorical"), style]



"""
Interactive Binning Page:
Show/Hide categorical add elements control panel preview changes 
when user clicks on the 'Add Elements' button
"""


@app.callback(
    Output("categoric_add_elements_panel_preview_changes_div", "style"),
    [
        Input("categoric_add_elements_panel_add_button", "n_clicks"),
        Input("categoric_add_elements_panel_hide_details_button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def show_categoric_create_new_bin_preview_changes_div(n_clicks, n_clicks2):
    triggered = dash.callback_context.triggered

    if triggered[0]['prop_id'] == "categoric_add_elements_panel_add_button.n_clicks":
        return {}
    else:
        return {"display": "none"}
    
"""
Interactive Binning Page:
Update selected bin info for categoric add elements panel
based on user clicks
"""
@app.callback(
    Output("categoric_add_elements_panel_selected_bin_info", "children"),
    Input("mixed_chart", "clickData"),
    [
        State("temp_chart_info", "data"),
        State("temp_col_bins_settings", "data"),
    ],
)
def update_categoric_add_elements_panel_selected_bin_info(click_data, temp_chart_info_data, temp_col_bins_settings_data):
    temp_chart_info = json.loads(temp_chart_info_data)
    temp_col_bins_settings = json.loads(temp_col_bins_settings_data)
    return generate_selected_bin_info_div_children(temp_chart_info=temp_chart_info, temp_col_bins_settings=temp_col_bins_settings, click_data=click_data, dtype="categorical")
 
"""
Interactive Binning Page:
Update selected bin info for categoric merge panel
based on user's selections
"""
@app.callback(
    Output("categoric_merge_panel_selected_bin_info_div", "children"),
    Input("mixed_chart", "selectedData"),
    [
        State("temp_chart_info", "data"),
        State("temp_col_bins_settings", "data"),
    ],
)
def update_categoric_merge_panel_selected_bin_info(selected_data, temp_chart_info_data, temp_col_bins_settings_data):
    temp_chart_info = json.loads(temp_chart_info_data)
    temp_col_bins_settings = json.loads(temp_col_bins_settings_data)
    return generate_selected_bin_info_div_children(temp_chart_info=temp_chart_info, temp_col_bins_settings=temp_col_bins_settings, click_data=selected_data, dtype="categorical")
  
"""
Interactive Binning Page:
Update selected bin info for numeric merge panel
based on user's selections
"""
@app.callback(
    Output("numeric_merge_panel_selected_bin_info_div", "children"),
    Input("mixed_chart", "selectedData"),
    [
        State("temp_chart_info", "data"),
        State("temp_col_bins_settings", "data"),
    ],
)
def update_numeric_merge_panel_selected_bin_info(selected_data, temp_chart_info_data, temp_col_bins_settings_data):
    temp_chart_info = json.loads(temp_chart_info_data)
    temp_col_bins_settings = json.loads(temp_col_bins_settings_data)
    return generate_selected_bin_info_div_children(temp_chart_info=temp_chart_info, temp_col_bins_settings=temp_col_bins_settings, click_data=selected_data, dtype="numerical")
    


"""
Interactive Binning Page:
Update categoric add elements panel dropdown options and value
when user click on a bar
"""
@app.callback(
    [
        Output("categoric_add_elements_panel_dropdown", "options"),
        Output("categoric_add_elements_panel_dropdown", "value"),
    ],
    Input("mixed_chart", "clickData"),
    State("temp_col_bins_settings", "data"),
)
def update_categoric_add_elements_dropdown(click_data, temp_col_bins_settings_data):
    if click_data is None:
        return [convert_column_list_to_dropdown_options([]), []]
    
    clicked_bin_name = click_data["points"][0]["x"]
    temp_col_bins_settings = json.loads(temp_col_bins_settings_data)
    
    bin_elements = None
    for bin_def in temp_col_bins_settings["bins"]:
        if bin_def["name"] == clicked_bin_name:
            bin_elements = bin_def["elements"]
    
    unique_element = df[temp_col_bins_settings["column"]].unique().tolist()
    
    options_li = [x for x in unique_element if x not in bin_elements]
    
    return [convert_column_list_to_dropdown_options(options_li), []]
 
       
"""
Interactive Binning Page:
Show/Hide categorical split control panel preview changes 
when user clicks on the 'Split Bin' button
"""
@app.callback(
    Output("categoric_split_panel_preview_changes_div", "style"),
    [
        Input("categoric_split_panel_split_button", "n_clicks"),
        Input("categoric_split_panel_hide_details_button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def show_categoric_split_preview_changes_div(n_clicks, n_clicks2):
    triggered = dash.callback_context.triggered

    if triggered[0]['prop_id'] == "categoric_split_panel_split_button.n_clicks":
        return {}
    else:
        return {"display": "none"}

"""
Interactive Binning Page:
Show/Hide categorical rename control panel preview changes 
when user clicks on the 'Rename Bin' button
"""
@app.callback(
    Output("categoric_rename_panel_preview_changes_div", "style"),
    [
        Input("categoric_rename_panel_rename_button", "n_clicks"),
        Input("categoric_rename_panel_hide_details_button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def show_categoric_split_preview_changes_div(n_clicks, n_clicks2):
    triggered = dash.callback_context.triggered

    if triggered[0]['prop_id'] == "categoric_rename_panel_rename_button.n_clicks":
        return {}
    else:
        return {"display": "none"}

"""
Interactive Binning Page:
Show/Hide categorical merge bin control panel preview changes 
when user clicks on the 'Merge Bin' button
"""
@app.callback(
    Output("categoric_merge_bin_panel_preview_changes_div", "style"),
    [
        Input("categoric_merge_panel_merge_button", "n_clicks"),
        Input("categoric_merge_panel_hide_details_button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def show_categoric_split_preview_changes_div(n_clicks, n_clicks2):
    triggered = dash.callback_context.triggered

    if triggered[0]['prop_id'] == "categoric_merge_panel_merge_button.n_clicks":
        return {}
    else:
        return {"display": "none"}
   


"""
Interactive Binning Page:
Show/Hide numerical adjust cutpoint control panel preview changes 
when user clicks on the 'Adjust Cutpoints' button
"""
@app.callback(
    Output("numeric_create_new_bin_preview_changes_div", "style"),
    [
        Input("numeric_create_new_bin_panel_create_new_bin_button", "n_clicks"),
        Input("numeric_create_new_bin_hide_details_button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def show_categoric_split_preview_changes_div(n_clicks, n_clicks2):
    triggered = dash.callback_context.triggered

    if triggered[0]['prop_id'] == "numeric_create_new_bin_panel_create_new_bin_button.n_clicks":
        return {}
    else:
        return {"display": "none"}

    
"""
Interactive Binning Page:
Show/Hide numerical adjust cutpoint control panel preview changes 
when user clicks on the 'Adjust Cutpoints' button
"""
@app.callback(
    Output("numeric_adjust_cutpoints_panel_preview_changes_div", "style"),
    [
        Input("numeric_adjust_cutpoints_panel_adjust_cutpoints_button", "n_clicks"),
        Input("numeric_adjust_cutpoints_panel_hide_details_button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def show_categoric_split_preview_changes_div(n_clicks, n_clicks2):
    triggered = dash.callback_context.triggered

    if triggered[0]['prop_id'] == "numeric_adjust_cutpoints_panel_adjust_cutpoints_button.n_clicks":
        return {}
    else:
        return {"display": "none"}
    
   
"""
Interactive Binning Page:
Show/Hide numerical rename control panel preview changes 
when user clicks on the 'Rename bin' button
"""
@app.callback(
    Output("numeric_rename_panel_preview_changes_div", "style"),
    [
        Input("numeric_rename_panel_rename_button", "n_clicks"),
        Input("numeric_rename_panel_hide_details_button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def show_categoric_split_preview_changes_div(n_clicks, n_clicks2):
    triggered = dash.callback_context.triggered

    if triggered[0]['prop_id'] == "numeric_rename_panel_rename_button.n_clicks":
        return {}
    else:
        return {"display": "none"}

    
"""
Interactive Binning Page:
Show/Hide numerical merge control panel preview changes 
when user clicks on the 'Merge' button
"""
@app.callback(
    Output("numeric_merge_panel_preview_changes_div", "style"),
    [
        Input("numeric_merge_panel_merge_button", "n_clicks"),
        Input("numeric_merge_panel_hide_details_button", "n_clicks"),
    ],
    prevent_initial_call=True,
)
def show_categoric_split_preview_changes_div(n_clicks, n_clicks2):
    triggered = dash.callback_context.triggered

    if triggered[0]['prop_id'] == "numeric_merge_panel_merge_button.n_clicks":
        return {}
    else:
        return {"display": "none"}
    

"""
Interactive Binning Page:
Update selected bin info for categoric split panel
based on user clicks
"""
@app.callback(
    Output("categoric_split_panel_selected_bin_info", "children"),
    Input("mixed_chart", "clickData"),
    [
        State("temp_chart_info", "data"),
        State("temp_col_bins_settings", "data"),
    ],
)
def update_categoric_split_panel_selected_bin_info(click_data, temp_chart_info_data, temp_col_bins_settings_data):
    temp_chart_info = json.loads(temp_chart_info_data)
    temp_col_bins_settings = json.loads(temp_col_bins_settings_data)
    return generate_selected_bin_info_div_children(temp_chart_info=temp_chart_info, temp_col_bins_settings=temp_col_bins_settings, click_data=click_data, dtype="categorical")
  
    
    



"""
Interactive Binning Page:
Update selected bin info for categoric rename panel
based on user clicks
"""
@app.callback(
    Output("categoric_rename_panel_selected_bin_info", "children"),
    Input("mixed_chart", "clickData"),
    [
        State("temp_chart_info", "data"),
        State("temp_col_bins_settings", "data"),
    ],
)
def update_categoric_split_panel_selected_bin_info(click_data, temp_chart_info_data, temp_col_bins_settings_data):
    temp_chart_info = json.loads(temp_chart_info_data)
    temp_col_bins_settings = json.loads(temp_col_bins_settings_data)
    return generate_selected_bin_info_div_children(temp_chart_info=temp_chart_info, temp_col_bins_settings=temp_col_bins_settings, click_data=click_data, dtype="categorical")
 
    
    
"""
Interactive Binning Page:
Update selected bin info for numeric adjust cutpoints panel
based on user clicks
"""
@app.callback(
    Output("numeric_adjust_cutpoints_panel_selected_bin_info_div", "children"),
    Input("mixed_chart", "clickData"),
    [
        State("temp_chart_info", "data"),
        State("temp_col_bins_settings", "data"),
    ],
)
def update_numeric_adjust_cutpoints_panel_selected_bin_info(click_data, temp_chart_info_data, temp_col_bins_settings_data):
    temp_chart_info = json.loads(temp_chart_info_data)
    temp_col_bins_settings = json.loads(temp_col_bins_settings_data)
    return generate_selected_bin_info_div_children(temp_chart_info=temp_chart_info, temp_col_bins_settings=temp_col_bins_settings, click_data=click_data, dtype="numerical")
  
    
    
"""
Interactive Binning Page:
Update selected bin info for numeric adjust cutpoints panel
based on user clicks
"""
@app.callback(
    Output("numeric_rename_panel_selected_bin_info_div", "children"),
    Input("mixed_chart", "clickData"),
    [
        State("temp_chart_info", "data"),
        State("temp_col_bins_settings", "data"),
    ],
)
def update_numeric_adjust_cutpoints_panel_selected_bin_info(click_data, temp_chart_info_data, temp_col_bins_settings_data):
    temp_chart_info = json.loads(temp_chart_info_data)
    temp_col_bins_settings = json.loads(temp_col_bins_settings_data)
    return generate_selected_bin_info_div_children(temp_chart_info=temp_chart_info, temp_col_bins_settings=temp_col_bins_settings, click_data=click_data, dtype="numerical")
  
    
    
    
"""
Interactive Binning Page:
Update categorical split control panel's dropdown 
options and value when user changes the var to bin in predictor
variable dropdown
"""
@app.callback(
    [
        Output("categoric_split_panel_dropdown", "options"),
        Output("categoric_split_panel_dropdown", "value"),
    ],
    Input("mixed_chart", "clickData"),
    State("temp_col_bins_settings", "data"),
)
def update_categoric_create_new_bin_dropdown(click_data, temp_col_bins_settings_data):
    if click_data is None:
        return [convert_column_list_to_dropdown_options([]), []]
    
    clicked_bin_name = click_data["points"][0]["x"]
    temp_col_bins_settings = json.loads(temp_col_bins_settings_data)
    
    bin_elements = None
    for bin_def in temp_col_bins_settings["bins"]:
        if bin_def["name"] == clicked_bin_name:
            bin_elements = bin_def["elements"]
    
    return [convert_column_list_to_dropdown_options(bin_elements), bin_elements]
    

"""
Interactive Binning Page:
Add/Remove ranges from numerical create new bin control panel
"""
@app.callback(
    Output("numeric_create_new_bin_panel_range_list", "children"),
    [
        Input("numeric_create_new_bin_panel_add_button", "n_clicks"),
        Input("numeric_create_new_bin_panel_remove_button", "n_clicks"),
    ],
    [
        State({"index": ALL, "type": "numeric_create_new_bin_lower"}, "value"),
        State({"index": ALL, "type": "numeric_create_new_bin_upper"}, "value"),
        State({"index": ALL, "type": "numeric_create_new_bin_checkbox"}, "value"),
    ],
)
def edit_numeric_create_new_bin_panel_ranges(add_clicks, remove_clicks, lower_list, upper_list, checkbox_list):
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    adding = len([i for i in triggered if i ==
                 "numeric_create_new_bin_panel_add_button.n_clicks"])
    removing = len([i for i in triggered if i ==
                   "numeric_create_new_bin_panel_remove_button.n_clicks"])
    new_spec = [
        (lower, upper, selected) for lower, upper, selected in zip(lower_list, upper_list, checkbox_list)
        if not (removing and selected)
    ]
    if adding:
        new_spec.append((0, 1, []))
    new_list = [
        html.Div([
            html.P(str(idx+1) + ".", style={"float": "left", "marginRight": 10}),
            dcc.Input(
                type="number",
                min=0,
                value=lower,
                id={"index": idx, "type": "numeric_create_new_bin_lower"},
                style={"width": 100, "float": "left"},
            ),
            html.P(
                "一", style={"float": "left", "marginLeft": 7, "fontWeight": "bold"}
            ),
            dcc.Input(
                type="number",
                min=0,
                value=upper,
                id={"index": idx, "type": "numeric_create_new_bin_upper"},
                style={"width": 100, "float": "left", "marginLeft": 7},
            ),
            dcc.Checklist(
                id={"index": idx, "type": "numeric_create_new_bin_checkbox"},
                options=[{"label": "", "value": "selected"}],
                value=selected,
                style={"display": "inline", "marginLeft": 7, "marginBottom": 7},
            ),
        ], style={"display": "flex", "alignItems": "flex-end", "marginTop": 10},)
        for idx, (lower, upper, selected) in enumerate(new_spec)
    ]
    
    return new_list
    
   
"""
Interactive Binning Page:
Add/Remove ranges from numerical adjust cutpoints control panel
"""
@app.callback(
    Output("numeric_adjust_cutpoints_panel_range_list", "children"),
    [
        Input("numeric_adjust_cutpoints_panel_add_button", "n_clicks"),
        Input("numeric_adjust_cutpoints_panel_remove_button", "n_clicks"),
    ],
    [
        State({"index": ALL, "type": "numeric_adjust_cutpoints_lower"}, "value"),
        State({"index": ALL, "type": "numeric_adjust_cutpoints_upper"}, "value"),
        State({"index": ALL, "type": "numeric_adjust_cutpoints_checkbox"}, "value"),
    ],
)
def edit_numeric_create_new_bin_panel_ranges(add_clicks, remove_clicks, lower_list, upper_list, checkbox_list):
    triggered = [t["prop_id"] for t in dash.callback_context.triggered]
    adding = len([i for i in triggered if i ==
                 "numeric_adjust_cutpoints_panel_add_button.n_clicks"])
    removing = len([i for i in triggered if i ==
                   "numeric_adjust_cutpoints_panel_remove_button.n_clicks"])
    new_spec = [
        (lower, upper, selected) for lower, upper, selected in zip(lower_list, upper_list, checkbox_list)
        if not (removing and selected)
    ]
    if adding:
        new_spec.append((0, 1, []))
    new_list = [
        html.Div([
            html.P(str(idx+1) + ".", style={"float": "left", "marginRight": 10}),
            dcc.Input(
                type="number",
                min=0,
                value=lower,
                id={"index": idx, "type": "numeric_adjust_cutpoints_lower"},
                style={"width": 100, "float": "left"},
            ),
            html.P(
                "一", style={"float": "left", "marginLeft": 7, "fontWeight": "bold"}
            ),
            dcc.Input(
                type="number",
                min=0,
                value=upper,
                id={"index": idx, "type": "numeric_adjust_cutpoints_upper"},
                style={"width": 100, "float": "left", "marginLeft": 7},
            ),
            dcc.Checklist(
                id={"index": idx, "type": "numeric_adjust_cutpoints_checkbox"},
                options=[{"label": "", "value": "selected"}],
                value=selected,
                style={"display": "inline", "marginLeft": 7, "marginBottom": 7},
            ),
        ], style={"display": "flex", "alignItems": "flex-end", "marginTop": 10},)
        for idx, (lower, upper, selected) in enumerate(new_spec)
    ]
    
    return new_list
    
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


# Get bins settings in ib page


@app.callback(
    Output("ib_show_bins_settings_text", "children"),
    Input("bins_settings", "data"),
)
def update_bins_settings_text_in_ib(data):
    adict = json.loads(data)
    return "bins settings = " + str(adict)

# Get good bad def in ib page


@app.callback(
    Output("ib_show_good_bad_def_text", "children"),
    Input("good_bad_def", "data")
)
def update_good_bad_def_text_in_ib(data):
    return "good bad def = " + str(json.loads(data))

# Get selected data info in ib page


@app.callback(
    Output("test_select", "children"),
    Input("mixed_chart", "selectedData"),
)
def output_selected_data_info(selected_data):
    return str(selected_data)

# Get click data info in ib page


@app.callback(
    Output("test_click", "children"),
    Input("mixed_chart", "clickData"),
)
def output_selected_data_info(click_data):
    return str(click_data)

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
