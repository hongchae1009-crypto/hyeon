"""66문항 변형 모의고사 빌드: items/*.py 의 ITEMS 를 읽어 시험지·해설지 HTML/PDF 생성.

문항 dict 스키마
  set        회차 (1~6)          no      회차 내 번호
  points     2 또는 4            kind    '기입형' | '서술형'
  area       영역 코드(AREAS 키)  stars   중요도 1~3
  src        변형 대상 기출 (예 '2024학년도 A형 3번')  src_topic  기출 원문항 요지
  paper      {'cite': 'J. Org. Chem. 2009, 74, 5458–5470', 'book': 'Klein 13.68', 'what': '논문 반응 요지'}
  nobel      관련 노벨상 문자열 또는 ''
  body       문제 본문 HTML (발문+반응식 상자+요구사항, 배점 포함)
  answer     정답 HTML (구조식 포함 가능)
  explain    해설 HTML
  change     기출 대비 변형 포인트 (문자열)
"""
import glob, importlib.util, html, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from areas import AREAS, SETS, EXAM_ITEMS, allocate

CSS = open(os.path.join(HERE, 'style.css'), encoding='utf-8').read()
PAG = open(os.path.join(HERE, 'paginate.js'), encoding='utf-8').read()


def load_items(files=None):
    items = []
    for f in (files or sorted(glob.glob(os.path.join(HERE, 'items', '*.py')))):
        spec = importlib.util.spec_from_file_location(os.path.basename(f)[:-3], f)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        items.extend(m.ITEMS)
    alloc = allocate(); meta = {k: (p, a) for k, p, a in EXAM_ITEMS}
    seen = set()
    for d in items:
        k = d['key']; assert k in alloc, k; assert k not in seen, 'dup ' + k; seen.add(k)
        d['set'], d['no'] = alloc[k]
        d['points'], d['area'] = meta[k]
        d.setdefault('stars', AREAS[d['area']]['stars'])
        d['kind'] = '기입형' if d['points'] == 2 else '서술형'
        d['body'] = d['body'].replace('[[PTS]]', f'<span class="pts">[{d["points"]}점]</span>')
    missing = [k for k in alloc if k not in seen]
    if missing and not files: print('MISSING', len(missing), missing)
    items.sort(key=lambda d: (d['set'], d['no']))
    return items


def cover(s):
    return f'''<template id="cover-{s['id']}">
<div class="title1">중등학교교사 임용 대비 유기화학 기출변형 모의고사 [{s['id']}회]</div>
<div class="title2">화 학</div>
<div class="idrow"><span>수험 번호 : (<span class="blank w1"></span>)</span><span>성 명 : (<span class="blank w2"></span>)</span></div>
<table class="info"><tr><td>제1차 시험 대비</td><td>{s['label']}</td><td>{s['count']}문항 {s['points']}점</td><td>시험 시간 {s['time']}분</td></tr></table>
<div class="notice">◦ 문제지 전체 면수가 맞는지 확인하시오.<br>◦ 모든 문항에는 배점이 표시되어 있습니다.　◦ 각 문항 아래에 변형 기출·소스 논문이 표시되어 있습니다.</div>
</template>'''


def q_html(d, show_src=True):
    src = ''
    if show_src:
        src = (f'<div class="src">◆ 변형 기출: {d["src"]} · 출처: {d["paper"]["cite"]} ({d["paper"]["book"]})'
               + (f' · 노벨상: {d["nobel"]}' if d.get('nobel') else '') + '</div>')
    return (f'<div class="q" data-set="{d["set"]}"><span class="qn">{d["no"]}.</span>{d["body"]}{src}</div>')


