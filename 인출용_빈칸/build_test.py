# -*- coding: utf-8 -*-
"""꼭 암기할 부분 인출 테스트지(A4) + 정답 PDF"""
import html, pathlib, re, subprocess, sys
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).parent; sys.path.insert(0, str(HERE))
from test_spec import T
CHROME = "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome"
no, body, key = 1, [], []
for title, lines in T:
    lis = []
    for ln in lines:
        def rep(m):
            global no
            a = m.group(1); w = max(3.0, 0.95 * len(a) + 1.4)
            key.append((no, a, title)); s = f"<span class='bl' style='min-width:{w:.1f}em'><i>{no}</i></span>"; no += 1
            return s
        lis.append("<li>" + re.sub(r"\[\[(.+?)\]\]", rep, ln) + "</li>")
    body.append(f"<h2>{html.escape(title)}</h2><ul>{''.join(lis)}</ul>")
N = no - 1
css = """@page{size:A4;margin:12mm 13mm 13mm}body{font-family:'NanumGothic',sans-serif;font-size:9.6pt;line-height:2.1;margin:0;color:#111}
.hd{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.4pt solid #111;padding-bottom:1.5mm;margin-bottom:2mm;line-height:1.4}
.hd h1{font-size:13.5pt;margin:0}.hd .sub{font-size:8.3pt;color:#444}.who span{display:inline-block;border-bottom:.8pt solid #111;min-width:24mm}
h2{font-size:10pt;margin:3mm 0 .5mm;padding:.5mm 2mm;background:#eef1f5;border-left:3pt solid #1a3d6d;line-height:1.5;break-after:avoid}
ul{margin:0;padding-left:4mm;list-style:'◦ '}li{margin:0 0 .6mm;word-break:keep-all}
.bl{display:inline-block;border-bottom:.8pt solid #111;height:1.2em;vertical-align:-.15em;position:relative;margin:0 .12em}
.bl i{font-style:normal;font-size:6.6pt;color:#666;position:absolute;left:.1em;top:-.2em}
.ans{font-size:9pt;line-height:1.5}.ans h1{font-size:13pt;border-bottom:1.2pt solid #000;padding-bottom:1.5mm}
.g{column-count:3;column-gap:6mm;column-rule:.5pt solid #ccc}.g div{break-inside:avoid}.g b{display:inline-block;min-width:7mm;color:#1a3d6d}"""
hd = f"<div class='hd'><div><h1>과학교육론 핵심 암기 — 인출 테스트</h1><div class='sub'>정리본(26.11.05) 중 꼭 외울 단계명·유형·조건만 모음 · 빈칸 {N}개</div></div><div class='who'>날짜 <span></span>&nbsp; 점수 <span style='min-width:14mm'></span> / {N}</div></div>"
docs = {"핵심암기_인출테스트": hd + "".join(body),
        "핵심암기_인출테스트_정답": "<div class='ans'><h1>핵심 암기 인출 테스트 — 정답</h1><div class='g'>" + "".join(f"<div><b>{n}</b>{html.escape(a)}</div>" for n, a, _ in key) + "</div></div>"}
for stem, b in docs.items():
    h = HERE / f"{stem}.html"
    h.write_text(f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>{stem}</title><style>{css}</style></head><body>{b}</body></html>", encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={HERE / (stem + '.pdf')}", f"file://{h}"], capture_output=True)
print("빈칸", N)
