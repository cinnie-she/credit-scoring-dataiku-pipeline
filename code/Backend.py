import pandas as pd
import numpy as np

df = pd.DataFrame()

# A class for performing binning based on bins settings & good bad definition
class BinningMachine:
    # A method for performing binning for the whole dataframe based on bins_settings, returns a binned_df
    def perform_binning_on_whole_df(self, bins_settings_list):
        binned_df = df[df.columns.to_list()]

        for predictor_var_info in bins_settings_list:
            new_col_name = predictor_var_info["column"] + "_binned"
            if predictor_var_info["bins"] == "none":
                binned_df[new_col_name] = df[predictor_var_info["column"]]
            elif predictor_var_info["bins"] == "equal width":
                pass
            elif predictor_var_info["bins"] == "equal frequency":
                pass
            else:
                pass

        return binned_df
    
    # A method for performing binning for a single column based on bins_settings, returns a pd.Series
    def perform_binning_on_col(self, col_df, bin_method):
        if bin_method["bins"] == "none":
            return col_df.iloc[:, 0] # no binning
        elif isinstance(bin_method["bins"], dict):  # auto binning
            if bin_method["bins"]["algo"] == "equal width":
                if bin_method["bins"]["method"] == "width":
                    return self.__perform_eq_width_binning_by_width__(col_df, bin_method["type"], bin_method["bins"]["value"])
                else: # by num of bins
                    return self.__perform_eq_width_binning_by_num_bins__(col_df, bin_method["type"], bin_method["bins"]["value"])
            else: # equal frequency
                if bin_method["bins"]["method"] == "freq":
                    return self.__perform_eq_freq_binning_by_freq__(col_df, bin_method["type"], bin_method["bins"]["value"])
                else: # by num of bins
                    return self.__perform_eq_freq_binning_by_num_bins__(col_df, bin_method["type"], bin_method["bins"]["value"])
        else: # custom binning
            return self.__perform_custom_binning__(col_df, bin_method["type"], bin_method["bins"])
    
    # A method for performing equal width binning with a specified width, returns a pd.Series
    def __perform_eq_width_binning_by_width__(self, col_df, dtype, width):
        # Check if the width is valid
        if width <= 0:
            raise ValueError("Width should be a positive number.")
        col_name = df.columns[0]
        if dtype == "categorical" and width > col_df[col_name].nunique():
            raise ValueError("For categorical variable, width should not be greater than number of unique values in the column.")
            
        # Bin the column
        if dtype == "numerical":
            min_value = col_df[col_name].min()
            max_value = col_df[col_name].max()
            num_bins = int(np.ceil((max_value - min_value) / width))
            return pd.cut(col_df[col_name], bins=num_bins, right=False)
        else: # categorical
            num_unique_value = col_df[col_name].nunique()
            bins_num_elements = list()
            
            num_bins = int(np.ceil(num_unique_value/width))

            for i in range(num_bins-1):
                bins_num_elements.append(width)
            bins_num_elements.append(num_unique_value - (num_bins-1) * width)

            unique_values = col_df[col_name].unique().tolist()
            bin_defs = list()
            bin_names = list()
            
            for num_elements in bins_num_elements:
                def_list = list()
                bin_name = ""
                
                def_list.append(unique_values[0])
                bin_name += str(unique_values[0])
                unique_values.pop(0)
                for i in range(num_elements-1):
                    def_list.append(unique_values[0])
                    bin_name += (", " + str(unique_values[0]))
                    unique_values.pop(0)
                    
                bin_defs.append(def_list)
                bin_names.append(bin_name)
            
            assigned_bin = list()
            for _, row in col_df.iterrows():
                for i in range(len(bin_defs)):
                    if row[0] in bin_defs[i]:
                        assigned_bin.append(bin_names[i])
                        break
                
            return pd.Series(assigned_bin)
    
    # A method for performing equal width binning with a specified number of fixed-width bins, returns a pd.Series
    def __perform_eq_width_binning_by_num_bins__(self, col_df, dtype, num_bins):
        # Check if the width is valid
        if num_bins <= 0 or not isinstance(num_bins, int):
            raise ValueError("Number of bins should be a positive integer.")
        col_name = df.columns[0]
        if dtype == "categorical" and num_bins > col_df[col_name].nunique():
            raise ValueError("For categorical variable, number of bins should not be greater than number of unique values in the column.")
            
        # Bin the column
        if dtype == "numerical":
            return pd.cut(col_df[col_name], bins=num_bins, right=False)
        else: # categorical
            num_unique_value = col_df[col_name].nunique()
            bins_num_elements = list() # list storing the number of elements in each bin
            
            if num_bins % num_unique_value == 0:
                for i in range(num_unique_value):
                    bins_num_elements.append(num_bins // num_unique_value)
            else:
                zp = num_bins - (num_unique_value % num_bins)
                pp = num_unique_value//num_bins
                for i in range(num_bins):
                    if(i>= zp):
                        bins_num_elements.append(pp+1)
                    else:
                        bins_num_elements.append(pp)
            #print(bins_num_elements)
            
            unique_values = col_df[col_name].unique().tolist()
            bin_defs = list()
            bin_names = list()
            
            for num_elements in bins_num_elements:
                def_list = list()
                bin_name = ""
                
                def_list.append(unique_values[0])
                bin_name += str(unique_values[0])
                unique_values.pop(0)
                for i in range(num_elements-1):
                    def_list.append(unique_values[0])
                    bin_name += (", " + str(unique_values[0]))
                    unique_values.pop(0)
                    
                bin_defs.append(def_list)
                bin_names.append(bin_name)
            
            assigned_bin = list()
            for _, row in col_df.iterrows():
                for i in range(len(bin_defs)):
                    if row[0] in bin_defs[i]:
                        assigned_bin.append(bin_names[i])
                        break
                
            return pd.Series(assigned_bin)
    
    # A method for performing equal frequency binning with a specified frequency, returns a pd.Series
    def __perform_eq_freq_binning_by_freq__(self, col_df, dtype, freq):
        # Check if the width is valid
        if freq <= 0 or not isinstance(freq, int):
            raise ValueError("Frequency should be a positive integer.")
        col_name = df.columns[0]
        
        # Bin the column
        if dtype == "numerical":
            num_rows = len(col_df)
            num_bins = int(np.ceil(num_rows/freq))
            return pd.qcut(col_df[col_name], num_bins, duplicates="drop")
        else: # categorical
            pass
    
    # A method for performing equal frequency binning with a specified number of fixed-frequency bins, returns a pd.Series
    def __perform_eq_freq_binning_by_num_bins__(self, col_df, dtype, num_bins):
        # Check if the width is valid
        if num_bins <= 0 or not isinstance(num_bins, int):
            raise ValueError("Frequency should be a positive integer.")
        col_name = df.columns[0]
        if dtype == "categorical" and num_bins > col_df[col_name].nunique():
            raise ValueError("For categorical variable, number of bins should not be greater than number of unique values in the column.")
            
        # Bin the column
        if dtype == "numerical":
            return pd.qcut(col_df[col_name], num_bins, duplicates="drop")
        else: # categorical
            pass
    
    # A method for performing binning based on boundary points obtained from interactive binning, returns a pd.Series
    def __perform_custom_binning__(self, col_df, dtype, bins_settings):
        pass


# A class to calculate statistical values for displaying the mixed chart & statistical tables
class StatCalculator:
    def __init__(self, df, col_bins_settings, good_bad_def) -> None:
        self.df = df # for binning & good bad calculation, need whole df (OR only columns to be binned & columns involved in good bad def)
        self.col_bins_settings = col_bins_settings # for binning
        self.good_bad_def = good_bad_def # for good bad calculation

    # Output - a dataframe representing the summary statistics table of the column
    def compute_summary_stat_table(self):
        """
        1. Binning
        """
        col_to_bin = self.col_bins_settings["column"] # get the name of column to be binned
        
        col_df = self.df.loc[:, [col_to_bin]] # get a single column
        
        # perform binning
        binning_machine = BinningMachine()
        binned_series = binning_machine.perform_binning_on_col(col_df, self.col_bins_settings)
        self.df.insert(loc=0, column=col_to_bin+"_binned", value=binned_series)
        
        """
        2. Compute Summary Statistic Table
        """
        # Initialize an empty dictionary for storing information of each rows of the summary table (i.e., each bin)
        summary_dict = dict()
        # Create a list which stores summary table' column names
        summary_table_col_name_list = ["Bin", "Good", "Bad", "Odds", "Total", "Good%", "Bad%", "Total%", "Info_Odds", "WOE", "MC"]

        # Get and save a list of unique bin_name
        bin_name_list = self.df.iloc[:, 0].unique().tolist()
        
        # Get total good & bad
        good_bad_counter = GoodBadCounter()
        _, _, _, _, _, total_good_count, total_bad_count = good_bad_counter.get_statistics(self.df, self.good_bad_def)
        
        # For each bin_name in the list (i.e. loop nbin times)
        for bin_name in bin_name_list:
            # Get a DataFrame which filtered out rows that does not belong to the bin
            bin_df = self.df.loc[self.df.iloc[:,0] == bin_name]
            # Call compute_bin_stats(var_df : pd.DataFrame, total_num_records : Integer, bin_name : String) and save as bin_stats_list
            bin_stats_list = self.__compute_bin_stats__(bin_df, bin_name, total_good_count, total_bad_count)
            # Add an element in the dictionary, with bin_name as the key, and bin_stats_list as the value
            summary_dict[bin_name] = bin_stats_list
        
        # Create a pd.DataFrame object using the created dictionary
        var_summary_df = pd.DataFrame.from_dict(summary_dict, orient='index', columns=summary_table_col_name_list)

        # Call compute_var_stats(var_df: pd.DataFrame, var_summary_df : pd.DataFrame, total_num_records : Integer) and save the list
        var_stats_list = self.__compute_var_stats__(var_summary_df, total_good_count, total_bad_count)

        # Create a dictionary using "all" as the key, and the list created as the value
        all_summary_series = pd.Series(var_stats_list, index = summary_table_col_name_list)

        # Append the dictionary as a row to the pd.DataFrame created
        var_summary_df = var_summary_df.append(all_summary_series, ignore_index=True)
    
        # format df
        for col in ['Odds','Info_Odds','WOE','MC']:
            var_summary_df[col] = var_summary_df[col].apply(lambda x: 0 if (x != None and abs(x) < 0.001) else x)
            var_summary_df[col] = var_summary_df[col].apply(lambda x: round(x, 4))
        
        for col in ['Good%', 'Bad%', 'Total%']:
            var_summary_df[col] = var_summary_df[col].apply(lambda x: round(x, 2))
            
        return var_summary_df
    
    def __compute_bin_stats__(self, bin_df, bin_name, total_good, total_bad):
        # Initialize an empty list (e.g., bin_stats_list) for storing the statistics for a bin
        bin_stats_list = list()

        # Compute bin good & bad count
        good_bad_counter = GoodBadCounter()
        _, _, _, _, _, good, bad = good_bad_counter.get_statistics(bin_df, self.good_bad_def)
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
        bin_stats_row = [bin_name, good, bad, odds, total, good_pct*100, bad_pct*100, total_pct*100, info_odds, woe, mc]
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
        var_stats_list = ["Total", good, bad, odds, total, good_pct*100, bad_pct*100, total_pct*100, info_odds, woe, mc]
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
        if info_odds == None or info_odds == 0:
            return None
        else:
            return np.log(info_odds)

    @staticmethod
    def compute_mc(good_pct, bad_pct, woe):
        if woe == None:
            return 0
        else:
            return (good_pct - bad_pct)*woe


# A class for counting the number of good and bad samples/population in the column
class GoodBadCounter:    
    # A method to get the number of sample bad, sample indeterminate, sample good, population good, and population bad
    def get_statistics(self, dframe, good_bad_def):
        new_dframe, sample_bad_count = self.__count_sample_bad(dframe, good_bad_def["bad"])
        sample_indeterminate_count = self.__count_sample_indeterminate(new_dframe, good_bad_def["indeterminate"])
        sample_good_count = self.__count_sample_good(dframe, sample_bad_count, sample_indeterminate_count)
        good_weight = good_bad_def["good"]["weight"]
        bad_weight = good_bad_def["bad"]["weight"]
        population_good_count = self.__get_population_good(sample_good_count, good_weight)
        population_bad_count = self.__get_population_bad(sample_bad_count, bad_weight)
        return (sample_bad_count, sample_indeterminate_count, sample_good_count, good_weight, bad_weight, population_good_count, population_bad_count)
    
    # A method to count the number of sample bad
    def __count_sample_bad(self, dframe, bad_defs):
        bad_count = 0
        for bad_numeric_def in bad_defs["numerical"]:
            # count number of rows if dframe row is in bad_numeric_def range, and add to bad_count
            for a_range in bad_numeric_def["ranges"]:
                bad_count += len(dframe[(dframe[bad_numeric_def["column"]] >= a_range[0]) & (dframe[bad_numeric_def["column"]] < a_range[1])])
                # delete rows if dframe row is in bad_numeric_def range
                dframe = dframe.drop(dframe[(dframe[bad_numeric_def["column"]] >= a_range[0]) & (dframe[bad_numeric_def["column"]] < a_range[1])].index)
                
        for bad_categoric_def in bad_defs["categorical"]:
            # count number of rows if dframe row is having any one of the bad_categoric_def elements value
            for element in bad_categoric_def["elements"]:
                bad_count += len(dframe[(dframe[bad_categoric_def["column"]] == element)])
                # delete rows if dframe row has value 'element'
                dframe = dframe.drop(dframe[(dframe[bad_categoric_def["column"]] == element)].index)
        
        return (dframe, bad_count)
    
    # A method to count the number of sample indeterminate
    def __count_sample_indeterminate(self, dframe, indeterminate_defs):
        indeterminate_count = 0
        for indeterminate_numeric_def in indeterminate_defs["numerical"]:
            # count number of rows if dframe row is in indeterminate_numeric_def range, and add to indeterminate_count
            for a_range in indeterminate_numeric_def["ranges"]:
                indeterminate_count += len(dframe[(dframe[indeterminate_numeric_def["column"]] >= a_range[0]) & (dframe[indeterminate_numeric_def["column"]] < a_range[1])])
                # delete rows if dframe row is in indeterminate_numeric_def range
                dframe = dframe.drop(dframe[(dframe[indeterminate_numeric_def["column"]] >= a_range[0]) & (dframe[indeterminate_numeric_def["column"]] < a_range[1])].index)
                
        for indeterminate_categoric_def in indeterminate_defs["categorical"]:
            # count number of rows if dframe row is having any one of the indeterminate_categoric_def elements value
            for element in indeterminate_categoric_def["elements"]:
                indeterminate_count += len(dframe[(dframe[indeterminate_categoric_def["column"]] == element)])
                # delete rows if dframe row has value 'element'
                dframe = dframe.drop(dframe[(dframe[indeterminate_categoric_def["column"]] == element)].index)
        
        return indeterminate_count
    
    # A method to count the number of sample good
    def __count_sample_good(self, dframe, sample_bad_count, sample_indeterminate_count):
        return (len(dframe) - sample_bad_count - sample_indeterminate_count)
    
    # A method to count the number of population good
    def __get_population_good(self, sample_good_count, good_weight):
        return sample_good_count * good_weight
    
    # A method to count the number of population bad
    def __get_population_bad(self, sample_bad_count, bad_weight):
        return sample_bad_count * bad_weight
    


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
            if a_range[1] <= a_range[0]:
                return False
        return True


# A class for obtaining user inputs from the section UI info
class GoodBadDefDecoder:
    # A method to translate section UI info to a list of numerical definition
    def get_numeric_def_list_from_section(self, numeric_info_list):
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
                            numeric_list[def_idx]["ranges"][def_range_idx] = [a_range[0], a_range[1]]
                            overlapped_def_range_idxes.insert(0, def_range_idx)
                        elif def_range[0] <= a_range[0] and def_range[1] >= a_range[1]:
                            has_range_overlap = True
                        elif a_range[0] <= def_range[0] and a_range[1] >= def_range[0] and a_range[1] <= def_range[1]:
                            has_range_overlap = True
                            numeric_list[def_idx]["ranges"][def_range_idx] = [a_range[0], def_range[1]]
                            overlapped_def_range_idxes.insert(0, def_range_idx)
                        elif a_range[0] >= def_range[0] and a_range[0] <= def_range[1] and a_range[1] >= def_range[1]:
                            has_range_overlap = True
                            numeric_list[def_idx]["ranges"][def_range_idx] = [def_range[0], a_range[1]]
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
        return numeric_list
    # A method to translate section UI info to a list of categorical definition

    def get_categorical_def_list_from_section(self, categoric_info_list):
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
