# -*- coding: utf-8 -*-
"""2022 개정 과학과 교육과정 원문(김지현 편집 스캔 PDF)을 B4 모아찍기로 컷아웃한다.
  1쪽: 내용 체계 표 6개  /  2쪽~: 성취기준 · 성취기준 해설 · 적용 시 고려 사항
쪽마다 바깥 테두리 안쪽만 잘라, 빈 줄로 나뉜 내용 띠를 다단으로 차례대로 채운다.
사용: python3 b4_merge.py <2022 교육과정-1-23.pdf> <2022 교육과정-24-48.pdf>"""
import io, pathlib, re, subprocess, sys
import numpy as np, pymupdf
from PIL import Image
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).parent
FONT = "/root/.fonts/NanumGothic-Bold.ttf"
MM = 72 / 25.4
B4 = (257 * MM, 364 * MM)
PAPER = {"B4": B4, "A3": (297 * MM, 420 * MM)}
FOLD = [B4]  # 반 접기 판의 종이(세로 기준 너비, 높이)
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

def kind_of(im):
    """한 줄짜리 좁은 띠를 OCR해서 세부 단원 제목 '(1) …'인지, 지울 머리 제목('나. 성취기준' 등)인지 가린다."""
    if im.height > 75 or im.width > 0.6 * 1400: return "body"
    t = subprocess.run(["tesseract", "-", "-", "-l", "kor", "--psm", "7"], input=_png(im), capture_output=True).stdout.decode("utf-8", "ignore")
    t = re.sub(r"\s+", "", t)
    if re.match(r"^[\(（]\d+[\)）]", t): return "unit"
    if re.match(r"^(나\.|가\.|\d\.)?(성취기준|내용체계)", t) or re.match(r"^\d\.내용체계", t): return "drop"
    return "body"

def _png(im):
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True); return buf.getvalue()

