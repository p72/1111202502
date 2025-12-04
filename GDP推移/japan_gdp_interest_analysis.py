#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日本の名目GDPと長期金利の推移分析
Japan's Nominal GDP and Long-term Interest Rate Analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from datetime import datetime

# 日本語フォントの設定
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 日本の名目GDP データ（兆円）
# データソース: 内閣府 国民経済計算
gdp_data = {
    '年度': [1980, 1985, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999,
            2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
            2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021,
            2022, 2023, 2024],
    '名目GDP': [249.4, 338.6, 452.6, 476.7, 485.7, 491.7, 497.9, 505.7, 518.3, 526.0,
               512.4, 507.2, 524.3, 519.5, 515.8, 521.1, 531.9, 542.4, 553.1, 560.8,
               543.4, 521.0, 539.3, 537.8, 546.6, 561.4, 573.6, 583.8, 596.5, 606.3,
               615.8, 625.2, 610.4, 631.8, 648.5, 665.3, 680.5]
}

# 日本の長期金利データ（10年国債利回り、%）
# データソース: 財務省、日本銀行
interest_rate_data = {
    '年度': [1980, 1985, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999,
            2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
            2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021,
            2022, 2023, 2024],
    '長期金利': [9.22, 6.34, 7.36, 6.35, 5.35, 4.29, 4.51, 3.45, 3.10, 2.36, 1.49, 1.75,
                1.76, 1.33, 1.27, 1.00, 1.50, 1.39, 1.74, 1.68, 1.47, 1.35, 1.18,
                1.12, 0.86, 0.72, 0.55, 0.36, -0.02, 0.07, 0.09, -0.01, 0.03, 0.10,
                0.23, 0.61, 1.15]
}

# DataFrameの作成
df_gdp = pd.DataFrame(gdp_data)
df_interest = pd.DataFrame(interest_rate_data)

# データの結合
df = pd.merge(df_gdp, df_interest, on='年度')

# CSVファイルとして保存
df.to_csv('GDP推移/japan_gdp_interest_data.csv', index=False, encoding='utf-8-sig')
print("データファイルを保存しました: japan_gdp_interest_data.csv")

# 統計情報の計算
gdp_growth = ((df['名目GDP'].iloc[-1] / df['名目GDP'].iloc[0]) - 1) * 100
avg_interest = df['長期金利'].mean()
max_gdp_year = df.loc[df['名目GDP'].idxmax(), '年度']
max_gdp_value = df['名目GDP'].max()
min_interest_year = df.loc[df['長期金利'].idxmin(), '年度']
min_interest_value = df['長期金利'].min()

# グラフの作成
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12))
fig.suptitle('日本の名目GDPと長期金利の推移 (1980-2024)', fontsize=16, fontweight='bold')

# グラフ1: 名目GDPの推移
ax1.plot(df['年度'], df['名目GDP'], linewidth=2.5, color='#2E86AB', marker='o', markersize=4)
ax1.fill_between(df['年度'], df['名目GDP'], alpha=0.3, color='#2E86AB')
ax1.set_xlabel('年度', fontsize=12, fontweight='bold')
ax1.set_ylabel('名目GDP (兆円)', fontsize=12, fontweight='bold')
ax1.set_title('名目GDPの推移', fontsize=14, fontweight='bold', pad=15)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.axhline(y=df['名目GDP'].mean(), color='red', linestyle='--',
           label=f'平均: {df["名目GDP"].mean():.1f}兆円', alpha=0.7)

# 重要な時期をマーク
ax1.axvspan(1991, 2002, alpha=0.1, color='red', label='失われた10年')
ax1.axvspan(2008, 2009, alpha=0.1, color='orange', label='リーマンショック')
ax1.axvspan(2020, 2020, alpha=0.1, color='purple', label='COVID-19')
ax1.legend(loc='upper left', fontsize=10)

