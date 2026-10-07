"""18 고리형 협동반응 · 19 C–C 결합형성반응 문항 그림"""
import math
from chemsvg import Mol, Fig, benzene, L, RED, BLUE, INK

GREEN = "#2f7d5b"
ORANGE = "#d97706"


def orbital_row(f, x0, y0, phases, dx=34, term_hl=True, label=None, nodes=True):
    """p 오비탈 사슬. phases: +1/−1 목록 (+1 = 위 로브 채움)."""
    n = len(phases)
    f.raw(f'<line x1="{x0 - 8}" y1="{y0}" x2="{x0 + (n - 1) * dx + 8}" y2="{y0}" stroke="{INK}" stroke-width="1.6"/>')
    for i, ph in enumerate(phases):
        f.porb(x0 + i * dx, y0, ph, rx=8, ry=15)
    if nodes:
        for i in range(n - 1):
            if phases[i] != phases[i + 1]:
                xm = x0 + i * dx + dx / 2
                f.raw(f'<line x1="{xm}" y1="{y0 - 30}" x2="{xm}" y2="{y0 + 30}" stroke="#9aa3ad" stroke-dasharray="3 3"/>')
    if term_hl:
        for i in (0, n - 1):
            x = x0 + i * dx
            f.raw(f'<rect x="{x - 13}" y="{y0 - 36}" width="26" height="72" rx="6" fill="none" stroke="{RED}" stroke-width="1.4"/>')
    if label:
        f.text(x0 - 22, y0, label, size=13, anchor="end", weight="bold")


def rot_pair(f, x1, x2, y, con=True):
    """두 말단의 회전 방향 기호"""
    f.rotarrow(x1, y, cw=True, r=10)
    f.rotarrow(x2, y, cw=con, r=10)


# ------------------------------------------------------------------ 2013 #39 (가) octatriene
def triene_U(m, p, cx, cy, closed=False, me=("w", "h")):
    """C2..C7를 육각형 꼭짓점에 배치 (오른쪽 변이 열린/닫힌 고리). 메틸은 C2(r1), C7(r2)."""
    m.ring(p, cx, cy, 6, L, 90, bonds=False)
    r = [f"{p}{i}" for i in range(6)]
    # r1=C2, r0=C3, r5=C4, r4=C5, r3=C6, r2=C7
    if not closed:
        m.bond(r[1], r[0], "in", (cx, cy))
        m.bond(r[0], r[5])
        m.bond(r[5], r[4], "in", (cx, cy))
        m.bond(r[4], r[3])
        m.bond(r[3], r[2], "in", (cx, cy))
        m.sub(p + "m1", r[1], 30)
        m.sub(p + "m2", r[2], -30)
    else:
        m.bond(r[1], r[0])
        m.bond(r[0], r[5], "in", (cx, cy))
        m.bond(r[5], r[4])
        m.bond(r[4], r[3], "in", (cx, cy))
        m.bond(r[3], r[2])
        m.bond(r[2], r[1])
        m.sub(p + "m1", r[1], 30, kind=me[0])
        m.sub(p + "m2", r[2], -30, kind=me[1])
    return r


def f2013_39a():
    f = Fig(800, 330)
    f.text(20, 20, "헥사트라이엔(6π)의 π 분자 궤도 — 말단(C2·C7) 로브의 위상", size=13, anchor="start", weight="bold")
    # ψ3 (바닥 상태 HOMO)
    orbital_row(f, 150, 85, [1, 1, -1, -1, 1, 1], label="ψ₃")
    f.text(360, 70, "바닥 상태 HOMO (열 반응)", size=12, anchor="start")
    f.text(360, 92, "말단 위상 같음 → 반대 회전(disrotatory)", size=12, anchor="start")
    rot_pair(f, 150, 320, 125, con=False)
    orbital_row(f, 150, 200, [1, -1, -1, 1, 1, -1], label="ψ₄*")
    f.text(360, 185, "들뜬 상태 HOMO (광반응: ψ₃ → ψ₄* 전자 승위)", size=12, anchor="start", color=RED)
    f.text(360, 207, "말단 위상 반대 → 같은 방향 회전(conrotatory)", size=12, anchor="start", color=RED, weight="bold")
    rot_pair(f, 150, 320, 240, con=True)
    f.text(20, 282, "Woodward–Hoffmann (전자 고리화): 4n+2 π(6π) → 열: dis / 빛: con,   4n π(4π) → 열: con / 빛: dis", size=12, anchor="start")
    f.text(20, 305, "(2E,4Z,6E) 기질: 열(dis) → cis-5,6-dimethyl,   빛(con) → trans-5,6-dimethylcyclohexa-1,3-diene", size=12, anchor="start", weight="bold")
    return f.render()


