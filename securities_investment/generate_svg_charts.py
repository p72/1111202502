#!/usr/bin/env python3
"""
証券投資データのSVGグラフ生成スクリプト

Pythonの標準ライブラリのみを使用してSVGグラフを生成します。
外部ライブラリは不要です。
"""

import csv
import xml.etree.ElementTree as ET
from datetime import datetime

def create_svg_element(width, height):
    """SVGルート要素を作成"""
    svg = ET.Element('svg', {
        'xmlns': 'http://www.w3.org/2000/svg',
        'width': str(width),
        'height': str(height),
        'viewBox': f'0 0 {width} {height}'
    })

    # スタイル定義
    style = ET.SubElement(svg, 'style')
    style.text = """
        .title { font: bold 24px sans-serif; }
        .axis-label { font: bold 14px sans-serif; }
        .tick-label { font: 12px sans-serif; }
        .legend-text { font: 12px sans-serif; }
        .grid { stroke: #ddd; stroke-width: 1; stroke-dasharray: 5,5; }
        .axis { stroke: #000; stroke-width: 2; }
        .line-outward { stroke: #4BC0C0; stroke-width: 2; fill: none; }
        .line-inward { stroke: #FF6384; stroke-width: 2; fill: none; }
        .bar-positive { fill: #36A2EB; opacity: 0.8; }
        .bar-negative { fill: #FF6384; opacity: 0.8; }
    """

    return svg

def add_text(parent, x, y, text, class_name='', anchor='start'):
    """テキスト要素を追加"""
    elem = ET.SubElement(parent, 'text', {
        'x': str(x),
        'y': str(y),
        'text-anchor': anchor,
        'class': class_name
    })
    elem.text = str(text)
    return elem

def add_line(parent, x1, y1, x2, y2, class_name=''):
    """線要素を追加"""
    ET.SubElement(parent, 'line', {
        'x1': str(x1),
        'y1': str(y1),
        'x2': str(x2),
        'y2': str(y2),
        'class': class_name
    })

def add_rect(parent, x, y, width, height, class_name=''):
    """矩形要素を追加"""
    ET.SubElement(parent, 'rect', {
        'x': str(x),
        'y': str(y),
        'width': str(width),
        'height': str(height),
        'class': class_name
    })

def add_polyline(parent, points, class_name=''):
    """折れ線を追加"""
    points_str = ' '.join([f'{x},{y}' for x, y in points])
    ET.SubElement(parent, 'polyline', {
        'points': points_str,
        'class': class_name
    })

# CSVファイルからデータを読み込む
dates = []
labels = []
outward_data = []
inward_data = []
net_data = []

