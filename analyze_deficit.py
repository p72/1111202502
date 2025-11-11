import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# CSVファイルを読み込む（Shift-JISエンコーディングで試す）
encodings = ['shift-jis', 'cp932', 'utf-8']
df = None

for encoding in encodings:
    try:
        df = pd.read_csv('資金循環統計 資金過不足1980.csv', encoding=encoding)
        print(f"Successfully read with {encoding} encoding")
        break
    except:
        continue

if df is None:
    print("Failed to read CSV with any encoding")
    exit(1)

# データの確認
print("\nColumn names:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head())
print("\nData shape:", df.shape)