def f2013_39a_rxn():
    f = Fig(800, 170)
    m = Mol()
    triene_U(m, "t", 0, 0)
    f.mol(m, 110, 85)
    f.cap(110, 150, "(2E,4Z,6E)-octatriene")
    f.arrow(210, 70, 330, 70, "hν", "conrotatory")
    f.rotarrow(250, 110, cw=True)
    f.rotarrow(290, 110, cw=True)
    m = Mol()
    triene_U(m, "p", 0, 0, closed=True, me=("w", "h"))
    f.mol(m, 400, 85)
    f.cap(420, 150, "trans (광반응 생성물) ✓", color=GREEN)
    f.arrow(210, 30, 330, 30, "", "", color="#9aa3ad", kind="dash")
    f.text(270, 18, "Δ (dis)이면", size=11, color="#5b6270")
    m = Mol()
    triene_U(m, "q", 0, 0, closed=True, me=("w", "w"))
    f.mol(m, 640, 85)
    f.cap(660, 150, "cis (열 반응 생성물)", color="#5b6270")
    return f.render()


# ------------------------------------------------------------------ 2013 #39 (나) 보기
def allyl(m, p, frm, ang0):
    a = m.sub(p + "1", frm, ang0)
    b = m.sub(p + "2", a, ang0 - 60 if ang0 > 0 else ang0 + 60)
    m.sub(p + "3", b, ang0, kind="2")
    return a


def f2013_39b_g():
    """ㄱ: ortho가 막힌 알릴 아릴 에터 → Claisen → Cope → para"""
    f = Fig(800, 250)
    # 출발 물질
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    o = m.sub("o", "r0", 90, "O")
    a = m.sub("a1", o, 30)
    b = m.sub("a2", a, 90)
    m.sub("a3", b, 30, kind="2")
    m.sub("m1", "r1", 30, "OMe", anchor="start")
    m.sub("m2", "r5", 150, "MeO", anchor="end")
    f.mol(m, 75, 135)
    f.arrow(150, 118, 205, 118, "[3,3]", "Claisen")
    # ortho 다이엔온
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90, bonds=False)
    for x, y, k in [("r0", "r1", 1), ("r1", "r2", 1), ("r2", "r3", "in"), ("r3", "r4", 1), ("r4", "r5", "in"), ("r5", "r0", 1)]:
        m.bond(x, y, k, (0, 0) if k == "in" else None)
    m.sub("o", "r0", 90, "O", kind="2")
    m.sub("om", "r1", -10, "OMe", anchor="start")
    a = m.sub("a1", "r1", 70)
    b = m.sub("a2", a, 10)
    m.sub("a3", b, 70, kind="2")
    m.sub("m2", "r5", 150, "MeO", anchor="end")
    f.mol(m, 285, 135)
    f.text(285, 205, "ortho 다이엔온", size=11.5)
    f.text(285, 220, "(사차 C → 방향족화 불가)", size=10.5, color=RED)
    f.arrow(350, 118, 400, 118, "[3,3]", "Cope")
    # para 다이엔온
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90, bonds=False)
    for x, y, k in [("r0", "r1", 1), ("r1", "r2", "in"), ("r2", "r3", 1), ("r3", "r4", 1), ("r4", "r5", "in"), ("r5", "r0", 1)]:
        m.bond(x, y, k, (0, 0) if k == "in" else None)
    m.sub("o", "r0", 90, "O", kind="2")
    m.sub("om", "r1", 30, "OMe", anchor="start")
    m.sub("m2", "r5", 150, "MeO", anchor="end")
    m.sub("h", "r3", -150, "H")
    a = m.sub("a1", "r3", -30)
    b = m.sub("a2", a, 30)
    m.sub("a3", b, -30, kind="2")
    f.mol(m, 470, 120)
    f.text(470, 215, "para 다이엔온", size=11.5)
    f.arrow(555, 118, 605, 118, "토토머화", "")
    # 생성물
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    m.sub("o", "r0", 90, "OH")
    m.sub("m1", "r1", 30, "OMe", anchor="start")
    m.sub("m2", "r5", 150, "MeO", anchor="end")
    a = m.sub("a1", "r3", -90)
    b = m.sub("a2", a, -30)
    m.sub("a3", b, -90, kind="2")
    f.mol(m, 690, 115)
    f.text(770, 232, "ㄱ ○", size=14, color=GREEN, weight="bold")
    return f.render()


