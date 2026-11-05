# -*- coding: utf-8 -*-
"""컷아웃 빈칸 시험지(컷아웃/*.png)를 B4 모아찍기로 합친다.
쪽마다 내용 덩어리(빈 줄로 나뉜 띠)만 잘라 내어 다단으로 채운다.
  1쪽: 내용 체계 6개 표  /  2쪽: 성취기준·해설·적용 시 고려 사항 전체
정답지는 같은 B4 한 쪽에 내용 체계·성취기준 정답을 모은다."""
import io, pathlib, re, subprocess, sys
import numpy as np, pymupdf
from PIL import Image
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).parent
SRC = HERE / "컷아웃"
FONT = "/root/.fonts/NanumGothic-Bold.ttf"
CHROME = next(iter(sorted(pathlib.Path("/opt/pw-browsers").glob("chromium-*/chrome-linux*/chrome"))))
MM = 72 / 25.4
B4 = (257 * MM, 364 * MM)
ORDER = ["중학교 과학(물질)", "통합과학12", "화학", "물질과 에너지", "화학 반응의 세계"]
LABEL = {"통합과학12": "통합과학1·2", 27: "통합과학1", 34: "통합과학2"}

def bands(f, min_h):
    """쪽 그림에서 테두리를 빼고, 28px 이상 빈 줄로 나뉜 내용 띠(잘라 낸 그림)를 돌려준다."""
    im = Image.open(f).convert("L"); a = np.array(im) < 150; H, W = a.shape
    bc = np.where(a.sum(0) > 0.8 * H)[0]; br = np.where(a.sum(1) > 0.8 * W)[0]
    x0 = bc[bc < W / 2].max() + 6 if (bc < W / 2).any() else 0
    x1 = bc[bc > W / 2].min() - 6 if (bc > W / 2).any() else W
    y1 = br[br > H / 2].min() - 6 if (br > H / 2).any() else H
    sub = a[:y1, x0:x1]; rows = sub.sum(1) > 0
    out, s, gap = [], None, 0
    for y, r in enumerate(list(rows) + [False] * 30):
        if r:
            s = y if s is None else s; gap = 0; e = y
        elif s is not None:
            gap += 1
            if gap >= 28:
                if e - s + 1 >= min_h:
                    cols = np.where(sub[s:e + 1].any(0))[0]
                    if cols.max() - cols.min() < 0.97 * sub.shape[1] or e - s > 20:  # 쪽 아래 가로줄 제외
                        out.append(im.crop((x0 + cols.min() - 4, s - 4, x0 + cols.max() + 5, e + 5)))
                s = None
    return out

def pages(kind):
    fs = sorted(SRC.glob(f"{kind}_*.png"), key=lambda f: (ORDER.index(f.stem.split("_")[1]), int(f.stem.split("_")[2])))
    return [(f.stem.split("_")[1], int(f.stem.split("_")[2]), f) for f in fs]

def layout(doc, items, ncol, title, sub, k_max, gap=2.2):
    """items: ('label', 글) 또는 ('img', PIL) — ncol단에 한 쪽으로 넣는다. 들어가는 가장 큰 배율을 찾는다."""
    W, H = B4; mx, top, bot, cg = 9 * MM, 19 * MM, 8 * MM, 5 * MM
    cw = (W - 2 * mx - (ncol - 1) * cg) / ncol; ch = H - top - bot
    def place(k):
        pos, c, y = [], 0, 0
        for t, v in items:
            h = 4.6 * MM if t == "label" else v.height * k
            w = 0 if t == "label" else v.width * k
            if t == "img" and w > cw: return None
            if y + h > ch and y > 0:
                c += 1; y = 0
                if c >= ncol: return None
            pos.append((t, v, c, y, h)); y += h + (0.6 * MM if t == "label" else gap * MM)
        return pos
    k = k_max
    while (pos := place(k)) is None: k *= 0.985
    pg = doc.new_page(width=W, height=H)
    pg.insert_font(fontname="ng", fontfile=FONT)
    pg.insert_text((mx, 11 * MM), title, fontname="ng", fontsize=13)
    pg.insert_text((mx, 15.5 * MM), sub, fontname="ng", fontsize=8.5, color=(.3, .3, .3))
    pg.insert_text((W - mx - 62 * MM, 13 * MM), "이름 ____________   점수 ________", fontname="ng", fontsize=10)
    pg.draw_line((mx, 17 * MM), (W - mx, 17 * MM), width=1.1)
    for c in range(1, ncol):
        x = mx + c * cw + (c - 0.5) * cg
        pg.draw_line((x, top), (x, H - bot), width=.4, color=(.7, .7, .7))
    for t, v, c, y, h in pos:
        x = mx + c * (cw + cg); yy = top + y
        if t == "label":
            pg.draw_rect(pymupdf.Rect(x, yy, x + cw, yy + h), color=None, fill=(.88, .91, .96))
            pg.insert_text((x + 1.5 * MM, yy + h - 1.2 * MM), v, fontname="ng", fontsize=8.6, color=(.1, .24, .43))
        else:
            buf = io.BytesIO(); v.save(buf, "PNG")
            pg.insert_image(pymupdf.Rect(x, yy, x + v.width * k, yy + h), stream=buf.getvalue())
    return k

