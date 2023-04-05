from good_bad_counter import GoodBadCounter
import pandas as pd
import pytest

"""
TEST GoodBadCounter class
"""

"""
Test Scenario 1
Test given a dataframe and a dictionary telling the bad definitions, count the number of bad samples.

Assumptions:
(1) Columns appearing in definitions must also appears in the dataframe.
(2) Categorical column must not appears in numerical definitions.

Input in the form of:
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

bad_defs = {
    "numerical": [
        {
            "column": "person_age",
            "ranges": [[18, 22]],  # 22 is exclusive
        },
        {
            "column": "paid_past_due",
            "ranges": [[90, 121], [70, 80]],  # 121 is exclusive
        }
    ],
    "categorical": [
        {
            "column": "loan_status",
            "elements": [1]
        },
        {
            "column": "person_home_ownership",
            "elements": ["rent", "mortgage"]
        }
    ],
    "weight": 1.00
}
Output: 
(1) A pd.DataFrame which have removed all bad rows from the input dataset
(2) A natural number representing the sample count of bad in the dataframe

------------------------
Test Cases Design
------------------------
(1) Empty dataframe + Empty definitions
(2) Dataframe with 1 numerical column + Numerical definition with 1 range (have data within the range)
(3) Dataframe with 1 numerical column + Numerical definition with 1 range (no data within the range)
(4) Dataframe with 1 numerical column + Numerical definition with 2 ranges (have data within both of the ranges)
(5) Dataframe with 1 numerical column + Numerical definition with 2 ranges (no data within any ranges)
(6) Dataframe with 1 numerical column + Numerical definition with 2 ranges (have data in 1 range, while another range does not)
(7) Dataframe with 1 numerical column + Categorical definition with 1 element (with no data having that value)
(8) Dataframe with 1 numerical column + Categorical definition with 1 element (with data having that value)
(9) Dataframe with 1 numerical column + Categorical definition with 2 elements (have data taking the 2 values)
(10) Dataframe with 1 numerical column + Categorical definition with 2 elements (no data taking any of the 2 values)
(11) Dataframe with 1 numerical column + Categorical definition with 2 elements (have data taking 1 value, but no data taking another)
(12) Dataframe with 1 numerical column + Empty definitions
(13) Dataframe with 1 categorical column + Empty definitions
(14) Dataframe with 1 categorical column + Categorical definition with 1 element (with no data having that value)
(15) Dataframe with 1 categorical column + Categorical definition with 1 element (with data having that value)
(16) Dataframe with 1 categorical column + Categorical definition with 2 elements (have data taking the 2 values)
(17) Dataframe with 1 categorical column + Categorical definition with 2 elements (no data taking any of the 2 values)
(18) Dataframe with 1 categorical column + Categorical definition with 2 elements (have data taking 1 value, but no data taking another)
(19) Dataframe with 1 numerical & 1 categorical column + Numerical definition
(20) Dataframe with 1 numerical & 1 categorical column + Categorical definition
(21) Dataframe with 1 numerical & 1 categorical column + Numerical & Categorical definitions
(22) Kaggle dataframe + paid_past_due (numerical) + loan_status (categorical)
"""

