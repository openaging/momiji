import os
import anndata
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer, SimpleImputer
from urllib.request import urlretrieve


def my_func(x):
    """Converts a Numpy array with string elements into an integer Numpy array.

    Args:
        A Numpy array with string elements (e.g., my_array)

    Returns:
        A Numpy array with int64 elements

    Example:
        >>> import mypackageabc as my
        >>> my.my_func(my.my_array)

    Note:
        This is very simple function only for the demonstration

    """
    return x.astype(np.int64)


def create_anndata_object(df: pd.DataFrame) -> anndata.AnnData:
    """
    Creates an AnnData object from a pandas DataFrame, removing columns that contain only missing values.

    Args:
        df (pd.DataFrame): The input DataFrame to be converted.

    Returns:
        anndata.AnnData: The created AnnData object with original data stored in layers.

    Raises:
        ValueError: If the variable names (column names) are not unique.
    """
    na_column_mask = df.isna().all()

    if na_column_mask.sum() > 0:
        columns_with_nas = df.columns[na_column_mask]
        df = df.drop(columns=columns_with_nas)

    X = df.values
    obs_names = df.index.astype(str)
    var_names = df.columns.astype(str)

    if len(np.unique(var_names)) != len(var_names):
        raise ValueError("Column names (variable names) must be unique.")

    obs = pd.DataFrame(index=obs_names)
    var = pd.DataFrame(index=var_names)
    adata = anndata.AnnData(X=X, obs=obs, var=var, layers={"X_original": X})

    return adata


def log_data_statistics(X: np.ndarray) -> None:
    """
    Logs statistics of the data matrix including the number of observations, features, and the percentage of missing values.

    Args:
        X (np.ndarray): The data matrix.

    Returns:
        None
    """
    n_obs, n_features = X.shape
    total_nas = np.isnan(X).sum()
    percent_nas = 100 * total_nas / (n_obs * n_features)
    print(f"Number of observations: {n_obs}")
    print(f"Number of features: {n_features}")
    print(f"Total missing values: {total_nas}")
    print(f"Percentage of missing values: {percent_nas:.2f}%")


def impute_missing_values(adata: anndata.AnnData, strategy: str) -> None:
    """
    Imputes missing values in the AnnData object using the specified strategy.

    Args:
        adata (anndata.AnnData): The AnnData object containing the data to be imputed.
        strategy (str): The imputation strategy to use. Options are "mean", "median", "constant", or "knn".

    Returns:
        None

    Raises:
        ValueError: If the provided imputation strategy is not supported.
    """
    adata.var["percent_na"] = np.isnan(adata.X).sum(axis=0) / adata.X.shape[0]

    if adata.var["percent_na"].sum() != 0:
        imputers = {
            "mean": SimpleImputer(strategy="mean", keep_empty_features=True),
            "median": SimpleImputer(
                strategy="median", keep_empty_features=True
            ),
            "constant": SimpleImputer(
                strategy="constant", fill_value=0, keep_empty_features=True
            ),
            "knn": KNNImputer(),
        }

        imputer = imputers.get(strategy)
        if not imputer:
            raise ValueError(f"Invalid imputer strategy: {strategy}")
        adata.X = imputer.fit_transform(adata.X)
        adata.layers["X_imputed"] = adata.X


def add_unstructured_data(
    adata: anndata.AnnData, imputer_strategy: str
) -> None:
    """
    Adds unstructured data to the AnnData object, specifically the imputation strategy used.

    Args:
        adata (anndata.AnnData): The AnnData object to which unstructured data will be added.
        imputer_strategy (str): The imputation strategy used.

    Returns:
        None
    """
    adata.uns["imputer_strategy"] = imputer_strategy


def load_ensembl_metadata(dir: str) -> pd.DataFrame:
    """Load and filter Ensembl genome metadata specific to Homo sapiens.

    This function downloads the Ensembl gene metadata for Homo sapiens from a predefined URL and
    filters it to include only the genes located on specified chromosomes.

    Args:
        dir (str):  The directory to deposit the downloaded file.

    Returns:
        pd.DataFrame:
            A DataFrame containing filtered gene metadata from Ensembl. Rows correspond to genes, indexed
            by their Ensembl gene IDs, and columns include various gene attributes.
    """

    url = "https://pyaging.s3.amazonaws.com/supporting_files/Ensembl-105-EnsDb-for-Homo-sapiens-genes.csv"
    file_path = os.path.join(dir,url.split("/")['-1'])
    if not os.path.exists(dir):
        os.makedirs(dir,exists_ok=True)
    
    if not os.path.exists(file_path):
        urlretrieve(url,file_path)

    # Define chromosomes of interest
    chromosomes = [
        "1",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "2",
        "20",
        "21",
        "22",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "X",
    ]

    # Read and filter the gene data
    genes_path = os.path.join(dir, "Ensembl-105-EnsDb-for-Homo-sapiens-genes.csv")
    genes = pd.read_csv(genes_path)
    genes = genes[genes["chr"].apply(lambda x: x in chromosomes)]
    genes.index = genes.gene_id
    return genes
