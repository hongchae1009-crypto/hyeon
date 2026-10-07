"""참고 해설(유기 기출 해설)과 같은 책 형식의 모범답안 HTML/PDF 빌더.

각 문항: [머리글 상자: 연도 | 단원] → 원본 문항 이미지 → [해설] (정답 → 핵심 개념 → 풀이 → 그림 → 예상 의문점)
사용: python3 build_book.py <모범답안.html> <출력 폴더> <교재 PDF 3개> <2025·2026 시험지 PDF 4개>
"""
import base64
import html
import importlib
import pathlib
import re
import sys

import build
import build_problems as BP
import extract_pages
import problems_2526

MODULES = ["content_u01_04", "content_u05_08", "content_u09_12", "content_u13_16", "content_17_20", "content_u21"]

BOOK_CSS = """
body{font-family:'Noto Serif CJK KR','Batang','Malgun Gothic',serif;color:#111}
.ph{display:flex;width:264pt;border:.8pt solid #000;font-family:'Noto Sans CJK KR','Malgun Gothic',sans-serif;font-size:11.5pt;line-height:1.25;color:#000;margin:0 0 8pt;background:#fff}
.ph .y{flex:none;width:58pt;text-align:center;border-right:.8pt solid #000;padding:0 4pt}
.ph .u{padding:0 8pt}
.qimg{display:block;max-width:100%;height:auto;margin:0 0 10px}
.hs{font-weight:700;margin:12px 0 4px;font-size:15px}
article.q{background:#fff;border:1px solid #d6d9de;border-radius:4px}
article.q .q-head,article.q .stem,article.q h3.unit-h{display:none}
article.q .answer{background:none;border:none;border-left:3px solid #111;border-radius:0;padding:2px 0 2px 10px;margin:4px 0 10px}
article.q .answer .lbl{background:#111}
article.q h5{color:#111;font-size:14.5px;border-bottom:.6pt solid #999;padding-bottom:2px}
article.q .cur,article.q .refcmp{background:#fafafa;border:.8pt solid #999}
article.q .refcmp h5{color:#111}
.faq{border-left:2px solid #999}
@media print{
  body{background:#fff;font-size:10.3pt}
  .cover,.ut,.yt{display:none!important}
  article.q{break-before:page;page-break-before:always;border:none;border-radius:0;padding:0;margin:0;break-inside:auto;page-break-inside:auto}
  .unit-sec,.year-sec{break-before:auto;page-break-before:auto;margin:0}
  .unit-sec:first-child article.q:first-child,.year-sec:first-child article.q:first-child{break-before:auto;page-break-before:auto}
  .keep{break-inside:auto;page-break-inside:auto}
  .qimg{width:var(--pw);break-inside:avoid}
  figure{break-inside:avoid}
}
@page{@bottom-center{content:none}}
"""

MARGIN = {"top": "14mm", "bottom": "18mm", "left": "14mm", "right": "14mm"}


def esc(t):
    return html.escape(str(t), quote=True)


def model_id(year, exam):
    m = re.match(r"(전공[AB]) (기입형|서술형|논술형) (\d+)번", exam)
    return f"y-{year}-{m.group(1)}-{m.group(2)}-{m.group(3)}"


def load_units(arts):
    units = []
    for mn in MODULES:
        units += importlib.import_module(mn).UNITS
    byno = {u["no"]: u for u in units}
    # 2025·2026: 기존 모범답안 파일의 해설 재사용 (단원 맨 앞, 최근 연도 먼저)
    for it in sorted(problems_2526.ITEMS, key=lambda x: -x["year"]):
        aid = model_id(it["year"], it["exam"])
        sub = re.search(r'<h3 class="unit-h">(.*?)</h3>', arts[aid]).group(1)
        new = {"reuse": aid, "year": it["year"], "exam": it["exam"], "pts": it["pts"], "sub": html.unescape(sub),
               "src": it["src"], "_2526": True}
        u = byno[it["unit"]]
        k = sum(1 for x in u["items"] if x.get("_2526"))
        u["items"].insert(k, new)
    return sorted(units, key=lambda u: u["no"])


def attach_images(units, book_pdfs, exams):
    bym = {}
    for b in extract_pages.extract(book_pdfs):
        bym.setdefault(b["unit"], []).append(b)
    for u in units:
        bl = bym.get(u["no"], [])
        used = [False] * len(bl)
        book_items = [it for it in u["items"] if not it.get("_2526")]
        pending = []
        for it in book_items:  # 같은 연도의 쪽부터 순서대로
            for j, b in enumerate(bl):
                if not used[j] and int(b["year"][:4]) == it["year"]:
                    used[j] = True
                    it["_img"] = b
                    break
            else:
                pending.append(it)
        left = [b for j, b in enumerate(bl) if not used[j]]
        for it in pending:  # 교재 머리글 연도가 잘못된 쪽(2016→2015, 2019→2013)
            it["_img"] = left.pop(0)
        for it in u["items"]:
            if it.get("_2526"):
                ab, page, q = it["src"]
                it["_img"] = extract_pages.extract_exam_question(exams[(it["year"], ab)], page, q)
                it["_img"]["year"] = f'{it["year"]} {ab}'


