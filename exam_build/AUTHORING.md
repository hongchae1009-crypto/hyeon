# 기출변형 문항 작성 지침 (에이전트 공용)

## 목표
중등교사 임용 화학(1차 전공A/B) **유기화학 기출 66문항을 1:1로 변형**한 고품질 문항을 만든다.
각 변형 문항은 (1) 원 기출의 유형·배점·발문 형식을 따르고, (2) **Klein 유기화학 교재에 인용된 실제 논문의 반응**을 소재로 사용하며,
(3) 가능하면 **노벨 화학상 주제**와 연계하고, (4) 상세한 정답·해설을 갖춘다. 결과물은 A4 인쇄용 시험지/해설지로 자동 조판된다.

## 자료 위치 (SCR = /tmp/claude-0/-home-user-hyeon/e196aa5e-9821-56b2-b877-2f07b790959e/scratchpad)
- 기출 유기 문항 카탈로그(원문 발문, 반응식 SMILES, 정답):
  - 2014–2017: SCR/exam_organic_catalog_2014-2017.md
  - 2018–2021: SCR/exam_organic_catalog_2018-2021.md
  - 2022–2026: SCR/exam_organic_catalog.md
  - 원문 페이지 이미지: SCR/exam/<YYYYX>/p-N.jpg (필요 시 확인. 2014~2021은 PDF 페이지 = 인쇄 면수−1)
- 교재 인용 논문·반응 추출본 (Klein 1–23장): SCR/extract_1-6.md, extract_7-11a.md(7–9장), extract_7-11b.md(9장 후반·10·11·12장),
  extract_12-14.md(13–14장), extract_15-19.md, extract_20-23.md
- 견본 문항: /home/user/hyeon/exam_build/items/area_D.py (반드시 먼저 읽을 것)

## 출력 형식
`/home/user/hyeon/exam_build/items/<지정 파일명>.py` 에 `ITEMS = [dict(...), ...]` 를 작성한다. 필드:
- `key`: 지정된 기출 키 (예 '2024A-11') — 정확히 일치해야 함
- `src`: 표시용 '2024학년도 A형 11번' (2014A 기입/서술 체계는 '2014학년도 A형 서술형 4번', 논술형은 'B형 논술형 2번' 식)
- `src_topic`: 원 기출 문항 요지 한 줄
- `change`: 기출 대비 무엇을 어떻게 바꿨는지 (출제 의도 포함)
- `paper`: dict(cite='J. Org. Chem. 2009, 74, 5458–5470' ← 추출본 참고문헌 그대로, book='Klein 13.68', what='논문/문제의 반응 요지')
- `nobel`: 관련 노벨 화학상(연도·수상자·주제) 또는 '' (억지 연결 금지)
- `body`: 문제 HTML. 배점 자리에는 문자열 `[[PTS]]` 를 넣는다(자동 치환). 끝은 `<p class="ask">…요구사항… [[PTS]]</p>`
- `answer`: 정답 HTML (구조식은 M(SMILES, 라벨, scale) 사용)
- `explain`: 해설 HTML (`<p>①…</p><p>②…</p>` 단계별, 메커니즘·입체·근거 상세; 오답 함정도 언급)
- 선택: `stars` (1~3, 기본은 영역 별점)

## 조판 도구 (from chem import ...)
- `M(smiles, label='', scale=17)` 구조식 SVG (입체 SMILES면 쐐기 자동). 단 폭 85 mm ≈ 320 px — 한 줄에 구조 2~3개 + 화살표가 한계, scale 14~18 권장.
- `L('A')` 굵은 화합물 기호, `arrow(top, bottom)` 시약 화살표(폭 자동), `varrow(left, right)` 아래 화살표,
  `scheme(...)` 한 줄, `rows(scheme(...), varrow(...), scheme(...))` 여러 줄, `frame(..., title='[반응 1]')` 테두리 상자, `plus()`.
- 스펙트럼: `spec(nmr([(δ, 's'|'d'|'t'|'q'|'quint'|'sext'|'sept'|'dd'|'m'|'br', 적분, '표시'), ...], title='¹H NMR 스펙트럼(300 MHz, CDCl₃)', x0=10, x1=0))`,
  ¹³C는 `nmr(..., title='¹³C NMR', x0=220, x1=0, tms=False)` (다중도 's'), `spec(ir([(파수, 깊이0~1, 폭, '라벨'), ...]))`.
  분광 문항은 표(`<table class="data">`)로 δ/다중도/적분을 함께 주어도 좋다(기출처럼 스펙트럼 + 필요시 표).
