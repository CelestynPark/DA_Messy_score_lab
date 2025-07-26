import pandas as pd

def flag_suspicious_profiles(df, name_col='이름', age_col='나이', score_col='점수', date_col='시험일_정제'):
    conditions = (
        df[date_col].isna() &
        df[score_col].notna() &
        (df[name_col].isna() | df[age_col].isna())
    )
    df['is_suspicious'] = conditions
    return df

def extract_suspicious_profiles(df):
    if 'is_suspicious' not in df.columns:
        raise ValueError('먼저 flag_suspicious_profiles()를 실행하세요')
    return df[df['is_suspicious'] == True].copy()
