# '물질과 에너지' + '화학 반응의 세계' 최종 엄선판 빌더 (중요도 ★5 15문항 + 도금 탐구 1문항) — build_v3의 레이아웃(표지·1문항 1쪽·문항별 해설 쪽)을 그대로 사용
# 1~10번: 물질과 에너지, 11~20번: 화학 반응의 세계. 캡처 파일은 p{번호}_{k}.png
import json, pathlib, re, shutil, sys
sys.dont_write_bytecode = True
import build_v3 as B
from items_me import QE
from items_rw import QR
from figs_merw import FIGE, FIGR
from expl_merw import EXPLE, EXPLR

ME = ["gas", "hbp", "colli", "osm", "hess", "ent", "order", "tcat"]
RW = ["ph4", "titc", "salt", "buf", "mb", "cell", "plate", "carb"]
# 20제 번호(캡처 파일 번호) → 최종판 번호
OLD = {"gas": 1, "hbp": 2, "colli": 3, "osm": 4, "hess": 5, "ent": 6, "order": 8, "tcat": 10, "ph4": 11, "titc": 12, "salt": 13, "buf": 14, "mb": 16, "cell": 17, "plate": 18, "carb": 20}

Q, FIG, EXPL = [], {}, {}
for k in ME:
    Q.append(QE[k]); FIG[len(Q)] = FIGE[k]; EXPL[len(Q)] = EXPLE[k]
for k in RW:
    Q.append(QR[k]); FIG[len(Q)] = FIGR[k]; EXPL[len(Q)] = EXPLR[k]

CAPDIR = B.HERE / "캡처_물에화반_최종"

