# 통합과학1·2 + 화학 중요 문항 20제 빌더 — build_v3의 레이아웃(표지·1문항 1쪽·문항별 해설 쪽)을 그대로 사용
# 1~7번: 통합과학 10제의 4~10번, 8~20번: 고등학교 '화학' 13문항
import json, pathlib, re, shutil, sys
sys.dont_write_bytecode = True
import build_v3 as B
from items_tong import QT
from figs_tong import FIGT
from expl_tong import EXPLT
from items_chem import QC
from figs_chem import FIGC
from expl_chem import EXPLC

TONG = [4, 5, 6, 7, 8, 9, 10]
CHEM = ["mol", "stoich", "elec", "en", "vsepr", "polar", "dyn", "K", "shift", "std", "ph", "titr", "ssi"]

Q, FIG, EXPL = [], {}, {}
for k in TONG:
    Q.append(QT[k - 1]); FIG[len(Q)] = FIGT[k]; EXPL[len(Q)] = EXPLT[k]
for k in CHEM:
    Q.append(QC[k]); FIG[len(Q)] = FIGC[k]; EXPL[len(Q)] = EXPLC[k]

CAPDIR = B.HERE / "캡처_통과화학"

def gather_caps(chem_src=None):
    """캡처_통과의 t4~t10을 h1~h7로, chem_src(h8~h20)를 그대로 모아 캡처_통과화학에 둔다."""
    CAPDIR.mkdir(exist_ok=True)
    meta = {}
    tmeta = json.loads((B.HERE / "캡처_통과" / "captions.json").read_text(encoding="utf-8"))
    for n, k in enumerate(TONG, 1):
        for p in sorted((B.HERE / "캡처_통과").glob(f"t{k}_*.png")):
            new = f"h{n}_" + p.name.split("_", 1)[1]
            shutil.copy(p, CAPDIR / new); meta[new] = tmeta.get(p.name, "교과서 탐구 활동")
    if chem_src:
        src = pathlib.Path(chem_src)
        cmeta = json.loads((src / "captions.json").read_text(encoding="utf-8")) if (src / "captions.json").exists() else {}
        for p in sorted(src.glob("h*_*.png")):
            shutil.copy(p, CAPDIR / p.name); meta[p.name] = cmeta.get(p.name, "교과서 탐구 활동")
    (CAPDIR / "captions.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")

B.Q, B.FIG, B.EXPL = Q, FIG, EXPL
B.CUR = "2022 개정 과학과 교육과정 ‘통합과학1’·‘통합과학2’·‘화학’"
B.CAPDIR = CAPDIR
B.CAP_PREFIX = "h"
B.COVER_TITLE = "중등 화학 임용 대비 과교론 기출 변형 — 통합과학·화학 중요 문항 {N}제 <small>(탐구 그림·교과서 캡처 포함판)</small>"
B.COVER_SUB = ("2022 개정 고등학교 ‘통합과학1’·‘통합과학2’ 화학 관련 단원(1~7번) + 일반 선택 ‘화학’ 전 단원(8~20번) — 화학의 언어 · 물질의 구조와 성질 · 화학 평형 · 역동적인 화학 반응<br>"
               "소재: 비상교육·미래엔 교과서의 탐구 활동 + {CUR} 원문(성취기준·탐구 활동·성취기준 해설·적용 시 고려 사항·내용 체계·교수·학습 및 평가)")
B.COVER_LEGEND = ("◦ 파란 굵은 글씨로 표시한 &lt;자료&gt;는 교육과정 원문을 그대로 옮긴 것이며, 빈칸은 원문의 해당 용어입니다. "
                  "◦ [ ] 안은 변형한 원 기출(화교론 우선, 물·생·지는 경향 참고)입니다. ◦ 지도서 문장은 쓰지 않았고, 오개념·유의점만 기출 유형에 맞게 재구성했습니다.<br>")
def _unit_of(tb):
    m = re.search(r"\[(.*?)\]\s*([ⅠⅡⅢⅣⅤⅥ]-?\d?)", tb)
    return (m.group(1) + " " + m.group(2)) if m else tb
B.unit_of = _unit_of
B.OUT_STEM = "화교론_기출변형_통합과학화학{N}제_그림포함"

if __name__ == "__main__":
    gather_caps(sys.argv[1] if len(sys.argv) > 1 else None)
    B.main()
