# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu
import json

# Read recipe inputs
ib_settings = dataiku.Dataset("ib_settings")
ib_settings_df = ib_settings.get_dataframe()
bins_settings_data = ib_settings_df.iloc[0, 0]

bins_settings = json.loads(bins_settings_data)

print("Bins settings: " + str(bins_settings))
print("Bins settings: " + str(type(bins_settings)))

for bin_def_idx in range(len(bins_settings)):
    if bins_settings[bin_def_idx]["type"] == "numerical":
        for bin_idx in range(len(bins_settings[bin_def_idx]["bins"])):
            if isinstance(bins_settings[bin_def_idx]["bins"], list):
                for r_idx in range(len(bins_settings[bin_def_idx]["bins"][bin_idx]["ranges"])):
                    bins_settings[bin_def_idx]["bins"][bin_idx]["ranges"][r_idx][0] = float(bins_settings[bin_def_idx]["bins"][bin_idx]["ranges"][r_idx][0])
                    bins_settings[bin_def_idx]["bins"][bin_idx]["ranges"][r_idx][1] = float(bins_settings[bin_def_idx]["bins"][bin_idx]["ranges"][r_idx][1])
                

print("TYPE: " + str(type(bins_settings[0]["bins"][0]["ranges"][0][0])))
print("TYPE: " + str(bins_settings[0]["bins"][0]["ranges"][0][0]))

credit_risk_dataset_generated = dataiku.Dataset("credit_risk_dataset_generated")
df = credit_risk_dataset_generated.get_dataframe()



# Compute recipe outputs
binned_credit_risk_dataset_df = pd.DataFrame([])

# Write recipe outputs
binned_credit_risk_dataset = dataiku.Dataset("binned_credit_risk_dataset")
binned_credit_risk_dataset.write_with_schema(binned_credit_risk_dataset_df)
