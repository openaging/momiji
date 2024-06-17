import unittest
from urllib.request import urlretrieve

import pandas as pd
import pyaging as pya
import torch

from momiji.predict.predict import Predictor


class TestPredictor(unittest.TestCase):
    def setUp(self):
        # Create a dummy model and anndata.AnnData object for testing
        clock_name = "OcampoATAC1"
        clock_name = clock_name.lower()
        url = f"https://pyaging.s3.amazonaws.com/clocks/weights0.1.0/{clock_name}.pt"
        file_path = f"{clock_name}.pt"
        urlretrieve(url, file_path)

        self.model = torch.load(file_path)

        pya.data.download_example_data("GSE193140")
        df = pd.read_pickle("pyaging_data/GSE193140.pkl")
        self.adata = pya.preprocess.df_to_adata(df)

    """
    def test_check_features_in_adata(self):
        predictor = Predictor(self.adata, self.model)
        adata_with_features = predictor.check_features_in_adata(self.adata, self.model)

        # Assert that the missing features are correctly handled
        self.assertIn("clock_name_percent_na", adata_with_features.uns)
        self.assertIn("clock_name_missing_features", adata_with_features.uns)
        self.assertIn(
            f"X_{self.model.metadata['clock_name']}", adata_with_features.obsm
        )
    """

    def test_forward(self):
        predictor = Predictor(self.adata, self.model)
        predictions = predictor.forward(self.adata)

        # Assert that the predictions have the correct shape
        self.assertEqual(predictions.shape, torch.Size([self.adata.n_obs, 1]))


if __name__ == "__main__":
    unittest.main()
