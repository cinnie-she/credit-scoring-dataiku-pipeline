from stat_calculator import StatCalculator
import pandas as pd
import pytest

"""
TEST StatCalculator class
"""

"""
Test Scenario 1
Compute percentage based on given nominator and denominator.

Test computation of percentage.

------------------------
Test Cases Design
------------------------
(1) value = 0
(2) total_value = 0
(3) value = total_value = 0
(4) value > total_value
(5) value < total_value
(6) value = total_value != 0
"""  

compute_pct_test_data = [
    (0, 100, 0), # 1
    (100, 0, None), # 2
    (0, 0, None), # 3
    (1000, 100, 10), # 4
    (100, 1000, 0.1), # 5
    (100, 100, 1), # 6
]

@pytest.mark.parametrize("value,total_value,expected", compute_pct_test_data)
def test_compute_pct(value, total_value, expected):
    result = StatCalculator.compute_pct(value, total_value)
    assert result == expected


"""
Test Scenario 2
Compute odds based on given good and bad counts.

Test computation of odds.

------------------------
Test Cases Design
------------------------
(1) good = 0
(2) bad = 0
(3) good = bad = 0
(4) good > bad
(5) good < bad
(6) good = bad != 0
"""  

compute_odds_test_data = [
    (0, 100, 0), # 1
    (100, 0, None), # 2
    (0, 0, None), # 3
    (1000, 100, 10), # 4
    (100, 1000, 0.1), # 5
    (100, 100, 1), # 6
]

@pytest.mark.parametrize("good,bad,expected", compute_odds_test_data)
def test_compute_odds(good, bad, expected):
    result = StatCalculator.compute_odds(good, bad)
    assert result == expected


"""
Test Scenario 3
Compute info_odds based on given good% and bad%.

Test computation of info_odds.

------------------------
Test Cases Design
------------------------
(1) good_pct = 0
(2) bad_pct = 0
(3) good_pct = bad_pct = 0
(4) good_pct > bad_pct
(5) good_pct < bad_pct
(6) good_pct = bad_pct != 0
"""  

compute_info_odds_test_data = [
    (0, 100, 0), # 1
    (100, 0, None), # 2
    (0, 0, None), # 3
    (1000, 100, 10), # 4
    (100, 1000, 0.1), # 5
    (100, 100, 1), # 6
]

@pytest.mark.parametrize("good_pct,bad_pct,expected", compute_info_odds_test_data)
def test_compute_info_odds(good_pct, bad_pct, expected):
    result = StatCalculator.compute_info_odds(good_pct, bad_pct)
    assert result == expected


"""
Test Scenario 4
Compute woe based on given info_odds.

Test computation of woe.

------------------------
Test Cases Design
------------------------
(1) info_odds = None
(2) info_odds = -1 (boundary case)
(3) info_odds = 0 (boundary case)
(4) info_odds = 1 (boundary case)
(5) info_odds = 5 (typical case)
"""  

compute_woe_test_data = [
    (None, None), # 1
    (-1, None), # 2
    (0, None), # 3
    (1, 0), # 4
    (5, 1.60943791243), # 5
]

@pytest.mark.parametrize("info_odds,expected", compute_woe_test_data)
def test_compute_woe(info_odds, expected):
    result = StatCalculator.compute_woe(info_odds)
    if expected != None:
        assert (result - expected < 0.0001)
    else:
        assert result == expected


"""
Test Scenario 5
Compute mc based on given good%, bad%, and woe.

Test computation of mc.

------------------------
Test Cases Design
------------------------
(1) woe = None
(2) good_pct - bad_pct = 0
(3) woe = 0
(4) woe = -1
(5) woe = 1
(6) woe = -ve and (good% - bad%) = -ve
(7) woe = -ve and (good% - bad%) = +ve
(8) woe = +ve and (good% - bad%) = -ve
(9) woe = +ve and (good% - bad%) = +ve
"""  

compute_mc_test_data = [
    (0.5, 0.3, None, 0), # 1
    (0.5, 0.5, 52.7, 0), # 2
    (0.5, 0.3, 0, 0), # 3
    (0.5, 0.3, -1, -0.2), # 4
    (0.5, 0.3, 1, 0.2), # 5
    (0.3, 0.6, -50.2, 15.06), # 6
    (0.6, 0.3, -50.2, -15.06), # 7
    (0.3, 0.6, 50.2, -15.06), # 8
    (0.6, 0.3, 50.2, 15.06), # 9
]

