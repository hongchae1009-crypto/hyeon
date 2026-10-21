"""안병천 1회 유기 문항의 메커니즘 그림(굽은 화살표). 라디칼 단계는 반쪽 화살표(fishhook)."""
import os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_tools'))
import mechlib
from mechlib import panel, mechanism

IMG = os.path.join(os.path.dirname(__file__), '..', 'img')
P = lambda n: os.path.join(IMG, n + '.svg')

# 반쪽 화살표: 공용 도구는 건드리지 않고 이 파일에서만 화살촉을 한쪽 날개로 바꾼다
_full_arrow = mechlib._arrow
FISH = False


def _arrow(*a, **k):
    svg = _full_arrow(*a, **k)
    if FISH:
        svg = re.sub(r"<polygon points='([\d.\-]+),([\d.\-]+) ([\d.\-]+),([\d.\-]+) [\d.\-]+,[\d.\-]+' fill='([^']+)'/>",
                     lambda m: f"<polyline points='{m[3]},{m[4]} {m[1]},{m[2]}' fill='none' stroke='{m[5]}' stroke-width='1.6'/>",
                     svg)
    return svg


mechlib._arrow = _arrow

# 한 단 높이(약 180 mm ≈ 700 px)를 넘는 그림은 '↓' 줄에서 고르게 나눠 _2, _3 … 파일로 저장


