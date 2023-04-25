# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Read recipe inputs
binned_credit_risk_dataset = dataiku.Dataset("binned_credit_risk_dataset")
df = binned_credit_risk_dataset.get_dataframe()

col_li = list(df.columns)

idx_to_remove = list()
for idx in range(len(col_li)):
    if "_binned" not in col_li[idx]:
        idx_to_remove.append(idx)

for idx in sorted(idx_to_remove, reverse=True):
    del col_li[idx]
    
col_li.append("loan_status")
    
binned_credit_risk_dataset_prepared_df = df.loc[:, col_li] 

# Write recipe outputs
binned_credit_risk_dataset_prepared = dataiku.Dataset("binned_credit_risk_dataset_prepared")
binned_credit_risk_dataset_prepared.write_with_schema(binned_credit_risk_dataset_prepared_df)
