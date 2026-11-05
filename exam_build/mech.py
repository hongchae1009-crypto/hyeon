"""굽은 화살표 반응 메커니즘 그림 도구 (RDKit 구조식 + SVG 전자 이동 화살표).

기본 사용
---------
SMILES 에 원자 맵 번호를 붙여 화살표가 가리킬 원자를 지정한다(맵 번호는 그림에 표시되지 않음).
명시적 H 가 필요하면 [H:5] 처럼 맵 번호를 달아 쓴다.

    from mech import step, mechanism, ar
    s1 = step('[OH-:1].[H:2][CH2:3][C:4](=[O:5])C',
              arrows=[ar('lp', 1, 'a', 2),          # O1 비공유 전자쌍 → H2
                      ar('b', (3, 2), 'm', (3, 4)),  # C3–H2 결합 → C3–C4 사이(π 형성)
                      ar('b', (4, 5), 'a', 5)],      # C4=O5 π 결합 → O5
              lp=[1, 5], caption='① 엔올레이트 형성')
    html = mechanism(s1, ('⇌', ''), step('C=C([O-])C', caption='엔올레이트'))

화살표 출발점 종류: 'lp' 원자의 비공유 전자쌍(원자 맵 번호), 'b' 결합(두 맵 번호 튜플)
화살표 도착점 종류: 'a' 원자, 'm' 두 원자 사이(새 결합이 생길 자리), 'b' 결합 중점
옵션: side=+1/-1 (휘는 방향 강제), bend=0.0~0.8 (곡률), fish=True (반쪽 화살촉, 라디칼 단일 전자)
step(..., lp=[맵...]) 비공유 전자쌍 점 표시, rad=[맵...] 홀전자 점, notes={맵: '㉠'} 원자 옆 주석,
     dash=[(i,j)...] 형성/절단 중인 결합을 점선으로 (전이 상태용), hl=[맵...] 회색 원 강조,
     rotate=각도(도), flip=True(좌우 반전), scale=결합 길이(px)
mechanism(*parts): step() 결과와 ('→' | '⇌' | '⟶', 시약 위, 시약 아래) 튜플을 섞어 한 줄 이상으로 배치
"""
import math
import re

from rdkit import Chem
from rdkit.Chem import rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Geometry import Point2D

rdDepictor.SetPreferCoordGen(True)


def ar(src_kind, src, dst_kind, dst, side=0, bend=0.45, fish=False):
    return dict(sk=src_kind, s=src, dk=dst_kind, d=dst, side=side, bend=bend, fish=fish)


def _parse(smiles):
    ps = Chem.SmilesParserParams()
    ps.removeHs = False
    mol = Chem.MolFromSmiles(smiles, ps)
    if mol is None:
        raise ValueError('bad SMILES: ' + smiles)
    idx = {}
    for a in mol.GetAtoms():
        m = a.GetAtomMapNum()
        if m:
            if m in idx:
                raise ValueError(f'duplicate map number {m} in {smiles}')
            idx[m] = a.GetIdx()
            a.SetAtomMapNum(0)
    return mol, idx


def _transform(mol, rotate, flip):
    conf = mol.GetConformer()
    th = math.radians(rotate or 0)
    for i in range(mol.GetNumAtoms()):
        p = conf.GetAtomPosition(i)
        x, y = p.x, p.y
        if flip:
            x = -x
        x, y = x * math.cos(th) - y * math.sin(th), x * math.sin(th) + y * math.cos(th)
        conf.SetAtomPosition(i, (x, y, 0))


def _unit(vx, vy):
    n = math.hypot(vx, vy) or 1.0
    return vx / n, vy / n


def _free_dir(P, mol, i, k=0):
    """원자 i 에서 이웃이 없는 방향(단위벡터). k 번째 후보(여러 전자쌍 배치용)."""
    a = mol.GetAtomWithIdx(i)
    nb = [n.GetIdx() for n in a.GetNeighbors()]
    x0, y0 = P[i]
    if not nb:
        angs = [math.pi / 2 * 3 + k * math.pi * 2 / 3]
        return math.cos(angs[0]), math.sin(angs[0])
    vecs = [_unit(P[j][0] - x0, P[j][1] - y0) for j in nb]
    # 후보 각도 36개 중 이웃과의 최소 각거리가 큰 순서
    cands = []
    for t in range(36):
        ang = t * math.pi / 18
        cx, cy = math.cos(ang), math.sin(ang)
        mind = min(math.acos(max(-1, min(1, cx * vx + cy * vy))) for vx, vy in vecs)
        cands.append((mind, ang))
    cands.sort(reverse=True)
    picked = []
    for mind, ang in cands:
        if all(abs((ang - p + math.pi) % (2 * math.pi) - math.pi) > math.radians(70) for p in picked):
            picked.append(ang)
        if len(picked) > k:
            break
    ang = picked[min(k, len(picked) - 1)]
    return math.cos(ang), math.sin(ang)


