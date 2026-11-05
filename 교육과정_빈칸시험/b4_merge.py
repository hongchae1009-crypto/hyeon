# -*- coding: utf-8 -*-
"""2022 개정 과학과 교육과정 원문(김지현 편집 스캔 PDF)을 B4 모아찍기로 컷아웃한다.
  1쪽: 내용 체계 표 6개  /  2쪽~: 성취기준 · 성취기준 해설 · 적용 시 고려 사항
쪽마다 바깥 테두리 안쪽만 잘라, 빈 줄로 나뉜 내용 띠를 다단으로 차례대로 채운다.
사용: python3 b4_merge.py <2022 교육과정-1-23.pdf> <2022 교육과정-24-48.pdf>"""
import io, pathlib, sys
import numpy as np, pymupdf
from PIL import Image
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).parent
FONT = "/root/.fonts/NanumGothic-Bold.ttf"
MM = 72 / 25.4
B4 = (257 * MM, 364 * MM)
DPI = 250
NATIVE = 25.4 / DPI * MM          # 원문 실제 크기(pt/px)
SUBJ = [  # (과목명, [(내용 체계 쪽, 표 이름)], 성취기준·해설 쪽)
    ("중학교 과학(물질)", [(9, "중학교 과학 — 물질")], [12, 13, 14, 15, 16]),
    ("통합과학1·2", [(27, "통합과학1"), (34, "통합과학2")], [28, 29, 30, 31, 35, 36]),
    ("화학", [(62, "화학")], [63, 64, 65, 66]),
    ("물질과 에너지", [(74, "물질과 에너지")], [75, 76, 77, 78]),
    ("화학 반응의 세계", [(86, "화학 반응의 세계")], [87, 88, 89]),
]

