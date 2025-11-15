import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

# Major funds established through supplementary budgets
fund_names = [
    'Semiconductor &\nDigital Industry\nSupport Fund',
    'GX (Green\nTransformation)\nFund',
    'Education DX\nFund',
    'Child & Family\nSupport Fund',
    'Innovation\nPromotion Fund',
    'Space Strategy\nFund',
    'Other Funds'
]

# Estimated amounts (trillion yen)
fund_amounts = [2.0, 1.5, 1.0, 0.8, 0.7, 0.5, 1.2]
fund_colors = ['#9B59B6', '#27AE60', '#3498DB', '#E67E22', '#E74C3C', '#34495E', '#95A5A6']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Left: Pie chart of fund allocation
wedges, texts, autotexts = ax1.pie(fund_amounts, labels=fund_names,
                                     autopct=lambda pct: f'{pct:.1f}%\n(¥{pct*sum(fund_amounts)/100:.2f}T)',
                                     colors=fund_colors, startangle=45,
                                     textprops={'fontsize': 9, 'fontweight': 'bold'})
ax1.set_title('Major Funds Established Through Supplementary Budgets',
              fontsize=14, fontweight='bold', pad=20)

# Right: Fund characteristics - execution timeline
fund_types = ['Annual\nExecution', 'Multi-Year\nFund', 'Long-Term\nFund']
fund_counts = [12, 25, 18]  # Number of funds in each category
avg_size = [0.3, 0.8, 1.5]  # Average size in trillion yen

x = np.arange(len(fund_types))
width = 0.35

fig2, ax2 = plt.subplots(figsize=(8, 7))

# Create twin axis
ax2_twin = ax2.twinx()

bars1 = ax2.bar(x - width/2, fund_counts, width, label='Number of Funds',
                color='#3498DB', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax2_twin.bar(x + width/2, avg_size, width, label='Avg Size (¥T)',
                     color='#E74C3C', alpha=0.8, edgecolor='black', linewidth=1.5)

# Add value labels
for bar, count in zip(bars1, fund_counts):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(count)}', ha='center', va='bottom', fontsize=11, fontweight='bold')

for bar, size in zip(bars2, avg_size):
    height = bar.get_height()
    ax2_twin.text(bar.get_x() + bar.get_width()/2., height,
                  f'¥{size:.1f}T', ha='center', va='bottom', fontsize=11, fontweight='bold')

ax2.set_ylabel('Number of Funds', fontsize=13, fontweight='bold', color='#3498DB')
ax2_twin.set_ylabel('Average Size (Trillion Yen)', fontsize=13, fontweight='bold', color='#E74C3C')
ax2.set_xlabel('Fund Type', fontsize=13, fontweight='bold')
ax2.set_title('Fund Characteristics by Execution Timeline',
              fontsize=14, fontweight='bold', pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(fund_types)
ax2.tick_params(axis='y', labelcolor='#3498DB')
ax2_twin.tick_params(axis='y', labelcolor='#E74C3C')
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Add legends
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2_twin.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=11)

plt.tight_layout()
plt.savefig('/home/user/1111202502/最近の補正予算/04_基金分析_type.png', dpi=300, bbox_inches='tight')
plt.close()

# Save the first figure
fig.savefig('/home/user/1111202502/最近の補正予算/04_基金分析.png', dpi=300, bbox_inches='tight')
print("Graphs saved: 04_基金分析.png and 04_基金分析_type.png")
