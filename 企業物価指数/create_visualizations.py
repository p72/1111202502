import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from datetime import datetime

# 日本語フォントの設定
matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# CSVファイルの読み込み（Shift-JISエンコーディング）
df = pd.read_csv('企業物価指数円ベースpr01_m_1.csv', encoding='shift_jis', skiprows=2)

# ヘッダー行から列名を取得
header_row = df.iloc[0]
print("列名情報:")
for i, col_name in enumerate(header_row):
    print(f"{i}: {col_name}")

# メタデータ行をスキップして実際のデータを取得（行7以降）
data_df = df.iloc[6:].copy()
data_df.columns = ['date', 'domestic_yoy', 'export_yoy', 'import_yoy', 'chain_yoy',
                   'domestic_index', 'summer_adj', 'export_index', 'import_index', 'chain_index']

# 日付列をdatetime型に変換
data_df['date'] = pd.to_datetime(data_df['date'], format='%Y/%m')

# 数値列を数値型に変換
numeric_columns = ['export_yoy', 'import_yoy', 'export_index', 'import_index']
for col in numeric_columns:
    data_df[col] = pd.to_numeric(data_df[col], errors='coerce')

# データの基本統計
print("\n=== データ統計情報 ===")
print(f"データ期間: {data_df['date'].min()} ～ {data_df['date'].max()}")
print(f"\n輸出物価指数（前年比%）統計:")
print(data_df['export_yoy'].describe())
print(f"\n輸入物価指数（前年比%）統計:")
print(data_df['import_yoy'].describe())

# 最近のデータ
print("\n=== 最近のデータ（直近12ヶ月）===")
print(data_df[['date', 'export_yoy', 'import_yoy', 'export_index', 'import_index']].tail(12).to_string())

# グラフ1: 輸出物価指数と輸入物価指数の推移（指数）
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(data_df['date'], data_df['export_index'], label='Export Price Index (Yen basis)', linewidth=2, color='#2E86AB')
ax.plot(data_df['date'], data_df['import_index'], label='Import Price Index (Yen basis)', linewidth=2, color='#A23B72')
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Price Index (2020=100)', fontsize=12)
ax.set_title('Export and Import Price Index Trends (Yen basis)', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('price_index_trends.png', dpi=300, bbox_inches='tight')
print("\nグラフ保存: price_index_trends.png")

# グラフ2: 輸出物価指数と輸入物価指数の前年比推移
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(data_df['date'], data_df['export_yoy'], label='Export Price YoY Change (%)', linewidth=2, color='#2E86AB')
ax.plot(data_df['date'], data_df['import_yoy'], label='Import Price YoY Change (%)', linewidth=2, color='#A23B72')
ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Year-over-Year Change (%)', fontsize=12)
ax.set_title('Export and Import Price Index - Year-over-Year Changes', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('price_yoy_trends.png', dpi=300, bbox_inches='tight')
print("グラフ保存: price_yoy_trends.png")

# グラフ3: 近年のデータ（2015年以降）
recent_data = data_df[data_df['date'] >= '2015-01-01'].copy()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# 指数の推移
ax1.plot(recent_data['date'], recent_data['export_index'], label='Export Price Index', linewidth=2.5, color='#2E86AB')
ax1.plot(recent_data['date'], recent_data['import_index'], label='Import Price Index', linewidth=2.5, color='#A23B72')
ax1.set_ylabel('Price Index (2020=100)', fontsize=12)
ax1.set_title('Recent Trends in Export and Import Price Indices (2015-)', fontsize=14, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# 前年比の推移
ax2.plot(recent_data['date'], recent_data['export_yoy'], label='Export Price YoY (%)', linewidth=2.5, color='#2E86AB')
ax2.plot(recent_data['date'], recent_data['import_yoy'], label='Import Price YoY (%)', linewidth=2.5, color='#A23B72')
ax2.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
ax2.set_xlabel('Date', fontsize=12)
ax2.set_ylabel('Year-over-Year Change (%)', fontsize=12)
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('recent_price_trends.png', dpi=300, bbox_inches='tight')
print("グラフ保存: recent_price_trends.png")

# グラフ4: 輸出入価格指数の差（スプレッド）
fig, ax = plt.subplots(figsize=(14, 7))
spread = data_df['import_index'] - data_df['export_index']
ax.plot(data_df['date'], spread, linewidth=2, color='#F18F01')
ax.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
ax.fill_between(data_df['date'], spread, 0, where=(spread > 0), alpha=0.3, color='red', label='Import > Export')
ax.fill_between(data_df['date'], spread, 0, where=(spread <= 0), alpha=0.3, color='blue', label='Export > Import')
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('Price Index Difference (Import - Export)', fontsize=12)
ax.set_title('Import-Export Price Index Spread', fontsize=14, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('price_spread.png', dpi=300, bbox_inches='tight')
print("グラフ保存: price_spread.png")

# 統計サマリーをCSVに出力
summary_stats = pd.DataFrame({
    'Metric': ['Export Index Mean', 'Export Index Std', 'Export Index Min', 'Export Index Max',
               'Import Index Mean', 'Import Index Std', 'Import Index Min', 'Import Index Max',
               'Export YoY Mean', 'Export YoY Std', 'Import YoY Mean', 'Import YoY Std'],
    'Value': [
        data_df['export_index'].mean(), data_df['export_index'].std(),
        data_df['export_index'].min(), data_df['export_index'].max(),
        data_df['import_index'].mean(), data_df['import_index'].std(),
        data_df['import_index'].min(), data_df['import_index'].max(),
        data_df['export_yoy'].mean(), data_df['export_yoy'].std(),
        data_df['import_yoy'].mean(), data_df['import_yoy'].std()
    ]
})
summary_stats.to_csv('summary_statistics.csv', index=False)
print("\n統計サマリー保存: summary_statistics.csv")

print("\n全ての可視化が完了しました！")
