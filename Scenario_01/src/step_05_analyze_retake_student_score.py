import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'Malgun Gothic'

def clean_score_column(df):
    def convert_score(val):
        try:
            if pd.isna(val):
                return None
            val = str(val).strip()
            val = val.replace('점', '')
            return float(val) if val.replace('.', '').isdigit() else None
        except:
            return None

    df['정제점수'] = df['점수'].apply(convert_score)
    return df

def analyze_retake_characteristics(df):
    df = clean_score_column(df)
    print(f"1. 점수 분포 비교 (평균 & 중앙값): ")
    score_stats = df.groupby('재응시여부')['정제점수'].agg(['count', 'mean', 'median']).round(2)
    print(score_stats) 
    
    print(f"2. 시험률 결측률 (재응시자 대상): ")
    is_retake = df['재응시여부'] == 'Y'
    total_retake = is_retake.sum()
    no_exam_date = df.loc[is_retake, '시험일'].isna().sum()
    print(f"재응시자 수: {total_retake}, 시험일 결측: {no_exam_date}, 결측률: {round(no_exam_date / total_retake * 100, 2)}%")

    print(f"3. 이름/나이 결측률 (재응시자 vs 응시자): ")
    name_rate = df.groupby('재응시여부')['이름'].apply(lambda x: x.isna().mean()).round(2)
    age_rate = df.groupby('재응시여부')['나이'].apply(lambda x: x.isna().mean()).round(2)
    print(f"이름 결측률: {name_rate * 100}")
    print(f"나이 결측률: {age_rate * 100}")
    
    print(f"\nBoxplot: 점수분포")
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x='재응시여부', y='정제점수')
    plt.title('재응시 여부에 따른 점수 분포')
    plt.xlabel('재응시여부')
    plt.ylabel('정제점수')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    from step_04_apply_and_summarize import show_retake_stats

    df = pd.read_csv('data/cleaned_student_scores_500.csv')
    show_retake_stats(df)
    analyze_retake_characteristics(df)
