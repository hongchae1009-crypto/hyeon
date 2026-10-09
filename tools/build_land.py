"""가로형(A4 landscape) 모범답안: 왼쪽 = 기출 원문 + 풀이 그림, 오른쪽 = 해설 본문, 한 쪽에 한 문항.

사용: python3 build_land.py <모범답안.html> <출력 폴더> <교재 PDF 3개> <2025·2026 시험지 PDF 4개>
"""
import base64
import html
import pathlib
import re
import sys

import build
import build_book as BB
import build_problems as BP
import pdflinks
import pymupdf as fitz

C = "#dc2626"

LAND_CSS = """
body{font-family:'Noto Sans CJK KR','Malgun Gothic','Apple SD Gothic Neo',sans-serif}
article.q.land{display:grid;grid-template-columns:minmax(0,43fr) minmax(0,57fr);gap:0 16px;padding:14px 16px}
article.q.land .lp{min-width:0}
article.q.land .rp{min-width:0}
.lt{font-size:17px;font-weight:800;margin:0 0 8px;line-height:1.35}
.toidx{float:right;font-size:11px;font-weight:600;color:#6b7280;text-decoration:none;margin-top:3px}
.lt .sj{font-size:13px;font-weight:600;color:var(--c);margin-left:8px}
.card{border:1px solid #cfd4db;border-radius:8px;padding:10px 12px;background:#fff}
.og{display:inline-block;font-size:11.5px;font-weight:700;color:#fff;background:#4b5563;border-radius:5px;padding:0 7px;margin-right:6px}
.ogl{font-size:12px;color:var(--muted)}
.qimg{display:block;max-width:100%;height:auto;margin:8px 0 4px}
.fg{border-top:1.5px dashed #cfd4db;margin-top:10px;padding-top:8px}
.fgl{font-size:12px;color:var(--muted);margin-bottom:4px}
.lp figure{margin:6px 0 10px}
.lp figure svg{width:100%;height:auto}
article.q.land .rp .keep h3.unit-h{display:none}
article.q.land .rp .q-head h4{font-size:17px}
@media screen and (max-width:1000px){article.q.land{display:block}}
@media print{
  @page{size:A4 landscape;margin:10mm 11mm 12mm}
  body{font-size:9.2pt;line-height:1.5;background:#fff}
  .cover,.ut,.yt{display:none!important}
  article.q.land{break-before:page;page-break-before:always;border:none;padding:0;margin:0;break-inside:auto;page-break-inside:auto}
  .unit-sec,.year-sec{break-before:auto;page-break-before:auto;margin:0}
  .unit-sec:first-child article.q:first-child,.year-sec:first-child article.q:first-child{break-before:auto;page-break-before:auto}
  .keep{break-inside:auto;page-break-inside:auto}
  .lt{font-size:13.5pt}
  article.q.land .rp .q-head h4{font-size:12pt}
  .card{border:.8pt solid #9aa3ad}
  .qimg{width:var(--pw);max-width:100%}
  .lp figure,.rp figure{break-inside:avoid}
  .faq,.answer,.stem{break-inside:avoid}
}
@page{@bottom-center{content:none}}
"""

FOOT = '<div style="font-size:8pt;color:#666;width:100%;text-align:center">- <span class="pageNumber"></span> -</div>'
MARGIN = {"top": "10mm", "bottom": "12mm", "left": "11mm", "right": "11mm"}


def esc(t):
    return html.escape(str(t), quote=True)


def exam_title(it):
    ex = re.sub(r"전공([AB]) ", r"\1형 ", it["exam"])
    return f'{it["year"]} {ex}'


