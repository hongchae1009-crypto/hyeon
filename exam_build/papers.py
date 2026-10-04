"""논문·반응 정리집 빌드: data/papers_*.json + 기출 출제 경향 분석 → out/논문반응_정리집.(html|pdf)"""
import glob, html, json, os, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from chem import mol_svg, arrow, box
from areas import AREAS, EXAM_ITEMS
from build import CSS, to_pdf

NOBEL = [
    ('2025', 'Kitagawa · Robson · Yaghi', '금속–유기 골격체(MOF)', '배위 결합 기반 다공성 골격 — 착화합물·무기 영역과 연계'),
    ('2022', 'Bertozzi · Meldal · Sharpless', '클릭 화학·생체직교 화학', 'CuAAC(1,4-트라이아졸), 변형 촉진 SPAAC, 알카인 꼬리표 아미노산'),
    ('2021', 'List · MacMillan', '비대칭 유기촉매', '프롤린 엔아민 촉매(알돌·Robinson/Hajos–Parrish), 이미늄 촉매 Diels–Alder, ee 계산'),
    ('2010', 'Heck · Negishi · Suzuki', 'Pd 촉매 교차 짝지음', '산화적 첨가–금속 교환–환원적 제거, 아릴 할라이드·다이아조늄 활용'),
    ('2005', 'Chauvin · Grubbs · Schrock', '올레핀 복분해', '금속 카벤, 고리 닫음 복분해(RCM)'),
    ('2001', 'Knowles · Noyori · Sharpless', '키랄 촉매 수소화·산화', 'Sharpless 비대칭 에폭시화(DET), BINAP–Ru 수소화'),
    ('1994', 'Olah', '탄소 양이온 화학', '초강산·초친전자체, 탄소 양이온 자리옮김'),
    ('1990', 'Corey', '역합성 분석', '합성 설계(신톤), 보호기 전략'),
    ('1981', 'Fukui · Hoffmann', '프런티어 오비탈·궤도 대칭', 'HOMO–LUMO, Diels–Alder 위치/endo 선택성, 전자고리화'),
    ('1979', 'Brown · Wittig', '수소화붕소화 · Wittig 반응', 'anti-Markovnikov syn 첨가, oxaphosphetane, 알켄 기하'),
    ('1969', 'Barton · Hassel', '형태 분석', '의자 형태·A값·축/적도 반응성(E2 trans-diaxial)'),
    ('1950', 'Diels · Alder', 'Diels–Alder 반응', '[4+2] 협동 고리화 첨가, endo 규칙'),
    ('1912', 'Grignard · Sabatier', 'Grignard 시약 · 촉매 수소화', '탄소 친핵체의 카보닐 첨가'),
]

PCSS = '''
@page { size: A4; margin: 13mm 14mm 14mm; }
body { font-family: "NanumGothic", sans-serif; font-size: 9.4pt; line-height: 1.6; color:#000; background:#fff; margin:0; }
@media screen { body { max-width: 190mm; margin: 0 auto; padding: 10mm; } }
h1 { text-align:center; font-size: 19pt; margin: 6mm 0 1mm; }
.subt { text-align:center; color:#333; margin-bottom: 6mm; }
h2 { font-size: 14pt; border-bottom: 2.4px solid #000; padding-bottom: 1mm; margin: 0 0 3mm; break-before: page; }
h2.first { break-before: auto; }
h3 { font-size: 11pt; margin: 4mm 0 2mm; break-after: avoid; }
.chsum { border: 1px solid #000; background: #f4f4f4; padding: 2mm 4mm; margin-bottom: 3mm; columns: 2; column-gap: 6mm; font-size: 8.8pt; }
.chsum li { break-inside: avoid; }
.ref { border: 1px solid #555; margin: 0 0 2.6mm; break-inside: avoid; }
.ref .rh { display:flex; justify-content:space-between; gap: 3mm; background:#e9e9e9; padding: .8mm 2.5mm; font-weight:700; font-size: 8.9pt; }
.ref .rb { padding: 1.2mm 2.5mm; font-size: 8.8pt; }
.ref .rb div { margin-bottom: .6mm; }
.ref .k { display:inline-block; min-width: 13mm; font-weight:700; }
.ref .cite { font-family: "Times New Roman", serif; font-style: italic; }
.ref .nob { font-weight: 700; }
.ref .sch { display:flex; align-items:center; justify-content:center; flex-wrap:wrap; gap: 1mm 2mm; padding: 1mm 0 .5mm; border-top: 1px dashed #aaa; margin-top: 1mm; }
.cmpd { display:flex; flex-direction:column; align-items:center; }
.cmpd .lbl { font-size: 7.6pt; color:#333; }
.arr { display:flex; flex-direction:column; align-items:center; font-family: Arial, "NanumGothic", sans-serif; font-size: 7.4pt; line-height: 1.2; }
.arr .rt, .arr .rb { text-align:center; white-space: nowrap; min-height: 9px; }
table.t { border-collapse: collapse; width: 100%; font-size: 8.8pt; margin: 2mm 0 4mm; }
table.t th, table.t td { border: 1px solid #000; padding: .8mm 2mm; text-align:center; vertical-align: middle; }
table.t th { background:#e9e9e9; }
table.t td.l { text-align:left; }
.bar { display:grid; grid-template-columns: 52mm 1fr 10mm; align-items:center; gap: 2mm; margin: 1.2mm 0; font-size: 9pt; }
.bar .track { height: 4.2mm; background: #f0f0f0; border-radius: 0 4px 4px 0; }
.bar .fill { height: 100%; background: #333; border-radius: 0 4px 4px 0; }
.bar .v { font-weight: 700; }
.note { font-size: 8.6pt; color:#333; }
.stars { letter-spacing: 1px; }
'''


