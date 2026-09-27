"""21 유기 분광 — 새로 작성한 문항(2002–2013) 그림.

색 약속: ¹H NMR 귀속 = RED, ¹³C NMR 귀속 = GREEN, IR 띠 = BLUE, MS = PURPLE
"""
import math
from chemsvg import Mol, Fig, benzene, L, RED, BLUE, INK

GREEN = "#2f7d5b"
PURPLE = "#7c3aed"
GRAY = "#5b6270"


# ------------------------------------------------------------------ 공용 헬퍼
def A(m, name, ox, oy):
    """분자 좌표 → 그림 절대 좌표"""
    x, y = m.pos(name)
    return ox + x, oy + y


def lead(f, x1, y1, x2, y2, color=RED):
    f.raw(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" '
          f'stroke-width="0.9" stroke-dasharray="2 2"/>')


def tag(f, m, name, ox, oy, dx, dy, text, color=RED, anchor="middle", size=11.5):
    """원자 name에서 (dx, dy)만큼 떨어진 곳에 귀속 라벨 + 점선 지시선"""
    x, y = A(m, name, ox, oy)
    tx, ty = x + dx, y + dy
    d = math.hypot(dx, dy) or 1
    lead(f, x + dx * 9 / d, y + dy * 9 / d, tx - dx * 8 / d, ty - dy * 8 / d, color)
    f.text(tx, ty, text, size=size, anchor=anchor, color=color)


