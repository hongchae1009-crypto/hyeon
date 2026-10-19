"""MDEET 2024 자연과학Ⅱ 유기화학 21–30번 해설 그림."""
import math
from chemsvg import Mol, Fig, benzene, L, RED, BLUE, INK

GREEN = "#2f7d5b"
GRAY = "#5b6270"
R5 = L / (2 * math.sin(math.radians(36)))   # 오각형 외접원 반지름 (변 = L)
R4 = L / math.sqrt(2)                         # 정사각형


# ------------------------------------------------------------------ 공용 헬퍼
def P(m, name, ox, oy, s=1.0):
    x, y = m.pos(name)
    return ox + s * x, oy + s * y


def mid(p, q, t=0.5):
    return p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t


def ok(f, x, y, text, good=True, size=12, anchor="middle"):
    f.text(x, y, ("○ " if good else "✗ ") + text, size=size, anchor=anchor,
           color=BLUE if good else RED, weight="bold")


def line(f, x1, y1, x2, y2, color=INK, w=1.4, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    f.raw(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
          f'stroke-width="{w}" stroke-linecap="round"{d}/>')


def newman(f, cx, cy, front, back, r=19, color_map=None):
    """front/back: [(각도, 라벨)] (각도: 0=오른쪽, 90=위)"""
    color_map = color_map or {}
    for ang, lab in back:
        a = math.radians(ang)
        c, s = math.cos(a), -math.sin(a)
        line(f, cx + r * c, cy + r * s, cx + (r + 13) * c, cy + (r + 13) * s)
    f.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="1.4"/>')
    for ang, lab in front:
        a = math.radians(ang)
        c, s = math.cos(a), -math.sin(a)
        line(f, cx, cy, cx + (r + 13) * c, cy + (r + 13) * s)
    for ang, lab in front + back:
        a = math.radians(ang)
        c, s = math.cos(a), -math.sin(a)
        d = r + 22 if len(lab) <= 1 else r + 20
        anc = "start" if c > 0.3 else ("end" if c < -0.3 else "middle")
        x = cx + d * c + (-6 if anc == "start" else (6 if anc == "end" else 0))
        y = cy + d * s + (0 if anc != "middle" else (4 if s > 0 else -4))
        f.text(x, y, lab, size=12.5, anchor=anc, color=color_map.get(lab, INK))


def fischer(f, cx, cy, top, bot, left, right, arm=34, hl=None):
    hl = hl or {}
    line(f, cx, cy - arm, cx, cy + arm)
    line(f, cx - arm, cy, cx + arm, cy)
    f.text(cx, cy - arm - 10, top, size=12.5, color=hl.get(top, INK))
    f.text(cx, cy + arm + 11, bot, size=12.5, color=hl.get(bot, INK))
    f.text(cx - arm - 4, cy, left, size=12.5, anchor="end", color=hl.get(left, INK))
    f.text(cx + arm + 4, cy, right, size=12.5, anchor="start", color=hl.get(right, INK))


def cyclohexane(m, p, cx, cy, start=0):
    return m.ring(p, cx, cy, 6, L, start)


# ------------------------------------------------------------------ 21
def _cot_tub():
    """D2d 통(tub) 모양 COT 3차원 좌표 → 2차원 투영"""
    z = 0.55
    pts = [(0.67, 1.55, z), (-0.67, 1.55, z), (-1.55, 0.67, -z), (-1.55, -0.67, -z),
           (-0.67, -1.55, z), (0.67, -1.55, z), (1.55, -0.67, -z), (1.55, 0.67, -z)]
    th = math.radians(35)   # 비스듬히 옆에서 봄
    ph = math.radians(8)
    out = []
    for x, y, z in pts:
        x1 = x * math.cos(ph) - y * math.sin(ph)
        y1 = x * math.sin(ph) + y * math.cos(ph)
        y2 = y1 * math.cos(th) - z * math.sin(th)
        z2 = y1 * math.sin(th) + z * math.cos(th)
        out.append((x1 * 28, -z2 * 28, y2))
    return out


def f21():
    f = Fig(800, 300)
    f.text(20, 20, "21  A·B·C의 실제(가장 안정한) 구조 — 정답 ② ㄴ", size=13, anchor="start", weight="bold")
    # A: 직사각형 cyclobutadiene
    m = Mol()
    for n, (x, y) in zip("abcd", [(-24, -16), (24, -16), (24, 16), (-24, 16)]):
        m.atom(n, x, y)
    m.bond("a", "b", "in", (0, 0)); m.bond("b", "c"); m.bond("c", "d", "in", (0, 0)); m.bond("d", "a")
    f.mol(m, 130, 105)
    f.text(130, 70, "짧은 C=C", size=10.5, color=GRAY)
    f.text(176, 105, "긴 C–C", size=10.5, color=GRAY, anchor="start")
    f.text(130, 150, "A cyclobutadiene", size=12.5, weight="bold")
    f.text(130, 170, "평면·고리형·완전 공액, π 전자 4개", size=11)
    f.text(130, 188, "4n (n = 1) → 반방향족(antiaromatic)", size=11, color=RED)
    f.text(130, 206, "직사각형으로 찌그러지고 −78 ℃ 이상 불안정", size=11)
    ok(f, 130, 236, "ㄱ 방향족이다 → 거짓", good=False)
    # B: benzene
    for i, ox in enumerate((345, 445)):
        m = Mol()
        m.ring("r", 0, 0, 6, L, 90, arom=[0, 2, 4] if i == 0 else [1, 3, 5])
        f.mol(m, ox, 100)
    f.resarrow(382, 408, 100)
    f.text(395, 150, "B benzene", size=12.5, weight="bold")
    f.text(395, 170, "π 전자 6개 (4n+2, n = 1) → 방향족", size=11, color=BLUE)
    f.text(395, 188, "두 케쿨레 구조의 공명 혼성: 6개 C–C 모두 139 pm", size=11)
    f.text(395, 206, "(C–C 154 pm과 C=C 134 pm의 중간, D₆h 정육각형)", size=11)
    ok(f, 395, 236, "ㄴ 결합 길이가 모두 같다 → 참", good=True)
    # C: tub COT
    pts = _cot_tub()
    cx, cy = 660, 100
    dbl = {(0, 1), (2, 3), (4, 5), (6, 7)}
    order = sorted(range(8), key=lambda i: 0)
    for i in range(8):
        j = (i + 1) % 8
        x1, y1 = cx + pts[i][0], cy + pts[i][1]
        x2, y2 = cx + pts[j][0], cy + pts[j][1]
        back = (pts[i][2] + pts[j][2]) / 2 > 0.3
        col = "#9aa1ab" if back else INK
        if (i, j) in dbl:
            dx, dy = x2 - x1, y2 - y1
            d = math.hypot(dx, dy)
            nx, ny = -dy / d * 2.4, dx / d * 2.4
            line(f, x1 + nx, y1 + ny, x2 + nx, y2 + ny, col)
            line(f, x1 - nx, y1 - ny, x2 - nx, y2 - ny, col)
        else:
            line(f, x1, y1, x2, y2, col)
    f.text(660, 150, "C cyclooctatetraene", size=12.5, weight="bold")
    f.text(660, 170, "평면이면 π 8개(4n) → 반방향족 + 각 135° 변형", size=11)
    f.text(660, 188, "→ 통(tub) 모양으로 접혀 공액이 끊긴 폴리엔", size=11, color=RED)
    f.text(660, 206, "C=C 134 pm / C–C 147 pm (교대), 비방향족", size=11)
    ok(f, 660, 236, "ㄷ 평면 구조이다 → 거짓", good=False)
    f.text(400, 275, "Hückel 규칙: 평면 + 고리형 + 모든 원자 p 궤도 연속 + π 전자 4n+2 → 방향족, 4n → 반방향족(불안정; 가능하면 비평면으로 피함)",
           size=11, color=GRAY)
    return f.render()


def f21b():
    f = Fig(800, 250)
    f.text(20, 20, "Frost 원(내접 다각형) 으로 본 π MO 준위와 전자 배치", size=13, anchor="start", weight="bold")
    data = [(4, 140, "cyclobutadiene (4π)", "비결합 MO 2개에 홀전자 → 반방향족", RED),
            (6, 400, "benzene (6π)", "결합 MO가 모두 채워진 닫힌 껍질 → 방향족", BLUE),
            (8, 660, "평면 COT (가상, 8π)", "비결합 MO에 홀전자 → 반방향족 → 통 모양", RED)]
    R = 52
    cy = 118
    for n, cx, name, note, col in data:
        f.raw(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#cfd4db" stroke-width="1.2"/>')
        line(f, cx - R - 22, cy, cx + R + 22, cy, GRAY, 1, "4 3")
        verts = []
        for k in range(n):
            th = math.radians(-90 + 360 * k / n)
            verts.append((cx + R * math.cos(th), cy - R * math.sin(th)))
        f.raw('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in verts) +
              f'" fill="none" stroke="{INK}" stroke-width="1"/>')
        # 준위별 전자 채우기
        levels = {}
        for x, y in verts:
            levels.setdefault(round(y, 1), []).append(x)
        e = n
        for y in sorted(levels, reverse=True):     # 아래(결합성)부터
            xs = sorted(levels[y])
            k = len(xs)
            fill = [0] * k
            for s in range(2):
                for i in range(k):
                    if e > 0:
                        fill[i] += 1
                        e -= 1
            for x, nel in zip(xs, fill):
                line(f, x - 9, y, x + 9, y, INK, 2)
                t = {0: "", 1: "↑", 2: "↑↓"}[nel]
                if t:
                    f.text(x, y - 10, t, size=13, color=col if nel == 1 else INK, weight="bold")
        f.text(cx + R + 26, cy, "α", size=11, anchor="start", color=GRAY)
        f.text(cx, cy + R + 28, name, size=12, weight="bold")
        f.text(cx, cy + R + 46, note, size=11, color=col)
    return f.render()


# ------------------------------------------------------------------ 22
def f22():
    f = Fig(800, 250)
    f.text(20, 20, "22  C₄H₈ (불포화도 1)의 모든 이성질체 — 정답 ① ㄱ", size=13, anchor="start", weight="bold")
    xs = [65, 185, 300, 410, 560, 690]
    names = ["but-1-ene", "(Z)-but-2-ene", "(E)-but-2-ene", "2-methylpropene", "cyclobutane", "methylcyclopropane"]
    y0 = 95
    # 1-butene
    m = Mol(); m.atom("c1", -40, 8); m.sub("c2", "c1", 30, kind=2); m.sub("c3", "c2", -30); m.sub("c4", "c3", 30)
    f.mol(m, xs[0], y0)
    # cis
    m = Mol(); m.atom("c2", -15, -5); m.sub("c3", "c2", 0, kind=2); m.sub("c1", "c2", -120); m.sub("c4", "c3", -60)
    f.mol(m, xs[1], y0)
    # trans
    m = Mol(); m.atom("c2", -15, 0); m.sub("c3", "c2", 0, kind=2); m.sub("c1", "c2", 120); m.sub("c4", "c3", -60)
    f.mol(m, xs[2], y0)
    # isobutylene
    m = Mol(); m.atom("c2", 0, 0); m.sub("c1", "c2", 90, kind=2); m.sub("a", "c2", 210); m.sub("b", "c2", 330)
    f.mol(m, xs[3], y0 + 5)
    # cyclobutane
    m = Mol(); m.ring("r", 0, 0, 4, R4, 45)
    f.mol(m, xs[4], y0)
    # methylcyclopropane
    m = Mol(); m.ring("r", 0, 8, 3, L / math.sqrt(3), 90); m.sub("me", "r0", 90)
    f.mol(m, xs[5], y0)
    for x, n in zip(xs, names):
        f.text(x, 150, n, size=11.5)
    f.text(xs[1] + 57, 168, "← 기하(cis/trans) 이성질체 = 부분입체이성질체 →", size=10.5, color=GRAY)
    f.box(18, 182, 452, 30, fill="#eef4fc", stroke=BLUE)
    ok(f, 244, 197, "ㄱ 알켄 4가지 (구조 3 + 기하 1)", good=True)
    f.box(486, 182, 296, 30, fill="#fdf0ee", stroke=RED)
    ok(f, 634, 197, "ㄴ 고리형은 2가지 (1가지 아님)", good=False)
    ok(f, 400, 233, "ㄷ 6가지 모두 거울면을 가짐(카이랄 중심 없음) → 거울상 이성질체 없음", good=False)
    return f.render()


# ------------------------------------------------------------------ 23
def _alaninamide(m, wedge="w"):
    m.atom("n1", 0, 0, "H_2N", "end")
    m.sub("ca", "n1", -30)
    m.sub("cm", "ca", -90, "CH_3", kind=wedge)
    m.sub("cc", "ca", 30)
    m.sub("o", "cc", 90, "O", kind="2")
    m.sub("n2", "cc", -30, "NH_2", anchor="start")
    return m


def f23():
    f = Fig(800, 270)
    f.text(20, 20, "23  (R)-2-aminopropanamide (D-alaninamide)의 배열과 피셔 투영 — ㄴ 거짓", size=13, anchor="start", weight="bold")
    m = _alaninamide(Mol())
    ox, oy = 70, 110
    f.mol(m, ox, oy)
    # 우선순위 표시
    for nm, t, dx, dy in (("n1", "①", -12, -18), ("cc", "②", 0, 22), ("cm", "③", 26, 0)):
        x, y = P(m, nm, ox, oy)
        f.text(x + dx, y + dy, t, size=12, color=RED, weight="bold")
    x, y = P(m, "ca", ox, oy)
    f.text(x - 18, y + 16, "H(④, 뒤)", size=10, color=GRAY, anchor="end")
    f.rotarrow(x, y - 2, cw=True, r=9)
    f.text(110, 190, "H가 뒤 → ①→②→③ 시계 방향", size=11)
    f.text(110, 208, "= (R)", size=12.5, weight="bold", color=RED)
    f.text(110, 232, "sp² 탄소: C=O 탄소 1개뿐 (ㄱ ○)", size=11, color=BLUE)
    # 정답 피셔
    f.arrow(225, 110, 285, 110, "피셔 투영", None)
    fischer(f, 365, 110, "CONH_2", "CH_3", "H", "NH_2", hl={"NH_2": RED})
    f.text(365, 185, "(R): NH₂가 오른쪽 = D형", size=11.5, weight="bold", color=BLUE)
    f.text(365, 205, "가로 = 앞(관찰자 쪽), 세로 = 뒤", size=10.5, color=GRAY)
    # 보기 ㄴ 피셔
    f.box(480, 45, 300, 200, fill="#fdf0ee", stroke=RED)
    f.text(630, 62, "보기 ㄴ의 피셔 투영", size=12, weight="bold", color=RED)
    fischer(f, 545, 125, "CONH_2", "CH_3", "H_2N", "H", hl={"H_2N": RED})
    f.text(615, 100, "① NH₂ → ② CONH₂ → ③ CH₃", size=10.5, anchor="start")
    f.text(625, 118, "= 반시계, H는 가로(앞)", size=10.5, anchor="start")
    f.text(625, 136, "→ 뒤집어 (S) (L형)", size=10.5, anchor="start", weight="bold")
    f.text(630, 200, "문제의 화합물(R)의 거울상 이성질체", size=11)
    ok(f, 630, 225, "ㄴ 거짓", good=False)
    return f.render()


def f23b():
    f = Fig(800, 210)
    f.text(20, 20, "ㄷ 염기도: a(아민 N) > b(아마이드 N)", size=13, anchor="start", weight="bold")
    # 아마이드 공명: R–C(=O)–NH2 (C 중심, R 왼쪽 아래, O 위, N 오른쪽 아래)
    def amide(double_on_n):
        m = Mol()
        m.atom("c", 0, 0)
        m.sub("r", "c", 210, "R")
        m.sub("o", "c", 90, "O", kind=1 if double_on_n else "2")
        m.sub("n", "c", -30, "NH_2", anchor="start", kind="2" if double_on_n else 1)
        return m
    m = amide(False)
    ox, oy = 80, 110
    f.mol(m, ox, oy)
    n = P(m, "n", ox, oy); c = P(m, "c", ox, oy); o = P(m, "o", ox, oy)
    f.lp(n[0] - 3, n[1] + 11, -90)
    f.curly(n[0] - 8, n[1] + 13, *mid(c, n, 0.4), bend=-1.1)
    f.curly(*mid(c, o, 0.5), o[0] + 10, o[1] + 1, bend=0.6)
    f.resarrow(165, 195, 105)
    m2 = amide(True)
    ox2 = 245
    f.mol(m2, ox2, oy)
    n2 = P(m2, "n", ox2, oy); o2 = P(m2, "o", ox2, oy)
    f.charge(n2[0] + 28, n2[1] - 10, "+")
    f.charge(o2[0] + 14, o2[1] - 6, "−")
    f.text(175, 160, "b: N 비공유쌍이 C=O로 비편재화 (N은 sp², 평면)", size=11)
    f.text(175, 178, "양성자화하면 공명 안정화 상실 → 약염기 (짝산 pKₐ ≈ −0.5, O에서)", size=11, color=RED)
    # 아민
    f.box(440, 45, 340, 140, fill="#eef4fc", stroke=BLUE)
    f.text(610, 65, "a: 1차 알킬 아민 N (sp³)", size=12, weight="bold", color=BLUE)
    f.text(610, 90, "비공유쌍이 국재화 → H⁺와 결합 가능", size=11)
    f.text(610, 110, "R–NH₂ + H⁺ ⇌ R–NH₃⁺ (짝산 pKₐ ≈ 8)", size=11)
    f.text(610, 130, "(α-C=O의 유발 효과로 일반 아민(≈10.6)보다는 약함)", size=10.5, color=GRAY)
    ok(f, 610, 160, "ㄷ a가 b보다 염기도 크다 → 참", good=True)
    return f.render()


# ------------------------------------------------------------------ 24
def f24():
    f = Fig(800, 330)
    f.text(20, 20, "24  세 쌍의 크기 비교 — 정답 ④ ㄴ, ㄷ", size=13, anchor="start", weight="bold")
    # ㄱ
    f.text(20, 50, "ㄱ 탄소 음이온 안정도", size=12, anchor="start", weight="bold")
    m = Mol()
    m.atom("c1", 0, 0)
    m.sub("c2", "c1", 0, kind="2")
    m.sub("h1", "c1", 120, "H"); m.sub("h2", "c1", 240, "H"); m.sub("h3", "c2", 60, "H")
    ox, oy = 60, 95
    f.mol(m, ox, oy)
    c2 = P(m, "c2", ox, oy)
    f.lp(c2[0] + 5, c2[1] + 8, -60)
    f.charge(c2[0] + 15, c2[1] + 12, "−")
    f.text(75, 140, "vinyl 음이온: sp² (s 33%)", size=11)
    f.text(75, 157, "ethene pKₐ ≈ 44", size=11, color=GRAY)
    f.text(165, 95, "<", size=18, weight="bold", color=RED)
    m = Mol()
    m.atom("h", 0, 0, "H")
    m.sub("c1", "h", 0)
    m.sub("c2", "c1", 0, kind=3)
    ox, oy = 200, 95
    f.mol(m, ox, oy)
    c2 = P(m, "c2", ox, oy)
    f.lp(c2[0] + 6, c2[1], 0)
    f.charge(c2[0] + 17, c2[1] - 8, "−")
    f.text(240, 140, "acetylide: sp (s 50%)", size=11)
    f.text(240, 157, "ethyne pKₐ ≈ 25", size=11, color=GRAY)
    f.text(150, 182, "s 성질↑ → 전자쌍이 핵 가까이 → 안정", size=11)
    ok(f, 150, 204, "보기의 부등호가 반대 → 거짓", good=False)
    # ㄴ
    f.text(310, 50, "ㄴ 이형태체 안정도 (butane)", size=12, anchor="start", weight="bold")
    newman(f, 370, 112, [(270, "CH_3"), (30, "H"), (150, "H")], [(90, "CH_3"), (210, "H"), (330, "H")],
           color_map={"CH_3": BLUE})
    f.text(440, 112, ">", size=18, weight="bold", color=BLUE)
    newman(f, 510, 112, [(270, "CH_3"), (30, "H"), (150, "H")], [(90, "H"), (210, "H"), (330, "CH_3")],
           color_map={"CH_3": RED})
    f.text(370, 172, "anti (0)", size=11, weight="bold")
    f.text(510, 172, "gauche (+3.8 kJ/mol)", size=11, weight="bold")
    f.text(440, 188, "gauche: CH₃···CH₃ 입체 반발(60°)", size=11)
    ok(f, 440, 204, "참", good=True)
    # ㄷ
    f.text(610, 50, "ㄷ 정상 끓는점", size=12, anchor="start", weight="bold")
    m = Mol()
    m.atom("a", 0, 0); m.sub("b", "a", 30); m.sub("c", "b", -30); m.sub("n", "c", 30, "NH_2", anchor="start"); m.sub("d", "b", 90)
    f.mol(m, 625, 100)
    f.text(670, 128, "2-methylpropan-1-amine", size=10.5)
    f.text(670, 144, "M 73, bp ≈ 68 ℃", size=11, color=BLUE, weight="bold")
    m = Mol()
    m.atom("a", 0, 0); m.sub("b", "a", 30); m.sub("c", "b", -30); m.sub("e", "c", 30); m.sub("d", "b", 90)
    f.mol(m, 645, 205)
    f.text(690, 228, "2-methylbutane, M 72, bp ≈ 28 ℃", size=10.5)
    f.text(660, 262, "분자량·모양 비슷 → 차이는 N–H···N 수소 결합", size=10.5)
    ok(f, 660, 284, "참", good=True)
    f.text(400, 315, "ㄱ 함정: '음이온이 탄소 위에 있다'만 보고 치환이 많을수록 불안정(알킬 +I)이라 판단하면 안 됨 — 혼성(s 성질)이 우선", size=10.5, color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 25
def _pentyl(m, sub_label=None, kind="w"):
    m.atom("c1", 0, 0)
    m.sub("c2", "c1", 30)
    m.sub("c3", "c2", -30)
    m.sub("c4", "c3", 30)
    m.sub("c5", "c4", -30)
    if sub_label:
        m.sub("x", "c2", 90, sub_label, kind=kind)
    return m


def f25():
    f = Fig(800, 300)
    f.text(20, 20, "25  토실화(입체 유지) → S_N2 (입체 반전) — 정답 ① ㄱ", size=13, anchor="start", weight="bold")
    m = _pentyl(Mol(), "OH", "w")
    f.mol(m, 35, 105)
    f.text(80, 140, "A (R)-pentan-2-ol", size=11.5, weight="bold")
    ok(f, 80, 160, "ㄱ 참", good=True, size=11)
    f.arrow(160, 100, 235, 100, "TsCl", "pyridine")
    m = _pentyl(Mol(), "OTs", "w")
    f.mol(m, 255, 105)
    f.text(300, 140, "B (R)-pentan-2-yl tosylate", size=11.5, weight="bold")
    f.text(300, 158, "C–O 불변 → 배열 유지 (OTs 쐐기)", size=10.5, color=BLUE)
    f.arrow(380, 100, 470, 100, "NaCN", "DMSO, S_N2")
    m = _pentyl(Mol(), "CN", "h")
    f.mol(m, 490, 105)
    f.text(535, 140, "C (S)-2-methylpentanenitrile", size=11.5, weight="bold")
    f.text(535, 158, "뒷면 공격 → 반전 (CN 점선)", size=10.5, color=RED)
    # 오답
    f.box(625, 45, 160, 120, fill="#fdf0ee", stroke=RED)
    f.text(705, 62, "보기의 구조", size=11.5, weight="bold", color=RED)
    f.text(705, 85, "ㄴ: OTs 점선 = (S) 토실레이트", size=10.5)
    f.text(705, 103, "→ 반전된 것처럼 그림", size=10.5)
    f.text(705, 126, "ㄷ: CN 쐐기 = (R) 나이트릴", size=10.5)
    f.text(705, 144, "→ 반전이 빠짐", size=10.5)
    ok(f, 705, 185, "ㄴ, ㄷ 거짓", good=False)
    f.text(400, 215, "A의 배열: ① OH > ② CH₂CH₂CH₃ > ③ CH₃ > ④ H(뒤): 위 → 오른쪽 아래 → 왼쪽 아래 = 시계 방향 = R", size=11)
    f.text(400, 235, "C의 배열: ① CN > ② CH₂CH₂CH₃ > ③ CH₃, H가 앞(쐐기) → 시계 방향으로 읽혀도 뒤집어 S", size=11)
    f.text(400, 260, "주의: R/S 표기 변화는 '우선순위'로 정해지므로 반전 여부는 반드시 공간 배치(쐐기↔점선)로 판단", size=10.5, color=GRAY)
    f.text(400, 280, "(여기서는 OH와 CN이 모두 1순위라 '배치 반전 = R→S'가 우연히 일치)", size=10.5, color=GRAY)
    return f.render()


def f25b():
    f = Fig(800, 230)
    f.text(20, 20, "메커니즘: ① O가 S를 공격(C–O 불변) ② CN⁻ 뒷면 공격(협동, 한 단계)", size=13, anchor="start", weight="bold")
    # 단계 1
    f.text(45, 95, "R", size=13)
    line(f, 54, 95, 75, 95)
    f.text(84, 95, "O", size=13)
    f.lp(84, 84, 90)
    f.text(84, 112, "H", size=13)
    line(f, 84, 103, 84, 104)
    f.text(155, 95, "S", size=13)
    f.text(155, 70, "O", size=13); f.text(155, 120, "O", size=13)
    line(f, 152, 77, 152, 87); line(f, 158, 77, 158, 87)
    line(f, 152, 103, 152, 113); line(f, 158, 103, 158, 113)
    line(f, 163, 95, 190, 95)
    f.text(200, 95, "Cl", size=13)
    f.text(125, 95, "Ar–", size=12, anchor="end")
    f.curly(88, 82, 147, 86, bend=-0.4)
    f.curly(176, 92, 198, 84, bend=-0.6)
    f.arrow(225, 95, 270, 95, "− Cl⁻", "py: −H⁺")
    f.text(285, 95, "R–O–SO₂Ar (= ROTs)", size=12.5, anchor="start")
    f.text(150, 150, "탄소의 결합은 하나도 끊어지지 않음 → 배열 유지", size=11, color=BLUE)
    f.text(150, 168, "pyridine: HCl 중화(염기), TsCl 활성화", size=10.5, color=GRAY)
    # 단계 2 SN2
    cx, cy = 600, 105
    f.text(470, cy, "N≡C", size=13)
    f.lp(489, cy, 0)
    f.charge(478, cy - 15, "−")
    f.curly(494, cy - 4, cx - 12, cy - 4, bend=-0.35)
    line(f, cx, cy, cx + 38, cy)
    f.text(cx + 48, cy, "OTs", size=13, anchor="start")
    f.curly(cx + 20, cy + 3, cx + 52, cy + 12, bend=0.6)
    line(f, cx, cy, cx - 6, cy - 30); f.text(cx - 8, cy - 40, "CH_3", size=12)
    line(f, cx, cy, cx + 8, cy + 28); f.text(cx + 12, cy + 38, "C_3H_7", size=12)
    f.text(cx + 14, cy - 22, "H", size=12)
    line(f, cx, cy, cx + 8, cy - 14, dash="2 2")
    f.text(620, 165, "Nu는 이탈기 반대편(180°)에서 σ*(C–O)로 들어감", size=11, color=RED)
    f.text(620, 183, "→ 세 치환기가 우산처럼 뒤집힘", size=11, color=RED)
    f.text(620, 201, "DMSO(극성 비양성자성): CN⁻을 덜 용매화 → S_N2 가속", size=10.5, color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 26
def f26():
    f = Fig(800, 300)
    f.text(20, 20, "26  라디칼 단일브로민화 — 정답 ④ ㄴ, ㄷ", size=13, anchor="start", weight="bold")
    # ㄱ
    f.text(20, 48, "ㄱ 2,2,4-trimethylpentane: 서로 다른 H 4종류", size=12, anchor="start", weight="bold")
    m = Mol()
    m.atom("c4", 0, 0)
    m.sub("d1", "c4", 210); m.sub("d2", "c4", 90)
    m.sub("c3", "c4", -30)
    m.sub("c2", "c3", 30)
    m.sub("a1", "c2", 90); m.sub("a2", "c2", 330); m.sub("a3", "c2", 30)
    ox, oy = 60, 120
    f.mol(m, ox, oy)
    for nm, t, dx, dy in (("d1", "d", -10, 0), ("d2", "d", -10, 0), ("c4", "c", 0, 14), ("c3", "b", 0, 13),
                          ("a1", "a", 10, 0), ("a2", "a", 9, 6), ("a3", "a", 10, 0)):
        x, y = P(m, nm, ox, oy)
        f.text(x + dx, y + dy, t, size=12, color=RED, weight="bold")
    rows = [("a (9H, 1°)", "1-bromo-2,2,4-trimethylpentane", "카이랄 ✗", "1"),
            ("b (2H, 2°)", "3-bromo-2,2,4-trimethylpentane", "C3 카이랄", "2"),
            ("c (1H, 3°)", "2-bromo-2,4,4-trimethylpentane", "카이랄 ✗", "1"),
            ("d (6H, 1°)", "1-bromo-2,4,4-trimethylpentane", "C2 카이랄", "2")]
    y = 72
    f.text(185, y, "H", size=11, anchor="start", weight="bold"); f.text(268, y, "생성물", size=11, anchor="start", weight="bold")
    f.text(470, y, "입체", size=11, anchor="start", weight="bold"); f.text(540, y, "수", size=11, anchor="start", weight="bold")
    for i, (h, n, st, k) in enumerate(rows):
        yy = y + 20 + 18 * i
        f.text(185, yy, h, size=10.5, anchor="start")
        f.text(268, yy, n, size=10.5, anchor="start")
        f.text(470, yy, st, size=10.5, anchor="start")
        f.text(545, yy, k, size=10.5, anchor="middle")
    f.text(375, 178, "구조 이성질체 4가지, 입체이성질체 포함 6가지 → 어느 쪽으로 세어도 7가지 아님", size=11)
    ok(f, 700, 125, "ㄱ 거짓", good=False)
    # ㄴ
    f.text(20, 210, "ㄴ", size=12, anchor="start", weight="bold")
    m = Mol(); m.atom("c", 0, 0); m.sub("a", "c", 90); m.sub("b", "c", 210); m.sub("d", "c", 330)
    f.mol(m, 65, 255)
    f.arrow(100, 250, 150, 250, "Br•", "−HBr")
    f.text(172, 250, "(CH₃)₃C•", size=12.5, anchor="start")
    f.text(195, 270, "3° 라디칼", size=10.5, color=BLUE)
    f.arrow(240, 250, 285, 250, "Br₂", None)
    m = Mol(); m.atom("c", 0, 0); m.sub("a", "c", 90, "Br"); m.sub("b", "c", 210); m.sub("d", "c", 330)
    f.mol(m, 315, 258)
    f.text(240, 290, "Br•의 H 추출은 흡열 → 늦은 TS(Hammond) → 3°:1° 선택성 ≈ 1600:1", size=10.5)
    ok(f, 380, 230, "참", good=True, anchor="start")
    # ㄷ
    f.text(450, 210, "ㄷ (S)-sec-butylbenzene", size=12, anchor="start", weight="bold")
    cx, cy = 560, 255
    m = Mol(); benzene(m, "r", 0, 0, 90)
    f.mol(m, cx - 62, cy, scale=0.75)
    line(f, cx - 62 + 0.75 * 26, cy - 0.75 * 15, cx - 6, cy)
    f.porb(cx, cy, 1, rx=6, ry=12)
    line(f, cx + 4, cy, cx + 26, cy + 10)
    f.text(cx + 32, cy + 14, "Et", size=11, anchor="start")
    line(f, cx + 4, cy, cx + 24, cy - 10)
    f.text(cx + 30, cy - 14, "CH_3", size=11, anchor="start")
    f.text(cx, cy - 34, "Br₂ (위)", size=10, color=RED)
    f.text(cx, cy + 36, "Br₂ (아래)", size=10, color=RED)
    f.text(690, 245, "벤질 라디칼: sp², 평면", size=10.5, anchor="start")
    f.text(690, 262, "→ 양면 공격 1:1", size=10.5, anchor="start")
    f.text(690, 279, "→ 라세미 혼합물", size=10.5, anchor="start", color=BLUE)
    ok(f, 750, 228, "참", good=True)
    return f.render()


# ------------------------------------------------------------------ 27
def _iso(m, mode):
    """3-methylbutan-2-ol 골격. mode: oh, one, br, ene2, ene1"""
    m.atom("c3", 0, 0)
    m.sub("ma", "c3", 120); m.sub("mb", "c3", 240)
    m.sub("c2", "c3", 0, kind="2" if mode == "ene2" else 1)
    m.sub("c1", "c2", -60, kind="2" if mode == "ene1" else 1)
    if mode == "oh":
        m.sub("x", "c2", 60, "OH")
    elif mode == "one":
        m.sub("x", "c2", 60, "O", kind="2")
    elif mode == "br":
        m.sub("x", "c2", 60, "Br")
    return m


def f27():
    f = Fig(800, 330)
    f.text(20, 20, "27  3-methylbutan-2-ol의 세 갈래 반응 — 정답 ⑤ ㄱ, ㄴ, ㄷ", size=13, anchor="start", weight="bold")
    f.mol(_iso(Mol(), "oh"), 45, 175)
    f.text(70, 215, "3-methylbutan-2-ol (2°)", size=10.5)
    line(f, 150, 80, 150, 285)
    line(f, 125, 175, 150, 175)
    # A
    f.arrow(150, 80, 260, 80, "Na₂Cr₂O₇", "H₂SO₄")
    f.mol(_iso(Mol(), "one"), 280, 88)
    f.text(390, 80, "A 3-methylbutan-2-one: 2° 알코올 → 케톤 (더 산화 안 됨)", size=11, anchor="start")
    ok(f, 390, 100, "ㄱ 참", good=True, size=11, anchor="start")
    # B → C
    f.arrow(150, 175, 260, 175, "PBr₃", "ether")
    f.mol(_iso(Mol(), "br"), 280, 183)
    f.text(325, 220, "B 2-bromo-3-methylbutane", size=10.5)
    f.text(325, 236, "S_N2, 탄소 양이온 없음 → 자리옮김 없음", size=10.5, color=BLUE)
    ok(f, 325, 254, "ㄴ 참", good=True, size=11)
    f.arrow(390, 175, 480, 175, "NaOEt", "EtOH, E2")
    f.mol(_iso(Mol(), "ene2"), 500, 183)
    f.text(545, 215, "C 2-methylbut-2-ene", size=10.5, weight="bold")
    f.text(545, 231, "Zaitsev (3치환, 주)", size=10.5, color=BLUE)
    f.mol(_iso(Mol(), "ene1"), 655, 183)
    f.text(700, 222, "3-methylbut-1-ene", size=10.5, color=GRAY)
    f.text(700, 238, "(1치환, 부)", size=10.5, color=GRAY)
    # D
    f.arrow(150, 285, 260, 285, "POCl₃", "pyridine")
    f.mol(_iso(Mol(), "ene2"), 280, 293)
    f.text(390, 278, "D 2-methylbut-2-ene: ROH → R–OPOCl₂(좋은 이탈기) → pyridine에 의한 E2", size=11, anchor="start")
    f.text(390, 296, "산성 조건(E1)이 아니므로 탄소 양이온·자리옮김 없이 Zaitsev 생성물", size=11, anchor="start", color=BLUE)
    ok(f, 390, 316, "ㄷ C = D (같은 화합물) 참", good=True, size=11, anchor="start")
    return f.render()


def f27b():
    f = Fig(800, 230)
    f.text(20, 20, "D의 메커니즘 (POCl₃ / pyridine): O-인산화 → E2  |  비교: H₂SO₄/가열(E1)이면?", size=13, anchor="start", weight="bold")
    m = Mol()
    m.atom("c3", 0, 0)
    m.sub("ma", "c3", 120); m.sub("mb", "c3", 240)
    m.sub("c2", "c3", 0)
    m.sub("c1", "c2", -60)
    m.sub("o", "c2", 60, "O")
    m.sub("p", "o", 0, "POCl_2", anchor="start")
    m.sub("h", "c3", -90, "H")
    ox, oy = 90, 120
    f.mol(m, ox, oy)
    h = P(m, "h", ox, oy); c3 = P(m, "c3", ox, oy); c2 = P(m, "c2", ox, oy); o = P(m, "o", ox, oy)
    f.text(h[0] - 60, h[1] + 25, "py:", size=13)
    f.curly(h[0] - 48, h[1] + 20, h[0] - 7, h[1] + 6, bend=-0.4)
    f.curly(*mid(c3, h, 0.5), *mid(c3, c2, 0.5), bend=-0.7)
    f.curly(*mid(c2, o, 0.45), o[0] + 6, o[1] - 10, bend=0.7)
    f.text(140, 195, "β-H(3°, C3)와 이탈기 OPOCl₂가 anti 배열에서 한 번에", size=11)
    f.text(140, 213, "→ 더 치환된 2-methylbut-2-ene (D)", size=11, color=BLUE)
    f.box(395, 45, 390, 170, fill="#fff7e6", stroke="#e0b25a")
    f.text(590, 65, "만약 H₂SO₄, 가열(E1)이라면", size=12, weight="bold")
    f.text(590, 90, "ROH₂⁺ → 2° 탄소 양이온(C2)", size=11)
    f.text(590, 110, "→ C3-H의 1,2-수소화 음이온 이동 → 3° 양이온", size=11)
    f.text(590, 130, "→ 여기서는 E1도 같은 2-methylbut-2-ene이 주생성물", size=11)
    f.text(590, 155, "(자리옮김이 골격을 바꾸는 예: 3,3-dimethylbutan-2-ol", size=10.5, color=GRAY)
    f.text(590, 172, "  → E1은 2,3-dimethylbut-2-ene, POCl₃는 3,3-dimethylbut-1-ene)", size=10.5, color=GRAY)
    f.text(590, 197, "POCl₃/pyridine = 자리옮김 없는 탈수의 대표 조건", size=11, color=BLUE)
    return f.render()


# ------------------------------------------------------------------ 28
def _ph(m, ox=0):
    benzene(m, "r", ox, 0, 90)
    return "r1"


def f28():
    f = Fig(800, 340)
    f.text(20, 20, "28  KMnO₄ 산화 — 정답 ③ ㄱ, ㄷ", size=13, anchor="start", weight="bold")
    ys = [85, 185, 285]
    # ㄱ
    m = Mol(); a = _ph(m); c = m.sub("c", a, 30); m.sub("o", c, 90, "O", kind="2"); m.sub("h", c, -30, "H")
    f.mol(m, 60, ys[0] + 8)
    f.arrow(150, ys[0], 250, ys[0], "KMnO₄, H₂O", "H₃O⁺")
    m = Mol(); a = _ph(m); c = m.sub("c", a, 30); m.sub("o", c, 90, "O", kind="2"); m.sub("h", c, -30, "OH")
    f.mol(m, 290, ys[0] + 8)
    f.text(420, ys[0] - 10, "알데하이드 C–H → C–OH (쉽게 산화)", size=11, anchor="start")
    ok(f, 420, ys[0] + 12, "ㄱ 참 (benzoic acid)", good=True, size=11.5, anchor="start")
    # ㄴ
    m = Mol(); a = _ph(m); c = m.sub("c", a, 30); m.sub("m1", c, 90); m.sub("m2", c, 330); m.sub("m3", c, 30)
    f.mol(m, 60, ys[1] + 8)
    f.arrow(150, ys[1], 250, ys[1], "KMnO₄, H₂O", "H₃O⁺")
    f.text(300, ys[1], "반응 없음", size=13, weight="bold", color=RED, anchor="start")
    f.text(420, ys[1] - 18, "곁사슬 산화는 벤질 C–H 추출(벤질 라디칼)로 시작", size=11, anchor="start")
    f.text(420, ys[1], "tert-butylbenzene은 벤질 탄소가 4차(H 없음)", size=11, anchor="start")
    ok(f, 420, ys[1] + 22, "ㄴ 거짓 (benzoic acid 생기지 않음)", good=False, size=11.5, anchor="start")
    x, y = 60 + 26 + 26, ys[1] + 8 - 15 - 15
    f.raw(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="none" stroke="{RED}" stroke-width="1.5"/>')
    # ㄷ
    m = Mol(); a = _ph(m); c = m.sub("c", a, 30); m.sub("c2", c, -30, kind="2")
    f.mol(m, 60, ys[2] + 8)
    f.arrow(150, ys[2], 250, ys[2], "KMnO₄, H₂O, 100 ℃", "H₃O⁺")
    m = Mol(); a = _ph(m); c = m.sub("c", a, 30); m.sub("o", c, 90, "O", kind="2"); m.sub("h", c, -30, "OH")
    f.mol(m, 290, ys[2] + 8)
    f.text(355, ys[2] + 20, "+ CO₂", size=12, anchor="start")
    f.text(420, ys[2] - 10, "뜨거운 KMnO₄: C=C 산화 절단 → PhCOOH + HCOOH(→CO₂)", size=11, anchor="start")
    ok(f, 420, ys[2] + 12, "ㄷ 참", good=True, size=11.5, anchor="start")
    return f.render()


# ------------------------------------------------------------------ 29
def _cyhex(m, left, right):
    """left: 'O'(케톤), 'HO', 'ketal'  right: 'ester', 'ch2oh'"""
    cyclohexane(m, "p", 0, 0, 0)
    if left == "O":
        m.sub("l", "p3", 180, "O", kind="2")
    elif left == "HO":
        m.sub("l", "p3", 180, "HO", anchor="end")
    elif left == "ketal":
        cx = m.pos("p3")[0] - R5
        m.ring("d", cx, 0, 5, R5, 0)
        m.label("d1", "O"); m.label("d4", "O")
    if right == "ester":
        m.sub("cc", "p0", 30)
        m.sub("co", "cc", 90, "O", kind="2")
        m.sub("om", "cc", -30, "OMe", anchor="start")
    elif right == "ch2oh":
        m.sub("cc", "p0", 30)
        m.sub("oh", "cc", 90, "OH")
    return m


def f29():
    f = Fig(800, 330)
    f.text(20, 20, "29  화학 선택성: 아세탈 보호 → LiAlH₄ → 탈보호 — 정답 ⑤ ㄱ, ㄴ, ㄷ", size=13, anchor="start", weight="bold")
    f.mol(_cyhex(Mol(), "O", "ester"), 70, 90)
    f.text(85, 135, "A", size=12.5, weight="bold")
    f.arrow(180, 85, 295, 85, "1. LiAlH₄(과량)", "2. H₂O")
    f.mol(_cyhex(Mol(), "HO", "ch2oh"), 390, 90)
    f.text(410, 135, "B 4-(hydroxymethyl)cyclohexan-1-ol", size=11, weight="bold")
    f.text(500, 70, "케톤 → 2° 알코올, 에스터 → 1° 알코올 (둘 다 환원)", size=10.5, anchor="start")
    ok(f, 500, 92, "ㄱ 참 (cis/trans 혼합 가능)", good=True, size=11, anchor="start")
    f.arrow(85, 150, 85, 205, "HOCH₂CH₂OH", "H⁺ 촉매")
    f.mol(_cyhex(Mol(), "ketal", "ester"), 110, 260)
    f.text(110, 308, "C (아세탈은 케톤에만 생김)", size=11, weight="bold")
    ok(f, 110, 324, "ㄴ 참", good=True, size=11)
    f.arrow(225, 255, 315, 255, "1. LiAlH₄", "2. H₂O")
    f.mol(_cyhex(Mol(), "ketal", "ch2oh"), 400, 260)
    f.text(400, 308, "에스터만 환원 (아세탈은 염기·H⁻에 안정)", size=10.5)
    f.arrow(500, 255, 585, 255, "H₃O⁺", "탈보호")
    f.mol(_cyhex(Mol(), "O", "ch2oh"), 668, 260)
    f.text(672, 308, "D 4-(hydroxymethyl)cyclohexan-1-one", size=10.5, weight="bold")
    ok(f, 672, 324, "ㄷ 참", good=True, size=11)
    f.text(560, 175, "케톤 C=O가 에스터보다 친전자성 큼", size=10.5, color=GRAY)
    f.text(560, 192, "→ 아세탈화는 케톤에서 선택적으로", size=10.5, color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 30
def _c5(m, mode):
    m.ring("r", 0, 0, 5, R5, 90)
    if mode in ("one", "enone", "me1"):
        m.sub("o", "r0", 90, "O", kind="2")
    if mode == "enone":
        m.set_bond("r1", "r2", "in", (0, 0))
    if mode == "me1":
        m.sub("me", "r1", 18)
    if mode == "ol":
        m.set_bond("r1", "r2", "in", (0, 0))
        m.sub("oh", "r0", 140, "HO", anchor="end")
        m.sub("me", "r0", 40)
    return m


def f30():
    f = Fig(800, 300)
    f.text(20, 20, "30  ② 오답: 단단한 유기리튬은 1,2-첨가, 무른 큐프레이트는 1,4-첨가", size=13, anchor="start", weight="bold")
    f.mol(_c5(Mol(), "enone"), 60, 100)
    f.arrow(110, 95, 210, 95, "1. CH₃Li", "2. H₃O⁺")
    f.mol(_c5(Mol(), "ol"), 265, 100)
    f.text(265, 150, "1-methylcyclopent-2-en-1-ol", size=11, weight="bold", color=BLUE)
    f.text(265, 167, "(실제 주생성물, 1,2-첨가)", size=10.5, color=BLUE)
    f.mol(_c5(Mol(), "me1"), 430, 100)
    f.cross(430, 100, 22)
    f.text(430, 150, "2-methylcyclopentanone", size=11, color=RED)
    f.text(430, 167, "(선지 ②의 구조: 1,4-첨가도 아님)", size=10.5, color=RED)
    f.text(600, 70, "1,4-첨가였다면 3-methyl-", size=10.5, anchor="start", color=GRAY)
    f.text(600, 86, "cyclopentanone (β-C에 CH₃)", size=10.5, anchor="start", color=GRAY)
    f.text(600, 110, "선지의 CH₃는 α-탄소 →", size=10.5, anchor="start", color=GRAY)
    f.text(600, 126, "어느 경로로도 불가", size=10.5, anchor="start", color=GRAY)
    # 비교 표
    f.box(20, 190, 760, 100)
    f.text(40, 210, "친핵체", size=11.5, anchor="start", weight="bold")
    f.text(210, 210, "공격 위치", size=11.5, anchor="start", weight="bold")
    f.text(360, 210, "이유", size=11.5, anchor="start", weight="bold")
    rows = [("RLi, RMgX, LiAlH₄", "C=O 탄소 (1,2)", "전하 밀집(단단함) → 전하 제어, 양전하가 큰 C1을 빠르고 비가역적으로 공격"),
            ("R₂CuLi (Gilman)", "β-탄소 (1,4)", "무른 친핵체 → 궤도 제어(LUMO 계수 큰 C3), ③ 3-ethylcyclohexanone ○"),
            ("엔올레이트·아민·RS⁻", "β-탄소 (1,4)", "가역적 1,2-첨가 → 열역학적으로 안정한 1,4-생성물(C=O 유지)")]
    for i, (a, b, c) in enumerate(rows):
        y = 232 + 20 * i
        f.text(40, y, a, size=11, anchor="start")
        f.text(210, y, b, size=11, anchor="start")
        f.text(360, y, c, size=10.5, anchor="start")
    return f.render()


def _c6one(m, mode):
    """2-methylcyclohexanone 계열. p0=C1(C=O), p1=C2(CH₃), p5=C6"""
    m.ring("p", 0, 0, 6, L, 90)
    if mode == "enolate":
        m.sub("o", "p0", 90, "O^−")
        m.set_bond("p0", "p5", "in", (0, 0))
    else:
        m.sub("o", "p0", 90, "O", kind="2")
    m.sub("me", "p1", 30)
    if mode == "prod":
        m.sub("e1", "p5", 150)
        m.sub("e2", "e1", 90)
    return m


def f30b():
    f = Fig(800, 250)
    f.text(20, 20, "⑤ LDA, −78 ℃: 속도론적 엔올레이트(덜 치환된 α-C) → 알킬화  |  ①·④ 요약", size=13, anchor="start", weight="bold")
    m = _c6one(Mol(), "one")
    f.mol(m, 60, 110)
    x, y = P(m, "p5", 60, 110)
    f.text(x - 14, y - 8, "H", size=11, color=RED)
    f.text(60, 165, "C6-H: 2°, 덜 가림", size=10.5, color=RED)
    f.arrow(110, 105, 200, 105, "LDA", "THF, −78 ℃")
    f.mol(_c6one(Mol(), "enolate"), 250, 110)
    f.text(250, 165, "속도론적 엔올레이트", size=10.5, weight="bold")
    f.text(250, 181, "(크고 강한 염기, 비가역, 저온)", size=10.5)
    f.arrow(300, 105, 380, 105, "CH₃CH₂I", "S_N2")
    f.mol(_c6one(Mol(), "prod"), 435, 110)
    f.text(435, 165, "2-ethyl-6-methylcyclohexanone", size=10.5, weight="bold", color=BLUE)
    ok(f, 435, 183, "⑤ 옳음", good=True, size=11)
    f.box(540, 40, 245, 165, fill="#f7f8fa")
    f.text(552, 60, "① Wolff–Kishner 환원", size=11, anchor="start", weight="bold")
    f.text(552, 78, "C=O → 하이드라존 → KOH/가열", size=10.5, anchor="start")
    f.text(552, 94, "−N₂ → CH₂: methylcyclopentane ○", size=10.5, anchor="start")
    f.text(552, 120, "④ 자체 알돌 축합", size=11, anchor="start", weight="bold")
    f.text(552, 138, "엔올레이트 + 다른 분자 C=O → β-하이", size=10.5, anchor="start")
    f.text(552, 154, "드록시 케톤 → E1cB 탈수 → 공액", size=10.5, anchor="start")
    f.text(552, 170, "엔온 2-cyclohexylidenecyclohexan-", size=10.5, anchor="start")
    f.text(552, 186, "1-one ○", size=10.5, anchor="start")
    f.text(270, 225, "열역학적 조건(NaOEt, 실온·평형)이면 더 치환된 엔올레이트 → 2-ethyl-2-methylcyclohexanone이 주생성물",
           size=10.5, color=GRAY)
    return f.render()
