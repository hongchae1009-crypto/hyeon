"""유기화학 단원별 기출문제집 (문제만) HTML/PDF 빌더.

사용: python3 build_problems.py <모범답안.html> <출력 폴더> <교재 PDF ...>
  - 교재 문항: PDF 쪽에서 문항 영역을 잘라 이미지로 수록
  - 2025·2026 문항: problems_2526.ITEMS (재구성, 정답 미포함)
"""
import base64
import re
import html
import pathlib
import sys

import build
import pdflinks
import pymupdf as fitz
import extract_pages
import problems_2526

C = "#dc2626"
UNIT_NAMES = {
    1: "결합과 구조", 2: "산과 염기", 3: "알케인과 사이클로알케인", 4: "입체화학",
    5: "할로젠화 알킬의 친핵성 치환반응", 6: "할로젠화 알킬의 제거 반응", 7: "알켄", 8: "알카인",
    9: "알코올", 10: "에터와 에폭사이드", 11: "벤젠과 방향족성", 12: "방향족 화합물의 반응",
    13: "알데하이드와 케톤", 14: "카복실산과 그 유도체", 15: "카보닐 화합물의 α탄소 치환반응",
    16: "카보닐 화합물의 축합반응", 17: "아민", 18: "고리형 협동반응", 19: "C–C 결합형성반응",
    20: "유기화학실험", 21: "유기 분광",
}

FOOT = '<div style="font-size:9pt;color:#000;width:100%;text-align:center;font-family:serif">- <span class="pageNumber"></span> -</div>'

CSS = """
article.q .pimg{display:block;margin:6px auto 0;max-width:100%;height:auto}
article.q.new .ask{margin:8px 0 2px;font-weight:600}
.recon{font-size:12px;color:#7c5c00;background:#fff8e6;border:1px solid #f0c36d;border-radius:6px;padding:1px 8px;margin-left:4px}
.badge.new{background:#7c3aed}
.notes li{margin:3px 0}
.ph{display:none}
.phw .toidx{display:none}
@media print{
  body{background:#fff}
  .cover,.q-head,.ut,.yt,.work{display:none!important}
  article.q{break-inside:avoid;page-break-inside:avoid;break-before:page;page-break-before:always;border:none;padding:0;margin:0;background:none}
  .unit-sec:first-child article.q:first-child,.year-sec:first-child article.q:first-child{break-before:auto;page-break-before:auto}
  .unit-sec,.year-sec{break-before:auto;page-break-before:auto;margin:0}
  .phw{display:flex;justify-content:space-between;align-items:flex-start}
  .phw .toidx{display:inline;font-size:8.5pt;color:#666;text-decoration:none;font-family:'Noto Sans CJK KR',sans-serif}
  .ph{display:flex;width:264pt;border:.8pt solid #000;font-family:'Noto Sans CJK KR','Malgun Gothic',sans-serif;font-size:11.5pt;line-height:1.25;color:#000;margin:0 0 8pt}
  .ph .y{flex:none;width:58pt;text-align:center;border-right:.8pt solid #000;padding:0 4pt}
  .ph .u{padding:0 8pt}
  article.q .pimg{width:var(--pw);height:auto;margin:0}
}
@page{@bottom-center{content:none}}
"""


def esc(t):
    return html.escape(t, quote=True)


def year_num(y):
    return int(str(y)[:4])


# 교재 머리글 연도 오기 바로잡기 (단원, 교재 쪽) → 실제 연도 (모범답안과 같은 판단)
YEAR_FIX = {(3, 14): "2015 A", (9, 47): "2013"}


def exam_map(paths):
    """'2025 … A.pdf' → {(2025, 'A'): path}"""
    out = {}
    for p in paths:
        m = re.search(r"(2025|2026).*?([AB])\.pdf$", p)
        if m:
            out[(int(m.group(1)), m.group(2))] = p
    return out


