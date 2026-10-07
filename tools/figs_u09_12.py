"""9 알코올 · 10 에터와 에폭사이드 · 11 벤젠과 방향족성 · 12 방향족 화합물의 반응 — 문항 그림"""
import math
from chemsvg import Mol, Fig, benzene, L, RED, BLUE, INK

GREEN = "#2f7d5b"
GRAY = "#5b6270"


# ------------------------------------------------------------------ 공통 헬퍼
def ring_bonds(m, p, kinds, c=(0, 0)):
    """ring(bonds=False)로 만든 6각 고리에 변별 결합 종류 지정. kinds: 6개 (1 | 'in')"""
    n = len(kinds)
    for i, k in enumerate(kinds):
        m.bond(f"{p}{i}", f"{p}{(i + 1) % n}", k, c if k == "in" else None)


def cyhex(m, p, subs=(), cx=0, cy=0, start=90):
    """사이클로헥세인 + 치환기 [(idx, label, kind, ang)] (ang=None → 바깥 방향)"""
    m.ring(p, cx, cy, 6, L, start)
    for j, (i, lab, kind, ang) in enumerate(subs):
        a = start - 60 * i if ang is None else ang
        m.sub(f"{p}s{j}", f"{p}{i}", a, lab, kind=kind)
    return m


def ok(f, x, y, good=True, t=None):
    f.text(x, y, t or ("✓" if good else "✗"), size=16, color=GREEN if good else RED, weight="bold")


# ================================================================== 9 알코올
# ------------------------------------------------------------------ 2013 #38 (보호기)
def f09_38():
    f = Fig(800, 330)
    # X
    m = cyhex(Mol(), "x", [(1, "OH", 1, None), (3, "Br", 1, None)])
    f.mol(m, 70, 95)
    f.cap(40, 160, "X")
    f.arrow(120, 95, 215, 95, "A: Et₃SiCl, Et₃N", "OH 보호")
    m = cyhex(Mol(), "a", [(1, "OSiEt_3", 1, None), (3, "Br", 1, None)])
    f.mol(m, 260, 95)
    f.text(275, 180, "TES 에터 (O–H 없음)", size=11.5)
    f.arrow(345, 95, 420, 95, "B: Mg, Et₂O", "")
    m = cyhex(Mol(), "b", [(1, "OSiEt_3", 1, None), (3, "MgBr", 1, None)])
    f.mol(m, 465, 95)
    f.text(480, 180, "그리냐르 시약", size=11.5)
    f.arrow(550, 95, 640, 95, "C: 1) CH₂O", "2) H₂O")
    m = cyhex(Mol(), "c", [(1, "OSiEt_3", 1, None)])
    c = m.sub("k1", "c3", -90)
    m.sub("k2", c, -30, "OH")
    f.mol(m, 690, 85)
    f.text(710, 190, "1차 알코올 (보호 유지)", size=11.5)
    # 2행
    f.arrow(700, 225, 610, 265, "", "")
    f.text(690, 262, "D: H₃O⁺ (탈보호)", size=11, anchor="start")
    m = cyhex(Mol(), "y", [(1, "OH", 1, None)])
    c = m.sub("k1", "y3", -90)
    m.sub("k2", c, -30, "OH")
    f.mol(m, 500, 245, scale=0.8)
    f.cap(450, 300, "Y")
    f.box(20, 215, 360, 100, fill="#fff5f5", stroke="#f0b4ac")
    f.text(30, 235, "보호 없이 Mg를 먼저 넣으면?", size=12, anchor="start", weight="bold", color=RED)
    f.text(30, 257, "R–MgBr + R–OH (pKₐ ≈ 16) → R–H + R–OMgBr", size=11.5, anchor="start")
    f.text(30, 278, "그리냐르 시약이 자기 분자의 O–H에 의해 즉시", size=11.5, anchor="start")
    f.text(30, 298, "양성자화되어 소멸 → CH₂O와 반응할 수 없음", size=11.5, anchor="start")
    return f.render()


# ------------------------------------------------------------------ 2012 #39
def f09_39_pinacol():
    f = Fig(800, 230)
    f.text(20, 18, "ㄱ. 피나콜 자리옮김 — 더 안정한 탄소 양이온(Ph₂C⁺) 생성 → 고리 C–C 결합 이동(고리 확장)", size=12.5, anchor="start", weight="bold")
    # 반응물
    m = Mol()
    m.ring("q", 0, 0, 5, 25.5, 90)
    m.sub("o", "q1", 60, "OH")
    c = m.sub("c", "q1", -20)
    m.sub("co", c, 40, "OH")
    m.sub("p1", c, -40, "Ph")
    m.sub("p2", c, -100, "Ph")
    f.mol(m, 70, 120)
    f.arrow(160, 115, 230, 115, "H⁺", "−H₂O")
    # 양이온
    m = Mol()
    m.ring("q", 0, 0, 5, 25.5, 90)
    m.sub("o", "q1", 60, "OH")
    c = m.sub("c", "q1", -20)
    m.sub("p1", c, 10, "Ph")
    m.sub("p2", c, -70, "Ph")
    f.mol(m, 285, 120)
    cx, cy = m.pos("c")
    f.charge(285 + cx + 3, 120 + cy - 15)
    # 결합 이동 화살표 (q1–q2 결합 → C+)
    x1, y1 = m.pos("q1")
    x2, y2 = m.pos("q2")
    f.curly(285 + (x1 + x2) / 2 - 4, 120 + (y1 + y2) / 2 + 4, 285 + cx - 4, 120 + cy + 6, bend=0.6)
    f.text(285, 190, "3차 벤질 양이온 (공명 안정화)", size=11.5)
    f.arrow(385, 115, 455, 115, "1,2-알킬 이동", "(고리 확장)")
    # 옥소카베늄 → 케톤
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.sub("o", "r0", 90, "OH^+", kind="2")
    m.sub("p1", "r1", 60, "Ph")
    m.sub("p2", "r1", 0, "Ph")
    f.mol(m, 505, 125)
    f.arrow(590, 115, 640, 115, "−H⁺", "")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.sub("o", "r0", 90, "O", kind="2")
    m.sub("p1", "r1", 50, "Ph")
    m.sub("p2", "r1", -10, "Ph")
    f.mol(m, 695, 125)
    f.text(710, 200, "2,2-diphenylcyclohexanone", size=11.5)
    ok(f, 775, 30, True, "ㄱ ✓")
    return f.render()


def f09_39_bv():
    f = Fig(800, 300)
    f.text(20, 18, "ㄴ. Baeyer–Villiger 산화 — 이동 경향: 3차 > 2차(사이클로헥실) ≈ 페닐 > 1차 > CH₃", size=12.5, anchor="start", weight="bold")
    m = cyhex(Mol(), "a")
    c = m.sub("c", "a1", 30)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("me", c, -30)
    f.mol(m, 60, 100)
    f.arrow(150, 95, 250, 95, "PhCO₃H", "CHCl₃")
    m = cyhex(Mol(), "b")
    o = m.sub("o1", "b1", 30, "O")
    c = m.sub("c", o, -30)
    m.sub("o", c, -90, "O", kind="2")
    m.sub("me", c, 30)
    f.mol(m, 300, 100)
    f.text(335, 160, "cyclohexyl acetate (실제 주생성물)", size=11.5, color=GREEN)
    m = cyhex(Mol(), "d")
    c = m.sub("c", "d1", 30)
    m.sub("o", c, 90, "O", kind="2")
    o = m.sub("o2", c, -30, "O")
    m.sub("me", o, 30)
    f.mol(m, 560, 100)
    f.text(600, 160, "보기: methyl ester (CH₃ 이동)", size=11.5, color=RED)
    ok(f, 770, 60, False, "ㄴ ✗")
    # ㄷ Curtius
    f.text(20, 195, "ㄷ. 아실 아자이드 → Curtius 자리옮김 → 아이소사이아네이트 → 가수분해·탈카복실화", size=12.5, anchor="start", weight="bold")
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    m.sub("me", "r0", 90)
    c = m.sub("c1", "r1", 30)
    c2 = m.sub("c2", c, -30)
    m.sub("o", c2, -90, "O", kind="2")
    m.sub("cl", c2, 30, "Cl")
    f.mol(m, 55, 250)
    f.arrow(160, 250, 215, 250, "", "NaN₃")
    f.text(262, 245, "ArCH₂C(=O)N₃", size=12)
    f.arrow(318, 245, 378, 245, "Δ, −N₂", "[1,2]-이동")
    f.text(432, 245, "ArCH₂N=C=O", size=12)
    f.arrow(485, 245, 555, 245, "H₂O", "−CO₂")
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    m.sub("me", "r0", 90)
    c = m.sub("c1", "r1", 30)
    m.sub("n", c, -30, "NH_2")
    f.mol(m, 610, 250)
    ok(f, 770, 250, True, "ㄷ ✓")
    return f.render()


# ------------------------------------------------------------------ 2001 #7 (K2Cr2O7)
def f09_2001_7():
    f = Fig(800, 265)
    f.text(20, 18, "에탄올의 K₂Cr₂O₇/H⁺ 산화 (Cr⁶⁺ 주황 → Cr³⁺ 초록)", size=12.5, anchor="start", weight="bold")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30)
    m.sub("o", b, -30, "OH")
    f.mol(m, 50, 80)
    f.text(80, 115, "ethanol", size=11.5)
    f.arrow(150, 75, 240, 75, "[O]", "−2H")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30)
    m.sub("o", b, -30, "O", kind="2")
    m.sub("h", b, 90, "H")
    f.mol(m, 270, 80)
    f.text(295, 115, "acetaldehyde (중간 산화물)", size=11.5)
    f.arrow(370, 75, 460, 75, "[O], H₂O", "(수화물 경유)")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30)
    m.sub("o", b, 90, "O", kind="2")
    m.sub("oh", b, -30, "OH")
    f.mol(m, 490, 80)
    f.text(520, 115, "acetic acid (최종 산화물)", size=11.5)
    # 공명
    f.text(20, 150, "아세트산 이온(CH₃COO⁻)의 공명 구조", size=12.5, anchor="start", weight="bold")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30)
    m.sub("o", b, 90, "O", kind="2")
    m.sub("om", b, -30, "O^−")
    f.mol(m, 90, 222)
    f.resarrow(170, 230, 222)
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30)
    m.sub("o", b, 90, "O^−")
    m.sub("om", b, -30, "O", kind="2")
    f.mol(m, 260, 222)
    f.box(380, 165, 400, 80, fill="#f7f9fc")
    f.text(395, 187, "두 공명 구조의 기여가 같음 (동등한 공명 구조)", size=11.5, anchor="start")
    f.text(395, 209, "→ 음전하가 두 O에 −½씩 비편재화, C–O 결합 차수 1.5", size=11.5, anchor="start")
    f.text(395, 231, "→ 두 C–O 길이 같음(≈127 pm), 짝염기 안정 → pKₐ 4.76", size=11.5, anchor="start")
    return f.render()


# ------------------------------------------------------------------ 2001 #15 (EtOH + HBr)
def f09_2001_15():
    f = Fig(800, 260)
    f.text(20, 18, "① NaBr + EtOH: 평형이 왼쪽 (OH⁻는 나쁜 이탈기) — 역반응(가수분해)은 자발적", size=12.5, anchor="start", weight="bold")
    f.text(40, 50, "C₂H₅OH + Br⁻", size=13, anchor="start")
    f.eqarrow(150, 240, 48, "✗ (거의 진행 안 함)", "가수분해 (쉬움)")
    f.text(255, 50, "C₂H₅Br + OH⁻", size=13, anchor="start")
    f.text(420, 50, "OH⁻ (H₂O pKₐ 15.7) ≫ Br⁻ (HBr pKₐ −9) 염기성", size=11.5, anchor="start", color=GRAY)
    f.text(20, 110, "② HBr(또는 NaBr + 진한 H₂SO₄) 사용: –OH를 양성자화 → 좋은 이탈기 H₂O → Br⁻의 S_N2 공격", size=12.5, anchor="start", weight="bold")
    # 단계 1: 양성자화
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30)
    m.sub("o", b, -30, "OH")
    f.mol(m, 40, 180)
    f.text(135, 180, "+ H–Br", size=12.5)
    f.arrow(175, 175, 225, 175, "빠른 평형", "")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30)
    m.sub("o", b, -30, "OH_2^+")
    f.mol(m, 250, 180)
    f.text(345, 180, "+ Br⁻", size=12.5)
    # 단계 2: SN2
    f.arrow(375, 175, 425, 175, "S_N2", "")
    f.text(505, 175, "[Br···C···OH₂]^‡", size=12)
    f.arrow(575, 175, 625, 175, "", "")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30)
    m.sub("o", b, -30, "Br")
    f.mol(m, 650, 180)
    f.text(750, 180, "+ H₂O", size=12.5)
    f.text(400, 235, "1차 알킬 → 탄소 양이온 불안정 → S_N2 (뒷면 공격, 1단계 협동)", size=12, color=RED)
    return f.render()


