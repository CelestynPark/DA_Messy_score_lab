import pandas as pd

def detect_suspicious(df: pd.DataFrame) -> pd.DataFrame:
    """
    이상 응시자 여부를 판단하고, 조건별 Boolean 컬럼과 is_suspicious 컬럼을 추가한다.

    Parameters:
        df (pd.DataFrame): 정제된_나이, 점수, 성별, 이름, 시험일 등을 포함한 데이터프레임

    Returns:
        pd.DataFrame: 이상 조건 Boolean 컬럼 + 이상조건_총족수 + is_suspicious 포함된 DataFrame
    """

    df = df.copy()

    # 조건 1: 이름이 없음 또는 공백/NaN
    df['is_name_missing'] = df['이름'].isna() | (df['이름'].astype(str).str.strip() == '')

    # 조건 2: 정제된 점수가 NaN
    df['is_score_mising'] = df['정제된_점수'].isna()

    # 조건 3: 시험일 NaT 또는 결측
    df['is_date_missing'] = pd.to_datetime(df['시험일'], errors='coerce').isna()

    # 조건 4: 정제된 나이가 NaN
    df['is_age_missing'] = df['정제된_나이'].isna()

    # 조건 5: 성별이 공란이거나 정산 값이 아님
    df['is_gender_invalid'] = ~df['성별'].astype(str).str.upper().isin(['M', 'F'])

    # 조건 6: 재응시자인데 점수 또는 시험일이 없음
    df['is_retake_with_missing_info'] = (
    df['재응시여부'].astype(str).str.upper() == 'Y'
    ) & (
    df['정제된_점수'].isna() | pd.to_datetime(df['시험일'], errors='coerce').isna()
    )

    condition_cols = [
        'is_name_missing',
        'is_score_mising',
        'is_date_missing',
        'is_age_missing',
        'is_gender_invalid',
        'is_retake_with_missing_info'
    ]

    df['이상조건_충족수'] = df[condition_cols].sum(axis=1)

    # 이상 응시자 여부
    df['is_suspicious'] = df['이상조건_충족수'].apply(lambda x: 'Y' if x >= 2 else 'N')

    return df