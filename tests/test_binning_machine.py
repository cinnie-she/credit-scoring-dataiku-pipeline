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
(13) Single bin
(14) With missing values
(15) width == 0
(16) width == -1
(17) col_df with all None values
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
    ([0, 10], 20, ['[0.0, 20.0)', '[0.0, 20.0)']), # 13
    ([0, 3, 5, 100, 8, None, None, 18], 5, ['[0.0, 5.0)', '[0.0, 5.0)', '[5.0, 10.0)', '[100.0, 105.0)', '[5.0, 10.0)', None, None, '[15.0, 20.0)']), # 14
    ([0, 3, 5, 100, 8, 18], 0, -1), # 15
    ([0, 3, 5, 100, 8, 18], -1, -1), # 16
    ([None, None, None, None, None, None], 3, [None, None, None, None, None, None]), # 17
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
(10) Single bin
(11) With missing value
(12) num_bins == 0
(13) num_bins < 0
(14) col_df with all None values
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
    ([0, 10], 1, ['[0.0, 10.1)', '[0.0, 10.1)']), # 10
    ([0, 3, 5, 100, 8, None, None, 18], 2, ['[0.0, 50.0)', '[0.0, 50.0)', '[0.0, 50.0)', '[50.0, 100.5)', '[0.0, 50.0)', None, None, '[0.0, 50.0)']), # 11
    ([0, 3, 5, 100, 8, 18], 0, -1), # 12
    ([0, 3, 5, 100, 8, 18], -1, -1), # 13
    ([None, None, None, None, None, None], 3, [None, None, None, None, None, None]), # 14
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
Test given a column and a frequency, perform equal frequency binning based on frequency.

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
(1) Empty col_df with no data --> error returns -1
(2) Categorical col_df --> error returns -1
(3) Float frequency --> error returns -1
(4) Non-numeric frequency --> error returns -1
(5) Frequency == 0 --> error returns -1
(6) Frequency < 0 --> error returns -1
(7) Frequency > number of samples in col_df --> error returns -1
(8) Frequency == number of samples in col_df
(9) Frequency == number of samples in col_df - 1 
(10) Integer col_df & Integer num_bins, with number of samples divisible by frequency
(11) Integer col_df & Integer num_bins, with number of samples NOT divisible by frequency
(12) Float col_df & Integer num_bins, with number of samples divisible by frequency
(13) Float col_df & Integer num_bins, with number of samples NOT divisible by frequency
(14) col_df with negative number
(15) With missing value
(16) col_df with all None values
(17) col_df with all same values
"""

eq_freq_by_freq_test_data = [
    ([], 1, -1), # 1
    (["A", "B", "C", "D", "E"], 3, -1), # 2
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], 3.0, -1), # 3
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], "A", -1), # 4
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], 0, -1), # 5
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], -1, -1), # 6
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], 10, -1), # 7
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], 9, ['[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)']), # 8
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], 8, ['[-0.001, 8.0)', '[-0.001, 8.0)', '[-0.001, 8.0)', '[-0.001, 8.0)', '[8.0, 101.0)', '[8.0, 101.0)', '[8.0, 101.0)', '[-0.001, 8.0)', '[8.0, 101.0)']), # 9
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], 3, ['[6.333, 9.667)', '[-0.001, 6.333)', '[-0.001, 6.333)', '[-0.001, 6.333)', '[9.667, 101.0)', '[9.667, 101.0)', '[9.667, 101.0)', '[6.333, 9.667)', '[6.333, 9.667)']), # 10
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], 2, ['[4.2, 7.2)', '[-0.001, 4.2)', '[-0.001, 4.2)', '[4.2, 7.2)', '[13.8, 101.0)', '[8.8, 13.8)', '[13.8, 101.0)', '[7.2, 8.8)', '[8.8, 13.8)']), # 11
    ([0.01, 3.07, 5.5, 9.4, 11.01, 15.33], 2, ['[0.009000000000000001, 4.69)', '[0.009000000000000001, 4.69)', '[4.69, 9.937)', '[4.69, 9.937)', '[9.937, 15.33)', '[9.937, 15.33)']), # 12
    ([0.01, 3.07, 5.5, 9.4, 11.01, 15.33], 4, ['[0.009000000000000001, 7.45)', '[0.009000000000000001, 7.45)', '[0.009000000000000001, 7.45)', '[7.45, 15.33)', '[7.45, 15.33)', '[7.45, 15.33)']), # 13
    ([-3.7, 0.01, 3.07, -19.246, 5.5, 9.4, 11.01], 4, ['[-19.247, 3.07)', '[-19.247, 3.07)', '[-19.247, 3.07)', '[-19.247, 3.07)', '[3.07, 11.01)', '[3.07, 11.01)', '[3.07, 11.01)']),  # 14
    ([7,0, 3, 5, 101, 11, 18, 8, None, 9], 4, ['[6.333, 9.667)', '[-0.001, 6.333)', '[-0.001, 6.333)', '[-0.001, 6.333)', '[9.667, 101.0)', '[9.667, 101.0)', '[9.667, 101.0)', '[6.333, 9.667)', None, '[6.333, 9.667)']), # 15
    ([None, None, None, None, None, None], 3, [None, None, None, None, None, None]), # 16
    ([3, 3, 3, 3, 3, 3], 3, ['[3.0, 4.0)', '[3.0, 4.0)', '[3.0, 4.0)', '[3.0, 4.0)', '[3.0, 4.0)', '[3.0, 4.0)']), # 17
]

@pytest.mark.parametrize("input,freq,expected", eq_freq_by_freq_test_data)
def test_perform_eq_freq_binning_by_freq(input, freq, expected):
    col_df = pd.DataFrame(input)
    result = BinningMachine.perform_eq_freq_binning_by_freq(col_df, freq)
    
    if expected != -1:
        result = result.to_list()
    
    print("Result: ")
    print(result)
    print("Expected: ")
    print(expected)
    
    assert result == expected


"""
Test Scenario 4
Test given a column, and a number of bins, perform equal frequency binning based on number of bins.

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
(1) Empty col_df with no data --> error returns -1
(2) Categorical col_df --> error returns -1
(3) Float num_bins --> error returns -1
(4) Non-numeric num_bins --> error returns -1
(5) num_bins == 0 --> error returns -1
(6) num_bins < 0 --> error returns -1
(7) num_bins == 1
(8) Integer col_df & Integer num_bins, with number of samples divisible by num_bins
(9) Integer col_df & Integer num_bins, with number of samples NOT divisible by num_bins
(10) Float col_df & Integer num_bins, with number of samples divisible by num_bins
(11) Float col_df & Integer num_bins, with number of samples NOT divisible by num_bins
(12) col_df with negative number
(13) With missing value
(14) col_df with all None values
(15) col_df with all same values

