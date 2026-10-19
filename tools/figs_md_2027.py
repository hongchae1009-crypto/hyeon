"""MDEET 2027 자연과학Ⅱ 유기화학 21–30번 해설 그림."""
import math
from chemsvg import Mol, Fig, benzene, L, RED, BLUE, INK

GRAY = "#5b6270"
GREEN = "#1e8449"


def P(m, name, ox, oy):
    x, y = m.pos(name)
    return ox + x, oy + y


def num(f, m, name, ox, oy, t, dx=0, dy=-12, color=BLUE):
    x, y = P(m, name, ox, oy)
    f.text(x + dx, y + dy, t, size=10.5, color=color, weight="bold")


def ringnum(f, m, ox, oy, labels, center=(0, 0), k=1.42):
    """고리 원자 번호를 고리 바깥쪽에 표시. labels: {원자: 번호}"""
    for name, t in labels.items():
        x, y = m.pos(name)
        cx, cy = center
        f.text(ox + cx + (x - cx) * k, oy + cy + (y - cy) * k, t, size=10.5, color=BLUE, weight="bold")


def ok(f, x, y, good=True, t=None):
    f.text(x, y, t or ("○" if good else "✗"), size=15, weight="bold", color=GREEN if good else RED)


def chain(m, p, start, angs, labels=None, kinds=None):
    """start 원자에서 각도 목록대로 사슬을 잇는다. 반환: 원자 이름 목록"""
    names = [start]
    for i, a in enumerate(angs):
        lab = labels[i] if labels else None
        k = kinds[i] if kinds else 1
        names.append(m.sub(f"{p}{i + 1}", names[-1], a, lab, kind=k))
    return names


