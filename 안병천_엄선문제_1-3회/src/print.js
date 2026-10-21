// 상세해설 HTML을 A4 가로 PDF로 인쇄한다(문항별 책갈피 포함).
// 사용법: node print.js <html> <pdf> [글씨 크기 조정 JSON, 예: {"a5": 9.5}]
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

(async () => {
  const [src, out, sizes] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(src));
  await page.waitForSelector('body[data-ready="1"]', { timeout: 120000 });
  console.log(await page.evaluate(() => document.body.dataset.report));
  await page.emulateMedia({ media: 'print' });
  await page.evaluate(sizes => {
    for (const [id, pt] of Object.entries(sizes)) {
      document.getElementById(id).closest('section').querySelector('.flow').style.fontSize = pt + 'pt';
    }
  }, JSON.parse(sizes || '{}'));
  await page.pdf({
    path: out,
    preferCSSPageSize: true,
    printBackground: true,
    outline: true,
    tagged: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate:
      '<div style="width:100%;font-size:7px;color:#888;text-align:center;font-family:sans-serif">' +
      '안병천 1~3회 엄선 문항 · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
  });
  await browser.close();
})();
