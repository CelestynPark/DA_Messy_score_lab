import pandas as pd
import re

def detect_suspicious_cases(df: pd.DataFrame) -> pd.DataFrame:
    def is_retake_note(note: str) -> bool:
        if pd.isna(note):
            return False
        note = note.lower()
        patterns = ["재응시", "재시험", "retake", "re-take", "retook"]
        return any(p in note for p in patterns)

    df["is_retake_candidate"] = df["비고"].apply(is_retake_note)

    cond_low_quality = df["score_quality"] == "C"
    cond_invalid_score = (df["정제된_점수"] > 100) | (df["정제된_점수"] <= 0)
    cond_retake_note = df["is_retake_candidate"] == True

    suspicious_df = df[cond_low_quality | cond_invalid_score | cond_retake_note].copy()
    return suspicious_df


def compare_sample_quality(df: pd.DataFrame) -> pd.DataFrame:
    pass # TODO: Implement the function to classify samples into high and low confidence categories