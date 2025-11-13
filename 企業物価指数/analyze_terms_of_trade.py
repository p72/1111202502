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

# メタデータ行をスキップして実際のデータを取得（行7以降）
data_df = df.iloc[6:].copy()
data_df.columns = ['date', 'domestic_yoy', 'export_yoy', 'import_yoy', 'chain_yoy',
                   'domestic_index', 'summer_adj', 'export_index', 'import_index', 'chain_index']

# 日付列をdatetime型に変換
data_df['date'] = pd.to_datetime(data_df['date'], format='%Y/%m')

# 数値列を数値型に変換
numeric_columns = ['export_index', 'import_index']
for col in numeric_columns:
    data_df[col] = pd.to_numeric(data_df[col], errors='coerce')

# 欠損値を削除
data_df = data_df.dropna(subset=['export_index', 'import_index'])

# 交易条件の計算 (Terms of Trade = Export Price Index / Import Price Index * 100)
data_df['terms_of_trade'] = (data_df['export_index'] / data_df['import_index']) * 100

# 前年同月比の計算
data_df['tot_yoy'] = data_df['terms_of_trade'].pct_change(12) * 100

# 基準値（2020年平均）の計算
base_2020 = data_df[data_df['date'].dt.year == 2020]['terms_of_trade'].mean()
print(f"2020年の交易条件平均値: {base_2020:.2f}")

# データの統計情報
print("\n=== 交易条件（Terms of Trade）統計情報 ===")
print(f"データ期間: {data_df['date'].min().strftime('%Y年%m月')} ～ {data_df['date'].max().strftime('%Y年%m月')}")
print(f"\n交易条件統計:")
print(data_df['terms_of_trade'].describe())
print(f"\n最大値: {data_df['terms_of_trade'].max():.2f} ({data_df.loc[data_df['terms_of_trade'].idxmax(), 'date'].strftime('%Y年%m月')})")
print(f"最小値: {data_df['terms_of_trade'].min():.2f} ({data_df.loc[data_df['terms_of_trade'].idxmin(), 'date'].strftime('%Y年%m月')})")

# 時期別の統計
print("\n=== 時期別の交易条件平均 ===")
decades = {
    '1980年代': (1980, 1989),
    '1990年代': (1990, 1999),
    '2000年代': (2000, 2009),
    '2010年代': (2010, 2019),
    '2020年代': (2020, 2025)
}

for period_name, (start_year, end_year) in decades.items():
    period_data = data_df[(data_df['date'].dt.year >= start_year) & (data_df['date'].dt.year <= end_year)]
    if len(period_data) > 0:
        avg_tot = period_data['terms_of_trade'].mean()
        print(f"{period_name}: {avg_tot:.2f}")

# 最近のデータ
print("\n=== 最近の交易条件（直近24ヶ月）===")
recent_data = data_df.tail(24)[['date', 'export_index', 'import_index', 'terms_of_trade', 'tot_yoy']]
recent_data['date_str'] = recent_data['date'].dt.strftime('%Y/%m')
print(recent_data[['date_str', 'export_index', 'import_index', 'terms_of_trade', 'tot_yoy']].to_string(index=False))

# 重要な転換点を特定
print("\n=== 主要な転換点 ===")
# ローカル最大値と最小値を見つける
window = 24  # 2年間のウィンドウ
data_df['local_max'] = data_df['terms_of_trade'].rolling(window=window, center=True).max() == data_df['terms_of_trade']
data_df['local_min'] = data_df['terms_of_trade'].rolling(window=window, center=True).min() == data_df['terms_of_trade']

print("\n主要なピーク（直近5つ）:")
peaks = data_df[data_df['local_max'] == True].tail(5)[['date', 'terms_of_trade']]
for idx, row in peaks.iterrows():
    print(f"{row['date'].strftime('%Y年%m月')}: {row['terms_of_trade']:.2f}")

print("\n主要なボトム（直近5つ）:")
bottoms = data_df[data_df['local_min'] == True].tail(5)[['date', 'terms_of_trade']]
for idx, row in bottoms.iterrows():
    print(f"{row['date'].strftime('%Y年%m月')}: {row['terms_of_trade']:.2f}")