def collect(pdfs, exams):
    units = {n: [] for n in UNIT_NAMES}
    for it in problems_2526.ITEMS:  # 최근 문항이 단원 맨 앞
        ab, page, q = it["src"]
        path = exams.get((it["year"], ab))
        if path:  # 원본 시험지에서 잘라 넣기
            units[it["unit"]].append({"kind": "exam", **it, **extract_pages.extract_exam_question(path, page, q)})
        else:
            units[it["unit"]].append({"kind": "new", **it})
    for b in extract_pages.extract(pdfs):
        b["year"] = YEAR_FIX.get((b["unit"], b["page"]), b["year"])
        units[b["unit"]].append({"kind": "book", **b})
    for n in units:  # 2025·2026 문항끼리는 연도 내림차순
        new = sorted([x for x in units[n] if x["kind"] != "book"], key=lambda x: -x["year"])
        units[n] = new + [x for x in units[n] if x["kind"] == "book"]
    return units


def render_item(n, k, it):
    uid = f"p{n:02d}-{k:02d}"
    ulab = f"{n}. {UNIT_NAMES[n]}"
    if it["kind"] == "exam":
        src = "data:image/png;base64," + base64.b64encode(it["png"]).decode()
        body = f'<img class="pimg" src="{src}" width="{round(it["w"] * 0.9)}" style="--pw:{round(it["w"] * 0.64)}px" alt="{it["year"]} {esc(it["exam"])}">'
        badges = (f'<span class="badge new">{it["year"]}</span><span class="badge b2">{esc(it["exam"])}</span>'
                  f'<span class="badge b3">{esc(ulab)}</span><span class="pts">[{it["pts"]}점] · 시험지 원본</span>')
        search = f'{it["year"]} {it["exam"]} {ulab} {it["stem"]}'
        cls = "q"
    elif it["kind"] == "book":
        src = "data:image/png;base64," + base64.b64encode(it["png"]).decode()
        w = round(it["w"] * 0.9)
        body = f'<img class="pimg" src="{src}" width="{w}" style="--pw:{round(it["w"] * 0.64)}px" alt="{esc(it["year"])} 기출 문항">'
        badges = (f'<span class="badge">{esc(str(it["year"]))}</span><span class="badge b3">{esc(ulab)}</span>'
                  f'<span class="pts">교재 {it["page"]}쪽</span>')
        search = f'{it["year"]} {ulab}'
        cls = "q"
    else:
        body = (f'<div class="stem">{it["stem"]}</div><figure>{it["fig"]()}</figure>'
                f'<p class="ask">{it["ask"]} [{it["pts"]}점]</p>')
        badges = (f'<span class="badge new">{it["year"]}</span><span class="badge b2">{esc(it["exam"])}</span>'
                  f'<span class="badge b3">{esc(ulab)}</span><span class="recon">재구성 문항</span>')
        search = f'{it["year"]} {it["exam"]} {ulab} {it["stem"]} {it["ask"]}'
        cls = "q new"
    ylab = str(it["year"]) if it["kind"] == "book" else f'{it["year"]} {it["src"][0]}'
    ph = (f'<div class="phw"><div class="ph"><span class="y">{esc(ylab)}</span><span class="u">{esc(ulab)}</span></div>'
          f'<a class="toidx" href="#">▲ 색인</a></div>')
    return (f'<article class="{cls}" id="{uid}" data-subject="유기화학" data-year="{year_num(it["year"])}" data-unit="{n}" '
            f'data-search="{esc(search)}"><div class="keep">{ph}<div class="q-head" style="--c:{C}">{badges}</div>{body}</div></article>'), uid


