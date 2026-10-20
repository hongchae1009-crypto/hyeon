"""반응 메커니즘 그림(굽은 화살표 포함)을 SVG로 만드는 공용 도구.

한 단계(panel) = 한 줄의 분자들(SMILES, '.'로 여러 조각) + 전자 이동 화살표.
원자는 SMILES의 원자 맵 번호([C:1])로 가리키고, 그림에는 번호가 나오지 않는다.
여러 단계를 위에서 아래로 쌓고 단계 사이에 '↓ 시약/설명' 줄을 넣는다.

화살표 지정:
  ('lp', m)        m번 원자의 비공유 전자쌍(원자 바깥쪽에서 출발)
  ('a', m)         m번 원자
  ('b', m1, m2)    m1–m2 결합의 가운데
화살표 = (출발, 도착) 또는 (출발, 도착, 휘는 방향 +1/-1)
"""
import math, re
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D

RED = '#c0392b'
W = 330


def _mol(smi, arrows=()):
    p = Chem.SmilesParserParams()
    p.removeHs = False
    m = Chem.MolFromSmiles(smi, p)
    assert m is not None, smi
    maps = {}
    for a in m.GetAtoms():
        if a.GetAtomMapNum():
            maps[a.GetAtomMapNum()] = a.GetIdx()
            a.SetAtomMapNum(0)
    AllChem.Compute2DCoords(m)
    # 여러 조각(반응물·시약)은 SMILES 순서대로 왼쪽→오른쪽에 나란히 놓는다
    frags = Chem.GetMolFrags(m)
    if len(frags) > 1:
        conf = m.GetConformer()
        frags = sorted(frags, key=min)
        where = {i: k for k, fr in enumerate(frags) for i in fr}
        # 조각 사이를 건너는 화살표의 끝 원자가 상대 조각 쪽을 보도록 좌우로 뒤집는다
        want = {}
        for ar in arrows:
            a1 = maps[ar[0][1]] if ar[0][0] != 'b' else maps[ar[0][1]]
            a2 = maps[ar[1][1]]
            f1, f2 = where[a1], where[a2]
            if f1 != f2:
                want.setdefault(f1, (a1, 1 if f2 > f1 else -1))
                want.setdefault(f2, (a2, 1 if f1 > f2 else -1))
        for k, (atom, direction) in want.items():
            fr = frags[k]
            cx = sum(conf.GetAtomPosition(i).x for i in fr) / len(fr)
            if (conf.GetAtomPosition(atom).x - cx) * direction < 0:
                for i in fr:
                    q = conf.GetAtomPosition(i)
                    conf.SetAtomPosition(i, (2 * cx - q.x, q.y, 0))
        x = 0.0
        for fr in frags:
            xs = [conf.GetAtomPosition(i).x for i in fr]
            ys = [conf.GetAtomPosition(i).y for i in fr]
            dx, dy = x - min(xs), -(min(ys) + max(ys)) / 2
            for i in fr:
                q = conf.GetAtomPosition(i)
                conf.SetAtomPosition(i, (q.x + dx, q.y + dy, 0))
            x += max(xs) - min(xs) + 1.8
    return m, maps


def _pt(d, m, maps, spec, centroid):
    kind = spec[0]
    if kind == 'b':
        p1, p2 = d.GetDrawCoords(maps[spec[1]]), d.GetDrawCoords(maps[spec[2]])
        return ((p1.x + p2.x) / 2, (p1.y + p2.y) / 2), None
    if kind == 'nb':   # 새로 생길 결합 자리(두 원자 사이, 도착 원자 쪽)
        p1, p2 = d.GetDrawCoords(maps[spec[1]]), d.GetDrawCoords(maps[spec[2]])
        return (0.35 * p1.x + 0.65 * p2.x, 0.35 * p1.y + 0.65 * p2.y), None
    i = maps[spec[1]]
    p = d.GetDrawCoords(i)
    if kind == 'lp':
        nb = [d.GetDrawCoords(n.GetIdx()) for n in m.GetAtomWithIdx(i).GetNeighbors()]
        cx, cy = (sum(q.x for q in nb) / len(nb), sum(q.y for q in nb) / len(nb)) if nb else centroid
        vx, vy = p.x - cx, p.y - cy
        L = math.hypot(vx, vy) or 1
        return (p.x + 13 * vx / L, p.y + 13 * vy / L), None
    return (p.x, p.y), 'atom'