def scheme_html(sch):
    parts = []
    for s in sch:
        if 'smiles' in s:
            try:
                parts.append(box(mol_svg(s['smiles'], scale=14), html.escape(s.get('label', ''))))
            except Exception:
                parts.append(f'<div class="cmpd">[{html.escape(s.get("label",""))}]</div>')
        elif 'arrow' in s:
            parts.append(arrow(html.escape(s['arrow'])[:60]))
        elif 'plus' in s:
            parts.append('<div>+</div>')
    return f'<div class="sch">{"".join(parts)}</div>' if parts else ''


def trend_section():
    tot = Counter(a for _, _, a in EXAM_ITEMS)
    per = {'2014–2017': Counter(), '2018–2021': Counter(), '2022–2026': Counter()}
    pts = Counter()
    for k, p, a in EXAM_ITEMS:
        y = int(k[:4]); key = '2014–2017' if y <= 2017 else ('2018–2021' if y <= 2021 else '2022–2026')
        per[key][a] += 1; pts[(a, p)] += 1
    order = sorted(tot, key=lambda a: -tot[a])
    mx = max(tot.values())
    bars = ''.join(f'<div class="bar"><div>{AREAS[a]["name"]}</div><div class="track"><div class="fill" style="width:{tot[a]/mx*100:.1f}%"></div></div><div class="v">{tot[a]}</div></div>' for a in order)
    rows = ''.join(f'<tr><td class="l">{AREAS[a]["name"]}</td>' + ''.join(f'<td>{per[p][a]}</td>' for p in per) +
                   f'<td>{pts[(a,2)]}</td><td>{pts[(a,4)]}</td><td><b>{tot[a]}</b></td><td class="stars">{"★"*AREAS[a]["stars"]}</td></tr>' for a in order)
    nob = ''.join(f'<tr><td>{y}</td><td>{w}</td><td class="l">{t}</td><td class="l">{d}</td></tr>' for y, w, t, d in NOBEL)
    return f'''<h2 class="first">Ⅰ. 기출 출제 경향 분석 (2014~2026학년도 유기화학 66문항)</h2>
<h3>1. 영역별 출제 빈도</h3>{bars}
<table class="t"><tr><th>영역</th>{''.join(f'<th>{p}</th>' for p in per)}<th>2점</th><th>4점</th><th>합계</th><th>중요도</th></tr>{rows}</table>
<p class="note">· 2점(기입형)은 분광 구조 결정과 짧은 입체화학, 4점(서술형)은 카보닐 축합·방향족 다단계 합성 + 굽은 화살표 메커니즘이 주류이다.<br>
· 최근(2022~2026) 경향: ① 다단계 합성에서 중간체 분자식 제시 → 구조 추론, ② 고리 형성 단계(Robinson, Dieckmann, 분자 내 알돌, Claisen 자리옮김) 메커니즘 요구, ③ 입체특이성(Wittig→에폭시화, 동역학적 분할·ee), ④ 방향족성·FMO와 결합한 고리화 첨가.</p>
<h3>2. 핵심 반응 우선순위 (출제 빈도·최신성 기준)</h3>
<table class="t"><tr><th>순위</th><th>핵심 반응/개념</th><th>대표 기출</th></tr>
<tr><td>1</td><td class="l">엔올레이트 축합: 알돌·Claisen·Dieckmann·Michael·Robinson 고리 형성, 말론산/아세토아세트산 에스터 합성, 탈카복실화</td><td class="l">2026A-11, 2025A-11, 2024B-7, 2023A-10, 2023B-7, 2022B-9</td></tr>
<tr><td>2</td><td class="l">방향족: EAS 배향·속도, SNAr(Meisenheimer), 벤자인, 다이아조늄(Sandmeyer, 짝지음, 페놀화), Hofmann 자리옮김</td><td class="l">2026A-10, 2025A-10, 2024A-10/11, 2023A-2, 2022B-8</td></tr>
<tr><td>3</td><td class="l">분광: IR 카보닐·OH, ¹H NMR 이동·갈라짐·J, ¹³C/DEPT, MS 동위원소·McLafferty</td><td class="l">매년 1~2문항</td></tr>
<tr><td>4</td><td class="l">입체화학: anti/syn 첨가 → meso/라셈, E2 trans-diaxial, 에폭사이드 열림, 동역학적 분할·ee, A값</td><td class="l">2026A-1, 2024B-2, 2023B-2, 2021B-8, 2017A-13</td></tr>
<tr><td>5</td><td class="l">고리화 첨가·자리옮김: Diels–Alder(endo, 위치), Claisen/Cope, 방향족성(Hückel)</td><td class="l">2025B-7, 2024A-11, 2020B-7, 2019B-4, 2022A-2</td></tr>
<tr><td>6</td><td class="l">작용기 변환: Grignard/큐프레이트(1,2 vs 1,4), 알카인 수화, 라디칼 첨가, 아실 치환 메커니즘(¹⁸O), 인접기 관여</td><td class="l">2026B-7, 2021B-9, 2020B-8, 2017A-4</td></tr>
</table>
<h3>3. 노벨 화학상과 유기화학 출제 포인트</h3>
<table class="t"><tr><th>연도</th><th>수상자</th><th>주제</th><th>임용 연계 포인트</th></tr>{nob}</table>'''


