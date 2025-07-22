import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.rcParams['font.family'] = 'Malgun Gothic'

def plot_score_quality_distribution(df: pd.DataFrame, save_path: str = None) -> None:
    counts = df['score_quality'].value_counts().sort_index()

    plt.figure(figsize=(6, 6))
    plt.pie(
        counts,
        labels=counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("pastel")[:3]
    )
    plt.title("Score Quality 등급 분포 (A/B/C)")
    if not os.path.exists(save_path):
        plt.savefig(save_path, bbox_inches='tight')
    plt.close()

def plot_score_boxplot(df: pd.DataFrame, save_path: str = None) -> None:
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x='score_quality', y='정제된_점수', order=['A', 'B', 'C'], palette="pastel")
    plt.title('Score Quality 별 정제된 점수 분포')
    plt.xlabel('Score Quality')
    plt.ylabel('정제된 점수')

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.close()