def build_html(units, css, title="유기화학 단원별 기출문제", sub="중등 화학 임용 · 1997–2026학년도"):
    secs, toc_u, rows, nav_years = [], [], [], {}
    total = 0
    for n, items in units.items():
        if not items:
            continue
        parts = []
        for k, it in enumerate(items):
            h, uid = render_item(n, k, it)
            if k == 0:
                h = h.replace('<div class="keep">', f'<div class="keep"><h2 class="ut">{esc(f"{n}. {UNIT_NAMES[n]}")}<small>{len(items)}문항</small></h2>', 1)
            parts.append(h)
            label = f'{it["year"]}' + (f' · 교재 {it["page"]}쪽' if it["kind"] == "book" else f' · {it["exam"]}')
            rows.append((n, it, uid, label))
            nav_years.setdefault(year_num(it["year"]), []).append((n, uid, label))
        total += len(items)
        secs.append(f'<section class="unit-sec" id="u{n}" style="--c:{C}">' + "".join(parts) + "</section>")
        links = "".join(f'<div class="tq"><a href="#{uid}">{esc(lab)}</a></div>' for (nn, it, uid, lab) in rows if nn == n)
        toc_u.append(f'<details><summary><a href="#u{n}">{n}. {esc(UNIT_NAMES[n])} ({len(items)})</a></summary>{links}</details>')
    toc_y = []
    for y in sorted(nav_years, reverse=True):
        links = "".join(f'<div class="tq"><a href="#{uid}-y">{n}. {esc(UNIT_NAMES[n])} · {esc(lab)}</a></div>' for n, uid, lab in nav_years[y])
        toc_y.append(f'<details><summary><a href="#yr{y}">{y}학년도</a></summary>{links}</details>')
    # 단원별 문항 수 표
    cnt = "".join(f'<tr><td>{n}</td><td class="l"><a href="#u{n}">{esc(UNIT_NAMES[n])}</a></td><td>{len(units[n])}</td>'
                  f'<td class="l">{esc(", ".join(sorted({str(year_num(x["year"])) for x in units[n]}, reverse=True)))}</td></tr>'
                  for n in units if units[n])
    idx = f'<table class="tb idx idx2"><caption>단원별 문항 수</caption><tr><th>단원</th><th>단원명</th><th>문항</th><th>출제 연도</th></tr>{cnt}</table>'
    chips_u = '<span class="chip on" data-u="전체">전체</span>' + "".join(
        f'<span class="chip" data-u="{n}">{n}</span>' for n in units if units[n])
    nav = (f'<nav class="side"><h1>{title}</h1><div class="sub">{sub} · {total}문항</div>'
           '<div class="view-chips"><span class="chip on" data-v="unit">단원별 보기</span><span class="chip" data-v="year">연도별 보기</span></div>'
           f'<input id="q" placeholder="검색 (예: 2025, 아민)"><div class="chips">{chips_u}</div>'
           f'<div class="toc"><div class="toc-unit">{"".join(toc_u)}</div><div class="toc-year">{"".join(toc_y)}</div></div></nav>')
    cover = (f'<div class="cover"><h1>{title}</h1><p>{sub} · {total}문항 · 단원 → 문항(최근 연도 순) · <b>정답·풀이 미포함</b></p>'
             '<ul class="notes">'
             '<li>2024학년도까지: 교재(유기화학 기출문제, 단원별)의 문항을 원본 그대로 수록. 교재에 같은 쪽이 중복된 경우 한 번만 수록.</li>'
             '<li><b>2025·2026학년도 10문항</b>: 2025·2026학년도 1차 시험지(전공A·B) 원본에서 문항을 잘라 수록. 배지 <span class="badge new">2025</span> 로 표시.</li>'
             '<li>15단원: 교재 90–91쪽은 원본 파일이 빈 쪽이라 해당 쪽 문항이 빠져 있을 수 있음.</li>'
             '<li>모범답안은 같은 폴더의 「유기화학 단원별 기출 모범답안」 파일 참고.</li>'
             '<li>PDF·인쇄: <b>한 문항당 한 페이지</b>, 왼쪽 위 머리글 상자(연도 | 단원), 문항 아래는 풀이 공간, 아래 가운데 쪽 번호.</li><li class="noprint">왼쪽에서 단원별 / 연도별 보기를 바꾸거나 검색할 수 있습니다.</li></ul>'
             f'{idx}</div>')
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title><style>{css}{build.EXTRA_CSS}{CSS}</style></head><body><div class="layout">{nav}<main>{cover}'
            f'<div id="unitview">{"".join(secs)}</div><div id="yearview"></div></main></div>{build.SCRIPT}</body></html>'), total


TOC_CSS = """
@page{size:A4;margin:18mm 20mm}
body{font-family:'Noto Sans CJK KR','Malgun Gothic',sans-serif;color:#000;margin:0}
h1{font-size:19pt;margin:6mm 0 1mm;letter-spacing:.5pt}
.sub{font-size:9.5pt;color:#444;margin:0 0 7mm}
h2{font-size:11pt;margin:0 0 2mm;padding-bottom:1.5mm;border-bottom:.8pt solid #000}
.toc{columns:2;column-gap:12mm;font-size:9.5pt;line-height:1.75}
.row{display:flex;break-inside:avoid}
.row .t{white-space:nowrap}
.row .dots{flex:1;border-bottom:.6pt dotted #888;margin:0 2mm 1.2mm}
.row .p{white-space:nowrap}
.note{font-size:8.5pt;color:#555;margin-top:7mm;line-height:1.6}
"""


