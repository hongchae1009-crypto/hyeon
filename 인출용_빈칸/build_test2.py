# -*- coding: utf-8 -*-
import html, pathlib, re, subprocess, sys
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).parent; sys.path.insert(0, str(HERE))
from test2_spec import L
CHROME = "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome"
no, key = 1, []
def blanks(s):
    global no
    out, i = [], 0
    for m in re.finditer(r"\[\[(.+?)\]\]", s):
        out.append(s[i:m.start()]); a = m.group(1)
        w = max(3.2, 1.0 * len(a) + 1.4)
        out.append(f"<span class='bl' style='min-width:{w:.1f}em'><i>{no}</i></span>"); key.append((no, a)); no += 1; i = m.end()
    out.append(s[i:]); return "".join(out)
parts, box = [], None
for raw in L.strip("\n").split("\n"):
    if box is not None:
        if raw.endswith("]BOX"):
            box.append(raw[:-4]); parts.append("<div class='box'>" + "".join(f"<p>{blanks(x)}</p>" for x in box) + "</div>"); box = None
        else: box.append(raw)
        continue
    if raw.startswith("BOX["):
        rest = raw[4:]
        if rest.endswith("]BOX"): parts.append(f"<div class='box'><p>{blanks(rest[:-4])}</p></div>")
        else: box = [rest]
        continue
    if raw == "SP": parts.append("<div class='sp'></div>")
    elif raw.startswith("H:"): parts.append(f"<h2>{blanks(raw[2:])}</h2>")
    elif raw.startswith("S:"): parts.append(f"<h3>{blanks(raw[2:])}</h3>")
    elif raw.startswith("s:"): parts.append(f"<h4>{blanks(raw[2:])}</h4>")
    elif raw.strip() == "↓": parts.append("<p class='ar'>↓</p>")
    elif raw.startswith("•"): parts.append(f"<p class='it'>{blanks(raw)}</p>")
    else: parts.append(f"<p class='ln'>{blanks(raw)}</p>")
N = no - 1
css = """@page{size:A4;margin:13mm 12mm 13mm}body{font-family:'NanumGothic',sans-serif;font-size:9.3pt;line-height:1.95;margin:0;color:#111}
.hd{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1.2pt solid #111;padding-bottom:1mm;margin-bottom:2mm;line-height:1.4}
.hd b{font-size:12pt}.who span{display:inline-block;border-bottom:.8pt solid #111;min-width:22mm}
.cols{column-count:2;column-gap:8mm;column-rule:.5pt solid #bbb}
h2{text-align:center;font-size:10pt;margin:3mm 0 1.5mm;break-after:avoid}
h3{font-size:9.4pt;margin:2mm 0 .3mm;font-weight:bold;break-after:avoid}h4{font-size:9.2pt;margin:1.2mm 0 .2mm;font-weight:normal;break-after:avoid}
p{margin:0}.it{padding-left:3.2mm;text-indent:-3.2mm}.ln{padding-left:2mm}.ar{padding-left:6mm;line-height:1.3}
.box{border:.7pt solid #333;padding:1mm 2mm;margin:1mm 0 1mm 3mm;break-inside:avoid}.sp{height:2mm}
.bl{display:inline-block;border-bottom:.8pt solid #111;height:1.2em;vertical-align:-.15em;position:relative;margin:0 .12em}
.bl i{font-style:normal;font-size:6.2pt;color:#777;position:absolute;left:.1em;top:-.25em}
.ans{font-size:9pt;line-height:1.5}.ans h1{font-size:13pt;border-bottom:1.2pt solid #000;padding-bottom:1.5mm}
.g{column-count:3;column-gap:6mm;column-rule:.5pt solid #ccc}.g div{break-inside:avoid}.g b{display:inline-block;min-width:7mm;color:#1a3d6d}"""
hd = f"<div class='hd'><div><b>과교론 암기 필요 파트 — 인출 테스트</b> <small>(빈칸 {N}개)</small></div><div class='who'>날짜 <span></span>&nbsp; 점수 <span style='min-width:12mm'></span> / {N}</div></div>"
docs = {"암기필요파트_인출테스트": hd + "<div class='cols'>" + "".join(parts) + "</div>",
        "암기필요파트_인출테스트_정답": "<div class='ans'><h1>암기 필요 파트 인출 테스트 — 정답</h1><div class='g'>" + "".join(f"<div><b>{n}</b>{html.escape(a)}</div>" for n, a in key) + "</div></div>"}
for stem, b in docs.items():
    h = HERE / f"{stem}.html"
    h.write_text(f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>{stem}</title><style>{css}</style></head><body>{b}</body></html>", encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={HERE / (stem + '.pdf')}", f"file://{h}"], capture_output=True)
print("빈칸", N)
