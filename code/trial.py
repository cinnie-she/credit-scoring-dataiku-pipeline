def generate_categoric_old_div_children(old_bin_list=[], dtype=None):
    if dtype == None: 
        return []
    if len(old_bin_list) == 0:
        return []
    
    if dtype == "categorical":
        s = "Element"
    else:
        s = "Range"
    
    idx = 1
    old_element_list = list()
    for old_bin in old_bin_list:
        old_element_list.append(
            [[
                [
                [["(" + str(idx) + ") "]],
                [[["Old Bin Name: " + old_bin[0]], ["Old Bin " + s + "(s): " + old_bin[1]]]]
            ]]]
        )
        idx += 1
        
    return old_element_list


def generate_categoric_new_div_children(new_bin_list=[], dtype=None):
    if dtype == None: 
        return []
    if len(new_bin_list) == 0:
        return []
    
    if dtype == "categorical":
        s = "Element"
    else:
        s = "Range"
    
    idx = 1
    new_element_list = list()
    for new_bin in new_bin_list:
        new_element_list.append(
            [[
                [[["(" + str(idx) + ") "]],
                [[["New Bin Name: " + new_bin[0]], ["New Bin "+ s + "(s): " + new_bin[1]]],]]]
            ],
        )
        idx += 1
    
    return new_element_list

def generate_bin_changes_div_children(old_bin_list=[], new_bin_list=[], dtype=None):
    if dtype == None:
        return []
    
    children = list()
    
    children.append(["Preview Changes:"])
    
    if len(old_bin_list) != 0:
        old_element_list = generate_categoric_old_div_children(old_bin_list=old_bin_list, dtype=dtype)
        children.append(["Old Bin(s):"])
        children.append([old_element_list])
    
    if len(new_bin_list) != 0:
        children.append(["Will be changed to:"])
        new_element_list = generate_categoric_new_div_children(new_bin_list, dtype=dtype)
        children.append([new_element_list])
    else:
        children.append(["No changes."])

    return children

print(generate_bin_changes_div_children(old_bin_list=[], new_bin_list=[["Rent or Mortgage", "['RENT', 'MORTGAGE']"]], dtype="categorical"))