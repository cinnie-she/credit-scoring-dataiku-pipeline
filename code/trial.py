# https://note.nkmk.me/en/python-pandas-cut-qcut-binning/
import pandas as pd
import numpy as np


@app.callback(
    [
        Output("auto_bin_algo_dropdown", "value"),
        Output("auto_bin_algo_dropdown", "options"),
        Output("equal_width_radio_button", "value"),
        Output("equal_width_width_input", "value"),
        Output("equal_width_num_bin_input", "value"),
        Output("equal_freq_radio_button", "value"),
        Output("equal_freq_freq_input", "value"),
        Output("equal_freq_num_bin_input", "value"),
    ],
    Input("predictor_var_ib_dropdown", "value"),
    State("bins_settings", "data"),
)
def update_auto_bin_panel_on_bin_var_change(var_to_bin, bins_settings_data):
    bins_settings_dict = json.loads(bins_settings_data)
    bins_settings_list = bins_settings_dict["variable"]
    dtype = None
    for var in bins_settings_list:
        if var["column"] == var_to_bin:
            dtype = var["type"]

    if dtype == "categorical":
        options = [
            {"label": "No Binnings", "value": "none"},
            {"label": "Equal Width", "value": "equal width"},
        ]
        return ["none", options, "width", 1, 10, "frequency", 1000, 10]
    else:
        options = [
            {"label": "No Binnings", "value": "none"},
            {"label": "Equal Width", "value": "equal width"},
            {
                "label": "Equal Frequency",
                "value": "equal frequency",
            },
        ]
        return ["none", options, "width", 1, 10, "frequency", 1000, 10]