@pytest.mark.parametrize("good_pct,bad_pct,woe,expected", compute_mc_test_data)
def test_compute_mc(good_pct, bad_pct, woe, expected):
    result = StatCalculator.compute_mc(good_pct, bad_pct, woe)
    assert (result - expected < 0.0001)
    

"""
Test Scenario 6
Compute summary statistical table based on input dataframe, col_bins_settings, and good bad definitions.

Test computation summary statistical table.

------------------------
Test Cases Design
------------------------
(1) Empty dataframe
(2) Empty col_bins_settings
(3) Empty good_bad_def
(4 - 5) Numerical column + No binning + loan_status (0 = Good, 1 = Bad)
(6 - 7) Categorical column + No binning + loan_status (0 = Good, 1 = Bad)
(8) paid_past_due column + No binning + loan_status (0 = Good, 1 = Bad)
(9) loan_status column + No binning + loan_status (0 = Good, 1 = Bad)

(10 - 11) Numerical column + No binning + paid_past_due ([0, 60) = Good, [60, 90) = Indeterminate, [90, 120) = Bad)
(12 - 13) Categorical column + No binning + paid_past_due ([0, 60) = Good, [60, 90) = Indeterminate, [90, 120) = Bad)
(14) paid_past_due column + No binning + paid_past_due ([0, 60) = Good, [60, 90) = Indeterminate, [90, 120) = Bad)
(15) loan_status column + No binning + paid_past_due ([0, 60) = Good, [60, 90) = Indeterminate, [90, 120) = Bad)

(16 - 17) Numerical column + Equal width (by width) + loan_status (0 = Good, 1 = Bad)
(18) paid_past_due column + Equal width (by width) + loan_status (0 = Good, 1 = Bad)
(19 - 20) Numerical column + Equal width (by width) + paid_past_due ([0, 60) = Good, [60, 90) = Indeterminate, [90, 120) = Bad)
(21) paid_past_due column + Equal width (by width) + paid_past_due ([0, 60) = Good, [60, 90) = Indeterminate, [90, 120) = Bad)

(22 - 23) Numerical column + Equal width (by num_bins) + loan_status (0 = Good, 1 = Bad)
(24) paid_past_due column + Equal width (by num_bins) + loan_status (0 = Good, 1 = Bad)
(25 - 26) Numerical column + Equal width (by num_bins) + paid_past_due ([0, 60) = Good, [60, 90) = Indeterminate, [90, 120) = Bad)
(27) paid_past_due column + Equal width (by num_bins) + paid_past_due ([0, 60) = Good, [60, 90) = Indeterminate, [90, 120) = Bad)

(28 - 29) Numerical column + Equal frequency (by frequency) + loan_status (0 = Good, 1 = Bad)
(30) paid_past_due column + Equal frequency (by frequency) + loan_status (0 = Good, 1 = Bad)
(31 - 32) Numerical column + Equal frequency (by frequency) + paid_past_due ([0, 60) = Good, [60, 90) = Indeterminate, [90, 120) = Bad)
(33) paid_past_due column + Equal frequency (by frequency) + paid_past_due ([0, 60) = Good, [60, 90) = Indeterminate, [90, 120) = Bad)

(34 - 35) Numerical column + Equal frequency (by num_bins) + loan_status (0 = Good, 1 = Bad)
(36) paid_past_due column + Equal frequency (by num_bins) + loan_status (0 = Good, 1 = Bad)
(37 - 38) Numerical column + Equal frequency (by num_bins) + paid_past_due ([0, 60) = Good, [60, 90) = Indeterminate, [90, 120) = Bad)
(39) paid_past_due column + Equal frequency (by num_bins) + paid_past_due ([0, 60) = Good, [60, 90) = Indeterminate, [90, 120) = Bad)
""" 

