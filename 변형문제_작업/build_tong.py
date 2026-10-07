# 통합과학 기출 변형 10제 빌더 — build_v3의 레이아웃(표지·1문항 1쪽·문항별 해설 쪽)을 그대로 사용
import pathlib, sys
sys.dont_write_bytecode = True
import build_v3 as B
from items_tong import QT, CURT
from figs_tong import FIGT
from expl_tong import EXPLT

B.Q = QT
B.FIG = FIGT
B.EXPL = EXPLT
B.CUR = CURT
B.CAPDIR = B.HERE / "캡처_통과"
B.CAP_PREFIX = "t"
B.COVER_TITLE = "중등 화학 임용 대비 과교론 기출 변형 — 통합과학 {N}제 <small>(탐구 그림·교과서 캡처 포함판)</small>"
B.COVER_SUB = ("2022 개정 고등학교 공통 과목 ‘통합과학1’·‘통합과학2’ 화학 관련 단원 — 과학의 기초 · 물질과 규칙성 · 변화와 다양성(화학 변화)<br>"
               "소재: 비상교육·미래엔 통합과학 교과서의 탐구 활동 + 2022 개정 과학과 교육과정(교육부 고시 제2022-33호) 통합과학 원문(성취기준·탐구 활동·성취기준 해설·교수·학습 및 평가)")
B.COVER_LEGEND = ("◦ 파란 굵은 글씨로 표시한 &lt;자료&gt;는 교육과정 원문을 그대로 옮긴 것이며, 빈칸은 원문의 해당 용어입니다. "
                  "◦ [ ] 안은 변형한 원 기출(화교론 우선, 물·생·지는 경향 참고)입니다.<br>")
import re
def _unit_of(tb):
    m = re.search(r"\[(.*?)\]\s*([ⅠⅡⅢⅣⅤⅥ]-?\d?)", tb)
    return (m.group(1) + " " + m.group(2)) if m else tb
B.unit_of = _unit_of
B.OUT_STEM = "화교론_기출변형_통합과학{N}제_그림포함"

if __name__ == "__main__":
    B.main()
