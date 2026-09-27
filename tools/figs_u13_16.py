"""13 알데하이드와 케톤 · 14 카복실산과 그 유도체 · 15 α탄소 치환반응 · 16 축합반응 문항 그림"""
import math
from chemsvg import Mol, Fig, benzene, L, RED, BLUE, INK

GREEN = "#2f7d5b"
GRAY = "#5b6270"
R5 = L / (2 * math.sin(math.pi / 5))  # 오각형 외접 반지름


# ------------------------------------------------------------------ 공통 헬퍼
def poly_on_edge(m, p, a1, a2, n, away, kinds=None):
    """a1–a2 변을 공유하는 n각형을 away 점의 반대쪽에 붙인다.
    새 원자 p1..p(n-2) (p1은 a2 옆, 마지막은 a1 옆). kinds: a2→p1→…→a1 결합 종류 목록."""
    (x1, y1), (x2, y2) = m.pos(a1), m.pos(a2)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)
    nx, ny = -dy / d, dx / d
    if nx * (away[0] - mx) + ny * (away[1] - my) > 0:
        nx, ny = -nx, -ny
    apo = d / (2 * math.tan(math.pi / n))
    R = d / (2 * math.sin(math.pi / n))
    cx, cy = mx + nx * apo, my + ny * apo
    t1 = math.atan2(y1 - cy, x1 - cx)
    t2 = math.atan2(y2 - cy, x2 - cx)
    diff = (t2 - t1 + math.pi) % (2 * math.pi) - math.pi
    s = (2 * math.pi / n) * (1 if diff > 0 else -1)
    names = []
    for k in range(1, n - 1):
        t = t2 + s * k
        nm = f"{p}{k}"
        m.atom(nm, cx + R * math.cos(t), cy + R * math.sin(t))
        names.append(nm)
    seq = [a2] + names + [a1]
    kinds = kinds or [1] * (len(seq) - 1)
    for i in range(len(seq) - 1):
        k = kinds[i]
        if k == "in":
            m.bond(seq[i], seq[i + 1], "in", (cx, cy))
        else:
            m.bond(seq[i], seq[i + 1], k)
    return names, (cx, cy)


def enone(m, p="r"):
    """2-cyclohexenone (p0 = C1, p1=p2 이중 결합)"""
    m.ring(p, 0, 0, 6, L, 90, arom=[1])
    m.sub(p + "o", p + "0", 90, "O", kind="2")
    return m


def cyhex_one(m, p="r"):
    m.ring(p, 0, 0, 6, L, 90)
    m.sub(p + "o", p + "0", 90, "O", kind="2")
    return m


