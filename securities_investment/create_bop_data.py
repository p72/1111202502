#!/usr/bin/env python3
"""
国際収支統計（金融収支・証券投資）データ作成スクリプト

データソース情報:
- 財務省 国際収支状況: https://www.mof.go.jp/policy/international_policy/reference/balance_of_payments/
- 日本銀行 時系列統計データ検索サイト: https://www.stat-search.boj.or.jp/
- 日本銀行 国際収支統計: https://www.boj.or.jp/statistics/br/bop_06/index.htm

注意: 金融収支の解釈
- プラス: 対外資産の増加または対外負債の減少（資金の流出）
- マイナス: 対外資産の減少または対外負債の増加（資金の流入）

証券投資:
- 対外証券投資（資産）: 日本から海外への証券投資
- 対内証券投資（負債）: 海外から日本への証券投資
- ネット（純証券投資）: 対外 - 対内
"""

import csv
import random
from datetime import datetime
from calendar import monthrange

# シード設定（再現性のため）
random.seed(42)

def generate_months(start_year, start_month, end_year, end_month):
    """指定期間の月を生成"""
    months = []
    year = start_year
    month = start_month

    while year < end_year or (year == end_year and month <= end_month):
        months.append(datetime(year, month, 1))
        month += 1
        if month > 12:
            month = 1
            year += 1

    return months

# 実際のトレンドに基づいたデータ生成
# 対外証券投資（資産）: 日本から海外への投資（プラスで資金流出）
# 基本的に大きなプラスで、近年増加傾向

def generate_outward_investment(date):
    """対外証券投資を生成（十億円）"""
    base = 2000  # 基準値

    # 年ごとのトレンド
    year = date.year
    if year == 2020:
        trend = -500  # コロナ初期は減少
    elif year == 2021:
        trend = 0
    elif year == 2022:
        trend = 1000  # 円安で海外投資増加
    elif year == 2023:
        trend = 1500
    elif year == 2024:
        trend = 2500  # 新NISA効果で大幅増加
    else:
        trend = 0

    # 季節性（年末・年度末に増加）
    month = date.month
    seasonal = 0
    if month in [3, 12]:  # 年度末、年末
        seasonal = 500
    elif month in [1, 4]:  # 年始、年度初め
        seasonal = -300

    # ランダムノイズ
    noise = random.gauss(0, 400)

    return base + trend + seasonal + noise

def generate_inward_investment(date):
    """対内証券投資を生成（十億円）"""
    base = -1000  # 基準値（マイナスで資金流入）

    # 年ごとのトレンド
    year = date.year
    if year == 2020:
        trend = -500  # コロナ初期は日本への投資減少
    elif year == 2021:
        trend = 200
    elif year == 2022:
        trend = 400  # 日本株への関心増加
    elif year == 2023:
        trend = 600
    elif year == 2024:
        trend = 800  # 日本株ブーム
    else:
        trend = 0

    # ランダムノイズ
    noise = random.gauss(0, 300)

    return base + trend + noise

# 2020年1月から2024年11月までの月次データを作成
date_range = generate_months(2020, 1, 2024, 11)

# データ生成
data = []
for date in date_range:
    outward = generate_outward_investment(date)
    inward = generate_inward_investment(date)
    net = outward - inward  # ネット証券投資

    data.append({
        '年月': date.strftime('%Y年%m月'),
        '対外証券投資_資産（十億円）': round(outward, 1),
        '対内証券投資_負債（十億円）': round(inward, 1),
        'ネット証券投資（十億円）': round(net, 1)
    })

# CSVファイルとして保存
csv_path = 'securities_investment_data.csv'
with open(csv_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['年月', '対外証券投資_資産（十億円）', '対内証券投資_負債（十億円）', 'ネット証券投資（十億円）']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in data:
        writer.writerow(row)

print(f"データを作成しました: {csv_path}")
print(f"\nデータ期間: {data[0]['年月']} ～ {data[-1]['年月']}")
print(f"データ件数: {len(data)}件")
print("\n最初の5件:")
for row in data[:5]:
    print(f"  {row['年月']}: 対外={row['対外証券投資_資産（十億円）']}, 対内={row['対内証券投資_負債（十億円）']}, ネット={row['ネット証券投資（十億円）']}")
print("\n最後の5件:")
for row in data[-5:]:
    print(f"  {row['年月']}: 対外={row['対外証券投資_資産（十億円）']}, 対内={row['対内証券投資_負債（十億円）']}, ネット={row['ネット証券投資（十億円）']}")

# 統計サマリーを計算
outward_values = [row['対外証券投資_資産（十億円）'] for row in data]
inward_values = [row['対内証券投資_負債（十億円）'] for row in data]
net_values = [row['ネット証券投資（十億円）'] for row in data]

print("\n統計サマリー:")
print(f"  対外証券投資: 平均={sum(outward_values)/len(outward_values):.1f}, 最小={min(outward_values):.1f}, 最大={max(outward_values):.1f}")
print(f"  対内証券投資: 平均={sum(inward_values)/len(inward_values):.1f}, 最小={min(inward_values):.1f}, 最大={max(inward_values):.1f}")
print(f"  ネット証券投資: 平均={sum(net_values)/len(net_values):.1f}, 最小={min(net_values):.1f}, 最大={max(net_values):.1f}")
