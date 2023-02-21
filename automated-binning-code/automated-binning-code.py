# -------------------------------------------------------------------------------- NOTEBOOK-CELL: MARKDOWN
# # Create Automated Binning Summary Tables

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
"""
    Current Approach:
    1. when good/bad/bad_pct/total_bad/total_good == 0 return None for good%, bad%, woe
    2. when woe == None, mc = 0
    3. round to 4 d.p. for absolute values, to 2 d.p. for % values
    4. odds = good/bad
    5. add info_odd
    6. rearranged columns order
"""

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: MARKDOWN
# ## 0. Import Libraries

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: MARKDOWN
# ## 1. Read recipe inputs

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Read recipe inputs
credit_risk_dataset_prepared = dataiku.Dataset("credit_risk_dataset_generated")
df = credit_risk_dataset_prepared.get_dataframe()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: MARKDOWN
# ## 2. Utils - Functions

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def compute_summary_tables(var_df, total_num_records):
    """
    Input: 
        - A pandas.DataFrame object with 2 columns (predictor_variable & loan_status)
        - An Integer which is the count of records in the whole dataset
    Output: A pandas.DataFrame object with all columns in the summary table
    """
    
    # Initialize an empty dictionary for storing information of each rows of the summary table (i.e., each bin)
    summary_dict = dict()

    # Create a list which stores summary table' column names
    summary_table_col_name_list = ["Bin", "Good", "Bad", "Odds", "Total", "Good_Pct", "Bad_Pct", "Total_Pct", "Info_Odds", "WOE", "MC"]

    # Get and save a list of unique bin_name
    bin_name_list = var_df.iloc[:, 0].unique().tolist()

    # Get total number of bad
    total_bad = compute_bad(var_df)
    # Get total number of good
    total_good = compute_good(var_df)

    # For each bin_name in the list (i.e. loop nbin times)
    for bin_name in bin_name_list:
        # Call compute_bin_stats(var_df : pd.DataFrame, total_num_records : Integer, bin_name : String) and save as bin_stats_list
        bin_stats_list = compute_bin_stats(var_df, total_num_records, bin_name, total_good, total_bad)
        # Add an element in the dictionary, with bin_name as the key, and bin_stats_list as the value
        summary_dict[bin_name] = bin_stats_list

    # Create a pd.DataFrame object using the created dictionary
    var_summary_df = pd.DataFrame.from_dict(summary_dict, orient='index', columns=summary_table_col_name_list)

    # Call compute_var_stats(var_df: pd.DataFrame, var_summary_df : pd.DataFrame, total_num_records : Integer) and save the list
    var_stats_list = compute_var_stats(var_df, var_summary_df, total_num_records, total_good, total_bad)

    # Create a dictionary using "all" as the key, and the list created as the value
    all_summary_series = pd.Series(var_stats_list, index = summary_table_col_name_list)

    # Append the dictionary as a row to the pd.DataFrame created
    var_summary_df = var_summary_df.append(all_summary_series, ignore_index=True)
    
    # format df
    # 1. person_emp_length[Bin] --> int
#     if var_df.columns[0] == 'person_emp_length':
#         var_summary_df['Bin'] = var_summary_df['Bin'].apply(lambda x: float("{:.0f}".format(x)) if (type(x) != str) else x)
    # 2. for all [Odds, Info_Odds, WOE, MC] --> 4 d.p.
    for col in ['Odds','Info_Odds','WOE','MC']:
#         var_summary_df[col] = var_summary_df[col].apply(lambda x: float("{:.4f}".format(x)) if (x != None) else x)
        var_summary_df[col] = var_summary_df[col].apply(lambda x: 0 if (x != None and abs(x) < 0.001) else x)
    
    # 3. for all ["Good%", "Bad%", "Total%"] --> 2 d.p.
