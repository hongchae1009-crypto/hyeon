# -*- coding: utf-8 -*-
"""교육과정 원문 스캔 컷아웃 빈칸 시험지 빌더.
원문 스캔(김지현 편집 2022 개정 과학과 교육과정)의 쪽 이미지 + tesseract OCR 글자 위치(tsv) → spec.py의 빈칸 말을
문맥(앞뒤 글자)으로 근사 매칭하여 그 자리에 빈칸 상자를 덮는다. 내용 체계 파일과 성취기준·해설 파일을 따로 만든다."""
import csv, html, pathlib, re, subprocess, sys
sys.dont_write_bytecode = True
from PIL import Image, ImageDraw, ImageFont
from rapidfuzz import fuzz
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from spec import S

PG = pathlib.Path(sys.argv[1])          # 쪽 이미지(b{쪽}c.png)와 OCR(b{쪽}.tsv)이 있는 폴더
OUT = HERE / "컷아웃"; OUT.mkdir(exist_ok=True)
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
FONT = ImageFont.truetype("/root/.fonts/NanumGothic.ttf", 30)
MID_PAGES = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else []  # 중학교 물질 단원 성취기준 쪽

SUBJ = [  # (spec 절 번호, 과목명, 내용 체계 쪽, 성취기준·해설 쪽)
    (1, "중학교 과학(물질)", [9], MID_PAGES),
    (2, "통합과학1·2", [27, 34], [28, 29, 30, 31, 35, 36]),
    (3, "화학", [62], [63, 64, 65, 66]),
    (4, "물질과 에너지", [74], [75, 76, 77, 78]),
    (5, "화학 반응의 세계", [86], [87, 88, 89]),
]
DOTS = str.maketrans({"・": "·", "ㆍ": "·", "•": "·", "‧": "·", "∙": "·", "‘": "'", "’": "'", "“": '"', "”": '"'})
def nz(s): return re.sub(r"\s+", "", s.translate(DOTS))

def load(pno):
    """쪽의 글자 목록: (글자, x0, y0, x1, y1, 줄 id)"""
    rows = csv.DictReader(open(PG / f"b{pno}.tsv", encoding="utf-8"), delimiter="\t", quoting=csv.QUOTE_NONE)
    chars = []
    for r in rows:
        if r["level"] != "5": continue
        t = nz(r["text"] or "")
        if not t: continue
        x, y, w, h = (int(r[k]) for k in ("left", "top", "width", "height"))
        lid = (r["block_num"], r["par_num"], r["line_num"])
        for i, c in enumerate(t):
            chars.append((c, x + w * i / len(t), y, x + w * (i + 1) / len(t), y + h, lid))
    return chars

def find(chars, item, term):
    """item 문장 안의 term 자리를 쪽 글자열에서 찾아 (점수, 시작, 끝)을 돌려준다."""
    txt = "".join(c[0] for c in chars)
    it, tm = nz(item), nz(term)
    k = it.find(tm)
    if k < 0: return None
    best = None
    for ctx in (8, 5, 3):
        pat = it[max(0, k - ctx):k] + tm + it[k + len(tm):k + len(tm) + ctx]
        a = fuzz.partial_ratio_alignment(pat, txt)
        if a is None or a.score < 72: continue
        win = txt[a.dest_start:a.dest_end]
        b = fuzz.partial_ratio_alignment(tm, win)
        if b is None: continue
        pre = k - max(0, k - ctx)
        # 문맥 길이로 대략 위치를 잡고, 말 자체 정렬로 미세 조정
        s0 = a.dest_start + b.dest_start; e0 = a.dest_start + b.dest_end
        sc = min(a.score, b.score + 10)
        if best is None or sc > best[0]: best = (sc, s0, e0)
        if a.score >= 88: break
    return best

def draw(img, chars, spans):
    d = ImageDraw.Draw(img)
    for no, s, e in spans:
        segs = {}
        for c in chars[s:e]:
            g = segs.setdefault(c[5], [1e9, 1e9, -1, -1])
            g[0] = min(g[0], c[1]); g[1] = min(g[1], c[2]); g[2] = max(g[2], c[3]); g[3] = max(g[3], c[4])
        first = True
        for g in sorted(segs.values(), key=lambda g: (g[1], g[0])):
            x0, y0, x1, y1 = g[0] - 4, g[1] - 6, g[2] + 4, g[3] + 6
            d.rectangle((x0, y0, x1, y1), fill=255)
            d.line((x0, y1, x1, y1), fill=0, width=3)
            if first:
                d.text((x0 + 2, y0 - 2), str(no), fill=90, font=FONT); first = False

