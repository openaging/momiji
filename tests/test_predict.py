import unittest
import torch
import anndata
from momiji.predict.predict import Predictor

class TestPredictor(unittest.TestCase):
    def setUp(self):
        # Create a dummy model and anndata.AnnData object for testing
        self.model = torch.nn.Linear(10, 1)
        self.adata = anndata.AnnData(X=torch.randn(100, 10))

    def test_check_features_in_adata(self):
        predictor = Predictor(self.adata, self.model)
        adata_with_features = predictor.check_features_in_adata(self.adata, self.model)

        # Assert that the missing features are correctly handled
        self.assertIn("clock_name_percent_na", adata_with_features.uns)
        self.assertIn("clock_name_missing_features", adata_with_features.uns)
        self.assertIn(f"X_{self.model.metadata['clock_name']}", adata_with_features.obsm)

    def test_forward(self):
        predictor = Predictor(self.adata, self.model)
        predictions = predictor.forward(self.adata)

        # Assert that the predictions have the correct shape
        self.assertEqual(predictions.shape, torch.Size([self.adata.n_obs, 1]))

if __name__ == "__main__":
    unittest.main()
