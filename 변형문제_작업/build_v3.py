# v3: 문항별 탐구 그림·모형 포함, 표지 없이 1문항 1페이지, 문항별 모범 답안·해설(교과서 탐구 캡처 포함) 1페이지
import html, json, pathlib, re, sys
sys.dont_write_bytecode = True
from build_v2 import Q, stars, esc
from figs import FIG
from expl_v3 import EXPL

HERE = pathlib.Path(__file__).parent
CAPDIR = HERE / "캡처"
FIT_JS = """<script>
// 화면 렌더 폭을 인쇄 폭(182mm)에 맞춘 뒤, 한 페이지(약 248mm)를 넘는 해설 페이지의 캡처 이미지를 줄인다.
window.addEventListener("load",function(){const mm=96/25.4, lim=248*mm;
document.querySelectorAll('.ansp').forEach(pg=>{let ims=pg.querySelectorAll('.caps img'), h=ims.length>1?95:140; ims.forEach(im=>im.style.maxHeight=h+'mm');
 while(pg.scrollHeight>lim && h>25){h-=3; pg.querySelectorAll('.caps img').forEach(im=>im.style.maxHeight=h+'mm');}});
document.querySelectorAll('.pg:not(.ansp)').forEach(pg=>{let f=10.2; while(pg.scrollHeight>lim && f>8.4){f-=0.3; pg.style.fontSize=f+"pt";}});});
</script>"""
SMALL = {}  # 문항 번호 -> 글자 크기(pt), 한 페이지 넘칠 때 조정

def caps_for(i):
    meta = {}
    mf = CAPDIR / "captions.json"
    if mf.exists():
        meta = json.loads(mf.read_text(encoding="utf-8"))
    out = []
    for p in sorted(CAPDIR.glob(f"q{i}_*.png")):
        out.append((p.name, meta.get(p.name, "교과서 탐구 활동")))
    return out

def main():
    pages = []
    for i, it in enumerate(Q, 1):
        fs = SMALL.get(i)
        style = f" style='font-size:{fs}pt'" if fs else ""
        data_html = "".join(f"<div class='box'><div class='lab'>&lt;{esc(t)}&gt;</div>{body}</div>" for t, body in it["data"])
        how_html = "".join(f"<li>{esc(h)}</li>" for h in it["how"])
        fig = f"<div class='fig'>{FIG[i]}</div>" if i in FIG else ""
        pages.append(f"""<section class='pg'{style}><div class='meta'><span class='src'>[{esc(it['src'])}]</span>
<span class='star'>중요도/출제가능성 {stars(it['star'])}</span></div>
<div class='tb'>교과서 탐구: {esc(it['tb'])}</div>
<p class='stem'><b>{i}.</b> {esc(it['stem'])}</p>{fig}{data_html}
<div class='box how'><div class='lab'>&lt;작성 방법&gt;</div><ul>{how_html}</ul></div></section>""")
    for i, it in enumerate(Q, 1):
        caps = caps_for(i)
        if caps:
            imgs = "".join(f"<figure><img src='캡처/{n}'><figcaption>{esc(c)}</figcaption></figure>" for n, c in caps)
            capbox = f"<div class='caps n{min(len(caps),2)}'>{imgs}</div>"
        else:
            capbox = f"<div class='fig'>{FIG[i]}</div><p class='fc'>교과서 탐구 장면을 그림으로 나타낸 것</p>"
        a = "".join(f"<li>{esc(x)}</li>" for x in it["ans"])
        ex = "".join(f"<p class='ex'><b>[{esc(k)}]</b> {esc(v)}</p>" for k, v in EXPL.get(i, []))
        pages.append(f"""<section class='pg ansp'><div class='meta'><span class='src'>{i}번 모범 답안 및 해설 [{esc(it['src'])}]</span>
<span class='star'>{stars(it['star'])}</span></div>
<div class='h3'>■ 관련 교과서 탐구 — {esc(it['tb'])}</div>{capbox}
<div class='h3'>■ 모범 답안</div><ul class='al'>{a}</ul>
<div class='h3'>■ 해설</div>{ex}<p class='ex'><b>[출제 포인트]</b> {esc(it['point'])}</p></section>""")
    css = (HERE / "variant_style.css").read_text(encoding="utf-8") + """
.cur{font-weight:bold;color:#1a3d6d}
body{width:182mm;margin:0}
.q{page-break-before:auto}
.pg{page-break-after:always;break-inside:avoid}
.pg:last-of-type{page-break-after:auto}
.fig{text-align:center;margin:6px 0 4px}.fig svg{max-width:100%;height:auto;max-height:62mm}
.fc{text-align:center;font-size:8.6pt;color:#555;margin:0 0 6px}
.h3{font-weight:bold;margin:8px 0 4px;border-left:4px solid #1a3d6d;padding-left:6px}
.caps{display:flex;flex-direction:column;gap:4px;align-items:center}
.caps figure{margin:0;text-align:center}
.caps img{max-width:100%;max-height:60mm;border:1px solid #888}
.caps.n1 img{max-height:100mm}
.caps figcaption{font-size:8.4pt;color:#444;margin-top:2px}
.al{margin:2px 0;padding-left:18px}.al li{margin:3px 0}
.ex{margin:2px 0;text-align:justify}
"""
    doc = f"""<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>화교론 기출변형 15제 v3</title><style>{css}</style></head><body>
{''.join(pages)}{FIT_JS}</body></html>"""
    out = HERE / "화교론_기출변형15제_중1-2_v3_그림포함.html"
    out.write_text(doc, encoding="utf-8")
    print(out, len(Q))

if __name__ == "__main__":
    main()
