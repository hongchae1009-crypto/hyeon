"""유기화학 단원별 기출 모범답안 HTML/PDF 빌더.

사용: python3 build.py <모범답안.html> <출력 폴더> <content 모듈명> [...]
  - 기존 모범답안 파일의 CSS와 이미 작성된 문항(article)을 재사용한다.
  - 단원별 파일 + 전체 합본을 HTML과 PDF로 만든다.
"""
import html
import importlib
import pathlib
import re
import sys

C = "#dc2626"  # 유기화학 색

EXTRA_CSS = """
body{font-family:'Malgun Gothic','Apple SD Gothic Neo','Noto Sans KR','Noto Sans CJK KR',sans-serif}
.ut{font-size:21px;margin:0 0 10px;padding:9px 14px;border-radius:10px;color:#fff;background:var(--c)}
.ut small{font-weight:400;opacity:.85;font-size:14px;margin-left:8px}
.yt{font-size:21px;margin:0 0 10px;padding:6px 0;border-bottom:3px solid var(--ink)}
.unit-sec,.year-sec{margin-top:30px}
.badge.b3{background:#fff;color:#374151;border:1px solid #cbd5e1}
.view-chips{display:flex;gap:6px;margin-bottom:10px}
.toc .tq{margin-left:10px;font-size:12.5px;color:var(--muted)}
#yearview{display:none}
body.yv #unitview{display:none} body.yv #yearview{display:block}
body.yv .toc-unit{display:none} .toc-year{display:none} body.yv .toc-year{display:block}
.idx2 caption{font-weight:700;text-align:left;margin:14px 0 4px}
.fig-note{font-size:12px;color:var(--muted)}
figure svg{background:#fff}
@media print{
  .unit-sec,.year-sec{break-before:page;page-break-before:always;margin-top:0}
  .ut,.yt{break-after:avoid;page-break-after:avoid}
  .year-h{display:block}
  figure svg{max-height:235mm}
}
"""

SCRIPT = """
<script>
(function(){
 const B=document.body, inp=document.getElementById('q');
 let unit='전체';
 // 연도별 보기: 문항을 복제하여 연도 순으로 재배치
 const yv=document.getElementById('yearview');
 const arts=[...document.querySelectorAll('#unitview article.q')];
 const sorted=arts.map((a,i)=>[a,i]).sort((x,y)=>(+y[0].dataset.year)-(+x[0].dataset.year)||x[1]-y[1]).map(x=>x[0]);
 let cur=null, sec=null;
 sorted.forEach(a=>{
   const c=a.cloneNode(true); c.id=a.id+'-y';
   c.querySelectorAll('.ut').forEach(e=>e.remove());
   if(a.dataset.year!==cur){cur=a.dataset.year; sec=document.createElement('section'); sec.className='year-sec'; sec.id='yr'+cur; yv.appendChild(sec);
     const h=document.createElement('h2'); h.className='yt'; h.textContent=cur+'학년도';
     const k=c.querySelector('.keep'); (k||c).insertBefore(h,(k||c).firstChild);}
   sec.appendChild(c);
 });
 function apply(){const t=(inp.value||'').trim().toLowerCase();
  document.querySelectorAll('article.q').forEach(a=>{const ok=(unit==='전체'||a.dataset.unit===unit)&&(!t||a.dataset.search.toLowerCase().includes(t)||a.textContent.toLowerCase().includes(t));a.classList.toggle('hidden',!ok)});
  document.querySelectorAll('.unit-sec,.year-sec').forEach(b=>b.classList.toggle('hidden',!b.querySelector('article.q:not(.hidden)')));
 }
 inp.addEventListener('input',apply);
 document.querySelectorAll('.chip[data-u]').forEach(c=>c.addEventListener('click',()=>{document.querySelectorAll('.chip[data-u]').forEach(x=>x.classList.remove('on'));c.classList.add('on');unit=c.dataset.u;apply();}));
 document.querySelectorAll('.chip[data-v]').forEach(c=>c.addEventListener('click',()=>{document.querySelectorAll('.chip[data-v]').forEach(x=>x.classList.remove('on'));c.classList.add('on');B.classList.toggle('yv',c.dataset.v==='year');window.scrollTo(0,0);}));
 if(location.hash==='#year'||new URLSearchParams(location.search).get('view')==='year'){document.querySelector('.chip[data-v=year]').click();}
})();
</script>
"""


def esc(t):
    return html.escape(t, quote=True)


def strip_tags(s):
    return re.sub(r"<[^>]+>", " ", s)


def load_model(path):
    s = pathlib.Path(path).read_text(encoding="utf-8")
    css = s[s.index("<style>") + 7:s.index("</style>")]
    arts = {}
    for m in re.finditer(r'<article class="q" id="([^"]+)"', s):
        st = m.start()
        arts[m.group(1)] = s[st:s.index("</article>", st) + 10]
    return css, arts


