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
    # 고신뢰 / 저신뢰 샘플을 분류하여 집계 비교용 태그 칼럼을 추가

    def is_high_confidence(row):
        return(
            row['score_quality'] == 'A' and
            pd.isna(row['시험일']) and
            pd.isna(row['이름']) and str(row['이름']).strip() == "" or
            pd.isna(row['나이'])
        )
    
    def is_low_condfidence(row):
        return(
            row['score_quality'] == 'C' and
            pd.isna(row['시험일']) and
            (
                pd.isna(row['이름']) or
                pd.isna(row['나이']) or
                pd.isna(row['성별']) or
                pd.isna(row['비고'])
            )
        )
    
    tags = []
    for _, row in df.iterrows():
        if is_high_confidence(row):
            tags.append('고신뢰')
        elif is_low_condfidence(row):
            tags.append('저신뢰')
        else:
            tags.append('중간')

    df['신뢰도_샘플_분류'] = tags
    return df