def _arrow(s, e, side, centroid, shorten_end):
    (x1, y1), (x2, y2) = s, e
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    if shorten_end:
        x2, y2 = x2 - 10 * dx / L, y2 - 10 * dy / L
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    px, py = -dy / L, dx / L
    if side == 0:
        if L > 70:   # 조각 사이를 건너는 긴 화살표는 위로 휘게(아래 설명 글자와 겹치지 않게)
            side = 1 if py < 0 else -1
        else:        # 짧은 화살표는 분자 바깥쪽으로
            side = 1 if (px * (mx - centroid[0]) + py * (my - centroid[1])) > 0 else -1
    k = max(16, min(0.4 * L, 45)) * side
    cx, cy = mx + px * k, my + py * k
    tx, ty = x2 - cx, y2 - cy
    T = math.hypot(tx, ty) or 1
    ux, uy = tx / T, ty / T
    h1 = (x2 - 7 * ux + 3.5 * uy, y2 - 7 * uy - 3.5 * ux)
    h2 = (x2 - 7 * ux - 3.5 * uy, y2 - 7 * uy + 3.5 * ux)
    return (f"<path d='M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}' fill='none' stroke='{RED}' stroke-width='1.6'/>"
            f"<polygon points='{x2:.1f},{y2:.1f} {h1[0]:.1f},{h1[1]:.1f} {h2[0]:.1f},{h2[1]:.1f}' fill='{RED}'/>")


def panel(smi, arrows=(), h=135, legend=''):
    m, maps = _mol(smi, arrows)
    body = h - (20 if legend else 0)
    d = rdMolDraw2D.MolDraw2DSVG(W, body)
    o = d.drawOptions()
    o.bondLineWidth = 1.6
    o.fixedBondLength = 24          # 모든 단계에서 같은 크기
    o.padding = 0.1
    o.annotationFontScale = 0.7
    d.DrawMolecule(m)
    pts = [d.GetDrawCoords(i) for i in range(m.GetNumAtoms())]
    centroid = (sum(p.x for p in pts) / len(pts), sum(p.y for p in pts) / len(pts))
    extra = ''
    for ar in arrows:
        s, _ = _pt(d, m, maps, ar[0], centroid)
        tgt = ar[1]
        if ar[0][0] == 'b' and tgt[0] == 'a' and tgt[1] in ar[0][1:]:
            tgt = ('lp', tgt[1])   # 결합 전자쌍이 이웃 원자로 갈 때: 원자 바깥쪽(새 비공유 전자쌍 자리)으로
        e, kind = _pt(d, m, maps, tgt, centroid)
        extra += _arrow(s, e, ar[2] if len(ar) > 2 else 0, centroid, kind == 'atom')
    d.FinishDrawing()
    svg = d.GetDrawingText()
    if legend:
        svg = svg.replace(f"height='{body}px'", f"height='{h}px'").replace(f"viewBox='0 0 {W} {body}'", f"viewBox='0 0 {W} {h}'")
        extra += (f"<text x='{W/2}' y='{h-5}' text-anchor='middle' font-size='12.5' fill='#374151' "
                  f"font-family='Noto Sans KR, sans-serif'>{legend}</text>")
    svg = svg.replace('</svg>', extra + '</svg>')
    return re.sub(r"<\?xml[^>]*\?>\s*", '', svg), h


def mechanism(path, steps):
    """steps: panel(...) 결과와 '↓ 설명' 문자열을 차례로 담은 목록."""
    parts, y = [], 0
    for st in steps:
        if isinstance(st, str):
            parts.append(f"<text x='{W/2}' y='{y+17}' text-anchor='middle' font-size='13' fill='#1f2933' "
                         f"font-family='Noto Sans KR, sans-serif'>{st}</text>")
            y += 26
        else:
            svg, h = st
            parts.append(svg.replace('<svg ', f"<svg x='0' y='{y}' ", 1))
            y += h
    out = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {y}' width='{W}' height='{y}'>"
           f"<rect width='{W}' height='{y}' fill='white'/>{''.join(parts)}</svg>")
    open(path, 'w').write(out)
    print(path.split('/')[-1], y)
