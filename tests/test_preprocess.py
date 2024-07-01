import pandas as pd

from momiji.preprocess._preprocess import df_to_adata


def test_df_to_adata():
    # Create a dummy DataFrame
    df = pd.DataFrame(
        {
            "gene1": [1, 2, 3, 4, 5],
            "gene2": [6, 7, 8, 9, 10],
            "gene3": [11, 12, 13, 14, 15],
        },
        index_names=[
            "sample_1",
            "sample_2",
            "sample_3",
            "sample_4",
            "sample_5",
        ],
    )

    # Convert the DataFrame to an anndata.AnnData object
    adata = df_to_adata(df)

    # Assert that the adata object has the correct shape
    assert adata.X.shape == (5, 3)
