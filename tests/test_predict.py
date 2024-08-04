import pandas as pd
import pytest
import torch

from momiji.models.model import MyModel
from momiji.predict.predict import Predictor
from momiji.preprocess._preprocess import df_to_adata


@pytest.fixture(scope="module")
def setup():
    # Define the clock name
    clock_name = "OcampoATAC1"

    # Load the data
    df = pd.read_pickle("tests/GSE193140.pkl")
    adata = df_to_adata(df)

    features = adata.var.index.values
    model = MyModel(80400, 1, clock_name, features)
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
