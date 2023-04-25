# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import json

# Read recipe inputs
ib_settings = dataiku.Dataset("ib_settings")
ib_settings_df = ib_settings.get_dataframe()
bins_settings_data = ib_settings_df.iloc[0, 0]

bins_settings = json.loads(bins_settings_data)

for bin_def_idx in range(len(bins_settings)):
    if bins_settings[bin_def_idx]["type"] == "numerical":
        for bin_idx in range(len(bins_settings[bin_def_idx]["bins"])):
            if isinstance(bins_settings[bin_def_idx]["bins"], list):
                for r_idx in range(len(bins_settings[bin_def_idx]["bins"][bin_idx]["ranges"])):
                    bins_settings[bin_def_idx]["bins"][bin_idx]["ranges"][r_idx][0] = float(bins_settings[bin_def_idx]["bins"][bin_idx]["ranges"][r_idx][0])
                    bins_settings[bin_def_idx]["bins"][bin_idx]["ranges"][r_idx][1] = float(bins_settings[bin_def_idx]["bins"][bin_idx]["ranges"][r_idx][1])
            elif isinstance(bins_settings[bin_def_idx]["bins"], dict):
                if bins_settings[bin_def_idx]["bins"]["method"] == "num_bins":
                    bins_settings[bin_def_idx]["bins"]["value"] = int(bins_settings[bin_def_idx]["bins"]["value"])
                elif bins_settings[bin_def_idx]["bins"]["algo"] == "equal width":
                    bins_settings[bin_def_idx]["bins"]["value"] = float(bins_settings[bin_def_idx]["bins"]["value"])
                else:
                    bins_settings[bin_def_idx]["bins"]["value"] = int(bins_settings[bin_def_idx]["bins"]["value"])

# Remove loan_status from bins_settings if have
for bin_def_idx in range(len(bins_settings)):
    if bins_settings[bin_def_idx]["column"] == "loan_status":
        del bins_settings[bin_def_idx]
        break
                    
credit_risk_dataset_generated = dataiku.Dataset("credit_risk_dataset_generated")
df = credit_risk_dataset_generated.get_dataframe()


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
                binned_result.append("Missing")

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
                binned_result.append("Missing")
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
        max_val = float(col_df.max())
        binned_result = list()
        for idx in range(len(interval_li)):
            if not isinstance(interval_li[idx], pd._libs.interval.Interval):
                binned_result.append("Missing")
            else:
                if interval_li[idx].right == max_val:
                    binned_result.append(
                        f"[[{interval_li[idx].left}, {interval_li[idx].right+0.0001})]")
                else:
                    binned_result.append(
                        f"[[{interval_li[idx].left}, {interval_li[idx].right})]")

        def_set = set()
        for idx in range(len(interval_li)):
            if isinstance(interval_li[idx], pd._libs.interval.Interval):
                if interval_li[idx].right == max_val:
                    def_set.add((interval_li[idx].left, interval_li[idx].right+0.0001))
                else:
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

        print(f"column_df: {col_df}")
        print(f"interval_li: {interval_li}, len: {len(interval_li)}")
            
        # convert to the format we want
        max_val = float(col_df.max())
        binned_result = list()
        for idx in range(len(interval_li)):
            if not isinstance(interval_li[idx], pd._libs.interval.Interval):
                binned_result.append("Missing")
            else:
                print(f"interval_li[idx].right: {interval_li[idx].right}, max_val: {max_val}")
                print(f"interval_li[idx].right: {type(interval_li[idx].right)}, max_val: {type(max_val)}")
                if interval_li[idx].right == max_val:
                    binned_result.append(
                        f"[[{interval_li[idx].left}, {interval_li[idx].right+0.0001})]")
                else:
                    binned_result.append(
                        f"[[{interval_li[idx].left}, {interval_li[idx].right})]")

        def_set = set()
        for idx in range(len(interval_li)):
            if isinstance(interval_li[idx], pd._libs.interval.Interval):
                if interval_li[idx].right == max_val:
                    def_set.add((interval_li[idx].left, interval_li[idx].right+0.0001))
                else:
                    def_set.add((interval_li[idx].left, interval_li[idx].right))
        bin_ranges = list(def_set)
        
        print(f"bin_ranges: {bin_ranges}, len: {len(bin_ranges)}")
        
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
            for a_bin in bins_settings:
                if val in a_bin["elements"]:
                    binned_result.append(a_bin["name"])
                    has_assigned_bin = True
                    break
            if has_assigned_bin == False:  # does not belongs to any bin
                binned_result.append("Missing")

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
            for a_bin in bins_settings:
                for r in a_bin["ranges"]:
                    if val >= r[0] and val < r[1]:
                        binned_result.append(a_bin["name"])
                        has_assigned_bin = True
                        break

            if has_assigned_bin == False:  # does not belongs to any bin
                binned_result.append("Missing")

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


# Compute recipe outputs
binned_credit_risk_dataset_df = BinningMachine.perform_binning_on_whole_df(df, bins_settings)

# Write recipe outputs
binned_credit_risk_dataset = dataiku.Dataset("binned_credit_risk_dataset")
binned_credit_risk_dataset.write_with_schema(binned_credit_risk_dataset_df)