def restructure(h, units):
    """각 article을 [왼쪽: 기출 원문 + 풀이 그림] [오른쪽: 본문] 두 칸으로 재배치"""
    for u in units:
        for it in u["items"]:
            aid = it["_aid"]
            st = h.index(f'id="{aid}"')
            a0 = h.rindex("<article", 0, st)
            a1 = h.index("</article>", st) + len("</article>")
            art = h[a0:a1]
            open_tag = art[:art.index(">") + 1].replace('class="q"', 'class="q land"', 1)
            body = art[len(art[:art.index(">") + 1]):-len("</article>")]
            figs = re.findall(r"<figure>.*?</figure>", body, flags=re.S)
            for fg in figs:
                body = body.replace(fg, "", 1)
            img = it["_img"]
            src = "data:image/png;base64," + base64.b64encode(img["png"]).decode()
            title = exam_title(it)
            pg = f' · 교재 {img["page"]}쪽' if img.get("page") else ""
            left = (f'<div class="lp" style="--c:{C}"><div class="lt"><a class="toidx" href="#">▲ 색인</a>{esc(title)}<span class="sj">유기화학 · {esc(build.unit_label(u))}</span></div>'
                    f'<div class="card"><span class="og">기출 원문</span><span class="ogl">{esc(img.get("year") or it["year"])}'
                    f'{pg}</span>'
                    f'<img class="qimg" src="{src}" width="{round(img["w"] * 0.9)}" style="--pw:{round(img["w"] * 0.64)}px" alt="기출 원문">'
                    + (f'<div class="fg"><div class="fgl">풀이 그림</div>{"".join(figs)}</div>' if figs else "")
                    + "</div></div>")
            new = f'{open_tag}{left}<div class="rp">{body}</div></article>'
            h = h[:a0] + new + h[a1:]
    return h


def start_pages(pdf, n):
    import pymupdf as fitz
    d = fitz.open(pdf)
    starts = [i + 1 for i in range(d.page_count) if "기출 원문" in d[i].get_text()]
    total = d.page_count
    d.close()
    assert len(starts) == n, (len(starts), n)
    return starts, total


INDEX_CSS = """
@page{size:A4 landscape;margin:12mm 12mm}
body{font-family:'Noto Sans CJK KR','Malgun Gothic',sans-serif;color:#111;margin:0;font-size:8.6pt}
h1{font-size:19pt;margin:0 0 2mm}
.sub{color:#555;font-size:9pt;margin:0 0 4mm}
table{border-collapse:collapse;width:100%}
th,td{border:.5pt solid #c9ced6;padding:1.2mm 1.6mm;vertical-align:top}
th{background:#eef1f5;font-weight:700;white-space:nowrap}
td.n{white-space:nowrap;text-align:center}
td.u{white-space:nowrap;color:#dc2626;font-weight:700}
tr{break-inside:avoid}
thead{display:table-header-group}
"""


def index_pdf(path, title, sub, rows):
    from playwright.sync_api import sync_playwright
    trs = "".join(
        f'<tr><td class="n">{r["year"]}</td><td class="n">{esc(r["exam"])}</td><td class="u">{esc(r["unit"])}</td>'
        f'<td>{esc(r["sub"])}</td><td class="n">{r["pts"]}</td><td>{r["title"]}</td><td class="n">{r["page"]}</td></tr>' for r in rows)
    h = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{INDEX_CSS}</style></head><body>'
         f'<h1>{esc(title)}</h1><p class="sub">{esc(sub)}</p><table><thead><tr><th>연도</th><th>문항</th><th>단원</th><th>세부영역</th>'
         f'<th>배점</th><th>주제</th><th>쪽</th></tr></thead><tbody>{trs}</tbody></table></body></html>')
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = br.new_page()
        pg.set_content(h)
        pg.pdf(path=str(path), prefer_css_page_size=True, print_background=True)
        br.close()


