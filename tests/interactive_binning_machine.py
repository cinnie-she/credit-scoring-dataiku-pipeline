
class InteractiveBinningMachine:
    
    # A method to get the changes in bins settings for categoric create new bin action
    # Return 2 list for old bins and new bins info
    @staticmethod
    def get_categoric_create_new_bin_changes(new_name, bin_element_list, var_to_bin, col_bin_list):
        """_summary_

        Args:
            new_name (str): The name of the new bin input by the user
            bin_element_list (list): The list of elements to be included in the new bin input by the user
            var_to_bin (str): The name of variable that is currently binning
            col_bin_settings (list): The info each bin for the variable that is currently binning
            
        Return:
            old_bin_list (list): The info of bins before any changes by user in the form of [[old_bin_name, old_bin_element_list_str], [old_bin_name2, old_bin_element_list_str2], ...]
            new_bin_list (list): The info of bins after any changes by user in the form of [[new_bin_name, new_bin_element_list_str], [new_bin_name2, new_bin_element_list_str2], ...]
        """
        
        
