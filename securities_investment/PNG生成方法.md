# PNG形式のグラフ生成方法

## 概要

証券投資グラフをPNG画像として生成・保存する方法を説明します。

## 方法1: SVGビューアからPNG変換（最も簡単）

### 手順

1. **svg_viewer.html** をブラウザで開く
   ```bash
   # Linux
   xdg-open svg_viewer.html

   # macOS
   open svg_viewer.html

   # Windows
   start svg_viewer.html
   ```

2. 各グラフの下にある「**📥 PNG形式でダウンロード**」ボタンをクリック

3. PNG画像が自動的にダウンロードされます

### 注意事項
- ブラウザのセキュリティ設定により、ローカルファイルのCanvas変換が制限される場合があります
- その場合は、方法2または方法3を使用してください

---

## 方法2: ブラウザのスクリーンショット機能を使用

### Chrome / Edge の場合

1. **svg_viewer.html** をブラウザで開く

2. **F12** キーを押して開発者ツールを開く

3. **Ctrl + Shift + P** (Mac: **Cmd + Shift + P**) でコマンドパレットを開く

4. 「**screenshot**」と入力し、以下のいずれかを選択：
   - **Capture screenshot** - 表示領域のスクリーンショット
   - **Capture full size screenshot** - ページ全体のスクリーンショット
   - **Capture node screenshot** - 選択した要素のスクリーンショット

5. PNG画像が自動的にダウンロードされます

### Firefox の場合

1. **svg_viewer.html** をブラウザで開く

2. **Shift + F2** でコマンドラインを開く（または右クリック → スクリーンショットを撮る）

3. 以下のコマンドを入力：
   ```
   :screenshot --fullpage
   ```

4. PNG画像が自動的にダウンロードされます

### Safari の場合

1. **svg_viewer.html** をブラウザで開く

2. 開発メニューを有効にする（環境設定 → 詳細 → メニューバーに開発メニューを表示）

3. **開発** → **Webインスペクタを表示**

4. 要素を右クリック → **スクリーンショットを撮る**

---

## 方法3: matplotlibを使用（ローカル環境、最高品質）

### 前提条件

Python 3とpipがインストールされていること

### 手順

1. **matplotlibをインストール**
   ```bash
   pip install matplotlib
   ```

2. **PNG生成スクリプトを実行**
   ```bash
   cd securities_investment
   python3 generate_png_charts.py
   ```

3. 以下の4つのPNG画像が生成されます：
   - `securities_investment_outward_inward.png` - 対外・対内証券投資（全期間）
   - `securities_investment_net.png` - ネット証券投資（全期間）
   - `securities_investment_yearly_average.png` - 年次平均比較
   - `securities_investment_2024_nisa_impact.png` - 2024年詳細（新NISA影響）

### 特徴
- 高解像度（300 DPI）
- プロフェッショナル品質
- カスタマイズ可能

---

## 方法4: Chart.jsのHTMLから保存

### 手順

1. **securities_investment_chart.html** をブラウザで開く

2. グラフ上で **右クリック** → **名前を付けて画像を保存**

3. ブラウザによっては、グラフを画像として直接保存できます

### または

1. ブラウザのスクリーンショット機能を使用（方法2参照）

---

## 方法5: SVGファイルを直接変換

### オンラインコンバーター

1. 以下のオンラインサービスにアクセス：
   - [CloudConvert](https://cloudconvert.com/svg-to-png)
   - [Convertio](https://convertio.co/ja/svg-png/)
   - [Online-Convert](https://www.online-convert.com/)

2. SVGファイルをアップロード：
   - `securities_investment_outward_inward.svg`
   - `securities_investment_net.svg`

3. PNG形式に変換してダウンロード

### コマンドライン（ImageMagick）

ImageMagickがインストールされている場合：

```bash
convert securities_investment_outward_inward.svg securities_investment_outward_inward.png
convert securities_investment_net.svg securities_investment_net.png
```

### コマンドライン（Inkscape）

Inkscapeがインストールされている場合：

```bash
inkscape securities_investment_outward_inward.svg --export-png=securities_investment_outward_inward.png --export-dpi=300
inkscape securities_investment_net.svg --export-png=securities_investment_net.png --export-dpi=300
```

---

## 比較表

| 方法 | 難易度 | 品質 | 速度 | おすすめ度 |
|---|---|---|---|---|
| SVGビューア | ★☆☆ | ★★★☆ | ★★★ | ★★★★★ |
| ブラウザスクショ | ★☆☆ | ★★★★ | ★★★ | ★★★★☆ |
| matplotlib | ★★☆ | ★★★★★ | ★★☆ | ★★★★★ |
| Chart.js保存 | ★☆☆ | ★★★☆ | ★★★ | ★★★☆☆ |
| オンライン変換 | ★☆☆ | ★★★★ | ★☆☆ | ★★★☆☆ |

---

## トラブルシューティング

### Q1: SVGビューアのPNG変換ボタンが動作しない

**A:** ブラウザのセキュリティ設定が原因です。以下を試してください：
1. HTTPサーバーを起動してアクセス：
   ```bash
   python3 -m http.server 8000
   # ブラウザで http://localhost:8000/svg_viewer.html を開く
   ```
2. または、方法2（ブラウザスクショ）を使用

### Q2: matplotlibで日本語が表示されない

**A:** 日本語フォントが必要です：
```python
# generate_png_charts.py の先頭に追加
plt.rcParams['font.family'] = ['Hiragino Sans', 'Yu Gothic', 'Meiryo', 'sans-serif']
```

### Q3: 画像が低解像度になる

**A:** 以下の方法で高解像度化：
1. matplotlib使用時: `dpi=300` を指定（既に設定済み）
2. ブラウザスクショ: 拡張機能「Awesome Screenshot」等を使用
3. SVG変換時: `--export-dpi=300` を指定

### Q4: グラフの一部が切れる

**A:**
1. svg_viewer.htmlの場合: ブラウザウィンドウを最大化
2. matplotlibの場合: `plt.tight_layout()` が効いているか確認（既に設定済み）
3. ブラウザスクショの場合: フルページスクショを選択

---

## おすすめの方法

### 初心者向け
→ **方法1（SVGビューア）** または **方法2（ブラウザスクショ）**

### 品質重視
→ **方法3（matplotlib）**

### 手軽さ重視
→ **方法1（SVGビューア）**

### 複数枚必要
→ **方法3（matplotlib）** - 4枚のグラフが一度に生成されます

---

## 生成されるファイル

### SVG形式（ベクター、拡大しても綺麗）
- `securities_investment_outward_inward.svg`
- `securities_investment_net.svg`

### PNG形式（ラスター、ドキュメント埋め込み用）
- `securities_investment_outward_inward.png`
- `securities_investment_net.png`
- `securities_investment_yearly_average.png` (matplotlibのみ)
- `securities_investment_2024_nisa_impact.png` (matplotlibのみ)

---

**作成日**: 2024年11月27日
**更新日**: 2024年11月27日
