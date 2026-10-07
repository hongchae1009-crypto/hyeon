# v3: 문항별 탐구 그림·모형 포함, 표지 없이 1문항 1페이지, 문항별 모범 답안·해설(교과서 탐구 캡처 포함) 1페이지
import html, json, pathlib, re, sys
sys.dont_write_bytecode = True
from build_v2 import Q, stars, esc, unit_of, CUR
import items_m3  # noqa: F401  중3 16~20번을 Q에 추가
from figs import FIG
from expl_v3 import EXPL

HERE = pathlib.Path(__file__).parent
CAPDIR = HERE / "캡처"
FIT_JS = """<script>
// 화면 렌더 폭을 인쇄 폭(182mm)에 맞춘 뒤, 한 페이지(약 248mm)를 넘는 해설 페이지의 캡처 이미지를 줄인다.
window.addEventListener("load",function(){const mm=96/25.4, lim=248*mm;
document.querySelectorAll('.ansp').forEach(pg=>{let ims=pg.querySelectorAll('.caps img'); const tall=[...ims].every(im=>im.naturalHeight>im.naturalWidth*0.9); if(ims.length==2&&tall){const c=pg.querySelector('.caps'); c.style.flexDirection='row'; c.style.alignItems='flex-start'; c.querySelectorAll('figure').forEach(f=>f.style.flex='1');} let h=(ims.length>1&&!tall)?95:140; ims.forEach(im=>im.style.maxHeight=h+'mm');
 while(pg.scrollHeight>lim && h>25){h-=3; pg.querySelectorAll('.caps img').forEach(im=>im.style.maxHeight=h+'mm');}});
document.querySelectorAll('.pg:not(.ansp)').forEach(pg=>{let f=10.2; while(pg.scrollHeight>lim && f>8.4){f-=0.3; pg.style.fontSize=f+"pt";}});});
</script>"""
SMALL = {}  # 문항 번호 -> 글자 크기(pt), 한 페이지 넘칠 때 조정
# 다른 문항 세트(예: 통합과학)에서 바꿔 쓰는 설정값
CAP_PREFIX = "q"
COVER_TITLE = "중등 화학 임용 대비 과교론 기출 변형 {N}제 <small>(탐구 그림·교과서 캡처 포함판)</small>"
COVER_SUB = ("2022 개정 중학교 과학 1~3학년 화학 단원 — (4) 물질의 상태 변화 · (6) 기체의 성질 · (8) 물질의 특성 · (11) 물질의 구성 · (16) 화학 반응의 규칙성<br>"
             "소재: 비상교육·미래엔 교과서의 탐구 활동 + {CUR} 원문(성취기준·성취기준 해설·적용 시 고려 사항·탐구 활동·내용 체계·교수·학습 및 평가)")
COVER_LEGEND = "◦ 파란 굵은 글씨로 표시한 &lt;자료&gt;는 교육과정 원문을 그대로 옮긴 것이며, 빈칸은 원문의 해당 용어입니다. ◦ [ ] 안은 변형한 원 기출(화교론 우선, 물·생·지는 경향 참고)입니다.<br>"
OUT_STEM = "화교론_기출변형{N}제_중1-3_그림포함"

def caps_for(i):
    meta = {}
    mf = CAPDIR / "captions.json"
    if mf.exists():
        meta = json.loads(mf.read_text(encoding="utf-8"))
    out = []
    for p in sorted(CAPDIR.glob(f"{CAP_PREFIX}{i}_*.png")):
        out.append((p.name, meta.get(p.name, "교과서 탐구 활동")))
    return out

def cover():
    rows, N = [], len(Q)
    for i, it in enumerate(Q, 1):
        theme = re.sub(r"\s*변형$", "", it["src"])
        rows.append(f"<tr><td>{i}</td><td>{esc(unit_of(it['tb']))}</td><td>{esc(theme)}</td><td class='star'>{stars(it['star'])}</td><td>{i+1}</td><td>{i+1+N}</td></tr>")
    return f"""<section class='pg cover'><h1>{COVER_TITLE.format(N=N)}</h1>
<div class='sub'>{COVER_SUB.format(CUR=CUR)}</div>
<div class='legend'>{COVER_LEGEND}
◦ 별점은 2024–2026 물화생지 과교론 출제 경향 기준 중요도·출제 가능성입니다. ◦ 모든 문항은 4점 서술형이며, 한 문항이 한 쪽입니다.<br>
◦ 모범 답안 및 해설({N+2}–{2*N+1}쪽)은 문항별 1쪽으로, 관련 교과서 탐구 캡처 · 모범 답안 · 해설(핵심 이론, 교육과정 근거, 채점 포인트, 출제 포인트) 순으로 실었습니다.</div>
<table class='idx'><tr><th>번호</th><th>교과서·단원</th><th>원 기출 / 핵심 이론</th><th>별점</th><th>문제 쪽</th><th>해설 쪽</th></tr>{''.join(rows)}</table></section>"""

def main():
    pages = [cover()]
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
            imgs = "".join(f"<figure><img src='{CAPDIR.name}/{n}'><figcaption>{esc(c)}</figcaption></figure>" for n, c in caps)
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
.cover h1{margin-top:0;font-size:15pt}.cover .sub,.cover .legend{font-size:8.8pt}.cover .idx{font-size:8.4pt}.cover .idx td{padding:2px 4px;line-height:1.35}.idx th{white-space:nowrap}.idx td:nth-child(1),.idx td:nth-child(5),.idx td:nth-child(6){text-align:center;white-space:nowrap}
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
    doc = f"""<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>화교론 기출변형 {len(Q)}제</title><style>{css}</style></head><body>
{''.join(pages)}{FIT_JS}</body></html>"""
    out = HERE / (OUT_STEM.format(N=len(Q)) + ".html")
    out.write_text(doc, encoding="utf-8")
    print(out, len(Q))

if __name__ == "__main__":
    main()
