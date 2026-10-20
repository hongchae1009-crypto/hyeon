"""모의고사1회_상세해설.md → 독립 실행형 HTML(이미지·글꼴·KaTeX 내장).

사용법: python3 build.py <katex_dist_dir> <noto_sans_kr_files_dir>
PDF는 같은 폴더의 print.js로 이 HTML을 인쇄해 만든다.
"""
import base64, html, os, re, sys
import markdown

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
KATEX, FONTS = sys.argv[1], sys.argv[2]
MD = os.path.join(ROOT, '모의고사1회_상세해설.md')
OUT = os.path.join(ROOT, '모의고사1회_상세해설.html')


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
        name = m.group(1)
        return f"url(data:font/woff2;base64,{b64(os.path.join(KATEX, 'fonts', name))})"
    css = re.sub(r'url\(fonts/([^)]+?\.woff2)\)', font, css)
    # woff/ttf 대체 경로는 지운다 (woff2만 내장)
    return re.sub(r',\s*url\(fonts/[^)]+\)\s*format\("(woff|truetype)"\)', '', css)


def main():
    src = open(MD, encoding='utf-8').read()
    src, store = protect_math(src)
    body = markdown.markdown(src, extensions=['tables', 'attr_list', 'md_in_html'])
    body = re.sub(r'MATHPH(\d+)X', lambda m: html.escape(store[int(m.group(1))], quote=False), body)

    def embed(m):
        path = os.path.join(ROOT, m.group(1))
        mime = 'image/svg+xml' if path.endswith('.svg') else 'image/png'
        return f'src="data:{mime};base64,{b64(path)}"'
    body = re.sub(r'src="(img/[^"]+)"', embed, body)

    title = '전공화학 모의고사 1회 상세해설'
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
<script>
renderMathInElement(document.body, {{delimiters: [
  {{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}],
  throwOnError: false}});
document.body.dataset.ready = '1';
</script></body></html>"""
    open(OUT, 'w', encoding='utf-8').write(page)
    print('wrote', OUT, f'{len(page) / 1e6:.1f} MB')


CSS = """
:root{--ink:#1f2933;--muted:#5b6672;--line:#d5dbe3;--accent:#1d4ed8;--ans:#eef4ff;--note:#fff7e6;--noteline:#e0a63b;--bg:#ffffff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'Noto Sans KR',sans-serif;font-size:10.5pt;line-height:1.7;word-break:keep-all}
main{max-width:820px;margin:0 auto;padding:28px 16px 60px}
h1{font-size:20pt;line-height:1.35;margin:0 0 12px;padding-bottom:10px;border-bottom:3px solid var(--ink)}
main>h1:not(:first-child){margin-top:36px;break-before:page}
h2{font-size:14pt;margin:34px 0 12px;padding:6px 12px;background:var(--ink);color:#fff;border-radius:4px;break-after:avoid}
h3{font-size:12pt;margin:20px 0 8px;color:var(--accent)}
h1+h2{break-before:avoid}
p{margin:8px 0}
strong{color:#0b1b33}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:9.5pt;break-inside:avoid}
th,td{border:1px solid var(--line);padding:5px 8px;vertical-align:middle;text-align:left}
th{background:#f1f4f8;font-weight:700}
a{color:var(--accent);text-decoration:none}
img.s.wide{max-height:none;width:100%}
img.q{display:block;width:96mm;max-width:100%;margin:10px auto 14px;border:1px solid var(--line);border-radius:4px;padding:4px;background:#fff}
img.s{display:block;max-width:100%;max-height:64mm;width:auto;height:auto;margin:8px auto}
.ans{background:var(--ans);border-left:5px solid var(--accent);border-radius:4px;padding:8px 14px;margin:12px 0 16px;break-inside:avoid}
.ans>p:first-child{margin-top:4px}
.note{background:var(--note);border-left:5px solid var(--noteline);border-radius:4px;padding:6px 14px;margin:12px 0;break-inside:avoid}
ul,ol{padding-left:22px;margin:6px 0}
li{margin:3px 0}
.katex{font-size:1.05em}
.katex-display{margin:10px 0;overflow-x:auto;overflow-y:hidden}
hr{border:none;border-top:1px solid var(--line);margin:30px 0 10px}
.foot{color:var(--muted);font-size:9pt}
@media print{main{max-width:none;padding:0}h2[id]{break-before:page;margin-top:0}main>h1:not(:first-child)+h2{break-before:avoid}}
@page{size:A4;margin:16mm 15mm 18mm}
"""

if __name__ == '__main__':
    main()
