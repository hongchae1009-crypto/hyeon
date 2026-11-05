// 사용: node print.js in.html out.pdf  (paginate.js 가 있으면 body[data-ready] 대기)
const { chromium } = require('playwright');
(async () => {
  const [inp, out] = process.argv.slice(2);
  const fs = require('fs'); const dirs = fs.readdirSync('/opt/pw-browsers').filter(d => /^chromium-\d+$/.test(d)).sort();
  const exe = dirs.map(d => ['/opt/pw-browsers/' + d + '/chrome-linux/chrome', '/opt/pw-browsers/' + d + '/chrome-linux64/chrome']).flat().find(p => fs.existsSync(p));
  const b = await chromium.launch(exe ? { executablePath: exe } : {});
  const p = await b.newPage();
  await p.goto('file://' + require('path').resolve(inp), { waitUntil: 'networkidle' });
  if (await p.$('#pool')) await p.waitForSelector('body[data-ready="1"]', { timeout: 60000 });
  const over = await p.$$eval('.q.overflow', els => els.length).catch(() => 0);
  if (over) console.error('WARNING: overflowing questions:', over);
  await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
