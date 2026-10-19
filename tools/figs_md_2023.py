"""MDEET 2023 자연과학Ⅱ 유기화학 21–30번 해설 그림"""
import math
from chemsvg import Mol, Fig, benzene, phenyl_at, L, RED, BLUE, INK

GRAY = "#8a8f98"


def ap(m, name, ox, oy):
    """분자 좌표 → 그림 절대 좌표"""
    x, y = m.pos(name)
    return x + ox, y + oy


def mid(p, q, t=0.5):
    return p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t


def ring_atoms(m, p, cx, cy, n=6, r=L, start=90):
    """결합 없이 고리 원자만"""
    return m.ring(p, cx, cy, n, r, start, bonds=False)


def circle(f, x, y, r, color=INK):
    f.raw(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="{color}" stroke-width="1.3"/>')


def dipole(f, x1, y1, x2, y2, color=BLUE):
    """쌍극자 화살표(+ 꼬리): (x1,y1) δ+ → (x2,y2) δ−"""
    f.arrow(x1, y1, x2, y2, color=color)
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy) or 1
    nx, ny = -dy / d * 5, dx / d * 5
    px, py = x1 + dx * 0.12, y1 + dy * 0.12
    f.raw(f'<line x1="{px + nx:.1f}" y1="{py + ny:.1f}" x2="{px - nx:.1f}" y2="{py - ny:.1f}" stroke="{color}" stroke-width="1.5"/>')


# ------------------------------------------------------------------ 21
def _cyclohexenol(nums, color):
    m = Mol()
    r = m.ring("r", 0, 0, 6, L, 90)
    m.set_bond("r5", "r0", "in", (0, 0))
    m.sub("oh", "r4", 210, "HO", anchor="end")
    m.sub("me1", "r1", 60)
    m.sub("me2", "r1", 0)
    return m


