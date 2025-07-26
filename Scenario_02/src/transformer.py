import pandas as pd
from src.cleaner import clean_score

def transform_scores(df: pd.DataFrame, score_col: str = '점수') -> pd.DataFrame:
    cleaned_scores = []
    qualities = []

    for score in df[score_col]:
        cleaned_score, quality = clean_score(score)
        cleaned_scores.append(cleaned_score)
        qualities.append(quality)

    df['정제된_점수'] = cleaned_scores
    df['score_quality'] = qualities
    df['is_score_clean'] = df['score_quality'] == 'A'

    return df