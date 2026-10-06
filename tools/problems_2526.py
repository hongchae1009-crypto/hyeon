"""2025·2026학년도 유기화학 기출 — 문제지용 재구성 (정답 미포함).

원본 시험지 대신 기존 모범답안 파일의 '문제 요지'를 바탕으로 문제 형태로 다시 쓰고 도식을 새로 그렸다.
"""
import math
from chemsvg import Mol, Fig, benzene, L, RED, BLUE, INK


def _scheme_arrow(f, x1, x2, y, top, bot=None):
    f.arrow(x1, y, x2, y, top, bot)


def _box_label(f, x, y, t, sub=None):
    f.text(x, y, t, size=17, weight="bold")
    if sub:
        f.text(x, y + 20, sub, size=11.5)


# ------------------------------------------------------------- 2025 A 서술형 10
def f25a10():
    f = Fig(800, 250)
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    m.sub("me", "r0", 90, "CH_3")
    f.mol(m, 55, 110)
    f.text(55, 175, "toluene", size=12)
    _scheme_arrow(f, 100, 215, 110, "Cl₂, FeCl₃")
    _box_label(f, 240, 110, "A")
    _scheme_arrow(f, 265, 420, 110, "1) KMnO₄, H₂O, 가열", "2) H₃O⁺")
    _box_label(f, 445, 110, "B")
    _scheme_arrow(f, 470, 600, 110, "1) SOCl₂", "2) NH₃")
    _box_label(f, 630, 110, "C", "(C₇H₆NOCl)")
    f.arrow(630, 145, 630, 200, None, None)
    f.text(642, 165, "1) NaOH, Br₂", size=11, anchor="start")
    f.text(642, 182, "2) H₂O", size=11, anchor="start")
    _box_label(f, 630, 222, "D", "")
    f.text(660, 222, "(C₆H₆NCl)", size=11.5, anchor="start")
    return f.render()


# ------------------------------------------------------------- 2025 A 서술형 11
def f25a11():
    f = Fig(800, 300)
    m = Mol()
    c1 = m.atom("c1", 0, 0)
    c2 = m.sub("c2", c1, -30)
    m.sub("c2m", c2, -90)
    c3 = m.sub("c3", c2, 30)
    c4 = m.sub("c4", c3, -30, kind="2r")
    c5 = m.sub("c5", c4, 30)
    c6 = m.sub("c6", c5, -30)
    c7 = m.sub("c7", c6, 30)
    m.sub("br", c7, -30, "Br")
    f.mol(m, 20, 80)
    f.text(130, 150, "(E)-7-bromo-2-methyl-3-heptene", size=11.5)
    _scheme_arrow(f, 250, 410, 85, "1) NaCH(CO₂Et)₂", "2) H₃O⁺")
    _box_label(f, 440, 85, "A", "(C₁₁H₁₈O₄)")
    _scheme_arrow(f, 475, 590, 85, "가열")
    _box_label(f, 620, 85, "B", "(C₁₀H₁₈O₂)")
    _box_label(f, 60, 230, "C")
    _scheme_arrow(f, 85, 330, 230, "1) n-BuLi  2) Br(CH₂)₄COOH", "3) H₃O⁺")
    _box_label(f, 360, 230, "D", "(C₁₀H₁₆O₂)")
    _scheme_arrow(f, 395, 590, 230, "(가)")
    _box_label(f, 620, 230, "B")
    f.text(700, 230, "C: 삼중 결합 포함", size=11, anchor="start", color="#5b6270")
    return f.render()


