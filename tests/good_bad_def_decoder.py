# A class for merging overlapping good bad definition ranges/elements for the same type (bad or indeterminate)
class GoodBadDefDecoder:    
    # A method to translate numerical definition ranges defined by user (with/without overlapping) info to a list of numerical definition (no overlapping)
    def get_numeric_def_list_from_section(self, numeric_info_list):
        numeric_list = list()  # initialization

        for numeric_info in numeric_info_list:
            single_def_dict = dict()
            column = numeric_info[0]
            a_range = [numeric_info[1], numeric_info[2]]
            # The 2 bounds are valid, now check if any overlapping with previously saved data
            has_column_overlap = False
            for def_idx, saved_def in enumerate(numeric_list):
                if saved_def["column"] == column:
                    has_column_overlap = True
                    has_range_overlap = False
                    overlapped_def_range_idxes = list()
                    # Merge range to element list
                    for def_range_idx, def_range in enumerate(saved_def["ranges"]):
                        if len(overlapped_def_range_idxes) != 0:
                            a_range = numeric_list[def_idx]["ranges"][overlapped_def_range_idxes[0]]

                        if a_range[0] <= def_range[0] and a_range[1] >= def_range[1]:
                            has_range_overlap = True
                            numeric_list[def_idx]["ranges"][def_range_idx] = [
                                a_range[0], a_range[1]]
                            overlapped_def_range_idxes.insert(0, def_range_idx)
                        elif def_range[0] <= a_range[0] and def_range[1] >= a_range[1]:
                            has_range_overlap = True
                        elif a_range[0] <= def_range[0] and a_range[1] >= def_range[0] and a_range[1] <= def_range[1]:
                            has_range_overlap = True
                            numeric_list[def_idx]["ranges"][def_range_idx] = [
                                a_range[0], def_range[1]]
                            overlapped_def_range_idxes.insert(0, def_range_idx)
                        elif a_range[0] >= def_range[0] and a_range[0] <= def_range[1] and a_range[1] >= def_range[1]:
                            has_range_overlap = True
                            numeric_list[def_idx]["ranges"][def_range_idx] = [
                                def_range[0], a_range[1]]
                            overlapped_def_range_idxes.insert(0, def_range_idx)
                    if len(overlapped_def_range_idxes) != 0:
                        del overlapped_def_range_idxes[0]
                        for i in sorted(overlapped_def_range_idxes, reverse=True):
                            del numeric_list[def_idx]["ranges"][i]
                    if has_range_overlap == False:
                        numeric_list[def_idx]["ranges"].append(a_range)
                    break
            if has_column_overlap == False:
                single_def_dict["column"] = column
                single_def_dict["ranges"] = [a_range]
                numeric_list.append(single_def_dict)
        return numeric_list
    
    # # A method to translate categorical definition elements defined by user (with/without overlapping) info to a list of categorical definition (no overlapping)
    def get_categorical_def_list_from_section(self, categoric_info_list):
        categoric_list = list()  # initialization
        for categoric_info in categoric_info_list:
            single_def_dict = dict()
            column = categoric_info[0]
            elements = categoric_info[1]
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