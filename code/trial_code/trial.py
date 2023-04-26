def validate_new_name(new_name, temp_col_bins_settings, selected_bin_name=None):
        # Return false if name has already been use. otherwise, return True
        if selected_bin_name == None:
            for bin_def in temp_col_bins_settings["bins"]:
                if bin_def["name"] == new_name:
                    return False
            return True
        else:
            if selected_bin_name == new_name:
                return True
            for bin_def in temp_col_bins_settings["bins"]:
                if bin_def["name"] == new_name:
                    return False
            return True
 
 
def sort_numerical_def_ranges(numeric_def_r):
    sorted_def_ranges = list()
    for r in numeric_def_r:
        has_appended = False
        for idx in range(len(sorted_def_ranges)):
            if r[0] < sorted_def_ranges[idx][0]:
                sorted_def_ranges.insert(idx, r)
                has_appended = True
                break
        if has_appended == False:
            sorted_def_ranges.append(r)
    return sorted_def_ranges
 
def get_str_from_ranges(ranges):
    if not isinstance(ranges, list):
        return -1
    if len(ranges) == 0:
        return '[]'
    
    ranges = sort_numerical_def_ranges(ranges)
    
    ranges_str = "["
    ranges_str = f"{ranges_str}[{ranges[0][0]}, {ranges[0][1]})"
    for idx in range(1, len(ranges)):
        ranges_str = f"{ranges_str}, [{ranges[idx][0]}, {ranges[idx][1]})"
    ranges_str += "]"
    return ranges_str 
        
def numeric_create_new_bin(new_bin_name, new_bin_ranges, temp_col_bins_settings):
    if len(new_bin_ranges) == 0:
        return (temp_col_bins_settings, -6, -6) 
    
    if validate_new_name(new_bin_name, temp_col_bins_settings) == False:
        return (temp_col_bins_settings, -1, -1)
    
    old_bin_list = list()
    new_bin_list = list()
    
    bin_to_remove_idx_li = list()
    # for all bins, remove overlapped ranges with new_bin_ranges
    for bin_def_idx in range(len(temp_col_bins_settings["bins"])):
        with_changes = False
        for new_r in new_bin_ranges:
            r_to_remove_idx_li = list()
            r_to_append_li = list()
            for r_idx in range(len(temp_col_bins_settings["bins"][bin_def_idx]["ranges"])):
                r = temp_col_bins_settings["bins"][bin_def_idx]["ranges"][r_idx]
                if new_r[1] <= r[0]:
                    continue
                elif new_r[0] <= r[0] and new_r[1] > r[0] and new_r[1] < r[1]:
                    if with_changes == False:
                        old_bin_list.append([temp_col_bins_settings["bins"][bin_def_idx]["name"], get_str_from_ranges(temp_col_bins_settings["bins"][bin_def_idx]["ranges"])])
                        with_changes = True
                    # then new def = [new_r[1], r[1]]
                    temp_col_bins_settings["bins"][bin_def_idx]["ranges"][r_idx] = [new_r[1], r[1]]
                elif new_r[0] <= r[0] and new_r[1] > r[0] and new_r[1] >= r[1]:
                    if with_changes == False:
                        old_bin_list.append([temp_col_bins_settings["bins"][bin_def_idx]["name"], get_str_from_ranges(temp_col_bins_settings["bins"][bin_def_idx]["ranges"])])
                        with_changes = True
                    # remove the def r
                    r_to_remove_idx_li.append(r_idx)
                elif new_r[0] > r[0] and new_r[1] < r[1]:
                    if with_changes == False:
                        old_bin_list.append([temp_col_bins_settings["bins"][bin_def_idx]["name"], get_str_from_ranges(temp_col_bins_settings["bins"][bin_def_idx]["ranges"])])
                        with_changes = True
                    # split to two = [r[0], new_r[0]] & [new_r[1], r[1]]
                    temp_col_bins_settings["bins"][bin_def_idx]["ranges"][r_idx] = [r[0], new_r[0]]
                    r_to_append_li.append([new_r[1], r[1]])
                elif new_r[0] > r[0] and new_r[0] < r[1] and new_r[1] >= r[1]:
                    if with_changes == False:
                        old_bin_list.append([temp_col_bins_settings["bins"][bin_def_idx]["name"], get_str_from_ranges(temp_col_bins_settings["bins"][bin_def_idx]["ranges"])])
                        with_changes = True
                    # new def = [r[0], new_r[0]]
                    temp_col_bins_settings["bins"][bin_def_idx]["ranges"][r_idx] = [r[0], new_r[0]]
                elif new_r[0] >= r[1]:
                    continue
            
            for idx in sorted(r_to_remove_idx_li, reverse=True):
                del temp_col_bins_settings["bins"][bin_def_idx]["ranges"][idx]
            
            for r_to_append in r_to_append_li:
                temp_col_bins_settings["bins"][bin_def_idx]["ranges"].append(r_to_append)
                
        if len(temp_col_bins_settings["bins"][bin_def_idx]["ranges"]) == 0:
            bin_to_remove_idx_li.append(bin_def_idx)
        elif with_changes == True:
            new_bin_list.append([temp_col_bins_settings["bins"][bin_def_idx]["name"], get_str_from_ranges(temp_col_bins_settings["bins"][bin_def_idx]["ranges"])])
            
    # Remove bin_def if it has empty def range list
    for idx in sorted(bin_to_remove_idx_li, reverse=True):
        del temp_col_bins_settings["bins"][idx]
    
    if new_bin_name == "" or new_bin_name == None:
        new_bin_name = get_str_from_ranges(new_bin_ranges)
        
    if validate_new_name(new_bin_name, temp_col_bins_settings) == False:
        return (temp_col_bins_settings, -1, -1)
    
    # Add new bin to def
    new_bin = {
        "name": new_bin_name,
        "ranges": new_bin_ranges,
    }

    temp_col_bins_settings["bins"].append(new_bin)

    new_bin_list.append([new_bin_name, get_str_from_ranges(new_bin_ranges)])
    
    return (temp_col_bins_settings, old_bin_list, new_bin_list)
     
new_bin_name = "HI"
new_bin_ranges = [[10, 20], [50, 90]]
temp_col_bins_settings = {"column": "person_age", "type": "numerical", "bins": [{"name": "Aha", "ranges": [[0, 5], [20, 40]]}, {"name": "Bha", "ranges": [[5, 20], [45, 85]]}]}

print(numeric_create_new_bin(new_bin_name, new_bin_ranges, temp_col_bins_settings))