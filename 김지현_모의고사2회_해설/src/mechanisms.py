"""김지현 2회 유기 문항의 메커니즘 그림(굽은 화살표)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_tools'))
from mechlib import panel, mechanism

IMG = os.path.join(os.path.dirname(__file__), '..', 'img')
P = lambda n: os.path.join(IMG, n + '.svg')

# ---------- A형 10번 ----------
mechanism(P('m_A10_e2'), [
    panel('[NH2-:1].[H:2][CH:3](C)[C:4]([H])([Br:5])CBr', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('nb', 3, 4)), (('b', 4, 5), ('a', 5))],
          legend='(1) E2: H 제거와 Br⁻ 이탈이 동시에 (anti)'),
    '↓ 두 번째 NaNH₂: 같은 방식의 E2',
    panel('CC#C', h=95, legend='propyne'),
    '↓ 세 번째 NaNH₂',
    panel('[NH2-:1].C[C]#[C:2][H:3]', [(('lp', 1), ('a', 3)), (('b', 2, 3), ('a', 2))],
          legend='(2) 말단 ≡C–H 제거 → 아세틸라이드 (후처리로 재양성자화)'),
    '↓ H₂ 1당량, Ni₂B(P-2) — cis 첨가 후 멈춤',
    panel('C=CC', h=95, legend='A propene'),
])
mechanism(P('m_A10_radical'), [
    panel('[Cl:1][Cl:2]', h=90, legend='개시: 400 °C에서 Cl–Cl 균일 분해 → 2 Cl·'),
    '↓',
    panel('[Cl:1].[H:2][CH2:3]C=C', [(('a', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) Cl·이 알릴 H를 뗌 (라디칼 단계: 화살표 = 전자 1개 이동)'),
    '↓ 공명 안정화된 알릴 라디칼',
    panel('[CH2:3]=C[CH2:4].[Cl:5][Cl:6]', [(('a', 4), ('nb', 4, 5)), (('b', 5, 6), ('a', 6))],
          legend='(2) 알릴 라디칼이 Cl₂에서 Cl을 뗌 → Cl· 재생'),
    '↓',
    panel('ClCC=C', h=95, legend='allyl chloride'),
])
mechanism(P('m_A10_halohydrin'), [
    panel('ClC[CH:1]=[CH2:2].[Cl:3][Cl:4]', [(('b', 1, 2), ('a', 3)), (('b', 3, 4), ('a', 4))],
          legend='(1) C=C가 Cl₂ 공격 → 클로로늄 이온'),
    '↓',
    panel('[OH2:5].ClC[CH:1]1[CH2:2][Cl+:3]1', [(('lp', 5), ('a', 1)), (('b', 1, 3), ('a', 3))],
          legend='(2) H₂O가 더 치환된 탄소(뒷면) 공격'),
    '↓ −H⁺',
    panel('ClCC(O)CCl', h=100, legend='B 1,3-dichloro-2-propanol'),
])
mechanism(P('m_A10_epox'), [
    panel('[OH-:1].ClCC([O:2][H:3])CCl', [(('lp', 1), ('a', 3)), (('b', 2, 3), ('a', 2))],
          legend='(1) HO⁻ 1당량: OH 양성자 제거'),
    '↓',
    panel('ClC[CH:4]([O-:2])[CH2:5][Cl:6]', [(('lp', 2), ('a', 5)), (('b', 5, 6), ('a', 6))],
          legend='(2) 분자 내 SN2: O⁻가 이웃 C–Cl 공격'),
    '↓',
    panel('ClCC1CO1', h=100, legend='C epichlorohydrin'),
    '↓ HO⁻ 과량',
    panel('[OH-:1].ClC[CH:2]1[CH2:3][O:4]1', [(('lp', 1), ('a', 3)), (('b', 3, 4), ('a', 4))],
          legend='(3) 에폭사이드 개환(덜 치환된 탄소) + 남은 C–Cl도 SN2'),
    '↓ 양성자화',
    panel('OCC(O)CO', h=100, legend='D glycerol'),
])

# ---------- A형 11번 ----------
mechanism(P('m_A11_cannizzaro'), [
    panel('[OH-:1].[O:2]=[CH:3]c1ccccc1', [(('lp', 1), ('a', 3)), (('b', 3, 2), ('a', 2))],
          legend='(1) HO⁻가 C=O 탄소 공격'),
    '↓',
    panel('c1ccccc1[C:3]([H:4])([OH:1])[O-:2].[O:5]=[CH:6]c1ccccc1',
          [(('lp', 2), ('b', 2, 3)), (('b', 3, 4), ('a', 6)), (('b', 6, 5), ('a', 5))],
          legend='(2) C=O 재생하며 H⁻를 다른 PhCHO로 전달'),
    '↓',
    panel('OC(=O)c1ccccc1.[O-]Cc1ccccc1', h=105, legend='(3) 벤조산 + 벤질 알콕사이드'),
    '↓ 양성자 이동 (산–염기)',
    panel('[O-]C(=O)c1ccccc1.OCc1ccccc1', h=105, legend='A 벤조산 이온(H₃O⁺ 처리 → 벤조산), B 벤질 알코올'),
])
mechanism(P('m_A11_henry'), [
    panel('[OH-:1].[H:2][CH:3](C)[N+](=O)[O-]', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) α-H 제거 → 니트로네이트'),
    '↓',
    panel('C[CH-:3][N+](=O)[O-].[O:4]=[CH:5]c1ccccc1', [(('lp', 3), ('a', 5)), (('b', 5, 4), ('a', 4))],
          legend='(2) C=O 탄소에 친핵성 첨가'),
    '↓ 양성자화 → β-니트로 알코올',
    panel('[OH:6][CH:7](c1ccccc1)[C:8]([H:9])(C)[N+](=O)[O-]', h=115, legend='(3) β-니트로 알코올'),
    '↓ 염기, 가열: E1cB 탈수',
    panel('[OH-:1].[OH:6][CH:7](c1ccccc1)[C:8]([H:9])(C)[N+](=O)[O-]',
          [(('lp', 1), ('a', 9)), (('b', 8, 9), ('nb', 8, 7)), (('b', 7, 6), ('a', 6))],
          legend='(4) α-H 제거, HO⁻ 이탈'),
    '↓',
    panel('C/C(=C\\c1ccccc1)[N+](=O)[O-]', h=105, legend='C (E)-2-nitro-1-phenylpropene'),
])
mechanism(P('m_A11_wittig'), [
    panel('C=C[CH-:1][P+:2](C)(C)C.[O:3]=[CH:4]c1ccccc1',
          [(('lp', 1), ('a', 4)), (('b', 4, 3), ('nb', 3, 2))],
          legend='(1) 일라이드 C → C=O 탄소, O → P (PPh₃는 PMe₃로 표시)'),
    '↓',
    panel('C=C[CH:1]1[CH:4](c2ccccc2)[O:3][P:2]1(C)(C)C',
          [(('b', 1, 2), ('nb', 1, 4)), (('b', 4, 3), ('nb', 3, 2))],
          legend='(2) 옥사포스페테인 분해'),
    '↓ − Ph₃P=O',
    panel('C=C/C=C/c1ccccc1', h=100, legend='D 1-phenyl-1,3-butadiene'),
])

# ---------- B형 1번 ----------
mechanism(P('m_B01_os'), [
    panel('OC(=O)/[CH:1]=[CH:2]/C(=O)O.[O:3]=[Os:5](=O)(=O)=[O:4]',
          [(('b', 1, 2), ('a', 3)), (('b', 5, 3), ('a', 3)), (('b', 5, 4), ('nb', 4, 2))],
          legend='(1) OsO₄ [3+2] 협동 첨가 → 두 O가 같은 면(syn)'),
    '↓',
    panel('OC(=O)[CH:1]1[CH:2](C(=O)O)[O:4][Os](=O)(=O)[O:3]1', h=120, legend='(2) 고리형 오스메이트 에스터'),
    '↓ NaHSO₃/H₂O: Os–O 절단, C–O 유지',
    panel('OC(=O)[C@@H](O)[C@H](O)C(=O)O', h=105, legend='A: trans + syn → (R,R)/(S,S) 라셈'),
])
mechanism(P('m_B01_br'), [
    panel('OC(=O)/[CH:1]=[CH:2]/C(=O)O.[Br:3][Br:4]', [(('b', 1, 2), ('a', 3)), (('b', 3, 4), ('a', 4))],
          legend='(1) C=C가 Br₂ 공격 → 브로모늄 이온'),
    '↓',
    panel('[Br-:4].OC(=O)[CH:1]1[CH:2](C(=O)O)[Br+:3]1', [(('lp', 4), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(2) Br⁻가 브로모늄 뒷면 공격 (anti)'),
    '↓',
    panel('OC(=O)[C@@H](Br)[C@@H](Br)C(=O)O', h=105, legend='C: trans + anti → meso (E에서는 F 라셈)'),
])

# ---------- B형 10번 ----------
mechanism(P('m_B10_lactone'), [
    panel('O=C(O)CCC(=[O:1])c1ccc(Cl)c(Cl)c1', h=115, legend='A'),
    '↓ NaBH₄: H⁻가 케톤만 환원 → 알코올',
    panel('[OH:2][C:3](=[O:4])CC[CH:5]([OH:6])c1ccc(Cl)c(Cl)c1', [(('lp', 6), ('a', 3)), (('b', 3, 4), ('a', 4))],
          legend='(1) HCl: C=O 양성자화 후 γ-OH가 공격 (분자 내 에스터화)'),
    '↓ −H₂O',
    panel('O=C1CCC(c2ccc(Cl)c(Cl)c2)O1', h=115, legend='B γ-락톤 (C₁₀H₈O₂Cl₂)'),
])
mechanism(P('m_B10_fc'), [
    panel('O=C1CC[CH:1](c2ccc(Cl)c(Cl)c2)[O:2]1.[Al:3](Cl)(Cl)Cl', [(('lp', 2), ('a', 3)), (('b', 1, 2), ('a', 2))],
          legend='(1) AlCl₃가 고리 O에 배위 → C–O 끊어짐'),
    '↓',
    panel('[O-]C(=O)CC[CH+:1]c1ccc(Cl)c(Cl)c1.[cH:4]1cccc[cH:5]1', [(('b', 4, 5), ('a', 1))], h=140,
          legend='(2) 벤질 탄소양이온(공명 안정) ← 벤젠 π 전자 공격'),
    '↓ 아레늄 이온에서 H⁺ 제거(방향족성 회복), H₃O⁺',
    panel('O=C(O)CCC(c1ccccc1)c1ccc(Cl)c(Cl)c1', h=125, legend='C (C₁₆H₁₄O₂Cl₂)'),
])
mechanism(P('m_B10_acyl'), [
    panel('Clc1ccc(cc1Cl)C(CC[C:1](=O)[Cl:2])c1ccccc1', h=125, legend='SOCl₂: 산 → 산 염화물'),
    '↓ AlCl₃',
    panel('CC(CC[C+:1]=O)c1ccc[cH:4][cH:3]1', [(('b', 4, 3), ('a', 1))],
          legend='(1) 페닐 ortho C가 아실륨 공격 (Ar은 CH₃로 표시)'),
    '↓ 아레늄 이온에서 H⁺ 제거',
    panel('O=C1CCC(c2ccc(Cl)c(Cl)c2)c2ccccc21', h=125, legend='D 테트랄론 (C₁₆H₁₂OCl₂)'),
])

# B형 10번 보강: NaBH₄ 환원, 아실륨 생성과 아레늄 이온 탈양성자화
mechanism(P('m_B10_nabh4'), [
    panel('[H-:3].[O:2]=[C:1](C)c1ccc(Cl)c(Cl)c1', [(('a', 3), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(1) H⁻가 케톤 C 공격 (사슬은 CH₃로 표시)'),
    '↓',
    panel('[OH:5][H:4].[O-:2][CH:1](C)c1ccc(Cl)c(Cl)c1', [(('lp', 2), ('a', 4)), (('b', 4, 5), ('a', 5))],
          legend='(2) 알콕사이드 양성자화 (COOH는 NaBH₄와 반응 안 함)'),
    '↓',
    panel('O=C(O)CCC(O)c1ccc(Cl)c(Cl)c1', h=115, legend='γ-하이드록시산 (HCl에서 고리화 → B)'),
])
mechanism(P('m_B10_acylium'), [
    panel('C[C:1](=O)[Cl:2].[Al:3](Cl)(Cl)Cl', [(('lp', 2), ('a', 3))],
          legend='(1) 산 염화물의 Cl이 AlCl₃에 배위 (R은 CH₃로 표시)'),
    '↓',
    panel('C[C:1](=O)[Cl+:2][Al-:3](Cl)(Cl)Cl', [(('b', 1, 2), ('a', 2))],
          legend='(2) C–Cl 결합이 끊어지며 AlCl₄⁻ 이탈'),
    '↓',
    panel('C[C+]=O.CC#[O+]', h=115, legend='(3) 아실륨 이온 R–C⁺=O ↔ R–C≡O⁺ (공명 안정)'),
    '↓ 페닐 고리가 아실륨 공격 → 아레늄 이온',
    panel('[Cl-:3].[H:2][C:1]1([CH3])C=CC=C[CH+:4]1', [(('lp', 3), ('a', 2)), (('b', 1, 2), ('b', 1, 4))],
          legend='(4) AlCl₄⁻가 H⁺ 제거 (아실기는 CH₃로 표시)'),
])