with open('securities_investment_data.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        labels.append(row['年月'])
        outward_data.append(float(row['対外証券投資_資産（十億円）']))
        inward_data.append(float(row['対内証券投資_負債（十億円）']))
        net_data.append(float(row['ネット証券投資（十億円）']))

# グラフ1: 証券投資の推移（対外・対内）
print("Generating Graph 1: Outward & Inward Securities Investment...")

width = 1400
height = 800
margin = {'top': 80, 'right': 100, 'bottom': 100, 'left': 100}
plot_width = width - margin['left'] - margin['right']
plot_height = height - margin['top'] - margin['bottom']

svg1 = create_svg_element(width, height)

# タイトル
add_text(svg1, width/2, 40, 'Securities Investment Trends (Outward & Inward)',
         'title', 'middle')
add_text(svg1, width/2, 65, '2020-2024', 'axis-label', 'middle')

# データの範囲を計算
all_values = outward_data + inward_data
y_min = min(all_values)
y_max = max(all_values)
y_range = y_max - y_min
y_min = y_min - y_range * 0.1
y_max = y_max + y_range * 0.1

# スケール関数
def scale_x(i):
    return margin['left'] + (i / (len(labels) - 1)) * plot_width

def scale_y(value):
    return margin['top'] + plot_height - ((value - y_min) / (y_max - y_min)) * plot_height

# グリッド
for i in range(11):
    y_val = y_min + (y_max - y_min) * i / 10
    y_pos = scale_y(y_val)
    add_line(svg1, margin['left'], y_pos, width - margin['right'], y_pos, 'grid')
    add_text(svg1, margin['left'] - 10, y_pos + 5, f'{y_val:.0f}', 'tick-label', 'end')

# X軸ラベル（3ヶ月ごと）
for i in range(0, len(labels), 3):
    x_pos = scale_x(i)
    add_text(svg1, x_pos, height - margin['bottom'] + 25, labels[i], 'tick-label', 'middle')

# 軸
add_line(svg1, margin['left'], margin['top'], margin['left'],
         height - margin['bottom'], 'axis')
add_line(svg1, margin['left'], height - margin['bottom'],
         width - margin['right'], height - margin['bottom'], 'axis')
add_line(svg1, margin['left'], scale_y(0), width - margin['right'], scale_y(0), 'axis')

# 軸ラベル
add_text(svg1, width/2, height - 20, 'Year-Month', 'axis-label', 'middle')
add_text(svg1, 30, height/2, 'Amount (Billion Yen)', 'axis-label', 'middle')

# データプロット
outward_points = [(scale_x(i), scale_y(val)) for i, val in enumerate(outward_data)]
inward_points = [(scale_x(i), scale_y(val)) for i, val in enumerate(inward_data)]

add_polyline(svg1, outward_points, 'line-outward')
add_polyline(svg1, inward_points, 'line-inward')

# 凡例
legend_x = width - margin['right'] + 10
legend_y = margin['top']
add_line(svg1, legend_x, legend_y, legend_x + 30, legend_y, 'line-outward')
add_text(svg1, legend_x + 35, legend_y + 5, 'Outward', 'legend-text')

legend_y += 25
add_line(svg1, legend_x, legend_y, legend_x + 30, legend_y, 'line-inward')
add_text(svg1, legend_x + 35, legend_y + 5, 'Inward', 'legend-text')

# SVGを保存
svg1_file = 'securities_investment_outward_inward.svg'
tree1 = ET.ElementTree(svg1)
ET.indent(tree1, space='  ')
tree1.write(svg1_file, encoding='utf-8', xml_declaration=True)
print(f"✓ Saved: {svg1_file}")

# グラフ2: ネット証券投資
print("Generating Graph 2: Net Securities Investment...")

svg2 = create_svg_element(width, height)

# タイトル
add_text(svg2, width/2, 40, 'Net Securities Investment Trends (Outward - Inward)',
         'title', 'middle')
add_text(svg2, width/2, 65, '2020-2024', 'axis-label', 'middle')

# データの範囲
y_min_net = min(net_data)
y_max_net = max(net_data)
y_range_net = y_max_net - y_min_net
y_min_net = min(y_min_net - y_range_net * 0.1, 0)
y_max_net = y_max_net + y_range_net * 0.1

def scale_y_net(value):
    return margin['top'] + plot_height - ((value - y_min_net) / (y_max_net - y_min_net)) * plot_height

# グリッド
for i in range(11):
    y_val = y_min_net + (y_max_net - y_min_net) * i / 10
    y_pos = scale_y_net(y_val)
    add_line(svg2, margin['left'], y_pos, width - margin['right'], y_pos, 'grid')
    add_text(svg2, margin['left'] - 10, y_pos + 5, f'{y_val:.0f}', 'tick-label', 'end')

# X軸ラベル
for i in range(0, len(labels), 3):
    x_pos = scale_x(i)
    add_text(svg2, x_pos, height - margin['bottom'] + 25, labels[i], 'tick-label', 'middle')

# 軸
add_line(svg2, margin['left'], margin['top'], margin['left'],
         height - margin['bottom'], 'axis')
add_line(svg2, margin['left'], height - margin['bottom'],
         width - margin['right'], height - margin['bottom'], 'axis')
add_line(svg2, margin['left'], scale_y_net(0), width - margin['right'], scale_y_net(0), 'axis')

# 軸ラベル
add_text(svg2, width/2, height - 20, 'Year-Month', 'axis-label', 'middle')
add_text(svg2, 30, height/2, 'Amount (Billion Yen)', 'axis-label', 'middle')

# バーチャート
bar_width = plot_width / len(net_data) * 0.8
for i, val in enumerate(net_data):
    x_pos = scale_x(i) - bar_width / 2
    if val >= 0:
        y_pos = scale_y_net(val)
        bar_height = scale_y_net(0) - y_pos
        add_rect(svg2, x_pos, y_pos, bar_width, bar_height, 'bar-positive')
    else:
        y_pos = scale_y_net(0)
        bar_height = scale_y_net(val) - y_pos
        add_rect(svg2, x_pos, y_pos, bar_width, bar_height, 'bar-negative')

# 凡例
legend_x = width - margin['right'] + 10
legend_y = margin['top']
add_rect(svg2, legend_x, legend_y - 10, 20, 15, 'bar-positive')
add_text(svg2, legend_x + 25, legend_y + 5, 'Net Outflow', 'legend-text')

legend_y += 25
add_rect(svg2, legend_x, legend_y - 10, 20, 15, 'bar-negative')
add_text(svg2, legend_x + 25, legend_y + 5, 'Net Inflow', 'legend-text')

# SVGを保存
svg2_file = 'securities_investment_net.svg'
tree2 = ET.ElementTree(svg2)
ET.indent(tree2, space='  ')
tree2.write(svg2_file, encoding='utf-8', xml_declaration=True)
print(f"✓ Saved: {svg2_file}")

print("\n=== Summary ===")
print(f"Generated 2 SVG charts:")
print(f"1. {svg1_file}")
print(f"2. {svg2_file}")
print("\nTo convert SVG to PNG, you can:")
print("1. Open in a web browser and take a screenshot")
print("2. Use ImageMagick: convert file.svg file.png")
print("3. Use Inkscape: inkscape file.svg --export-png=file.png")
print("4. Use online converters like cloudconvert.com")