bad_defs_test_data = [
    ("tests\\test_input_datasets\\empty_dataset.xlsx", {"numerical": [], "categorical": [], "weight": 1}, (0, 0)), # 1
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [{"column": "person_age", "ranges": [[20, 30]]}], "categorical": [], "weight": 1}, (9073, 23508)), # 2
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [{"column": "person_age", "ranges": [[0, 20]]}], "categorical": [], "weight": 1}, (32581, 0)), # 3
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [{"column": "person_age", "ranges": [[20, 30], [50, 60]]}], "categorical": [], "weight": 1}, (8818, 23763)), # 4
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [{"column": "person_age", "ranges": [[-8, 8], [-82, -12]]}], "categorical": [], "weight": 1}, (32581, 0)), # 5
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [{"column": "person_age", "ranges": [[0, 20], [32, 33]]}], "categorical": [], "weight": 1}, (31617, 964)), # 6
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_age", "elements": [18]}], "weight": 1}, (32581, 0)), # 7
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_age", "elements": [20]}], "weight": 1}, (32566, 15)), # 8
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_age", "elements": [20, 32]}], "weight": 1}, (31602, 979)), # 9
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_age", "elements": [-7, 18]}], "weight": 1}, (32581, 0)), # 10
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_age", "elements": [-7, 20]}], "weight": 1}, (32566, 15)), # 11
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [], "categorical": [], "weight": 1}, (32581, 0)), # 12
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"numerical": [], "categorical": [], "weight": 1}, (32581, 0)), # 13
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["Rent"]}], "weight": 1}, (32581, 0)), # 14
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT"]}], "weight": 1}, (16135, 16446)), # 15
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "MORTGAGE"]}], "weight": 1}, (2691, 29890)), # 16
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["Rent", "Mortgage"]}], "weight": 1}, (32581, 0)), # 17
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "Mortgage"]}], "weight": 1}, (16135, 16446)), # 18
    ("tests\\test_input_datasets\\single_numeric_categoric_col_dataset.xlsx", {"numerical": [{"column": "person_age", "ranges": [[20, 30], [50, 60]]}], "categorical": [], "weight": 1}, (8818, 23763)), # 19
    ("tests\\test_input_datasets\\single_numeric_categoric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "MORTGAGE"]}], "weight": 1}, (2691, 29890)), # 20
    ("tests\\test_input_datasets\\single_numeric_categoric_col_dataset.xlsx", {"numerical": [{"column": "person_age", "ranges": [[20, 30], [50, 60]]}], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "MORTGAGE"]}], "weight": 1}, (720, 31861)), # 21
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, (25473, 7108)), # 22
]

@pytest.mark.parametrize("path,bad_defs,expected", bad_defs_test_data)
def test_count_sample_bad(path, bad_defs, expected):
    dframe = pd.read_excel(path)
    result_df, result_bad_count = GoodBadCounter.count_sample_bad(dframe, bad_defs)
    expected_df_len, expected_bad_count = expected
    print(result_df)
    print(f'length = {len(result_df)}    vs    expected length = {expected_df_len}')
    print(f'bad count = {result_bad_count}    vs    expected bad count = {expected_bad_count}')
    assert (len(result_df) == expected_df_len and result_bad_count == expected_bad_count)


"""
Test Scenario 2
Test given a dataframe and a dictionary telling the indeterminate definitions, count the number of indeterminate samples.

Assumptions:
(1) Columns appearing in definitions must also appears in the dataframe.
(2) Categorical column must not appears in numerical definitions.

Input in the form of:
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

indeteraminte_defs = {
    "numerical": [
        {
            "column": "person_age",
            "ranges": [[18, 22]],  # 22 is exclusive
        },
        {
            "column": "paid_past_due",
            "ranges": [[90, 121], [70, 80]],  # 121 is exclusive
        }
    ],
    "categorical": [
        {
            "column": "loan_status",
            "elements": [1]
        },
        {
            "column": "person_home_ownership",
            "elements": ["rent", "mortgage"]
        }
    ],
    "weight": 1.00
}
Output: A natural number representing the sample count of bad in the dataframe

------------------------
Test Cases Design
------------------------
Exactly same as that for bad definition (i.e., Test Scenario 1)
"""

indeterminate_defs_test_data = [
    ("tests\\test_input_datasets\\empty_dataset.xlsx", {"numerical": [], "categorical": [], "weight": 1}, (0)), # 1
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [{"column": "person_age", "ranges": [[20, 30]]}], "categorical": [], "weight": 1}, 23508), # 2
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [{"column": "person_age", "ranges": [[0, 20]]}], "categorical": [], "weight": 1}, 0), # 3
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [{"column": "person_age", "ranges": [[20, 30], [50, 60]]}], "categorical": [], "weight": 1}, 23763), # 4
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [{"column": "person_age", "ranges": [[-8, 8], [-82, -12]]}], "categorical": [], "weight": 1}, 0), # 5
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [{"column": "person_age", "ranges": [[0, 20], [32, 33]]}], "categorical": [], "weight": 1}, 964), # 6
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_age", "elements": [18]}], "weight": 1}, 0), # 7
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_age", "elements": [20]}], "weight": 1}, 15), # 8
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_age", "elements": [20, 32]}], "weight": 1}, 979), # 9
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_age", "elements": [-7, 18]}], "weight": 1}, 0), # 10
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_age", "elements": [-7, 20]}], "weight": 1}, 15), # 11
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"numerical": [], "categorical": [], "weight": 1}, 0), # 12
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"numerical": [], "categorical": [], "weight": 1}, 0), # 13
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["Rent"]}], "weight": 1}, 0), # 14
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT"]}], "weight": 1}, 16446), # 15
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "MORTGAGE"]}], "weight": 1}, 29890), # 16
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["Rent", "Mortgage"]}], "weight": 1}, 0), # 17
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "Mortgage"]}], "weight": 1}, 16446), # 18
    ("tests\\test_input_datasets\\single_numeric_categoric_col_dataset.xlsx", {"numerical": [{"column": "person_age", "ranges": [[20, 30], [50, 60]]}], "categorical": [], "weight": 1}, 23763), # 19
    ("tests\\test_input_datasets\\single_numeric_categoric_col_dataset.xlsx", {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "MORTGAGE"]}], "weight": 1}, 29890), # 20
    ("tests\\test_input_datasets\\single_numeric_categoric_col_dataset.xlsx", {"numerical": [{"column": "person_age", "ranges": [[20, 30], [50, 60]]}], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "MORTGAGE"]}], "weight": 1}, 31861), # 21
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, 7108), # 22
]

