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
    f.text(468, 108, "OH(8시) → C3(4시) → CH₃(12시): 반시계 = S", size=11.5, anchor="start")
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
    f.text(460, 295, "B: C보다 ≈ 28 kJ/mol 안정 (공액 + 이치환 알켄)", size=11.5, anchor="start", color=BLUE)
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


# ------------------------------------------------------------------ 의자형 (figs_u01_04와 같은 방식)
def chair_pts(R=42, h=8, t=12):
    """의자형 6개 탄소의 화면 좌표. k 짝수: 위(axial ↑), 홀수: 아래(axial ↓)."""
    ts, tc = math.sin(math.radians(t)), math.cos(math.radians(t))
    pts = []
    for k in range(6):
        th = math.radians(60 * k)
        x3, y3 = R * math.cos(th), R * math.sin(th)
        z3 = h if k % 2 == 0 else -h
        pts.append((x3, -(z3 * tc + y3 * ts), (x3, y3, z3)))
    return pts, ts, tc


def chair(f, x, y, subs=None, R=42, h=8, t=12, blen=26, size=12, hlc=None):
    """subs: {k: (axial 라벨, equatorial 라벨)} — None/'' 이면 결합 생략.
    라벨 앞에 '!'를 붙이면 빨간색."""
    subs = subs or {}
    pts, ts, tc = chair_pts(R, h, t)
    for k in range(6):
        x1, y1, _ = pts[k]
        x2, y2, _ = pts[(k + 1) % 6]
        line(f, x + x1, y + y1, x + x2, y + y2, w=1.6)
    for k, (ax, eq) in subs.items():
        px, py, (x3, y3, z3) = pts[k]
        up = 1 if z3 > 0 else -1
        for lab, vec in ((ax, (0, 0, up)), (eq, (x3 / R, y3 / R, -up * 0.33))):
            if not lab:
                continue
            n = math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)
            vx, vy, vz = (v / n for v in vec)
            dx = vx * blen
            dy = -(vz * tc + vy * ts) * blen
            col = INK
            if lab.startswith("!"):
                lab, col = lab[1:], RED
            d = math.hypot(dx, dy)
            short = 0 if lab == "·" else 9
            line(f, x + px, y + py, x + px + dx * (d - short) / d, y + py + dy * (d - short) / d, color=col)
            if lab != "·":
                anc = "middle"
                lx, ly = x + px + dx, y + py + dy
                if abs(dx) > 12:
                    anc = "start" if dx > 0 else "end"
                    lx += -6 if dx > 0 else 6
                f.add(rich(lx, ly, lab, size=size, anchor=anc, color=col, halo=True))
    return pts




# ------------------------------------------------------------------ 26
def _hex(m, p="r", dbl12=False):
    """cyclohexane, p0 위, 시계 방향. p1(오른쪽 위)·p2(오른쪽 아래)가 반응 자리"""
    r = m.ring(p, 0, 0, 6, L, 90, arom=[1] if dbl12 else None)
    return r


def _epoxide_fused(m, p="r"):
    _hex(m, p)
    m.atom("ox", 2 * C30, 0, "O")
    m.bond(f"{p}1", "ox")
    m.bond(f"{p}2", "ox")


