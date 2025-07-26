import pandas as pd
from src.loader import load_raw_scores
from src.transformer import transform_scores
from src.statistic import compute_quality_stats
from src.visualizer import plot_score_quality_distribution, plot_score_boxplot
from src.analyzer import detect_suspicious_cases, compare_sample_quality

df = load_raw_scores('raw/messy_student_scores_500.csv')

df_cleaned = transform_scores(df)

# print(df_cleaned[['점수', '정제된_점수', 'score_quality', 'is_score_clean']].head())

stats_df = compute_quality_stats(df_cleaned)
print('n\등급별 통계 summary:')
print(stats_df)

plot_score_quality_distribution(df_cleaned, save_path='output/score_quality_piechart.png')
plot_score_boxplot(df_cleaned, save_path='output/score_boxplot.png')

df_cleaned.to_csv('output/cleaned_scores.csv', index=False)

suspicious_df = detect_suspicious_cases(df_cleaned)
print("\n이상 케이스:")
print(suspicious_df[['이름', '점수', '정제된_점수', 'score_quality', '비고', 'is_retake_candidate']].head())

suspicious_df.to_csv('output/suspicious_cases.csv', index=False)

df_with_confidence = compare_sample_quality(df_cleaned)

summary = df_with_confidence.groupby('신뢰도_샘플_분류').agg(
    인원수=('정제된_점수', 'count'),
    평균점수=('정제된_점수', 'mean'),
    응시일_결측비율=('시험일', lambda x: x.isna().mean() * 100)
).reindex(['고신뢰', '중간', '저신뢰'])

print("\n신뢰도 샘플 비교: ")
print(summary)

df_with_confidence.to_csv('output/final_scored_dataset.csv', index=False)