def toc_pdf(path, title, sub, heading, rows, note):
    """rows: [(제목, 첫쪽, 끝쪽)] → 쪽 번호 없는 1쪽짜리 목차 PDF"""
    from playwright.sync_api import sync_playwright
    items = "".join(f'<div class="row"><span class="t">{esc(t)}</span><span class="dots"></span>'
                    f'<span class="p">{a}{"" if a == z else f"–{z}"}</span></div>' for t, a, z in rows)
    h = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{TOC_CSS}</style></head><body>'
         f'<h1>{esc(title)}</h1><p class="sub">{esc(sub)}</p><h2>{esc(heading)}</h2><div class="toc">{items}</div>'
         f'<p class="note">{note}</p></body></html>')
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = br.new_page()
        pg.set_content(h)
        pg.pdf(path=str(path), format="A4", prefer_css_page_size=True, print_background=True)
        br.close()


def prepend(toc_path, body_path):
    import pymupdf as fitz
    toc, body = fitz.open(toc_path), fitz.open(body_path)
    toc.insert_pdf(body)
    toc.save(str(body_path) + ".tmp")
    toc.close(); body.close()
    pathlib.Path(str(body_path) + ".tmp").replace(body_path)
    pathlib.Path(toc_path).unlink()


def page_ranges(units):
    """단원순·연도순 PDF에서 각 묶음의 쪽 범위 (한 문항 = 한 쪽)"""
    seq = [(n, it) for n, items in units.items() for it in items]
    by_unit, p = [], 1
    for n, items in units.items():
        if items:
            by_unit.append((f"{n}. {UNIT_NAMES[n]}", p, p + len(items) - 1))
            p += len(items)
    order = sorted(range(len(seq)), key=lambda i: (-year_num(seq[i][1]["year"]), i))
    by_year, cur = [], None
    for page, i in enumerate(order, 1):
        y = year_num(seq[i][1]["year"])
        if y != cur:
            by_year.append([f"{y}학년도", page, page])
            cur = y
        else:
            by_year[-1][2] = page
    return by_unit, [tuple(r) for r in by_year]


def make_combined(units, css, outdir, base, title, sub, note):
    """단원순·연도순 합본 HTML/PDF (목차·하이퍼링크·책갈피 포함)"""
    h, total = build_html(units, css, title, sub.split(" · ")[0] + " · " + sub.split(" · ")[1] if " · " in sub else sub)
    outdir.mkdir(parents=True, exist_ok=True)
    hp = outdir / f"{base}.html"
    hp.write_text(h, encoding="utf-8")
    build.to_pdf(hp, outdir / f"{base}(단원순).pdf", footer=FOOT, margin={"top": "14mm", "bottom": "18mm", "left": "14mm", "right": "14mm"})
    build.to_pdf(hp, outdir / f"{base}(연도순).pdf", view="year", footer=FOOT, margin={"top": "14mm", "bottom": "18mm", "left": "14mm", "right": "14mm"})
    by_unit, by_year = page_ranges(units)
    for kind, rows, heading in (("단원순", by_unit, "목차 (단원별)"), ("연도순", by_year, "목차 (연도별)")):
        pdf = outdir / f"{base}({kind}).pdf"
        tp = outdir / f"_toc_{kind}.pdf"
        toc_pdf(tp, title, sub, heading, rows, note)
        k = fitz.open(tp).page_count
        prepend(tp, pdf)
        seq = [(n, it) for n, its in units.items() for it in its]
        order = list(range(len(seq))) if kind == "단원순" else sorted(range(len(seq)), key=lambda i: (-year_num(seq[i][1]["year"]), i))
        outline, cur = [[1, "목차", 1]], None
        for pos, i in enumerate(order):
            n, it = seq[i]
            grp = f"{n}. {UNIT_NAMES[n]}" if kind == "단원순" else f'{year_num(it["year"])}학년도'
            if grp != cur:
                outline.append([1, grp, k + pos + 1])
                cur = grp
            lab = f'{it["year"]} · 교재 {it["page"]}쪽' if it["kind"] == "book" else f'{it["year"]} {it["exam"]}'
            outline.append([2, lab if kind == "단원순" else f"{lab} · {n}. {UNIT_NAMES[n]}", k + pos + 1])
        pdflinks.finalize(pdf, k, toc_rows=[(t, k + a - 1) for t, a, z in rows], outline=outline)
    return h, total


