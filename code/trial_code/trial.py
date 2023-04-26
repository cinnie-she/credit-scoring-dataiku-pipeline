unique_bins = ['Bin1', 'Bin2', 'Bin3', 'Bin4']
total_count_list = [200, 300, 400, 500]
bad_count_list = [50, 100, 150, 200]
woe_list = [0.5, 1, 1.5, 2]

combined_info = tuple(zip(unique_bins, total_count_list, bad_count_list, woe_list))

sorted_combined_info = sorted(combined_info, key=lambda x: x[3], reverse=True)

sorted_unique_bins, sorted_total_count_list, sorted_bad_count_list, sorted_woe_list = zip(*sorted_combined_info)

sorted_unique_bins = list(sorted_unique_bins)
sorted_total_count_list = list(sorted_total_count_list)
sorted_bad_count_list = list(sorted_bad_count_list)
sorted_woe_list = list(sorted_woe_list)

print(sorted_unique_bins)
print(sorted_total_count_list)
print(sorted_bad_count_list)
print(sorted_woe_list)
