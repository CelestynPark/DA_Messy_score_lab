import pandas as pd
import numpy as np
from typing import Tuple

def score_quality(df: pd.DataFrame) -> pd.DataFrame:
    """
    데이터의 컬럼별 결함을 판별하고, 행별 결함 수와 품질 등급을 계산한다.

    Parameters:
        df(pd.DataFrame): 정제된 데이터프레임 (cleaned_student_scors.csv)

    Returns:
        pd.DataFrame: 결함 컬럼, 결함 수, 품질등급, 데이터셋 품질평가 컬럼이 추가된 DataFrame
    """

    df = df.copy()
    # 1단계: 컬럼별 결함 여부 판별
    df['결함_이름'] = df['이름'].isna() | (df['이름'].astype(str).str.strip() == '') | (df['이름'].str.len() <= 1) | (df['이름'].str.contains(',', na=False))
    df['결함_정제된_나이'] = df['정제된_나이'].isna()
    df['결함_성별'] = ~df['성별'].astype(str).str.upper().isin(['M', 'F'])
    df['결함_정제된_점수'] = df['정제된_점수'].isna() | (df['정제된_점수'] <= 0) | (df['정제된_점수'] > 100)
    df['결함_시험일'] = pd.to_datetime(df['시험일'], errors='coerce').isna()

    # '재응시여부' 결함 판별에서 제외 (시나리오 명시 사항)

    # 2단계: 행별 결함 수 계산
    detect_columns = [col for col in df.columns if col.startswith('결함_')]
    df['결함_계수'] = df[detect_columns].sum(axis=1)

    # 3단계: 품질 등급 부여
    def assign_grage(n_defects):
        if n_defects <= 1:
            return 'A'
        elif n_defects <= 3:
            return 'B'
        else:
            return 'C'
        
    df['품질등급'] = df['결함_계수'].apply(assign_grage)

    # 4단계: 전체 품질 평가 (우수/보통/취약) -> 비율 계산 후 결과만 부여 (별도 시각화에서 활용)
    quality_counts = df['품질등급'].value_counts(normalize=True) * 100
    a_ratio = quality_counts.get('A', 0)

    if a_ratio >= 70:
        dataset_quality = '우수'
    elif a_ratio >= 40:
        dataset_quality = '보통'
    else:
        dataset_quality = '취약'

    df['데이터셋_품질평가'] = dataset_quality # 전 행에 동일하게 표시

    return df
