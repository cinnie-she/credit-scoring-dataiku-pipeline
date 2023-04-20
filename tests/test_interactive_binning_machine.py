from interactive_binning_machine import InteractiveBinningMachine
import pandas as pd
import pytest

"""
TEST InteractiveBinningMachine class
"""

"""
Test Scenario 1
Split bins for categorical column by amending the bins_settings

Test split bins for categorical column.

------------------------
Test Cases Design
------------------------
(1) Simply splitting
(2) Include all elements from selected bin (i.e., do nothing)
(3) Include no elements (i.e., do nothing)
(4) Add 1 elements from another bin (which another bin only have that element)
(5) Add 2 elements from another bin (which another bin only have that 2 elements)
(6) Add 1 elements from another bin (which another bin still have other elements)
(7) Split & Add 1 element from other bin (which another bin only have that element)
(8) Split & Add 1 element from other bin (which another bin still have other elements)
"""
categorical_split_bin_test_data = [
    ([{'name': 'Good', 'elements': ['A', 'B', 'C']}, {'name': 'Poor', 'elements': ['F', 'E']}, {'name': 'Indeterminate', 'elements': ['D']}], "Good", ["A", "B"], [{'name': "['C']", 'elements': ['C']}, {'name': 'Poor', 'elements': ['F', 'E']}, {'name': 'Indeterminate', 'elements': ['D']}, {'name': "['A', 'B']", 'elements': ['A', 'B']}], [['Good', ['A', 'B', 'C']]], [["['C']", ['C']], ["['A', 'B']", ['A', 'B']]]), # 1
    ([{'name': 'Good', 'elements': ['A', 'B', 'C']}, {'name': 'Poor', 'elements': ['F', 'E']}, {'name': 'Indeterminate', 'elements': ['D']}], "Good", ["A", "B", "C"], [{'name': "Good", 'elements': ['A', 'B', 'C']}, {'name': 'Poor', 'elements': ['F', 'E']}, {'name': 'Indeterminate', 'elements': ['D']}], [], []), # 2
    ([{'name': 'Good', 'elements': ['A', 'B', 'C']}, {'name': 'Poor', 'elements': ['F', 'E']}, {'name': 'Indeterminate', 'elements': ['D']}], "Good", [], [{'name': "Good", 'elements': ['A', 'B', 'C']}, {'name': 'Poor', 'elements': ['F', 'E']}, {'name': 'Indeterminate', 'elements': ['D']}], [], []), # 3
    
    ([{'name': 'Good', 'elements': ['A', 'B', 'C']}, {'name': 'Poor', 'elements': ['F', 'E']}, {'name': 'Indeterminate', 'elements': ['D']}], "Good", ["A", "B", "C", "D"], [{'name': 'Good', 'elements': ['A', 'B', 'C', 'D']}, {'name': 'Poor', 'elements': ['F', 'E']}], [['Indeterminate', ['D']], ['Good', ['A', 'B', 'C']]], [['Good', ['A', 'B', 'C', 'D']]]), # 4
    ([{'name': 'Good', 'elements': ['A', 'B', 'C']}, {'name': 'Poor', 'elements': ['F', 'E']}, {'name': 'Indeterminate', 'elements': ['D', 'G']}], "Good", ["A", "B", "C", "D", "G"], [{'name': 'Good', 'elements': ['A', 'B', 'C', 'D', 'G']}, {'name': 'Poor', 'elements': ['F', 'E']}], [['Indeterminate', ['D', 'G']], ['Good', ['A', 'B', 'C']]], [['Good', ['A', 'B', 'C', 'D', 'G']]]), # 5
    ([{'name': 'Good', 'elements': ['A', 'B', 'C']}, {'name': 'Poor', 'elements': ['F', 'E']}, {'name': 'Indeterminate', 'elements': ['D', 'G']}], "Good", ["A", "B", "C", "D"], [{'name': 'Good', 'elements': ['A', 'B', 'C', 'D']}, {'name': 'Poor', 'elements': ['F', 'E']}, {'name': 'Indeterminate', 'elements': ['G']}], [['Indeterminate', ['D', 'G']], ['Good', ['A', 'B', 'C']]], [['Good', ['A', 'B', 'C', 'D']], ['Indeterminate', ['G']]]), # 6
    
    ([{'name': 'Good', 'elements': ['A', 'B', 'C']}, {'name': 'Poor', 'elements': ['F', 'E']}, {'name': 'Indeterminate', 'elements': ['D']}], "Good", ["A", "D"], [{'name': "['B', 'C']", 'elements': ['B', 'C']}, {'name': 'Poor', 'elements': ['F', 'E']}, {'name': "['A', 'D']", 'elements': ['A', 'D']}], [['Good', ['A', 'B', 'C']], ['Indeterminate', ['D']]], [["['B', 'C']", ['B', 'C']], ["['A', 'D']", ['A', 'D']]]), # 7
    ([{'name': 'Good', 'elements': ['A', 'B', 'C']}, {'name': 'Poor', 'elements': ['F', 'E']}, {'name': 'Indeterminate', 'elements': ['D']}], "Good", ["A", "F"], [{'name': "['B', 'C']", 'elements': ['B', 'C']}, {'name': 'Poor', 'elements': ['E']}, {'name': 'Indeterminate', 'elements': ['D']}, {'name': "['A', 'F']", 'elements': ['A', 'F']}], [['Good', ['A', 'B', 'C']], ['Poor', ['F', 'E']]], [["['B', 'C']", ['B', 'C']], ["['A', 'F']", ['A', 'F']], ['Poor', ['E']]]), # 8
]