def f21():
    f = Fig(760, 210)
    # 올바른 번호
    for k, (ox, nums, col, title) in enumerate([
            (130, ["3", "4", "5", "6", "1", "2"], BLUE, "옳은 번호: 4,4-dimethylcyclohex-2-en-1-ol"),
            (500, ["1", "6", "5", "4", "3", "2"], GRAY, "⑤의 번호: OH 탄소가 3번 → 규칙 위반")]):
        m = _cyclohexenol(nums, col)
        oy = 100
        f.mol(m, ox, oy)
        for i, n in enumerate(nums):
            x, y = ap(m, f"r{i}", ox, oy)
            f.text(ox + (x - ox) * 0.62, oy + (y - oy) * 0.62, n, size=11, color=col, weight="bold")
        f.text(ox, 175, title, size=12, color=(BLUE if k == 0 else RED), weight="bold")
    f.cross(600, 70)
    f.text(20, 22, "① OH(주기능기, 접미사 -ol) → C1  ② C=C에 낮은 번호 → C2=C3  ③ CH₃ → C4,4", size=11, anchor="start")
    f.text(560, 40, "C=C는 1번이지만 주기능기 OH가 3번", size=11, color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 22
def f22():
    f = Fig(780, 250)
    cols = {"a": BLUE, "b": RED, "c": "#2e8b57"}
    specs = [("A  1,2-dioxane", (0, 1), ["", "", "a", "b", "b", "a"], "¹³C 2종 (a, b)", "μ ≠ 0 (gauche O–O)"),
             ("B  1,3-dioxane", (0, 2), ["", "a", "", "b", "c", "b"], "¹³C 3종 (a, b, c)", "μ ≈ 2.1 D"),
             ("C  1,4-dioxane", (0, 3), ["", "a", "a", "", "a", "a"], "¹³C 1종 (a)", "μ ≈ 0 (의자형, 대칭 중심)")]
    for k, (name, ox_i, envs, nmr, mu) in enumerate(specs):
        ox, oy = 130 + 260 * k, 95
        m = Mol()
        m.ring("r", 0, 0, 6, L, 90)
        for i in ox_i:
            m.label(f"r{i}", "O")
        f.mol(m, ox, oy)
        for i, e in enumerate(envs):
            if e:
                x, y = ap(m, f"r{i}", ox, oy)
                f.text(ox + (x - ox) * 1.42, oy + (y - oy) * 1.42, e, size=12, color=cols[e], weight="bold", italic=True)
        f.cap(ox, 165, name)
        f.text(ox, 190, nmr, size=12)
        f.text(ox, 212, mu, size=12, color=BLUE)
    # B 쌍극자
    dipole(f, 452, 118, 452, 72)
    f.text(466, 95, "μ", size=12, color=BLUE)
    f.text(390, 236, "A·B·C 모두 C₄H₈O₂ — A/B는 O의 위치만 다른 구조 이성질체", size=11, color=INK)
    return f.render()


# ------------------------------------------------------------------ 23
_MORPH = {  # 이미지(400 dpi) 좌표
    "O3": (397, 172), "C3": (447, 205), "C2": (517, 160), "C1": (587, 200), "C11": (587, 280),
    "C12": (517, 320), "C4": (447, 280), "O5": (392, 365), "C5": (447, 440), "C13": (517, 405),
    "H5": (402, 456), "C6": (447, 520), "O6": (392, 553), "C7": (517, 560), "C8": (587, 520),
    "C14": (587, 440), "H14": (607, 488), "C9": (657, 405), "H9": (690, 478), "C10": (657, 320),
    "N": (735, 425), "Me": (790, 480), "C16": (690, 352), "C15": (590, 360),
}


def _morphine(s=0.5, x0=517, y0=360):
    m = Mol()
    lab = {"O3": ("HO", "end"), "O5": ("O", "middle"), "H5": ("H", "middle"), "O6": ("HO", "end"),
           "H14": ("H", "middle"), "H9": ("H", "middle"), "N": ("N", "middle")}
    for k, (x, y) in _MORPH.items():
        l, a = lab.get(k, (None, "middle"))
        m.atom(k, (x - x0) * s, (y - y0) * s, l, a)
    cA = ((517 - x0) * s, (240 - y0) * s)
    cC = ((517 - x0) * s, (480 - y0) * s)
    for a1, a2 in [("C3", "O3"), ("C3", "C2"), ("C1", "C11"), ("C12", "C4"), ("C4", "O5"), ("O5", "C5"),
                   ("C12", "C13"), ("C5", "C13"), ("C5", "C6"), ("C6", "C7"), ("C8", "C14"), ("C13", "C14"),
                   ("C14", "C9"), ("C9", "C10"), ("C10", "C11"), ("C9", "N"), ("N", "Me"), ("N", "C16"),
                   ("C16", "C15")]:
        m.bond(a1, a2)
    m.bond("C2", "C1", "in", cA)
    m.bond("C11", "C12", "in", cA)
    m.bond("C4", "C3", "in", cA)
    m.bond("C7", "C8", "in", cC)
    m.bond("C5", "H5", "w")
    m.bond("C6", "O6", "h")
    m.bond("C14", "H14", "w")
    m.bond("C9", "H9", "h")
    m.bond("C13", "C15", "w")
    return m


def f23():
    f = Fig(780, 300)
    m = _morphine()
    ox, oy = 230, 150
    f.mol(m, ox, oy)
    tags = {"C5": ("5", 13, 6), "C6": ("6", 13, -6), "C9": ("9", 10, -12),
            "C13": ("13", -16, -10), "C14": ("14", -14, 8)}
    for k, (t, dx, dy) in tags.items():
        x, y = ap(m, k, ox, oy)
        f.raw(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{RED}"/>')
        f.text(x + dx, y + dy, t, size=11, color=RED, weight="bold")
    xa, ya = ap(m, "O3", ox, oy)
    f.text(xa - 38, ya, "a", size=14, weight="bold", color=BLUE)
    xb, yb = ap(m, "O6", ox, oy)
    f.text(xb - 38, yb, "b", size=14, weight="bold", color=BLUE)
    f.text(230, 270, "카이랄 중심 5개(●): 5R, 6S, 9R, 13S, 14R", size=12, weight="bold", color=RED)
    f.text(230, 290, "a: 페놀 O–H   b: 2차 알릴 알코올 O–H", size=11, color=BLUE)
    # CIP at C5
    f.box(440, 40, 320, 200)
    f.text(600, 60, "* = C5 의 CIP 우선순위", size=13, weight="bold")
    for i, t in enumerate(["① O(에터)", "② C6 : (O, C, H)", "③ C13 : (C, C, C)", "④ H — 쐐기(앞쪽)"]):
        f.text(460, 90 + 24 * i, t, size=12, anchor="start")
    f.text(460, 192, "①→②→③ 화면상 반시계(S로 보임)", size=12, anchor="start")
    f.text(460, 214, "H가 앞쪽이므로 뒤집어 → (R)", size=12, anchor="start", color=RED, weight="bold")
    return f.render()


def f23b():
    f = Fig(780, 215)
    # phenoxide resonance
    for k, ox in enumerate([80, 230, 380]):
        m = Mol()
        m.ring("r", 0, 0, 6, L, 90, arom=([0, 2, 4] if k == 0 else [2, 4] if k == 1 else [0, 3]))
        o = m.sub("o", "r0", 90, "O")
        if k == 1:
            m.set_bond("r0", "o", "2")
        if k == 2:
            m.set_bond("r0", "o", "2")
            m.set_bond("r1", "r2", "in", (0, 0))
        f.mol(m, ox, 110)
        if k == 0:
            f.charge(ox + 14, 110 - 72, "-")
            f.lp(ox - 10, 110 - 60, 180)
        elif k == 1:
            x, y = ap(m, "r1", ox, 110)
            f.charge(x + 10, y - 8, "-")
        else:
            x, y = ap(m, "r3", ox, 110)
            f.charge(x, y + 13, "-")
    f.resarrow(130, 180, 110)
    f.resarrow(280, 330, 110)
    f.text(230, 180, "a: 페녹사이드 — 음전하가 o·p 탄소로 비편재화 (pKₐ ≈ 10)", size=12, weight="bold", color=BLUE)
    # alkoxide
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.set_bond("r2", "r3", "in", (0, 0))
    m.sub("o", "r0", 90, "O")
    f.mol(m, 610, 110)
    f.charge(624, 38, "-")
    f.text(610, 180, "b: 알콕사이드 — 음전하가 O에 국재 (pKₐ ≈ 16)", size=12, weight="bold", color=RED)
    f.text(610, 200, "(O가 붙은 C는 sp³ — π계와 공액 불가)", size=11, color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 24
def _pea(m, p, cx, cy, nh2_kind):
    """1-phenylethylamine: 중심 C, CH3(왼위), NH2(오른위), Ph(아래)"""
    c = m.atom(p + "c", cx, cy)
    m.sub(p + "me", c, 150)
    n = m.sub(p + "n", c, 30, "NH_2", anchor="start", kind=nh2_kind)
    benz = m.ring(p + "r", cx, cy + 2 * L, 6, L, 90, arom=[1, 3, 5])
    m.bond(c, p + "r0")
    return c


def f24():
    f = Fig(800, 360)
    # A
    m = Mol()
    m.atom("c", 0, 0)
    m.sub("me", "c", 150)
    m.sub("n", "c", 30, "NH", anchor="start", kind="2")
    m.ring("r", 0, 2 * L, 6, L, 90, arom=[1, 3, 5])
    m.bond("c", "r0")
    f.mol(m, 60, 70)
    f.cap(60, 175, "A (이민, 평면)")
    f.arrow(110, 95, 185, 95, "NaBH₄", "H⁻: 두 면 공격")
    # B racemate
    m = Mol()
    _pea(m, "R", 0, 0, "w")
    _pea(m, "S", 95, 0, "h")
    f.mol(m, 220, 70)
    f.text(220, 180, "(R)", size=12, weight="bold", color=BLUE)
    f.text(315, 180, "(S)", size=12, weight="bold", color=RED)
    f.cap(268, 200, "B: 1 : 1 라세미 혼합물")
    f.text(268, 30, "C=N 양면 동등 공격", size=11, color=GRAY)
    # 산
    f.arrow(380, 95, 470, 95, "(S)-malic acid", "산–염기 반응")
    f.text(615, 40, "C: 부분입체이성질체 염의 혼합물", size=13, weight="bold")
    f.box(490, 55, 250, 75)
    f.text(615, 78, "(R)-RNH₃⁺ · (S)-malate⁻", size=12, color=BLUE)
    f.text(615, 104, "(S)-RNH₃⁺ · (S)-malate⁻", size=12, color=RED)
    f.text(615, 145, "R,S 와 S,S → 거울상 아님 → 용해도·녹는점 다름", size=11)
    # 분리
    f.arrow(615, 160, 615, 205, "분별 결정(용해도 차이)", None)
    f.text(615, 222, "덜 녹는 염 결정 → 여과 → NaOH(aq)로 유리 아민 회수", size=11)
    m = Mol()
    _pea(m, "D", 0, 0, "w")
    f.mol(m, 430, 262)
    f.cap(640, 290, "D = (R)-1-phenylethanamine")
    f.text(640, 312, "NH₂ > Ph > CH₃, H는 뒤쪽 → 시계 방향 = R", size=11, color=BLUE)
    return f.render()


# ------------------------------------------------------------------ 25
def _azulene(m, cx, cy, kekule=True):
    r7 = L / (2 * math.sin(math.pi / 7))
    a7 = L / (2 * math.tan(math.pi / 7))
    a5 = L / (2 * math.tan(math.pi / 5))
    r5 = L / (2 * math.sin(math.pi / 5))
    ring_atoms(m, "p", cx, cy, 7, r7, 180 / 7)
    ring_atoms(m, "q", cx + a7 + a5, cy, 5, r5, 144)
    bonds = [("p0", "p1"), ("p1", "p2"), ("p2", "p3"), ("p3", "p4"), ("p4", "p5"), ("p5", "p6"), ("p6", "p0"),
             ("p0", "q1"), ("q1", "q2"), ("q2", "q3"), ("q3", "p1")]
    dbl = {("p6", "p0"): (cx, cy), ("p2", "p3"): (cx, cy), ("p4", "p5"): (cx, cy),
           ("q1", "q2"): (cx + a7 + a5, cy), ("q3", "p1"): (cx + a7 + a5, cy)} if kekule else {}
    for b in bonds:
        if b in dbl:
            m.bond(b[0], b[1], "in", dbl[b])
        else:
            m.bond(*b)
    return (cx, cy), (cx + a7 + a5, cy)


def f25():
    f = Fig(800, 350)
    f.text(20, 20, "ㄱ. 쌍극자 모멘트", size=13, weight="bold", anchor="start")
    # naphthalene
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90, arom=[0, 2, 4])
    c2 = 2 * L * math.cos(math.radians(30))
    for i, ang in enumerate([90, 30, -30, -90]):
        pass
    m.atom("s0", c2, -L)
    m.atom("s1", c2 + L * math.cos(math.radians(30)), -L / 2)
    m.atom("s2", c2 + L * math.cos(math.radians(30)), L / 2)
    m.atom("s3", c2, L)
    m.bond("r1", "s0")
    m.bond("s0", "s1", "in", (c2, 0))
    m.bond("s1", "s2")
    m.bond("s2", "s3", "in", (c2, 0))
    m.bond("s3", "r2")
    f.mol(m, 70, 95)
    f.text(96, 150, "naphthalene: μ = 0", size=12, weight="bold")
    f.text(96, 168, "(D₂h, 대칭 중심)", size=11, color=GRAY)
    # azulene ↔ polar
    m = Mol()
    _azulene(m, 0, 0)
    f.mol(m, 280, 95)
    f.resarrow(370, 410, 95)
    m = Mol()
    c7, c5 = _azulene(m, 0, 0, kekule=False)
    f.mol(m, 470, 95)
    circle(f, 470 + c7[0], 95, 20)
    circle(f, 470 + c5[0], 95, 13)
    f.charge(470 - 2, 95, "+")
    f.charge(470 + c5[0], 95, "-")
    dipole(f, 470 - 20, 135, 470 + c5[0] + 10, 135)
    f.text(390, 160, "azulene: 7원 고리(6π, +) – 5원 고리(6π, −) 분극 → μ ≈ 1.0 D", size=12, weight="bold")
    f.text(660, 95, "∴ naphthalene < azulene", size=13, weight="bold", color=RED)
    f.text(660, 115, "ㄱ ✗", size=13, weight="bold", color=RED)
    # ㄴ
    f.text(20, 200, "ㄴ. 끓는점", size=13, weight="bold", anchor="start")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90, arom=[0, 2, 4])
    m.sub("c1", "r0", 90, "Cl")
    m.sub("c2", "r1", 30, "Cl")
    f.mol(m, 160, 270)
    dipole(f, 208, 296, 236, 254)
    f.text(160, 335, "o-: μ ≈ 2.5 D, bp 180 ℃", size=12, weight="bold")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90, arom=[0, 2, 4])
    m.sub("c1", "r0", 90, "Cl")
    m.sub("c2", "r3", 270, "Cl")
    f.mol(m, 400, 250)
    f.text(400, 335, "p-: μ = 0, bp 174 ℃ (mp 53 ℃)", size=12, weight="bold")
    f.text(640, 250, "쌍극자–쌍극자 인력: o- > p-", size=12)
    f.text(640, 272, "끓는점 o- > p- → ㄴ ○", size=13, weight="bold", color=BLUE)
    f.text(640, 294, "(녹는점은 대칭·결정 쌓임 때문에 p- > o-)", size=11, color=GRAY)
    return f.render()


