# A class for validating user inputs for good bad definitions
class GoodBadDefValidator:
    # A method to validate if numerical definitions for bad/indeterminate has overlapped
    def validate_if_numerical_def_overlapped(self, bad_numeric_list, indeterminate_numeric_list):
        for bad_numeric_def in bad_numeric_list:
            column = bad_numeric_def["column"]
            for indeterminate_numeric_def in indeterminate_numeric_list:
                # found matching column definition
                if indeterminate_numeric_def["column"] == column:
                    # Check if any overlapping definition
                    for bad_range in bad_numeric_def["ranges"]:
                        for indeterminate_range in indeterminate_numeric_def["ranges"]:
                            if bad_range[0] < indeterminate_range[0] and bad_range[1] > indeterminate_range[0]:
                                return False
                            if bad_range[0] < indeterminate_range[1] and bad_range[1] > indeterminate_range[1]:
                                return False
                            if bad_range[0] == indeterminate_range[0] and bad_range[1] <= indeterminate_range[1]:
                                return False
                            if bad_range[1] == indeterminate_range[1] and bad_range[0] >= indeterminate_range[0]:
                                return False
                    break
        return True

    # A method to validate if categorical definitions for bad/indeterminate has overlapped
    def validate_if_categorical_def_overlapped(self, bad_categoric_list, indeterminate_categoric_list):
        for bad_categoric_def in bad_categoric_list:
            column = bad_categoric_def["column"]
            for indeterminate_categoric_def in indeterminate_categoric_list:
                # found matching column definition
                if indeterminate_categoric_def["column"] == column:
                    # Check if any overlapping definition
                    for element in bad_categoric_def["elements"]:
                        if element in indeterminate_categoric_def["elements"]:
                            return False
                    break
        return True

    # A method to validate if all numerical definition range have upper bound > lower bound, if not, returns false
    def validate_numerical_bounds(self, numeric_info_list):
        for numeric_info in numeric_info_list:
            a_range = [numeric_info[1], numeric_info[2]]
            try:
                if a_range[1] <= a_range[0]:
                    return False
            except:
                return False
        return True