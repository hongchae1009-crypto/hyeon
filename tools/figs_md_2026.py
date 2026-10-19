"""MDEET 2026학년도 자연과학Ⅱ 유기화학 21–30번 해설 그림"""
import math
from chemsvg import Mol, Fig, benzene, L, RED, BLUE, INK, rich

GREEN = "#2f7d5b"
GRAY = "#5b6270"
ORANGE = "#d97706"
C30 = L * math.cos(math.radians(30))


# ------------------------------------------------------------------ 공용 헬퍼
def line(f, x1, y1, x2, y2, color=INK, w=1.4, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    f.raw(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{w}"{d} stroke-linecap="round"/>')


def P(m, name, ox, oy):
    x, y = m.pos(name)
    return x + ox, y + oy


def mid(a, b, t=0.5):
    return a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t


def zig(m, p, n, x=0, y=0, up_first=False):
    """지그재그 사슬 p0..p(n-1) (짝수 번째 아래, 홀수 번째 위; up_first면 반대)"""
    names = []
    for i in range(n):
        hi = (i % 2 == 1) != up_first
        m.atom(f"{p}{i}", x + i * C30, y + (-L / 2 if hi else 0))
        names.append(f"{p}{i}")
        if i:
            m.bond(names[i - 1], names[i])
    return names


def newman(f, x, y, front, back, r=19, ln=40, size=11.5, hl=(), bln=None):
    """front/back: [(각도, 라벨)] (각도: 수학 좌표, 90 = 위)"""
    f.raw(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="1.4"/>')

    def put(ang, lab, frm, ln=ln):
        a = math.radians(ang)
        c, s = math.cos(a), -math.sin(a)
        line(f, x + frm * c, y + frm * s, x + (ln - 10) * c, y + (ln - 10) * s)
        anc = "start" if c > 0.3 else ("end" if c < -0.3 else "middle")
        lx = x + ln * c + (-6 if anc == "start" else 6 if anc == "end" else 0)
        ly = y + ln * s + (0 if anc != "middle" else (-2 if s < 0 else 2))
        f.add(rich(lx, ly, lab, size=size, anchor=anc, color=RED if lab in hl else INK, halo=True))

    for ang, lab in back:
        put(ang, lab, r, bln or ln)
    for ang, lab in front:
        put(ang, lab, 0)
    f.raw(f'<circle cx="{x}" cy="{y}" r="2" fill="{INK}"/>')


def check(f, x, y, ok=True, size=15):
    f.text(x, y, "○" if ok else "✗", size=size, weight="bold", color=GREEN if ok else RED)


def cyclohexane(m, p, cx, cy, start=90):
    return m.ring(p, cx, cy, 6, L, start)


# ------------------------------------------------------------------ 21
def f21():
    f = Fig(800, 300)
    newman(f, 110, 130, [(90, "CH_3"), (210, "HO"), (330, "H")],
           [(30, "CH_3"), (150, "H"), (270, "C_2H_5")], hl=("HO",))
    f.text(110, 215, "앞 탄소 = C2 (OH, CH₃, H)", size=11.5, color=RED)
    f.text(110, 233, "뒤 탄소 = C3 (CH₃, C₂H₅, H)", size=11.5, color=BLUE)
    f.arrow(185, 130, 245, 130, "같은 분자", "지그재그")
    m = Mol()
    z = zig(m, "z", 5, up_first=False)
    # z0=C1(아래) z1=C2(위) z2=C3(아래) z3=C4 z4=C5
    m.sub("oh", "z1", 90, "OH", kind="w")
    m.sub("me", "z2", -90, None, kind="h")
    f.mol(m, 275, 140)
    for i in (0, 3, 4):
        x, y = P(m, f"z{i}", 275, 140)
        f.text(x, y + (14 if i % 2 == 0 else -12), str(i + 1), size=10, color=GRAY)
    x1, y1 = P(m, "z1", 275, 140)
    x2, y2 = P(m, "z2", 275, 140)
    f.text(x1 - 16, y1 + 2, "C2", size=10.5, color=RED, weight="bold")
    f.text(x2 + 14, y2 + 6, "C3", size=10.5, color=BLUE, weight="bold")
    f.cap(330, 250, "(2R,3S)-3-methylpentan-2-ol")
    # 판정 상자
    f.box(455, 28, 330, 250)
    f.text(468, 48, "C2 (앞 탄소)", size=12.5, anchor="start", weight="bold", color=RED)
    f.text(468, 68, "우선순위: OH ① > C3 ② > CH₃ ③ > H ④", size=11.5, anchor="start")
    f.text(468, 88, "뒤를 향한 C3(②)와 H(④, 4시)를 맞바꾸면 H가 뒤", size=11.5, anchor="start")
    f.text(468, 108, "OH(7시) → C3(4시) → CH₃(12시): 반시계 = S", size=11.5, anchor="start")
    f.text(468, 128, "교환 1회로 배열이 뒤집혔으므로 원래는 반대", size=11.5, anchor="start")
    f.text(468, 148, "⇒ C2 = R", size=12.5, anchor="start", weight="bold", color=RED)
    f.text(468, 176, "C3 (뒤 탄소)", size=12.5, anchor="start", weight="bold", color=BLUE)
    f.text(468, 196, "우선순위: C2 ① > C₂H₅ ② > CH₃ ③ > H ④", size=11.5, anchor="start")
    f.text(468, 216, "앞을 향한 C2(①)와 H(④, 10시) 교환 → H가 앞", size=11.5, anchor="start")
    f.text(468, 236, "C2(10시)→C₂H₅(6시)→CH₃(2시): 반시계 → H 앞이므로 R", size=11.5, anchor="start")
    f.text(468, 258, "교환 1회 → 원래는 S ⇒ C3 = S → 정답 ②", size=12.5, anchor="start", weight="bold", color=BLUE)
    return f.render()


def f21b():
    """④·⑤의 번호 붙이기 오류와 C2 판정 보조 그림"""
    f = Fig(800, 170)
    f.text(20, 20, "주사슬 번호: OH(주작용기)가 붙은 탄소에 낮은 번호 → pentan-2-ol (④·⑤의 ‘-4-ol’은 번호 방향이 거꾸로)", size=12, anchor="start", weight="bold")
    m = Mol()
    zig(m, "z", 5)
    m.sub("oh", "z1", 90, "OH")
    m.sub("me", "z2", -90)
    f.mol(m, 60, 100)
    for i in range(5):
        x, y = P(m, f"z{i}", 60, 100)
        dy = {0: 16, 1: 14, 2: -13, 3: -12, 4: 16}[i]
        f.text(x, y + dy, str(i + 1), size=11, color=GREEN, weight="bold")
    f.text(120, 150, "OH 위치 2 (○)", size=12, color=GREEN, weight="bold")
    m = Mol()
    zig(m, "z", 5)
    m.sub("oh", "z1", 90, "OH")
    m.sub("me", "z2", -90)
    f.mol(m, 300, 100)
    for i in range(5):
        x, y = P(m, f"z{i}", 300, 100)
        dy = {0: 16, 1: 14, 2: -13, 3: -12, 4: 16}[i]
        f.text(x, y + dy, str(5 - i), size=11, color=RED, weight="bold")
    f.text(360, 150, "OH 위치 4 (✗, 위치 번호 합 3+4 > 2+3)", size=12, color=RED, weight="bold")
    f.box(560, 45, 225, 110)
    f.text(672, 66, "Newman → R/S 요령", size=12, weight="bold")
    f.text(672, 88, "① 우선순위 매기기", size=11.5)
    f.text(672, 106, "② 최하위(H)가 앞/뒤 어디인지 확인", size=11.5)
    f.text(672, 124, "③ H가 앞을 향하면 읽은 방향을 뒤집음", size=11.5)
    f.text(672, 142, "④ 다른 기가 뒤 → 교환 1회마다 뒤집음", size=11.5)
    return f.render()


# ------------------------------------------------------------------ 22
def _conf(f, x, y, phi, size=10.5):
    front = [(90, "Me"), (210, "H"), (330, "Me")]
    ecl = abs((phi % 120)) < 1e-6
    off = -20 if ecl else 0
    base = 90 - phi + off
    back = [(base, "Me"), (base - 120, "H"), (base - 240, "H")]
    newman(f, x, y, front, back, r=17, ln=34, size=size, hl=(), bln=46 if ecl else 34)
    a = math.radians(base)
    f.raw(f'<circle cx="{x + 17 * math.cos(a):.1f}" cy="{y - 17 * math.sin(a):.1f}" r="3" fill="{RED}"/>')


def f22():
    f = Fig(800, 500)
    f.text(20, 18, "앞: C2 (Me, Me, H) 고정 · 뒤: C3 (Me, H, H)를 시계 방향으로 회전 (Me = CH₃, 빨간 점 = 뒤쪽 C3의 CH₃)", size=12, anchor="start", weight="bold")
    data = [("A", 0, "Me/Me·Me/H·H/H 가려짐"), ("B", 60, "gauche ×2"), ("C", 120, "Me/Me·Me/H·H/H 가려짐"),
            ("D", 180, "gauche ×1 (anti 1)"), ("E", 240, "Me/H ×3 가려짐")]
    E = {0: 21.0, 60: 7.6, 120: 21.0, 180: 3.8, 240: 18.0, 300: 3.8, 360: 21.0}
    for i, (lab, phi, desc) in enumerate(data):
        x = 85 + i * 157
        _conf(f, x, 110, phi)
        f.cap(x, 42, f"{lab} ({phi}°)")
        f.text(x, 168, desc, size=10.5, color=GRAY)
        f.text(x, 186, f"≈ {E[phi]:g} kJ/mol", size=11, weight="bold", color=RED if E[phi] >= 18 else GREEN)
    # 에너지 도표
    x0, x1, yb, sc = 90, 750, 470, 10.5
    X = lambda p: x0 + (x1 - x0) * p / 360
    Y = lambda e: yb - e * sc
    line(f, x0, yb, x1 + 10, yb)
    line(f, x0, yb, x0, Y(23) - 5)
    f.text(x0 + 8, Y(23) - 6, "상대 에너지 (kJ/mol)", size=11, anchor="start")
    f.text(x1 + 26, yb, "φ", size=13, italic=True)
    for p in range(0, 361, 60):
        line(f, X(p), yb, X(p), yb + 5)
        f.text(X(p), yb + 18, f"{p}°", size=10.5)
    for e in (0, 5, 10, 15, 20):
        line(f, x0 - 4, Y(e), x0, Y(e))
        f.text(x0 - 8, Y(e), str(e), size=10, anchor="end")
    pts = []
    ks = sorted(E)
    for k in range(len(ks) - 1):
        a, b = ks[k], ks[k + 1]
        for j in range(21):
            t = j / 20
            p = a + (b - a) * t
            e = E[a] + (E[b] - E[a]) * (1 - math.cos(math.pi * t)) / 2
            pts.append(f"{X(p):.1f},{Y(e):.1f}")
    f.raw(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{BLUE}" stroke-width="2"/>')
    for lab, p in [("A", 0), ("B", 60), ("C", 120), ("D", 180), ("E", 240), ("(F)", 300)]:
        f.raw(f'<circle cx="{X(p):.1f}" cy="{Y(E[p]):.1f}" r="3.5" fill="{RED}"/>')
        f.text(X(p) + (12 if p == 0 else 0), Y(E[p]) - 13, lab, size=12, weight="bold")
    line(f, X(0), Y(21), X(120), Y(21), color=RED, dash="4 3")
    f.text(X(60), Y(21) - 10, "A = C (ㄱ ○)", size=11.5, color=RED, weight="bold")
    f.text(X(240) + 14, Y(18) + 16, "E < A = C (ㄷ ✗)", size=11.5, color=RED, weight="bold", anchor="start")
    f.text(X(120), Y(5.7), "D(가장 안정) < B (ㄴ ✗)", size=11.5, color=GREEN, weight="bold")
    return f.render()


# ------------------------------------------------------------------ 23
def _pent(m, kind):
    """A: CH2=C=CH-CH2-CH3, B: (E)-CH2=CH-CH=CH-CH3, C: CH2=CH-CH2-CH=CH2"""
    if kind == "A":
        m.atom("z0", 0, 0)
        m.sub("z1", "z0", 30, "C", kind=2)
        m.sub("z2", "z1", 30, kind=2)
        m.sub("z3", "z2", -30)
        m.sub("z4", "z3", 30)
        return
    zig(m, "z", 5)
    if kind == "B":
        m.set_bond("z0", "z1", "2l")
        m.set_bond("z2", "z3", "2l")
    else:
        m.set_bond("z0", "z1", "2l")
        m.set_bond("z3", "z4", "2r")


def f23():
    f = Fig(800, 450)
    names = [("A", "1,2-pentadiene (누적, allene)"), ("B", "(E)-1,3-pentadiene (공액)"), ("C", "1,4-pentadiene (고립)")]
    for i, (k, nm) in enumerate(names):
        m = Mol()
        _pent(m, k)
        x = 90 + i * 240
        f.mol(m, x, 70)
        f.cap(x + 55, 100, k)
        f.text(x + 55, 118, nm, size=11, color=GRAY)
    f.text(400, 148, "모두 C₅H₈ (불포화도 2), 연결 순서가 다름 → 구조 이성질체 (ㄱ ○)", size=12, color=GREEN, weight="bold")
    yb, sc = 425, 0.78
    Y = lambda h: yb - h * sc
    f.text(30, 178, "수소화 반응 엔탈피 ΔH° (kJ/mol, 기체 ΔH°f로 계산한 근삿값)", size=11.5, anchor="start", weight="bold")
    line(f, 30, yb, 440, yb, w=2)
    f.text(450, yb, "n-pentane (공통 생성물, C₅H₁₂)", size=11.5, anchor="start", weight="bold")
    for x, k, h, c in [(80, "A", 288, RED), (220, "C", 253, INK), (360, "B", 225, BLUE)]:
        line(f, x - 34, Y(h), x + 34, Y(h), color=c, w=2.4)
        f.text(x + 40, Y(h), k, size=13, anchor="start", weight="bold", color=c)
        f.arrow(x, Y(h) + 3, x, yb - 3, color=c, top=None)
        f.text(x - 6, (Y(h) + yb) / 2, f"−{h}", size=11.5, anchor="end", color=c, weight="bold")
        f.text(x + 6, (Y(h) + yb) / 2 + 18, "+2 H₂", size=10.5, anchor="start", color=GRAY)
    f.text(460, 215, "A: 누적 이중 결합(중앙 sp 탄소) → 가장 불안정", size=11.5, anchor="start", color=RED)
    f.text(460, 235, "→ |ΔH°| 가장 큼: A > C > B  ⇒ ㄴ ✗", size=11.5, anchor="start", color=RED, weight="bold")
    f.text(460, 265, "C: 고립 다이엔 = 일치환 알켄 2개", size=11.5, anchor="start")
    f.text(460, 295, "B: 공액 안정화(≈ 15 kJ/mol) + 이치환 알켄", size=11.5, anchor="start", color=BLUE)
    f.text(460, 315, "→ 가장 안정, 방출 열 가장 작음", size=11.5, anchor="start", color=BLUE)
    f.text(460, 345, "같은 생성물로 가는 반응: |ΔH°| 작을수록 반응물 안정", size=11.5, anchor="start", color=GRAY)
    return f.render()


def f23b():
    f = Fig(800, 230)
    f.text(20, 18, "π 궤도의 배열: 공액(B)만 π 전자가 4중심에 비편재화 → HOMO–LUMO 간격 감소 → λmax 증가 (ㄷ ○)", size=12, anchor="start", weight="bold")
    # B: 4 parallel p orbitals
    y = 100
    xs = [60, 100, 140, 180]
    line(f, 52, y, 188, y, w=1.6)
    for i, x in enumerate(xs):
        f.porb(x, y, 1, rx=8, ry=15)
    f.text(120, 150, "B: p 궤도 4개가 모두 평행", size=11.5, weight="bold", color=BLUE)
    f.text(120, 168, "λmax ≈ 223 nm (217 + 알킬 5)", size=11.5, color=BLUE)
    # C: isolated
    xs = [290, 330, 400, 440]
    line(f, 282, y, 448, y, w=1.6)
    for x in xs:
        f.porb(x, y, 1, rx=8, ry=15)
    f.raw(f'<circle cx="365" cy="{y}" r="4" fill="#fff" stroke="{INK}"/>')
    f.text(365, 132, "sp³ CH₂", size=10.5, color=GRAY)
    f.text(365, 150, "C: sp³ 탄소가 공액을 끊음", size=11.5, weight="bold")
    f.text(365, 168, "λmax < 200 nm (에틸렌형, ~180)", size=11.5)
    # A: allene orthogonal
    cx = [560, 610, 660]
    line(f, 548, y, 672, y, w=1.6)
    f.porb(560, y, 1, rx=8, ry=15)
    f.porb(610, y, 1, rx=8, ry=15)
    for xx in (610, 660):
        f.raw(f'<ellipse cx="{xx - 9}" cy="{y}" rx="8" ry="5" fill="{ORANGE}" fill-opacity="0.75" stroke="{INK}"/>'
              f'<ellipse cx="{xx + 9}" cy="{y}" rx="8" ry="5" fill="#fff" stroke="{INK}"/>')
    f.text(610, 150, "A: 두 π 결합이 서로 직교", size=11.5, weight="bold", color=RED)
    f.text(610, 168, "공액 ✗, λmax < 200 nm", size=11.5, color=RED)
    f.text(560, 58, "C1", size=10, color=GRAY)
    f.text(610, 58, "C2(sp)", size=10, color=GRAY)
    f.text(668, 82, "C3", size=10, color=GRAY)
    f.text(400, 205, "고립(C)·누적(A) 다이엔은 π 결합이 독립 → 에틸렌 수준의 π→π* (진공 UV 영역)", size=11.5, color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 24
def _epox(m, k1, k2):
    m.atom("c2", 0, 0)
    m.atom("c3", L, 0)
    m.atom("o", L / 2, -L * 0.85, "O")
    m.bond("c2", "c3")
    m.bond("c2", "o")
    m.bond("c3", "o")
    m.sub("m2", "c2", 210, kind=k1)
    m.sub("m3", "c3", -30, kind=k2)


def _oxetane(m, kind):
    s = L * 0.9
    m.atom("c2", 0, 0)
    m.atom("c3", s, 0)
    m.atom("c4", s, s)
    m.atom("o", 0, s, "O")
    m.bond("c2", "c3")
    m.bond("c3", "c4")
    m.bond("c4", "o")
    m.bond("o", "c2")
    m.sub("me", "c2", 135, kind=kind)


def f24():
    f = Fig(800, 300)
    # A
    m = Mol()
    m.atom("a", 0, 0)
    m.sub("b", "a", 30)
    m.sub("c", "a", -90)
    m.sub("d", "a", 150)
    m.sub("o", "b", -30, "O", kind="2")
    f.mol(m, 40, 80)
    f.cap(55, 140, "A")
    f.text(55, 158, "2-methylpropanal", size=10.5, color=GRAY)
    f.eqarrow(118, 168, 80, "토토머")
    m = Mol()
    m.atom("a", 0, 0)
    m.sub("c", "a", -90)
    m.sub("d", "a", 150)
    m.sub("b", "a", 30, kind=2)
    m.sub("o", "b", -30, "OH")
    f.mol(m, 215, 80)
    f.cap(225, 140, "B")
    f.text(225, 158, "엔올 (C=C–OH)", size=10.5, color=GRAY)
    f.text(140, 190, "H의 위치 + π 결합 위치만 다름", size=11, color=GREEN)
    f.text(140, 207, "→ 빠르게 상호 변환되는 구조 이성질체 (ㄱ ○)", size=11, color=GREEN, weight="bold")
    # C, D
    m = Mol()
    _epox(m, "w", "w")
    f.mol(m, 335, 95)
    f.cap(350, 140, "C")
    f.text(350, 158, "cis (2R,3S) 메조", size=10.5, color=GRAY)
    m = Mol()
    _epox(m, "h", "w")
    f.mol(m, 445, 95)
    f.cap(460, 140, "D")
    f.text(460, 158, "trans (2S,3S) 키랄", size=10.5, color=GRAY)
    f.text(405, 190, "입체 중심 2개 중 1개만 반대", size=11, color=GREEN)
    f.text(405, 207, "→ 거울상 ✗ → 부분입체 (ㄴ ○)", size=11, color=GREEN, weight="bold")
    # E, F
    m = Mol()
    _oxetane(m, "w")
    f.mol(m, 585, 75)
    f.cap(598, 140, "E")
    f.text(598, 158, "(S)-2-methyloxetane", size=10.5, color=GRAY)
    m = Mol()
    _oxetane(m, "h")
    f.mol(m, 700, 75)
    f.cap(713, 140, "F")
    f.text(713, 158, "(R)-2-methyloxetane", size=10.5, color=GRAY)
    f.text(655, 190, "입체 중심 1개, 배열만 반대", size=11, color=GREEN)
    f.text(655, 207, "→ 거울상 (ㄷ ○)", size=11, color=GREEN, weight="bold")
    for xx in (285, 535):
        line(f, xx, 40, xx, 215, color="#cfd4db")
    f.box(20, 230, 760, 58)
    f.text(400, 249, "이성질체 판정 순서: 분자식 같음 → 연결 순서 같은가? (아니오: 구조 이성질체, 토토머 포함)", size=12)
    f.text(400, 270, "→ 예: 입체이성질체 → 겹쳐지지 않는 거울상인가? (예: 거울상이성질체 / 아니오: 부분입체이성질체, 메조 포함)", size=12)
    return f.render()


def f24b():
    """토토머화 메커니즘(산 촉매)과 C의 메조 대칭면"""
    f = Fig(800, 210)
    f.text(20, 18, "산 촉매 케토–엔올 토토머화: ① C=O 양성자화 → ② α-C–H 탈양성자화", size=12, anchor="start", weight="bold")
    m = Mol()
    m.atom("a", 0, 0)
    m.sub("ha", "a", -90, "H")
    m.sub("d", "a", 180)
    m.sub("d2", "a", 120)
    m.sub("b", "a", 30)
    m.sub("o", "b", -30, "O", kind="2")
    ox, oy = 60, 100
    f.mol(m, ox, oy)
    o = P(m, "o", ox, oy)
    f.lp(o[0] + 8, o[1] + 4, ang=-30)
    f.text(o[0] + 40, o[1] - 18, "H–A", size=12)
    f.curly(o[0] + 6, o[1] + 8, o[0] + 30, o[1] - 12, bend=0.5)
    f.arrow(160, 100, 220, 100, "H⁺")
    m = Mol()
    m.atom("a", 0, 0)
    m.sub("ha", "a", -90, "H")
    m.sub("d", "a", 180)
    m.sub("d2", "a", 120)
    m.sub("b", "a", 30)
    m.sub("o", "b", -30, "OH", kind="2")
    ox, oy = 270, 100
    f.mol(m, ox, oy)
    o = P(m, "o", ox, oy)
    f.charge(o[0] + 18, o[1] - 12)
    a, h = P(m, "a", ox, oy), P(m, "ha", ox, oy)
    b = P(m, "b", ox, oy)
    f.text(h[0] - 30, h[1] + 20, ":A⁻", size=12)
    f.curly(h[0] - 22, h[1] + 14, h[0] - 4, h[1] + 4, bend=-0.4)
    f.curly(*mid(a, h), *mid(a, b), bend=-0.6)
    f.curly(*mid(b, o, 0.5), o[0] - 4, o[1] - 10, bend=-0.6)
    f.arrow(370, 100, 430, 100, "−H⁺")
    m = Mol()
    m.atom("a", 0, 0)
    m.sub("d", "a", 180)
    m.sub("d2", "a", 120)
    m.sub("b", "a", 30, kind=2)
    m.sub("o", "b", -30, "OH")
    f.mol(m, 480, 100)
    f.text(510, 160, "B (엔올)", size=12, weight="bold")
    # 메조 대칭면
    m = Mol()
    _epox(m, "w", "w")
    f.mol(m, 655, 120)
    line(f, 670, 70, 670, 160, color=BLUE, dash="4 3")
    f.text(700, 175, "C: 거울면 존재 → 메조(비키랄)", size=11, color=BLUE)
    return f.render()


# ------------------------------------------------------------------ 25
def _tbuoh(m):
    m.atom("c", 0, 0)
    m.sub("m1", "c", 120)
    m.sub("m2", "c", 60)
    m.sub("m3", "c", 210)
    m.sub("o", "c", -30, "OH")


def _etoh(m):
    m.atom("c1", 0, 0)
    m.sub("c2", "c1", -30)
    m.sub("o", "c2", 30, "OH")


def _proh(m):
    zig(m, "z", 3)
    m.sub("o", "z2", -30, "OH")


def _cl2(m):
    m.atom("c", 0, 0)
    m.sub("me", "c", 210)
    m.sub("cl1", "c", 120, "Cl")
    m.sub("cl2", "c", 60, "Cl")
    m.sub("c1", "c", -30)
    m.sub("o", "c1", 30, "OH")


def _acac_enol(m):
    zig(m, "z", 5)
    m.sub("o", "z1", 90, "O", kind=2)
    m.sub("oh", "z3", 90, "OH")
    m.set_bond("z2", "z3", "2l")


def _hydroxyketone(m):
    zig(m, "z", 5)
    m.sub("o", "z1", 90, "O", kind=2)
    m.sub("oh", "z3", 90, "OH")


def f25():
    f = Fig(800, 430)
    rows = [
        ("ㄱ", _tbuoh, "pKₐ ≈ 18", _etoh, "pKₐ ≈ 16", False,
         "수용액: 부피 큰 t-BuO⁻는 물 분자에 둘러싸이기(용매화) 어려워 덜 안정 → EtOH가 더 강한 산"),
        ("ㄴ", _proh, "pKₐ ≈ 16", _cl2, "pKₐ ≈ 13 (추정)", False,
         "β-탄소의 Cl 2개가 유발 효과(−I)로 RO⁻의 음전하를 분산 → 오른쪽이 더 강한 산"),
        ("ㄷ", _acac_enol, "pKₐ ≈ 9", _hydroxyketone, "pKₐ ≈ 16", True,
         "왼쪽 짝염기는 음전하가 O–C=C–C=O에 비편재화(비닐로그 카복실산) → 왼쪽이 훨씬 강한 산"),
    ]
    for i, (k, lm, lp, rm, rp, ok, why) in enumerate(rows):
        y = 75 + i * 120
        f.text(25, y - 10, k, size=15, weight="bold")
        m = Mol()
        lm(m)
        f.mol(m, 110, y)
        f.text(160, y + 32, lp, size=12, weight="bold", color=BLUE)
        f.text(330, y - 8, ">", size=18, weight="bold", color=GREEN if ok else RED)
        m = Mol()
        rm(m)
        f.mol(m, 440, y)
        f.text(490, y + 32, rp, size=12, weight="bold", color=BLUE)
        check(f, 730, y - 8, ok, size=20)
        f.text(400, y + 55, why, size=11.5, color=GRAY)
        line(f, 20, y + 72, 780, y + 72, color="#e3e6ea")
    f.text(400, 418, "산의 세기 = 짝염기의 안정성: 공명 > 유발 효과 · 용매화 (기체상에서는 t-BuOH > EtOH로 순서가 뒤집힘)", size=11.5, weight="bold", color=BLUE)
    return f.render()


def _acac_anion(m, form):
    """form 0: O⁻(오른쪽), C3=C4 / 1: C3⁻ / 2: O⁻(왼쪽), C2=C3"""
    m.atom("c2", 0, 0)
    m.atom("c3", C30, L / 2)
    m.atom("c4", 2 * C30, 0)
    m.sub("c1", "c2", 210)
    m.sub("c5", "c4", -30)
    m.atom("o2", 0, -L, "O")
    m.atom("o4", 2 * C30, -L, "O")
    m.bond("c2", "o2", 1 if form == 2 else 2)
    m.bond("c4", "o4", 1 if form == 0 else 2)
    m.bond("c2", "c3", 2 if form == 2 else 1)
    m.bond("c3", "c4", 2 if form == 0 else 1)


def f25b():
    f = Fig(800, 240)
    f.text(20, 18, "ㄷ 짝염기의 공명: 음전하가 두 산소에 걸쳐 비편재화 (카복실레이트와 같은 형태, ‘비닐로그 산’)", size=12, anchor="start", weight="bold")
    oy = 130
    xs = [70, 250, 430]
    for j, ox in enumerate(xs):
        m = Mol()
        _acac_anion(m, j)
        f.mol(m, ox, oy)
        if j == 0:
            o4, c4, c3 = P(m, "o4", ox, oy), P(m, "c4", ox, oy), P(m, "c3", ox, oy)
            f.charge(o4[0] + 13, o4[1] - 8, "-")
            f.curly(o4[0] + 6, o4[1] + 8, *mid(o4, c4, 0.6), bend=-0.9)
            f.curly(*mid(c3, c4), c3[0] - 2, c3[1] + 10, bend=-0.9)
        elif j == 1:
            c3 = P(m, "c3", ox, oy)
            f.charge(c3[0], c3[1] + 16, "-")
        else:
            o2 = P(m, "o2", ox, oy)
            f.charge(o2[0] - 13, o2[1] - 8, "-")
    f.resarrow(170, 215, 120)
    f.resarrow(350, 395, 120)
    f.text(260, 190, "음전하: O · C3 · O 세 곳 (전기 음성도가 큰 O 두 곳이 주 기여)", size=11.5, color=BLUE, weight="bold")
    f.text(260, 210, "Z-엔올은 분자 내 O–H···O 수소 결합으로 안정하지만, 산도는 짝염기 공명이 결정", size=11, color=GRAY)
    f.box(565, 45, 220, 160)
    f.text(675, 66, "비교: 4-hydroxypentan-2-one", size=11.5, weight="bold")
    m = Mol()
    zig(m, "z", 5)
    m.sub("o", "z1", 90, "O", kind=2)
    m.sub("oh", "z3", 90, "O^−")
    f.mol(m, 610, 150)
    f.text(675, 175, "O⁻이 sp³ 탄소로 막혀", size=11, color=RED)
    f.text(675, 192, "C=O와 공액 ✗ → 국재화", size=11, color=RED)
    return f.render()