def mechanism(path, steps):
    total = sum(26 if isinstance(st, str) else st[1] for st in steps)
    target = total / -(-total // 700) if total > 700 else total + 1   # 조각 높이를 고르게
    parts, cur, h = [], [], 0
    for st in steps:
        sh = 26 if isinstance(st, str) else st[1]
        if cur and isinstance(st, str) and h >= target - 60:
            parts.append(cur); cur, h = [], 0
        cur.append(st); h += sh
    parts.append(cur)
    for k, part in enumerate(parts, 1):
        mechlib.mechanism(path if k == 1 else path.replace('.svg', f'_{k}.svg'), part)


NO2 = 'c1ccc(cc1)[N+](=O)[O-]'

# ---------- A형 2번 ----------
mechanism(P('m_A02_sn2'), [
    panel('CC(=O)[O-:1].[Cl:3][CH:2]1CCCCC1', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) SN2: AcO⁻가 C–Cl 뒷면(축 방향)에서 공격'),
    '↓ 협동 단계: C–O 생성과 C–Cl 끊어짐이 동시에',
    panel('CC(=O)OC1CCCCC1.[Cl-]', h=110, legend='(2) 입체 반전: 적도 Cl → 축 OAc (B) · 고리는 단순화'),
])
mechanism(P('m_A02_ts'), [
    panel('C1CCCC[CH:2]1[OH:1].Cc1ccc(cc1)[S:3](=O)(=O)[Cl:4]', [(('lp', 1), ('a', 3)), (('b', 3, 4), ('a', 4))],
          h=150, legend='(1) ROH의 O가 TsCl의 S 공격, Cl⁻ 이탈'),
    '↓',
    panel('C1CCCC[CH:4]1[O+:1]([H:2])S(=O)(=O)c1ccc(C)cc1.c1cc[n:3]cc1', [(('lp', 3), ('a', 2)), (('b', 1, 2), ('a', 1))],
          h=150, legend='(2) pyridine이 O–H 양성자 제거'),
    '↓',
    panel('C1CCCCC1OS(=O)(=O)c1ccc(C)cc1', h=115, legend='C: C–O 결합은 끊기지 않음 → 입체 유지'),
])

# ---------- A형 3번 (산 촉매 에스터 가수분해, AAC2) ----------
mechanism(P('m_A03_hyd'), [
    panel('CC(C)(C)[C:1](=[O:2])OC.[H:3][OH2+:4]', [(('lp', 2), ('a', 3)), (('b', 3, 4), ('a', 4))],
          legend='(1) 카보닐 O 양성자화 (C의 친전자성↑)'),
    '↓',
    panel('CC(C)(C)[C:1](=[OH+:2])OC.[OH2:3]', [(('lp', 3), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(2) H₂O가 카보닐 탄소 공격'),
    '↓ 양성자 이동 (OH₂⁺ → OCH₃)',
    panel('CC(C)(C)[C:1]([OH:2])(O)[OH+:4]C', [(('lp', 2), ('b', 2, 1)), (('b', 1, 4), ('a', 4))],
          legend='(3) 사면체 중간체에서 CH₃OH 이탈'),
    '↓ −H⁺',
    panel('CC(C)(C)C(=O)O.CO', h=110, legend='(4) pivalic acid + CH₃OH'),
])

# ---------- A형 8번 ----------
mechanism(P('m_A08_os'), [
    panel('C[C:1]1=[CH:2][CH]2CC[CH]1C2.[O-:5][Os+:3](=O)(=O)=[O:4]',
          [(('b', 1, 2), ('a', 4)), (('lp', 5), ('a', 2)), (('b', 3, 4), ('a', 3))],
          h=150, legend='(1) [3+2] 고리화: OsO₄가 exo 면(C7 다리 쪽)에서 syn 첨가'),
    '↓',
    panel('CC12O[Os](=O)(=O)OC1C1CCC2C1', h=130, legend='(2) 고리형 오스메이트 에스터 (Os(VIII)→Os(VI))'),
    '↓ NaHSO₃/H₂O: Os–O 가수분해',
    panel('C[C@@]1(O)[C@H]2CC[C@H](C2)[C@@H]1O', h=120, legend='B: exo-cis-다이올 (두 C–O 유지 → syn)'),
])
mechanism(P('m_A08_hio4'), [
    panel('C[C:1]12[O:3][I:5](=O)(=O)(O)[O:4][CH:2]1C1CCC2C1',
          [(('b', 1, 2), ('b', 2, 4)), (('b', 4, 5), ('a', 5)), (('lp', 3), ('b', 3, 1)), (('b', 3, 5), ('a', 5))],
          h=160, legend='(1) 고리형 과아이오딘산 에스터의 협동 분해'),
    '↓ C–C 절단, I(VII) → I(V)',
    panel('CC(=O)[C@H]1CC[C@@H](C=O)C1.OI(=O)=O', h=125, legend='C: cis-3-acetylcyclopentane-1-carbaldehyde'),
])
mechanism(P('m_A08_acetal'), [
    panel('[H-:1].C[C@@]1([O:2][H:3])[C@H]2CC[C@H](C2)[C@@H]1O', [(('lp', 1), ('a', 3)), (('b', 2, 3), ('a', 2))],
          h=140, legend='(1) NaH: O–H 탈양성자화 (H₂ 발생)'),
    '↓',
    panel('C[C@@]1([O-:2])[C@H]2CC[C@H](C2)[C@@H]1O.[Br:4][CH2:3]Br', [(('lp', 2), ('a', 3)), (('b', 3, 4), ('a', 4))],
          h=140, legend='(2) 알콕사이드의 SN2: CH₂Br₂의 C 공격'),
    '↓ 두 번째 OH도 NaH로 탈양성자화',
    panel('C[C@@]1(O[CH2:3][Br:4])[C@H]2CC[C@H](C2)[C@@H]1[O-:5]', [(('lp', 5), ('a', 3)), (('b', 3, 4), ('a', 4))],
          h=140, legend='(3) 분자 내 SN2 → 5원 고리 아세탈'),
    '↓',
    panel('C[C@@]1(O9)[C@H]2CC[C@H](C2)[C@@H]1OC9', h=120, legend='D: 메틸렌 아세탈 (C₉H₁₄O₂, 수소결핍지수 3)'),
])

# ---------- B형 8번 ----------
FISH = True
mechanism(P('m_B08_nbs'), [
    panel('CC[CH:3]([H:2])c1ccc(cc1)[N+](=O)[O-].[Br:1]', [(('a', 1), ('nb', 1, 2)), (('b', 2, 3), ('nb', 2, 1)), (('b', 2, 3), ('a', 3))],
          legend='(1) Br•가 벤질 H 제거 (반쪽 화살표 = 전자 1개)'),
    '↓ 벤질 라디칼: 고리와 공명 안정화',
    panel('[O-][N+](=O)c1ccc(cc1)[CH:3]CC.[Br:4][Br:5]', [(('a', 3), ('nb', 3, 4)), (('b', 4, 5), ('nb', 4, 3)), (('b', 4, 5), ('a', 5))],
          legend='(2) Br₂(NBS + HBr에서 소량 공급)와 반응 → Br• 재생'),
    '↓',
    panel('BrC(CC)' + NO2, h=110, legend='벤질 브로마이드'),
])
FISH = False
mechanism(P('m_B08_e2'), [
    panel('CC[O-:1].[H:2][CH:3](C)[CH:4]([Br:5])' + NO2,
          [(('lp', 1), ('a', 2)), (('b', 2, 3), ('b', 3, 4)), (('b', 4, 5), ('a', 5))],
          legend='E2: EtO⁻가 β-H 제거, anti-periplanar Br 이탈'),
    '↓',
    panel('C/C=C/' + NO2, h=105, legend='B: (E)-알켄 (고리와 콘쥬게이션, Zaitsev)'),
])
mechanism(P('m_B08_da'), [
    panel('[CH2]1[CH:1]=[CH:2][CH:3]=[CH:4]1.C[CH:6]=[CH:5]' + NO2,
          [(('b', 3, 4), ('nb', 4, 5)), (('b', 5, 6), ('nb', 6, 1)), (('b', 1, 2), ('b', 2, 3))],
          h=150, legend='Diels–Alder [4+2]: 고리형 화살표 3개 (협동)'),
    '↓ 가열 · 엔도 규칙: π계(아릴)가 다이엔 아래로',
    panel('C[C@H]1[C@H](c2ccc([N+](=O)[O-])cc2)[C@@H]2C=C[C@H]1C2', h=130, legend='C: trans 유지, Ar endo · Me exo (라셈)'),
])
mechanism(P('m_B08_o3'), [
    panel('C[CH:1]=[CH:2]C.[O-:3][O+:4]=[O:5]', [(('lp', 3), ('a', 1)), (('b', 1, 2), ('a', 5)), (('b', 4, 5), ('a', 4))],
          legend='(1) 1,3-쌍극자 첨가 (반응하는 C=C만 표시)'),
    '↓',
    panel('C[CH:1]1[CH:2](C)[O:5][O:4][O:3]1', [(('b', 1, 2), ('b', 1, 3)), (('b', 3, 4), ('b', 4, 5)), (('b', 5, 2), ('a', 5))],
          h=120, legend='(2) 1차 오존화물 → 역[3+2] 분해'),
    '↓ 카보닐 옥사이드 → 2차 오존화물 → Me₂S',
    panel('C[C@H]1[C@H](c2ccc([N+](=O)[O-])cc2)[C@H](C=O)C[C@@H]1C=O', h=130, legend='D: cis-1,3-다이알데하이드 (C₁₄H₁₅NO₄, 라셈)'),
])

# ---------- B형 9번 ----------
mechanism(P('m_B09_fischer'), [
    panel('c1ccccc1[C:1](=[O:2])O.[H:3][O:4]S(=O)(=O)O', [(('lp', 2), ('a', 3)), (('b', 3, 4), ('a', 4))],
          legend='(1) H₂SO₄가 카보닐 O 양성자화'),
    '↓',
    panel('c1ccccc1[C:1](=[OH+:2])O.C[OH:3]', [(('lp', 3), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(2) CH₃OH가 카보닐 탄소 공격'),
    '↓ 양성자 이동 (CH₃OH⁺ → OH)',
    panel('c1ccccc1[C:1]([OH:2])(OC)[OH2+:4]', [(('lp', 2), ('b', 2, 1)), (('b', 1, 4), ('a', 4))],
          legend='(3) H₂O 이탈'),
    '↓ −H⁺ (과량 CH₃OH → 평형 이동)',
    panel('COC(=O)c1ccccc1', h=105, legend='A: methyl benzoate'),
])
mechanism(P('m_B09_meli'), [
    panel('c1ccccc1C(=O)[O:1][H:2].[CH3-:3]', [(('lp', 3), ('a', 2)), (('b', 1, 2), ('a', 1))],
          legend='(1) 1당량째 CH₃Li: 산–염기 반응 (CH₄ 발생)'),
    '↓',
    panel('c1ccccc1[C:1](=[O:2])[O-].[CH3-:3]', [(('lp', 3), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(2) 2당량째: 카복실레이트 C=O에 첨가'),
    '↓ 다이알콕사이드: 더 첨가되지 않음',
    panel('c1ccccc1C(C)([O-])[O-]', h=110, legend='(3) 반응 혼합물 속 중간체'),
    '↓ H₃O⁺ 처리 → 수화물(gem-다이올)',
    panel('c1ccccc1[C:2](C)([OH:1])[OH2+:3]', [(('lp', 1), ('b', 1, 2)), (('b', 2, 3), ('a', 3))],
          legend='(4) 물 이탈'),
    '↓ −H⁺',
    panel('CC(=O)c1ccccc1', h=105, legend='acetophenone (3차 알코올이 아님)'),
])
