"""문제지 쪽 이미지(170 dpi)에서 문항을 한 단씩 잘라 img/A01.png … B11.png로 저장한다.

단 경계에서 넉넉히 자른 뒤 단 구분선·쪽 테두리 같은 세로줄을 지우고, 글자가 있는 영역만 남겨
사방에 같은 흰 여백(PAD)을 붙인다. 그래서 모든 문항이 같은 배율·같은 여백을 갖는다.

사용법: python3 crop_questions.py <쪽 이미지 폴더>   (A-1.png … B-6.png, pdftoppm -r 170)
"""
import os, sys
import numpy as np
from PIL import Image

PAGES = sys.argv[1]
OUT = os.path.join(os.path.dirname(__file__), '..', 'img')
PAD = 28          # px (170 dpi 기준 약 4 mm)
INK = 150         # 이보다 어두우면 잉크로 본다

# (쪽 파일, 단) 순서 = 문항 번호 순서. 한 단에 한 문항씩 배치된 문제지다.
LAYOUT = {'A': [(p, s) for p in range(1, 7) for s in 'LR'],
          'B': [(p, s) for p in range(1, 7) for s in 'LR'][:11]}


def crop(page, side, first):
    im = Image.open(page).convert('L')
    w, h = im.size
    mid = w // 2
    # 머리말(시험 정보 표)·바닥글을 피하는 위아래 범위
    top = int(h * (0.15 if first else 0.072))
    bottom = int(h * 0.905)
    x0, x1 = (int(w * 0.03), mid - 3) if side == 'L' else (mid + 3, int(w * 0.97))
    a = np.array(im.crop((x0, top, x1, bottom)))
    if first:
        # 1쪽: 머리말 표·유의사항 상자의 마지막 가로줄 아래부터 문항이 시작한다
        rule = np.where((a < INK).sum(1) > 0.6 * a.shape[1])[0]
        rule = rule[rule < 0.15 * h]  # 머리말·유의사항 상자(쪽 높이의 위 30 %)까지만 본다
        if len(rule):
            a = a[rule[-1] + 4:]
    ink = a < INK
    # 세로로 길게 이어진 줄(단 구분선, 테두리)은 지운다
    tall = ink.sum(0) > 0.85 * ink.shape[0]
    ink[:, tall] = False
    # 가로로 긴 줄(머리말 아래 구분선 등)도 위쪽 120 px 안에서는 지운다
    wide = ink.sum(1) > 0.85 * ink.shape[1]
    wide[120:] = False
    ink[wide, :] = False
    rows = np.where(ink.sum(1) > 0)[0]
    cols = np.where(ink.sum(0) > 0)[0]
    r0, r1, c0, c1 = rows[0], rows[-1] + 1, cols[0], cols[-1] + 1
    a[:, tall] = 255
    a[wide, :] = 255
    body = Image.fromarray(a[r0:r1, c0:c1])
    canvas = Image.new('L', (body.width + 2 * PAD, body.height + 2 * PAD), 255)
    canvas.paste(body, (PAD, PAD))
    return canvas


for form, cells in LAYOUT.items():
    for i, (p, side) in enumerate(cells, 1):
        img = crop(os.path.join(PAGES, f'{form}-{p}.png'), side, p == 1)
        name = f'{form}{i:02d}.png'
        img.save(os.path.join(OUT, name), optimize=True)
        print(name, img.size)
