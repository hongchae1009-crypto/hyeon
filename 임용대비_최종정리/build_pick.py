# -*- coding: utf-8 -*-
"""그동안 만든 과교론 문제(교과서 변형 3세트 + 실전 모의고사 1~5회)에서 반드시 볼 문항 엄선 → 한 PDF.
원본 PDF의 문제 쪽·해설 쪽을 그대로 뽑아 A4로 모으고, 앞에 엄선 목차(하이퍼링크)를 붙인다."""
import pathlib, subprocess
import pymupdf
HERE = pathlib.Path(__file__).parent; ROOT = HERE.parent
CHROME = str(sorted(pathlib.Path("/opt/pw-browsers").glob("chromium-*/chrome-linux*/chrome"))[-1])
SRC = {
    "M": ROOT / "변형문제_작업/화교론_기출변형20제_중1-3_그림포함.pdf",
    "T": ROOT / "변형문제_작업/화교론_기출변형_통합과학화학20제_그림포함.pdf",
    "E": ROOT / "변형문제_작업/화교론_기출변형_물질과에너지·화학반응의세계_최종엄선16제.pdf",
    "F": ROOT / "변형문제_작업/화교론_기출변형_물질과에너지·화학반응의세계20제_그림포함.pdf",
}
SETNAME = {"M": "교과서 변형 중1-3 20제", "T": "교과서 변형 통합과학·화학 20제", "E": "교과서 변형 물에·화반 16제", "F": "교과서 변형 물에·화반 20제"}
MOCK = lambda r: ROOT / f"모의고사/화학교육론_실전모의고사_{r}회.pdf"
MOCK_POS = {"A5": (0, 0), "A6": (0, 1), "A7": (1, 0), "B3": (2, 0), "B4": (2, 1), "B5": (3, 0)}
MOCK_ANS = {"A5": 4, "A6": 5, "A7": 6, "B3": 7, "B4": 8, "B5": 9}

