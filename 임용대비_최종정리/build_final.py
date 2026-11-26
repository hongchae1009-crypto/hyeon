# -*- coding: utf-8 -*-
"""마지막 정리 한 권(화면용, 원본 색 그대로, 쪽수 최소).
쪽마다 내용 덩어리(띠)만 잘라 A4에 빈틈없이 이어 붙인다(원본 벡터·이미지 그대로, 래스터화 없음).
순서: 출제 예상 → 2026 기출 → 내 기출 정리본 → 김지현 엄선(문제 바로 아래 답안) → 직접 만든 변형 엄선(문제 + 해설)
사용: python3 build_final.py <김지현 작업 폴더(src/w{주}q.pdf, w{주}a.pdf, work/items.json)>"""
import csv, io, json, pathlib, re, subprocess, sys
import numpy as np, pymupdf
HERE = pathlib.Path(__file__).parent; ROOT = HERE.parent
KJH = pathlib.Path(sys.argv[1])
UP = pathlib.Path("/root/.claude/uploads/f884566e-9634-59dc-ada1-6c4980c71812")
MYNOTE = {"a": next(UP.glob("ebe4ede1-*")), "b": next(UP.glob("3eb9180a-*")), "c": next(UP.glob("30abfd56-*"))}
CHROME = str(sorted(pathlib.Path("/opt/pw-browsers").glob("chromium-*/chrome-linux*/chrome"))[-1])
FONT = pymupdf.Font(fontfile="/root/.fonts/NanumGothic-Bold.ttf")
A4 = pymupdf.paper_rect("a4"); M = 10; UW = A4.width - 2 * M
sys.path.insert(0, str(HERE)); sys.dont_write_bytecode = True

# ── 2026 기출(최종 정리 해설 쪽에서): 문항 id
Y26 = ["26A5", "26A7", "26B3", "26B4"]
# ── 내 기출 정리본: (파일, 쪽 0부터, 문항, 왜)
NOTE = [
 ("c", 18, "2025 A5", "화학 반응의 세계 과목 구조 · 고려 사항 · 중화 적정 곡선 범위"),
 ("c", 20, "2025 A7", "드라이버 생각의 재구성 · 하슈웨 C1·C2·R1·R2"),
 ("c", 23, "2025 B5", "측정 신뢰도·실험 타당도 · 형성 평가 검토"),
 ("c", 13, "2024 A6", "설계의 개요 · 과정·기능"),
 ("c", 14, "2024 A7", "통합과학2 산화·환원 · 산화수 범위 X"),
 ("c", 16, "2024 B4", "다니엘 전지 · 변인 · 전지 오개념"),
 ("c", 6, "2023 A5", "귀추 — 답이 비어 있던 문항"),
 ("c", 9, "2023 B3", "오수벨 상관적 포섭"),
 ("c", 10, "2023 B4", "혼성 오비탈 범위 위배 · 피아제"),
 ("c", 0, "2022 A5", "라카토스 긍정적·부정적 발견법"),
 ("b", 28, "2021 B4", "연역 vs 가설–연역(헷갈렸던 문항) · 관찰의 이론 의존성"),
 ("b", 26, "2021 A7", "STS 모형 · 당량점 = 중성 오개념"),
 ("b", 4, "2017 논술 8", "POE 예측 단계 역할 · 포스너 조건(밀도)"),
 ("a", 16, "2016 서술 2", "산화·환원 정의 변천 · 인지 갈등 유형"),
]
# ── 김지현 엄선: (주, 번호, 주제)
KSEL = [(1, 16, "라카토스 발견법(학생 A·B) · 귀추적 사고 · 과정·기능"), (3, 5, "라카토스 발견법 선택 · 쿤 수수께끼 풀이"),
        (4, 18, "귀추 · 가설–연역 · 귀납 추론 구분"), (2, 25, "가설–연역 · 후건 긍정의 오류"),
        (2, 18, "로슨 서술적 → 경험–귀추적"), (4, 16, "하슈웨 인지 갈등 + 드라이버 모형"),
        (3, 14, "오수벨 상위적 학습 · 비교 선행조직자"), (3, 7, "물질과 에너지 내용 체계 · 성취기준 해설"),
        (4, 11, "과목 간 내용 위계 · 통합과학2 범위 · 브루너"), (3, 24, "설계의 개요 · 과정·기능")]
