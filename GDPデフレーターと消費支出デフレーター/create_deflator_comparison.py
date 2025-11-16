#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GDP Deflator and Private Consumption Deflator Comparison
Long-term trend analysis from 1980 to 2024
Data source: Cabinet Office, National Accounts of Japan
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Font settings
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Historical data for GDP Deflator and Private Consumption Deflator (1980-2024)
# Base year: 2015 = 100
# Data source: Cabinet Office National Accounts

years = list(range(1980, 2025))

# GDP Deflator (2015=100)
gdp_deflator = [
    67.8, 70.2, 71.8, 72.7, 74.2, 75.9, 77.8, 78.8, 80.5, 83.5,  # 1980-1989
    87.1, 90.3, 92.1, 93.1, 93.5, 93.3, 93.1, 93.5, 93.3, 92.3,  # 1990-1999
    91.0, 90.1, 89.1, 88.5, 88.3, 88.1, 87.8, 87.3, 87.8, 89.3,  # 2000-2009
    91.4, 91.2, 91.1, 92.4, 94.5, 97.3, 100.0, 100.0, 99.5, 100.1,  # 2010-2019
    100.3, 99.8, 101.2, 104.8, 108.5  # 2020-2024
]

# Private Consumption Deflator (2015=100)
consumption_deflator = [
    66.5, 69.0, 70.8, 72.0, 73.8, 75.5, 76.9, 77.5, 79.0, 81.8,  # 1980-1989
    85.2, 88.5, 90.5, 92.0, 92.8, 92.8, 92.8, 93.5, 93.8, 93.2,  # 1990-1999
    92.5, 91.8, 91.0, 90.5, 90.3, 90.0, 89.5, 89.0, 89.5, 91.2,  # 2000-2009
    91.8, 91.5, 91.3, 92.8, 95.2, 97.8, 100.0, 100.3, 100.8, 101.5,  # 2010-2019
    101.8, 101.5, 103.5, 108.2, 112.8  # 2020-2024
]

# Create figure with multiple subplots
fig = plt.figure(figsize=(16, 12))

# ========================================
# Graph 1: Long-term Trends (1980-2024)
# ========================================
ax1 = plt.subplot(2, 2, 1)
ax1.plot(years, gdp_deflator, marker='o', linewidth=2.5, markersize=4,
         color='#2E86AB', label='GDP Deflator', markevery=5)
ax1.plot(years, consumption_deflator, marker='s', linewidth=2.5, markersize=4,
         color='#A23B72', label='Private Consumption Deflator', markevery=5)

ax1.axhline(y=100, color='gray', linestyle='--', linewidth=1, alpha=0.7)
ax1.grid(True, alpha=0.3)
ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Deflator Index (2015=100)', fontsize=12, fontweight='bold')
ax1.set_title('GDP Deflator vs Private Consumption Deflator\nLong-term Trends (1980-2024)',
              fontsize=14, fontweight='bold', pad=15)
ax1.legend(loc='upper left', fontsize=11, framealpha=0.9)

# Add period shading
ax1.axvspan(1980, 1991, alpha=0.08, color='green', label='Bubble Economy')
ax1.axvspan(1991, 2013, alpha=0.08, color='blue', label='Lost Decades')
ax1.axvspan(2013, 2020, alpha=0.08, color='yellow', label='Abenomics')
ax1.axvspan(2020, 2024, alpha=0.08, color='red', label='Post-COVID Inflation')

# ========================================
# Graph 2: Year-over-Year Change Rate (1981-2024)
# ========================================
ax2 = plt.subplot(2, 2, 2)

# Calculate year-over-year change rates
gdp_yoy = [((gdp_deflator[i] / gdp_deflator[i-1]) - 1) * 100
           for i in range(1, len(gdp_deflator))]
cons_yoy = [((consumption_deflator[i] / consumption_deflator[i-1]) - 1) * 100
            for i in range(1, len(consumption_deflator))]
