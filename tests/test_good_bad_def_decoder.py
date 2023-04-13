from good_bad_def_decoder import GoodBadDefDecoder
import pytest
"""
TEST GoodBadDefDecoder class
"""

"""
Test Scenario 1
Merge overlapping numerical ranges

Test translation from ((column_name, lower_bound, upper_bound), (column_name2, lower_bound2, upper_bound2), ...)
to [
    {
        "column": column_name,
        "ranges": [[lower, upper]],
    },
    {
        "column": column_name2,
        "ranges": [[lower2, upper2], [lower3, upper3]],
    }
], which, there should not be any overlapping between range among the same column.

------------------------
Test Cases Design
------------------------
(0) Single column + no same column definition
(1) Single column + All possible combinations of 2 ranges [r0, r1] & [b0, b1] with both +ve integer
(2) Single column + All possible combinations of 2 ranges [r0, r1] & [b0, b1] with both -ve integer
(3) Empty tuple
(4) 2 columns
(5) Single column + 2 ranges with lower bound == -ve & upper bound == +ve integer
(6) Single column + 2 ranges with +ve float bounds
(7) Single column + 2 ranges with -ve float bounds
(8) Single column + 2 ranges with lower bound == -ve & upper bound == +ve float
(9) More than 1 type of range overlapping
(10) All possible combinations of a range overlapping with 2 definition ranges
"""