"""

eq_freq_by_num_bins_test_data = [
    ([], 1, -1), # 1
    (["A", "B", "C", "D", "E"], 2, -1), # 2
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], 3.0, -1), # 3
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], "D", -1), # 4
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], 0, -1), # 5
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], -1, -1), # 6
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], 1, ['[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)']), # 7
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], 3, ['[6.333, 9.667)', '[-0.001, 6.333)', '[-0.001, 6.333)', '[-0.001, 6.333)', '[9.667, 101.0)', '[9.667, 101.0)', '[9.667, 101.0)', '[6.333, 9.667)', '[6.333, 9.667)']), # 8
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], 5, ['[4.2, 7.2)', '[-0.001, 4.2)', '[-0.001, 4.2)', '[4.2, 7.2)', '[13.8, 101.0)', '[8.8, 13.8)', '[13.8, 101.0)', '[7.2, 8.8)', '[8.8, 13.8)']), # 9
    ([0.01, 3.07, 5.5, 9.4, 11.01, 15.33], 2, ['[0.009000000000000001, 7.45)', '[0.009000000000000001, 7.45)', '[0.009000000000000001, 7.45)', '[7.45, 15.33)', '[7.45, 15.33)', '[7.45, 15.33)']), # 10
    ([0.01, 3.07, 5.5, 9.4, 11.01, 15.33], 4, ['[0.009000000000000001, 3.677)', '[0.009000000000000001, 3.677)', '[3.677, 7.45)', '[7.45, 10.608)', '[10.608, 15.33)', '[10.608, 15.33)']), # 11
    ([-3.7, 0.01, 3.07, -19.246, 5.5, 9.4, 11.01], 3, ['[-19.247, 0.01)', '[-19.247, 0.01)', '[0.01, 5.5)', '[-19.247, 0.01)', '[0.01, 5.5)', '[5.5, 11.01)', '[5.5, 11.01)']), # 12
    ([7,0, 3, 5, 101, 11, 18, 8, None, 9], 3, ['[6.333, 9.667)', '[-0.001, 6.333)', '[-0.001, 6.333)', '[-0.001, 6.333)', '[9.667, 101.0)', '[9.667, 101.0)', '[9.667, 101.0)', '[6.333, 9.667)', None, '[6.333, 9.667)']), # 13
    ([None, None, None, None, None, None], 3, [None, None, None, None, None, None]), # 16
    ([3, 3, 3, 3, 3, 3], 3, ['[3.0, 4.0)', '[3.0, 4.0)', '[3.0, 4.0)', '[3.0, 4.0)', '[3.0, 4.0)', '[3.0, 4.0)']), # 17
]

@pytest.mark.parametrize("input,num_bins,expected", eq_freq_by_num_bins_test_data)
def test_perform_eq_freq_binning_by_num_bins(input, num_bins, expected):
    col_df = pd.DataFrame(input)
    result = BinningMachine.perform_eq_freq_binning_by_num_bins(col_df, num_bins)
    
    if expected != -1:
        result = result.to_list()
    
    print("Result: ")
    print(result)
    print("Expected: ")
    print(expected)
    
    assert result == expected

"""
Test Scenario 5
Test given a categorical column, and bins settings, perform custom binning.

Input:
col_df = pd.DataFrame
           loan_grade
