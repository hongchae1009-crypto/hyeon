"""MDEET 자연과학Ⅱ 유기화학(21–30번) 5개년: 문제집(문제만) + 상세 해설집(가로형).

사용: python3 build_md.py <모범답안.html(CSS용)> <출력 폴더> [--problems-only]
문제지 PDF는 업로드 폴더에서 연도로 찾는다.
"""
import base64
import glob
import html
import importlib
import pathlib
import sys

import build
import build_land as BL
import build_problems as BP
import extract_pages
import pdflinks
import pymupdf as fitz

UP = "/root/.claude/uploads/6ef8c8cd-b37c-5968-b1c9-51a802c3b4d1/"
YEARS = [2027, 2026, 2025, 2024, 2023]          # 최근 연도부터
KEY = {
    2023: "③④②⑤④④②③①①", 2024: "②①③④①④⑤③⑤②", 2025: "③③②④⑤⑤①①③④",
    2026: "②①③⑤②④⑤③②④", 2027: "③⑤④①④④⑤②③①",
}
TITLE_P = "MDEET 자연과학Ⅱ 유기화학 기출 (2023–2027학년도)"
TITLE_S = "MDEET 자연과학Ⅱ 유기화학 상세 해설 (2023–2027학년도)"


def esc(t):
    return html.escape(str(t), quote=True)


def load_images():
    imgs = {}
    for y in YEARS:
        f = glob.glob(UP + f"*{y}________2.pdf")[0]
        for r in extract_pages.extract_md(f):
            imgs[(y, r["q"])] = r
    return imgs


def load_items():
    """연도별 해설 모듈(md_YYYY.py)이 있으면 읽는다"""
    out = {}
    for y in YEARS:
        try:
            out[y] = {it["q"]: it for it in importlib.import_module(f"md_{y}").ITEMS}
        except ModuleNotFoundError:
            out[y] = {}
    return out


# ------------------------------------------------------------------ 문제집
P_CSS = """
body{font-family:'Noto Sans CJK KR','Malgun Gothic',sans-serif;color:#111;margin:0;background:#f6f7f9}
main{max-width:820px;margin:0 auto;padding:20px}
article.q{background:#fff;border:1px solid #e3e6eb;border-radius:10px;padding:14px 18px;margin:0 0 18px}
.phw{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px}
.ph{display:flex;border:.8pt solid #000;font-size:11.5pt;line-height:1.25}
.ph .y{width:96pt;text-align:center;border-right:.8pt solid #000;padding:0 4pt}
.ph .u{padding:0 8pt;min-width:150pt}
.toidx{font-size:8.5pt;color:#666;text-decoration:none}
.pimg{display:block;max-width:100%;height:auto}
h1{font-size:22px}
@media print{
  @page{size:A4;margin:14mm 14mm 18mm}
  body{background:#fff} main{padding:0;max-width:none}
  .cover{display:none}
  article.q{break-after:page;page-break-after:always;break-inside:avoid;border:none;padding:0;margin:0}
  article.q:last-of-type{break-after:auto;page-break-after:auto}
  .pimg{width:var(--pw);max-width:100%;height:auto;max-height:243mm;object-fit:contain;object-position:left top}
}
@page{@bottom-center{content:none}}
"""


