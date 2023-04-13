from binning_machine import BinningMachine
import pandas as pd
import pytest

"""
TEST BinningMachine class
"""

"""
Test Scenario 1
Test given a column, and a width, perform equal width binning based on width.

Input:
col_df = pd.DataFrame
           person_age
0              22 
1              21 
2              25 
3              23 
4              24 
...           ... 
32576          57 
32577          54 
32578          65 
32579          56 
32580          66 

width = int or float

Ouput (2 possibilities): 
(1) pd.Series containing the equal-width bins assigned to each row in the col_df
0              [20.0, 25.0) 
1              [20.0, 25.0)  
2              [25.0, 30.0)  
3              [20.0, 25.0)  
4              [20.0, 25.0)  
...           ... 
32576          [55.0, 60.0)  
32577          [50.0, 55.0)  
32578          [65.0, 70.0)  
32579          [55.0, 60.0)  
32580          [65.0, 70.0)  

OR if error occurs
(2) int: -1

------------------------
Test Cases Design
------------------------
(1) Empty col_df with no data --> error returns -1
(2) Categorical col_df --> error returns -1
(3) Integer col_df & Integer width, with max-min divisible by width
(4) Integer col_df & Integer width, with max-min NOT divisible by width
(5) Integer col_df & Float width, with max-min divisible by width
(6) Integer col_df & Float width, with max-min NOT divisible by width
(7) Float col_df & Integer width, with max-min divisible by width
(8) Float col_df & Integer width, with max-min NOT divisible by width
(9) Float col_df & Float width, with max-min divisible by width
(10) Float col_df & Float width, with max-min NOT divisible by width
(11) col_df with negative number
(12) Width is non-numeric --> error returns -1
"""

eq_width_by_width_test_data = [
    ([], 1, -1), # 1
    (["A", "B", "C", "D", "A", "A", "C"], 5, -1), # 2
    ([0, 3, 5, 100, 8, 18], 10, ['[0.0, 10.0)', '[0.0, 10.0)', '[0.0, 10.0)', '[100.0, 110.0)', '[0.0, 10.0)', '[10.0, 20.0)']), # 3
    ([0, 3, 5, 100, 8, 18], 7, ['[0.0, 7.0)', '[0.0, 7.0)', '[0.0, 7.0)', '[98.0, 105.0)', '[7.0, 14.0)', '[14.0, 21.0)']), # 4
    ([0, 3, 5, 55, 8, 18], 5.5, ['[0.0, 5.5)', '[0.0, 5.5)', '[0.0, 5.5)', '[55.0, 60.5)', '[5.5, 11.0)', '[16.5, 22.0)']), # 5
    ([0, 3, 5, 100, 8, 18], 5.5, ['[0.0, 5.5)', '[0.0, 5.5)', '[0.0, 5.5)', '[99.0, 104.5)', '[5.5, 11.0)', '[16.5, 22.0)']), # 6
    ([0.01, 3.07, 5.5, 9.4, 11.01], 1, ['[0.01, 1.01)', '[3.01, 4.01)', '[5.01, 6.01)', '[9.01, 10.01)', '[11.01, 12.01)']), # 7
    ([0.01, 3.07, 5.5, 9.4, 11.7], 1, ['[0.01, 1.01)', '[3.01, 4.01)', '[5.01, 6.01)', '[9.01, 10.01)', '[11.01, 12.01)']), # 8
    ([0.01, 3.07, 5.5, 9.4, 11.01], 0.005, ['[0.01, 0.015)', '[3.07, 3.075)', '[5.5, 5.505)', '[9.4, 9.405)', '[11.01, 11.015)']), # 9
    ([0.01, 3.07, 5.5, 9.4, 11.01], 0.2, ['[0.01, 0.21)', '[3.01, 3.21)', '[5.41, 5.61)', '[9.21, 9.41)', '[11.01, 11.21)']), # 10
    ([-3.7, 0.01, 3.07, -19.246, 5.5, 9.4, 11.01], 5.2, ['[-8.846, -3.646)', '[-3.646, 1.554)', '[1.554, 6.754)', '[-19.246, -14.046)', '[1.554, 6.754)', '[6.754, 11.954)', '[6.754, 11.954)']), # 11
    ([0.01, 3.07, 5.5, 9.4, 11.01], "", -1), # 12
]

