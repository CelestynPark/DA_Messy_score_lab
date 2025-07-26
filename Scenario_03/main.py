import pandas as pd
from src.date_utils import enrich_exam_date_column

RAW_DATA_PATH = 'raw/messy_student_scores_500.csv'

df = pd.read_csv(RAW_DATA_PATH)

print(df.columns)
print(df.head())

df = enrich_exam_date_column(df)
print(df.head())