def build(kind):
    pages_html, keys, report = [], [], []
    for sidx, name, pc, ps in SUBJ:
        pages = pc if kind == "내용체계" else ps
        groups = S[sidx]["groups"]
        groups = groups[:1] if kind == "내용체계" else groups[1:]
        chars = {p: load(p) for p in pages}
        found = {p: [] for p in pages}
        for g in groups:
            for text, terms in g["items"]:
                for t in terms:
                    cands = [(r, p) for p in pages if (r := find(chars[p], text, t))]
                    if not cands:
                        report.append(f"{name}: 못 찾음 — {t}"); continue
                    (sc, s, e), p = max(cands, key=lambda x: x[0][0])
                    if any(not (e <= s2 or s >= e2) for _, s2, e2, _ in found[p]):
                        report.append(f"{name}: 겹침 생략 — {t}"); continue
                    found[p].append((t, s, e, sc))
        no, ak = 1, []
        for p in pages:
            img = Image.open(PG / f"b{p}c.png").convert("L")
            spans = []
            for t, s, e, sc in sorted(found[p], key=lambda f: (chars[p][f[1]][2] // 25, chars[p][f[1]][1])):
                spans.append((no, s, e)); ak.append((no, t, p)); no += 1
            draw(img, chars[p], spans)
            # 아래쪽 빈 여백 잘라 내기
            px = img.load(); h = img.height
            while h > 200 and all(px[x, h - 1] > 235 for x in range(0, img.width, 7)): h -= 1
            img = img.crop((0, 0, img.width, min(img.height, h + 30)))
            fn = f"{kind}_{name}_{p}.png".replace("·", "")
            img.save(OUT / fn)
            pages_html.append(f"<section class='pg'><div class='hd'><b>{html.escape(name)}</b> — {'내용 체계' if kind == '내용체계' else '성취기준 · 성취기준 해설 · 적용 시 고려 사항'} "
                              f"<span>원문 {p}쪽</span><span class='who'>이름 ______ 점수 ____</span></div><img src='{OUT.name}/{fn}'></section>")
        keys.append(f"<h3>{html.escape(name)} — {len(ak)}개</h3><div class='grid'>" +
                    "".join(f"<div><b>{n}</b>{html.escape(t)} <small>({p}쪽)</small></div>" for n, t, p in ak) + "</div>")
        print(f"[{kind}] {name}: 빈칸 {len(ak)}개")
    for r in report: print("  ", r)
    css = """@page{size:A4;margin:10mm 12mm}body{margin:0;font-family:'NanumGothic',sans-serif}
.pg{page-break-after:always;text-align:center}.pg:last-child{page-break-after:auto}
.hd{text-align:left;font-size:10pt;border-bottom:1pt solid #111;padding-bottom:1.5mm;margin-bottom:2mm;display:flex;gap:4mm;align-items:baseline}
.hd span{color:#555;font-size:9pt}.hd .who{margin-left:auto;color:#111}
.pg img{width:100%;max-height:262mm;object-fit:contain}
.ans{font-size:9.2pt;line-height:1.45}.ans h1{font-size:13pt;border-bottom:1.2pt solid #111;padding-bottom:1.5mm}
.ans h3{font-size:10.2pt;margin:4mm 0 1.5mm;color:#1a3d6d}.grid{column-count:3;column-gap:6mm;column-rule:.5pt solid #ccc}
.grid div{break-inside:avoid;padding:.3mm 0}.grid b{display:inline-block;min-width:7mm;color:#1a3d6d}.grid small{color:#888}"""
    title = "내용 체계" if kind == "내용체계" else "성취기준·해설"
    docs = {f"교육과정_원문컷아웃_{kind}_문제지": "".join(pages_html),
            f"교육과정_원문컷아웃_{kind}_정답지": f"<div class='ans'><h1>2022 개정 교육과정 원문 컷아웃 빈칸 — {title} 정답</h1>{''.join(keys)}</div>"}
    for stem, body in docs.items():
        h = HERE / f"{stem}.html"
        h.write_text(f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>{stem}</title><style>{css}</style></head><body>{body}</body></html>", encoding="utf-8")
        subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                        f"--print-to-pdf={HERE / (stem + '.pdf')}", f"file://{h}"], capture_output=True)

if __name__ == "__main__":
    build("내용체계"); build("성취기준")