def bracket(f, x, y1, y2, left=True, n=False):
    d = 6 if left else -6
    f.raw(f'<path d="M{x + d},{y1} L{x},{y1} L{x},{y2} L{x + d},{y2}" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    if n:
        f.text(x + 7, y2 + 4, "n", size=12, italic=True)


def ok(f, x, y, t, good=True):
    f.text(x, y, t, size=12.5, weight="bold", color=GREEN if good else RED)


# ================================================================== 13. 알데하이드와 케톤
# ---------------------------------------------------------------- 2012 1차 39번
def f2012_39_g():
    f = Fig(800, 215)
    f.text(16, 18, "ㄱ. pinacol 자리옮김 — 안정한 Ph₂C⁺ 생성 → 고리 C–C 결합 이동(5→6 고리 확장)", size=13, anchor="start", weight="bold")
    # 출발 물질
    m = Mol()
    m.ring("r", 0, 0, 5, R5, 0)
    m.sub("oh", "r0", 95, "OH")
    c = m.sub("c", "r0", 0)
    m.sub("o2", c, 40, "OH")
    m.sub("p1", c, -40, "Ph")
    m.sub("p2", c, -100, "Ph")
    f.mol(m, 55, 110)
    f.arrow(150, 105, 215, 105, "H₂SO₄", "–H₂O")
    # 탄소 양이온
    m = Mol()
    m.ring("r", 0, 0, 5, R5, 0)
    m.sub("oh", "r0", 95, "OH")
    c = m.sub("c", "r0", 0, "C^+")
    m.sub("p1", c, -40, "Ph")
    m.sub("p2", c, 40, "Ph")
    f.mol(m, 265, 110)
    x0, y0 = 265 + R5, 110
    f.curly(x0 - 7, y0 + 15, x0 + 22, y0 + 5, bend=0.6)
    f.text(292, 180, "고리 결합 1,2-이동", size=11, color=RED)
    f.arrow(360, 105, 425, 105, "고리 확장", "(5 → 6)")
    # 옥소카베늄
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.sub("o", "r0", 90, "O^+H", kind="2")
    m.sub("p1", "r1", 30, "Ph")
    m.sub("p2", "r1", -30, "Ph")
    f.mol(m, 480, 125)
    f.arrow(555, 105, 610, 105, "–H⁺")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.sub("o", "r0", 90, "O", kind="2")
    m.sub("p1", "r1", 30, "Ph")
    m.sub("p2", "r1", -30, "Ph")
    f.mol(m, 670, 125)
    ok(f, 690, 200, "2,2-diphenylcyclohexanone ✓")
    return f.render()


def f2012_39_nd():
    f = Fig(800, 330)
    f.text(16, 18, "ㄴ. Baeyer–Villiger 산화 — 이동 경향: 3° > 2°(cyclohexyl) ≈ Ph > 1° > CH₃", size=13, anchor="start", weight="bold")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    c = m.sub("c", "r1", 30)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("me", c, -30)
    f.mol(m, 60, 95)
    f.arrow(165, 90, 250, 90, "PhCO₃H", "CHCl₃")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    o = m.sub("o1", "r1", 30, "O")
    c = m.sub("c", o, -30)
    m.sub("o2", c, -90, "O", kind="2")
    m.sub("me", c, 30)
    f.mol(m, 300, 95)
    ok(f, 350, 150, "cyclohexyl acetate (주생성물)")
    f.text(560, 70, "보기의 methyl cyclohexanecarboxylate는", size=12)
    f.text(560, 90, "CH₃가 이동했다고 본 것 → ✗", size=12, color=RED, weight="bold")
    f.text(560, 115, "O는 더 잘 이동하는 cyclohexyl 쪽에 삽입", size=11.5, color=GRAY)
    # ㄷ
    f.text(16, 185, "ㄷ. 아실 아자이드의 Curtius 자리옮김 → 아이소사이아네이트 → 가수분해·탈카복실 (탄소 1개 감소)", size=13, anchor="start", weight="bold")
    m = Mol()
    benzene(m, "a", 0, 0, 90)
    ch = m.sub("ch", "a1", 30)
    c = m.sub("c", ch, -30)
    m.sub("o", c, -90, "O", kind="2")
    m.sub("cl", c, 30, "Cl")
    m.sub("me", "a2", -30)
    f.mol(m, 45, 265)
    f.arrow(150, 268, 195, 268, "NaN₃")
    f.text(250, 262, "ArCH_2–CO–N_3", size=12.5)
    f.arrow(305, 262, 370, 262, "Δ, –N₂", "Curtius")
    f.text(430, 262, "ArCH_2–N=C=O", size=12.5)
    f.arrow(488, 262, 560, 262, "H₂O", "–CO₂")
    m = Mol()
    benzene(m, "a", 0, 0, 90)
    ch = m.sub("ch", "a1", 30)
    m.sub("n", ch, -30, "NH_2")
    m.sub("me", "a2", -30)
    f.mol(m, 610, 265)
    ok(f, 650, 318, "2-methylbenzylamine ✓")
    return f.render()


# ---------------------------------------------------------------- 2012 2차 논술형 4번
def f2012_4_struct():
    f = Fig(800, 270)
    # (가) aldol 첨가 생성물
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.sub("o", "r5", 150, "O", kind="2")
    b0 = m.sub("b0", "r0", 90)
    m.ring("b", 0, -90, 6, L, 270)
    m.sub("oh", "b0", 210, "OH")
    f.mol(m, 95, 175)
    f.cap(95, 232, "(가) aldol 첨가 생성물")
    f.text(95, 252, "2-(1-hydroxycyclohexyl)cyclohexanone", size=10.5, color=GRAY)
    # (나) 이미늄 이온
    m = Mol()
    m.ring("p", 0, 0, 5, R5, 90)
    n = "p0"
    m.label(n, "N^+")
    c = m.sub("c", n, 30, kind="2")
    m.sub("me", c, -30)
    f.mol(m, 275, 170)
    f.cap(285, 232, "(나) 이미늄 이온")
    f.text(285, 252, "CH₃CH=N⁺(CH₂)₄", size=11, color=GRAY)
    # (다) polycarbonate
    m = Mol()
    m.atom("o1", 0, 0, "O")
    m.ring("a", 2 * L, 0, 6, L, 180, arom=[0, 2, 4])
    m.bond("o1", "a0")
    q = m.sub("q", "a3", 0)
    m.sub("q1", q, 90)
    m.sub("q2", q, -90)
    m.ring("b", 6 * L, 0, 6, L, 180, arom=[0, 2, 4])
    m.bond(q, "b0")
    o2 = m.sub("o2", "b3", 0, "O")
    c = m.sub("c", o2, 0)
    m.sub("co", c, 90, "O", kind="2")
    m.atom("e1", -L, 0)
    m.bond("e1", "o1")
    m.atom("e2", 10 * L, 0)
    m.bond(c, "e2")
    f.mol(m, 435, 165)
    bracket(f, 413, 140, 190, left=True)
    bracket(f, 738, 140, 190, left=False, n=True)
    f.cap(580, 232, "(다) 폴리카보네이트 (bisphenol A polycarbonate)")
    return f.render()


def f2012_4_enolate():
    f = Fig(800, 210)
    f.text(16, 18, "[반응 Ⅰ] 엔올레이트 생성 평형: 염기의 짝산 pKₐ와 비교", size=13, anchor="start", weight="bold")
    f.box(16, 34, 372, 160)
    f.text(202, 54, "NaOH / EtOH (양성자성)", size=12.5, weight="bold")
    f.text(202, 84, "케톤(pKₐ ≈ 19–20) + OH⁻/EtO⁻(짝산 pKₐ 15.7–16)", size=11.5)
    f.text(202, 106, "K ≈ 10^{−3.5} → 엔올레이트 극소량(가역)", size=11.5)
    f.text(202, 130, "EtOH가 엔올레이트를 곧바로 양성자화·수소 결합 용매화", size=11.5)
    f.text(202, 156, "→ 엔올레이트 농도 ↓, 첨가 단계 느림·가역", size=12, color=GRAY, weight="bold")
    f.text(202, 178, "(대신 남은 케톤이 많아 자기 aldol·탈수 진행)", size=11, color=GRAY)
    f.box(410, 34, 372, 160, fill="#fdf1f0", stroke="#e6b0aa")
    f.text(596, 54, "LDA / THF (비양성자성)", size=12.5, weight="bold", color=RED)
    f.text(596, 84, "케톤 + (i-Pr)₂N⁻ (짝산 pKₐ ≈ 36)", size=11.5)
    f.text(596, 106, "K ≈ 10^{16} → 정량적·비가역 탈양성자화", size=11.5)
    f.text(596, 130, "부피 큰 비친핵성 염기, THF는 H⁺ 공급·수소 결합 ✗", size=11.5)
    f.text(596, 156, "→ 엔올레이트 농도 최대, 친핵성 ↑(빠른 반응)", size=12, color=RED, weight="bold")
    f.text(596, 178, "(케톤이 거의 남지 않음 → 친전자체를 따로 넣는 지정 aldol)", size=11, color=GRAY)
    return f.render()


def f2012_4_imine():
    f = Fig(800, 330)
    f.text(16, 18, "[반응 Ⅱ] 환원성 아미노화: 이미늄 형성(산 촉매) → NaBH₃CN의 선택적 환원", size=13, anchor="start", weight="bold")
    y = 70
    f.text(60, y, "CH_3CHO + R_2NH", size=12.5)
    f.eqarrow(115, 170, y, "첨가")
    f.text(245, y, "CH_3CH(OH)–NR_2", size=12.5)
    f.text(245, y + 22, "카비놀아민", size=11, color=GRAY)
    f.eqarrow(315, 370, y, "H⁺")
    f.text(440, y, "CH_3CH(O^+H_2)–NR_2", size=12.5)
    f.arrow(515, y, 565, y, "–H₂O")
    f.text(625, y, "CH_3CH=N^+R_2", size=12.5, color=RED)
    f.text(625, y + 22, "(나) 이미늄", size=11, color=RED)
    f.arrow(625, y + 34, 625, y + 64, "H⁻ (NaBH₃CN)")
    f.text(625, y + 78, "CH_3CH_2–NR_2", size=12.5)
    f.text(672, y + 80, "N-ethylpyrrolidine", size=11, color=GRAY, anchor="start")
    f.text(60, y + 30, "R₂NH = pyrrolidine", size=11, color=GRAY)
    # 속도–pH 곡선
    x0, y0, w, h = 60, 300, 330, 150
    f.raw(f'<line x1="{x0}" y1="{y0}" x2="{x0 + w}" y2="{y0}" stroke="{INK}" stroke-width="1.3"/>'
          f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 - h}" stroke="{INK}" stroke-width="1.3"/>')
    pts = []
    for i in range(61):
        ph = 1 + 9 * i / 60
        fa = 1 / (1 + 10 ** (ph - 5.8))        # 탈수에 필요한 H⁺
        fb = 1 / (1 + 10 ** (3.2 - ph))        # 자유 아민 분율(유효)
        pts.append((x0 + (ph - 1) / 9 * w, fa * fb))
    mx = max(p[1] for p in pts)
    d = "M" + " L".join(f"{x:.1f},{y0 - 8 - (v / mx) * (h - 20):.1f}" for x, v in pts)
    f.raw(f'<path d="{d}" fill="none" stroke="{BLUE}" stroke-width="2"/>')
    for ph in (2, 5, 8):
        x = x0 + (ph - 1) / 9 * w
        f.raw(f'<line x1="{x:.1f}" y1="{y0}" x2="{x:.1f}" y2="{y0 + 5}" stroke="{INK}"/>')
        f.text(x, y0 + 14, f"pH {ph}", size=10.5)
    f.text(x0 + 6, y0 - h - 8, "↑ 이미늄 형성 속도", size=11, anchor="start")
    f.text(x0 + 4 / 9 * w + 60, y0 - h + 10, "최적 pH ≈ 4–5", size=11, color=BLUE)
    f.box(420, 170, 365, 145, fill="#fdf1f0", stroke="#e6b0aa")
    f.text(432, 190, "pH 5 → pH 2로 낮추면", size=12.5, anchor="start", weight="bold", color=RED)
    f.text(432, 213, "• pyrrolidine(짝산 pKₐ ≈ 11.3) 거의 전부 R₂NH₂⁺", size=11.5, anchor="start")
    f.text(432, 233, "  → 친핵체 농도 ↓ → 카비놀아민·이미늄 농도 ↓", size=11.5, anchor="start")
    f.text(432, 256, "• C=O가 양성자화되어 BH₃CN⁻이 알데하이드를", size=11.5, anchor="start")
    f.text(432, 276, "  직접 환원(→ 에탄올) → 선택성 상실", size=11.5, anchor="start")
    f.text(432, 299, "• 강산에서 NaBH₃CN 분해(HCN 발생) → 환원 효율 ↓", size=11.5, anchor="start")
    return f.render()


def f2012_4_pc():
    f = Fig(800, 150)
    f.text(16, 18, "[반응 Ⅲ] 페놀(페녹사이드)의 친핵성 아실 치환 반복 → 축합 중합 (–2 HCl)", size=13, anchor="start", weight="bold")
    f.text(130, 60, "Ar–OH + Cl–CO–Cl", size=12.5)
    f.arrow(215, 60, 290, 60, "–HCl")
    f.text(365, 60, "Ar–O–CO–Cl", size=12.5)
    f.arrow(420, 60, 500, 60, "+ HO–Ar′", "–HCl")
    f.text(610, 60, "Ar–O–CO–O–Ar′ (카보네이트)", size=12.5, color=RED)
    f.text(400, 100, "대체: bisphenol A + (EtO)₂C=O —(염기, Δ)→ 에스터 교환, EtOH 제거 (포스젠 불필요)", size=12)
    f.text(400, 125, "BPA 용출: 남은 단량체 또는 카보네이트 결합의 가수분해(열·산·염기) → 다시 BPA 생성", size=12, color=GRAY)
    return f.render()


# ---------------------------------------------------------------- 2003 16-2
def f2003_16_2():
    f = Fig(800, 220)
    f.text(60, 95, "CH_3CHO", size=13)
    f.text(60, 118, "(④ acetaldehyde)", size=11, color=GRAY)
    f.text(118, 95, "+", size=16)
    f.text(190, 95, "H_2N–NH–Ar", size=13)
    f.text(190, 118, "(2,4-DNPH)", size=11, color=GRAY)
    f.arrow(250, 95, 330, 95, "H⁺ (H₂SO₄)", "–H₂O")
    m = Mol()
    m.ring("a", 0, 0, 6, L, 180, arom=[0, 2, 4])
    n1 = m.sub("n1", "a0", 210, "N")
    m.sub("h", n1, 270, "H", length=22)
    n2 = m.sub("n2", n1, 150, "N")
    c = m.sub("c", n2, 210, kind="2")
    m.sub("me", c, 150)
    m.sub("no1", "a1", 120, "O_2N", anchor="end")
    m.sub("no2", "a3", 0, "NO_2", anchor="start")
    f.mol(m, 530, 100)
    ok(f, 520, 190, "acetaldehyde 2,4-dinitrophenylhydrazone (노란–주황 침전)")
    f.text(400, 212, "반응성: 알데하이드 > 케톤(②, 입체 장애 큼) ≫ 에스터(③)·요소(⑤: 공명으로 C=O 친전자성 ↓), ① C=O 없음", size=11, color=GRAY)
    return f.render()


# ---------------------------------------------------------------- 2002 14번
def f2002_14():
    f = Fig(800, 420)
    rows = [(70, "1) C₂H₅MgBr/Et₂O", "2) H₃O⁺", "1,2-첨가 (단단한 친핵체)"),
            (205, "CH₃NH₂ / H₂O", "", "1,4-(짝지음) 첨가"),
            (345, "+ 1,3-butadiene", "Δ", "Diels–Alder [4+2]")]
    for y, t, b, note in rows:
        m = Mol()
        enone(m)
        f.mol(m, 70, y + 10)
        f.arrow(150, y, 290, y, t, b)
        f.text(220, y + 34 if b else y + 16, note, size=11, color=BLUE)
    # 1
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90, arom=[1])
    m.sub("oh", "r0", 60, "OH")
    e1 = m.sub("e1", "r0", 120)
    m.sub("e2", e1, 180)
    f.mol(m, 400, 90)
    ok(f, 590, 70, "1-ethylcyclohex-2-en-1-ol")
    # 2
    m = Mol()
    cyhex_one(m)
    m.sub("n", "r2", -30, "NHCH_3", anchor="start")
    f.mol(m, 400, 215)
    ok(f, 590, 205, "3-(methylamino)cyclohexanone")
    # 3
    m = Mol()
    m.ring("a", 0, 0, 6, L, 90)
    m.ring("b", 2 * 26, 0, 6, L, 90, bonds=False)
    m.bond("a1", "b0")
    m.bond("b0", "b1")
    m.bond("b1", "b2", "in", (52, 0))
    m.bond("b2", "b3")
    m.bond("b3", "a2")
    m.sub("o", "a0", 90, "O", kind="2")
    m.sub("h1", "a1", 90, "H", kind="w", length=22)
    m.sub("h2", "a2", -90, "H", kind="w", length=22)
    f.mol(m, 380, 355)
    ok(f, 620, 335, "cis-융합 bicyclic 케톤")
    f.text(620, 357, "cis-3,4,4a,5,8,8a-hexahydronaphthalen-1(2H)-one", size=10.5, color=GRAY)
    f.text(620, 377, "(친다이엔체의 cis 배치 보존 → 두 H 같은 면)", size=10.5, color=GRAY)
    return f.render()