def chapter_section(ch):
    s = ''.join(f'<li>{html.escape(x)}</li>' for x in ch.get('summary', []))
    refs = []
    for r in ch.get('refs', []):
        imp = int(r.get('importance', 2) or 2)
        nob = f'<div><span class="k">노벨상</span><span class="nob">{html.escape(r["nobel"])}</span></div>' if r.get('nobel') else ''
        refs.append(f'''<div class="ref"><div class="rh"><span>문제 {html.escape(str(r.get("problem","")))} · {html.escape(r.get("compound",""))}</span><span class="stars">중요도 {"★"*imp}{"☆"*(3-imp)}</span></div>
<div class="rb"><div><span class="k">문헌</span><span class="cite">{html.escape(r.get("cite",""))}</span></div>
<div><span class="k">반응</span>{html.escape(r.get("reaction_ko",""))}</div>
<div><span class="k">개념</span>{html.escape(r.get("concept_ko",""))}</div>{nob}
{scheme_html(r.get("scheme") or [])}</div></div>''')
    return f'<h2>제{ch["no"]}장 {html.escape(ch.get("title",""))}</h2><ul class="chsum">{s}</ul>{"".join(refs)}'


def main():
    chs = []
    for f in sorted(glob.glob(os.path.join(HERE, 'data', 'papers_*.json'))):
        chs += json.load(open(f, encoding='utf-8'))['chapters']
    chs.sort(key=lambda c: int(c['no']))
    n = sum(len(c.get('refs', [])) for c in chs)
    toc = ''.join(f'<tr><td>{c["no"]}장</td><td class="l">{html.escape(c.get("title",""))}</td><td>{len(c.get("refs",[]))}</td>'
                  f'<td>{sum(1 for r in c.get("refs",[]) if int(r.get("importance",2) or 2)==3)}</td></tr>' for c in chs)
    body = (trend_section() +
            f'<h2>Ⅱ. 교재(Klein 유기화학) 인용 논문 · 반응 정리 — 총 {n}편</h2>'
            f'<p class="note">각 장 끝 「참고문헌」에 실린 논문과, 그 논문을 소재로 한 도전·종합 문제의 반응을 정리했다. 중요도는 임용 출제 관점(★★★ 빈출 핵심)이다. 구조식은 RDKit으로 생성·검증하였다.</p>'
            f'<table class="t"><tr><th>장</th><th>제목</th><th>논문 수</th><th>★★★</th></tr>{toc}</table>' +
            ''.join(chapter_section(c) for c in chs))
    doc = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>논문·반응 정리집</title><style>{PCSS}</style></head><body>
<h1>유기화학 논문·반응 정리집</h1><div class="subt">Klein 유기화학 1~23장 인용 문헌 · 기출 출제 경향 · 노벨상 연계</div>{body}</body></html>'''
    p = os.path.join(HERE, 'out', '논문반응_정리집.html')
    open(p, 'w', encoding='utf-8').write(doc)
    if '--nopdf' not in sys.argv:
        to_pdf(p, p[:-5] + '.pdf')
    print(len(chs), 'chapters,', n, 'refs')


if __name__ == '__main__':
    main()
