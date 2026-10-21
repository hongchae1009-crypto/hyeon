"""안병천 2회 유기 문항의 메커니즘 그림(굽은 화살표)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_tools'))
from mechlib import panel, mechanism

IMG = os.path.join(os.path.dirname(__file__), '..', 'img')
P = lambda n: os.path.join(IMG, n + '.svg')

# ---------- A형 2번: 짝염기의 안정화 ----------
mechanism(P('m_A02_A'), [
    panel('O=C1CCCCC1C(=O)[O:1][H:2].[OH-:3]', [(('lp', 3), ('a', 2)), (('b', 1, 2), ('a', 1))],
          legend='A: O–H(Hc) 제거'),
    '↓',
    panel('O=C1CCCCC1[C:4](=[O:5])[O-:1]', [(('lp', 1), ('b', 1, 4)), (('b', 4, 5), ('a', 5))],
          legend='카복실레이트: O 두 개에 분산 (pKa≈4)'),
])
mechanism(P('m_A02_B'), [
    panel('c1ccccc1CC(=O)[CH:1]([H:2])C(=O)CC.[OH-:3]', [(('lp', 3), ('a', 2)), (('b', 1, 2), ('a', 1))],
          legend='B: 두 C=O 사이 Hb 제거'),
    '↓',
    panel('c1ccccc1C[C:4](=[O:5])[CH-:1]C(=O)CC', [(('lp', 1), ('b', 1, 4)), (('b', 4, 5), ('a', 5))],
          legend='엔올레이트: O 두 개+C에 분산 (pKa≈9)'),
])
mechanism(P('m_A02_C'), [
    panel('C[C:6](=[O:7])[C:5]1=[CH:4][CH:3]([H:2])CCC1.[OH-:1]', [(('lp', 1), ('a', 2)), (('b', 3, 2), ('a', 3))],
          legend='C: γ-위치(C3)의 Hc 제거'),
    '↓',
    panel('C[C:6](=[O:7])[C:5]1=[CH:4][CH-:3]CCC1',
          [(('lp', 3), ('b', 3, 4)), (('b', 4, 5), ('b', 5, 6)), (('b', 6, 7), ('a', 7))],
          legend='확장 엔올레이트: 음전하가 O까지'),
    '↓ 비교: Ha(C6) 제거',
    panel('C[C:6](=[O:7])[C:5]1=[CH:4]CCC[CH-:8]1', [(('lp', 8), ('b', 8, 5)), (('b', 5, 4), ('a', 4))],
          legend='C6 음이온: O까지 못 감 (교차 콘쥬게이션)'),
])

# ---------- A형 8번 ----------
mechanism(P('m_A08_hb'), [
    panel('CC(C)[C:1]1=[CH:2]CCCC1.C[B:3]([H:4])C', [(('b', 1, 2), ('a', 3)), (('b', 3, 4), ('a', 1))],
          legend='(1) syn 첨가: B→C2, H→C1'),
    '↓ 4중심 전이 상태 (자리옮김 없음)',
    panel('CB(C)[C@H]1CCCC[C@@H]1C(C)C', h=115, legend='(2) 보레인: B와 iPr는 trans'),
])
mechanism(P('m_A08_hb2'), [
    panel('C[B:1](C)[C@H:2]1CCCC[C@@H]1C(C)C.[O-:3][OH:4]', [(('lp', 3), ('a', 1))],
          legend='(3) H₂O₂, NaOH: HOO⁻가 B의 빈 p 오비탈 공격'),
    '↓',
    panel('C[B-:1](C)([C@H:2]1CCCC[C@@H]1C(C)C)[O:3][OH:4]', [(('b', 1, 2), ('a', 3)), (('b', 3, 4), ('a', 4))],
          legend='(4) 1,2-이동(배열 유지), HO⁻ 이탈'),
    '↓ 가수분해(B–O 절단)',
    panel('O[C@H]1CCCC[C@@H]1C(C)C', h=115, legend='A trans-2-isopropylcyclohexanol'),
])
mechanism(P('m_A08_B'), [
    panel('CC(C)C1CCCC[CH:4]1[OH:1].Cl[P:2](=O)(Cl)[Cl:3]', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) O가 P 공격, Cl⁻ 이탈'),
    '↓ –OPOCl₂: 좋은 이탈기',
    panel('c1cc[n:1]cc1.[H:2][CH:3]1CCC[CH:5](C(C)C)[CH:4]1[O:6]P(=O)(Cl)Cl',
          [(('lp', 1), ('a', 2)), (('b', 2, 3), ('b', 3, 4)), (('b', 4, 6), ('a', 6))],
          legend='(2) E2: 피리딘이 C6(CH₂) 축 H 제거'),
    '↓',
    panel('CC(C)C1CCCC=C1', h=105, legend='B 3-isopropylcyclohexene'),
])
mechanism(P('m_A08_C'), [
    panel('CC(C)C1CCCC[CH:4]1[OH:1].Cc1ccc(cc1)[S:2](=O)(=O)[Cl:3]', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) O가 S 공격, Cl⁻ 이탈 → OTs'),
    '↓',
    panel('CC(C)(C)[O-:1].[H:2][CH:3]1CCC[CH:5](C(C)C)[CH:4]1[O:6]S(=O)(=O)C',
          [(('lp', 1), ('a', 2)), (('b', 2, 3), ('b', 3, 4)), (('b', 4, 6), ('a', 6))],
          legend='(2) E2: t-BuO⁻가 C6(CH₂) 축 H 제거'),
    '↓',
    panel('CC(C)C1CCCC=C1', h=105, legend='C = B (3-isopropylcyclohexene)'),
])

# ---------- B형 8번: Na / NH3(l) 용해 금속 환원 ----------
mechanism(P('m_B08_na'), [
    panel('[CH:1]#[C:2][C@H](C)CC', h=100, legend='(1) Na가 준 전자 1개 → π*'),
    '↓ + e⁻',
    panel('[CH-:1]=[C:2][C@H](C)CC.[H:3][NH2:4]', [(('lp', 1), ('a', 3)), (('b', 3, 4), ('a', 4))],
          legend='(2) 탄소음이온이 NH₃의 H⁺ 제거'),
    '↓ + e⁻ (바이닐 음이온)',
    panel('[CH2:1]=[C-:2][C@H](C)CC.[H:3][NH2:4]', [(('lp', 2), ('a', 3)), (('b', 3, 4), ('a', 4))],
          legend='(3) 두 번째 양성자화'),
    '↓',
    panel('C=C[C@H](C)CC', h=100, legend='D 3-methylpent-1-ene (= B)'),
])

# ---------- B형 9번 ----------
mechanism(P('m_B09_ms'), [
    panel('[OH:1][CH]1CCCC2([2H])CCCCC12.C[S:2](=O)(=O)[Cl:3]', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) O가 S 공격, Cl⁻ 이탈 → B'),
    '↓ NaOMe, 가열',
    panel('C[O-:1].[H:2][C:3]12CCCCC1([2H])CCC[CH:4]2[O:5]S(C)(=O)=O',
          [(('lp', 1), ('a', 2)), (('b', 2, 3), ('b', 3, 4)), (('b', 4, 5), ('a', 5))],
          legend='(2) E2: C8a–H와 C1–OMs anti'),
    '↓',
    panel('[2H]C12CCCCC1=CCCC2', h=105, legend='C Δ¹⁽⁸ᵃ⁾-옥탈린 (C1=C8a)'),
])
mechanism(P('m_B09_hb'), [
    panel('[2H]C12CCCC[C:1]1=[CH:2]CCC2.[2H][B:3]([2H])[2H:4]', [(('b', 1, 2), ('a', 3)), (('b', 3, 4), ('a', 1))],
          legend='(1) BD₃ syn 첨가: B→C1, D→C8a'),
    '↓ C4a–D 반대 면에서 접근',
    panel('[2H]B([2H])[C@H]1CCC[C@@]2([2H])CCCC[C@]12[2H]', h=125,
          legend='(2) B·C8a–D 같은 면 (trans 접합)'),
    '↓ H₂O₂, NaOH (배열 유지)',
    panel('O[C@H]1CCC[C@@]2([2H])CCCC[C@]12[2H]', h=125, legend='D: OH 적도, 접합 탄소 둘 다 D'),
])