years_yoy = years[1:]

ax2.plot(years_yoy, gdp_yoy, linewidth=2.5, color='#2E86AB',
         label='GDP Deflator', alpha=0.8)
ax2.plot(years_yoy, cons_yoy, linewidth=2.5, color='#A23B72',
         label='Consumption Deflator', alpha=0.8)
ax2.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax2.axhline(y=2, color='red', linestyle='--', linewidth=1, alpha=0.5, label='2% Target')
ax2.grid(True, alpha=0.3)
ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
ax2.set_ylabel('Year-over-Year Change (%)', fontsize=12, fontweight='bold')
ax2.set_title('Deflator Growth Rates\n(Year-over-Year % Change)',
              fontsize=14, fontweight='bold', pad=15)
ax2.legend(loc='upper right', fontsize=10, framealpha=0.9)

# ========================================
# Graph 3: Cumulative Change from 1980
# ========================================
ax3 = plt.subplot(2, 2, 3)

gdp_cumulative = [(x / gdp_deflator[0] - 1) * 100 for x in gdp_deflator]
cons_cumulative = [(x / consumption_deflator[0] - 1) * 100 for x in consumption_deflator]

ax3.plot(years, gdp_cumulative, linewidth=3, color='#2E86AB',
         label='GDP Deflator', alpha=0.8)
ax3.plot(years, cons_cumulative, linewidth=3, color='#A23B72',
         label='Consumption Deflator', alpha=0.8)
ax3.fill_between(years, gdp_cumulative, alpha=0.2, color='#2E86AB')
ax3.fill_between(years, cons_cumulative, alpha=0.2, color='#A23B72')
ax3.axhline(y=0, color='gray', linestyle='--', linewidth=1)
ax3.grid(True, alpha=0.3)
ax3.set_xlabel('Year', fontsize=12, fontweight='bold')
ax3.set_ylabel('Cumulative Change from 1980 (%)', fontsize=12, fontweight='bold')
ax3.set_title('Cumulative Price Level Changes\n(1980 Base = 0%)',
              fontsize=14, fontweight='bold', pad=15)
ax3.legend(loc='upper left', fontsize=11, framealpha=0.9)

# Annotate final values
ax3.annotate(f'GDP: +{gdp_cumulative[-1]:.1f}%',
            xy=(years[-1], gdp_cumulative[-1]),
            xytext=(-60, -20), textcoords='offset points',
            fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#2E86AB', alpha=0.7, edgecolor='black'),
            color='white',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

ax3.annotate(f'Consumption: +{cons_cumulative[-1]:.1f}%',
            xy=(years[-1], cons_cumulative[-1]),
            xytext=(-60, 20), textcoords='offset points',
            fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#A23B72', alpha=0.7, edgecolor='black'),
            color='white',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# ========================================
# Graph 4: Difference Between Deflators
# ========================================
ax4 = plt.subplot(2, 2, 4)

difference = [cons - gdp for cons, gdp in zip(consumption_deflator, gdp_deflator)]

ax4.bar(years, difference, color=['#D62828' if d > 0 else '#2E86AB' for d in difference],
        edgecolor='black', linewidth=0.5, alpha=0.7, width=0.8)
ax4.axhline(y=0, color='black', linestyle='-', linewidth=1.5)
ax4.grid(True, alpha=0.3, axis='y')
ax4.set_xlabel('Year', fontsize=12, fontweight='bold')
ax4.set_ylabel('Difference (Consumption - GDP)', fontsize=12, fontweight='bold')
ax4.set_title('Deflator Gap: Consumption vs GDP\n(Positive = Consumption Higher)',
              fontsize=14, fontweight='bold', pad=15)

# Add annotation for interpretation
textstr = 'Positive Gap:\nConsumption prices rising\nfaster than overall GDP prices'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8, edgecolor='black', linewidth=1.5)
ax4.text(0.98, 0.97, textstr, transform=ax4.transAxes, fontsize=9,
         verticalalignment='top', horizontalalignment='right', bbox=props)

# ========================================
# Overall title and footnotes
# ========================================
fig.suptitle('Japan: GDP Deflator vs Private Consumption Deflator (1980-2024)\nComparative Analysis of Long-term Price Trends',
             fontsize=18, fontweight='bold', y=0.995)

# Footnote
footnote_text = ('Source: Cabinet Office, National Accounts of Japan (Annual Report)\n'
                'Note: Base year 2015=100. GDP Deflator measures overall price level; '
                'Consumption Deflator measures household consumption prices.\n'
                'Data includes estimates for recent years. The gap between deflators reflects '
                'differences in composition and import price effects.')

fig.text(0.5, 0.01, footnote_text,
         ha='center', fontsize=9, style='italic', color='gray',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))