# ================================================================== 14. 카복실산과 그 유도체
# ---------------------------------------------------------------- 2011 38번
def ester(m, x_or="O", r="R^*"):
    c = m.atom("c", 0, 0)
    m.sub("o1", c, 90, "O", kind="2")
    m.sub("ph", c, 210, "Ph")
    o2 = m.sub("o2", c, -30, "O")
    m.sub("r", o2, 30, r, anchor="start")
    return m


def f2011_38():
    f = Fig(800, 250)
    f.text(16, 18, "염기성 가수분해(비누화) = BAc2: 아실 C–O 결합 절단, 입체 중심 C*–O 결합은 유지", size=13, anchor="start", weight="bold")
    m = Mol()
    ester(m)
    f.mol(m, 70, 110)
    f.text(40, 75, "HO^−", size=12.5, color=RED)
    f.curly(52, 82, 68, 104, bend=-0.3)
    f.arrow(140, 110, 190, 110, "①")
    # 사면체 중간체
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("o1", c, 90, "O^−")
    m.sub("oh", c, 180, "HO", anchor="end")
    m.sub("ph", c, 270, "Ph")
    o2 = m.sub("o2", c, 0, "O")
    m.sub("r", o2, 30, "R^*", anchor="start")
    f.mol(m, 245, 110)
    f.text(165, 128, "사면체 중간체", size=10.5, color=GRAY)
    f.arrow(320, 110, 370, 110, "②", "RO⁻ 이탈")
    f.text(430, 105, "PhCOOH  +", size=12.5)
    f.text(510, 105, "^−O–R^*", size=13, color=RED, weight="bold")
    f.text(505, 132, "(R)-sec-BuO⁻ = 중간체 (ㄴ)", size=11, color=RED)
    f.arrow(560, 110, 610, 110, "③ H⁺ 이동")
    f.text(700, 100, "PhCOO^− + HO–R^*", size=12.5)
    f.text(700, 122, "(R) 배치 유지", size=11, color=GREEN, weight="bold")
    f.box(16, 160, 768, 80)
    f.text(28, 180, "ㄱ ✗: OH⁻는 카복실레이트(PhCOO⁻) 생성에 1당량 소모 → 촉매가 아니라 반응물(비가역 산–염기 단계가 추진력)", size=11.5, anchor="start")
    f.text(28, 202, "ㄴ ○: ②에서 이탈한 알콕사이드가 ③에서 산을 탈양성자화 → 형성 후 소모되는 중간체", size=11.5, anchor="start")
    f.text(28, 224, "ㄷ ○: 카보닐 탄소–O(알콕시) 단일 결합 절단 → 알코올의 입체 배치 유지(C*에서 SN2가 일어났다면 반전)", size=11.5, anchor="start")
    return f.render()