def f25b():
    f = Fig(780, 150)
    f.text(20, 20, "ㄷ. 탄소 양이온 안정도", size=13, weight="bold", anchor="start")
    # allyl
    for k, ox in enumerate([60, 190]):
        m = Mol()
        m.atom("a", 0, 0)
        m.sub("b", "a", 30)
        m.sub("c", "b", -30)
        m.set_bond("a", "b", "2" if k == 0 else 1)
        m.set_bond("b", "c", 1 if k == 0 else "2")
        f.mol(m, ox, 75)
        x, y = ap(m, "c" if k == 0 else "a", ox, 75)
        f.charge(x + (8 if k == 0 else -8), y + 12, "+")
        if k == 0:
            f.curly(ox + 11, 75 - 14, ox + 40, 75 - 14, bend=-0.6)
    f.resarrow(125, 170, 70)
    f.text(155, 120, "알릴 양이온: 공명(p 궤도 3개 공액) — 전하 비편재화", size=12, weight="bold", color=BLUE)
    m = Mol()
    m.atom("a", 0, 0)
    m.sub("b", "a", 30)
    m.sub("c", "b", -30)
    f.mol(m, 470, 75)
    x, y = ap(m, "c", 470, 75)
    f.charge(x + 8, y + 12, "+")
    f.text(500, 120, "1차 propyl 양이온: 초공액만 → 불안정", size=12, weight="bold", color=RED)
    f.text(680, 75, "allyl > propyl : ㄷ ○", size=13, weight="bold", color=BLUE)
    return f.render()