# ── 직접 만든 변형 엄선: build_pick 키
PSEL = ["mock1A6", "mock4A7", "mock5A7", "mock3A7", "T4", "T14", "E6", "E8", "F19", "mock3A6", "T17", "mock5B4"]

# ─────────────────────────── 띠 나누기 · 이어 붙이기
def bands(doc, pno, clip=None, drop_top=0.0, drop_bot=1.0, gap_pt=9, dpi=60, noframe=False):
    """쪽(또는 clip)에서 빈 가로줄로 나뉜 내용 띠 [Rect] (PDF 좌표). drop_top/bot: 이 비율 밖의 띠는 버림(머리말·꼬리말)."""
    pg = doc[pno]; R = clip or pg.rect
    pm = pg.get_pixmap(dpi=dpi, clip=R, colorspace=pymupdf.csGRAY)
    a = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width) < 225
    sc = R.width / pm.width
    if noframe:  # 쪽 전체를 감싸는 테두리선(긴 세로선·가로선)은 내용으로 치지 않음
        a = a.copy(); vc = a.sum(0) > 0.45 * a.shape[0]
        for x in np.where(vc)[0]: a[:, max(0, x - 2):x + 3] = False
        hr = a.sum(1) > 0.85 * a.shape[1]; a[hr] = False
    rows = a.sum(1) > 0; gap = max(2, int(gap_pt / sc)); out = []; s = None; g = 0
    for y, r in enumerate(list(rows) + [False] * (gap + 1)):
        if r:
            if s is None: s = y
            g = 0; e = y
        elif s is not None:
            g += 1
            if g > gap:
                cols = np.where(a[s:e + 1].any(0))[0]
                rr = pymupdf.Rect(R.x0 + cols.min() * sc - 2, R.y0 + s * sc - 2, R.x0 + (cols.max() + 1) * sc + 2, R.y0 + (e + 1) * sc + 2)
                fy0, fy1 = (rr.y0 - pg.rect.y0) / pg.rect.height, (rr.y1 - pg.rect.y0) / pg.rect.height
                if fy1 > drop_top and fy0 < drop_bot: out.append(rr)
                s = None
    return out

