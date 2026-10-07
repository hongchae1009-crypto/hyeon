"""17 아민 · 유기화학실험 문항 그림"""
import math
from chemsvg import Mol, Fig, benzene, phenyl_at, L, RED, BLUE, INK


def nme2(m, p, attach, ang=0, l1=150, l2=-150):
    """attach에서 ang 방향 N(CH3)2 — 메틸은 골격선으로"""
    n = m.sub(p + "N", attach, ang, "N")
    m.sub(p + "m1", n, ang + 60)
    m.sub(p + "m2", n, ang - 60)
    return n


# ------------------------------------------------------------------ 2011 #36
def f2011_36_scheme():
    f = Fig(800, 300)
    # A: benzenediazonium
    m = Mol()
    benzene(m, "a", 0, 0, start=0)
    n1 = m.sub("n1", "a0", 0, "N^+")
    m.sub("n2", n1, 0, "N", kind=3)
    f.mol(m, 50, 80)
    f.text(155, 58, "Cl^−", size=12)
    f.cap(95, 128, "A")
    f.text(170, 80, "+", size=18)
    # B
    m = Mol()
    benzene(m, "b", 0, 0, start=0)
    nme2(m, "b", "b0")
    f.mol(m, 225, 80)
    f.cap(250, 128, "B")
    f.arrow(318, 80, 385, 80, "짝지음", "(para 공격)")
    # C
    m = Mol()
    benzene(m, "c", 0, 0, start=0)
    x = m.sub("x1", "c0", 0, "N")
    y = m.sub("x2", x, 0, "N", kind="2")
    r = m.ring("d", m.pos(y)[0] + 60, 0, 6, L, 180, arom=[0, 2, 4])
    m.bond(y, "d0")
    nme2(m, "d", "d3")
    f.mol(m, 425, 80)
    f.cap(560, 128, "C (아조 화합물, 주황색)")
    # 두 번째 줄: A + D ✗
    m = Mol()
    benzene(m, "a", 0, 0, start=0)
    n1 = m.sub("n1", "a0", 0, "N^+")
    m.sub("n2", n1, 0, "N", kind=3)
    f.mol(m, 50, 225)
    f.text(155, 203, "Cl^−", size=12)
    f.text(170, 225, "+", size=18)
    m = Mol()
    benzene(m, "e", 0, 0, start=0)
    nme2(m, "e", "e0")
    m.sub("o1", "e5", 60)
    m.sub("o2", "e1", -60)
    f.mol(m, 225, 225)
    f.cap(250, 283, "D")
    f.arrow(318, 225, 385, 225, "", "")
    f.cross(351, 225)
    f.text(560, 215, "반응하지 않음 (E 생성 ✗)", size=13, color=RED, weight="bold")
    f.text(560, 240, "o-CH₃ ↔ N-CH₃ 입체 반발 → 공명 억제", size=12)
    return f.render()