def circ(f, x, y, r=13, color=RED):
    f.raw(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="none" stroke="{color}" stroke-width="1.8"/>')


def legend(f, x, y, items=(("¹H NMR", RED), ("¹³C NMR", GREEN), ("IR", BLUE))):
    for i, (t, c) in enumerate(items):
        xx = x + i * 88
        f.raw(f'<rect x="{xx}" y="{y - 5}" width="10" height="10" fill="{c}"/>')
        f.text(xx + 15, y, t, size=11, anchor="start", color=c)


def bars(f, x0, y0, w, h, lo, hi, peaks, color=PURPLE, ticks=()):
    """막대 질량 스펙트럼. peaks: [(m/z, 상대세기 0–100, 라벨)]"""
    f.raw(f'<line x1="{x0}" y1="{y0}" x2="{x0 + w}" y2="{y0}" stroke="{INK}" stroke-width="1.2"/>')
    sx = lambda v: x0 + (v - lo) / (hi - lo) * w
    for mz, rel, lab in peaks:
        x = sx(mz)
        f.raw(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0 - rel / 100 * h:.1f}" stroke="{color}" stroke-width="3"/>')
        if lab:
            f.text(x, y0 - rel / 100 * h - 10, lab, size=11, color=color)
    for t in ticks:
        f.text(sx(t), y0 + 13, str(t), size=10.5, color=GRAY)


def fused_iq(m, p, cx, cy, aromatic=True):
    """(3,4-다이하이드로)아이소퀴놀린 골격. 반환: 번호 → 원자 이름 dict"""
    benzene(m, p + "L", cx, cy, 90)              # 왼쪽 벤젠 고리 (C8, C8a, C4a, C5, C6, C7)
    rx = cx + 2 * L * math.cos(math.radians(30))
    m.ring(p + "R", rx, cy, 6, L, 90, bonds=False)
    n = {"1": p + "R0", "2": p + "R1", "3": p + "R2", "4": p + "R3", "4a": p + "L2", "8a": p + "L1",
         "5": p + "L3", "6": p + "L4", "7": p + "L5", "8": p + "L0"}
    c = (rx, cy)
    m.label(n["2"], "N")
    m.bond(n["8a"], n["1"])
    m.bond(n["1"], n["2"], "in", c)
    m.bond(n["2"], n["3"])
    m.bond(n["3"], n["4"], "in" if aromatic else 1, c if aromatic else None)
    m.bond(n["4"], n["4a"])
    return n


# ------------------------------------------------------------------ 2013 #40 ethyl cyanoacetate
def f2013_40():
    f = Fig(800, 250)
    f.text(20, 20, "정답 ②  ethyl cyanoacetate  NC–CH₂–CO₂CH₂CH₃  (C₅H₇NO₂, M = 113)", size=13, anchor="start", weight="bold")
    legend(f, 560, 20, (("¹H NMR", RED), ("IR", BLUE), ("MS", PURPLE)))
    m = Mol()
    m.atom("n", 0, 0, "N")
    m.sub("c1", "n", 0, kind=3)
    m.sub("c2", "c1", 0)
    m.sub("c3", "c2", -30)
    m.sub("o2", "c3", -90, "O", kind="2")
    m.sub("o1", "c3", 30, "O")
    m.sub("c4", "o1", -30)
    m.sub("c5", "c4", 30)
    ox, oy = 90, 110
    f.mol(m, ox, oy)
    tag(f, m, "c2", ox, oy, -5, -42, "δ 3.45 (s, 2H)")
    tag(f, m, "c4", ox, oy, 25, 45, "δ 4.25 (q, 2H)")
    tag(f, m, "c5", ox, oy, 40, -35, "δ 1.30 (t, 3H)")
    tag(f, m, "c1", ox, oy, -10, 45, "2260 C≡N (약)", color=BLUE)
    tag(f, m, "o2", ox, oy, 0, 38, "1745 C=O (에스터)", color=BLUE)
    # MS
    f.box(360, 55, 425, 175)
    f.text(372, 75, "질량 스펙트럼: α-절단(아실 C–O 결합 끊어짐)", size=12, anchor="start", color=PURPLE, weight="bold")
    f.text(470, 112, "[NC–CH_2–CO–OCH_2CH_3]^{+•}", size=12.5)
    f.text(470, 132, "m/z 113 (M^{+•})", size=12, color=PURPLE)
    f.arrow(588, 112, 648, 112, "− •OC_2H_5", "(45)", color=PURPLE)
    f.text(715, 112, "NC–CH_2–C≡O^+", size=12.5)
    f.text(715, 132, "m/z 68 (아실륨)", size=12, color=PURPLE)
    f.text(372, 170, "113 − 45 = 68 : 에톡시 라디칼이 떨어진 아실륨 이온", size=11.5, anchor="start")
    f.text(372, 192, "공명 안정화: NC–CH_2–C^+=O ↔ NC–CH_2–C≡O^+", size=11.5, anchor="start")
    f.text(372, 214, "(①의 C₂H₅CO⁺ = 57, ④의 CH₃CO⁺ = 43이 주로 나와야 함)", size=11, anchor="start", color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 2012 #40 N-methylacetamide
def f2012_40():
    f = Fig(800, 230)
    f.text(20, 20, "정답 ④  N-methylacetamide  CH₃CONHCH₃ (C₃H₇NO, 2차 아마이드)", size=13, anchor="start", weight="bold")
    legend(f, 600, 20, (("¹H NMR", RED), ("IR", BLUE)))
    m = Mol()
    m.atom("a", 0, 0, "H_3C", "end")
    m.sub("c", "a", 30)
    m.sub("o", "c", 90, "O", kind="2")
    m.sub("n", "c", -30, "N")
    m.sub("h", "n", 30, "H")
    m.sub("nm", "n", -90, "CH_3")
    ox, oy = 130, 125
    f.mol(m, ox, oy)
    tag(f, m, "a", ox, oy, -40, 45, "δ 2.0 (s, 3H)")
    tag(f, m, "nm", ox, oy, 0, 42, "δ 2.8 (d, J ≈ 5 Hz, 3H)")
    tag(f, m, "h", ox, oy, 60, -20, "δ ≈ 7.3 (넓은 봉우리, 1H)", anchor="start")
    tag(f, m, "o", ox, oy, 45, -12, "1654 C=O (amide I)", color=BLUE, anchor="start")
    tag(f, m, "h", ox, oy, 60, 20, "3300 N–H 신축", color=BLUE, anchor="start")
    # 공명
    f.box(420, 45, 365, 170)
    f.text(432, 64, "아마이드 공명 → C=O 결합 차수 ↓ (1654 cm⁻¹)", size=12, anchor="start", weight="bold")
    for k, (ox2, charge) in enumerate([(470, False), (680, True)]):
        m = Mol()
        m.atom("a", 0, 0, "H_3C", "end")
        m.sub("c", "a", 30)
        m.sub("o", "c", 90, "O^−" if charge else "O", kind=1 if charge else "2")
        m.sub("n", "c", -30, "N^+" if charge else "N", kind="2" if charge else 1)
        m.sub("h", "n", 30, "H")
        m.sub("nm", "n", -90, "CH_3")
        f.mol(m, ox2, 135)
    f.resarrow(580, 635, 125)
    f.text(432, 200, "C–N 부분 이중 결합: 회전 제한, N 비공유쌍 비편재화", size=11, anchor="start", color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 2011 #40 ethyl salicylate
def f2011_40():
    f = Fig(800, 290)
    f.text(20, 20, "정답 ④  ethyl salicylate (ethyl 2-hydroxybenzoate, C₉H₁₀O₃)", size=13, anchor="start", weight="bold")
    legend(f, 560, 20)
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    m.sub("c", "r1", 30)
    m.sub("o", "c", 90, "O", kind="2")
    m.sub("oh", "r0", 90, "O")
    m.sub("h", "oh", 30, "H")
    m.bond("h", "o", "dash")
    m.sub("oe", "c", -30, "O")
    m.sub("e1", "oe", 30)
    m.sub("e2", "e1", -30)
    ox, oy = 170, 175
    f.mol(m, ox, oy)
    tag(f, m, "h", ox, oy, -55, -40, "δ 10.8 (s, 1H, OH…O=C)", anchor="end")
    tag(f, m, "r2", ox, oy, 30, 50, "H6 δ 7.85 (dd, 1H)", anchor="start")
    tag(f, m, "r4", ox, oy, -35, 30, "H4 δ 7.45 (td, 1H)", anchor="end")
    tag(f, m, "r5", ox, oy, -40, -18, "H3 δ 6.97 (d, 1H)", anchor="end")
    tag(f, m, "r3", ox, oy, 0, 60, "H5 δ 6.87 (t, 1H)")
    tag(f, m, "e1", ox, oy, 45, -35, "δ 4.40 (q, 2H)", anchor="start")
    tag(f, m, "e2", ox, oy, 35, 40, "δ 1.41 (t, 3H)")
    f.text(225, 78, "분자 내 수소 결합", size=10.5, color=GRAY)
    # 13C 표
    f.box(455, 45, 330, 235)
    f.text(467, 64, "¹³C NMR 귀속 (9개 신호 = 9 C, 대칭 없음)", size=12, anchor="start", color=GREEN, weight="bold")
    rows = [("170", "C=O (에스터)"), ("162", "C2 (C–OH)"), ("136", "C4"), ("130", "C6"),
            ("119", "C5"), ("118", "C3"), ("112", "C1 (C–CO₂Et)"), ("61", "OCH₂"), ("14", "CH₃")]
    for i, (d, t) in enumerate(rows):
        f.text(485, 88 + i * 21, f"δ {d}", size=11.5, anchor="start", color=GREEN)
        f.text(555, 88 + i * 21, t, size=11.5, anchor="start")
    return f.render()


# ------------------------------------------------------------------ 2010 #40 cinnamaldehyde
def f2010_40():
    f = Fig(800, 250)
    f.text(20, 20, "정답 ③  (E)-cinnamaldehyde  Ph–CH=CH–CHO (C₉H₈O)", size=13, anchor="start", weight="bold")
    legend(f, 600, 20, (("¹H NMR", RED), ("IR", BLUE)))
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    m.sub("cb", "r1", 30)
    m.sub("ca", "cb", -30, kind="2")
    m.sub("cho", "ca", 30)
    m.sub("o", "cho", -30, "O", kind="2")
    m.sub("hc", "cho", 90, "H")
    m.sub("hb", "cb", 90, "H")
    m.sub("ha", "ca", -90, "H")
    ox, oy = 110, 140
    f.mol(m, ox, oy)
    tag(f, m, "hc", ox, oy, 40, -25, "δ 9.70 (d, J = 7.7 Hz, 1H)", anchor="start")
    tag(f, m, "hb", ox, oy, -10, -40, "Hβ δ 7.48 (d, J = 16 Hz)", anchor="middle")
    tag(f, m, "ha", ox, oy, 20, 38, "Hα δ 6.72 (dd, J = 16, 7.7 Hz)", anchor="start")
    tag(f, m, "r4", ox, oy, -10, 50, "ArH δ 7.4–7.6 (m, 5H)")
    tag(f, m, "o", ox, oy, 45, 15, "1680 C=O (공액), 2820·2740 CHO C–H", color=BLUE, anchor="start")
    # 짝지음 나무
    x = 590
    f.text(x, 55, "Hα(6.72)의 짝지음 나무", size=12, weight="bold")
    f.raw(f'<line x1="{x}" y1="70" x2="{x}" y2="90" stroke="{INK}" stroke-width="1.4"/>')
    for s in (-1, 1):
        xa = x + s * 40
        f.raw(f'<line x1="{x}" y1="90" x2="{xa}" y2="115" stroke="{RED}" stroke-width="1.2"/>')
        f.raw(f'<line x1="{xa}" y1="115" x2="{xa}" y2="130" stroke="{INK}" stroke-width="1.4"/>')
        for t in (-1, 1):
            xb = xa + t * 19
            f.raw(f'<line x1="{xa}" y1="130" x2="{xb}" y2="155" stroke="{BLUE}" stroke-width="1.2"/>')
            f.raw(f'<line x1="{xb}" y1="155" x2="{xb}" y2="185" stroke="{INK}" stroke-width="2"/>')
    f.text(x + 70, 102, "³J(Hα–Hβ) = 16 Hz", size=11, anchor="start", color=RED)
    f.text(x + 70, 142, "³J(Hα–CHO) = 7.7 Hz", size=11, anchor="start", color=BLUE)
    f.text(x, 205, "→ 4개의 선(dd): trans(E) C=C 확인", size=11.5)
    return f.render()


# ------------------------------------------------------------------ 2009 #27 2-pentyn-1-ol
def f2009_27():
    f = Fig(800, 250)
    f.text(20, 20, "C₅H₈O = 2-pentyn-1-ol  HO–CH₂–C≡C–CH₂–CH₃  (카이랄 탄소 없음)", size=13, anchor="start", weight="bold")
    legend(f, 560, 20)
    m = Mol()
    m.atom("oh", 0, 0, "HO", "end")
    m.sub("c1", "oh", -30)
    m.sub("c2", "c1", 0)
    m.sub("c3", "c2", 0, kind=3)
    m.sub("c4", "c3", 0)
    m.sub("c5", "c4", 30)
    ox, oy = 150, 130
    f.mol(m, ox, oy)
    x1, y1 = A(m, "c1", ox, oy)
    x4, y4 = A(m, "c4", ox, oy)
    f.raw(f'<path d="M{x1:.1f},{y1 - 8:.1f} Q{(x1 + x4) / 2:.1f},{y1 - 70:.1f} {x4:.1f},{y4 - 8:.1f}" fill="none" '
          f'stroke="{RED}" stroke-width="1.5" stroke-dasharray="5 3" marker-start="url(#{f.id}r)" marker-end="url(#{f.id}r)"/>')
    f.text((x1 + x4) / 2, y1 - 52, "⁵J ≈ 2 Hz (H–C1–C2≡C3–C4–H)", size=11.5, color=RED, weight="bold")
    tag(f, m, "c1", ox, oy, -20, 50, "δ 4.25 (t, ⁵J, 2H)")
    tag(f, m, "c4", ox, oy, 5, 50, "δ 2.23 (qt, 2H)")
    tag(f, m, "c5", ox, oy, 55, -15, "δ 1.13 (t, 3H)", anchor="start")
    tag(f, m, "oh", ox, oy, -30, -35, "δ ≈ 1.6 (s, 1H, OH)", anchor="end")
    f.text(30, 215, "IR: 3332 O–H(넓음) · 2229 C≡C(약, 내부 알카인) · 1014 C–O   /  ≡C–H(3300 날카로움) 없음 → 내부 알카인",
           size=11.5, anchor="start", color=BLUE)
    f.box(450, 55, 335, 135)
    f.text(462, 75, "Hz 눈금 읽기 (300 MHz)", size=12, anchor="start", weight="bold")
    f.text(462, 98, "1275 Hz ÷ 300 = 4.25 ppm: 선 간격 ≈ 2 Hz → t", size=11.5, anchor="start")
    f.text(462, 120, "669 Hz ÷ 300 = 2.23 ppm: q(7.5 Hz) × t(2 Hz)", size=11.5, anchor="start")
    f.text(462, 145, "C1H₂와 C4H₂ 사이 결합: H–C, C–C, C≡C, C–C, C–H", size=11.5, anchor="start")
    f.text(462, 167, "= 5개 → 긴 거리 ⁵J (알카인 π를 통한 전달)", size=11.5, anchor="start", color=RED)
    return f.render()


# ------------------------------------------------------------------ 2008 #13 3-butyn-1-ol
def butynol(m, olabel="OH"):
    m.atom("h", 0, 0, "H", "end")
    m.sub("c1", "h", 0)
    m.sub("c2", "c1", 0, kind=3)
    m.sub("c3", "c2", 0)
    m.sub("c4", "c3", -30)
    m.sub("o", "c4", 30, olabel)


def f2008_13():
    f = Fig(800, 260)
    f.text(20, 20, "A = 3-butyn-1-ol (C₄H₆O)  →  B = 4-methoxy-1-butyne (C₅H₈O)", size=13, anchor="start", weight="bold")
    legend(f, 600, 20, (("¹H NMR", RED), ("IR", BLUE)))
    m = Mol()
    butynol(m)
    ox, oy = 60, 120
    f.mol(m, ox, oy)
    x, y = A(m, "c3", ox, oy)
    circ(f, x, y, 12)
    tag(f, m, "c3", ox, oy, -5, -48, "δ 2.33 (td, 2H)")
    tag(f, m, "h", ox, oy, -10, 45, "δ 1.97 (t, J = 2.7 Hz, 1H)", anchor="start")
    tag(f, m, "c4", ox, oy, 60, 40, "δ 3.59 (t, 2H)", anchor="start")
    tag(f, m, "o", ox, oy, 20, -40, "δ 2.67 (s, 1H)")
    f.text(40, 215, "IR: 3294 (O–H + ≡C–H), 2117 C≡C, 1049 C–O", size=11.5, anchor="start", color=BLUE)
    f.text(40, 237, "pKₐ: R–OH ≈ 16 < RC≡C–H ≈ 25", size=11.5, anchor="start", color=GRAY)
    f.arrow(340, 110, 480, 110, "1) NaH (1.0 당량)", "2) CH_3I (S_N2)")
    f.text(410, 160, "NaH 1당량은 더 강한 산인 O–H만 탈양성자화", size=11, color=GRAY)
    f.text(410, 178, "→ RO⁻Na⁺ → CH₃I와 Williamson 에터 합성", size=11, color=GRAY)
    m = Mol()
    butynol(m, "OCH_3")
    f.mol(m, 520, 120)
    f.cap(600, 160, "B (C₅H₈O)", color=GREEN)
    return f.render()


# ------------------------------------------------------------------ 2007 #12 isoquinoline 합성
def phen_chain(m, p, cx, cy):
    benzene(m, p, cx, cy, 90)
    return p + "1"


def f2007_12_scheme():
    f = Fig(800, 360)
    f.text(20, 20, "Henry 반응 → 환원 → 아세틸화 → Bischler–Napieralski 고리화 → 탈수소화", size=13, anchor="start", weight="bold")
    # 1행
    m = Mol()
    a = phen_chain(m, "r", 0, 0)
    m.sub("c", a, 30)
    m.sub("o", "c", 90, "O", kind="2")
    m.sub("h", "c", -30, "H")
    f.mol(m, 55, 100)
    f.text(160, 100, "+ CH_3NO_2", size=13)
    f.arrow(205, 100, 285, 100, "OH^−, Δ", "(−H₂O)")
    m = Mol()
    a = phen_chain(m, "r", 0, 0)
    m.sub("cb", a, 30)
    m.sub("ca", "cb", -30, kind="2")
    m.sub("n", "ca", 30, "NO_2", anchor="start")
    f.mol(m, 335, 100)
    f.cap(385, 150, "(E)-β-nitrostyrene")
    f.text(385, 168, "C₈H₇NO₂", size=11, color=GRAY)
    f.arrow(470, 100, 550, 100, "H_2, Pt/C", "C=C, NO₂ 환원")
    m = Mol()
    a = phen_chain(m, "r", 0, 0)
    m.sub("c1", a, 30)
    m.sub("c2", "c1", -30)
    m.sub("n", "c2", 30, "NH_2", anchor="start")
    f.mol(m, 605, 100)
    f.cap(660, 150, "A: 2-phenylethylamine", color=RED)
    f.text(660, 168, "C₈H₁₁N", size=11, color=GRAY)
    # 2행
    f.arrow(40, 265, 115, 265, "CH_3COCl", "pyridine")
    f.text(25, 265, "A", size=14, weight="bold", color=RED)
    m = Mol()
    a = phen_chain(m, "r", 0, 0)
    m.sub("c1", a, 30)
    m.sub("c2", "c1", -30)
    m.sub("n", "c2", 30, "NH")
    m.sub("co", "n", -30)
    m.sub("o", "co", -90, "O", kind="2")
    m.sub("me", "co", 30)
    f.mol(m, 160, 260)
    f.text(230, 325, "N-(2-phenylethyl)acetamide  C₁₀H₁₃NO", size=11, color=GRAY)
    f.arrow(345, 265, 435, 265, "P_2O_5, 205 ℃", "고리화(−H₂O)")
    m = Mol()
    n = fused_iq(m, "q", 0, 0, aromatic=False)
    m.sub("me", n["1"], 90)
    f.mol(m, 470, 270)
    f.cap(495, 320, "B: 1-methyl-3,4-dihydroisoquinoline", color=RED)
    f.text(495, 338, "C₁₀H₁₁N", size=11, color=GRAY)
    f.arrow(575, 265, 645, 265, "Pd, 190 ℃", "−H₂ (방향족화)")
    m = Mol()
    n = fused_iq(m, "q", 0, 0, aromatic=True)
    m.sub("me", n["1"], 90)
    f.mol(m, 685, 270)
    f.cap(715, 320, "C: 1-methylisoquinoline", color=RED)
    f.text(715, 338, "C₁₀H₉N", size=11, color=GRAY)
    return f.render()


def f2007_12_nmr():
    f = Fig(800, 275)
    legend(f, 560, 18, (("¹H NMR", RED), ("¹³C NMR", GREEN)))
    f.text(20, 18, "스펙트럼 귀속", size=13, anchor="start", weight="bold")
    m = Mol()
    a = phen_chain(m, "r", 0, 0)
    m.sub("c1", a, 30)
    m.sub("c2", "c1", -30)
    m.sub("n", "c2", 30, "NH_2", anchor="start")
    ox, oy = 90, 125
    f.mol(m, ox, oy)
    tag(f, m, "c1", ox, oy, -5, -50, "δ 2.73 (t, 2H) / 40.2", anchor="middle")
    tag(f, m, "c2", ox, oy, 15, 50, "δ 2.97 (t, 2H) / 43.6")
    tag(f, m, "n", ox, oy, 40, -35, "δ 1.1 (s, 2H)", anchor="start")
    tag(f, m, "r4", ox, oy, -10, 50, "δ 7.2–7.3 (m, 5H)")
    f.text(20, 258, "A ¹³C: 139.8(ipso) 128.8·128.4(o, m) 126.1(p) 43.6 40.2", size=11.5, anchor="start", color=GREEN)
    m = Mol()
    n = fused_iq(m, "q", 0, 0, aromatic=True)
    m.sub("me", n["1"], 90)
    ox, oy = 540, 140
    f.mol(m, ox, oy)
    tag(f, m, "me", ox, oy, -40, -15, "δ 2.95 (s, 3H) / 22.3", anchor="end")
    tag(f, m, n["3"], ox, oy, 45, 10, "H3 δ 8.4 (d) / 141.6", anchor="start")
    tag(f, m, n["4"], ox, oy, 20, 42, "H4 δ 7.5 (d) / 119.2", anchor="start")
    tag(f, m, n["1"], ox, oy, 45, -30, "C1 158.4 (C=N)", color=GREEN, anchor="start")
    tag(f, m, n["8"], ox, oy, -45, -20, "H8 δ 8.1 (d)", anchor="end")
    tag(f, m, n["6"], ox, oy, -35, 30, "H5–H7 δ 7.5–7.8", anchor="end")
    f.text(430, 258, "C ¹³C: 10개 신호 — 135.7(C4a), 125–130(C5–C8, C8a)", size=11.5, anchor="start", color=GREEN)
    return f.render()


# ------------------------------------------------------------------ 2006 #13 ethyl cyanoformate
def f2006_13():
    f = Fig(800, 240)
    f.text(20, 20, "C₄H₅NO₂ = ethyl cyanoformate  N≡C–CO₂CH₂CH₃", size=13, anchor="start", weight="bold")
    legend(f, 560, 20)
    m = Mol()
    m.atom("c2", 0, 0)
    m.sub("c1", "c2", 150)
    m.sub("n", "c1", 150, "N", kind=3)
    m.sub("o", "c2", -90, "O", kind="2")
    m.sub("oe", "c2", 30, "O")
    m.sub("e1", "oe", -30)
    m.sub("e2", "e1", 30)
    ox, oy = 200, 130
    f.mol(m, ox, oy)
    tag(f, m, "c1", ox, oy, -55, 30, "109.5 (C≡N)", color=GREEN, anchor="end")
    tag(f, m, "c2", ox, oy, 0, -55, "144.3 (C=O)", color=GREEN)
    tag(f, m, "e1", ox, oy, 20, 45, "65.3 / δ 4.41 (q, 2H)")
    tag(f, m, "e2", ox, oy, 40, -30, "13.7 / δ 1.39 (t, 3H)", anchor="start")
    tag(f, m, "n", ox, oy, -10, -40, "2246 C≡N", color=BLUE)
    tag(f, m, "o", ox, oy, -40, 35, "1750 C=O, 1245 C–O", color=BLUE, anchor="end")
    f.box(430, 45, 355, 180)
    f.text(442, 65, "분자식 구하기 (M = 99.1)", size=12, anchor="start", weight="bold")
    rows = ["C: 99.1 × 0.485 ÷ 12.01 = 4.00", "H: 99.1 × 0.051 ÷ 1.008 = 5.0",
            "N: 99.1 × 0.141 ÷ 14.01 = 1.00", "O: 99.1 × 0.323 ÷ 16.00 = 2.00",
            "→ C₄H₅NO₂,  불포화도 = (2·4 + 2 + 1 − 5)/2 = 3", "   = C≡N (2) + C=O (1)"]
    for i, t in enumerate(rows):
        f.text(452, 90 + i * 22, t, size=11.5, anchor="start", color=RED if i >= 4 else INK)
    return f.render()


# ------------------------------------------------------------------ 2005 #13 4-methoxyphenylacetone
def f2005_13():
    f = Fig(800, 300)
    f.text(20, 20, "M⁺ = 164, C₁₀H₁₂O₂ = 1-(4-methoxyphenyl)propan-2-one (4-methoxyphenylacetone)", size=13, anchor="start", weight="bold")
    legend(f, 560, 42, (("¹H NMR", RED), ("IR", BLUE), ("MS", PURPLE)))
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    m.sub("c1", "r0", 90)
    m.sub("c2", "c1", 30)
    m.sub("o2", "c2", 90, "O", kind="2")
    m.sub("c3", "c2", -30)
    m.sub("o", "r3", -90, "O")
    m.sub("me", "o", -30, "CH_3", anchor="start")
    ox, oy = 170, 165
    f.mol(m, ox, oy)
    tag(f, m, "c1", ox, oy, -50, -15, "δ 3.64 (s, 2H)", anchor="end")
    tag(f, m, "c3", ox, oy, 45, 10, "δ 2.14 (s, 3H)", anchor="start")
    tag(f, m, "r1", ox, oy, 55, 0, "δ 7.10 (d, J ≈ 8.5, 2H)", anchor="start")
    tag(f, m, "r2", ox, oy, 55, 5, "δ 6.86 (d, J ≈ 8.5, 2H)", anchor="start")
    tag(f, m, "me", ox, oy, 50, 10, "δ 3.79 (s, 3H)", anchor="start")
    tag(f, m, "o2", ox, oy, 50, 12, "1715 C=O (비공액 케톤)", color=BLUE, anchor="start")
    tag(f, m, "o", ox, oy, -45, 10, "1250 Ar–O–C", color=BLUE, anchor="end")
    f.box(470, 75, 315, 205)
    f.text(482, 95, "판단 근거", size=12, anchor="start", weight="bold")
    rows = [("적분 4 : 3 : 2 : 3 = 12 H", INK), ("AA′BB′ 두 doublet → para 이치환", INK),
            ("3.79(3H) = Ar–OCH₃, 3.64(2H, s) = ArCH₂C=O", INK),
            ("2.14(3H, s) = CH₃C=O (메틸 케톤)", INK), ("1715: 공액 안 된 C=O(CH₂가 끊음)", BLUE),
            ("830 cm⁻¹: para 치환 C–H 면외 굽힘", BLUE), ("MS 예상: 121 (MeO–C₆H₄–CH₂⁺, 기준),", PURPLE),
            ("         43 (CH₃C≡O⁺)", PURPLE)]
    for i, (t, c) in enumerate(rows):
        f.text(482, 119 + i * 21, t, size=11.2, anchor="start", color=c)
    return f.render()


# ------------------------------------------------------------------ 2004 #6
def heptanol(m):
    m.atom("c", 0, 0)
    m.sub("oh", "c", 90, "OH")
    m.sub("me", "c", -90)
    m.sub("a1", "c", 30)
    m.sub("a2", "a1", -30)
    m.sub("a3", "a2", 30)
    m.sub("b1", "c", 150)
    m.sub("b2", "b1", 210)
    m.sub("b3", "b2", 150)


def f2004_6():
    f = Fig(800, 345)
    f.text(20, 20, "A(C₈H₁₈O) —H₂SO₄, Δ→ B(C₈H₁₆) —O₃→ C(C₅H₁₀O) + D(C₃H₆O)", size=13, anchor="start", weight="bold")
    m = Mol()
    heptanol(m)
    f.mol(m, 110, 100)
    f.cap(110, 160, "A: 4-methyl-4-heptanol")
    f.text(110, 178, "3차 알코올, 대칭(두 프로필) → 비카이랄", size=11, color=GRAY)
    f.arrow(230, 95, 330, 95, "H_2SO_4, Δ", "E1, −H₂O (Zaitsev)")
    m = Mol()
    m.atom("c1", 0, 0)
    m.sub("c2", "c1", -30)
    m.sub("c3", "c2", 30)
    m.sub("c4", "c3", -30, kind="2")
    m.sub("c5", "c4", 30)
    m.sub("c6", "c5", -30)
    m.sub("c7", "c6", 30)
    m.sub("me", "c4", -90)
    f.mol(m, 360, 100)
    f.cap(450, 160, "B: 4-methyl-3-heptene (E/Z)")
    f.text(450, 178, "삼치환 알켄(주), 이중결합 C3=C4", size=11, color=GRAY)
    f.raw(f'<line x1="425" y1="60" x2="425" y2="140" stroke="{RED}" stroke-width="1.4" stroke-dasharray="4 3"/>')
    f.text(560, 72, "O₃ 절단 위치", size=11, color=RED)
    # 2행
    f.arrow(40, 245, 120, 245, "1) O_3", "2) Zn, H_2O")
    f.text(25, 245, "B", size=14, weight="bold")
    m = Mol()
    m.atom("c1", 0, 0)
    m.sub("c2", "c1", -30)
    m.sub("o", "c2", -90, "O", kind="2")
    m.sub("c3", "c2", 30)
    m.sub("c4", "c3", -30)
    m.sub("c5", "c4", 30)
    ox, oy = 160, 245
    f.mol(m, ox, oy)
    tag(f, m, "c1", ox, oy, -20, -35, "δ 2.05 (s)")
    tag(f, m, "c3", ox, oy, 0, -40, "δ 2.32 (t)")
    tag(f, m, "c4", ox, oy, 30, 42, "δ 1.56 (6중선)")
    tag(f, m, "c5", ox, oy, 50, -15, "δ 0.90 (t)", anchor="start")
    tag(f, m, "o", ox, oy, -45, 20, "1710 C=O", color=BLUE, anchor="end")
    f.cap(250, 332, "C: 2-pentanone")
    f.text(345, 245, "+", size=16)
    m = Mol()
    m.atom("o", 0, 0, "O")
    m.sub("c1", "o", -30, kind="2")
    m.sub("h", "c1", -90, "H")
    m.sub("c2", "c1", 30)
    m.sub("c3", "c2", -30)
    f.mol(m, 390, 245)
    f.cap(430, 332, "D: propanal")
    f.box(520, 200, 265, 115)
    rows = ["D: 은거울(Tollens) + → 알데하이드", "   아이오도폼 − → CH₃CO– 없음", "   ∴ CH₃CH₂CHO (acetone 아님)",
            "C: 2.05(s, 3H) → CH₃CO– 메틸 케톤"]
    for i, t in enumerate(rows):
        f.text(530, 222 + i * 23, t, size=11.3, anchor="start")
    return f.render()


# ------------------------------------------------------------------ 2004 #7
def f2004_7():
    f = Fig(800, 320)
    f.text(20, 20, "C₆H₁₀Br₂ (M = 240, 불포화도 1): C·CH₂·CH₃ 탄소가 각각 한 종류씩(2개씩 동등)", size=13, anchor="start", weight="bold")
    # (1) 2,3-bis(bromomethyl)-2-butene
    m = Mol()
    m.atom("c2", 0, 0)
    m.sub("c3", "c2", 0, kind="2")
    m.sub("b1", "c2", 120)
    m.sub("br1", "b1", 180, "Br")
    m.sub("m1", "c2", 240)
    m.sub("b2", "c3", -60)
    m.sub("br2", "b2", 0, "Br")
    m.sub("m2", "c3", 60)
    f.mol(m, 100, 110)
    f.cap(115, 175, "① 1,4-dibromo-2,3-")
    f.cap(115, 193, "dimethyl-2-butene (E/Z)")
    # (2) 1,2-dibromo-1,2-dimethylcyclobutane
    m = Mol()
    m.ring("q", 0, 0, 4, L / math.sqrt(2), 135)
    m.sub("br1", "q0", 115, "Br")
    m.sub("m1", "q0", 190)
    m.sub("br2", "q1", 65, "Br")
    m.sub("m2", "q1", -10)
    f.mol(m, 330, 110)
    f.cap(330, 175, "② 1,2-dibromo-1,2-")
    f.cap(330, 193, "dimethylcyclobutane")
    # (3) 1,3-dibromo-1,3-dimethylcyclobutane
    m = Mol()
    m.ring("q", 0, 0, 4, L / math.sqrt(2), 180)
    m.sub("br1", "q0", 135, "Br")
    m.sub("m1", "q0", 225)
    m.sub("br2", "q2", 45, "Br")
    m.sub("m2", "q2", -45)
    f.mol(m, 540, 110)
    f.cap(540, 175, "③ 1,3-dibromo-1,3-")
    f.cap(540, 193, "dimethylcyclobutane")
    f.text(700, 90, "각 구조:", size=11.5, weight="bold")
    f.text(700, 110, "C–Br 사차 C ×2", size=11, color=RED)
    f.text(700, 128, "CH₂ ×2 (DEPT-135 ↓)", size=11, color=BLUE)
    f.text(700, 146, "CH₃ ×2 (DEPT-135 ↑)", size=11, color=GREEN)
    f.text(700, 164, "CH 없음 (DEPT-90 빈칸)", size=11, color=GRAY)
    # MS
    bars(f, 70, 295, 200, 70, 238, 246, [(240, 51, "240"), (242, 100, "242"), (244, 49, "244")], ticks=())
    f.text(310, 238, "M : M+2 : M+4 ≈ 1 : 2 : 1 → Br 2개", size=12, anchor="start", color=PURPLE, weight="bold")
    f.text(310, 260, "(1 + 0.98)² = 1 : 1.96 : 0.96  (⁷⁹Br : ⁸¹Br = 100 : 98)", size=11.5, anchor="start")
    f.text(310, 282, "240 − 2×79 = 82 → C₆H₁₀ → C₆H₁₀Br₂, 불포화도 = (14 − 12)/2 = 1", size=11.5, anchor="start")
    return f.render()


# ------------------------------------------------------------------ 2003 #17
def anisole_acyl(m, ortho=False):
    benzene(m, "r", 0, 0, 90)
    m.sub("c", "r0", 90)
    m.sub("o", "c", 30, "O", kind="2")
    m.sub("me", "c", 150)
    if ortho:
        m.sub("om", "r5", 210, "O")
        m.sub("om2", "om", 150, "CH_3", anchor="end")
    else:
        m.sub("om", "r3", -90, "O")
        m.sub("om2", "om", -30, "CH_3", anchor="start")


def f2003_17():
    f = Fig(800, 300)
    f.text(20, 20, "anisole + CH₃COCl / AlCl₃ (Friedel–Crafts 아실화, –OCH₃: o,p-지향)", size=13, anchor="start", weight="bold")
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    m.sub("o", "r0", 90, "OCH_3")
    f.mol(m, 60, 140)
    f.text(135, 140, "+ CH_3COCl", size=13)
    f.arrow(185, 140, 255, 140, "AlCl_3", "")
    m = Mol()
    anisole_acyl(m)
    ox, oy = 335, 150
    f.mol(m, ox, oy)
    for nm, lab, dx, dy in [("me", "b", -18, -8), ("r1", "c", 16, -6), ("r5", "c", -16, -6),
                            ("r2", "d", 16, 6), ("r4", "d", -16, 6), ("om2", "a", 30, 8)]:
        x, y = A(m, nm, ox, oy)
        f.text(x + dx, y + dy, lab, size=13, color=RED, weight="bold")
    f.cap(335, 262, "A (para, 주): 4-methoxyacetophenone")
    f.text(335, 282, "¹H 4종류: a 3.87(s,3H) b 2.55(s,3H) c 7.93(d,2H) d 6.93(d,2H)", size=11, color=RED)
    f.text(468, 140, "+", size=16)
    m = Mol()
    anisole_acyl(m, ortho=True)
    ox, oy = 600, 150
    f.mol(m, ox, oy)
    for nm, lab, dx, dy in [("me", "b", -18, -8), ("r1", "c", 16, -6), ("r2", "d", 16, 6),
                            ("r3", "e", 0, 16), ("r4", "f", -16, 6), ("om2", "a", -10, 16)]:
        x, y = A(m, nm, ox, oy)
        f.text(x + dx, y + dy, lab, size=13, color=RED, weight="bold")
    f.cap(625, 262, "B (ortho, 부): 2-methoxyacetophenone")
    f.text(625, 282, "¹H 6종류: CH₃ 2개 + 방향족 H 4개 모두 다름", size=11, color=RED)
    return f.render()


def f2003_17b():
    f = Fig(800, 250)
    f.text(20, 20, "17-2  A의 ¹³C 신호 7종류   |   17-3  페놀의 O-아세틸화", size=13, anchor="start", weight="bold")
    m = Mol()
    anisole_acyl(m)
    ox, oy = 120, 140
    f.mol(m, ox, oy)
    for nm, lab, dx, dy in [("c", "1", 14, 4), ("me", "2", -4, -14), ("r0", "3", 0, 14), ("r1", "4", 14, -4),
                            ("r5", "4", -14, -4), ("r2", "5", 14, 4), ("r4", "5", -14, 4), ("r3", "6", 13, 2), ("om2", "7", 5, 15)]:
        x, y = A(m, nm, ox, oy)
        f.text(x + dx, y + dy, lab, size=12.5, color=GREEN, weight="bold")
    rows = ["1 C=O 196.8", "2 COCH₃ 26.3", "3 C1 130.3", "4 C2,6 130.6", "5 C3,5 113.7", "6 C4 163.5", "7 OCH₃ 55.5"]
    for i, t in enumerate(rows):
        f.text(225, 72 + i * 21, t, size=11.3, anchor="start", color=GREEN)
    f.text(225, 232, "대칭면 → C2=C6, C3=C5", size=11, anchor="start", color=GRAY)
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    m.sub("o", "r0", 90, "OH")
    f.mol(m, 410, 140)
    f.text(495, 140, "+ CH_3COCl", size=13)
    f.arrow(545, 140, 615, 140, "염기", "(pyridine/NaOH)")
    m = Mol()
    benzene(m, "r", 0, 0, 90)
    m.sub("o", "r0", 90, "O")
    m.sub("c", "o", 30)
    m.sub("o2", "c", 90, "O", kind="2")
    m.sub("me", "c", -30)
    f.mol(m, 670, 150)
    f.cap(700, 225, "C: phenyl acetate (에스터)", color=RED)
    return f.render()


# ------------------------------------------------------------------ 2002 #15
def dm_core(m, head):
    """head: 'vinyl' | 'cho' | 'cooh' — C(CH3)2CH2CH3 골격"""
    m.atom("q", 0, 0)
    m.sub("m1", "q", 60)
    m.sub("m2", "q", 120)
    m.sub("e1", "q", -30)
    m.sub("e2", "e1", 30)
    m.sub("h1", "q", 210)
    if head == "vinyl":
        m.sub("h2", "h1", 150, kind="2")
    elif head == "cho":
        m.sub("h2", "h1", 150, "O", kind="2")
        m.sub("hh", "h1", -90, "H")
    else:
        m.sub("h2", "h1", 150, "O", kind="2")
        m.sub("hh", "h1", -90, "OH")


def f2002_15():
    f = Fig(800, 270)
    f.text(20, 20, "A = 3,3-dimethyl-1-pentene → B = 2,2-dimethylbutanal → C = 2,2-dimethylbutanoic acid", size=13, anchor="start", weight="bold")
    legend(f, 560, 42, (("¹H NMR", RED), ("¹³C NMR", GREEN)))
    m = Mol()
    dm_core(m, "vinyl")
    f.mol(m, 90, 120)
    f.cap(90, 185, "A (C₇H₁₄)")
    f.arrow(160, 120, 230, 120, "1) O_3", "2) Zn, H_2O")
    m = Mol()
    dm_core(m, "cho")
    f.mol(m, 310, 120)
    f.cap(310, 185, "B (C₆H₁₂O)")
    f.text(310, 203, "+ HCHO", size=11.5, color=GRAY)
    f.text(310, 221, "Fehling (+): 알데하이드", size=11, color=GRAY)
    f.arrow(385, 120, 470, 120, "1) Ag_2O, OH^−", "2) H_3O^+")
    m = Mol()
    dm_core(m, "cooh")
    ox, oy = 590, 130
    f.mol(m, ox, oy)
    tag(f, m, "hh", ox, oy, -10, 40, "δ 12.08 (s, 1H) / 185.2", anchor="end")
    tag(f, m, "m1", ox, oy, 45, -12, "δ 1.15 (s, 6H) / 24.4", anchor="start")
    tag(f, m, "e1", ox, oy, 0, 50, "δ 1.57 (q, 2H) / 33.2")
    tag(f, m, "e2", ox, oy, 40, 15, "δ 0.89 (t, 3H) / 9.2", anchor="start")
    tag(f, m, "q", ox, oy, -50, -55, "사차 C 42.5", color=GREEN, anchor="end")
    f.cap(590, 245, "C (C₆H₁₂O₂)")
    return f.render()
