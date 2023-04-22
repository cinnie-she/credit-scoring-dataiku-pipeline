"""
Numerical:
Narrow down ranges to split the bin
Amend bin boundaries (conflicting boundaries of another bin(s) will be automatically narrowed down)

Categorical:
Split the bin into 2 by indicating the element(s) to be included in one of the bins
Add element(s) from other bin(s) to the selected bin, the added element(s) will be automatically removed from the other bin(s)
"""
from good_bad_def_decoder import GoodBadDefDecoder

# A class for performing interactive binning mechanisms
class InteractiveBinningMachine:
    
    # A method that split bins for categorical column by amending the bins_settings
    @staticmethod
    def categorical_split_bin(col_bin_list, selected_bin_name, element_list):
        if len(element_list) == 0:
            return (col_bin_list, [], [])
        
        old_bin_info_list = list() # TODO: need check empty later 
        updated_bin_info_list = list()
        # If have overlapping
        if InteractiveBinningMachine.check_if_categorical_overlapped(col_bin_list, selected_bin_name, element_list) == True:
            selected_bin_idx = None
            selected_bin_elements = None
            # Find dict with name == selected bin name
            for idx in range(len(col_bin_list)):
                if col_bin_list[idx]["name"] == selected_bin_name:
                    selected_bin_idx = idx
                    selected_bin_elements = col_bin_list[idx]["elements"]
                    break
                
            # Update other bins
            to_remove_idx = list()
            overlapped_element_list = list()
            for idx in range(len(col_bin_list)):
                intersaction = set(col_bin_list[idx]["elements"]) & set(element_list)
                if bool(intersaction) == True and col_bin_list[idx]["name"] != selected_bin_name: 
                    # Get all overlapped elements
                    for intersacted_element in list(intersaction):
                        overlapped_element_list.append(intersacted_element)
                    # Remove overlapped elements from other bins
                    print("update old 1")
                    print([col_bin_list[idx]["name"], col_bin_list[idx]["elements"]])
                    old_bin_info_list.append([col_bin_list[idx]["name"], col_bin_list[idx]["elements"].copy()])
                    print(f"old_bin_info_list: {old_bin_info_list}")
                    col_bin_list[idx]["elements"] = [x for x in col_bin_list[idx]["elements"] if x not in list(intersaction)]
                    # print(col_bin_list[idx]["name"])
                    # print(col_bin_list[idx]["elements"])
                    if len(col_bin_list[idx]["elements"]) == 0:
                        to_remove_idx.append(idx)
                    # bin["name"] = str(bin["elements"])
                    else:
                        print("update new 4")
                        updated_bin_info_list.append([col_bin_list[idx]["name"], col_bin_list[idx]["elements"]])
                        # print(updated_bin_info_list)
            
            for idx in sorted(to_remove_idx, reverse=True):
                del col_bin_list[idx]
            
            # Check if all elements in bin["elements"] appears in element_list (I.e. only add element but not split)
            if all(element in element_list for element in selected_bin_elements) is True:
                # Only add elements, no need split & change name
                print("update old 5")
                print([col_bin_list[selected_bin_idx]["name"], col_bin_list[selected_bin_idx]["elements"]])
                old_bin_info_list.append([col_bin_list[selected_bin_idx]["name"], col_bin_list[selected_bin_idx]["elements"].copy()])
                print(f"old_bin_info_list: {old_bin_info_list}")
                for overlapped_element in overlapped_element_list:
                    col_bin_list[selected_bin_idx]["elements"].append(overlapped_element)
                print("update new 5")
                print([col_bin_list[selected_bin_idx]["name"], col_bin_list[selected_bin_idx]["elements"]])
                updated_bin_info_list.insert(0, [col_bin_list[selected_bin_idx]["name"], col_bin_list[selected_bin_idx]["elements"]])
                print(f"old_bin_info_list: {old_bin_info_list}")
            else: # Need spliting
                print("update 6")
                old_bin_info_list.insert(0, [col_bin_list[selected_bin_idx]["name"], col_bin_list[selected_bin_idx]["elements"]])
                # Remove all elements of elements_list from selected_bin_elements
                col_bin_list[selected_bin_idx]["elements"] = [x for x in col_bin_list[selected_bin_idx]["elements"] if x not in element_list]
                # Change the name
                col_bin_list[selected_bin_idx]["name"] = str(col_bin_list[selected_bin_idx]["elements"])
                updated_bin_info_list.insert(0, [col_bin_list[selected_bin_idx]["name"], col_bin_list[selected_bin_idx]["elements"]])
                # Add a new bin with all element_list elements
                new_bin = {
                    "name": str(element_list),
                    "elements": element_list
                }
                col_bin_list.append(new_bin)
                print("update new 5")
                updated_bin_info_list.insert(1, [str(element_list), element_list])
                

        # IF have no overlapping
        else:
          # Find dict with name == selected bin name
          for bin in col_bin_list:
                if bin["name"] == selected_bin_name:
                    # Only if some element in the selected bin is missing in element_list, then need split, else, nothing need to be done
                    if not all(element in element_list for element in bin["elements"]) is True:
                        old_bin_info_list.append([bin["name"], bin["elements"]])
                        # Remove elements_list from bin["elements"]
                        bin["elements"] = [x for x in bin["elements"] if x not in element_list ]
                        # Change bin["name"] using bin["elements"]
                        bin["name"] = str(bin["elements"])
                        print("update 7")
                        updated_bin_info_list.append([bin["name"], bin["elements"]])

                        # Append new bin to col_bin_list with element_list element
                        new_bin = {
                            "name": str(element_list),
                            "elements": element_list
                        }
                        col_bin_list.append(new_bin)
                        print("update 6")
                        updated_bin_info_list.append([str(element_list), element_list])
                        
                    break
        return (col_bin_list, old_bin_info_list, updated_bin_info_list)

    # Check if any elements in dropdown does not belong to the selected bin
    @staticmethod
    def check_if_categorical_overlapped(col_bin_list, selected_bin_name, element_list):
        # Find dict with name == selected bin name
        for bin in col_bin_list:
            if bin["name"] == selected_bin_name:
                # Loop over element_list to check if any not belong to bin["elements"]
                for element in element_list:
                     if element not in bin["elements"]:
                          return True
            break
        return False

    # A method that merge bins for categorical columns given a list of bin names
    @staticmethod
    def categorical_merge_bins(col_bin_list, selected_bin_name_list):
        # Append the new merged def into col_bin_list
        selected_bin_idx_list = list()
        merged_element_list = list()
        for selected_bin_name in selected_bin_name_list:
            # Search for the bin elements given the name
            bin_elements = None
            for idx in range(len(col_bin_list)):
                if col_bin_list[idx]["name"] == selected_bin_name:
                    selected_bin_idx_list.append(idx)
                    bin_elements =  col_bin_list[idx]["elements"]
            # Append the bin elements to merged_element_list
            for element in bin_elements:
                merged_element_list.append(element)
        
        # Update the new_bin_info
        new_bin_info = [str(merged_element_list), merged_element_list]
        new_bin = {
            "name": new_bin_info[0],
            "elements": new_bin_info[1],
        }
        col_bin_list.append(new_bin)
        
        # Remove all definitions for selected bins
        for index in sorted(selected_bin_idx_list, reverse=True):
            del col_bin_list[index]
        
        return (col_bin_list, new_bin_info)
    
    # A method that takes 2 definition (1 target & 1 for removal), and returns a narrowed definition of bin ranges
    @staticmethod
    def numerical_compute_narrowed_bin_ranges(target, element_to_remove_list):
        has_changed = False
        idx_to_remove_from_target = list()
        ranges_to_add = list()
        for target_idx in range(len(target)):
            for curr_idx in range(len(element_to_remove_list)):
                if element_to_remove_list[curr_idx][0] < target[target_idx][1]:
                    if element_to_remove_list[curr_idx][1] >= target[target_idx][1] and element_to_remove_list[curr_idx][0] <= target[target_idx][0]: # completely remove r
                        idx_to_remove_from_target.append(target_idx)
                        has_changed = True
                        break
                    elif element_to_remove_list[curr_idx][1] >= target[target_idx][1] and element_to_remove_list[curr_idx][0] > target[target_idx][0]: # narrow down
                        target[target_idx] = [target[target_idx][0], element_to_remove_list[curr_idx][0]]
                        has_changed = True
                        break
                    elif element_to_remove_list[curr_idx][1] < target[target_idx][1] and element_to_remove_list[curr_idx][1] > target[target_idx][0] and element_to_remove_list[curr_idx][0] <= target[target_idx][0]: # narrow down
                        target[target_idx] = [element_to_remove_list[curr_idx][1], target[target_idx][1]]
                        has_changed = True
                        break
                    elif element_to_remove_list[curr_idx][1] < target[target_idx][1] and element_to_remove_list[curr_idx][1] > target[target_idx][0] and element_to_remove_list[curr_idx][0] > target[target_idx][0]: # split to two
                        target[target_idx] = [target[target_idx][0], element_to_remove_list[curr_idx][0]]
                        ranges_to_add.append([element_to_remove_list[curr_idx][1], target[target_idx][1]])
                        has_changed = True
                        break
        
        for idx in sorted(idx_to_remove_from_target, reverse=True):
            del target[idx]
        for r in ranges_to_add:
            target.append(r)
        
        return (has_changed, target)
        
    # A method that split bin for numerical columns based on the selected bin and user-specified ranges
    @staticmethod
    def numerical_split_bin(col_bin_list, range_list):
        """
        E.g., 
        selected bin= [      [1, 10],       [15, 20],         [30, 35],       [40, 60],       [70, 75],       [80, 90],       [98,   100]]
        
        another bin = [[0, 1],      [10, 15],       [ 20, 30 ],       [35, 40],       [60, 70],       [75, 80],       [90, 98]]
        
        new_range =   [         [5,  13], [14, 18],  [23, 25],   [33,            50],   [65,                             95],   [99, 100]]
        """
        old_bin_info_list = list()
        updated_bin_info_list = list()
        
        sorted_range_list = GoodBadDefDecoder.sort_numerical_def_ranges(range_list)
        
        idx_to_remove = list()
        # For each col_bin in col_bin_list, remove range_list
        for idx in range(len(col_bin_list)):
            has_changed, updated_bin_ranges = InteractiveBinningMachine.numerical_compute_narrowed_bin_ranges(col_bin_list[idx]["ranges"], sorted_range_list)
            if has_changed == True:
                old_bin_info_list.append([col_bin_list[idx]["name"], InteractiveBinningMachine.get_str_from_ranges(col_bin_list[idx]["ranges"])])
                col_bin_list[idx]["ranges"] = updated_bin_ranges
                if len(updated_bin_ranges) == 0: # check if after removal becomes empty, if so need to remove it later
                    idx_to_remove.append(idx)
                    updated_bin_info_list.append([col_bin_list[idx]["name"], "This bin will be removed."])
                else:
                    updated_bin_info_list.append([col_bin_list[idx]["name"], InteractiveBinningMachine.get_str_from_ranges(col_bin_list[idx]["ranges"])])
            
        # Remove empty defs
        for idx in sorted(idx_to_remove, reverse=True):
            del col_bin_list[idx]
        
        # Append to col_bin_list the range_list
        range_str = InteractiveBinningMachine.get_str_from_ranges(sorted_range_list)
        new_bin = {
            "name": range_str,
            "ranges": sorted_range_list,
        }
        col_bin_list.append(new_bin)
        updated_bin_info_list.append(range_str, range_str)
        
        return (col_bin_list, old_bin_info_list, updated_bin_info_list)
    
    # A method that merge bins for numerical columns based on a list name of the selected bins
    @staticmethod
    def numerical_merge_bins(col_bin_list, selected_bin_name_list):
        # Append the new merged def into col_bin_list
        selected_bin_idx_list = list()
        merged_ranges_list = list()
        for selected_bin_name in selected_bin_name_list:
            # Search for the bin rangess given the name
            bin_ranges = None
            for idx in range(len(col_bin_list)):
                if col_bin_list[idx]["name"] == selected_bin_name:
                    selected_bin_idx_list.append(idx)
                    bin_ranges =  col_bin_list[idx]["ranges"]
                    
            # Add the bin rangess to merged_ranges_list
            for r in bin_ranges:
                # Check if any continuous ranges can merge
                merge_with_idx = [None, None]
                for idx in range(len(merged_ranges_list)):
                    if merged_ranges_list[idx][0] == r[1]:
                        merge_with_idx[1] = idx
                    elif merged_ranges_list[idx][1] == r[0]:
                        merge_with_idx[0] = idx
                
                if merge_with_idx[0] == None and merge_with_idx[1] == None: # No merging needed
                    merged_ranges_list.append(r)
                elif merge_with_idx[0] != None and merge_with_idx[1] == None:
                    merged_ranges_list.append([merged_ranges_list[merge_with_idx[0]][0], r[1]])
                    # Remove overlapped range
                    del merged_ranges_list[merge_with_idx[0]]
                elif merge_with_idx[0] == None and merge_with_idx[1] != None:
                    merged_ranges_list.append([r[0], merged_ranges_list[merge_with_idx[1]][1]])
                    # Remove overlapped range
                    del merged_ranges_list[merge_with_idx[1]]
                else:
                    merged_ranges_list.append([merged_ranges_list[merge_with_idx[0]][0], merged_ranges_list[merge_with_idx[1]][1]])
                    merge_with_idx = sorted(merge_with_idx, reverse=True)
                    for idx in merge_with_idx:
                        del merged_ranges_list[idx]
                
        # Update the new_bin_info
        sorted_merged_ranges_list = GoodBadDefDecoder.sort_numerical_def_ranges(merged_ranges_list)
        ranges_str = InteractiveBinningMachine.get_str_from_ranges(sorted_merged_ranges_list)
        new_bin_info = [ranges_str, ranges_str]
        new_bin = {
            "name": ranges_str,
            "ranges": sorted_merged_ranges_list,
        }
        col_bin_list.append(new_bin)
        
        return (col_bin_list, new_bin_info)
    
    # A method to convert a list e.g., [[10, 20], [30, 50]], into a string e.g., "[[10, 20), [30, 50)]".
    @staticmethod
    def get_str_from_ranges(ranges):
        if not isinstance(ranges, list):
            return -1
        if len(ranges) == 0:
            return '[]'
        
        ranges = GoodBadDefDecoder.sort_numerical_def_ranges(ranges)
        
        ranges_str = "["
        ranges_str = f"{ranges_str}[{ranges[0][0]}, {ranges[0][1]})"
        for idx in range(1, len(ranges)):
            ranges_str = f"{ranges_str}, [{ranges[idx][0]}, {ranges[idx][1]})"
        ranges_str += "]"
        return ranges_str    
        
    # Check if any user-specified ranges falls outside the selected bin
    # @staticmethod
    # def check_if_numerical_overlapped(col_bin_list, selected_bin_name, range_list):
    #     # Get the definition ranges
    #     selected_bin_ranges = None
    #     for bin in col_bin_list:
    #         if bin["name"] == selected_bin_name:
    #             selected_bin_ranges = bin["ranges"]
                
    #     # Check any overlapping
    #     for r in range_list:
    #         for def_range in selected_bin_ranges:
    #             if r[0] < def_range[0] and r[1] >= def_range[0]: # the range cuts the definition, but falls outside the definition
    #                 return True
    #             elif r[0] >= def_range[0] and r[1] <= def_range[1]: # the range lies within the definition
    #                 break
    #             elif r[0] >= def_range[0] and r[0] <= def_range[1] and r[1] > def_range[1]: # the range cuts the definition, but falls outside the definition
    #                 return True
                       
    #     return False
    
    
    
    