# (그룹, 출처 키, 제목, 왜 봐야 하나(최근 기출 연결), 오개념·실험 유의점 포인트)
GROUPS = [
 ("A. 라카토스 발견법 구분 — 요약본 기준(긍정적 = 보호대 수정·보완, 부정적 = 견고한 핵 유지·변칙 무시)", [
  ("mock1A6", "라카토스 연구 프로그램(케쿨레의 벤젠 고리) — 답 수정", "2022 화학 A5 발견법 · 2026 생물 A6 · 2025 지구 A6", "고리 구조를 버리지 않음 = 부정적 / 보조 가설 ㉠을 덧붙여 설명 = 긍정적(이전 답 ‘부정적’은 오류, 이번에 바로잡음) / 새 사실 예측·확인 = 진보적"),
  ("M19", "라카토스(기체 반응 법칙과 아보가드로 분자설)", "2022 화학 A5 · 2026 생물 A6", "원자론 = 견고한 핵 · 분자 가설 = 보호대 수정(긍정적 발견법) · 변칙 사례(부피비) 설명 + 새 예측"),
 ]),
 ("B. 성취기준 해설 범위 — ‘어느 과목에서, 어디까지’ (정리본 빨간 펜 메모가 가장 많았던 부분)", [
  ("mock1A7", "‘화학 반응의 세계’ 과목 구조·핵심 아이디어·성취기준 해설", "2025 화학 A5 · 2026 화학 A7", "연계 과목(융합과학 탐구) · 완충 작용은 복잡한 pH 계산 지양 · 산화제·환원제는 정해져 있지 않음(상대적 세기)"),
  ("mock4A7", "‘화학’ 물질의 구조와 성질 성취기준 해설·고려 사항", "2023 화학 B4(혼성 오비탈 위배) · 2026 화학 A7", "쌍극자 모멘트 정성적 · 중심 원자 Be, B와 옥텟 규칙 한정 → PCl₅·SF₆(확장된 옥텟) X"),
  ("mock5A7", "‘물질과 에너지’ 성취기준 해설의 범위", "2026 화학 A7 잘못된 진술 찾기형", "결정 구조 X(결정 4종 구분만) · 적분 속도식 유도 X(자료로 반감기) · 몰랄 농도"),
  ("mock3A7", "통합과학1·2 성취기준 해설의 범위", "2024 화학 A7 · 2021 화학 A6", "산화·환원 = 산소와 전자의 이동, 산화수 X · 산·염기 = 아레니우스만 · 중화 = 온도·지시약 색만"),
  ("T4", "통합과학2 산화·환원(상관적 포섭, 산화수 범위, 잠정성)", "2016 화학 산화·환원 정의 변천 · 2024 화학 A7 · 2023 화학 B3", "전자의 이동 개념 = 상관적 포섭 / 산화수 계산은 범위 밖(→ 화학 반응의 세계)"),
  ("M15", "중학교 같은 족 원소(연역 추론, 성취기준 해설 범위)", "2026 화학 A7 · 2022 화학 A5", "‘원소의 주기성’, ‘반응의 구체적 설명·원리’ X · 1족과 물 반응은 영상으로(안전) · 연역적 추론"),
 ]),
 ("C. 고등학교 교과 개념 · 오개념 — 계산 없이 개념으로 답하는 문항", [
  ("T12", "분자 구조와 로슨 순환 학습 유형 구분(VSEPR)", "2025 화학 B3 · 2022 화학 B4 · 2026 생물 A7", "비공유 전자쌍을 빼고 구조를 정하는 오개념 · 자석 모형의 한계 · 유형 구분 근거"),
  ("T14", "동적 평형(카드 모의실험, 존스톤 세 수준)", "2023 화학 A6 표상 · 2025 화학 A7 평형 오개념", "평형 = 반응 멈춤 X(정·역반응 속도 같음) · 평형 = 농도 같음 X · NO₂ 실험은 모의실험으로"),
  ("T3", "이온 결합 물질의 성질(드라이버 생각의 재구성)", "2025 화학 A7 · 2019 화학 드라이버", "‘염화 나트륨 분자’ 표현 X · 고체 이온 결합 물질은 전류 X · 명료화와 교환 → 상충 상황 노출"),
  ("E6", "엔트로피와 자발성(드라이버, 범위)", "2015 화학 논술 · 2023 화학 B4", "자발적 = 발열 오개념 · 엔트로피는 계 전체로 판단 · 깁스 자유 에너지 X, 엔트로피 정성적"),
  ("E8", "온도·촉매와 반응 속도(하슈웨 인지 갈등)", "2025 화학 A7 하슈웨 · 2022 화학 B4 촉매", "온도↑ → 충돌 횟수 때문 X, 활성화 에너지 이상 분자 비율↑ · 촉매는 소모 X(재생), Ea 낮은 새 경로 · C1·R2·C2"),
  ("E13", "산화제·환원제(메틸렌 블루, 로슨 경험–귀추적)", "2025 화학 B3 · 2022 화학 B4", "산소만 산화제라는 오개념 · 마개 막을 때/흔들 때 산화제·환원제 구분 · NaOH 안전"),
  ("E16", "작용기 변화(은거울·음주 측정기, 관찰과 추리)", "2022 화학 A6 · 2021 화학 B5 · 2023 화학 B4", "관찰 vs 추리 구분 · 암모니아성 질산 은 보관 X · 다이크로뮴산 칼륨 안전 · 작용기 범위"),
  ("F19", "수소 연료 전지(STS 모형 단계, 전지 오개념)", "2023 화학 B5 · 2021 화학 A7 · 2022 화학 B5", "연료 전지 ≠ 이차 전지 · 생산 과정 CO₂ · STS 4단계 순서"),
 ]),
 ("D. 과학적 탐구 방법·추론 구분 — 정리본에서 ‘연역 vs 가설–연역’을 헷갈린 표시", [
  ("mock3A6", "귀추(아레니우스 전리설)와 과학의 본성", "2023 화학 A5 귀추 · 2026 지구 A6", "놀라운 현상 → 가장 잘 설명하는 가설 = 귀추 · 가설 세우고 실험으로 검증 = 가설–연역, 확립된 원리를 사례에 적용 = 연역"),
  ("mock2A6", "유추와 한계(반트호프 삼투압)", "2026 물리 A5 유추, 화학 미출제", "기반 영역(기체) ↔ 목표 영역(묽은 용액) · 대응이 모든 속성에서 성립 X"),
  ("mock5A6", "포퍼 반증주의(바틀렛의 제논 화합물)", "2026 지구 A5 · 2024 물리·생물", "반증 가능성 · 반증주의의 한계 · 후건 긍정"),
 ]),
 ("E. 실험 유의점 · 개념 변화 단계 — 문제로 내기 명확한 것", [
  ("T17", "표준 용액 만들기(농도 크게/작게, 관찰 평가표)", "2026 화학 A5 · 2017 체크리스트", "용매 500 mL에 녹임·비커 안 헹굼 → 농도 작아짐 · 부피 플라스크 이유 · ‘성실하게’ 같은 항목 X"),
  ("T1", "같은 족 원소 실험 설계(Li·Na 안전, 변인, 동료 평가)", "2018 화학 Li·Na · 2022 화학 A7", "조각 크기 같게 · 비커를 손으로 감싸지 않기 · 남은 금속 싱크대 X(석유 보관)"),
  ("mock5B5", "조작적 정의와 변인 통제(농도와 반응 속도)", "2026 생물 B5 · 2026 물리 B3", "반응 속도를 측정 가능하게 정의 · 아연 표면적도 달라진 통제 변인 오류"),
  ("mock5B4", "드라이버 구성주의 수업 모형(기체의 압력)", "2025 화학 A7 드라이버", "생각의 표현(활동지에 쓰기) vs 명료화와 교환(발표·비교·토론)"),
 ]),
]

