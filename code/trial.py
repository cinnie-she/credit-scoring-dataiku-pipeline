# https://note.nkmk.me/en/python-pandas-cut-qcut-binning/
import pandas as pd
import numpy as np

def equal_width_binning(df: pd.DataFrame, width: float) -> pd.Series:
    # Check if the input width is valid
    if width <= 0:
        raise ValueError("The input width should be a positive value.")
    
    # Get the column name and data type
    col_name = df.columns[0]
    col_dtype = df[col_name].dtype
    
    # Check if the data type is numerical or categorical
    if col_dtype == object:
        # For categorical data, use pandas.cut() function to perform binning
        bins = pd.cut(df[col_name], bins=np.arange(df[col_name].nunique()+1), right=False)
    else:
        # For numerical data, calculate the range of values and the number of bins
        min_value = df[col_name].min()
        max_value = df[col_name].max()
        num_bins = int(np.ceil((max_value - min_value) / width))
        
        # Use pandas.cut() function to perform binning
        bins = pd.cut(df[col_name], bins=num_bins, include_lowest=True)
    
    # Return the binned column as a pandas Series
    return pd.Series(bins, name=col_name)

# A method for performing equal width binning with a specified width, returns a pd.Series
def perform_eq_width_binning_by_width(col_df, dtype, width):
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
        return pd.cut(col_df[col_name], bins=num_bins, include_lowest=True)
    else: # categorical
        pass

df = pd.DataFrame([4, 9, 22, 40, 13, 80, 99, 55, 56, 78, 89, 30, 84, 22, 43, 86])
df2 = pd.DataFrame(["OWN", "OWN", "RENT", "MORTGAGE", "OWN", "RENT", "MORTGAGE", "OTHER", "OTHER", "RENT", "RENT"])

print(perform_eq_width_binning_by_width(df, "numerical", 10))
print("--------------------------")
print(perform_eq_width_binning_by_width(df, "numerical", 5))