import pandas as pd

def show_retake_stats(df):
    print(df['재응시여부'].value_counts())
    print(df['재응시여부'].value_counts(normalize=True).apply(lambda x: f"{x:.2%}"))

if __name__ == "__main__":
    df = pd.read_csv('data/cleaned_student_scores_500.csv')
    show_retake_stats(df)