# ================================================================== 10 에터와 에폭사이드
# ------------------------------------------------------------------ 2012 #36
def f10_36():
    f = Fig(800, 250)
    # 클로로하이드린 (지그재그): C4H3–C3(Cl,H)–C2(OH,Me2)
    m = Mol()
    c4 = m.atom("c4", 0, 0)
    c3 = m.sub("c3", c4, -30)
    m.sub("cl", c3, -120, "Cl", kind="w")
    m.sub("h", c3, -60, "H", kind="h")
    c2 = m.sub("c2", c3, 30)
    m.sub("oh", c2, -30, "O^−")
    m.sub("m1", c2, 60, kind="w")
    m.sub("m2", c2, 120, kind="h")
    f.mol(m, 50, 110)
    f.text(95, 180, "(S)-알콕사이드", size=11.5)
    ox, oy = m.pos("oh")
    cx, cy = m.pos("c3")
    f.curly(50 + ox + 2, 110 + oy + 10, 50 + cx + 8, 110 + cy + 14, bend=-0.6)
    f.text(95, 200, "O⁻가 C–Cl 뒷면 공격", size=11, color=RED)
    f.arrow(190, 105, 275, 105, "(가) 분자 내 S_N2", "C3 반전")
    # 에폭사이드
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.atom("b", 34, 0)
    o = m.atom("o", 17, 26, "O")
    m.bond(a, b)
    m.bond(a, o)
    m.bond(b, o)
    m.sub("m1", b, 60, kind="w")
    m.sub("m2", b, 0, kind="h")
    m.sub("me", a, 200, kind="h")
    m.sub("h", a, 120, "H", kind="w")
    f.mol(m, 330, 95)
    f.text(345, 160, "(R)-2,2,3-trimethyloxirane", size=11.5)
    f.curly(300, 118, 326, 100, bend=0.5)
    f.text(292, 128, "OH⁻", size=11.5, color=RED)
    f.arrow(400, 105, 490, 105, "(나) OH⁻ (S_N2)", "덜 막힌 C3 공격, 반전")
    m = Mol()
    c4 = m.atom("c4", 0, 0)
    c3 = m.sub("c3", c4, -30)
    m.sub("oh1", c3, -120, "HO", kind="w")
    m.sub("h", c3, -60, "H", kind="h")
    c2 = m.sub("c2", c3, 30)
    m.sub("oh", c2, -30, "OH")
    m.sub("m1", c2, 60, kind="w")
    m.sub("m2", c2, 120, kind="h")
    f.mol(m, 540, 110)
    f.text(590, 180, "(S)-2-methylbutane-2,3-diol", size=11.5)
    f.box(20, 212, 760, 30, fill="#f7f9fc")
    f.text(400, 227, "반전 × 2 = 알짜 입체 보존: 처음 C–Cl 자리에 C–OH가 놓임 (Cl과 OH의 우선순위가 같은 1순위 → S 유지)", size=11.5)
    return f.render()


# ------------------------------------------------------------------ 2011 #37
def f10_37():
    f = Fig(800, 300)
    # ㄱ
    f.text(20, 20, "ㄱ", size=13, weight="bold")
    m = cyhex(Mol(), "a")
    o = m.sub("o", "a1", 30, "O")
    t = m.sub("t", o, -30)
    for i, ang in enumerate((30, -30, -90)):
        m.sub(f"t{i}", t, ang)
    f.mol(m, 60, 60)
    f.arrow(190, 55, 250, 55, "HCl", "S_N1")
    m = cyhex(Mol(), "b", [(1, "OH", 1, None)])
    f.mol(m, 290, 60)
    f.text(390, 55, "+ (CH₃)₃C–Cl", size=12, anchor="start")
    f.text(520, 55, "O–C(3차) 쪽이 끊김: 안정한 (CH₃)₃C⁺", size=11.5, anchor="start")
    ok(f, 775, 55)
    # ㄴ
    f.text(20, 125, "ㄴ", size=13, weight="bold")
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    o = m.sub("o", "r1", 30, "O")
    c = m.sub("c", o, -30)
    m.sub("c1", c, 30)
    m.sub("c2", c, -90)
    f.mol(m, 60, 160)
    f.arrow(190, 155, 250, 155, "HI", "가열")
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    m.sub("o", "r1", 30, "OH")
    f.mol(m, 290, 160)
    f.text(390, 155, "+ (CH₃)₂CH–I", size=12, anchor="start")
    f.text(520, 147, "sp² C–O는 끊기지 않음(S_N1·S_N2 불가)", size=11.5, anchor="start")
    f.text(520, 165, "→ 항상 페놀 + 할로젠화 알킬", size=11.5, anchor="start")
    ok(f, 775, 155)
    # ㄷ
    f.text(20, 240, "ㄷ", size=13, weight="bold")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.atom("b", 30, 0)
    o = m.atom("o", 15, -24, "O")
    m.bond(a, b)
    m.bond(a, o)
    m.bond(b, o)
    m.sub("me", a, -140)
    f.mol(m, 70, 255)
    f.curly(150, 225, 108, 250, bend=0.4)
    f.text(160, 218, "Ph⁻", size=11.5, color=RED, anchor="start")
    f.arrow(190, 250, 250, 250, "1) PhMgBr", "2) H₃O⁺")
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    c = m.sub("c", "r1", 30)
    d = m.sub("d", c, -30)
    m.sub("oh", d, -90, "OH")
    m.sub("me", d, 30)
    f.mol(m, 290, 255)
    f.text(520, 242, "염기성 조건 개환 = S_N2:", size=11.5, anchor="start")
    f.text(520, 260, "덜 막힌 CH₂ 탄소 공격", size=11.5, anchor="start")
    ok(f, 775, 250)
    return f.render()