# ---------------------------------------------------------------- 2010 38번
def f2010_38():
    f = Fig(800, 300)
    m = Mol()
    c1 = m.atom("c1", -26, 0)
    c2 = m.sub("c2", c1, 30)
    c3 = m.sub("c3", c2, -30)
    m.sub("o1", c1, 150, "HO", anchor="end")
    m.sub("o2", c2, 90, "OH")
    m.sub("o3", c3, 30, "OH")
    f.text(16, 18, "A (트라이아실글리세롤) + 3 NaOH → B + 지방산 나트륨염(비누)", size=13, anchor="start", weight="bold")
    f.mol(m, 110, 85)
    ok(f, 110, 130, "B = glycerol (알코올)")
    f.text(420, 50, "염: CH₃(CH₂)₇CH=CH(CH₂)₇COO⁻Na⁺ + 2 CH₃(CH₂)₁₆COO⁻Na⁺", size=12)
    f.arrow(420, 62, 420, 88, "H₃O⁺")
    f.text(420, 102, "C: 올레산 C₁₈H₃₄O₂ (C=C 1개)    D: 스테아르산 C₁₈H₃₆O₂", size=12)
    f.text(16, 160, "C → 뜨거운 KMnO₄ (C=C 산화적 절단, 생긴 알데하이드는 카복실산까지 산화)", size=12.5, anchor="start", weight="bold")
    f.text(190, 190, "CH₃(CH₂)₇CH=CH(CH₂)₇COOH", size=12)
    f.arrow(300, 190, 360, 190, "KMnO₄, Δ")
    f.text(490, 190, "CH₃(CH₂)₇COOH  +  HOOC(CH₂)₇COOH", size=12, color=RED)
    f.text(490, 210, "E, F: nonanoic acid + azelaic acid → 알데하이드기 ✗ (ㄴ 틀림)", size=11, color=RED)
    f.text(16, 240, "D → LiAlH₄ → 1차 알코올 G → PCC → 알데하이드 (케톤 ✗)", size=12.5, anchor="start", weight="bold")
    f.text(130, 270, "CH₃(CH₂)₁₆COOH", size=12)
    f.arrow(195, 270, 275, 270, "1) LiAlH₄ 2) H₃O⁺")
    f.text(360, 270, "CH₃(CH₂)₁₆CH₂OH (G)", size=12, color=GREEN)
    f.arrow(440, 270, 510, 270, "PCC")
    f.text(610, 270, "CH₃(CH₂)₁₆CHO (알데하이드)", size=12, color=RED)
    return f.render()


