# -*- coding: utf-8 -*-
"""2027 화학 임용 과교론 최종 정리 PDF 빌더: spec.py + 기출·교육과정 컷아웃 → HTML → PDF(A4)"""
import html, pathlib, subprocess, sys
from PIL import Image
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
import cut
from spec import CUT, TOPICS, CORE, ITEMS, TB

IMG = HERE / "img"; IMG.mkdir(exist_ok=True)
CHROME = str(sorted(pathlib.Path("/opt/pw-browsers").glob("chromium-*/chrome-linux*/chrome"))[-1])
STEM = "2027_화학임용_과교론_최종정리"
NAME = {it["id"]: it for it in ITEMS}
lab = lambda i: NAME[i].get("lab") or f"20{i[:2]} {i[2:]}"
MM_PER_PX_EXAM = 25.4 / 200
MM_PER_PX_CUR = 25.4 / cut.DPI

def exam_img(it):
    f = IMG / f"exam_{it['id']}.png"
    im = cut.exam_cut(it["idx"])
    if not f.exists(): im.save(f, optimize=True)
    return f.name, im.size

def cur_img(key):
    f = IMG / f"cur_{key}.png"
    title, segs = CUT[key]
    if not f.exists():
        parts = []
        for p, a, b, opt in segs:
            im, sc = cut.cur_cut(p, a, b, **opt)
            if min(sc) < 70: print("  ! 컷아웃 위치 확인 필요:", key, p, a[:20], sc)
            parts.append(im)
        W = max(p.width for p in parts); H = sum(p.height for p in parts) + 18 * (len(parts) - 1)
        out = Image.new("L", (W, H), 255); y = 0
        for p in parts:
            out.paste(p, (0, y)); y += p.height + 18
        out.save(f, optimize=True)
    return f.name, Image.open(f).size, title

def tb_img(path):
    src = HERE / TB / path; f = IMG / ("tb_" + path.replace("/", "_"))
    if not f.exists():
        im = Image.open(src).convert("L"); im.thumbnail((1000, 1400)); im.save(f, optimize=True)
    return f.name

e = html.escape
def item_html(n, it):
    fn, (w, h) = exam_img(it)
    wide = w > 1000
    star = "<span class='key'>주요</span>" if it["key"] else ""
    head = (f"<div class='ih' id='q{it['id']}'><span class='no'>{n:02d}</span><b>{lab(it['id'])}</b>"
            f"<span class='tp'>{e(it['topic'])}</span>{star}"
            f"<span class='nav'><a href='#toc'>목차로</a>" + (" · <a href='#keys'>주요 문제로</a>" if it["key"] else "") + "</span></div>")
    if wide:
        ex = f"<div class='exw'><div class='cap'>기출 원문</div><img src='img/{fn}' style='width:{min(170, w * MM_PER_PX_EXAM * .84):.1f}mm'></div>"
    else:
        ex = f"<div class='ex'><div class='cap'>기출 원문</div><img src='img/{fn}' style='width:{min(78, w * MM_PER_PX_EXAM * .82):.1f}mm'></div>"
    ans = "".join(f"<tr><th>{e(k)}</th><td>{v}</td></tr>" for k, v in it["ans"])
    core = "".join(f"<li>{c}</li>" for c in it["core"])
    c22 = ""
    if it["cuts"] or it["c22"] or it["tb"]:
        body = f"<p class='c22t'>{it['c22']}</p>" if it["c22"] else ""
        for k in it["cuts"]:
            cf, (cw, chh), title = cur_img(k)
            body += (f"<div class='cut'><div class='ct'>2022 개정 원문 · {e(title)}</div>"
                     f"<img src='img/{cf}' style='width:{min(178, cw * MM_PER_PX_CUR * .86):.1f}mm'></div>")
        for path, capt in it["tb"]:
            body += f"<div class='tb'><img src='img/{tb_img(path)}'><div class='tc'>교과서 · {e(capt)}</div></div>"
        c22 = f"<div class='box'><div class='bt'>2022 개정으로 보기</div>{body}</div>"
    return (f"<section class='item'>{head}{ex}<div class='box'><div class='bt'>모범 답안</div><table class='ans'>{ans}</table></div>"
            f"<div class='box'><div class='bt'>핵심 · 짚고 넘어갈 점</div><ul>{core}</ul></div>{c22}<div class='clr'></div></section>")