numeric_test_data = [
    ((("paid_past_due", 70, 80),), [{"column": "paid_past_due", "ranges": [[70, 80]]}]), # 0
    ((("paid_past_due", 80, 100), ("paid_past_due", 80, 90)), [{"column": "paid_past_due", "ranges": [[80, 100]]}]), # 1
    ((("paid_past_due", 80, 100), ("paid_past_due", 90, 100)), [{"column": "paid_past_due", "ranges": [[80, 100]]}]), # 2
    ((("paid_past_due", 80, 90), ("paid_past_due", 80, 100)), [{"column": "paid_past_due", "ranges": [[80, 100]]}]), # 3
    ((("paid_past_due", 90, 100), ("paid_past_due", 80, 100)), [{"column": "paid_past_due", "ranges": [[80, 100]]}]), # 4
    ((("paid_past_due", 50, 90), ("paid_past_due", 30, 50)), [{"column": "paid_past_due", "ranges": [[30, 90]]}]), # 5
    ((("paid_past_due", 30, 50), ("paid_past_due", 50, 90)), [{"column": "paid_past_due", "ranges": [[30, 90]]}]), # 6
    ((("paid_past_due", 30, 50), ("paid_past_due", 20, 60)), [{"column": "paid_past_due", "ranges": [[20, 60]]}]), # 7
    ((("paid_past_due", 20, 60), ("paid_past_due", 30, 50)), [{"column": "paid_past_due", "ranges": [[20, 60]]}]), # 8
    ((("paid_past_due", 30, 50), ("paid_past_due", 20, 40)), [{"column": "paid_past_due", "ranges": [[20, 50]]}]), # 9
    ((("paid_past_due", 20, 40), ("paid_past_due", 30, 50)), [{"column": "paid_past_due", "ranges": [[20, 50]]}]), # 10
    ((("paid_past_due", 20, 50), ("paid_past_due", 70, 90)), [{"column": "paid_past_due", "ranges": [[20, 50], [70, 90]]}]), # 11
    
    ((), []), # 12
    ((("paid_past_due", 20, 50), ("person_age", 70, 90)), [{"column": "paid_past_due", "ranges": [[20, 50]]}, {"column": "person_age", "ranges": [[70, 90]]}]), # 13
    ((("paid_past_due", -9, 0), ("paid_past_due", -5, 5)), [{"column": "paid_past_due", "ranges": [[-9, 5]]}]), # 14
    ((("paid_past_due", 30.1, 50.9), ("paid_past_due", 20.7, 40.8)), [{"column": "paid_past_due", "ranges": [[20.7, 50.9]]}]), # 15
    ((("paid_past_due", -8.24, -0.923), ("paid_past_due", -1.73, -0.9)), [{"column": "paid_past_due", "ranges": [[-8.24, -0.9]]}]), # 16
    ((("paid_past_due", -8.24, -0.923), ("paid_past_due", -1.73, 0.9)), [{"column": "paid_past_due", "ranges": [[-8.24, 0.9]]}]), # 17
    
    ((("paid_past_due", -8, -1), ("paid_past_due", -8, -2)), [{"column": "paid_past_due", "ranges": [[-8, -1]]}]), # 18
    ((("paid_past_due", -10, -1), ("paid_past_due", -8, -1)), [{"column": "paid_past_due", "ranges": [[-10, -1]]}]), # 19
    ((("paid_past_due", -8, -2), ("paid_past_due", -8, -1)), [{"column": "paid_past_due", "ranges": [[-8, -1]]}]), # 20
    ((("paid_past_due", -8, -1), ("paid_past_due", -10, -1)), [{"column": "paid_past_due", "ranges": [[-10, -1]]}]), # 21
    ((("paid_past_due", -5, -1), ("paid_past_due", -8, -5)), [{"column": "paid_past_due", "ranges": [[-8, -1]]}]), # 22
    ((("paid_past_due", -8, -5), ("paid_past_due", -5, -1)), [{"column": "paid_past_due", "ranges": [[-8, -1]]}]), # 23
    ((("paid_past_due", -5, -3), ("paid_past_due", -8, -1)), [{"column": "paid_past_due", "ranges": [[-8, -1]]}]), # 24
    ((("paid_past_due", -8, -1), ("paid_past_due", -5, -3)), [{"column": "paid_past_due", "ranges": [[-8, -1]]}]), # 25
    ((("paid_past_due", -5, -1), ("paid_past_due", -8, -3)), [{"column": "paid_past_due", "ranges": [[-8, -1]]}]), # 26
    ((("paid_past_due", -8, -3), ("paid_past_due", -5, -1)), [{"column": "paid_past_due", "ranges": [[-8, -1]]}]), # 27
    ((("paid_past_due", -3, -1), ("paid_past_due", -8, -5)), [{"column": "paid_past_due", "ranges": [[-8, -5], [-3, -1]]}]), # 28
    ((("paid_past_due", 10, 20), ("paid_past_due", 15, 25), ("paid_past_due", 7, 11), ("paid_past_due", 1, 30), ("paid_past_due", -1, 2), ("paid_past_due", 80, 90)), [{"column": "paid_past_due", "ranges": [[-1, 30], [80, 90]]}]), # 29
    ((("paid_past_due", -8, -3), ("paid_past_due", -8, -3)), [{"column": "paid_past_due", "ranges": [[-8, -3]]}]), # 30
    ((("paid_past_due", 1, 3), ("paid_past_due", 5, 7)), [{"column": "paid_past_due", "ranges": [[1, 3], [5, 7]]}]), # 31
    
    ((("paid_past_due", 1, 3), ("paid_past_due", 5, 7), ("paid_past_due", 2, 6)), [{"column": "paid_past_due", "ranges": [[1, 7]]}]), # 32
    ((("paid_past_due", 1, 3), ("paid_past_due", 5, 7), ("paid_past_due", 3, 7)), [{"column": "paid_past_due", "ranges": [[1, 7]]}]), # 33
    ((("paid_past_due", 1, 3), ("paid_past_due", 5, 7), ("paid_past_due", 3, 8)), [{"column": "paid_past_due", "ranges": [[1, 8]]}]), # 34
    ((("paid_past_due", 1, 3), ("paid_past_due", 5, 7), ("paid_past_due", 2, 8)), [{"column": "paid_past_due", "ranges": [[1, 8]]}]), # 35
    ((("paid_past_due", 1, 3), ("paid_past_due", 5, 7), ("paid_past_due", -1, 8)), [{"column": "paid_past_due", "ranges": [[-1, 8]]}]), # 36
    ((("paid_past_due", 1, 3), ("paid_past_due", 5, 7), ("paid_past_due", 1, 8)), [{"column": "paid_past_due", "ranges": [[1, 8]]}]), # 37
    ((("paid_past_due", 1, 3), ("paid_past_due", 5, 7), ("paid_past_due", 0, 7)), [{"column": "paid_past_due", "ranges": [[0, 7]]}]), # 38
    ((("paid_past_due", 1, 3), ("paid_past_due", 5, 7), ("paid_past_due", 0, 6)), [{"column": "paid_past_due", "ranges": [[0, 7]]}]), # 39
    ((("paid_past_due", 1, 3), ("paid_past_due", 5, 7), ("paid_past_due", 0, 5)), [{"column": "paid_past_due", "ranges": [[0, 7]]}]), # 40
]