def make(units, arts, css, out_html, out_pdf, title, sub, views=("unit", "year")):
    h = build.build(units, arts, css, title, sub)
    h = h.replace("</style>", LAND_CSS + "</style>", 1)
    h = restructure(h, units)
    out_html.write_text(h, encoding="utf-8")
    seq = [(u, it) for u in units for it in u["items"]]
    n = len(seq)
    for view in views:
        pdf = out_pdf if view == "unit" else out_pdf.with_name(out_pdf.name.replace("(단원순)", "(연도순)"))
        build.to_pdf(out_html, pdf, view=view, footer=FOOT, margin=MARGIN)
        starts, _ = start_pages(pdf, n)
        order = list(range(n)) if view == "unit" else sorted(range(n), key=lambda i: (-seq[i][1]["year"], i))
        rows = []
        for pos, i in enumerate(order):
            u, it = seq[i]
            rows.append({"year": it["year"], "exam": it["exam"], "unit": build.unit_label(u), "sub": it["sub"],
                         "pts": build.pts_num(it["pts"]), "title": it.get("title", ""), "page": starts[pos]})
        ip = pdf.with_name("_index.pdf")
        index_pdf(ip, title, sub + (" · 연도순" if view == "year" else ""), rows)
        k = fitz.open(ip).page_count
        BP.prepend(ip, pdf)
        # 하이퍼링크: 색인 행 → 문항 쪽, 문항 쪽 '▲ 색인' → 첫 쪽, 책갈피
        targets = [k + p - 1 for p in starts]
        outline, cur = [[1, "색인", 1]], None
        for pos, i in enumerate(order):
            u, it = seq[i]
            grp = build.unit_label(u) if view == "unit" else f'{it["year"]}학년도'
            if grp != cur:
                outline.append([1, grp, targets[pos] + 1])
                cur = grp
            outline.append([2, f'{it["year"]} {it["exam"]} · {pdflinks.plain(it.get("title", ""))}'[:120], targets[pos] + 1])
        pdflinks.finalize(pdf, k, index_targets=targets, outline=outline)


if __name__ == "__main__":
    model, outdir, rest = sys.argv[1], pathlib.Path(sys.argv[2]), [a for a in sys.argv[3:] if not a.startswith("--")]
    exams = BP.exam_map(rest)
    book = [p for p in rest if p not in exams.values()]
    css, arts = build.load_model(model)
    units = BB.load_units(arts)
    BB.attach_images(units, book, exams)
    outdir.mkdir(parents=True, exist_ok=True)
    yr = [a for a in sys.argv if a.startswith("--years=")]
    if yr:  # 연도 범위만 모은 모범답안 (예: --years=2009-2013)
        y0, y1 = map(int, yr[0].split("=")[1].split("-"))
        sel = []
        for u in units:
            its = [it for it in u["items"] if y0 <= it["year"] <= y1]
            if its:
                sel.append({**u, "items": its})
        n = sum(len(u["items"]) for u in sel)
        make(sel, arts, css, outdir / f"유기화학_모범답안_{y0}-{y1}.html", outdir / f"유기화학_모범답안_{y0}-{y1}(단원순).pdf",
             f"유기화학 기출 모범답안 ({y0}–{y1}학년도)", f"중등 화학 교사 임용시험 · {y0}–{y1}학년도 · {n}문항 · 단원 → 문항(최근 연도 순)")
        print(n, "문항")
        sys.exit(0)
    n = sum(len(u["items"]) for u in units)
    sub = f"중등 화학 교사 임용시험 1차 · 1997–2026학년도 · {n}문항 · 단원 → 문항(최근 연도 순)"
    make(units, arts, css, outdir / "유기화학_단원별_모범답안_합본.html", outdir / "유기화학_단원별_모범답안_합본(단원순).pdf",
         "중등 화학 임용 유기화학 기출 모범답안", sub)
    for u in units:
        if True:
            name = f'유기화학_{u["no"]:02d}_{u["name"].replace(" ", "").replace("–", "-")}'
            make([u], arts, css, outdir / f"{name}.html", outdir / f"{name}.pdf",
                 f"유기화학 기출 모범답안 — {build.unit_label(u)}", f"중등 화학 교사 임용시험 1차 · {len(u['items'])}문항", views=("unit",))
    print(n, "문항")
