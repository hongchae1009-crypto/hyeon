# -*- coding: utf-8 -*-
"""컷아웃 도구: (1) 기출 문항 쪽 그림 잘라 내기, (2) 2022 교육과정 스캔에서 지정한 문장 범위 잘라 내기(OCR로 위치 찾기)."""
import io, json, pathlib, re, subprocess, sys
import numpy as np, pymupdf
from PIL import Image
from rapidfuzz import fuzz
HERE = pathlib.Path(__file__).parent
UP = pathlib.Path("/root/.claude/uploads/f884566e-9634-59dc-ada1-6c4980c71812")
CUR_A = next(UP.glob("02bbd04b-*")); CUR_B = next(UP.glob("c884542d-*"))
EXAM = HERE.parent / "화교론_기출_14-26.pdf"
CACHE = HERE / "_cache"; CACHE.mkdir(exist_ok=True)
DPI = 220
_docs = {}
def _doc(p):
    if p not in _docs: _docs[p] = pymupdf.open(p)
    return _docs[p]

def cur_page(p):
    """교육과정 책 쪽 p의 그림(회색조). 앞 파일: 펼침 i = (2i-1, 2i)쪽, 뒤 파일: 펼침 j = (45+2j, 46+2j)쪽."""
    f = CACHE / f"cur{p}.png"
    if not f.exists():
        d, i = (_doc(CUR_A), (p + 1) // 2) if p <= 44 else (_doc(CUR_B), (p - 45) // 2)
        r = d[i].rect; w = r.width / 2
        clip = pymupdf.Rect(0, 0, w, r.height) if p % 2 else pymupdf.Rect(w, 0, r.width, r.height)
        d[i].get_pixmap(dpi=DPI, clip=clip, colorspace=pymupdf.csGRAY).save(f)
    return Image.open(f)

def lines(p):
    """OCR 줄 목록 [(글자(공백 제거), x0, y0, x1, y1)] — 캐시."""
    f = CACHE / f"cur{p}.json"
    if not f.exists():
        im = cur_page(p); buf = io.BytesIO(); im.save(buf, "PNG")
        tsv = subprocess.run(["tesseract", "-", "-", "-l", "kor", "--psm", "4", "tsv"], input=buf.getvalue(), capture_output=True).stdout.decode("utf-8", "ignore")
        L = {}
        for row in tsv.splitlines()[1:]:
            c = row.split("\t")
            if len(c) < 12 or not c[11].strip(): continue
            key = (c[2], c[3], c[4]); x, y, w, h = map(int, c[6:10])
            t, a, ws = L.get(key, ["", [9e9, 9e9, 0, 0], []])
            L[key] = [t + c[11], [min(a[0], x), min(a[1], y), max(a[2], x + w), max(a[3], y + h)], ws + [[c[11], x, x + w]]]
        out = sorted([(re.sub(r"\s+", "", t), *b, ws) for t, b, ws in L.values()], key=lambda r: (r[2], r[1]))
        f.write_text(json.dumps(out, ensure_ascii=False))
    return json.loads(f.read_text())

norm = lambda s: re.sub(r"[\s・·•ㆍ‧∙'‘’\"“”]", "", s)
def find(p, pat, after=0):
    """pat(원문 문장 앞부분)과 가장 비슷한 줄의 번호."""
    L = lines(p); q = norm(pat); best = (0, None)
    for i, r in enumerate(L):
        if r[2] < after: continue
        sc = fuzz.partial_ratio(q[:28], norm(r[0])) if len(norm(r[0])) >= 6 else 0
        if sc > best[0]: best = (sc, i)
    return best

def _word_at(ws, target, start=True):
    """단어 상자 목록에서 target 글자열이 시작(또는 끝)나는 단어."""
    t = norm(target); acc, spans = "", []
    for w in ws:
        n = norm(w[0]); spans.append((len(acc), len(acc) + len(n), w)); acc += n
    k = acc.find(t)
    if k < 0: return None
    pos = k if start else k + len(t) - 1
    return next((w for a, b, w in spans if a <= pos < b), None)

def cur_cut(p, start, end=None, pad=10, from_word=None, to_word=None, cont=True):
    """책 p쪽에서 start 문장이 시작하는 줄 ~ end 문장이 있는 줄까지 잘라 낸다(가로는 본문 틀 안쪽 전체)."""
    im = cur_page(p); L = lines(p)
    s_sc, si = find(p, start)
    if end:
        e_sc, ei = find(p, end, after=L[si][2])
    else:
        e_sc, ei = s_sc, si
    a = np.array(im) < 150; H, W = a.shape
    bc = np.where(a.sum(0) > 0.7 * H)[0]
    x0 = bc[bc < W / 2].max() + 10 if (bc < W / 2).any() else 0
    x1 = bc[bc > W / 2].min() - 10 if (bc > W / 2).any() else W
    # 끝 줄의 문단이 다음 줄로 이어지면(들여 쓴 줄) 문단 끝까지
    lh = L[ei][4] - L[ei][2]; px0 = L[ei][1]; j = ei
    while (cont and j + 1 < len(L) and not L[j][0].endswith("다.") and L[j + 1][2] - L[j][4] < 1.3 * lh
           and L[j + 1][1] > px0 + 12 and not re.match(r"^[•＊*\[(<]", L[j + 1][0])):
        j += 1
    ei = j
    y0, y1 = L[si][2] - pad, L[ei][4] + pad
    # 줄 끝이 다음 줄과 붙어 있으면(같은 문단 계속) 아래로 늘린다
    sub = a[y1:y1 + 60, x0:x1].sum(1)
    im = im.copy()
    from PIL import ImageDraw
    dr = ImageDraw.Draw(im)
    if from_word:  # 첫 줄에서 from_word가 든 단어 앞부분 지우기
        w = _word_at(L[si][5], from_word, start=True)
        if w: dr.rectangle((0, L[si][2] - pad, w[1] - 4, L[si][4] + 2), fill=255)
    if to_word:  # 끝 줄에서 to_word가 든 단어 뒷부분 지우기
        w = _word_at(L[ei][5], to_word, start=False)
        if w: dr.rectangle((w[2] + 4, L[ei][2] - 2, W, L[ei][4] + pad), fill=255)
            # 다음 줄이 비치지 않게 아래 여백도 지움
        dr.rectangle((0, L[ei][4] + 3, W, L[ei][4] + pad + 2), fill=255)
    dr.rectangle((0, y0 - 2, W, L[si][2] - 3), fill=255)      # 위 줄 비침 지우기
    dr.rectangle((0, L[ei][4] + 3, W, y1 + 2), fill=255)      # 아래 줄 비침 지우기
    sub_im = im.crop((x0, y0, x1, y1))
    # 틀의 세로선 지우기
    arr = np.array(sub_im); vb = (arr < 150).sum(0) > 0.8 * arr.shape[0]
    arr[:, vb] = 255; sub_im = Image.fromarray(arr)
    # 가로 여백 줄이기
    s = np.array(sub_im) < 150
    cols = np.where(s.any(0))[0]
    if len(cols): sub_im = sub_im.crop((max(0, cols.min() - 6), 0, min(s.shape[1], cols.max() + 7), s.shape[0]))
    return sub_im, (s_sc, e_sc)

def exam_cut(idx):
    """기출 PDF 쪽(0부터) → 문항 그림. 가운데 세로선·쪽 번호·연도 제목 상자를 빼고, 두 단에 걸친 문항은 원래 배치 그대로."""
    f = CACHE / f"exam{idx}.png"
    if f.exists(): return Image.open(f)
    pm = _doc(EXAM)[idx].get_pixmap(dpi=200, colorspace=pymupdf.csGRAY)
    im = Image.frombytes("L", (pm.width, pm.height), pm.samples)
    a = np.array(im) < 160; H, W = a.shape
    vc = np.where(a.sum(0) > 0.6 * H)[0]  # 가운데 세로선
    arr = np.array(im)
    for x in vc: arr[:, max(0, x - 2):x + 3] = 255
    im = Image.fromarray(arr); a = arr < 160
    # 연도 제목 상자: 맨 처음 잉크가 긴 가로선이면 상자 아래 선까지 건너뛴다
    rs = a.sum(1); first = int(np.argmax(rs > 0))
    if rs[first] > 0.3 * W:
        nxt = [y for y in range(first + 20, min(H, first + 220)) if rs[y] > 0.3 * W]
        if nxt: a[:nxt[-1] + 4] = False
    rows = a.any(1); bands, s, gap = [], None, 0
    for y, r in enumerate(list(rows) + [False] * 40):
        if r:
            s = y if s is None else s; gap = 0; e = y
        elif s is not None:
            gap += 1
            if gap >= 35: bands.append((s, e)); s = None
    # 쪽 번호(맨 아래 작은 띠), 연도 제목 상자(맨 위 작은 띠, 긴 가로선 포함) 제외
    if bands and bands[-1][0] > 0.85 * H and bands[-1][1] - bands[-1][0] < 60: bands.pop()
    y0, y1 = bands[0][0], bands[-1][1]
    cols = np.where(a[y0:y1 + 1].any(0))[0]
    out = im.crop((cols.min() - 8, y0 - 8, cols.max() + 9, y1 + 9))
    out.save(f); return out