def layout_fold(doc, groups, npages, cph, title, k_max, unit_gap=3.2, gap=1.0):
    """B4 가로를 반으로 접어 쓰는 판(왼쪽·오른쪽 반이 각각 B5 세로). groups: [(과목 제목, [(종류, 그림)])].
    과목마다 테두리 상자로 묶고(단이 넘어가면 '(계속)' 머리), 세부 단원 사이는 띄운다. 들어가는 가장 큰 배율을 쓴다."""
    W, H = FOLD[0][1], FOLD[0][0]; half = W / 2
    mo, mi, top, bot, cg = 8 * MM, 7 * MM, 14 * MM, 7 * MM, 4 * MM
    pad, hd, sg = 1.8 * MM, 5.2 * MM, 3.0 * MM  # 상자 안 여백, 상자 머리 높이, 상자 사이 간격
    cw = (half - mo - mi - (cph - 1) * cg) / cph; ch = H - top - bot; ncol = npages * 2 * cph
    iw = cw - 2 * pad
    def colx(c):
        h, j = divmod(c % (2 * cph), cph)
        return (mo if h == 0 else half + mi) + j * (cw + cg)
    def place(k):
        out, c, y = [], 0, 0  # out: (종류, 값, 단, y, 높이, 과목 번호)
        for gi, (name, items) in enumerate(groups):
            if name.startswith("과학과 교육과정 설계") and y > 0:  # 개요는 새 단 맨 위에서 시작
                c += 1; y = 0
                if c >= ncol: return None
            if y > 0: y += sg
            first = True
            for i, (kd, im) in enumerate(items):
                if im.width * k > iw: return None
                h = im.height * k
                pre = (unit_gap * MM if kd == "unit" and not first else gap * MM if not first else 0)
                nxt = items[i + 1][1].height * k if kd == "unit" and i + 1 < len(items) else 0  # 단원 제목은 다음 덩어리와 함께
                head = hd if first else 0
                if y + head + pre + h + nxt + pad > ch and y > 0:
                    c += 1; y = 0
                    if c >= ncol: return None
                    out.append(("head", name + (" (계속)" if not first else ""), c, 0, hd, gi)); y = hd + pad; pre = 0
                elif first:
                    out.append(("head", name, c, y, hd, gi)); y += hd + pad
                y += pre
                out.append((kd, im, c, y, h, gi)); y += h
                first = False
            y += pad
        return out
    k = k_max
    while (pos := place(k)) is None: k *= 0.99
    F = pymupdf.Font(fontfile=FONT); base = len(doc)
    for n in range(npages):
        pg = doc.new_page(width=W, height=H); pg.insert_font(fontname="ng", fontfile=FONT)
        for hf in range(2):
            x0 = mo if hf == 0 else half + mi; x1 = half - mi if hf == 0 else W - mo
            pg.insert_text((x0, 10 * MM), title, fontname="ng", fontsize=11.5)
            tag = f"{n * 2 + hf + 1} / {npages * 2}"
            pg.insert_text((x1 - F.text_length(tag, fontsize=8.5), 10 * MM), tag, fontname="ng", fontsize=8.5, color=(.4, .4, .4))
            pg.draw_line((x0, 12 * MM), (x1, 12 * MM), width=1)
        pg.draw_line((half, 4 * MM), (half, H - 4 * MM), width=.5, color=(.6, .6, .6), dashes="[3 3] 0")
    # 과목 상자: 같은 과목·같은 단의 덩어리를 하나의 테두리로
    seg = {}
    for kd, v, c, y, h, gi in pos:
        a0, a1 = seg.get((gi, c), (y, y + h)); seg[(gi, c)] = (min(a0, y), max(a1, y + h))
    for (gi, c), (y0, y1) in seg.items():
        pg = doc[base + c // (2 * cph)]; x = colx(c)
        pg.draw_rect(pymupdf.Rect(x, top + y0, x + cw, top + y1 + pad), color=(.10, .24, .43), width=.9)
    for kd, v, c, y, h, gi in pos:
        pg = doc[base + c // (2 * cph)]; x = colx(c); yy = top + y
        if kd == "head":
            pg.draw_rect(pymupdf.Rect(x, yy, x + cw, yy + h), color=None, fill=(.10, .24, .43))
            fs = min(9.5, (cw - 3.6 * MM) / F.text_length(v, fontsize=1))
            pg.insert_text((x + 1.8 * MM, yy + h / 2 + fs * 0.36), v, fontname="ng", fontsize=fs, color=(1, 1, 1))
        else:
            if kd == "unit":  # 세부 단원: 옅은 띠 + 앞쪽 구분선
                pg.draw_rect(pymupdf.Rect(x + pad * .5, yy - .6 * MM, x + cw - pad * .5, yy + h + .4 * MM), color=None, fill=(.91, .93, .97))
            pg.insert_image(pymupdf.Rect(x + pad, yy, x + pad + v.width * k, yy + h), stream=_png(v))
    return k

def layout_rows(doc, subjects, title, k_max, per_row=4):
    """성취기준 '과목 = 가로 한 줄, 단원 = 칸' 배치. B4 가로를 반으로 접어 쓰므로 한 줄의 칸은 접는 선 양쪽에 반씩.
    subjects: [(과목 제목, [단원별 [(종류, 그림)]])]. 과목마다 남색 머리 + 테두리, 단원 사이는 세로 구분선.
    한 과목이 per_row개보다 단원이 많으면 다음 줄로 이어 간다. 줄이 쪽에 안 들어가면 다음 쪽."""
    W, H = FOLD[0][1], FOLD[0][0]; half = W / 2
    mo, mi, top, bot, cg = 8 * MM, 7 * MM, 14 * MM, 6 * MM, 3 * MM
    pad, hd, sg = 1.6 * MM, 5.6 * MM, 3.5 * MM
    cph = per_row // 2
    cw = (half - mo - mi - (cph - 1) * cg) / cph; ch = H - top - bot
    def colx(j):
        h, jj = divmod(j, cph)
        return (mo if h == 0 else half + mi) + jj * (cw + cg)
    uh = lambda u, k: sum(im.height * k for _, im in u) + 1.2 * MM * (len(u) - 1)
    rows = []  # (과목 번호, 이어짐 여부, [단원])
    for gi, (name, units) in enumerate(subjects):
        for r in range(0, len(units), per_row): rows.append((gi, r > 0, units[r:r + per_row]))
    def paginate(k):
        pages, y = [[]], 0
        for gi, cont, us in rows:
            h = hd + pad + max(uh(u, k) for u in us) + pad
            if y + h > ch and y > 0: pages.append([]); y = 0
            pages[-1].append((gi, cont, us, y, h)); y += h + sg
        return pages
    k = min(k_max, min((cw - 2 * pad) / im.width for _, us in subjects for u in us for _, im in u))
    best = paginate(k)
    for t in range(1, 11):  # 10%까지 줄여서 쪽 수가 줄면 그 배율을 쓴다
        pp = paginate(k * (1 - t / 100))
        if len(pp) < len(best): k, best = k * (1 - t / 100), pp; break
    F = pymupdf.Font(fontfile=FONT); NAVY = (.10, .24, .43)
    for n, rws in enumerate(best):
        pg = doc.new_page(width=W, height=H); pg.insert_font(fontname="ng", fontfile=FONT)
        for hf in range(2):
            x0 = mo if hf == 0 else half + mi; x1 = half - mi if hf == 0 else W - mo
            pg.insert_text((x0, 10 * MM), title, fontname="ng", fontsize=11.5)
            tag = f"{n * 2 + hf + 1} / {len(best) * 2}"
            pg.insert_text((x1 - F.text_length(tag, fontsize=8.5), 10 * MM), tag, fontname="ng", fontsize=8.5, color=(.4, .4, .4))
            pg.draw_line((x0, 12 * MM), (x1, 12 * MM), width=1)
        pg.draw_line((half, 4 * MM), (half, H - 4 * MM), width=.5, color=(.6, .6, .6), dashes="[3 3] 0")
        for gi, cont, us, y, h in rws:
            name = subjects[gi][0]; yy = top + y
            for hf in range(2):
                js = [j for j in range(len(us)) if j // cph == hf]
                if not js: continue
                x0 = colx(js[0]); x1 = colx(js[-1]) + cw if hf == 0 or len(js) > 0 else 0
                if hf == 0 and len(us) <= cph: x1 = colx(cph - 1) + cw
                if hf == 1: x1 = colx(2 * cph - 1) + cw
                if hf == 0: x1 = colx(cph - 1) + cw
                lab = name + (" (계속)" if cont or hf == 1 else "")
                pg.draw_rect(pymupdf.Rect(x0, yy, x1, yy + hd), color=None, fill=NAVY)
                fs = min(10, (x1 - x0 - 4 * MM) / F.text_length(lab, fontsize=1))
                pg.insert_text((x0 + 2 * MM, yy + hd / 2 + fs * .36), lab, fontname="ng", fontsize=fs, color=(1, 1, 1))
                pg.draw_rect(pymupdf.Rect(x0, yy, x1, yy + h), color=NAVY, width=1)
                for j in js[1:]:
                    xs = colx(j) - cg / 2
                    pg.draw_line((xs, yy + hd + pad), (xs, yy + h - pad), width=.5, color=(.6, .66, .75))
            for j, u in enumerate(us):
                x = colx(j) + pad; cy = yy + hd + pad
                for kd, im in u:
                    hh = im.height * k
                    if kd == "unit":
                        pg.draw_rect(pymupdf.Rect(x - .8 * MM, cy - .5 * MM, colx(j) + cw - pad + .8 * MM, cy + hh + .4 * MM), color=None, fill=(.90, .93, .98))
                    pg.insert_image(pymupdf.Rect(x, cy, x + im.width * k, cy + hh), stream=_png(im))
                    cy += hh + 1.2 * MM
    return k, len(best)

def layout_rows_flow(doc, subjects, title, k_max, cph=3):
    """성취기준 한 쪽 판: 과목 = 가로 한 줄(접는 선 양쪽 cph단씩, 모두 2·cph단), 줄 안에서는 단원을 1→2→3…
    왼쪽 단부터 차례로 흘려 담는다(단원 제목은 다음 덩어리와 함께, 단원 사이는 띄움). 과목 줄의 높이는
    그 과목이 들어가는 가장 낮은 높이로 맞추고, 모든 과목이 한 쪽에 들어가는 가장 큰 배율을 찾는다."""
    W, H = FOLD[0][1], FOLD[0][0]; half = W / 2
    mo, mi, top, bot, cg = 7 * MM, 6 * MM, 13 * MM, 5 * MM, 2.6 * MM
    pad, hd, sg, ug, ig = 1.3 * MM, 4.6 * MM, 2.2 * MM, 2.4 * MM, .7 * MM
    ncol = 2 * cph; cw = (half - mo - mi - (cph - 1) * cg) / cph; ch = H - top - bot
    def colx(j):
        h, jj = divmod(j, cph)
        return (mo if h == 0 else half + mi) + jj * (cw + cg)
    flat = [[(kd, im) for u in units for kd, im in u] for _, units in subjects]
    def flow(items, k, hmax):
        pos, c, y = [], 0, 0
        for i, (kd, im) in enumerate(items):
            h = im.height * k
            pre = (ug if kd == "unit" else ig) if y > 0 else 0
            nxt = items[i + 1][1].height * k + ig if kd == "unit" and i + 1 < len(items) else 0
            if y + pre + h + nxt > hmax and y > 0:
                c += 1; y = 0; pre = 0
                if c >= ncol: return None
            pos.append((kd, im, c, y + pre, h)); y += pre + h
        return pos
    def fit(items, k):  # 이 과목이 들어가는 가장 낮은 줄 높이
        lo, hi = max(im.height * k for _, im in items), ch
        if flow(items, k, hi) is None: return None
        for _ in range(30):
            mid = (lo + hi) / 2
            if flow(items, k, mid) is None: lo = mid
            else: hi = mid
        return hi, flow(items, k, hi)
    def total(k):
        r = [fit(it, k) for it in flat]
        if any(x is None for x in r): return None
        return sum(hd + 2 * pad + x[0] for x in r) + sg * (len(r) - 1), r
    k = min(k_max, min((cw - 2 * pad) / im.width for it in flat for _, im in it))
    while (t := total(k)) is None or t[0] > ch: k *= 0.99
    F = pymupdf.Font(fontfile=FONT); NAVY = (.10, .24, .43)
    pg = doc.new_page(width=W, height=H); pg.insert_font(fontname="ng", fontfile=FONT)
    for hf in range(2):
        x0 = mo if hf == 0 else half + mi; x1 = half - mi if hf == 0 else W - mo
        pg.insert_text((x0, 9.5 * MM), title, fontname="ng", fontsize=11)
        pg.draw_line((x0, 11.3 * MM), (x1, 11.3 * MM), width=1)
    pg.draw_line((half, 4 * MM), (half, H - 4 * MM), width=.5, color=(.6, .6, .6), dashes="[3 3] 0")
    y = top
    for (name, _), (hh, pos) in zip(subjects, t[1]):
        bh = hd + 2 * pad + hh
        for hf in range(2):
            x0, x1 = colx(hf * cph), colx(hf * cph + cph - 1) + cw
            if hf == 1 and not any(c >= cph for _, _, c, _, _ in pos): continue
            lab = name if hf == 0 else name.split("  ")[0] + " (계속)"
            pg.draw_rect(pymupdf.Rect(x0, y, x1, y + hd), color=None, fill=NAVY)
            fs = min(9.5, (x1 - x0 - 4 * MM) / F.text_length(lab, fontsize=1))
            pg.insert_text((x0 + 1.8 * MM, y + hd / 2 + fs * .36), lab, fontname="ng", fontsize=fs, color=(1, 1, 1))
            pg.draw_rect(pymupdf.Rect(x0, y, x1, y + bh), color=NAVY, width=.9)
            for j in range(hf * cph + 1, hf * cph + cph):
                if any(c == j for _, _, c, _, _ in pos):
                    xs = colx(j) - cg / 2
                    pg.draw_line((xs, y + hd + pad), (xs, y + bh - pad), width=.4, color=(.6, .66, .75))
        for kd, im, c, yy, h in pos:
            x = colx(c) + pad; Y = y + hd + pad + yy
            if kd == "unit":
                pg.draw_rect(pymupdf.Rect(x - .7 * MM, Y - .4 * MM, colx(c) + cw - pad + .7 * MM, Y + h + .3 * MM), color=None, fill=(.90, .93, .98))
            pg.insert_image(pymupdf.Rect(x, Y, x + im.width * k, Y + h), stream=_png(im))
        y += bh + sg
    return k

def _partition(hs, ncol, gap):
    """단원 높이 hs를 순서대로 ncol칸 이하로 나눌 때 가장 높은 칸이 가장 낮은 나눔(칸별 단원 번호 목록)."""
    import itertools
    n = len(hs); best = None
    for m in range(1, min(ncol, n) + 1):
        for cuts in itertools.combinations(range(1, n), m - 1):
            b = (0,) + cuts + (n,)
            cols = [list(range(b[i], b[i + 1])) for i in range(m)]
            hmax = max(sum(hs[j] for j in c) + gap * (len(c) - 1) for c in cols)
            if best is None or hmax < best[0] - 1e-6: best = (hmax, cols)
    return best

def layout_halves(doc, subjects, title, k_max, cph=3):
    """성취기준 한 쪽 판(반 접기): 접은 한 면(왼쪽·오른쪽 반)마다 과목을 위에서 아래로 쌓고,
    과목 상자 안에서는 단원을 cph칸에 1→2→3… 순서로 나눠 담는다. 단원은 절대 자르지 않는다.
    앞쪽 과목들은 왼쪽 면, 나머지는 오른쪽 면 — 둘 다 들어가는 가장 큰 배율을 찾는다."""
    W, H = FOLD[0][1], FOLD[0][0]; half = W / 2
    mo, mi, top, bot, cg = 7 * MM, 6 * MM, 13.5 * MM, 5 * MM, 3 * MM
    pad, hd, sg, ug, ig = 1.5 * MM, 5.6 * MM, 3 * MM, 2.6 * MM, .5 * MM
    cw = (half - mo - mi - (cph - 1) * cg) / cph; ch = H - top - bot
    uh = lambda u, k: sum(im.height * k for _, im in u) + ig * (len(u) - 1)
    def block(units, k):
        hmax, cols = _partition([uh(u, k) for u in units], cph, ug)
        return hd + 2 * pad + hmax, cols
    def plan(k):
        bl = [block(us, k) for _, us in subjects]
        for m in range(1, len(subjects)):
            L = sum(h for h, _ in bl[:m]) + sg * (m - 1); R = sum(h for h, _ in bl[m:]) + sg * (len(bl) - m - 1)
            if L <= ch and R <= ch: return m, bl, max(L, R)
        return None
    k = min(k_max, min((cw - 2 * pad) / im.width for _, us in subjects for u in us for _, im in u))
    while (pl := plan(k)) is None: k *= 0.99
    m, bl, _ = pl
    F = pymupdf.Font(fontfile=FONT); NAVY = (.10, .24, .43)
    pg = doc.new_page(width=W, height=H); pg.insert_font(fontname="ng", fontfile=FONT)
    pg.draw_line((half, 4 * MM), (half, H - 4 * MM), width=.5, color=(.6, .6, .6), dashes="[3 3] 0")
    for hf, idx in enumerate((range(0, m), range(m, len(subjects)))):
        x0 = mo if hf == 0 else half + mi; x1 = x0 + cph * cw + (cph - 1) * cg
        pg.insert_text((x0, 10 * MM), title, fontname="ng", fontsize=13)
        tag = f"{hf + 1} / 2"
        pg.insert_text((x1 - F.text_length(tag, fontsize=9), 10 * MM), tag, fontname="ng", fontsize=9, color=(.4, .4, .4))
        pg.draw_line((x0, 12 * MM), (x1, 12 * MM), width=1.1)
        y = top
        for gi in idx:
            name, units = subjects[gi]; bh, cols = bl[gi]
            pg.draw_rect(pymupdf.Rect(x0, y, x1, y + hd), color=None, fill=NAVY)
            fs = min(11, (x1 - x0 - 4 * MM) / F.text_length(name, fontsize=1))
            pg.insert_text((x0 + 2 * MM, y + hd / 2 + fs * .36), name, fontname="ng", fontsize=fs, color=(1, 1, 1))
            pg.draw_rect(pymupdf.Rect(x0, y, x1, y + bh), color=NAVY, width=1)
            for j, col in enumerate(cols):
                cx = x0 + j * (cw + cg)
                if j: pg.draw_line((cx - cg / 2, y + hd + pad), (cx - cg / 2, y + bh - pad), width=.5, color=(.6, .66, .75))
                yy = y + hd + pad
                for ui in col:
                    for kd, im in units[ui]:
                        h = im.height * k
                        if kd == "unit":
                            pg.draw_rect(pymupdf.Rect(cx + pad - .8 * MM, yy - .5 * MM, cx + cw - pad + .8 * MM, yy + h + .4 * MM), color=None, fill=(.90, .93, .98))
                        pg.insert_image(pymupdf.Rect(cx + pad, yy, cx + pad + im.width * k, yy + h), stream=_png(im))
                        yy += h + ig
                    yy += ug - ig
            y += bh + sg
    return k

def build_land(a, b, paper="A3"):
    """가로(반 접기) 2쪽 판: 1쪽 내용 체계 + 교육과정 설계의 개요, 2쪽 성취기준 전체."""
    FOLD[0] = PAPER[paper]
    bk = Book(a, b); doc = pymupdf.open(); groups = []
    for name, tabs, _ in SUBJ:
        for p, lab in tabs:
            groups.append((f"{lab} — 내용 체계 ({p}쪽)", [("body", x) for x in bands(bk.page(p), 200)]))
    ov = bands(bk.page(5), 10)
    i0 = next(i for i, x in enumerate(ov) if x.height < 90 and "설계" in re.sub(r"\s+", "", subprocess.run(
        ["tesseract", "-", "-", "-l", "kor", "--psm", "7"], input=_png(x), capture_output=True).stdout.decode("utf-8", "ignore")))
    ov = ov[i0 + 1:] + bands(bk.page(6), 10)
    groups.append(("과학과 교육과정 설계의 개요 (5~6쪽)", [("body", x) for x in ov]))
    k1 = layout_fold(doc, groups, 1, 2, "2022 개정 교육과정 — 내용 체계 · 교육과정 설계의 개요", NATIVE)
    subjects = []
    for name, _, ps in SUBJ:
        units, cur = [], None
        for p in ps:
            for x in bands(bk.page(p), 10):
                kd = kind_of(x)
                if kd == "drop": continue
                if kd == "unit" or cur is None: cur = []; units.append(cur)
                cur.append((kd, x))
        subjects.append((f"{name}  성취기준 ({ps[0]}~{ps[-1]}쪽)", units))
    k2 = layout_halves(doc, subjects, "2022 개정 교육과정 — 성취기준", NATIVE)
    out = HERE / f"교육과정_원문컷아웃_{paper}가로.pdf"
    doc.save(out, garbage=4, deflate=True)
    print(f"{out.name}: {len(doc)}쪽 — 1쪽 원문 대비 {k1 / NATIVE:.0%}, 성취기준 {k2 / NATIVE:.0%}")

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
    if "--세로" in sys.argv:
        build(sys.argv[1], sys.argv[2], 1); build(sys.argv[1], sys.argv[2], 2)
    build_land(sys.argv[1], sys.argv[2])