# ---------------------------------------------------------------- 2009 26번
def phthalimide(m, cx=0, n_label="NH"):
    benzene(m, "a", cx, 0, 90)
    names, cen = poly_on_edge(m, "f", "a1", "a2", 5, (cx, 0))
    # names: f1(a2 옆, 아래 C=O), f2(N), f3(a1 옆, 위 C=O)
    m.label("f2", n_label)
    m.sub("ob", "f1", -60, "O", kind="2")
    m.sub("ot", "f3", 60, "O", kind="2")
    return m


def f2009_26():
    f = Fig(800, 330)
    f.text(16, 18, "ㄱ ○  말단 알카인 C–H(pKₐ 25) + CH₃MgBr(짝산 CH₄, pKₐ ≈ 50) → 알카이닐 Grignard → 알데하이드 첨가", size=12.5, anchor="start", weight="bold")
    f.text(70, 55, "PhC≡C–H", size=12.5)
    f.arrow(110, 55, 185, 55, "CH₃MgBr", "–CH₄")
    f.text(245, 55, "PhC≡C–MgBr", size=12.5)
    f.arrow(300, 55, 385, 55, "CH₃CHO", "H₃O⁺")
    f.text(395, 55, "PhC≡C–CH(OH)–CH₃", size=12.5, color=GREEN, weight="bold", anchor="start")
    f.text(16, 100, "ㄴ ○  나이트릴 + Grignard → 이민 음이온 염(1회 첨가에서 멈춤) → 가수분해 → 케톤", size=12.5, anchor="start", weight="bold")
    f.text(70, 135, "PhC≡N", size=12.5)
    f.arrow(100, 135, 175, 135, "CH₃MgBr")
    f.text(245, 135, "Ph(CH₃)C=N^−MgBr^+", size=12.5)
    f.arrow(315, 135, 385, 135, "H₃O⁺")
    f.text(395, 135, "PhCOCH₃ (acetophenone) + NH₄⁺", size=12.5, color=GREEN, weight="bold", anchor="start")
    f.text(16, 180, "ㄷ ✗  프탈이미드 N–H(pKₐ ≈ 8.3)가 먼저 탈양성자화 → 1당량 소진, C=O 첨가 없음", size=12.5, anchor="start", weight="bold")
    m = Mol()
    phthalimide(m)
    f.mol(m, 60, 265)
    f.arrow(150, 265, 230, 265, "CH₃MgBr", "–CH₄")
    m = Mol()
    phthalimide(m, n_label="N^−")
    f.mol(m, 280, 265)
    f.text(372, 250, "MgBr⁺", size=11.5)
    f.arrow(395, 265, 460, 265, "H₃O⁺")
    m = Mol()
    phthalimide(m)
    f.mol(m, 510, 265)
    f.text(690, 255, "phthalimide 회수", size=12, color=RED, weight="bold")
    f.text(690, 277, "(보기의 2-acetylbenzamide ✗)", size=11.5, color=RED)
    return f.render()


# ---------------------------------------------------------------- 2008 14번
def salicylic(m, oh_label="OH"):
    benzene(m, "a", 0, 0, 90)
    c = m.sub("c", "a0", 90)
    m.sub("co", c, 30, "O", kind="2")
    m.sub("coh", c, 150, "HO", anchor="end")
    m.sub("po", "a1", 30, oh_label)
    return m


def f2008_14_mech():
    f = Fig(800, 330)
    f.text(16, 18, "친핵성 아실 치환(첨가–제거): 페놀 O의 공격 → 사면체 중간체 → Cl⁻ 이탈 → 피리딘이 H⁺ 제거", size=13, anchor="start", weight="bold")
    m = Mol()
    salicylic(m)
    f.mol(m, 70, 130)
    # 분자 내 수소 결합
    f.raw(f'<line x1="{70 + 31:.1f}" y1="{130 - 68:.1f}" x2="{70 + 47:.1f}" y2="{130 - 40:.1f}" stroke="{BLUE}" stroke-width="1.3" stroke-dasharray="3 3"/>')
    f.text(150, 58, "분자 내 H-결합", size=10.5, color=BLUE)
    # 아세틸 클로라이드
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("me", c, 210, "H_3C", anchor="end")
    m.sub("cl", c, -30, "Cl")
    f.mol(m, 215, 140)
    f.curly(135, 102, 207, 136, bend=-0.3)
    f.curly(215, 130, 217, 108, bend=0.6)
    f.arrow(265, 130, 320, 130)
    f.text(420, 115, "Ar–O^+(H)–C(O^−)(Cl)CH_3", size=12.5)
    f.text(420, 140, "사면체 중간체", size=11, color=GRAY)
    f.arrow(510, 130, 570, 130, "–Cl⁻", "py: –H⁺")
    m = Mol()
    benzene(m, "a", 0, 0, 90)
    c = m.sub("c", "a0", 90)
    m.sub("co", c, 30, "O", kind="2")
    m.sub("coh", c, 150, "HO", anchor="end")
    o = m.sub("po", "a1", -30, "O")
    ac = m.sub("ac", o, 30)
    m.sub("aco", ac, 90, "O", kind="2")
    m.sub("acm", ac, -30)
    f.mol(m, 640, 140)
    ok(f, 670, 205, "Aspirin (acetylsalicylic acid)")
    f.box(16, 230, 768, 90)
    f.text(28, 250, "수율이 낮은 이유", size=12.5, anchor="start", weight="bold", color=RED)
    f.text(28, 272, "① 페놀 O의 비공유쌍이 고리로 비편재화 → 친핵성 약함  ② o-COOH와 분자 내 수소 결합 + 입체 장애 → O의 반응성 더 감소", size=11.5, anchor="start")
    f.text(28, 294, "③ CH₃COCl이 수분과 가수분해·–COOH와 혼합 무수물 형성 등 부반응  ④ 생성 에스터(아스피린) 일부 가수분해, 분리·재결정 손실", size=11.5, anchor="start")
    return f.render()