# ------------------------------------------------------------------ 2010 논술 1
def f10_2010_sn1():
    f = Fig(800, 345)
    f.text(20, 18, "[반응 I] S_N1 가용매 분해 (3-bromo-3-methylhexane → 라세미 3-methylhexan-3-ol)", size=12.5, anchor="start", weight="bold")
    # 기질: 중심 C
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("br", c, 90, "Br", kind="h")
    m.sub("me", c, -30, "CH_3", kind="w")
    e1 = m.sub("e1", c, 150)
    m.sub("e2", e1, -150)
    p1 = m.sub("p1", c, -90)
    p2 = m.sub("p2", p1, -150)
    m.sub("p3", p2, 150)
    f.mol(m, 90, 105)
    f.curly(96, 92, 112, 66, bend=-0.6)
    f.arrow(150, 100, 225, 100, "① 느린 단계", "이온화 (RDS)")
    # 탄소 양이온 (평면)
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("me", c, 0, "CH_3")
    e1 = m.sub("e1", c, 120)
    m.sub("e2", e1, 180)
    p1 = m.sub("p1", c, -120)
    m.sub("p2", p1, -60)
    f.mol(m, 285, 105)
    f.charge(296, 92)
    f.text(300, 180, "평면 3차 탄소 양이온 + Br⁻", size=11.5)
    f.curly(245, 60, 280, 88, bend=0.4)
    f.curly(245, 150, 280, 122, bend=-0.4)
    f.text(242, 55, "H₂O (위)", size=11, color=RED, anchor="end")
    f.text(242, 140, "H₂O (아래)", size=11, color=RED, anchor="end")
    f.arrow(365, 100, 440, 100, "② 빠름", "−H⁺ (③)")
    f.text(560, 90, "양쪽 면 공격 확률 동일", size=11.5)
    f.text(560, 112, "→ (R) : (S) ≈ 1 : 1 (라세미)", size=11.5, weight="bold")
    # 에너지 도표
    x0, y0 = 70, 205
    f.raw(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 + 125}" stroke="{INK}" stroke-width="1.3" marker-end="url(#{f.id}k)" transform="rotate(180 {x0} {y0 + 62})"/>')
    f.raw(f'<line x1="{x0}" y1="{y0 + 125}" x2="{x0 + 470}" y2="{y0 + 125}" stroke="{INK}" stroke-width="1.3"/>')
    f.text(x0 - 10, y0 + 60, "G", size=12, anchor="end", italic=True)
    f.text(x0 + 235, y0 + 138 - 5, "반응 좌표", size=11)
    path = (f"M{x0 + 10},{y0 + 95} C{x0 + 70},{y0 + 95} {x0 + 90},{y0 + 5} {x0 + 130},{y0 + 5} "
            f"C{x0 + 170},{y0 + 5} {x0 + 180},{y0 + 45} {x0 + 215},{y0 + 45} "
            f"C{x0 + 245},{y0 + 45} {x0 + 255},{y0 + 30} {x0 + 280},{y0 + 30} "
            f"C{x0 + 310},{y0 + 30} {x0 + 350},{y0 + 110} {x0 + 450},{y0 + 110}")
    f.raw(f'<path d="{path}" fill="none" stroke="{BLUE}" stroke-width="2"/>')
    f.text(x0 + 130, y0 - 4, "TS₁ (C⁺ 성격 큼)", size=11, color=RED)
    f.text(x0 + 215, y0 + 60, "R₃C⁺", size=11)
    f.text(x0 + 30, y0 + 110, "R₃C–Br", size=11)
    f.text(x0 + 430, y0 + 98, "R₃C–OH", size=11)
    f.box(560, 195, 225, 140, fill="#fff8e6", stroke="#f0c36d")
    f.text(570, 213, "Hammond 가설", size=12, anchor="start", weight="bold")
    f.text(570, 235, "흡열 단계의 TS₁은 에너지가", size=11, anchor="start")
    f.text(570, 253, "가까운 R₃C⁺와 구조가 닮음", size=11, anchor="start")
    f.text(570, 273, "→ C⁺를 안정화하는 요인이", size=11, anchor="start")
    f.text(570, 291, "   TS₁을 낮춰 속도 증가", size=11, anchor="start")
    f.text(570, 313, "3차 기질 · 좋은 이탈기 · 극성", size=11, anchor="start", weight="bold")
    f.text(570, 329, "양성자성 용매(H₂O/EtOH)", size=11, anchor="start", weight="bold")
    return f.render()


def newman(f, cx, cy, front, back, r=30, hl=()):
    """뉴먼 투영. front/back: {각도: 라벨}. hl: 강조할 (front|back, 각도) 목록"""
    f.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="1.4"/>')
    for isf, dd in ((False, back), (True, front)):
        for ang, lab in dd.items():
            a = math.radians(ang)
            x0 = cx if isf else cx + r * math.cos(a)
            y0 = cy if isf else cy - r * math.sin(a)
            x1, y1 = cx + (r + 18) * math.cos(a), cy - (r + 18) * math.sin(a)
            col = GREEN if ("f" if isf else "b", ang) in hl else INK
            f.raw(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{col}" stroke-width="{2.2 if col != INK else 1.4}"/>')
            f.text(cx + (r + 30) * math.cos(a), cy - (r + 30) * math.sin(a), lab, size=11.5, color=col)


def f10_2010_e2():
    f = Fig(800, 350)
    f.text(20, 18, "[반응 II] E2는 C–Cl과 β C–H가 anti-periplanar(고리에서는 trans-diaxial)일 때만 진행", size=12.5, anchor="start", weight="bold")
    # 반응물 (평면 구조)
    m = Mol()
    m.ring("r", 0, 0, 6, L, 0)
    m.sub("me", "r3", 180, "H_3C", kind="w")
    m.sub("ip", "r0", 0, "i-Pr", kind="h")
    m.sub("cl", "r1", -60, "Cl", kind="w")
    f.mol(m, 95, 95)
    f.text(20, 162, "menthyl chloride형 (C1–Cl, C2–i-Pr)", size=11, anchor="start")
    f.text(20, 186, "안정 의자형: Cl·i-Pr·CH₃ 모두 equatorial", size=11.5, anchor="start")
    f.text(20, 204, "→ Cl이 eq이면 anti인 β-H 없음 (E2 불가)", size=11.5, anchor="start", color=RED)
    f.text(20, 222, "→ 고리 뒤집기: 세 치환기 모두 axial인", size=11.5, anchor="start")
    f.text(20, 240, "   불리한 형태에서만 E2 진행 (느림)", size=11.5, anchor="start")
    # 뉴먼 1: C1→C6
    f.text(320, 45, "diaxial 형태, C1→C6 방향", size=11.5, weight="bold")
    newman(f, 320, 130, {90: "Cl", 210: "C2", 330: "H"}, {270: "H", 150: "C5", 30: "H"},
           hl=(("f", 90), ("b", 270)))
    f.text(320, 210, "Cl ↔ C6–H(axial): 180° ✓", size=11.5, color=GREEN)
    f.text(320, 228, "→ C1=C6 이중 결합 = A", size=11.5, color=GREEN, weight="bold")
    # 뉴먼 2: C1→C2
    f.text(520, 45, "diaxial 형태, C1→C2 방향", size=11.5, weight="bold")
    newman(f, 520, 130, {90: "Cl", 330: "C6", 210: "H"}, {270: "i-Pr", 30: "C3", 150: "H"},
           hl=(("f", 90),))
    f.text(520, 210, "Cl의 anti 자리 = i-Pr (H는 gauche) ✗", size=11.5, color=RED)
    f.text(520, 228, "→ C1=C2 (B) 생성 불가", size=11.5, color=RED, weight="bold")
    f.box(640, 60, 150, 110, fill="#f7f9fc")
    f.text(650, 80, "결과", size=12, anchor="start", weight="bold")
    f.text(650, 100, "NaOEt/EtOH (E2)", size=11, anchor="start")
    f.text(650, 117, "→ A 100 %", size=11, anchor="start", color=GREEN)
    f.text(650, 140, "80% EtOH, 가열 (E1)", size=11, anchor="start")
    f.text(650, 157, "→ B 주생성물", size=11, anchor="start", color=BLUE)
    f.text(400, 268, "E2: 입체전자적 요구(anti-periplanar)가 Zaitsev 규칙보다 우선 → 덜 치환된 A (p-menth-2-ene)", size=11.5)
    f.text(400, 293, "E1: 평면 탄소 양이온에서 H⁺ 이탈 → 기하 제약 없음 → 더 안정한 3치환 알켄 B (p-menth-3-ene, Zaitsev)", size=11.5)
    f.text(400, 316, "(2차 C⁺ → 이웃 C2–H의 1,2-수소화 이동으로 3차 C⁺가 생기면 B가 더 우세)", size=11, color=GRAY)
    return f.render()


def f10_2010_epox():
    f = Fig(800, 250)
    f.text(20, 18, "[반응 III] (2R,3R)-3-bromobutan-2-ol → 알콕사이드의 분자 내 S_N2 (O⁻와 Br이 anti) → cis-2,3-dimethyloxirane (meso)", size=12, anchor="start", weight="bold")
    # 원래 그림 (O, Br 같은 쪽)
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.atom("b", 34, 0)
    m.bond(a, b)
    m.sub("oh", a, 100, "HO")
    m.sub("h1", a, 200, "H", kind="h")
    m.sub("m1", a, -120, "H_3C", kind="w")
    m.sub("br", b, 80, "Br")
    m.sub("m2", b, -20, "CH_3", kind="h")
    m.sub("h2", b, -100, "H", kind="w")
    f.mol(m, 70, 110)
    f.text(90, 175, "(2R,3R) (threo)", size=11.5)
    f.arrow(160, 105, 225, 105, "NaOH", "C–C 회전")
    # anti 형태의 뉴먼 투영
    cx, cy, r = 320, 110, 34
    f.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="1.4"/>')

    def arm(ang, lab, front, col=INK):
        a = math.radians(ang)
        x0 = cx if front else cx + r * math.cos(a)
        y0 = cy if front else cy - r * math.sin(a)
        x1, y1 = cx + (r + 22) * math.cos(a), cy - (r + 22) * math.sin(a)
        f.raw(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{INK}" stroke-width="1.4"/>')
        f.text(cx + (r + 34) * math.cos(a), cy - (r + 34) * math.sin(a), lab, size=12, color=col)
    # 앞 C2: O⁻ 위, CH3, H ; 뒤 C3: Br 아래 (anti)
    arm(90, "O^−", True, RED)
    arm(330, "CH_3", True)
    arm(210, "H", True)
    arm(270, "Br", False, RED)
    arm(30, "CH_3", False)
    arm(150, "H", False)
    f.text(cx, cy + 82, "O⁻ / Br anti-periplanar", size=11.5)
    f.text(cx, cy + 98, "두 CH₃는 gauche(같은 쪽)", size=11.5)
    f.arrow(410, 105, 480, 105, "분자 내 S_N2", "C3 반전, −Br⁻")
    # cis 에폭사이드
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.atom("b", 36, 0)
    o = m.atom("o", 18, -28, "O")
    m.bond(a, b)
    m.bond(a, o)
    m.bond(b, o)
    m.sub("m1", a, -120, "H_3C", kind="w")
    m.sub("m2", b, -60, "CH_3", kind="w")
    m.sub("h1", a, 200, "H", kind="h")
    m.sub("h2", b, -20, "H", kind="h")
    f.mol(m, 540, 120)
    f.text(560, 185, "C: cis-2,3-dimethyloxirane", size=11.5, weight="bold")
    f.text(560, 203, "(2R,3S) = meso", size=11.5)
    f.text(560, 221, "분자 내 대칭면 → 광학 비활성", size=11.5, color=RED)
    return f.render()


# ------------------------------------------------------------------ 2007 #11
def epox_ring(m, p, o_kind="w", me_kind="h", h_kind="h"):
    m.ring(p, 0, 0, 6, L, 90)
    # p1 (위 오른쪽) = C1(CH3), p2 (아래 오른쪽) = C2(H)
    x1, y1 = m.pos(p + "1")
    x2, y2 = m.pos(p + "2")
    m.atom(p + "O", x1 + 22, (y1 + y2) / 2, "O")
    m.bond(p + "1", p + "O", o_kind)
    m.bond(p + "2", p + "O", o_kind)
    m.sub(p + "me", p + "1", 50, "CH_3", kind=me_kind)
    m.sub(p + "h", p + "2", -50, "H", kind=h_kind)
    return m


def diol(m, p, oh1, me, oh2, h2):
    m.ring(p, 0, 0, 6, L, 90)
    m.sub(p + "o1", p + "1", 60, "OH", kind=oh1)
    m.sub(p + "m", p + "1", 0, "CH_3", kind=me)
    m.sub(p + "o2", p + "2", -30, "OH", kind=oh2)
    m.sub(p + "h", p + "2", -90, "H", kind=h2)
    return m


def f10_2007_11():
    f = Fig(800, 300)
    m = epox_ring(Mol(), "e")
    f.mol(m, 385, 110)
    f.text(395, 175, "(1R,2S)-1-methyl-1,2-epoxycyclohexane", size=11)
    # A (산)
    f.arrow(330, 105, 250, 105, "H₃O⁺", "C1(3차) 공격")
    m = diol(Mol(), "a", "h", "w", "w", "h")
    f.mol(m, 110, 110)
    f.cap(130, 180, "A: (1S,2S)")
    # B (염기)
    f.arrow(470, 105, 550, 105, "OH⁻/H₂O", "C2(2차) 공격")
    m = diol(Mol(), "b", "w", "h", "h", "w")
    f.mol(m, 620, 110)
    f.cap(640, 180, "B: (1R,2R)")
    f.text(400, 212, "A, B 모두 trans-1-methylcyclohexane-1,2-diol이지만 서로 거울상 이성질체", size=12, weight="bold", color=RED)
    f.box(20, 228, 370, 64, fill="#f7f9fc")
    f.text(30, 246, "산성: 양성자화된 에폭사이드 → C1에 δ+ 집중", size=11.5, anchor="start")
    f.text(30, 264, "→ 더 치환된 C1을 뒷면 공격 (S_N1 성격의 S_N2)", size=11.5, anchor="start")
    f.text(30, 282, "→ C1 반전, C2 보존", size=11.5, anchor="start")
    f.box(410, 228, 370, 64, fill="#f7f9fc")
    f.text(420, 246, "염기성: 중성 에폭사이드에 OH⁻ 직접 공격 (S_N2)", size=11.5, anchor="start")
    f.text(420, 264, "→ 입체 장애가 작은 C2 공격", size=11.5, anchor="start")
    f.text(420, 282, "→ C2 반전, C1 보존", size=11.5, anchor="start")
    return f.render()


# ------------------------------------------------------------------ 2001 #17
def f10_2001_17():
    f = Fig(800, 245)
    f.text(20, 40, "CH₃CH₂CH₃ + Br₂", size=13, anchor="start")
    f.arrow(140, 36, 210, 36, "hν 또는 Δ", "라디칼")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30)
    m.sub("c", b, -30)
    m.sub("br", b, 90, "Br")
    f.mol(m, 235, 50)
    f.text(265, 80, "A (주, 97%)", size=11.5, weight="bold")
    f.text(265, 96, "2-bromopropane", size=11)
    f.text(325, 45, "+", size=16)
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30)
    c = m.sub("c", b, -30)
    m.sub("br", c, 30, "Br")
    f.mol(m, 345, 50)
    f.text(390, 80, "B (부, 3%)", size=11.5, weight="bold")
    f.text(390, 96, "1-bromopropane", size=11)
    f.box(470, 15, 315, 95, fill="#fff8e6", stroke="#f0c36d")
    f.text(480, 33, "Br· 수소 추출은 흡열 → 늦은 TS (Hammond)", size=11, anchor="start")
    f.text(480, 52, "→ 라디칼 안정성(2° > 1°) 차이가 크게 반영", size=11, anchor="start")
    f.text(480, 71, "선택성 2°:1° ≈ 82:1 (H 1개당)", size=11, anchor="start")
    f.text(480, 90, "2H×82 : 6H×1 ≈ 164 : 6 → A ≈ 97 %", size=11, anchor="start")
    # 2행
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30)
    m.sub("c", b, -30)
    m.sub("br", b, 90, "MgBr")
    f.mol(m, 60, 180)
    f.text(85, 210, "C: (CH₃)₂CHMgBr", size=11.5, weight="bold")
    f.text(155, 180, "+", size=16)
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.atom("b", 30, 0)
    o = m.atom("o", 15, -24, "O")
    m.bond(a, b)
    m.bond(a, o)
    m.bond(b, o)
    f.mol(m, 175, 190)
    f.arrow(230, 175, 300, 175, "1) Et₂O", "S_N2 개환")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30)
    m.sub("c", b, -30)
    d = m.sub("d", b, 90)
    e = m.sub("e", d, 30)
    m.sub("o", e, -30, "O^−")
    f.mol(m, 320, 190)
    f.text(420, 196, "MgBr⁺", size=11.5)
    f.arrow(450, 175, 520, 175, "2) H⁺", "")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30)
    m.sub("c", b, -30)
    d = m.sub("d", b, 90)
    e = m.sub("e", d, 30)
    m.sub("o", e, -30, "OH")
    f.mol(m, 545, 190)
    f.text(610, 215, "D: 3-methylbutan-1-ol", size=11.5, weight="bold")
    f.text(610, 232, "(탄소 2개 증가한 1차 알코올)", size=11, color=GRAY)
    return f.render()


# ================================================================== 11 벤젠과 방향족성
def poly_on_edge(m, p, a, b, n, side=1, bonds=True):
    """원자 a→b 변 위에 정 n각형을 만든다(side=±1: 진행 방향 왼/오른쪽). 새 원자 p0.. 반환 목록은 [a, b, 새 원자들]"""
    ax, ay = m.pos(a)
    bx, by = m.pos(b)
    d = math.hypot(bx - ax, by - ay)
    rr = d / (2 * math.sin(math.pi / n))
    mx, my = (ax + bx) / 2, (ay + by) / 2
    apo = d / (2 * math.tan(math.pi / n))
    nx, ny = -(by - ay) / d * side, (bx - ax) / d * side
    cx, cy = mx + nx * apo, my + ny * apo
    a0 = math.atan2(by - cy, bx - cx)
    names = [a, b]
    step = 2 * math.pi / n * (1 if (math.atan2(ay - cy, ax - cx) - a0) % (2 * math.pi) > math.pi else -1)
    for k in range(1, n - 1):
        t = a0 + step * k
        nm = f"{p}{k}"
        m.atom(nm, cx + rr * math.cos(t), cy + rr * math.sin(t))
        names.append(nm)
    if bonds:
        for i in range(1, n - 1):
            m.bond(names[i], names[i + 1])
        m.bond(names[-1], a)
    return names, (cx, cy)