# グラフ1: 交易条件の長期推移
fig, ax = plt.subplots(figsize=(14, 8))
ax.plot(data_df['date'], data_df['terms_of_trade'], linewidth=2.5, color='#2E86AB', label='Terms of Trade')
ax.axhline(y=100, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Parity (100)')
ax.axhline(y=base_2020, color='orange', linestyle='--', linewidth=1.5, alpha=0.7, label=f'2020 Average ({base_2020:.1f})')
ax.fill_between(data_df['date'], data_df['terms_of_trade'], 100,
                 where=(data_df['terms_of_trade'] > 100), alpha=0.2, color='green', label='Favorable')
ax.fill_between(data_df['date'], data_df['terms_of_trade'], 100,
                 where=(data_df['terms_of_trade'] <= 100), alpha=0.2, color='red', label='Unfavorable')
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Terms of Trade (Export/Import Price Index * 100)', fontsize=12, fontweight='bold')
ax.set_title('Terms of Trade: Long-term Trends (1980-2025)', fontsize=14, fontweight='bold')
ax.legend(fontsize=10, loc='best')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('terms_of_trade_long_term.png', dpi=300, bbox_inches='tight')
print("\n\nグラフ保存: terms_of_trade_long_term.png")

# グラフ2: 交易条件の前年比変化
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(data_df['date'], data_df['tot_yoy'], linewidth=2, color='#A23B72', label='Terms of Trade YoY Change (%)')
ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
ax.fill_between(data_df['date'], data_df['tot_yoy'], 0,
                 where=(data_df['tot_yoy'] > 0), alpha=0.3, color='green')
ax.fill_between(data_df['date'], data_df['tot_yoy'], 0,
                 where=(data_df['tot_yoy'] <= 0), alpha=0.3, color='red')
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Year-over-Year Change (%)', fontsize=12, fontweight='bold')
ax.set_title('Terms of Trade: Year-over-Year Changes', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('terms_of_trade_yoy.png', dpi=300, bbox_inches='tight')
print("グラフ保存: terms_of_trade_yoy.png")

# グラフ3: 近年の交易条件（2015年以降）
recent_df = data_df[data_df['date'] >= '2015-01-01'].copy()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# 交易条件の推移
ax1.plot(recent_df['date'], recent_df['terms_of_trade'], linewidth=2.5, color='#2E86AB', label='Terms of Trade')
ax1.axhline(y=100, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Parity (100)')
ax1.set_ylabel('Terms of Trade', fontsize=12, fontweight='bold')
ax1.set_title('Recent Terms of Trade Trends (2015-)', fontsize=14, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# 輸出入物価指数との比較
ax2.plot(recent_df['date'], recent_df['export_index'], linewidth=2.5, color='#2E86AB', label='Export Price Index')
ax2.plot(recent_df['date'], recent_df['import_index'], linewidth=2.5, color='#A23B72', label='Import Price Index')
ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
ax2.set_ylabel('Price Index (2020=100)', fontsize=12, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('terms_of_trade_recent.png', dpi=300, bbox_inches='tight')
print("グラフ保存: terms_of_trade_recent.png")

# グラフ4: 交易条件の分布とトレンド
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ヒストグラム
ax1.hist(data_df['terms_of_trade'], bins=50, color='#2E86AB', alpha=0.7, edgecolor='black')
ax1.axvline(x=100, color='red', linestyle='--', linewidth=2, label='Parity (100)')
ax1.axvline(x=data_df['terms_of_trade'].mean(), color='orange', linestyle='--', linewidth=2,
            label=f'Mean ({data_df["terms_of_trade"].mean():.1f})')
ax1.set_xlabel('Terms of Trade', fontsize=12, fontweight='bold')
ax1.set_ylabel('Frequency', fontsize=12, fontweight='bold')
ax1.set_title('Distribution of Terms of Trade', fontsize=13, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# 10年移動平均
data_df['tot_ma_10y'] = data_df['terms_of_trade'].rolling(window=120, center=True).mean()
ax2.plot(data_df['date'], data_df['terms_of_trade'], linewidth=1, color='lightgray', alpha=0.5, label='Monthly')
ax2.plot(data_df['date'], data_df['tot_ma_10y'], linewidth=3, color='#2E86AB', label='10-Year Moving Average')
ax2.axhline(y=100, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Parity (100)')
ax2.set_xlabel('Date', fontsize=12, fontweight='bold')
ax2.set_ylabel('Terms of Trade', fontsize=12, fontweight='bold')
ax2.set_title('Terms of Trade with 10-Year Moving Average', fontsize=13, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('terms_of_trade_distribution.png', dpi=300, bbox_inches='tight')
print("グラフ保存: terms_of_trade_distribution.png")

# 統計サマリーをCSVに保存
summary_data = {
    'Period': [],
    'Average_TOT': [],
    'Std_Dev': [],
    'Min': [],
    'Max': []
}

for period_name, (start_year, end_year) in decades.items():
    period_data = data_df[(data_df['date'].dt.year >= start_year) & (data_df['date'].dt.year <= end_year)]
    if len(period_data) > 0:
        summary_data['Period'].append(period_name)
        summary_data['Average_TOT'].append(period_data['terms_of_trade'].mean())
        summary_data['Std_Dev'].append(period_data['terms_of_trade'].std())
        summary_data['Min'].append(period_data['terms_of_trade'].min())
        summary_data['Max'].append(period_data['terms_of_trade'].max())

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv('terms_of_trade_summary.csv', index=False)
print("\n統計サマリー保存: terms_of_trade_summary.csv")

# 最新24ヶ月のデータもCSVに保存
recent_export = data_df.tail(24)[['date', 'export_index', 'import_index', 'terms_of_trade', 'tot_yoy']].copy()
recent_export['date'] = recent_export['date'].dt.strftime('%Y/%m')
recent_export.to_csv('recent_terms_of_trade.csv', index=False)
print("最近のデータ保存: recent_terms_of_trade.csv")

print("\n\n=== 分析完了 ===")
print(f"現在の交易条件（{data_df['date'].iloc[-1].strftime('%Y年%m月')}）: {data_df['terms_of_trade'].iloc[-1]:.2f}")
print(f"前年同月比: {data_df['tot_yoy'].iloc[-1]:.2f}%")
print(f"パリティ（100）との乖離: {data_df['terms_of_trade'].iloc[-1] - 100:.2f}ポイント")