@pytest.mark.parametrize("path,indeterminate_defs,expected", indeterminate_defs_test_data)
def test_count_sample_indeterminate(path, indeterminate_defs, expected):
    dframe = pd.read_excel(path)
    result_indeterminate_count = GoodBadCounter.count_sample_indeterminate(dframe, indeterminate_defs)
    print(f'indeterminate count = {result_indeterminate_count}    vs    expected indeterminate count = {expected}')
    assert result_indeterminate_count == expected

"""
Test Scenario 3
Test given a dataframe, the count of sample bad, and the count of sample indeterminate, returns the number of good samples.

Assumptions:
(1) sample_bad_count must be a natural number (i.e., An integer >= 0)
(2) sample_indeterminate_count must be a natural number (i.e., An integer >= 0)

Input in the form of:
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

sample_bad_count = int
sample_indeterminate_count = int

Output: int representing the count of sample good

------------------------
Test Cases Design
------------------------
(1) Empty dataframe + sample_bad_count == sample_indetermainte_count == 0
(2) Dataframe with 1 row + sample_bad_count == 0 + sample_indeterminate_count = 0
(3) Kaggle dataset + sample_bad_count == +ve int + sample_indeterminate_count = 0
(4) Kaggle dataset + sample_bad_count == +ve int + sample_indeterminate_count = +ve int [normal case]
(5) Kaggle dataset + sample_bad_count == len(df)-2 + sample_indeterminate_count = 1
(6) Kaggle dataset + sample_bad_count == len(df)-1 + sample_indeterminate_count = 1
(7) Kaggle dataset + sample_bad_count == len(df) + sample_indeterminate_count = 0
(8) Kaggle dataset + sample_bad_count == 1 + sample_indeterminate_count = len(df)-2
(9) Kaggle dataset + sample_bad_count == 1 + sample_indeterminate_count = len(df)-1
(10) Kaggle dataset + sample_bad_count == 1 + sample_indeterminate_count = len(df)
"""

sample_counts_test_data = [
    ("tests\\test_input_datasets\\empty_dataset.xlsx", 0, 0, 0), # 1
    ("tests\\test_input_datasets\\single_row_dataset.xlsx", 0, 0, 1), # 2
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", 979, 0, 31602), # 3
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", 979, 602, 31000), # 4
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", 32579, 1, 1), # 5
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", 32580, 1, 0), # 6
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", 32581, 0, 0), # 7
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", 1, 32579, 1), # 8
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", 1, 32580, 0), # 9
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", 0, 32581, 0), # 10
]

@pytest.mark.parametrize("path,sample_bad_count,sample_indeterminate_count,expected", sample_counts_test_data)
def test_count_sample_good(path, sample_bad_count, sample_indeterminate_count, expected):
    dframe = pd.read_excel(path)
    result_good_count = GoodBadCounter.count_sample_good(dframe, sample_bad_count, sample_indeterminate_count)
    assert result_good_count == expected