def f26():
    f = Fig(800, 420)
    rows = [130 - 75, 195, 330]
    # ㄱ
    y = 70
    f.text(20, y, "ㄱ", size=15, weight="bold")
    m = Mol(); _hex(m); m.sub("o", "r1", 30, "O", kind=2); f.mol(m, 90, y)
    f.arrow(160, y, 270, y, "Ph₃P⁺–CH₂⁻", "Wittig")
    m = Mol(); _hex(m); m.sub("c", "r1", 30, kind=2); f.mol(m, 320, y)
    f.text(395, y - 8, "+ Ph₃P=O", size=12, anchor="start")
    f.text(395, y + 14, "알켄 (methylenecyclohexane)", size=11.5, anchor="start", color=RED)
    check(f, 755, y, False, 20)
    f.text(395, y + 48, "황 일라이드 (CH₃)₂S⁺–CH₂⁻(Corey–Chaykovsky)라면", size=11, color=GRAY, anchor="start")
    f.text(395, y + 66, "→ 스파이로 에폭사이드(1-oxaspiro[2.5]octane) →", size=11, color=GRAY, anchor="start")
    m = Mol(); _hex(m)
    m.sub("ea", "r1", 0); m.sub("eb", "r1", 60, "O"); m.bond("ea", "eb")
    f.mol(m, 680, y + 58, scale=0.8)
    line(f, 20, 165, 780, 165, color="#e3e6ea")
    # ㄴ
    y = 220
    f.text(20, y, "ㄴ", size=15, weight="bold")
    m = Mol(); _hex(m); m.sub("br", "r1", 30, "Br", kind="w"); m.sub("oh", "r2", -30, "OH", kind="h"); f.mol(m, 90, y)
    f.arrow(165, y, 225, y, "NaOH", "−H₂O")
    m = Mol(); _hex(m); m.sub("br", "r1", 30, "Br", kind="w"); m.sub("oh", "r2", -30, "O^−", kind="h"); f.mol(m, 275, y)
    f.text(300, y + 52, "알콕사이드", size=11, color=GRAY)
    f.arrow(350, y, 420, y, "분자 내 S_N2", "−Br⁻")
    m = Mol(); _epoxide_fused(m); f.mol(m, 470, y)
    f.text(545, y - 8, "cyclohexene oxide", size=11.5, anchor="start", color=GREEN, weight="bold")
    f.text(545, y + 12, "(Br과 O⁻이 trans → 뒤쪽 공격 가능)", size=11, anchor="start", color=GREEN)
    check(f, 755, y, True, 20)
    line(f, 20, 290, 780, 290, color="#e3e6ea")
    # ㄷ
    y = 350
    f.text(20, y, "ㄷ", size=15, weight="bold")
    m = Mol(); _hex(m, dbl12=True); f.mol(m, 90, y)
    f.arrow(165, y, 300, y, "mCPBA (RCO₃H)", "협동적 syn 첨가")
    m = Mol(); _epoxide_fused(m); f.mol(m, 350, y)
    f.text(425, y - 8, "cyclohexene oxide + m-ClC₆H₄CO₂H", size=11.5, anchor="start", color=GREEN, weight="bold")
    f.text(425, y + 12, "(알켄의 cis 관계 유지, 입체 특이적)", size=11, anchor="start", color=GREEN)
    check(f, 755, y, True, 20)
    return f.render()


def f26b():
    f = Fig(800, 300)
    f.text(20, 18, "ㄴ: 분자 내 Williamson(S_N2) — O⁻와 C–Br이 anti-periplanar(이축 배향)일 때만 뒤쪽 공격", size=12, anchor="start", weight="bold")
    x, y = 120, 150
    pts = chair(f, x, y, {0: ("O^−", ""), 5: ("Br", "")}, size=12, R=50, h=16, t=25)
    o = (x + pts[0][0], y + pts[0][1] - 26)
    c2 = (x + pts[5][0], y + pts[5][1])
    br = (x + pts[5][0], y + pts[5][1] + 26)
    f.curly(o[0] - 10, o[1] + 2, c2[0] - 4, c2[1] - 6, bend=0.5)
    f.curly(c2[0] - 3, c2[1] + 9, br[0] - 12, br[1] - 4, bend=0.6)
    f.text(x + 10, y + 95, "C1–O⁻(축 ↑) · C2–Br(축 ↓): 180°", size=11, color=BLUE)
    f.text(x + 10, y + 112, "trans-1,2 → 이축 의자형에서 반응", size=11, color=BLUE)
    f.arrow(240, 150, 300, 150, "", "")
    m = Mol(); _epoxide_fused(m); f.mol(m, 330, 150)
    f.text(360, 200, "에폭사이드 (C1·C2 cis 접합)", size=11, color=GREEN)
    line(f, 440, 40, 440, 290, color="#e3e6ea")
    # mCPBA butterfly
    f.text(455, 45, "ㄷ: 과산(peroxy acid)의 협동 메커니즘", size=12, anchor="start", weight="bold")
    ox, oy = 480, 165
    m = Mol()
    m.atom("c1", 0, -16); m.atom("c2", 0, 16); m.bond("c1", "c2", 2)
    m.atom("od", 55, 0, "O"); m.atom("h", 80, -32, "H"); m.atom("oc", 130, -30, "O")
    m.atom("cc", 145, 2); m.atom("op", 105, 28, "O"); m.atom("ar", 180, 20, "Ar")
    m.bond("od", "h"); m.bond("h", "oc", "dash"); m.bond("oc", "cc", 2); m.bond("cc", "op"); m.bond("op", "od"); m.bond("cc", "ar")
    f.mol(m, ox, oy)
    c1, c2 = P(m, "c1", ox, oy), P(m, "c2", ox, oy)
    od, h, oc, cc, op = (P(m, k, ox, oy) for k in ("od", "h", "oc", "cc", "op"))
    f.curly(c1[0] + 3, c1[1] + 4, od[0] - 9, od[1] - 4, bend=-0.45)
    f.curly(*mid(od, op), op[0] - 4, op[1] - 10, bend=0.6)
    f.curly(*mid(oc, cc), oc[0] + 9, oc[1] - 4, bend=0.6)
    f.curly(*mid(od, h), od[0] - 6, od[1] + 10, bend=0.9)
    f.text(615, 220, "① π(C=C) → O(원위)  ② O–O 결합 → C=O", size=11, color=GRAY)
    f.text(615, 238, "③ C=O π → O–H  ④ O–H → 두 번째 C–O", size=11, color=GRAY)
    f.text(615, 262, "한 단계(협동) → syn 첨가, 입체 보존", size=11.5, color=GREEN, weight="bold")
    return f.render()