def f2011_36_resonance():
    """B의 공명: N 비공유쌍 → para 탄소 전자 밀도 ↑, 그리고 짝지음 공격"""
    f = Fig(800, 250)
    # 구조 1
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90, arom=[0, 2, 4])
    n = m.sub("n", "r0", 90, "N")
    m.sub("m1", n, 150)
    m.sub("m2", n, 30)
    f.mol(m, 90, 130)
    f.lp(90, 130 - 60 - 10, 90)   # 대략 N 위
    # 굽은 화살표: N lp → N–C,  C=C → 옆,  C=C → para
    f.curly(84, 58, 84, 86, bend=0.7)
    f.curly(106, 104, 123, 128, bend=-0.7)
    f.curly(106, 156, 92, 170, bend=-0.7)
    f.resarrow(160, 215, 130)
    # 구조 2 (퀴노이드)
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90, bonds=False)
    for a, b, k in [("r0", "r1", 1), ("r1", "r2", "in"), ("r2", "r3", 1), ("r3", "r4", 1), ("r4", "r5", "in"), ("r5", "r0", 1)]:
        m.bond(a, b, k, (0, 0) if k == "in" else None)
    n = m.sub("n", "r0", 90, "N^+", kind="2")
    m.sub("m1", n, 150)
    m.sub("m2", n, 30)
    f.mol(m, 285, 130)
    f.charge(285, 172, "−")
    f.text(285, 205, "para 탄소에 음전하 → 강한 친핵체", size=12)
    # 오른쪽: 궤도 정렬 모식도
    f.box(430, 12, 360, 226, fill="#f7f9fc")
    f.text(610, 30, "N 비공유쌍(p)과 고리 π계의 겹침", size=12.5, weight="bold")

    def edge(x0, y0, twisted, title):
        # 고리를 옆에서 본 모습: 탄소 4개 + N
        for i in range(4):
            cx = x0 + i * 26
            f.porb(cx, y0, 1, rx=6, ry=12)
        f.raw(f'<line x1="{x0 - 6}" y1="{y0}" x2="{x0 + 3 * 26 + 6}" y2="{y0}" stroke="{INK}" stroke-width="2"/>')
        nx = x0 + 3 * 26 + 34
        f.raw(f'<line x1="{x0 + 3 * 26}" y1="{y0}" x2="{nx}" y2="{y0}" stroke="{INK}" stroke-width="1.6"/>')
        f.raw(f'<circle cx="{nx}" cy="{y0}" r="4" fill="{INK}"/>')
        f.text(nx + 10, y0 + 12, "N", size=12, anchor="start")
        if twisted:
            f.raw(f'<ellipse cx="{nx + 14}" cy="{y0}" rx="13" ry="6" fill="#f0c36d" stroke="{INK}"/>')
            f.raw(f'<ellipse cx="{nx - 14}" cy="{y0}" rx="13" ry="6" fill="#fff" stroke="{INK}"/>')
        else:
            f.raw(f'<ellipse cx="{nx}" cy="{y0 - 13}" rx="6" ry="13" fill="#f0c36d" stroke="{INK}"/>')
            f.raw(f'<ellipse cx="{nx}" cy="{y0 + 13}" rx="6" ry="13" fill="#fff" stroke="{INK}"/>')
        f.text(x0 + 55, y0 + 38, title, size=11.5)

    edge(460, 90, False, "B: 평행 → 공명 ○")
    edge(460, 180, True, "D: 수직(≈90° 비틀림) → 공명 ✗")
    f.text(745, 90, "✓", size=20, color="#2f7d5b", weight="bold")
    f.text(745, 180, "✗", size=20, color=RED, weight="bold")
    return f.render()