def build():
    doc = pymupdf.open(); info = []
    # 1쪽: 내용 체계
    items = []
    for subj, p, f in pages("내용체계"):
        items.append(("label", f"{LABEL.get(p, LABEL.get(subj, subj))} — 내용 체계 (원문 {p}쪽)"))
        items += [("img", b) for b in bands(f, 200)]
    k1 = layout(doc, items, 2, "2022 개정 과학과 교육과정 — 내용 체계 (원문 컷아웃 빈칸)",
                "중학교 과학(물질) · 통합과학1·2 · 화학 · 물질과 에너지 · 화학 반응의 세계  |  빈칸 번호는 과목별로 1번부터", 0.2)
    # 2쪽: 성취기준
    items, last = [], None
    for subj, p, f in pages("성취기준"):
        if subj != last:
            items.append(("label", f"{LABEL.get(subj, subj)} — 성취기준 · 해설 · 적용 시 고려 사항")); last = subj
        items += [("img", b) for b in bands(f, 10)]
    k2 = layout(doc, items, 4, "2022 개정 과학과 교육과정 — 성취기준 (원문 컷아웃 빈칸)",
                "성취기준 · 성취기준 해설 · 적용 시 고려 사항  |  빈칸 번호는 과목별로 1번부터", 0.2, gap=1.2)
    out = HERE / "교육과정_원문컷아웃_B4_문제지.pdf"
    doc.save(out, garbage=4, deflate=True)
    native = 186 / 1755 * MM  # 기존 A4 컷아웃 시험지 배율
    print(f"문제지 {len(doc)}쪽 — 내용 체계 배율 {k1 / native:.2f}, 성취기준 배율 {k2 / native:.2f} (A4 컷아웃 대비)")
    # 정답지: 기존 정답 HTML 두 개의 본문을 B4 한 쪽에
    body = ""
    for kind in ("내용체계", "성취기준"):
        h = (HERE / f"교육과정_원문컷아웃_{kind}_정답지.html").read_text(encoding="utf-8")
        h = re.search(r"<div class='ans'>(.*)</div></body>", h, re.S).group(1)
        body += re.sub(r"<h1>.*?</h1>", f"<h2>{'내용 체계' if kind == '내용체계' else '성취기준 · 해설 · 적용 시 고려 사항'}</h2>", h, flags=re.S)
    css = """@page{size:257mm 364mm;margin:9mm 9mm}body{margin:0;font-family:'NanumGothic',sans-serif;font-size:7.6pt;line-height:1.32}
h1{font-size:12pt;margin:0 0 2mm;border-bottom:1.1pt solid #111;padding-bottom:1mm}
h2{font-size:9.4pt;margin:2mm 0 1mm;background:#1a3d6d;color:#fff;padding:.4mm 2mm}
h3{font-size:8.2pt;margin:1.6mm 0 .6mm;color:#1a3d6d;border-bottom:.4pt solid #9ab}
.grid{column-count:5;column-gap:3.5mm;column-rule:.4pt solid #ccc}.grid div{break-inside:avoid}
.grid b{display:inline-block;min-width:5mm;color:#1a3d6d}.grid small{color:#999}"""
    stem = "교육과정_원문컷아웃_B4_정답지"
    hp = HERE / f"{stem}.html"
    hp.write_text(f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>{stem}</title><style>{css}</style></head><body>"
                  f"<h1>2022 개정 교육과정 원문 컷아웃 빈칸 — 정답 (B4)</h1>{body}</body></html>", encoding="utf-8")
    subprocess.run([str(CHROME), "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={HERE / (stem + '.pdf')}", f"file://{hp}"], capture_output=True)
    print("정답지", len(pymupdf.open(HERE / f"{stem}.pdf")), "쪽")

if __name__ == "__main__":
    build()
