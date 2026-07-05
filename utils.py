import pandas as pd
import numpy as np

def create_sample_data():
    """サンプルデータ（売上データ）を生成する関数"""
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    sales = np.random.randint(100, 5000, size=len(dates))
    categories = np.random.choice(["食品", "衣料", "電化製品", "雑貨"], size=len(dates))
    
    data = pd.DataFrame({
        "日付": dates,
        "売上": sales,
        "カテゴリ": categories
    })
    return data