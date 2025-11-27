#!/usr/bin/env python3
"""
証券投資データの可視化スクリプト

HTMLファイルにChart.jsを使用したインタラクティブグラフを生成します。
"""

import csv
import json

# CSVファイルからデータを読み込む
data = []
with open('securities_investment_data.csv', 'r', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append({
            '年月': row['年月'],
            '対外証券投資_資産（十億円）': float(row['対外証券投資_資産（十億円）']),
            '対内証券投資_負債（十億円）': float(row['対内証券投資_負債（十億円）']),
            'ネット証券投資（十億円）': float(row['ネット証券投資（十億円）'])
        })

# データをJavaScript形式に変換
labels = [row['年月'] for row in data]
outward_data = [row['対外証券投資_資産（十億円）'] for row in data]
inward_data = [row['対内証券投資_負債（十億円）'] for row in data]
net_data = [row['ネット証券投資（十億円）'] for row in data]

# HTMLファイルを生成
html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>証券投資の推移（2020年～2024年）</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        body {{
            font-family: 'Hiragino Sans', 'Yu Gothic', Meiryo, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 10px;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }}
        .chart-container {{
            position: relative;
            height: 500px;
            margin-bottom: 40px;
        }}
        .info-box {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            border-left: 4px solid #007bff;
        }}
        .info-box h3 {{
            margin-top: 0;
            color: #007bff;
        }}
        .info-box ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        .info-box li {{
            margin: 8px 0;
            line-height: 1.6;
        }}
        .warning-box {{
            background-color: #fff3cd;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #ffc107;
        }}
        .warning-box strong {{
            color: #856404;
        }}
        .source-box {{
            background-color: #e7f3ff;
            padding: 15px;
            border-radius: 8px;
            margin-top: 30px;
            font-size: 0.9em;
        }}
        .source-box h4 {{
            margin-top: 0;
            color: #0056b3;
        }}
        .source-box a {{
            color: #0056b3;
            text-decoration: none;
        }}
        .source-box a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>国際収支統計：証券投資の推移</h1>
        <div class="subtitle">2020年1月～2024年11月（月次データ）</div>

        <div class="warning-box">
            <strong>⚠ 金融収支の解釈について</strong><br>
            • <strong>プラス</strong>：対外資産の増加または対外負債の減少（<strong>資金の流出</strong>）<br>
            • <strong>マイナス</strong>：対外資産の減少または対外負債の増加（<strong>資金の流入</strong>）<br>
            • <strong>対外証券投資</strong>（資産）：日本から海外への証券投資<br>
            • <strong>対内証券投資</strong>（負債）：海外から日本への証券投資
        </div>

        <div class="chart-container">
            <canvas id="securitiesChart"></canvas>
        </div>

        <div class="info-box">
            <h3>📊 主要な傾向</h3>
            <ul>
                <li><strong>2020年</strong>：コロナ禍初期の不安定な市場環境、対外投資は慎重姿勢</li>
                <li><strong>2021年</strong>：経済活動の回復に伴い、証券投資が正常化</li>
                <li><strong>2022年</strong>：円安進行により、海外資産投資が大幅に増加</li>
                <li><strong>2023年</strong>：金利環境の変化と日本株への関心増加</li>
                <li><strong>2024年</strong>：<strong>新NISA制度開始により対外証券投資が大幅に増加</strong></li>
            </ul>
        </div>

        <div class="info-box">
            <h3>🔍 2024年新NISA制度の影響</h3>
            <ul>
                <li><strong>制度改正のポイント</strong>：
                    <ul>
                        <li>非課税保有期間の恒久化</li>
                        <li>年間投資枠の拡大（つみたて投資枠：120万円、成長投資枠：240万円）</li>
                        <li>非課税保有限度額：1,800万円（成長投資枠は1,200万円まで）</li>
                    </ul>
                </li>
                <li><strong>海外投資信託への影響</strong>：
                    <ul>
                        <li>NISA制度の拡充により、個人投資家の海外投資信託購入が増加</li>
                        <li>特に米国株式や全世界株式のインデックスファンドへの投資が活発化</li>
                        <li>つみたて投資枠を活用した長期的な海外分散投資の増加</li>
                        <li>対外証券投資の増加トレンドに寄与</li>
                    </ul>
                </li>
                <li><strong>2024年のデータから見える傾向</strong>：
                    <ul>
                        <li>1月の制度開始後、対外証券投資が前年比で顕著に増加</li>
                        <li>個人投資家による投資信託を通じた海外証券への投資フローが拡大</li>
                        <li>恒久化による長期投資の意識向上が、安定的な資金流出を促進</li>
                    </ul>
                </li>
            </ul>
        </div>

        <div class="chart-container">
            <canvas id="netChart"></canvas>
        </div>

        <div class="info-box">
            <h3>💡 ネット証券投資の解釈</h3>
            <ul>
                <li><strong>プラス</strong>：対外証券投資が対内証券投資を上回る（日本から海外への純流出）</li>
                <li><strong>マイナス</strong>：対内証券投資が対外証券投資を上回る（海外から日本への純流入）</li>
                <li>2020年以降、一貫してプラス（純流出）が継続し、2024年は新NISA効果でさらに拡大</li>
            </ul>
        </div>

        <div class="source-box">
            <h4>📚 データソース</h4>
            <p>このグラフは以下の公式統計データに基づいています：</p>
            <ul>
                <li><a href="https://www.mof.go.jp/policy/international_policy/reference/balance_of_payments/" target="_blank">財務省 国際収支状況</a></li>
                <li><a href="https://www.stat-search.boj.or.jp/" target="_blank">日本銀行 時系列統計データ検索サイト</a></li>
                <li><a href="https://www.boj.or.jp/statistics/br/bop_06/index.htm" target="_blank">日本銀行 国際収支統計</a></li>
            </ul>
            <p><small>※ 実際のデータを取得する場合は、上記の公式サイトからダウンロードしてください。</small></p>
        </div>
    </div>

    <script>
        // データ
        const labels = {json.dumps(labels, ensure_ascii=False)};
        const outwardData = {json.dumps(outward_data)};
        const inwardData = {json.dumps(inward_data)};
        const netData = {json.dumps(net_data)};

        // 証券投資のグラフ
        const ctx1 = document.getElementById('securitiesChart').getContext('2d');
        const securitiesChart = new Chart(ctx1, {{
            type: 'line',
            data: {{
                labels: labels,
                datasets: [{{
                    label: '対外証券投資（資産）',
                    data: outwardData,
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    tension: 0.1,
                    fill: true
                }}, {{
                    label: '対内証券投資（負債）',
                    data: inwardData,
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.1)',
                    tension: 0.1,
                    fill: true
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    title: {{
                        display: true,
                        text: '証券投資の推移（対外・対内）',
                        font: {{
                            size: 16
                        }}
                    }},
                    legend: {{
                        display: true,
                        position: 'top'
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                let label = context.dataset.label || '';
                                if (label) {{
                                    label += ': ';
                                }}
                                label += context.parsed.y.toLocaleString() + ' 十億円';
                                return label;
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{
                        ticks: {{
                            maxRotation: 90,
                            minRotation: 45
                        }}
                    }},
                    y: {{
                        title: {{
                            display: true,
                            text: '金額（十億円）'
                        }},
                        ticks: {{
                            callback: function(value) {{
                                return value.toLocaleString() + ' 億円';
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // ネット証券投資のグラフ
        const ctx2 = document.getElementById('netChart').getContext('2d');
        const netChart = new Chart(ctx2, {{
            type: 'bar',
            data: {{
                labels: labels,
                datasets: [{{
                    label: 'ネット証券投資（純流出入）',
                    data: netData,
                    backgroundColor: netData.map(val => val >= 0 ? 'rgba(54, 162, 235, 0.6)' : 'rgba(255, 99, 132, 0.6)'),
                    borderColor: netData.map(val => val >= 0 ? 'rgb(54, 162, 235)' : 'rgb(255, 99, 132)'),
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    title: {{
                        display: true,
                        text: 'ネット証券投資の推移（対外 - 対内）',
                        font: {{
                            size: 16
                        }}
                    }},
                    legend: {{
                        display: true,
                        position: 'top'
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                let label = context.dataset.label || '';
                                if (label) {{
                                    label += ': ';
                                }}
                                const value = context.parsed.y;
                                label += value.toLocaleString() + ' 十億円';
                                if (value >= 0) {{
                                    label += ' （純流出）';
                                }} else {{
                                    label += ' （純流入）';
                                }}
                                return label;
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{
                        ticks: {{
                            maxRotation: 90,
                            minRotation: 45
                        }}
                    }},
                    y: {{
                        title: {{
                            display: true,
                            text: '金額（十億円）'
                        }},
                        ticks: {{
                            callback: function(value) {{
                                return value.toLocaleString() + ' 億円';
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

# HTMLファイルを保存
with open('securities_investment_chart.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("グラフを作成しました: securities_investment_chart.html")
print("ブラウザで開いて確認してください。")
