import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# 日本語フォントの設定
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

# 資金過不足データの読み込み
df_deficit = pd.read_csv('資金循環統計 資金過不足1980.csv', encoding='shift-jis')

# 1行目が系列名称なので、2行目以降を使用
# データコード列を年として使用
years = df_deficit['データコード'][1:].astype(int).values
gov_deficit = df_deficit["FF'FOF_FFYF420L700"][1:].astype(float).values

# 名目GDPデータの読み込み
df_gdp = pd.read_csv('nominal_gdp.csv')

# データを結合
df = pd.DataFrame({
    '年度': years,
    '一般政府資金過不足_億円': gov_deficit,
})

# GDPデータとマージ
df = df.merge(df_gdp, left_on='年度', right_on='年度')

# 名目GDPを億円に変換（兆円→億円）
df['名目GDP_億円'] = df['名目GDP_兆円'] * 10000

# 資金過不足/名目GDP比を計算（%表示）
df['資金過不足GDP比_%'] = (df['一般政府資金過不足_億円'] / df['名目GDP_億円']) * 100

# 結果を保存
df.to_csv('government_deficit_gdp_ratio.csv', index=False, encoding='utf-8-sig')

print("計算結果:")
print(df[['年度', '一般政府資金過不足_億円', '名目GDP_兆円', '資金過不足GDP比_%']].head(10))
print("\n...")
print(df[['年度', '一般政府資金過不足_億円', '名目GDP_兆円', '資金過不足GDP比_%']].tail(5))

# グラフの作成
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# グラフ1: 一般政府の資金過不足の推移
ax1.plot(df['年度'], df['一般政府資金過不足_億円']/10000, marker='o', linewidth=2, markersize=4)
ax1.axhline(y=0, color='red', linestyle='--', alpha=0.5)
ax1.set_xlabel('Year', fontsize=12)
ax1.set_ylabel('Trillion Yen', fontsize=12)
ax1.set_title('General Government Financial Surplus/Deficit (Flow of Funds Statistics)', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(1980, 2024)

# グラフ2: 資金過不足/名目GDP比の推移
ax2.plot(df['年度'], df['資金過不足GDP比_%'], marker='o', linewidth=2, markersize=4, color='darkblue')
ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
ax2.set_xlabel('Year', fontsize=12)
ax2.set_ylabel('% of GDP', fontsize=12)
ax2.set_title('General Government Financial Surplus/Deficit as % of Nominal GDP', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(1980, 2024)

plt.tight_layout()
plt.savefig('government_deficit_gdp_ratio.png', dpi=300, bbox_inches='tight')
print("\nグラフを保存しました: government_deficit_gdp_ratio.png")

# 統計情報
print("\n統計情報:")
print(f"期間: {df['年度'].min()}年 - {df['年度'].max()}年")
print(f"資金過不足GDP比の平均: {df['資金過不足GDP比_%'].mean():.2f}%")
print(f"資金過不足GDP比の最小値: {df['資金過不足GDP比_%'].min():.2f}% ({df.loc[df['資金過不足GDP比_%'].idxmin(), '年度']:.0f}年)")
print(f"資金過不足GDP比の最大値: {df['資金過不足GDP比_%'].max():.2f}% ({df.loc[df['資金過不足GDP比_%'].idxmax(), '年度']:.0f}年)")
