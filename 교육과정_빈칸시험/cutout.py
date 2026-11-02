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
ONLY_RIGHT = {9: (950, 420)}  # 중학교 내용 체계 표: 핵심 아이디어 아래는 '중학교 1~3학년' 열만 대상
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
    """쪽의 글자 목록: (글자, x0, y0, x1, y1, 줄 id) — tesseract hOCR 문자 상자(h{쪽}.hocr)"""
    src = (PG / f"h{pno}.hocr").read_text(encoding="utf-8")
    chars = []
    for li, line in enumerate(re.split(r"<span class='ocr_line'", src)[1:]):
        for m in re.finditer(r"<span class='ocrx_cinfo' title='x_bboxes (\d+) (\d+) (\d+) (\d+)[^']*'>([^<]*)</span>", line):
            c = nz(html.unescape(m.group(5)))
            if not c: continue
            x0, y0, x1, y1 = map(int, m.groups()[:4])
            if pno in ONLY_RIGHT and y0 > ONLY_RIGHT[pno][1] and x0 < ONLY_RIGHT[pno][0]: continue
            chars.append((c[0], x0, y0, x1, y1, li))
    return chars

def find(chars, item, term):
    """원문 문장 전체를 쪽 OCR 글자열과 정렬한 뒤, term 글자들이 대응하는 OCR 글자 범위를 돌려준다."""
    import difflib
    txt = "".join(c[0] for c in chars)
    it, tm = nz(item), nz(term)
    k = it.find(tm)
    if k < 0: return None
    # 문장 전체(길면 term 주변 40자)로 쪽에서 위치를 잡는다
    lo, hi = max(0, k - 40), min(len(it), k + len(tm) + 40)
    seg = it[lo:hi]; kk = k - lo
    a = fuzz.partial_ratio_alignment(seg, txt)
    if a is None or a.score < 70: return None
    w0, w1 = max(0, a.dest_start - 10), min(len(txt), a.dest_end + 10)
    win = txt[w0:w1]
    sm = difflib.SequenceMatcher(None, seg, win, autojunk=False)
    m = {}
    for bi, bj, n in sm.get_matching_blocks():
        for t in range(n): m[bi + t] = w0 + bj + t
    hit = [i for i in range(kk, kk + len(tm)) if i in m]
    if not hit: return None
    i0, i1 = hit[0], hit[-1]
    s0 = m[i0] - (i0 - kk); e0 = m[i1] + (kk + len(tm) - 1 - i1) + 1
    s0, e0 = max(0, s0), min(len(txt), e0)
    sc = a.score * len(hit) / len(tm)
    return (sc, s0, e0) if sc >= 45 else None

def snap(px, W, H, xs, ys, first_x, last_x, pitch):
    """대략 위치를 실제 잉크에 맞춘 상자로 바꾼다. 가로는 첫 글자 시작 ~ 마지막 글자 시작+피치까지만."""
    ink = lambda x, y: px[x, y] < 140
    cy = int(sorted(ys)[len(ys) // 2])
    xa, xb = int(first_x), int(last_x + pitch * 0.92)
    rows = lambda y: sum(ink(x, y) for x in range(max(0, xa), min(W, xb), 2))
    top = bot = cy
    while top > cy - 30 and rows(top - 1) > 0: top -= 1
    while bot < cy + 30 and rows(bot + 1) > 0: bot += 1
    if bot - top < 18: top, bot = cy - 16, cy + 16
    col = lambda x: 0 <= x < W and any(ink(x, y) for y in range(top, bot + 1))
    def to_gap(x, rng):  # x 근처(±rng)에서 잉크 없는 세로줄로 맞춘다
        for k in range(0, int(rng)):
            for xx in (x + k, x - k):
                if not col(xx): return xx
        return x
    return to_gap(xa - 1, pitch * 0.3), top, to_gap(xb, pitch * 0.3), bot

def draw(img, chars, spans):
    d = ImageDraw.Draw(img); px = img.load(); W, H = img.size
    hs = sorted(c[4] - c[2] for c in chars) or [34]
    h0 = hs[len(hs) // 2]
    adv = sorted(b[1] - a[1] for a, b in zip(chars, chars[1:]) if a[5] == b[5] and 0.6 * h0 < b[1] - a[1] < 1.6 * h0)
    pitch = adv[len(adv) // 2] if adv else h0
    for no, s, e, term in spans:
        segs, cur = [], None
        for c in chars[s:e]:
            cy = (c[2] + c[4]) / 2
            ok = c[4] - c[2] <= 1.6 * h0
            if cur and (not ok or (abs(cy - cur["y"][-1]) < 0.7 * h0 and c[1] - cur["x"][-1] < 2.5 * pitch)):
                cur["n"] += 1
                if ok: cur["x"].append(c[1]); cur["y"].append(cy)
            elif ok:
                cur = {"x": [c[1]], "y": [cy], "n": 1}; segs.append(cur)
        # 각 줄 조각에 들어가는 띄어쓰기 수
        letters = [ch for ch in term if not ch.isspace()]
        i = 0
        for g in segs:
            sp, cnt = 0, 0
            while i < len(term) and cnt < g["n"]:
                if term[i].isspace(): sp += 1
                else: cnt += 1
                i += 1
            g["w"] = g["n"] * pitch + sp * 0.32 * pitch
        first = True
        for g in segs:
            x0, y0, x1, y1 = snap(px, W, H, g["x"], g["y"], min(g["x"]), max(max(g["x"]), min(g["x"]) + g["w"] - pitch * 1.15), pitch)
            x0, y0, x1, y1 = x0 - 2, y0 - 4, x1 + 1, y1 + 4
            d.rectangle((x0, y0, x1, y1), fill=255)
            d.line((x0, y1, x1, y1), fill=0, width=3)
            if first:
                d.text((x0 + 3, y0 - 6), str(no), fill=90, font=FONT); first = False

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
                spans.append((no, s, e, t)); ak.append((no, t, p)); no += 1
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