def f2008_14_tyl():
    f = Fig(800, 170)
    m = Mol()
    benzene(m, "a", 0, 0, 0)
    m.sub("oh", "a3", 180, "HO", anchor="end")
    m.sub("n", "a0", 0, "NH_2", anchor="start")
    f.mol(m, 80, 85)
    f.arrow(170, 85, 280, 85, "CH₃COCl", "pyridine")
    m = Mol()
    benzene(m, "a", 0, 0, 0)
    m.sub("oh", "a3", 180, "HO", anchor="end")
    n = m.sub("n", "a0", 0, "N")
    m.sub("nh", n, 90, "H", length=22)
    c = m.sub("c", n, -30)
    m.sub("o", c, -90, "O", kind="2")
    m.sub("me", c, 30)
    f.mol(m, 380, 85)
    ok(f, 430, 150, "Tylenol = acetaminophen (N-(4-hydroxyphenyl)acetamide)")
    f.text(640, 60, "N(sp³ 아민)이 페놀 O보다", size=11.5)
    f.text(640, 80, "훨씬 강한 친핵체 → N-아실화", size=11.5, color=RED)
    return f.render()


# ---------------------------------------------------------------- 2003 18번
def f2003_18():
    f = Fig(800, 280)
    f.text(16, 18, "18-1. 나이트릴의 부분 가수분해 → 아마이드", size=13, anchor="start", weight="bold")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30, kind="2")
    c = m.sub("c", b, -30)
    m.sub("n", c, 0, "N", kind=3)
    f.mol(m, 60, 75)
    f.text(95, 105, "A = acrylonitrile", size=12, color=GREEN, weight="bold")
    f.arrow(170, 65, 280, 65, "H₂O (H⁺ 또는 OH⁻)", "부분 가수분해")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30, kind="2")
    c = m.sub("c", b, -30)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("n", c, -30, "NH_2")
    f.mol(m, 310, 75)
    f.text(360, 110, "acrylamide", size=12)
    f.text(470, 55, "CH₂=CH–C≡N + H₂O → CH₂=CH–CONH₂", size=12, anchor="start")
    f.text(470, 78, "(공업: Cu 촉매 수화·니트릴 하이드라테이스)", size=11, anchor="start", color=GRAY)
    f.text(16, 140, "18-2. 라디칼 첨가 중합 → polyacrylamide (삼량체 단위)", size=13, anchor="start", weight="bold")
    m = Mol()
    pts = []
    for i in range(6):
        x = i * 26
        y = 0 if i % 2 == 0 else -15
        m.atom(f"c{i}", x, y)
        if i:
            m.bond(f"c{i - 1}", f"c{i}")
    for i in (1, 3, 5):
        m.sub(f"k{i}", f"c{i}", 90, "CONH_2")
    m.atom("e1", -26, -15)
    m.bond("e1", "c0")
    m.atom("e2", 156, 0)
    m.bond("c5", "e2")
    f.mol(m, 305, 250)
    bracket(f, 285, 185, 262, left=True)
    bracket(f, 472, 185, 262, left=False, n=True)
    f.text(640, 215, "–[CH₂–CH(CONH₂)]₃– 반복", size=12)
    f.text(640, 237, "C=C π 결합이 열려 머리–꼬리 결합", size=11.5, color=GRAY)
    return f.render()


# ================================================================== 15. α탄소 치환반응
def f2010_37():
    f = Fig(800, 430)
    f.text(16, 18, "ㄱ ○  LDA(부피 큼, 저온) → 덜 치환된 α-C의 H 제거(속도론적 엔올레이트) → SN2 알킬화", size=12.5, anchor="start", weight="bold")
    m = Mol()
    cyhex_one(m)
    m.sub("me", "r5", 150)
    f.mol(m, 70, 95)
    f.arrow(135, 85, 205, 85, "LDA, −20 ℃")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90, arom=[0])
    m.sub("o", "r0", 90, "O^−")
    m.sub("me", "r5", 150)
    f.mol(m, 275, 95)
    f.text(275, 138, "덜 치환된 엔올레이트", size=11, color=GRAY)
    f.arrow(340, 85, 420, 85, "PhCH₂Br", "SN2")
    m = Mol()
    cyhex_one(m)
    m.sub("me", "r5", 150)
    ch = m.sub("ch", "r1", 30)
    m.sub("ph", ch, -30, "Ph")
    f.mol(m, 490, 95)
    ok(f, 690, 140, "2-benzyl-6-methylcyclohexanone")
    f.text(16, 160, "ㄴ ○  Michael 첨가(1,4) → 에스터 가수분해 → β-케토산 탈카복실(아세토아세트산 에스터 합성)", size=12.5, anchor="start", weight="bold")
    m = Mol()
    enone(m)
    f.mol(m, 60, 235)
    f.text(155, 183, "+ CH₃COCH₂CO₂Et", size=12)
    f.arrow(110, 225, 200, 225, "NaOEt", "H₃O⁺")
    m = Mol()
    cyhex_one(m)
    ch = m.sub("ch", "r2", -30, "CH(COCH_3)CO_2Et", anchor="start")
    f.mol(m, 240, 235)
    f.arrow(375, 225, 445, 225, "H₃O⁺, Δ", "–EtOH, –CO₂")
    m = Mol()
    cyhex_one(m)
    ch = m.sub("ch", "r2", -30)
    c = m.sub("c", ch, 30)
    m.sub("o", c, 90, "O", kind="2")
    m.sub("me", c, -30)
    f.mol(m, 490, 235)
    ok(f, 690, 280, "3-(2-oxopropyl)cyclohexanone")
    f.text(16, 300, "ㄷ ○  LDA 2당량 → 이음이온; 두 번째(덜 안정한) 탄소 음이온인 γ-CH₂⁻가 더 친핵성 → γ-알킬화", size=12.5, anchor="start", weight="bold")
    f.text(130, 370, "^−CH_2–C(O^−)=CH–CO_2CH_3", size=12.5)
    f.text(130, 393, "(α: 두 C=O 사이, 먼저 제거 · γ: 말단 CH₃)", size=10.5, color=GRAY)
    f.arrow(240, 365, 320, 365, "PhCH₂Cl", "H₂O")
    m = Mol()
    names = []
    for i in range(6):
        m.atom(f"c{i}", i * 26, 0 if i % 2 == 0 else -15)
        if i:
            m.bond(f"c{i - 1}", f"c{i}")
    m.label("c0", "Ph")
    m.sub("o3", "c3", 90, "O", kind="2")
    m.sub("o5", "c5", 90, "O", kind="2")
    m.sub("om", "c5", -30, "OCH_3")
    f.mol(m, 360, 385)
    ok(f, 660, 375, "methyl 3-oxo-5-phenylpentanoate")
    return f.render()


