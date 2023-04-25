# When user change the variable to be binned
# 1. Update auto bin panel
#   - Get from bins_settings the binning method of that variable
#   - If it is auto-bin/none, change to auto bin panel with it
#   - Else if it is custom binning, change auto bin panel to no_binning
# 2. Update mixed chart
#   - Based on what we calculated in (4)
#   - Update the bar charts with all bin counts
#   - Update the line chart with all WOE
# 3. Update stat table (before)
#   - Update it to None
# 4. Update stat table (after)
#   - Get from bins_settings the binning method of that variable
#   - Extract the column from original dataset
#   - Bin the column based on the binning method to obtain a binned column
#   - Based on the binned column, get a dataframe with each unique bins
#   - For each bin, compute sample good count, bad count, and indeterminate count
#   - For each bin, compute population good count, population bad count, and total population count
#   - For each bin, compute the good%, bad%, and total%
#   - For each bin, compute good/bad Odds, WOE, and MC
#   - Get the total population good, total population bad, good/bad Odds, total population, and Info value
#   - Create a dataframe for all these numbers calculated, and update data table UI


# When user clicked on the Refresh button on auto bin panel
#   - Get the variable currently binning
#   - Extract the column from original dataset
#   - Get the auto bin method from the auto bin panel
#   - Bin the column based on auto bin method
# 1. Show/Update mixed chart
#   - Based on what we calculated in (4)
#   - Update the bar charts with all bin counts
#   - Update the line chart with all WOE
# 2. Show/Update stat table (before)
#   - Use the df from stat table (after) as its value
# 3. Show/Update stat table (after)
#   - Based on the binned column, get a dataframe with each unique bins
#   - For each bin, compute sample good count, bad count, and indeterminate count
#   - For each bin, compute population good count, population bad count, and total population count
#   - For each bin, compute the good%, bad%, and total%
#   - For each bin, compute good/bad Odds, WOE, and MC
#   - Get the total population good, total population bad, good/bad Odds, total population, and Info value
#   - Create a dataframe for all these numbers calculated, and update data table UI
# 4. Save a temp_bins_settings


# When user click on a bar on the mixed chart
# 1. Update bin information
#   - Check if the variable is numerical or categorical
#   - If numerical:
#       -> Show the bin name, bin good & bad count, and list of ranges of the bin
#   - If categorical:
#       -> Show the bin name, bin good & bad count, and elements of the bin


"""
Interactive Binning features:
1. Split bin (and Change Bin Boundaries)
    - numerical
        -> The user clicks on the bar representing the bin
        -> The interface shows the list of ranges of the bin
        -> The interface shows another section, allow user to dynamically add/remove ranges to split the bin
        -> The user clicks the 'split' button
        -> The interface validate if all ranges specified by the users are within the ranges of the bin
        -> If it is valid, 
            * the interface based on the user-specified ranges, and the temp_bins_settings, calculate & update stat tables and chart
            * the interface update the value of temp_bins_settings
        -> Else if it is not valid,
            * the interface shows an error message
    - categorical
        -> The user clicks on the bar representing the bin
        -> The interface shows multi-value dropdown, with no initial value, with options including all elements of the bin
        -> The user can choose one or more elements
        -> The user clicks the 'split' button
        -> The interface based on the dropdown values, and the temp_bins_settings, calculate & update stat tables and chart
        -> The interface update the value of temp_bins_settings
2. Merge bin
    - numerical
        -> The user uses the select tool to select multiple bar(s) representing bins
        -> The interface shows the bin name, bin good & bad count, and list of ranges of each bin
        -> The user clicks the 'merge' button
        -> The interface based on the selected bins, and the temp_bins_settings, calculate & update stat tables and chart
        -> The interface update the vlaue of temp_bins_settings
    - categorical
        -> The user uses the select tool to select multiple bar(s) representing bins
        -> The interface shows the bin name, bin good & bad count, and elements of each bins
        -> The user clicks the 'merge' button
        -> The interface based on the selected bins, and the temp_bins_settings, calculate & update stat tables and chart
        -> The interface update the vlaue of temp_bins_settings
3. Rename bin
"""