class Flow:
    def __init__(self):
        self.doc = pymupdf.open(); self.y = None; self.pg = None; self.marks = []; self.pend = None
    def newpage(self):
        self.pg = self.doc.new_page(width=A4.width, height=A4.height); self.y = M
    def room(self): return A4.height - M - self.y if self.pg else -1
    def empty(self): return self.pg is None or self.y <= M + 1
    def head(self, tag, title):
        """머리줄은 첫 내용과 같은 쪽에 그리도록 미뤄 둔다."""
        self.pend = (tag, title)
    def _draw_head(self):
        tag, title = self.pend; self.pend = None
        if not self.empty(): self.y += 6
        pg, y = self.pg, self.y
        tw = pymupdf.TextWriter(pg.rect); tw.append((M, y + 9), f"{tag}  {title}"[:95], font=FONT, fontsize=8.2); tw.write_text(pg, color=(0.05, 0.2, 0.45))
        bw = FONT.text_length("목차로", fontsize=7.5)
        tw = pymupdf.TextWriter(pg.rect); tw.append((A4.width - M - bw, y + 9), "목차로", font=FONT, fontsize=7.5); tw.write_text(pg)
        pg.draw_line((M, y + 12), (A4.width - M, y + 12), width=0.8, color=(0.05, 0.2, 0.45))
        self.marks.append((tag, title, self.doc.page_count - 1))
        self.y = y + 15
    def _place(self, src, pno, r, s):
        h = r.height * s; w = r.width * s; xo = M + (UW - w) / 2
        self.pg.show_pdf_page(pymupdf.Rect(xo, self.y, xo + w, self.y + h), src, pno, clip=r)
        self.y += h + 2
    @staticmethod
    def _cut(src, pno, r, hmax):
        """띠 r을 위에서 hmax(원본 좌표) 이내의 빈 줄(글줄 사이)에서 자를 y. 상자 세로선은 무시. 없으면 None."""
        pm = src[pno].get_pixmap(dpi=72, clip=r, colorspace=pymupdf.csGRAY)
        a = np.frombuffer(pm.samples, np.uint8).reshape(pm.height, pm.width) < 200
        k = r.height / pm.height; lim = int(hmax / k)
        blank = a.sum(1) <= max(4, 0.012 * pm.width)
        for y in range(min(lim, pm.height - 1), int(pm.height * 0.08), -1):
            if blank[y] and blank[y - 1]: return r.y0 + y * k
        return None
    def put(self, src, pno, rects, smax=1.15):
        """한 원본 쪽의 띠들을 같은 배율로 이어 붙인다. 남은 칸이 넉넉한데 띠가 안 들어가면 글줄 사이에서 잘라 채운다."""
        if not rects: return
        x0 = min(r.x0 for r in rects); x1 = max(r.x1 for r in rects)
        s = min(UW / (x1 - x0), smax)
        todo = [pymupdf.Rect(x0, r.y0, x1, r.y1) for r in rects]
        while todo:
            r = todo.pop(0); ss = s
            hh = 21 if self.pend else 0
            if self.pg is None: self.newpage()
            room = self.room() - hh
            if r.height * ss > room and room > 70:
                y = self._cut(src, pno, r, room / ss)
                if y and y - r.y0 > 20:
                    todo.insert(0, pymupdf.Rect(r.x0, y, r.x1, r.y1)); r = pymupdf.Rect(r.x0, r.y0, r.x1, y)
            if r.height * ss + hh > A4.height - 2 * M: ss = (A4.height - 2 * M - hh) / r.height
            if r.height * ss + hh > self.room() and not self.empty(): self.newpage()
            if self.pend: self._draw_head()
            self._place(src, pno, r, ss)
    def put_onepage(self, groups, smax=1.1):
        """groups: [(src, pno, rects)] — 새 쪽 한 장에 모두 들어가도록 배율을 줄여 배치."""
        groups = [(d, p, rs) for d, p, rs in groups if rs]
        if not self.empty() or self.pg is None: self.newpage()
        sc = []
        for d, p, rs in groups:
            x0 = min(r.x0 for r in rs); x1 = max(r.x1 for r in rs); sc.append((x0, x1, min(UW / (x1 - x0), smax)))
        need = sum(sum(r.height for r in rs) * s + 2 * len(rs) for (d, p, rs), (_, _, s) in zip(groups, sc)) + 6 * len(groups)
        avail = A4.height - 2 * M - 21; f = min(1.0, avail / need)
        if self.pend: self._draw_head()
        for (d, p, rs), (x0, x1, s) in zip(groups, sc):
            for r in rs: self._place(d, p, pymupdf.Rect(x0, r.y0, x1, r.y1), s * f)
            self.y += 4

