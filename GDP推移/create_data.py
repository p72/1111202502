#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日本の名目GDPと長期金利のデータ生成
Japan's Nominal GDP and Long-term Interest Rate Data Generation
"""

import csv
import json

# 日本の名目GDP データ（兆円）と長期金利データ（%）
data = [
    {'年度': 1980, '名目GDP': 249.4, '長期金利': 9.22},
    {'年度': 1985, '名目GDP': 338.6, '長期金利': 6.34},
    {'年度': 1990, '名目GDP': 452.6, '長期金利': 7.36},
    {'年度': 1991, '名目GDP': 476.7, '長期金利': 6.35},
    {'年度': 1992, '名目GDP': 485.7, '長期金利': 5.35},
    {'年度': 1993, '名目GDP': 491.7, '長期金利': 4.29},
    {'年度': 1994, '名目GDP': 497.9, '長期金利': 4.51},
    {'年度': 1995, '名目GDP': 505.7, '長期金利': 3.45},
    {'年度': 1996, '名目GDP': 518.3, '長期金利': 3.10},
    {'年度': 1997, '名目GDP': 526.0, '長期金利': 2.36},
    {'年度': 1998, '名目GDP': 512.4, '長期金利': 1.49},
    {'年度': 1999, '名目GDP': 507.2, '長期金利': 1.75},
    {'年度': 2000, '名目GDP': 524.3, '長期金利': 1.76},
    {'年度': 2001, '名目GDP': 519.5, '長期金利': 1.33},
    {'年度': 2002, '名目GDP': 515.8, '長期金利': 1.27},
    {'年度': 2003, '名目GDP': 521.1, '長期金利': 1.00},
    {'年度': 2004, '名目GDP': 531.9, '長期金利': 1.50},
    {'年度': 2005, '名目GDP': 542.4, '長期金利': 1.39},
    {'年度': 2006, '名目GDP': 553.1, '長期金利': 1.74},
    {'年度': 2007, '名目GDP': 560.8, '長期金利': 1.68},
    {'年度': 2008, '名目GDP': 543.4, '長期金利': 1.47},
    {'年度': 2009, '名目GDP': 521.0, '長期金利': 1.35},
    {'年度': 2010, '名目GDP': 539.3, '長期金利': 1.18},
    {'年度': 2011, '名目GDP': 537.8, '長期金利': 1.12},
    {'年度': 2012, '名目GDP': 546.6, '長期金利': 0.86},
    {'年度': 2013, '名目GDP': 561.4, '長期金利': 0.72},
    {'年度': 2014, '名目GDP': 573.6, '長期金利': 0.55},
    {'年度': 2015, '名目GDP': 583.8, '長期金利': 0.36},
    {'年度': 2016, '名目GDP': 596.5, '長期金利': -0.02},
    {'年度': 2017, '名目GDP': 606.3, '長期金利': 0.07},
    {'年度': 2018, '名目GDP': 615.8, '長期金利': 0.09},
    {'年度': 2019, '名目GDP': 625.2, '長期金利': -0.01},
    {'年度': 2020, '名目GDP': 610.4, '長期金利': 0.03},
    {'年度': 2021, '名目GDP': 631.8, '長期金利': 0.10},
    {'年度': 2022, '名目GDP': 648.5, '長期金利': 0.23},
    {'年度': 2023, '名目GDP': 665.3, '長期金利': 0.61},
    {'年度': 2024, '名目GDP': 680.5, '長期金利': 1.15},
]

# CSVファイルとして保存
csv_file = 'GDP推移/japan_gdp_interest_data.csv'
with open(csv_file, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['年度', '名目GDP', '長期金利'])
    writer.writeheader()
    writer.writerows(data)

print(f"✓ CSVファイルを保存しました: {csv_file}")

# 統計計算
gdp_values = [d['名目GDP'] for d in data]
interest_values = [d['長期金利'] for d in data]

gdp_start = gdp_values[0]
gdp_end = gdp_values[-1]
gdp_max = max(gdp_values)
gdp_min = min(gdp_values)
gdp_avg = sum(gdp_values) / len(gdp_values)

interest_start = interest_values[0]
interest_end = interest_values[-1]
interest_max = max(interest_values)
interest_min = min(interest_values)
interest_avg = sum(interest_values) / len(interest_values)

gdp_growth = ((gdp_end / gdp_start) - 1) * 100
interest_change = interest_end - interest_start

# 相関係数の計算
def correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator_x = sum((x[i] - mean_x) ** 2 for i in range(n)) ** 0.5
    denominator_y = sum((y[i] - mean_y) ** 2 for i in range(n)) ** 0.5

    return numerator / (denominator_x * denominator_y)

corr = correlation(gdp_values, interest_values)

# 統計レポートをテキストファイルとして保存
report_file = 'GDP推移/statistical_summary.txt'
with open(report_file, 'w', encoding='utf-8') as f:
    f.write("="*70 + "\n")
    f.write("日本の名目GDPと長期金利 - 統計サマリー\n")
    f.write("Japan's Nominal GDP and Long-term Interest Rate - Statistical Summary\n")
    f.write("="*70 + "\n\n")
    f.write(f"【分析期間】 {data[0]['年度']}年 ～ {data[-1]['年度']}年 ({len(data)}年間)\n\n")

    f.write("【名目GDP】\n")
    f.write(f"  期初 ({data[0]['年度']}年): {gdp_start:.1f} 兆円\n")
    f.write(f"  期末 ({data[-1]['年度']}年): {gdp_end:.1f} 兆円\n")
    f.write(f"  増加額: {gdp_end - gdp_start:.1f} 兆円\n")
    f.write(f"  増加率: {gdp_growth:.1f}%\n")
    f.write(f"  最大値: {gdp_max:.1f} 兆円\n")
    f.write(f"  最小値: {gdp_min:.1f} 兆円\n")
    f.write(f"  平均値: {gdp_avg:.1f} 兆円\n\n")

    f.write("【長期金利（10年国債利回り）】\n")
    f.write(f"  期初 ({data[0]['年度']}年): {interest_start:.2f}%\n")
    f.write(f"  期末 ({data[-1]['年度']}年): {interest_end:.2f}%\n")
    f.write(f"  変化: {interest_change:.2f} ポイント\n")
    f.write(f"  最高値: {interest_max:.2f}%\n")
    f.write(f"  最低値: {interest_min:.2f}%\n")
    f.write(f"  平均値: {interest_avg:.2f}%\n\n")

    f.write("【相関分析】\n")
    f.write(f"  GDPと金利の相関係数: {corr:.3f}\n")

    if abs(corr) > 0.7:
        strength = "強い"
    elif abs(corr) > 0.4:
        strength = "中程度の"
    else:
        strength = "弱い"
    direction = "正" if corr > 0 else "負"
    f.write(f"  解釈: {strength}{direction}の相関関係\n\n")

    f.write("【主要な経済イベント】\n")
    f.write("  • 1980年代後半: バブル経済期 - GDP急成長、高金利\n")
    f.write("  • 1991-2002年: 失われた10年 - GDP停滞、金利低下\n")
    f.write("  • 2008-2009年: リーマンショック - GDP減少\n")
    f.write("  • 2013年: アベノミクス開始 - 金融緩和政策\n")
    f.write("  • 2016年: マイナス金利政策導入\n")
    f.write("  • 2020年: COVID-19パンデミック - GDP減少\n")
    f.write("  • 2022-2024年: 金利正常化への動き\n\n")

    f.write("="*70 + "\n")

print(f"✓ 統計レポートを保存しました: {report_file}")

# 詳細データをJSONでも保存
json_file = 'GDP推移/japan_gdp_interest_data.json'
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump({
        'data': data,
        'statistics': {
            'gdp': {
                'start': gdp_start,
                'end': gdp_end,
                'growth_rate': gdp_growth,
                'max': gdp_max,
                'min': gdp_min,
                'average': gdp_avg
            },
            'interest_rate': {
                'start': interest_start,
                'end': interest_end,
                'change': interest_change,
                'max': interest_max,
                'min': interest_min,
                'average': interest_avg
            },
            'correlation': corr
        }
    }, f, ensure_ascii=False, indent=2)

print(f"✓ JSONファイルを保存しました: {json_file}")

print("\n" + "="*70)
print("統計サマリー（コンソール出力）")
print("="*70)
print(f"\n名目GDP: {gdp_start:.1f}兆円 → {gdp_end:.1f}兆円 (+{gdp_growth:.1f}%)")
print(f"長期金利: {interest_start:.2f}% → {interest_end:.2f}% ({interest_change:+.2f}ポイント)")
print(f"相関係数: {corr:.3f} ({strength}{direction}の相関)")
print("\n" + "="*70)
print("\nデータファイルが正常に作成されました！")
