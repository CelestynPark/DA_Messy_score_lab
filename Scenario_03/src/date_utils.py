import pandas as pd
from dateutil import parser

def parse_exam_date(date_str):
    if pd.isna(date_str) or str(date_str).strip() == '':
        return pd.NaT
    try:
        return parser.parse(str(date_str), fuzzy=True)
    except:
        return pd.NaT
    
def enrich_exam_date_column(df, source_col='시험일'):
    df['시험일_정제'] = df[source_col].apply(parse_exam_date)

    df['요일'] = df['시험일_정제'].dt.day_name()
    df['응시_주차'] = df['시험일_정제'].dt.isocalendar().week
    df['응시_월'] = df['시험일_정제'].dt.month
    df['주말여부'] = df['요일'].isin(['Saturday', 'Sunday'])

    return df