# ------------------------------------------------------------------ 26
def f26a():
    f = Fig(780, 210)
    f.text(20, 18, "ㄱ. SN2 친핵체 N₃⁻의 용매화", size=13, weight="bold", anchor="start")
    for k, (cx, solv) in enumerate([(190, "CH_3CN"), (560, "CH_3OH")]):
        f.raw(f'<circle cx="{cx}" cy="105" r="22" fill="#fff" stroke="{BLUE if k == 0 else RED}" stroke-width="1.6"/>')
        f.text(cx, 105, "N_3^−", size=14, weight="bold")
        if k == 1:
            for ang in (0, 72, 144, 216, 288):
                a = math.radians(ang)
                x1, y1 = cx + 24 * math.cos(a), 105 - 24 * math.sin(a)
                x2, y2 = cx + 52 * math.cos(a), 105 - 52 * math.sin(a)
                f.raw(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{RED}" stroke-dasharray="3 3" stroke-width="1.3"/>')
                f.text(cx + 72 * math.cos(a), 105 - 70 * math.sin(a), "H–OCH_3", size=11)
            f.text(cx, 192, "(나) 양성자성: H-결합 용매 우리 → 친핵성↓ (느림)", size=12, weight="bold", color=RED)
        else:
            for ang in (30, 150, 270):
                a = math.radians(ang)
                f.text(cx + 66 * math.cos(a), 105 - 60 * math.sin(a), "CH_3C≡N", size=11, color=GRAY)
            f.text(cx, 192, "(가) 비양성자성 극성: 음이온 ‘벌거숭이’ → 친핵성↑ (빠름)", size=12, weight="bold", color=BLUE)
    return f.render()


def _chair(m, p, sc=1.15):
    """교과서식 의자형: p0 왼쪽 끝(발, 아래) … p3 오른쪽 끝(머리, 위).
    축 방향: p0·p2·p4 아래, p1·p3·p5 위.  반환: sub(name, i, 'ax'|'eq', label, length, anchor)"""
    e1, e2, e3 = (16 * sc, -26 * sc), (40 * sc, 12 * sc), (28 * sc, -14 * sc)
    pts = [(0.0, 0.0)]
    for e in (e1, e2, e3, (-e1[0], -e1[1]), (-e2[0], -e2[1])):
        pts.append((pts[-1][0] + e[0], pts[-1][1] + e[1]))
    for i, (x, y) in enumerate(pts):
        m.atom(f"{p}{i}", x, y)
    for i in range(6):
        m.bond(f"{p}{i}", f"{p}{(i + 1) % 6}")
    up = {0: False, 1: True, 2: False, 3: True, 4: False, 5: True}
    # 적도 방향: 한 칸 건너 결합과 평행, 바깥쪽
    eqd = {0: (-e2[0], -e2[1]), 3: e2, 1: (-e3[0], -e3[1]), 4: e3, 2: e1, 5: (-e1[0], -e1[1])}

    def sub(name, i, kind, label=None, length=28, anchor="middle"):
        x, y = pts[i]
        if kind == "ax":
            d = (0, -1) if up[i] else (0, 1)
        else:
            dx, dy = eqd[i]
            n = math.hypot(dx, dy)
            d = (dx / n, dy / n)
        m.atom(name, x + d[0] * length, y + d[1] * length, label, anchor)
        m.bond(f"{p}{i}", name)
        return name
    return sub


def f26b():
    f = Fig(780, 250)
    f.text(20, 18, "ㄴ. E2: 이탈기와 β-H의 anti-periplanar(trans-이축) 배열 필요", size=13, weight="bold", anchor="start")
    for k, (ox, title, col) in enumerate([(200, "(가) trans: Br 적도 — anti β-H 없음 (느림)", RED),
                                          (560, "(나) cis: Br 축 — β-H(축)와 anti (빠름)", BLUE)]):
        m = Mol()
        sub = _chair(m, "c")
        sub("tb", 0, "eq", "t-Bu", anchor="end", length=30)
        if k == 0:
            sub("br", 3, "eq", "Br", anchor="start", length=30)
            sub("h0", 3, "ax", "H", length=24)
            sub("h1", 2, "ax", "H", length=24)
            sub("h5", 4, "ax", "H", length=24)
        else:
            sub("br", 3, "ax", "Br", length=34)
            sub("h1", 2, "ax", "H", length=26)
            sub("h5", 4, "ax", "H", length=26)
        oy = 125
        ox -= 50
        f.mol(m, ox, oy)
        if k == 1:
            x1, y1 = ap(m, "br", ox, oy)
            x2, y2 = ap(m, "h5", ox, oy)
            f.raw(f'<line x1="{x1 + 14:.1f}" y1="{y1:.1f}" x2="{x1 + 14:.1f}" y2="{y2:.1f}" stroke="{BLUE}" stroke-dasharray="2 3" stroke-width="1"/>')
            f.text(x1 + 34, (y1 + y2) / 2, "180°", size=11, color=BLUE)
            f.text(ox + 50, 178, "β-H(C2·C6 축, 아래)과 Br(축, 위) → anti", size=11, color=BLUE)
        else:
            x1, y1 = ap(m, "br", ox, oy)
            f.cross(x1 + 12, y1 + 20, s=6)
            f.text(ox + 50, 178, "Br(적도)과 anti인 것은 고리 C–C 결합뿐", size=11, color=RED)
        f.text(ox + 50, 202, title, size=12, weight="bold", color=col)
    f.text(390, 232, "t-Bu는 항상 적도(A값 ≈ 4.9 kcal/mol) → 형태 고정. (가)는 Br이 축으로 갈 수 없어 E2가 매우 느리다 → ㄴ ✗", size=11)
    return f.render()


def _phthalimide_N(m, n):
    """n(N 원자)을 왼쪽 꼭짓점으로 하는 프탈이미드 고리"""
    x0, y0 = m.pos(n)
    r5 = L / (2 * math.sin(math.pi / 5))
    a5 = L / (2 * math.tan(math.pi / 5))
    a6 = L * math.cos(math.radians(30))
    cx = x0 + r5
    pts = {}
    for nm, ang in (("k1", 108), ("k3", 36), ("k4", -36), ("k2", -108)):
        pts[nm] = m.atom(nm, cx + r5 * math.cos(math.radians(ang)), y0 - r5 * math.sin(math.radians(ang)))
    m.bond(n, "k1"); m.bond("k1", "k3"); m.bond("k4", "k2"); m.bond("k2", n)
    m.sub("ko1", "k1", 108 + 36, "O", kind="2", length=26)
    m.sub("ko2", "k2", -108 - 36, "O", kind="2", length=26)
    bx = cx + a5 + a6
    m.ring("b", bx, y0, 6, L, 150, bonds=False)
    # b0 (150°) = k3, b5 (210°) = k4
    m.a["b0"][:2] = list(m.pos("k3"))
    m.a["b5"][:2] = list(m.pos("k4"))
    ctr = (bx, y0)
    m.bond("k3", "b1", "in", ctr); m.bond("b1", "b2"); m.bond("b2", "b3", "in", ctr)
    m.bond("b3", "b4"); m.bond("b4", "k4", "in", ctr); m.bond("k4", "k3")
    m.a.pop("b0"); m.a.pop("b5")

def f26c():
    f = Fig(800, 250)
    f.text(20, 18, "ㄷ. SNAr: 첨가(rds) → Meisenheimer 착물 → F⁻ 제거", size=13, weight="bold", anchor="start")
    # para: sigma complex with charge on C bearing NO2 → nitronate
    def sigma(ox, oy, nitro_pos, form):
        m = Mol()
        m.ring("r", 0, 0, 6, L, 90)
        m.sub("f", "r0", 60, "F", length=26)
        m.sub("o", "r0", 120, "OCH_3", anchor="end", length=26)
        x = f"r{nitro_pos}"
        ang = {3: 270, 2: -30}[nitro_pos]
        n = m.sub("n", x, ang, "N^+", length=28)
        m.sub("o1", n, ang + 50, "O^−" if form == 0 else "O^−", length=24)
        m.sub("o2", n, ang - 50, "O", length=24, kind="2")
        if form == 0:  # 탄소 음이온 at r3, doubles r1=r2, r4=r5
            m.set_bond("r1", "r2", "in", (0, 0))
            m.set_bond("r4", "r5", "in", (0, 0))
        else:  # 나이트로네이트: r3=N, doubles r1=r2, r4=r5, N–O− x2
            m.set_bond("r1", "r2", "in", (0, 0))
            m.set_bond("r4", "r5", "in", (0, 0))
            m.set_bond("r3", "n", "2")
            m.label("o2", "O^−")
            m.set_bond("n", "o2", 1)
        return m
    m = sigma(0, 0, 3, 0)
    f.mol(m, 110, 110)
    x, y = ap(m, "r3", 110, 110)
    f.charge(x - 16, y - 4, "-")
    f.resarrow(185, 225, 110)
    m = sigma(0, 0, 3, 1)
    f.mol(m, 300, 110)
    f.text(205, 205, "(가) p-NO₂: 음전하가 NO₂의 O까지 비편재화(−M)", size=12, weight="bold", color=BLUE)
    f.text(205, 225, "→ 중간체·전이 상태 안정 → 빠름", size=12, color=BLUE)
    # meta
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.sub("f", "r0", 60, "F", length=26)
    m.sub("o", "r0", 120, "OCH_3", anchor="end", length=26)
    m.set_bond("r2", "r3", "in", (0, 0))
    m.set_bond("r4", "r5", "in", (0, 0))
    n = m.sub("n", "r2", -30, "NO_2", anchor="start", length=28)
    f.mol(m, 600, 110)
    x, y = ap(m, "r1", 600, 110)
    f.charge(x + 12, y - 8, "-")
    f.text(600, 205, "(나) m-NO₂: 음전하는 C1의 o·p(C2,C4,C6)에만", size=12, weight="bold", color=RED)
    f.text(600, 225, "NO₂ 탄소(C3)에 오지 않음 → 유발 효과만 → 느림", size=12, color=RED)
    return f.render()


# ------------------------------------------------------------------ 27
def f27():
    f = Fig(800, 230)
    f.text(20, 18, "ㄱ. 방향족 Claisen 자리옮김 ([3,3]-시그마 자리옮김) — 알릴기는 ortho로", size=13, weight="bold", anchor="start")
    # 반응물 TS 형태
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90, arom=[0, 2, 4])
    o = m.atom("o", 0, -2 * L, "O")
    m.bond("r0", "o")
    m.atom("a1", 27, -2 * L - 15)
    m.atom("a2", 54, -2 * L)
    m.atom("a3", 54, -L + 2)
    m.bond("o", "a1")
    m.bond("a1", "a2")
    m.bond("a2", "a3", "2r")
    m.bond("a3", "r1", "form")
    ox, oy = 90, 150
    f.mol(m, ox, oy)
    P = lambda n: ap(m, n, ox, oy)
    f.curly(*mid(P("r0"), P("r1")), *mid(P("r1"), P("a3"), 0.55), bend=-0.5)
    f.curly(*mid(P("a2"), P("a3")), *mid(P("a1"), P("a2")), bend=0.6)
    f.curly(*mid(P("o"), P("a1")), *mid(P("o"), P("r0")), bend=0.7)
    f.text(ox + 20, 215, "6원 고리 의자형 TS", size=11, color=GRAY)
    f.arrow(170, 150, 225, 150, "250 ℃")
    # dienone
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.set_bond("r2", "r3", "in", (0, 0))
    m.set_bond("r4", "r5", "in", (0, 0))
    m.sub("o", "r0", 90, "O", kind="2")
    m.sub("h", "r1", 30, "H", length=24)
    a1 = m.sub("a1", "r1", -30)
    a2 = m.sub("a2", a1, 30)
    m.sub("a3", a2, -30, kind="2")
    f.mol(m, 275, 150)
    f.text(300, 215, "6-allylcyclohexa-2,4-dienone", size=11)
    f.arrow(380, 150, 440, 150, "토토머화", "방향족성 회복")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90, arom=[0, 2, 4])
    m.sub("o", "r0", 90, "OH")
    a1 = m.sub("a1", "r1", -30)
    a2 = m.sub("a2", a1, 30)
    m.sub("a3", a2, -30, kind="2")
    f.mol(m, 490, 150)
    f.text(515, 215, "2-allylphenol (ortho, 주생성물)", size=12, weight="bold", color=BLUE)
    f.box(620, 70, 165, 110)
    f.text(702, 92, "보기의 3-allylphenol(meta)", size=11, color=RED, weight="bold")
    f.text(702, 112, "✗ — [3,3]은 O의 바로", size=11, color=RED)
    f.text(702, 130, "이웃 탄소(ortho)에만 결합", size=11, color=RED)
    f.text(702, 150, "두 ortho가 막히면 Cope를", size=11, color=GRAY)
    f.text(702, 168, "한 번 더 → para", size=11, color=GRAY)
    return f.render()


