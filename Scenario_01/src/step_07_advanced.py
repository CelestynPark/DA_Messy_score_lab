import pandas as pd

def detect_suspicious_columns(df):
    df['is_suspicious'] = 'N'

    suspicious_condition = (
        (df['재응시여부'] == 'Y') & 
        (
            df['시험일'].isna() |
            df['정제점수'].isna() |
            df['이름'].isna()
        )
    )

    df.loc[suspicious_condition, 'is_suspicious'] = 'Y'
    print(f"이상행 수: {df['is_suspicious'].value_counts().to_dict()}")
    return df

if __name__ == '__main__':
    from step_05_analyze_retake_student_score import clean_score_column
    df = pd.read_csv('data/cleaned_student_scores_500.csv')
    df = clean_score_column(df)

    detect_suspicious_columns(df)

    df.to_csv('data/retake_tagged_with_suspicious.csv', index=False)
    