"""
Test Scenario 4
Test given the count of sample good, and weight for good, returns the population good count.

Assumptions:
(1) sample_good_count must be a natural number (i.e., An integer >= 0)
(2) good_weight must be a non-negative number (i.e., An integer or float >= 0)

Input in the form of:
sample_good_count = int
good_weight = non-negative number

Output: non-negative number representing the population good count

------------------------
Test Cases Design
------------------------
(1) sample_good_count = 0 and good_weight = 0
(2) sample_good_count = 979 and good_weight = 0
(3) sample_good_count = 1000 and = < good_weight < 1
(4) sample_good_count = 1000 and good_weight is int > 1 
(5) sample_good_count = 1000 and good_weight is float > 1 
(6) population_good_count is a float
"""

population_good_test_data = [
    (0, 0, 0), # 1
    (979, 0, 0), # 2
    (1000, 0.79, 790), # 3
    (1000, 3, 3000), # 4
    (1000, 1.46, 1460), # 5
    (30, 3.6879, 110.637) # 6
]

@pytest.mark.parametrize("sample_good_count,good_weight,expected", population_good_test_data)
def test_get_population_good(sample_good_count, good_weight, expected):
    result_pop_good_count = GoodBadCounter.get_population_good(sample_good_count, good_weight)
    assert result_pop_good_count == expected


"""
Test Scenario 5
Test given the count of sample bad, and weight for bad, returns the population bad count.

Assumptions:
(1) sample_bad_count must be a natural number (i.e., An integer >= 0)
(2) bad_weight must be a non-negative number (i.e., An integer or float >= 0)

Input in the form of:
sample_bad_count = int
bad_weight = non-negative number

Output: non-negative number representing the population bad count

------------------------
Test Cases Design
------------------------
(1) sample_bad_count = 0 and bad_weight = 0
(2) sample_bad_count = 979 and bad_weight = 0
(3) sample_bad_count = 1000 and = < bad_weight < 1
(4) sample_bad_count = 1000 and bad_weight is int > 1 
(5) sample_bad_count = 1000 and bad_weight is float > 1 
(6) population_bad_count is a float
"""

population_bad_test_data = [
    (0, 0, 0), # 1
    (979, 0, 0), # 2
    (1000, 0.79, 790), # 3
    (1000, 3, 3000), # 4
    (1000, 1.46, 1460), # 5
    (30, 3.6879, 110.637) # 6
]

@pytest.mark.parametrize("sample_bad_count,bad_weight,expected", population_bad_test_data)
def test_get_population_bad(sample_bad_count, bad_weight, expected):
    result_pop_bad_count = GoodBadCounter.get_population_bad(sample_bad_count, bad_weight)
    assert result_pop_bad_count == expected



"""
Test Scenario 6
Test given a dataframe, the count of sample bad, and the count of sample indeterminate, returns the number of good samples.

Assumptions:
(1) Columns appearing in definitions must also appears in the dataframe.
(2) Categorical column must not appears in numerical definitions.
(3) good_weight/bad_weight must be a non-negative number (i.e., An integer or float >= 0)

Input in the form of:
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

good_bad_def = dict
{
    "bad": {
        "numerical": [
            {
                "column": "person_age",
                "ranges": [[18, 22]],  # 22 is exclusive
            },
            {
                "column": "paid_past_due",
                "ranges": [[90, 121], [70, 80]],  # 121 is exclusive
            }
        ],
        "categorical": [
            {
                "column": "loan_status",
                "elements": ["1"]
            },
            {
                "column": "person_home_ownership",
                "elements": ["rent", "mortgage"]
            }
        ],
        "weight": 1.00
    },
    "indeterminate": {
        "numerical": [
            {
                "column": "person_age",
                "ranges": [[25, 30]],  # 30 is exclusive
            },
            {
                "column": "paid_past_due",
                "ranges": [[60, 90]],  # 90 is exclusive
            }
        ],
        "categorical": [
            {
                "column": "loan_grade",
                "elements": ["C", "D", "E"],
            }
        ],
    },
    "good": {
        "weight": 1.49
    }
}

Output: 
(1) sample_bad_count : a natural number (int >= 0)
(2) sample_indeterminate_count : a natural number (int >= 0)
(3) sample_good_count : a natural number (int >= 0)
(4) good_weight : a non-negative number (int or float >= 0)
(5) bad_weight : a non-negative number (int or float >= 0)
(6) population_good_count : a non-negative number (int or float >= 0)
(7) population_bad_count : a non-negative number (int or float >= 0)

------------------------
Test Cases Design
------------------------
Please check: https://docs.google.com/spreadsheets/d/1ueiTi9b9sklCMl7qN1T0Ih38KnSBJ04B/edit?usp=sharing&ouid=104644026075892761599&rtpof=true&sd=true
for details.

"""