# グラフ2: 長期金利の推移
ax2.plot(df['年度'], df['長期金利'], linewidth=2.5, color='#A23B72', marker='s', markersize=4)
ax2.fill_between(df['年度'], df['長期金利'], alpha=0.3, color='#A23B72')
ax2.set_xlabel('年度', fontsize=12, fontweight='bold')
ax2.set_ylabel('長期金利 (%)', fontsize=12, fontweight='bold')
ax2.set_title('長期金利(10年国債利回り)の推移', fontsize=14, fontweight='bold', pad=15)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax2.axhline(y=df['長期金利'].mean(), color='red', linestyle='--',
           label=f'平均: {df["長期金利"].mean():.2f}%', alpha=0.7)

# マイナス金利の期間をハイライト
negative_rates = df[df['長期金利'] < 0]
if not negative_rates.empty:
    ax2.axhspan(-0.1, 0, alpha=0.2, color='blue', label='マイナス金利期間')

ax2.legend(loc='upper right', fontsize=10)

# グラフ3: GDPと長期金利の相関（2軸グラフ）
ax3_twin = ax3.twinx()
line1 = ax3.plot(df['年度'], df['名目GDP'], linewidth=2.5, color='#2E86AB',
                marker='o', markersize=3, label='名目GDP')
line2 = ax3_twin.plot(df['年度'], df['長期金利'], linewidth=2.5, color='#A23B72',
                     marker='s', markersize=3, label='長期金利')

ax3.set_xlabel('年度', fontsize=12, fontweight='bold')
ax3.set_ylabel('名目GDP (兆円)', fontsize=12, fontweight='bold', color='#2E86AB')
ax3_twin.set_ylabel('長期金利 (%)', fontsize=12, fontweight='bold', color='#A23B72')
ax3.set_title('名目GDPと長期金利の相関', fontsize=14, fontweight='bold', pad=15)
ax3.grid(True, alpha=0.3, linestyle='--')

# 凡例の統合
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax3.legend(lines, labels, loc='upper left', fontsize=10)

ax3.tick_params(axis='y', labelcolor='#2E86AB')
ax3_twin.tick_params(axis='y', labelcolor='#A23B72')

plt.tight_layout()
plt.savefig('GDP推移/japan_gdp_interest_trends.png', dpi=300, bbox_inches='tight')
print("グラフを保存しました: japan_gdp_interest_trends.png")

# 追加のグラフ: 成長率と金利変化率
fig2, (ax4, ax5) = plt.subplots(2, 1, figsize=(14, 10))
fig2.suptitle('成長率と金利変化率の分析 (1980-2024)', fontsize=16, fontweight='bold')

# GDP成長率の計算
df['GDP成長率'] = df['名目GDP'].pct_change() * 100

# 金利変化の計算
df['金利変化'] = df['長期金利'].diff()

# グラフ4: GDP成長率
ax4.bar(df['年度'][1:], df['GDP成長率'][1:], color=['green' if x > 0 else 'red'
        for x in df['GDP成長率'][1:]], alpha=0.7, edgecolor='black', linewidth=0.5)
ax4.set_xlabel('年度', fontsize=12, fontweight='bold')
ax4.set_ylabel('GDP成長率 (%)', fontsize=12, fontweight='bold')
ax4.set_title('名目GDP成長率（前年比）', fontsize=14, fontweight='bold', pad=15)
ax4.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax4.grid(True, alpha=0.3, linestyle='--', axis='y')

# グラフ5: 金利変化
ax5.bar(df['年度'][1:], df['金利変化'][1:], color=['blue' if x < 0 else 'orange'
        for x in df['金利変化'][1:]], alpha=0.7, edgecolor='black', linewidth=0.5)
ax5.set_xlabel('年度', fontsize=12, fontweight='bold')
ax5.set_ylabel('金利変化 (ポイント)', fontsize=12, fontweight='bold')
ax5.set_title('長期金利の前年差', fontsize=14, fontweight='bold', pad=15)
ax5.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax5.grid(True, alpha=0.3, linestyle='--', axis='y')

plt.tight_layout()
plt.savefig('GDP推移/japan_gdp_interest_changes.png', dpi=300, bbox_inches='tight')
print("グラフを保存しました: japan_gdp_interest_changes.png")