def _layout_frags(mol, gap=1.6, frag_dy=None, frag_dx=None, layout='h'):
    """조각(분자)들을 SMILES 순서대로 배치. layout='h' 왼쪽→오른쪽(세로 중앙), 'v' 위→아래(가로 중앙).
    frag_dx/frag_dy={조각번호: 이동량(결합 길이 단위, y는 위쪽이 +)} 로 미세 조정."""
    frags = Chem.GetMolFrags(mol)
    conf = mol.GetConformer()
    pos = 0.0
    for k, fr in enumerate(frags):
        xs = [conf.GetAtomPosition(i).x for i in fr]
        ys = [conf.GetAtomPosition(i).y for i in fr]
        if layout == 'v':
            dx = -(min(xs) + max(xs)) / 2
            dy = pos - max(ys)
            pos -= (max(ys) - min(ys)) + gap
        else:
            dx = pos - min(xs)
            dy = -(min(ys) + max(ys)) / 2
            pos += (max(xs) - min(xs)) + gap
        dx += (frag_dx or {}).get(k, 0)
        dy += (frag_dy or {}).get(k, 0)
        for i in fr:
            q = conf.GetAtomPosition(i)
            conf.SetAtomPosition(i, (q.x + dx, q.y + dy, 0))


def _arrow_path(x0, y0, qx, qy, x1, y1, fish, side):
    """2차 베지어 곡선 + 화살촉(끝 접선 방향). fish=True 면 반쪽 화살촉."""
    tx, ty = _unit(x1 - qx, y1 - qy)
    hl_, hw = 6.5, 3.2
    bx, by = x1 - tx * hl_, y1 - ty * hl_
    px_, py_ = -ty, tx
    if fish:
        head = f'M{x1:.1f},{y1:.1f} L{bx + px_ * hw * side:.1f},{by + py_ * hw * side:.1f} L{bx:.1f},{by:.1f} z'
    else:
        head = (f'M{x1:.1f},{y1:.1f} L{bx + px_ * hw:.1f},{by + py_ * hw:.1f} '
                f'L{bx - px_ * hw:.1f},{by - py_ * hw:.1f} z')
    return (f'<path d="M{x0:.1f},{y0:.1f} Q{qx:.1f},{qy:.1f} {bx:.1f},{by:.1f}" fill="none" stroke="#c00" stroke-width="1.25"/>'
            f'<path d="{head}" fill="#c00"/>')


