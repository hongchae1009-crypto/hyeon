"""안병천 5회 유기 문항의 메커니즘 그림(굽은 화살표)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_tools'))
import mechlib
from mechlib import panel, mechanism

# 조각 사이 간격을 넓혀야 하는 그림만 쓰는 지역 보정 (3회와 같은 방식, 공용 mechlib는 그대로).
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

RED, INK = '#c0392b', '#1f2933'


def _txt(x, y, t, size=13, anchor='middle', color=INK):
    return (f"<text x='{x}' y='{y}' font-size='{size}' text-anchor='{anchor}' fill='{color}' "
            f"font-family='Noto Sans KR, sans-serif'>{t}</text>")


def _curve(x1, y1, x2, y2, bend):
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


def da_panel(legend):
    """s-cis (2E,4E)-hexa-2,4-diene + acrolein, 고리형 화살표 3개 (손그림).
    다이엔 말단 C1·C4의 CH₃는 둘 다 '바깥쪽' → 생성물에서 서로 cis."""
    W, H = 330, 195
    C1, C2, C3, C4 = (120, 40), (85, 62), (85, 108), (120, 130)
    C5, C6 = (205, 112), (205, 58)
    ln = lambda a, b, w=2: f"<line x1='{a[0]}' y1='{a[1]}' x2='{b[0]}' y2='{b[1]}' stroke='{INK}' stroke-width='{w}'/>"
    dbl = lambda a, b, o: ln(a, b) + ln((a[0] + o[0], a[1] + o[1]), (b[0] + o[0], b[1] + o[1]), 1.6)
    b = dbl(C1, C2, (5, 5)) + ln(C2, C3) + dbl(C3, C4, (5, -5))
    b += ln(C5, C6) + ln((C5[0] - 5, C5[1]), (C6[0] - 5, C6[1]), 1.6)
    b += ln(C1, (140, 16)) + _txt(150, 14, 'CH₃', 12, 'start') + ln(C4, (140, 154)) + _txt(150, 162, 'CH₃', 12, 'start')
    b += ln(C6, (232, 42)) + _txt(240, 40, 'CHO', 12, 'start') + _txt(272, 54, '(endo)', 10.5, 'start', '#6b7280')
    b += "<line x1='130' y1='42' x2='195' y2='58' stroke='#9ca3af' stroke-width='1' stroke-dasharray='4 3'/>"
    b += "<line x1='130' y1='128' x2='195' y2='112' stroke='#9ca3af' stroke-width='1' stroke-dasharray='4 3'/>"
    b += _curve(100, 48, 82, 84, -14)       # C1=C2 π → C2–C3 (새 π)
    b += _curve(103, 122, 165, 122, 14)     # C3=C4 π → C4–C5 새 σ
    b += _curve(212, 86, 165, 48, 16)       # C5=C6 π → C6–C1 새 σ
    b += _txt(W / 2, H - 6, legend, 12.5, color='#374151')
    return (f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}px' height='{H}px' viewBox='0 0 {W} {H}'>{b}</svg>", H)


IMG = os.path.join(os.path.dirname(__file__), '..', 'img')
P = lambda n: os.path.join(IMG, n + '.svg')

# ---------- A형 2번: 내부 알카인 오존 분해 → 두 카복실산 ----------
mechanism(P('m_A02_ozone'), [
    panel('C[C:1]#[C:2]C.[O-:3][O+:4]=[O:5]', [(('lp', 3), ('a', 1)), (('b', 1, 2), ('a', 5)), (('b', 4, 5), ('a', 4))],
          legend='(1) O₃ 1,3-쌍극자 첨가 (sec-butyl은 CH₃로 간략히)'),
    '↓ 오존화물 자리옮김',
    panel('C[C:1](=O)[C:2](=O)[C@@H](C)CC', h=105, legend='(2) 1,2-다이케톤형 중간체를 거쳐'),
    '↓ H₂O (가수분해·산화 절단)',
    panel('CC(=O)O.OC(=O)[C@@H](C)CC', h=110, legend='아세트산 + C (S)-2-methylbutanoic acid'),
])

# ---------- A형 3번: PCC 산화 (2차 알코올 → 케톤) ----------
mechanism(P('m_A03_pcc'), [
    panel('c1ccccc1C[CH:1](C)[OH:2].[O-:3][Cr:4](=[O:5])(=O)Cl', [(('lp', 2), ('a', 4)), (('b', 4, 5), ('a', 5))],
          legend='(1) 알코올 O가 Cr(VI)에 첨가 (PCC = pyH⁺ CrO₃Cl⁻)'),
    '↓ 양성자 이동 → 크로메이트 에스터',
    wide('[n:7]1ccccc1.[H:6][C:1](C)(C)[O:2][Cr:4](=O)(=O)Cl',
          [(('lp', 7), ('a', 6)), (('b', 1, 6), ('b', 1, 2)), (('b', 2, 4), ('a', 4))], h=150,
          legend='(2) α-H 제거 → C=O, Cr–O 끊김 (PhCH₂ → CH₃로 간략히)'),
    '↓ Cr(VI) → Cr(IV)',
    panel('CC(=O)Cc1ccccc1', h=100, legend='B phenylacetone (C₉H₁₀O)'),
])

# ---------- A형 8번: Diels–Alder (endo) ----------
mechanism(P('m_A08_DA'), [
    da_panel('(1) [4+2] 협동: 화살표 3개가 고리 모양으로 동시에'),
    '↓ endo 전이 상태 (2차 궤도 겹침)',
    panel('C[C@@H]1C=C[C@H](C)[C@H](C=O)C1', h=120, legend='A: CHO와 두 CH₃가 모두 cis (+ 거울상 1:1)'),
])

# ---------- A형 8번: 수소붕소화–산화 ----------
mechanism(P('m_A08_hb'), [
    panel('[CH2:1]=[C:2]1C[C@H](C)C=C[C@@H]1C.[H:4][BH2:3]', [(('b', 1, 2), ('a', 3)), (('b', 3, 4), ('a', 2))],
          legend='(1) 4중심 syn 첨가: B는 CH₂에, H는 고리 C에'),
    '↓ 인접 CH₃의 반대 면에서 접근',
    panel('[BH2:3][CH2:1][C@@H]1C[C@H](C)C=C[C@@H]1C.[O-:5][OH:6]', [(('lp', 5), ('a', 3))],
          legend='(2) HOO⁻가 B의 빈 p 오비탈 공격'),
])
mechanism(P('m_A08_hb2'), [
    panel('C[CH2:2][BH2-:3][O:5][OH:6]', [(('b', 2, 3), ('a', 5)), (('b', 5, 6), ('a', 6))], h=110,
          legend='(3) 1,2-이동: C가 O로, OH⁻ 이탈 (고리는 CH₃로 간략히)'),
    '↓ 가수분해 (B–O 끊김)',
    panel('OC[C@@H]1C[C@H](C)C=C[C@@H]1C', h=115, legend='1차 알코올 (CH₂OH와 두 CH₃ 모두 cis)'),
])
mechanism(P('m_A08_pcc'), [
    panel('C[CH2:1][OH:2].[O-:3][Cr:4](=[O:5])(=O)Cl', [(('lp', 2), ('a', 4)), (('b', 4, 5), ('a', 5))], h=120,
          legend='(1) O → Cr(VI) 첨가 (고리는 CH₃로 간략히)'),
    '↓ 양성자 이동 → 크로메이트 에스터',
    wide('[n:7]1ccccc1.[H:6][CH:1](C)[O:2][Cr:4](=O)(=O)Cl',
          [(('lp', 7), ('a', 6)), (('b', 1, 6), ('b', 1, 2)), (('b', 2, 4), ('a', 4))], h=150,
          legend='(2) α-H 제거 → C=O (고리는 R=CH₃로 간략히)'),
    '↓',
    panel('C[C@@H]1C=C[C@H](C)[C@H](C=O)C1', h=115, legend='B (1R,2S,5S) — 한 거울상만'),
])

# ---------- B형 9번 ----------
mechanism(P('m_B09_amide'), [
    panel('C1CCCCC1[C:1](=[O:2])Cl.[NH3:3]', [(('lp', 3), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(1) NH₃가 아실 C 공격 (첨가)'),
    '↓',
    panel('C1CCCCC1[C:1]([O-:2])([Cl:4])[NH3+:3]', [(('lp', 2), ('b', 2, 1)), (('b', 1, 4), ('a', 4))],
          legend='(2) C=O 회복, Cl⁻ 이탈 (제거)'),
    '↓ 두 번째 NH₃가 N–H 양성자 제거 (NH₄Cl)',
    panel('NC(=O)C1CCCCC1', h=100, legend='B cyclohexanecarboxamide'),
])
mechanism(P('m_B09_pocl3'), [
    panel('C1CCCCC1[C:1](=[O:2])N.[P:4](=O)(Cl)(Cl)[Cl:5]', [(('lp', 2), ('a', 4)), (('b', 4, 5), ('a', 5))],
          legend='(1) 아마이드 O가 P 공격, Cl⁻ 이탈'),
    '↓ −H⁺ (N–H)',
    panel('[Cl-:7].C1CCCCC1[C:1](=[N:3][H:6])[O:2]P(=O)(Cl)Cl',
          [(('lp', 7), ('a', 6)), (('b', 3, 6), ('b', 1, 3)), (('b', 1, 2), ('a', 2))],
          legend='(2) N–H 제거와 함께 O–PO₂Cl₂ 이탈 → C≡N'),
    '↓',
    panel('N#CC1CCCCC1', h=95, legend='C cyclohexanecarbonitrile'),
])
mechanism(P('m_B09_grig'), [
    wide('C1CCCCC1[C:1]#[N:2].C[CH:3](C)[Mg:4]Br', [(('b', 3, 4), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(1) i-Pr⁻(탄소 친핵체)가 나이트릴 C 공격'),
    '↓ 이민 음이온 Mg염에서 멈춤 → H₃O⁺',
    panel('C1CCCCC1[C:1](=[NH2+:2])C(C)C.[OH2:3]', [(('lp', 3), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(2) 이미늄 C에 물 첨가'),
    '↓ 양성자 이동',
    panel('C1CCCCC1[C:1]([OH:3])([NH3+:2])C(C)C', [(('lp', 3), ('b', 3, 1)), (('b', 1, 2), ('a', 2))],
          legend='(3) C=O 형성, NH₃ 이탈 → −H⁺'),
    '↓',
    panel('CC(C)C(=O)C1CCCCC1', h=100, legend='D cyclohexyl isopropyl ketone'),
])
mechanism(P('m_B09_dibal'), [
    wide('C1CCCCC1C#[N:2].[H:3][Al:4](C)C', [(('lp', 2), ('a', 4))], gap=1.2,
          legend='(1) N → Al 배위 (i-Bu는 CH₃로 간략히)'),
    '↓',
    panel('C1CCCCC1[C:1]#[N+:2][Al-:4]([H:3])(C)C', [(('b', 4, 3), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(2) Al–H의 수소화 이온이 C로 (−78 °C, 1당량)'),
    '↓ Al 이민염 → H₃O⁺ (D와 같은 가수분해)',
    panel('O=CC1CCCCC1', h=100, legend='E cyclohexanecarbaldehyde'),
])
mechanism(P('m_B09_cuprate'), [
    panel('C1CCCCC1[C:1](=[O:2])Cl.[CH3:3][Cu-:4]C', [(('b', 3, 4), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(1) CH₃ 전달 (실제로는 Cu 산화적 첨가–환원적 제거)'),
    '↓',
    panel('C1CCCCC1[C:1]([O-:2])([Cl:5])C', [(('lp', 2), ('b', 2, 1)), (('b', 1, 5), ('a', 5))],
          legend='(2) C=O 회복, Cl⁻ 이탈'),
    '↓ 케톤은 무른 큐프레이트와 더 반응하지 않음',
    panel('CC(=O)C1CCCCC1', h=100, legend='A cyclohexyl methyl ketone'),
])