def pts_txt(p):
    if p is None:
        return ""
    return f"[{p:g}점]"


def pts_num(p):
    return "" if p is None else f"{p:g}"


def unit_label(u):
    return f"{u['no']}. {u['name']}"


def render_new(it, u):
    figs = "".join(
        f"<figure>{fn()}<figcaption>{esc(cap)}</figcaption></figure>" for fn, cap in it["figs"])
    faq = "".join(f'<div class="faq"><p class="fq"><b>Q.</b> {q}</p><p class="fa"><b>A.</b> {a}</p></div>' for q, a in it["faq"])
    concepts = "".join(f"<li>{c}</li>" for c in it["concepts"])
    search = esc(strip_tags(f"{it['title']} {it['stem']} {it['sub']} {unit_label(u)}"))
    return (
        f'<article class="q" id="{it["id"]}" data-subject="유기화학" data-year="{it["year"]}" data-unit="{u["no"]}" data-search="{search}">'
        f'<div class="keep"><h3 class="unit-h">{esc(it["sub"])}</h3>'
        f'<div class="q-head" style="--c:{C}"><span class="badge">{it["year"]}</span><span class="badge b2">{esc(it["exam"])}</span>'
        f'<span class="badge b3">{esc(unit_label(u))}</span><span class="pts">{pts_txt(it["pts"])}</span><h4>{it["title"]}</h4></div>'
        f'<div class="stem"><span class="lbl">문제 요지</span>{it["stem"]}</div>'
        f'<div class="answer"><span class="lbl">모범답안</span>{it["answer"]}</div></div>'
        f'<section class="blk"><h5>핵심 개념 · 공식</h5><ul class="concepts">{concepts}</ul></section>'
        f'<section class="blk"><h5>풀이 과정 · 메커니즘</h5><div class="sol">{it["sol"]}</div></section>'
        f'{figs}<section class="blk"><h5>예상 의문점 Q&amp;A</h5>{faq}</section></article>')


def render_reuse(it, u, arts):
    a = arts[it["reuse"]]
    # 단원 배지와 data-unit 추가
    a = a.replace('<article class="q" ', f'<article class="q" data-unit="{u["no"]}" ', 1)
    a = re.sub(r'(<span class="badge b2">[^<]*</span>)', r'\1' + f'<span class="badge b3">{esc(unit_label(u))}</span>', a, count=1)
    # 기존 파일의 title(h4)을 목차용으로 추출
    it.setdefault("title", re.search(r"<h4>(.*?)</h4>", a).group(1))
    it.setdefault("sub_orig", re.search(r'<h3 class="unit-h">(.*?)</h3>', a).group(1))
    return a


def insert_unit_title(article_html, u, n):
    t = f'<h2 class="ut">{esc(unit_label(u))}<small>{n}문항</small></h2>'
    return article_html.replace('<div class="keep">', '<div class="keep">' + t, 1)


