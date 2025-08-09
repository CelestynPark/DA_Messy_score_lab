import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

def plot_column_defect_rate(df: pd.DataFrame, save_path: Path = None) -> pd.DataFrame:
    """
    컬럼별 결함율(%)을 계산한고 상위 5개 항목을 바 차트로 시각화

    Parameters:
        df(pd.DataFrame): score_quality() 이후의 데이터프레임
        save_path (Path): 저장할 이미지 경로. None이면 저장하지 않음
    """
    defect_cols = [col for col in df.columns if col.startswith('결함_')]
    defect_rates = df[defect_cols].mean().sort_values(ascending=False)

    top_defects = defect_rates.head(5)

    plt.figure(figsize=(8, 5))
    sns.barplot(x=top_defects.values, y=top_defects.index, palette="Reds_r")
    plt.title('상위 5개 컬럼 결함율 (%)')
    plt.xlabel('결함율 (%)')
    plt.ylabel('결함 걸럼명')
    plt.tight_layout()

    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=100)
        print(f"[INFO] 결함율 시각화 저장 완료: {save_path}")
    else:
        plt.show()

def plot_quality_distribution(df: pd.DataFrame, save_path: Path = None) -> pd.DataFrame:
    """
    품질등급(A/B/C) 분포를 파이 차트로 시각화

    Parameters:
        df (pd.DataFrame): score_quality() 이후의 데이터프레임
        save_path(Path): 저장할 이미지 경로, None이면 저장하지 않음
    """

    quality_counts = df['품질등급'].value_counts().sort_index()

    plt.figure(figsize=(6, 6))
    plt.pie(
        quality_counts,
        labels=quality_counts.index,
        autopct='%1.1f%%',
        colors=['#66c2a5', '#fc8d62', '#8da0cb'],
        startangle=90,
        counterclock=False
    )
    plt.title('품질등급 분포 (A/B/C)')
    plt.tight_layout()

    if save_path:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=100)
        print(f"[INFO] 품질등급 분포 시각화 저장 완료: {save_path}")
    else:
        plt.show()