# ------------------------------------------------------------------ 27
def _hexpos(cx, cy, r=L):
    return [(cx + r * math.cos(math.radians(90 - 60 * i)), cy - r * math.sin(math.radians(90 - 60 * i))) for i in range(6)]


def _cyc(f, ox, oy, bonds, labels=None, subs=None, r=L):
    """육각 배치 원자 v0..v5 사이에 bonds=[(i,j,kind)]만 그림"""
    m = Mol()
    for i, (x, y) in enumerate(_hexpos(0, 0, r)):
        m.atom(f"v{i}", x, y, (labels or {}).get(i))
    for i, j, k in bonds:
        m.bond(f"v{i}", f"v{j}", k if k != "in" else "in", (0, 0) if k == "in" else None)
    for (i, ang, lab, k) in (subs or []):
        m.sub(f"s{i}{ang}", f"v{i}", ang, lab, kind=k)
    f.mol(m, ox, oy)
    return [P(m, f"v{i}", ox, oy) for i in range(6)]


def f27():
    f = Fig(800, 470)
    f.text(20, 18, "굽은 화살표로 본 세 고리형 협동 반응 (모두 6개 전자 · 6중심 고리 전이 상태, 열 허용)", size=12, anchor="start", weight="bold")
    # ㄱ 6π 전자 고리화
    y = 95
    f.text(20, y, "ㄱ", size=15, weight="bold")
    v = _cyc(f, 100, y, [(0, 1, "in"), (5, 0, 1), (4, 5, "in"), (3, 4, 1), (2, 3, "in")])
    f.curly(*mid(v[0], v[1]), *mid(v[5], v[0]), bend=-0.9)
    f.curly(*mid(v[4], v[5]), *mid(v[3], v[4]), bend=-0.9)
    f.curly(*mid(v[2], v[3]), *mid(v[1], v[2], 0.5), bend=-0.9)
    f.arrow(165, y, 255, y, "Δ", "")
    _cyc(f, 310, y, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, "in"), (4, 5, 1), (5, 0, "in")])
    f.text(370, y - 10, "1,3-cyclohexadiene", size=11.5, anchor="start", weight="bold", color=GREEN)
    f.text(370, y + 10, "6π 전자 고리화: 열 → 반대 방향 회전(dis)", size=11, anchor="start")
    f.text(370, y + 28, "π 결합 3 → π 2 + σ 1 (σ가 더 강해 발열)", size=11, anchor="start", color=GRAY)
    check(f, 755, y, True, 20)
    line(f, 20, 160, 780, 160, color="#e3e6ea")
    # ㄴ Claisen
    y = 235
    f.text(20, y, "ㄴ", size=15, weight="bold")
    v = _cyc(f, 100, y, [(0, 1, "in"), (5, 0, 1), (4, 5, 1), (3, 4, 1), (2, 3, "in")], labels={5: "O"})
    f.curly(*mid(v[0], v[1]), *mid(v[1], v[2]), bend=0.9)
    f.curly(*mid(v[4], v[5]), *mid(v[5], v[0]), bend=0.9)
    f.curly(*mid(v[2], v[3]), *mid(v[3], v[4]), bend=0.9)
    f.arrow(165, y, 255, y, "Δ", "[3,3]")
    _cyc(f, 310, y, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, "in"), (5, 0, "in")], labels={5: "O"})
    f.text(370, y - 10, "pent-4-enal (γ,δ-불포화 알데하이드)", size=11.5, anchor="start", weight="bold", color=GREEN)
    f.text(370, y + 10, "Claisen 자리옮김: C–O σ 끊김, C–C σ 생성", size=11, anchor="start")
    f.text(370, y + 28, "C=O(강함) 생성이 원동력 → 비가역", size=11, anchor="start", color=GRAY)
    check(f, 755, y, True, 20)
    line(f, 20, 300, 780, 300, color="#e3e6ea")
    # ㄷ Diels-Alder
    y = 385
    f.text(20, y, "ㄷ", size=15, weight="bold")
    pos = _hexpos(0, 0, 34)
    m = Mol()
    for i in (0, 5, 4, 3):
        m.atom(f"v{i}", *pos[i])
    m.bond("v0", "v5", "2r"); m.bond("v5", "v4"); m.bond("v4", "v3", "2r")
    m.atom("v1", pos[1][0] + 14, pos[1][1]); m.atom("v2", pos[2][0] + 14, pos[2][1]); m.bond("v1", "v2", 3)
    m.sub("cn1", "v1", 60, "CN"); m.sub("cn2", "v2", -60, "CN")
    ox, oy = 95, y
    f.mol(m, ox, oy)
    v = {k: P(m, f"v{k}", ox, oy) for k in range(6)}
    f.curly(*mid(v[0], v[5]), *mid(v[0], v[1]), bend=-0.7)
    f.curly(v[1][0] + 3, (v[1][1] + v[2][1]) / 2, *mid(v[2], v[3]), bend=-0.7)
    f.curly(*mid(v[4], v[3]), *mid(v[4], v[5]), bend=-0.9)
    f.arrow(185, y, 255, y, "Δ", "[4+2]")
    _cyc(f, 310, y, [(0, 1, 1), (1, 2, "in"), (2, 3, 1), (3, 4, 1), (4, 5, "in"), (5, 0, 1)],
         subs=[(1, 30, "CN", 1), (2, -30, "CN", 1)])
    f.text(390, y - 10, "1,2-dicyanocyclohexa-1,4-diene", size=11.5, anchor="start", weight="bold", color=GREEN)
    f.text(390, y + 10, "Diels–Alder: 다이엔 HOMO + 친다이엔체 LUMO", size=11, anchor="start")
    f.text(390, y + 28, "알카인 친다이엔체 → 1,4-다이엔 (CN = EWG, 반응 빠름)", size=11, anchor="start", color=GRAY)
    check(f, 755, y, True, 20)
    return f.render()


