"""교재 PDF에서 문항 영역(머리 상자 아래 ~ 쪽 번호 위)을 잘라 PNG로 추출한다.

반환: [{"unit": 단원번호, "year": "2014 A", "page": 교재 쪽, "png": bytes, "w": px, "h": px}, ...]
같은 내용의 중복 쪽과 빈 쪽은 건너뛴다.
"""
import hashlib
import io
import re

import pymupdf as fitz
from PIL import Image, ImageChops

UNIT_NAMES = {
    "결합과 구조": 1, "산과 염기": 2, "알케인과 사이클로알케인": 3, "입체화학": 4,
    "할로젠화 알킬의 친핵성 치환반응": 5, "할로젠화 알킬의 제거반응": 6, "할로젠화 알킬의 제거 반응": 6,
    "알켄": 7, "알카인": 8, "알코올": 9, "에터와 에폭사이드": 10, "벤젠과 방향족성": 11,
    "방향족 화합물의 반응": 12, "알데하이드와 케톤": 13, "카복실산과 그 유도체": 14,
    "카보닐 화합물의 α탄소 치환반응": 15, "카보닐 화합물의 축합반응": 16, "아민": 17,
    "고리형 협동반응": 18, "C-C 결합형성반응": 19, "유기화학실험": 20, "유기 분광": 21,
}


def _header(page):
    year, unit, book = None, None, None
    spans = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            for s in l["spans"]:
                spans.append((s["bbox"], s["text"]))
    top = [t for (bb, t) in spans if bb[3] < 58]
    foot = [(bb, t) for (bb, t) in spans if re.fullmatch(r"\s*-\s*\d+\s*-\s*", t)]
    if not top:
        return None
    joined = re.sub(r"\s+", " ", " ".join(top)).strip()
    hit = max((n for n in UNIT_NAMES if n in joined), key=len, default=None)
    if hit is None:
        raise ValueError(f"알 수 없는 단원명: {joined!r}")
    unit = UNIT_NAMES[hit]
    year = re.sub(r"\s*\d+\s*\.\s*$", "", joined[:joined.index(hit)]).strip()
    year = re.sub(r"\s*\.\s*", ".", year)
    book = int(re.search(r"\d+", foot[0][1]).group()) if foot else None
    foot_top = foot[0][0][1] if foot else page.rect.height - 40
    return year, unit, book, foot_top


def _autocrop(im, pad=12):
    g = im.convert("L")
    bg = Image.new("L", g.size, 255)
    diff = ImageChops.difference(g, bg).point(lambda v: 255 if v > 40 else 0)
    box = diff.getbbox()
    if not box:
        return None
    x0, y0, x1, y1 = box
    return im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))


def extract(pdf_paths, dpi=150):
    out, seen = [], set()
    for path in pdf_paths:
        doc = fitz.open(path)
        for i in range(doc.page_count):
            page = doc[i]
            h = _header(page)
            if h is None:
                continue  # 목차·빈 쪽
            year, unit, book, foot_top = h
            clip = fitz.Rect(0, 57, page.rect.width, foot_top - 3)
            pm = page.get_pixmap(dpi=dpi, clip=clip)
            im = Image.open(io.BytesIO(pm.tobytes("png"))).convert("RGB")
            im = _autocrop(im)
            if im is None:
                continue
            key = hashlib.md5(im.convert("L").resize((120, int(120 * im.height / im.width))).tobytes()).hexdigest()
            if key in seen:
                continue  # 같은 쪽 중복
            seen.add(key)
            # 회색조 + 팔레트로 용량 축소 (빨간 표시 등 색이 있으면 컬러 유지)
            rgb = im.convert("RGB")
            r, g, b = rgb.split()
            colored = ImageChops.difference(r, g).getextrema()[1] > 60 or ImageChops.difference(g, b).getextrema()[1] > 60
            q = rgb.quantize(64) if colored else rgb.convert("L").quantize(16)
            buf = io.BytesIO()
            q.save(buf, "PNG", optimize=True)
            out.append({"unit": unit, "year": year, "page": book, "png": buf.getvalue(), "w": im.width, "h": im.height,
                        "src": f"{path.split('/')[-1][:8]}#{i + 1}"})
    return out


if __name__ == "__main__":
    import sys
    blocks = extract(sys.argv[1:])
    tot = sum(len(b["png"]) for b in blocks)
    from collections import Counter
    print(len(blocks), "blocks", round(tot / 1e6, 1), "MB")
    print(sorted(Counter(b["unit"] for b in blocks).items()))