def build_problems(imgs, items, outdir):
    arts, rows, order = [], [], []
    for y in YEARS:
        for q in range(21, 31):
            r = imgs[(y, q)]
            it = items[y].get(q, {})
            topic = it.get("sub", "")
            src = "data:image/png;base64," + base64.b64encode(r["png"]).decode()
            arts.append(f'<article class="q" id="p{y}-{q}"><div class="phw"><div class="ph"><span class="y">{y} MDEET</span>'
                        f'<span class="u">자연과학Ⅱ {q}번</span></div><a class="toidx" href="#">▲ 목차</a></div>'
                        f'<img class="pimg" src="{src}" width="{round(r["w"] * 0.9)}" style="--pw:{round(r["w"] * 0.64)}px" alt="{y} {q}번"></article>')
            order.append((y, q, topic))
    h = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
         f'<title>{TITLE_P}</title><style>{P_CSS}</style></head><body><main><div class="cover"><h1>{TITLE_P}</h1>'
         f'<p>2023–2027학년도 MDEET 자연과학Ⅱ 21–30번 · 50문항 · 정답·해설은 별도 해설집</p></div>{"".join(arts)}</main></body></html>')
    hp = outdir / "MDEET_유기화학_기출문제_2023-2027.html"
    hp.write_text(h, encoding="utf-8")
    pdf = outdir / "MDEET_유기화학_기출문제_2023-2027.pdf"
    build.to_pdf(hp, pdf, footer=BP.FOOT, margin={"top": "14mm", "bottom": "18mm", "left": "14mm", "right": "14mm"})
    # 목차: 문항마다 한 줄 (한 문항 = 한 쪽)
    rows = [(f'{y} · {q}번' + (f' · {t[:22]}' if t else ""), i + 1, i + 1) for i, (y, q, t) in enumerate(order)]
    tp = outdir / "_toc.pdf"
    BP.toc_pdf(tp, TITLE_P, "중등 화학 임용 대비 · MDEET 자연과학Ⅱ 21–30번(유기화학) · 50문항", "목차",
               rows, "· 문항은 시험지 원본을 그대로 잘라 수록했고, 한 문항당 한 쪽이며 아래 빈 공간은 풀이 공간입니다.<br>"
                     "· 정답과 상세 해설(반응·메커니즘·원리·27 임용 연관 분석)은 별도 해설집에 있습니다.")
    k = fitz.open(tp).page_count
    BP.prepend(tp, pdf)
    outline = [[1, "목차", 1]]
    for y in YEARS:
        outline.append([1, f"{y}학년도", k + order.index(next(o for o in order if o[0] == y)) + 1])
        outline += [[2, f"{q}번" + (f" · {t}" if t else ""), k + i + 1] for i, (yy, q, t) in enumerate(order) if yy == y]
    pdflinks.BACK = "▲ 목차"
    pdflinks.finalize(pdf, k, toc_rows=[(t, k + a - 1) for t, a, z in rows], outline=outline)
    pdflinks.BACK = "▲ 색인"
    return pdf


# ------------------------------------------------------------------ 해설집
def build_solutions(imgs, items, css, outdir):
    units = []
    for i, y in enumerate(YEARS, 1):
        its = []
        for q in range(21, 31):
            it = dict(items[y][q])
            it.setdefault("ref_src", f"정답: MDEET {y}학년도 자연과학Ⅱ 정답표(최종) {q}번 {KEY[y][q - 21]}")
            r = imgs[(y, q)]
            it["_img"] = {"png": r["png"], "w": r["w"], "h": r["h"], "year": f"{y} MDEET 자연과학Ⅱ"}
            its.append(it)
        units.append({"no": i, "name": f"{y}학년도 MDEET", "label": f"{y}학년도 MDEET", "items": its})
    orig = build.unit_label
    build.unit_label = lambda u: u.get("label") or orig(u)
    try:
        BL.make(units, {}, css, outdir / "MDEET_유기화학_상세해설_2023-2027.html", outdir / "MDEET_유기화학_상세해설_2023-2027(단원순).pdf",
                TITLE_S, "중등 화학 임용 대비 · 2023–2027학년도 21–30번 · 50문항 · 정답·보기 판정·반응·메커니즘·원리 정리·27 임용 연관 분석",
                views=("unit",))
    finally:
        build.unit_label = orig
    p = outdir / "MDEET_유기화학_상세해설_2023-2027(단원순).pdf"
    p.replace(outdir / "MDEET_유기화학_상세해설_2023-2027.pdf")


# ------------------------------------------------------------------ 문제집 (A3, 한 쪽에 두 문항, 시험지형 2단)
P2_CSS = """
@page{size:A3;margin:12mm 16mm 16mm}
body{font-family:'Noto Sans CJK KR','Malgun Gothic',sans-serif;color:#111;margin:0}
.page{height:392mm;display:flex;flex-direction:column;break-after:page;page-break-after:always;overflow:hidden}
.page:last-child{break-after:auto;page-break-after:auto}
.hd{display:flex;align-items:baseline;gap:14px;padding:0 0 6px;border-bottom:1.2pt solid #111}
.hd b{font-size:17pt;font-weight:800}
.hd span{font-size:10pt;color:#444}
.cols{flex:1;display:grid;grid-template-columns:1fr 1fr;border-bottom:1.2pt solid #111;min-height:0}
.col{padding:8px 12px 0 0;min-width:0}
.col+.col{border-left:.8pt solid #111;padding:8px 0 0 12px}
.tag{font-size:9.5pt;color:#1f5fbf;font-weight:600;margin:0 0 8px}
.col img{display:block;max-width:100%;height:auto}
.solve{font-size:9.5pt;color:#888}
"""


