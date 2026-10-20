"""김지현 6회 유기 문항의 메커니즘 그림(굽은 화살표)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_tools'))
from mechlib import panel, mechanism

IMG = os.path.join(os.path.dirname(__file__), '..', 'img')
P = lambda n: os.path.join(IMG, n + '.svg')
from rdkit import Chem


def lab(smi, *names):
    """SMILES의 * 자리에 차례로 이름표(Ph, CO₂Et 등)를 붙인 CXSMILES를 만든다."""
    p = Chem.SmilesParserParams()
    p.removeHs = False
    m = Chem.MolFromSmiles(smi, p)
    it = iter(names)
    labels = [next(it) if a.GetAtomicNum() == 0 else '' for a in m.GetAtoms()]
    return smi + ' |$' + ';'.join(labels) + '$|'

# ---------- A형 10번 ----------
mechanism(P('m_A10_acid'), [
    panel('CC[C:1]1(C)[CH2:2][O:3]1.[H:4][18OH2+:5]', [(('lp', 3), ('a', 4)), (('b', 4, 5), ('a', 5))],
          legend='(1) 에폭사이드 O 양성자화'),
    '↓',
    panel('[18OH2:6].CC[C:1]1(C)[CH2:2][OH+:3]1', [(('lp', 6), ('a', 1)), (('b', 1, 3), ('a', 3))],
          legend='(2) H₂¹⁸O가 3차 탄소(δ+ 큼)를 뒤쪽에서 공격'),
    '↓ 3차 탄소 배열 반전 (anti)',
    panel('CC[C:1](C)([18OH+:6][H:8])CO.[OH2:7]', [(('lp', 7), ('a', 8)), (('b', 6, 8), ('a', 6))],
          legend='(3) 탈양성자화'),
    '↓',
    panel('CCC(C)([18OH])CO', h=105, legend='A (¹⁸O가 3차 탄소에)'),
])
mechanism(P('m_A10_base'), [
    panel('[18OH-:1].[CH2:2]1[O:3][C:4]1(C)CC', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) ¹⁸OH⁻가 덜 막힌 CH₂를 SN2 공격'),
    '↓ 고리 열림',
    panel('[18OH][CH2]C(C)(CC)[O-:3].[H:4][OH:5]', [(('lp', 3), ('a', 4)), (('b', 4, 5), ('a', 5))],
          legend='(2) 알콕사이드 양성자화 (H₂O)'),
    '↓ 3차 탄소 배열 유지',
    panel('CCC(C)(O)C[18OH]', h=105, legend='B (¹⁸O가 1차 탄소에)'),
])

# ---------- A형 11번 ----------
mechanism(P('m_A11_B'), [
    panel('[OH-:1].[H:3][C:2]1(c2ccccc2)C=CC=C1', [(('lp', 1), ('a', 3)), (('b', 2, 3), ('a', 2))],
          legend='(1) B의 sp³ C–H 제거'),
    '↓',
    panel('c1ccccc1[C-:2]1[CH:3]=[CH:4][CH]=[CH]1', [(('lp', 2), ('b', 2, 3)), (('b', 3, 4), ('a', 4))],
          legend='(2) 음전하가 고리 다섯 탄소에 비편재화'),
    '↓',
    panel('[cH-]1cccc1-c1ccccc1', h=110, legend='6π 방향족 Cp⁻ → B가 더 산성'),
])
mechanism(P('m_A11_D'), [
    panel('[OH-:6].[H:5][CH2:4][C:1](C)=[C:2]1[CH:3]=CC(C)=C1',
          [(('lp', 6), ('a', 5)), (('b', 4, 5), ('b', 4, 1)), (('b', 1, 2), ('a', 2))],
          legend='(1) D의 CH₃ H 제거: π 전자가 고리 탄소로'),
    '↓',
    panel('C=C(C)c1[cH-]cc(C)c1', h=110, legend='(2) 방향족 Cp⁻ (6π) → D가 가장 산성'),
])

# ---------- B형 1번 ----------
mechanism(P('m_B01_no2'), [
    panel('[O-:4][N+:2](=[O:1])[OH2+:3]', [(('lp', 4), ('b', 4, 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) HNO₃ + H₂SO₄ → H₂NO₃⁺, H₂O 이탈'),
    '↓',
    panel('O=[N+]=O', h=95, legend='나이트로늄 이온 NO₂⁺'),
])
mechanism(P('m_B01_c2'), [
    panel('[NH:1]1[CH:2]=[CH:3][CH:4]=[CH:5]1.[O:6]=[N+:7]=[O:8]',
          [(('b', 2, 3), ('a', 7)), (('b', 7, 8), ('a', 8))],
          legend='(1) C2 공격: C2=C3 π가 NO₂⁺에'),
    '↓ σ 착물 공명구조 3개',
    panel('[NH:1]1[CH:2]([N+](=O)[O-])[CH+:3][CH:4]=[CH:5]1', [(('b', 4, 5), ('b', 3, 4))],
          legend='(2a) C3에 양전하'),
    '↕',
    panel('[NH:1]1[CH:2]([N+](=O)[O-])[CH:3]=[CH:4][CH+:5]1', [(('lp', 1), ('b', 1, 5))],
          legend='(2b) C5에 양전하'),
    '↕',
    panel('[NH+:1]1=[CH:5][CH:4]=[CH:3][CH:2]1[N+](=O)[O-]', h=120,
          legend='(2c) N⁺: 모든 원자 옥텟 (가장 큰 기여)'),
])
mechanism(P('m_B01_c2b'), [
    panel('[O-:10]S(=O)(=O)O.[NH:1]1[C:2]([H:9])([N+](=O)[O-])[CH+:3][CH:4]=[CH:5]1',
          [(('lp', 10), ('a', 9)), (('b', 2, 9), ('b', 2, 3))],
          legend='(3) C2–H 제거 → 방향족성 회복'),
    '↓',
    panel('[O-][N+](=O)c1ccc[nH]1', h=105, legend='C 2-nitropyrrole (주생성물)'),
])
mechanism(P('m_B01_c3'), [
    panel('[NH:1]1[CH:2]=[CH:3][CH:4]=[CH:5]1.[O:6]=[N+:7]=[O:8]',
          [(('b', 2, 3), ('a', 7)), (('b', 7, 8), ('a', 8))],
          legend='(1) C3 공격: C2=C3 π 사용, 양전하는 C2'),
    '↓ σ 착물 공명구조 2개',
    panel('[NH:1]1[CH+:2][CH:3]([N+](=O)[O-])[CH:4]=[CH:5]1', [(('lp', 1), ('b', 1, 2))],
          legend='(2a) C2에 양전하 (C4=C5와 콘쥬게이션 안 됨)'),
    '↕',
    panel('[NH+:1]1=[CH:2][CH:3]([N+](=O)[O-])[CH:4]=[CH:5]1', h=120, legend='(2b) N⁺ — 공명구조 2개뿐 → 덜 안정'),
    '↓ −H⁺',
    panel('[O-][N+](=O)c1cc[nH]c1', h=105, legend='D 3-nitropyrrole (부생성물)'),
])

# ---------- B형 11번 ---------- (CO₂Et, Ph는 이름표로 줄여 표기)
E = 'CO<sub>2</sub>Et'
mechanism(P('m_B11_knoev'), [
    panel(lab('CC[O-:1].[H:3][CH:2](*)*', E, E), [(('lp', 1), ('a', 3)), (('b', 2, 3), ('a', 2))],
          legend='(1) EtO⁻가 활성 메틸렌 H 제거 (pKa ≈ 13)'),
    '↓',
    panel(lab('*[CH-:2]*.[O:4]=[CH:5]c1ccccc1', E, E), [(('lp', 2), ('a', 5)), (('b', 5, 4), ('a', 4))],
          legend='(2) 엔올레이트가 C=O 탄소 공격'),
    '↓',
    panel(lab('*[CH:2](*)[CH:5]([O-:4])c1ccccc1', E, E), h=110, legend='알콕사이드 중간체'),
])
mechanism(P('m_B11_knoev2'), [
    panel(lab('*[CH:2](*)[CH:5]([O-:4])c1ccccc1.[H:6][O:7]CC', E, E), [(('lp', 4), ('a', 6)), (('b', 6, 7), ('a', 7))],
          legend='(3) 알콕사이드 양성자화 (EtOH)'),
    '↓ EtO⁻',
    panel(lab('CC[O-:1].*[C:2]([H:3])(*)[CH:5]([OH:4])c1ccccc1', E, E),
          [(('lp', 1), ('a', 3)), (('b', 2, 3), ('b', 2, 5)), (('b', 5, 4), ('a', 4))],
          legend='(4) E1cB 탈수: α-H 제거 → OH⁻ 이탈'),
    '↓',
    panel(lab('*C(*)=Cc1ccccc1', E, E), h=110, legend='Knoevenagel 생성물'),
])
mechanism(P('m_B11_decarb'), [
    panel(lab('*C(*)=Cc1ccccc1', E, E), h=110, legend='Knoevenagel 생성물'),
    '↓ H₃O⁺, 가열: 에스터 가수분해 (−2 EtOH)',
    panel(lab('[O:1]=[C:2]([OH])[C:4](=C*)[C:5](=[O:6])[O:7][H:8]', 'Ph'),
          [(('lp', 1), ('a', 8)), (('b', 7, 8), ('b', 7, 5)), (('b', 5, 4), ('b', 4, 2)), (('b', 2, 1), ('a', 1))],
          h=160, legend='(1) 고리형 전이 상태: H 이동과 C–C 끊김이 동시에'),
    '↓ −CO₂',
    panel('OC(O)=C=Cc1ccccc1', h=110, legend='(2) 엔다이올 (불안정)'),
    '↓ 토토머화',
    panel('OC(=O)/C=C/c1ccccc1', h=105, legend='C cinnamic acid (C₉H₈O₂)'),
])
mechanism(P('m_B11_hydrazone'), [
    panel('c1ccccc1N[NH2:1].[O:2]=[CH:3]c1ccccc1', [(('lp', 1), ('a', 3)), (('b', 3, 2), ('a', 2))],
          legend='(1) 말단 NH₂가 C=O 탄소 공격'),
    '↓ 양성자 이동, H⁺',
    panel('c1ccccc1N[NH:1][CH:3]([OH2+:2])c1ccccc1', [(('lp', 1), ('b', 1, 3)), (('b', 3, 2), ('a', 2))],
          legend='(2) N이 밀어내며 H₂O 이탈'),
    '↓ −H⁺',
    panel('c1ccccc1N/N=C/c1ccccc1', h=105, legend='A phenylhydrazone'),
])
mechanism(P('m_B11_wittig'), [
    panel(lab('[P+:4](*)(*)(*)[CH-:1]C=C.[O:2]=[CH:3]c1ccccc1', 'Ph', 'Ph', 'Ph'),
          [(('lp', 1), ('a', 3)), (('b', 3, 2), ('a', 2))],
          legend='(1) 일라이드 탄소가 C=O 탄소 공격'),
    '↓',
    panel(lab('C=C[CH:1]([P+:4](*)(*)*)[CH:3]([O-:2])c1ccccc1', 'Ph', 'Ph', 'Ph'), [(('lp', 2), ('a', 4))],
          legend='(2) O⁻가 P⁺에 결합 → 4원 고리'),
    '↓',
    panel(lab('C=C[CH:1]1[CH:3](c2ccccc2)[O:2][P:4]1(*)(*)*', 'Ph', 'Ph', 'Ph'),
          [(('b', 1, 4), ('b', 1, 3)), (('b', 2, 3), ('b', 2, 4))],
          legend='(3) 옥사포스페테인 분해 (P=O 결합이 매우 강함)'),
    '↓ −Ph₃P=O',
    panel('C=C/C=C/c1ccccc1', h=105, legend='B 1-phenyl-1,3-butadiene'),
])