def build():
    # 목차
    rows = "".join((f"<tr><td colspan='4' class='sep'>옛 기출(2016~2020) — 주제가 다시 나올 만한 문항, 2022 개정 기준으로 다시 보기</td></tr>" if it["id"] == next(i["id"] for i in ITEMS if int(i["id"][:2]) < 21) else "") + f"<tr><td>{n:02d}</td><td><a href='#q{it['id']}'>{lab(it['id'])}</a></td><td class='l'><a href='#q{it['id']}'>{e(it['topic'])}</a></td><td>{'●' if it['key'] else ''}</td></tr>"
                   for n, it in enumerate(ITEMS, 1))
    keys = "".join(f"<li><a href='#q{it['id']}'><b>{lab(it['id'])}</b> {e(it['topic'])}</a></li>" for it in ITEMS if it["key"])
    toc = f"""<section class='toc' id='toc'><h1>2027 중등 화학 임용 · 과학교육론 최종 정리</h1>
<p class='sub'>근거: 화학교육론 기출 2014~2026, 물리·생물·지구과학 교육론 기출 2024~2026 · 기준: 2022 개정 과학과 교육과정(교육부 고시 제2022-33호)</p>
<div class='box'><div class='bt'>구성</div><ol class='parts'>
<li><a href='#topics'>Ⅰ. 2027 출제 유력 주제</a> — 물·생·지 최근 기출에서 화학으로 넘어올 주제</li>
<li><a href='#core'>Ⅱ. 핵심 압축</a> — 문항 해설에서 다 못 다룬 이론 용어</li>
<li><a href='#items'>Ⅲ. 다시 볼 기출 {len(ITEMS)}문항</a> — 2021~2026 {sum(int(i['id'][:2]) >= 21 for i in ITEMS)}문항 + 주제가 다시 나올 만한 2016~2020 {sum(int(i['id'][:2]) < 21 for i in ITEMS)}문항 · 기출 원문 · 모범 답안 · 짚을 점 · 2022 개정 원문 컷아웃 · 교과서</li></ol></div>
<div class='box' id='keys'><div class='bt'>주요 문제 {sum(i['key'] for i in ITEMS)}선 — 시간이 없으면 이것부터</div><ol class='keys'>{keys}</ol></div>
<div class='box' id='items'><div class='bt'>Ⅲ. 다시 볼 기출 목록 (● 주요 문제)</div><table class='toct'><tr><th>번호</th><th>문항</th><th>주제</th><th>주요</th></tr>{rows}</table></div></section>"""
    trs = ""
    for star, name, other, chem, pred, ids in TOPICS:
        links = " ".join(f"<a href='#q{i}'>{lab(i)}</a>" for i in ids)
        trs += f"<tr><td class='s'>{star}</td><td class='l'><b>{e(name)}</b></td><td class='l'>{e(other)}</td><td class='l'>{e(pred)}</td><td class='l'>{links}</td></tr>"
    topics = f"""<section class='pg' id='topics'><div class='ph'><h2>Ⅰ. 2027 출제 유력 주제</h2><span class='nav'><a href='#toc'>목차로</a></span></div>
<p class='sub'>2021년부터 과목당 6문항(전공A 5·6·7, 전공B 3·4·5), 모두 4점 서술형. 한 문항 = 교육론 이론 1~2개 + 교과 내용 오류 수정 또는 교육과정 적용의 결합형. 2025년부터 ‘2022 개정 과학과 교육과정(교육부 고시 제2022-33호)’을 명시한다.</p>
<table class='tp'><tr><th style='width:11%'>출제 가능성</th><th style='width:17%'>주제</th><th style='width:24%'>물·생·지 근거(2024~2026)</th><th>화학 예상 소재 · 발문</th><th style='width:13%'>관련 기출</th></tr>{trs}</table>
<div class='box'><div class='bt'>최근 경향 세 줄</div><ul>
<li>2026년 물화생지 24문항 중 약 12문항이 2022 개정 원문(성취기준·해설·탐구 활동·내용 체계·교수·학습)을 직접 인용했다.</li>
<li>학습 이론은 비고츠키(3과목)·오수벨(3과목)·로슨(2과목)이 같은 해에 겹쳐 나왔다. 한 과목에서 나온 이론은 다음 해 다른 과목으로 옮겨 가는 경우가 많다.</li>
<li>화학에서 최근 안 나왔지만 타 과목에서 나온 것: 라카토슈(2026 생물), 포퍼 반증 가능성(2026 지구), 로슨 3유형 구분(2026 생물·물리), 분석적 채점·피드백(2026 지구), 귀추적 탐구 모형(2026 지구), 프로젝트 학습·디지털 소양(2026 지구), 외삽(2026 물리).</li></ul></div></section>"""
    cores = "".join(f"<div class='cb'><div class='bt'>{e(t)}</div><ul>{''.join(f'<li>{x}</li>' for x in xs)}</ul></div>" for t, xs in CORE)
    core = f"<section class='pg' id='core'><div class='ph'><h2>Ⅱ. 핵심 압축</h2><span class='nav'><a href='#toc'>목차로</a></span></div><div class='cg'>{cores}</div></section>"
    items = "".join(item_html(n, it) for n, it in enumerate(ITEMS, 1))
    css = """@page{size:A4;margin:11mm 11mm 12mm}
body{margin:0;font-family:'NanumGothic',sans-serif;font-size:8.7pt;line-height:1.5;color:#000}
a{color:#000;text-decoration:underline;text-decoration-thickness:.4pt;text-underline-offset:1.5pt}
h1{font-size:16pt;margin:0 0 1.5mm}h2{font-size:13pt;margin:0}
.sub{color:#333;margin:0 0 3mm;font-size:8.4pt}
.box{border:.7pt solid #000;padding:1.6mm 2.6mm 2mm;margin:0 0 2.6mm;break-inside:auto;display:flow-root}
.bt{font-weight:bold;font-size:8.9pt;border-bottom:.5pt solid #000;padding-bottom:.8mm;margin-bottom:1.4mm}
ul{margin:0;padding-left:4.2mm}li{margin:.3mm 0}
.parts{margin:0;padding-left:5mm}.parts li{margin:.8mm 0}
.keys{margin:0;padding-left:6mm;columns:2;column-gap:6mm}.keys li{margin:.6mm 0;break-inside:avoid}
table{border-collapse:collapse;width:100%}
.toct td,.toct th,.tp td,.tp th{border:.5pt solid #000;padding:.8mm 1.6mm;text-align:center;vertical-align:top}
.toct th,.tp th{font-weight:bold;border-bottom:1pt solid #000}
td.l{text-align:left}td.s{white-space:nowrap;letter-spacing:-.5pt}
.tp{font-size:8.1pt;line-height:1.42;margin-bottom:3mm}
.toc,.pg{break-after:page}
.ph{display:flex;align-items:baseline;justify-content:space-between;border-bottom:1.2pt solid #000;padding-bottom:1mm;margin-bottom:2.5mm}
.nav{font-size:8pt;font-weight:normal;white-space:nowrap}
.cg{columns:2;column-gap:4mm}.cb{border:.7pt solid #000;padding:1.6mm 2.4mm 2mm;margin:0 0 3mm;break-inside:avoid}
.item{break-before:page}
.ih{display:flex;align-items:baseline;gap:2.2mm;border-bottom:1.2pt solid #000;padding-bottom:1mm;margin-bottom:2.4mm}
.ih .no{font-size:8pt;border:.6pt solid #000;padding:0 1.2mm}
.ih b{font-size:12.5pt;white-space:nowrap}.ih .tp{font-size:9.6pt;flex:1}
.ih .nav{margin-left:auto}
.key{font-size:7.8pt;border:.9pt solid #000;padding:0 1.3mm;font-weight:bold;white-space:nowrap}
.ex{float:left;margin:0 3.4mm 2mm 0;border:.6pt solid #000;padding:1mm 1.2mm}
.exw{border:.6pt solid #000;padding:1mm 1.2mm;margin:0 0 2.6mm;text-align:center}
.cap{font-size:7.4pt;border-bottom:.4pt solid #000;margin-bottom:1mm;text-align:left}
.ex img,.exw img{display:block}
.ans th{width:16mm;text-align:left;vertical-align:top;padding:.7mm 1.5mm .7mm 0;font-size:8.2pt;border-bottom:.3pt solid #999}
.ans td{padding:.7mm 0;border-bottom:.3pt solid #999}.ans tr:last-child th,.ans tr:last-child td{border-bottom:0}
.c22t{margin:0 0 1.6mm}
.cut{border:.5pt dashed #000;padding:1mm 1.4mm;margin:0 0 1.8mm;display:inline-block;max-width:100%;box-sizing:border-box}
.cut img{display:block;max-width:100%}.ct{font-size:7.3pt;margin-bottom:.8mm;font-weight:bold}
.tb{border:.5pt solid #000;padding:1mm;margin:0 0 1.5mm;display:inline-block;width:62mm;vertical-align:top}
.tb img{width:100%;display:block}.tc{font-size:7.2pt;margin-top:.6mm}
.clr{clear:both}
.toct{font-size:7.8pt;line-height:1.3}.toct td{padding:.35mm 1.4mm!important}.toc .box{margin-bottom:2mm}
.sep{text-align:left!important;font-weight:bold;border-top:1.2pt solid #000!important}"""
    doc = f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>{STEM}</title><style>{css}</style></head><body>{toc}{topics}{core}{items}</body></html>"
    h = HERE / f"{STEM}.html"; h.write_text(doc, encoding="utf-8")
    pdf = HERE / f"{STEM}.pdf"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000",
                    f"--print-to-pdf={pdf}", f"file://{h}"], capture_output=True)
    print(pdf.name, "만듦")

if __name__ == "__main__":
    build()
