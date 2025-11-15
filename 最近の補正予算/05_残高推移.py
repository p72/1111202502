import matplotlib.pyplot as plt
import numpy as np
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']

# Cumulative data for supplementary budgets and execution
years = np.array([2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])
cumulative_budget = np.array([2.7, 5.4, 7.8, 12.3, 85.3, 136.5, 174.6, 187.8, 201.7])  # Cumulative trillion yen
cumulative_executed = np.array([2.7, 5.2, 7.5, 11.8, 78.5, 122.3, 155.1, 165.3, 178.5])  # Cumulative executed
unexecuted_balance = cumulative_budget - cumulative_executed

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# Top: Cumulative supplementary budget and execution
ax1.fill_between(years, 0, cumulative_budget, alpha=0.3, color='#3498DB', label='Cumulative Budget')
ax1.fill_between(years, 0, cumulative_executed, alpha=0.5, color='#2ECC71', label='Cumulative Executed')
ax1.plot(years, cumulative_budget, 'o-', color='#3498DB', linewidth=2.5, markersize=8, label='Budget Line')
ax1.plot(years, cumulative_executed, 's-', color='#2ECC71', linewidth=2.5, markersize=8, label='Executed Line')

# Add annotations for major peaks
ax1.annotate('COVID-19\nPandemic', xy=(2020, 85.3), xytext=(2018.5, 100),
             arrowprops=dict(arrowstyle='->', color='red', lw=2),
             fontsize=11, fontweight='bold', color='red')
ax1.annotate('Recovery\nPhase', xy=(2021, 136.5), xytext=(2021.5, 150),
             arrowprops=dict(arrowstyle='->', color='orange', lw=2),
             fontsize=11, fontweight='bold', color='orange')

ax1.set_ylabel('Cumulative Amount (Trillion Yen)', fontsize=13, fontweight='bold')
ax1.set_xlabel('Fiscal Year', fontsize=13, fontweight='bold')
ax1.set_title('Cumulative Supplementary Budget and Execution\n累積補正予算額と執行額',
              fontsize=15, fontweight='bold', pad=20)
ax1.legend(loc='upper left', fontsize=11)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(2015.5, 2024.5)

# Bottom: Unexecuted balance over time
colors = ['#E74C3C' if val > 15 else '#F39C12' if val > 5 else '#2ECC71' for val in unexecuted_balance]
bars = ax2.bar(years, unexecuted_balance, color=colors, edgecolor='black', linewidth=1.5, alpha=0.8)

# Add value labels
for year, balance, bar in zip(years, unexecuted_balance, bars):
    ax2.text(year, balance + 0.5, f'¥{balance:.1f}T',
             ha='center', va='bottom', fontsize=9, fontweight='bold')

# Add threshold lines
ax2.axhline(y=5, color='orange', linestyle='--', linewidth=2, alpha=0.6, label='Moderate Level (¥5T)')
ax2.axhline(y=15, color='red', linestyle='--', linewidth=2, alpha=0.6, label='High Level (¥15T)')

ax2.set_ylabel('Unexecuted Balance (Trillion Yen)', fontsize=13, fontweight='bold')
ax2.set_xlabel('Fiscal Year', fontsize=13, fontweight='bold')
ax2.set_title('Unexecuted Balance Trend\n未執行残高の推移',
              fontsize=15, fontweight='bold', pad=20)
ax2.legend(loc='upper left', fontsize=11)
ax2.grid(axis='y', alpha=0.3, linestyle='--')
ax2.set_xlim(2015.5, 2024.5)

plt.tight_layout()
plt.savefig('/home/user/1111202502/最近の補正予算/05_残高推移.png', dpi=300, bbox_inches='tight')
print("Graph saved: 05_残高推移.png")
