import pandas as pd

def load_raw_scores(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df