summary_stat_table_test_data = [
    ("tests\\test_input_datasets\\empty_dataset.xlsx", {"column": "person_age", "type": "numerical", "bins": "none"}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, None), # 1
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", None, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, None), # 2
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_age", "type": "numerical", "bins": "none"}, None, None), # 3
    ("tests\\test_input_datasets\\credit_risk_dataset_generated_sorted_by_age.xlsx", {"column": "person_age", "type": "numerical", "bins": "none"}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc4.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated_sorted_by_income.xlsx", {"column": "person_income", "type": "numerical", "bins": "none"}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc5.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_home_ownership", "type": "numerical", "bins": "none"}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc6.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "loan_intent", "type": "numerical", "bins": "none"}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc7.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "paid_past_due", "type": "numerical", "bins": "none"}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc8.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "loan_status", "type": "numerical", "bins": "none"}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc9.xlsx"),
    
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_age", "type": "numerical", "bins": "none"}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc10.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_income", "type": "numerical", "bins": "none"}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc11.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_home_ownership", "type": "numerical", "bins": "none"}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc12.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "loan_intent", "type": "numerical", "bins": "none"}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc13.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "paid_past_due", "type": "numerical", "bins": "none"}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc14.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "loan_status", "type": "numerical", "bins": "none"}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc15.xlsx"),
    
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 10}}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc16.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_income", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 10000}}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc17.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "paid_past_due", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 10}}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc18.xlsx"),
    
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 10}}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc19.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_income", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 10000}}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc20.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "paid_past_due", "type": "numerical", "bins": {"algo": "equal width", "method": "width", "value": 10}}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc21.xlsx"),
    
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 10}}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc22.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_income", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 10}}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc23.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "paid_past_due", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 10}}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc24.xlsx"),
    
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_age", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 10}}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc25.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_income", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 10}}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc26.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "paid_past_due", "type": "numerical", "bins": {"algo": "equal width", "method": "num_bins", "value": 10}}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc27.xlsx"),
    
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 1000}}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc28.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_income", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 1000}}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc29.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "paid_past_due", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 1000}}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc30.xlsx"),
    
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 1000}}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc31.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_income", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 1000}}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc32.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "paid_past_due", "type": "numerical", "bins": {"algo": "equal frequency", "method": "freq", "value": 1000}}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc33.xlsx"),
    
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 10}}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc34.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_income", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 10}}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc35.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "paid_past_due", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 10}}, {"bad": {"numerical": [], "categorical": [{"column": "loan_status", "elements": [1]}], "weight": 1}, "indeterminate": {"numerical": [], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc36.xlsx"),
    
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_age", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 10}}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc37.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "person_income", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 10}}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc38.xlsx"),
    ("tests\\test_input_datasets\\credit_risk_dataset_generated.xlsx", {"column": "paid_past_due", "type": "numerical", "bins": {"algo": "equal frequency", "method": "num_bins", "value": 10}}, {"bad": {"numerical": [{"column": "paid_past_due", "ranges": [[90, 121]]}], "categorical": [], "weight": 1}, "indeterminate": {"numerical": [{"column": "paid_past_due", "ranges": [[60, 90]]}], "categorical": []}, "good": {"weight": 1}}, "tests\\test_output_datasets\\stat_calculator_ts6_tc39.xlsx"),
]

@pytest.mark.parametrize("input_df_path,col_bins_settings,good_bad_def,expected", summary_stat_table_test_data)
def test_compute_summary_stat_table(input_df_path, col_bins_settings, good_bad_def, expected):
    print(expected)
    dframe = pd.read_excel(input_df_path)
    if expected != None:
        expected = pd.read_excel(expected)
        expected = expected.values.tolist()
    
    stat_calculator = StatCalculator(dframe, col_bins_settings, good_bad_def)
    result = stat_calculator.compute_summary_stat_table()
    if isinstance(result, pd.DataFrame):
        result = result.values.tolist()
    
    is_same = True
    if expected != None:
        for row_idx in range(len(result)):
            for col_idx in range(len(result[row_idx])):
                result_val = result[row_idx][col_idx]
                expected_val = expected[row_idx][col_idx]
                if (isinstance(result_val, int) or isinstance(result_val, float)) and result_val - expected_val > 0.0001:
                    # print(f'row_idx={row_idx}, col_idx={col_idx}, result={result_val}, expected={expected_val}')
                    is_same = False
    else:
        is_same = (result == expected)
    
    assert is_same == True
    
    

 