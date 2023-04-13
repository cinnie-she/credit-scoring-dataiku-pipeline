import pandas as pd
import numpy as np
from decimal import Decimal

# A class for performing binning based on bins settings
class BinningMachine:
    # Perform equal width binning based on a specified width (for numerical column only)
    @staticmethod
    def perform_eq_width_binning_by_width(col_df, width):
        if len(col_df) == 0:
            return -1
        if not pd.api.types.is_numeric_dtype(col_df.iloc[:, 0]): # Cannot be categorical type
            return -1
        if not (isinstance(width, int) or isinstance(width, float)): # width cannot be non-numeric
            return -1
        
        min = col_df.min()
        max = col_df.max()
        num_bins = int(np.ceil((max - min) / width)) + 1
        
        bin_edges = list()
        for i in range(num_bins):
            bin_edges.append(float(Decimal(str(float(min))) + Decimal(str(width)) * i))
        
        bin_ranges = [[edge, float(Decimal(str(edge))+Decimal(str(width)))] for edge in bin_edges]
        
        binned_result = list()
        for _, row in col_df.iterrows():
            val = row.iloc[0]
            for bin_range in bin_ranges:
                if val >= bin_range[0] and val < bin_range[1]:
                    binned_result.append(f"[{bin_range[0]}, {bin_range[1]})")
                    break
        print(bin_ranges)
        print(binned_result)
        return pd.Series(binned_result)
    
    # A method to perform equal width binning based on a specified number of bins
    @staticmethod
    def perform_eq_width_binning_by_num_bins(col_df, num_bins):
        if len(col_df) == 0:
            return -1
        if not pd.api.types.is_numeric_dtype(col_df.iloc[:, 0]): # Cannot be categorical type
            return -1
        if not isinstance(num_bins, int):
            return -1
        
        min = col_df.min()
        max = col_df.max()
        width = (float(max) - float(min)) / num_bins
        add_to_last_width = Decimal(str(width * 0.01)) # to include max value
        
        bin_edges = list()
        for i in range(num_bins):
            bin_edges.append(float(Decimal(str(float(min))) + Decimal(str(width)) * i))
        
        bin_ranges = [[edge, float(Decimal(str(edge))+Decimal(str(width)))] for edge in bin_edges]
        bin_ranges[len(bin_ranges)-1][1] = float(Decimal(str(add_to_last_width)) + Decimal(str(bin_ranges[len(bin_ranges)-1][1])))
        
        binned_result = list()
        for _, row in col_df.iterrows():
            val = row.iloc[0]
            for bin_range in bin_ranges:
                if val >= bin_range[0] and val < bin_range[1]:
                    binned_result.append(f"[{bin_range[0]}, {bin_range[1]})")
                    break
        print(bin_ranges)
        print(binned_result)
        return pd.Series(binned_result)
    
    # A method to perform equal frequency binning based on a specified frequency
    # @staticmethod
    # def perform_eq_freq_binning_by_freq(col_df, freq):
    #     if len(col_df) == 0:
    #         return -1
    #     if not pd.api.types.is_numeric_dtype(col_df.iloc[:, 0]): # Cannot be categorical type
    #         return -1
    #     if not isinstance(freq, int) or freq <= 0 or freq > len(col_df):
    #         return -1
        
        
    #     num_bins = int(np.ceil(len(col_df)/freq))
    #     print(num_bins)
    #     if num_bins == 1: # i.e., no binnings
    #         print(type(col_df.iloc[:, 0]))
    #         return col_df.iloc[:, 0]
        
    #     # bin the col_df
    #     interval_li = pd.qcut(col_df.iloc[:, 0], num_bins, duplicates="drop").to_list()
    #     print(interval_li)
        
    #     # convert to the format we want
    #     binned_result = list()
    #     for idx in range(len(interval_li)):
    #         binned_result.append(f"[{interval_li[idx].left}, {interval_li[idx].right})")
        
    #     print(binned_result)
    #     return pd.Series(binned_result)
    
# df = pd.DataFrame([7,0, 3, 5, 101, 11, 18, 8, 9])
# df = pd.DataFrame([1, 1])
# df = pd.DataFrame([1,1,1,1,1,1,1])
# print(BinningMachine.perform_eq_freq_binning_by_freq(df, 2))








# # Get the indexes that sort col_df in ascending order
#         df_order_li = col_df.iloc[:, 0].argsort().tolist()
#         print(df_order_li)
        
#         # Calculate number of bins
#         # num_bins = int(np.ceil(len(col_df) / freq))
#         # print(num_bins)
        
#         # Get list of bin lower boundaries
#         low_bounds = [df_order_li[idx] for idx in range(len(df_order_li)) if idx % freq == 0]
#         print(low_bounds)
        
#         # Prepare bin ranges
#         bin_ranges = list()
#         for idx in range(len(low_bounds)):
#             if idx != len(low_bounds) - 1:
#                 bin_ranges.append([float(col_df.iloc[low_bounds[idx]]), float(col_df.iloc[low_bounds[idx+1]])])
#             else:
#                 bin_ranges.append([float(col_df.iloc[low_bounds[idx]]), float(col_df.iloc[low_bounds[idx]])+1])
#         print(bin_ranges)
        
#         curr = 0
#         for _, row in col_df.iterrows():
#             val = row.iloc[0]
            