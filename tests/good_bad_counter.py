# A class for counting the number of good and bad samples/population in the column
class GoodBadCounter:
    # A method to get the number of sample bad, sample indeterminate, sample good, population good, and population bad
    @staticmethod
    def get_statistics(dframe, good_bad_def):
        new_dframe, sample_bad_count = GoodBadCounter.count_sample_bad(
            dframe, good_bad_def["bad"])
        sample_indeterminate_count = GoodBadCounter.count_sample_indeterminate(
            new_dframe, good_bad_def["indeterminate"])
        sample_good_count = GoodBadCounter.count_sample_good(
            dframe, sample_bad_count, sample_indeterminate_count)
        good_weight = good_bad_def["good"]["weight"]
        bad_weight = good_bad_def["bad"]["weight"]
        population_good_count = GoodBadCounter.get_population_good(
            sample_good_count, good_weight)
        population_bad_count = GoodBadCounter.get_population_bad(
            sample_bad_count, bad_weight)
        return (sample_bad_count, sample_indeterminate_count, sample_good_count, good_weight, bad_weight, population_good_count, population_bad_count)

    # A method to count the number of sample bad
    @staticmethod
    def count_sample_bad(dframe, bad_defs):
        bad_count = 0
        for bad_numeric_def in bad_defs["numerical"]:
            # count number of rows if dframe row is in bad_numeric_def range, and add to bad_count
            for a_range in bad_numeric_def["ranges"]:
                bad_count += len(dframe[(dframe[bad_numeric_def["column"]] >= a_range[0]) & (
                    dframe[bad_numeric_def["column"]] < a_range[1])])
                # delete rows if dframe row is in bad_numeric_def range
                dframe = dframe.drop(dframe[(dframe[bad_numeric_def["column"]] >= a_range[0]) & (
                    dframe[bad_numeric_def["column"]] < a_range[1])].index)

        for bad_categoric_def in bad_defs["categorical"]:
            # count number of rows if dframe row is having any one of the bad_categoric_def elements value
            for element in bad_categoric_def["elements"]:
                bad_count += len(dframe[(dframe[bad_categoric_def["column"]] == element)])
                # delete rows if dframe row has value 'element'
                dframe = dframe.drop(
                    dframe[(dframe[bad_categoric_def["column"]] == element)].index)

        return (dframe, bad_count)

    # A method to count the number of sample indeterminate
    @staticmethod
    def count_sample_indeterminate(dframe, indeterminate_defs):
        indeterminate_count = 0
        for indeterminate_numeric_def in indeterminate_defs["numerical"]:
            # count number of rows if dframe row is in indeterminate_numeric_def range, and add to indeterminate_count
            for a_range in indeterminate_numeric_def["ranges"]:
                indeterminate_count += len(dframe[(dframe[indeterminate_numeric_def["column"]] >= a_range[0]) & (
                    dframe[indeterminate_numeric_def["column"]] < a_range[1])])
                # delete rows if dframe row is in indeterminate_numeric_def range
                dframe = dframe.drop(dframe[(dframe[indeterminate_numeric_def["column"]] >= a_range[0]) & (
                    dframe[indeterminate_numeric_def["column"]] < a_range[1])].index)

        for indeterminate_categoric_def in indeterminate_defs["categorical"]:
            # count number of rows if dframe row is having any one of the indeterminate_categoric_def elements value
            for element in indeterminate_categoric_def["elements"]:
                indeterminate_count += len(
                    dframe[(dframe[indeterminate_categoric_def["column"]] == element)])
                # delete rows if dframe row has value 'element'
                dframe = dframe.drop(
                    dframe[(dframe[indeterminate_categoric_def["column"]] == element)].index)

        return indeterminate_count

    # A method to count the number of sample good
    @staticmethod
    def count_sample_good(dframe, sample_bad_count, sample_indeterminate_count):
        return (len(dframe) - sample_bad_count - sample_indeterminate_count)

    # A method to count the number of population good
    @staticmethod
    def get_population_good(sample_good_count, good_weight):
        return sample_good_count * good_weight

    # A method to count the number of population bad
    @staticmethod
    def get_population_bad(sample_bad_count, bad_weight):
        return sample_bad_count * bad_weight