@pytest.mark.parametrize("col_bin_list,selected_bin_name,element_list,expected_col_bin_list,expected_old_bin_info_list,expected_updated_bin_info_list", categorical_split_bin_test_data)
def test_categorical_split_bin(col_bin_list, selected_bin_name, element_list, expected_col_bin_list, expected_old_bin_info_list, expected_updated_bin_info_list):
    result_col_bin_list, result_old_bin_info_list, result_updated_bin_info_list = InteractiveBinningMachine.categorical_split_bin(col_bin_list, selected_bin_name, element_list)
    print("---------------------")
    print(f"col_bin_list: {col_bin_list}, selected_bin_name: {selected_bin_name}, element_list: {element_list}")
    print()
    print(f"result_col_bin_list: {result_col_bin_list}, expected_col_bin_list: {expected_col_bin_list}")
    is_same_1 = True
    for idx in range(len(result_col_bin_list)):
        for element_idx in range(len(result_col_bin_list[idx]["elements"])):
            if result_col_bin_list[idx]["elements"][element_idx] not in expected_col_bin_list[idx]["elements"]:
                is_same_1 = False
    print(is_same_1)
    print()
    print(f"result_old_bin_info_list: {result_old_bin_info_list}, expected_old_bin_info_list: {expected_old_bin_info_list}")
    is_same_2 = True
    for idx in range(len(result_old_bin_info_list)):
        for old_bin_info_idx in range(len(result_old_bin_info_list[idx][1])):
            if result_old_bin_info_list[idx][1][old_bin_info_idx] not in expected_old_bin_info_list[idx][1]:
                is_same_2 = False
    print(is_same_2)
    print()
    print(f"result_updated_bin_info_list: {result_updated_bin_info_list}, expected_updated_bin_info_list: {expected_updated_bin_info_list}")
    is_same_3 = True
    for idx in range(len(result_updated_bin_info_list)):
        for new_bin_info_idx in range(len(result_updated_bin_info_list[idx][1])):
            if result_updated_bin_info_list[idx][1][new_bin_info_idx] not in expected_updated_bin_info_list[idx][1]:
                is_same_3 = False
    print(is_same_3)
    print()
    assert (is_same_1 and is_same_2 and is_same_3)

"""
Test Scenario 2
Check if any elements in dropdown does not belong to the selected bin

Test checking any categorical elements in dropdown does not belong to the selected bin.

------------------------
Test Cases Design
------------------------
(1) 
"""

# def test_check_if_categorical_overlapped(col_bin_list, selected_bin_name, element_list, expected):
#     pass

