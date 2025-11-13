import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# 日本語フォントの設定
matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# CSVファイルの読み込み（Shift-JISエンコーディング）
df = pd.read_csv('企業物価指数円ベースpr01_m_1.csv', encoding='shift_jis', skiprows=2)

# データの基本情報を表示
print("データの基本情報:")
print(df.head(10))
print("\nカラム名:")
print(df.columns.tolist())
print("\nデータ形状:")
print(df.shape)
print("\nデータ型:")
print(df.dtypes)
print("\n統計情報:")
print(df.describe())

# 最初の数行を詳細に表示
print("\n\n最初の20行のデータ:")
print(df.head(20).to_string())
