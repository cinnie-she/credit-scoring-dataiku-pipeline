@app.callback(
    Output("mixed_chart", "figure"),
    [
        Input("temp_binned_col", "data"),
        Input("mixed_chart", "clickData"),  
        Input("mixed_chart", "selectedData"),   
    ],
    [
        State("good_bad_def", "data"),
        State("auto_bin_algo_dropdown", "value"),
        State("equal_width_radio_button", "value"),
        State("equal_width_width_input", "value"),
        State("equal_width_num_bin_input", "value"),
        State("equal_freq_radio_button", "value"),
        State("equal_freq_freq_input", "value"),
        State("equal_freq_num_bin_input", "value"),
    ],
)
def save_temp_chart_info(temp_binned_col_data, click_data, selected_data, good_bad_def_data, auto_bin_algo, equal_width_method, width, ew_num_bins, equal_freq_method, freq, ef_num_bins):
    triggered = dash.callback_context.triggered
    
    temp_binned_col_dict = json.loads(temp_binned_col_data)
    temp_df = pd.DataFrame(temp_binned_col_dict)

    good_bad_def = json.loads(good_bad_def_data)

    unique_bins = sorted(temp_df['binned_col'].unique().tolist())
    total_count_list = get_list_of_total_count(
        temp_df, 'binned_col', unique_bins, good_bad_def)
    bad_count_list = get_list_of_bad_count(
        temp_df,
        'binned_col',
        unique_bins,
        good_bad_def,
    )
    woe_list = get_list_of_woe(
        temp_df, 'binned_col', unique_bins, good_bad_def)

    combined_info = tuple(
        zip(unique_bins, total_count_list, bad_count_list, woe_list))

    sorted_combined_info = sorted(
        combined_info, key=lambda x: x[3] if x[3] is not None else float('-inf'), reverse=True)

    sorted_unique_bins, sorted_total_count_list, sorted_bad_count_list, sorted_woe_list = zip(
        *sorted_combined_info)

    sorted_unique_bins = list(sorted_unique_bins)
    sorted_total_count_list = list(sorted_total_count_list)
    sorted_bad_count_list = list(sorted_bad_count_list)
    sorted_woe_list = list(sorted_woe_list)

    temp_chart_info = {
        "unique_bins": sorted_unique_bins,
        "total_count_list": sorted_total_count_list,
        "bad_count_list": sorted_bad_count_list,
        "woe_list": sorted_woe_list,
    }
    
    clicked_bar_index = None
    selected_bars_index_set = set()

    if click_data is not None and click_data["points"][0]["curveNumber"] != 2:
        clicked_bar_index = click_data["points"][0]["pointIndex"]

    if selected_data is not None:
        for point in selected_data['points']:
            if point['curveNumber'] != 2:
                selected_bars_index_set.add(point['pointIndex'])

    if triggered[0]['prop_id'] == 'temp_binned_col.data' or (click_data is not None and click_data["points"][0]["curveNumber"] == 2):
        clicked_bar_index = None
        selected_bars_index_set = None
    
    return generate_mixed_chart_fig(unique_bins=temp_chart_info['unique_bins'], total_count_list=temp_chart_info['total_count_list'], bad_count_list=temp_chart_info['bad_count_list'], woe_list=temp_chart_info['woe_list'], clicked_bar_index=clicked_bar_index, selected_bars_index_set=selected_bars_index_set)