def exam_html(items):
    sets = [dict(s) for s in SETS]
    present = {d['set'] for d in items}
    sets = [s for s in sets if s['id'] in present]
    for s in sets:
        its = [d for d in items if d['set'] == s['id']]
        s['count'] = len(its); s['points'] = sum(d['points'] for d in its)
        s['tag'] = f'유기화학 변형 {s["id"]}회'
    pool = ''.join(q_html(d) for d in items)
    covers = ''.join(cover(s) for s in sets)
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>유기화학 기출변형 모의고사</title><style>{CSS}
@media screen {{ body {{ background:#888; }} .page {{ margin: 8mm auto; background:#fff; box-shadow:0 1px 6px rgba(0,0,0,.4); }} }}
</style></head><body>{covers}<div id="book"></div>
<div id="pool" data-sets='{html.escape(json.dumps(sets, ensure_ascii=False))}' style="position:absolute;left:-9999px;width:85mm">{pool}</div>
<script>{PAG}</script></body></html>'''


ANS_CSS = '''
@page { size: A4; margin: 14mm 15mm 14mm; }
body { font-family: "NanumGothic", sans-serif; font-size: 9.6pt; line-height: 1.65; color:#000; background:#fff; margin:0; }
@media screen { body { max-width: 190mm; margin: 0 auto; padding: 10mm; background:#fff; } }
h1 { font-size: 17pt; text-align:center; margin: 2mm 0 1mm; }
h2 { font-size: 13pt; border-bottom: 2px solid #000; padding-bottom: 1mm; margin: 6mm 0 3mm; page-break-after: avoid; break-before: page; }
h2.nobreak { break-before: auto; }
.sub { text-align:center; color:#333; margin-bottom: 4mm; }
.a { border: 1px solid #000; margin: 0 0 4mm; }
.a .ah, .a .meta { break-after: avoid; break-inside: avoid; }
.a .ans, .a .exp p, .a .ansbox, .a svg { break-inside: avoid; }
.a .ah { display:flex; justify-content:space-between; align-items:center; background:#eee; border-bottom:1px solid #000; padding: 1.2mm 3mm; font-weight:700; }
.a .ah .st { letter-spacing: 1px; }
.a .meta { padding: 1.5mm 3mm; border-bottom: 1px dashed #999; font-size: 8.6pt; }
.a .meta td { padding: .2mm 2mm .2mm 0; vertical-align: top; }
.a .meta td:first-child { white-space: nowrap; font-weight: 700; }
.a .ans { padding: 2mm 3mm; border-bottom: 1px dashed #999; }
.a .ans b.t, .a .exp b.t { display:inline-block; background:#000; color:#fff; padding: 0 2mm; margin-right: 2mm; font-size: 8.4pt; }
.a .exp { padding: 2mm 3mm; }
.a .exp p { margin: 0 0 1.2mm; }
table.idx { border-collapse: collapse; width: 100%; font-size: 8.4pt; margin-bottom: 3mm; }
table.idx th, table.idx td { border: 1px solid #000; padding: .6mm 1.5mm; text-align: center; }
table.idx th { background:#eee; }
table.idx td.l { text-align:left; }
table.idx td:nth-child(-n+3), table.idx th { white-space: nowrap; }
'''


def ans_html(items):
    rows = ''.join(
        f'<tr><td>{d["set"]}회 {d["no"]}번</td><td>{d["points"]}점</td><td>{"★"*d["stars"]}</td><td class="l">{AREAS[d["area"]]["name"]}</td>'
        f'<td>{d["src"]}</td><td class="l">{d["paper"]["cite"]}</td></tr>' for d in items)
    blocks = []
    cur = None
    for d in items:
        if d['set'] != cur:
            cur = d['set']
            blocks.append(f'<h2>{cur}회 정답 및 해설</h2>')
        blocks.append(f'''<div class="a"><div class="ah"><span>{d["set"]}회 {d["no"]}번 ({d["kind"]} {d["points"]}점) · {AREAS[d["area"]]["name"]}</span><span class="st">중요도 {"★"*d["stars"]}{"☆"*(3-d["stars"])}</span></div>
<div class="meta"><table>
<tr><td>변형 기출</td><td>{d["src"]} — {d["src_topic"]}</td></tr>
<tr><td>변형 포인트</td><td>{d["change"]}</td></tr>
<tr><td>소스 논문</td><td>{d["paper"]["cite"]} ({d["paper"]["book"]}) — {d["paper"]["what"]}</td></tr>
{f'<tr><td>노벨상 연계</td><td>{d["nobel"]}</td></tr>' if d.get("nobel") else ''}
</table></div>
<div class="ans"><b class="t">정답</b>{d["answer"]}</div>
<div class="exp"><b class="t">해설</b>{d["explain"]}</div></div>''')
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>기출변형 정답과 해설</title><style>{CSS.replace("@page { size: A4; margin: 0; }","")}{ANS_CSS}</style></head><body>
<h1>유기화학 기출변형 모의고사 — 정답 및 해설</h1>
<div class="sub">변형 기출 · 소스 논문(Klein 유기화학 인용 문헌) · 노벨상 연계 · 상세 해설</div>
<h2 class="nobreak">문항 색인</h2>
<table class="idx"><tr><th>문항</th><th>배점</th><th>중요도</th><th>영역</th><th>변형 기출</th><th>소스 논문</th></tr>{rows}</table>
{"".join(blocks)}</body></html>'''


def to_pdf(html_path, pdf_path):
    env = dict(os.environ)
    env['NODE_PATH'] = subprocess.check_output(['npm', 'root', '-g'], text=True).strip()
    subprocess.check_call(['node', os.path.join(HERE, 'print.js'), html_path, pdf_path], env=env)


if __name__ == '__main__':
    # 전체: python3 build.py   |  미리보기: python3 build.py --preview items/area_C.py [--nopdf]
    files = None; prefix = '변형모의고사'
    if '--preview' in sys.argv:
        files = [sys.argv[sys.argv.index('--preview') + 1]]
        prefix = 'preview_' + os.path.basename(files[0])[:-3]
    items = load_items(files)
    outd = os.path.join(HERE, 'out'); os.makedirs(outd, exist_ok=True)
    for name, fn in [(prefix + '_문제지', exam_html), (prefix + '_정답해설', ans_html)]:
        p = os.path.join(outd, name + '.html')
        open(p, 'w', encoding='utf-8').write(fn(items))
        if '--nopdf' not in sys.argv:
            to_pdf(p, p[:-5] + '.pdf')
    print(len(items), 'items built ->', prefix)
