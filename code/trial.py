# https://note.nkmk.me/en/python-pandas-cut-qcut-binning/
import pandas as pd
import numpy as np

# A method for performing equal frequency binning with a specified frequency, returns a pd.Series
def __perform_eq_freq_binning_by_freq__(col_df, dtype, freq):
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
def __perform_eq_freq_binning_by_num_bins__(col_df, dtype, num_bins):
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

df = pd.DataFrame([0, 4, 9, 22, 40, 13, 80, 99, 55, 56, 78, 89, 30, 84, 22, 43, 86, 100])
df2 = pd.DataFrame(["OWN", "OWN", "RENT", "MORTGAGE", "OWN", "RENT", "MORTGAGE", "OTHER", "OTHER", "RENT", "RENT"])

# print(perform_eq_width_binning_by_width(df, "numerical", 10))
# print("--------------------------")
# print(perform_eq_width_binning_by_width(df, "numerical", 5))
print("--------------------------")
print(__perform_eq_freq_binning_by_freq__(df, "numerical", 18))
print("--------------------------")
print(__perform_eq_freq_binning_by_freq__(df, "numerical", 9))
print("--------------------------")
print(__perform_eq_freq_binning_by_freq__(df, "numerical", 5))
print("--------------------------")
print(__perform_eq_freq_binning_by_freq__(df, "numerical", 1))