def newman(f, cx, cy, front, back, r=17, ln=17, color=INK):
    """front/back: [(각도, 라벨)] — 앞 탄소 결합은 중심에서, 뒤 탄소 결합은 원 둘레에서"""
    f.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{color}" stroke-width="1.4"/>')
    for ang, lab in back:
        a = math.radians(ang)
        x1, y1 = cx + r * math.cos(a), cy - r * math.sin(a)
        x2, y2 = cx + (r + ln) * math.cos(a), cy - (r + ln) * math.sin(a)
        f.raw(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1.4"/>')
        _nlab(f, x2, y2, a, lab)
    for ang, lab in front:
        a = math.radians(ang)
        x2, y2 = cx + (r + ln) * math.cos(a), cy - (r + ln) * math.sin(a)
        f.raw(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1.4"/>')
        _nlab(f, x2, y2, a, lab)


def _nlab(f, x, y, a, lab):
    c, s = math.cos(a), math.sin(a)
    anchor = "start" if c > 0.3 else ("end" if c < -0.3 else "middle")
    f.text(x + 4 * c + (2 if anchor == "start" else (-2 if anchor == "end" else 0)), y - 9 * s, lab, size=12, anchor=anchor)


def fischer(f, x, y, top, rows, bottom, dy=34, star=None, hl=None):
    """피셔 투영도. rows: [(왼쪽, 오른쪽)]. hl: {(행, 'l'|'r'): 색}"""
    hl = hl or {}
    n = len(rows)
    y1 = y - 12
    y2 = y + dy * (n - 1) + 12
    f.raw(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{INK}" stroke-width="1.4"/>')
    f.text(x, y1 - 10, top, size=12)
    f.text(x, y2 + 10, bottom, size=12)
    for i, (l, r) in enumerate(rows):
        yy = y + dy * i
        f.raw(f'<line x1="{x - 20}" y1="{yy}" x2="{x + 20}" y2="{yy}" stroke="{INK}" stroke-width="1.4"/>')
        f.text(x - 23, yy, l, size=12, anchor="end", color=hl.get((i, "l"), INK))
        f.text(x + 23, yy, r, size=12, anchor="start", color=hl.get((i, "r"), INK))


# ------------------------------------------------------------------ 21
def f21():
    f = Fig(800, 250)
    # ㄱ
    m = Mol()
    m.atom("c4", 0, 0)
    c3 = m.sub("c3", "c4", 30)
    m.sub("me", c3, 90)
    c2 = m.sub("c2", c3, -30)
    c1 = m.sub("c1", c2, 30)
    m.sub("br", c1, -30, "Br")
    ox, oy = 50, 110
    f.mol(m, ox, oy)
    for n, t, dy in (("c1", "1", -12), ("c2", "2", 13), ("c3", "3", 14), ("c4", "4", 13)):
        num(f, m, n, ox, oy, t, dy=dy)
    f.text(25, 40, "ㄱ", size=14, weight="bold")
    f.text(120, 175, "주사슬 4C, Br 쪽부터 번호", size=11.5, color=GRAY)
    f.text(120, 197, "1-Bromo-3-methylbutane", size=12.5, weight="bold")
    ok(f, 120, 222, True)
    # ㄴ
    m = Mol()
    m.atom("o", 0, 0, "HO", anchor="end")
    chain(m, "c", "o", [-30, 30, -30, 30, -30], [None, None, None, None, "Br"])
    ox, oy = 320, 100
    f.mol(m, ox, oy)
    for i, dy in ((1, 13), (2, -12), (3, 13), (4, -12)):
        num(f, m, f"c{i}", ox, oy, str(i), dy=dy)
    f.text(285, 40, "ㄴ", size=14, weight="bold")
    f.text(395, 175, "–OH(주작용기, 접미사) 탄소가 C1", size=11.5, color=GRAY)
    f.text(395, 197, "4-Bromobutan-1-ol", size=12.5, weight="bold")
    ok(f, 395, 222, True)
    # ㄷ
    m = Mol()
    m.ring("r", 0, 0, 6, L, 120, arom=[1])
    m.sub("m1", "r0", 90)
    m.sub("m2", "r0", 150)
    m.sub("m3", "r1", 30)
    ox, oy = 640, 105
    f.mol(m, ox, oy)
    ringnum(f, m, ox, oy, {"r1": "1", "r2": "2", "r3": "3", "r4": "4", "r5": "5"})
    num(f, m, "r0", ox, oy, "6", dx=12, dy=8)
    f.text(560, 40, "ㄷ", size=14, weight="bold")
    f.text(660, 160, "C=C에 1·2, 치환기 {1,6,6} < {2,3,3}", size=11.5, color=GRAY)
    f.text(660, 182, "옳은 이름: 1,6,6-Trimethylcyclohex-1-ene", size=12.5, weight="bold", color=BLUE)
    f.text(660, 202, "“1,2,2-…”: sp² C2에 CH₃ 2개 → 불가능", size=11.5, color=RED)
    ok(f, 660, 225, False)
    return f.render()


# ------------------------------------------------------------------ 22
def f22():
    f = Fig(800, 300)
    f.text(20, 22, "ㄱ. 알켄 안정도: 치환도가 클수록 안정", size=12.5, anchor="start", weight="bold")
    m = Mol()
    m.atom("a0", 0, 0)
    a = chain(m, "a", "a0", [-30, 30, -30, 30], kinds=[1, "2r", 1, 1])
    m.sub("me", "a2", 90)
    f.mol(m, 40, 75)
    f.text(95, 120, "3-methylpent-2-ene (삼치환)", size=11.5)
    f.text(200, 75, ">", size=18)
    m = Mol()
    m.atom("b0", 0, 0)
    chain(m, "b", "b0", [-30, 30, -30, 30], kinds=["2r", 1, 1, 1])
    m.sub("me", "b2", 90)
    f.mol(m, 235, 75)
    f.text(290, 120, "3-methylpent-1-ene (일치환)", size=11.5)
    f.text(190, 145, "ΔH°(수소화)가 작을수록 안정 · 초공액(C–H σ → π*) 수: 7 ≫ 2", size=11, color=GRAY)
    ok(f, 395, 75, True)
    # ㄴ
    f.text(440, 22, "ㄴ. ∠C–C–C", size=12.5, anchor="start", weight="bold")
    m = Mol()
    benzene(m, "r", 0, 0)
    f.mol(m, 485, 85)
    f.text(485, 135, "sp², 평면: 120°", size=11.5)
    f.text(545, 85, ">", size=18)
    m = Mol()
    pts = [(0, 0), (19, -37), (64, -26), (106, -37), (85, 0), (42, -11)]
    for i, (x, y) in enumerate(pts):
        m.atom(f"c{i}", x * 0.75, y * 0.75)
    for i in range(6):
        m.bond(f"c{i}", f"c{(i + 1) % 6}")
    f.mol(m, 580, 100)
    f.text(620, 135, "sp³, 의자형: ≈111°", size=11.5)
    ok(f, 730, 85, True)
    # ㄷ
    f.text(20, 178, "ㄷ. 표시된 C(H₃)–C(=O) 결합 길이", size=12.5, anchor="start", weight="bold")
    m = Mol()
    m.atom("me", 0, 0, "H_3C", anchor="end")
    c = m.sub("c", "me", 30)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("n", c, -30, "NH_2", anchor="start")
    m.set_bond("me", "c", 1, RED)
    f.mol(m, 80, 250)
    f.text(110, 285, "acetamide", size=11.5)
    f.text(190, 245, ">", size=18)
    m = Mol()
    m.atom("me", 0, 0, "H_3C", anchor="end")
    c = m.sub("c", "me", 30)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("n", c, -30, "CH_3", anchor="start")
    m.set_bond("me", "c", 1, RED)
    f.mol(m, 250, 250)
    f.text(280, 285, "acetone", size=11.5)
    f.text(390, 215, "케톤: π*C=O가 낮고 C=O 탄소의 δ+ 큼 → C–H σ(CH₃) → π*C=O 초공액이 강함", size=11, anchor="start")
    f.text(390, 235, "  → C(H₃)–C(=O)에 약간의 이중결합성 → 더 짧음", size=11, anchor="start")
    f.text(390, 257, "아마이드: n_N → π*C=O 공명이 π*를 이미 채우고 끌어올림", size=11, anchor="start")
    f.text(390, 277, "  → CH₃ 초공액 약화 → C–C가 상대적으로 김", size=11, anchor="start")
    ok(f, 360, 245, True)
    return f.render()


def f22b():
    f = Fig(800, 170)
    ox, oy = 90, 95
    m = Mol()
    m.atom("me", 0, 0, "H_3C", anchor="end")
    c = m.sub("c", "me", 30)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("n", c, -30, "NH_2", anchor="start")
    f.mol(m, ox, oy)
    nx, ny = P(m, "n", ox, oy)
    cx, cy = P(m, "c", ox, oy)
    o = P(m, "o", ox, oy)
    f.lp(nx - 2, ny + 11, -90)
    f.curly(nx - 6, ny + 13, (nx + cx) / 2 - 2, (ny + cy) / 2 + 5, bend=-0.5)
    f.curly(cx + 5, cy - 14, o[0] + 9, o[1] + 2, bend=0.7)
    f.resarrow(200, 250, 90)
    ox2 = 320
    m = Mol()
    m.atom("me", 0, 0, "H_3C", anchor="end")
    c = m.sub("c", "me", 30)
    m.sub("o", c, 90, "O")
    m.sub("n", c, -30, "NH_2", anchor="start", kind="2")
    f.mol(m, ox2, oy)
    o = P(m, "o", ox2, oy)
    n = P(m, "n", ox2, oy)
    f.charge(o[0] + 13, o[1] - 6, "-")
    f.charge(n[0] + 2, n[1] + 15, "+")
    f.text(570, 40, "아마이드 공명 (C–N 부분 이중결합)", size=12.5, weight="bold")
    f.text(570, 66, "C–N ≈ 1.38 Å (보통 C–N 1.47 Å보다 짧음)", size=11.5)
    f.text(570, 88, "C=O는 길어지고 카보닐 탄소의 δ+는 작아짐", size=11.5)
    f.text(570, 110, "→ π*C=O 에너지↑ → CH₃의 초공액 주개 효과↓", size=11.5)
    f.text(570, 132, "결과: C(H₃)–C(O) 아마이드 ≳ 케톤 (≈1.52 vs ≈1.51 Å)", size=11.5, color=RED)
    return f.render()


# ------------------------------------------------------------------ 23
def _trans12(m, left_w=True):
    m.ring("r", 0, 0, 6, L, 120)
    m.sub("a", "r0", 105)
    m.sub("b", "r1", 75)
    m.set_bond("r0", "a", "w" if left_w else "h")
    m.set_bond("r1", "b", "h" if left_w else "w")


def f23():
    f = Fig(800, 250)
    f.text(20, 22, "ㄱ. trans-1,2-dimethylcyclohexane의 두 거울상", size=12.5, anchor="start", weight="bold")
    m = Mol()
    _trans12(m, True)
    f.mol(m, 80, 120)
    f.text(80, 175, "(1R,2R)", size=12, color=BLUE)
    f.raw(f'<line x1="150" y1="55" x2="150" y2="185" stroke="{GRAY}" stroke-dasharray="5 4"/>')
    f.text(150, 200, "거울면", size=11, color=GRAY)
    m = Mol()
    _trans12(m, False)
    f.mol(m, 220, 120)
    f.text(220, 175, "(1S,2S)", size=12, color=BLUE)
    f.text(150, 228, "겹쳐지지 않음 → 거울상이성질체 (같은 화합물 ✗)", size=11.5, color=RED)
    # ㄴ
    f.text(420, 22, "ㄴ. 두 뉴먼 투영 = 모두 2-methylbutane", size=12.5, anchor="start", weight="bold")
    newman(f, 500, 115, [(90, "H"), (210, "H"), (330, "CH_3")], [(150, "H_3C"), (30, "H"), (270, "CH_3")])
    newman(f, 680, 115, [(90, "H"), (210, "H_3C"), (330, "H")], [(150, "H"), (30, "CH_3"), (270, "CH_3")])
    f.text(590, 185, "앞 C: H, H, CH₃ (= CH₂CH₃의 CH₂)  ·  뒤 C: CH₃, CH₃, H (= CH(CH₃)₂)", size=11)
    f.text(590, 207, "둘 다 CH₃↔CH₃ gauche 1개 + anti 1개인 엇갈린 형태 (서로 거울상 형태)", size=11)
    f.text(590, 229, "비카이랄 분자 + C–C 회전으로 상호 전환 → 같은 화합물 ○", size=11.5, color=GREEN)
    return f.render()


def f23b():
    f = Fig(800, 270)
    f.text(20, 22, "ㄷ. (1S,2S,5R)-2,5-dimethylcyclohexan-1-amine — 평면 구조식과 의자형", size=12.5, anchor="start",
           weight="bold")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 120)
    m.sub("me2", "r0", 120)
    m.set_bond("r0", "me2", "h")
    m.sub("n", "r1", 60, "NH_2", anchor="start")
    m.set_bond("r1", "n", "w")
    m.sub("me5", "r3", -60)
    m.set_bond("r3", "me5", "h")
    ox, oy = 110, 130
    f.mol(m, ox, oy)
    ringnum(f, m, ox, oy, {"r5": "3", "r4": "4", "r2": "6"})
    num(f, m, "r1", ox, oy, "1", dx=-12, dy=-4)
    num(f, m, "r0", ox, oy, "2", dx=12, dy=-4)
    num(f, m, "r3", ox, oy, "5", dx=-14, dy=4)
    f.text(110, 205, "C1 NH₂ 위, C2 CH₃ 아래, C5 CH₃ 아래", size=11.5)
    f.text(250, 130, "=", size=22)
    # 의자형 (문항 그림 좌표)
    m = Mol()
    pts = {"c4": (1078, 412), "c3": (1110, 350), "c1x": (1185, 368), "c6": (1255, 350), "c5": (1220, 412), "c4b": (1148, 393)}
    sc = 0.95
    names = ["A", "B", "C", "D", "E", "F"]
    coords = [(1078, 412), (1110, 350), (1185, 368), (1255, 350), (1220, 412), (1148, 393)]
    for nme, (x, y) in zip(names, coords):
        m.atom(nme, (x - 1078) * sc, (y - 412) * sc)
    for i in range(6):
        m.bond(names[i], names[(i + 1) % 6])
    m.atom("me2", (1040 - 1078) * sc, (368 - 412) * sc)
    m.bond("B", "me2")
    m.atom("n", (1210 - 1078) * sc, (322 - 412) * sc, "NH_2")
    m.bond("C", "n")
    m.atom("me5", (1220 - 1078) * sc, (488 - 412) * sc)
    m.bond("E", "me5")
    ox, oy = 320, 140
    f.mol(m, ox, oy)
    for n, t, dx, dy in (("C", "1", -2, 14), ("B", "2", 2, -12), ("A", "3", -10, 6), ("F", "4", 0, 13),
                         ("E", "5", 12, 4), ("D", "6", 10, -8)):
        num(f, m, n, ox, oy, t, dx=dx, dy=dy)
    f.text(410, 255, "NH₂(eq, 위) · C2-CH₃(eq, 아래) · C5-CH₃(ax, 아래)", size=11.5)
    tx = 560
    f.text(tx, 70, "① 치환 위치 1,2,5 동일", size=11.5, anchor="start")
    f.text(tx, 94, "② 1,2-trans: eq/eq ↔ 위/아래 ✓", size=11.5, anchor="start")
    f.text(tx, 118, "③ 1,5(1,3 관계)-trans: eq/ax ↔ 위/아래 ✓", size=11.5, anchor="start")
    f.text(tx, 142, "④ 2,5(1,4 관계)-cis: eq/ax ↔ 아래/아래 ✓", size=11.5, anchor="start")
    f.text(tx, 166, "⑤ 위에서 본 C1→C2 방향도 같음 → 거울상 아님", size=11.5, anchor="start")
    f.text(tx, 194, "→ 같은 화합물 ○", size=12.5, anchor="start", weight="bold", color=GREEN)
    return f.render()


# ------------------------------------------------------------------ 24
def f24():
    f = Fig(800, 270)
    f.text(20, 22, "L-threose의 C2 배열 판정과 알도테트로스의 입체이성질체 4개", size=12.5, anchor="start", weight="bold")
    fischer(f, 110, 110, "CHO ②", [("H ④", "OH ①"), ("HO", "H")], "CH₂OH", hl={(0, "r"): RED, (0, "l"): GRAY})
    f.text(110, 82, "", size=10)
    f.raw(f'<path d="M150,108 A30,30 0 0 0 112,72" fill="none" stroke="{RED}" stroke-width="1.4" marker-end="url(#{f.id}r)"/>')
    f.text(110, 215, "①→②→③ 반시계(S), H가 가로 → 뒤집어 R", size=11)
    f.text(110, 236, "③ = C3(O,C,H) < ② CHO(O,O,H)", size=11, color=GRAY)
    xs = [360, 470, 600, 710]
    data = [("D-erythrose", [("H", "OH"), ("H", "OH")], "(2R,3R)"),
            ("L-erythrose", [("HO", "H"), ("HO", "H")], "(2S,3S)"),
            ("D-threose", [("HO", "H"), ("H", "OH")], "(2S,3R)"),
            ("L-threose", [("H", "OH"), ("HO", "H")], "(2R,3S)")]
    for x, (nm, rows, cfg) in zip(xs, data):
        fischer(f, x, 95, "CHO", rows, "CH₂OH")
        f.text(x, 175, nm, size=12, weight="bold", color=BLUE if nm == "L-threose" else INK)
        f.text(x, 195, cfg, size=11.5)
    f.raw(f'<line x1="415" y1="60" x2="415" y2="160" stroke="{GRAY}" stroke-dasharray="4 3"/>')
    f.raw(f'<line x1="655" y1="60" x2="655" y2="160" stroke="{GRAY}" stroke-dasharray="4 3"/>')
    f.text(415, 215, "거울상", size=11, color=GRAY)
    f.text(655, 215, "거울상", size=11, color=GRAY)
    f.text(535, 240, "입체 중심 2개, 메조 없음 → 2² = 4개 (ㄴ ✗) · erythrose ↔ threose = 부분입체이성질체", size=11.5)
    return f.render()


def f24b():
    f = Fig(800, 195)
    f.text(20, 22, "ㄷ의 구조 = D-erythrose (2R,3R) → L-threose (2R,3S)와 부분입체이성질체", size=12.5, anchor="start",
           weight="bold")
    m = Mol()
    m.atom("h", 0, 0, "H")
    c1 = m.sub("c1", "h", 30)
    m.sub("o", c1, 90, "O", kind="2")
    c2 = m.sub("c2", c1, -30)
    m.sub("o2", c2, -90, "OH")
    m.set_bond("c2", "o2", "w")
    c3 = m.sub("c3", c2, 30)
    m.sub("o3", c3, 90, "OH")
    m.set_bond("c3", "o3", "h")
    c4 = m.sub("c4", c3, -30)
    m.sub("o4", c4, 30, "OH", anchor="start")
    ox, oy = 60, 100
    f.mol(m, ox, oy)
    f.text(130, 172, "C2: R  ·  C3: R", size=11.5, color=RED, weight="bold")
    f.arrow(250, 100, 320, 100, "피셔 변환", "")
    fischer(f, 400, 85, "CHO", [("H", "OH"), ("H", "OH")], "CH₂OH")
    f.text(400, 165, "D-erythrose", size=12, weight="bold")
    f.text(540, 70, "C2: L-threose와 같음 (R)", size=11.5, anchor="start")
    f.text(540, 94, "C3: L-threose는 S, 이 구조는 R", size=11.5, anchor="start")
    f.text(540, 118, "→ 1곳만 다름 = 부분입체이성질체(에피머)", size=11.5, anchor="start")
    f.text(540, 146, "거울상이 되려면 두 중심이 모두 반대여야 함", size=11.5, anchor="start", color=RED)
    return f.render()


# ------------------------------------------------------------------ 25
def f25():
    f = Fig(800, 330)
    rr = 25.5
    # ㄱ
    f.text(20, 22, "ㄱ. 짝염기 안정성", size=12.5, anchor="start", weight="bold")
    m = Mol()
    m.ring("a", 0, 0, 5, rr, 90)
    f.mol(m, 70, 85)
    f.text(70, 130, "cyclopentane", size=11)
    f.text(70, 148, "pKₐ ≈ 50", size=11.5, weight="bold")
    f.text(130, 85, "<", size=18)
    m = Mol()
    m.ring("b", 0, 0, 5, rr, 90, arom=[1, 3])
    f.mol(m, 190, 85)
    f.text(190, 130, "1,3-cyclopentadiene", size=11)
    f.text(190, 148, "pKₐ ≈ 16", size=11.5, weight="bold")
    f.arrow(240, 85, 290, 85, "−H^+", "")
    m = Mol()
    m.ring("c", 0, 0, 5, rr, 90, arom=[1, 3])
    f.mol(m, 340, 85)
    f.charge(340, 85 - rr - 10, "-")
    f.text(340, 130, "C₅H₅⁻: 6π 방향족", size=11)
    f.text(340, 148, "(음전하 5탄소 비편재)", size=11, color=GRAY)
    ok(f, 395, 85, False)
    f.text(220, 172, "cyclopentane > cyclopentadiene 산도라는 ㄱ은 틀림", size=11, color=RED)
    # ㄴ
    f.text(440, 22, "ㄴ. N 비공유쌍의 위치", size=12.5, anchor="start", weight="bold")
    m = Mol()
    m.ring("d", 0, 0, 5, rr, -90)
    m.label("d0", "NH")
    f.mol(m, 500, 80)
    f.lp(500, 80 + rr + 10, -90)
    f.text(500, 130, "pyrrolidine: sp³ N", size=11)
    f.text(500, 148, "pKₐH ≈ 11.3", size=11.5, weight="bold")
    f.text(565, 80, ">", size=18)
    m = Mol()
    m.ring("e", 0, 0, 5, rr, -90, arom=[1, 3])
    m.label("e0", "NH")
    f.mol(m, 640, 80)
    f.text(640, 135, "pyrrole: 비공유쌍 = 6π 일부", size=11)
    f.text(640, 153, "pKₐH ≈ −3.8 (C2 양성자화)", size=11.5, weight="bold")
    ok(f, 740, 80, True)
    # ㄷ
    f.text(20, 205, "ㄷ. 물에 대한 용해도 (O 비공유쌍의 수소결합 받개 능력)", size=12.5, anchor="start", weight="bold")
    m = Mol()
    m.ring("f", 0, 0, 5, rr, -90)
    m.label("f0", "O")
    f.mol(m, 80, 260)
    f.lp(80 - 9, 260 + rr + 8, -135)
    f.lp(80 + 9, 260 + rr + 8, -45)
    f.text(80, 312, "THF: 물과 완전 혼화", size=11.5)
    f.text(150, 260, ">", size=18)
    m = Mol()
    m.ring("g", 0, 0, 5, rr, -90, arom=[1, 3])
    m.label("g0", "O")
    f.mol(m, 220, 260)
    f.text(220, 312, "furan: ≈1 g/100 mL", size=11.5)
    f.text(300, 245, "THF: sp³ O의 두 비공유쌍이 국재 → H₂O와 강한 수소결합, 쌍극자 ≈1.7 D", size=11, anchor="start")
    f.text(300, 267, "furan: O 비공유쌍 1개가 방향족 6π에 비편재 → 받개 능력·쌍극자(≈0.7 D) 작음", size=11, anchor="start")
    f.text(300, 289, "∴ 용해도 THF > furan", size=11.5, anchor="start", color=GREEN)
    ok(f, 280, 260, True)
    return f.render()


# ------------------------------------------------------------------ 26
def _butyne(m):
    m.atom("c1", 0, 0)
    m.sub("c2", "c1", 20)
    m.sub("c3", "c2", 20, kind=3)
    m.sub("c4", "c3", 20)


def _alkene(m, cis=True):
    m.atom("c2", 0, 0)
    m.sub("c3", "c2", 0, kind="2")
    m.sub("c1", "c2", 240)
    m.sub("c4", "c3", -60 if cis else 60)


def _epox(m, k2="w", k3="w"):
    m.atom("c2", 0, 0)
    m.sub("c3", "c2", 0)
    m.atom("o", 15, -24, "O")
    m.bond("c2", "o")
    m.bond("c3", "o")
    m.sub("m2", "c2", 210)
    m.set_bond("c2", "m2", k2)
    m.sub("m3", "c3", -30)
    m.set_bond("c3", "m3", k3)


def _diol(m):
    m.atom("c1", 0, 0)
    m.sub("c2", "c1", 30)
    m.sub("o2", "c2", 90, "OH")
    m.set_bond("c2", "o2", "w")
    m.sub("c3", "c2", -30)
    m.sub("o3", "c3", -90, "OH")
    m.set_bond("c3", "o3", "h")
    m.sub("c4", "c3", 30)


def f26():
    f = Fig(800, 300)
    m = Mol()
    _butyne(m)
    f.mol(m, 20, 150)
    f.text(60, 175, "but-2-yne", size=11)
    f.raw(f'<path d="M115,140 L135,140 L135,70 L160,70 M135,140 L135,220 L160,220" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    f.arrow(160, 70, 235, 70, "H₂, Lindlar", "syn 첨가")
    m = Mol()
    _alkene(m, True)
    f.mol(m, 265, 70)
    f.cap(280, 115, "A: cis-but-2-ene")
    f.arrow(325, 70, 410, 70, "mCPBA", "syn, 입체특이적")
    m = Mol()
    _epox(m)
    f.mol(m, 450, 80)
    f.cap(465, 115, "B: cis-2,3-dimethyloxirane")
    f.text(465, 133, "(메조, 대칭면) — ㄴ ○", size=11, color=GREEN)
    f.arrow(160, 220, 235, 220, "Na, NH₃(l)", "anti 첨가")
    m = Mol()
    _alkene(m, False)
    f.mol(m, 265, 225)
    f.cap(280, 265, "C: trans-but-2-ene")
    f.arrow(325, 220, 410, 220, "1. mCPBA", "")
    m = Mol()
    _epox(m, "w", "h")
    f.mol(m, 445, 230)
    f.text(460, 262, "trans-에폭사이드 (라셈)", size=11)
    f.arrow(505, 220, 590, 220, "2. HO⁻, H₂O", "SN2 anti 개환")
    m = Mol()
    _diol(m)
    f.mol(m, 625, 225)
    f.cap(668, 280, "D: meso-butane-2,3-diol — ㄷ ○")
    f.text(400, 160, "A·C: cis/trans = 부분입체이성질체(입체이성질체) → ‘구조 이성질체’ ㄱ ✗", size=11.5, color=RED)
    return f.render()


def f26b():
    f = Fig(800, 210)
    f.text(20, 22, "D 생성: trans-에폭사이드의 염기성 개환 (뒤쪽 공격 → 반전)", size=12.5, anchor="start", weight="bold")
    # 에폭사이드 (R,R) 한쪽 거울상
    m = Mol()
    _epox(m, "w", "h")
    ox, oy = 150, 110
    f.mol(m, ox, oy)
    c2 = P(m, "c2", ox, oy)
    o = P(m, "o", ox, oy)
    f.text(c2[0] - 8, c2[1] + 45, "HO^−", size=13)
    f.curly(c2[0] - 6, c2[1] + 34, c2[0] - 2, c2[1] + 6, bend=-0.4)
    f.curly((c2[0] + o[0]) / 2 + 2, (c2[1] + o[1]) / 2 + 2, o[0] - 6, o[1] - 10, bend=-0.6)
    f.arrow(250, 110, 320, 110, "", "")
    f.text(285, 95, "C2 반전", size=11)
    m = Mol()
    _diol(m)
    m.label("o3", "O^−")
    f.mol(m, 345, 110)
    f.text(395, 160, "알콕사이드", size=11)
    f.arrow(450, 110, 520, 110, "H₂O", "양성자 이동")
    m = Mol()
    _diol(m)
    f.mol(m, 560, 110)
    f.text(610, 160, "(2R,3S) = 메조", size=12, weight="bold", color=BLUE)
    f.text(400, 192, "어느 탄소를 공격하든, 어느 거울상에서 출발하든 같은 메조 다이올 → D는 광학 비활성 단일 화합물", size=11)
    return f.render()


# ------------------------------------------------------------------ 27
def _acnh(m, p, ring_start=90):
    benzene(m, p, 0, 0, start=90)
    n = m.sub(p + "n", p + "0", 90, "NH")
    c = m.sub(p + "c", n, 30)
    m.sub(p + "o", c, 90, "O", kind="2")
    m.sub(p + "m", c, -30)


def f27():
    f = Fig(800, 360)
    m = Mol()
    benzene(m, "a", 0, 0)
    m.sub("n", "a0", 90, "NH_2")
    f.mol(m, 50, 120)
    f.arrow(95, 120, 165, 120, "CH₃COCl", "pyridine")
    m = Mol()
    _acnh(m, "b")
    f.mol(m, 205, 120)
    f.cap(205, 172, "A: acetanilide (ㄱ ○)")
    f.arrow(275, 120, 345, 120, "(가) Br₂", "CH₃COOH")
    m = Mol()
    _acnh(m, "c")
    m.sub("br", "c3", -90, "Br")
    f.mol(m, 385, 120)
    f.cap(385, 195, "B: 4-bromoacetanilide")
    f.arrow(455, 120, 530, 120, "HO⁻, H₂O", "가열")
    m = Mol()
    benzene(m, "d", 0, 0)
    m.sub("n", "d0", 90, "NH_2")
    m.sub("br", "d3", -90, "Br")
    f.mol(m, 575, 120)
    f.text(690, 90, "–NHCOCH₃: 중간 활성 o/p", size=11)
    f.text(690, 110, "(N 비공유쌍이 C=O와 공명)", size=11, color=GRAY)
    f.text(690, 130, "→ 일치환·para 우세", size=11)
    f.text(690, 150, "–NH₂ 그대로면 2,4,6-트라이브로모", size=11, color=RED)
    # 두 번째 줄
    m = Mol()
    benzene(m, "e", 0, 0)
    m.sub("n", "e0", 90, "NO_2")
    f.mol(m, 50, 280)
    f.arrow(95, 280, 175, 280, "Br₂", "FeBr₃")
    m = Mol()
    benzene(m, "f", 0, 0)
    m.sub("n", "f0", 90, "NO_2")
    m.sub("br", "f2", -30, "Br")
    f.mol(m, 220, 280)
    f.cap(225, 342, "C: 1-bromo-3-nitrobenzene")
    f.arrow(285, 280, 365, 280, "Fe", "HCl")
    m = Mol()
    benzene(m, "g", 0, 0)
    m.sub("n", "g0", 90, "NH_2")
    m.sub("br", "g2", -30, "Br")
    f.mol(m, 410, 280)
    f.cap(415, 342, "D: 3-bromoaniline (ㄷ ○)")
    f.text(620, 255, "–NO₂: 강한 불활성화·meta 지향", size=11)
    f.text(620, 275, "(o/p σ 착물은 N⁺ 옆 C⁺ → 불안정)", size=11, color=GRAY)
    f.text(620, 295, "Fe/HCl: NO₂ → NH₂ (Ar–Br 유지)", size=11)
    f.text(620, 315, "순서가 핵심: 먼저 Br, 나중에 환원", size=11, color=BLUE)
    return f.render()


# ------------------------------------------------------------------ 28
def _sk(m, x_label, kind):
    """3-methylbutan-2-yl X: C2 위, X는 kind(w/h)"""
    m.atom("c1", 0, 0)
    m.sub("c2", "c1", 30)
    m.sub("x", "c2", 90, x_label)
    m.set_bond("c2", "x", kind)
    m.sub("c3", "c2", -30)
    m.sub("m3", "c3", -90)
    m.sub("c4", "c3", 30)


def f28():
    f = Fig(800, 420)
    f.text(20, 22, "기준 반응: Finkelstein형 SN2 (뒤쪽 공격, 배열 반전)", size=12.5, anchor="start", weight="bold")
    m = Mol()
    _sk(m, "Cl", "w")
    f.mol(m, 60, 90)
    f.text(90, 135, "(R)-2-chloro-3-methylbutane", size=11)
    f.arrow(180, 85, 270, 85, "LiBr", "acetone (SN2)")
    m = Mol()
    _sk(m, "Br", "h")
    f.mol(m, 310, 90)
    f.cap(340, 135, "A: (S)-2-bromo-3-methylbutane")
    f.text(470, 70, "Br⁻가 C–Cl의 σ* 뒤쪽 로브 공격 → Walden 반전", size=11, anchor="start")
    f.text(470, 92, "Cl·Br은 CIP 순위가 같은 자리(1순위) → R → S", size=11, anchor="start")
    f.text(470, 114, "acetone: LiCl 침전·극성 비양성자성 → SN2 유리", size=11, anchor="start", color=GRAY)
    y = 175
    rows = [
        ("ㄱ", "2-methylbut-2-ene", "HBr", "Markovnikov: 3° 탄소 양이온", "2-bromo-2-methylbutane (구조 다름)", False),
        ("ㄴ", "(R)-3-methylbutan-2-ol", "PBr₃", "ROPBr₂ 형성(보존) → Br⁻ SN2(반전)", "(S)-2-bromo-3-methylbutane = A", True),
        ("ㄷ", "(S)-3-methylbutan-2-ol", "1. TsCl, py  2. LiBr", "ROTs(C–O 유지, 보존) → SN2(반전)", "(R)-2-bromo-3-methylbutane = A의 거울상", False),
    ]
    for i, (k, sm, rg, how, prod, good) in enumerate(rows):
        yy = y + i * 80
        f.text(20, yy + 10, k, size=14, weight="bold")
        m = Mol()
        if i == 0:
            m.atom("c1", 0, 0)
            m.sub("c2", "c1", 30)
            m.sub("c3", "c2", -30, kind="2r")
            m.sub("m3", "c3", -90)
            m.sub("c4", "c3", 30)
        else:
            _sk(m, "OH", "w" if i == 1 else "h")
        f.mol(m, 50, yy + 25)
        f.arrow(150, yy + 15, 240, yy + 15, rg, "")
        m = Mol()
        if i == 0:
            m.atom("c1", 0, 0)
            m.sub("c2", "c1", 30)
            m.sub("c3", "c2", -30)
            m.sub("m3", "c3", -90)
            m.sub("br", "c3", 90, "Br")
            m.sub("c4", "c3", 30)
        else:
            _sk(m, "Br", "h" if i == 1 else "w")
        f.mol(m, 270, yy + 25)
        f.text(390, yy + 2, how, size=11, anchor="start")
        f.text(390, yy + 24, prod, size=11.5, anchor="start", weight="bold", color=GREEN if good else RED)
        ok(f, 770, yy + 14, good)
    return f.render()


# ------------------------------------------------------------------ 29
def _octalin(m):
    m.ring("a", 0, 0, 6, L, 90)
    m.set_bond("a1", "a2", "2")
    m.ring("b", 2 * L * math.cos(math.radians(30)), 0, 6, L, 90, bonds=False)
    for p, q in (("b5", "b0"), ("b0", "b1"), ("b1", "b2"), ("b2", "b3"), ("b3", "b4")):
        m.bond(p, q)
    m.bond("b4", "a2")
    m.bond("b5", "a1")


def _c10(m, p, ko):
    r = L / (2 * math.sin(math.radians(18)))
    m.ring(p, 0, 0, 10, r, 162)
    for k in ko:
        x0, y0 = m.pos(f"{p}{k}")
        ang = math.degrees(math.atan2(-y0, x0))
        m.sub(f"{p}o{k}", f"{p}{k}", ang, "O", kind="2")


def f29():
    f = Fig(800, 260)
    f.text(20, 22, "③ 오존 분해: C9=C10이 끊겨 두 C=O가 되고, 두 6원 고리가 하나의 10원 고리로", size=12.5, anchor="start",
           weight="bold")
    m = Mol()
    _octalin(m)
    ox, oy = 50, 130
    f.mol(m, ox, oy)
    a1 = P(m, "a1", ox, oy)
    a2 = P(m, "a2", ox, oy)
    f.text(a1[0] + 9, a1[1] - 4, "a", size=11, color=RED, weight="bold")
    f.text(a2[0] + 9, a2[1] + 5, "b", size=11, color=RED, weight="bold")
    f.arrow(160, 130, 245, 130, "1. O₃", "2. Zn, AcOH")
    f.text(200, 170, "(몰오조나이드 →", size=10.5, color=GRAY)
    f.text(200, 184, "오조나이드 → 환원)", size=10.5, color=GRAY)
    m = Mol()
    _c10(m, "c", [0, 5])
    ox, oy = 340, 130
    f.mol(m, ox, oy)
    f.cap(340, 225, "cyclodecane-1,6-dione (옳은 생성물)")
    f.text(340, 243, "두 C=O 사이 CH₂: 4개 / 4개", size=11, color=GREEN)
    m = Mol()
    _c10(m, "d", [0, 4])
    ox, oy = 610, 130
    f.mol(m, ox, oy)
    f.cross(610, 130, 14)
    f.cap(610, 225, "문항의 그림: cyclodecane-1,5-dione")
    f.text(610, 243, "CH₂ 3개 / 5개 → 원래 탄소 배열과 불일치", size=11, color=RED)
    return f.render()


def f29b():
    f = Fig(800, 300)
    f.text(20, 22, "④ trans-hex-3-ene + Br₂: 브로모늄 이온 → Br⁻ anti 공격 → meso", size=12.5, anchor="start", weight="bold")
    m = Mol()
    m.atom("c3", 0, 0)
    m.sub("c4", "c3", 0)
    m.atom("br", 15, -26, "Br^+")
    m.bond("c3", "br")
    m.bond("c4", "br")
    m.sub("e3", "c3", 210)
    m.set_bond("c3", "e3", "w")
    m.sub("e3b", "e3", 150)
    m.sub("e4", "c4", 30)
    m.set_bond("c4", "e4", "h")
    m.sub("e4b", "e4", -30)
    ox, oy = 110, 110
    f.mol(m, ox, oy)
    c4 = P(m, "c4", ox, oy)
    f.text(c4[0] + 25, c4[1] + 40, "Br^−", size=13)
    f.curly(c4[0] + 18, c4[1] + 32, c4[0] + 3, c4[1] + 6, bend=0.3)
    f.text(130, 165, "브로모늄 (뒤쪽 면만 열림)", size=11)
    f.arrow(240, 110, 320, 110, "anti", "")
    m = Mol()
    m.atom("e1", 0, 0)
    chain(m, "z", "e1", [30, -30, 30, -30, 30])
    m.sub("b3", "z2", 90, "Br")
    m.set_bond("z2", "b3", "w")
    m.sub("b4", "z3", -90, "Br")
    m.set_bond("z3", "b4", "h")
    f.mol(m, 350, 115)
    f.text(430, 175, "(3R,4S)-3,4-dibromohexane = meso (○)", size=11.5, color=GREEN)
    f.text(640, 70, "다른 선지 요약", size=12, weight="bold")
    f.text(640, 94, "① 수은 이온: 자리옮김 없음,", size=11)
    f.text(640, 110, "   Markovnikov → 3-methylbutan-2-ol ○", size=11)
    f.text(640, 134, "② 수소붕소화: 역-Markovnikov, syn", size=11)
    f.text(640, 150, "   → hexan-1-ol ○", size=11)
    f.text(640, 174, "⑤ Br₂/H₂O: 브로모늄을 H₂O가", size=11)
    f.text(640, 190, "   더 치환된 C에서 공격 → 3° OH ○", size=11)
    f.text(400, 230, "cf. 3-methylbut-1-ene + H₃O⁺(산 촉매 수화)였다면 2°→3° 수소 이동 → 2-methylbutan-2-ol", size=11,
           color=GRAY)
    f.text(400, 252, "옥시수은화는 고리형 머큐리늄 이온이 자유 탄소 양이온을 만들지 않아 자리옮김이 없다", size=11, color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 30
def _enone(m, p="r", oh=False, keto=True, db=True, me3=False):
    m.ring(p, 0, 0, 6, L, 90, arom=[2] if db else None)
    if keto:
        m.sub(p + "o", p + "1", 30, "O", kind="2")
    if oh:
        m.sub(p + "o", p + "1", 30, "OH", anchor="start")
    if me3:
        m.sub(p + "m", p + "3", -90)


def f30():
    f = Fig(800, 350)
    m = Mol()
    _enone(m)
    ox, oy = 70, 170
    f.mol(m, ox, oy)
    ringnum(f, m, ox, oy, {"r2": "2", "r3": "3"})
    num(f, m, "r1", ox, oy, "1", dx=-4, dy=-12)
    f.text(70, 222, "cyclohex-2-en-1-one", size=11)
    f.raw(f'<path d="M125,170 L150,170 M150,60 L150,280 M150,60 L175,60 M150,170 L175,170 M150,280 L175,280" '
          f'fill="none" stroke="{INK}" stroke-width="1.4"/>')
    rows = [(60, "1. LiAlH₄ 2. H₂O", "H⁻: 단단한 친핵체 → C=O 직접(1,2-) 첨가", dict(oh=True, keto=False, db=True),
             "A: cyclohex-2-en-1-ol"),
            (170, "H₂ (1당량), Pd/C", "C=C가 C=O보다 훨씬 빨리 수소화", dict(keto=True, db=False), "B: cyclohexanone"),
            (280, "1. (CH₃)₂CuLi 2. H₂O", "큐프레이트: 부드러운 친핵체 → β-C(1,4-) 공격", dict(keto=True, db=False, me3=True),
             "C: 3-methylcyclohexanone")]
    for yy, rg, why, kw, nm in rows:
        f.arrow(178, yy, 300, yy, rg, "")
        m = Mol()
        _enone(m, **kw)
        f.mol(m, 345, yy)
        f.text(420, yy - 8, nm, size=12, anchor="start", weight="bold", color=BLUE)
        f.text(420, yy + 12, why, size=11, anchor="start")
    f.text(420, 312, "→ 엔올레이트 생성 후 H₂O로 α-C 양성자화(토토머화)", size=11, anchor="start", color=GRAY)
    return f.render()


def f30b():
    f = Fig(800, 200)
    f.text(20, 22, "1,4-(짝지은) 첨가 메커니즘: 큐프레이트 → β 탄소, 엔올레이트 → 케톤", size=12.5, anchor="start", weight="bold")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90, arom=[2])
    m.sub("o", "r1", 30, "O", kind="2")
    ox, oy = 110, 110
    f.mol(m, ox, oy)
    r3 = P(m, "r3", ox, oy)
    r2 = P(m, "r2", ox, oy)
    r1 = P(m, "r1", ox, oy)
    o = P(m, "o", ox, oy)
    f.text(r3[0] - 5, r3[1] + 50, "(CH₃)₂CuLi", size=12)
    f.curly(r3[0] - 2, r3[1] + 40, r3[0] + 1, r3[1] + 6, bend=0.3)
    f.curly((r2[0] + r3[0]) / 2 + 3, (r2[1] + r3[1]) / 2 + 3, (r1[0] + r2[0]) / 2 + 4, (r1[1] + r2[1]) / 2, bend=0.5)
    f.curly((r1[0] + o[0]) / 2 - 2, (r1[1] + o[1]) / 2 - 6, o[0] + 2, o[1] - 12, bend=-0.6)
    f.text(r3[0] - 12, r3[1] + 10, "β", size=12, color=RED, weight="bold")
    f.arrow(210, 110, 290, 110, "", "")
    m = Mol()
    m.ring("s", 0, 0, 6, L, 90, arom=[1])
    m.sub("o", "s1", 30, "O^−", anchor="start")
    m.sub("m", "s3", -90)
    f.mol(m, 340, 110)
    f.text(340, 175, "리튬 엔올레이트", size=11)
    f.arrow(410, 110, 490, 110, "H₂O", "")
    m = Mol()
    _enone(m, "t", keto=True, db=False, me3=True)
    f.mol(m, 540, 110)
    f.text(540, 175, "C (라셈)", size=11)
    f.text(690, 110, "LiAlH₄ (A):", size=11, weight="bold")
    f.text(690, 98, "H⁻ → C1(카보닐 C)", size=11)
    f.text(690, 122, "Grignard·RLi도 1,2", size=11, color=GRAY)
    f.text(690, 140, "Gilman·엔올레이트·", size=11, color=GRAY)
    f.text(690, 156, "아민 등은 1,4", size=11, color=GRAY)
    return f.render()
