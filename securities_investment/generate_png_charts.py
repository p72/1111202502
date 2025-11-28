#!/usr/bin/env python3
"""
証券投資データのPNGグラフ生成スクリプト

matplotlib を使用して高品質なPNG画像を生成します。
日本語表示のため、適切なフォント設定が必要です。
"""

import csv
import matplotlib
matplotlib.use('Agg')  # GUIなし環境用
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 日本語フォントの設定
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False  # マイナス記号の文字化け対策

# CSVファイルからデータを読み込む
dates = []
outward_data = []
inward_data = []
net_data = []

with open('securities_investment_data.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # 年月を日付オブジェクトに変換
        year_month = row['年月']
        year = int(year_month[:4])
        month = int(year_month[5:7])
        dates.append(datetime(year, month, 1))

        outward_data.append(float(row['対外証券投資_資産（十億円）']))
        inward_data.append(float(row['対内証券投資_負債（十億円）']))
        net_data.append(float(row['ネット証券投資（十億円）']))

# グラフ1: 証券投資の推移（対外・対内）
fig1, ax1 = plt.subplots(figsize=(14, 8))

ax1.plot(dates, outward_data, label='Outward Securities Investment (Assets)',
         color='#4BC0C0', linewidth=2, marker='o', markersize=4)
ax1.plot(dates, inward_data, label='Inward Securities Investment (Liabilities)',
         color='#FF6384', linewidth=2, marker='s', markersize=4)

ax1.set_title('Securities Investment Trends (Outward & Inward)\n2020-2024',
              fontsize=16, fontweight='bold', pad=20)
ax1.set_xlabel('Year-Month', fontsize=12, fontweight='bold')
ax1.set_ylabel('Amount (Billion Yen)', fontsize=12, fontweight='bold')

# X軸の日付フォーマット
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# グリッド
ax1.grid(True, alpha=0.3, linestyle='--')

# 凡例
ax1.legend(loc='upper left', fontsize=11, framealpha=0.9)

# Y軸の範囲を見やすく調整
ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

# レイアウト調整
plt.tight_layout()

# 保存
png_file1 = 'securities_investment_outward_inward.png'
plt.savefig(png_file1, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Graph 1 saved: {png_file1}")
plt.close()

# グラフ2: ネット証券投資の推移
fig2, ax2 = plt.subplots(figsize=(14, 8))

# プラス・マイナスで色を分ける
colors = ['#36A2EB' if x >= 0 else '#FF6384' for x in net_data]
ax2.bar(dates, net_data, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5, width=20)

ax2.set_title('Net Securities Investment Trends (Outward - Inward)\n2020-2024',
              fontsize=16, fontweight='bold', pad=20)
ax2.set_xlabel('Year-Month', fontsize=12, fontweight='bold')
ax2.set_ylabel('Amount (Billion Yen)', fontsize=12, fontweight='bold')

# X軸の日付フォーマット
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

# グリッド
ax2.grid(True, alpha=0.3, linestyle='--', axis='y')

# ゼロラインを強調
ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)

# 凡例
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#36A2EB', alpha=0.7, label='Net Outflow (Positive)'),
    Patch(facecolor='#FF6384', alpha=0.7, label='Net Inflow (Negative)')
]
ax2.legend(handles=legend_elements, loc='upper left', fontsize=11, framealpha=0.9)

# レイアウト調整
plt.tight_layout()

