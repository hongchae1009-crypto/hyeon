"""안병천 6회 유기 문항의 메커니즘 그림(굽은 화살표)."""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_tools'))
import mechlib
from mechlib import panel, mechanism

# 조각 사이 간격을 넓혀야 하는 그림만 쓰는 지역 보정 (3회와 같은 방식, 공용 mechlib는 그대로).
_orig_mol = mechlib._mol
EXTRA_GAP = 0.0


KEKULE = False   # True면 SMILES에 쓴 케쿨레 이중결합 위치를 그대로 그린다(방향족 고리에서 화살표 출발점 고정)


def _read(smi, arrows):
    if not KEKULE:
        return _orig_mol(smi, arrows)
    from rdkit import Chem
    orig = Chem.MolFromSmiles
    def patched(s, params=None):
        m = orig(s, sanitize=False)
        Chem.SanitizeMol(m, Chem.SanitizeFlags.SANITIZE_ALL ^ Chem.SanitizeFlags.SANITIZE_SETAROMATICITY)
        return m
    Chem.MolFromSmiles = patched
    try:
        return _orig_mol(smi, arrows)
    finally:
        Chem.MolFromSmiles = orig


def _mol_gap(smi, arrows=()):
    m, maps = _read(smi, arrows)
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


def kek(*a, **k):
    global KEKULE
    KEKULE = True
    try:
        return wide(*a, **k) if 'gap' in k else panel(*a, **k)
    finally:
        KEKULE = False


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


IMG = os.path.join(os.path.dirname(__file__), '..', 'img')
P = lambda n: os.path.join(IMG, n + '.svg')

# ---------- A형 2번: 다이음이온 → 말단 알릴화 → 환원 → 브로모에터화 ----------
mechanism(P('m_A02_dianion'), [
    panel('CC(=O)[CH:1]([H:2])C(=O)Cc1ccccc1.[NH2-:3]', [(('lp', 3), ('a', 2)), (('b', 1, 2), ('a', 1))],
          legend='(1) NH₂⁻ 1당량: 가장 산성인 H_B(두 C=O 사이) 제거'),
    '↓',
    panel('CC(=O)[CH-]C(=O)[CH:1]([H:2])c1ccccc1.[NH2-:3]', [(('lp', 3), ('a', 2)), (('b', 1, 2), ('a', 1))],
          legend='(2) 2당량째: 다음으로 산성인 H_A(벤질·α) 제거'),
    '↓ 다이음이온 + CH₂=CHCH₂Br',
    wide('CC(=O)[CH-]C(=O)[CH-:1]C.C=C[CH2:2][Br:3]', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))], gap=1.2,
          legend='(3) 바깥(벤질) 탄소음이온이 SN2 (Ph는 CH₃로 간략)'),
    '↓ H₃O⁺ (가운데 C 양성자화)',
    panel('C=CCC(c1ccccc1)C(=O)CC(C)=O', h=105, legend='알릴화 생성물 (C₁₄H₁₆O₂)'),
])
mechanism(P('m_A02_red'), [
    wide('C=CCC(c1ccccc1)C(=O)C[C:1](C)=[O:2].[H-:3]', [(('a', 3), ('a', 1)), (('b', 1, 2), ('a', 2))], gap=1.0,
          legend='(4) NaBH₄의 H⁻가 C=O 탄소 공격 (다른 C=O도 같은 방식)'),
    '↓ EtOH가 알콕사이드 양성자화 (두 번)',
    panel('C=CCC(c1ccccc1)C(O)CC(C)O', h=110, legend='1,3-다이올 (C₁₄H₂₀O₂)'),
])
mechanism(P('m_A02_br'), [
    wide('[CH2:1]=[CH:2]CC(c1ccccc1)C(O)CC(C)O.[Br:3][Br:4]', [(('b', 1, 2), ('a', 3)), (('b', 3, 4), ('a', 4))], gap=1.0,
          legend='(5) C=C π 전자가 Br₂ 공격 → 브로모늄 이온, Br⁻ 이탈'),
    '↓',
    panel('C[CH:9](O)C[CH:7]([OH:5])[CH:8](c1ccccc1)C[CH:2]1[CH2:1][Br+:3]1',
          [(('lp', 5), ('a', 2)), (('b', 2, 3), ('a', 3))], h=160,
          legend='(6) C2–OH가 브로모늄의 안쪽 C를 뒤에서 공격 (5-exo)'),
    '↓ Br⁻가 O–H 양성자 제거',
    panel('CC(O)CC1OC(CBr)CC1c1ccccc1', h=120, legend='A: 2-(bromomethyl)테트라하이드로퓨란 (C₁₄H₁₉BrO₂)'),
])