0              A 
1              A 
2              C 
3              D 
4              B 
...           ... 
32576          B 
32577          B 
32578          E 
32579          B 
32580          A 

For categorical column:
bins_settings = [
    {
        "name": ["A", "B""],
        "members": ["A", "A"],
    },
    {
        "name": ["E"],
        "members": ["E"],
    },
]

Ouput: 
(1) pd.Series containing the equal-frequency bins assigned to each row in the col_df
0              ["A", "B"]
1              ["A", "B"]  
2              ["C", "D"]  
3              ["A", "B"]
4              ["A", "B"]  
...           ... 
32576          ["C", "D"]  
32577          ["A", "B"]
32578          ["E"]  
32579          ["E"]  
32580          ["C", "D"]  

------------------------
Test Cases Design
------------------------
(1) Empty col_df
(2) Non-empty col_df + Empty bins_settings
(3) Numerical col_df + typical bins_settings
(4) Categorical col_df + typical bins_settings
(5) Numerical col_df + bins_settings with some values of col_df not in any bins
(6) Categorical col_df + bins_settings with some values of col_df not in any bins
"""

categorical_custom_binning_test_data = [
    ([], [], -1), # 1
    (["A", "B", "B", "A", "C", "D", "D", "E"], [], [None, None, None, None, None, None, None, None]), # 2
    ([1, 2, 3, 2, 4, 5, 1], [{"name": "nice", "elements": [1, 3, 5]}, {"name": "oh", "elements": [2, 4, 6]}], ["nice", "oh", "nice", "oh", "oh", "nice", "nice"]), # 3
    (["A", "B", "B", "A", "C", "D", "D", "E"], [{"name": "good", "elements": ["A", "B"]}, {"name": "ok", "elements": ["C", "D"]}, {"name": "poor", "elements": ["E"]}], ["good", "good", "good", "good", "ok", "ok", "ok", "poor"]), # 4
    ([1, 2, 3, 2, 4, 5, 1], [{"name": "nice", "elements": [1]}, {"name": "oh", "elements": [2, 4, 6]}], ["nice", "oh", None, "oh", "oh", None, "nice"]), # 5
    (["A", "B", "B", "A", "C", "D", "D", "E"], [{"name": "good", "elements": ["A"]}, {"name": "ok", "elements": ["C", "D"]}, {"name": "poor", "elements": ["E"]}], ["good", None, None, "good", "ok", "ok", "ok", "poor"]), # 6
    (["A", "B", "B", "A", "C", "D", None, "E"], [{"name": "good", "elements": ["A"]}, {"name": "ok", "elements": ["C", "D"]}, {"name": "poor", "elements": ["E"]}], ["good", None, None, "good", "ok", "ok", None, "poor"]), # 7
]

@pytest.mark.parametrize("input,bins_settings,expected", categorical_custom_binning_test_data)
def test_perform_categorical_custom_binning(input, bins_settings, expected):
    col_df = pd.DataFrame(input)
    result = BinningMachine.perform_categorical_custom_binning(col_df, bins_settings)
    
    if expected != -1:
        result = result.to_list()
    
    print("Result: ")
    print(result)
    print("Expected: ")
    print(expected)
    
    assert result == expected
    

"""
Test Scenario 6
Test given a categorical column, and bins settings, perform custom binning.

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
(1) Empty col_df
(2) Non-empty col_df + Empty bins_settings
(3) Numerical col_df + typical bins_settings
(4) Numerical col_df + bins_settings with some values of col_df not in any bins
(5) With empty row

"""
numerical_custom_binning_test_data = [
    ([], [{"name": "good", "ranges": [[10, 20], [25, 50]]}, {"name": "poor", "ranges": [[80, 100], [110, 120]]}], -1), # 1
    ([18, 19, 25, 40, 99, 90, 25, 19], [], [None, None, None, None, None, None, None, None]), # 2
    ([18, 19, 25, 40, 99, 90, 25, 19], [{"name": "good", "ranges": [[10, 20], [25, 50]]}, {"name": "poor", "ranges": [[80, 100], [110, 120]]}], ["good", "good", "good", "good", "poor", "poor", "good", "good"]), # 3
    ([18, 19, 25, 20, 99, 90, 25, 23], [{"name": "good", "ranges": [[10, 20], [25, 50]]}, {"name": "poor", "ranges": [[80, 100], [110, 120]]}], ["good", "good", "good", None, "poor", "poor", "good", None]), # 4
    ([18, 19, 25, 20, 99, None, 25, 23], [{"name": "good", "ranges": [[10, 20], [25, 50]]}, {"name": "poor", "ranges": [[80, 100], [110, 120]]}], ["good", "good", "good", None, "poor", None, "good", None]), # 5
]

@pytest.mark.parametrize("input,bins_settings,expected", numerical_custom_binning_test_data)
def test_perform_numerical_custom_binning(input, bins_settings, expected):
    col_df = pd.DataFrame(input)
    result = BinningMachine.perform_numerical_custom_binning(col_df, bins_settings)
    
    if expected != -1:
        result = result.to_list()
    
    print("Result: ")
    print(result)
    print("Expected: ")
    print(expected)
    
    assert result == expected

"""
Test Scenario 7
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
(1) Empty dataframe
(2) Numerical col_df with no binning
(3) Categorical col_df with no binning
...Repeat all test cases for individual algorithms
(4 - 20) Equal-width based on width
(21 - 34) Equal-width based on num_bins
(35 - 51) Equal-frequency based on frequency
(52 - 66) Equal-frequency based on num_bins
(67 - 73) Categorical custom binning
(74 - 78) Numerical custom binning

"""

col_binning_test_data = [
    ([], {"column": "person_age", "type": "numerical", "bins": "none"}, -1), # 1
    ([1, 3, 10, 25, 95, 39, 48, 1, 2], {"column": "person_age", "type": "numerical", "bins": "none"}, [1, 3, 10, 25, 95, 39, 48, 1, 2]), # 2
    (["A", "C", "D", "A", "B", "B", "C", "D"], {"column": "loan_grade", "type": "categorical", "bins": "none"}, ["A", "C", "D", "A", "B", "B", "C", "D"]), # 3
    # equal-width by width
    ([], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 1}}, -1), # 4
    (["A", "B", "C", "D", "A", "A", "C"], {"column": "person_age", "type": "categorical", "bins": {"algo": "equal width", "method": "width", "value": 5}}, -1), # 5
    ([0, 3, 5, 100, 8, 18], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 10}}, ['[0.0, 10.0)', '[0.0, 10.0)', '[0.0, 10.0)', '[100.0, 110.0)', '[0.0, 10.0)', '[10.0, 20.0)']), # 6
    ([0, 3, 5, 100, 8, 18], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 7}}, ['[0.0, 7.0)', '[0.0, 7.0)', '[0.0, 7.0)', '[98.0, 105.0)', '[7.0, 14.0)', '[14.0, 21.0)']), # 7
    ([0, 3, 5, 55, 8, 18], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 5.5}}, ['[0.0, 5.5)', '[0.0, 5.5)', '[0.0, 5.5)', '[55.0, 60.5)', '[5.5, 11.0)', '[16.5, 22.0)']), # 8
    ([0, 3, 5, 100, 8, 18], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 5.5}}, ['[0.0, 5.5)', '[0.0, 5.5)', '[0.0, 5.5)', '[99.0, 104.5)', '[5.5, 11.0)', '[16.5, 22.0)']), # 9
    ([0.01, 3.07, 5.5, 9.4, 11.01], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 1}}, ['[0.01, 1.01)', '[3.01, 4.01)', '[5.01, 6.01)', '[9.01, 10.01)', '[11.01, 12.01)']), # 10
    ([0.01, 3.07, 5.5, 9.4, 11.7], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 1}}, ['[0.01, 1.01)', '[3.01, 4.01)', '[5.01, 6.01)', '[9.01, 10.01)', '[11.01, 12.01)']), # 11
    ([0.01, 3.07, 5.5, 9.4, 11.01], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 0.005}}, ['[0.01, 0.015)', '[3.07, 3.075)', '[5.5, 5.505)', '[9.4, 9.405)', '[11.01, 11.015)']), # 12
    ([0.01, 3.07, 5.5, 9.4, 11.01], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 0.2}}, ['[0.01, 0.21)', '[3.01, 3.21)', '[5.41, 5.61)', '[9.21, 9.41)', '[11.01, 11.21)']), # 13
    ([-3.7, 0.01, 3.07, -19.246, 5.5, 9.4, 11.01], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 5.2}}, ['[-8.846, -3.646)', '[-3.646, 1.554)', '[1.554, 6.754)', '[-19.246, -14.046)', '[1.554, 6.754)', '[6.754, 11.954)', '[6.754, 11.954)']), # 14
    ([0.01, 3.07, 5.5, 9.4, 11.01], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": ""}}, -1), # 15
    ([0, 10], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 20}}, ['[0.0, 20.0)', '[0.0, 20.0)']), # 16
    ([0, 3, 5, 100, 8, None, None, 18],  {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 5}}, ['[0.0, 5.0)', '[0.0, 5.0)', '[5.0, 10.0)', '[100.0, 105.0)', '[5.0, 10.0)', None, None, '[15.0, 20.0)']), # 17
    ([0, 3, 5, 100, 8, 18], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 0}}, -1), # 18
    ([0, 3, 5, 100, 8, 18], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": -1}}, -1), # 19
    ([None, None, None, None, None, None], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 3}}, [None, None, None, None, None, None]), # 20
    # equal-width by num_bins
    ([], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 1}}, -1), # 21
    (["A", "B", "C", "D", "A", "A", "C"], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 5}}, -1), # 22
    ([0, 3, 5, 100, 8, 18], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 5.0}}, -1), # 23
    ([0, 3, 5, 100, 8, 18], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": ""}}, -1), # 24
    ([0, 3, 5, 100, 8, 18], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 10}}, ['[0.0, 10.0)', '[0.0, 10.0)', '[0.0, 10.0)', '[90.0, 100.1)', '[0.0, 10.0)', '[10.0, 20.0)']), # 25
    ([0, 3, 5, 100, 8, 18], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 8}}, ['[0.0, 12.5)', '[0.0, 12.5)', '[0.0, 12.5)', '[87.5, 100.125)', '[0.0, 12.5)', '[12.5, 25.0)']), # 26
    ([0.01, 3.07, 5.5, 9.4, 11.01], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 11}}, ['[0.01, 1.01)', '[3.01, 4.01)', '[5.01, 6.01)', '[9.01, 10.01)', '[10.01, 11.02)']), # 27
    ([0.01, 3.07, 5.5, 9.4, 11.01], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 10}}, ['[0.01, 1.11)', '[2.21, 3.31)', '[4.41, 5.51)', '[8.81, 9.91)', '[9.91, 11.021)']), # 28
    ([-3.7, 0.01, 3.07, -19.246, 5.5, 9.4, 11.01], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 2}}, ['[-4.118, 11.16128)', '[-4.118, 11.16128)', '[-4.118, 11.16128)', '[-19.246, -4.118)', '[-4.118, 11.16128)', '[-4.118, 11.16128)', '[-4.118, 11.16128)']), # 29
    ([0, 10], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 1}}, ['[0.0, 10.1)', '[0.0, 10.1)']), # 30
    ([0, 3, 5, 100, 8, None, None, 18], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 2}}, ['[0.0, 50.0)', '[0.0, 50.0)', '[0.0, 50.0)', '[50.0, 100.5)', '[0.0, 50.0)', None, None, '[0.0, 50.0)']), # 31
    ([0, 3, 5, 100, 8, 18], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 0}}, -1), # 32
    ([0, 3, 5, 100, 8, 18], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": -1}}, -1), # 33
    ([None, None, None, None, None, None], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 3}}, [None, None, None, None, None, None]), # 34
    # equal-frequency by frequency
    ([], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 1}}, -1), # 35
    (["A", "B", "C", "D", "E"], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 3}}, -1), # 36
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 3.0}}, -1), # 37
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": "A"}}, -1), # 38
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 0}}, -1), # 39
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": -1}}, -1), # 40
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 10}}, -1), # 41
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 9}}, ['[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)']), # 42
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 8}}, ['[-0.001, 8.0)', '[-0.001, 8.0)', '[-0.001, 8.0)', '[-0.001, 8.0)', '[8.0, 101.0)', '[8.0, 101.0)', '[8.0, 101.0)', '[-0.001, 8.0)', '[8.0, 101.0)']), # 43
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 3}}, ['[6.333, 9.667)', '[-0.001, 6.333)', '[-0.001, 6.333)', '[-0.001, 6.333)', '[9.667, 101.0)', '[9.667, 101.0)', '[9.667, 101.0)', '[6.333, 9.667)', '[6.333, 9.667)']), # 44
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 2}}, ['[4.2, 7.2)', '[-0.001, 4.2)', '[-0.001, 4.2)', '[4.2, 7.2)', '[13.8, 101.0)', '[8.8, 13.8)', '[13.8, 101.0)', '[7.2, 8.8)', '[8.8, 13.8)']), # 45
    ([0.01, 3.07, 5.5, 9.4, 11.01, 15.33], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 2}}, ['[0.009000000000000001, 4.69)', '[0.009000000000000001, 4.69)', '[4.69, 9.937)', '[4.69, 9.937)', '[9.937, 15.33)', '[9.937, 15.33)']), # 46
    ([0.01, 3.07, 5.5, 9.4, 11.01, 15.33], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 4}}, ['[0.009000000000000001, 7.45)', '[0.009000000000000001, 7.45)', '[0.009000000000000001, 7.45)', '[7.45, 15.33)', '[7.45, 15.33)', '[7.45, 15.33)']), # 47
    ([-3.7, 0.01, 3.07, -19.246, 5.5, 9.4, 11.01], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 4}}, ['[-19.247, 3.07)', '[-19.247, 3.07)', '[-19.247, 3.07)', '[-19.247, 3.07)', '[3.07, 11.01)', '[3.07, 11.01)', '[3.07, 11.01)']), # 48
    ([7,0, 3, 5, 101, 11, 18, 8, None, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 4}}, ['[6.333, 9.667)', '[-0.001, 6.333)', '[-0.001, 6.333)', '[-0.001, 6.333)', '[9.667, 101.0)', '[9.667, 101.0)', '[9.667, 101.0)', '[6.333, 9.667)', None, '[6.333, 9.667)']), # 49
    ([None, None, None, None, None, None], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 3}}, [None, None, None, None, None, None]), # 50
    ([3, 3, 3, 3, 3, 3], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 3}}, ['[3.0, 4.0)', '[3.0, 4.0)', '[3.0, 4.0)', '[3.0, 4.0)', '[3.0, 4.0)', '[3.0, 4.0)']), # 51
    # equal-frequency by num_bins
    ([], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 1}}, -1), # 52
    (["A", "B", "C", "D", "E"], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 2}}, -1), # 53
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 3.0}}, -1), # 54
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": "D"}}, -1), # 55
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 0}}, -1), # 56
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": -1}}, -1), # 57
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 1}}, ['[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)', '[-0.001, 101.0)']), # 58
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 3}}, ['[6.333, 9.667)', '[-0.001, 6.333)', '[-0.001, 6.333)', '[-0.001, 6.333)', '[9.667, 101.0)', '[9.667, 101.0)', '[9.667, 101.0)', '[6.333, 9.667)', '[6.333, 9.667)']), # 59
    ([7, 0, 3, 5, 101, 11, 18, 8, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 5}}, ['[4.2, 7.2)', '[-0.001, 4.2)', '[-0.001, 4.2)', '[4.2, 7.2)', '[13.8, 101.0)', '[8.8, 13.8)', '[13.8, 101.0)', '[7.2, 8.8)', '[8.8, 13.8)']), # 60
    ([0.01, 3.07, 5.5, 9.4, 11.01, 15.33], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 2}}, ['[0.009000000000000001, 7.45)', '[0.009000000000000001, 7.45)', '[0.009000000000000001, 7.45)', '[7.45, 15.33)', '[7.45, 15.33)', '[7.45, 15.33)']), # 61
    ([0.01, 3.07, 5.5, 9.4, 11.01, 15.33], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 4}}, ['[0.009000000000000001, 3.677)', '[0.009000000000000001, 3.677)', '[3.677, 7.45)', '[7.45, 10.608)', '[10.608, 15.33)', '[10.608, 15.33)']), # 62
    ([-3.7, 0.01, 3.07, -19.246, 5.5, 9.4, 11.01], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 3}}, ['[-19.247, 0.01)', '[-19.247, 0.01)', '[0.01, 5.5)', '[-19.247, 0.01)', '[0.01, 5.5)', '[5.5, 11.01)', '[5.5, 11.01)']), # 63
    ([7,0, 3, 5, 101, 11, 18, 8, None, 9], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 3}}, ['[6.333, 9.667)', '[-0.001, 6.333)', '[-0.001, 6.333)', '[-0.001, 6.333)', '[9.667, 101.0)', '[9.667, 101.0)', '[9.667, 101.0)', '[6.333, 9.667)', None, '[6.333, 9.667)']), # 64
    ([None, None, None, None, None, None], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 3}}, [None, None, None, None, None, None]), # 65
    ([3, 3, 3, 3, 3, 3], {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 3}}, ['[3.0, 4.0)', '[3.0, 4.0)', '[3.0, 4.0)', '[3.0, 4.0)', '[3.0, 4.0)', '[3.0, 4.0)']), # 66
    # categorical custom binning
    ([], {"column": "loan_grade", "type": "categorical", "bins": []}, -1), # 67
    (["A", "B", "B", "A", "C", "D", "D", "E"], {"column": "loan_grade", "type": "categorical", "bins": []}, [None, None, None, None, None, None, None, None]), # 68
    ([1, 2, 3, 2, 4, 5, 1], {"column": "loan_grade", "type": "categorical", "bins": [{"name": "nice", "elements": [1, 3, 5]}, {"name": "oh", "elements": [2, 4, 6]}]}, ["nice", "oh", "nice", "oh", "oh", "nice", "nice"]), # 69
    (["A", "B", "B", "A", "C", "D", "D", "E"], {"column": "loan_grade", "type": "categorical", "bins": [{"name": "good", "elements": ["A", "B"]}, {"name": "ok", "elements": ["C", "D"]}, {"name": "poor", "elements": ["E"]}]}, ["good", "good", "good", "good", "ok", "ok", "ok", "poor"]), # 70
    ([1, 2, 3, 2, 4, 5, 1], {"column": "loan_grade", "type": "categorical", "bins": [{"name": "nice", "elements": [1]}, {"name": "oh", "elements": [2, 4, 6]}]}, ["nice", "oh", None, "oh", "oh", None, "nice"]), # 71
    (["A", "B", "B", "A", "C", "D", "D", "E"], {"column": "loan_grade", "type": "categorical", "bins": [{"name": "good", "elements": ["A"]}, {"name": "ok", "elements": ["C", "D"]}, {"name": "poor", "elements": ["E"]}]}, ["good", None, None, "good", "ok", "ok", "ok", "poor"]), # 72
    (["A", "B", "B", "A", "C", "D", None, "E"], {"column": "loan_grade", "type": "categorical", "bins": [{"name": "good", "elements": ["A"]}, {"name": "ok", "elements": ["C", "D"]}, {"name": "poor", "elements": ["E"]}]}, ["good", None, None, "good", "ok", "ok", None, "poor"]), # 73
    # numerical custom binning
    ([], {"column": "person_age", "type": "numerical", "bins": [{"name": "good", "ranges": [[10, 20], [25, 50]]}, {"name": "poor", "ranges": [[80, 100], [110, 120]]}]}, -1), # 74
    ([18, 19, 25, 40, 99, 90, 25, 19], {"column": "person_age", "type": "numerical", "bins": []}, [None, None, None, None, None, None, None, None]), # 75
    ([18, 19, 25, 40, 99, 90, 25, 19], {"column": "person_age", "type": "numerical", "bins": [{"name": "good", "ranges": [[10, 20], [25, 50]]}, {"name": "poor", "ranges": [[80, 100], [110, 120]]}]}, ["good", "good", "good", "good", "poor", "poor", "good", "good"]), # 76
    ([18, 19, 25, 20, 99, 90, 25, 23], {"column": "person_age", "type": "numerical", "bins": [{"name": "good", "ranges": [[10, 20], [25, 50]]}, {"name": "poor", "ranges": [[80, 100], [110, 120]]}]}, ["good", "good", "good", None, "poor", "poor", "good", None]), # 77
    ([18, 19, 25, 20, 99, None, 25, 23], {"column": "person_age", "type": "numerical", "bins": [{"name": "good", "ranges": [[10, 20], [25, 50]]}, {"name": "poor", "ranges": [[80, 100], [110, 120]]}]}, ["good", "good", "good", None, "poor", None, "good", None]), # 78
]

@pytest.mark.parametrize("input,col_bins_settings,expected", col_binning_test_data)
def test_perform_binning_on_col(input, col_bins_settings, expected):
    col_df = pd.DataFrame(input)
    result = BinningMachine.perform_binning_on_col(col_df, col_bins_settings)
    
    if expected != -1:
        result = result.to_list()
    
    print("Result: ")
    print(result)
    print("Expected: ")
    print(expected)
    
    assert result == expected


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
(1) Empty dframe
(2) Single numerical column + no binning
(3) Single numerical column + equal width (by width)
(4) Single numerical column + equal width (by num_bins)
(5) Single numerical column + equal frequency (by frequency)
(6) Single numerical column + equal frequency (by num_bins)
(7) Single numerical column + custom binning
(8) Single categorical column + no binning
(9) Single categorical column + equal width (by width) --> no such thing --> error (i.e., -1)
(10) Single categorical column + equal width (by num_bins) --> no such thing --> error (i.e., -1)
(11) Single categorical column + equal frequency (by frequency) --> no such thing --> error (i.e., -1)
(12) Single categorical column + equal frequency (by num_bins) --> no such thing --> error (i.e., -1)
(13) Single categorical column + custom binning
(14) 2 columns (1 returns error i.e., -1)
(15) Multiple columns with 1 having no bins_settings + typical cases

"""

df_binning_test_data = [
    ({}, [{"column": "person_age", "type": "numerical", "bins": "none"}], []), # 1
    ({"person_age": [1, 3, 10, 25, 95, 39, 48, 1, 2]}, [{"column": "person_age", "type": "numerical", "bins": "none"}], [[1, 1], [3, 3], [10, 10], [25, 25], [95, 95], [39, 39], [48, 48], [1, 1], [2, 2]]), # 2
    ({"person_age": [-3.7, 0.01, 3.07, -19.246, 5.5, 9.4, 11.01]}, [{"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 5.2}}], [[-3.7, '[-8.846, -3.646)'], [0.01, '[-3.646, 1.554)'], [3.07, '[1.554, 6.754)'], [-19.246, '[-19.246, -14.046)'], [5.5, '[1.554, 6.754)'], [9.4, '[6.754, 11.954)'], [11.01, '[6.754, 11.954)']]), # 3
    ({"person_age": [-3.7, 0.01, 3.07, -19.246, 5.5, 9.4, 11.01]}, [{"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 2}}], [[-3.7, '[-4.118, 11.16128)'], [0.01, '[-4.118, 11.16128)'], [3.07, '[-4.118, 11.16128)'], [-19.246, '[-19.246, -4.118)'], [5.5, '[-4.118, 11.16128)'], [9.4, '[-4.118, 11.16128)'], [11.01, '[-4.118, 11.16128)']]), # 4
    ({"person_age": [-3.7, 0.01, 3.07, -19.246, 5.5, 9.4, 11.01]}, [{"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 4}}], [[-3.7, '[-19.247, 3.07)'], [0.01, '[-19.247, 3.07)'], [3.07, '[-19.247, 3.07)'], [-19.246, '[-19.247, 3.07)'], [5.5, '[3.07, 11.01)'], [9.4, '[3.07, 11.01)'], [11.01, '[3.07, 11.01)']]), # 5
    ({"person_age": [-3.7, 0.01, 3.07, -19.246, 5.5, 9.4, 11.01]}, [{"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 3}}], [[-3.7, '[-19.247, 0.01)'], [0.01, '[-19.247, 0.01)'], [3.07, '[0.01, 5.5)'], [-19.246, '[-19.247, 0.01)'], [5.5, '[0.01, 5.5)'], [9.4, '[5.5, 11.01)'], [11.01, '[5.5, 11.01)']]), # 6
    ({"person_age": [18, 19, 25, 20, 99, 15, 25, 23]}, [{"column": "person_age", "type": "numerical", "bins": [{"name": "good", "ranges": [[10, 20], [25, 50]]}, {"name": "poor", "ranges": [[80, 100], [110, 120]]}]}], [[18.0, 'good'], [19.0, 'good'], [25.0, 'good'], [20.0, None], [99.0, 'poor'], [15.0, 'good'], [25.0, 'good'], [23.0, None]]), # 7
    ({"loan_grade": ["A", "B", "B", "C", "A", "E", "C", "D", "B"]}, [{"column": "loan_grade", "type": "categorical", "bins": "none"}], [['A', 'A'], ['B', 'B'], ['B', 'B'], ['C', 'C'], ['A', 'A'], ['E', 'E'], ['C', 'C'], ['D', 'D'], ['B', 'B']]), # 8
    ({"loan_grade": ["A", "B", "B", "C", "A", "E", "C", "D", "B"]}, [{"column": "loan_grade", "type": "categorical", "bins": {"algo": "equal width", "method": "width", "value": 5.2}}], -1), # 9
    ({"loan_grade": ["A", "B", "B", "C", "A", "E", "C", "D", "B"]}, [{"column": "loan_grade", "type": "categorical", "bins": {"algo": "equal width", "method": "num_bins", "value": 5.2}}], -1), # 10
    ({"loan_grade": ["A", "B", "B", "C", "A", "E", "C", "D", "B"]}, [{"column": "loan_grade", "type": "categorical", "bins": {"algo": "equal frequency", "method": "freq", "value": 5.2}}], -1), # 11
    ({"loan_grade": ["A", "B", "B", "C", "A", "E", "C", "D", "B"]}, [{"column": "loan_grade", "type": "categorical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 5.2}}], -1), # 12
    ({"loan_grade": ["A", "B", "B", "C", "A", "E", "C", "D", "B"]}, [{"column": "loan_grade", "type": "categorical", "bins": [{"name": "good", "elements": ["A", "B"]}, {"name": "poor", "elements": ["D", "E", "F"]}, {"name": "normal", "elements": ["C"]}]}], [['A', 'good'], ['B', 'good'], ['B', 'good'], ['C', 'normal'], ['A', 'good'], ['E', 'poor'], ['C', 'normal'], ['D', 'poor'], ['B', 'good']]), # 13
    ({"loan_grade": ["A", "B", "B", "C", "A", "E", "C", "D", "B"], "person_age": [1, 3, 10, 25, 95, 39, 48, 1, 2]}, [{"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 5.2}}, {"column": "loan_grade", "type": "categorical", "bins": {"algo": "equal width", "method": "width", "value": 5.2}}], -1), # 14
    ({"person_age": [1, 3, 10, 25, 95, 39, 48, 1, 2], "loan_grade": ["A", "B", "B", "C", "A", "E", "C", "D", "B"], "person_income": [1000, 2000, 25000, 30000, 10000, 10300, 30000, 50000, 20000], "loan_amnt": [1000, 2000, 1500, 2500, 3500, 30000, 10000, 15000, 2500], "home_ownership": ["OWN", "OWN", "MORTGAGE", "RENT", "RENT", "RENT", "RENT", "OTHERS", "MORTGAGE"]}, [{"column": "person_age", "type": "numerical", "bins": [{"name": "good", "ranges": [[10, 20], [25, 50]]}]}, {"column": "loan_amnt", "type": "numerical", "bins": "none"}, {"column": "home_ownership", "type": "categorical", "bins": "none"}, {"column": "loan_grade", "type": "categorical", "bins": [{"name": "good", "elements": ["A", "B"]}, {"name": "poor", "elements": ["D", "E", "F"]}, {"name": "normal", "elements": ["C"]}]}], [[1, 'A', 1000, 1000, 'OWN', None, 'good', 1000, 'OWN'], [3, 'B', 2000, 2000, 'OWN', None, 'good', 2000, 'OWN'], [10, 'B', 25000, 1500, 'MORTGAGE', 'good', 'good', 1500, 'MORTGAGE'], [25, 'C', 30000, 2500, 'RENT', 'good', 'normal', 2500, 'RENT'], [95, 'A', 10000, 3500, 'RENT', None, 'good', 3500, 'RENT'], [39, 'E', 10300, 30000, 'RENT', 'good', 'poor', 30000, 'RENT'], [48, 'C', 30000, 10000, 'RENT', 'good', 'normal', 10000, 'RENT'], [1, 'D', 50000, 15000, 'OTHERS', None, 'poor', 15000, 'OTHERS'], [2, 'B', 20000, 2500, 'MORTGAGE', None, 'good', 2500, 'MORTGAGE']]), # 15
]

@pytest.mark.parametrize("input,bins_settings_list,expected", df_binning_test_data)
def test_perform_binning_on_whole_df(input, bins_settings_list, expected):
    dframe = pd.DataFrame(input)
    result = BinningMachine.perform_binning_on_whole_df(dframe, bins_settings_list)
    
    if expected != -1:
        result = result.values.tolist()
    
    print("Result: ")
    print(result)
    print("Expected: ")
    print(expected)
    
    assert result == expected
