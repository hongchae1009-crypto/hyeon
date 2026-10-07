"""질문별·버전별 산출물 아카이브 생성기.
- md → html(+pdf): 추출본·카탈로그·계획서·색인 등 텍스트 문서
- html → md(+svg 자산): 시험지·해설·정리집 (구조식 SVG는 assets/ 로 분리)
사용: python3 make_archive.py <spec.json>
"""
import json, os, re, shutil, subprocess, sys
import markdown
from bs4 import BeautifulSoup
from markdownify import markdownify

PRINT = '/home/user/hyeon/exam_build/print.js'

MD_CSS = '''
@page { size: A4; margin: 15mm 14mm 15mm; }
body { font-family: "NanumGothic", "Noto Sans CJK KR", sans-serif; font-size: 10pt; line-height: 1.65; color: #111; background: #fff; margin: 0; }
@media screen { body { max-width: 190mm; margin: 0 auto; padding: 12mm 10mm; } }
h1 { font-size: 18pt; border-bottom: 2.5px solid #000; padding-bottom: 2mm; margin: 0 0 4mm; }
h2 { font-size: 14pt; border-bottom: 1.5px solid #000; padding-bottom: 1mm; margin: 7mm 0 3mm; break-after: avoid; }
h3 { font-size: 11.5pt; margin: 5mm 0 2mm; break-after: avoid; }
h4 { font-size: 10.5pt; margin: 4mm 0 1.5mm; break-after: avoid; }
table { border-collapse: collapse; width: 100%; margin: 2mm 0 4mm; font-size: 8.8pt; }
th, td { border: 1px solid #555; padding: .8mm 1.8mm; vertical-align: top; text-align: left; }
th { background: #eee; }
tr { break-inside: avoid; }
code { font-family: "NanumGothicCoding", monospace; font-size: 8.4pt; background: #f3f3f3; padding: 0 1mm; word-break: break-all; }
pre { background: #f3f3f3; padding: 2mm 3mm; white-space: pre-wrap; word-break: break-all; font-size: 8.4pt; }
blockquote { border-left: 3px solid #999; margin: 2mm 0; padding: .5mm 3mm; color: #333; }
li { margin: .4mm 0; }
hr { border: 0; border-top: 1px dashed #999; margin: 5mm 0; }
img { max-width: 100%; }
.vtag { display: inline-block; border: 1.5px solid #000; padding: 0 2mm; font-weight: 700; margin-right: 2mm; }
'''


def pdf(html_path, pdf_path):
    env = dict(os.environ)
    env['NODE_PATH'] = subprocess.check_output(['npm', 'root', '-g'], text=True).strip()
    subprocess.check_call(['node', PRINT, html_path, pdf_path], env=env)


def md_to_html_pdf(md_text, out_base, title):
    body = markdown.markdown(md_text, extensions=['tables', 'fenced_code', 'sane_lists', 'toc'])
    doc = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
           f'<title>{title}</title><style>{MD_CSS}</style></head><body>{body}</body></html>')
    open(out_base + '.md', 'w', encoding='utf-8').write(md_text)
    open(out_base + '.html', 'w', encoding='utf-8').write(doc)
    pdf(out_base + '.html', out_base + '.pdf')


def _svgs_to_files(soup, root, asset_dir, prefix):
    os.makedirs(os.path.join(root, asset_dir), exist_ok=True)
    for i, svg in enumerate(soup.find_all('svg')):
        s = str(svg)
        if 'xmlns=' not in s.split('>', 1)[0]:
            s = s.replace('<svg', '<svg xmlns="http://www.w3.org/2000/svg"', 1)
        name = f'{prefix}_{i:04d}.svg'
        open(os.path.join(root, asset_dir, name), 'w', encoding='utf-8').write(s)
        img = soup.new_tag('img', src=f'{asset_dir}/{name}', alt='구조식/스펙트럼')
        svg.replace_with(img)


def _md(html_frag):
    md = markdownify(html_frag, heading_style='ATX', bullets='-', sub_symbol='<sub>', sup_symbol='<sup>')
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md.strip() + '\n'


def html_to_md(html_path, md_path, title, kind):
    root = os.path.dirname(md_path)
    base = os.path.splitext(os.path.basename(md_path))[0]
    soup = BeautifulSoup(open(html_path, encoding='utf-8').read(), 'html.parser')
    for t in soup(['style', 'script', 'template']):
        t.decompose()
    _svgs_to_files(soup, root, 'assets', base)
    parts = [f'# {title}\n']
    if kind == 'exam':
        pool = soup.find(id='pool')
        cur = None
        for q in pool.select('.q'):
            s = q.get('data-set')
            if s != cur:
                cur = s
                parts.append(f'\n## {s}회\n')
            qn = q.select_one('.qn')
            num = qn.get_text(strip=True) if qn else ''
            if qn: qn.decompose()
            src = q.select_one('.src')
            src_md = ''
            if src:
                src_md = '\n> ' + src.get_text(' ', strip=True) + '\n'
                src.decompose()
            parts.append(f'\n### {num}\n\n' + _md(str(q)) + src_md + '\n---\n')
    else:
        parts.append(_md(str(soup.body)))
    open(md_path, 'w', encoding='utf-8').write('\n'.join(parts))


def main(spec_path):
    spec = json.load(open(spec_path, encoding='utf-8'))
    out = spec['out']
    for v in spec['versions']:
        vd = os.path.join(out, v['dir'])
        os.makedirs(vd, exist_ok=True)
        for d in v['docs']:
            base = os.path.join(vd, d['name'])
            if d['type'] == 'md':  # 마크다운 원천 (파일 목록 결합 또는 직접 텍스트)
                text = d.get('text', '')
                for f in d.get('files', []):
                    text += '\n\n' + open(f, encoding='utf-8').read()
                md_to_html_pdf(text.strip() + '\n', base, d['title'])
            elif d['type'] == 'html':  # 조판 HTML/PDF 원천
                shutil.copy(d['html'], base + '.html')
                if d.get('pdf'):
                    shutil.copy(d['pdf'], base + '.pdf')
                else:
                    pdf(base + '.html', base + '.pdf')
                html_to_md(d['html'], base + '.md', d['title'], d.get('kind', 'doc'))
            print('ok', v['dir'], d['name'])


if __name__ == '__main__':
    main(sys.argv[1])