@pytest.mark.parametrize("input,width,expected", eq_width_by_width_test_data)
def test_perform_eq_width_binning_by_width(input, width, expected):
    col_df = pd.DataFrame(input)
    result = BinningMachine.perform_eq_width_binning_by_width(col_df, width)
    
    if expected != -1:
        result = result.to_list()
    
    print("Result: ")
    print(result)
    print("Expected: ")
    print(expected)
    
    assert result == expected



"""
Test Scenario 2
Test given a column, and a number of bins, perform equal width binning based on number of bins.

Input:
col_df = pd.DataFrame
           person_age
0              22 
1              21 
2              25 
3              23 
4              24 
...           ... 
32576          57 
32577          54 
32578          65 
32579          56 
32580          66 

num_bins = int

Ouput: 
(1) pd.Series containing the equal-width bins assigned to each row in the col_df
0              [20.0, 25.0) 
1              [20.0, 25.0)  
2              [25.0, 30.0)  
3              [20.0, 25.0)  
4              [20.0, 25.0)  
...           ... 
32576          [55.0, 60.0)  
32577          [50.0, 55.0)  
32578          [65.0, 70.0)  
32579          [55.0, 60.0)  
32580          [65.0, 70.0) 

------------------------
Test Cases Design
------------------------
(1) Empty col_df with no data --> error returns -1
(2) Categorical col_df --> error returns -1
(3) Float num_bins --> error returns -1
(4) Non-numeric num_bins --> error returns -1
(5) Integer col_df & Integer num_bins, with max-min divisible by num_bins
(6) Integer col_df & Integer num_bins, with max-min NOT divisible by num_bins
(7) Float col_df & Integer num_bins, with max-min divisible by num_bins
(8) Float col_df & Integer num_bins, with max-min NOT divisible by num_bins
(9) col_df with negative number
"""

eq_width_by_num_bins_test_data = [
    ([], 1, -1), # 1
    (["A", "B", "C", "D", "A", "A", "C"], 5, -1), # 2
    ([0, 3, 5, 100, 8, 18], 5.0, -1), # 3
    ([0, 3, 5, 100, 8, 18], "", -1), # 4
    ([0, 3, 5, 100, 8, 18], 10, ['[0.0, 10.0)', '[0.0, 10.0)', '[0.0, 10.0)', '[90.0, 100.1)', '[0.0, 10.0)', '[10.0, 20.0)']), # 5
    ([0, 3, 5, 100, 8, 18], 8, ['[0.0, 12.5)', '[0.0, 12.5)', '[0.0, 12.5)', '[87.5, 100.125)', '[0.0, 12.5)', '[12.5, 25.0)']), # 6
    ([0.01, 3.07, 5.5, 9.4, 11.01], 11, ['[0.01, 1.01)', '[3.01, 4.01)', '[5.01, 6.01)', '[9.01, 10.01)', '[10.01, 11.02)']), # 7
    ([0.01, 3.07, 5.5, 9.4, 11.01], 10, ['[0.01, 1.11)', '[2.21, 3.31)', '[4.41, 5.51)', '[8.81, 9.91)', '[9.91, 11.021)']), # 8
    ([-3.7, 0.01, 3.07, -19.246, 5.5, 9.4, 11.01], 2, ['[-4.118, 11.16128)', '[-4.118, 11.16128)', '[-4.118, 11.16128)', '[-19.246, -4.118)', '[-4.118, 11.16128)', '[-4.118, 11.16128)', '[-4.118, 11.16128)']), # 9
]

@pytest.mark.parametrize("input,num_bins,expected", eq_width_by_num_bins_test_data)
def test_perform_eq_width_binning_by_num_bins(input, num_bins, expected):
    col_df = pd.DataFrame(input)
    result = BinningMachine.perform_eq_width_binning_by_num_bins(col_df, num_bins)
    
    if expected != -1:
        result = result.to_list()
    
    print("Result: ")
    print(result)
    print("Expected: ")
    print(expected)
    
    assert result == expected


