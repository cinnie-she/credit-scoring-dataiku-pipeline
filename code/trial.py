
import pandas as pd
import numpy as np


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
                    binned_result.append(f"[[{bin_range[0]}, {bin_range[1]})]")
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
                    binned_result.append(f"[[{bin_range[0]}, {bin_range[1]})]")
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
                    f"[[{interval_li[idx].left}, {interval_li[idx].right})]")

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
                    f"[[{interval_li[idx].left}, {interval_li[idx].right})]")

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




df = pd.read_excel("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx")
var_to_show = 'person_age'
def update_summary_statistics_table(var_to_show):
    bins_settings = {'variable': [{'column': 'person_age', 'type': 'numerical', 'bins': 'none'}, {'column': 'loan_status', 'type': 'categorical', 'bins': 'none'}]}
    good_bad_def = {'bad': {'numerical': [], 'categorical': [{'column': 'loan_status', 'elements': [1]}], 'weight': 1}, 'indeterminate': {'numerical': [], 'categorical': []}, 'good': {'weight': 1}}
    stat_df = None
    for bin_def in bins_settings["variable"]:
        if bin_def["column"] == var_to_show:
            stat_calculator = StatCalculator(df=df.copy(), col_bins_settings=bin_def, good_bad_def=good_bad_def)
            stat_df = stat_calculator.compute_summary_stat_table()
            break
    return stat_df

print(update_summary_statistics_table(var_to_show))