def f27b():
    """FMO: 헥사트라이엔 ψ3(dis), DA HOMO–LUMO"""
    f = Fig(800, 210)
    f.text(20, 18, "궤도 대칭으로 본 열 허용 조건", size=12, anchor="start", weight="bold")
    y = 100
    xs = [60, 95, 130, 165, 200, 235]
    line(f, 52, y, 243, y, w=1.6)
    for x, ph in zip(xs, [1, 1, -1, -1, 1, 1]):
        f.porb(x, y, ph, rx=8, ry=15)
    f.text(148, 150, "헥사트라이엔 HOMO ψ₃: 말단 위상 같음", size=11.5, weight="bold")
    f.text(148, 168, "→ 반대 방향 회전(dis)으로 같은 위상끼리 겹침", size=11.5, color=BLUE)
    f.rotarrow(60, 52, cw=True, r=9)
    f.rotarrow(235, 52, cw=False, r=9)
    # DA
    xs = [470, 505, 540, 575]
    line(f, 462, 80, 583, 80, w=1.6)
    for x, ph in zip(xs, [1, 1, -1, -1]):
        f.porb(x, 80, ph, rx=8, ry=13)
    f.text(600, 80, "다이엔 HOMO ψ₂", size=11.5, anchor="start")
    line(f, 497, 150, 548, 150, w=1.6)
    for x, ph in zip((505, 540), (1, -1)):
        f.porb(x, 150, ph, rx=8, ry=13)
    f.text(600, 150, "친다이엔체 LUMO π*", size=11.5, anchor="start")
    for x1, x2 in ((470, 505), (575, 540)):
        line(f, x1, 108, x2, 122, color=RED, dash="4 3")
    f.text(600, 115, "양 끝 위상 일치 → [4+2] 허용", size=11.5, anchor="start", color=RED)
    f.text(400, 198, "Claisen [3,3]도 6전자 방향족성(Hückel) 의자형 전이 상태 → 열 허용", size=11.5, color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 28
def _ph_chain(m, n=3, co=False, br=False, pbr=False):
    benzene(m, "r", 0, 0, 90)
    prev = "r1"
    angs = [30, -30, 30, -30]
    for i in range(n):
        prev = m.sub(f"c{i}", prev, angs[i])
    if co:
        m.sub("o", "c0", 90, "O", kind=2)
    if br:
        m.sub("br", "c0", 90, "Br")
    if pbr:
        m.sub("pbr", "r4", 210, "Br")
    return m


def f28():
    f = Fig(800, 330)
    y = 90
    m = Mol(); benzene(m, "r", 0, 0, 90); f.mol(m, 50, y)
    f.arrow(95, y, 215, y, "EtCOCl, AlCl₃", "F–C 아실화")
    m = Mol(); _ph_chain(m, 3, co=True); f.mol(m, 265, y)
    f.cap(320, y + 48, "A = propiophenone (ㄱ ○)", color=GREEN)
    f.arrow(410, y, 530, y, "(가) H₂NNH₂, KOH", "가열")
    m = Mol(); _ph_chain(m, 3); f.mol(m, 580, y)
    f.cap(635, y + 48, "propylbenzene", color=INK)
    f.text(635, y + 68, "Wolff–Kishner: C=O → CH₂ (ㄴ ○)", size=11.5, color=GREEN, weight="bold")
    line(f, 20, 175, 780, 175, color="#e3e6ea")
    y = 250
    m = Mol(); _ph_chain(m, 3); f.mol(m, 50, y)
    f.arrow(160, y, 270, y, "NBS, hν", "벤질 위치 라디칼")
    m = Mol(); _ph_chain(m, 3, br=True); f.mol(m, 315, y)
    f.cap(370, y + 50, "B = (1-bromopropyl)benzene (라셈)", color=GREEN)
    f.text(445, y - 40, "벤질 C–H만 선택적", size=11, anchor="start", color=GRAY)
    f.text(445, y - 24, "(BDE ≈ 356 kJ/mol)", size=11, anchor="start", color=GRAY)
    f.box(585, 195, 200, 125, fill="#fdf1f0", stroke="#e8b4ae")
    m = Mol(); _ph_chain(m, 3, pbr=True); f.mol(m, 635, 255, scale=0.85)
    f.text(685, 210, "제시된 B (✗)", size=11.5, weight="bold", color=RED)
    f.text(685, 308, "고리 브로민화 = Br₂/FeBr₃ (SEAr)", size=10.5, color=RED)
    return f.render()


def f28b():
    f = Fig(800, 290)
    f.text(20, 18, "① 아실륨 이온: 공명 안정화 → 자리옮김 없음 / ② 벤질 라디칼: 고리와 공명 → NBS가 저농도 Br₂ 공급", size=12, anchor="start", weight="bold")
    # acylium
    m = Mol(); m.atom("et", 0, 0, "Et"); m.sub("c", "et", 0, "C"); m.sub("o", "c", 0, "O^+", kind=3)
    f.mol(m, 40, 80)
    f.resarrow(130, 165, 80)
    m = Mol(); m.atom("et", 0, 0, "Et"); m.sub("c", "et", 0, "C^+"); m.sub("o", "c", 0, "O", kind=2)
    f.mol(m, 185, 80)
    f.text(150, 115, "Cl–C(=O)Et + AlCl₃ → EtC≡O⁺ + AlCl₄⁻", size=11, color=GRAY)
    f.text(150, 133, "생성물 케톤은 고리를 불활성화 → 일치환에서 멈춤", size=11, color=GRAY)
    f.text(150, 151, "알킬화(1-chloropropane)였다면 1°→2° 자리옮김 → cumene", size=11, color=RED)
    line(f, 320, 40, 320, 280, color="#e3e6ea")
    # radical chain
    f.text(340, 50, "개시: Br₂ —hν→ 2 Br•", size=11.5, anchor="start")
    f.text(340, 72, "전파 1: PhCH₂Et + Br• → PhĊHEt + HBr", size=11.5, anchor="start")
    f.text(340, 94, "전파 2: PhĊHEt + Br₂ → PhCHBrEt + Br•", size=11.5, anchor="start")
    f.text(340, 116, "NBS + HBr → 숙신이미드 + Br₂ (낮은 농도 유지)", size=11.5, anchor="start", color=BLUE)
    m = Mol(); benzene(m, "r", 0, 0, 90); m.sub("c", "r1", 30); m.sub("e", "c", -30)
    ox, oy = 380, 215
    f.mol(m, ox, oy)
    c = P(m, "c", ox, oy)
    f.raw(f'<circle cx="{c[0]:.1f}" cy="{c[1] - 8:.1f}" r="2.4" fill="{RED}"/>')
    r1, r0, r2 = P(m, "r1", ox, oy), P(m, "r0", ox, oy), P(m, "r2", ox, oy)
    f.curly(c[0] + 2, c[1] - 10, *mid(c, r1), bend=-0.8, half=True)
    f.curly(*mid(r1, r0, 0.5), *mid(c, r1, 0.4), bend=0.8, half=True)
    f.curly(*mid(r1, r0, 0.5), r0[0] + 2, r0[1] - 10, bend=-0.6, half=True)
    f.resarrow(470, 510, 215)
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.set_bond("r2", "r3", "in", (0, 0)); m.set_bond("r4", "r5", "in", (0, 0))
    m.sub("c", "r1", 30, kind=2); m.sub("e", "c", -30)
    ox2 = 560
    f.mol(m, ox2, oy)
    r0b = P(m, "r0", ox2, oy)
    f.raw(f'<circle cx="{r0b[0]:.1f}" cy="{r0b[1] - 8:.1f}" r="2.4" fill="{RED}"/>')
    f.text(668, 196, "홀전자: 벤질 C와", size=11, anchor="start")
    f.text(668, 212, "o·p 탄소에 비편재화", size=11, anchor="start")
    f.text(668, 232, "→ Br은 벤질 C에", size=11, anchor="start", color=GREEN)
    f.text(560, 275, "(낚싯바늘 화살표 = 전자 1개 이동)", size=10.5, color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 29
R5 = L / (2 * math.sin(math.radians(36)))


def _lactam(m, co=True, nlabel="NH", oform="O", iminium=False):
    m.ring("p", 0, 0, 5, R5, 90)
    m.label("p1", nlabel)
    if co:
        m.sub("o", "p0", 126, oform, kind=2)
    if iminium:
        m.set_bond("p0", "p1", "2l")
    return m


def f29():
    f = Fig(800, 430)
    # ㄱ
    y = 75
    f.text(20, y, "ㄱ", size=15, weight="bold")
    m = Mol(); _lactam(m); f.mol(m, 80, y)
    f.arrow(125, y, 240, y, "1. LiAlH₄", "2. H₂O")
    m = Mol(); _lactam(m, co=False); f.mol(m, 285, y)
    f.text(330, y - 8, "pyrrolidine (고리형 아민)", size=11.5, anchor="start", color=GREEN, weight="bold")
    f.text(330, y + 12, "아마이드 C=O → CH₂ (C–N 유지, 고리 그대로)", size=11, anchor="start")
    f.text(330, y + 30, "제시된 H₂N(CH₂)₄OH: 고리가 열린 구조 ✗", size=11, anchor="start", color=RED)
    check(f, 755, y, False, 20)
    line(f, 20, 130, 780, 130, color="#e3e6ea")
    # ㄴ
    y = 205
    f.text(20, y, "ㄴ", size=15, weight="bold")
    m = Mol(); benzene(m, "r", 0, 0, 90); m.sub("c", "r1", 30); m.sub("n", "c", 30, "N", kind=3); f.mol(m, 65, y)
    f.arrow(160, y, 235, y, "CH₃MgBr", "")
    m = Mol(); benzene(m, "r", 0, 0, 90); m.sub("c", "r1", 30); m.sub("n", "c", 90, "N^−MgBr^+", kind=2); m.sub("me", "c", -30)
    f.mol(m, 280, y)
    f.text(335, y + 50, "이민 음이온 염 (C=N⁻: 두 번째 첨가 ✗)", size=10.5, color=GRAY)
    f.arrow(395, y, 470, y, "H₃O⁺", "가수분해")
    m = Mol(); benzene(m, "r", 0, 0, 90); m.sub("c", "r1", 30); m.sub("o", "c", 90, "O", kind=2); m.sub("me", "c", -30)
    f.mol(m, 515, y)
    f.text(640, y - 8, "acetophenone", size=11.5, anchor="start", color=GREEN, weight="bold")
    f.text(640, y + 12, "(제시 구조와 같음)", size=11, anchor="start", color=GREEN)
    check(f, 755, y, True, 20)
    line(f, 20, 275, 780, 275, color="#e3e6ea")
    # ㄷ
    y = 350
    f.text(20, y, "ㄷ", size=15, weight="bold")
    m = Mol(); m.ring("r", 0, 0, 6, L, 0); m.sub("c", "r0", 30); m.sub("o", "c", 90, "O", kind=2); m.sub("cl", "c", -30, "Cl")
    f.mol(m, 65, y)
    f.arrow(160, y, 270, y, "1. (CH₃)₂CuLi", "2. H₂O")
    m = Mol(); m.ring("r", 0, 0, 6, L, 0); m.sub("c", "r0", 30); m.sub("o", "c", 90, "O", kind=2); m.sub("me", "c", -30)
    f.mol(m, 310, y)
    f.text(420, y - 18, "1-cyclohexylethan-1-one (케톤에서 멈춤)", size=11.5, anchor="start", color=GREEN, weight="bold")
    f.text(420, y + 2, "큐프레이트: 산 염화물과만 반응, 케톤과는 거의 ✗", size=11, anchor="start")
    f.text(420, y + 22, "제시된 3차 알코올 = CH₃MgBr(과량)일 때 ✗", size=11, anchor="start", color=RED)
    check(f, 755, y, False, 20)
    return f.render()


def f29b():
    f = Fig(800, 250)
    f.text(20, 18, "ㄱ LiAlH₄의 아마이드(락탐) 환원: 산소가 알루미네이트로 떨어지고 이미늄을 거쳐 아민", size=12, anchor="start", weight="bold")
    y = 120
    m = Mol(); _lactam(m); f.mol(m, 70, y)
    o = P(m, "o", 70, y); c = P(m, "p0", 70, y)
    f.text(c[0] + 40, c[1] - 32, "H–AlH₃⁻", size=11)
    f.curly(c[0] + 26, c[1] - 26, c[0] + 4, c[1] - 6, bend=0.5)
    f.curly(*mid(c, o), o[0] - 10, o[1] + 4, bend=0.7)
    f.arrow(130, y, 180, y)
    m = Mol(); _lactam(m, oform="OAlH_3^−"); m.set_bond("p0", "o", 1); m.sub("h", "p0", 54, "H")
    ox = 235
    f.mol(m, ox, y)
    n = P(m, "p1", ox, y); c = P(m, "p0", ox, y); o = P(m, "o", ox, y)
    f.curly(n[0] - 2, n[1] - 10, *mid(n, c), bend=0.7)
    f.curly(*mid(c, o), o[0] + 4, o[1] + 10, bend=-0.6)
    f.text(ox, y + 50, "사면체 중간체", size=11, color=GRAY)
    f.arrow(300, y, 365, y, "−‾OAlH₂", "")
    m = Mol(); _lactam(m, co=False, nlabel="NH^+", iminium=True)
    f.mol(m, 410, y)
    c = P(m, "p0", 410, y)
    f.text(c[0] - 34, c[1] - 30, "H–AlH₃⁻", size=11)
    f.curly(c[0] - 18, c[1] - 22, c[0] - 3, c[1] - 6, bend=-0.5)
    f.text(410, y + 50, "이미늄 이온", size=11, color=GRAY)
    f.arrow(470, y, 530, y)
    m = Mol(); _lactam(m, co=False); f.mol(m, 575, y)
    f.text(575, y + 50, "pyrrolidine", size=11.5, color=GREEN, weight="bold")
    f.text(400, 215, "에스터는 OR가 떨어져 알데하이드 → 1° 알코올(C–O 절단), 아마이드는 O가 떨어져 아민(C–N 유지)", size=11.5, color=BLUE)
    f.text(400, 235, "이유: N 비공유쌍이 O보다 잘 밀어 주고, R₂N⁻는 매우 나쁜 이탈기", size=11, color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 30
def _acyl(m, n):
    """n개 탄소 사슬, 마지막 탄소가 C=O(위). 반환: 카보닐 탄소 이름"""
    z = zig(m, "z", n, up_first=((n - 1) % 2 == 0))
    m.sub("o", z[-1], 90, "O", kind=2)
    return z[-1]


def _ester_tail(m, c, r="Et"):
    o = m.sub("eo", c, -30, "O")
    a = m.sub("e1", o, 30)
    if r == "Et":
        m.sub("e2", a, -30)


def _cy_acyl(m, ch2=False):
    m.ring("r", 0, 0, 6, L, 0)
    prev = "r0"
    if ch2:
        prev = m.sub("m", prev, -30)
        c = m.sub("c", prev, 30)
    else:
        c = m.sub("c", prev, 30)
    m.sub("o", c, 90, "O", kind=2)
    return c


def f30():
    f = Fig(800, 470)
    f.text(20, 18, "에스터 + 친핵체: 친핵성 아실 치환 (첨가–제거) — 실제 주생성물", size=12, anchor="start", weight="bold")
    rows = []
    # ①
    y = 70
    f.text(20, y, "①", size=14, weight="bold")
    m = Mol(); c = _cy_acyl(m, ch2=True); _ester_tail(m, c, "Me"); f.mol(m, 70, y, scale=0.85)
    f.arrow(215, y, 285, y, "NH₃", "")
    m = Mol(); c = _cy_acyl(m, ch2=True); m.sub("n", c, -30, "NH_2"); f.mol(m, 320, y, scale=0.85)
    f.text(470, y, "아마이드 + CH₃OH (아민 분해)", size=11.5, anchor="start", color=GREEN)
    check(f, 755, y, True, 18)
    # ②
    y = 155
    f.text(20, y, "②", size=14, weight="bold")
    m = Mol(); c = _acyl(m, 4); _ester_tail(m, c); f.mol(m, 50, y + 10, scale=0.85)
    f.arrow(215, y, 285, y, "1. NaOH, Δ", "2. H₃O⁺")
    m = Mol(); c = _acyl(m, 4); m.sub("oh", c, -30, "OH"); f.mol(m, 320, y + 10, scale=0.85)
    f.text(470, y, "butanoic acid + EtOH (비누화 → 산성화)", size=11.5, anchor="start", color=GREEN)
    check(f, 755, y, True, 18)
    # ③
    y = 240
    f.text(20, y, "③", size=14, weight="bold")
    m = Mol(); c = _acyl(m, 4); _ester_tail(m, c, "Me"); f.mol(m, 50, y + 10, scale=0.85)
    f.arrow(215, y, 285, y, "1. CH₃MgBr(과량)", "2. H₃O⁺")
    m = Mol(); z = zig(m, "z", 4); m.sub("a", "z3", 90); m.sub("b", "z3", 30); m.sub("oh", "z3", -30, "OH")
    f.mol(m, 320, y + 10, scale=0.85)
    f.text(470, y, "2-methylpentan-2-ol (케톤 경유, 2당량 첨가)", size=11.5, anchor="start", color=GREEN)
    check(f, 755, y, True, 18)
    # ④
    y = 325
    f.box(12, y - 42, 776, 84, fill="#fdf1f0", stroke="#e8b4ae")
    f.text(20, y, "④", size=14, weight="bold", color=RED)
    m = Mol(); c = _acyl(m, 3); _ester_tail(m, c); f.mol(m, 50, y + 10, scale=0.85)
    f.arrow(215, y, 285, y, "1. LiAlH₄(과량)", "2. H₂O")
    m = Mol(); zig(m, "z", 3); m.sub("oh", "z2", 30, "OH"); f.mol(m, 305, y + 8, scale=0.85)
    f.text(385, y, "+", size=14)
    m = Mol(); zig(m, "z", 2); m.sub("oh", "z1", -30, "OH"); f.mol(m, 400, y + 2, scale=0.85)
    f.text(560, y - 10, "propan-1-ol + ethanol", size=11.5, anchor="start", color=RED, weight="bold")
    f.text(560, y + 10, "제시된 에터(C–O–C)는 생기지 않음", size=11, anchor="start", color=RED)
    check(f, 755, y, False, 18)
    # ⑤
    y = 415
    f.text(20, y, "⑤", size=14, weight="bold")
    m = Mol(); c = _cy_acyl(m); _ester_tail(m, c); f.mol(m, 70, y + 4, scale=0.85)
    f.arrow(215, y, 285, y, "1. DIBAH (−78 ℃)", "2. H₂O")
    m = Mol(); c = _cy_acyl(m); m.sub("h", c, -30, "H"); f.mol(m, 330, y + 4, scale=0.85)
    f.text(470, y, "cyclohexanecarbaldehyde (1당량, 저온)", size=11.5, anchor="start", color=GREEN)
    check(f, 755, y, True, 18)
    return f.render()


def f30b():
    f = Fig(800, 260)
    f.text(20, 18, "④ LiAlH₄ 환원: H⁻ 첨가 → EtO⁻ 이탈(알데하이드) → 두 번째 H⁻ 첨가 → 1° 알콕사이드 → H₂O", size=12, anchor="start", weight="bold")
    y = 110

    def tet(ox, lab_o="O", lab_h=None, carbonyl=True, tail=True, h2=False):
        m = Mol()
        m.atom("et", 0, 0, "Et")
        c = m.sub("c", "et", 0)
        m.sub("o", c, 90, lab_o, kind=2 if carbonyl else 1)
        if tail:
            m.sub("or", c, 0, "OEt")
        if lab_h:
            m.sub("h", c, -90, "H")
        if h2:
            m.sub("h2", c, 0, "H")
        f.mol(m, ox, y)
        return m

    m = tet(40)
    o, c = P(m, "o", 40, y), P(m, "c", 40, y)
    f.text(c[0] - 6, c[1] + 42, "H–AlH₃⁻", size=11)
    f.curly(c[0] - 8, c[1] + 32, c[0] - 2, c[1] + 6, bend=0.5)
    f.curly(*mid(c, o), o[0] + 9, o[1] + 2, bend=-0.7)
    f.arrow(135, y, 175, y)
    m = tet(195, "O^−", lab_h=True, carbonyl=False)
    o, c, orr = P(m, "o", 195, y), P(m, "c", 195, y), P(m, "or", 195, y)
    f.curly(o[0] - 10, o[1] + 2, c[0] - 4, c[1] - 8, bend=-0.6)
    f.curly(*mid(c, orr), orr[0] + 2, orr[1] + 12, bend=0.7)
    f.arrow(290, y, 335, y, "−EtO⁻", "")
    m = tet(355, tail=False, h2=True)
    f.text(390, y + 45, "알데하이드 (에스터보다 반응성 큼)", size=10.5, color=GRAY)
    f.arrow(430, y, 480, y, "H⁻", "")
    m = Mol(); m.atom("et", 0, 0, "Et"); c = m.sub("c", "et", 0, "CH_2"); m.sub("o", c, 0, "O^−"); f.mol(m, 500, y)
    f.arrow(590, y, 640, y, "H₂O", "")
    f.text(650, y - 8, "CH₃CH₂CH₂OH", size=12, anchor="start", weight="bold", color=GREEN)
    f.text(650, y + 12, "+ CH₃CH₂OH", size=12, anchor="start", weight="bold", color=GREEN)
    f.box(20, 175, 760, 72)
    f.text(400, 196, "DIBAH(⑤): −78 ℃에서 Al에 배위된 사면체 중간체가 안정 → 무너지지 않음 → 처리(H₂O) 후 알데하이드", size=11.5)
    f.text(400, 218, "LiAlH₄: 중간체가 바로 무너져 알데하이드 생성 → 더 빠르게 환원 → 알데하이드에서 멈출 수 없음", size=11.5)
    f.text(400, 238, "에스터 C–O(acyl–O)만 끊기므로 R–O–R′ 에터는 원리상 생길 수 없음", size=11.5, color=RED)
    return f.render()