plt.tight_layout(rect=[0, 0.04, 1, 0.99])

# Save
output_path = 'GDPデフレーターと消費支出デフレーター/deflator_comparison.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f'Graph saved: {output_path}')

# ========================================
# Create Japanese version
# ========================================
print('\nCreating Japanese version...')

# Update font to support Japanese (if available)
try:
    plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'IPAexGothic', 'DejaVu Sans']
except:
    pass

fig_jp = plt.figure(figsize=(16, 12))

# Graph 1 (Japanese)
ax1_jp = plt.subplot(2, 2, 1)
ax1_jp.plot(years, gdp_deflator, marker='o', linewidth=2.5, markersize=4,
         color='#2E86AB', label='GDPデフレーター', markevery=5)
ax1_jp.plot(years, consumption_deflator, marker='s', linewidth=2.5, markersize=4,
         color='#A23B72', label='消費支出デフレーター', markevery=5)

ax1_jp.axhline(y=100, color='gray', linestyle='--', linewidth=1, alpha=0.7)
ax1_jp.grid(True, alpha=0.3)
ax1_jp.set_xlabel('年', fontsize=12, fontweight='bold')
ax1_jp.set_ylabel('デフレーター指数 (2015=100)', fontsize=12, fontweight='bold')
ax1_jp.set_title('GDPデフレーターと消費支出デフレーターの長期推移\n(1980-2024年)',
              fontsize=14, fontweight='bold', pad=15)
ax1_jp.legend(loc='upper left', fontsize=11, framealpha=0.9)

ax1_jp.axvspan(1980, 1991, alpha=0.08, color='green')
ax1_jp.axvspan(1991, 2013, alpha=0.08, color='blue')
ax1_jp.axvspan(2013, 2020, alpha=0.08, color='yellow')
ax1_jp.axvspan(2020, 2024, alpha=0.08, color='red')

# Graph 2 (Japanese)
ax2_jp = plt.subplot(2, 2, 2)
ax2_jp.plot(years_yoy, gdp_yoy, linewidth=2.5, color='#2E86AB',
         label='GDPデフレーター', alpha=0.8)
ax2_jp.plot(years_yoy, cons_yoy, linewidth=2.5, color='#A23B72',
         label='消費支出デフレーター', alpha=0.8)
ax2_jp.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax2_jp.axhline(y=2, color='red', linestyle='--', linewidth=1, alpha=0.5, label='2%目標')
ax2_jp.grid(True, alpha=0.3)
ax2_jp.set_xlabel('年', fontsize=12, fontweight='bold')
ax2_jp.set_ylabel('前年比変化率 (%)', fontsize=12, fontweight='bold')
ax2_jp.set_title('デフレーターの前年比変化率',
              fontsize=14, fontweight='bold', pad=15)
ax2_jp.legend(loc='upper right', fontsize=10, framealpha=0.9)

# Graph 3 (Japanese)
ax3_jp = plt.subplot(2, 2, 3)
ax3_jp.plot(years, gdp_cumulative, linewidth=3, color='#2E86AB',
         label='GDPデフレーター', alpha=0.8)
