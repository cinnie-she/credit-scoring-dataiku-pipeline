if triggered[0]['prop_id'] == "numeric_adjust_cutpoints_panel_submit_button.n_clicks":
        temp_col_bins_settings = json.loads(temp_col_bins_settings_data)
        
        ranges = tuple(zip(numeric_adjust_cutpoints_lower, numeric_adjust_cutpoints_upper))

        isValid = validate_numerical_bounds(ranges)
        
        if isValid == False:
            raise PreventUpdate
        else:
            ranges = decode_ib_ranges(ranges)
            new_settings, _, __ = InteractiveBinningMachine.get_numeric_adjust_cutpoints(selected_bin_name=click_data["points"][0]["x"], new_bin_name=numeric_adjust_cutpoints_panel_new_bin_name_input, new_bin_ranges=ranges, temp_col_bins_settings=temp_col_bins_settings)

        def_li, binned_series = BinningMachine.perform_binning_on_col(
        df.loc[:, [new_settings["column"]]], new_settings)
        temp_df = df.copy()
        temp_df['binned_col'] = binned_series.values
        
        return [json.dumps(new_settings), json.dumps(temp_df.to_dict())]
    