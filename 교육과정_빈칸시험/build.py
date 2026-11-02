# -*- coding: utf-8 -*-
"""교육과정 원문 빈칸 시험지·정답지 빌더: spec.py → 원문 대조 검사 → HTML → PDF(A4)"""
import glob, html, pathlib, re, subprocess, sys
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from spec import S

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
CUR = HERE.parent / "변형문제_작업" / "교육과정"
norm = lambda s: re.sub(r"\s+", " ", s).strip()
CORPUS = norm(" ".join(p.read_text(encoding="utf-8") for p in CUR.glob("*.md")))

def check():
    bad = 0
    for s in S:
        for g in s["groups"]:
            for text, terms in g["items"]:
                if norm(text) not in CORPUS:
                    bad += 1; print("원문 불일치:", text[:70])
                for t in terms:
                    if t not in text:
                        bad += 1; print("빈칸 말 없음:", t, "←", text[:50])
    return bad

def blanks(text, terms):
    """terms를 앞에서부터 차례로 찾아 (시작, 끝, 말) 목록으로 돌려준다(겹침 없음)."""
    spans, pos = [], 0
    for t in terms:
        i = text.find(t, pos)
        if i < 0:
            i = next(j for j in (m.start() for m in re.finditer(re.escape(t), text))
                     if all(j >= e or j + len(t) <= b for b, e, _ in spans))
        spans.append((i, i + len(t), t)); pos = i + len(t)
    return sorted(spans)

def render_item(text, terms, no):
    out, cur, ans = [], 0, []
    for b, e, t in blanks(text, terms):
        out.append(html.escape(text[cur:b]))
        w = max(3.2, 0.95 * len(t) + 1.6)
        out.append(f"<span class='bl' style='min-width:{w:.1f}em'><i>{no}</i></span>")
        ans.append((no, t)); no += 1; cur = e
    out.append(html.escape(text[cur:]))
    return "".join(out), ans, no

CSS = """
@page{size:A4;margin:15mm 14mm 16mm}
body{font-family:'NanumMyeongjo','Nanum Myeongjo',serif;font-size:10.4pt;line-height:2.05;color:#111;margin:0}
.test{page-break-after:always}
.test:last-child{page-break-after:auto}
.hd{border:1.4pt solid #111;padding:2.5mm 4mm;margin-bottom:4mm;display:flex;gap:6mm;justify-content:space-between;align-items:flex-end;line-height:1.5}.hd>div:first-child{flex:1;min-width:0}
.hd h1{font-size:14pt;margin:0}.hd .sub{font-size:8.8pt;color:#333;margin-top:1mm}
.hd .who{flex:none;font-size:10pt;white-space:nowrap;text-align:right;line-height:2}
.hd .who span{display:inline-block;border-bottom:.8pt solid #111;min-width:28mm;margin-left:2mm}
h2{font-family:'NanumGothic',sans-serif;font-size:10.6pt;margin:4mm 0 1mm;padding:.6mm 2.5mm;background:#eef1f5;border-left:3pt solid #1a3d6d;line-height:1.5}
ol{margin:0;padding-left:0;list-style:none}
li{margin:0 0 1.4mm;text-align:left;word-break:keep-all;padding-left:3.5mm;text-indent:-3.5mm}li::before{content:'◦ ';color:#777}
.bl{text-indent:0;display:inline-block;border-bottom:.9pt solid #111;height:1.25em;vertical-align:-.15em;position:relative;margin:0 .15em;text-align:left}
.bl i{font-style:normal;font-family:'NanumGothic',sans-serif;font-size:7.4pt;color:#555;position:absolute;left:.15em;top:-.15em}
.note{font-size:8.6pt;color:#444;margin:0 0 2mm;line-height:1.5}
/* 정답지 */
.ans{font-family:'NanumGothic',sans-serif;font-size:9.2pt;line-height:1.45}
.ans h1{font-size:13pt;margin:0 0 3mm;border-bottom:1.2pt solid #111;padding-bottom:1.5mm}
.ans h3{font-size:10.2pt;margin:4mm 0 1.5mm;color:#1a3d6d}
.grid{column-count:3;column-gap:6mm;column-rule:.5pt solid #ccc}
.grid div{break-inside:avoid;padding:.4mm 0}
.grid b{display:inline-block;min-width:7mm;color:#1a3d6d}
"""

def build():
    if check():
        sys.exit("원문 검사 실패 — spec.py를 고칠 것")
    tests, keys = [], []
    for k, s in enumerate(S, 1):
        no, body, ak = 1, [], []
        for g in s["groups"]:
            lis = []
            for text, terms in g["items"]:
                h, a, no = render_item(text, terms, no)
                h = re.sub(r"^•\s*", "", h)
                lis.append(f"<li>{h}</li>"); ak += a
            body.append(f"<h2>{html.escape(g['name'])}</h2><ol>{''.join(lis)}</ol>")
        n = no - 1
        tests.append(f"""<section class='test'><div class='hd'><div><h1>[{k}] {html.escape(s['title'])}</h1>
<div class='sub'>2022 개정 과학과 교육과정(교육부 고시 제2022-33호) 원문 빈칸 채우기 · {html.escape(s['sub'])} · 빈칸 {n}개</div></div>
<div class='who'>이름<span></span><br>점수<span style='min-width:18mm'></span> / {n}</div></div>
<p class='note'>◦ 빈칸에는 교육과정 원문의 용어를 그대로 쓰시오. (빈칸 왼쪽 위의 작은 숫자가 문항 번호)</p>{''.join(body)}</section>""")
        cells = "".join(f"<div><b>{i}</b>{html.escape(t)}</div>" for i, t in ak)
        keys.append(f"<h3>[{k}] {html.escape(s['title'])} — {n}개</h3><div class='grid'>{cells}</div>")
        print(f"[{k}] {s['title']}: 빈칸 {n}개")
    doc = lambda title, body: f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>"
    files = {
        "교육과정_원문빈칸_문제지": doc("교육과정 원문 빈칸 문제지", "".join(tests)),
        "교육과정_원문빈칸_정답지": doc("교육과정 원문 빈칸 정답지", "<div class='ans'><h1>2022 개정 교육과정 원문 빈칸 채우기 — 정답</h1>" + "".join(keys) + "</div>"),
    }
    for stem, d in files.items():
        h = HERE / f"{stem}.html"; h.write_text(d, encoding="utf-8")
        subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        "--virtual-time-budget=6000", f"--print-to-pdf={HERE / (stem + '.pdf')}", f"file://{h}"], capture_output=True)

if __name__ == "__main__":
    build()