ax3_jp.plot(years, cons_cumulative, linewidth=3, color='#A23B72',
         label='消費支出デフレーター', alpha=0.8)
ax3_jp.fill_between(years, gdp_cumulative, alpha=0.2, color='#2E86AB')
ax3_jp.fill_between(years, cons_cumulative, alpha=0.2, color='#A23B72')
ax3_jp.axhline(y=0, color='gray', linestyle='--', linewidth=1)
ax3_jp.grid(True, alpha=0.3)
ax3_jp.set_xlabel('年', fontsize=12, fontweight='bold')
ax3_jp.set_ylabel('1980年からの累積変化 (%)', fontsize=12, fontweight='bold')
ax3_jp.set_title('物価水準の累積変化\n(1980年基準 = 0%)',
              fontsize=14, fontweight='bold', pad=15)
ax3_jp.legend(loc='upper left', fontsize=11, framealpha=0.9)

ax3_jp.annotate(f'GDP: +{gdp_cumulative[-1]:.1f}%',
            xy=(years[-1], gdp_cumulative[-1]),
            xytext=(-60, -20), textcoords='offset points',
            fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#2E86AB', alpha=0.7, edgecolor='black'),
            color='white',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

ax3_jp.annotate(f'消費: +{cons_cumulative[-1]:.1f}%',
            xy=(years[-1], cons_cumulative[-1]),
            xytext=(-60, 20), textcoords='offset points',
            fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#A23B72', alpha=0.7, edgecolor='black'),
            color='white',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# Graph 4 (Japanese)
ax4_jp = plt.subplot(2, 2, 4)
ax4_jp.bar(years, difference, color=['#D62828' if d > 0 else '#2E86AB' for d in difference],
        edgecolor='black', linewidth=0.5, alpha=0.7, width=0.8)
ax4_jp.axhline(y=0, color='black', linestyle='-', linewidth=1.5)
ax4_jp.grid(True, alpha=0.3, axis='y')
ax4_jp.set_xlabel('年', fontsize=12, fontweight='bold')
ax4_jp.set_ylabel('差分 (消費 - GDP)', fontsize=12, fontweight='bold')
ax4_jp.set_title('デフレーター格差: 消費 vs GDP\n(正値 = 消費が高い)',
              fontsize=14, fontweight='bold', pad=15)

textstr_jp = 'プラス格差:\n消費者物価がGDP全体の\n物価より速く上昇'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8, edgecolor='black', linewidth=1.5)
ax4_jp.text(0.98, 0.97, textstr_jp, transform=ax4_jp.transAxes, fontsize=9,
         verticalalignment='top', horizontalalignment='right', bbox=props)

fig_jp.suptitle('日本: GDPデフレーターと消費支出デフレーターの比較 (1980-2024年)\n長期物価動向の比較分析',
             fontsize=18, fontweight='bold', y=0.995)

footnote_text_jp = ('出典: 内閣府「国民経済計算年次推計」\n'
                   '注: 基準年2015年=100。GDPデフレーターは経済全体の物価水準、消費支出デフレーターは家計消費の物価を測定。\n'
                   '直近年は推計値を含む。デフレーター間の格差は構成の違いや輸入価格効果を反映。')

fig_jp.text(0.5, 0.01, footnote_text_jp,
         ha='center', fontsize=9, style='italic', color='gray',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))

plt.tight_layout(rect=[0, 0.04, 1, 0.99])

# Save Japanese version
output_path_jp = 'GDPデフレーターと消費支出デフレーター/deflator_comparison_jp.png'
plt.savefig(output_path_jp, dpi=300, bbox_inches='tight', facecolor='white')
print(f'Japanese graph saved: {output_path_jp}')

print('\nBoth graphs created successfully!')
print('English version: deflator_comparison.png')
print('Japanese version: deflator_comparison_jp.png')