if __name__ == "__main__":
    model, outdir, rest = sys.argv[1], pathlib.Path(sys.argv[2]), [a for a in sys.argv[3:] if not a.startswith('--')]
    exams = exam_map(rest)
    pdfs = [p for p in rest if p not in exams.values()]
    css, _ = build.load_model(model)
    units = collect(pdfs, exams)
    print("시험지 원본:", sorted(exams))
    note = ("· 2024학년도까지는 단원별 기출 교재의 문항, 2025·2026학년도는 시험지 원본에서 수록했습니다.<br>"
            "· 한 문항당 한 페이지이며, 문항 아래 빈 공간은 풀이 공간입니다.<br>"
            "· 15단원은 교재 90–91쪽이 원본 파일에서 빈 쪽이라 해당 문항이 빠져 있을 수 있습니다.")
    yr = [a for a in sys.argv if a.startswith("--years=")]
    if yr:  # 연도 범위만 모은 합본 (예: --years=2009-2013)
        y0, y1 = map(int, yr[0].split("=")[1].split("-"))
        sel = {n: [it for it in its if y0 <= year_num(it["year"]) <= y1] for n, its in units.items()}
        total = sum(len(v) for v in sel.values())
        outdir.mkdir(parents=True, exist_ok=True)
        make_combined(sel, css, outdir, f"유기화학_기출문제_{y0}-{y1}", f"유기화학 기출문제 ({y0}–{y1}학년도)",
                      f"중등 화학 교사 임용시험 · {y0}–{y1}학년도 · {total}문항",
                      "· 단원별 기출 교재의 문항을 원본 그대로 수록했습니다.<br>· 한 문항당 한 페이지이며, 문항 아래 빈 공간은 풀이 공간입니다.")
        print(total, "문항")
        sys.exit(0)
    sub = f"중등 화학 교사 임용시험 1차 · 1997–2026학년도 · {sum(len(v) for v in units.values())}문항"
    outdir.mkdir(parents=True, exist_ok=True)
    h, total = make_combined(units, css, outdir, "유기화학_단원별_기출문제", "유기화학 단원별 기출문제", sub, note)
    # 단원별 파일
    ud = outdir / "단원별"
    ud.mkdir(exist_ok=True)
    for n, items in units.items():
        if not items:
            continue
        one = {k: (v if k == n else []) for k, v in units.items()}
        uh, _ = build_html(one, css)
        name = f"유기화학_기출_{n:02d}_{UNIT_NAMES[n].replace(' ', '').replace('–', '-')}"
        hp1 = ud / f"{name}.html"
        hp1.write_text(uh, encoding="utf-8")
        pdf = ud / f"{name}.pdf"
        build.to_pdf(hp1, pdf, footer=FOOT, margin={"top": "14mm", "bottom": "18mm", "left": "14mm", "right": "14mm"})
        rows = []
        for i, it in enumerate(items, 1):
            lab = f'{it["year"]} · 교재 {it["page"]}쪽' if it["kind"] == "book" else f'{it["year"]} {it["exam"]} (시험지 원본)'
            rows.append((lab, i, i))
        tp = ud / "_toc.pdf"
        toc_pdf(tp, f"유기화학 기출문제 — {n}. {UNIT_NAMES[n]}", f"중등 화학 교사 임용시험 1차 · {len(items)}문항", "문항 목록", rows,
                note if n == 15 else note.rsplit("<br>", 1)[0])
        k = fitz.open(tp).page_count
        prepend(tp, pdf)
        pdflinks.finalize(pdf, k, toc_rows=[(t, k + a - 1) for t, a, z in rows],
                          outline=[[1, "문항 목록", 1]] + [[1, t, k + a] for t, a, z in rows])
    print(total, "문항", round(len(h) / 1e6, 1), "MB")