def build_problems_a3(imgs, items, outdir):
    seq = []
    for y in YEARS:
        for q in range(21, 31):
            r = imgs[(y, q)]
            it = items[y].get(q, {})
            seq.append({"y": y, "q": q, "r": r, "pts": it.get("pts"), "sub": it.get("sub", "")})
    col_h_px = (392 - 16) / 25.4 * 96          # 단 높이(CSS px) — 머리글·꼬리표 제외 근사
    def h_px(e):
        return e["r"]["h"] * 0.64
    def cell(n, e):
        r = e["r"]
        src = "data:image/png;base64," + base64.b64encode(r["png"]).decode()
        pts = f' [{e["pts"]}점]' if e["pts"] else ""
        return (f'<div class="col" id="p{e["y"]}-{e["q"]}"><p class="tag">{n}. {e["y"]}학년도 MDEET 자연과학Ⅱ {e["q"]}번{pts}</p>'
                f'<img src="{src}" width="{round(r["w"] * 0.64)}" alt="{e["y"]} {e["q"]}번"></div>')
    pages, i, n = [], 0, 1
    while i < len(seq):
        a = seq[i]
        short = lambda e: h_px(e) <= col_h_px * 0.55
        if i + 1 < len(seq) and short(a) and short(seq[i + 1]) and seq[i + 1]["y"] == a["y"]:
            pages.append(([a, seq[i + 1]], cell(n, a) + cell(n + 1, seq[i + 1])))
            i, n = i + 2, n + 2
        else:
            pages.append(([a], cell(n, a) + '<div class="col"><p class="solve">풀이</p></div>'))
            i, n = i + 1, n + 1
    body = "".join(f'<section class="page"><div class="hd"><b>MDEET 유기화학 기출</b><span>자연과학Ⅱ 21–30번 · {es[0]["y"]}학년도</span></div>'
                   f'<div class="cols">{cells}</div></section>' for es, cells in pages)
    h = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{TITLE_P}</title><style>{P2_CSS}</style></head>'
         f'<body>{body}</body></html>')
    hp = outdir / "MDEET_유기화학_기출문제_2023-2027.html"
    hp.write_text(h, encoding="utf-8")
    pdf = outdir / "MDEET_유기화학_기출문제_2023-2027.pdf"
    foot = ('<div style="font-size:8.5pt;color:#333;width:100%;text-align:center;font-family:sans-serif">'
            'MDEET 유기화학 기출 (<span class="totalPages"></span>면 중 <span class="pageNumber"></span>면)</div>')
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = b.new_page()
        pg.goto(hp.resolve().as_uri())
        pg.emulate_media(media="print")
        pg.pdf(path=str(pdf), prefer_css_page_size=True, print_background=True, display_header_footer=True,
               header_template="<span></span>", footer_template=foot,
               margin={"top": "12mm", "bottom": "16mm", "left": "16mm", "right": "16mm"})
        b.close()
    # 책갈피: 연도 → 문항
    doc = fitz.open(pdf)
    toc, cur = [], None
    for pno, (es, _) in enumerate(pages, 1):
        for e in es:
            if e["y"] != cur:
                toc.append([1, f'{e["y"]}학년도', pno])
                cur = e["y"]
            toc.append([2, f'{e["q"]}번' + (f' · {e["sub"]}' if e["sub"] else ""), pno])
    doc.set_toc(toc)
    tmp = str(pdf) + ".tmp"
    doc.save(tmp, garbage=1, deflate=True)
    doc.close()
    pathlib.Path(tmp).replace(pdf)
    return pdf, len(pages)


if __name__ == "__main__":
    model, outdir = sys.argv[1], pathlib.Path(sys.argv[2])
    outdir.mkdir(parents=True, exist_ok=True)
    imgs = load_images()
    items = load_items()
    print(build_problems_a3(imgs, items, outdir))
    if "--problems-only" not in sys.argv:
        css, _ = build.load_model(model)
        build_solutions(imgs, items, css, outdir)
        print("해설집 완료")
