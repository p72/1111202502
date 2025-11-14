#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cumulative Contribution Graph Creation Script for Price Level Changes
Visualizing CPI and category-wise contributions from 2015-2024
"""

import matplotlib
matplotlib.use('Agg')  # Backend for non-GUI environment
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Font settings
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Graph settings
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 11

# Data definition
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
cpi_index = [98.2, 98.5, 99.0, 100.0, 100.5, 100.0, 99.8, 102.3, 106.7, 109.5]
cpi_change = [0, 0.3, 0.8, 1.8, 2.3, 1.8, 1.6, 4.2, 8.7, 11.5]  # Cumulative change from 2015

# Cumulative contribution data by 10 major categories (estimated, 2015-2024)
categories = ['Food', 'Utilities', 'Recreation', 'Transport/Comm', 'Housing',
              'Misc.', 'Furniture', 'Clothing', 'Medical', 'Education']
contributions = [4.0, 2.75, 1.35, 1.15, 0.9, 0.8, 0.6, 0.4, 0.4, 0.15]  # points
contribution_rates = [34.8, 23.9, 11.7, 10.0, 7.8, 7.0, 5.2, 3.5, 3.5, 1.3]  # contribution rate (%)

# Color definition
colors = ['#FF6B6B', '#FFA500', '#4ECDC4', '#45B7D1', '#96CEB4',
          '#FFEAA7', '#DDA15E', '#BC6C25', '#C9ADA7', '#9B9B9B']

# Create graphs
fig = plt.figure(figsize=(16, 12))

# ========================================
# Graph 1: Overall CPI Cumulative Change (2015 base)
# ========================================
ax1 = plt.subplot(2, 2, 1)
ax1.plot(years, cpi_change, marker='o', linewidth=3, markersize=8,
         color='#2C3E50', label='Cumulative Change')
ax1.fill_between(years, 0, cpi_change, alpha=0.3, color='#3498DB')
ax1.axhline(y=0, color='gray', linestyle='--', linewidth=1)
ax1.grid(True, alpha=0.3)
ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Change from 2015 (points)', fontsize=12, fontweight='bold')
ax1.set_title('Consumer Price Index Cumulative Change\n(2015 Base)', fontsize=14, fontweight='bold', pad=15)
ax1.legend(loc='upper left', fontsize=11)

# Add data labels
for i, (year, change) in enumerate(zip(years, cpi_change)):
    if i % 2 == 0 or i == len(years)-1:  # Every other year + final year
        ax1.annotate(f'+{change:.1f}',
                    xy=(year, change),
                    xytext=(0, 10),
                    textcoords='offset points',
                    ha='center',
                    fontsize=10,
                    fontweight='bold')

# Period background colors
ax1.axvspan(2015, 2019.5, alpha=0.1, color='green', label='Stable Period')
ax1.axvspan(2019.5, 2021.5, alpha=0.1, color='yellow', label='Pandemic Period')
ax1.axvspan(2021.5, 2024, alpha=0.1, color='red', label='Surge Period')

# ========================================
# Graph 2: Cumulative Contribution by 10 Major Categories
# ========================================
ax2 = plt.subplot(2, 2, 2)
y_pos = np.arange(len(categories))
bars = ax2.barh(y_pos, contributions, color=colors, edgecolor='black', linewidth=1.5)
ax2.set_yticks(y_pos)
ax2.set_yticklabels(categories, fontsize=11)
ax2.set_xlabel('Cumulative Contribution (points)', fontsize=12, fontweight='bold')
ax2.set_title('Cumulative Contribution by 10 Major Categories\n(2015-2024, Total +11.5 points)',
              fontsize=14, fontweight='bold', pad=15)
ax2.grid(True, axis='x', alpha=0.3)
ax2.invert_yaxis()

# Add data labels
for i, (bar, val, rate) in enumerate(zip(bars, contributions, contribution_rates)):
    ax2.text(val + 0.15, bar.get_y() + bar.get_height()/2,
            f'+{val:.2f} ({rate:.1f}%)',
            va='center', fontsize=10, fontweight='bold')

# ========================================
# Graph 3: Pie Chart (Contribution Rate Composition)
# ========================================
ax3 = plt.subplot(2, 2, 3)

# Top 3 and others
top3_labels = ['Food\n(33-37%)', 'Utilities\n(22-26%)', 'Recreation\n(10-13%)']
top3_values = [35, 24, 12]
others_value = 29
pie_labels = top3_labels + ['Other 7 Items\n(29%)']
pie_values = top3_values + [others_value]
pie_colors = ['#FF6B6B', '#FFA500', '#4ECDC4', '#CCCCCC']

wedges, texts, autotexts = ax3.pie(pie_values, labels=pie_labels, colors=pie_colors,
                                     autopct='%1.0f%%', startangle=90,
                                     textprops={'fontsize': 12, 'fontweight': 'bold'},
                                     wedgeprops={'edgecolor': 'black', 'linewidth': 2})

# Bold percentage display
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontsize(13)
    autotext.set_fontweight('bold')

ax3.set_title('Contribution Rate Composition\n(Top 3: ~70%)',
              fontsize=14, fontweight='bold', pad=15)

# ========================================
# Graph 4: Cumulative Contribution by Period (Stacked Bar)
# ========================================
ax4 = plt.subplot(2, 2, 4)

# Period data (estimated)
periods = ['2015-2021\nStable', '2022-2024\nSurge', 'Total\n2015-2024']
period_food = [0.7, 3.3, 4.0]
period_energy = [0.0, 2.75, 2.75]
period_entertainment = [0.4, 0.95, 1.35]
period_others = [0.5, 2.9, 3.4]

width = 0.6
x_pos = np.arange(len(periods))

# Stacked bar chart
p1 = ax4.bar(x_pos, period_food, width, label='Food', color='#FF6B6B', edgecolor='black')
p2 = ax4.bar(x_pos, period_energy, width, bottom=period_food,
            label='Utilities', color='#FFA500', edgecolor='black')
p3 = ax4.bar(x_pos, period_entertainment, width,
            bottom=np.array(period_food) + np.array(period_energy),
            label='Recreation', color='#4ECDC4', edgecolor='black')
p4 = ax4.bar(x_pos, period_others, width,
            bottom=np.array(period_food) + np.array(period_energy) + np.array(period_entertainment),
            label='Others', color='#96CEB4', edgecolor='black')

ax4.set_ylabel('Cumulative Contribution (points)', fontsize=12, fontweight='bold')
ax4.set_title('Cumulative Contribution by Period\n(By Category)', fontsize=14, fontweight='bold', pad=15)
ax4.set_xticks(x_pos)
ax4.set_xticklabels(periods, fontsize=11)
ax4.legend(loc='upper left', fontsize=10)
ax4.grid(True, axis='y', alpha=0.3)

# Display total values
totals = [sum([period_food[i], period_energy[i], period_entertainment[i], period_others[i]])
          for i in range(len(periods))]
for i, (pos, total) in enumerate(zip(x_pos, totals)):
    ax4.text(pos, total + 0.3, f'+{total:.1f}',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

# Overall title
fig.suptitle('Japan Price Level Change: Cumulative Contribution Analysis 2015-2024',
             fontsize=18, fontweight='bold', y=0.995)

# Footnote
fig.text(0.5, 0.01,
         'Source: Statistics Bureau of Japan "Consumer Price Index" (2020 base)\n'
         'Note: Cumulative contributions include estimated values. Analysis based on 2015 index (98.2) to 2024 (109.5).',
         ha='center', fontsize=9, style='italic', color='gray')

plt.tight_layout(rect=[0, 0.03, 1, 0.99])

# Save
output_path = '物価水準変化の内訳/cumulative_contribution_graph.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f'Graph saved: {output_path}')