def step(smiles, arrows=(), lp=(), rad=(), notes=None, dash=(), hl=(), rotate=0, flip=False,
         scale=24, caption='', box_label='', gap=1.6, frag_rot=None, frag_flip=(), frag_dy=None, frag_dx=None, layout='h', labels=None):
    """labels={맵: 'Ph'} 원자를 축약 기호로 표시(예: [*:7] 더미 원자에 'Ph', P 원자에 'Ph<sub>3</sub>P').
    frag_rot={조각번호: 각도}, frag_flip=(조각번호,...): 조각별 회전/반전, frag_dy={조각번호: 세로 이동(결합 길이 단위)}"""
    mol, idx = _parse(smiles)
    rdDepictor.Compute2DCoords(mol)
    if frag_rot or frag_flip:
        conf = mol.GetConformer()
        for k, fr in enumerate(Chem.GetMolFrags(mol)):
            th = math.radians((frag_rot or {}).get(k, 0)); fl = k in frag_flip
            cx0 = sum(conf.GetAtomPosition(i).x for i in fr) / len(fr)
            cy0 = sum(conf.GetAtomPosition(i).y for i in fr) / len(fr)
            for i in fr:
                q = conf.GetAtomPosition(i); x, y = q.x - cx0, q.y - cy0
                if fl: x = -x
                x, y = x * math.cos(th) - y * math.sin(th), x * math.sin(th) + y * math.cos(th)
                conf.SetAtomPosition(i, (x + cx0, y + cy0, 0))
    _transform(mol, rotate, flip)
    _layout_frags(mol, gap, frag_dy, frag_dx, layout)
    for a in mol.GetAtoms():
        a.SetNumRadicalElectrons(0)
    conf = mol.GetConformer()
    xs = [conf.GetAtomPosition(i).x for i in range(mol.GetNumAtoms())]
    ys = [conf.GetAtomPosition(i).y for i in range(mol.GetNumAtoms())]
    pad = 3.0 if arrows else 2.4
    w = int((max(xs) - min(xs)) * scale + pad * scale)
    h = int((max(ys) - min(ys)) * scale + pad * scale)
    w, h = max(w, 50), max(h, 44)
    d = rdMolDraw2D.MolDraw2DSVG(w, h)
    o = d.drawOptions()
    o.useBWAtomPalette()
    o.clearBackground = False
    o.bondLineWidth = 1.3
    o.fixedBondLength = scale
    o.fixedFontSize = int(scale * 0.62)
    o.padding = 0.12 if arrows else 0.06
    o.addStereoAnnotation = False
    m2 = Chem.Mol(mol)
    if labels:
        for k, v in labels.items():
            m2.GetAtomWithIdx(idx[k]).SetProp('atomLabel', str(v))
    if notes:
        for k, v in notes.items():
            m2.GetAtomWithIdx(idx[k]).SetProp('atomNote', str(v))
    for (i, j) in dash:
        b = m2.GetBondBetweenAtoms(idx[i], idx[j])
        if b is not None:
            pass  # 점선은 오버레이로 그림
    d.DrawMolecule(m2)
    P = {}
    for i in range(mol.GetNumAtoms()):
        pt = d.GetDrawCoords(i)
        P[i] = (pt.x, pt.y)
    d.FinishDrawing()
    svg = d.GetDrawingText()
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg).replace("<!-- END OF HEADER -->", "")
    svg = re.sub(r"<rect[^>]*style='opacity:1.0;fill:#FFFFFF[^>]*>\s*</rect>", "", svg)

    bl = scale
    ov = []
    cx = sum(p[0] for p in P.values()) / len(P)
    cy = sum(p[1] for p in P.values()) / len(P)
    used_lp = {}

    def lp_point(i):
        k = used_lp.get(i, 0)
        ux, uy = _free_dir(P, mol, i, k)
        return P[i][0] + ux * bl * 0.42, P[i][1] + uy * bl * 0.42, ux, uy

    # 비공유 전자쌍 / 홀전자 점
    for m in lp:
        i = idx[m]
        for k in range(1 if isinstance(m, int) else 1):
            ux, uy = _free_dir(P, mol, i, 0)
            px, py = P[i][0] + ux * bl * 0.40, P[i][1] + uy * bl * 0.40
            tx, ty = -uy, ux
            for s in (-1, 1):
                ov.append(f'<circle cx="{px + tx * s * 2.6:.1f}" cy="{py + ty * s * 2.6:.1f}" r="1.35" fill="#000"/>')
    for m in rad:
        i = idx[m]
        ux, uy = _free_dir(P, mol, i, 0)
        ov.append(f'<circle cx="{P[i][0] + ux * bl * 0.40:.1f}" cy="{P[i][1] + uy * bl * 0.40:.1f}" r="1.5" fill="#000"/>')
    for m in hl:
        i = idx[m]
        ov.append(f'<circle cx="{P[i][0]:.1f}" cy="{P[i][1]:.1f}" r="{bl * 0.42:.1f}" fill="none" stroke="#777" stroke-width="1" stroke-dasharray="2,1.5"/>')
    for (a1, a2) in dash:
        i, j = idx[a1], idx[a2]
        ov.append(f'<line x1="{P[i][0]:.1f}" y1="{P[i][1]:.1f}" x2="{P[j][0]:.1f}" y2="{P[j][1]:.1f}" stroke="#000" stroke-width="1.1" stroke-dasharray="3,2.5"/>')

    def endpoint(kind, ref, toward=None):
        if kind == 'lp':
            x, y, _, _ = lp_point(idx[ref])
            return x, y
        if kind == 'a':
            i = idx[ref]
            x, y = P[i]
            if toward is not None:  # 원자 글자에 닿지 않도록 살짝 앞에서 멈춤
                ux, uy = _unit(toward[0] - x, toward[1] - y)
                return x + ux * bl * 0.38, y + uy * bl * 0.38
            return x, y
        if kind in ('b', 'm'):
            i, j = idx[ref[0]], idx[ref[1]]
            if kind == 'm':
                f = 0.5
            else:
                f = 0.5
            return P[i][0] + (P[j][0] - P[i][0]) * f, P[i][1] + (P[j][1] - P[i][1]) * f
        raise ValueError(kind)

    for k, a_ in enumerate(arrows):
        # 결합 → 그 결합의 한쪽 원자(헤테로리시스·π→원자): 결합 바깥쪽으로 둥글게 도는 짧은 화살표
        if a_['sk'] == 'b' and a_['dk'] == 'a' and a_['d'] in a_['s']:
            i, j = idx[a_['s'][0]], idx[a_['s'][1]]
            if idx[a_['d']] == i:
                i, j = j, i
            ux, uy = _unit(P[j][0] - P[i][0], P[j][1] - P[i][1])
            nx, ny = -uy, ux
            mx, my = (P[i][0] + P[j][0]) / 2, (P[i][1] + P[j][1]) / 2
            side = a_['side'] or (1 if math.hypot(mx + nx * bl - cx, my + ny * bl - cy) >= math.hypot(mx - nx * bl - cx, my - ny * bl - cy) else -1)
            nx, ny = nx * side, ny * side
            x0, y0 = mx + nx * bl * 0.16 - ux * bl * 0.12, my + ny * bl * 0.16 - uy * bl * 0.12
            x1, y1 = P[j][0] + nx * bl * 0.36 + ux * bl * 0.10, P[j][1] + ny * bl * 0.36 + uy * bl * 0.10
            qx, qy = (x0 + x1) / 2 + nx * bl * 0.42, (y0 + y1) / 2 + ny * bl * 0.42
            ov.append(_arrow_path(x0, y0, qx, qy, x1, y1, a_['fish'], 1))
            continue
        x0, y0 = endpoint(a_['sk'], a_['s'])
        # 도착점: 원자면 출발점 쪽에서 멈춤
        x1, y1 = endpoint(a_['dk'], a_['d'], toward=(x0, y0))
        if a_['sk'] == 'lp':
            used_lp[idx[a_['s']]] = used_lp.get(idx[a_['s']], 0)
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / L, dx / L
        side = a_['side']
        bend = max(a_['bend'] * L, bl * 0.42 if L < bl * 1.2 else 0)
        if side == 0:  # 분자 중심에서 먼 쪽으로 휘게
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            c1 = math.hypot(mx + nx * bend - cx, my + ny * bend - cy)
            c2 = math.hypot(mx - nx * bend - cx, my - ny * bend - cy)
            side = 1 if c1 >= c2 else -1
        qx, qy = (x0 + x1) / 2 + nx * bend * side, (y0 + y1) / 2 + ny * bend * side
        ov.append(_arrow_path(x0, y0, qx, qy, x1, y1, a_['fish'], side))

    svg = svg.replace('</svg>', ''.join(ov) + '</svg>')
    cap = f'<div class="mcap">{caption}</div>' if caption else ''
    lab = f'<div class="mlab">{box_label}</div>' if box_label else ''
    return f'<div class="mstep">{lab}{svg}{cap}</div>'