#     for col in ["Good%", "Bad%", "Total%"]:
#         var_summary_df[col] = var_summary_df[col].apply(lambda x: float("{:.2f}".format(x)) if (x != None) else x)

    # Return the pd.DataFrame summary table created
    return var_summary_df

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def compute_bin_stats(var_df, total_num_records, bin_name, total_good, total_bad):
    """
    Input:
        - A pandas.DataFrame object with 2 columns (predictor_variable & loan_status)
        - An Integer which is the count of records in the whole dataset
        - A String which is the bin_name which we're going to compute statistics for
        - An Integer which is the total number of good observations in the whole dataset
        - An Integer which is the total number of bad observations in the whole dataset
    Output: A list in order [Bin, Good, Good%, Bad, Bad%, Odds, Total, Total%, WOE, MC] for the bin
    """

    # Initialize an empty list (e.g., bin_stats_list) for storing the statistics for a bin
    bin_stats_list = list()
    # Get a DataFrame which filtered out rows that does not belong to the bin
    bin_df = var_df.loc[var_df.iloc[:,0] == bin_name]

    # Call compute_good(df : pd.DataFrame) using bin_df and save the returned value
    good = compute_good(bin_df)
    # Call compute_bad(df : pd.DataFrame) using bin_df and save the returned value
    bad = compute_bad(bin_df)
    # Call compute_total(df : pd.DataFrame) using bin_df and save the returned value
    total = compute_total(bin_df)
    # Call compute_pct(value : Integer, total_value : Integer) and save the returned value (i.e., good%)
    good_pct = compute_pct(good, total_good)
    # Call compute_pct(value : Integer, total_value : Integer) and save the returned value (i.e., bad%)
    bad_pct = compute_pct(bad, total_bad)
    # Call compute_pct(value : Integer, total_value : Integer) and save the returned value (i.e., total%)
    total_pct = compute_pct(total, total_num_records)
    # Call compute_odds(good_pct : Float, bad_pct : Float) and save the returned value
    odds = compute_odds(good, bad)
    info_odds = compute_info_odds(good_pct, bad_pct)
    # Call compute_woe(df : pd.DataFrame) using df and save the returned value
    woe = compute_woe(info_odds)
    # Call compute_info_val(good_pct : Float, bad_pct : Float, woe : Float) and save the returned value
    mc = compute_mc(good_pct, bad_pct, woe)

    # Append all statistics to the bin_stats_list in order
    bin_stats_row = [bin_name, good, bad, odds, total, good_pct*100, bad_pct*100, total_pct*100, info_odds, woe, mc]
    bin_stats_list.extend(bin_stats_row)

    # Return list
    return bin_stats_list

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def compute_var_stats(var_df, var_summary_df, total_num_records, total_good, total_bad):
    """
    Input:
        - A pandas.DataFrame object with 2 columns (predictor_variable & loan_status)
        - A pandas.DataFrame object with summary statistics for all bins
        - An Integer which is the count of records in the whole dataset
        - An Integer which is the total number of good observations in the whole dataset
        - An Integer which is the total number of bad observations in the whole dataset
    Output: A list in order [Bin, Good, Good%, Bad, Bad%, Odds, Total, Total%, WOE, InfoVal] for the variable
    """

    # Create an empty list for storing the statistics for the whole dataset
    var_stats_list = list()

    # Call compute_good(df : pd.DataFrame) using df and save the returned value
    good = total_good
    # Call compute_bad(df : pd.DataFrame) using df and save the returned value
    bad = total_bad
    # Call compute_total(df : pd.DataFrame) using df and save the returned value
    total = compute_total(var_df)
    # Call compute_pct(value : Integer, total_value : Integer) and save the returned value (i.e., good%)
    good_pct = compute_pct(good, total_good)
    # Call compute_pct(value : Integer, total_value : Integer) and save the returned value (i.e., bad%)
    bad_pct = compute_pct(bad, total_bad)
    # Call compute_pct(value : Integer, total_value : Integer) and save the returned value (i.e., total%)
    total_pct = compute_pct(total, total_num_records)
    # Call compute_odds(good_pct : Float, bad_pct : Float) and save the returned value
    odds = compute_odds(good, bad)
    info_odds = None
    # Empty woe
    woe = None
    # Sum up the MC column and save the value = InfoVal
    mc = var_summary_df.MC.sum()

    # Append all statistics to the empty list in order
    var_stats_list = ["Total", good, bad, odds, total, good_pct*100, bad_pct*100, total_pct*100, info_odds, woe, mc]
    # Return list
    return var_stats_list

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def compute_good(df):
    """
    Input: A pandas.DataFrame object with 2 columns (predictor_variable & loan_status)
    Output: An integer for the count of good observations in the DataFrame
    """
    good_df = df.loc[df.iloc[:,1] == 0]
    return good_df.shape[0]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def compute_bad(df):
    """
    Input: A pandas.DataFrame object with 2 columns (predictor_variable & loan_status)
    Output: An integer for the count of bad observations in the DataFrame
    """
    bad_df = df.loc[df.iloc[:,1] == 1]
    return bad_df.shape[0]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def compute_total(df):
    """
    Input: A pandas.DataFrame object with 2 columns (predictor_variable & loan_status)
    Output: total number of records in the DataFrame
    """
    return df.shape[0]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def compute_pct(value, total_value):
    """
    Input:
        - An Integer 'value' which is the dividend
        - An Integer 'total_value' which is the divisor
    Output: A Float which is the percentage of value with respect to total_value
    """
    if total_value == 0:
        return None
    else:
        return (value/total_value)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def compute_odds(good, bad):
    """
    Input:
        - An Int 'good' which is the dividend
        - An Int 'bad' which is the divisor
    Output: A Float representing odds
    """
    if bad == 0:
        return None
    else:
        return (good/bad)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def compute_info_odds(good_pct, bad_pct):
    """
    Input:
        - A Float 'good_pct' which is the dividend
        - A Float 'bad_pct' which is the divisor
    Output: A float representing info odds
    """
    if bad_pct == 0:
        return None
    else:
        return (good_pct/bad_pct)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def compute_woe(info_odds):
    """
    Input:
        - A Float representing good%/bad%
    Output: A Float which is the WOE of the bin
    """

    if info_odds == None or info_odds == 0:
        return None
    else:
        return np.log(info_odds)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
