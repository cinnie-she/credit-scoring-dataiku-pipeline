# Draft of good bad definition data structure.
good_bad_def = {
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


# A class for validating user inputs for good bad definitions
class GoodBadDefValidator:
    # A method to validate if numerical definitions for bad/indeterminate has overlapped
    def validateIfNumericalDefOverlapped(self, bad_numeric_list, indeterminate_numeric_list):
        return True
    
    # A method to validate if categorical definitions for bad/indeterminate has overlapped
    def validateIfCategoricalDefOverlapped(self, bad_categoric_list, indeterminate_categoric_list):
        for bad_categoric_def in bad_categoric_list:
            column = bad_categoric_def["column"]
            for indeterminate_categoric_def in indeterminate_categoric_list:
                if indeterminate_categoric_def["column"] == column: # found matching column definition
                    # Check if any overlapping definition
                    for element in bad_categoric_def["elements"]:
                        if element in indeterminate_categoric_def["elements"]:
                            return False
                    break
        return True
    
    # A method to validate if all numerical definition range have upper bound > lower bound, if not, returns false
    def validateNumericalBounds(self, numeric_info_list):
        for numeric_info in numeric_info_list:
            a_range = [numeric_info["props"]["children"][3]['props']['value'],
                       numeric_info["props"]["children"][6]['props']['value']]
            if a_range[1] <= a_range[0]:
                return False
        return True


# A class for obtaining user inputs from the section UI info
class GoodBadDefDecoder:
    # A method to translate section UI info to a list of numerical definition
    def getNumericDefListFromSection(self, numeric_info_list):
        numeric_list = list()  # initialization

        for numeric_info in numeric_info_list:
            single_def_dict = dict()
            column = numeric_info["props"]["children"][1]['props']['value']
            a_range = [numeric_info["props"]["children"][3]['props']['value'],
                       numeric_info["props"]["children"][6]['props']['value']]
            # The 2 bounds are valid, now check if any overlapping with previously saved data
            has_column_overlap = False
            for def_idx, saved_def in enumerate(numeric_list):
                if saved_def["column"] == column:
                    has_column_overlap = True
                    has_range_overlap = False
                    # Merge range to element list
                    for def_range_idx, def_range in enumerate(saved_def["ranges"]):
                        if a_range[0] <= def_range[0] and a_range[1] >= def_range[1]:
                            has_range_overlap = True
                            numeric_list[def_idx]["ranges"][def_range_idx] = [
                                a_range[0], a_range[1]]
                            break
                        elif a_range[0] <= def_range[0] and a_range[1] >= def_range[0] and a_range[1] <= def_range[1]:
                            has_range_overlap = True
                            numeric_list[def_idx]["ranges"][def_range_idx] = [
                                a_range[0], def_range[1]]
                            break
                        elif a_range[0] >= def_range[0] and a_range[0] <= def_range[1] and a_range[1] >= def_range[1]:
                            has_range_overlap = True
                            numeric_list[def_idx]["ranges"][def_range_idx] = [
                                def_range[0], a_range[1]]
                            break
                    if has_range_overlap == False:
                        numeric_list[def_idx]["ranges"].append(a_range)
                    break
            if has_column_overlap == False:
                single_def_dict["column"] = column
                single_def_dict["ranges"] = [a_range]
                numeric_list.append(single_def_dict)
        return numeric_list
    # A method to translate section UI info to a list of categorical definition

    def getCategoricalDefListFromSection(self, section):
        categoric_info_list = section[0]['props']['children'][4]['props']['children']
        categoric_list = list()  # initialization
        for categoric_info in categoric_info_list:
            single_def_dict = dict()
            column = categoric_info["props"]["children"][1]['props']['value']
            elements = categoric_info["props"]["children"][3]['props']['value']
            # Check if any overlapping with previously saved data
            has_overlap = False
            for saved_def in categoric_list:
                if saved_def["column"] == column:
                    has_overlap = True
                    # Append element to elements list if it is not existed yet
                    for element in elements:
                        if element not in saved_def["elements"]:
                            saved_def["elements"].append(element)
                    break
            if has_overlap == False:
                single_def_dict["column"] = column
                single_def_dict["elements"] = elements
                categoric_list.append(single_def_dict)
        return categoric_list
