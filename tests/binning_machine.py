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
            return col_df.iloc[:, 0]  # no binning
        elif isinstance(bin_method["bins"], dict):  # auto binning
            if bin_method["bins"]["algo"] == "equal width":
                if bin_method["bins"]["method"] == "width":
                    return self.__perform_eq_width_binning_by_width__(col_df, bin_method["type"], bin_method["bins"]["value"])
                else:  # by num of bins
                    return self.__perform_eq_width_binning_by_num_bins__(col_df, bin_method["type"], bin_method["bins"]["value"])
            else:  # equal frequency
                if bin_method["bins"]["method"] == "freq":
                    return self.__perform_eq_freq_binning_by_freq__(col_df, bin_method["type"], bin_method["bins"]["value"])
                else:  # by num of bins
                    return self.__perform_eq_freq_binning_by_num_bins__(col_df, bin_method["type"], bin_method["bins"]["value"])
        else:  # custom binning
            return self.__perform_custom_binning__(col_df, bin_method["type"], bin_method["bins"])

    # A method for performing equal width binning with a specified width, returns a pd.Series
    def __perform_eq_width_binning_by_width__(self, col_df, dtype, width):
        # Check if the width is valid
        if width <= 0:
            # Width should be a positive number.
            raise PreventUpdate
        col_name = df.columns[0]
        if dtype == "categorical" and width > col_df[col_name].nunique():
            # For categorical variable, width should not be greater than number of unique values in the column.
            raise PreventUpdate

        # Bin the column
        if dtype == "numerical":
            min_value = col_df[col_name].min()
            max_value = col_df[col_name].max()
            num_bins = int(np.ceil((max_value - min_value) / width))
            return pd.cut(col_df[col_name], bins=num_bins, right=False)
        else:  # categorical
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
            # Number of bins should be a positive integer.
            raise PreventUpdate
        col_name = df.columns[0]
        if dtype == "categorical" and num_bins > col_df[col_name].nunique():
            # For categorical variable, number of bins should not be greater than number of unique values in the column.
            raise PreventUpdate

        # Bin the column
        if dtype == "numerical":
            return pd.cut(col_df[col_name], bins=num_bins, right=False)
        else:  # categorical
            num_unique_value = col_df[col_name].nunique()
            bins_num_elements = list()  # list storing the number of elements in each bin

            if num_bins % num_unique_value == 0:
                for i in range(num_unique_value):
                    bins_num_elements.append(num_bins // num_unique_value)
            else:
                zp = num_bins - (num_unique_value % num_bins)
                pp = num_unique_value//num_bins
                for i in range(num_bins):
                    if (i >= zp):
                        bins_num_elements.append(pp+1)
                    else:
                        bins_num_elements.append(pp)
            # print(bins_num_elements)

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
            # Frequency should be a positive integer.
            raise PreventUpdate
        col_name = df.columns[0]

        # Bin the column
        if dtype == "numerical":
            num_rows = len(col_df)
            num_bins = int(np.ceil(num_rows/freq))
            return pd.qcut(col_df[col_name], num_bins, duplicates="drop")
        else:  # categorical
            pass

    # A method for performing equal frequency binning with a specified number of fixed-frequency bins, returns a pd.Series
    def __perform_eq_freq_binning_by_num_bins__(self, col_df, dtype, num_bins):
        # Check if the width is valid
        if num_bins <= 0 or not isinstance(num_bins, int):
            raise ValueError("Frequency should be a positive integer.")
        col_name = df.columns[0]
        if dtype == "categorical" and num_bins > col_df[col_name].nunique():
            raise ValueError(
                "For categorical variable, number of bins should not be greater than number of unique values in the column.")

        # Bin the column
        if dtype == "numerical":
            return pd.qcut(col_df[col_name], num_bins, duplicates="drop")
        else:  # categorical
            pass

    # A method for performing binning based on boundary points obtained from interactive binning, returns a pd.Series
    def __perform_custom_binning__(self, col_df, dtype, bins_settings):
        pass