def fused(m, p, x0, y0, reactant):
    """ㄴ: 사이클로헥센 고리(왼쪽) + 트라이엔/새 고리(오른쪽)"""
    m.ring(p + "L", x0, y0, 6, L, 90)
    cx = x0 + 2 * L * math.cos(math.radians(30))
    m.ring(p + "R", cx, y0, 6, L, 90, bonds=False)
    # 공유 변: L1=R5, L2=R4 → 같은 좌표이므로 R5, R4 대신 L1, L2 사용
    R = {0: p + "R0", 1: p + "R1", 2: p + "R2", 3: p + "R3", 4: p + "L2", 5: p + "L1"}
    c = (cx, y0)
    if reactant:
        m.set_bond(p + "L1", p + "L2", "in", (x0, y0))
        m.bond(R[5], R[0])
        m.bond(R[0], R[1], "in", c)
        m.bond(R[4], R[3])
        m.bond(R[3], R[2], "in", c)
    else:
        m.bond(R[5], R[0], "in", c)
        m.bond(R[0], R[1])
        m.bond(R[1], R[2])
        m.bond(R[2], R[3])
        m.bond(R[3], R[4], "in", c)
    return R


def f2013_39b_n():
    f = Fig(800, 190)
    m = Mol()
    R = fused(m, "a", 0, 0, True)
    m.sub("p1", R[1], 30, "Ph", anchor="start")
    m.sub("p2", R[2], -30, "Ph", anchor="start")
    f.mol(m, 60, 95)
    f.cap(95, 170, "(E,Z,E)-트라이엔 (6π)")
    f.arrow(200, 95, 300, 95, "Δ (열)", "disrotatory")
    f.rotarrow(235, 135, cw=True)
    f.rotarrow(265, 135, cw=False)
    m = Mol()
    R = fused(m, "b", 0, 0, False)
    m.sub("p1", R[1], 30, "Ph", anchor="start", kind="w")
    m.sub("p2", R[2], -30, "Ph", anchor="start", kind="w")
    f.mol(m, 360, 95)
    f.cap(400, 170, "올바른 생성물: cis ✓", color=GREEN)
    m = Mol()
    R = fused(m, "c", 0, 0, False)
    m.sub("p1", R[1], 30, "Ph", anchor="start", kind="w")
    m.sub("p2", R[2], -30, "Ph", anchor="start", kind="h")
    f.mol(m, 590, 95)
    f.cap(630, 170, "보기의 trans → ㄴ ✗", color=RED)
    return f.render()


def norbornene(m, p, x, y, subs):
    """norbornene 투시도. C5=C6(뒤, 이중결합), C2–C3(앞 아래). subs: {'2': ('endo'|'exo', builder)}"""
    P = {1: (0, 8), 2: (16, 32), 3: (50, 32), 4: (66, 8), 5: (50, -4), 6: (16, -4), 7: (33, -30)}
    for k, (a, b) in P.items():
        m.atom(f"{p}{k}", x + a, y + b)
    for a, b, k in [(1, 2, 1), (2, 3, 1), (3, 4, 1), (4, 5, 1), (5, 6, "2"), (6, 1, 1), (1, 7, 1), (7, 4, 1)]:
        m.bond(f"{p}{a}", f"{p}{b}", k)
    return {k: f"{p}{k}" for k in P}


def f2013_39b_d():
    f = Fig(800, 200)
    m = Mol()
    m.ring("c", 0, 0, 5, L * 0.95, 90, arom=[1, 3])
    f.mol(m, 60, 100)
    f.text(110, 100, "+", size=18)
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, -30, kind="2l")
    c = m.sub("c", a, 90)
    m.sub("o", c, 150, "O", kind="2")
    m.sub("me", c, 30)
    f.mol(m, 140, 110)
    f.arrow(200, 100, 280, 100, "Δ", "endo 규칙")
    # endo 생성물
    m = Mol()
    N = norbornene(m, "n", 0, 0, {})
    c = m.sub("ac", N[2], -90)
    m.sub("o", c, -150, "O", kind="2")
    m.sub("me", c, -30)
    m.sub("h", N[2], 200, "H", length=22)
    f.mol(m, 320, 70)
    f.cap(355, 185, "endo (주생성물) ✓", color=GREEN)
    # exo (보기)
    m = Mol()
    N = norbornene(m, "x", 0, 0, {})
    c = m.sub("ac", N[2], 200, length=30)
    m.sub("o", c, 260, "O", kind="2")
    m.sub("me", c, 150)
    m.sub("h", N[2], -90, "H", length=22)
    f.mol(m, 520, 70)
    f.cap(560, 185, "보기의 구조 = exo → ㄷ ✗", color=RED)
    f.text(660, 50, "C7 다리의 반대쪽(C=C 쪽,", size=11, anchor="start")
    f.text(660, 66, "그림의 아래) = endo", size=11, anchor="start")
    return f.render()