def locate(key):
    """(문제 쪽 목록[(doc, idx, clip or None)], 해설 쪽 목록[(doc, idx)], 출처 이름)"""
    if key.startswith("mock"):
        r = int(key[4]); no = key[5:]; d = pymupdf.open(MOCK(r))
        pi, col = MOCK_POS[no]; R = d[pi].rect; w = R.width / 2
        clip = pymupdf.Rect(col * w, 0, (col + 1) * w, R.height)
        bl = [b for b in d[pi].get_text("blocks", clip=clip) if b[4].strip() and b[1] < R.height - 130]
        dr = [x["rect"] for x in d[pi].get_drawings() if clip.contains(x["rect"]) and x["rect"].y1 < R.height - 130 and x["rect"].height < 0.5 * R.height]
        ys = [b[1] for b in bl] + [r.y0 for r in dr]; ye = [b[3] for b in bl] + [r.y1 for r in dr]
        xs = [b[0] for b in bl] + [r.x0 for r in dr]; xe = [b[2] for b in bl] + [r.x1 for r in dr]
        clip = pymupdf.Rect(max(clip.x0, min(xs) - 6), max(0, min(ys) - 6), min(clip.x1, max(xe) + 6), max(ye) + 8)
        return [(d, pi, clip)], [(d, MOCK_ANS[no])], f"실전 모의고사 {r}회 전공{no[0]} {no[1]}번"
    s, n = key[0], int(key[1:]); d = pymupdf.open(SRC[s])
    if s == "M":
        return [(d, n, None)], [(d, 20 + n)], f"{SETNAME[s]} {n}번"
    first = 17 if s == "E" else 21
    a = first + 2 * (n - 1)
    return [(d, n, None)], [(d, a), (d, a + 1)], f"{SETNAME[s]} {n}번"