# ─────────────────────────── 김지현 답안 위치
def kjh_answers(w):
    d = pymupdf.open(KJH / "src" / f"w{w}a.pdf"); marks = []
    for i in range(1, len(d)):
        pm = d[i].get_pixmap(dpi=150, colorspace=pymupdf.csGRAY)
        tsv = subprocess.run(["tesseract", "-", "-", "-l", "kor", "--psm", "4", "tsv"], input=pm.tobytes("png"), capture_output=True).stdout.decode("utf-8", "ignore")
        lines = {}
        for r in csv.DictReader(io.StringIO(tsv), delimiter="\t", quoting=csv.QUOTE_NONE):
            if r["level"] == "5" and (r["text"] or "").strip():
                lines.setdefault((r["block_num"], r["par_num"], r["line_num"]), []).append(r)
        for ws in lines.values():
            m = re.match(r"^(\d{1,2})[.)]$", ws[0]["text"])
            if m and int(ws[0]["left"]) < 160 and int(m.group(1)) > 0:
                marks.append((i, int(ws[0]["top"]), int(m.group(1)), pm.height))
    marks.sort(); seq, last = [], 0
    for mk in marks:
        if mk[2] == last + 1: seq.append(mk); last = mk[2]
    k72 = 72 / 150; res = {}
    for k, (i, y, n, H) in enumerate(seq):
        top, bot = 175, int(H * 0.94); nxt = seq[k + 1] if k + 1 < len(seq) else None
        seg = [(i, y - 12, nxt[1] - 12 if nxt and nxt[0] == i else bot)]
        if nxt and nxt[0] == i + 1 and nxt[1] > top + 60: seg.append((i + 1, top, nxt[1] - 12))
        res[n] = [(i, pymupdf.Rect(100 * k72, y0 * k72, 1140 * k72, y1 * k72)) for i, y0, y1 in seg]
    return d, res