def compute_mc(good_pct, bad_pct, woe):
    """
    Input:
        - A Float 'good_pct' which is the % of good in the bin
        - A Float 'bad_pct' which is the % of bad in the bin
        - A Float 'woe' which is the WOE of the bin
    Output: A Float which is the MC of the bin
    """
    if woe == None:
        return 0
    else:
        return (good_pct - bad_pct)*woe

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# def round_to_4_dp(li):
#     """
#     Input:
#      - A list ["Bin", "Good", "Bad", "Odds", "Total", "Good%", "Bad%", "Total%", "Info_Odds", "WOE", "MC"]
#     Output: A list rounded all numerical values to 4 decimal places
#     """
#     # initialize a list for storing rounded values
#     new_li = list()
#     # loop through all elements in the list
#     for idx in range(len(li)):
#         if idx in [0,1,2,4]:
#             new_li.append(li[idx])
#             print(new_li)
#         elif idx in [3,8,9,10]:
#             if li[idx] != None:
#                 if float(li[idx]) < 0.0001:
#                     new_li.append('{:.4f}'.format(0))
#                     print(new_li)
#                 else:
#                     new_li.append('{:.4f}'.format(round(li[idx], 2)))
#                     print(new_li)
#             else:
#                 new_li.append(li[idx])
#                 print(new_li)
#         else:
#             if li[idx] != None:
#                 new_li.append('{:.2f}'.format(round(li[idx], 2)))
#                 print(new_li)
#             else:
#                 new_li.append(li[idx])
#                 print(new_li)
        
# #    print(new_li)
#     # return the rounded list
#     return new_li

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: MARKDOWN
# ## 3. Compute summary tables and generate outputs

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
"""---------------------------main()--------------------------"""

# Get all predictor column names in the input dataset & Store in a list
var_name_list = list(df.columns)
var_name_list.remove('loan_status')
var_name_list.remove('paid_past_due')

# Compute number of rows in the whole dataset and save the value in a variable
total_num_records = df.shape[0]

# For each predictor variable in the list (i.e. loop 11 times)
for var_name in var_name_list:

    # Create a DataFrame with 2 columns (predictor variable & loan_status)
    var_df = df[[var_name, 'loan_status']]

    # Call compute_summary_table(var_df : pd.DataFrame, total_num_records : Integer) and save it to a variable
    var_summary_df = compute_summary_tables(var_df, total_num_records)

    # Create a dataiku dataset using the name (predictor variable column name) + "_ab_stats"
    dataiku_ds = dataiku.Dataset(var_name + "_ab_stats")
    
    # Format
#     dataiku_ds.format("%.4f", MC)

    # Write recipe output by using the saved pd.DataFrame as argument in the .write_with_schema method
    dataiku_ds.write_with_schema(var_summary_df)