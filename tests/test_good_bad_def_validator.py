from good_bad_def_validator import GoodBadDefValidator
import pytest

"""
TEST GoodBadDefValidator class
"""

"""
Test Scenario 1
Check if any overlapping definitions between bad & indeterminate numerical definition ranges.

Test check any overlapping between bad & indeterminate definition ranges, which both are in the form of:
[
    {
        "column": column_name,
        "ranges": [[lower, upper]],
    },
    {
        "column": column_name2,
        "ranges": [[lower2, upper2], [lower3, upper3]],
    }
], if have overlapping, expected result is a Boolean False,
else, if no overlapping, expected result is a Boolean True.

------------------------
Test Cases Design
------------------------
(1) Single column + no overlapping
(2) Single column + no overlapping (for [r0, r1] & [b0, b1], r1 == b0)
(3) Single column + no overlapping (for [r0, r1] & [b0, b1], r0 == b1)
(4) Single column + with overlapping (case {[]})
(5) Single column + with overlapping (case [{]})
(6) Single column + with overlapping (case {}])
(7) Single column + with overlapping (case {})
(8) Single column + with overlapping (case {[})
(9) Single column + with overlapping (case [{])
(10) Empty definition list for bad
(11) Empty definition list for indeterminate
(12) Empty definition list for bad & indeterminate
(13) 2 column + overlapping of one of the column
(14) 2 columns + no overlapping
"""

numeric_test_data = [
    ([{"column": "paid_past_due", "ranges": [[90, 121]]}], [{"column": "paid_past_due", "ranges": [[70, 80]]}], True), # 1
    ([{"column": "paid_past_due", "ranges": [[90, 121]]}], [{"column": "paid_past_due", "ranges": [[70, 90]]}], True), # 2
    ([{"column": "paid_past_due", "ranges": [[90, 100]]}], [{"column": "paid_past_due", "ranges": [[100, 121]]}], True), # 3
    ([{"column": "paid_past_due", "ranges": [[90, 121]]}], [{"column": "paid_past_due", "ranges": [[91, 100]]}], False), # 4
    ([{"column": "paid_past_due", "ranges": [[90, 121]]}], [{"column": "paid_past_due", "ranges": [[80, 100]]}], False), # 5
    ([{"column": "paid_past_due", "ranges": [[90, 121]]}], [{"column": "paid_past_due", "ranges": [[90, 125]]}], False), # 6
    ([{"column": "paid_past_due", "ranges": [[90, 100]]}], [{"column": "paid_past_due", "ranges": [[90, 100]]}], False), # 7
    ([{"column": "paid_past_due", "ranges": [[90, 110]]}], [{"column": "paid_past_due", "ranges": [[100, 110]]}], False), # 8
    ([{"column": "paid_past_due", "ranges": [[90, 110]]}], [{"column": "paid_past_due", "ranges": [[80, 110]]}], False), # 9
    ([], [{"column": "paid_past_due", "ranges": [[100, 121]]}], True), # 10
    ([{"column": "paid_past_due", "ranges": [[90, 100]]}], [], True), # 11
    ([], [], True), # 12
    ([{"column": "paid_past_due", "ranges": [[90, 100]]}, {"column": "person_age", "ranges": [[10, 30]]}], [{"column": "paid_past_due", "ranges": [[60, 90]]}, {"column": "person_age", "ranges": [[28, 34]]}], False), # 13
    ([{"column": "paid_past_due", "ranges": [[90, 100]]}, {"column": "person_age", "ranges": [[10, 30]]}], [{"column": "paid_past_due", "ranges": [[60, 90]]}, {"column": "person_age", "ranges": [[60, 90]]}], True), # 14
]

@pytest.mark.parametrize("bad_numeric_list,indeterminate_numeric_list,expected", numeric_test_data)
def test_validate_if_numerical_def_overlapped(bad_numeric_list, indeterminate_numeric_list, expected):
    validator = GoodBadDefValidator()
    isValid = validator.validate_if_numerical_def_overlapped(bad_numeric_list, indeterminate_numeric_list)
    assert isValid == expected


