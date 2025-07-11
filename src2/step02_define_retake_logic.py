import pandas as pd
import os
from rules.retake_keywords import RETAKE_KEYWORDS

def determine_retake(note: str) -> str:
    if pd.isna(note):
        return "N"
    
    note_lower = str(note).strip().lower()
    
    if note_lower in ["", ".", "없음", "null"]:
        return "N"
    
    for keyword in RETAKE_KEYWORDS:
        if keyword.lower() in note_lower:
            return "Y"
    
    return "N"

def add_retake_column(csv_path: str, save_path: str = None) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["재응시여부"] = df["비고"].apply(determine_retake)
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_csv(save_path, index=False)
    
    return df
