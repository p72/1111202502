#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
物価水準変化の累積寄与度グラフ作成スクリプト
2015-2024年のCPIと費目別寄与度を可視化
"""

import matplotlib
matplotlib.use('Agg')  # GUIなし環境用バックエンド
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# 日本語フォント設定
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# グラフの設定
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 11

# データ定義
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
cpi_index = [98.2, 98.5, 99.0, 100.0, 100.5, 100.0, 99.8, 102.3, 106.7, 109.5]
cpi_change = [0, 0.3, 0.8, 1.8, 2.3, 1.8, 1.6, 4.2, 8.7, 11.5]  # 2015年からの累積変化

# 10大費目の累積寄与度データ（推定値、2015-2024年）
categories = ['食料', '光熱・水道', '教養娯楽', '交通・通信', '住居',
              '諸雑費', '家具・家事用品', '被服及び履物', '保健医療', '教育']
contributions = [4.0, 2.75, 1.35, 1.15, 0.9, 0.8, 0.6, 0.4, 0.4, 0.15]  # ポイント
contribution_rates = [34.8, 23.9, 11.7, 10.0, 7.8, 7.0, 5.2, 3.5, 3.5, 1.3]  # 寄与率（%）

# 色の定義
colors = ['#FF6B6B', '#FFA500', '#4ECDC4', '#45B7D1', '#96CEB4',
          '#FFEAA7', '#DDA15E', '#BC6C25', '#C9ADA7', '#9B9B9B']

# グラフ作成
fig = plt.figure(figsize=(16, 12))

# ========================================
# グラフ1: 総合CPIの推移（2015年=100として換算）
# ========================================
ax1 = plt.subplot(2, 2, 1)
ax1.plot(years, cpi_change, marker='o', linewidth=3, markersize=8,
         color='#2C3E50', label='累積変化')
ax1.fill_between(years, 0, cpi_change, alpha=0.3, color='#3498DB')
ax1.axhline(y=0, color='gray', linestyle='--', linewidth=1)
ax1.grid(True, alpha=0.3)
ax1.set_xlabel('年', fontsize=12, fontweight='bold')
ax1.set_ylabel('2015年からの変化（ポイント）', fontsize=12, fontweight='bold')
ax1.set_title('総合消費者物価指数の累積変化\n（2015年基準）', fontsize=14, fontweight='bold', pad=15)
ax1.legend(loc='upper left', fontsize=11)

# データラベルを追加
for i, (year, change) in enumerate(zip(years, cpi_change)):
    if i % 2 == 0 or i == len(years)-1:  # 隔年＋最終年にラベル
        ax1.annotate(f'+{change:.1f}',
                    xy=(year, change),
                    xytext=(0, 10),
                    textcoords='offset points',
                    ha='center',
                    fontsize=10,
                    fontweight='bold')

# 時期区分の背景色
ax1.axvspan(2015, 2019.5, alpha=0.1, color='green', label='安定期')
ax1.axvspan(2019.5, 2021.5, alpha=0.1, color='yellow', label='パンデミック期')
ax1.axvspan(2021.5, 2024, alpha=0.1, color='red', label='急騰期')

# ========================================
# グラフ2: 10大費目別の累積寄与度（横棒グラフ）
# ========================================
ax2 = plt.subplot(2, 2, 2)
y_pos = np.arange(len(categories))
bars = ax2.barh(y_pos, contributions, color=colors, edgecolor='black', linewidth=1.5)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(categories, fontsize=11)
ax2.set_xlabel('累積寄与度（ポイント）', fontsize=12, fontweight='bold')
ax2.set_title('10大費目別の累積寄与度\n（2015-2024年、合計+11.5ポイント）',
              fontsize=14, fontweight='bold', pad=15)
ax2.grid(True, axis='x', alpha=0.3)
ax2.invert_yaxis()

# データラベルを追加
for i, (bar, val, rate) in enumerate(zip(bars, contributions, contribution_rates)):
    ax2.text(val + 0.15, bar.get_y() + bar.get_height()/2,
            f'+{val:.2f} ({rate:.1f}%)',
            va='center', fontsize=10, fontweight='bold')

# ========================================
# グラフ3: 円グラフ（主要項目の寄与率）
# ========================================
ax3 = plt.subplot(2, 2, 3)

# トップ3とその他に集約
top3_labels = ['食料\n(33-37%)', '光熱・水道\n(22-26%)', '教養娯楽\n(10-13%)']
top3_values = [35, 24, 12]
others_value = 29
pie_labels = top3_labels + ['その他7項目\n(29%)']
pie_values = top3_values + [others_value]
pie_colors = ['#FF6B6B', '#FFA500', '#4ECDC4', '#CCCCCC']

wedges, texts, autotexts = ax3.pie(pie_values, labels=pie_labels, colors=pie_colors,
                                     autopct='%1.0f%%', startangle=90,
                                     textprops={'fontsize': 12, 'fontweight': 'bold'},
                                     wedgeprops={'edgecolor': 'black', 'linewidth': 2})

# パーセント表示を太字に
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(13)
    autotext.set_fontweight('bold')

ax3.set_title('物価上昇の寄与率構成\n（トップ3で約70%）',
              fontsize=14, fontweight='bold', pad=15)

# ========================================
# グラフ4: 時期別の累積寄与度（積み上げ棒グラフ）
# ========================================
ax4 = plt.subplot(2, 2, 4)

# 時期別データ（推定）
periods = ['2015-2021年\n安定期', '2022-2024年\n急騰期', '合計\n2015-2024年']
period_food = [0.7, 3.3, 4.0]
period_energy = [0.0, 2.75, 2.75]
period_entertainment = [0.4, 0.95, 1.35]
period_others = [0.5, 2.9, 3.4]

width = 0.6
x_pos = np.arange(len(periods))

# 積み上げ棒グラフ
p1 = ax4.bar(x_pos, period_food, width, label='食料', color='#FF6B6B', edgecolor='black')
p2 = ax4.bar(x_pos, period_energy, width, bottom=period_food,
            label='光熱・水道', color='#FFA500', edgecolor='black')
p3 = ax4.bar(x_pos, period_entertainment, width,
            bottom=np.array(period_food) + np.array(period_energy),
            label='教養娯楽', color='#4ECDC4', edgecolor='black')
p4 = ax4.bar(x_pos, period_others, width,
            bottom=np.array(period_food) + np.array(period_energy) + np.array(period_entertainment),
            label='その他', color='#96CEB4', edgecolor='black')

ax4.set_ylabel('累積寄与度（ポイント）', fontsize=12, fontweight='bold')
ax4.set_title('時期別の累積寄与度\n（費目別内訳）', fontsize=14, fontweight='bold', pad=15)
ax4.set_xticks(x_pos)
ax4.set_xticklabels(periods, fontsize=11)
ax4.legend(loc='upper left', fontsize=10)
ax4.grid(True, axis='y', alpha=0.3)

# 合計値を表示
totals = [sum([period_food[i], period_energy[i], period_entertainment[i], period_others[i]])
          for i in range(len(periods))]
for i, (pos, total) in enumerate(zip(x_pos, totals)):
    ax4.text(pos, total + 0.3, f'+{total:.1f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

# 全体のタイトル
fig.suptitle('2015-2024年 物価水準変化の累積寄与度分析',
             fontsize=18, fontweight='bold', y=0.995)

# 注釈を追加
fig.text(0.5, 0.01,
         '出典: 総務省統計局「消費者物価指数」（2020年基準）を基に作成\n'
         '注: 累積寄与度は推定値を含む。2015年の指数98.2を基準とした2024年（109.5）までの変化を分析。',
         ha='center', fontsize=9, style='italic', color='gray')

plt.tight_layout(rect=[0, 0.03, 1, 0.99])

# 保存
output_path = '物価水準変化の内訳/累積寄与度グラフ.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f'グラフを保存しました: {output_path}')
