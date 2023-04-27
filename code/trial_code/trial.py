# width width
if not isinstance(width, (int, float)):
    error = "Error: The width must be a number"
elif width <= 0:
    error = "Error: The width must be a positive number."
else:

# width num_bins
num_unique_val = len(df.loc[:, [col_bins_settings["column"]]])
if not isinstance(ew_num_bins, int) or ew_num_bins <= 0:
    error = "Error: The number of bins must be a positive integer."
elif ew_num_bins > num_unique_val:
    error = "Error: The number of bins needs to be a positive integer smaller or equal to the number of unique values in the column, which is " + str(num_unique_val) + "."
else:

# freq freq
num_samples = len(df)
if isinstance(freq, int) or freq <= 0:
    error = "Error: The frequency must be a positive integer."
elif freq > num_samples:
    error = "Error: The frequency must be smaller or equal to the total number of samples in the dataset, which is " + str(num_samples) + "."
else:

# freq num_bins
num_unique_val = len(df.loc[:, [col_bins_settings["column"]]])
if not isinstance(ef_num_bins, int) or ef_num_bins <= 0:
    error = "Error: The number of bins must be a positive integer."
elif ef_num_bins > num_unique_val:
    error = "Error: The number of bins needs to be a positive integer smaller or equal to the number of unique values in the column, which is " + str(num_unique_val) + "."
else: