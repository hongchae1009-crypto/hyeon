# -*- coding: utf-8 -*-
"""마지막 정리 파일 하나: 출제 예상 → 기출(2026 해설 + 내 기출 정리본 원본 쪽) → 김지현 엄선(문제+답안) → 직접 만든 변형 엄선.
사용: python3 build_final.py <김지현 작업 폴더(src/w{주}q.pdf, w{주}a.pdf, work/items.json)>"""
import csv, io, json, pathlib, re, subprocess, sys
import pymupdf
from PIL import Image
HERE = pathlib.Path(__file__).parent; ROOT = HERE.parent
KJH = pathlib.Path(sys.argv[1])
UP = pathlib.Path("/root/.claude/uploads/f884566e-9634-59dc-ada1-6c4980c71812")
MYNOTE = {"a": next(UP.glob("ebe4ede1-*")), "b": next(UP.glob("3eb9180a-*")), "c": next(UP.glob("30abfd56-*"))}
CHROME = str(sorted(pathlib.Path("/opt/pw-browsers").glob("chromium-*/chrome-linux*/chrome"))[-1])
FONT = pymupdf.Font(fontfile="/root/.fonts/NanumGothic-Bold.ttf")
A4 = pymupdf.paper_rect("a4")
sys.path.insert(0, str(HERE)); sys.dont_write_bytecode = True

# ── 기출 정리본에서 볼 쪽: (파일, 쪽 번호 0부터, 문항, 왜)
NOTE = [
 ("c", 18, "2025 A5", "화학 반응의 세계 과목 구조 · 성취기준 고려 사항 · 중화 적정 곡선 범위"),
 ("c", 19, "2025 A6", "귀납 · 가치·태도(개방성) · 과학자 공동체 합의"),
 ("c", 20, "2025 A7", "드라이버 생각의 재구성 · 하슈웨 C1·C2·R1·R2"),
 ("c", 21, "2025 B3", "로슨 경험–귀추적 · 활성화 에너지"),
 ("c", 23, "2025 B5", "측정 신뢰도·실험 타당도 · 형성 평가 검토"),
 ("c", 13, "2024 A6", "설계의 개요 · 과정·기능"),
 ("c", 14, "2024 A7", "통합과학2 산화·환원 · 산화수 범위 X"),
 ("c", 15, "2024 B3", "기어리 모형 평가(플로지스톤)"),
 ("c", 16, "2024 B4", "다니엘 전지 · 문제 인식·변인 · 전지 오개념"),
 ("c", 6, "2023 A5", "귀추(이전의 성공적인 설명 빌려 오기) — 답 다시 채우기"),
 ("c", 9, "2023 B3", "오수벨 상관적 포섭 · 변인"),
 ("c", 10, "2023 B4", "혼성 오비탈 범위 위배 · 피아제"),
 ("c", 0, "2022 A5", "라카토스 긍정적·부정적 발견법"),
 ("c", 4, "2022 B4", "로슨 경험–귀추적 vs 서술적"),
 ("b", 28, "2021 B4", "관찰의 이론 의존성 · 연역 vs 가설–연역(헷갈렸던 문항)"),
 ("b", 26, "2021 A7", "STS 모형 · 당량점 = 중성 오개념"),
 ("b", 25, "2021 A6", "통합과학 중화 반응 범위 · 기구 용도"),
 ("b", 22, "2020 B4", "고윈 V도 · 활성화 에너지"),
 ("b", 10, "2018 논술 8", "발생 학습 도전 단계 · 귀납 · 포퍼 한계"),
 ("b", 4, "2017 논술 8", "POE 예측 단계 역할 · 포스너 조건(밀도)"),
 ("b", 2, "2017 서술 10", "조작적 정의 · 변인 통제 · 체크리스트"),
 ("a", 16, "2016 서술 2", "산화·환원 정의 변천 · 인지 갈등 유형"),
 ("a", 13, "2016 서술 9", "비고츠키 비계 · 염의 가수 분해"),
 ("a", 14, "2016 서술 10", "분석적 vs 총체적 채점표"),
]
# ── 김지현 화교론 엄선: (주, 번호, 주제)
KSEL = [
 ("라카토스 · 포퍼 · 쿤", [(1, 16, "귀추적 사고 · 라카토스 발견법(학생 A·B) · 과정·기능"), (3, 5, "라카토스 발견법 선택 · 과학의 본성 · 쿤 수수께끼 풀이"),
   (4, 9, "라카토스 전진적 프로그램(옥텟 규칙) · 쿤 위기·혁명"), (2, 24, "포퍼 반증주의 한계 · 쿤 · 라카토스(2024 물리 A6 각색)")]),
 ("탐구 방법 · 추론 구분", [(2, 25, "가설–연역 · 후건 긍정의 오류(2024 생물 A6 각색)"), (4, 18, "귀추 · 가설–연역 · 귀납 추론 구분"),
   (4, 1, "탐구 과정 · 인과적 의문 · 귀추"), (2, 12, "산·염기 정의 변천 · 반증 가능성 · 포스너 조건")]),
 ("수업 모형 · 개념 변화 · 학습 이론", [(2, 18, "로슨 서술적 → 경험–귀추적"), (4, 7, "5E → 경험–귀추적 순환 학습 · 평가표"),
   (4, 16, "하슈웨 인지 갈등 + 드라이버 모형(산화·환원)"), (3, 14, "오수벨 상위적 학습 · 비교 선행조직자"), (4, 22, "물 분자 극성 오개념 · 비계 발문 · ZPD")]),
 ("성취기준 · 내용 체계 · 평가", [(3, 7, "물질과 에너지 내용 체계 · 디지털 도구 · 성취기준 해설"), (3, 16, "비고츠키 · 화학 변화의 자발성 · 해설 범위"),
   (4, 11, "과목 간 내용 위계 · 통합과학2 범위 · 브루너"), (3, 1, "내용 체계 · 평가 준거 작성 · 탐구 유의점(염화 리튬 불꽃)"),
   (3, 24, "설계의 개요 · 과정·기능(2024 생물 A5 각색)")]),
]

def img_page(out, im, title=None, quality=72):
    """회색조 그림 한 장 → A4 한 쪽(비율 유지, 위쪽 정렬)."""
    buf = io.BytesIO(); im.convert("L").save(buf, "JPEG", quality=quality); data = buf.getvalue()
    pg = out.new_page(width=A4.width, height=A4.height)
    top = 26 if title else 14
    s = min((A4.width - 28) / im.width, (A4.height - top - 14) / im.height)
    w, h = im.width * s, im.height * s; x0 = (A4.width - w) / 2
    pg.insert_image(pymupdf.Rect(x0, top, x0 + w, top + h), stream=data)
    return pg

def render(doc, idx, dpi=115):
    pm = doc[idx].get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY)
    return Image.frombytes("L", (pm.width, pm.height), pm.samples)

def stamp(pg, tag):
    tw = pymupdf.TextWriter(pg.rect); tw.append((14, 15), tag, font=FONT, fontsize=7.5); tw.write_text(pg)
    back = "목차로"; bw = FONT.text_length(back, fontsize=7.5); W = pg.rect.width
    tw = pymupdf.TextWriter(pg.rect); tw.append((W - 14 - bw, 15), back, font=FONT, fontsize=7.5); tw.write_text(pg)
    pg.draw_line((W - 14 - bw, 17), (W - 14, 17), width=.4)
    pg.insert_link({"kind": pymupdf.LINK_GOTO, "from": pymupdf.Rect(W - 16 - bw, 5, W - 12, 19), "page": 0})

def kjh_answers(w):
    """답안지 쪽마다 문항 번호 위치(OCR) → {번호: [(쪽, y0, y1)]} (1~25 첫 순서만)."""
    d = pymupdf.open(KJH / "src" / f"w{w}a.pdf"); marks = []
    for i in range(1, len(d)):
        im = render(d, i, 150); buf = io.BytesIO(); im.save(buf, "PNG")
        tsv = subprocess.run(["tesseract", "-", "-", "-l", "kor", "--psm", "4", "tsv"], input=buf.getvalue(), capture_output=True).stdout.decode("utf-8", "ignore")
        lines = {}
        for r in csv.DictReader(io.StringIO(tsv), delimiter="\t", quoting=csv.QUOTE_NONE):
            if r["level"] == "5" and (r["text"] or "").strip():
                lines.setdefault((r["block_num"], r["par_num"], r["line_num"]), []).append(r)
        for ws in lines.values():
            m = re.match(r"^(\d{1,2})[.)]$", ws[0]["text"])
            if m and int(ws[0]["left"]) < 160 and int(m.group(1)) > 0:
                marks.append((i, int(ws[0]["top"]), int(m.group(1)), im.height))
    marks.sort(); seq, last = [], 0
    for mk in marks:
        if mk[2] == last + 1: seq.append(mk); last = mk[2]
    res = {}
    for k, (i, y, n, H) in enumerate(seq):
        top, bot = 175, int(H * 0.94)
        nxt = seq[k + 1] if k + 1 < len(seq) else None
        if nxt and nxt[0] == i: res[n] = [(i, y - 12, nxt[1] - 12)]
        else:
            res[n] = [(i, y - 12, bot)]
            if nxt and nxt[0] == i + 1 and nxt[1] > top + 60: res[n].append((i + 1, top, nxt[1] - 12))
    return d, res

def build():
    out = pymupdf.open(); toc = []
    # 0) 목차 자리(나중에 앞에 붙임)
    # 1) 출제 예상
    sec = []
    p = pymupdf.open(HERE / "2027_화학임용_과교론_출제예상주제.pdf"); s0 = len(out); out.insert_pdf(p)
    stamp(out[s0], "Ⅰ. 2027 출제 예상 이론·모형"); toc.append(("Ⅰ. 2027 출제 예상 이론·모형 (2쪽)", [("", "물·생·지 2023~2026 출제 지도와 2027 예상 순위", s0)]))
    # 2) 2026 기출(정리본에 없음) — 최종 정리 해설 쪽
    import spec
    fin = pymupdf.open(HERE / "2027_화학임용_과교론_최종정리.pdf")
    heads = []
    for n, it in enumerate(spec.ITEMS, 1):
        lab = f"{n:02d}"
        pi = next(i for i in range(2, len(fin)) if re.search(rf"(^|\n){n:02d}\n", fin[i].get_text()[:60]))
        heads.append((it, pi))
    rows = []
    for k, (it, pi) in enumerate(heads):
        if not it["id"].startswith("26"): continue
        end = heads[k + 1][1] if k + 1 < len(heads) else len(fin)
        st = len(out); out.insert_pdf(fin, from_page=pi, to_page=end - 1)
        stamp(out[st], f"Ⅱ-1 · 2026 {it['id'][2:]}"); rows.append((f"2026 {it['id'][2:]}", it["topic"], st))
    toc.append(("Ⅱ-1. 2026 기출 6문항 — 기출 원문 · 모범 답안 · 2022 개정 원문 컷아웃", rows))
    # 3) 내 기출 정리본 원본 쪽
    rows = []; docs = {k: pymupdf.open(v) for k, v in MYNOTE.items()}
    for f, i, lab, why in NOTE:
        st = len(out); img_page(out, render(docs[f], i, 120), title=True)
        stamp(out[st], f"Ⅱ-2 · 기출 정리본 {lab}"); rows.append((lab, why, st))
    toc.append(("Ⅱ-2. 내 기출 정리본에서 다시 볼 쪽 (원본 그대로)", rows))
    # 4) 김지현 엄선 — 문제 쪽 + 답안 조각
    items = json.load(open(KJH / "work" / "items.json"))
    ans = {w: kjh_answers(w) for w in (1, 2, 3, 4)}
    qd = {w: pymupdf.open(KJH / "src" / f"w{w}q.pdf") for w in (1, 2, 3, 4)}
    for g, xs in KSEL:
        rows = []
        for w, n, topic in xs:
            a, b = items[f"{w}-{n}"]; st = len(out)
            for p in range(a, b + 1):
                img_page(out, render(qd[w], p - 1, 120), title=True)
            ad, am = ans[w]
            pieces = [render(ad, i, 150).crop((100, y0, 1140, y1)) for i, y0, y1 in am.get(n, [])]
            if pieces:
                W = max(x.width for x in pieces); H = sum(x.height for x in pieces) + 20
                hd = 40; comb = Image.new("L", (W, H + hd), 255); y = hd
                for x in pieces: comb.paste(x, (0, y)); y += x.height + 20
                from PIL import ImageDraw, ImageFont
                ImageDraw.Draw(comb).text((4, 6), f"{w}주 {n}번 답안", fill=0, font=ImageFont.truetype("/root/.fonts/NanumGothic-Bold.ttf", 26))
                pg = out.new_page(width=A4.width, height=A4.height)
                buf = io.BytesIO(); comb.save(buf, "JPEG", quality=75)
                s = min((A4.width - 40) / comb.width, (A4.height - 50) / comb.height, 0.62)
                pg.insert_image(pymupdf.Rect(20, 28, 20 + comb.width * s, 28 + comb.height * s), stream=buf.getvalue())
            stamp(out[st], f"Ⅲ · 김지현 {w}주 {n}번"); rows.append((f"{w}주 {n}번", topic, st))
        toc.append((f"Ⅲ. 김지현 화교론 엄선 — {g}", rows))
    # 5) 직접 만든 변형 엄선(문제 + 해설)
    pk = pymupdf.open(HERE / "과교론_반드시볼문제_엄선.pdf")
    import build_pick as BP
    ptoc = 2; st0 = len(out); out.insert_pdf(pk, from_page=ptoc)
    k = 0
    for g, xs in BP.GROUPS:
        rows = []
        for key, title, why, point in xs:
            k += 1
            pi = next(i for i in range(st0, len(out)) if f"S{k:02d} · " in out[i].get_text())
            rows.append((f"S{k:02d}", title, pi))
        toc.append((f"Ⅳ. 직접 만든 변형 엄선 — {g.split(' — ')[0]}", rows))
    for i in range(st0, len(out)):  # 엄선 파일의 ‘엄선 목차로’ 링크를 이 파일 목차로
        for r in out[i].search_for("엄선 목차로"):
            out[i].insert_link({"kind": pymupdf.LINK_GOTO, "from": r, "page": 0})
    # 6) 목차 만들기 → 앞에 붙이고 링크
    body = ""
    for sec, rows in toc:
        body += f"<tr><td colspan='3' class='g'>{sec}</td></tr>"
        for lab, txt, pg in rows:
            body += f"<tr><td class='n'>{lab or '보기'}</td><td class='l'>{txt}</td><td class='p'>@@{pg}@@</td></tr>"
    css = """@page{size:A4;margin:9mm 10mm}body{margin:0;font-family:'NanumGothic',sans-serif;font-size:7.4pt;line-height:1.28}
h1{font-size:14pt;margin:0 0 1mm}.sub{font-size:7.8pt;margin:0 0 2mm}table{border-collapse:collapse;width:100%}
td{border:.5pt solid #000;padding:.35mm 1.2mm;vertical-align:top}td.g{font-weight:bold;border-top:1.1pt solid #000;padding:.8mm 1.4mm;font-size:8pt}
td.n{white-space:nowrap;font-weight:bold;width:15%}td.p{width:7%;text-align:right;white-space:nowrap}.box{border:.7pt solid #000;padding:1.2mm 2mm;margin:0 0 2mm}"""
    html_ = f"""<!doctype html><html lang='ko'><head><meta charset='utf-8'><style>{css}</style></head><body>
<h1>2027 화학 임용 과교론 — 마지막 정리 한 권</h1>
<p class='sub'>Ⅰ 출제 예상 → Ⅱ 기출(2026 해설 + 내 기출 정리본 원본) → Ⅲ 김지현 화교론 엄선(문제 + 답안) → Ⅳ 직접 만든 변형 엄선(문제 + 해설). 항목을 누르면 이동하고, 각 쪽 오른쪽 위 ‘목차로’를 누르면 돌아온다.</p>
<table>{body}</table></body></html>"""
    hp = HERE / "_final_toc.html"; tp = HERE / "_final_toc.pdf"
    def make_toc(offset):
        hp.write_text(re.sub(r"@@(\d+)@@", lambda m: f"{int(m.group(1)) + offset + 1}쪽", html_), encoding="utf-8")
        subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={tp}", f"file://{hp}"], capture_output=True)
        return pymupdf.open(tp)
    t = make_toc(2); t = make_toc(len(t)); nt = len(t)
    final = pymupdf.open(); final.insert_pdf(t); final.insert_pdf(out)
    # 링크: 목차 → 쪽, 각 쪽 ‘목차로’ → 0쪽 (본문 링크는 nt만큼 밀림)
    for i in range(nt, len(final)):
        for l in final[i].get_links():
            if l.get("kind") == pymupdf.LINK_GOTO:
                final[i].delete_link(l)
        for r in final[i].search_for("목차로"):
            final[i].insert_link({"kind": pymupdf.LINK_GOTO, "from": pymupdf.Rect(r.x0 - 2, r.y0 - 2, r.x1 + 2, r.y1 + 2), "page": 0})
    allrows = [(lab, txt, pg) for _, rows in toc for lab, txt, pg in rows]
    for i in range(nt):
        for lab, txt, pg in allrows:
            for r in final[i].search_for(f"{pg + nt + 1}쪽"):
                final[i].insert_link({"kind": pymupdf.LINK_GOTO, "from": pymupdf.Rect(16, r.y0 - 1, r.x1, r.y1 + 1), "page": pg + nt})
    dst = HERE / "2027_과교론_마지막정리_한권.pdf"
    final.save(dst, garbage=4, deflate=True); hp.unlink(); tp.unlink()
    print(dst.name, len(final), "쪽", round(dst.stat().st_size / 1e6, 1), "MB")

if __name__ == "__main__":
    build()