def f11_24():
    f = Fig(800, 250)
    # (ㄱ) azulene
    m = Mol()
    m.ring("s", 0, 0, 7, 34.6, 90, bonds=False)
    for i in range(7):
        m.bond(f"s{i}", f"s{(i + 1) % 7}", "in" if i in (2, 4, 6) else 1, (0, 0) if i in (2, 4, 6) else None)
    nm, c5 = poly_on_edge(m, "f", "s1", "s2", 5, side=-1, bonds=False)
    m.bond(nm[1], nm[2]); m.bond(nm[2], nm[3], "in", c5); m.bond(nm[3], nm[4]); m.bond(nm[4], nm[0], "in", c5)
    f.mol(m, 65, 90, scale=0.8)
    f.text(85, 160, "(ㄱ) azulene", size=11.5, weight="bold")
    f.text(85, 178, "10π 방향족, μ ≈ 1.0 D", size=11)
    f.text(85, 196, "7원(+ 6π)·5원(− 6π) 기여", size=11)
    f.text(85, 216, "① ✗ (쌍극자 있음)", size=11.5, color=RED)
    # (ㄴ) COT
    m = Mol()
    m.ring("c", 0, 0, 8, 36, 90 - 22.5, bonds=False)
    for i in range(8):
        m.bond(f"c{i}", f"c{(i + 1) % 8}", "in" if i % 2 == 0 else 1, (0, 0) if i % 2 == 0 else None)
    f.mol(m, 235, 90, scale=0.8)
    f.text(235, 160, "(ㄴ) COT + 2K → COT²⁻", size=11.5, weight="bold")
    f.text(235, 178, "8π + 2e⁻ = 10π (4n+2, n=2)", size=11)
    f.text(235, 196, "평면 방향족 이음이온", size=11)
    f.text(235, 216, "② ✗ (12π 아님)", size=11.5, color=RED)
    # (ㄷ) tropylium
    m = Mol()
    m.ring("t", 0, 0, 7, 30, 90, bonds=False)
    for i in range(7):
        m.bond(f"t{i}", f"t{(i + 1) % 7}", "in" if i in (1, 3, 5) else 1, (0, 0) if i in (1, 3, 5) else None)
    m.sub("h", "t0", 90, "H", length=22)
    f.mol(m, 395, 95, scale=0.85)
    f.charge(395, 95)
    f.text(395, 160, "(ㄷ) C₇H₇⁺ (tropylium)", size=11.5, weight="bold")
    f.text(395, 178, "p 오비탈 7개 중첩, 6π", size=11)
    f.text(395, 196, "(빈 p 오비탈 포함)", size=11)
    f.text(395, 216, "③ ✗ (중첩 2p 7개)", size=11.5, color=RED)
    # (ㄹ) pyrene — Clar 구조: 위·아래 고리 sextet, 양 끝 C=C
    R = 17
    h3 = R * math.sqrt(3) / 2
    cen = [(-h3, 0), (h3, 0), (0, -1.5 * R), (0, 1.5 * R)]
    sx, sy = 560, 95
    segs = {}
    for (x, y) in cen:
        pts = [(x + R * math.cos(math.radians(90 - 60 * i)), y - R * math.sin(math.radians(90 - 60 * i))) for i in range(6)]
        for i in range(6):
            a_, b_ = pts[i], pts[(i + 1) % 6]
            key = tuple(sorted([(round(a_[0]), round(a_[1])), (round(b_[0]), round(b_[1]))]))
            segs[key] = (a_, b_)
    for (a_, b_) in segs.values():
        f.raw(f'<line x1="{sx + a_[0]:.1f}" y1="{sy + a_[1]:.1f}" x2="{sx + b_[0]:.1f}" y2="{sy + b_[1]:.1f}" stroke="{INK}" stroke-width="1.4"/>')
    for (x, y) in cen[2:]:
        f.raw(f'<circle cx="{sx + x:.1f}" cy="{sy + y:.1f}" r="{R * 0.55:.1f}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    for sg in (-1, 1):
        xx = sx + sg * (2 * h3 - 4.5)
        f.raw(f'<line x1="{xx:.1f}" y1="{sy - R / 2 + 3:.1f}" x2="{xx:.1f}" y2="{sy + R / 2 - 3:.1f}" stroke="{INK}" stroke-width="1.4"/>')
    f.text(560, 160, "(ㄹ) pyrene C₁₆H₁₀", size=11.5, weight="bold")
    f.text(560, 178, "16π (4n) 이지만 가장자리 14π", size=11)
    f.text(560, 196, "고리 전류 → 방향족", size=11)
    f.text(560, 216, "④ ○ (정답)", size=11.5, color=GREEN, weight="bold")
    # (ㅁ) [10]annulene (trans,cis,cis,cis,cis — 안쪽 H 2개)
    m = Mol()
    m.ring("a", -13, 0, 6, 26, 90, bonds=False)
    m.ring("b", 32, 0, 6, 26, 90, bonds=False)
    per = [("a1", "a0", "a"), ("a0", "a5", None), ("a5", "a4", "a"), ("a4", "a3", None), ("a3", "a2", "a"),
           ("b4", "b3", None), ("b3", "b2", "b"), ("b2", "b1", None), ("b1", "b0", "b"), ("b0", "b5", None)]
    for x_, y_, d_ in per:
        m.bond(x_, y_, "in" if d_ else 1, ((-13, 0) if d_ == "a" else (32, 0)) if d_ else None)
    m.atom("ha", 3, -6, "H")
    m.atom("hb", 16, 6, "H")
    m.bond("a1", "ha")
    m.bond("b4", "hb")
    f.mol(m, 715, 95, scale=0.85)
    f.text(725, 160, "(ㅁ) [10]annulene", size=11.5, weight="bold")
    f.text(725, 178, "10π 이지만 안쪽 H–H 반발", size=11)
    f.text(725, 196, "→ 비평면 → 비방향족", size=11)
    f.text(725, 216, "⑤ ✗ (Br₂ 첨가 반응)", size=11.5, color=RED)
    return f.render()


def frost(f, x, y, n, ne, R=34, title=None, verdict=None, col=INK):
    """Frost 원: n각형(꼭짓점 아래), ne개 π 전자 채우기"""
    f.raw(f'<circle cx="{x}" cy="{y}" r="{R}" fill="none" stroke="#b8c0cc" stroke-dasharray="3 3"/>')
    pts = []
    for k in range(n):
        t = -math.pi / 2 + 2 * math.pi * k / n
        pts.append((x + R * math.cos(t), y - R * math.sin(t)))
    f.raw('<polygon points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in pts) + f'" fill="none" stroke="{INK}" stroke-width="1"/>')
    # 준위 (y 좌표별로 묶기)
    lv = {}
    for a, b in pts:
        lv.setdefault(round(b, 1), []).append(a)
    levels = sorted(lv.items(), key=lambda kv: -kv[0])  # 아래(낮은 에너지)부터
    left = ne
    for yy, xs in levels:
        for xx in sorted(xs):
            f.raw(f'<line x1="{xx - 9:.1f}" y1="{yy:.1f}" x2="{xx + 9:.1f}" y2="{yy:.1f}" stroke="{BLUE}" stroke-width="2.4"/>')
        # 전자 채우기: 겹친 준위는 Hund 규칙
        k = len(xs)
        fill = [0] * k
        for e in range(min(left, 2 * k)):
            fill[e % k] += 1
        left -= min(left, 2 * k)
        for xx, nfill in zip(sorted(xs), fill):
            if nfill >= 1:
                f.text(xx - 3, yy - 8, "↑", size=11, color=RED)
            if nfill == 2:
                f.text(xx + 3, yy - 8, "↓", size=11, color=RED)
    if title:
        f.text(x, y + R + 18, title, size=11.5, weight="bold")
    if verdict:
        f.text(x, y + R + 36, verdict, size=11.5, color=col, weight="bold")


def f11_2005_12():
    f = Fig(800, 300)
    # cyclopentadiene → anion
    m = Mol()
    m.ring("c", 0, 0, 5, 25.5, 90, bonds=False)
    for i, k in enumerate([1, "in", 1, "in", 1]):
        m.bond(f"c{i}", f"c{(i + 1) % 5}", k, (0, 0) if k == "in" else None)
    m.sub("h1", "c0", 120, "H", length=22)
    m.sub("h2", "c0", 60, "H", length=22)
    f.mol(m, 60, 80)
    f.text(60, 130, "pKₐ ≈ 16", size=11.5, weight="bold", color=GREEN)
    f.arrow(100, 80, 160, 80, "−H⁺", "")
    m = Mol()
    m.ring("c", 0, 0, 5, 25.5, 90, bonds=False)
    for i, k in enumerate([1, "in", 1, "in", 1]):
        m.bond(f"c{i}", f"c{(i + 1) % 5}", k, (0, 0) if k == "in" else None)
    m.sub("h1", "c0", 90, "H", length=20)
    f.mol(m, 200, 80)
    f.charge(200, 54, "−")
    f.text(200, 130, "C₅H₅⁻: 6π, 평면", size=11.5)
    frost(f, 320, 80, 5, 6, title="", verdict="")
    f.text(320, 145, "결합성 MO 모두 채움", size=11.5)
    f.text(320, 163, "방향족 → 매우 안정", size=11.5, color=GREEN, weight="bold")
    # cycloheptatriene → anion
    m = Mol()
    m.ring("t", 0, 0, 7, 34.6, 90, bonds=False)
    for i, k in enumerate([1, "in", 1, "in", 1, "in", 1]):
        m.bond(f"t{i}", f"t{(i + 1) % 7}", k, (0, 0) if k == "in" else None)
    m.sub("h1", "t0", 120, "H", length=22)
    m.sub("h2", "t0", 60, "H", length=22)
    f.mol(m, 470, 90, scale=0.85)
    f.text(470, 150, "pKₐ ≈ 36–39", size=11.5, weight="bold", color=RED)
    f.arrow(515, 85, 570, 85, "−H⁺", "")
    m = Mol()
    m.ring("t", 0, 0, 7, 34.6, 90, bonds=False)
    for i, k in enumerate([1, "in", 1, "in", 1, "in", 1]):
        m.bond(f"t{i}", f"t{(i + 1) % 7}", k, (0, 0) if k == "in" else None)
    m.sub("h1", "t0", 90, "H", length=20)
    f.mol(m, 615, 90, scale=0.85)
    f.charge(615, 62, "−")
    f.text(615, 150, "C₇H₇⁻: 8π", size=11.5)
    frost(f, 735, 90, 7, 8)
    f.text(735, 150, "비결합성 준위에 홀전자 2개", size=11)
    f.text(735, 168, "반방향족 → 불안정", size=11.5, color=RED, weight="bold")
    f.box(20, 195, 760, 95, fill="#f7f9fc")
    f.text(35, 215, "Hückel 규칙: 고리형 · 평면 · 완전 공액 + (4n+2)π → 방향족 (특별히 안정),  4nπ → 반방향족 (특별히 불안정)", size=11.5, anchor="start")
    f.text(35, 238, "산성도 ∝ 짝염기의 안정성:  C₅H₅⁻ (6π, n=1) 방향족 ≫ C₇H₇⁻ (8π, n=2의 4n) 반방향족", size=11.5, anchor="start")
    f.text(35, 261, "∴ cyclopentadiene (pKₐ ≈ 16, 물·알코올 수준)이 cycloheptatriene (pKₐ ≈ 36)보다 약 10²⁰배 더 강한 산", size=11.5, anchor="start", weight="bold")
    f.text(35, 281, "(참고: 양이온은 반대 — C₇H₇⁺ 6π 방향족(안정), C₅H₅⁺ 4π 반방향족(불안정))", size=11, anchor="start", color=GRAY)
    return f.render()


# ================================================================== 12 방향족 화합물의 반응
def benzyne_ring(m, p, e):
    """벤자인: 변 e(원자 p{e}–p{e+1})가 삼중 결합. 바깥 선은 outer_line()으로 추가"""
    m.ring(p, 0, 0, 6, L, 90, bonds=False)
    kinds = ["in" if (i - e) % 2 == 0 else 1 for i in range(6)]
    ring_bonds(m, p, kinds)
    return m


def outer_line(f, m, p, e, x, y, sc=1.0):
    ax, ay = m.pos(f"{p}{e}")
    bx, by = m.pos(f"{p}{(e + 1) % 6}")
    mx, my = (ax + bx) / 2, (ay + by) / 2
    d = math.hypot(mx, my)
    ox, oy = mx / d * 5.5, my / d * 5.5
    sh = 0.14
    x1, y1 = ax + (bx - ax) * sh + ox, ay + (by - ay) * sh + oy
    x2, y2 = bx - (bx - ax) * sh + ox, by - (by - ay) * sh + oy
    f.raw(f'<line x1="{x + x1 * sc:.1f}" y1="{y + y1 * sc:.1f}" x2="{x + x2 * sc:.1f}" y2="{y + y2 * sc:.1f}" stroke="{INK}" stroke-width="1.4"/>')
def arom(m, p, cx=0, cy=0, start=90):
    return benzene(m, p, cx, cy, start)


def f12_37_a():
    """ㄱ: 벤자인 경로"""
    f = Fig(800, 250)
    f.text(20, 18, "ㄱ. 4-chlorotoluene + NaNH₂/NH₃(l): 제거–첨가(벤자인) — Cl 자리와 그 이웃 자리에 NH₂", size=12.5, anchor="start", weight="bold")
    m = Mol()
    arom(m, "r")
    m.sub("me", "r0", 90)
    m.sub("cl", "r3", -90, "Cl")
    m.sub("h", "r2", -30, "H")
    f.mol(m, 60, 115)
    f.text(60, 205, "4-chlorotoluene", size=11)
    f.arrow(120, 110, 200, 110, "NH₂⁻", "−NH₃, −Cl⁻")
    # 벤자인
    m = benzyne_ring(Mol(), "b", 2)
    m.sub("me", "b0", 90)
    f.mol(m, 250, 115)
    outer_line(f, m, "b", 2, 250, 115)
    f.text(250, 205, "4-methylbenzyne", size=11)
    f.arrow(300, 90, 390, 60, "", "")
    f.text(330, 58, "NH₂⁻ → C4", size=11, anchor="end")
    f.arrow(300, 140, 390, 170, "", "")
    f.text(330, 172, "NH₂⁻ → C3", size=11, anchor="end")
    m = Mol()
    arom(m, "p")
    m.sub("me", "p0", 90)
    m.sub("n", "p3", -90, "NH_2")
    f.mol(m, 450, 65, scale=0.8)
    f.text(535, 60, "p-toluidine", size=11.5, anchor="start")
    m = Mol()
    arom(m, "q")
    m.sub("me", "q0", 90)
    m.sub("n", "q2", -30, "NH_2")
    f.mol(m, 450, 175, scale=0.8)
    f.text(535, 185, "m-toluidine", size=11.5, anchor="start")
    f.text(535, 110, "≈ 1 : 1 혼합물", size=12, anchor="start", weight="bold")
    f.box(640, 40, 150, 150, fill="#fff5f5", stroke="#f0b4ac")
    f.text(715, 60, "보기의 생성물", size=11.5, weight="bold", color=RED)
    m = Mol()
    arom(m, "x")
    m.sub("me", "x0", 90)
    m.sub("n", "x1", 30, "NH_2")
    m.sub("cl", "x3", -90, "Cl")
    f.mol(m, 705, 120, scale=0.7)
    f.text(715, 180, "Cl 유지 + ortho NH₂ ✗", size=11, color=RED)
    return f.render()


def f12_37_bc():
    f = Fig(800, 310)
    f.text(20, 18, "ㄴ. S_NAr (첨가–제거): o·p-NO₂가 Meisenheimer 착물의 음전하를 공명 안정화", size=12.5, anchor="start", weight="bold")
    m = Mol()
    arom(m, "r")
    m.sub("cl", "r0", 90, "Cl")
    m.sub("n1", "r1", 30, "NO_2")
    m.sub("n2", "r3", -90, "NO_2")
    f.mol(m, 60, 100)
    f.arrow(125, 95, 195, 95, "H₂NNH₂", "첨가 (느림)")
    m = Mol()
    m.ring("s", 0, 0, 6, L, 90, bonds=False)
    ring_bonds(m, "s", [1, "in", 1, 1, "in", 1])
    m.sub("cl", "s0", 130, "Cl")
    m.sub("nh", "s0", 50, "NH_2NH_2^+")
    m.sub("n1", "s1", 30, "NO_2")
    m.sub("n2", "s3", -90, "NO_2")
    f.mol(m, 260, 105)
    f.charge(262, 108, "−")
    f.text(262, 192, "Meisenheimer 착물", size=11.5)
    f.arrow(335, 95, 400, 95, "−Cl⁻, −H⁺", "제거 (빠름)")
    m = Mol()
    arom(m, "p")
    n = m.sub("nh", "p0", 90, "NH")
    m.sub("nh2", n, 30, "NH_2")
    m.sub("n1", "p1", 30, "NO_2")
    m.sub("n2", "p3", -90, "NO_2")
    f.mol(m, 460, 110)
    f.text(460, 196, "2,4-dinitrophenylhydrazine", size=11.5)
    ok(f, 770, 100, True, "ㄴ ✓")
    # 음전하 비편재
    f.text(580, 60, "음전하 비편재 위치:", size=11.5, anchor="start")
    f.text(580, 80, "C2, C4, C6 (Cl 기준 o, p)", size=11.5, anchor="start")
    f.text(580, 100, "→ C2·C4의 NO₂ 산소까지", size=11.5, anchor="start")
    f.text(580, 120, "(니트로 공명 구조)", size=11.5, anchor="start")
    # ㄷ
    f.text(20, 228, "ㄷ. 피리딘 나이트로화: N이 고리를 강하게 불활성화(+ 산성에서 피리디늄) → 가혹 조건, C3 치환", size=12.5, anchor="start", weight="bold")
    m = Mol()
    m.ring("y", 0, 0, 6, 24, 90, bonds=False)
    ring_bonds(m, "y", ["in", 1, "in", 1, "in", 1])
    m.label("y3", "N")
    f.mol(m, 50, 272)
    f.arrow(85, 268, 165, 268, "HNO₃/H₂SO₄", "300 ℃")
    m = Mol()
    m.ring("y", 0, 0, 6, 24, 90, bonds=False)
    ring_bonds(m, "y", ["in", 1, "in", 1, "in", 1])
    m.label("y3", "N")
    m.sub("n", "y1", 30, "NO_2", length=24)
    f.mol(m, 200, 272)
    f.text(270, 255, "3-nitropyridine (저수율)", size=11.5, anchor="start")
    f.text(270, 275, "C2·C4 공격 σ 착물: 공명 구조 하나가 N⁺(6전자) → 매우 불안정", size=11.5, anchor="start")
    f.text(270, 295, "C3 공격 σ 착물: 양전하가 N에 오지 않음 → 상대적으로 유리", size=11.5, anchor="start")
    ok(f, 770, 272, True, "ㄷ ✓")
    return f.render()


def f12_2006_11():
    f = Fig(800, 200)
    m = Mol()
    arom(m, "r")
    f.mol(m, 45, 100)
    f.arrow(85, 95, 190, 95, "(나) EtCOCl, AlCl₃", "F-C 아실화")
    m = Mol()
    arom(m, "a")
    c = m.sub("c", "a1", 30)
    m.sub("o", c, 90, "O", kind="2")
    e = m.sub("e", c, -30)
    m.sub("e2", e, 30)
    f.mol(m, 230, 105)
    f.text(250, 160, "propiophenone", size=11)
    f.text(250, 176, "(C=O: meta 지향)", size=11, color=BLUE)
    f.arrow(320, 95, 425, 95, "(가) Br₂, FeBr₃", "meta 브로민화")
    m = Mol()
    arom(m, "b")
    c = m.sub("c", "b1", 30)
    m.sub("o", c, 90, "O", kind="2")
    e = m.sub("e", c, -30)
    m.sub("e2", e, 30)
    m.sub("br", "b3", -90, "Br")
    f.mol(m, 465, 95)
    f.text(485, 170, "m-bromopropiophenone", size=11)
    f.arrow(555, 95, 650, 95, "(라) Zn(Hg), HCl", "Clemmensen")
    m = Mol()
    arom(m, "c")
    c = m.sub("c", "c1", 30)
    e = m.sub("e", c, -30)
    m.sub("e2", e, 30)
    m.sub("br", "c3", -90, "Br")
    f.mol(m, 690, 95)
    f.text(705, 170, "m-bromopropylbenzene", size=11, weight="bold")
    f.text(400, 192, "불필요: (다) 1-클로로프로페인 F-C 알킬화 — 1차 C⁺ 자리옮김(→ isopropyl)·o/p 지향·다중 알킬화 / (마) KMnO₄ — 곁사슬을 COOH로 산화", size=11, color=RED)
    return f.render()


def f12_2005_9():
    f = Fig(800, 250)
    m = Mol()
    arom(m, "r")
    m.sub("br", "r0", 90, "Br")
    m.sub("h", "r1", 30, "H")
    m.sub("o", "r3", -90, "OCH_3")
    f.mol(m, 60, 120)
    f.text(60, 210, "p-bromoanisole", size=11)
    f.curly(150, 60, 106, 88, bend=0.4)
    f.text(155, 55, "NH₂⁻", size=11.5, color=RED, anchor="start")
    f.arrow(120, 115, 200, 115, "① −NH₃", "② −Br⁻ (E2형)")
    m = benzyne_ring(Mol(), "b", 0)
    m.sub("o", "b3", -90, "OCH_3")
    f.mol(m, 255, 120)
    outer_line(f, m, "b", 0, 255, 120)
    f.text(255, 210, "벤자인 (3,4-didehydroanisole)", size=11)
    f.text(255, 226, "sp² 궤도 옆면 겹침 → 약한 π 결합", size=10.5, color=GRAY)
    f.arrow(310, 90, 400, 60, "", "")
    f.text(340, 58, "NH₂⁻ → C4", size=11, anchor="end")
    f.arrow(310, 150, 400, 185, "", "")
    f.text(340, 188, "NH₂⁻ → C3", size=11, anchor="end")
    m = Mol()
    arom(m, "p")
    m.sub("n", "p0", 90, "NH_2")
    m.sub("o", "p3", -90, "OCH_3")
    f.mol(m, 460, 75, scale=0.8)
    f.text(530, 60, "p-anisidine (4-methoxyaniline)", size=11.5, anchor="start", weight="bold")
    f.text(530, 80, "원래 Br 자리(ipso)에 NH₂", size=11, anchor="start")
    m = Mol()
    arom(m, "q")
    m.sub("n", "q1", 30, "NH_2")
    m.sub("o", "q3", -90, "OCH_3")
    f.mol(m, 460, 175, scale=0.8)
    f.text(530, 170, "m-anisidine (3-methoxyaniline)", size=11.5, anchor="start", weight="bold")
    f.text(530, 190, "이웃 자리(cine 치환)에 NH₂", size=11, anchor="start")
    f.text(530, 225, "벤자인의 두 탄소 모두 공격 가능 → 두 이성질체", size=11.5, anchor="start", color=RED)
    return f.render()


def ring_sub(f, p, x, y, subs, sc=0.8):
    """벤젠 + 치환기 {원자번호: 라벨 | 'iPr'} (0=위, 1=오른쪽 위, 2=오른쪽 아래, 3=아래 ...)"""
    m = Mol()
    arom(m, p)
    for i, lab in subs.items():
        ang = 90 - 60 * i
        if lab == "iPr":
            c = m.sub(p + "c", f"{p}{i}", ang)
            m.sub(p + "c1", c, ang - 60)
            m.sub(p + "c2", c, ang + 60)
        else:
            m.sub(f"{p}s{i}", f"{p}{i}", ang, lab)
    f.mol(m, x, y, scale=sc)
    return m


def f12_2002_13():
    f = Fig(800, 300)
    ring_sub(f, "r", 60, 150, {0: "iPr"})
    f.text(60, 205, "cumene", size=11)
    f.text(60, 222, "(알킬: o,p 지향·활성화)", size=10.5, color=BLUE)
    f.arrow(110, 125, 185, 90)
    f.text(130, 92, "HNO₃/H₂SO₄", size=11)
    f.arrow(110, 175, 185, 210)
    f.text(120, 228, "1) KMnO₄, OH⁻, Δ", size=11, anchor="start")
    f.text(120, 244, "2) H₃O⁺", size=11, anchor="start")
    ring_sub(f, "a", 235, 85, {0: "iPr", 3: "NO_2"})
    f.text(290, 70, "A: p-nitrocumene", size=11.5, anchor="start", weight="bold")
    f.text(290, 88, "(ortho는 입체 장애로 소량)", size=10.5, anchor="start", color=GRAY)
    f.arrow(440, 85, 520, 85, "1) KMnO₄, OH⁻, Δ", "2) H₃O⁺")
    ring_sub(f, "b", 570, 85, {0: "COOH", 3: "NO_2"})
    f.text(625, 85, "B: p-nitrobenzoic acid", size=11.5, anchor="start", weight="bold")
    ring_sub(f, "c", 235, 215, {0: "COOH"})
    f.text(290, 205, "C: benzoic acid", size=11.5, anchor="start", weight="bold")
    f.text(290, 223, "(벤질 C–H 1개 이상 → COOH)", size=10.5, anchor="start", color=GRAY)
    f.arrow(440, 215, 520, 215, "HNO₃/H₂SO₄", "")
    ring_sub(f, "d", 570, 215, {0: "COOH", 2: "NO_2"})
    f.text(640, 250, "D: m-nitrobenzoic acid", size=11.5, anchor="start", weight="bold")
    f.text(640, 268, "(COOH: meta 지향·불활성화)", size=10.5, anchor="start", color=GRAY)
    f.text(400, 292, "B(para)와 D(meta)는 같은 시약을 순서만 바꾼 결과 — 지향성은 반응 시점에 고리에 있는 치환기가 결정", size=11.5, color=RED, weight="bold")
    return f.render()


def f12_2000_11():
    f = Fig(800, 260)
    ring_sub(f, "r", 50, 125, {})
    f.arrow(90, 105, 165, 70)
    f.text(85, 60, "HNO₃, H₂SO₄", size=11, anchor="start")
    f.arrow(90, 145, 165, 180)
    f.text(95, 190, "Br₂, Fe", size=11, anchor="start")
    ring_sub(f, "a", 210, 75, {0: "NO_2"})
    f.text(250, 105, "nitrobenzene", size=11, anchor="start")
    f.text(250, 121, "(NO₂: meta 지향)", size=10.5, anchor="start", color=BLUE)
    f.arrow(375, 75, 470, 75, "Br₂, FeBr₃", "가열")
    ring_sub(f, "b", 520, 75, {0: "NO_2", 2: "Br"})
    f.text(575, 75, "m-bromonitrobenzene", size=11.5, anchor="start", weight="bold")
    ring_sub(f, "c", 210, 185, {0: "Br"})
    f.text(250, 215, "bromobenzene", size=11, anchor="start")
    f.text(250, 231, "(Br: o,p 지향)", size=10.5, anchor="start", color=BLUE)
    f.arrow(375, 185, 470, 185, "HNO₃, H₂SO₄", "")
    ring_sub(f, "d", 520, 180, {0: "Br", 3: "NO_2"})
    f.text(575, 175, "p-bromonitrobenzene", size=11.5, anchor="start", weight="bold")
    f.text(575, 193, "(+ ortho 이성질체, 재결정 분리)", size=10.5, anchor="start", color=GRAY)
    f.text(400, 252, "순서가 위치를 결정: meta 지향기(NO₂) 먼저 → meta,  o/p 지향기(Br) 먼저 → para", size=11.5, weight="bold", color=RED)
    return f.render()


def f12_1997_map():
    f = Fig(800, 340)
    sc = 0.7
    ring_sub(f, "r0", 50, 55, {}, sc)
    f.arrow(85, 55, 165, 55, "HNO₃/H₂SO₄", "")
    ring_sub(f, "a", 210, 55, {1: "NO_2"}, sc)
    f.text(215, 98, "A: nitrobenzene", size=11.5, weight="bold")
    f.arrow(270, 55, 350, 55, "Sn, HCl", "")
    ring_sub(f, "an", 395, 55, {1: "NH_2"}, sc)
    f.text(425, 95, "aniline", size=11, anchor="start")
    f.arrow(50, 85, 50, 145)
    f.text(58, 115, "Br₂/FeBr₃", size=10.5, anchor="start")
    ring_sub(f, "br", 50, 175, {1: "Br"}, sc)
    f.arrow(100, 175, 175, 175, "NaNH₂/NH₃", "(−HBr)")
    m = benzyne_ring(Mol(), "bz", 1)
    f.mol(m, 215, 175, scale=sc)
    outer_line(f, m, "bz", 1, 215, 175, sc)
    f.text(215, 215, "B: benzyne", size=11.5, weight="bold")
    f.arrow(245, 150, 360, 85)
    f.text(292, 108, "NH₃", size=11, anchor="end")
    f.arrow(50, 205, 50, 255)
    f.text(58, 230, "NaOH, H₂O, 340 ℃ → H₃O⁺", size=10.5, anchor="start")
    ring_sub(f, "ph", 50, 290, {1: "OH"}, sc)
    f.arrow(450, 60, 560, 60, "CH₃COOH", "(가열, −H₂O)")
    m = Mol()
    arom(m, "c")
    n = m.sub("n", "c1", 30, "NH")
    c = m.sub("cc", n, -30)
    m.sub("o", c, -90, "O", kind="2")
    m.sub("me", c, 30)
    f.mol(m, 600, 60, scale=sc)
    f.text(640, 110, "C: acetanilide", size=11.5, weight="bold")
    f.arrow(395, 85, 395, 180)
    f.text(403, 125, "NaNO₂, HCl", size=10.5, anchor="start")
    f.text(403, 140, "0–5 ℃ (다이아조화)", size=10.5, anchor="start")
    m = Mol()
    arom(m, "d")
    n = m.sub("n", "d1", 30, "N^+")
    m.sub("n2", n, 30, "N", kind=3)
    f.mol(m, 385, 215, scale=sc)
    f.text(455, 205, "Cl⁻", size=11)
    f.text(410, 258, "D: benzenediazonium chloride", size=11.5, weight="bold")
    f.arrow(100, 290, 540, 290)
    f.text(320, 280, "페놀(약염기성) + D → 아조 짝지음 (para)", size=11)
    f.arrow(460, 235, 540, 270)
    m = Mol()
    arom(m, "e")
    n = m.sub("n", "e1", 30, "N")
    n2 = m.sub("n2", n, -30, "N", kind="2")
    m.ring("g", m.pos(n2)[0] + 2 * L * math.cos(math.radians(30)), m.pos(n2)[1] - L, 6, L, 210, arom=[0, 2, 4])
    m.bond(n2, "g0")
    m.sub("oh", "g3", 30, "OH")
    f.mol(m, 575, 300, scale=0.6)
    f.text(680, 330, "E: p-hydroxyazobenzene", size=11.5, weight="bold")
    return f.render()


def f12_1997_mech():
    f = Fig(800, 240)
    f.text(20, 18, "1-2. 브로민화: ① Br₂ + FeBr₃ → Br⁺ 친전자체 ② π 전자 공격 → σ 착물(느림) ③ H⁺ 이탈 → 방향족성 회복(빠름)", size=12, anchor="start", weight="bold")
    f.text(30, 55, "Br–Br + FeBr₃ ⇌ Br^{δ+}···Br–FeBr₃^{δ−}  (Lewis 산이 Br–Br을 분극)", size=12, anchor="start")
    m = Mol()
    arom(m, "r")
    f.mol(m, 50, 140)
    f.curly(62, 118, 110, 90, bend=-0.4)
    f.text(130, 88, "Br⁺", size=12, color=RED)
    f.arrow(95, 135, 165, 135, "느림 (RDS)", "")
    for k, (pos_plus) in enumerate([1, 3, 5]):
        m = Mol()
        m.ring("s", 0, 0, 6, L, 90, bonds=False)
        dbl = {1: [1, 1, "in", 1, "in", 1], 3: [1, "in", 1, 1, "in", 1], 5: [1, "in", 1, "in", 1, 1]}[pos_plus]
        ring_bonds(m, "s", dbl)
        m.sub("br", "s0", 60, "Br")
        m.sub("h", "s0", 120, "H")
        x = 225 + k * 110
        f.mol(m, x, 140)
        px, py = m.pos(f"s{pos_plus}")
        f.charge(x + px * 0.55, 140 + py * 0.55)
        if k < 2:
            f.resarrow(x + 40, x + 70, 140)
    f.text(335, 200, "σ 착물 (arenium 이온): 양전하가 Br 기준 o, p 탄소에 비편재", size=11.5)
    f.arrow(505, 135, 575, 135, "FeBr₄⁻", "−H⁺ (빠름)")
    m = Mol()
    arom(m, "p")
    m.sub("br", "p0", 90, "Br")
    f.mol(m, 625, 145)
    f.text(700, 150, "+ HBr + FeBr₃", size=11.5, anchor="start")
    return f.render()


def f12_1997_phenol():
    f = Fig(800, 260)
    f.text(20, 18, "1-3. 페놀 나이트로화: –OH의 비공유 전자쌍이 σ 착물을 옥소늄 공명 구조로 추가 안정화 (o, p만 가능)", size=12, anchor="start", weight="bold")

    def sig(x, y, sub_idx, plus, oxon, lab):
        m = Mol()
        m.ring("s", 0, 0, 6, L, 90, bonds=False)
        kinds = [1] * 6
        # 이중 결합 배치: 양전하 위치와 sp3 탄소를 피해 지정
        for i in lab:
            kinds[i] = "in"
        ring_bonds(m, "s", kinds)
        if oxon:
            m.sub("o", "s0", 90, "OH^+", kind="2")
        else:
            m.sub("o", "s0", 90, "OH")
        m.sub("n", f"s{sub_idx}", -30 if sub_idx == 2 else (-90 if sub_idx == 3 else 30), "NO_2", length=26)
        m.sub("h", f"s{sub_idx}", -150 if sub_idx == 2 else (-150 if sub_idx == 3 else 90), "H", length=20)
        f.mol(m, x, y, scale=0.85)
        if plus is not None:
            px, py = m.pos(f"s{plus}")
            f.charge(x + px * 0.85 * 0.6, y + py * 0.85 * 0.6)
    # para 공격: sp3 = s3 ; 양전하 s2, s4, s0
    f.text(20, 55, "para", size=12, anchor="start", weight="bold", color=BLUE)
    sig(95, 105, 3, 2, False, [0, 4])
    f.resarrow(135, 160, 105)
    sig(205, 105, 3, 4, False, [1, 5])
    f.resarrow(245, 270, 105)
    sig(315, 105, 3, 0, False, [1, 4])
    f.resarrow(355, 380, 105)
    sig(425, 105, 3, None, True, [1, 4])
    f.box(372, 55, 108, 110, fill="none", stroke=GREEN)
    f.text(426, 180, "옥소늄: 모든 원자 옥텟", size=11, color=GREEN, weight="bold")
    f.box(510, 45, 280, 130, fill="#f7f9fc")
    f.text(520, 65, "ortho 공격도 같은 옥소늄 구조 가능", size=11.5, anchor="start")
    f.text(520, 85, "→ o, p σ 착물: 공명 구조 4개", size=11.5, anchor="start")
    f.text(520, 105, "meta 공격: 양전하가 C–OH 탄소에", size=11.5, anchor="start")
    f.text(520, 125, "오지 않음 → 3개만 (옥소늄 ✗)", size=11.5, anchor="start")
    f.text(520, 150, "∴ –OH: o,p 지향 + 강한 활성화", size=12, anchor="start", weight="bold", color=RED)
    f.text(400, 212, "묽은 HNO₃(상온)만으로도 o-·p-nitrophenol 생성 (o : p ≈ 1 : 1~2), 진한 HNO₃/H₂SO₄ → 2,4,6-trinitrophenol(피크르산)", size=11.5)
    f.text(400, 236, "(–OH의 유발 효과 −I < 공명 효과 +M → 전체적으로 전자 주개)", size=11, color=GRAY)
    return f.render()


# ================================================================== 참고 해설 반영 — 메커니즘 그림
def ap(m, n, ox, oy, sc=1.0):
    """분자 좌표 → 그림 절대 좌표"""
    x, y = m.pos(n)
    return ox + x * sc, oy + y * sc


def mid(p, q, t=0.5):
    return p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t


def hline(f, x1, y1, x2, y2, kind=1, col=INK):
    """그림 좌표에서 직접 결합선 (kind 1 | 2)"""
    if kind == 2:
        d = math.hypot(x2 - x1, y2 - y1) or 1
        nx, ny = -(y2 - y1) / d * 2.6, (x2 - x1) / d * 2.6
        for s in (1, -1):
            f.raw(f'<line x1="{x1 + nx * s:.1f}" y1="{y1 + ny * s:.1f}" x2="{x2 + nx * s:.1f}" y2="{y2 + ny * s:.1f}" stroke="{col}" stroke-width="1.4"/>')
    else:
        f.raw(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="1.4"/>')


# ------------------------------------------------------------------ 2013 #38 메커니즘
def f09_38_mech():
    f = Fig(800, 270)
    f.text(20, 18, "① A 단계(보호): O의 비공유쌍이 Si를 공격하고 Cl⁻가 떨어진 뒤, Et₃N이 O–H의 H⁺를 떼어 낸다", size=12.5, anchor="start", weight="bold")
    y = 85
    # R–O–H + Et3Si–Cl
    f.text(40, y, "R", size=14)
    hline(f, 48, y, 70, y)
    f.text(80, y, "O", size=14)
    f.lp(80, y - 13, 90)
    hline(f, 89, y, 108, y)
    f.text(116, y, "H", size=14)
    f.text(185, y, "Et₃Si", size=14)
    hline(f, 206, y, 228, y)
    f.text(240, y, "Cl", size=14)
    f.curly(82, y - 18, 182, y - 12, bend=-0.3)
    f.curly(217, y - 4, 242, y - 12, bend=-0.6)
    f.arrow(265, y, 320, y, "", "")
    # 옥소늄
    f.text(345, y, "R", size=14)
    hline(f, 353, y, 375, y)
    f.text(385, y, "O", size=14)
    f.charge(396, y - 12)
    hline(f, 394, y, 412, y)
    f.text(437, y, "SiEt₃", size=14)
    hline(f, 385, y + 9, 385, y + 28)
    f.text(385, y + 36, "H", size=14)
    f.text(468, y + 36, "Cl⁻", size=13)
    f.text(320, y + 58, "Et₃N", size=14)
    f.lp(342, y + 58, 0)
    f.curly(347, y + 56, 377, y + 40, bend=0.3)
    f.curly(392, y + 20, 396, y + 6, bend=0.9)
    f.arrow(495, y, 550, y, "", "")
    f.text(560, y, "R–O–SiEt₃  +  Et₃NH⁺ Cl⁻", size=14, anchor="start")
    f.text(560, y + 24, "(R = 3-bromocyclohexyl; O–H가 사라진 TES 에터)", size=11, anchor="start", color=GRAY)
    # ② 그리냐르
    f.text(20, 175, "② C 단계: C–Mg 결합의 전자쌍(δ⁻ 탄소)이 C=O 탄소(δ⁺)를 공격하고, π 전자쌍은 O로 → 알콕사이드", size=12.5, anchor="start", weight="bold")
    y = 235
    f.text(45, y, "R", size=14)
    f.text(45, y + 20, "δ⁻", size=10.5, color=BLUE)
    hline(f, 54, y, 82, y)
    f.text(105, y, "MgBr", size=14)
    f.text(105, y + 20, "δ⁺", size=10.5, color=BLUE)
    f.text(200, y, "H₂C", size=14)
    f.text(203, y + 20, "δ⁺", size=10.5, color=BLUE)
    hline(f, 218, y, 242, y, kind=2)
    f.text(252, y, "O", size=14)
    f.text(252, y + 20, "δ⁻", size=10.5, color=BLUE)
    f.lp(252, y - 13, 90)
    f.curly(68, y - 5, 192, y - 12, bend=-0.3)
    f.curly(230, y - 5, 252, y - 18, bend=-0.6)
    f.arrow(285, y, 340, y, "", "")
    f.text(350, y, "R–CH₂–O⁻ ⁺MgBr", size=14, anchor="start")
    f.arrow(495, y, 555, y, "H₂O", "")
    f.text(565, y, "R–CH₂–OH", size=14, anchor="start")
    f.text(565, y + 22, "(이후 D: H₃O⁺로 Si–O 절단)", size=11, anchor="start", color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 2012 #39 메커니즘
def f09_39_mech():
    f = Fig(800, 440)
    f.text(20, 18, "ㄱ. 어느 OH가 떠나는가 — 더 안정한 탄소 양이온을 만드는 경로가 빠르다", size=12.5, anchor="start", weight="bold")
    f.box(20, 32, 375, 74, fill="#f3faf6", stroke="#86b7a4")
    f.text(30, 50, "경로 ① (빠름): 곁사슬 C(Ph)₂–OH 양성자화 → H₂O 이탈", size=11.5, anchor="start")
    f.text(30, 70, "→ Ph₂C⁺ (3차 + 두 페닐 공명) → 고리 C–C 1,2-이동", size=11.5, anchor="start")
    f.text(30, 90, "→ 6원 고리 옥소카베늄 → −H⁺ → 2,2-diphenylcyclohexanone", size=11.5, anchor="start", color=GREEN)
    f.box(405, 32, 375, 74, fill="#fff5f5", stroke="#f0b4ac")
    f.text(415, 50, "경로 ② (느림): 고리 C–OH 양성자화 → H₂O 이탈", size=11.5, anchor="start")
    f.text(415, 70, "→ 3차 사이클로펜틸 양이온 (페닐 공명 없음)", size=11.5, anchor="start")
    f.text(415, 90, "→ 훨씬 불안정 → 이 경로의 생성물은 무시", size=11.5, anchor="start", color=RED)
    # ㄴ Criegee
    f.text(20, 128, "ㄴ. Baeyer–Villiger: 과산 첨가 → Criegee 중간체 → 사이클로헥실(2차)이 O로 이동하며 O–O 결합이 끊어짐", size=12.5, anchor="start", weight="bold")
    m = Mol()
    m.atom("c", 0, 0)
    m.sub("oh", "c", 90, "OH")
    m.sub("me", "c", 180, "H_3C")
    m.ring("q", -30, 52, 6, L, 60)
    m.bond("c", "q0")
    m.sub("o1", "c", 0, "O")
    m.sub("o2", "o1", 30, "O")
    cc = m.sub("cc", "o2", -30)
    m.sub("co", cc, -90, "O", kind="2")
    m.sub("ph", cc, 30, "Ph")
    ox, oy = 150, 200
    f.mol(m, ox, oy)
    C = ap(m, "c", ox, oy)
    Q = ap(m, "q0", ox, oy)
    O1 = ap(m, "o1", ox, oy)
    O2 = ap(m, "o2", ox, oy)
    OH = ap(m, "oh", ox, oy)
    f.curly(*mid(C, Q), O1[0] - 4, O1[1] + 9, bend=0.45)
    f.curly(*mid(O1, O2), O2[0] - 2, O2[1] - 12, bend=-0.7)
    f.lp(OH[0] - 13, OH[1], 0)
    f.curly(OH[0] - 16, OH[1] + 5, C[0] - 5, C[1] - 8, bend=0.6)
    f.text(150, 300, "Criegee 중간체", size=11.5)
    f.text(150, 316, "(이동하는 기는 입체 보존)", size=10.5, color=GRAY)
    f.arrow(300, 200, 370, 200, "", "")
    m = cyhex(Mol(), "b")
    o = m.sub("o1", "b1", 30, "O")
    c = m.sub("c", o, -30)
    m.sub("o", c, -90, "O", kind="2")
    m.sub("me", c, 30)
    f.mol(m, 420, 205)
    f.text(455, 270, "cyclohexyl acetate", size=11.5, color=GREEN)
    f.text(560, 200, "+ PhCO₂H", size=13, anchor="start")
    f.text(560, 230, "이동 경향: 3차 > 2차 ≈ Ph > 1차 > CH₃", size=11, anchor="start")
    f.text(560, 248, "→ CH₃가 이동한 methyl ester(보기 ㄴ) ✗", size=11, anchor="start", color=RED)
    # ㄷ Curtius
    f.text(20, 338, "ㄷ. Curtius: 아실 아자이드 가열 → R 이동과 N₂ 이탈이 협동 → 아이소사이아네이트 → 물 첨가·탈카복실화", size=12.5, anchor="start", weight="bold")
    m = Mol()
    m.atom("c", 0, 0)
    m.sub("r", "c", 210, "ArCH_2")
    m.sub("o", "c", 90, "O", kind="2")
    m.sub("n1", "c", -30, "N")
    m.sub("n2", "n1", 30, "N^+", kind="2")
    m.sub("n3", "n2", 30, "N^−", kind="2")
    ox, oy = 110, 400
    f.mol(m, ox, oy)
    C = ap(m, "c", ox, oy)
    R = ap(m, "r", ox, oy)
    N1 = ap(m, "n1", ox, oy)
    N2 = ap(m, "n2", ox, oy)
    f.lp(N1[0], N1[1] + 12, -90)
    f.curly(*mid(C, R, 0.45), N1[0] - 6, N1[1] + 6, bend=0.6)
    f.curly(*mid(N1, N2), N2[0] + 4, N2[1] - 12, bend=-0.7)
    f.arrow(225, 400, 285, 400, "Δ, −N₂", "")
    f.text(345, 400, "ArCH₂–N=C=O", size=13)
    f.arrow(400, 400, 450, 400, "H₂O", "")
    f.text(520, 400, "ArCH₂NH–COOH", size=13)
    f.text(520, 420, "(카밤산)", size=10.5, color=GRAY)
    f.arrow(585, 400, 635, 400, "−CO₂", "")
    f.text(690, 400, "ArCH₂NH₂", size=13, weight="bold")
    f.text(690, 420, "(탄소 1개 감소)", size=10.5, color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 2010 2차 [반응 II] B 합성 경로
def menth(m, lg=None, lg_kind="w", alkene=False):  # noqa
    m.ring("r", 0, 0, 6, L, 0, bonds=False)
    for i in range(6):
        m.bond(f"r{i}", f"r{(i + 1) % 6}", "2r" if (alkene and i == 0) else 1)
    m.sub("me", "r3", 180, "H_3C", kind="w")
    m.sub("ip", "r0", 0, "i-Pr", kind=(1 if alkene else "h"))
    if lg:
        m.sub("lg", "r1", -60, lg, kind=lg_kind)
    return m


def f10_2010_route():
    f = Fig(800, 360)
    f.text(20, 18, "[반응 Ⅱ] 같은 출발 물질에서 B 얻기 — C1 배열을 반전시켜 이탈기를 axial에 둘 수 있게 만든 뒤 E2 (참고 해설 경로)", size=12, anchor="start", weight="bold")
    sc = 0.75
    y = 90
    f.mol(menth(Mol(), "Cl", "w"), 85, y, scale=sc)
    f.text(85, y + 68, "출발 물질 (Cl eq)", size=11)
    f.arrow(160, y, 270, y, "① AcO⁻ (S_N2)", "C1 반전")
    f.mol(menth(Mol(), "OAc", "h"), 345, y, scale=sc)
    f.text(345, y + 68, "아세테이트 (반전)", size=11)
    f.arrow(420, y, 530, y, "② H₃O⁺, 가열", "아실–O 절단(배열 유지)")
    f.mol(menth(Mol(), "OH", "h"), 610, y, scale=sc)
    f.text(610, y + 68, "neomenthol형 알코올", size=11)
    f.arrow(700, y + 40, 700, 200, "", "")
    f.text(708, y + 62, "③ MsCl,", size=11, anchor="start")
    f.text(708, y + 78, "pyridine", size=11, anchor="start")
    f.text(708, y + 94, "(배열 유지)", size=11, anchor="start")
    y2 = 240
    f.mol(menth(Mol(), "OMs", "h"), 640, y2, scale=sc)
    f.text(640, y2 + 68, "메실레이트", size=11)
    f.arrow(565, y2, 455, y2, "④ NaOEt/EtOH", "E2")
    f.mol(menth(Mol(), alkene=True), 380, y2, scale=sc)
    f.text(380, y2 + 68, "B (p-menth-3-ene, Zaitsev)", size=11, weight="bold", color=BLUE)
    f.box(14, 185, 262, 134, fill="#fff8ec", stroke="#e6c48a")
    f.text(24, 203, "E1 조건(묽은 NaOEt, 180 ℃)의 한계", size=11.5, anchor="start", weight="bold")
    f.text(24, 223, "2차 C⁺ → 1,2-H 이동 → 3차 C⁺", size=11, anchor="start")
    f.text(24, 241, "→ S_N1 경쟁 (에틸 에터 부생성물)", size=11, anchor="start")
    f.text(24, 259, "→ 3차 C⁺의 E1: B와 그 거울상이", size=11, anchor="start")
    f.text(24, 277, "    함께 생김 (라세미)", size=11, anchor="start")
    f.text(24, 297, "→ B만 선택적으로 얻기 어려움", size=11, anchor="start", color=RED)
    f.text(510, 343, "OMs가 axial인 안정 의자형: C2–H·C6–H 모두 anti → 더 안정한 3치환 알켄 B 우세", size=11, color=GREEN)
    return f.render()


# ------------------------------------------------------------------ 2007 #11 산성 개환 메커니즘
def f10_2007_mech():
    f = Fig(800, 200)
    f.text(20, 18, "A의 메커니즘: ① O 양성자화 ② H₂O가 C1(3차, δ⁺ 큼)을 O 반대편에서 공격 (S_N1 성격의 S_N2) ③ −H⁺", size=12.5, anchor="start", weight="bold")
    m = epox_ring(Mol(), "e")
    f.mol(m, 80, 110)
    O = ap(m, "eO", 80, 110)
    f.lp(O[0] + 10, O[1], 0)
    f.text(O[0] + 52, O[1] - 28, "H⁺", size=13, color=RED)
    f.curly(O[0] + 14, O[1] - 4, O[0] + 46, O[1] - 22, bend=-0.4)
    f.arrow(185, 110, 245, 110, "", "")
    m = epox_ring(Mol(), "p")
    m.label("pO", "OH^+")
    f.mol(m, 320, 110)
    C1 = ap(m, "p1", 320, 110)
    O = ap(m, "pO", 320, 110)
    f.curly(*mid(C1, O, 0.45), O[0] - 2, O[1] + 12, bend=-0.6)
    f.text(C1[0] - 40, C1[1] - 30, "H₂O:", size=13, color=BLUE)
    f.curly(C1[0] - 26, C1[1] - 26, C1[0] - 5, C1[1] - 5, bend=0.3)
    f.text(320, 180, "양성자화된 에폭사이드", size=11)
    f.arrow(425, 110, 485, 110, "", "")
    m = diol(Mol(), "d", "h", "w", "w", "h")
    m.label("do1", "OH_2^+")
    f.mol(m, 560, 110)
    f.arrow(645, 110, 690, 110, "−H⁺", "")
    f.text(745, 110, "A", size=15, weight="bold")
    f.text(745, 132, "(1S,2S)", size=11)
    return f.render()


# ------------------------------------------------------------------ 2009 #24 보충
def azulene(m, polar=False):
    m.ring("s", 0, 0, 7, 34.6, 90, bonds=False)
    dbl7 = (2, 4, 6)
    for i in range(7):
        m.bond(f"s{i}", f"s{(i + 1) % 7}", "in" if i in dbl7 else 1, (0, 0) if i in dbl7 else None)
    nm, c5 = poly_on_edge(m, "f", "s1", "s2", 5, side=-1, bonds=False)
    if polar:  # s1=f3 전자쌍이 f3로 → s1(+), f3(−)
        m.bond(nm[1], nm[2]); m.bond(nm[2], nm[3], "in", c5); m.bond(nm[3], nm[4]); m.bond(nm[4], nm[0])
    else:
        m.bond(nm[1], nm[2]); m.bond(nm[2], nm[3], "in", c5); m.bond(nm[3], nm[4]); m.bond(nm[4], nm[0], "in", c5)
    return m, c5


def cot(f, x, y, R=26, dbl=True, inner=None):
    pts = [(x + R * math.cos(math.radians(67.5 - 45 * i)), y - R * math.sin(math.radians(67.5 - 45 * i))) for i in range(8)]
    for i in range(8):
        a, b = pts[i], pts[(i + 1) % 8]
        hline(f, a[0], a[1], b[0], b[1])
        if dbl and i % 2 == 0:
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            dx, dy = x - mx, y - my
            d = math.hypot(dx, dy)
            ox, oy = dx / d * 5, dy / d * 5
            hline(f, a[0] + (b[0] - a[0]) * 0.16 + ox, a[1] + (b[1] - a[1]) * 0.16 + oy,
                  b[0] - (b[0] - a[0]) * 0.16 + ox, b[1] - (b[1] - a[1]) * 0.16 + oy)
    if inner:
        f.raw(f'<circle cx="{x}" cy="{y}" r="{R * 0.6:.1f}" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    return pts


def f11_24_mech():
    f = Fig(800, 215)
    f.text(20, 18, "① azulene의 극성 공명 구조          ② COT의 2전자 환원 (전자 1개씩)", size=12.5, anchor="start", weight="bold")
    m, c5 = azulene(Mol())
    f.mol(m, 75, 100, scale=0.8)
    S1 = ap(m, "s1", 75, 100, 0.8)
    F3 = ap(m, "f3", 75, 100, 0.8)
    md = mid(S1, F3)
    f.curly(md[0] - 2, md[1] + 3, F3[0] + 6, F3[1] + 10, bend=0.8)
    f.resarrow(150, 185, 100)
    m, c5 = azulene(Mol(), polar=True)
    f.mol(m, 225, 100, scale=0.8)
    f.charge(225, 100, "+")
    f.charge(225 + c5[0] * 0.8, 100 + c5[1] * 0.8, "−")
    f.text(20, 165, "7원 고리: tropylium형 6π(+) · 5원 고리: cyclopentadienide형 6π(−)", size=11, anchor="start")
    f.text(20, 184, "→ 전자 밀도가 5원 고리로 치우침, μ ≈ 1.0 D (참고 해설 1.04 D)", size=11, anchor="start")
    f.text(20, 203, "① ‘쌍극자 모멘트를 갖지 않는다’ ✗", size=11, color=RED, anchor="start")
    # COT
    cot(f, 450, 92)
    f.arrow(485, 92, 530, 92, "K", "−K⁺")
    cot(f, 570, 92)
    f.text(570, 92, "•  −", size=13)
    f.arrow(605, 92, 650, 92, "K", "−K⁺")
    cot(f, 700, 92, dbl=False, inner=True)
    f.text(700, 92, "2−", size=12)
    f.text(450, 134, "COT (8π, 욕조형)", size=10.5)
    f.text(570, 134, "라디칼 음이온 (9π)", size=10.5)
    f.text(700, 134, "COT²⁻ (10π, 평면)", size=10.5)
    f.text(575, 165, "4n+2 = 10 (n = 2) → 방향족 이음이온", size=11)
    f.text(575, 184, "② ‘12개의 π 전자’ ✗", size=11, color=RED)
    return f.render()


# ------------------------------------------------------------------ 2012 #37 ㄱ 벤자인 메커니즘
def f12_37_a():
    """ㄱ: 벤자인 경로 (제거–첨가, 굽은 화살표)"""
    f = Fig(800, 360)
    f.text(20, 18, "ㄱ. 4-chlorotoluene + NaNH₂/NH₃(l): 제거(탈양성자화 → Cl⁻ 이탈) – 첨가(NH₂⁻ → 벤자인) – 양성자화", size=12.5, anchor="start", weight="bold")
    y = 140
    m = Mol()
    arom(m, "r")
    m.sub("me", "r0", 90)
    m.sub("cl", "r3", -90, "Cl")
    m.sub("h", "r2", -30, "H")
    f.mol(m, 60, y)
    H = ap(m, "h", 60, y)
    C2 = ap(m, "r2", 60, y)
    f.text(H[0] + 30, H[1] + 32, "NH₂⁻", size=12, color=RED)
    f.curly(H[0] + 22, H[1] + 24, H[0] + 6, H[1] + 8, bend=0.4)
    f.curly(*mid(C2, H), C2[0] + 4, C2[1] + 8, bend=0.9)
    f.text(60, y + 92, "4-chlorotoluene", size=11)
    f.arrow(130, y - 10, 185, y - 10, "−NH₃", "")
    # 아릴 음이온
    m = Mol()
    arom(m, "a")
    m.sub("me", "a0", 90)
    m.sub("cl", "a3", -90, "Cl")
    ox = 245
    f.mol(m, ox, y)
    A2 = ap(m, "a2", ox, y)
    A3 = ap(m, "a3", ox, y)
    CL = ap(m, "cl", ox, y)
    lpx, lpy = A2[0] + 13, A2[1] + 7.5
    f.lp(lpx, lpy, -30)
    f.charge(A2[0] + 18, A2[1] - 6, "−")
    f.curly(lpx + 2, lpy + 4, *mid(A2, A3), bend=0.6)
    f.curly(*mid(A3, CL), CL[0] + 9, CL[1] - 4, bend=-0.7)
    f.text(ox, y + 92, "아릴 음이온 (sp² 궤도)", size=11)
    f.arrow(315, y - 10, 370, y - 10, "−Cl⁻", "")
    # 벤자인
    m = benzyne_ring(Mol(), "b", 2)
    m.sub("me", "b0", 90)
    ox = 425
    f.mol(m, ox, y)
    outer_line(f, m, "b", 2, ox, y)
    f.text(ox, y + 92, "4-methylbenzyne", size=11)
    f.arrow(470, y - 25, 525, y - 70, "", "")
    f.arrow(470, y + 15, 525, y + 60, "", "")
    f.text(492, y - 70, "NH₂⁻ → C4", size=11, anchor="end")
    f.text(492, y + 62, "NH₂⁻ → C3", size=11, anchor="end")
    # C4 첨가 → C3 음이온
    sc = 0.7
    m = Mol()
    arom(m, "p")
    m.sub("me", "p0", 90)
    m.sub("n", "p3", -90, "NH_2")
    f.mol(m, 570, 75, scale=sc)
    P2 = ap(m, "p2", 570, 75, sc)
    f.charge(P2[0] + 12, P2[1] + 6, "−")
    f.arrow(605, 75, 655, 75, "NH₃", "")
    m = Mol()
    arom(m, "pp")
    m.sub("me", "pp0", 90)
    m.sub("n", "pp3", -90, "NH_2")
    f.mol(m, 700, 75, scale=sc)
    f.text(700, 140, "p-toluidine", size=11.5, weight="bold")
    # C3 첨가 → C4 음이온
    m = Mol()
    arom(m, "q")
    m.sub("me", "q0", 90)
    m.sub("n", "q2", -30, "NH_2")
    f.mol(m, 570, 215, scale=sc)
    Q3 = ap(m, "q3", 570, 215, sc)
    f.charge(Q3[0], Q3[1] + 13, "−")
    f.arrow(615, 215, 655, 215, "NH₃", "")
    m = Mol()
    arom(m, "qq")
    m.sub("me", "qq0", 90)
    m.sub("n", "qq2", -30, "NH_2")
    f.mol(m, 700, 215, scale=sc)
    f.text(700, 268, "m-toluidine", size=11.5, weight="bold")
    f.text(765, 160, "≈ 1 : 1", size=12, weight="bold")
    # 보기
    f.box(20, 285, 760, 64, fill="#fff5f5", stroke="#f0b4ac")
    m = Mol()
    arom(m, "x")
    m.sub("me", "x0", 90)
    m.sub("n", "x1", 30, "NH_2")
    m.sub("cl", "x3", -90, "Cl")
    f.mol(m, 75, 318, scale=0.5)
    f.text(120, 305, "보기 ㄱ의 생성물(5-chloro-2-methylaniline): Cl이 그대로 남고 CH₃의 ortho에 NH₂ → 벤자인 경로로는 생길 수 없음 ✗", size=11.5, anchor="start", color=RED)
    f.text(120, 328, "실제: Cl이 떨어지고 NH₂는 원래 Cl 자리(ipso, C4) 또는 그 이웃(cine, C3)에만 들어감", size=11.5, anchor="start")
    return f.render()


# ------------------------------------------------------------------ 2018 A12 (참고 해설 비교용)
def sigma_ring(m, p, sp3, cx=0, cy=0):
    """σ 착물: sp3 탄소 = p{sp3}, + 는 p0(치환기 탄소)에 놓이는 공명 구조"""
    m.ring(p, cx, cy, 6, L, 90, bonds=False)
    dbl = {3: [(1, 2), (4, 5)], 1: [(2, 3), (4, 5)]}[sp3]
    for i in range(6):
        j = (i + 1) % 6
        k = "in" if (i, j) in dbl else 1
        m.bond(f"{p}{i}", f"{p}{j}", k, (cx, cy) if k == "in" else None)
    return m


def f12_2018a12_sigma():
    f = Fig(800, 250)
    f.text(20, 18, "t-Bu 벤젠 나이트로화의 속도 결정 단계(첨가, 흡열) — σ 착물 비교 (+는 t-Bu가 붙은 3차 탄소에 놓일 수 있음)", size=12, anchor="start", weight="bold")
    m = sigma_ring(Mol(), "a", 3)
    m.sub("t", "a0", 90, "C(CH_3)_3")
    m.sub("h", "a3", -130, "H")
    m.sub("n", "a3", -50, "NO_2")
    f.mol(m, 120, 120)
    f.charge(120, 120 - L + 14, "+")
    f.text(120, 205, "para 공격 σ 착물", size=11.5, weight="bold")
    f.text(120, 223, "입체 반발 작음 → 더 안정, 빠름 → A (주)", size=11, color=GREEN)
    m = sigma_ring(Mol(), "b", 1)
    m.sub("t", "b0", 90, "C(CH_3)_3")
    m.sub("n", "b1", 50, "NO_2")
    m.sub("h", "b1", -10, "H")
    f.mol(m, 400, 120)
    f.charge(400, 120 - L + 14, "+")
    f.text(400 + 30, 60, ")(", size=15, color=RED, weight="bold")
    f.text(400, 205, "ortho 공격 σ 착물", size=11.5, weight="bold")
    f.text(400, 223, "NO₂ ↔ t-Bu 입체 반발 → 덜 안정, 느림 → B (부)", size=11, color=RED)
    f.box(560, 60, 225, 120, fill="#f7f9fc")
    f.text(570, 80, "에너지 관점 (Hammond)", size=11.5, anchor="start", weight="bold")
    f.text(570, 102, "1단계 첨가: rds, 흡열", size=11, anchor="start")
    f.text(570, 120, "→ TS ≈ σ 착물", size=11, anchor="start")
    f.text(570, 138, "2단계 −H⁺: 빠름, 발열", size=11, anchor="start")
    f.text(570, 156, "(방향족성 회복)", size=11, anchor="start")
    return f.render()
