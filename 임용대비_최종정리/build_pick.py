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
}
SETNAME = {"M": "교과서 변형 중1-3 20제", "T": "교과서 변형 통합과학·화학 20제", "E": "교과서 변형 물에·화반 16제"}
MOCK = lambda r: ROOT / f"모의고사/화학교육론_실전모의고사_{r}회.pdf"
MOCK_POS = {"A5": (0, 0), "A6": (0, 1), "A7": (1, 0), "B3": (2, 0), "B4": (2, 1), "B5": (3, 0)}
MOCK_ANS = {"A5": 4, "A6": 5, "A7": 6, "B3": 7, "B4": 8, "B5": 9}

# (그룹, 출처 키, 제목, 왜 봐야 하나(최근 기출 연결), 오개념·실험 유의점 포인트)
GROUPS = [
 ("A. 개념 변화 모형의 단계 구분 — 헷갈렸던 드라이버 단계부터", [
  ("mock5B4", "드라이버 구성주의 수업 모형(기체의 압력)", "2025 화학 A7 드라이버, 단계 이름 쓰기형", "‘생각의 표현’(활동지에 쓰기) vs ‘명료화와 교환’(발표·비교·토론) / 기체 입자가 멈춰 꽉 차 있다는 오개념, 압력 = 입자 충돌"),
  ("T3", "드라이버 생각의 재구성 세부 단계(이온 결합·공유 결합 물질 성질 비교)", "2025 화학 A7 · 2019 화학 드라이버", "㉡ 명료화와 교환(서로의 생각 설명·비교) → ㉢ 상충된 상황에 노출(6홈판 실험) / ‘염화 나트륨 분자’ 표현 오류, 고체 NaCl은 전류 X"),
  ("E6", "드라이버 모형과 엔트로피(자발적 변화)", "2015 화학 논술(엔트로피·드라이버) · 2023 화학 B4(범위 위배)", "‘자발적 = 발열’ 오개념 → 엔트로피 증가 흡열 반응 / 교육과정 범위 밖 계획 찾기"),
  ("M9", "포스너 개념 변화 조건(밀도)", "2017 화학 논술 밀도·포스너, 2026 화학 B3 포스너", "밀도 오개념(무거우면 가라앉는다, 양이 많으면 밀도 큼) / 그럴듯함·유용성을 교사 활동으로 쓰기"),
  ("T2", "발생 학습 모형 도전 단계(원자의 전자 배치)", "2018 화학 논술 발생 학습 · 26 예측 이월", "초점 → 도전(관점 비교·과학자 관점·증거) 구분 / 18족 원자가 전자 수 0 오개념"),
 ]),
 ("B. 로슨 순환 학습 3유형 — 화학은 경험–귀추적만 나왔음", [
  ("mock1B4", "로슨 가설–연역적 순환 학습(농도 변화와 평형 이동)", "2026 물리·생물 3유형 구분, 2024 지구 가설–연역적", "학생이 가설을 세우고 검증 실험을 설계하는가가 판단 근거 / 평형 이동 = 반응 속도 오개념"),
  ("T12", "로슨 순환 학습 유형 구분(분자 구조, VSEPR)", "2025 화학 B3 · 2022 화학 B4 · 2026 생물 A7", "1·2차시 유형을 근거 문장으로 구분 / 비공유 전자쌍 무시 오개념, 자석 모형의 한계"),
 ]),
 ("C. 과학철학 · 과학적 추론 — 물·생·지에서 최근 계속 출제", [
  ("mock5A6", "포퍼 반증주의(바틀렛의 제논 화합물)", "2026 지구 A5 포퍼, 2024 물리·생물", "반증 가능성 · 반증주의 한계 · 후건 긍정"),
  ("T13", "포퍼 반증과 임시방편 가설(극성 물질)", "2024 물리 A6 · 2018 화학 논술", "가설을 땜질하면 반증 가능성이 줄어든다 / 대전된 빨대 실험 물질 선택 오류"),
  ("mock2A6", "유추와 모형의 한계(반트호프 삼투압)", "2026 물리 A5 유추, 화학 미출제", "유추의 형식 · 비유물–목표물 대응 · 한계"),
  ("M11", "귀추와 귀추적 탐구(순물질과 혼합물)", "2023 화학 A5 귀추 · 2026 지구 A6 귀추적 탐구 모형", "귀추 형식(C 관찰 → A면 C 설명 → A일 것) / 밀도·녹는점·끓는점은 측정 조건과 함께, 혼합물은 일정하지 않음"),
  ("E5", "가설–연역적 탐구와 실험 오류(중화 반응으로 헤스 법칙)", "2026 화학 A6 가설 연역 · 2026 화학 A5 실험 오류", "가설 → 예측(연역) → 검증 / 단열·온도 측정 시점 등 실험 설계 문제점"),
 ]),
 ("D. 5E · 평가 — 화학에서 아직 안 나왔거나 매년 나오는 것", [
  ("T6", "5E 정교화 단계(산과 염기 혼합 시 온도 변화)", "2025 물리·지구 5E 정교화, 화학 미출제", "㉠ 정교화 = 산성 토양·제산제처럼 새 상황에 개념 확장 / 최고 온도가 중화점 아닌 홈에서 나온 원인(측정 방법)"),
  ("M7", "평가 계획 · 채점 기준 · 피드백(냉각 곡선)", "2026 지구 A7 분석적 채점·피드백 · 2016 화학", "성취기준 해설 빈칸(열에너지 출입) · 평가 요소별 채점 기준 · 학생 답에 줄 피드백 / 상태 변화 중 온도 일정 이유"),
 ]),
 ("E. 실험 유의점 · 오차 · 조작적 정의 — 문제로 내기 가장 명확한 것", [
  ("T17", "표준 용액 만들기(오차 방향·관찰 평가표)", "2026 화학 A5 실험 오류·오차 방향 · 2017 체크리스트", "용매 500 mL에 녹임 → 농도 작아짐, 비커 안 헹굼 → 농도 작아짐 / 부피 플라스크 쓰는 이유 / ‘성실하게’ 같은 관찰 불가 평가 항목 수정"),
  ("T1", "같은 족 원소 실험 설계(Li·Na 안전, 변인, 동료 평가)", "2018 화학 Li·Na 안전 · 2022 화학 A7 동료 평가", "금속 조각 크기를 같게(변인 통제) · 반응 중 비커를 손으로 감싸지 않기 · 남은 금속은 싱크대 X(석유 속 보관) / 근거 없는 동료 평가 댓글"),
  ("M17", "질량 보존(부력, 툴민 논증)", "2025 화학 A7 질량 보존 · 2026 지구 A5 툴민", "기체 발생 반응을 열린 용기에서 측정 · 부력 영향(고려 사항 원문) / 논거·보강"),
  ("mock5B5", "조작적 정의와 변인 통제(농도와 반응 속도, 압력 센서)", "2026 생물 B5 조작적 정의 · 2026 물리 B3 변인 통제", "반응 속도 = 1/시간 등 측정 가능한 정의 / 통제 변인 찾기"),
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
    first = 21 if s == "T" else 17
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
<h1>과교론 반드시 볼 문제 18선 — 직접 만든 문제에서 엄선</h1>
<p class='sub'>대상: 교과서 변형 중1-3 20제 · 통합과학·화학 20제 · 물질과 에너지·화학 반응의 세계 16제 · 실전 모의고사 1~5회(30문항) — 총 86문항 중 18문항</p>
<div class='box'><p><b>고른 기준</b> ① 2027 출제 예상 상위 주제(포퍼, 로슨 3유형, 추론, 평가, 5E, 개념 변화 모형)와 직접 맞는 문항 ② 교과서 오개념이나 실험 유의점이 답으로 딱 떨어지는 문항 ③ 약한 파트로 보이는 개념 변화 모형 단계 구분(드라이버·발생 학습)을 맨 앞에</p>
<p><b>보는 법</b> 번호(S01~)를 누르면 문제로 이동, 문제 다음 쪽이 모범 답안·해설, 각 문제 첫 쪽 오른쪽 위 ‘엄선 목차로’를 누르면 여기로 돌아옴</p></div>
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
    dst = HERE / "과교론_반드시볼문제_엄선18.pdf"
    out.save(dst, garbage=4, deflate=True)
    hp.unlink(); tp.unlink()
    print(dst.name, len(out), "쪽, 목차", ntoc, "쪽")

if __name__ == "__main__":
    build()
