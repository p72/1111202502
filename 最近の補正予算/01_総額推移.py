import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

# Data for supplementary budgets (FY2016-2024)
years = ['FY2016', 'FY2017', 'FY2018', 'FY2019', 'FY2020\n1st', 'FY2020\n2nd', 'FY2020\n3rd',
         'FY2021', 'FY2022\n1st', 'FY2022\n2nd', 'FY2023', 'FY2024']
amounts = [2.7, 2.7, 2.4, 4.5, 25.7, 31.9, 15.4, 35.9, 2.7, 28.9, 13.2, 13.9]  # in trillion yen

# Color coding: Red for COVID era (2020-2021), Blue for others
colors = ['#4A90E2'] * 4 + ['#E74C3C'] * 4 + ['#4A90E2'] * 4

fig, ax = plt.subplots(figsize=(14, 8))

bars = ax.bar(years, amounts, color=colors, edgecolor='black', linewidth=1.5, alpha=0.8)

# Add value labels on bars
for i, (bar, amount) in enumerate(zip(bars, amounts)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'¥{amount:.1f}T',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

# Styling
ax.set_ylabel('Amount (Trillion Yen)', fontsize=14, fontweight='bold')
ax.set_xlabel('Fiscal Year', fontsize=14, fontweight='bold')
ax.set_title('Supplementary Budget Trends (FY2016-2024)',
             fontsize=16, fontweight='bold', pad=20)
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_ylim(0, max(amounts) * 1.15)

# Add legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#E74C3C', alpha=0.8, label='COVID-19 Era (2020-2021)'),
                   Patch(facecolor='#4A90E2', alpha=0.8, label='Other Years')]
ax.legend(handles=legend_elements, loc='upper left', fontsize=11)

# Add average line for recent years (excluding COVID peak)
recent_avg = np.mean([2.7, 28.9, 13.2, 13.9])
ax.axhline(y=recent_avg, color='green', linestyle='--', linewidth=2, alpha=0.6,
           label=f'Recent Avg (FY2022-2024): ¥{recent_avg:.1f}T')

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('/home/user/1111202502/最近の補正予算/01_総額推移.png', dpi=300, bbox_inches='tight')
print("Graph saved: 01_総額推移.png")