stat_test_data = [
    ("tests\\test_input_datasets\\empty_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, (0,0,0,1,1,0,0)), # 1
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[20, 30]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, (23508,0,9073,1,1,9073,23508)), # 2
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[20, 30]]}], "categorical": [], "weight": 2}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1.49}}, (23508,0,9073,1.49,2,13518.77,47016)), # 3
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[20, 30]]}], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 2}}, (23508,0,9073,2,1.49,18146,35026.92)), # 4
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[0, 20]]}], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 2}}, (0,0,32581,2,1.49,65162,0)), # 5
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[20, 30], [50, 60]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, (23763,0,8818,1,1,8818,23763)), # 6
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[20, 30], [50, 60]]}], "categorical": [], "weight": 2}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1.49}}, (23763,0,8818,1.49,2,13138.82,47526)), # 7
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[20, 30], [50, 60]]}], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 2}}, (23763,0,8818,2,1.49,17636,35406.87)), # 8
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[-8, 8], [-82, -12]]}], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 2}}, (0,0,32581,2,1.49,65162,0)), # 9
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[0, 20], [32, 33]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, (964,0,31617,1,1,31617,964)), # 10
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[0, 20], [32, 33]]}], "categorical": [], "weight": 2}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1.49}}, (964,0,31617,1.49,2,47109.33,1928)), # 11
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[0, 20], [32, 33]]}], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 2}}, (964,0,31617,2,1.49,63234,1436.36)), # 12
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_age", "elements": [20]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, (15,0,32566,1,1,32566,15)), # 13
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_age", "elements": [20]}], "weight": 2}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1.49}}, (15,0,32566,1.49,2,48523.34,30)), # 14
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_age", "elements": [20]}], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 2}}, (15,0,32566,2,1.49,65132,22.35)), # 15
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_age", "elements": [18]}], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 2}}, (0,0,32581,2,1.49,65162,0)), # 16
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_age", "elements": [20, 32]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, (979,0,31602,1,1,31602,979)), # 17
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_age", "elements": [20, 32]}], "weight": 2}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1.49}}, (979,0,31602,1.49,2,47086.98,1958)), # 18
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_age", "elements": [20, 32]}], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 2}}, (979,0,31602,2,1.49,63204,1458.71)), # 19
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_age", "elements": [-7, 18]}], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 2}}, (0,0,32581,2,1.49,65162,0)), # 20
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_age", "elements": [-7, 20]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, (15,0,32566,1,1,32566,15)), # 21
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_age", "elements": [-7, 20]}], "weight": 2}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1.49}}, (15,0,32566,1.49,2,48523.34,30)), # 22
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_age", "elements": [-7, 20]}], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 2}}, (15,0,32566,2,1.49,65132,22.35)), # 23
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, (0,0,32581,1,1,32581,0)), # 24
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, (0,0,32581,1,1,32581,0)), # 25
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT"]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, (16446,0,16135,1,1,16135,16446)), # 26
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT"]}], "weight": 2}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1.49}}, (16446,0,16135,1.49,2,24041.15,32892)), # 27
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT"]}], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 2}}, (16446,0,16135,2,1.49,32270,24504.54)), # 28
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["Rent"]}], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 2}}, (0,0,32581,2,1.49,65162,0)), # 29
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "MORTGAGE"]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, (29890,0,2691,1,1,2691,29890)), # 30
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "MORTGAGE"]}], "weight": 2}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1.49}}, (29890,0,2691,1.49,2,4009.59,59780)), # 31
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "MORTGAGE"]}], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 2}}, (29890,0,2691,2,1.49,5382,44536.1)), # 32
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["Rent", "Mortgage"]}], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 2}}, (0,0,32581,2,1.49,65162,0)), # 33
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "Mortgage"]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, (16446,0,16135,1,1,16135,16446)), # 34
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "Mortgage"]}], "weight": 2}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1.49}}, (16446,0,16135,1.49,2,24041.15,32892)), # 35
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "Mortgage"]}], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 2}}, (16446,0,16135,2,1.49,32270,24504.54)), # 36
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[20, 30]]}], "categorical": []}, "good": {"weight": 1}}, (0,23508,9073,1,1,9073,0)), # 37
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 2}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[20, 30]]}], "categorical": []}, "good": {"weight": 1.49}}, (0,23508,9073,1.49,2,13518.77,0)), # 38
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[20, 30]]}], "categorical": []}, "good": {"weight": 2}}, (0,23508,9073,2,1.49,18146,0)), # 39
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[0, 20]]}], "categorical": []}, "good": {"weight": 2}}, (0,0,32581,2,1.49,65162,0)), # 40
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[20, 30], [50, 60]]}], "categorical": []}, "good": {"weight": 1}}, (0,23763,8818,1,1,8818,0)), # 41
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 2}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[20, 30], [50, 60]]}], "categorical": []}, "good": {"weight": 1.49}}, (0,23763,8818,1.49,2,13138.82,0)), # 42
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[20, 30], [50, 60]]}], "categorical": []}, "good": {"weight": 2}}, (0,23763,8818,2,1.49,17636,0)), # 43
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[-8, 8], [-82, -12]]}], "categorical": []}, "good": {"weight": 2}}, (0,0,32581,2,1.49,65162,0)), # 44
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[0, 20], [32, 33]]}], "categorical": []}, "good": {"weight": 1}}, (0,964,31617,1,1,31617,0)), # 45
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 2}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[0, 20], [32, 33]]}], "categorical": []}, "good": {"weight": 1.49}}, (0,964,31617,1.49,2,47109.33,0)), # 46
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[0, 20], [32, 33]]}], "categorical": []}, "good": {"weight": 2}}, (0,964,31617,2,1.49,63234,0)), # 47
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_age", "elements": [20]}]}, "good": {"weight": 1}}, (0,15,32566,1,1,32566,0)), # 48
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 2}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_age", "elements": [20]}]}, "good": {"weight": 1.49}}, (0,15,32566,1.49,2,48523.34,0)), # 49
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_age", "elements": [20]}]}, "good": {"weight": 2}}, (0,15,32566,2,1.49,65132,0)), # 50
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_age", "elements": [18]}]}, "good": {"weight": 2}}, (0,0,32581,2,1.49,65162,0)), # 51
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_age", "elements": [20, 32]}]}, "good": {"weight": 1}}, (0,979,31602,1,1,31602,0)), # 52
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 2}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_age", "elements": [20, 32]}]}, "good": {"weight": 1.49}}, (0,979,31602,1.49,2,47086.98,0)), # 53
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_age", "elements": [20, 32]}]}, "good": {"weight": 2}}, (0,979,31602,2,1.49,63204,0)), # 54
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_age", "elements": [-7, 18]}]}, "good": {"weight": 2}}, (0,0,32581,2,1.49,65162,0)), # 55
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_age", "elements": [-7, 20]}]}, "good": {"weight": 1}}, (0,15,32566,1,1,32566,0)), # 56
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 2}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_age", "elements": [-7, 20]}]}, "good": {"weight": 1.49}}, (0,15,32566,1.49,2,48523.34,0)), # 57
    ("tests\\test_input_datasets\\single_numeric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_age", "elements": [-7, 20]}]}, "good": {"weight": 2}}, (0,15,32566,2,1.49,65132,0)), # 58
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT"]}]}, "good": {"weight": 1}}, (0,16446,16135,1,1,16135,0)), # 59
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 2}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT"]}]}, "good": {"weight": 1.49}}, (0,16446,16135,1.49,2,24041.15,0)), # 60
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT"]}]}, "good": {"weight": 2}}, (0,16446,16135,2,1.49,32270,0)), # 61
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["Rent"]}]}, "good": {"weight": 2}}, (0,0,32581,2,1.49,65162,0)), # 62
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "MORTGAGE"]}]}, "good": {"weight": 1}}, (0,29890,2691,1,1,2691,0)), # 63
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 2}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "MORTGAGE"]}]}, "good": {"weight": 1.49}}, (0,29890,2691,1.49,2,4009.59,0)), # 64
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "MORTGAGE"]}]}, "good": {"weight": 2}}, (0,29890,2691,2,1.49,5382,0)), # 65
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["Rent", "Mortgage"]}]}, "good": {"weight": 2}}, (0,0,32581,2,1.49,65162,0)), # 66
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "Mortgage"]}]}, "good": {"weight": 1}}, (0,16446,16135,1,1,16135,0)), # 67
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 2}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "Mortgage"]}]}, "good": {"weight": 1.49}}, (0,16446,16135,1.49,2,24041.15,0)), # 68
    ("tests\\test_input_datasets\\single_categoric_col_dataset.xlsx", {"bad": {"numerical": [], "categorical": [], "weight": 1.49}, "indeterminate": {"numerical": [], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "Mortgage"]}]}, "good": {"weight": 2}}, (0,16446,16135,2,1.49,32270,0)), # 69 
    ("tests\\test_input_datasets\\single_numeric_categoric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[20, 25]]}], "categorical": [{"column": "person_home_ownership", "elements": ["RENT"]}], "weight": 1}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[25, 30]]}], "categorical": [{"column": "person_home_ownership", "elements": ["MORTGAGE"]}]}, "good": {"weight": 1}}, (22196,9647,738,1,1,738,22196)), # 70
    ("tests\\test_input_datasets\\single_numeric_categoric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[20, 25]]}], "categorical": [{"column": "person_home_ownership", "elements": ["RENT"]}], "weight": 2}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[25, 30]]}], "categorical": [{"column": "person_home_ownership", "elements": ["MORTGAGE"]}]}, "good": {"weight": 1.49}}, (22196,9647,738,1.49,2,1099.62,44392)), # 71
    ("tests\\test_input_datasets\\single_numeric_categoric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[20, 25]]}], "categorical": [{"column": "person_home_ownership", "elements": ["RENT"]}], "weight": 1.49}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[25, 30]]}], "categorical": [{"column": "person_home_ownership", "elements": ["MORTGAGE"]}]}, "good": {"weight": 2}}, (22196,9647,738,2,1.49,1476,33072.04)), # 72
    ("tests\\test_input_datasets\\single_numeric_categoric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[20, 25], [50, 55]]}], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "OTHER"]}], "weight": 1}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[25, 30], [55, 60]]}], "categorical": [{"column": "person_home_ownership", "elements": ["MORTGAGE"]}]}, "good": {"weight": 1}}, (22324,9556,701,1,1,701,22324)), # 73
    ("tests\\test_input_datasets\\single_numeric_categoric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[20, 25], [50, 55]]}], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "OTHER"]}], "weight": 2}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[25, 30], [55, 60]]}], "categorical": [{"column": "person_home_ownership", "elements": ["MORTGAGE"]}]}, "good": {"weight": 1.49}}, (22324,9556,701,1.49,2,1044.49,44648)), # 74  
    ("tests\\test_input_datasets\\single_numeric_categoric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[20, 25], [50, 55]]}], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "OTHER"]}], "weight": 1.49}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[25, 30], [55, 60]]}], "categorical": [{"column": "person_home_ownership", "elements": ["MORTGAGE"]}]}, "good": {"weight": 2}}, (22324,9556,701,2,1.49,1402,33262.76)), # 75
    ("tests\\test_input_datasets\\single_numeric_categoric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[20, 25], [50, 55]]}], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "OTHER"]}], "weight": 1}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[25, 30], [5, 10]]}], "categorical": [{"column": "person_home_ownership", "elements": ["MORTGAGE"]}]}, "good": {"weight": 1}}, (22324,9553,704,1,1,704,22324)), # 76
    ("tests\\test_input_datasets\\single_numeric_categoric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[20, 25], [50, 55]]}], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "OTHER"]}], "weight": 2}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[25, 30], [5, 10]]}], "categorical": [{"column": "person_home_ownership", "elements": ["MORTGAGE"]}]}, "good": {"weight": 1.49}}, (22324,9553,704,1.49,2,1048.96,44648)), # 77
    ("tests\\test_input_datasets\\single_numeric_categoric_col_dataset.xlsx", {"bad": {"numerical": [{"column": "person_age", "ranges": [[20, 25], [50, 55]]}], "categorical": [{"column": "person_home_ownership", "elements": ["RENT", "OTHER"]}], "weight": 1.49}, "indeterminate": {"numerical": [{"column": "person_age", "ranges": [[25, 30], [5, 10]]}], "categorical": [{"column": "person_home_ownership", "elements": ["MORTGAGE"]}]}, "good": {"weight": 2}}, (22324,9553,704,2,1.49,1408,33262.76)), # 78
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, (7108,8585,16888,1,1,16888,7108)), # 79
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 2}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1.49}}, (7108,8585,16888,1.49,2,25163.12,14216)), # 80
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1.49}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 2}}, (7108,8585,16888,2,1.49,33776,10590.92)), # 81
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 100], [110, 121]]}, {"column": "loan_amnt", "ranges": [[30000, 31000], [33000, 36000]]}], "categorical": [{"column": "loan_grade", "elements": ["E", "F", "G"]}], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 70], [75, 80]]}, {"column": "person_age", "ranges": [[20, 23], [50, 52]]}], "categorical": [{"column": "loan_grade", "elements": ["C", "D"]}]}, "good": {"weight": 1}}, (5775,13147,13659,1,1,13659,5775)), # 82
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 100], [110, 121]]}, {"column": "loan_amnt", "ranges": [[30000, 31000], [33000, 36000]]}], "categorical": [{"column": "loan_grade", "elements": ["E", "F", "G"]}], "weight": 2}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 70], [75, 80]]}, {"column": "person_age", "ranges": [[20, 23], [50, 52]]}], "categorical": [{"column": "loan_grade", "elements": ["C", "D"]}]}, "good": {"weight": 1.49}}, (5775,13147,13659,1.49,2,20351.91,11550)), # 83
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 100], [110, 121]]}, {"column": "loan_amnt", "ranges": [[30000, 31000], [33000, 36000]]}], "categorical": [{"column": "loan_grade", "elements": ["E", "F", "G"]}], "weight": 1.49}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 70], [75, 80]]}, {"column": "person_age", "ranges": [[20, 23], [50, 52]]}], "categorical": [{"column": "loan_grade", "elements": ["C", "D"]}]}, "good": {"weight": 2}}, (5775,13147,13659,2,1.49,27318,8604.75)), # 84
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 100], [110, 121]]}, {"column": "loan_amnt", "ranges": [[30000, 31000], [33000, 36000]]}], "categorical": [{"column": "loan_grade", "elements": ["E", "F", "G"]}], "weight": 0}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 70], [75, 80]]}, {"column": "person_age", "ranges": [[20, 23], [50, 52]]}], "categorical": [{"column": "loan_grade", "elements": ["C", "D"]}]}, "good": {"weight": 0}}, (5775,13147,13659,0,0,0,0)), # 85
]