"""
Test Scenario 3
Test given a column, the datatype (numerical or categorical), and a frequency, perform equal frequency binning based on frequency.

Input:
col_df = pd.DataFrame
           person_age
0              22 
1              21 
2              25 
3              23 
4              24 
...           ... 
32576          57 
32577          54 
32578          65 
32579          56 
32580          66 

dtype = "numerical" OR "categorical"

freq = int

Ouput: 
(1) pd.Series containing the equal-frequency bins assigned to each row in the col_df
0              [20.0, 25.0) 
1              [20.0, 25.0)  
2              [25.0, 30.0)  
3              [20.0, 25.0)  
4              [20.0, 25.0)  
...           ... 
32576          [55.0, 60.0)  
32577          [50.0, 55.0)  
32578          [65.0, 70.0)  
32579          [55.0, 60.0)  
32580          [65.0, 70.0)  

------------------------
Test Cases Design
------------------------
(1)


"""

eq_freq_by_freq_test_data = [
    
]

@pytest.mark.parametrize("input,freq,expected", eq_freq_by_freq_test_data)
def test_perform_eq_freq_binning_by_freq(input, freq, expected):
    pass


"""
Test Scenario 4
Test given a column, the datatype (numerical or categorical), and a number of bins, perform equal frequency binning based on number of bins.

Input:
col_df = pd.DataFrame
           person_age
0              22 
1              21 
2              25 
3              23 
4              24 
...           ... 
32576          57 
32577          54 
32578          65 
32579          56 
32580          66 

dtype = "numerical" OR "categorical"

num_bins = int

Ouput: 
(1) pd.Series containing the equal-frequency bins assigned to each row in the col_df
0              [20.0, 25.0) 
1              [20.0, 25.0)  
2              [25.0, 30.0)  
3              [20.0, 25.0)  
4              [20.0, 25.0)  
...           ... 
32576          [55.0, 60.0)  
32577          [50.0, 55.0)  
32578          [65.0, 70.0)  
32579          [55.0, 60.0)  
32580          [65.0, 70.0)  

------------------------
Test Cases Design
------------------------
(1)


"""

eq_freq_by_num_bins_test_data = [
    
]

@pytest.mark.parametrize("col_df,dtype,num_bins,expected", eq_freq_by_num_bins_test_data)
def test_perform_eq_freq_binning_by_num_bins(col_df, dtype, num_bins, expected):
    pass

"""
Test Scenario 5
Test given a column, the datatype (numerical or categorical), and bins settings, perform custom binning.

Input:
col_df = pd.DataFrame
           person_age
0              22 
1              21 
2              25 
3              23 
4              24 
...           ... 
32576          57 
32577          54 
32578          65 
32579          56 
32580          66 

dtype = "numerical" OR "categorical"

For numerical column:
bins_settings = [
    {
        "name": "0-9999, 30000-39999",
        "cut_points": [[0, 9999], [30000, 39999]],
    },
    {
        "name": "20000-29999",
        "cut_points": [[20000, 29999]],
    },
]
For categorical column:
bins_settings = [
    {
        "name": "RENT, MORTGAGE",
        "members": ["RENT", "MORTGAGE"],
    },
    {
        "name": "OWN",
        "members": ["OWN"],
    },
]

Ouput: 
(1) pd.Series containing the equal-frequency bins assigned to each row in the col_df
0              [[20, 25), [40, 50)]
1              [[20, 25), [40, 50)]  
2              [25, 30)  
3              [[20, 25), [40, 50)]  
4              [[20, 25), [40, 50)]  
...           ... 
32576          [55, 60)  
32577          [[50, 55), [90, 100), [110, 120)]
32578          [65, 70)  
32579          [55, 60)  
32580          [65, 70)  

------------------------
Test Cases Design
------------------------
(1)


"""

custom_binning_test_data = [
    
]

@pytest.mark.parametrize("col_df,dtype,bins_settings,expected", custom_binning_test_data)
def test_perform_custom_binning(col_df, dtype, bins_settings, expected):
    pass


"""
Test Scenario 6
Test given a column, and bins method, perform either no binning, equal-width binning, equal-frequency binning, or custom binning.

Input:
col_df = pd.DataFrame
           person_age
0              22 
1              21 
2              25 
3              23 
4              24 
...           ... 
32576          57 
32577          54 
32578          65 
32579          56 
32580          66 

dtype = "numerical" OR "categorical"

bin_method = {
    "column": "person_home_ownership",
    "type": "categorical",
    "info_val": 0.07,
    "bins": [
        {
            "name": "RENT, MORTGAGE",
            "members": ["RENT", "MORTGAGE"],
        },
        {
            "name": "OWN",
            "members": ["OWN"],
        },
    ],
}

Ouput: 
(1) pd.Series containing the equal-frequency bins assigned to each row in the col_df
0              [[20, 25), [40, 50)]
1              [[20, 25), [40, 50)]  
2              [25, 30)  
3              [[20, 25), [40, 50)]  
4              [[20, 25), [40, 50)]  
...           ... 
32576          [55, 60)  
32577          [[50, 55), [90, 100), [110, 120)]
32578          [65, 70)  
32579          [55, 60)  
32580          [65, 70)  

------------------------
Test Cases Design
------------------------
(1)


"""