# 保存
png_file2 = 'securities_investment_net.png'
plt.savefig(png_file2, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Graph 2 saved: {png_file2}")
plt.close()

# グラフ3: 年次平均の比較（棒グラフ）
# 年ごとのデータを集計
yearly_outward = {}
yearly_inward = {}
yearly_net = {}
yearly_counts = {}

for i, date in enumerate(dates):
    year = date.year
    if year not in yearly_outward:
        yearly_outward[year] = 0
        yearly_inward[year] = 0
        yearly_net[year] = 0
        yearly_counts[year] = 0

    yearly_outward[year] += outward_data[i]
    yearly_inward[year] += inward_data[i]
    yearly_net[year] += net_data[i]
    yearly_counts[year] += 1

# 平均を計算
years = sorted(yearly_outward.keys())
avg_outward = [yearly_outward[y] / yearly_counts[y] for y in years]
avg_inward = [yearly_inward[y] / yearly_counts[y] for y in years]
avg_net = [yearly_net[y] / yearly_counts[y] for y in years]

fig3, ax3 = plt.subplots(figsize=(12, 8))

x = range(len(years))
width = 0.25

bars1 = ax3.bar([i - width for i in x], avg_outward, width,
                label='Outward (Assets)', color='#4BC0C0', alpha=0.8, edgecolor='black')
bars2 = ax3.bar([i for i in x], avg_inward, width,
                label='Inward (Liabilities)', color='#FF6384', alpha=0.8, edgecolor='black')
bars3 = ax3.bar([i + width for i in x], avg_net, width,
                label='Net Investment', color='#FFCE56', alpha=0.8, edgecolor='black')

ax3.set_title('Average Securities Investment by Year\n2020-2024',
              fontsize=16, fontweight='bold', pad=20)
ax3.set_xlabel('Year', fontsize=12, fontweight='bold')
ax3.set_ylabel('Average Monthly Amount (Billion Yen)', fontsize=12, fontweight='bold')
ax3.set_xticks(x)
ax3.set_xticklabels(years)

# グリッド
ax3.grid(True, alpha=0.3, linestyle='--', axis='y')
ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

# 凡例
ax3.legend(loc='upper left', fontsize=11, framealpha=0.9)

# 値をバーの上に表示
def autolabel(bars):
    for bar in bars:
        height = bar.get_height()
        ax3.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3 if height >= 0 else -15),
                    textcoords="offset points",
                    ha='center', va='bottom' if height >= 0 else 'top',
                    fontsize=8)

autolabel(bars1)
autolabel(bars2)
autolabel(bars3)

# レイアウト調整
plt.tight_layout()

# 保存
png_file3 = 'securities_investment_yearly_average.png'
plt.savefig(png_file3, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Graph 3 saved: {png_file3}")
plt.close()

# グラフ4: 2024年の月次推移（新NISA効果の可視化）
dates_2024 = [d for d in dates if d.year == 2024]
outward_2024 = [outward_data[i] for i, d in enumerate(dates) if d.year == 2024]
inward_2024 = [inward_data[i] for i, d in enumerate(dates) if d.year == 2024]
net_2024 = [net_data[i] for i, d in enumerate(dates) if d.year == 2024]

fig4, (ax4_1, ax4_2) = plt.subplots(2, 1, figsize=(14, 10))

# 上段: 対外・対内
ax4_1.plot(dates_2024, outward_2024, label='Outward Investment',
          color='#4BC0C0', linewidth=3, marker='o', markersize=8)
ax4_1.plot(dates_2024, inward_2024, label='Inward Investment',
          color='#FF6384', linewidth=3, marker='s', markersize=8)
ax4_1.set_title('2024 Securities Investment Trends (New NISA Impact)\nOutward & Inward',
               fontsize=14, fontweight='bold', pad=15)
ax4_1.set_ylabel('Amount (Billion Yen)', fontsize=11, fontweight='bold')
ax4_1.grid(True, alpha=0.3, linestyle='--')
ax4_1.legend(loc='upper left', fontsize=10, framealpha=0.9)
ax4_1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

# 下段: ネット
colors_2024 = ['#36A2EB' if x >= 0 else '#FF6384' for x in net_2024]
ax4_2.bar(dates_2024, net_2024, color=colors_2024, alpha=0.7,
         edgecolor='black', linewidth=0.5, width=20)
ax4_2.set_title('Net Securities Investment', fontsize=14, fontweight='bold', pad=15)
ax4_2.set_xlabel('Month (2024)', fontsize=11, fontweight='bold')
ax4_2.set_ylabel('Amount (Billion Yen)', fontsize=11, fontweight='bold')
ax4_2.grid(True, alpha=0.3, linestyle='--', axis='y')
ax4_2.axhline(y=0, color='black', linestyle='-', linewidth=1)

# X軸の日付フォーマット
for ax in [ax4_1, ax4_2]:
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

# レイアウト調整
plt.tight_layout()

# 保存
png_file4 = 'securities_investment_2024_nisa_impact.png'
plt.savefig(png_file4, dpi=300, bbox_inches='tight', facecolor='white')
print(f"Graph 4 saved: {png_file4}")
plt.close()

print("\n=== Summary ===")
print(f"Total graphs created: 4")
print(f"1. {png_file1} - Outward & Inward trends (2020-2024)")
print(f"2. {png_file2} - Net investment trends (2020-2024)")
print(f"3. {png_file3} - Yearly averages comparison")
print(f"4. {png_file4} - 2024 detailed view (New NISA impact)")
print("\nAll graphs saved as PNG files (300 DPI, high quality)")
