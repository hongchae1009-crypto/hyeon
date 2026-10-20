"""모의고사4회_상세해설.md → A4 가로판 독립 실행형 HTML(이미지·글꼴·KaTeX 내장).

가독성 우선: 본문 10pt 고정, 3단 흐름(첫 단에 문제지 원문, 이어서 정답·공식·풀이).
문항마다 새 쪽에서 시작하고, 상자·표·그림·수식은 단이나 쪽 경계에서 쪼개지 않는다.

사용법: python3 build.py <katex_dist_dir> <noto_sans_kr_files_dir>
PDF는 같은 폴더의 print.js로 이 HTML을 인쇄해 만든다.
"""
import base64, html, os, re, sys
import markdown
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
KATEX, FONTS = sys.argv[1], sys.argv[2]
MD = os.path.join(ROOT, '모의고사4회_상세해설.md')
OUT = os.path.join(ROOT, '모의고사4회_상세해설.html')

# 원문 이미지 배율: 모든 문항에 같은 배율(0.12 mm/px, 한 단 너비에 맞음). 긴 문항은 crop_questions.py가 단 높이로 나눠 둔다.
MM_PER_PX = 0.12


def b64(path):
    return base64.b64encode(open(path, 'rb').read()).decode()


def protect_math(text):
    store = []

    def keep(m):
        store.append(m.group(0))
        return f'MATHPH{len(store) - 1}X'
    text = re.sub(r'\$\$.+?\$\$', keep, text, flags=re.S)
    text = re.sub(r'(?<!\\)\$[^$\n]+?\$', keep, text)
    return text, store


def katex_css():
    css = open(os.path.join(KATEX, 'katex.min.css')).read()

    def font(m):
        return f"url(data:font/woff2;base64,{b64(os.path.join(KATEX, 'fonts', m.group(1)))})"
    css = re.sub(r'url\(fonts/([^)]+?\.woff2)\)', font, css)
    # woff/ttf 대체 경로는 지운다 (woff2만 내장)
    return re.sub(r',\s*url\(fonts/[^)]+\)\s*format\("(woff|truetype)"\)', '', css)


def cover_page(cover, foot):
    """표지 겸 목차: 제목·안내, 전공 A/B 정답표를 나란히, 검토 메모."""
    m = re.search(r'(<h3>전공 A.*?</table>)\s*(<h3>전공 B.*?</table>)', cover, re.S)
    grid = f'<div class="grid2"><div>{m.group(1)}</div><div>{m.group(2)}</div></div>'
    cover = cover[:m.start()] + grid + cover[m.end():]
    return f'<section class="page cover"><div class="fit">{cover}{foot}</div></section>'


def question_page(chunk):
    """문항 한 개: 제목 띠 아래 3단 흐름. 원문 → 정답 → 공식·핵심 개념 → 출제 가능성 → 풀이 순서로 이어진다."""
    h2 = re.match(r'<h2 id="([^"]+)">(.*?)</h2>', chunk, re.S)
    rest = chunk[h2.end():]
    qs = re.findall(r'<img class="q" src="(img/[^"]+)"[^>]*>', rest)
    # 긴 문항은 crop_questions.py가 A05.png, A05_2.png …로 나눠 둔다
    qs = [x for q in qs for x in [q] + sorted(f'img/{f}' for f in os.listdir(os.path.join(ROOT, 'img'))
                                                  if re.fullmatch(re.escape(os.path.basename(q)[:-4]) + r'_\d+\.png', f))]
    rest = re.sub(r'(<p>\s*)?<img class="q" src="img/[^"]+"[^>]*>(\s*</p>)?', '', rest)
    # 정답 상자 속 구조식·그림은 상자 밖 바로 아래 블록으로 빼서, 큰 상자가 통째로 다음 단으로 밀리지 않게 한다
    def split_ans(m):
        box = m.group(0)
        imgs = re.findall(r'<img class="s[^"]*"[^>]*>', box)
        box = re.sub(r'<p>\s*(<img class="s[^"]*"[^>]*>\s*)+</p>', '', box)
        box = re.sub(r'<img class="s[^"]*"[^>]*>', '', box)
        return box + ''.join(f'<div class="ansfig">{i}</div>' for i in imgs)
    rest = re.sub(r'<div class="ans">.*?</div>', split_ans, rest, count=1, flags=re.S)
    figs = ''.join(f'<figure class="orig"><img src="{q}" style="width:{Image.open(os.path.join(ROOT, q)).size[0] * MM_PER_PX:.1f}mm" alt="문항 원문"></figure>'
                   for q in qs)
    return (f'<section class="page q">'
            f'<div class="qhead"><h2 id="{h2.group(1)}">{h2.group(2)}</h2><a class="top" href="#toc">목차로 ↑</a></div>'
            f'<div class="flow">{figs}'
            f'{rest}</div></section>')