def f2003_16_1():
    f = Fig(800, 300)
    f.text(16, 18, "① I₂/KOH(= OI⁻, 산화제)가 2차 알코올 CH₃CH(OH)– 를 메틸 케톤으로 산화", size=13, anchor="start", weight="bold")
    f.text(95, 60, "CH_3CH(OH)CH_2CH_3", size=12.5)
    f.arrow(170, 60, 250, 60, "I₂, KOH", "산화")
    m = Mol()
    a = m.atom("a", 0, 0)
    c = m.sub("c", a, 30)
    m.sub("o", c, 90, "O", kind="2")
    d = m.sub("d", c, -30)
    m.sub("e", d, 30)
    f.mol(m, 285, 90)
    ok(f, 335, 118, "A = 2-butanone")
    f.text(16, 140, "② 할로폼 반응: α-CH₃ 3회 요오드화(엔올레이트 + I₂) → CI₃ 기 이탈 → B + CHI₃(노란 침전)", size=13, anchor="start", weight="bold")
    f.text(100, 190, "CH_3COCH_2CH_3", size=12.5)
    f.arrow(160, 190, 235, 190, "3 I₂, 3 OH⁻")
    f.text(295, 190, "I_3C–CO–CH_2CH_3", size=12.5)
    f.arrow(355, 190, 405, 190, "OH⁻")
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("o", c, 90, "O^−")
    m.sub("oh", c, 270, "OH")
    m.sub("ci", c, 180, "I_3C", anchor="end")
    m.sub("et", c, 0, "C_2H_5", anchor="start")
    f.mol(m, 470, 190)
    f.curly(478, 166, 478, 184, bend=-0.9)
    f.curly(456, 194, 440, 206, bend=-0.5)
    f.arrow(540, 190, 590, 190)
    f.text(690, 180, "C_2H_5COO^−K^+ + CHI_3↓", size=12.5, color=RED)
    ok(f, 690, 205, "B = propanoate (CH₃CH₂COO⁻)")
    f.text(400, 260, "I₃C⁻는 세 I의 유발 효과로 안정 → 이탈기 역할 → 빠른 H⁺ 이동으로 카복실레이트 + CHI₃ (산 처리 시 B = propanoic acid)", size=11.5, color=GRAY)
    return f.render()


# ================================================================== 16. 축합반응
def lactone(m, alpha="br"):
    m.ring("a", 0, 0, 6, L, 90)
    names, cen = poly_on_edge(m, "l", "a1", "a2", 5, (0, 0))
    # l1: O (a2 옆), l2: C=O, l3: Cα (a1 옆)
    m.label("l1", "O")
    m.sub("lo", "l2", 0, "O", kind="2")
    m.sub("h1", "a1", 90, "H", kind="w", length=22)
    m.sub("h2", "a2", -90, "H", kind="h", length=22)
    if alpha == "br":
        m.sub("br", "l3", 45, "Br", kind="w")
        m.sub("me", "l3", 110, kind="h")
    else:
        m.sub("ch2", "l3", 80, kind="2")
    return m


def f2013_36_gn():
    f = Fig(800, 330)
    f.text(16, 18, "ㄱ ○  C3a–H와 C–Br이 같은 면(syn) → 고리 H와 anti-주변평면 E2 불가 → CH₃의 H 제거 → exo-메틸렌", size=12.5, anchor="start", weight="bold")
    m = Mol()
    lactone(m, "br")
    f.mol(m, 80, 105)
    f.text(225, 135, "H(C3a)·Br 모두 쐐기 = syn", size=10.5, color=RED)
    f.arrow(185, 100, 265, 100, "NaOMe", "E2")
    m = Mol()
    lactone(m, "ene")
    f.mol(m, 340, 105)
    ok(f, 540, 90, "α-methylene-γ-butyrolactone")
    f.text(540, 112, "(CH₃는 자유 회전 → anti H 항상 가능)", size=11, color=GRAY)
    f.text(16, 190, "ㄴ ✗  Friedel–Crafts 알킬화: 2° 탄소 양이온 → 1,2-H 이동 → 3° 탄소 양이온 → 자리옮김 생성물", size=12.5, anchor="start", weight="bold")
    f.text(70, 235, "(CH_3)_2CH–C^+H–CH_3", size=12.5)
    f.text(70, 257, "2°", size=11, color=GRAY)
    f.arrow(135, 235, 205, 235, "~H⁻")
    f.text(275, 235, "(CH_3)_2C^+–CH_2CH_3", size=12.5)
    f.text(275, 257, "3° (더 안정)", size=11, color=GRAY)
    f.arrow(345, 235, 420, 235, "PhH", "–H⁺")
    m = Mol()
    benzene(m, "a", 0, 0, 0)
    q = m.sub("q", "a0", 0)
    m.sub("m1", q, 90)
    m.sub("m2", q, -90)
    e = m.sub("e", q, 0)
    m.sub("e2", e, -60)
    f.mol(m, 470, 245)
    f.text(610, 235, "(2-methylbutan-2-yl)benzene", size=12.5, color=GREEN, weight="bold", anchor="start")
    f.text(610, 258, "보기(3-methylbutan-2-yl 치환)는", size=11, color=RED, anchor="start")
    f.text(610, 276, "자리옮김 전 구조 ✗", size=11, color=RED, anchor="start")
    return f.render()


