"""김지현 5회 유기 문항의 메커니즘 그림(굽은 화살표). 라디칼 단계는 반쪽 화살표(fishhook)."""
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

# ---------- A형 10번: Baeyer–Villiger ----------
mechanism(P('m_A10_bv'), [
    panel('COCC1[CH:3]2C=CC1C[C:1]2=[O:2].CC(=O)O[O:4][H:5]',
          [(('lp', 4), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(1) 과산의 O가 C=O 탄소 공격 (RCO₃H = mCPBA)'),
    '↓ 양성자 이동',
    panel('COCC1[CH:3]2C=CC1C[C:1]2([OH:2])[O:4][O:5]C(C)=O',
          [(('lp', 2), ('b', 2, 1)), (('b', 1, 3), ('nb', 3, 4)), (('b', 4, 5), ('a', 5))],
          h=150, legend='(2) Criegee 중간체: 머리 CH(2°)가 O로 이동, RCOO⁻ 이탈'),
    '↓ −H⁺',
    panel('COCC1C2C=CC1OC(=O)C2.CC(=O)O', h=125, legend='B 락톤 (C₉H₁₂O₃) + RCOOH'),
])
mechanism(P('m_A10_hyd'), [
    panel('COCC1C2C=CC1[O:3][C:1](=[O:2])C2.[OH-:4]',
          [(('lp', 4), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(1) HO⁻가 락톤 C=O 탄소 공격'),
    '↓',
    panel('COCC1C2C=CC1[O:3][C:1]([O-:2])([OH:4])C2',
          [(('lp', 2), ('b', 2, 1)), (('b', 1, 3), ('a', 3))],
          legend='(2) 사면체 중간체: C=O 회복, 고리 O 이탈(고리 열림)'),
    '↓',
    panel('COCC1C([O-:3])C=CC1CC(=O)[O:4][H:5]',
          [(('lp', 3), ('a', 5)), (('b', 4, 5), ('a', 4))],
          legend='(3) 양성자 이동 → 카복실산 이온 + 알코올'),
    '↓ H₃O⁺',
    panel('COCC1C(O)C=CC1CC(=O)[O-:4].[H:5][OH2+:6]',
          [(('lp', 4), ('a', 5)), (('b', 5, 6), ('a', 6))],
          legend='(4) 카복실산 이온 양성자화'),
    '↓',
    panel('COCC1C(O)C=CC1CC(=O)O', h=120, legend='C (C₉H₁₄O₄)'),
])

# ---------- A형 11번 ----------
mechanism(P('m_A11_hofelim'), [
    panel('C1CCNCC1', h=105, legend='piperidine'),
    '↓ CH₃I 과량(SN2 2회), Ag₂O/H₂O',
    panel('[OH-:1].C[N+:2]1(C)[CH2:3][CH:4]([H:5])CCC1',
          [(('lp', 1), ('a', 5)), (('b', 4, 5), ('b', 4, 3)), (('b', 3, 2), ('a', 2))],
          legend='(1) 가열: E2 — β-H 제거, N 이탈(고리 열림)'),
    '↓',
    panel('CN(C)CCCC=C', h=110, legend='A N,N-dimethylpent-4-en-1-amine'),
    '↓ CH₃I 과량, Ag₂O/H₂O',
    panel('[OH-:1].C[N+:2](C)(C)[CH2:3][CH:4]([H:5])CC=C',
          [(('lp', 1), ('a', 5)), (('b', 4, 5), ('b', 4, 3)), (('b', 3, 2), ('a', 2))],
          legend='(2) 가열: 두 번째 Hofmann 제거'),
    '↓',
    panel('C=CCC=C.CN(C)C', h=110, legend='B penta-1,4-diene + (CH₃)₃N'),
])
mechanism(P('m_A11_curtius'), [
    panel('[N-:5]=[N+:4]=[N-:3].CC(C)(C)C[C:1](=[O:2])[Cl:6]',
          [(('lp', 3), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(1) N₃⁻가 산 염화물 C=O 공격'),
    '↓',
    panel('CC(C)(C)C[C:1]([O-:2])([Cl:6])[N:3]=[N+]=[N-]',
          [(('lp', 2), ('b', 2, 1)), (('b', 1, 6), ('a', 6))],
          legend='(2) C=O 회복, Cl⁻ 이탈 → 아실 아자이드'),
    '↓ 가열',
    panel('CC(C)(C)[CH2:7][C:1](=O)[N:3]=[N+:4]=[N-:5]',
          [(('b', 7, 1), ('nb', 7, 3)), (('b', 3, 4), ('a', 4))],
          legend='(3) Curtius: R가 N으로 이동하며 N₂ 이탈 (협동)'),
    '↓ −N₂',
    panel('CC(C)(C)C[N:3]=[C:1]=[O:2].[OH2:8]',
          [(('lp', 8), ('a', 1)), (('b', 1, 3), ('a', 3))],
          legend='(4) 아이소사이아네이트에 물 첨가'),
    '↓ 양성자 이동',
    panel('CC(C)(C)C[NH2+:3][C:1](=O)[O-:2]',
          [(('lp', 2), ('b', 2, 1)), (('b', 1, 3), ('a', 3))],
          legend='(5) 카밤산 → CO₂ 탈리'),
    '↓',
    panel('CC(C)(C)CN.O=C=O', h=110, legend='C neopentylamine + CO₂'),
])
mechanism(P('m_A11_hofrearr'), [
    panel('[OH-:1].O=C([N:2]([H:3])[H:9])C1Cc2ccccc2C1',
          [(('lp', 1), ('a', 3)), (('b', 2, 3), ('a', 2))],
          legend='(1) HO⁻가 N–H 양성자 제거'),
    '↓',
    panel('O=C([NH-:2])C1Cc2ccccc2C1.[Br:4][Br:5]',
          [(('lp', 2), ('a', 4)), (('b', 4, 5), ('a', 5))],
          legend='(2) 아마이드 음이온이 Br₂ 공격 → N-브로모아마이드'),
    '↓ HO⁻: 두 번째 N–H 제거',
    panel('[O:6]=[C:1]([N-:2][Br:4])[CH:7]1Cc2ccccc2C1',
          [(('b', 7, 1), ('nb', 7, 2)), (('b', 2, 4), ('a', 4))],
          legend='(3) 자리옮김: R가 N으로 이동, Br⁻ 이탈'),
    '↓',
    panel('[O:6]=[C:1]=[N:2]C1Cc2ccccc2C1.[OH-:8]',
          [(('lp', 8), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(4) 아이소사이아네이트에 HO⁻ 첨가'),
    '↓ 양성자 이동 → 카밤산 이온',
    panel('[O-:6][C:1](=O)[NH:2]C1Cc2ccccc2C1.[H:9][OH:10]',
          [(('lp', 2), ('a', 9)), (('b', 9, 10), ('a', 10))],
          legend='(5) N 양성자화'),
    '↓',
    panel('[O-:6][C:1](=O)[NH2+:2]C1Cc2ccccc2C1',
          [(('lp', 6), ('b', 6, 1)), (('b', 1, 2), ('a', 2))],
          legend='(6) CO₂ 탈리'),
    '↓',
    panel('NC1Cc2ccccc2C1.O=C=O', h=110, legend='D indan-2-amine + CO₂'),
])

# ---------- B형 1번: Haworth 합성 ----------
mechanism(P('m_B01_fc1'), [
    panel('O=C1CC[C:1](=[O:2])O1.Cl[Al:3](Cl)Cl',
          [(('lp', 2), ('a', 3))],
          legend='(1) C=O 산소가 AlCl₃에 배위'),
    '↓',
    panel('O=C1CC[C:1](=[O+:2][Al-](Cl)(Cl)Cl)[O:4]1',
          [(('b', 1, 4), ('a', 4))],
          legend='(2) C–O 결합이 끊어져 아실륨 이온 생성'),
    '↓',
    panel('C[C:9]1=[CH:8][CH:7]=[CH:5][CH:6]=[CH:10]1.[O-]C(=O)CC[C+:11]=[O:12]',
          [(('b', 5, 7), ('a', 11)), (('b', 11, 12), ('a', 12))],
          legend='(3) 톨루엔의 para 탄소가 아실륨 공격'),
    '↓',
    panel('CC1=C[CH+:7][C:5]([H:13])(C(=O)CCC(=O)[O-])C=C1.[Cl-:14]',
          [(('lp', 14), ('a', 13)), (('b', 5, 13), ('b', 5, 7))],
          legend='(4) σ-착물에서 H⁺ 제거 → 방향족성 회복'),
    '↓ H₃O⁺',
    panel('Cc1ccc(cc1)C(=O)CCC(=O)O', h=110, legend='A (C₁₁H₁₂O₃)'),
])
mechanism(P('m_B01_wk'), [
    panel('Cc1ccc(cc1)C(=O)CCC(=O)O', h=105, legend='A'),
    '↓ NH₂NH₂ (이민 형성과 같은 축합, −H₂O)',
    panel('Cc1ccc(cc1)[C:1](CCC(=O)[O-])=[N:2][NH:3][H:4].[OH-:5]',
          [(('lp', 5), ('a', 4)), (('b', 3, 4), ('b', 3, 2)), (('b', 2, 1), ('a', 1))],
          h=150, legend='(1) 하이드라존 N–H 제거 → 탄소 음이온'),
    '↓',
    panel('Cc1ccc(cc1)[C-:1](CCC(=O)[O-])[N:2]=[NH:3].[H:6][OH:7]',
          [(('lp', 1), ('a', 6)), (('b', 6, 7), ('a', 7))],
          h=150, legend='(2) 탄소 양성자화'),
    '↓',
    panel('Cc1ccc(cc1)[CH:1](CCC(=O)[O-])[N:2]=[N:3][H:4].[OH-:5]',
          [(('lp', 5), ('a', 4)), (('b', 3, 4), ('b', 2, 3)), (('b', 1, 2), ('a', 1))],
          h=150, legend='(3) N–H 제거, N₂ 이탈 → 탄소 음이온'),
    '↓ H₂O',
    panel('Cc1ccc(cc1)CCCC(=O)O', h=105, legend='B (C₁₁H₁₄O₂), 산 처리 후'),
])
mechanism(P('m_B01_fc2'), [
    panel('Cc1ccc(cc1)CCC[C:1](=O)[Cl:2].Cl[Al:3](Cl)Cl',
          [(('lp', 2), ('a', 3)), (('b', 1, 2), ('a', 2))],
          legend='(1) SOCl₂로 만든 산 염화물 + AlCl₃ → 아실륨'),
    '↓',
    panel('C[C:9]1=[CH:8][CH:7]=[C:5]([CH:6]=[CH:10]1)CCC[C+:11]=[O:12]',
          [(('b', 6, 10), ('a', 11)), (('b', 11, 12), ('a', 12))],
          h=150, legend='(2) 분자 내 공격: 사슬의 ortho 탄소 → 6원 고리'),
    '↓',
    panel('C[C:9]1=[CH:8][CH:7]=[C:5]2CCCC(=O)[C:6]2([H:13])[CH+:10]1.[Cl-:14]',
          [(('lp', 14), ('a', 13)), (('b', 6, 13), ('b', 6, 10))],
          h=150, legend='(3) σ-착물에서 H⁺ 제거'),
    '↓',
    panel('Cc1ccc2CCCC(=O)c2c1', h=110, legend='D 7-methyl-1-tetralone'),
])

# ---------- B형 10번: 라디칼 브로민화 (반쪽 화살표) ----------
FISH = True
mechanism(P('m_B10_rad'), [
    panel('[Br:1][Br:2]', [(('b', 1, 2), ('a', 1)), (('b', 1, 2), ('a', 2))], h=95,
          legend='개시: hν로 Br–Br 균일 분해'),
    '↓ 2 Br·',
    panel('[Br:1].C[CH:2]([H:3])C', [(('a', 1), ('nb', 1, 3)), (('b', 2, 3), ('nb', 1, 3)), (('b', 2, 3), ('a', 2))],
          h=115, legend='전파 ①: Br·가 2° H 추출 (흡열 +29 kJ/mol)'),
    '↓ HBr',
    panel('C[CH:1]C.[Br:2][Br:3]', [(('a', 1), ('nb', 1, 2)), (('b', 2, 3), ('nb', 1, 2)), (('b', 2, 3), ('a', 3))],
          h=115, legend='전파 ②: 2° 라디칼이 Br₂와 반응'),
    '↓ Br· 재생 (연쇄)',
    panel('CC(Br)C', h=95, legend='2-bromopropane (92 %)'),
])
FISH = False

# ---------- A형 3번: NaOD/D₂O에서 α-H 교환(엔올화) ----------
mechanism(P('m_A03_hd'), [
    panel('CC1(C)[CH:2]([H:3])[C:1](=[O:4])c2ccccc21.[O-:5][2H]',
          [(('lp', 5), ('a', 3)), (('b', 2, 3), ('b', 2, 1)), (('b', 1, 4), ('a', 4))],
          legend='(1) OD⁻가 C=O 옆(α) H를 떼어 냄'),
    '↓',
    panel('CC1(C)[CH:2]=[C:1]([O-:4])c2ccccc21.[2H:6][O:7][2H]',
          [(('lp', 4), ('b', 4, 1)), (('b', 1, 2), ('a', 6)), (('b', 6, 7), ('a', 7))],
          legend='(2) 엔올레이트의 α-탄소가 D₂O의 D를 받음'),
    '↓ 반복',
    panel('CC1(C)C([2H])([2H])C(=O)c2ccccc21', h=120, legend='α-CD₂: 2.6 ppm 신호 사라짐'),
])
