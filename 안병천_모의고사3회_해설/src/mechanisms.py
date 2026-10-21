"""안병천 3회 유기 문항의 메커니즘 그림(굽은 화살표)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_tools'))
import mechlib
from mechlib import panel, mechanism

# 조각 사이 간격을 넓혀야 하는 그림(이탈기와 공격체가 겹치는 경우)만 쓰는 지역 보정.
# 공용 mechlib는 고치지 않고, 그 안의 _mol을 감싸 두 번째 조각부터 오른쪽으로 더 민다.
_orig_mol = mechlib._mol
EXTRA_GAP = 0.0


def _mol_gap(smi, arrows=()):
    m, maps = _orig_mol(smi, arrows)
    if EXTRA_GAP:
        from rdkit import Chem
        frags = sorted(Chem.GetMolFrags(m), key=min)
        conf = m.GetConformer()
        for k, fr in enumerate(frags[1:], 1):
            for i in fr:
                q = conf.GetAtomPosition(i)
                conf.SetAtomPosition(i, (q.x + EXTRA_GAP * k, q.y, 0))
    return m, maps


mechlib._mol = _mol_gap


def wide(*a, gap=2.2, **k):
    global EXTRA_GAP
    EXTRA_GAP = gap
    try:
        return panel(*a, **k)
    finally:
        EXTRA_GAP = 0.0

import math
RED, INK = '#c0392b', '#1f2933'


def _t(x, y, t, size=14, anchor='middle', color=INK):
    return (f"<text x='{x}' y='{y}' font-size='{size}' text-anchor='{anchor}' fill='{color}' "
            f"font-family='Noto Sans KR, sans-serif'>{t}</text>")


def _arc(x1, y1, x2, y2, bend):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    cx, cy = mx - dy / L * bend, my + dx / L * bend
    tx, ty = x2 - cx, y2 - cy
    T = math.hypot(tx, ty)
    ux, uy = tx / T, ty / T
    h1 = (x2 - 7 * ux + 3.5 * uy, y2 - 7 * uy - 3.5 * ux)
    h2 = (x2 - 7 * ux - 3.5 * uy, y2 - 7 * uy + 3.5 * ux)
    return (f"<path d='M{x1},{y1} Q{cx:.1f},{cy:.1f} {x2},{y2}' fill='none' stroke='{RED}' stroke-width='1.6'/>"
            f"<polygon points='{x2},{y2} {h1[0]:.1f},{h1[1]:.1f} {h2[0]:.1f},{h2[1]:.1f}' fill='{RED}'/>")


def sn2_panel(legend):
    """Br⁻가 C–O 결합의 정반대(뒷면)에서 1차 탄소를 공격하는 그림 (손그림)."""
    W, H = 330, 140
    ln = lambda a, b, w=2, dash='': (f"<line x1='{a[0]}' y1='{a[1]}' x2='{b[0]}' y2='{b[1]}' stroke='{INK}' "
                                     f"stroke-width='{w}'{dash}/>")
    C = (165, 60)
    b = _t(60, 65, 'Br⁻', 16, color='#8a4b08')
    b += ln(C, (232, 60)) + _t(258, 65, 'OH₂⁺', 15, color='#c0392b')
    b += ln(C, (150, 25)) + _t(145, 20, 'CH₂CH₃', 13, 'end')
    b += ln(C, (145, 92)) + _t(138, 104, 'H', 13)
    b += f"<polygon points='{C[0]},{C[1]} {C[0]+12},{C[1]+30} {C[0]+20},{C[1]+27}' fill='{INK}'/>" + _t(C[0] + 22, C[1] + 45, 'H', 13)
    b += _arc(78, 52, 158, 56, -16)          # Br⁻ 비공유 전자쌍 → C (뒷면)
    b += _arc(205, 54, 255, 48, -12)         # C–O 결합 전자 → O
    b += _t(W / 2, H - 6, legend, 12.5, color='#374151')
    return (f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}px' height='{H}px' viewBox='0 0 {W} {H}'>{b}</svg>", H)


IMG = os.path.join(os.path.dirname(__file__), '..', 'img')
P = lambda n: os.path.join(IMG, n + '.svg')

# ---------- A형 2번: A → C (말단 알카인 수소붕소화–산화 → 엔올 → 알데하이드) ----------
mechanism(P('m_A02_alkyne'), [
    panel('CC[C@H](C)[C:1]#[CH:2].[H:4][BH2:3]', [(('b', 1, 2), ('a', 3)), (('b', 3, 4), ('a', 1))],
          legend='(1) 4중심 전이상태: B는 말단 C, H는 안쪽 C에 syn 첨가'),
    '↓',
    panel('CC[C@H](C)/[CH:1]=[CH:2]/[BH2:3].[O-:5][OH:6]', [(('lp', 5), ('a', 3))],
          legend='(2) HOO⁻가 빈 p 오비탈을 가진 B 공격'),
])
mechanism(P('m_A02_alkyne2'), [
    panel('CC[C@H](C)/[CH:1]=[CH:2]/[BH2-:3][O:5][OH:6]', [(('b', 2, 3), ('a', 5)), (('b', 5, 6), ('a', 6))],
          legend='(3) 1,2-이동: C–B 결합이 O로 옮겨 가며 OH⁻ 이탈'),
    '↓ 가수분해(B–O 끊김)',
    panel('CC[C@H](C)/[CH:1]=[CH:2]/[O-:3].[H:4][OH:5]', [(('lp', 3), ('b', 3, 2)), (('b', 2, 1), ('a', 4)), (('b', 4, 5), ('a', 5))],
          legend='(4) 엔올(엔올레이트) → α-탄소 양성자화 (토토머화)'),
    '↓',
    panel('CC[C@H](C)CC=O', h=105, legend='C (S)-3-methylpentanal (C3 배열 그대로)'),
])

# ---------- A형 2번: B → D (고리 알켄 수소붕소화–산화) ----------
mechanism(P('m_A02_alkene'), [
    panel('C[C@H]1[CH:1]=[CH:2]CC1.[H:4][BH2:3]', [(('b', 1, 2), ('a', 3)), (('b', 3, 4), ('a', 1))],
          legend='(1) BH₃가 CH₃ 반대 면에서 syn 첨가, B는 덜 붐비는 C에'),
    '↓',
    panel('C[C@H]1C[C@H]([BH2:3])CC1.[O-:5][OH:6]', [(('lp', 5), ('a', 3))],
          legend='(2) trans-알킬보레인에 HOO⁻ 첨가'),
    '↓',
    panel('C[C@H]1C[C@H:2]([BH2-:3][O:5][OH:6])CC1', [(('b', 2, 3), ('a', 5)), (('b', 5, 6), ('a', 6))],
          legend='(3) 배열을 유지한 채 C가 O로 이동 (입체 보존)'),
    '↓ 가수분해',
    panel('C[C@H]1C[C@H](O)CC1', h=110, legend='D (1R,3R)-trans-3-methylcyclopentan-1-ol'),
])

# ---------- A형 8번: 1-propanol + HBr ----------
mechanism(P('m_A08'), [
    panel('CCC[OH:1].[H:2][Br:3]', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) OH 양성자화 → 좋은 이탈기 H₂O'),
    '↓',
    sn2_panel('(2) SN2: Br⁻가 이탈기 반대편(뒷면)에서 1차 탄소 공격 → B'),
    '↓ (곁반응)',
    panel('[OH2:1].[H:2][CH:3](C)[CH2:4][OH2+:5]', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('b', 3, 4)), (('b', 4, 5), ('a', 5))],
          legend='(3) E2: 물이 β-H를 떼며 H₂O 이탈 → C 프로펜'),
])

# ---------- B형 8번: dienone–phenol 자리옮김 (R = OMe) ----------
mechanism(P('m_B08'), [
    panel('CO[C:7]1(C)[CH:5]=[CH:4][C:3](=[O:1])[CH:2]=[CH:6]1.[H+:9]', [(('lp', 1), ('a', 9))],
          legend='(1) 카보닐 O 양성자화 (첫 번째 평형)'),
    '↓',
    panel('[OH+:1]=[C:3]1[CH:4]=[CH:5][C:7](C)(OC)[CH:6]=[CH:2]1', [(('b', 4, 5), ('b', 3, 4)), (('b', 1, 3), ('a', 1))],
          legend='(2) 공명: 양전하가 C3(C4 옆)으로'),
    '↓',
    panel('O[C:3]1=[CH:4][CH+:5][C:7]([CH3:8])(OC)C=C1', [(('b', 7, 8), ('a', 5))],
          legend='(3) 1,2-CH₃ 이동 (C4 → C3)'),
])
mechanism(P('m_B08_2'), [
    panel('OC1=C[C:5]([H:10])([CH3:8])[C+:7]([O:9]C)C=C1', [(('lp', 9), ('b', 9, 7))],
          legend='(4) 중간체 B: C4⁺를 OMe 비공유 전자쌍이 안정화'),
    '↓ 옥소카베늄 공명',
    panel('OC1=C[C:5]([H:10])([CH3:8])[C:7](=[O+:9]C)C=C1.[OH2:11]',
          [(('lp', 11), ('a', 10)), (('b', 10, 5), ('b', 5, 7)), (('b', 7, 9), ('a', 9))],
          legend='(5) −H⁺ → 방향족화'),
    '↓',
    panel('COc1ccc(O)cc1C', h=105, legend='4-methoxy-3-methylphenol'),
])
mechanism(P('m_B08_A'), [
    panel('O[C:3]1=[CH:4][CH+:5][C:7](C)([O:8]C)C=C1', [(('b', 7, 8), ('a', 5))],
          legend='(경로 A) OMe가 이동하면'),
    '↓',
    panel('OC1=CC(OC)[C+](C)C=C1', h=120, legend='C4⁺에 CH₃만 남음 → 3차 탄소양이온(덜 안정)'),
])

# ---------- B형 9번 ----------
mechanism(P('m_B09_ac'), [
    panel('c1ccccc1[NH2:1].C[C:3](=[O:4])OC(C)=O', [(('lp', 1), ('a', 3)), (('b', 3, 4), ('a', 4))],
          legend='(1) 아닐린 N이 무수물 C=O 공격'),
    '↓',
    panel('c1ccccc1[NH2+:1][C:3](C)([O-:4])[O:5]C(C)=O', [(('lp', 4), ('b', 4, 3)), (('b', 3, 5), ('a', 5))],
          legend='(2) C=O 회복, 아세트산 이온 이탈 → −H⁺(pyridine)'),
    '↓',
    panel('CC(=O)Nc1ccccc1', h=100, legend='acetanilide (NH₂ 보호: 활성↓, 다중 치환·AlCl₃ 착물 방지)'),
])
mechanism(P('m_B09_fc'), [
    panel('CC(C)(C)[Cl:1].[Al:2](Cl)(Cl)Cl', [(('lp', 1), ('a', 2))],
          legend='(1) Cl이 AlCl₃에 배위 → (CH₃)₃C⁺ + AlCl₄⁻'),
    '↓',
    panel('CC(=O)[NH:7][C:1]1=[CH:2][CH:3]=[CH:4][CH]=[CH]1.[C+:5](C)(C)C',
          [(('b', 3, 4), ('a', 5)), (('lp', 7), ('b', 7, 1))],
          legend='(2) para 탄소가 t-Bu⁺ 공격 (N이 전자 공급)'),
    '↓',
    panel('CC(=O)[NH+:7]=[C:1]1[CH:2]=[CH:3][C:4]([H:6])(C(C)(C)C)C=C1.[Cl-:8]',
          [(('lp', 8), ('a', 6)), (('b', 4, 6), ('b', 3, 4)), (('b', 2, 3), ('b', 1, 2)), (('b', 7, 1), ('a', 7))],
          legend='(3) σ 착물의 H⁺ 제거 → 방향족 회복 → A'),
])
mechanism(P('m_B09_hyd'), [
    panel('[OH-:1].C[C:2](=[O:3])Nc1ccc(cc1)C(C)(C)C', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) OH⁻가 아마이드 C=O 공격'),
    '↓',
    panel('C[C:2]([OH:1])([O-:3])[NH:4]c1ccc(cc1)C(C)(C)C', [(('lp', 3), ('b', 3, 2)), (('b', 2, 4), ('a', 4))],
          legend='(2) C=O 회복, ArNH⁻ 이탈 (가열 필요)'),
    '↓ 양성자 이동',
    panel('Nc1ccc(cc1)C(C)(C)C', h=105, legend='B 4-tert-butylaniline (+ CH₃COO⁻)'),
])
mechanism(P('m_B09_cl'), [
    panel('[NH2:1][C:2]1=[CH:3][CH]=[C](C(C)(C)C)[CH]=[CH]1.[Cl:5][Cl:6]',
          [(('lp', 1), ('b', 1, 2)), (('b', 2, 3), ('a', 5)), (('b', 5, 6), ('a', 6))],
          legend='(1) NH₂가 밀어준 π 전자로 ortho C가 Cl₂ 공격'),
    '↓',
    panel('[NH2+:1]=[C:2]1[CH:3]([Cl:5])[CH]=C(C(C)(C)C)C=C1', h=125,
          legend='(2) σ 착물(이미늄형) → H⁺ 제거, 반대쪽 ortho도 같은 방식'),
    '↓',
    panel('Nc1c(Cl)cc(cc1Cl)C(C)(C)C', h=135, legend='C 2,6-dichloro-4-tert-butylaniline'),
])
mechanism(P('m_B09_diazo'), [
    panel('c1ccccc1[NH2:1].[N:2]#[O+:3]', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) ArNH₂의 N이 NO⁺ 공격 (Ar은 페닐로 단순화)'),
    '↓ −H⁺, 토토머화 → Ar–N=N–OH, H⁺',
    panel('c1ccccc1[N:1]=[N:2][OH2+:3]', [(('lp', 1), ('b', 1, 2)), (('b', 2, 3), ('a', 3))],
          legend='(2) OH 양성자화 후 H₂O 이탈'),
    '↓',
    panel('c1ccccc1[N+]#N', h=100, legend='아릴다이아조늄 이온 (0–5 °C에서 안정)'),
    '↓ (나) CuBr: Sandmeyer (단일 전자 이동, −N₂)',
    panel('Brc1c(Cl)cc(cc1Cl)C(C)(C)C', h=135, legend='D (Ar• + CuBr₂ → ArBr + CuBr)'),
])