def f2013_36_d():
    f = Fig(800, 250)
    f.text(16, 18, "ㄷ ○  Robinson 고리 형성: Michael 첨가 → 분자 내 aldol → 탈수(E1cB)", size=13, anchor="start", weight="bold")
    m = Mol()
    m.ring("r", 0, 0, 5, R5, 90)
    m.sub("o", "r1", 18, "O", kind="2")
    m.sub("es", "r0", 150, "CO_2Et", anchor="end")
    f.mol(m, 80, 130)
    f.text(80, 190, "β-케토 에스터(주개)", size=11, color=GRAY)
    f.text(175, 85, "+ EVK (CH₂=CH–CO–CH₂CH₃)", size=11.5)
    f.arrow(140, 120, 215, 120, "NaOEt", "Michael")
    m = Mol()
    m.ring("r", 0, 0, 5, R5, 90)
    m.sub("o", "r1", 18, "O", kind="2")
    m.sub("es", "r0", 150, "CO_2Et", anchor="end")
    a = m.sub("a", "r0", 60)
    b = m.sub("b", a, 0)
    c = m.sub("c", b, 60)
    m.sub("co", c, 120, "O", kind="2")
    d = m.sub("d", c, 0)
    m.sub("e", d, -60)
    f.mol(m, 285, 150)
    f.raw(f'<circle cx="{285 + 15 + 30 + 15 + 30:.1f}" cy="{150 - 25.5 - 26 - 26:.1f}" r="9" fill="none" stroke="{RED}" stroke-width="1.3"/>')
    f.text(330, 205, "Michael 부가물: 표시한 CH₂(α′)의 엔올레이트가 고리 C=O 공격 → 6원 고리", size=10.5, color=RED)
    f.arrow(425, 120, 505, 120, "aldol", "–H₂O")
    m = Mol()
    m.ring("h", 0, 0, 6, L, 90, bonds=False)
    m.bond("h5", "h0", "in", (0, 0))
    m.bond("h0", "h1")
    m.bond("h1", "h2")
    m.bond("h2", "h3")
    m.bond("h3", "h4")
    m.bond("h4", "h5")
    poly_on_edge(m, "p", "h5", "h4", 5, (0, 0))
    m.sub("me", "h0", 90)
    m.sub("o", "h1", 30, "O", kind="2")
    m.sub("es", "h4", -90, "CO_2Et")
    f.mol(m, 600, 120)
    ok(f, 650, 210, "보기의 생성물과 일치 ✓")
    return f.render()


def f2005_11():
    f = Fig(800, 400)

    def donor(m, mode):
        m.ring("r", 0, 0, 6, L, 90, bonds=False)
        for a, b in [("r1", "r2"), ("r2", "r3"), ("r3", "r4"), ("r4", "r5"), ("r5", "r0")]:
            m.bond(a, b)
        m.sub("m1", "r5", 150, "H_3C", anchor="end")
        m.sub("m2", "r5", 210, "H_3C", anchor="end")
        c = m.sub("c", "r1", -30)
        m.sub("oe", c, -90, "OEt")
        if mode == "H":
            m.bond("r0", "r1")
            m.sub("o", "r0", 90, "O", kind="2")
            m.sub("h", "r1", 30, "H", length=22)
            m.set_bond("r1", "c", 1)
            m.sub("co", c, 30, "O", kind="2")
        elif mode == "carb":
            m.bond("r0", "r1")
            m.sub("o", "r0", 90, "O", kind="2")
            m.sub("co", c, 30, "O", kind="2")
        elif mode == "ketO":
            m.bond("r0", "r1", "in", (0, 0))
            m.sub("o", "r0", 90, "O^−")
            m.sub("co", c, 30, "O", kind="2")
        elif mode == "estO":
            m.bond("r0", "r1")
            m.set_bond("r1", "c", "2")
            m.sub("o", "r0", 90, "O", kind="2")
            m.sub("co", c, 30, "O^−")
        return m

    f.text(16, 18, "Michael 주개 = β-케토 에스터(두 C=O 사이 C–H, pKₐ ≈ 11) · 받개 = ethyl acrylate", size=13, anchor="start", weight="bold")
    m = Mol()
    donor(m, "H")
    f.mol(m, 110, 100)
    f.raw(f'<circle cx="{110 + 45}" cy="{100 - 26}" r="10" fill="none" stroke="{RED}" stroke-width="1.4"/>')
    f.arrow(200, 95, 270, 95, "EtO⁻", "–EtOH")
    f.text(420, 70, "첫 번째 중간체: 엔올레이트(안정화된 탄소 음이온)", size=12, color=RED, weight="bold")
    f.text(420, 95, "→ CH₂=CH–CO₂Et의 β-탄소 공격(1,4-첨가) → 에스터 엔올레이트", size=11.5)
    f.text(420, 117, "→ EtOH에서 양성자화 → (H₃O⁺ 처리) 최종 생성물", size=11.5)
    f.text(16, 160, "엔올레이트의 공명 기여 구조 (음전하: α-C, 케톤 O, 에스터 O)", size=13, anchor="start", weight="bold")
    for i, mode in enumerate(["carb", "ketO", "estO"]):
        m = Mol()
        donor(m, mode)
        x = 100 + i * 250
        f.mol(m, x, 240)
        if mode == "carb":
            f.charge(x + 26 + 6, 240 - 15 - 12, "−")
        if i < 2:
            f.resarrow(x + 95, x + 145, 235)
    f.text(16, 320, "최종 생성물", size=13, anchor="start", weight="bold")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.sub("o", "r0", 90, "O", kind="2")
    m.sub("m1", "r5", 150, "H_3C", anchor="end")
    m.sub("m2", "r5", 210, "H_3C", anchor="end")
    m.sub("c", "r1", -30, "CO_2Et", anchor="start")
    a = m.sub("a", "r1", 60)
    b = m.sub("b", a, 0)
    m.sub("d", b, 60, "CO_2Et", anchor="start")
    f.mol(m, 160, 360)
    ok(f, 480, 350, "ethyl 1-(3-ethoxy-3-oxopropyl)-3,3-dimethyl-2-oxocyclohexane-1-carboxylate")
    f.text(480, 372, "(C1이 사차 탄소가 됨; 가열하지 않으므로 탈카복실 없음)", size=11, color=GRAY)
    return f.render()
