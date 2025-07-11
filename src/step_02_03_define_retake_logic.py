import pandas as pd
import os
from rules.retake_keywords import RETAKE_KEYWORDS

def detect_retake(df):
    def is_retake(text):
        if text =='':
            return 'N'
        
        text = str(text).strip().lower()
        meaningless = ['', '없음', 'null', '.']
        if text in meaningless:
            return 'N'
        
        for word in RETAKE_KEYWORDS:
            if word.lower() in text:
                return 'Y'
        return 'N'
    
    df['재응시여부'] = df['비고'].apply(is_retake)
    return df

def add_retake_column(csv_path: str, save_path:str = None) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df = detect_retake(df)
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        df.to_csv(save_path, index=False)

    return df

if __name__ == '__main__':
    add_retake_column('raw/messy_student_scores_500.csv', 'data/cleaned_student_scores_500.csv')
    