- 아래/위 첨자는 HTML `<sub>`, `<sup>`. 화합물 기호는 `<b class="lbltxt">A</b>`.

## 발문 형식 (기출 관례)
- "다음은 ○○로부터 중간 주생성물 **A**(C<sub>x</sub>H<sub>y</sub>O<sub>z</sub>)와 **B**를 거쳐 최종 주생성물 **C**를 합성하는 반응을 나타낸 것이다. (단, 각 반응에서는 적절한 분리·정제 과정을 수행하였다.)"
- 요구 동사: "구조를 그리시오", "입체구조를 그리시오", "굽은 화살표를 사용하여 반응 메커니즘을 제시하시오", "순서대로 나열하시오", "그 이유를 서술하시오".
- 2점(기입형)은 요구 1~2개, 4점(서술형)은 요구 3~4개(구조 + 메커니즘/이유). 원 기출의 배점·유형을 유지.
- 문항 하나가 단 높이(약 240 mm)를 넘지 않게: 반응식 상자 + 발문이 대략 단의 1/2~3/4 이내.

## 품질 규칙 (매우 중요)
1. **화학적으로 정확**해야 한다. 모든 SMILES는 RDKit으로 파싱·분자식 확인(제시한 분자식과 일치), 입체 SMILES는 CIP(R/S)와 cis/trans를 RDKit으로 검증.
2. 정답이 **유일**하게 결정되도록 조건(분자식, 주생성물, 당량, 온도, 스펙트럼 단서)을 충분히 준다.
3. 논문 소재는 추출본의 **[high] 신뢰도** 반응을 우선 사용. 복잡한 천연물은 반응 중심부만 단순화한 "모델 화합물"로 바꿔도 되며, 이때 해설에 "논문의 ○○ 단계를 모델화"라고 밝힌다. 인용(cite)은 추출본에 적힌 그대로 — **지어내지 말 것**.
4. 기출을 그대로 베끼지 말고, 같은 평가 요소(개념·사고과정)를 **다른 기질/시약/조건**으로 묻는다. 난이도는 기출과 같거나 약간 높게.
5. 노벨상 연계 후보: 2021(List·MacMillan 비대칭 유기촉매: 프롤린 알돌/Hajos–Parrish, 엔아민·이미늄), 2022(Sharpless·Meldal·Bertozzi 클릭/생체직교: CuAAC, SPAAC),
   2010(Heck·Negishi·Suzuki Pd 짝지음), 2005(Chauvin·Grubbs·Schrock 복분해), 2001(Knowles·Noyori·Sharpless 비대칭 수소화·산화), 1994(Olah 탄소 양이온),
   1990(Corey 역합성), 1979(Brown 수소화붕소화·Wittig), 1950(Diels·Alder), 1912(Grignard·Sabatier), 2024(단백질 설계—아미노산 소재일 때), 2025(MOF—해당 시만). 자연스러울 때만.
6. 해설은 수험생이 혼자 공부할 수 있을 만큼 상세하게: 단계별 근거, 메커니즘 서술(굽은 화살표 흐름을 말로), 입체화학 근거, 흔한 오답.
7. 한국어 용어는 기출 표기 따름(주생성물, 엔올레이트, 카보닐, 다이아조늄, 고리 형성 등). 화합물 이름은 영어 IUPAC/관용명.

## 검증·미리보기
- `cd /home/user/hyeon/exam_build && python3 build.py --preview items/<파일>.py` → out/preview_<파일>_문제지.pdf / _정답해설.pdf
- `pdftoppm -r 70 -jpeg out/preview_<파일>_문제지.pdf <SCR>/pv_<파일>` 로 이미지 확인(Read). 빨간 테두리(overflow) 없어야 하고 반응식이 깨지지 않아야 한다.
- 여러 에이전트가 동시에 작업하므로 **자기 파일만** 수정하고, build.py/chem.py/style.css는 수정하지 말 것(필요하면 보고).
