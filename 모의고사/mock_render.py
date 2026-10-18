# -*- coding: utf-8 -*-
"""화학교육론 실전 모의고사 렌더러 — 한국교육과정평가원 문제지 형식(A3 2단)을 본뜬 HTML → PDF.
문항 데이터: dict(no, part('A'|'B'), stem, blocks=[(제목, html)], how=[...], ans=[...], score=[...], note=...)"""
import html, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

CSS = """
@page{size:297mm 420mm;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:'NanumMyeongjo','Nanum Myeongjo',serif;color:#111;font-size:10.6pt;line-height:1.66;word-break:keep-all}
.page{width:297mm;height:420mm;position:relative;padding:20mm 15mm 22mm;page-break-after:always;overflow:hidden}
.page:last-child{page-break-after:auto}
.top{position:absolute;left:15mm;right:15mm;top:14mm;border-top:1.6pt solid #000}
.cols{display:flex;height:100%;border-top:0}
.col{flex:1;padding:4mm 6mm 0 2mm;overflow:hidden}
.col+.col{border-left:.9pt solid #000;padding-left:7mm;padding-right:2mm}
.foot{position:absolute;left:15mm;right:15mm;bottom:12mm;border-top:.9pt solid #000;padding-top:2.5mm;text-align:center;font-weight:bold;font-size:11pt;letter-spacing:.5px}
.foot .big{font-size:17pt;vertical-align:-1.5pt}
.foot .org{position:absolute;left:0;top:3mm;font-size:8.5pt;font-weight:normal;color:#444}
.notice{font-size:10pt;margin:0 0 3mm}
.item{margin:0 0 7mm}
.stem{margin:0 0 2.6mm;text-indent:-1.15em;padding-left:1.15em;text-align:justify}
.stem b.no{font-size:12.5pt;margin-right:.25em}
.pts{float:right}
fieldset{border:.8pt solid #222;margin:3.2mm 0;padding:2.2mm 3.4mm 2.6mm;min-width:0}
legend{margin:0 auto;padding:0 .7em;font-size:10.4pt;letter-spacing:.15em}
fieldset p{margin:.4mm 0;text-align:justify}
fieldset .ind{text-indent:-1.6em;padding-left:1.6em}
fieldset .dlg{display:grid;grid-template-columns:auto 1fr;column-gap:.5em}
fieldset .dlg span:nth-child(odd){white-space:nowrap}
fieldset table{border-collapse:collapse;margin:1.5mm auto;font-size:9.8pt}
fieldset td,fieldset th{border:.6pt solid #333;padding:.6mm 2.2mm;text-align:center;font-weight:normal}
fieldset th{background:#f2f2f2}
.how p{text-indent:-1.15em;padding-left:1.15em}
u{text-underline-offset:2px}
.cen{text-align:center}
.small{font-size:9.4pt}
.blank{color:#888;text-align:center;margin-top:60mm;font-size:12pt}
/* 정답 책자 */
.ans{font-family:'NanumGothic',sans-serif;font-size:9.6pt;line-height:1.6}
.ans .page{height:auto;min-height:420mm}
.ah{font-size:13pt;font-weight:bold;border-bottom:1.4pt solid #000;padding-bottom:1.5mm;margin:0 0 3mm}
.ai{border:.8pt solid #999;border-radius:2mm;padding:3mm 4mm;margin:0 0 4mm;break-inside:avoid}
.ai h3{margin:0 0 1.5mm;font-size:11pt}
.ai table{width:100%;border-collapse:collapse;margin:1.5mm 0}
.ai td,.ai th{border:.6pt solid #888;padding:1mm 2mm;vertical-align:top;text-align:left}
.ai th{background:#eef2f7;width:15%}
.ai .sc{width:12%;text-align:center}
.ai .note{background:#fafaf3;border-left:3px solid #c9b46b;padding:1.5mm 3mm;margin-top:2mm}
.acols{column-count:2;column-gap:8mm;column-rule:.6pt solid #bbb}
"""

FIT = """<script>
window.addEventListener('load',()=>{document.querySelectorAll('.col').forEach(c=>{let f=10.6;
 while(c.scrollHeight>c.clientHeight+1&&f>8.6){f-=0.2;c.style.fontSize=f+'pt';}});});
</script>"""

def esc(s): return s  # 문항 데이터는 HTML로 작성(밑줄·아래 첨자 등)

def item_html(it):
    blocks = "".join(f"<fieldset><legend>&lt;{t}&gt;</legend>{b}</fieldset>" for t, b in it["blocks"])
    how = "".join(f"<p>○ {h}</p>" for h in it["how"])
    return (f"<div class='item'><p class='stem'><b class='no'>{it['no']}.</b> {it['stem']} <span class='pts'>[4점]</span></p>"
            f"{blocks}<fieldset class='how'><legend>&lt;작성 방법&gt;</legend>{how}</fieldset></div>")

def page(cols, part, rnd, k, n, notice=False):
    inner = []
    for i, c in enumerate(cols):
        pre = "<p class='notice'>◦ 문제지 전체 면수가 맞는지 확인하시오.<br>◦ 모든 문항에는 배점이 표시되어 있습니다.</p>" if notice and i == 0 else ""
        inner.append(f"<div class='col'>{pre}{c}</div>")
    return (f"<section class='page'><div class='top'></div><div class='cols'>{''.join(inner)}</div>"
            f"<div class='foot'><span class='org'>화학교육론 실전 모의고사 · {rnd}회</span>화  학 [전공{part}] (모의 {rnd}회, {n}면 중 <span class='big'>{k}</span> 면)</div></section>")

def booklet(items, part, rnd):
    # 1면: 첫 두 문항(좌·우 단), 2면: 셋째 문항(좌 단) + 여백
    a, b, c = [item_html(x) for x in items]
    return page([a, b], part, rnd, 1, 2, notice=True) + page([c, "<p class='blank'>(이 면은 여백입니다.)</p>"], part, rnd, 2, 2)

def answer_html(items, rnd):
    out = [f"<div class='ah'>화학교육론 실전 모의고사 {rnd}회 — 모범 답안 및 채점 기준</div><div class='acols'>"]
    for it in items:
        rows = "".join(f"<tr><th>작성 {i+1}</th><td>{a}</td><td class='sc'>{s}</td></tr>" for i, (a, s) in enumerate(zip(it["ans"], it["score"])))
        out.append(f"<div class='ai'><h3>전공{it['part']} {it['no']}번 · {it['topic']}</h3>"
                   f"<table><tr><th>구분</th><th style='width:auto'>모범 답안</th><th class='sc'>배점</th></tr>{rows}</table>"
                   f"<div class='note'><b>출제 근거·해설</b> {it['note']}</div></div>")
    out.append("</div>")
    return "<div class='ans'><section class='page' style='padding:16mm 15mm'>" + "".join(out) + "</section></div>"

def render(items, rnd, out_stem):
    A = [x for x in items if x["part"] == "A"]; Bp = [x for x in items if x["part"] == "B"]
    body = booklet(A, "A", rnd) + booklet(Bp, "B", rnd) + answer_html(items, rnd)
    doc = f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>화학교육론 실전 모의고사 {rnd}회</title><style>{CSS}</style></head><body>{body}{FIT}</body></html>"
    h = HERE / f"{out_stem}.html"; h.write_text(doc, encoding="utf-8")
    pdf = HERE / f"{out_stem}.pdf"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=8000", f"--print-to-pdf={pdf}", f"file://{h}"], capture_output=True)
    return pdf
