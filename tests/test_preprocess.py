import anndata
import numpy as np
import pandas as pd

from momiji.preprocess._preprocess import df_to_adata


def test_df_to_adata():
    df = pd.read_pickle("tests/GSE193140.pkl")

    # Convert the DataFrame to an anndata.AnnData object
    adata = df_to_adata(df)

    # Assert that the adata object is of type anndata.AnnData
    assert isinstance(adata, anndata.AnnData)

    # Assert that the adata object has the correct shape
    assert adata.X.shape == (157, 80400)

    # Assert that the data in adata matches the original DataFrame
    np.testing.assert_array_equal(adata.X, df.values)

    # Assert that adata.obs and adata.var have correct dimensions
    assert adata.obs.shape[0] == df.shape[0]
    assert adata.var.shape[0] == df.shape[1]

    # Check that the number of elements in adata.X is correct
    assert adata.X.size == df.size

    # Optionally, check some specific values in adata to ensure correctness
    assert adata.X[0, 0] == df.iloc[0, 0]
    assert adata.X[-1, -1] == df.iloc[-1, -1]

    # Check that the column and row names are correctly set
    assert list(adata.var_names) == list(df.columns)
    assert list(adata.obs_names) == list(df.index)
