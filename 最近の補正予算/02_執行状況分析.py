import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

# FY2022 Supplementary Budget Execution Data
categories = ['Executed\nin FY2022', 'Carried Over\nto FY2023', 'Unexecuted']
amounts = [10.24, 8.62, 0.598]  # trillion yen
colors = ['#2ECC71', '#F39C12', '#E74C3C']

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Left: Pie chart
wedges, texts, autotexts = ax1.pie(amounts, labels=categories, autopct='%1.1f%%',
                                     colors=colors, startangle=90,
                                     textprops={'fontsize': 12, 'fontweight': 'bold'})
ax1.set_title('FY2022 Supplementary Budget Execution Status\n(¥18.86T Economic Stimulus Projects)',
              fontsize=14, fontweight='bold', pad=20)

# Add amount labels
for i, (text, amount) in enumerate(zip(texts, amounts)):
    text.set_text(f'{categories[i]}\n¥{amount:.2f}T')

# Right: Carryover analysis
years = ['FY2022', 'FY2023', 'FY2024']
carryover_rates = [46, 42, 35]  # Estimated percentages
executed_rates = [54, 58, 65]

x = np.arange(len(years))
width = 0.6

bars1 = ax2.bar(x, executed_rates, width, label='Executed in Same Year',
                color='#2ECC71', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax2.bar(x, carryover_rates, width, bottom=executed_rates,
                label='Carried Over', color='#F39C12', alpha=0.8,
                edgecolor='black', linewidth=1.5)

# Add percentage labels
for i, (e, c) in enumerate(zip(executed_rates, carryover_rates)):
    ax2.text(i, e/2, f'{e}%', ha='center', va='center',
             fontsize=11, fontweight='bold')
    ax2.text(i, e + c/2, f'{c}%', ha='center', va='center',
             fontsize=11, fontweight='bold')

ax2.set_ylabel('Percentage (%)', fontsize=13, fontweight='bold')
ax2.set_xlabel('Fiscal Year', fontsize=13, fontweight='bold')
ax2.set_title('Execution vs Carryover Rates Trend',
              fontsize=14, fontweight='bold', pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(years)
ax2.set_ylim(0, 100)
ax2.legend(loc='upper right', fontsize=11)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('/home/user/1111202502/最近の補正予算/02_執行状況分析.png', dpi=300, bbox_inches='tight')
print("Graph saved: 02_執行状況分析.png")
