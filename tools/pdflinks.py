"""완성된 PDF에 내부 하이퍼링크와 책갈피(목차)를 넣는다.

- 앞쪽 색인·목차의 각 행 → 해당 문항 쪽
- 각 문항 쪽의 '▲ 색인' 글자 → 첫 쪽(색인)
- 책갈피: 단원(또는 연도) → 문항
"""
import pathlib
import re

import pymupdf as fitz

BACK = "▲ 색인"


def _save(doc, path):
    tmp = str(path) + ".tmp"
    doc.save(tmp, garbage=1, deflate=True)
    doc.close()
    pathlib.Path(tmp).replace(path)


def _goto(page, rect, target):
    page.insert_link({"kind": fitz.LINK_GOTO, "page": target, "from": rect, "to": fitz.Point(0, 0)})


def link_rows_lastcol(doc, k, targets):
    """색인 표: 마지막 열(쪽)의 숫자를 위→아래로 모아 각 행 전체를 링크로"""
    cells = []
    for pno in range(k):
        page = doc[pno]
        # '쪽' 머리 칸의 x 범위에 있는 숫자만 (주제 칸 끝의 숫자 제외)
        head = [w for w in page.get_text("words") if w[4] == "쪽"]
        if not head:
            continue
        hx0, hx1 = head[0][0] - 12, head[0][2] + 12
        words = [w for w in page.get_text("words") if w[4].isdigit() and w[0] >= hx0 and w[2] <= hx1 + 6 and w[1] > head[0][3]]
        words.sort(key=lambda w: w[1])
        for i, w in enumerate(words):
            nxt = words[i + 1][1] if i + 1 < len(words) else None
            cells.append((pno, w, nxt))
    assert len(cells) == len(targets), (len(cells), len(targets))
    for (pno, w, nxt), t in zip(cells, targets):
        page = doc[pno]
        y1 = (nxt - 2) if nxt else w[3] + 2
        _goto(page, fitz.Rect(30, w[1] - 2, page.rect.width - 30, max(y1, w[3] + 1)), t)


def link_rows_text(doc, k, rows, min_y=130):
    """목차: 행 제목 글자를 찾아 링크 (rows = [(제목, 대상 쪽 index)]). min_y 위쪽(제목·부제목)은 건너뜀"""
    used = set()
    for label, t in rows:
        for pno in range(k):
            for r in doc[pno].search_for(label):
                if pno == 0 and r.y0 < min_y:
                    continue
                key = (pno, round(r.y0), round(r.x0))
                if key in used:
                    continue
                used.add(key)
                # 같은 줄의 점선·쪽 번호까지 포함하도록 오른쪽으로 넓힘
                col_right = doc[pno].rect.width / 2 - 10 if r.x0 < doc[pno].rect.width / 2 else doc[pno].rect.width - 40
                _goto(doc[pno], fitz.Rect(r.x0 - 2, r.y0 - 1, col_right, r.y1 + 1), t)
                break
            else:
                continue
            break


def back_links(doc, k):
    for pno in range(k, doc.page_count):
        for r in doc[pno].search_for(BACK):
            _goto(doc[pno], r + (-3, -2, 3, 2), 0)


def finalize(pdf, k, index_targets=None, toc_rows=None, outline=None):
    """k: 앞쪽(색인·목차) 쪽 수. index_targets: 색인 행 순서대로 대상 쪽(0부터).
    toc_rows: [(제목, 대상 쪽)] 글자 검색 방식. outline: [[level, title, page(1부터)], ...]"""
    doc = fitz.open(pdf)
    if index_targets:
        link_rows_lastcol(doc, k, index_targets)
    if toc_rows:
        link_rows_text(doc, k, toc_rows)
    back_links(doc, k)
    if outline:
        doc.set_toc(outline)
    _save(doc, pdf)


def plain(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", str(s))).strip()
