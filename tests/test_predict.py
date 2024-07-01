import tempfile
from urllib.request import urlopen

import pandas as pd
import pytest
import torch

from momiji.predict.predict import Predictor
from momiji.preprocess._preprocess import df_to_adata


@pytest.fixture(scope="module")
def setup():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a dummy model and anndata.AnnData object for testing
        clock_name = "OcampoATAC1"
        clock_name = clock_name.lower()
        url = f"https://pyaging.s3.amazonaws.com/clocks/weights0.1.0/{clock_name}.pt"
        file_path = f"{temp_dir}/{clock_name}.pt"
        data = urlopen(url).read()
        with open(file_path, "wb") as f:
            f.write(data)

        model = torch.load(file_path)
        model = model.float()  # Cast model weights to float32

        # Create a dummy DataFrame
        df = pd.read_pickle("tests/GSE193140.pkl")
        adata = df_to_adata(df)

        yield adata, model


def test_forward_01(setup):
    adata, model = setup
    predictor = Predictor(adata, model)
    predictions = predictor.forward(adata)

    # Assert that the predictions have the correct shape
    assert predictions.shape == torch.Size([adata.n_obs, 1])


def test_forward_02(setup):
    adata, model = setup
    predictor = Predictor(adata, model)
    predictions = predictor.forward(adata)

    # Assert that the predictions do not have an incorrect shape
    assert predictions.shape != torch.Size([adata.n_obs, 0])
