import pandas as pd
import numpy as np

# equal width - width
# Create a sample dataframe
df = pd.DataFrame({'A': [0, 5, 11, 22, 100]})

# Define bin width
bin_width = 10

# Calculate number of bins
num_bins = int(np.ceil((df['A'].max() - df['A'].min()) / bin_width))
print(num_bins)

# Create bin edges
bin_edges = np.linspace(df['A'].min(), df['A'].max(), num_bins + 1)
print(bin_edges)

# Bin the data
df['A_binned'] = pd.cut(df['A'], bins=num_bins)

print(df.head())



# equal width - number of bins
# Create a sample dataframe
df = pd.DataFrame({'A': [0, 5, 11, 22, 100]})

# Define number of bins
num_bins = 10

# Calculate bin width
bin_width = (df['A'].max() - df['A'].min()) / num_bins

# Create bin edges
bin_edges = np.arange(df['A'].min(), df['A'].max(), bin_width)
bin_edges = np.append(bin_edges, df['A'].max())

# Bin the data
df['A_binned'] = pd.cut(df['A'], bins=bin_edges)

print(df.head())