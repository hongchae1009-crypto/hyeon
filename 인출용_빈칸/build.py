# -*- coding: utf-8 -*-
"""정리 노트 PDF(한글 변환) 원본 위에서 외울 말만 지우고 번호 빈칸을 넣는다 → 인출용 PDF + 정답 PDF"""
import sys, pathlib, html, subprocess
sys.dont_write_bytecode = True
import pymupdf
HERE = pathlib.Path(__file__).parent; sys.path.insert(0, str(HERE))
from spec import B
SRC = pathlib.Path(sys.argv[1])
CHROME = "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome"

d = pymupdf.open(SRC)
lines = {}
for pi, p in enumerate(d, 1):
    L = []
    for b in p.get_text("rawdict")["blocks"]:
        for ln in b.get("lines", []):
            cs = [c for s in ln["spans"] for c in s["chars"]]
            if cs: L.append(("".join(c["c"] for c in cs), cs))
    lines[pi] = L

def locate(pg, ctx, term, nth=0):
    hits = []
    for txt, cs in lines[pg]:
        i = txt.find(ctx)
        while i >= 0:
            hits.append((txt, cs, i)); i = txt.find(ctx, i + 1)
    if len(hits) <= nth: return None
    txt, cs, i = hits[nth]
    k = txt.find(term, i)
    if k < 0 or k >= i + len(ctx): return None
    sel = cs[k:k + len(term)]
    r = pymupdf.Rect(sel[0]["bbox"])
    for c in sel: r |= pymupdf.Rect(c["bbox"])
    return r

miss, marks = [], {}
for item in B:
    pg, ctx, term = item[:3]; nth = item[3] if len(item) > 3 else 0
    r = locate(pg, ctx, term.strip(), nth)
    if r is None: miss.append(item); continue
    if any(r.intersects(o) for o, _ in marks.get(pg, [])): miss.append(item + ("겹침",)); continue
    marks.setdefault(pg, []).append((r, term.strip()))

ans, no = [], 1
for pg in sorted(marks):
    p = d[pg - 1]
    ms = sorted(marks[pg], key=lambda m: (round(m[0].y0), m[0].x0))
    for r, t in ms:
        p.add_redact_annot(r + (-0.6, -0.4, 0.6, 0.4), fill=(1, 1, 1))
    p.apply_redactions(images=0, graphics=0)
    for r, t in ms:
        w = max(r.width, 14)
        y = r.y1 + 0.6
        p.draw_line((r.x0, y), (r.x0 + w, y), color=(0, 0, 0), width=0.6)
        p.insert_text((r.x0 + 0.3, r.y1 - 0.8), str(no), fontsize=5.2, color=(0.45, 0.45, 0.45))
        ans.append((no, pg, t)); no += 1
out = HERE / "정리노트_인출용_빈칸.pdf"
d.save(out, garbage=3, deflate=True)
rows = "".join(f"<div><b>{n}</b>{html.escape(t)} <small>p{pg}</small></div>" for n, pg, t in ans)
doc = f"""<!doctype html><html lang='ko'><head><meta charset='utf-8'><style>@page{{size:A4;margin:12mm}}
body{{font-family:'NanumGothic',sans-serif;font-size:9pt;line-height:1.45}}h1{{font-size:13pt;border-bottom:1pt solid #000;padding-bottom:1.5mm}}
.g{{column-count:3;column-gap:6mm;column-rule:.5pt solid #ccc}}.g div{{break-inside:avoid}}.g b{{display:inline-block;min-width:8mm;color:#1a3d6d}}.g small{{color:#999}}</style></head>
<body><h1>정리 노트 인출용 빈칸 — 정답 ({len(ans)}개)</h1><div class='g'>{rows}</div></body></html>"""
h = HERE / "정답.html"; h.write_text(doc, encoding="utf-8")
subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={HERE / '정리노트_인출용_정답.pdf'}", f"file://{h}"], capture_output=True)
print("빈칸", len(ans), "누락", len(miss))
for m in miss: print("  ", m)