# ------------------------------------------------------------------ 2005 #14
def cyclobutene(m, p, x, y, me=("w", "w")):
    m.atom(p + "1", x, y)
    m.atom(p + "2", x, y + 32)
    m.atom(p + "4", x + 32, y + 32)
    m.atom(p + "3", x + 32, y)
    m.bond(p + "1", p + "2", "2r")
    m.bond(p + "2", p + "4")
    m.bond(p + "4", p + "3")
    m.bond(p + "3", p + "1")
    m.sub(p + "m3", p + "3", 45, "CH_3", anchor="start", kind=me[0])
    m.sub(p + "m4", p + "4", -45, "CH_3", anchor="start", kind=me[1])


def diene(m, p, x, y, e1=True, e2=True):
    """s-cis 헥사다이엔: 육각형 왼쪽 네 꼭짓점 (C2=r0, C3=r5, C4=r4, C5=r3)"""
    m.ring(p, x, y, 6, L, 90, bonds=False)
    m.bond(p + "0", p + "5", "in", (x, y))
    m.bond(p + "5", p + "4")
    m.bond(p + "4", p + "3", "in", (x, y))
    m.sub(p + "m1", p + "0", 90 if e1 else -30, "CH_3" if e1 else "CH_3", anchor="middle" if e1 else "start")
    m.sub(p + "m2", p + "3", -90 if e2 else 30, "CH_3", anchor="middle" if e2 else "start")


def f2005_14():
    f = Fig(800, 540)
    f.text(20, 20, "뷰타다이엔(4π)의 π 분자 궤도", size=13, anchor="start", weight="bold")
    orbital_row(f, 110, 80, [1, 1, -1, -1], dx=38, label="ψ₂")
    f.text(260, 66, "바닥 상태 HOMO (열): 말단 위상 반대", size=12, anchor="start")
    f.text(260, 88, "→ 같은 방향 회전(conrotatory)", size=12, anchor="start", weight="bold")
    rot_pair(f, 110, 224, 120, con=True)
    orbital_row(f, 110, 185, [1, -1, -1, 1], dx=38, label="ψ₃*")
    f.text(260, 171, "들뜬 상태 HOMO (hν: ψ₂ → ψ₃*): 말단 위상 같음", size=12, anchor="start", color=RED)
    f.text(260, 193, "→ 반대 방향 회전(disrotatory)", size=12, anchor="start", color=RED, weight="bold")
    rot_pair(f, 110, 224, 225, con=False)
    # 열 반응
    f.text(250, 262, "열 반응 (175 ℃)", size=12.5, anchor="start", weight="bold")
    m = Mol()
    cyclobutene(m, "a", 0, 0)
    f.mol(m, 60, 290)
    f.cap(90, 360, "cis-3,4-dimethylcyclobutene")
    f.arrow(190, 305, 300, 305, "Δ, conrotatory", "(허용)")
    m = Mol()
    diene(m, "d", 0, 0, e1=True, e2=False)
    f.mol(m, 360, 310)
    f.cap(365, 375, "(2E,4Z) ✓")
    f.text(470, 290, "dis로 열리면 (2E,4E) 또는 (2Z,4Z)", size=11.5, anchor="start", color=RED)
    f.text(470, 308, "→ 열적으로 대칭 금지이므로 생성 ✗", size=11.5, anchor="start", color=RED)
    # 광반응
    f.text(250, 400, "광반응", size=12.5, anchor="start", weight="bold")
    m = Mol()
    diene(m, "e", 0, 0, e1=True, e2=True)
    f.mol(m, 110, 450)
    f.cap(110, 525, "(2E,4E)-hexadiene")
    f.arrow(190, 450, 300, 450, "hν", "disrotatory")
    m = Mol()
    cyclobutene(m, "b", 0, 0)
    f.mol(m, 345, 434)
    f.cap(375, 505, "cis만 생성 ✓")
    f.text(470, 440, "con이어야 trans가 되므로 광반응에서는 trans ✗", size=11.5, anchor="start", color=RED)
    f.text(470, 458, "(다이엔만 빛을 흡수 → 고리화 쪽으로 광정류 상태)", size=11, anchor="start", color="#5b6270")
    return f.render()


