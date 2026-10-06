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

CSS = """
article.q .pimg{display:block;margin:6px auto 0;max-width:100%;height:auto}
article.q.new .ask{margin:8px 0 2px;font-weight:600}
.recon{font-size:12px;color:#7c5c00;background:#fff8e6;border:1px solid #f0c36d;border-radius:6px;padding:1px 8px;margin-left:4px}
.badge.new{background:#7c3aed}
.notes li{margin:3px 0}
@media print{ .pimg{width:94%;height:auto;max-height:238mm;object-fit:contain;object-position:top} article.q{break-inside:avoid;page-break-inside:avoid;break-before:page;page-break-before:always;border-bottom:none} }
"""


def esc(t):
    return html.escape(t, quote=True)


def year_num(y):
    return int(str(y)[:4])


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
        body = f'<img class="pimg" src="{src}" width="{round(it["w"] * 0.9)}" alt="{it["year"]} {esc(it["exam"])}">'
        badges = (f'<span class="badge new">{it["year"]}</span><span class="badge b2">{esc(it["exam"])}</span>'
                  f'<span class="badge b3">{esc(ulab)}</span><span class="pts">[{it["pts"]}점] · 시험지 원본</span>')
        search = f'{it["year"]} {it["exam"]} {ulab} {it["stem"]}'
        cls = "q"
    elif it["kind"] == "book":
        src = "data:image/png;base64," + base64.b64encode(it["png"]).decode()
        w = round(it["w"] * 0.9)
        body = f'<img class="pimg" src="{src}" width="{w}" alt="{esc(it["year"])} 기출 문항">'
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
    return (f'<article class="{cls}" id="{uid}" data-subject="유기화학" data-year="{year_num(it["year"])}" data-unit="{n}" '
            f'data-search="{esc(search)}"><div class="keep"><div class="q-head" style="--c:{C}">{badges}</div>{body}</div></article>'), uid


def build_html(units, css):
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
    title = "유기화학 단원별 기출문제"
    sub = "중등 화학 임용 · 1997–2026학년도"
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
             '<li>PDF·인쇄: <b>한 문항당 한 페이지</b> (단원·연도 제목은 그 단원의 첫 문항 페이지 맨 위).</li><li class="noprint">왼쪽에서 단원별 / 연도별 보기를 바꾸거나 검색할 수 있습니다.</li></ul>'
             f'{idx}</div>')
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title><style>{css}{build.EXTRA_CSS}{CSS}</style></head><body><div class="layout">{nav}<main>{cover}'
            f'<div id="unitview">{"".join(secs)}</div><div id="yearview"></div></main></div>{build.SCRIPT}</body></html>'), total


if __name__ == "__main__":
    model, outdir, rest = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3:]
    exams = exam_map(rest)
    pdfs = [p for p in rest if p not in exams.values()]
    css, _ = build.load_model(model)
    units = collect(pdfs, exams)
    print("시험지 원본:", sorted(exams))
    h, total = build_html(units, css)
    outdir.mkdir(parents=True, exist_ok=True)
    hp = outdir / "유기화학_단원별_기출문제.html"
    hp.write_text(h, encoding="utf-8")
    build.to_pdf(hp, outdir / "유기화학_단원별_기출문제(단원순).pdf")
    build.to_pdf(hp, outdir / "유기화학_단원별_기출문제(연도순).pdf", view="year")
    print(total, "문항", round(len(h) / 1e6, 1), "MB")