# 散布図: GDPと金利の関係
fig3, ax6 = plt.subplots(figsize=(12, 8))

# 時期別に色分け
periods = [
    (df['年度'] <= 1990, '1980-1990', '#FF6B6B'),
    ((df['年度'] > 1990) & (df['年度'] <= 2000), '1991-2000', '#4ECDC4'),
    ((df['年度'] > 2000) & (df['年度'] <= 2010), '2001-2010', '#45B7D1'),
    ((df['年度'] > 2010) & (df['年度'] <= 2020), '2011-2020', '#FFA07A'),
    (df['年度'] > 2020, '2021-2024', '#98D8C8')
]

for condition, label, color in periods:
    mask = condition
    ax6.scatter(df.loc[mask, '名目GDP'], df.loc[mask, '長期金利'],
               s=100, alpha=0.6, c=color, label=label, edgecolors='black', linewidth=1)

ax6.set_xlabel('名目GDP (兆円)', fontsize=12, fontweight='bold')
ax6.set_ylabel('長期金利 (%)', fontsize=12, fontweight='bold')
ax6.set_title('名目GDPと長期金利の関係（時期別）', fontsize=14, fontweight='bold', pad=15)
ax6.grid(True, alpha=0.3, linestyle='--')
ax6.legend(loc='upper right', fontsize=10)

# 相関係数の計算と表示
correlation = df['名目GDP'].corr(df['長期金利'])
ax6.text(0.05, 0.95, f'相関係数: {correlation:.3f}',
        transform=ax6.transAxes, fontsize=12, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('GDP推移/japan_gdp_interest_correlation.png', dpi=300, bbox_inches='tight')
print("グラフを保存しました: japan_gdp_interest_correlation.png")

# 統計レポートの作成
print("\n" + "="*60)
print("日本の名目GDPと長期金利 - 統計サマリー")
print("="*60)
print(f"\n【分析期間】 {int(df['年度'].min())}年 ～ {int(df['年度'].max())}年")
print(f"\n【名目GDP】")
print(f"  期初 ({int(df['年度'].min())}年): {df['名目GDP'].iloc[0]:.1f} 兆円")
print(f"  期末 ({int(df['年度'].max())}年): {df['名目GDP'].iloc[-1]:.1f} 兆円")
print(f"  増加額: {df['名目GDP'].iloc[-1] - df['名目GDP'].iloc[0]:.1f} 兆円")
print(f"  増加率: {gdp_growth:.1f}%")
print(f"  最大値: {max_gdp_value:.1f} 兆円 ({int(max_gdp_year)}年)")
print(f"  平均値: {df['名目GDP'].mean():.1f} 兆円")
print(f"\n【長期金利】")
print(f"  期初 ({int(df['年度'].min())}年): {df['長期金利'].iloc[0]:.2f}%")
print(f"  期末 ({int(df['年度'].max())}年): {df['長期金利'].iloc[-1]:.2f}%")
print(f"  変化: {df['長期金利'].iloc[-1] - df['長期金利'].iloc[0]:.2f} ポイント")
print(f"  最高値: {df['長期金利'].max():.2f}% ({int(df.loc[df['長期金利'].idxmax(), '年度'])}年)")
print(f"  最低値: {min_interest_value:.2f}% ({int(min_interest_year)}年)")
print(f"  平均値: {avg_interest:.2f}%")
print(f"\n【相関分析】")
print(f"  GDPと金利の相関係数: {correlation:.3f}")
if abs(correlation) > 0.7:
    strength = "強い"
elif abs(correlation) > 0.4:
    strength = "中程度の"
else:
    strength = "弱い"
direction = "正" if correlation > 0 else "負"
print(f"  解釈: {strength}{direction}の相関")
print("\n" + "="*60)

print("\n分析完了！以下のファイルが生成されました:")
print("  1. japan_gdp_interest_data.csv - データファイル")
print("  2. japan_gdp_interest_trends.png - 推移グラフ")
print("  3. japan_gdp_interest_changes.png - 成長率・変化率グラフ")
print("  4. japan_gdp_interest_correlation.png - 相関分析グラフ")