# ------------------------------------------------------------- NMR 막대 스펙트럼 도우미
def _nmr(f, x0, x1, y0, ppm_hi, ppm_lo, peaks, ticks, title):
    """peaks: [(δ, 높이(0-1), 라벨, 다중선 수)]"""
    X = lambda d: x0 + (ppm_hi - d) / (ppm_hi - ppm_lo) * (x1 - x0)
    f.raw(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="{INK}" stroke-width="1.2"/>')
    for t in ticks:
        x = X(t)
        f.raw(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0 + 5}" stroke="{INK}"/>')
        f.text(x, y0 + 15, f"{t:g}", size=11)
    f.text(x1, y0 + 32, "δ (ppm)", size=11, anchor="end")
    f.text(x0, 22, title, size=12, anchor="start", weight="bold")
    H = y0 - 50
    for d, hgt, lab, n in peaks:
        x = X(d)
        if n == 1:
            f.raw(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0 - H * hgt:.1f}" stroke="{BLUE}" stroke-width="2"/>')
        else:
            for k in range(n):
                xx = x + (k - (n - 1) / 2) * 3.2
                hh = H * hgt * (0.8 if k in (0, n - 1) else 1)
                f.raw(f'<line x1="{xx:.1f}" y1="{y0}" x2="{xx:.1f}" y2="{y0 - hh:.1f}" stroke="{BLUE}" stroke-width="1.2"/>')
        f.text(x, y0 - H * hgt - 12, lab, size=13, weight="bold")


def f25b1():
    f = Fig(800, 250)
    _nmr(f, 50, 760, 200, 8.0, 2.0,
         [(7.3, 1.0, "㉠", 6), (3.86, 0.25, "㉡", 4), (3.14, 0.25, "㉢", 4), (2.80, 0.25, "㉣", 4)],
         [8, 7, 6, 5, 4, 3, 2], "¹H NMR (300 MHz, CDCl₃) — C₈H₈O")
    f.text(600, 60, "적분비 ㉠ : ㉡ : ㉢ : ㉣ = 5 : 1 : 1 : 1", size=12)
    f.text(600, 80, "㉡~㉣은 확대하면 각각 4개의 선", size=12)
    return f.render()


# ------------------------------------------------------------- 2025 B 기입형 2
def f25b2():
    f = Fig(800, 300)
    x0, y0 = 70, 250
    f.raw(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="30" stroke="{INK}" stroke-width="1.3" marker-end="url(#{f.id}k)"/>')
    f.raw(f'<line x1="{x0}" y1="{y0}" x2="760" y2="{y0}" stroke="{INK}" stroke-width="1.3" marker-end="url(#{f.id}k)"/>')
    f.text(45, 140, "에너지", size=12)
    f.text(700, 272, "형태 변화", size=12)
    # 점: A(0) B(최고) C(국소 최소) D(작은 극대) C B A
    pts = [(100, 235, "A"), (205, 60, "B"), (310, 150, "C"), (410, 128, "D"), (510, 150, "C"), (615, 60, "B"), (720, 235, "A")]
    d = f"M{pts[0][0]},{pts[0][1]}"
    for (xa, ya, _), (xb, yb, _) in zip(pts, pts[1:]):
        cx = (xa + xb) / 2
        d += f" C{cx},{ya} {cx},{yb} {xb},{yb}"
    f.raw(f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="2.2"/>')
    for x, y, lab in pts:
        f.raw(f'<circle cx="{x}" cy="{y}" r="3.5" fill="{INK}"/>')
        f.text(x, y - 16 if lab in "BD" else y + 18 if lab == "A" else y + 18, lab, size=14, weight="bold")
    f.text(410, 285, "사이클로헥세인의 형태 A~D의 상대 에너지", size=11.5, color="#5b6270")
    return f.render()


# ------------------------------------------------------------- 2025 B 서술형 7
def ring7(m, p, cx, cy, doubles=(), ketone=True):
    m.ring(p, cx, cy, 7, 30, 90, bonds=False)
    for i in range(7):
        a, b = f"{p}{i}", f"{p}{(i + 1) % 7}"
        m.bond(a, b, "in" if i in doubles else 1, (cx, cy) if i in doubles else None)
    if ketone:
        m.sub(p + "o", f"{p}0", 90, "O", kind="2")


def f25b7():
    f = Fig(800, 330)
    for i, (lab, dbl) in enumerate((("A", (1, 3, 5)), ("B", (1,)), ("C", ()))):
        m = Mol()
        ring7(m, "r", 0, 0, dbl)
        x = 110 + i * 150
        f.mol(m, x, 100)
        f.text(x, 160, lab, size=15, weight="bold")
    f.text(560, 60, "A: cyclohepta-2,4,6-trien-1-one (tropone)", size=11.5, anchor="start")
    f.text(560, 82, "B: cyclohept-2-en-1-one", size=11.5, anchor="start")
    f.text(560, 104, "C: cycloheptanone", size=11.5, anchor="start")
    f.text(60, 220, "A  +  CH₂=CH₂", size=14, anchor="start")
    f.arrow(215, 220, 300, 220, "가열")
    f.text(320, 220, "D", size=15, anchor="start", weight="bold")
    f.text(340, 220, "(C₉H₁₀O)", size=11.5, anchor="start")
    f.text(60, 285, "B  +  1,3-butadiene", size=14, anchor="start")
    f.arrow(215, 285, 300, 285, "가열")
    f.text(320, 285, "E", size=15, anchor="start", weight="bold")
    f.text(340, 285, "(C₁₁H₁₆O)", size=11.5, anchor="start")
    return f.render()


# ------------------------------------------------------------- 2026 A 기입형 1
def f26a1():
    f = Fig(800, 200)
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    c = m.sub("c", "r1", 30)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("h", c, -30, "H")
    f.mol(m, 50, 110)
    f.text(160, 110, "+", size=18)
    f.text(240, 110, "Ph₃P⁺–C⁻H–Ph", size=13)
    f.arrow(305, 110, 380, 110, "", "")
    f.text(405, 110, "A", size=17, weight="bold")
    f.arrow(430, 110, 525, 110, "m-CPBA", "")
    # cis-2,3-diphenyloxirane
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.atom("b", 34, 0)
    o = m.atom("o", 17, -26, "O")
    m.bond("a", "b")
    m.bond("a", "o")
    m.bond("b", "o")
    m.sub("pa", a, 220, "Ph", anchor="end", kind="w")
    m.sub("pb", b, -40, "Ph", anchor="start", kind="w")
    m.sub("ha", a, 300, "H", length=20, kind="h")
    m.sub("hb", b, 240, "H", length=20, kind="h")
    f.mol(m, 610, 105)
    f.text(627, 175, "cis-2,3-diphenyloxirane", size=12)
    return f.render()


# ------------------------------------------------------------- 2026 A 서술형 10
def f26a10():
    f = Fig(800, 200)
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    m.sub("me", "r0", 90, "CH_3")
    m.sub("br", "r3", -90, "Br")
    f.mol(m, 60, 95)
    f.text(60, 185, "p-bromotoluene", size=12)
    f.arrow(110, 95, 230, 95, "KNH₂", "NH₃(l)")
    f.text(255, 95, "A", size=17, weight="bold")
    f.text(255, 117, "(C₇H₉N)", size=11.5)
    f.arrow(285, 95, 430, 95, "NaNO₂, HCl", "0 ℃")
    f.text(455, 95, "B", size=17, weight="bold")
    f.arrow(480, 95, 590, 95, "CuCN", "")
    f.text(615, 95, "C", size=17, weight="bold")
    return f.render()


# ------------------------------------------------------------- 2026 A 서술형 11
def f26a11():
    f = Fig(800, 330)
    # A
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.sub("o", "r0", 90, "O", kind="2")
    m.sub("e", "r1", 30, "CO_2Et", anchor="start")
    m.sub("m1", "r4", 180)
    m.sub("m2", "r4", 240)
    f.mol(m, 70, 95)
    f.text(70, 170, "A", size=15, weight="bold")
    f.text(165, 95, "+", size=18)
    # MVK
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, -30, kind="2l")
    c = m.sub("c", b, 30)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("me", c, -30)
    f.mol(m, 190, 105)
    f.text(240, 170, "methyl vinyl ketone", size=11.5)
    f.arrow(300, 95, 410, 95, "NaOEt, EtOH", "가열")
    f.text(435, 95, "B", size=17, weight="bold")
    f.text(435, 117, "(C₁₅H₂₂O₃)", size=11.5)
    f.arrow(470, 95, 630, 95, "1) HSCH₂CH₂SH, BF₃", "2) Raney Ni")
    # octalin ester
    m = Mol()
    m.ring("L", 0, 0, 6, L, 90)
    cx = 2 * L * math.cos(math.radians(30))
    m.ring("R", cx, 0, 6, L, 90, bonds=False)
    m.bond("L1", "R0")
    m.bond("R0", "R1")
    m.bond("R1", "R2")
    m.bond("R2", "R3")
    m.bond("R3", "L2", "in", (cx, 0))
    m.sub("e", "L1", 90, "CO_2Et")
    m.sub("m1", "L4", 180)
    m.sub("m2", "L4", 240)
    f.mol(m, 690, 105)
    f.arrow(690, 175, 690, 225, None, None)
    f.text(702, 190, "1) LiAlH₄ (과량)", size=11, anchor="start")
    f.text(702, 206, "2) BH₃·THF", size=11, anchor="start")
    f.text(702, 222, "3) H₂O₂, NaOH", size=11, anchor="start")
    f.text(690, 250, "C", size=17, weight="bold")
    f.arrow(665, 250, 470, 250, "CrO₃, H₃O⁺", "acetone")
    f.text(445, 250, "D", size=17, weight="bold")
    f.text(445, 272, "(C₁₃H₂₀O₃)", size=11.5)
    return f.render()


# ------------------------------------------------------------- 2026 B 기입형 1
def f26b1():
    f = Fig(800, 260)
    _nmr(f, 50, 600, 210, 10.5, 3.0,
         [(9.9, 0.25, "㉠", 1), (7.0, 0.45, "㉡", 1), (6.7, 0.25, "㉢", 1), (3.8, 1.0, "㉣", 1)],
         [10, 9, 8, 7, 6, 5, 4, 3], "¹H NMR (90 MHz, CDCl₃) — C₉H₁₀O₃")
    f.box(620, 40, 170, 150, fill="#f7f9fc")
    f.text(705, 58, "IR (cm⁻¹)", size=12, weight="bold")
    for i, t in enumerate(["≈ 2830, 2730 (약)", "≈ 1700 (강)", "≈ 1600"]):
        f.text(635, 84 + i * 22, t, size=12, anchor="start")
    f.text(635, 160, "적분비 1 : 2 : 1 : 6", size=11.5, anchor="start")
    f.text(635, 178, "(모두 단일선)", size=11.5, anchor="start")
    return f.render()


# ------------------------------------------------------------- 2026 B 서술형 7
def f26b7():
    f = Fig(800, 190)
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    c = m.sub("c", "r1", 30)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("me", c, -30)
    f.mol(m, 50, 110)
    f.text(90, 175, "acetophenone", size=12)
    f.arrow(150, 100, 290, 100, "1) HC≡CMgBr", "2) H₃O⁺")
    f.text(315, 100, "A", size=17, weight="bold")
    f.text(315, 122, "(C₁₀H₁₀O)", size=11.5)
    f.arrow(350, 100, 500, 100, "HgSO₄, H₂SO₄", "H₂O")
    f.text(525, 100, "B", size=17, weight="bold")
    f.arrow(550, 100, 690, 100, "(CO₂Et)₂", "NaH")
    f.text(715, 100, "C", size=17, weight="bold")
    f.text(715, 122, "(C₁₂H₁₀O₄)", size=11.5)
    return f.render()


ITEMS = [
    {"unit": 3, "year": 2025, "exam": "전공B 기입형 2번", "pts": 2, "fig": f25b2,
     "stem": "그림은 사이클로헥세인의 여러 형태 A~D(의자형, 반쪽 의자형, 보트형, 꼬인 보트형 중 하나)의 상대 에너지를 형태 변화에 따라 나타낸 것이다. "
             "A는 가장 안정한 형태이고, B는 가장 불안정한 형태이며, C는 국소 최소, D는 두 C 사이의 작은 극대에 해당한다.",
     "ask": "A와 D의 형태를 수소 원자를 생략하고 탄소 골격만으로 각각 그리시오. 또한 A의 점군을 쓰시오."},
    {"unit": 11, "year": 2025, "exam": "전공B 서술형 7번", "pts": 4, "fig": f25b7,
     "stem": "다음은 칠원자 고리 케톤 A~C와, A·B의 고리 첨가 반응을 나타낸 것이다. (단, 각 단계에서 적절한 분리·정제 과정을 수행하였다.)",
     "ask": "A가 방향족성을 갖는 이유를 A의 공명 구조를 그려 설명하시오. A~C를 IR 스펙트럼에서 C=O 신축 진동의 파수가 큰 것부터 순서대로 쓰시오. "
            "또한 가능한 주생성물 D의 구조와 E의 입체 구조를 각각 그리시오."},
    {"unit": 12, "year": 2026, "exam": "전공A 서술형 10번", "pts": 4, "fig": f26a10,
     "stem": "다음은 p-bromotoluene으로부터 A, B를 거쳐 C를 합성하는 반응이다. A의 ¹H NMR 스펙트럼에서 방향족 수소의 피크는 2가지 화학적 이동을 보인다. "
             "(단, 각 단계에서 적절한 분리·정제 과정을 수행하였다.)",
     "ask": "p-bromotoluene → A 반응에서 생성되는 중간체(C₇H₆)의 구조를 그리시오. 또한 A, B, C의 구조를 각각 그리시오."},
    {"unit": 12, "year": 2025, "exam": "전공A 서술형 10번", "pts": 4, "fig": f25a10,
     "stem": "다음은 톨루엔으로부터 A~C를 거쳐 D를 합성하는 반응이다. A의 ¹H NMR 스펙트럼에서 방향족 수소의 피크는 2가지 화학적 이동을 보인다. "
             "(단, 각 단계에서 적절한 분리·정제 과정을 수행하였다.)",
     "ask": "A, B, D의 구조를 각각 그리시오. 또한 C → D 반응 과정에서 생성되는 중간체(C₇H₄NOCl)의 구조를 그리시오."},
    {"unit": 13, "year": 2026, "exam": "전공A 기입형 1번", "pts": 2, "fig": f26a1,
     "stem": "다음은 benzaldehyde와 인 일라이드의 반응으로 A를 얻고, A를 m-CPBA로 에폭시화하여 cis-2,3-diphenyloxirane을 얻는 반응이다.",
     "ask": "A가 생성되는 과정에서 거치는 oxaphosphetane 중간체의 구조를 그리시오. 또한 A의 입체 구조를 그리시오."},
    {"unit": 15, "year": 2025, "exam": "전공A 서술형 11번", "pts": 4, "fig": f25a11,
     "stem": "다음은 서로 다른 두 경로로 같은 화합물 B를 합성하는 반응이다. C는 삼중 결합을 가진 화합물이다. "
             "(단, 각 단계에서 적절한 분리·정제 과정을 수행하였다.)",
     "ask": "A, B, C의 구조를 각각 그리시오. 또한 D → B의 반응 조건 (가)를 쓰시오. (B의 C=C는 E 배치를 갖는다.)"},
    {"unit": 16, "year": 2026, "exam": "전공A 서술형 11번", "pts": 4, "fig": f26a11,
     "stem": "다음은 β-케토 에스터 A와 methyl vinyl ketone으로부터 B를 만들고, 이를 거쳐 C와 D를 합성하는 반응이다. "
             "(단, 각 단계에서 적절한 분리·정제 과정을 수행하였다.)",
     "ask": "B, C, D의 구조를 각각 그리시오. 또한 A → B 반응에서 고리가 형성되는 단계의 메커니즘을 굽은 화살표를 사용하여 제시하시오."},
    {"unit": 16, "year": 2026, "exam": "전공B 서술형 7번", "pts": 4, "fig": f26b7,
     "stem": "다음은 acetophenone으로부터 A, B를 거쳐 고리 화합물 C를 합성하는 반응이다. (단, 각 단계에서 적절한 분리·정제 과정을 수행하였다.)",
     "ask": "A, B, C의 구조를 각각 그리시오. 또한 C로부터 생성될 수 있는 토토머(tautomer) 2가지의 구조를 그리시오."},
    {"unit": 21, "year": 2026, "exam": "전공B 기입형 1번", "pts": 2, "fig": f26b1,
     "stem": "다음은 분자식이 C₉H₁₀O₃인 화합물 A의 IR 자료와 ¹H NMR 스펙트럼을 나타낸 것이다. (단, ⁴J 짝지음은 무시한다.)",
     "ask": "A의 구조를 그리고, ㉠에 해당하는 수소에 ○ 표시를 하시오."},
    {"unit": 21, "year": 2025, "exam": "전공B 기입형 1번", "pts": 2, "fig": f25b1,
     "stem": "다음은 분자식이 C₈H₈O인 화합물의 ¹H NMR 스펙트럼(300 MHz, CDCl₃)을 나타낸 것이다. 피크 ㉠~㉣의 화학적 이동은 각각 약 7.3, 3.86, 3.14, 2.80 ppm이다.",
     "ask": "이 화합물의 구조를 그리고, ㉡에 해당하는 수소에 ○ 표시를 하시오."},
]

if __name__ == "__main__":
    import sys
    from preview import shot
    shot([it["fig"]() for it in ITEMS], sys.argv[1])