# ------------------------------------------------------------------ 2010 #39
def f2010_39():
    f = Fig(800, 330)
    # 벤조산
    m = Mol()
    benzene(m, "r", 0, 0, start=90)
    c = m.sub("c", "r1", 30)
    m.sub("o1", c, 90, "O", kind="2")
    m.sub("o2", c, -30, "OH")
    f.mol(m, 45, 90)
    f.cap(85, 150, "벤조산 (6.0 mmol)")
    f.arrow(150, 90, 225, 90, "CH₃Li (1당량)", "산–염기 (빠름)")
    # 카복실레이트
    m = Mol()
    benzene(m, "r", 0, 0, start=90)
    c = m.sub("c", "r1", 30)
    m.sub("o1", c, 90, "O", kind="2")
    m.sub("o2", c, -30, "O^−")
    f.mol(m, 265, 90)
    f.text(355, 118, "Li^+", size=12)
    f.text(300, 150, "+ CH₄↑", size=12)
    f.arrow(370, 90, 445, 90, "CH₃Li (2번째)", "친핵성 첨가")
    # 이음이온 사면체
    m = Mol()
    benzene(m, "r", 0, 0, start=90)
    c = m.sub("c", "r1", 30)
    m.sub("o1", c, 90, "O^−")
    m.sub("o2", c, -30, "O^−")
    m.sub("me", c, 30)
    f.mol(m, 490, 90)
    f.text(590, 128, "2 Li^+", size=12)
    f.text(530, 150, "이음이온 사면체 중간체", size=12)
    f.text(530, 166, "(안정, 붕괴하지 않음)", size=11, color="#5b6270")
    f.arrow(610, 90, 680, 90, "H₃O^+", "")
    f.text(645, 118, "수화물 → −H₂O", size=10.5)
    m = Mol()
    benzene(m, "r", 0, 0, start=90)
    c = m.sub("c", "r1", 30)
    m.sub("o1", c, 90, "O", kind="2")
    m.sub("me", c, -30)
    f.mol(m, 720, 90)
    f.cap(740, 150, "A: acetophenone")
    # TLC 판
    f.box(40, 190, 740, 128, fill="#f7f9fc")
    f.text(60, 208, "TLC (정상 실리카 겔, 20% EtOAc/n-hexane)", size=12.5, anchor="start", weight="bold")
    x0, y0, w, h = 90, 222, 90, 86
    f.raw(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="#fff" stroke="{INK}"/>')
    f.raw(f'<line x1="{x0}" y1="{y0 + h - 12}" x2="{x0 + w}" y2="{y0 + h - 12}" stroke="#999" stroke-dasharray="3 2"/>')
    f.raw(f'<line x1="{x0}" y1="{y0 + 8}" x2="{x0 + w}" y2="{y0 + 8}" stroke="#999" stroke-dasharray="3 2"/>')
    f.raw(f'<ellipse cx="{x0 + 25}" cy="{y0 + h - 30}" rx="7" ry="5" fill="#1f5fbf"/>')
    f.raw(f'<ellipse cx="{x0 + 65}" cy="{y0 + 32}" rx="7" ry="5" fill="#c0392b"/>')
    f.text(x0 + 25, y0 + h - 4, "SM", size=10)
    f.text(x0 + 65, y0 + h - 4, "A", size=10)
    f.text(x0 + w + 12, y0 + 12, "용매 전선", size=10.5, anchor="start")
    f.text(x0 + w + 12, y0 + h - 12, "원점", size=10.5, anchor="start")
    f.text(310, 240, "• 벤조산: –COOH가 실리카 Si–OH와 강한 수소 결합 → 느리게 이동 (R_f 작음, 꼬리 끌림)", size=11.5, anchor="start")
    f.text(310, 262, "• acetophenone: 수소 결합 주개 없음, 극성 작음 → 빨리 이동 (R_f 큼)", size=11.5, anchor="start")
    f.text(310, 284, "∴ R_f(A) > R_f(벤조산)  →  ②의 “A가 더 작다”는 틀림", size=12, anchor="start", weight="bold", color=RED)
    return f.render()


# ------------------------------------------------------------------ 2009 #25
def enone(m, p, x0, y0, conf):
    """dibenzalacetone: 가운데 C=O, 양쪽 CH=CH–Ph. conf=(왼쪽, 오른쪽) E/Z"""
    c = m.atom(p + "c", x0, y0)
    m.sub(p + "o", c, 90, "O", kind="2")
    for sgn, cf in ((1, conf[1]), (-1, conf[0])):
        base = 0 if sgn > 0 else 180
        a = m.sub(p + f"a{sgn}", c, base - sgn * 30)
        b = m.sub(p + f"b{sgn}", a, base + sgn * 30, kind="2")
        ang = (base - sgn * 30) if cf == "E" else 90
        bx, by = m.pos(b)
        cx = bx + 2 * L * math.cos(math.radians(ang))
        cy = by - 2 * L * math.sin(math.radians(ang))
        m.ring(p + f"p{sgn}", cx, cy, 6, L, ang + 180, arom=[0, 2, 4])
        m.bond(b, p + f"p{sgn}0")
    return c


def f2009_25():
    f = Fig(800, 360)
    # 반응: 알돌 → 탈수 (한쪽), 다시 반복
    f.text(400, 20, "① 엔올레이트 생성 → ② 알돌 첨가 → ③ E1cB 탈수 (×2회)", size=13, weight="bold")

    for i, (conf, name) in enumerate(((("E", "E"), "(E,E)"), (("E", "Z"), "(E,Z) = (Z,E)"), (("Z", "Z"), "(Z,Z)"))):
        m = Mol()
        enone(m, "x", 0, 0, conf)
        x = [150, 420, 680][i]
        f.mol(m, x, 130, scale=0.78)
        f.cap(x, 205, name)
    f.text(400, 232, "C=C 2개가 대칭적으로 놓여 있으므로 (E,Z)와 (Z,E)는 같은 화합물 → 기하 이성질체는 3개 (4개 ✗)", size=12.5, color=RED, weight="bold")
    # 수득률 계산 상자
    f.box(40, 252, 720, 96, fill="#fff8e6", stroke="#f0c36d")
    f.text(60, 272, "수득률 계산", size=12.5, anchor="start", weight="bold")
    f.text(60, 294, "한계 반응물: acetone 0.025 mol (benzaldehyde 0.050 mol = 정확히 2당량)", size=12, anchor="start")
    f.text(60, 314, "이론 수득량 = 0.025 mol × 234 g/mol = 5.85 g", size=12, anchor="start")
    f.text(60, 334, "수득률 = 3.51 g ÷ 5.85 g × 100 = 60 %  (④ 옳음)", size=12, anchor="start", weight="bold")
    return f.render()


def _at(m, name, ox, oy, scale=1.0):
    x, y = m.pos(name)
    return ox + x * scale, oy + y * scale


def _mid(p, q, t=0.5):
    return p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t


# ------------------------------------------------------------------ 2011 #36 메커니즘
def f2011_36_mech():
    """아조 짝지음의 SEAr 메커니즘: B의 para 탄소 → A의 말단 N (rds), σ 착물, −H⁺"""
    f = Fig(800, 360)
    # ---- 1행: B + A (굽은 화살표) ----
    ox, oy = 150, 95
    m = Mol()
    benzene(m, "b", 0, 0, start=0)
    nme2(m, "b", "b3", ang=180)
    f.mol(m, ox, oy)
    P = lambda n: _at(m, n, ox, oy)
    N, b0, b1, b2, b3 = P("bN"), P("b0"), P("b1"), P("b2"), P("b3")
    f.cap(ox, oy + 58, "B (친핵체)")
    # N 비공유쌍 (위쪽)
    f.lp(N[0], N[1] - 11, 90)
    f.curly(N[0] + 3, N[1] - 14, *_mid(N, b3, 0.6), bend=-0.8)
    f.curly(*_mid(b3, b2, 0.45), *_mid(b2, b1, 0.5), bend=0.9)
    # A (말단 N이 왼쪽)
    ax, ay = 235, 95
    a = Mol()
    a.atom("nt", 0, 0, "N")
    a.sub("np", "nt", 0, "N^+", kind=3)
    phenyl_at(a, "p", "np", 0)
    f.mol(a, ax, ay)
    nt, npl = _at(a, "nt", ax, ay), _at(a, "np", ax, ay)
    f.text(npl[0] + 2, ay + 26, "Cl^−", size=11)
    f.cap(ax + 90, ay + 58, "A (약한 친전자체)")
    f.curly(*_mid(b1, b0, 0.5), nt[0] - 9, nt[1] + 4, bend=0.55)
    f.curly(nt[0] + 15, nt[1] - 6, npl[0] - 1, npl[1] - 10, bend=-0.9)
    f.arrow(430, 95, 520, 95, "첨가 (rds)", "흡열 · 느림")
    f.text(660, 70, "① para 탄소의 π 전자가 말단 N을 공격", size=11.5, anchor="middle")
    f.text(660, 90, "(N 비공유쌍이 고리를 통해 밀어 줌)", size=11.5, anchor="middle")
    f.text(660, 112, "② N≡N의 π 전자 한 쌍 → N⁺ 위로", size=11.5, anchor="middle")
    f.text(660, 132, "→ 방향족성이 깨진 σ 착물 (rds)", size=11.5, anchor="middle", color=RED)
    # ---- 2행: σ 착물 → −H⁺ → C ----
    ox, oy = 150, 255
    m = Mol()
    m.ring("s", 0, 0, 6, L, 0, bonds=False)
    for u, v, k in [("s0", "s1", 1), ("s1", "s2", "in"), ("s2", "s3", 1), ("s3", "s4", 1), ("s4", "s5", "in"), ("s5", "s0", 1)]:
        m.bond(u, v, k, (0, 0) if k == "in" else None)
    n = m.sub("sN", "s3", 180, "N^+", kind="2")
    m.sub("m1", n, 120)
    m.sub("m2", n, 240)
    m.sub("h", "s0", 90, "H", length=24)
    m.sub("na", "s0", -30, "N")
    m.sub("nb", "na", 30, "N", kind="2")
    phenyl_at(m, "q", "nb", -30)
    f.mol(m, ox, oy)
    P = lambda n: _at(m, n, ox, oy)
    s0, s1, s2, s3, H, sN, na = P("s0"), P("s1"), P("s2"), P("s3"), P("h"), P("sN"), P("na")
    f.cap(ox + 40, oy + 85, "σ 착물 (이미늄형, sp³ 탄소)")
    f.lp(na[0] + 1, na[1] + 11, -90)
    # 염기가 H⁺ 제거
    f.text(H[0] + 48, H[1] - 14, "H₂O", size=12)
    f.lp(H[0] + 33, H[1] - 14, 0)
    f.curly(H[0] + 30, H[1] - 10, H[0] + 8, H[1] - 2, bend=0.3)
    f.curly(*_mid(s0, H, 0.45), *_mid(s0, s1, 0.5), bend=0.9)
    f.curly(*_mid(s1, s2, 0.5), *_mid(s2, s3, 0.5), bend=0.9)
    f.curly(*_mid(s3, sN, 0.45), sN[0] + 2, sN[1] + 12, bend=0.9)
    f.arrow(345, 255, 420, 255, "−H⁺", "빠름 · 방향족성 회복")
    # C
    m = Mol()
    benzene(m, "c", 0, 0, start=0)
    x = m.sub("x1", "c0", 0, "N")
    y = m.sub("x2", x, 0, "N", kind="2")
    m.ring("d", m.pos(y)[0] + 60, 0, 6, L, 180, arom=[0, 2, 4])
    m.bond(y, "d0")
    nme2(m, "d", "d3")
    f.mol(m, 470, 255, scale=0.85)
    f.cap(600, 300, "C (para 아조 화합물)")
    f.box(20, 318, 760, 34, fill="#fff5f3", stroke="#e8b4ab")
    f.text(400, 335, "D: N(CH₃)₂가 고리 평면에서 비틀려 첫 번째 화살표(N 비공유쌍 → 고리)가 불가능 → σ 착물 형성(rds)이 매우 느림 → 반응 ✗",
           size=11.5, color=RED)
    return f.render()


# ------------------------------------------------------------------ 2010 #39 메커니즘
def f2010_39_mech():
    """RCOOH + 2 CH3Li: 산–염기 → 친핵성 첨가 → 이음이온 → H3O+ → gem-diol ⇌ 케톤"""
    f = Fig(800, 330)
    sc = 0.9
    # 벤조산 + CH3–Li
    ox, oy = 45, 105
    m = Mol()
    benzene(m, "r", 0, 0, start=90)
    c = m.sub("c", "r1", 30)
    m.sub("o1", c, 90, "O", kind="2")
    m.sub("o2", c, -30, "O")
    m.sub("h", "o2", 30, "H", length=26)
    f.mol(m, ox, oy, scale=sc)
    o2, h = _at(m, "o2", ox, oy, sc), _at(m, "h", ox, oy, sc)
    li = Mol()
    li.atom("c", 0, 0, "H_3C")
    li.sub("li", "c", 0, "Li", length=34)
    lx, ly = 175, 45
    f.mol(li, lx, ly)
    f.curly(lx + 21, ly + 3, h[0] + 5, h[1] - 9, bend=0.35)
    f.curly(*_mid(o2, h, 0.55), o2[0] + 2, o2[1] + 11, bend=0.9)
    f.text(130, 165, "① 산–염기 (빠름)", size=11.5, color=RED)
    f.arrow(230, 105, 285, 105, "", "−CH₄↑")
    # 카복실레이트 + CH3–Li
    ox, oy = 315, 105
    m = Mol()
    benzene(m, "r", 0, 0, start=90)
    c = m.sub("c", "r1", 30)
    m.sub("o1", c, 90, "O", kind="2")
    m.sub("o2", c, -30, "O^−")
    m.label("o2", "OLi")
    m.a["o2"][3] = "start"
    f.mol(m, ox, oy, scale=sc)
    cc, o1 = _at(m, "c", ox, oy, sc), _at(m, "o1", ox, oy, sc)
    lx, ly = 425, 40
    f.mol(li, lx, ly)
    f.curly(lx + 22, ly + 4, cc[0] + 5, cc[1] - 3, bend=0.4)
    f.curly(*_mid(cc, o1, 0.5), o1[0] - 9, o1[1] + 2, bend=0.9)
    f.text(395, 165, "② 친핵성 첨가 (CH₃⁻ → C=O)", size=11.5, color=RED)
    f.arrow(470, 105, 525, 105)
    # 이음이온 사면체
    ox, oy = 555, 115
    m = Mol()
    benzene(m, "r", 0, 0, start=90)
    c = m.sub("c", "r1", 30)
    m.sub("o1", c, 90, "OLi")
    m.sub("o2", c, -30, "OLi", anchor="start")
    m.sub("me", c, 30)
    f.mol(m, ox, oy, scale=sc)
    f.text(640, 165, "이음이온 사면체 (붕괴 ✗ → 3차 알코올 ✗)", size=11.5)
    # 2행: H3O+ → gem-diol ⇌ acetophenone
    f.arrow(250, 255, 330, 255, "H₃O^+", "(4) 1 M HCl")
    ox, oy = 370, 265
    m = Mol()
    benzene(m, "r", 0, 0, start=90)
    c = m.sub("c", "r1", 30)
    m.sub("o1", c, 90, "OH")
    m.sub("o2", c, -30, "OH", anchor="start")
    m.sub("me", c, 30)
    f.mol(m, ox, oy, scale=sc)
    f.cap(420, 318, "gem-diol (수화물)")
    f.eqarrow(505, 570, 255, "−H₂O", "")
    ox, oy = 605, 265
    m = Mol()
    benzene(m, "r", 0, 0, start=90)
    c = m.sub("c", "r1", 30)
    m.sub("o1", c, 90, "O", kind="2")
    m.sub("me", c, -30)
    f.mol(m, ox, oy, scale=sc)
    f.cap(650, 318, "A: acetophenone")
    f.text(130, 240, "케톤은 산 처리(물 존재) 후에야", size=11.5)
    f.text(130, 258, "생기므로 남은 CH₃Li와", size=11.5)
    f.text(130, 276, "만나지 않는다", size=11.5)
    return f.render()


# ------------------------------------------------------------------ 2009 #25 메커니즘
def f2009_25_mech():
    """Claisen–Schmidt: 엔올레이트 → 알돌 첨가 → 양성자 이동 → E1cB 탈수"""
    f = Fig(800, 380)
    # (1) acetone + OH−
    ox, oy = 70, 110
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("me", c, 210)
    a = m.sub("a", c, -30)
    m.sub("h", a, 30, "H", length=24)
    f.mol(m, ox, oy)
    C, O, A, H = (_at(m, k, ox, oy) for k in ("c", "o", "a", "h"))
    f.text(H[0] + 40, H[1] - 6, "HO^−", size=12)
    f.lp(H[0] + 27, H[1] - 6, 0)
    f.curly(H[0] + 25, H[1] - 1, H[0] + 8, H[1] + 1, bend=-0.4)
    f.curly(*_mid(A, H, 0.5), *_mid(C, A, 0.5), bend=0.8)
    f.curly(*_mid(C, O, 0.5), O[0] - 9, O[1] + 3, bend=-0.9)
    f.arrow(170, 110, 220, 110, "", "−H₂O")
    # (2) 엔올레이트 (탄소 음이온 형태) + PhCHO
    ox, oy = 250, 110
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("me", c, 210)
    a = m.sub("a", c, -30)
    f.mol(m, ox, oy)
    A = _at(m, "a", ox, oy)
    f.charge(A[0] + 2, A[1] + 13, "−")
    f.lp(A[0] + 9, A[1] - 3, 30)
    b = Mol()
    k = b.atom("k", 0, 0)
    b.sub("o", k, 120, "O", kind="2")
    b.sub("h", k, 240, "H", length=22)
    phenyl_at(b, "p", k, 0)
    bx, by = 345, 105
    f.mol(b, bx, by)
    K, KO = _at(b, "k", bx, by), _at(b, "o", bx, by)
    f.curly(A[0] + 12, A[1] - 6, K[0] - 6, K[1] + 1, bend=-0.5)
    f.curly(*_mid(K, KO, 0.5), KO[0] + 10, KO[1] + 2, bend=0.9)
    f.text(285, 172, "엔올레이트(탄소 음이온형)", size=11)
    f.arrow(455, 110, 505, 110, "알돌 첨가", "")
    # (3) 알콕사이드 → H2O → β-하이드록시 케톤
    ox, oy = 530, 120
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("me", c, 210)
    a = m.sub("a", c, -30)
    b2 = m.sub("b", a, 30)
    m.sub("oh", b2, 90, "OH")
    phenyl_at(m, "p", b2, -30)
    f.mol(m, ox, oy)
    f.text(650, 75, "(O^− + H₂O → OH)", size=11)
    f.cap(610, 205, "β-하이드록시 케톤 (알돌)")
    # 2행: E1cB
    f.text(20, 235, "E1cB 탈수", size=12.5, anchor="start", weight="bold", color=RED)
    ox, oy = 90, 300
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("me", c, 210)
    a = m.sub("a", c, -30)
    m.sub("h", a, -90, "H", length=24)
    b2 = m.sub("b", a, 30)
    m.sub("oh", b2, 90, "OH")
    phenyl_at(m, "p", b2, -30)
    f.mol(m, ox, oy)
    A, H = _at(m, "a", ox, oy), _at(m, "h", ox, oy)
    f.text(H[0] - 42, H[1] + 4, "HO^−", size=12)
    f.lp(H[0] - 28, H[1] + 4, 0)
    f.curly(H[0] - 26, H[1] + 9, H[0] - 8, H[1] + 4, bend=-0.5)
    f.curly(*_mid(A, H, 0.5), A[0] + 8, A[1] - 2, bend=-0.9)
    f.arrow(260, 300, 315, 300, "α-H 제거", "")
    ox, oy = 345, 300
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("me", c, 210)
    a = m.sub("a", c, -30)
    b2 = m.sub("b", a, 30)
    m.sub("oh", b2, 90, "OH")
    phenyl_at(m, "p", b2, -30)
    f.mol(m, ox, oy)
    A, B2, OH = _at(m, "a", ox, oy), _at(m, "b", ox, oy), _at(m, "oh", ox, oy)
    f.charge(A[0], A[1] + 13, "−")
    f.curly(A[0] - 4, A[1] + 22, *_mid(A, B2, 0.5), bend=-0.9)
    f.curly(*_mid(B2, OH, 0.5), OH[0] + 20, OH[1] - 4, bend=-0.9)
    f.arrow(510, 300, 565, 300, "−OH^−", "(느림)")
    ox, oy = 590, 300
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("me", c, 210)
    a = m.sub("a", c, -30)
    b2 = m.sub("b", a, 30, kind="2")
    phenyl_at(m, "p", b2, -30)
    f.mol(m, ox, oy, scale=0.95)
    f.cap(680, 362, "benzalacetone (E, 공액)")
    f.text(160, 235, "→ 남은 CH₃에서 같은 과정을 한 번 더 반복 → (E,E)-dibenzalacetone", size=11.5, anchor="start")
    return f.render()


if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from preview import shot
    shot([f2011_36_scheme(), f2011_36_resonance(), f2011_36_mech(), f2010_39(), f2010_39_mech(), f2009_25(), f2009_25_mech()], sys.argv[1])