# ---------- A형 8번 ----------
mechanism(P('m_A08_ox'), [
    panel('CC(C)(C)C[CH2:1][OH:2].O[Cr:4](=[O:5])(=O)O', [(('lp', 2), ('a', 4)), (('b', 4, 5), ('a', 5))],
          legend='(1) 알코올 O가 Cr(VI) 공격 → 크로메이트 에스터'),
    '↓ 양성자 이동',
    wide('[OH2:7].[H:6][CH:1](CC(C)(C)C)[O:2][Cr:4](=O)(=O)O',
          [(('lp', 7), ('a', 6)), (('b', 1, 6), ('b', 1, 2)), (('b', 2, 4), ('a', 4))], gap=1.2, h=150,
          legend='(2) 물이 α-H 제거 → C=O, Cr(VI)→Cr(IV)'),
    '↓ 알데하이드 수화물(gem-다이올) → (1)(2) 반복',
    panel('CC(C)(C)CC(=O)O', h=95, legend='B 3,3-dimethylbutanoic acid'),
])
mechanism(P('m_A08_socl2'), [
    wide('CC(C)(C)C[C:1](=O)[OH:2].O=[S:3](Cl)[Cl:5]', [(('lp', 2), ('a', 3)), (('b', 3, 5), ('a', 5))], gap=1.0,
          legend='(1) OH가 S 공격, Cl⁻ 이탈 → 클로로설파이트'),
    '↓ −H⁺',
    wide('[Cl-:6].CC(C)(C)C[C:1](=[O:7])[O:2]S(=O)Cl', [(('lp', 6), ('a', 1)), (('b', 1, 7), ('a', 7))], gap=1.0,
          legend='(2) Cl⁻가 아실 탄소 공격 (첨가)'),
    '↓',
    panel('CC(C)(C)C[C:1]([O-:7])([Cl:6])[O:2]S(=O)Cl', [(('lp', 7), ('b', 7, 1)), (('b', 1, 2), ('a', 2))], h=140,
          legend='(3) C=O 회복, ⁻OS(O)Cl 이탈 → SO₂ + Cl⁻'),
    '↓',
    panel('CC(C)(C)CC(=O)Cl', h=95, legend='산 염화물'),
])
mechanism(P('m_A08_amide'), [
    wide('CC(C)(C)C[C:1](=[O:2])Cl.C[NH:3]C', [(('lp', 3), ('a', 1)), (('b', 1, 2), ('a', 2))], gap=1.0,
          legend='(4) Me₂NH의 N이 아실 C 공격 (첨가)'),
    '↓',
    panel('CC(C)(C)C[C:1]([O-:2])([Cl:4])[NH+:3](C)C', [(('lp', 2), ('b', 2, 1)), (('b', 1, 4), ('a', 4))], h=140,
          legend='(5) C=O 회복, Cl⁻ 이탈 (제거)'),
    '↓ 두 번째 Me₂NH가 N–H 양성자 제거',
    panel('CC(C)(C)CC(=O)N(C)C', h=100, legend='C N,N-dimethyl-3,3-dimethylbutanamide'),
])
mechanism(P('m_A08_lah'), [
    wide('CC(C)(C)C[C:1](=[O:2])N(C)C.[H-:3]', [(('a', 3), ('a', 1)), (('b', 1, 2), ('a', 2))], gap=1.0,
          legend='(6) LiAlH₄의 H⁻ 첨가 → 사면체 알콕사이드(O–Al)'),
    '↓',
    panel('CC(C)(C)C[CH:1]([O:2][AlH3-])[N:3](C)C', [(('lp', 3), ('b', 3, 1)), (('b', 1, 2), ('a', 2))], h=140,
          legend='(7) N이 밀어내 O–Al 이탈 → 이미늄 이온'),
    '↓',
    wide('CC(C)(C)C[CH:1]=[N+:3](C)C.[H-:4]', [(('a', 4), ('a', 1)), (('b', 1, 3), ('a', 3))], gap=1.0,
          legend='(8) 두 번째 H⁻가 이미늄 C 공격'),
    '↓ H₂O 처리',
    panel('CC(C)(C)CCN(C)C', h=95, legend='D (3차 아민)'),
])