col_bin_list = [
    {
        "name": "Good",
        "elements": ["A", "B", "C"],
    }, 
    {
        "name": "Poor",
        "elements": ["F", "E"],
    },
    {
        "name": "Indeterminate",
        "elements": ["D"]
    }
]
selected_bin_name = "Good"
element_list = ["A", "B", "C", "D"]
print(col_bin_list)
print(InteractiveBinningMachine.categorical_split_bin(col_bin_list, selected_bin_name, element_list))

# Split:
# ([{'name': 'Good', 'elements': ['A', 'B', 'C']}, {'name': 'Poor', 'elements': ['F', 'E']}, {'name': 'Indeterminate', 'elements': ['D']}], "Good", ["A", "B"], ([{'name': "['C']", 'elements': ['C']}, {'name': 'Poor', 'elements': ['F', 'E']}, {'name': 'Indeterminate', 'elements': ['D']}, {'name': "['A', 'B']", 'elements': ['A', 'B']}], [['Good', ['A', 'B', 'C']]], [["['C']", ['C']], ["['A', 'B']", ['A', 'B']]]))

# Split with overlap
# ([{'name': 'Good', 'elements': ['A', 'B', 'C']}, {'name': 'Poor', 'elements': ['F', 'E']}, {'name': 'Indeterminate', 'elements': ['D']}], "Good", ["A", "F"], ([{'name': "['B', 'C']", 'elements': ['B', 'C']}, {'name': 'Poor', 'elements': ['E']}, {'name': 'Indeterminate', 'elements': ['D']}, {'name': "['A', 'F']", 'elements': ['A', 'F']}], [['Good', ['A', 'B', 'C']], ['Poor', ['F', 'E']]], [['Good', ['B', 'C']], ["['A', 'F']", ['A', 'F']], ['Poor', ['E']]]))

([
    {'name': 'Good', 'elements': [['A', 'C', 'B', 'D']]}, 
    {'name': 'Poor', 'elements': ['F', 'E']}, 
    {'name': 'Indeterminate', 'elements': []}],  # should
 
 [['Good', ['A', 'B', 'C']], ['Indeterminate', ['D']], ['Good', [['A', 'C', 'B', 'D']]]], 
 [['Good', [['A', 'C', 'B', 'D']]], ['Good', [['A', 'C', 'B', 'D']]], ['Indeterminate', []]])