def gather_caps(src):
    """작업 폴더(src)의 p*_*.png와 captions.json을 캡처_물에화반으로 모은다."""
    CAPDIR.mkdir(exist_ok=True)
    src = pathlib.Path(src)
    meta = json.loads((src / "captions.json").read_text(encoding="utf-8")) if (src / "captions.json").exists() else {}
    out = {}
    new_of = {OLD[k]: i for i, k in enumerate(ME + RW, 1)}
    for p in sorted(src.glob("p*_*.png")):
        n, rest = re.match(r"p(\d+)_(.+)$", p.name).groups()
        if int(n) not in new_of: continue
        nm = f"p{new_of[int(n)]}_{rest}"
        shutil.copy(p, CAPDIR / nm); out[nm] = meta.get(p.name, "교과서 탐구 활동")
    (CAPDIR / "captions.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

B.Q, B.FIG, B.EXPL = Q, FIG, EXPL
B.CUR = "2022 개정 과학과 교육과정 진로 선택 ‘물질과 에너지’·‘화학 반응의 세계’"
B.CAPDIR = CAPDIR
B.CAP_PREFIX = "p"
B.COVER_TITLE = "중등 화학 임용 대비 과교론 기출 변형 — 물질과 에너지·화학 반응의 세계 최종 엄선 {N}제 <small>(탐구 그림·교과서 캡처 포함판)</small>"
B.COVER_SUB = ("2022 개정 고등학교 진로 선택 ‘물질과 에너지’(1~8번: 물질의 세 가지 상태 · 용액의 성질 · 화학 변화의 자발성 · 반응 속도) + "
               "‘화학 반응의 세계’(9~16번: 산 염기 평형 · 산화・환원 반응 · 탄소 화합물과 반응)<br>"
               "소재: 비상교육·미래엔 교과서의 탐구 활동 + {CUR} 원문(성취기준·탐구 활동·성취기준 해설·적용 시 고려 사항·내용 체계·교수·학습 및 평가)")
B.COVER_LEGEND = ("◦ 파란 굵은 글씨로 표시한 &lt;자료&gt;는 교육과정 원문을 그대로 옮긴 것이며, 빈칸은 원문의 해당 용어입니다. "
                  "◦ [ ] 안은 변형한 원 기출(화교론 우선, 물·생·지는 경향 참고)입니다. ◦ 지도서 문장은 쓰지 않았고, 오개념·유의점만 기출 유형에 맞게 재구성했습니다. ◦ 선정 기준: 출제 가능성 ★5 문항 전부 + 화학 반응의 세계 도금 탐구(실험 안전·채점) 1문항, 영역별 교육과정 탐구 활동과 성취기준 해설의 범위 제한을 빠짐없이 포함.<br>"
                  "<style>.cover .idx{font-size:7.6pt}.cover .idx td{padding:1px 3px;line-height:1.25}.cover .sub,.cover .legend{font-size:8.2pt}.cover h1{font-size:14pt}.caps:has(figure:nth-child(3)){display:grid!important;grid-template-columns:1fr 1fr;gap:4px 8px;align-items:start}.caps:has(figure:nth-child(3)) img{max-width:100%}</style>")
def _unit_of(tb):
    m = re.search(r"\[(.*?)\]\s*([ⅠⅡⅢⅣⅤⅥ]-?\d?)", tb)
    return (m.group(1) + " " + m.group(2)) if m else tb
B.unit_of = _unit_of
_esc = B.esc
def _esc_sub(s):  # 문항 본문의 아래 첨자(K<sub>a</sub> 등)는 그대로 살린다
    return re.sub(r"&lt;(/?)(sub|sup)&gt;", r"<\1\2>", _esc(s))
B.esc = _esc_sub
B.OUT_STEM = "화교론_기출변형_물질과에너지·화학반응의세계_최종엄선{N}제"


# ── 해설 2쪽 구성: (1) 교과서 탐구 캡처 전용 쪽 (2) 모범 답안·해설 쪽 ──
def _cover():
    rows, N = [], len(B.Q)
    for i, it in enumerate(B.Q, 1):
        theme = re.sub(r"\s*변형$", "", it["src"])
        a = N + 2 + 2 * (i - 1)
        rows.append(f"<tr><td>{i}</td><td>{B.esc(B.unit_of(it['tb']))}</td><td>{B.esc(theme)}</td><td class='star'>{B.stars(it['star'])}</td><td>{i+1}</td><td>{a}–{a+1}</td></tr>")
    return f"""<section class='pg cover'><h1>{B.COVER_TITLE.format(N=N)}</h1>
<div class='sub'>{B.COVER_SUB.format(CUR=B.CUR)}</div>
<div class='legend'>{B.COVER_LEGEND}
◦ 별점은 2024–2026 물화생지 과교론 출제 경향 기준 중요도·출제 가능성입니다. ◦ 모든 문항은 4점 서술형이며, 한 문항이 한 쪽입니다.<br>
◦ 모범 답안 및 해설({N+2}–{3*N+1}쪽)은 문항별 2쪽으로, 첫 쪽에 관련 교과서 탐구 캡처(비상교육·미래엔)를 크게 싣고, 둘째 쪽에 모범 답안 · 해설(핵심 이론, 교육과정 근거, 채점 포인트, 두 교과서 비교, 출제 포인트)을 실었습니다.</div>
<table class='idx'><tr><th>번호</th><th>교과서·단원</th><th>원 기출 / 핵심 이론</th><th>별점</th><th>문제 쪽</th><th>해설 쪽</th></tr>{''.join(rows)}</table></section>"""
B.cover = _cover

CAP_JS = """<script>
window.addEventListener("load",function(){const mm=96/25.4, lim=248*mm;
document.querySelectorAll('.capp').forEach(pg=>{const c=pg.querySelector('.caps'); if(!c) return; const ims=[...c.querySelectorAll('img')]; const n=ims.length;
 const tall=ims.every(im=>im.naturalHeight>im.naturalWidth*0.9); let h;
 if(n==1){h=228;} else if(n==2&&tall){c.style.flexDirection='row';c.style.alignItems='flex-start';c.querySelectorAll('figure').forEach(f=>f.style.flex='1');h=228;}
 else if(n==2){c.style.flexDirection='column';h=110;} else {h=n<=4?108:72;}
 ims.forEach(im=>{im.style.maxHeight=h+'mm';im.style.maxWidth='100%';});
 while(pg.scrollHeight>lim && h>30){h-=2; ims.forEach(im=>im.style.maxHeight=h+'mm');}});});
</script>"""

def split_answer_pages(html_path):
    html = html_path.read_text(encoding="utf-8")
    def rep(m):
        sec = m.group(0)
        meta = re.search(r"<div class='meta'>.*?</div>\n", sec, re.S).group(0)
        i_ans = sec.index("<div class='h3'>■ 모범 답안</div>")
        top = sec[:i_ans].replace("<section class='pg ansp'>", "<section class='pg ansp capp'>", 1) + "</section>"
        bottom = "<section class='pg ansp'>" + meta.replace("모범 답안 및 해설", "모범 답안 및 해설 (계속)") + sec[i_ans:]
        return top + bottom
    html = re.sub(r"<section class='pg ansp'>.*?</section>", rep, html, flags=re.S)
    html = html.replace("</body></html>", CAP_JS + "</body></html>")
    html_path.write_text(html, encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        gather_caps(sys.argv[1])
    B.main()
    split_answer_pages(B.HERE / (B.OUT_STEM.format(N=len(Q)) + ".html"))
