import pandas as pd

from app.config import POKEMON_PRODUCT_IDS_PARQUET

def see_all_ids(parquet_file):
    df = pd.read_parquet(parquet_file)
    return df