@pytest.mark.parametrize("path,good_bad_def,expected", stat_test_data)
def test_get_statistics(path, good_bad_def, expected):
    dframe = pd.read_excel(path)
    expected_sample_bad_count, expected_sample_indeterminate_count, expected_sample_good_count, expected_good_weight, expected_bad_weight, expected_population_good_count, expected_population_bad_count = expected
    result_sample_bad_count, result_sample_indeterminate_count, result_sample_good_count, result_good_weight, result_bad_weight, result_population_good_count, result_population_bad_count = GoodBadCounter.get_statistics(dframe, good_bad_def)
    print(f"result_sample_bad_count = {result_sample_bad_count} vs expected_sample_bad_count = {expected_sample_bad_count}")
    print(f"result_sample_indeterminate_count = {result_sample_indeterminate_count} vs expected_sample_indeterminate_count = {expected_sample_indeterminate_count}")
    print(f"result_sample_good_count = {result_sample_good_count} vs expected_sample_good_count = {expected_sample_good_count}")
    print(f"result_good_weight = {result_good_weight} vs expected_good_weight = {expected_good_weight}")
    print(f"result_bad_weight = {result_bad_weight} vs expected_bad_weight = {expected_bad_weight}")
    print(f"result_population_good_count = {result_population_good_count} vs expected_population_good_count = {expected_population_good_count}")
    print(f"result_population_bad_count = {result_population_bad_count} vs expected_population_bad_count = {expected_population_bad_count}")
    assert (
        result_sample_bad_count == expected_sample_bad_count and
        result_sample_indeterminate_count == expected_sample_indeterminate_count and
        result_sample_good_count == expected_sample_good_count and
        result_good_weight == expected_good_weight and
        result_bad_weight == expected_bad_weight and
        result_population_good_count == expected_population_good_count and
        result_population_bad_count == expected_population_bad_count
    )