# ------------------------------------------------------------------ 2011 #4
def f2011_4_grignard():
    f = Fig(800, 200)
    m = Mol()
    benzene(m, "r", 0, 0, 0)
    m.atom("mg", 62, 0, "MgBr", anchor="start")
    m.bond("r0", "mg", 1)
    f.mol(m, 50, 80)
    f.curly(98, 78, 175, 70, bend=-0.35)
    f.text(150, 118, "δ−  (탄소 친핵체)", size=11, color=RED)
    m = Mol()
    a = m.atom("c1", 0, 0)
    c = m.sub("c2", a, 0, "C")
    m.sub("n", c, 0, "N", kind=3)
    f.mol(m, 170, 80)
    f.text(193, 60, "δ+", size=11, color=BLUE)
    f.curly(214, 75, 231, 70, bend=-1.0)
    f.arrow(260, 80, 320, 80, "", "")
    # 이민 음이온 염
    m = Mol()
    benzene(m, "r", 0, 0, 0)
    c = m.sub("c", "r0", 0)
    m.sub("me", c, 90)
    m.sub("n", c, -30, "N", kind="2")
    m.sub("mg", "n", 30, "MgBr", anchor="start")
    f.mol(m, 360, 90)
    f.text(420, 150, "이민 마그네슘 염 (안정: 두 번째 첨가 없음)", size=11)
    f.arrow(505, 80, 575, 80, "H₃O^+", "이민 가수분해")
    m = Mol()
    benzene(m, "r", 0, 0, 0)
    c = m.sub("c", "r0", 0)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("me", c, -30)
    f.mol(m, 625, 90)
    f.cap(660, 160, "A: acetophenone")
    return f.render()


def f2011_4_da():
    f = Fig(800, 300)
    f.text(20, 20, "FMO: 다이엔 HOMO(ψ₂) – 친다이엔체 LUMO(π*)", size=13, anchor="start", weight="bold")
    xs = [90, 140, 190, 240]
    f.text(20, 80, "HOMO", size=11.5, anchor="start")
    f.raw(f'<line x1="{xs[0]}" y1="80" x2="{xs[3]}" y2="80" stroke="{INK}" stroke-width="1.6"/>')
    for x, ph in zip(xs, [1, 1, -1, -1]):
        f.porb(x, 80, ph, rx=8, ry=15)
    yb = 190
    f.text(20, yb, "LUMO", size=11.5, anchor="start")
    f.raw(f'<line x1="{xs[0]}" y1="{yb}" x2="{xs[3]}" y2="{yb}" stroke="{INK}" stroke-width="1.6"/>')
    f.porb(xs[0], yb, -1, rx=8, ry=15)
    f.porb(xs[3], yb, 1, rx=8, ry=15)
    # 카보닐 탄소 (2차 궤도)
    for x, ph, xa in ((xs[1], -1, xs[0]), (xs[2], 1, xs[3])):
        f.raw(f'<line x1="{xa}" y1="{yb}" x2="{x}" y2="{yb + 40}" stroke="{INK}" stroke-width="1.4"/>')
        f.porb(x, yb + 40, ph, rx=6, ry=11)
    f.text(165, yb + 72, "C=O 탄소 (π* 계수)", size=10.5)
    for x in (xs[0], xs[3]):
        f.raw(f'<line x1="{x}" y1="100" x2="{x}" y2="{yb - 20}" stroke="{GREEN}" stroke-width="2" stroke-dasharray="5 3"/>')
    for x in (xs[1], xs[2]):
        f.raw(f'<line x1="{x}" y1="100" x2="{x}" y2="{yb + 25}" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="2 3"/>')
    f.text(290, 60, "초록: 1차 궤도 겹침 (C1·C4 ↔ 친다이엔체 C)", size=11.5, anchor="start", color=GREEN)
    f.text(290, 78, "  위상 일치 → 결합 형성, 열적 허용 [π4s + π2s]", size=11.5, anchor="start", color=GREEN)
    f.text(290, 100, "주황: 2차 궤도 상호작용 (C2·C3 ↔ C=O 탄소)", size=11.5, anchor="start", color=ORANGE)
    f.text(290, 118, "  endo 전이 상태에서만 가능 → endo 주생성물", size=11.5, anchor="start", color=ORANGE)
    # 생성물
    f.text(440, 200, "25 ℃ →", size=12)
    m = Mol()
    N = norbornene(m, "n", 0, 0, {})
    c2 = m.sub("k2", N[2], -100, length=30)
    c3 = m.sub("k3", N[3], -80, length=30)
    m.atom("ob", 33 , 32 + 30 * math.sin(math.radians(100)) + 17, "O")
    m.bond(c2, "ob")
    m.bond(c3, "ob")
    m.sub("o2", c2, -160, "O", kind="2")
    m.sub("o3", c3, -20, "O", kind="2")
    m.sub("h2", N[2], 160, "H", length=20)
    m.sub("h3", N[3], 20, "H", length=20)
    f.mol(m, 530, 175)
    f.cap(620, 280, "B: endo 부가물 (endo-무수물)")
    return f.render()


