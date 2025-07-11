import pandas as pd
import numpy as np
import os

def load_data(data_path):
    data_path = os.path.join('raw', 'messy_student_scores_500.csv')
    df = pd.read_csv(data_path)

    print("[1] 비고 컬럼 고유값 및 빈도")
    print(df['비고'].value_counts(dropna=False))

