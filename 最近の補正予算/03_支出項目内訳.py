import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

# FY2024 Supplementary Budget Breakdown (¥13.9T total)
categories = [
    'Public-Private\nInvestment',
    'Price Support\nMeasures',
    'Disaster Prevention &\nNational Resilience',
    'Semiconductor &\nTech Support',
    'Other Measures'
]
amounts = [3.5, 4.2, 2.8, 2.1, 1.3]  # trillion yen (estimated based on available data)
colors = ['#3498DB', '#E74C3C', '#F39C12', '#9B59B6', '#95A5A6']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Left: Horizontal bar chart
y_pos = np.arange(len(categories))
bars = ax1.barh(y_pos, amounts, color=colors, edgecolor='black', linewidth=1.5, alpha=0.85)

# Add value labels
for i, (bar, amount) in enumerate(zip(bars, amounts)):
    ax1.text(amount + 0.1, bar.get_y() + bar.get_height()/2,
             f'¥{amount:.1f}T', va='center', fontsize=11, fontweight='bold')

ax1.set_yticks(y_pos)
ax1.set_yticklabels(categories, fontsize=11)
ax1.set_xlabel('Amount (Trillion Yen)', fontsize=13, fontweight='bold')
ax1.set_title('FY2024 Supplementary Budget Breakdown\n令和6年度補正予算の内訳',
              fontsize=14, fontweight='bold', pad=20)
ax1.grid(axis='x', alpha=0.3, linestyle='--')
ax1.set_xlim(0, max(amounts) * 1.2)

# Right: Comparison across three years
years = ['FY2022\n(2nd)', 'FY2023', 'FY2024']
price_support = [8.5, 4.8, 4.2]
investment = [12.3, 4.2, 3.5]
disaster = [5.1, 2.1, 2.8]
other = [3.0, 2.1, 3.4]

x = np.arange(len(years))
width = 0.6

bottom1 = np.zeros(len(years))
colors_stack = ['#E74C3C', '#3498DB', '#F39C12', '#95A5A6']
labels = ['Price Support', 'Investment', 'Disaster Prevention', 'Other']
data = [price_support, investment, disaster, other]

for i, (d, color, label) in enumerate(zip(data, colors_stack, labels)):
    ax2.bar(x, d, width, bottom=bottom1, label=label, color=color,
            alpha=0.85, edgecolor='black', linewidth=1.5)
    bottom1 += d

ax2.set_ylabel('Amount (Trillion Yen)', fontsize=13, fontweight='bold')
ax2.set_xlabel('Fiscal Year', fontsize=13, fontweight='bold')
ax2.set_title('Supplementary Budget Composition Trends\n補正予算の構成推移',
              fontsize=14, fontweight='bold', pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(years)
ax2.legend(loc='upper right', fontsize=10)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Add total labels
for i, (year_total) in enumerate([28.9, 13.2, 13.9]):
    ax2.text(i, year_total + 0.5, f'Total:\n¥{year_total}T',
             ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('/home/user/1111202502/最近の補正予算/03_支出項目内訳.png', dpi=300, bbox_inches='tight')
print("Graph saved: 03_支出項目内訳.png")