def inject(h, units):
    for u in units:
        for it in u["items"]:
            img = it["_img"]
            ylab = img.get("year") or str(it["year"])
            src = "data:image/png;base64," + base64.b64encode(img["png"]).decode()
            top = (f'<div class="ph"><span class="y">{esc(ylab)}</span><span class="u">{esc(build.unit_label(u))}</span></div>'
                   f'<img class="qimg" src="{src}" width="{round(img["w"] * 0.9)}" style="--pw:{round(img["w"] * 0.64)}px" alt="문항">'
                   '<div class="hs">[해설]</div>')
            st = h.index(f'id="{it["_aid"]}"')
            qh = h.index('<div class="q-head"', st)
            h = h[:qh] + top + h[qh:]
    return h


def start_pages(pdf, n_items):
    """각 쪽 머리글 상자 텍스트 위치로 문항 시작 쪽 찾기"""
    import pymupdf as fitz
    d = fitz.open(pdf)
    starts = []
    for i in range(d.page_count):
        t = d[i].get_text("dict")
        top = [s for b in t["blocks"] if b["type"] == 0 for l in b["lines"] for s in l["spans"] if s["bbox"][1] < 60]
        if any(re.fullmatch(r"\d{1,2}\. .+", s["text"].strip()) for s in top):
            starts.append(i + 1)
    total = d.page_count
    d.close()
    assert len(starts) == n_items, (len(starts), n_items)
    return starts, total


def make(units, arts, css, out_html, out_pdf, title, sub, kind="unit", per_unit=False):
    h = build.build(units, arts, css, title, sub)
    h = h.replace("</style>", BOOK_CSS + "</style>", 1)
    h = inject(h, units)
    out_html.write_text(h, encoding="utf-8")
    n = sum(len(u["items"]) for u in units)
    pdfs = []
    for view in (("unit", "year") if not per_unit else ("unit",)):
        pdf = out_pdf if view == "unit" else out_pdf.with_name(out_pdf.stem.replace("(단원순)", "(연도순)") + ".pdf")
        build.to_pdf(out_html, pdf, view=view, footer=BP.FOOT, margin=MARGIN)
        starts, total = start_pages(pdf, n)
        if per_unit:
            rows = [(f'{it["year"]} · {it["exam"]}', s, s) for it, s in zip(units[0]["items"], starts)]
            heading = "문항 목록"
        elif view == "unit":
            rows, k = [], 0
            for u in units:
                m = len(u["items"])
                end = starts[k + m] - 1 if k + m < n else total
                rows.append((build.unit_label(u), starts[k], end))
                k += m
            heading = "목차 (단원별)"
        else:
            seq = [it for u in units for it in u["items"]]
            order = sorted(range(len(seq)), key=lambda i: (-seq[i]["year"], i))
            rows, cur = [], None
            for pos, i in enumerate(order):
                y = seq[i]["year"]
                end = starts[pos + 1] - 1 if pos + 1 < n else total
                if y != cur:
                    rows.append([f"{y}학년도", starts[pos], end])
                    cur = y
                else:
                    rows[-1][2] = end
            rows = [tuple(r) for r in rows]
            heading = "목차 (연도별)"
        note = ("· 각 문항: 원본 문항 → [해설] 정답·핵심 개념·풀이 과정(메커니즘·계산)·그림·예상 의문점.<br>"
                "· 2002–2023학년도 해설은 「유기 기출 해설」과 대조·보강했고, 참고한 쪽을 각 문항 끝에 표시했습니다.<br>"
                "· 2024학년도까지 문항은 단원별 기출 교재, 2025·2026학년도는 시험지 원본에서 수록했습니다.")
        tp = pdf.with_name("_toc.pdf")
        BP.toc_pdf(tp, title, sub, heading, rows, note)
        BP.prepend(tp, pdf)
        pdfs.append(pdf)
    return pdfs


if __name__ == "__main__":
    model, outdir, rest = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3:]
    exams = BP.exam_map(rest)
    book = [p for p in rest if p not in exams.values()]
    css, arts = build.load_model(model)
    units = load_units(arts)
    attach_images(units, book, exams)
    outdir.mkdir(parents=True, exist_ok=True)
    n = sum(len(u["items"]) for u in units)
    sub = f"중등 화학 교사 임용시험 1차 · 1997–2026학년도 · {n}문항"
    make(units, arts, css, outdir / "유기화학_단원별_모범답안_합본.html", outdir / "유기화학_단원별_모범답안_합본(단원순).pdf",
         "유기화학 단원별 기출 해설", sub)
    for u in units:
        name = f'유기화학_{u["no"]:02d}_{u["name"].replace(" ", "").replace("–", "-")}'
        make([u], arts, css, outdir / f"{name}.html", outdir / f"{name}.pdf",
             f"유기화학 기출 해설 — {build.unit_label(u)}", f"중등 화학 교사 임용시험 1차 · {len(u['items'])}문항", per_unit=True)
    print(n, "문항")
