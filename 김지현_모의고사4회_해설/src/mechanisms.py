"""김지현 4회 유기 문항의 메커니즘 그림(굽은 화살표)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_tools'))
from mechlib import panel, mechanism

IMG = os.path.join(os.path.dirname(__file__), '..', 'img')
P = lambda n: os.path.join(IMG, n + '.svg')

# ---------- A형 10번 [반응 1]: Ag⁺ 보조 SN1 ----------
mechanism(P('m_A10_sn1'), [
    panel('C[C:1](C)=[CH:2][CH2:3][Cl:4].[Ag+:5]', [(('b', 3, 4), ('a', 4)), (('lp', 4), ('a', 5))],
          legend='(1) Ag⁺가 Cl을 끌어당겨 C–Cl 이탈 (AgCl↓)'),
    '↓ 3-chloro-3-methyl-1-butene도 같은 양이온',
    panel('C[C:1](C)=[CH:2][CH2+:3]', [(('b', 1, 2), ('b', 2, 3))],
          legend='(2) 알릴 양이온 A의 공명 (1차 쪽 ↔ 3차 쪽)'),
    '↔',
    panel('C[C+:1](C)[CH:2]=[CH2:3]', h=110, legend='3차 탄소 양전하 구조 (기여 큼)'),
    '↓ H₂O',
    panel('[OH2:6].C[C+:1](C)C=C', [(('lp', 6), ('a', 1))],
          legend='(3) 물이 3차 탄소 공격 (양전하 밀도 큼)'),
    '↓ −H⁺',
    panel('CC(C)(O)C=C', h=105, legend='B 2-methyl-3-buten-2-ol (85%)'),
])
mechanism(P('m_A10_minor'), [
    panel('[OH2:6].C[C:1](C)=C[CH2+:3]', [(('lp', 6), ('a', 3))],
          legend='1차 탄소 쪽 공명 구조를 물이 공격'),
    '↓ −H⁺',
    panel('CC(C)=CCO', h=105, legend='C 3-methyl-2-buten-1-ol (15%)'),
])
# ---------- A형 10번 [반응 2]: HBr 1,2/1,4-첨가 ----------
mechanism(P('m_A10_hbr'), [
    panel('[CH2:1]=[C:2](C)[C:3](C)=[CH2:4].[H:5][Br:6]', [(('b', 1, 2), ('a', 5)), (('b', 5, 6), ('a', 6))],
          legend='(1) 말단 C=C가 H⁺ 공격 → 3차·알릴 양이온 D'),
    '↓',
    panel('[CH3:1][C+:2](C)[C:3](C)=[CH2:4]', [(('b', 3, 4), ('b', 2, 3))],
          legend='(2) D의 공명: C2 ↔ C4에 양전하'),
    '↔',
    panel('[CH3:1][C:2](C)=[C:3](C)[CH2+:4]', h=110, legend='C4 양전하 구조'),
    '↓ Br⁻',
    panel('[Br-:6].[CH3:1][C+:2](C)[C:3](C)=[CH2:4]', [(('lp', 6), ('a', 2))],
          legend='(3a) 가까운 C2 공격 → E (1,2-첨가, 속도론적)'),
    '',
    panel('[Br-:6].[CH3:1][C:2](C)=[C:3](C)[CH2+:4]', [(('lp', 6), ('a', 4))],
          legend='(3b) C4 공격 → F (1,4-첨가, 열역학적)'),
    '↓',
    panel('C=C(C)C(C)(C)Br.CC(C)=C(C)CBr', h=110, legend='E (이치환 알켄)            F (사치환 알켄, 더 안정)'),
])

# ---------- A형 11번 ----------
mechanism(P('m_A11_A'), [
    panel('[OH-:1].Cl[C@@H]1CCCC[C@H]1[O:2][H:3]', [(('lp', 1), ('a', 3)), (('b', 2, 3), ('a', 2))],
          legend='(1) trans: OH 탈양성자화 → 알콕사이드'),
    '↓ 고리 뒤집기: O⁻와 Cl이 trans-diaxial',
    panel('[Cl:4][C@@H:5]1CCCC[C@H:6]1[O-:2]', [(('lp', 2), ('a', 5)), (('b', 5, 4), ('a', 4))],
          legend='(2) O⁻가 C–Cl 뒤쪽에서 분자 내 SN2'),
    '↓ −Cl⁻',
    panel('C1CCC2OC2C1', h=105, legend='A cyclohexene oxide'),
])
mechanism(P('m_A11_B'), [
    panel('[OH-:1].[Cl:4][C@H:5]1CCCC[C:6]1([H:7])[OH:2]', [(('lp', 1), ('a', 7)), (('b', 6, 7), ('b', 6, 5)), (('b', 5, 4), ('a', 4))],
          legend='(1) cis: C1–H가 Cl과 anti → E2'),
    '↓ −Cl⁻',
    panel('[OH:2][C:6]1=[CH:5]CCCC1', h=110, legend='(2) 엔올'),
    '↓ 토토머화 (양성자 이동)',
    panel('O=C1CCCCC1', h=105, legend='B cyclohexanone'),
])
mechanism(P('m_A11_C'), [
    panel('CC(C)(C)C1CC[C:1](=[CH2:2])CC1.[O:3]([H:4])[O:5]C(=O)c1cccc(Cl)c1',
          [(('b', 1, 2), ('a', 3)), (('b', 3, 5), ('a', 5))],
          legend='(1) mCPBA: C=C가 말단 O 공격 (협동, 나비형 TS)'),
    '↓ 덜 막힌 적도 방향에서 접근',
    panel('CC(C)(C)C1CCC2(CC1)CO2', h=110, legend='C 에폭사이드 O 적도·CH₂ 축'),
])
mechanism(P('m_A11_D'), [
    panel('CC(C)(C)C1CC[C:1](=[CH2:2])CC1.[Br:3][Br:4]', [(('b', 1, 2), ('a', 3)), (('b', 3, 4), ('a', 4))],
          legend='(1) Br₂ → 브로모늄 이온'),
    '↓ H₂O가 3차 탄소를 축 방향에서 공격',
    panel('[OH2:5].CC(C)(C)C1CC[C:1]2(CC1)[CH2:2][Br+:3]2', [(('lp', 5), ('a', 1)), (('b', 1, 3), ('a', 3))],
          legend='(2) 개환 → 할로하이드린 (OH 축)'),
    '↓ −H⁺, NaH',
    panel('CC(C)(C)C1CC[C:1]([O-:5])([CH2:2][Br:3])CC1', [(('lp', 5), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(3) O⁻가 CH₂Br을 분자 내 SN2'),
    '↓ −Br⁻',
    panel('CC(C)(C)C1CCC2(CC1)CO2', h=110, legend='D 에폭사이드 O 축 (C의 부분입체이성질체)'),
])

# ---------- B형 1번: Stork 엔아민 → 가수분해 → aldol 고리화 ----------
mechanism(P('m_B01_michael'), [
    panel('C1CC[N:1](C1)[C:2]1=[CH:3]c2ccccc2CC1.[CH2:4]=[CH:5][C:6](C)=[O:7]',
          [(('lp', 1), ('b', 1, 2)), (('b', 2, 3), ('a', 4)), (('b', 4, 5), ('b', 5, 6)), (('b', 6, 7), ('a', 7))],
          legend='(1) 엔아민 β-탄소(C1)가 MVK β-탄소 공격'),
    '↓',
    panel('C1CC[N+:1](C1)=[C:2]1CCc2ccccc2[CH:3]1C[CH:5]=[C:6](C)[O-:7]', h=150,
          legend='(2) 이미늄 + 엔올레이트 (양성자 이동)'),
    '↓ H₂O 매개 양성자 이동',
    panel('C1CCN(C1)C1=CCc2ccccc2C1CCC(C)=O', h=130, legend='A 엔아민 Michael 부가물 (C₁₈H₂₃NO)'),
])
mechanism(P('m_B01_hyd'), [
    panel('[H+:8].C1CCN(C1)[C:2]1=[CH:3]Cc2ccccc2C1CCC(C)=O', [(('b', 2, 3), ('a', 8))],
          legend='(1) 엔아민 β-탄소 양성자화 → 이미늄'),
    '↓ H₂O',
    panel('[OH2:9].C1CC[N+:1](C1)=[C:2]1CCc2ccccc2C1CCC(C)=O', [(('lp', 9), ('a', 2)), (('b', 1, 2), ('a', 1))],
          legend='(2) 물이 이미늄 탄소 공격'),
    '↓ 양성자 이동 (N 양성자화)',
    panel('C1CC[NH+:1](C1)[C:2]1([OH:9])CCc2ccccc2C1CCC(C)=O', [(('lp', 9), ('b', 9, 2)), (('b', 2, 1), ('a', 1))],
          legend='(3) C=O 재생, 피롤리딘 이탈'),
    '↓ −H⁺',
    panel('O=C1CCc2ccccc2C1CCC(C)=O', h=120, legend='B (C₁₄H₁₆O₂)'),
])
mechanism(P('m_B01_aldol'), [
    panel('[OH-:1].O=C1CCc2ccccc2C1CCC(=O)[CH2:2][H:3]', [(('lp', 1), ('a', 3)), (('b', 2, 3), ('a', 2))],
          legend='(1) 메틸 케톤 CH₃ 탈양성자화 → 엔올레이트'),
    '↓',
    panel('[O:4]=[C:5]1CCc2ccccc2C1CCC(=O)[CH2-:2]', [(('lp', 2), ('a', 5)), (('b', 5, 4), ('a', 4))],
          legend='(2) 분자 내 aldol: 고리 C=O 공격 (6원 고리)'),
    '↓ H₂O (양성자화)',
    panel('[OH-:1].O[C:5]12CCc3ccccc3C1CC[C:6](=[O:7])[CH:8]2[H:10]', [(('lp', 1), ('a', 10)), (('b', 8, 10), ('a', 8))], h=145,
          legend='(3) β-하이드록시 케톤: 염기가 α-H 제거'),
    '↓',
    panel('[OH:9][C:5]12CCc3ccccc3C1CC[C:6](=[O:7])[CH-:8]2', [(('lp', 8), ('b', 8, 5)), (('b', 5, 9), ('a', 9))],
          legend='(4) E1cB: OH⁻ 이탈'),
    '↓',
    panel('O=C1C=C2CCc3ccccc3C2CC1', h=120, legend='C 삼환 엔온 (C₁₄H₁₄O)'),
])

# ---------- B형 10번 ----------
mechanism(P('m_B10_epox'), [
    panel('C[C:1]1=[CH:2]CCC2C(C(C)(C)O)CCC2(C)C1.[O:3]([H:4])[O:5]C(C)=O',
          [(('b', 1, 2), ('a', 3)), (('b', 3, 5), ('a', 5))],
          legend='(1) mCPBA: 전자 풍부한 삼치환 C=C 에폭시화'),
    '↓ (NaHCO₃: 산을 중화해 에폭사이드 개환 방지)',
    panel('CC12OC1CCC1C(C(C)(C)O)CCC1(C)C2', h=120, legend='B (C₁₅H₂₆O₂)'),
])
mechanism(P('m_B10_socl2'), [
    panel('CC12OC1CCC1C(C(C)(C)[OH:1])CCC1(C)C2.[S:2](=O)([Cl:3])Cl', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) OH의 O가 S 공격, Cl⁻ 이탈'),
    '↓ Et₃N: O–H 탈양성자화',
    panel('CC12OC1CCC1C([C:4](C)([CH2:5][H:6])[O:7][S:8](=O)Cl)CCC1(C)C2.N(CC)(CC)[CH2:9]C',
          [(('lp', 9), ('a', 6)), (('b', 5, 6), ('b', 5, 4)), (('b', 4, 7), ('a', 7))], h=150,
          legend='(2) E2: Et₃N이 CH₃의 H 제거, OS(O)Cl 이탈'),
    '↓ −SO₂, −Cl⁻, −Et₃NH⁺',
    panel('CC12OC1CCC1C(C(C)=C)CCC1(C)C2', h=120, legend='C 이소프로펜일 (C₁₅H₂₄O)'),
])
mechanism(P('m_B10_cleave'), [
    panel('CC12OC1CCC1C([C:1](C)=[CH2:2])CCC1(C)C2', h=120, legend='C'),
    '↓ OsO₄ (syn 다이하이드록시화), NMO로 Os 재산화',
    panel('CC12OC1CCC1C([C:1](C)([OH:3])[CH2:2][OH:4])CCC1(C)C2', h=125, legend='1,2-다이올'),
    '↓ NaIO₄: 고리형 아이오데이트 에스터 → C–C 절단',
    panel('CC12OC1CCC1C(C(C)=O)CCC1(C)C2.C=O', h=125, legend='D 메틸 케톤 (C₁₄H₂₂O₂) + HCHO'),
])