def build():
    A4 = pymupdf.paper_rect("a4")
    items = [(g, *x) for g, xs in GROUPS for x in xs]
    # 1) 목차 HTML
    rows = ""; no = 0
    for g, xs in GROUPS:
        rows += f"<tr><td colspan='4' class='g'>{g}</td></tr>"
        for key, title, why, point in xs:
            no += 1
            _, _, srcname = locate(key)
            rows += (f"<tr><td class='n'>S{no:02d}</td><td class='l'><b>{title}</b><br><span class='src'>{srcname}</span></td>"
                     f"<td class='l'>{why}</td><td class='l'>{point}</td></tr>")
    css = """@page{size:A4;margin:10mm 10mm}body{margin:0;font-family:'NanumGothic',sans-serif;font-size:7.6pt;line-height:1.3;color:#000}
h1{font-size:14pt;margin:0 0 1mm}.sub{font-size:7.9pt;margin:0 0 2.4mm}
.box{border:.7pt solid #000;padding:1.4mm 2.2mm;margin:0 0 2.4mm}.box p{margin:.4mm 0}
table{border-collapse:collapse;width:100%}td,th{border:.5pt solid #000;padding:.4mm 1.1mm;vertical-align:top}
th{border-bottom:1pt solid #000}td.l{text-align:left}td.n{text-align:center;font-weight:bold;white-space:nowrap}
td.g{font-weight:bold;border-top:1.1pt solid #000;padding:.9mm 1.4mm}.src{font-size:7.2pt}"""
    html = f"""<!doctype html><html lang='ko'><head><meta charset='utf-8'><style>{css}</style></head><body>
<h1>과교론 반드시 볼 문제 {len(items)}선 — 직접 만든 문제에서 엄선</h1>
<p class='sub'>대상: 교과서 변형 중1-3 20제 · 통합과학·화학 20제 · 물질과 에너지·화학 반응의 세계 16제 · 실전 모의고사 1~5회(30문항) — 총 86문항 중 {len(items)}문항 · 계산형 문항 제외</p>
<div class='box'><p><b>고른 기준</b> ① 1차 기출 정리본에서 빨간 펜·물음표·빈 답이 많았던 부분(성취기준 범위, 탐구 방법·추론 구분, 개념 변화 모형)을 우선 ② 고등학교 교과 개념(화학·물질과 에너지·화학 반응의 세계)의 오개념·실험 유의점이 답으로 딱 떨어지는 문항 ③ 2027 출제 예상 상위 주제와 맞는 문항 ④ 몰 농도·pH·ΔH·분자량·전위 등 계산이 들어간 문항은 모두 제외</p><p><b>보는 법</b> 번호(S01~)를 누르면 문제로 이동, 문제 다음 쪽이 모범 답안·해설, 각 문제 첫 쪽 오른쪽 위 ‘엄선 목차로’를 누르면 여기로 돌아옴</p></div>
<table><tr><th style='width:6%'>번호</th><th style='width:27%'>문항</th><th style='width:27%'>최근 기출과 연결</th><th>오개념 · 실험 유의점 · 짚을 점</th></tr>{rows}</table></body></html>"""
    hp = HERE / "_pick_toc.html"; hp.write_text(html, encoding="utf-8")
    tp = HERE / "_pick_toc.pdf"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={tp}", f"file://{hp}"], capture_output=True)
    out = pymupdf.open(tp); ntoc = len(out); starts = []
    font = pymupdf.Font(fontfile="/root/.fonts/NanumGothic-Bold.ttf")
    # 2) 문항 쪽 붙이기
    for k, (g, key, title, why, point) in enumerate(items, 1):
        probs, anss, srcname = locate(key)
        starts.append(len(out))
        for d, idx, clip in probs:
            if clip is None:
                out.insert_pdf(d, from_page=idx, to_page=idx)
            else:  # A3 모의고사 한 단 → A4 한 쪽에 세로로 맞춤
                pg = out.new_page(width=A4.width, height=A4.height)
                s = min((A4.height - 40) / clip.height, (A4.width - 40) / clip.width)
                w, h = clip.width * s, clip.height * s
                x0 = (A4.width - w) / 2
                pg.show_pdf_page(pymupdf.Rect(x0, 30, x0 + w, 30 + h), d, idx, clip=clip)
        for d, idx in anss:
            if d[idx].rect.width > 700:  # A3 해설 쪽 → A4
                pg = out.new_page(width=A4.width, height=A4.height)
                pg.show_pdf_page(A4, d, idx)
            else:
                out.insert_pdf(d, from_page=idx, to_page=idx)
        # 첫 쪽 머리표·되돌아가기
        pg = out[starts[-1]]; W = pg.rect.width
        tag = f"S{k:02d} · {srcname}"
        tw = pymupdf.TextWriter(pg.rect); tw.append((14, 14), tag, font=font, fontsize=7.5); tw.write_text(pg)
        back = "엄선 목차로"; bw = font.text_length(back, fontsize=7.5)
        tw = pymupdf.TextWriter(pg.rect); tw.append((W - 14 - bw, 14), back, font=font, fontsize=7.5); tw.write_text(pg)
        pg.draw_line((W - 14 - bw, 16), (W - 14, 16), width=.4)
        pg.insert_link({"kind": pymupdf.LINK_GOTO, "from": pymupdf.Rect(W - 16 - bw, 5, W - 12, 18), "page": 0})
    # 3) 목차 번호에 링크
    for k, st in enumerate(starts, 1):
        lab = f"S{k:02d}"
        for pi in range(ntoc):
            for r in out[pi].search_for(lab):
                out[pi].insert_link({"kind": pymupdf.LINK_GOTO, "from": pymupdf.Rect(r.x0 - 2, r.y0 - 2, r.x1 + 120, r.y1 + 2), "page": st})
    dst = HERE / "과교론_반드시볼문제_엄선.pdf"
    out.save(dst, garbage=4, deflate=True)
    hp.unlink(); tp.unlink()
    print(dst.name, len(out), "쪽, 목차", ntoc, "쪽")

if __name__ == "__main__":
    build()
