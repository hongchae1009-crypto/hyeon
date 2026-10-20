"""문제지 쪽 이미지(170 dpi)에서 문항을 잘라 img/A01.png … B11.png로 저장한다.

한 문항이 두 단에 걸치면(A형 5·6번, B형 4번) 단 조각을 위아래로 이어 붙인다.
단 경계에서 넉넉히 자른 뒤 단 구분선·쪽 테두리 같은 긴 선을 지우고, 글자가 있는 영역만 남겨
사방에 같은 흰 여백(PAD)을 붙인다.

사용법: python3 crop_questions.py <쪽 이미지 폴더>   (A-1.png … B-8.png, pdftoppm -r 170)
"""
import os, sys
import numpy as np
from PIL import Image

PAGES = sys.argv[1]
OUT = os.path.join(os.path.dirname(__file__), '..', 'img')
PAD = 28          # px (170 dpi 기준 약 4 mm)
GAP = 24          # 이어 붙이는 조각 사이 간격
INK = 150         # 이보다 어두우면 잉크로 본다
FIRST = {'A-1', 'B-1'}   # 머리말(시험 정보 표)이 있는 쪽

# 문항 번호 순서대로 (쪽, 단[, 아래 끝 비율]) 조각 목록
LAYOUT = {
    'A': [[(f'A-{p}', s, 0.89 if (p, s) == (6, 'R') else 0.905)] for p in range(1, 7) for s in 'LR'],
    'B': [[(f'B-{p}', s, 0.89 if (p, s) == (6, 'L') else 0.905)] for p in range(1, 7) for s in 'LR'][:11],
}


def crop(page, side, bottom_frac=0.905):
    im = Image.open(os.path.join(PAGES, page + '.png')).convert('L')
    w, h = im.size
    mid = w // 2
    first = page in FIRST
    top = int(h * (0.15 if first else 0.05))
    x0, x1 = (int(w * 0.03), mid - 3) if side == 'L' else (mid + 3, int(w * 0.97))
    a = np.array(im.crop((x0, top, x1, int(h * bottom_frac))))
    # 위쪽 가로줄(머리말 표·유의사항 상자·쪽 위 구분선)의 마지막 줄 아래부터 문항이 시작한다
    rule = np.where((a < INK).sum(1) > 0.6 * a.shape[1])[0]
    rule = rule[rule < ((0.15 if side == 'L' else 0.08) if first else 0.03) * h]  # 1쪽 오른쪽 단은 머리말 표 아래 선까지만
    if len(rule):
        a = a[rule[-1] + 4:]
    ink = a < INK
    tall = ink.sum(0) > 0.85 * ink.shape[0]       # 단 구분선·테두리
    ink[:, tall] = False
    a[:, tall] = 255
    rows = np.where(ink.sum(1) > 0)[0]
    cols = np.where(ink.sum(0) > 0)[0]
    return a[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]


MAX_H = 1340      # 한 단(약 160 mm, 0.12 mm/px)에 제목 띠와 함께 들어가는 높이. 넘으면 빈 줄에서 나눈다


def split(canvas):
    """MAX_H보다 긴 이미지를 12 px 이상 비어 있는 줄에서 잘라 여러 조각으로 나눈다."""
    a = np.array(canvas)
    blank = (a < INK).sum(1) == 0
    parts, start = [], 0
    while a.shape[0] - start > MAX_H + 160:   # 조금 넘는 정도면 나누지 않는다
        cut = None
        for y in range(start + MAX_H, start + MAX_H // 3, -1):
            if blank[y - 12:y].all():
                cut = y - 6
                break
        cut = cut or start + MAX_H
        parts.append(a[start:cut])
        start = cut
    parts.append(a[start:])
    out = []
    for p in parts:
        rows = np.where((p < INK).sum(1) > 0)[0]
        p = p[max(rows[0] - PAD, 0):rows[-1] + PAD]
        out.append(Image.fromarray(p))
    return out


for form, questions in LAYOUT.items():
    for i, parts in enumerate(questions, 1):
        pieces = [crop(*p) for p in parts]
        width = max(p.shape[1] for p in pieces)
        height = sum(p.shape[0] for p in pieces) + GAP * (len(pieces) - 1)
        canvas = Image.new('L', (width + 2 * PAD, height + 2 * PAD), 255)
        y = PAD
        for p in pieces:
            canvas.paste(Image.fromarray(p), (PAD, y))
            y += p.shape[0] + GAP
        for k, part in enumerate(split(canvas), 1):
            name = f'{form}{i:02d}' + (f'_{k}' if k > 1 else '') + '.png'
            part.save(os.path.join(OUT, name), optimize=True)
            print(name, part.size)