class Book:
    """책 쪽 번호 → 스캔 쪽 그림. 앞 파일은 펼침 쪽 i에 (2i-1, 2i)쪽, 뒤 파일은 펼침 쪽 j에 (45+2j, 46+2j)쪽."""
    def __init__(self, a, b): self.a, self.b = pymupdf.open(a), pymupdf.open(b)
    def page(self, p):
        d, i = (self.a, (p + 1) // 2) if p <= 44 else (self.b, (p - 45) // 2)
        r = d[i].rect; w = r.width / 2
        clip = pymupdf.Rect(0, 0, w, r.height) if p % 2 else pymupdf.Rect(w, 0, r.width, r.height)
        pm = d[i].get_pixmap(dpi=DPI, clip=clip, colorspace=pymupdf.csGRAY)
        return Image.frombytes("L", (pm.width, pm.height), pm.samples)

def bands(im, min_h):
    """바깥 테두리(세로선) 안쪽만 남기고, 28px 이상 빈 줄로 나뉜 내용 띠를 잘라 돌려준다."""
    a = np.array(im) < 150; H, W = a.shape
    bc = np.where(a.sum(0) > 0.7 * H)[0]
    L, R = bc[bc < W / 2], bc[bc > W / 2]
    x0 = L.max() + 8 if len(L) else 0; x1 = R.min() - 8 if len(R) else W
    ref = L.max() if len(L) else (R.min() if len(R) else None)
    if ref is not None:
        ys = np.where(a[:, ref])[0]; y0, y1 = ys.min() + 8, ys.max() - 8
    else:
        y0, y1 = 0, H
    sub = a[y0:y1, x0:x1]; rows = sub.sum(1) > 0
    out, s, gap, e = [], None, 0, 0
    for y, r in enumerate(list(rows) + [False] * 30):
        if r:
            s = y if s is None else s; gap = 0; e = y
        elif s is not None:
            gap += 1
            if gap >= 28:
                cols = np.where(sub[s:e + 1].any(0))[0]
                full = cols.max() - cols.min() > 0.97 * sub.shape[1] and e - s < 12  # 테두리 가로줄
                if e - s + 1 >= min_h and not full:
                    out.append(im.crop((x0 + cols.min() - 4, y0 + s - 4, x0 + cols.max() + 5, y0 + e + 5)))
                s = None
    return out

def layout(doc, items, ncol, title, sub, k_max, gap=2.2):
    """items: ('label', 글) 또는 ('img', PIL)을 ncol단에 차례대로 채운다. 한 쪽에 들어가는 가장 큰 배율을 쓴다."""
    W, H = B4; mx, top, bot, cg = 9 * MM, 17 * MM, 7 * MM, 5 * MM
    cw = (W - 2 * mx - (ncol - 1) * cg) / ncol; ch = H - top - bot
    def place(k):
        pos, c, y = [], 0, 0
        for t, v in items:
            h = 4.8 * MM if t == "label" else v.height * k
            if t == "img" and v.width * k > cw: return None
            if y + h > ch and y > 0:
                c += 1; y = 0
                if c >= ncol: return None
            pos.append((t, v, c, y, h)); y += h + (0.8 * MM if t == "label" else gap * MM)
        return pos
    k = k_max
    while (pos := place(k)) is None: k *= 0.99
    pg = doc.new_page(width=W, height=H)
    pg.insert_font(fontname="ng", fontfile=FONT)
    pg.insert_text((mx, 10.5 * MM), title, fontname="ng", fontsize=13)
    F = pymupdf.Font(fontfile=FONT)
    pg.insert_text((W - mx - F.text_length(sub, fontsize=8.5), 10.5 * MM), sub, fontname="ng", fontsize=8.5, color=(.35, .35, .35))
    pg.draw_line((mx, 13.5 * MM), (W - mx, 13.5 * MM), width=1.1)
    for c in range(1, ncol):
        x = mx + c * cw + (c - 0.5) * cg
        pg.draw_line((x, top), (x, H - bot), width=.4, color=(.75, .75, .75))
    for t, v, c, y, h in pos:
        x = mx + c * (cw + cg); yy = top + y
        if t == "label":
            pg.draw_rect(pymupdf.Rect(x, yy, x + cw, yy + h), color=None, fill=(.10, .24, .43))
            fs = min(9, (cw - 3.6 * MM) / F.text_length(v, fontsize=1))
            pg.insert_text((x + 1.8 * MM, yy + h / 2 + fs * 0.36), v, fontname="ng", fontsize=fs, color=(1, 1, 1))
        else:
            buf = io.BytesIO(); v.save(buf, "PNG", optimize=True)
            pg.insert_image(pymupdf.Rect(x, yy, x + v.width * k, yy + h), stream=buf.getvalue())
    return k

def build(a, b, std_pages=1):
    bk = Book(a, b); doc = pymupdf.open()
    items = []
    for name, tabs, _ in SUBJ:
        for p, lab in tabs:
            items.append(("label", f"{lab} — 내용 체계 (원문 {p}쪽)"))
            items += [("img", x) for x in bands(bk.page(p), 200)]
    k1 = layout(doc, items, 2, "2022 개정 과학과 교육과정 — 내용 체계", "원문 컷아웃 · 중학교 과학(물질) · 통합과학1·2 · 화학 · 물질과 에너지 · 화학 반응의 세계", NATIVE)
    items = []
    for name, _, ps in SUBJ:
        items.append(("label", f"{name} (원문 {ps[0]}~{ps[-1]}쪽)"))
        for p in ps: items += [("img", x) for x in bands(bk.page(p), 10)]
    if std_pages == 1:
        k2 = layout(doc, items, 4, "2022 개정 과학과 교육과정 — 성취기준", "원문 컷아웃 · 성취기준 · 성취기준 해설 · 적용 시 고려 사항", NATIVE, gap=1.0)
    else:  # 두 쪽: 앞의 절반 과목 / 나머지
        n = next(i for i, (t, v) in enumerate(items) if t == "label" and v.startswith("화학 ("))
        k2 = min(layout(doc, items[:n], 3, "2022 개정 과학과 교육과정 — 성취기준 ①", "원문 컷아웃 · 중학교 과학(물질) · 통합과학1·2", NATIVE, gap=1.2),
                 layout(doc, items[n:], 3, "2022 개정 과학과 교육과정 — 성취기준 ②", "원문 컷아웃 · 화학 · 물질과 에너지 · 화학 반응의 세계", NATIVE, gap=1.2))
    out = HERE / f"교육과정_원문컷아웃_B4{'' if std_pages == 1 else '_성취기준2쪽'}.pdf"
    doc.save(out, garbage=4, deflate=True)
    print(f"{out.name}: {len(doc)}쪽 — 내용 체계 원문 대비 {k1 / NATIVE:.0%}, 성취기준 {k2 / NATIVE:.0%}")

if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], 1)
    build(sys.argv[1], sys.argv[2], 2)
