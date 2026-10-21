"""문제지 쪽 이미지(170 dpi)에서 문항을 잘라 img/A01.png … B11.png로 저장한다.

한 문항이 두 단에 걸치면(A형 5·6·7번, B형 3·4번) 단 조각을 위아래로 이어 붙인다.
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
FIRST = {'A-3', 'B-3'}   # 머리말(시험 정보 표)이 있는 쪽

# 문항 번호 순서대로 (쪽, 단[, 아래 끝 비율]) 조각 목록
LAYOUT = {
    'A': [[('A-3', 'L')], [('A-3', 'R')], [('A-4', 'L')], [('A-4', 'R')],
          [('A-5', 'L'), ('A-5', 'R')], [('A-6', 'L'), ('A-6', 'R')],
          [('A-7', 'L'), ('A-7', 'R', 0.50)], [('A-7', 'R', 0.905, 0.52)],   # 7번은 오른쪽 단 위까지, 8번은 그 아래
          [('A-8', 'L')], [('A-8', 'R')], [('A-9', 'L')], [('A-9', 'R')]],
    'B': [[('B-3', 'L')], [('B-3', 'R')], [('B-4', 'L'), ('B-4', 'R')], [('B-5', 'L'), ('B-5', 'R')],
          [('B-6', 'L')], [('B-6', 'R')], [('B-7', 'L')], [('B-7', 'R')],
          [('B-8', 'L')], [('B-8', 'R')], [('B-9', 'L')]],
}


def crop(page, side, bottom_frac=0.905, top_frac=None):
    im = Image.open(os.path.join(PAGES, page + '.png')).convert('L')
    w, h = im.size
    mid = w // 2
    first = page in FIRST
    top = int(h * (top_frac if top_frac is not None else (0.15 if first else 0.04)))
    x0, x1 = (int(w * 0.03), mid - 3) if side == 'L' else (mid + 3, int(w * 0.97))
    a = np.array(im.crop((x0, top, x1, int(h * bottom_frac))))
    # 위쪽 가로줄(머리말 표·유의사항 상자·쪽 위 구분선)의 마지막 줄 아래부터 문항이 시작한다
    rule = np.where((a < INK).sum(1) > 0.6 * a.shape[1])[0]
    # 1쪽: 왼쪽 단은 유의사항 상자 아래(쪽 높이 26 %), 오른쪽 단은 머리말 구분선(23 %)까지만 본다.
    # 그보다 아래의 가로줄은 문항 속 상자 테두리이므로 자르는 기준으로 쓰지 않는다.
    lim = 0 if top_frac is not None else ((0.115 if side == 'L' else 0.08) if first else 0.04)
    rule = rule[rule < lim * h]
    if len(rule):
        a = a[rule[-1] + 4:]
    ink = a < INK
    tall = ink.sum(0) > 0.85 * ink.shape[0]       # 단 구분선·테두리
    ink[:, tall] = False
    a[:, tall] = 255
    rows = np.where(ink.sum(1) > 0)[0]
    # 맨 아래 덩어리가 폭 40 px 미만이면 쪽 번호이므로 버린다
    gaps = np.where(np.diff(rows) > 20)[0]
    if len(gaps):
        tail = rows[gaps[-1] + 1:]
        tc = np.where(ink[tail[0]:tail[-1] + 1].sum(0) > 0)[0]
        if tc[-1] - tc[0] < 40:
            ink[tail[0]:] = False
            rows = rows[:gaps[-1] + 1]
    cols = np.where(ink.sum(0) > 0)[0]
    return a[rows[0]:rows[-1] + 1, cols[0]:cols[-1] + 1]


MAX_H = 1340      # 한 단(약 160 mm, 0.12 mm/px)에 제목 띠와 함께 들어가는 높이. 넘으면 빈 줄에서 나눈다


def split(canvas):
    """MAX_H보다 긴 이미지를 12 px 이상 비어 있는 줄에서 잘라 여러 조각으로 나눈다."""
    a = np.array(canvas)
    blank = (a < INK).sum(1) == 0
    parts, start = [], 0
    while a.shape[0] - start > MAX_H + 160:   # 조금 넘는 정도면 나누지 않는다
        rem = a.shape[0] - start
        n = -(-rem // MAX_H)                   # 남은 조각 수
        target = min(MAX_H, -(-rem // n) + 60)  # 조각 길이를 고르게(짧은 꼬리 조각 방지)
        cut = None
        for rng in (range(start + target, start + target // 3, -1), range(start + target, start + MAX_H)):
            for y in rng:
                if blank[y - 12:y].all():
                    cut = y - 6
                    break
            if cut:
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
