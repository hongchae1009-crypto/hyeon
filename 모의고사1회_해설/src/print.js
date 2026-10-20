// 상세해설 HTML을 A4 가로 PDF로 인쇄한다(문항별 책갈피 포함). 사용법: node print.js <html> <pdf>
const path = require('path');
const { execSync } = require('child_process');
const { chromium } = require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));

(async () => {
  const [src, out] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(src));
  await page.waitForSelector('body[data-ready="1"]', { timeout: 120000 });
  console.log(await page.evaluate(() => document.body.dataset.report));
  await page.emulateMedia({ media: 'print' });
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
      '전공화학 모의고사 1회 상세해설 · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
  });
  await browser.close();
})();
