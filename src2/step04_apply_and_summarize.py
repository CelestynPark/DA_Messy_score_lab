import pandas as pd
from step02_define_retake_logic import determine_retake

def apply_retake_classification(csv_path: str, save_path: str = None) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    df["재응시여부"] = df["비고"].apply(determine_retake)

    total = len(df)
    summary = df["재응시여부"].value_counts().reset_index()
    summary.columns = ["재응시여부", "인원수"]
    summary["비율(%)"] = (summary["인원수"] / total * 100).round(2)

    print("[재응시여부 분포]")
    print(summary)

    if save_path:
        df.to_csv(save_path, index=False)

    return df