def f27b():
    f = Fig(800, 335)
    f.text(20, 18, "ㄴ. Friedel–Crafts 알킬화: 1차 → 2차 탄소 양이온 (1,2-H 이동)", size=13, weight="bold", anchor="start")
    f.text(110, 70, "CH_3CH_2CH_2–Cl···AlCl_3", size=12)
    f.arrow(205, 70, 260, 70, "1,2-H⁻ 이동")
    f.text(330, 70, "CH_3–C^+H–CH_3 + AlCl_4^−", size=12)
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90, arom=[0, 2, 4])
    c = m.sub("c", "r0", 90)
    m.sub("m1", c, 150)
    m.sub("m2", c, 30)
    f.mol(m, 520, 115)
    f.text(520, 162, "cumene (주)", size=12, weight="bold", color=BLUE)
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90, arom=[0, 2, 4])
    c = m.sub("c", "r1", 30)
    c2 = m.sub("c2", c, -30)
    m.sub("c3", c2, 30)
    f.mol(m, 680, 115)
    f.text(690, 162, "propylbenzene (부) ✗", size=12, weight="bold", color=RED)
    f.text(330, 105, "더 안정한 2차 양이온 → isopropyl 치환", size=11, color=GRAY)
    f.text(330, 125, "(propyl을 원하면 아실화 → Clemmensen/Wolff–Kishner)", size=11, color=GRAY)
    # ㄷ
    f.text(20, 190, "ㄷ. 다이아조화 → Sandmeyer (위치 유지 치환)", size=13, weight="bold", anchor="start")
    for k, (ox, lab) in enumerate([(80, "NH_2"), (330, "N_2^+ Br^−"), (590, "Br")]):
        m = Mol()
        m.ring("r", 0, 0, 6, L, 90, arom=[0, 2, 4])
        m.sub("x", "r1", 30, lab, anchor="start")
        m.sub("cl", "r3", 270, "Cl")
        f.mol(m, ox, 255)
    f.arrow(150, 250, 260, 250, "NaNO₂, HBr", "0–5 ℃")
    f.arrow(420, 250, 540, 250, "CuBr", "−N₂ (라디칼 경로)")
    f.text(700, 318, "1-bromo-3-chlorobenzene ○", size=12, weight="bold", color=BLUE)
    return f.render()


