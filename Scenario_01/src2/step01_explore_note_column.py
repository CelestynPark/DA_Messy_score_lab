import pandas as pd

def explore_note_column(csv_path: str, top_n: int = 30) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    note_counts = df["비고"].value_counts(dropna=False).reset_index()
    note_counts.columns = ["표현", "빈도"]
    
    print(f"[비고 컬럼 고유값 Top {top_n}]")
    print(note_counts.head(top_n))
    
    return note_counts