def main():
    src = open(MD, encoding='utf-8').read()
    src, store = protect_math(src)
    doc = markdown.markdown(src, extensions=['tables', 'attr_list', 'md_in_html'])
    doc = re.sub(r'MATHPH(\d+)X', lambda m: html.escape(store[int(m.group(1))], quote=False), doc)

    doc, foot = doc.split('<hr />')
    start = doc.index('<h1>전공 A</h1>')
    cover, questions = doc[:start], doc[start:]
    questions = re.sub(r'<h1>전공 [AB]</h1>', '', questions)
    chunks = [c for c in re.split(r'(?=<h2 id=)', questions) if c.strip()]
    body = cover_page(cover, foot) + ''.join(question_page(c) for c in chunks)

    def embed(m):
        path = os.path.join(ROOT, m.group(1))
        mime = 'image/svg+xml' if path.endswith('.svg') else 'image/png'
        return f'src="data:{mime};base64,{b64(path)}"'
    body = re.sub(r'src="(img/[^"]+)"', embed, body)

    title = '안병천 전공화학 모의고사 4회 상세해설'
    noto = ''.join(
        f"@font-face{{font-family:'Noto Sans KR';font-weight:{w};src:url(data:font/woff2;base64,"
        f"{b64(os.path.join(FONTS, f'noto-sans-kr-korean-{w}-normal.woff2'))}) format('woff2');}}"
        for w in (400, 700))
    page = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{noto}{katex_css()}{CSS}</style>
<script>{open(os.path.join(KATEX, 'katex.min.js')).read()}</script>
<script>{open(os.path.join(KATEX, 'contrib', 'auto-render.min.js')).read()}</script>
</head><body><main>
{body}
</main>
<script>{FIT_JS}</script></body></html>"""
    open(OUT, 'w', encoding='utf-8').write(page)
    print('wrote', OUT, f'{len(page) / 1e6:.1f} MB', f'{len(chunks)} questions')


FIT_JS = r"""
renderMathInElement(document.body, {delimiters: [
  {left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}],
  throwOnError: false});