# ---------- B형 8번 ----------
mechanism(P('m_B08_ozone'), [
    wide('C[C:1](C)=[CH:2]C.[O-:3][O+:4]=[O:5]', [(('lp', 3), ('a', 1)), (('b', 1, 2), ('a', 5)), (('b', 4, 5), ('a', 4))],
          gap=1.0, legend='(1) O₃ 1,3-쌍극자 첨가 (반응하는 C=C 부분만)'),
    '↓ 1차 오존화물 → 2차 오존화물 → SMe₂ 환원',
    panel('CC(=O)[C@@H]1CC[C@H](C=O)[C@@H](CCO)C1', h=120, legend='고리가 열린 케토알데하이드 (고리 입체는 유지)'),
])
mechanism(P('m_B08_red'), [
    wide('C[C:1](=[O:2])C1CCC(C=O)C(CCO)C1.[H-:3]', [(('a', 3), ('a', 1)), (('b', 1, 2), ('a', 2))], gap=1.0,
          legend='(2) NaBH₄: 케톤·알데하이드 모두 H⁻ 첨가'),
    '↓ EtOH 양성자화',
    panel('C[C@@H](O)[C@@H]1CC[C@H](CO)[C@@H](CCO)C1', h=120,
          legend='B 트라이올: 곁사슬 CH(OH) 탄소는 R/S 혼합'),
])
mechanism(P('m_B08_ts'), [
    wide('C[CH2:1][OH:2].[S:3](=O)(=O)(c1ccc(C)cc1)[Cl:4]', [(('lp', 2), ('a', 3)), (('b', 3, 4), ('a', 4))], gap=1.0,
          legend='(3) 입체 장애가 가장 작은 1차 OH가 S 공격, Cl⁻ 이탈'),
    '↓ pyridine이 O–H 양성자 제거 → R–OTs',
    panel('C[C@@H](O)[C@@H]1CC[C@H]([CH2:5][OH:6])[C@@H](C[CH2:7][O:8]S(C)(=O)=O)C1',
          [(('lp', 6), ('a', 7)), (('b', 7, 8), ('a', 8))], h=165,
          legend='(4) 분자 내 SN2: CH₂OH의 O → C–OTs (Ts는 Ms로 간략)'),
    '↓ pyridine −H⁺ (6원 고리 에터)',
    panel('C[C@@H](O)[C@@H]1CC[C@@H]2COCC[C@H]2C1', h=120, legend='C: trans-접합 옥타하이드로아이소크로멘'),
])

# ---------- B형 9번 ----------
mechanism(P('m_B09_snar'), [
    wide('Brc1ccccc1[S:1][H:2].[O-:3]CC', [(('lp', 3), ('a', 2)), (('b', 1, 2), ('a', 1))], gap=1.0,
          legend='(1) Na + EtOH → EtO⁻가 S–H 제거 → B (티올레이트)'),
    '↓ 2,5-다이클로로나이트로벤젠',
    kek('Brc1ccccc1[S-:1].Cl[C:5]1=[C:6]([N+:7](=[O:8])[O-])C=C(Cl)C=C1',
        [(('lp', 1), ('a', 5)), (('b', 5, 6), ('b', 6, 7)), (('b', 7, 8), ('a', 8))], gap=1.0, h=150,
        legend='(2) 첨가: S⁻가 NO₂ ortho의 C–Cl 탄소 공격'),
    '↓ Meisenheimer 착물 (음전하가 NO₂ O까지)',
    kek('Brc1ccccc1[S:1][C:5]1([Cl:9])[C:6](=[N+:7]([O-:8])[O-])C=C(Cl)C=C1',
        [(('lp', 8), ('b', 8, 7)), (('b', 7, 6), ('b', 6, 5)), (('b', 5, 9), ('a', 9))], h=160,
        legend='(3) 제거: 방향족성 회복, Cl⁻ 이탈'),
    '↓',
    panel('O=[N+]([O-])c1cc(Cl)ccc1Sc1ccccc1Br', h=115, legend='C (2-bromophenyl)(4-chloro-2-nitrophenyl) sulfide'),
])