"""
Test Scenario 3
Merge bins for categorical columns given a list of bin names

Test merging bins for categorical columns given a list of bin names.

------------------------
Test Cases Design
------------------------
(1) 
"""

# def test_categorical_merge_bins(col_bin_list, selected_bin_name_list, expected):
#     pass


"""
Test Scenario 4
Takes 2 definition (1 target & 1 for removal), and returns a narrowed definition of bin ranges

Test taking 2 definition (1 target & 1 for removal), and returns a narrowed definition of bin ranges.

------------------------
Test Cases Design
------------------------
(1) 
"""

# def test_numerical_compute_narrowed_bin_ranges(target, element_to_remove_list, expected):
#     pass

"""
Test Scenario 5
Split bin for numerical columns based on the selected bin and user-specified ranges

Test splitting bin for numerical columns based on the selected bin and user-specified ranges.

------------------------
Test Cases Design
------------------------
(1) 
"""

# def test_numerical_split_bin(col_bin_list, range_list, expected):
#     pass


"""
Test Scenario 6
Merge bins for numerical columns based on a list name of the selected bins

Assumption: no overlapping of ranges between bins of the same column

Test merging bins for numerical columns based on a list name of the selected bins.

Input:
col_bin_list = [
    {
        "name": "0-9999, 30000-39999",
        "ranges": [[0, 9999], [30000, 39999]],
    },
    {
        "name": "20000-29999",
        "ranges": [[20000, 29999]],
    },
    ...
]

selected_bin_name_list = ["0-9999, 30000-39999", "good", "poor", ...]

Output: (col_bin_list, old_bin_info_list, updated_bin_info_list)

(1) col_bin_list = revised col_bin_list for storing
(2) old_bin_info_list = [[old_bin_name, old_bin_elements_list], [old_bin_name2, old_bin_elements_list2], ...] for later display on the UI
(3) updated_bin_info_list = [[updated_bin_name, updated_bin_elements_list], [updated_bin_name2, updated_bin_elements_list2], ...] for later display on the UI

------------------------
Test Cases Design
------------------------
(1) 
"""

# numerical_merge_bins_test_data = [
#     ([], [], ([], [], [])),
#     ([{"name": "good", "ranges": [[20, 30]]}, {"name": "normal", "ranges": [[10, 15]]}, {"name": "poor", "ranges": [[30, 35]]}, {"name": "others", "ranges": [[15, 20], [35, 50], [0, 10]]}], ["good", "noraml", "poor"], ([], [], [])),
# ]

# @pytest.mark.parametrize("input_df_path,col_bins_settings,good_bad_def,expected", numerical_merge_bins_test_data)
# def test_numerical_merge_bins(col_bin_list, selected_bin_name_list, expected):
#     pass


"""
Test Scenario 7
Convert a list e.g., [[10, 20], [30, 50]], into a string e.g., "[[10, 20), [30, 50)]".

Test converting a list e.g., [[10, 20], [30, 50]], into a string e.g., "[[10, 20), [30, 50)]".

------------------------
Test Cases Design
------------------------
(1) Empty list
(2) None
(3) Already sorted list
(4) Descendingly sorted list
(5) List with random order
(6) Single element
"""

str_from_ranges_test_data = [
    ([], "[]"), # 1
    (None, -1), # 2
    ([[10, 20], [30, 50], [60, 70]], '[[10, 20), [30, 50), [60, 70)]'), # 3
    ([[60, 70], [30, 50],[10, 20]], '[[10, 20), [30, 50), [60, 70)]'), # 4
    ([[60, 70], [15, 17], [30, 50], [18, 19], [10, 20], [22, 28], [80, 90]], '[[10, 20), [15, 17), [18, 19), [22, 28), [30, 50), [60, 70), [80, 90)]'), # 5
    ([[10, 20]], '[[10, 20)]'), # 6
]

@pytest.mark.parametrize("ranges,expected", str_from_ranges_test_data)
def test_get_str_from_ranges(ranges, expected):
    result = InteractiveBinningMachine.get_str_from_ranges(ranges)
    print(f"range: {ranges}, result: {result}, expected: {expected}")
    assert result == expected