document.fonts.ready.then(() => {
  const mm = v => v * 96 / 25.4;
  const PAGE_H = mm(189);           // 210 mm − 위·아래 여백
  // 단 너비보다 넓은 수식은 그 수식만 줄인다
  const shrinkWide = root => root.querySelectorAll('.katex-display > .katex').forEach(k => {
    k.style.fontSize = '';
    let s = 1;
    while (k.scrollWidth > k.parentElement.clientWidth + 1 && s > 0.6) { s -= 0.05; k.style.fontSize = s + 'em'; }
  });
  shrinkWide(document);
  const report = [];
  document.querySelectorAll('section.cover').forEach(sec => {
    const fit = sec.querySelector('.fit');
    let pt = 10;
    for (; pt >= 9; pt -= 0.25) {
      fit.style.fontSize = pt + 'pt';
      shrinkWide(fit);
      if (sec.getBoundingClientRect().height <= PAGE_H) break;
    }
    if (pt < 9) { pt = 9; fit.style.fontSize = pt + 'pt'; shrinkWide(fit); }
    const pages = Math.ceil(sec.getBoundingClientRect().height / PAGE_H);
    report.push((sec.querySelector('h2, h1') || {}).textContent.slice(0, 18) + ' ' + pt + 'pt ' + pages + '쪽');
  });
  document.body.dataset.report = report.join('\n');
  document.body.dataset.ready = '1';
});
"""

CSS = """
:root{--ink:#1f2933;--muted:#5b6672;--line:#d5dbe3;--accent:#1d4ed8;--ans:#eef4ff;--key:#ecfdf3;--keyline:#16a34a;--odds:#f5f3ff;--oddsline:#7c3aed;--note:#fff7e6;--noteline:#e0a63b}
*{box-sizing:border-box}
html{background:#e9edf2}
body{margin:0;color:var(--ink);font-family:'Noto Sans KR',sans-serif;line-height:1.65;word-break:keep-all;orphans:2;widows:2}
main{width:277mm;margin:0 auto}
section.page{background:#fff;break-before:page;overflow-x:clip}
section.page:first-child{break-before:auto}
@media screen{section.page{margin:10mm 0;box-shadow:0 0 0 10mm #fff,0 1px 14mm rgba(0,0,0,.08)}}
@media print{html{background:none}}
h1{font-size:17pt;line-height:1.3;margin:0 0 6px;padding-bottom:6px;border-bottom:3px solid var(--ink)}
h2{font-size:14pt;margin:0;padding:5px 12px;background:var(--ink);color:#fff;border-radius:4px;flex:1}
h3{font-size:11pt;margin:8px 0 4px;color:var(--accent)}
p{margin:5px 0}
strong{color:#0b1b33}
a{color:var(--accent);text-decoration:none}
table{border-collapse:collapse;width:100%;margin:6px 0;font-size:.92em;line-height:1.45;break-inside:avoid}
th,td{border:1px solid var(--line);padding:3px 6px;vertical-align:middle;text-align:left}
th{background:#f1f4f8;font-weight:700}
ul,ol{padding-left:20px;margin:4px 0}
li{margin:2px 0;break-inside:avoid}
.qhead{display:flex;align-items:center;gap:10px;margin-bottom:4mm;break-after:avoid}
.qhead .top{font-size:9pt;white-space:nowrap;border:1px solid var(--line);border-radius:4px;padding:3px 8px}
.flow{font-size:10pt;columns:3;column-gap:7mm;column-rule:1px solid var(--line);column-fill:auto}
.flow>p:has(>strong:first-child){break-after:avoid}
.flow>p:has(>strong:only-child){break-after:avoid}
figure.orig{margin:0 0 4mm;break-inside:avoid}
figure.orig img{display:block;max-width:100%;border:1px solid var(--line);border-radius:3px}
.ans,.key,.odds,.note{border-radius:4px;padding:5px 11px;margin:0 0 3.5mm;break-inside:avoid}
.ans{background:var(--ans);border-left:5px solid var(--accent)}
.ansfig{border-left:5px solid var(--accent);background:#f7faff;border-radius:4px;margin:-2.5mm 0 3.5mm;padding:2px 6px;break-inside:avoid}
.key{background:var(--key);border-left:5px solid var(--keyline)}
.key>p:first-child strong{color:#15803d}
.key ul{padding-left:16px}
.odds{background:var(--odds);border-left:5px solid var(--oddsline);font-size:.95em}
.odds strong{color:#5b21b6}
.stars{color:#d97706;letter-spacing:1px}
.note{background:var(--note);border-left:5px solid var(--noteline)}
.ans>p:first-child,.key>p:first-child{margin-top:2px}
img.s{display:block;max-width:100%;width:auto;height:auto;margin:6px auto;break-inside:avoid}
.katex{font-size:1.04em}
.katex .katex-mathml{display:none}
.katex-display{margin:6px 0;overflow:hidden;break-inside:avoid}
.cover .grid2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:6mm}
.cover h2{flex:none;display:block;margin:8px 0 4px}
.cover .note ol{columns:2;column-gap:8mm}
.foot{color:var(--muted);font-size:.85em;margin-top:6px}
@page{size:A4 landscape;margin:10mm 10mm 11mm}
"""

if __name__ == '__main__':
    main()
