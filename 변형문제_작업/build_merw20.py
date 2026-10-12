# '물질과 에너지' + '화학 반응의 세계' 엄선 20제 빌더 — build_v3의 레이아웃(표지·1문항 1쪽·문항별 해설 쪽)을 그대로 사용
# 1~10번: 물질과 에너지, 11~20번: 화학 반응의 세계. 캡처 파일은 p{번호}_{k}.png
import json, pathlib, re, shutil, sys
sys.dont_write_bytecode = True
import build_v3 as B
from items_me import QE
from items_rw import QR
from figs_merw import FIGE, FIGR
from expl_merw import EXPLE, EXPLR

ME = ["gas", "hbp", "colli", "fuel", "hess", "ent", "press", "order", "conc", "tcat"]
RW = ["ph4", "titc", "salt", "buf", "hyper", "oxn", "mb", "cell", "plate", "fut"]

Q, FIG, EXPL = [], {}, {}
for k in ME:
    Q.append(QE[k]); FIG[len(Q)] = FIGE[k]; EXPL[len(Q)] = EXPLE[k]
for k in RW:
    Q.append(QR[k]); FIG[len(Q)] = FIGR[k]; EXPL[len(Q)] = EXPLR[k]

CAPDIR = B.HERE / "캡처_물에화반"

def gather_caps(src):
    """작업 폴더(src)의 p*_*.png와 captions.json을 캡처_물에화반으로 모은다."""
    CAPDIR.mkdir(exist_ok=True)
    src = pathlib.Path(src)
    meta = json.loads((src / "captions.json").read_text(encoding="utf-8")) if (src / "captions.json").exists() else {}
    out = {}
    for p in sorted(src.glob("p*_*.png")):
        shutil.copy(p, CAPDIR / p.name); out[p.name] = meta.get(p.name, "교과서 탐구 활동")
    (CAPDIR / "captions.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

B.Q, B.FIG, B.EXPL = Q, FIG, EXPL
B.CUR = "2022 개정 과학과 교육과정 진로 선택 ‘물질과 에너지’·‘화학 반응의 세계’"
B.CAPDIR = CAPDIR
B.CAP_PREFIX = "p"
B.COVER_TITLE = "중등 화학 임용 대비 과교론 기출 변형 — 물질과 에너지·화학 반응의 세계 엄선 {N}제 <small>(탐구 그림·교과서 캡처 포함판)</small>"
B.COVER_SUB = ("2022 개정 고등학교 진로 선택 ‘물질과 에너지’(1~10번: 물질의 세 가지 상태 · 용액의 성질 · 화학 변화의 자발성 · 반응 속도) + "
               "‘화학 반응의 세계’(11~20번: 산 염기 평형 · 산화・환원 반응)<br>"
               "소재: 비상교육·미래엔 교과서의 탐구 활동 + {CUR} 원문(성취기준·탐구 활동·성취기준 해설·적용 시 고려 사항·내용 체계·교수·학습 및 평가)")
B.COVER_LEGEND = ("◦ 파란 굵은 글씨로 표시한 &lt;자료&gt;는 교육과정 원문을 그대로 옮긴 것이며, 빈칸은 원문의 해당 용어입니다. "
                  "◦ [ ] 안은 변형한 원 기출(화교론 우선, 물·생·지는 경향 참고)입니다. ◦ 지도서 문장은 쓰지 않았고, 오개념·유의점만 기출 유형에 맞게 재구성했습니다.<br>")
def _unit_of(tb):
    m = re.search(r"\[(.*?)\]\s*([ⅠⅡⅢⅣⅤⅥ]-?\d?)", tb)
    return (m.group(1) + " " + m.group(2)) if m else tb
B.unit_of = _unit_of
_esc = B.esc
def _esc_sub(s):  # 문항 본문의 아래 첨자(K<sub>a</sub> 등)는 그대로 살린다
    return re.sub(r"&lt;(/?)(sub|sup)&gt;", r"<\1\2>", _esc(s))
B.esc = _esc_sub
B.OUT_STEM = "화교론_기출변형_물질과에너지·화학반응의세계{N}제_그림포함"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        gather_caps(sys.argv[1])
    B.main()
