def categoric_rename_bin(selected_bin_name, new_bin_name, temp_col_bins_settings):
        if selected_bin_name == new_bin_name:
            return (temp_col_bins_settings, [], [])
        
        old_bin_list = list()
        new_bin_list = list()
        
        for idx in range(len(temp_col_bins_settings["bins"])):
            if temp_col_bins_settings["bins"][idx]["name"] == selected_bin_name:
                old_bin_list.append([temp_col_bins_settings["bins"][idx]["name"], str(temp_col_bins_settings["bins"][idx]["elements"])])
                temp_col_bins_settings["bins"][idx]["name"] = new_bin_name
                new_bin_list.append([temp_col_bins_settings["bins"][idx]["name"], str(temp_col_bins_settings["bins"][idx]["elements"])])
                break
                
        return (temp_col_bins_settings, old_bin_list, new_bin_list)
    
temp_col_bins_settings = {"column": "loan_grade", "type": "categorical", "bins": [{"name": "A", "elements": ['A']}, {"name": "B", "elements": ['B']}, {"name": "C", "elements": ['C']}]}
selected_bin_name = "B"
new_bin_name = "HI"

print(categoric_rename_bin(selected_bin_name, new_bin_name, temp_col_bins_settings))
