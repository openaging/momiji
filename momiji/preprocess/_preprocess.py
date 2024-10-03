import anndata
import pandas as pd
from pyBigWig import open as open_bw

from ._preprocess_utils import (
    add_unstructured_data,
    create_anndata_object,
    impute_missing_values,
    log_data_statistics,
    load_ensembl_metadata,
)

def bigwig_to_df(bw_files: str | list[str], dir: str = "pyaging_data") -> pd.DataFrame:
    """Convert bigWig files to a DataFrame, extracting signal data for genomic regions.

    Args:
        bw_files (str | list[str]): A list of bigWig file paths. If a single string is provided, it is converted to a list.
        dir (str, optional): The directory to deposit the downloaded file.. Defaults to "pyaging_data".
    

    Returns:
        pd.DataFrame: A DataFrame where each row represents a bigWig file and each column corresponds to a gene.
        The values in the DataFrame are the transformed signal data for each gene in each bigWig file.
    """
    
    
    # Ensure bws is a list
    if isinstance(bw_files, str):
        bw_files = [bw_files]

    # Get genomic annotation data
    genes = load_ensembl_metadata(dir, logger, indent_level=1)

    all_samples = []  # List to store signal data for each sample
    
    for bw_file in bw_files:
        # Open bigWig file
        with open_bw(bw_file) as bw:
            signal_sample = np.empty(shape=(0, 0), dtype=float)
            for i in main_tqdm(range(genes.shape[0]), indent_level=2):
                try:
                    signal = bw.stats(
                        "chr" + genes["chr"].iloc[i],
                        genes["start"].iloc[i] - 1,
                        genes["end"].iloc[i],
                        type="mean",
                        exact=True,
                    )[0]
                except:
                    signal = None

                signal_transformed = np.arcsinh(signal) if signal is not None else 0

                signal_sample = np.append(signal_sample, signal_transformed)

        # Append DataFrame for the current sample
        all_samples.append(pd.DataFrame(signal_sample[None, :], columns=genes.gene_id.tolist()))
    

    # Concatenate all sample dataframes
    df_concat = pd.concat(all_samples, ignore_index=True)

    # Add file name as index
    df_concat.index = bw_files

    return df_concat

def df_to_adata(
    df: pd.DataFrame,
    metadata_cols: list[str] = [],
    imputer_strategy: str = "knn",
) -> anndata.AnnData:
    """
    Converts a pandas DataFrame to an AnnData object with optional metadata columns and imputation strategy.

    Args:
        df (pd.DataFrame): The input data frame to be converted.
        metadata_cols (List[str], optional): List of columns in `df` to be used as metadata. Defaults to [].
        imputer_strategy (str, optional): Strategy to impute missing values. Can be "mean", "median", "most_frequent", or "knn". Defaults to "knn".

    Returns:
        anndata.AnnData: The resulting AnnData object after processing.

    Raises:
        TypeError: If the input `df` is not a pandas DataFrame.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input df must be a pandas DataFrame.")

    adata = create_anndata_object(df)

    log_data_statistics(adata.X)

    impute_missing_values(adata, imputer_strategy)

    if "X_imputed" in adata.layers:
        add_unstructured_data(adata, imputer_strategy)

    return adata