# ------------------------------------------------------------------ 28
def _phet(m, p, cx, cy):
    """PhCH2CH2– 의 페닐 + CH2 두 개, 마지막 탄소 이름 반환"""
    m.ring(p + "r", cx, cy, 6, L, 90, arom=[0, 2, 4])
    c1 = m.sub(p + "c1", p + "r1", 30)
    c2 = m.sub(p + "c2", c1, -30)
    return c2


def f28():
    f = Fig(800, 360)
    # ㄱ
    f.text(20, 20, "ㄱ", size=13, weight="bold")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90, arom=[0, 2, 4])
    c1 = m.sub("c1", "r1", 30)
    m.sub("cn", c1, -30, "C", length=28)
    m.sub("n", "cn", -30, "N", kind=3, length=26)
    f.mol(m, 70, 70)
    f.arrow(185, 70, 280, 70, "1. LiAlH₄ (H⁻ 2개)", "2. H₂O")
    m = Mol()
    c2 = _phet(m, "a", 0, 0)
    m.sub("n", c2, 30, "NH_2", anchor="start")
    f.mol(m, 330, 70)
    f.text(560, 70, "C≡N → CH₂–NH₂ : 탄소 1개 증가 ○", size=12, weight="bold", color=BLUE)
    # ㄴ
    f.text(20, 140, "ㄴ", size=13, weight="bold")
    m = Mol()
    c2 = _phet(m, "a", 0, 0)
    m.sub("br", c2, 30, "Br")
    f.mol(m, 70, 185)
    f.arrow(190, 175, 245, 175, "PhthN⁻K⁺", "SN2")
    m = Mol()
    c2 = _phet(m, "a", 0, 0)
    n = m.sub("n", c2, 30, "N")
    _phthalimide_N(m, n)
    f.mol(m, 285, 190)
    f.text(360, 250, "N-알킬프탈이미드 (과알킬화 없음)", size=11, color=GRAY)
    f.arrow(495, 175, 590, 175, "H₂N–NH₂", "−프탈하이드라자이드")
    m = Mol()
    c2 = _phet(m, "b", 0, 0)
    m.sub("n", c2, 30, "NH_2", anchor="start")
    f.mol(m, 650, 190)
    f.text(720, 245, "1차 아민 ○", size=12, weight="bold", color=BLUE)
    # ㄷ
    f.text(20, 280, "ㄷ", size=13, weight="bold")
    m = Mol()
    c2 = _phet(m, "a", 0, 0)
    n = m.sub("n", c2, 30, "NH", length=30)
    c = m.sub("co", n, -30)
    m.sub("o", c, -90, "O", kind="2", length=26)
    m.sub("me", c, 30)
    f.mol(m, 70, 310)
    f.arrow(255, 305, 340, 305, "1. LiAlH₄", "2. H₂O")
    m = Mol()
    c2 = _phet(m, "a", 0, 0)
    n = m.sub("n", c2, 30, "NH", length=30)
    c = m.sub("co", n, -30)
    m.sub("me", c, 30)
    f.mol(m, 390, 310)
    f.text(560, 300, "C=O → CH₂ : 2차 아민 ✗", size=12, weight="bold", color=RED, anchor="start")
    f.text(560, 322, "N-ethyl-2-phenylethanamine", size=12, color=RED, anchor="start")
    return f.render()


