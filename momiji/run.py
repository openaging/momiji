from urllib.request import urlretrieve
import pandas as pd
import torch
from predict import Predictor
from preprocess import df_to_adata

df = pd.read_pickle("GSE193140.pkl")
adata = df_to_adata(df)


clock_name = "OcampoATAC1"
clock_name = clock_name.lower()
url = f"https://pyaging.s3.amazonaws.com/clocks/weights0.1.0/{clock_name}.pt"
file_path = f"{clock_name}.pt"
urlretrieve(url, file_path)

model = torch.load(file_path)
model.base_m
"""
Traceback (most recent call last):
  File "/app/momiji/run.py", line 18, in <module>
    model.base_m
  File "/usr/local/lib/python3.10/site-packages/torch/nn/modules/module.py", line 1709, in __getattr__
    raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
AttributeError: 'OcampoATAC1' object has no attribute 'base_m'
"""

predictor = Predictor(adata, model, batch_size=1024)
preds = predictor(adata)