def build(units, arts, css, title, sub):
    body_units, toc_u, rows = [], [], []
    for u in units:
        parts = []
        for i, it in enumerate(u["items"]):
            h = render_reuse(it, u, arts) if "reuse" in it else render_new(it, u)
            if i == 0:
                h = insert_unit_title(h, u, len(u["items"]))
            parts.append(h)
            aid = it.get("reuse") or it["id"]
            it["_aid"] = aid
            rows.append((u, it))
        body_units.append(f'<section class="unit-sec" id="u{u["no"]}" style="--c:{C}">' + "".join(parts) + "</section>")
        links = "".join(f'<div class="tq"><a href="#{it["_aid"]}">{it["year"]} · {esc(it["exam"])}</a></div>' for it in u["items"])
        toc_u.append(f'<details open><summary><a href="#u{u["no"]}">{esc(unit_label(u))} ({len(u["items"])})</a></summary>{links}</details>')
    # 연도별 목차
    years = {}
    for u, it in rows:
        years.setdefault(it["year"], []).append((u, it))
    toc_y = []
    for y in sorted(years, reverse=True):
        links = "".join(f'<div class="tq"><a href="#{it["_aid"]}-y">{esc(unit_label(u))} · {esc(it["exam"])}</a></div>' for u, it in years[y])
        toc_y.append(f'<details open><summary><a href="#yr{y}">{y}학년도</a></summary>{links}</details>')

    def row(u, it, suffix=""):
        return (f'<tr><td>{it["year"]}</td><td style="color:{C};font-weight:700">{esc(unit_label(u))}</td>'
                f'<td>{esc(it["sub"])}</td><td>{esc(it["exam"])}</td><td>{pts_num(it["pts"])}</td>'
                f'<td class="l"><a href="#{it["_aid"]}{suffix}">{it["title"]}</a></td></tr>')
    head = "<tr><th>연도</th><th>단원</th><th>세부영역</th><th>문항</th><th>배점</th><th>주제</th></tr>"
    idx_u = f'<table class="tb idx idx2"><caption>단원별 색인</caption>{head}' + "".join(row(u, it) for u, it in rows) + "</table>"
    ys = sorted(rows, key=lambda r: -r[1]["year"])
    idx_y = f'<table class="tb idx idx2"><caption>연도별 색인</caption>{head}' + "".join(row(u, it) for u, it in ys) + "</table>"
    chips_u = '<span class="chip on" data-u="전체">전체</span>' + "".join(
        f'<span class="chip" data-u="{u["no"]}">{u["no"]}. {esc(u["name"])}</span>' for u in units)
    n = len(rows)
    nav = (f'<nav class="side"><h1>{esc(title)}</h1><div class="sub">{esc(sub)} · {n}문항</div>'
           f'<div class="view-chips"><span class="chip on" data-v="unit">단원별 보기</span><span class="chip" data-v="year">연도별 보기</span></div>'
           f'<input id="q" placeholder="검색 (예: endo, Heck, 다이아조늄)"><div class="chips">{chips_u}</div>'
           f'<div class="toc"><div class="toc-unit">{"".join(toc_u)}</div><div class="toc-year">{"".join(toc_y)}</div></div></nav>')
    cover = (f'<div class="cover"><h1>{esc(title)}</h1><p>{esc(sub)} · {n}문항 · 단원 → 문항(최근 연도 순)</p>'
             '<p>각 문항: 문제 요지 → <b>모범답안</b> → 핵심 개념·공식 → 풀이 과정·메커니즘(계산 포함) → 구조식·도식 그림 → 예상 의문점 Q&amp;A</p>'
             '<p class="noprint">왼쪽에서 <b>단원별 / 연도별 보기</b>를 바꾸거나 단원 필터·검색을 사용하세요. 인쇄(Ctrl+P) 시 단원(또는 연도)마다 새 페이지에서 시작하며, 단원 제목은 첫 문항과 같은 페이지에 놓입니다.</p>'
             f'{idx_u}{idx_y}</div>')
    return ('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(title)}</title><style>{css}{EXTRA_CSS}</style></head><body><div class="layout">{nav}<main>{cover}'
            f'<div id="unitview">{"".join(body_units)}</div><div id="yearview"></div></main></div>{SCRIPT}</body></html>')


def to_pdf(html_path, pdf_path, view="unit"):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = b.new_page()
        url = pathlib.Path(html_path).resolve().as_uri() + ("?view=year" if view == "year" else "")
        pg.goto(url)
        pg.wait_for_timeout(300)
        pg.emulate_media(media="print")
        pg.pdf(path=str(pdf_path), format="A4", print_background=True, prefer_css_page_size=True,
               display_header_footer=True, header_template="<span></span>",
               footer_template='<div style="font-size:8pt;color:#888;width:100%;text-align:center"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
               margin={"top": "14mm", "bottom": "16mm", "left": "12mm", "right": "12mm"})
        b.close()


if __name__ == "__main__":
    model, outdir = sys.argv[1], pathlib.Path(sys.argv[2])
    mods = sys.argv[3:]
    css, arts = load_model(model)
    outdir.mkdir(parents=True, exist_ok=True)
    all_units = []
    for mn in mods:
        all_units += importlib.import_module(mn).UNITS
    all_units.sort(key=lambda u: u["no"])
    made = []
    # 단원별 파일
    for u in all_units:
        name = f'유기화학_{u["no"]:02d}_{u["name"].replace(" ", "").replace("–", "-")}'
        h = build([u], arts, css, f"유기화학 기출 모범답안 — {unit_label(u)}", "중등 화학 임용 유기화학 단원별 기출")
        hp = outdir / f"{name}.html"
        hp.write_text(h, encoding="utf-8")
        to_pdf(hp, outdir / f"{name}.pdf")
        made.append(name)
    # 합본
    rng = f'{all_units[0]["no"]}-{all_units[-1]["no"]}'
    h = build(all_units, arts, css, "유기화학 단원별 기출 모범답안", f"단원 {rng} 합본")
    hp = outdir / "유기화학_단원별_모범답안_합본.html"
    hp.write_text(h, encoding="utf-8")
    to_pdf(hp, outdir / "유기화학_단원별_모범답안_합본(단원순).pdf")
    to_pdf(hp, outdir / "유기화학_단원별_모범답안_합본(연도순).pdf", view="year")
    print("\n".join(made))