"""
Test Scenario 2
Check if any overlapping definitions between bad & indeterminate categorical definition elements.

Test check any overlapping between bad & indeterminate definition elements, which both are in the form of:
[
    {
        "column": "loan_status",
        "elements": ["1"]
    },
    {
        "column": "person_home_ownership",
        "elements": ["rent", "mortgage"]
    }
], if have overlapping, expected result is a Boolean False,
else, if no overlapping, expected result is a Boolean True.

------------------------
Test Cases Design
------------------------
(1) Single column + no overlapping
(2) Single column + with overlapping
(3) Single column + empty element list
(4) Empty definition list for bad
(5) Empty definition list for indeterminate
(6) Empty definition list for bad & indeterminate
(7) 2 column + overlapping of one of the column
"""


categoric_test_data = [
    ([{"column": "loan_status", "elements": ["1"]}], [{"column": "loan_status", "elements": ["0"]}], True),
    ([{"column": "loan_status", "elements": ["1"]}], [{"column": "loan_status", "elements": ["1", "0"]}], False),
    ([{"column": "loan_status", "elements": []}], [{"column": "loan_status", "elements": ["0"]}], True),
    ([], [{"column": "loan_status", "elements": ["0"]}], True),
    ([{"column": "loan_status", "elements": ["1"]}], [], True),
    ([], [], True),
    ([{"column": "loan_status", "elements": ["1"]}, {"column": "person_home_ownership", "elements": ["RENT", "MORTGAGE"]}], [{"column": "loan_status", "elements": ["0"]}, {"column": "person_home_ownership", "elements": ["MORTGAGE", "OTHERS"]}], False),
]

@pytest.mark.parametrize("bad_categoric_list,indeterminate_categoric_list,expected", categoric_test_data)
def test_validate_if_categorical_def_overlapped(bad_categoric_list, indeterminate_categoric_list, expected):
    validator = GoodBadDefValidator()
    isValid = validator.validate_if_categorical_def_overlapped(bad_categoric_list, indeterminate_categoric_list)
    assert isValid == expected


"""
Test Scenario 3
Check if given a list of definitions, whether all boundaries are in numerical values, and if all upper bound > lower bound.

Test check any non-numerical boundary values entered by user and if all upper bound > lower bound, which the list of definitions
are in the form of:
(
    ("paid_past_due", 70, 80),
    ("paid_past_due", 39, -1),
    ("person_age", 30, 100),
    ...
), if non-numerical value(s) existed or some upper bound <= lower bound, expected result is a Boolean False,
else, expected result is a Boolean True.

------------------------
Test Cases Design
------------------------
(1) Single definition + upper > lower --> True
(2) Single definition + upper < lower --> False
(3) Single definition + upper == lower --> False
(4) Single definition + lower == None --> False
(5) Single definition + lower == upper == None --> False
(6) Single definition + upper == char --> False
(7) Single definition + upper == string --> False
(8) Multiple definitions + all pass --> True
(9) Multiple definitions + all pass except one upper == lower --> False
(10) Multiple definitions + all pass except one upper < lower --> False
(11) Empty definitions --> True
(12) Multiple definitions of different columns + all pass --> True
(13) Multiple definitions of different columns + all pass except 1 fail --> False
"""


numeric_info_test_data = [
    ((("paid_past_due", 70, 80),), True), # 1
    ((("paid_past_due", 60, 50),), False), # 2
    ((("paid_past_due", 0, 0),), False), # 3
    ((("paid_past_due", None, 80),), False), # 4
    ((("paid_past_due", None, None),), False), # 5
    ((("paid_past_due", 60, 'a'),), False), # 6
    ((("paid_past_due", 60, "hello"),), False), # 7
    ((("paid_past_due", 60, 90), ("paid_past_due", 20, 70)), True), # 8
    ((("paid_past_due", 60, 90), ("paid_past_due", 20, 70), ("paid_past_due", 5, 5)), False), # 9
    ((("paid_past_due", 60, 90), ("paid_past_due", 20, 70), ("paid_past_due", 5, 4)), False), # 10
    ((), True), # 11
    ((("paid_past_due", 60, 90), ("person_age", 20, 70), ("paid_past_due", 5, 10)), True), # 12
    ((("paid_past_due", 60, 90), ("person_age", 20, 70), ("paid_past_due", 5, 10), ("person_age", 20, -20)), False), # 13
]

@pytest.mark.parametrize("numeric_info_list,expected", numeric_info_test_data)
def test_validate_numerical_bounds(numeric_info_list, expected):
    validator = GoodBadDefValidator()
    isValid = validator.validate_numerical_bounds(numeric_info_list)
    assert isValid == expected