def _rarrow(kind, top='', bottom=''):
    from chem import _vislen
    w = int(max(40, 5.2 * max(_vislen(top), _vislen(bottom)) + 14))
    if kind == '⇌':
        body = (f'<line x1="2" y1="4" x2="{w-4}" y2="4" stroke="#000" stroke-width="1.1"/><path d="M{w-10},0.5 L{w-2},4 L{w-10},4 z" fill="#000"/>'
                f'<line x1="4" y1="10" x2="{w-2}" y2="10" stroke="#000" stroke-width="1.1"/><path d="M10,13.5 L2,10 L10,10 z" fill="#000"/>')
        hgt = 14
    else:
        body = (f'<line x1="2" y1="6" x2="{w-4}" y2="6" stroke="#000" stroke-width="1.1"/>'
                f'<path d="M{w-10},2 L{w-2},6 L{w-10},10 z" fill="#000"/>')
        hgt = 12
    return (f'<div class="marr"><div class="rt">{top}</div><svg width="{w}" height="{hgt}" viewBox="0 0 {w} {hgt}">{body}</svg>'
            f'<div class="rb">{bottom}</div></div>')


def mechanism(*parts, title=''):
    out = []
    for p in parts:
        if isinstance(p, tuple):
            out.append(_rarrow(*p))
        else:
            out.append(p)
    t = f'<div class="mtitle">{title}</div>' if title else ''
    return f'<div class="mech">{t}<div class="mrow">{"".join(out)}</div></div>'


def annotated(smiles, notes, caption='', scale=26, rotate=0, flip=False):
    """분광 해석용: 원자 옆에 피크 기호/δ 값을 붙인 구조 그림. notes={맵번호: '㉠ 9.51'}"""
    return step(smiles, notes=notes, caption=caption, scale=scale, rotate=rotate, flip=flip)


MECH_CSS = '''
.mech { border: 1px solid #bbb; border-radius: 2px; padding: 1.5mm 2mm; margin: 2mm 0; break-inside: avoid; }
.mech .mtitle { font-weight: 700; font-size: 8.8pt; margin-bottom: 1mm; }
.mech .mrow { display: flex; flex-wrap: wrap; align-items: center; gap: 1mm 1.5mm; }
.mstep { display: flex; flex-direction: column; align-items: center; }
.mstep svg { display: block; }
.mcap { font-size: 7.6pt; color: #333; text-align: center; max-width: 60mm; }
.mlab { font-size: 7.6pt; font-weight: 700; }
.marr { display: flex; flex-direction: column; align-items: center; font-family: Arial, "NanumGothic", sans-serif; font-size: 7.4pt; line-height: 1.2; }
.marr .rt, .marr .rb { white-space: nowrap; min-height: 9px; text-align: center; }
'''
