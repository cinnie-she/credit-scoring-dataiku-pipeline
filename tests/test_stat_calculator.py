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
    
