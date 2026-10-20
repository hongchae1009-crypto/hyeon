"""print.js로 PDF를 만들고, 한 쪽을 넘긴 문항만 9.5pt로 줄여 한 쪽에 들어가면 그 크기를 유지한다.

사용법: python3 make_pdf.py   (build.py로 HTML을 먼저 만든 뒤)
"""
import json, os, subprocess
import pypdf

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
HTML = os.path.join(ROOT, '모의고사4회_상세해설.html')
PDF = os.path.join(ROOT, '모의고사4회_상세해설.pdf')
IDS = [f'a{i}' for i in range(1, 13)] + [f'b{i}' for i in range(1, 12)]


def render(sizes):
    subprocess.run(['node', os.path.join(os.path.dirname(__file__), 'print.js'), HTML, PDF, json.dumps(sizes)],
                   check=True, stdout=subprocess.DEVNULL)
    r = pypdf.PdfReader(PDF)
    marks = []

    def walk(items):
        for x in items:
            if isinstance(x, list):
                walk(x)
            else:
                marks.append(r.get_destination_page_number(x))
    walk(r.outline)
    starts = sorted(set(marks))[-len(IDS):]  # 마지막 23개 = 문항 시작 쪽
    ends = starts[1:] + [len(r.pages)]
    return {q: e - s for q, s, e in zip(IDS, starts, ends)}, len(r.pages)


span, n = render({})
print('10pt:', n, '쪽,', '두 쪽 이상:', [q for q in IDS if span[q] > 1])
trial = {q: 9.5 for q in IDS if span[q] > 1}
span2, _ = render(trial)
keep = {q: 9.5 for q in trial if span2[q] < span[q]}
span3, n = render(keep)
print('9.5pt로 줄인 문항:', list(keep), '→', n, '쪽')