def build():
    import spec, build_pick as BP
    F = Flow(); toc = []
    # Ⅰ 출제 예상
    p = pymupdf.open(HERE / "2027_화학임용_과교론_출제예상주제.pdf")
    F.head("Ⅰ", "2027 출제 예상 이론·모형")
    for i in range(len(p)): F.put(p, i, bands(p, i))
    toc.append(("Ⅰ. 2027 출제 예상 이론·모형", F.marks[-1:]))
    # Ⅱ-1 2026 기출(최종 정리)
    fin = pymupdf.open(HERE / "2027_화학임용_과교론_최종정리.pdf"); n0 = len(F.marks)
    starts = {}
    for n, it in enumerate(spec.ITEMS, 1):
        starts[it["id"]] = next(i for i in range(2, len(fin)) if re.search(rf"(^|\n){n:02d}\n", fin[i].get_text()[:60]))
    order = [it["id"] for it in spec.ITEMS]
    for iid in Y26:
        a = starts[iid]; b = starts[order[order.index(iid) + 1]] if order.index(iid) + 1 < len(order) else len(fin)
        it = next(x for x in spec.ITEMS if x["id"] == iid)
        F.head(f"2026 {iid[2:]}", it["topic"])
        for i in range(a, b):
            rs = bands(fin, i)
            if i == a: rs = rs[1:]  # 원래 머리줄은 새 머리줄로 대체
            F.put(fin, i, rs)
    toc.append(("Ⅱ-1. 2026 기출 — 원문 · 모범 답안 · 2022 개정 원문 컷아웃", F.marks[n0:]))
    # Ⅱ-2 내 기출 정리본
    docs = {k: pymupdf.open(v) for k, v in MYNOTE.items()}; n0 = len(F.marks)
    for f, i, lab, why in NOTE:
        F.head(lab, why); F.put(docs[f], i, bands(docs[f], i, drop_bot=0.955), smax=1.05)
    toc.append(("Ⅱ-2. 내 기출 정리본 (원본 그대로)", F.marks[n0:]))
    # Ⅲ 김지현
    items = json.load(open(KJH / "work" / "items.json"))
    ans = {w: kjh_answers(w) for w in (1, 2, 3, 4)}
    qd = {w: pymupdf.open(KJH / "src" / f"w{w}q.pdf") for w in (1, 2, 3, 4)}; n0 = len(F.marks)
    for w, n, topic in KSEL:
        a, b = items[f"{w}-{n}"]; F.head(f"김지현 {w}주 {n}번", topic); grp = []
        for p in range(a, b + 1):
            grp.append((qd[w], p - 1, bands(qd[w], p - 1, drop_top=0.092, drop_bot=0.91, noframe=True)))
        ad, am = ans[w]
        for i, r in am.get(n, []):
            grp.append((ad, i, bands(ad, i, clip=r)))
        F.put_onepage(grp)
        F.pg = None  # 다음 문항은 새 쪽
    toc.append(("Ⅲ. 김지현 화교론 엄선 (문제 바로 아래 답안)", F.marks[n0:]))
    # Ⅳ 직접 만든 변형
    titles = {k: (t, pt) for g, xs in BP.GROUPS for k, t, why, pt in xs}; n0 = len(F.marks)
    for key in PSEL:
        probs, anss, srcname = BP.locate(key)
        F.head(srcname, titles[key][0])
        for d, idx, clip in probs:
            F.put(d, idx, bands(d, idx, clip=clip, drop_bot=0.97 if clip is None else 1))
        for d, idx in anss:
            F.put(d, idx, bands(d, idx, drop_bot=0.97))
    toc.append(("Ⅳ. 직접 만든 변형 엄선 (문제 + 해설)", F.marks[n0:]))
    body = F.doc
    # 목차
    rows = ""
    for sec, ms in toc:
        rows += f"<tr><td colspan='3' class='g'>{sec}</td></tr>"
        for tag, title, pg in ms:
            rows += f"<tr><td class='n'>{tag}</td><td class='l'>{title}</td><td class='p'>@@{pg}@@</td></tr>"
    css = """@page{size:A4;margin:9mm 10mm}body{margin:0;font-family:'NanumGothic',sans-serif;font-size:8pt;line-height:1.3}
h1{font-size:14pt;margin:0 0 1mm;color:#0d3373}.sub{font-size:8pt;margin:0 0 2mm}table{border-collapse:collapse;width:100%}
td{border:.5pt solid #889;padding:.5mm 1.4mm;vertical-align:top}td.g{font-weight:bold;background:#e8eef8;padding:.9mm 1.4mm;font-size:8.6pt;color:#0d3373}
td.n{white-space:nowrap;font-weight:bold;width:17%}td.p{width:7%;text-align:right;white-space:nowrap;color:#0d3373}"""
    hp = HERE / "_final_toc.html"; tp = HERE / "_final_toc.pdf"
    def make(off):
        h = f"""<!doctype html><html lang='ko'><head><meta charset='utf-8'><style>{css}</style></head><body>
<h1>2027 화학 임용 과교론 — 마지막 정리 한 권</h1><p class='sub'>Ⅰ 출제 예상 → Ⅱ 기출(2026 해설 + 내 정리본) → Ⅲ 김지현 엄선 → Ⅳ 직접 만든 변형 엄선. 항목을 누르면 이동, 각 문항 머리줄 오른쪽 ‘목차로’를 누르면 여기로.</p>
<table>{rows}</table></body></html>"""
        hp.write_text(re.sub(r"@@(\d+)@@", lambda m: f"{int(m.group(1)) + off + 1}쪽", h), encoding="utf-8")
        subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={tp}", f"file://{hp}"], capture_output=True)
        return pymupdf.open(tp)
    t = make(1); t = make(len(t)); nt = len(t)
    final = pymupdf.open(); final.insert_pdf(t); final.insert_pdf(body)
    for i in range(nt, len(final)):
        for r in final[i].search_for("목차로"):
            final[i].insert_link({"kind": pymupdf.LINK_GOTO, "from": pymupdf.Rect(r.x0 - 2, r.y0 - 2, r.x1 + 2, r.y1 + 2), "page": 0})
    allm = sorted({pg for _, ms in toc for _, _, pg in ms})
    for i in range(nt):
        for pg in allm:
            for r in final[i].search_for(f"{pg + nt + 1}쪽"):
                final[i].insert_link({"kind": pymupdf.LINK_GOTO, "from": pymupdf.Rect(20, r.y0 - 1, r.x1, r.y1 + 1), "page": pg + nt})
    dst = HERE / "2027_과교론_마지막정리_한권.pdf"
    final.rewrite_images(dpi_threshold=160, dpi_target=140, quality=78)  # 화면용 용량 줄이기(색 유지)
    final.save(dst, garbage=4, deflate=True); hp.unlink(); tp.unlink()
    print(dst.name, len(final), "쪽", round(dst.stat().st_size / 1e6, 1), "MB")

if __name__ == "__main__":
    build()