col_binning_test_data = [
    
]

@pytest.mark.parametrize("col_df,bin_method,expected", col_binning_test_data)
def test_perform_binning_on_col(col_df, bin_method, expected):
    pass


"""
Test Scenario 6
Test given a dataframe and bins settings, perform binning for the whole dataframe.

Input:
dframe = pd.DataFrame
       person_age  person_income person_home_ownership  ...  cb_person_default_on_file cb_person_cred_hist_length paid_past_due
0              22          59000                  RENT  ...                          Y                          3           114
1              21           9600                   OWN  ...                          N                          2            73
2              25           9600              MORTGAGE  ...                          N                          3           109
3              23          65500                  RENT  ...                          N                          2           119
4              24          54400                  RENT  ...                          Y                          4           106
...           ...            ...                   ...  ...                        ...                        ...           ...
32576          57          53000              MORTGAGE  ...                          N                         30            76
32577          54         120000              MORTGAGE  ...                          N                         19            81
32578          65          76000                  RENT  ...                          N                         28           104
32579          56         150000              MORTGAGE  ...                          N                         26            47
32580          66          42000                  RENT  ...                          N                         30            24

bins_settings_list = [
    {
        "column": "person_age",  # from Confirm Input Dataset Page
        "type": "numerical",  # from Confirm Input Dataset Page
        "info_val": 0.09,
        "bins": "none",  # either algo or custom binning (default = "none") ["none", "equal width", "equal frequency", (custom binning)]
    },
    {
        "column": "person_income",
        "type": "numerical",
        "info_val": 0.11,
        "bins": [
            {
                "name": "0-9999, 30000-39999",
                "cut_points": [[0, 9999], [30000, 39999]],
            },
            {
                "name": "20000-29999",
                "cut_points": [[20000, 29999]],
            },
        ],
    },
    {
        "column": "loan_grade",
        "type": "categorical",
        "info_val": 0.33,
        "bins": {
                    "algo": "eqaul width",
                    "method": "width", # OR num_bins
                    "value": 1, # represent width or num_bins
                },
    },
    {
        "column": "person_home_ownership",
        "type": "categorical",
        "info_val": 0.07,
        "bins": [
            {
                "name": "RENT, MORTGAGE",
                "members": ["RENT", "MORTGAGE"],
            },
            {
                "name": "OWN",
                "members": ["OWN"],
            },
        ],
    },
]

Ouput: 
(1) pd.DataFrame containing the both the original columns & the binned columns
       person_age  person_income person_home_ownership  ...  person_age_binned   person_income_binned
0              22          59000                  RENT  ...       [20, 30)            [0, 60000)                  
1              21           9600                   OWN  ...       [20, 30)            [0, 60000)   
2              25           9600              MORTGAGE  ...       [20, 30)            [0, 60000)   
3              23          65500                  RENT  ...       [20, 30)         [60000, 200000) 
4              24          54400                  RENT  ...       [20, 30)            [0, 60000)      
...           ...            ...                   ...  ...          ...                 ...           
32576          57          53000              MORTGAGE  ...       [50, 70)            [0, 60000)    
32577          54         120000              MORTGAGE  ...       [50, 70)         [60000, 200000)  
32578          65          76000                  RENT  ...       [50, 70)         [60000, 200000)        
32579          56         150000              MORTGAGE  ...       [50, 70)         [60000, 200000)        
32580          66          42000                  RENT  ...       [50, 70)            [0, 60000)       

------------------------
Test Cases Design
------------------------
(1)


"""

df_binning_test_data = [
    
]

@pytest.mark.parametrize("dframe,bins_settings_list,expected", df_binning_test_data)
def test_perform_binning_on_whole_df(dframe, bins_settings_list, expected):
    pass