def f2011_4_heck():
    f = Fig(800, 360)
    cx, cy, r = 250, 185, 120
    def arc(a1, a2, lab, lx, ly, anchor="start"):
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
        x2, y2 = cx + r * math.cos(math.radians(a2)), cy - r * math.sin(math.radians(a2))
        f.raw(f'<path d="M{x1:.1f},{y1:.1f} A{r},{r} 0 0 1 {x2:.1f},{y2:.1f}" fill="none" stroke="{BLUE}" stroke-width="1.8" marker-end="url(#{f.id}b)"/>')
        for i, t in enumerate(lab):
            f.text(lx, ly + i * 16, t, size=11.5, anchor=anchor, color=BLUE if i == 0 else INK, weight="bold" if i == 0 else "normal")

    arc(75, 15, ["① 산화성 첨가", "+ Ph–I (C–I 절단)"], cx + 95, cy - 118)
    arc(-15, -75, ["② 알켄 배위 · syn 삽입", "+ PhCH=CH₂ → 새 C–C 결합", "(Ph는 치환이 적은 말단 C로)"], cx + 100, cy + 88)
    arc(-105, -165, ["③ syn β-H 제거", "→ (E)-stilbene 방출"], cx - 225, cy + 95)
    arc(165, 105, ["④ 환원성 제거 (염기)", "K₂CO₃: HI 제거", "→ Pd(0) 재생"], cx - 240, cy - 125)
    nodes = {
        "top": (cx, cy - r, "Pd(0)L_2"),
        "right": (cx + r + 20, cy, "Ph–Pd(II)L_2–I"),
        "bottom": (cx, cy + r, "PhCH_2–CH(Ph)–PdL_2I"),
        "left": (cx - r - 10, cy, "H–Pd(II)L_2–I"),
    }
    for k, (x, y, t) in nodes.items():
        w = 12 + 7.2 * len(t.replace("_", ""))
        f.box(x - w / 2, y - 14, w, 28, fill="#fff", stroke="#9aa3ad", r=6)
        f.text(x, y, t, size=12, weight="bold")

    # 생성물 stilbene
    m = Mol()
    benzene(m, "r", 0, 0, 0)
    a = m.sub("a", "r0", -30)
    b = m.sub("b", a, 30, kind="2")
    m.ring("s", m.pos(b)[0] + 2 * L * math.cos(math.radians(-30)), m.pos(b)[1] + 2 * L * math.sin(math.radians(30)), 6, L, 150, arom=[0, 2, 4])
    m.bond(b, "s0")
    f.mol(m, 560, 150, scale=0.9)
    f.cap(655, 245, "C: (E)-stilbene (trans)")
    f.text(655, 265, "β-H 제거가 syn으로, 두 Ph가 멀어지는", size=11)
    f.text(655, 281, "형태에서 일어나 E 이성질체가 주생성물", size=11)
    return f.render()


if __name__ == "__main__":
    import sys
    from preview import shot
    shot([f2013_39a(), f2013_39a_rxn(), f2013_39b_g(), f2013_39b_n(), f2013_39b_d(), f2005_14(),
          f2011_4_grignard(), f2011_4_da(), f2011_4_heck()], sys.argv[1])