@pytest.mark.parametrize("numeric_info_list,expected", numeric_test_data)
def test_get_numeric_def_list_from_section(numeric_info_list, expected):
    decoded_numeric_list = GoodBadDefDecoder.get_numeric_def_list_from_section(numeric_info_list)
    print(decoded_numeric_list)
    assert decoded_numeric_list == expected
    
    

"""
Test Scenario 2
Merge overlapping categorical elements

Test translation from ((column_name, element_list), (column_name2, element_list2), ...)
to [
    {
        "column": "loan_status",
        "elements": ["1"]
    },
    {
        "column": "person_home_ownership",
        "elements": ["rent", "mortgage"]
    }
], which, there should not be any overlapping within the element list among the same column.

------------------------
Test Cases Design
------------------------
(1) Single column (with no 2 definitions for 1 single column)
(2) 2 columns (with no 2 definitions for 1 single column)
(3) Empty tuple
(4) Single column (with > 1 definitions for 1 single column, but with no element overlapping)
(5) Single column (with > 1 definitions for 1 single column, but with element(s) overlapping)
(6) Single column (with numerical element + with > 1 definitions for 1 single column, but with element(s) overlapping)
"""


categoric_test_data = [
    ((("person_home_ownership", ["OWN", "OTHERS"]),), [{"column": "person_home_ownership", "elements": ["OWN", "OTHERS"]}]), # 1
    ((("person_home_ownership", ["OWN", "OTHERS"]), ("loan_status", ["1"])), [{"column": "person_home_ownership", "elements": ["OWN", "OTHERS"]}, {"column": "loan_status", "elements": ["1"]}]), # 2
    ((), []), # 3
    ((("person_home_ownership", ["OWN"]), ("person_home_ownership", ["OTHERS"])), [{"column": "person_home_ownership", "elements": ["OWN", "OTHERS"]}]), # 4
    ((("person_home_ownership", ["OWN", "OTHERS"]), ("person_home_ownership", ["OTHERS", "MORTGAGE"])), [{"column": "person_home_ownership", "elements": ["OWN", "OTHERS", "MORTGAGE"]}]), # 5
    ((("loan_status", [1]), ("loan_status", [1, 0])), [{"column": "loan_status", "elements": [1, 0]}]) # 6
]

@pytest.mark.parametrize("categoric_info_list,expected", categoric_test_data)
def test_get_categorical_def_list_from_section(categoric_info_list, expected):
    decoded_categoric_list = GoodBadDefDecoder.get_categorical_def_list_from_section(categoric_info_list)
    print(decoded_categoric_list)
    assert decoded_categoric_list == expected
  

"""
Test Scenario 3
Sort numerical definition ranges in ascending order

Test sort in ascending order e.g., [[20, 30], [10, 15], [3, 5], [60, 80]] to [[3, 5], [10, 15], [20, 30], [60, 80]].

------------------------
Test Cases Design
------------------------
(1) Empty list
(2) Only single range in the list
(3) Typical case
"""  

sort_numerical_def_ranges_test_data = [
    ([], []), # 1
    ([[10, 20]], [[10, 20]]), # 2
    ([[20, 30], [10, 15], [3, 5], [60, 80]], [[3, 5], [10, 15], [20, 30], [60, 80]]), # 3
]
    
@pytest.mark.parametrize("numeric_def_r,expected", sort_numerical_def_ranges_test_data)
def test_sort_numerical_def_ranges(numeric_def_r, expected):
    result = GoodBadDefDecoder.sort_numerical_def_ranges(numeric_def_r)
    assert result == expected