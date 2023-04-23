

ranges = ((10, 20),)
    
def decode(ranges):
    if len(ranges) == 0:
        return []
    numeric_list = list()  # initialization
    print(len(ranges))
    for numeric_info in ranges:
        single_def_list = list()
        print(f"numeric_info: {numeric_info}")
        a_range = [numeric_info[0], numeric_info[1]]
        # The 2 bounds are valid, now check if any overlapping with previously saved data
        has_column_overlap = False
        for def_idx, saved_def in enumerate(numeric_list):
            print(f"def_idx: {def_idx}, saved_def: {saved_def}")
            has_column_overlap = True
            has_range_overlap = False
            overlapped_def_range_idxes = list()
            # Merge range to element list
            for def_range_idx, def_range in enumerate(saved_def):
                if len(overlapped_def_range_idxes) != 0:
                    a_range = numeric_list[def_idx][overlapped_def_range_idxes[0]]

                if a_range[0] <= def_range[0] and a_range[1] >= def_range[1]:
                    has_range_overlap = True
                    numeric_list[def_idx][def_range_idx] = [
                        a_range[0], a_range[1]]
                    overlapped_def_range_idxes.insert(0, def_range_idx)
                elif def_range[0] <= a_range[0] and def_range[1] >= a_range[1]:
                    has_range_overlap = True
                elif a_range[0] <= def_range[0] and a_range[1] >= def_range[0] and a_range[1] <= def_range[1]:
                    has_range_overlap = True
                    numeric_list[def_idx][def_range_idx] = [
                        a_range[0], def_range[1]]
                    overlapped_def_range_idxes.insert(0, def_range_idx)
                elif a_range[0] >= def_range[0] and a_range[0] <= def_range[1] and a_range[1] >= def_range[1]:
                    has_range_overlap = True
                    numeric_list[def_idx][def_range_idx] = [
                        def_range[0], a_range[1]]
                    overlapped_def_range_idxes.insert(0, def_range_idx)
            if len(overlapped_def_range_idxes) != 0:
                del overlapped_def_range_idxes[0]
                for i in sorted(overlapped_def_range_idxes, reverse=True):
                    del numeric_list[def_idx][i]
            if has_range_overlap == False:
                numeric_list[def_idx].append(a_range)
                print("hi2")
                print(numeric_list)
            break
        if has_column_overlap == False:
            single_def_list = [a_range]
            numeric_list.append(single_def_list)
            print("Hi")
            print(numeric_list)
    
    return numeric_list[0]

print(decode(ranges))