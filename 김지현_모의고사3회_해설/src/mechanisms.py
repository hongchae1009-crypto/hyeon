"""김지현 3회 유기 문항의 메커니즘 그림(굽은 화살표).

공용 _tools/mechlib.py를 쓰되, 방향족 고리를 SMILES에 쓴 케쿨레 구조 그대로 그리도록
이 파일 안에서만 분자 읽기 함수를 바꿔 끼운다(화살표가 정확한 이중결합에서 출발하게).
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_tools'))
import mechlib
from mechlib import panel, mechanism
from rdkit import Chem

_orig_mol = mechlib._mol


def _mol_no_arom(smi, arrows=()):
    # SMILES의 케쿨레 이중결합 위치를 유지: 방향족성 인식 없이 정리한다
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


mechlib._mol = _mol_no_arom

IMG = os.path.join(os.path.dirname(__file__), '..', 'img')
P = lambda n: os.path.join(IMG, n + '.svg')

# ---------- A형 10번 ----------
mechanism(P('m_A10_br'), [
    panel('[NH2:1][C:2]1=[CH:3]C=[CH:4]C=C1.[Br:5][Br:6]',
          [(('lp', 1), ('b', 1, 2)), (('b', 3, 2), ('a', 5)), (('b', 5, 6), ('a', 6))],
          legend='(1) N이 전자를 밀어 ortho 탄소가 Br₂ 공격'),
    '↓',
    panel('[NH2+:1]=[C:2]1[C:3]([Br:5])([H:7])C=CC=C1.[OH2:8]',
          [(('lp', 8), ('a', 7)), (('b', 3, 7), ('b', 3, 2)), (('b', 2, 1), ('a', 1))],
          legend='(2) 이미늄형 σ 착물 → H⁺ 제거로 방향족성 회복'),
    '↓ 같은 과정이 다른 ortho·para에서 반복 (촉매 불필요)',
    panel('NC1=C(Br)C=C(Br)C=C1Br', h=110, legend='A 2,4,6-tribromoaniline'),
])
mechanism(P('m_A10_ac'), [
    panel('C1=CC=C([NH2:1])C=C1.CC(=O)O[C:2](C)=[O:3]',
          [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) N이 무수물 C=O 공격 (아세틸화, a·e)'),
    '↓',
    panel('C1=CC=C([NH2+:1][C:2](C)([O-:3])[O:4]C(C)=O)C=C1',
          [(('lp', 3), ('b', 3, 2)), (('b', 2, 4), ('a', 4))],
          legend='(2) C=O 재생, 아세테이트 이탈 → −H⁺'),
    '↓',
    panel('CC(=O)NC1=CC=CC=C1', h=105, legend='acetanilide (N 활성 감소, 부피 증가)'),
])
mechanism(P('m_A10_no2'), [
    panel('CC(=O)[NH:1][C:2]1=CC=[C:3]([H:6])[CH:4]=C1.[O:8]=[N+:5]=O',
          [(('b', 3, 4), ('a', 5)), (('b', 5, 8), ('a', 8))],
          legend='(1) para 탄소가 NO₂⁺ 공격 (f: HNO₃/H₂SO₄)'),
    '↓',
    panel('CC(=O)[NH+:1]=[C:2]1C=C[C:3]([H:6])([N+](=O)[O-])C=C1.[OH2:7]',
          [(('lp', 7), ('a', 6)), (('b', 3, 6), ('b', 3, 2))],
          legend='(2) σ 착물(N 공명 안정화) → H⁺ 제거'),
    '↓ g: H₃O⁺ 가수분해, h: HO⁻',
    panel('NC1=CC=C([N+](=O)[O-])C=C1', h=105, legend='p-nitroaniline'),
])
mechanism(P('m_A10_dz'), [
    panel('C1=CC=C([NH2:1])C=C1.[N:2]#[O+:3]',
          [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) NaNO₂/H⁺ → NO⁺, N이 NO⁺ 공격'),
    '↓ −H⁺, 토토머화(Ar–N=N–OH), OH 양성자화',
    panel('C1=CC=C([N:1]=[N:2][OH2+:3])C=C1',
          [(('lp', 1), ('b', 1, 2)), (('b', 2, 3), ('a', 3))],
          legend='(2) H₂O 이탈 → 다이아조늄 B'),
    '↓ pH 5–7, N,N-dimethylaniline',
    panel('C1=CC=C([N:1]=[N+:2])C=C1.CN(C)[C:4]1=CC=[C:5]([H:7])[CH:6]=C1',
          [(('b', 5, 6), ('a', 2)), (('b', 2, 1), ('a', 1))],
          legend='(3) 아조 짝지음: para 탄소가 말단 N 공격'),
    '↓ σ 착물에서 H⁺ 제거',
    panel('CN(C)C1=CC=C(/N=N/C2=CC=CC=C2)C=C1', h=110, legend='C butter yellow'),
])

# ---------- A형 11번 ----------
# 원자 번호: O 1, Cα 2, Cβ 3, Cγ 4, ipso 5, ortho 6
mechanism(P('m_A11_claisen'), [
    panel('C[C:6]1=[C:5]([O:1][CH2:2][CH:3]=[CH:4]C)C(C)=CC=C1',
          [(('b', 3, 4), ('nb', 4, 6)), (('b', 6, 5), ('b', 5, 1)), (('b', 1, 2), ('b', 2, 3))],
          legend='(1) Claisen [3,3]: 고리형 전자 이동 세 쌍 (가열)'),
    '↓ ortho가 CH₃로 막혀 토토머화 불가',
    panel('C=[CH:3][CH:4](C)[C:6]1(C)[C:5](=O)C(C)=C[CH:8]=[CH:7]1',
          legend='(2) 2,4-cyclohexadienone (1-methylallyl기, 말단 뒤집힘)'),
])
mechanism(P('m_A11_cope'), [
    panel('[CH2:9]=[CH:3][CH:4](C)[C:6]1(C)C(=O)C(C)=[CH:10][CH:8]=[CH:7]1',
          [(('b', 9, 3), ('nb', 9, 8)), (('b', 4, 6), ('b', 4, 3)), (('b', 8, 7), ('b', 7, 6))],
          legend='(3) Cope [3,3]: C4(para)와 말단 CH₂가 결합, C6–C 끊김'),
    '↓',
    panel('C/C=C/C[C:8]1([H:11])[CH:7]=[C:6](C)C(=O)C(C)=[CH:10]1.[OH2:12]',
          legend='(4) 2,5-cyclohexadienone (크로틸기 복원)'),
    '↓ 토토머화(C4–H → O–H), 방향족성 회복',
    panel('C/C=C/CC1=CC(C)=C(O)C(C)=C1', h=110, legend='A 4-(but-2-enyl)-2,6-dimethylphenol'),
])
mechanism(P('m_A11_da'), [
    panel('C=CC[C:6]1(C)C(=O)[C:2](C)=[CH:3][CH:4]=[CH:5]1.O=C1OC(=O)[CH:9]=[CH:7]1',
          [(('b', 2, 3), ('nb', 2, 7)), (('b', 4, 5), ('b', 3, 4)), (('b', 7, 9), ('nb', 9, 5))],
          legend='(5) Diels–Alder [4+2]: 다이엔 + 말레산 무수물 (엔도)'),
    '↓',
    panel('C=CCC1(C)C(=O)C2(C)C=CC1C1C(=O)OC(=O)C12', h=130, legend='B (C₁₅H₁₆O₄)'),
])

# ---------- B형 10번 ----------
mechanism(P('m_B10_lah'), [
    panel('[O:1]=[C:2]1CCCC[O:3]1.[H-:4]', [(('a', 4), ('a', 2)), (('b', 2, 1), ('a', 1))],
          legend='(1) H⁻가 C=O 탄소 공격'),
    '↓',
    panel('[O-:1][CH:2]1CCCC[O:3]1', [(('lp', 1), ('b', 1, 2)), (('b', 2, 3), ('a', 3))],
          legend='(2) C=O 재생, 고리 O 이탈 (고리 열림)'),
    '↓',
    panel('[O:1]=[CH:2]CCCC[O-:3].[H-:4]', [(('a', 4), ('a', 2)), (('b', 2, 1), ('a', 1))],
          legend='(3) 알데하이드에 두 번째 H⁻'),
    '↓ aq. H₂SO₄ (두 O⁻ 양성자화)',
    panel('OCCCCCO', h=100, legend='A 1,5-pentanediol'),
])
mechanism(P('m_B10_hyd'), [
    panel('[O:1]=[C:2]1CCCC[O:3]1.[OH3+:4]', [(('lp', 1), ('a', 4))],
          legend='(1) C=O 산소 양성자화 (친전자성 증가)'),
    '↓',
    panel('[OH+:1]=[C:2]1CCCC[O:3]1.[OH2:5]', [(('lp', 5), ('a', 2)), (('b', 2, 1), ('a', 1))],
          legend='(2) 물이 카보닐 탄소 공격'),
    '↓ 양성자 이동 (고리 O에 H⁺)',
    panel('[OH:1][C:2]1([OH:5])CCCC[OH+:3]1', [(('lp', 5), ('b', 5, 2)), (('b', 2, 3), ('a', 3))],
          legend='(3) C=O 재생하며 고리 O 이탈 (고리 열림)'),
    '↓ −H⁺',
    panel('OCCCCC(=O)O', h=100, legend='C 5-hydroxypentanoic acid'),
])
mechanism(P('m_B10_grig'), [
    panel('[O:1]=[C:2]1CCCC[O:3]1.Br[Mg:5][C:4]1=CC=CC=C1', [(('b', 4, 5), ('a', 2)), (('b', 2, 1), ('a', 1))],
          legend='(1) C–Mg 결합 전자가 C=O 탄소 공격'),
    '↓',
    panel('[O-:1][C:2]1(C2=CC=CC=C2)CCCC[O:3]1', [(('lp', 1), ('b', 1, 2)), (('b', 2, 3), ('a', 3))],
          legend='(2) 고리 열림 → 케톤 + 알콕사이드'),
    '↓ 케톤이 에스터보다 반응적',
    panel('[O:1]=[C:2](CCCC[O-])C1=CC=CC=C1.Br[Mg:5][C:4]1=CC=CC=C1', [(('b', 4, 5), ('a', 2)), (('b', 2, 1), ('a', 1))],
          legend='(3) 두 번째 PhMgBr 첨가'),
    '↓ NH₄Cl, H₂O',
    panel('OCCCCC(O)(C1=CC=CC=C1)C1=CC=CC=C1', h=115, legend='D (C₁₇H₂₀O₂)'),
])

# ---------- A형 10번 추가: 술폰화(차단기)와 탈술폰화 ----------
mechanism(P('m_A10_so3'), [
    panel('CC(=O)NC1=CC=[C:3]([H:6])[CH:4]=C1.[O:8]=[S:5](=O)=O',
          [(('b', 3, 4), ('a', 5)), (('b', 5, 8), ('a', 8))],
          legend='(1) para 탄소의 π 전자가 SO₃의 S 공격'),
    '↓',
    panel('CC(=O)N[C+]1C=C[C:3]([H:6])(S(=O)(=O)[O-])C=C1.[OH2:7]',
          [(('lp', 7), ('a', 6))],
          legend='(2) σ 착물(+는 N 쪽 탄소까지 비편재화) → H⁺ 제거'),
    '↓',
    panel('CC(=O)NC1=CC=C(S(=O)(=O)O)C=C1', h=110, legend='(3) para가 SO₃H로 막힘 → 니트로화는 ortho로'),
    '↓ HNO₃: 남은 ortho 니트로화',
    panel('CC(=O)NC1=C([N+](=O)[O-])C=C(S(=O)(=O)O)C=C1', h=120, legend='(4) 2-nitro-4-sulfo-acetanilide'),
    '↓ (d) 묽은 H₂SO₄·가열 → 탈술폰화 + 아마이드 가수분해; HO⁻',
    panel('NC1=CC=CC=C1[N+](=O)[O-]', h=110, legend='(5) o-nitroaniline'),
])

# ---------- B형 1번: KMnO₄ 산화 절단 (cyclohexene) ----------
mechanism(P('m_B01_kmno4'), [
    panel('[CH:1]1=[CH:2]CCCC1.[O-:3][Mn:4](=[O:5])(=O)=O',
          [(('lp', 3), ('a', 1)), (('b', 1, 2), ('a', 5)), (('b', 5, 4), ('a', 4))],
          legend='(1) [3+2] 고리화 첨가: syn, 고리형 망가네이트 에스터'),
    '↓',
    panel('O=[Mn-]1(=O)OC2CCCCC2O1', h=125, legend='(2) 고리형 망가네이트 에스터'),
    '↓ HO⁻, 물: 가수분해 → cis-1,2-다이올',
    panel('OC1CCCCC1O', h=105, legend='(3) cis-cyclohexane-1,2-diol'),
    '↓ 뜨거운 KMnO₄: C–C 절단, 각 탄소 → C=O → COOH',
    panel('OC(=O)CCCCC(=O)O', h=105, legend='(4) adipic acid (H₃O⁺ 후처리)'),
])
