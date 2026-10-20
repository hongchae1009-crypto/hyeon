"""김지현 1회 유기 문항의 메커니즘 그림(굽은 화살표)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_tools'))
from mechlib import panel, mechanism

IMG = os.path.join(os.path.dirname(__file__), '..', 'img')
P = lambda n: os.path.join(IMG, n + '.svg')

# ---------- A형 10번 ----------
mechanism(P('m_A10_alk'), [
    panel('[NH2-:1].CC(=O)[CH:2]([H:3])C(C)=O', [(('lp', 1), ('a', 3)), (('b', 2, 3), ('a', 2))],
          legend='(1) 염기 1당량: 가장 산성인 가운데 H 제거'),
    '↓',
    panel('[NH2-:1].[H:3][CH2:2]C(=O)[CH-]C(C)=O', [(('lp', 1), ('a', 3)), (('b', 2, 3), ('a', 2))],
          legend='(2) 염기 2당량째: 말단 CH₃의 H 제거 → 다이음이온'),
    '↓ CH₃I',
    panel('[CH2-:1]C(=O)[CH-]C(C)=O.[CH3:2][I:3]', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(3) 덜 안정(더 반응적)한 말단 탄소가 SN2'),
    '↓ H₃O⁺',
    panel('CCC(=O)CC(C)=O', h=100, legend='A 2,4-hexanedione'),
])
mechanism(P('m_A10_michael'), [
    panel('CC(=O)[CH-:1]C(C)=O.[CH2:2]=[CH:3][C:4](C)=[O:5]',
          [(('lp', 1), ('a', 2)), (('b', 2, 3), ('b', 3, 4)), (('b', 4, 5), ('a', 5))],
          legend='(1) Michael: 엔올레이트가 MVK의 β-탄소 공격'),
    '↓',
    panel('CC(=O)C(C(C)=O)C[CH:3]=[C:4](C)[O-:5].[H:6][OH:7]',
          [(('lp', 5), ('b', 5, 4)), (('b', 4, 3), ('a', 6)), (('b', 6, 7), ('a', 7))],
          legend='(2) 엔올레이트의 α-탄소 양성자화'),
    '↓',
    panel('CC(=O)C(C(C)=O)CCC(C)=O', h=110, legend='1,5-다이카보닐 (Michael 부가물)'),
])
mechanism(P('m_A10_aldol'), [
    panel('[CH2-:1]C(=O)C(C(C)=O)CC[C:2](C)=[O:3]', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) 아세틸 CH₃ 엔올레이트 → 고리 C=O 공격'),
    '↓ 6원 고리 알콕사이드, 양성자화',
    panel('O=C1CC(C)(O)CCC1C(C)=O', h=115, legend='(2) β-하이드록시 케톤'),
    '↓ 염기: α-H 제거',
    panel('[O-:1][C:2]1=[CH:3][C:4](C)([OH:5])CCC1C(C)=O',
          [(('lp', 1), ('b', 1, 2)), (('b', 2, 3), ('b', 3, 4)), (('b', 4, 5), ('a', 5))],
          legend='(3) E1cB 탈수: OH⁻ 이탈'),
    '↓',
    panel('CC(=O)C1CCC(C)=CC1=O', h=110, legend='C (D: MVK의 CH₃가 아세틸 C=O 공격)'),
])
mechanism(P('m_A10_E'), [
    panel('CC(=O)[CH-:1]C(C)=O.[CH2:6]1[CH2]C[C:4](=[O:5])[CH:3]=[CH:2]1',
          [(('lp', 1), ('a', 2)), (('b', 2, 3), ('b', 3, 4)), (('b', 4, 5), ('a', 5))],
          legend='1,4-첨가: β-탄소 공격 → 엔올레이트'),
    '↓ 양성자화·토토머화',
    panel('CC(=O)C(C(C)=O)C1CCCC(=O)C1', h=115, legend='E (C₁₁H₁₆O₃)'),
])

# ---------- A형 11번 ----------
mechanism(P('m_A11_imine'), [
    panel('CC[NH2:1].[O:2]=[C:3]1CCCCC1', [(('lp', 1), ('a', 3)), (('b', 3, 2), ('a', 2))],
          legend='(1) N 비공유 전자쌍이 C=O 탄소 공격'),
    '↓ 양성자 이동',
    panel('CC[NH:1][C:3]1([OH:2])CCCCC1', h=115, legend='(2) 카비놀아민'),
    '↓ H⁺ (OH 양성자화)',
    panel('CC[NH:1][C:3]1([OH2+:2])CCCCC1', [(('lp', 1), ('b', 1, 3)), (('b', 3, 2), ('a', 2))],
          legend='(3) N이 밀어내며 H₂O 이탈 → 이미늄'),
    '↓ −H⁺ (N–H)',
    panel('CC[N:1]=[C:3]1CCCCC1', h=105, legend='A 이민'),
])
mechanism(P('m_A11_enamine'), [
    panel('CC[N+:1](CC)=[C:2]1[CH:3]([H:4])CCCC1.[OH2:5]',
          [(('lp', 5), ('a', 4)), (('b', 3, 4), ('b', 3, 2)), (('b', 2, 1), ('a', 1))],
          legend='이미늄(이민과 같은 과정) → N에 H가 없어 α-H 제거'),
    '↓',
    panel('CCN(CC)C1=CCCCC1', h=110, legend='B 엔아민'),
])
mechanism(P('m_A11_red'), [
    panel('CCC[NH2:1].[O:2]=[C:3](CC)CC', [(('lp', 1), ('a', 3)), (('b', 3, 2), ('a', 2))],
          legend='(1) 아민의 친핵성 첨가'),
    '↓ 양성자 이동, H⁺',
    panel('CCC[NH:1][C:3](CC)(CC)[OH2+:2]', [(('lp', 1), ('b', 1, 3)), (('b', 3, 2), ('a', 2))],
          legend='(2) H₂O 이탈 → 이미늄 이온'),
    '↓',
    panel('CCC[NH+:1]=[C:2](CC)CC.[H-:3]', [(('a', 3), ('a', 2)), (('b', 2, 1), ('a', 1))],
          legend='(3) NaBH₄의 H⁻가 이미늄 탄소 공격'),
    '↓',
    panel('CCCNC(CC)CC', h=105, legend='C N-propylpentan-3-amine'),
])

# ---------- B형 2번 ----------
mechanism(P('m_B02_lah'), [
    panel('c1ccccc1[C:1]#[N:2].[H-:3]', [(('a', 3), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(1) LiAlH₄: 첫 번째 H⁻ 첨가'),
    '↓',
    panel('c1ccccc1[CH:1]=[N-:2].[H-:3]', [(('a', 3), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(2) 이민 음이온에 두 번째 H⁻ 첨가'),
    '↓ H₂O (N 양성자화 2회)',
    panel('NCc1ccccc1', h=100, legend='A benzylamine'),
])
mechanism(P('m_B02_dibal'), [
    panel('c1ccccc1[C:1]#[N:2][Al:4](CC(C)C)CC(C)C.[H-:3]', [(('a', 3), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(1) N이 Al에 배위 → Al–H의 H⁻ 한 번 전달'),
    '↓ −78 °C에서 멈춤',
    panel('c1ccccc1C=N[Al-](CC(C)C)CC(C)C', h=120, legend='(2) 이민–알루미늄 착물 (더 환원 안 됨)'),
    '↓ H₃O⁺: 이민 가수분해',
    panel('O=Cc1ccccc1', h=100, legend='B benzaldehyde'),
])
mechanism(P('m_B02_imine'), [
    panel('c1ccccc1C[NH2:1].[O:2]=[CH:3]c1ccccc1', [(('lp', 1), ('a', 3)), (('b', 3, 2), ('a', 2))],
          legend='(1) A의 N이 B의 C=O 공격'),
    '↓ 양성자 이동, H⁺',
    panel('c1ccccc1C[NH:1][CH:3]([OH2+:2])c1ccccc1', [(('lp', 1), ('b', 1, 3)), (('b', 3, 2), ('a', 2))],
          legend='(2) H₂O 이탈'),
    '↓ −H⁺',
    panel('c1ccccc1C/N=C/c1ccccc1', h=105, legend='C (C₁₄H₁₃N)'),
])
mechanism(P('m_B02_cn'), [
    panel('N#[C-:1].[O:2]=[CH:3]c1ccccc1', [(('lp', 1), ('a', 3)), (('b', 3, 2), ('a', 2))],
          legend='(1) CN⁻가 C=O 탄소 공격'),
    '↓',
    panel('N#C[CH:3]([O-:2])c1ccccc1.[H:4][Cl:5]', [(('lp', 2), ('a', 4)), (('b', 4, 5), ('a', 5))],
          legend='(2) 알콕사이드 양성자화'),
    '↓',
    panel('N#CC(O)c1ccccc1', h=105, legend='D mandelonitrile'),
])

# ---------- B형 7번 ----------
mechanism(P('m_B07_snar'), [
    panel('C[O-:1].[Cl:2][C:3]1=[N:4][CH]=[CH][CH]=[CH]1', [(('lp', 1), ('a', 3)), (('b', 3, 4), ('a', 4))],
          legend='(1) 첨가: CH₃O⁻가 C2 공격, 음전하가 N으로'),
    '↓',
    panel('C[O:1][C:3]1([Cl:2])[N-:4][CH]=CC=C1', [(('lp', 4), ('b', 4, 3)), (('b', 3, 2), ('a', 2))],
          legend='(2) 제거: C=N 회복, Cl⁻ 이탈'),
    '↓',
    panel('COc1ccccn1', h=100, legend='B 2-methoxypyridine'),
])
mechanism(P('m_B07_ozone'), [
    panel('COC1=CCC(C)=CC1', h=105, legend='C (Birch 생성물)'),
    '↓ O₃ 1당량: 전자가 풍부한 엔올 에터 C=C',
    panel('CO[C:1](C)=[CH:2]C.[O-:3][O+:4]=[O:5]',
          [(('lp', 3), ('a', 1)), (('b', 1, 2), ('a', 5)), (('b', 4, 5), ('a', 4))],
          legend='(1) 1,3-쌍극자 첨가 (반응하는 C=C 부분만 표시)'),
    '↓',
    panel('CO[C:1]1(C)[CH:2](C)[O:5][O:4][O:3]1', h=115, legend='(2) 1차 오존화물 (불안정)'),
    '↓ 고리 열림 → 2차 오존화물 → Me₂S 환원',
    panel('COC(=O)C/C=C(\\C)CC=O', h=110, legend='D (C₈H₁₂O₃)'),
])
mechanism(P('m_B07_benzyne'), [
    panel('[NH2-:1].[H:2][C:3]1=[C:4]([Cl:5])[CH]=[CH][CH]=[C]1C', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) Cl 옆 H 제거 (C2–H)'),
    '↓',
    panel('[C-:3]1=[C:4]([Cl:5])C=CC=C1C', [(('lp', 3), ('b', 3, 4)), (('b', 4, 5), ('a', 5))],
          legend='(2) Cl⁻ 이탈 → 3-methylbenzyne'),
    '↓ NH₂⁻',
    panel('[NH2-:1].[C:3]1#[C:4]C=CC=C1C', [(('lp', 1), ('a', 4)), (('b', 3, 4), ('a', 3))],
          legend='(3) NH₂⁻ 첨가 (양쪽 탄소 모두 가능)'),
    '↓',
    panel('N[C:4]1=[C-:3]C(C)=CC=C1.[H:6][NH2:7]', [(('lp', 3), ('a', 6)), (('b', 6, 7), ('a', 7))],
          legend='(4) 양성자화 → m-toluidine (다른 쪽은 o-)'),
])