def f28b():
    f = Fig(800, 160)
    f.text(20, 18, "ㄷ의 메커니즘: 아마이드 LiAlH₄ 환원 — C=O가 CH₂로 (이미늄 경유)", size=13, weight="bold", anchor="start")
    f.text(100, 80, "R–NH–C(=O)–CH_3", size=12)
    f.arrow(170, 80, 230, 80, "H⁻")
    f.text(320, 80, "R–NH–CH(O–AlH_3^−)–CH_3", size=12)
    f.arrow(410, 80, 470, 80, "−‘O–Al’")
    f.text(540, 80, "R–N^+H=CH–CH_3", size=12)
    f.arrow(605, 80, 660, 80, "H⁻")
    f.text(730, 80, "R–NH–CH_2CH_3", size=12, weight="bold", color=RED)
    f.text(400, 130, "에스터와 달리 N이 O보다 좋은 주개이므로 O가 떨어져 나가 이미늄 생성 → 두 번째 H⁻ → 아민 (C–N 결합 유지)", size=11, color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 29
def _hex(m, p, cx, cy):
    return m.ring(p, cx, cy, 6, L, 0)


def f29():
    f = Fig(800, 320)
    m = Mol()
    _hex(m, "r", 0, 0)
    m.sub("o", "r0", 0, "O", kind="2")
    f.mol(m, 70, 160)
    f.cap(85, 205, "A = cyclohexanone")
    f.raw(f'<path d="M140,160 L170,160 M170,60 L170,265" stroke="{INK}" stroke-width="1.5" fill="none"/>')
    f.arrow(170, 60, 320, 60, "Ph₃P⁺–CH₂⁻", "Wittig")
    f.arrow(170, 160, 320, 160, "H₂NNH₂, KOH, 가열", "Wolff–Kishner")
    f.arrow(170, 265, 320, 265, "pyrrolidine, H⁺", "−H₂O")
    m = Mol()
    _hex(m, "r", 0, 0)
    m.sub("c", "r0", 0, kind="2")
    f.mol(m, 370, 60)
    f.text(450, 52, "methylenecyclohexane", size=12, anchor="start")
    f.text(450, 72, "ㄱ ○ : Ph₃P=CH₂가 C=O의 O를 =CH₂로 바꿈 → A는 cyclohexanone", size=11, color=BLUE, anchor="start")
    m = Mol()
    _hex(m, "r", 0, 0)
    f.mol(m, 370, 160)
    f.text(430, 152, "B = cyclohexane (C=O → CH₂)", size=12, weight="bold", color=BLUE, anchor="start")
    f.text(430, 172, "ㄴ ✗ : cyclohexanol은 NaBH₄ 환원 생성물", size=11, color=RED, anchor="start")
    m = Mol()
    _hex(m, "r", 0, 0)
    m.set_bond("r0", "r1", "in", (0, 0))
    n = m.sub("n", "r0", 0, "N")
    m.ring("p", m.pos(n)[0] + 25.5, 0, 5, 25.5, 180, bonds=False)
    m.a.pop("p0")
    for a1, a2 in ((n, "p1"), ("p1", "p2"), ("p2", "p3"), ("p3", "p4"), ("p4", n)):
        m.bond(a1, a2)
    f.mol(m, 370, 265)
    f.text(500, 255, "C = 1-(cyclohex-1-en-1-yl)pyrrolidine (엔아민)", size=12, weight="bold", color=BLUE, anchor="start")
    f.text(500, 275, "ㄷ ✗ : C=C는 N–C=C (N이 붙은 C와 α-C 사이),", size=11, color=RED, anchor="start")
    f.text(500, 293, "보기의 구조는 C4 위치 알릴 아민(위치 틀림)", size=11, color=RED, anchor="start")
    return f.render()


def f29b():
    f = Fig(800, 230)
    f.text(20, 18, "엔아민 형성 (2차 아민) vs Wolff–Kishner (하이드라진)", size=13, weight="bold", anchor="start")
    steps = ["C=O", "카비놀아민", "이미늄 C=N⁺R₂", "엔아민 N–C=C"]
    xs = [70, 230, 410, 610]
    for x, t in zip(xs, steps):
        f.text(x, 70, t, size=12, weight="bold")
    f.arrow(105, 70, 180, 70, "R₂NH 첨가")
    f.arrow(285, 70, 345, 70, "H⁺, −H₂O")
    f.arrow(475, 70, 555, 70, "α-C–H 탈양성자화")
    f.text(410, 100, "N에 H가 없어 이민(C=N–H)이 될 수 없음 → α-H가 떨어져 C=C", size=11, color=GRAY)
    steps = ["C=O", "하이드라존 C=N–NH₂", "C^−–N=NH (탈양성자·재양성자)", "CH₂ + N₂↑"]
    xs = [70, 230, 450, 680]
    for x, t in zip(xs, steps):
        f.text(x, 160, t, size=12, weight="bold")
    f.arrow(105, 160, 160, 160, "H₂NNH₂")
    f.arrow(305, 160, 350, 160, "KOH")
    f.arrow(555, 160, 625, 160, "−N₂", "가열")
    f.text(400, 200, "N₂ 기체 방출이 추진력 → 카보닐 탄소가 CH₂로 완전 환원 (알코올 단계 없음)", size=11, color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 30


def f30():
    f = Fig(800, 260)
    f.text(20, 18, "① Br₂ 첨가: 브로모늄 이온 → Br⁻ 뒷면 공격 → anti 첨가", size=13, weight="bold", anchor="start")
    m = Mol()
    m.ring("r", 0, 0, 5, 25.5, 90)
    m.set_bond("r1", "r2", "in", (0, 0))
    f.mol(m, 60, 120)
    f.text(60, 175, "cyclopentene", size=11)
    f.arrow(100, 120, 160, 120, "Br₂")
    m = Mol()
    m.ring("r", 0, 0, 5, 25.5, 90)
    x1, y1 = m.pos("r1")
    x2, y2 = m.pos("r2")
    m.atom("br", (x1 + x2) / 2 + 26, (y1 + y2) / 2, "Br^+")
    m.bond("r1", "br", "w")
    m.bond("r2", "br", "w")
    ox, oy = 210, 120
    f.mol(m, ox, oy)
    f.text(ox + 62, oy + 42, "Br^−", size=12, color=RED)
    f.curly(ox + 55, oy + 36, ox + x2 + 4, oy + y2 + 6, bend=-0.4)
    f.text(240, 175, "Br⁺는 위 면 → Br⁻는 아래 면에서 공격", size=11, color=RED)
    f.arrow(320, 120, 380, 120)
    for k, ox in enumerate([440, 560]):
        m = Mol()
        m.ring("r", 0, 0, 5, 25.5, 90)
        m.sub("b1", "r1", 30, "Br", kind=("w" if k == 0 else "h"))
        m.sub("b2", "r2", -30, "Br", kind=("h" if k == 0 else "w"))
        f.mol(m, ox, 120)
    f.text(500, 175, "trans-1,2-dibromocyclopentane (라세미)", size=12, weight="bold", color=BLUE)
    m = Mol()
    m.ring("r", 0, 0, 5, 25.5, 90)
    m.sub("b1", "r1", 30, "Br", kind="w")
    m.sub("b2", "r2", -30, "Br", kind="w")
    f.mol(m, 720, 120)
    f.cross(720, 120, s=14)
    f.text(720, 175, "보기 ① cis(메조) ✗", size=12, weight="bold", color=RED)
    f.text(400, 225, "브로모늄의 다리걸친 Br⁺가 한쪽 면을 막아 syn 첨가가 일어나지 않는다 → cis-이브로민화물은 생기지 않음", size=11)
    return f.render()


def f30b():
    f = Fig(800, 300)
    f.text(20, 18, "②–⑤ 옳은 생성물 요약", size=13, weight="bold", anchor="start")
    rows = [("② mCPBA", "syn 산소 전달(협동) → cis-융합 에폭사이드 (메조)"),
            ("③ O₃; Zn/H₂O", "C=C 절단 → 양끝 CHO: hexanedial(OHC–(CH₂)₄–CHO)"),
            ("④ Hg(OAc)₂, H₂O; NaBH₄", "Markovnikov, 자리옮김 없음 → 1-methylcyclohexan-1-ol"),
            ("⑤ BH₃; H₂O₂, NaOH", "역-Markovnikov + syn(H와 B가 같은 면) → trans-2-methylcyclohexan-1-ol (라세미)")]
    for i, (a, b) in enumerate(rows):
        f.text(30, 55 + 26 * i, a, size=12, anchor="start", weight="bold")
        f.text(240, 55 + 26 * i, b, size=12, anchor="start")
    oy = 240
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.set_bond("r0", "r1", "in", (0, 0))
    m.sub("me", "r0", 90)
    f.mol(m, 110, oy)
    f.arrow(160, oy, 220, oy, "H–BH₂", "같은 면")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.sub("me", "r0", 90, kind="h")
    m.sub("h0", "r0", 150, "H", kind="w", length=24)
    m.sub("b", "r1", 30, "BH_2", kind="w", anchor="start")
    m.sub("h1", "r1", -30, "H", kind="h", length=24)
    f.mol(m, 290, oy)
    f.arrow(370, oy, 440, oy, "H₂O₂, OH⁻", "배열 유지")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.sub("me", "r0", 90, kind="h")
    m.sub("b", "r1", 30, "OH", kind="w")
    f.mol(m, 500, oy)
    f.text(670, oy - 10, "H(C1)·OH(C2)는 cis →", size=11, color=BLUE)
    f.text(670, oy + 8, "CH₃·OH는 trans ○", size=11, color=BLUE, weight="bold")
    return f.render()
