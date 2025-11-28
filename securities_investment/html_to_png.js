#!/usr/bin/env node
/**
 * HTMLグラフをPNG画像に変換するスクリプト
 * puppeteerを使用してChart.jsグラフをキャプチャします
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function generatePNGs() {
    console.log('Starting browser...');
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();

        // HTMLファイルのパスを取得
        const htmlPath = path.join(__dirname, 'securities_investment_chart.html');
        const fileUrl = 'file://' + htmlPath;

        console.log(`Loading HTML: ${fileUrl}`);
        await page.goto(fileUrl, { waitUntil: 'networkidle0' });

        // ページが完全にロードされるまで待機
        await page.waitForTimeout(2000);

        // Chart.jsのレンダリングを待つ
        await page.waitForSelector('canvas');
        await page.waitForTimeout(1000);

        // ビューポートを大きく設定
        await page.setViewport({ width: 1400, height: 3000 });

        // ページ全体のスクリーンショット
        console.log('Capturing full page screenshot...');
        await page.screenshot({
            path: 'securities_investment_full_page.png',
            fullPage: true
        });
        console.log('✓ Saved: securities_investment_full_page.png');

        // 個別のグラフをキャプチャ
        const charts = await page.$$('canvas');

        if (charts.length >= 1) {
            console.log(`Found ${charts.length} chart(s)`);

            // 1つ目のグラフ（対外・対内）
            const chart1 = charts[0];
            const box1 = await chart1.boundingBox();
            if (box1) {
                await page.screenshot({
                    path: 'securities_investment_outward_inward.png',
                    clip: {
                        x: Math.max(0, box1.x - 20),
                        y: Math.max(0, box1.y - 80),
                        width: Math.min(box1.width + 40, 1400),
                        height: box1.height + 120
                    }
                });
                console.log('✓ Saved: securities_investment_outward_inward.png');
            }
        }

        if (charts.length >= 2) {
            // 2つ目のグラフ（ネット証券投資）
            const chart2 = charts[1];
            const box2 = await chart2.boundingBox();
            if (box2) {
                await page.screenshot({
                    path: 'securities_investment_net.png',
                    clip: {
                        x: Math.max(0, box2.x - 20),
                        y: Math.max(0, box2.y - 80),
                        width: Math.min(box2.width + 40, 1400),
                        height: box2.height + 120
                    }
                });
                console.log('✓ Saved: securities_investment_net.png');
            }
        }

        console.log('\n=== Summary ===');
        console.log('Successfully generated PNG images:');
        console.log('1. securities_investment_full_page.png (Full page)');
        console.log('2. securities_investment_outward_inward.png (Chart 1)');
        console.log('3. securities_investment_net.png (Chart 2)');

    } catch (error) {
        console.error('Error:', error);
        throw error;
    } finally {
        await browser.close();
        console.log('\nBrowser closed.');
    }
}

// 実行
generatePNGs()
    .then(() => {
        console.log('\n✓ All PNG images generated successfully!');
        process.exit(0);
    })
    .catch(error => {
        console.error('\n✗ Error generating PNG images:', error);
        process.exit(1);
    });
