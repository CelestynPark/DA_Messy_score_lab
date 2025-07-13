import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

plt.rcParams['font.family'] = 'Malgun Gothic'

def plot_pie_retake_ratio(df):
    counts = df['재응시여부'].value_counts()
    size = counts.values
    labels = counts.index

    plt.figure(figsize=(5, 5))
    plt.pie(size, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff9999'])
    plt.title('재응시 여부 비율')
    plt.tight_layout()
    plt.show()


def plot_box_score_by_retake(df):
    if '정제점수' not in df.columns:
        print("정제 점수가 컬럼에 없음. 먼저 정제 후 다시 실행해주세요.")
        return 

    plt.figure(figsize=(8, 6))
    sns.boxplot(data=df, x='재응시여부', y='정제점수', palette='Set2')
    plt.title('재응시 여부에 따른 점수 분포')
    plt.ylabel('정제점수')
    plt.xlabel('재응시 여부')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def time_series_by_exam_date(df):
    if '시험일' not in df.columns:
        print("시험일 컬럼이 없습니다.")
        return
    df_date = df.copy()
    df_date['시험일'] = pd.to_datetime(df_date['시험일'], errors='coerce')

    df_date = df_date.dropna(subset=['시험일'])
    retake_daily = df_date[df_date['재응시여부'] == 'Y']
    count_by_day = retake_daily.groupby('시험일').size()

    plt.figure(figsize=(10, 4))
    count_by_day.plot(marker='o', color='tomato')
    plt.title('시험일 기준 재응시자 수')
    plt.xlabel('시험일')
    plt.ylabel('재응시자 수')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    from step_05_analyze_retake_student_score import clean_score_column

    df = pd.read_csv('data/cleaned_student_scores_500.csv')
    df = clean_score_column(df)

    plot_pie_retake_ratio(df)
    plot_box_score_by_retake(df)
    time_series_by_exam_date(df)