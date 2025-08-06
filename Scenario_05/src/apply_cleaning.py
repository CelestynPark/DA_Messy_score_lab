import pandas as pd
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.clean_age import clean_age
from src.clean_score import clean_score


def apply_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    점수와 나이를 정제하여 새로운 컬럼을 추가한다.
    
    Parameters: 
        df (pd.DataFrame): 원본 데이터프레임

    Returns:
        pd.DataFrame: 재응시 여부 추론, 정제된 점수 및 나이, 품질 등급 컬럼이 추가된 DataFrame
    """

    df = df.copy()

    # 재응시 여부 추론
    df['재응시여부'] = df['비고'].astype(str).str.lower().str.contains(
        'retake|re-take|retook|재응시'
    ).map({True: 'Y', False: 'N'})

    # 점수 정제
    df[['정제된_점수', 'score_quality']] = df['점수'].apply(clean_score).apply(pd.Series)

    # 나이 정제
    df[['정제된_나이', 'age_quality']] = df['나이'].apply(clean_age).apply(pd.Series)

    return df

if __name__ == '__main__':
    INPUT_PATH = Path('raw/messy_student_scores_500.csv')
    OUTPUT_PATH = Path('data/processed/cleaned_student_scores.csv')

    df_raw = pd.read_csv(INPUT_PATH)
    df_cleaned = apply_cleaning(df_raw)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_cleaned.to_csv(OUTPUT_PATH, index=False)

    print(f"[INFO] 데이터 정제 완료: {OUTPUT_PATH}에 저장됨")