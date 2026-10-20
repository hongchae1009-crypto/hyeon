"""안병천 4회 유기 문항의 메커니즘 그림(굽은 화살표)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '_tools'))
from mechlib import panel, mechanism


import math
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
    """s-cis 다이엔 + 알카인 친다이엔체, 고리형 화살표 3개 (손그림)."""
    W, H = 330, 175
    C1, C2, C3, C4 = (120, 40), (85, 62), (85, 108), (120, 130)
    C5, C6 = (205, 112), (205, 58)
    ln = lambda a, b, w=2: f"<line x1='{a[0]}' y1='{a[1]}' x2='{b[0]}' y2='{b[1]}' stroke='{INK}' stroke-width='{w}'/>"
    dbl = lambda a, b, o: ln(a, b) + ln((a[0] + o[0], a[1] + o[1]), (b[0] + o[0], b[1] + o[1]), 1.6)
    b = dbl(C1, C2, (5, 5)) + ln(C2, C3) + dbl(C3, C4, (5, -5))
    b += ln(C5, C6) + ln((C5[0] + 5, C5[1]), (C6[0] + 5, C6[1]), 1.6) + ln((C5[0] - 5, C5[1]), (C6[0] - 5, C6[1]), 1.6)
    b += ln(C2, (55, 45)) + ln(C3, (55, 125))
    b += _txt(43, 42, 'CH₃', 12) + _txt(43, 138, 'CH₃', 12)
    b += ln(C6, (230, 40)) + _txt(250, 36, 'COPh', 12) + ln(C5, (230, 130)) + _txt(248, 142, 'CH₃', 12)
    b += "<line x1='130' y1='40' x2='195' y2='58' stroke='#9ca3af' stroke-width='1' stroke-dasharray='4 3'/>"
    b += "<line x1='130' y1='130' x2='195' y2='112' stroke='#9ca3af' stroke-width='1' stroke-dasharray='4 3'/>"
    b += _curve(100, 48, 82, 84, -14)      # C1=C2 π → C2–C3
    b += _curve(103, 122, 165, 122, 14)     # C3=C4 π → C4–C5 새 σ
    b += _curve(208, 86, 165, 48, 16)       # C5≡C6 π → C6–C1 새 σ
    b += _txt(W / 2, H - 6, legend, 12.5, color='#374151')
    return (f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}px' height='{H}px' viewBox='0 0 {W} {H}'>{b}</svg>", H)

IMG = os.path.join(os.path.dirname(__file__), '..', 'img')
P = lambda n: os.path.join(IMG, n + '.svg')

# ---------- A형 2번 ----------
mechanism(P('m_A02_cp'), [
    panel('[NH2-:1].[H:2][CH:3]1C=CC=C1', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) 염기가 sp³ CH₂의 H⁺ 제거'),
    '↓',
    panel('[CH-:1]1[CH:2]=[CH:3]C=C1', [(('lp', 1), ('b', 1, 2)), (('b', 2, 3), ('a', 3))],
          legend='(2) 음전하가 고리 다섯 탄소에 비편재화 (6π)'),
    '↓ 공명 5개 → 매우 안정',
    panel('[cH-]1cccc1', h=105, legend='(가) C₅H₅⁻ 방향족 → A의 pKa ≈ 16'),
])
mechanism(P('m_A02_trop'), [
    panel('[H:2][CH:3]1C=CC=CC=C1.[CH2+:1]c1ccccc1', [(('b', 2, 3), ('a', 1))],
          legend='(1) Ph₃C⁺ 등이 H⁻(수소화 이온)를 떼어 감'),
    '↓',
    panel('[CH+:1]1[CH:2]=[CH:3]C=CC=C1', [(('b', 2, 3), ('b', 1, 2))],
          legend='(2) 빈 p 오비탈로 π 전자 비편재화 (6π)'),
    '↓',
    panel('[cH+]1cccccc1', h=105, legend='(라) C₇H₇⁺ tropylium 방향족'),
])

# ---------- A형 3번 ----------
mechanism(P('m_A03_fischer'), [
    panel('CC[C:1](=[O:2])[OH:3].[H+:4]', [(('lp', 2), ('a', 4))],
          legend='(1) C=O 산소 양성자화 → 탄소의 친전자성↑'),
    '↓ CH₃OH',
    panel('C[OH:5].CC[C:1](=[OH+:2])O', [(('lp', 5), ('a', 1)), (('b', 1, 2), ('a', 2))],
          legend='(2) CH₃OH가 카보닐 탄소 공격'),
    '↓ 양성자 이동',
    panel('CC[C:1]([OH:2])([O:6]C)[OH2+:3]', [(('lp', 2), ('b', 2, 1)), (('b', 1, 3), ('a', 3))],
          legend='(3) H₂O 이탈 (사면체 중간체 붕괴)'),
    '↓ −H⁺',
    panel('CCC(=O)OC', h=100, legend='methyl propanoate'),
])
mechanism(P('m_A03_claisen'), [
    panel('C[O-:1].[H:2][CH:3](C)[C:4](=[O:5])OC', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) CH₃O⁻가 α-H 제거 → 엔올레이트'),
    '↓',
    panel('C[CH-:3]C(=O)OC.CC[C:6](=[O:7])OC', [(('lp', 3), ('a', 6)), (('b', 6, 7), ('a', 7))],
          legend='(2) 엔올레이트가 다른 에스터 C=O 공격'),
    '↓',
    panel('COC(=O)C(C)[C:6]([O-:7])([O:8]C)CC', [(('lp', 7), ('b', 7, 6)), (('b', 6, 8), ('a', 8))],
          legend='(3) 사면체 붕괴, CH₃O⁻ 이탈'),
    '↓',
    panel('COC(=O)[C:3]([H:2])(C)C(=O)CC.C[O-:1]', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(4) 두 C=O 사이 H 제거 → 평형이 생성물 쪽'),
    '↓ H₃O⁺',
    panel('CCC(=O)C(C)C(=O)OC', h=100, legend='A methyl 2-methyl-3-oxopentanoate'),
])

# ---------- A형 8번 ----------
mechanism(P('m_A08_A'), [
    panel('[NH2-:1].[H:2][C:3]#CC', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) NaNH₂: 말단 알카인 H 제거'),
    '↓ PhCHO',
    panel('CC#[C-:3].[O:5]=[CH:4]c1ccccc1', [(('lp', 3), ('a', 4)), (('b', 4, 5), ('a', 5))],
          legend='(2) 아세틸라이드가 C=O 탄소 공격'),
    '↓ H₃O⁺',
    panel('CC#CC(O)c1ccccc1', h=105, legend='(3) 2차 알코올'),
    '↓ CrO₃, H₂SO₄ (Jones 산화)',
    panel('CC#CC(=O)c1ccccc1', h=105, legend='A 1-phenylbut-2-yn-1-one'),
])
mechanism(P('m_A08_DA'), [
    da_panel('(1) [4+2]: 화살표 3개가 고리 모양으로 동시에 (s-cis 다이엔)'),
    '↓',
    panel('CC1=C(C(=O)c2ccccc2)CC(C)=C(C)C1', h=110, legend='(2) 1,4-cyclohexadiene 부가물'),
    '↓ mCPBA (전자가 풍부한 사치환 C=C)',
    panel('[C:1](C)(C)=[C:2](C)C.[O:3]([H:4])[O:5]C(=O)c1cccc(Cl)c1',
          [(('b', 1, 2), ('a', 3)), (('b', 3, 5), ('a', 5))],
          legend='(3) 협동(syn) 산소 전달 — 반응하는 C=C만 표시'),
    '↓',
    panel('CC1=C(C(=O)c2ccccc2)CC2(C)OC2(C)C1', h=115, legend='B cis-에폭사이드 (라셈)'),
])

# ---------- B형 8번 ----------
mechanism(P('m_B08_lah'), [
    panel('[H-:1].[O:3]=[C:2]1[O:4]C(=O)C2CC=CCC12', [(('a', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) H⁻가 무수물 C=O 탄소 공격'),
    '↓',
    panel('[O-:3][CH:2]1[O:4]C(=O)C2CC=CCC12', [(('lp', 3), ('b', 3, 2)), (('b', 2, 4), ('a', 4))],
          legend='(2) 고리 열림: 카복실레이트 이탈 → 알데하이드'),
    '↓ H⁻가 알데하이드·카복실레이트를 차례로 환원',
    panel('OCC1CC=CCC1CO', h=110, legend='(3) H₃O⁺ 후 cis-다이올'),
])
mechanism(P('m_B08_ether'), [
    panel('[H-:1].[H:2][O:3]CC1CC=CCC1CO', [(('a', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='(1) NaH: O–H 제거 (H₂ 발생), 양쪽 OH 모두'),
    '↓',
    panel('[O-:3]CC1CC=CCC1CO.[CH3:4][I:5]', [(('lp', 3), ('a', 4)), (('b', 4, 5), ('a', 5))],
          legend='(2) 알콕사이드 SN2 (MeI) — 두 번'),
    '↓',
    panel('COCC1CC=CCC1COC', h=110, legend='B (C₁₀H₁₈O₂)'),
])
mechanism(P('m_B08_ozone'), [
    panel('[CH:1](C)=[CH:2]C.[O-:3][O+:4]=[O:5]', [(('lp', 3), ('a', 1)), (('b', 1, 2), ('a', 5)), (('b', 4, 5), ('a', 4))],
          legend='(1) O₃ 1,3-쌍극자 첨가 (반응하는 C=C만 표시)'),
    '↓ 1차 오존화물 → 2차 오존화물',
    panel('COCC(CC=O)C(CC=O)COC', h=110, legend='(2) 고리 열림 → 다이알데하이드'),
    '↓ H₂O₂ (산화)',
    panel('COCC(CC(=O)O)C(CC(=O)O)COC', h=110, legend='C meso 다이카복실산'),
])

# ---------- B형 9번 ----------
mechanism(P('m_B09_ac'), [
    panel('Cc1ccccc1[NH2:1].CC(=O)O[C:2](C)=[O:3]', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='ㄷ (1) NH₂가 무수물 C=O 공격'),
    '↓ 사면체 붕괴, AcO⁻ 이탈, −H⁺',
    panel('Cc1ccccc1NC(C)=O', h=105, legend='(2) 아세트아닐라이드 (NHAc)'),
])
mechanism(P('m_B09_br'), [
    panel('CC(=O)[NH:1][C:2]1=[CH:3][CH:9]=[CH:4][CH:10]=[C:11]1C.[Br:5][Br:6]',
          [(('lp', 1), ('b', 1, 2)), (('b', 2, 3), ('b', 3, 9)), (('b', 9, 4), ('a', 5)), (('b', 5, 6), ('a', 6))],
          legend='ㄹ (1) N 전자쌍이 밀려 들어가 para 탄소가 Br₂ 공격'),
    '↓',
    panel('CC(=O)[NH+]=C1C=CC([H:7])([Br])C=C1C.[Br-:8]', [(('lp', 8), ('a', 7))],
          legend='(2) σ 착물 (양전하가 N까지 비편재화) → H⁺ 제거'),
    '↓ NaOH: 아마이드 가수분해',
    panel('Cc1cc(Br)ccc1N', h=105, legend='(3) 4-bromo-2-methylaniline'),
])
mechanism(P('m_B09_diazo'), [
    panel('Brc1ccc(c(C)c1)[NH2:1].[N:2]=[O+:3]', [(('lp', 1), ('a', 2)), (('b', 2, 3), ('a', 3))],
          legend='ㄱ (1) NaNO₂/H⁺ → NO⁺, ArNH₂가 공격'),
    '↓ 양성자 이동 · 토토머화',
    panel('Brc1ccc(c(C)c1)N=N[OH2+]', h=110, legend='(2) Ar–N=N–OH₂⁺ → H₂O 이탈'),
    '↓',
    panel('Brc1ccc(c(C)c1)[N+]#N', h=105, legend='(3) 다이아조늄 이온'),
    '↓ ㅁ H₃PO₂ (라디칼 연쇄: Ar· + H₃PO₂ → ArH)',
    panel('Cc1cccc(Br)c1', h=100, legend='B 3-bromotoluene (N₂ 방출)'),
])
