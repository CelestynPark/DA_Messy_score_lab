import pandas as pd

def compute_quality_stats(df: pd.DataFrame) -> pd.DataFrame:
    summary = df.groupby('score_quality').agg(
        인원수=('정제된_점수', 'count'),
        평균점수=('정제된_점수', 'mean')
    ).reindex(['A', 'B', 'C'])

    summary['C_등급_비율(%)'] = (summary.loc['C', '인원수'] / len(df)) * 100 if 'C' in summary.index else 0.0
    return summary