# -*- coding: utf-8 -*-
"""김지현 화교론 문제풀이 1~4주 엄선 문항 시험지(A3 2단, 쪽당 2문항) 빌더.
인자: 작업 폴더(주차별 문제지 쪽 이미지 q{주}-{쪽}.png, OCR q{주}-{쪽}.tsv, items.json)"""
import csv, json, pathlib, re, subprocess, sys, html
from PIL import Image
W = pathlib.Path(sys.argv[1]); HERE = pathlib.Path(__file__).parent
OUT = HERE / "img"; OUT.mkdir(exist_ok=True)
CHROME = "/opt/pw-browsers/chromium-1243/chrome-linux64/chrome"

# 2027 출제 대비 엄선 문항: (주차, 번호, 핵심 주제)
SEL = [
 (1, 2, "2022 내용 체계 핵심 아이디어·가치·태도 / 중화 반응 성취기준"), (1, 3, "로슨 순환학습 유형 · 브루너 표현 양식 · 내용 체계"),
 (1, 4, "POE 모형 단계 수정 · 가설 설정"), (1, 5, "평가표 타당성 · 가설 · 조작적 정의"), (1, 6, "하슈웨 인지 갈등 모형 · POE"),
 (1, 9, "물질 영역 내용 체계 · 2015↔2022 단원 비교"), (1, 10, "실험 보고서 평가표 · 과냉각 · 채점"), (1, 12, "ZPD · 문항 분석(난이도·변별도) · 오수벨"),
 (1, 13, "과학사 · 과학의 본성 · 반증주의와 한계"), (1, 16, "귀추적 사고 · 라카토슈 발견법 · 과정·기능"),
 (2, 2, "포퍼·라카토슈 관점 비교 · 개념 변화"), (2, 3, "POE · 라카토슈 견고한 핵 · 쿤"), (2, 6, "서술적 순환학습 · 교육과정 내용 범위"),
 (2, 9, "비고츠키 · 상태 변화 교과서 · 발문"), (2, 10, "내용 체계 · 반응 속도 실험 변인 통제"), (2, 12, "과학의 본성 · 반증 가능성 · 포스너 조건"),
 (2, 18, "로슨 서술적 → 경험-귀추적 순환학습"), (2, 20, "물질과 에너지 샤를 법칙 · 과정·기능 · 채점표"),
 (2, 24, "포퍼 반증주의 한계 · 쿤 · 라카토슈 (2024 물리 A6 각색)"), (2, 25, "가설-연역 · 후건 긍정의 오류 (2024 생물 A6 각색)"),
 (3, 1, "내용 체계 · 평가 준거 작성 · 탐구 유의점"), (3, 2, "POE vs 가설-연역적 수업 모형"), (3, 5, "라카토슈 발견법 · 관찰의 이론 의존성 · 쿤"),
 (3, 7, "물질과 에너지 내용 체계 · 디지털 도구 · 성취기준 해설"), (3, 11, "카플러스 순환학습 ↔ 쿤 · 하슈웨"), (3, 14, "오수벨 상위적 학습 · 비교 선행조직자"),
 (3, 15, "동료 평가 준거 · 성취기준"), (3, 16, "비고츠키 · 화학 변화의 자발성 · 해설 범위"), (3, 22, "용액의 총괄성 · 오수벨 병위적 학습 · 유의미가"),
 (3, 24, "2022 설계의 개요 · 과정·기능 (2024 생물 A5 각색)"),
 (4, 1, "탐구 과정 · 인과적 의문 · 귀추"), (4, 3, "오수벨 학습 형태(하위적·상위적) · 수업 원리"), (4, 7, "5E → 경험-귀추적 순환학습 · 평가표"),
 (4, 9, "라카토슈 전진적 프로그램 · 쿤 위기·혁명"), (4, 11, "과목 간 내용 체계 위계 · 통합과학2 범위 · 브루너"), (4, 12, "2022 내용 체계 범주명"),
 (4, 16, "하슈웨 인지 갈등 + 드라이버 모형"), (4, 18, "귀추·가설연역·귀납 추론 구분"), (4, 22, "공유 결합의 극성 · 비계 발문 · ZPD"),
 (4, 25, "문제 기반 학습(PBL) 특징"),
]

def footer_y(w, p, h):
    rows = [r for r in csv.DictReader(open(W / f"q{w}-{p:02d}.tsv", encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE)
            if r["level"] == "5" and (r["text"] or "").strip()]
    ys = [int(r["top"]) for r in rows if int(r["top"]) > h * 0.85 and re.search(r"김지현|전공|http|cafe", r["text"])]
    return min(ys) if ys else int(h * 0.955)

def crop(w, p, first):
    im = Image.open(W / f"q{w}-{p:02d}.png").convert("L")
    wd, h = im.size
    top = 255 if first else 230
    bot = footer_y(w, p, h) - 15
    im = im.crop((135, top, wd - 135, bot))
    return unframe(im)

def unframe(im):
    """문항 바깥 테두리(이중선)를 잘라 내고 흰 여백을 다듬는다. 안쪽 【자료】 상자는 그대로 둔다."""
    import numpy as np
    a = np.array(im) < 128; h, w = a.shape
    cols, rows = a.sum(0), a.sum(1)
    L = [x for x in range(min(60, w)) if cols[x] > 0.6 * h]
    R = [x for x in range(max(0, w - 60), w) if cols[x] > 0.6 * h]
    x0 = max(L) + 6 if L else 0; x1 = min(R) - 6 if R else w
    T = [y for y in range(min(60, h)) if a[y, x0:x1].sum() > 0.85 * (x1 - x0)]
    B = [y for y in range(max(0, h - 70), h) if a[y, x0:x1].sum() > 0.85 * (x1 - x0)]
    y0 = max(T) + 6 if T else 0; y1 = min(B) - 6 if B else h
    im = im.crop((x0, y0, x1, y1))
    a = np.array(im) < 160
    ys, xs = np.where(a)
    if len(xs):
        im = im.crop((max(0, xs.min() - 8), max(0, ys.min() - 8), min(im.width, xs.max() + 9), min(im.height, ys.max() + 9)))
    return im

CELL_W, CELL_H = 136.0, 172.0   # 칸 크기(mm): A4 가로 2단
def pieces(im):
    """칸 비율보다 긴 조각을 가로로 완전히 빈 줄에서 나눈다(상자는 세로선이 있어 자르지 않음)."""
    import numpy as np
    hmax = int(im.width * CELL_H / CELL_W)
    if im.height <= hmax * 1.04: return [im]
    blank = (np.array(im) < 160).sum(1) == 0
    out, y = [], 0
    while im.height - y > hmax * 1.04:
        cand = [r for r in range(y + int(hmax * 0.45), min(im.height, y + hmax)) if blank[r]]
        cut = cand[-1] if cand else y + hmax
        out.append(im.crop((0, y, im.width, cut))); y = cut
        while y < im.height and blank[y]: y += 1
    out.append(im.crop((0, y, im.width, im.height)))
    return out

items = json.load(open(W / "items.json"))
cells = []
for w, n, topic in SEL:
    p0, p1 = items[f"{w}-{n}"]
    parts = [pc for p in range(p0, p1 + 1) for pc in pieces(crop(w, p, p == p0))]
    for j, im in enumerate(parts):
        fn = f"w{w}_{n:02d}_{j + 1}.png"; im.save(OUT / fn)
        cells.append((w, n, topic, fn, j, len(parts)))

css = """@page{size:297mm 210mm;margin:0}*{box-sizing:border-box}
body{margin:0;font-family:'NanumGothic',sans-serif;color:#111}
.page{width:297mm;height:210mm;padding:8mm 9mm 9mm;position:relative;page-break-after:always;overflow:hidden}
.page:last-child{page-break-after:auto}
.top{border-top:1.2pt solid #000;margin-bottom:2mm}
.cols{display:flex;height:184mm}
.col{flex:none;width:50%;padding:0 4mm 0 0;display:flex;flex-direction:column;align-items:center}
.col+.col{border-left:.8pt solid #000;padding:0 0 0 4mm}
.tag{align-self:stretch;font-size:8pt;color:#444;margin:0 0 1mm}.tag b{color:#1a3d6d}
.col img{width:100%;max-height:177mm;object-fit:contain;object-position:top}
.foot{position:absolute;left:10mm;right:10mm;bottom:4mm;border-top:.6pt solid #000;padding-top:1mm;text-align:center;font-size:8pt}
.cover h1{font-size:15pt;margin:0 0 1.5mm}.cover p{font-size:8.6pt;line-height:1.5;margin:0 0 2mm}
.cover .tw{display:flex;gap:5mm}.cover table{border-collapse:collapse;width:50%;font-size:8pt}
.cover td,.cover th{border:.5pt solid #999;padding:.7mm 1.5mm;text-align:left}.cover th{background:#eef2f7}"""
items_only = [c for c in cells if c[4] == 0]
pg_of = {}
for k, c in enumerate(cells): pg_of.setdefault((c[0], c[1]), k // 2 + 2)
def tbl(rs): return "<table><tr><th>순서</th><th>출처</th><th>핵심 주제</th><th>쪽</th></tr>" + "".join(rs) + "</table>"
rows = [f"<tr><td>{i+1}</td><td>{w}주차 {n}번</td><td>{html.escape(t)}</td><td>{pg_of[(w, n)]}</td></tr>" for i, (w, n, t, *_ ) in enumerate(items_only)]
half = (len(rows) + 1) // 2
pages = [f"""<section class='page cover'><div class='top'></div><h1>김지현 화학교육론 문제풀이 1~4주 — 2027 대비 엄선 {len(items_only)}문항</h1>
<p>◦ 2014–2026 화학교육론 기출과 2024–2026 물리·생물·지구과학교육론 경향을 기준으로, 2027 출제 가능성이 높은 이론·유형(2022 개정 교육과정 문서, 평가, 로슨·POE·5E·드라이버 등 수업 모형, 비고츠키·오수벨, 포스너·하슈웨 개념 변화, 포퍼·쿤·라카토슈, 귀납·연역·귀추, 탐구 설계·변인)을 담은 문항만 골랐습니다.
◦ 원 문제를 그대로 옮겼고 한 쪽에 두 칸(좌우)씩 실었습니다. A4 가로로 출력해도 읽기 쉽도록 문항 테두리를 없애고, 긴 문제는 단락 사이에서 여러 칸으로 나누어 실었습니다(‘계속’ 표시).</p>
<div class='tw'>{tbl(rows[:half])}{tbl(rows[half:])}</div>
<div class='foot'>김지현 화교론 문제풀이 엄선 — 1</div></section>"""]
for k in range(0, len(cells), 2):
    cols = "".join(f"<div class='col'><p class='tag'><b>{w}주차 {n}번</b>{' (계속 ' + str(j + 1) + '/' + str(m) + ')' if j else (' (1/' + str(m) + ')' if m > 1 else '')} · {html.escape(t)}</p><img src='img/{fn}'></div>"
                   for w, n, t, fn, j, m in cells[k:k + 2])
    pages.append(f"<section class='page'><div class='top'></div><div class='cols'>{cols}</div><div class='foot'>김지현 화교론 문제풀이 엄선 — {k // 2 + 2}</div></section>")
doc = f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>김지현 화교론 엄선</title><style>{css}</style></head><body>{''.join(pages)}</body></html>"
h = HERE / "김지현_화교론_1-4주_엄선.html"; h.write_text(doc, encoding="utf-8")
subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000",
                f"--print-to-pdf={HERE / '김지현_화교론_1-4주_엄선.pdf'}", f"file://{h}"], capture_output=True)
print(len(items_only), "문항,", len(cells), "칸")
