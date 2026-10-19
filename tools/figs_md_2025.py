"""MDEET 2025 자연과학Ⅱ 유기화학 21–30번 그림"""
import math
from chemsvg import Mol, Fig, benzene, L, RED, BLUE, INK

GREEN = "#2f7d5b"
GRAY = "#6b7280"
R5 = L / (2 * math.sin(math.radians(36)))   # 오각형 외접원 반지름
R4 = L / math.sqrt(2)


def place(f, m, cx, cy, **kw):
    """분자의 원자 bbox 중심을 (cx, cy)에 놓고 오프셋을 돌려준다."""
    xs = [v[0] for v in m.a.values()]
    ys = [v[1] for v in m.a.values()]
    ox = cx - (min(xs) + max(xs)) / 2
    oy = cy - (min(ys) + max(ys)) / 2
    f.mol(m, ox, oy, **kw)
    return ox, oy


def P(m, n, o):
    x, y = m.pos(n)
    return x + o[0], y + o[1]


def mid(m, a, b, o, t=0.5):
    x1, y1 = P(m, a, o)
    x2, y2 = P(m, b, o)
    return x1 + (x2 - x1) * t, y1 + (y2 - y1) * t


def cpent(m, p="r", cx=0, cy=0, arom=None):
    return m.ring(p, cx, cy, 5, R5, 90, arom=arom)


def chex(m, p="r", cx=0, cy=0, arom=None):
    return m.ring(p, cx, cy, 6, L, 90, arom=arom)


# ------------------------------------------------------------------ 21
def f21():
    f = Fig(800, 250)
    cols = []
    # ① but-1-yne
    m = Mol(); m.atom("c1", 0, 0); m.sub("c2", "c1", 30, kind=3); m.sub("c3", "c2", 30); m.sub("c4", "c3", -30)
    cols.append((m, "But-3-yne", "but-1-yne", False, "C≡C 쪽부터 번호 → 1"))
    # ② 2-methylbut-1-ene
    m = Mol(); m.atom("c2", 0, 0); m.sub("c1", "c2", -30, kind="2"); m.sub("me", "c2", -150); m.sub("c3", "c2", 90); m.sub("c4", "c3", 150)
    cols.append((m, "2-Ethylpropene", "2-methylbut-1-ene", False, "가장 긴 사슬(C4)이 주사슬"))
    # ③ 3-methylbut-1-ene
    m = Mol(); m.atom("c3", 0, 0); m.sub("me", "c3", 90); m.sub("c4", "c3", -150); m.sub("c2", "c3", -30); m.sub("c1", "c2", 30, kind="2")
    cols.append((m, "3-Methylbut-1-ene", "3-methylbut-1-ene", True, "C=C에 1번, CH₃는 3번"))
    # ④ 1-methylcyclopentene
    m = Mol(); cpent(m, "r", arom=[0]); m.sub("me", "r1", 18)
    cols.append((m, "2-Methylcyclopentene", "1-methylcyclopentene", False, "C=C의 두 탄소가 C1·C2, 치환기에 1"))
    # ⑤ pent-1-en-3-yne
    m = Mol(); m.atom("c1", 0, 0); m.sub("c2", "c1", -30, kind="2"); m.sub("c3", "c2", 30); m.sub("c4", "c3", 30, kind=3); m.sub("c5", "c4", 30)
    cols.append((m, "Pent-3-yn-1-ene", "pent-1-en-3-yne", False, "접미사 순서 -en-…-yne"))
    for i, (m, given, right, ok, why) in enumerate(cols):
        cx = 80 + 160 * i
        f.text(cx, 22, "①②③④⑤"[i], size=16, weight="bold", color=GREEN if ok else INK)
        place(f, m, cx, 85)
        f.text(cx, 145, "제시: " + given, size=11, color=GRAY)
        f.text(cx, 168, right, size=13, weight="bold", color=GREEN if ok else BLUE)
        f.text(cx, 192, why, size=10.5)
        f.text(cx, 222, "○ 정답" if ok else "✗", size=15, weight="bold", color=GREEN if ok else RED)
    return f.render()


# ------------------------------------------------------------------ 22
def f22():
    f = Fig(800, 280)
    f.text(200, 18, "ㄷ. 아마이드 C–N의 부분 이중 결합 (공명)", size=13, weight="bold")
    m = Mol(); m.atom("c", 0, 0); o1 = m.sub("o", "c", 90, "O", kind="2"); m.sub("me", "c", -150); m.sub("n", "c", -30, "NH_2")
    o = place(f, m, 95, 110)
    nx, ny = P(m, "n", o)
    f.lp(nx + 1, ny - 11, 90)
    mx, my = mid(m, "c", "n", o)
    f.curly(nx + 4, ny - 15, mx + 2, my - 5, bend=0.9)
    cx, cy = mid(m, "c", "o", o)
    ox_, oy_ = P(m, "o", o)
    f.curly(cx - 4, cy + 2, ox_ - 9, oy_ + 2, bend=-0.7)
    f.resarrow(160, 205, 110)
    m = Mol(); m.atom("c", 0, 0); m.sub("o", "c", 90, "O"); m.sub("me", "c", -150); m.sub("n", "c", -30, "NH_2", kind="2")
    o = place(f, m, 270, 110)
    ox_, oy_ = P(m, "o", o)
    f.charge(ox_ + 13, oy_ - 6, "−")
    nx, ny = P(m, "n", o)
    f.charge(nx + 4, ny - 15, "+")
    f.text(200, 190, "C–N: 아민 1.47 Å  >  아마이드 1.35 Å", size=12.5, color=BLUE, weight="bold")
    f.text(200, 214, "N 비공유쌍의 비편재화 → C–N 결합 차수 > 1, 평면 N(sp²)", size=11.5)
    f.text(200, 236, "(C–N 회전 장벽 ≈ 18 kcal/mol)", size=11, color=GRAY)
    # 오른쪽: 혼성과 C–H 길이
    f.box(410, 10, 380, 258, fill="#f7f9fc")
    f.text(600, 30, "s 성격 ↑ → 혼성 궤도가 핵에 가까움 → 결합 짧음", size=12, weight="bold")
    rows = [("ㄱ", "C(sp²)–H 1.09 Å", ">", "C(sp)–H 1.06 Å", "○"),
            ("ㄴ", "C(sp²)–H 1.08 Å", "<", "C(sp³)–H 1.10 Å", "✗"),
            ("ㄷ", "C(sp³)–N 1.47 Å", ">", "C(O)–N 1.35 Å", "○")]
    for i, (k, a, s, b, v) in enumerate(rows):
        y = 75 + i * 52
        f.text(430, y, k, size=14, weight="bold", anchor="start")
        f.text(530, y, a, size=12.5)
        f.text(612, y, s, size=15, weight="bold", color=RED if v == "✗" else INK)
        f.text(695, y, b, size=12.5)
        f.text(772, y, v, size=15, weight="bold", color=GREEN if v == "○" else RED)
    f.text(600, 228, "s 성격: sp 50 % > sp² 33 % > sp³ 25 %", size=12)
    f.text(600, 250, "ㄴ은 부등호가 반대 (벤젠 C–H가 더 짧다)", size=11.5, color=RED)
    return f.render()


# ------------------------------------------------------------------ 23
def _proj(pts, e=20, rot=0):
    """3D 좌표 (x, y, z) → 화면 좌표. e: 고리 평면을 내려다보는 각도"""
    out = []
    for x, y, z in pts:
        r = math.radians(rot)
        x, y = x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r)
        ee = math.radians(e)
        out.append((x, -(y * math.sin(ee) + z * math.cos(ee))))
    return out


def f23():
    f = Fig(800, 300)
    def poly(pts, ox, oy, back=()):
        m = Mol()
        cx0 = (min(p[0] for p in pts) + max(p[0] for p in pts)) / 2
        cy0 = (min(p[1] for p in pts) + max(p[1] for p in pts)) / 2
        for i, (x, y) in enumerate(pts):
            m.atom(f"p{i}", x - cx0, y - cy0)
        n = len(pts)
        for i in range(n):
            j = (i + 1) % n
            m.bond(f"p{i}", f"p{j}", "dash" if (i, j) in back or (j, i) in back else 1)
        f.mol(m, ox, oy, lw=1.7)
    # A: 주름진 사이클로뷰테인 (3D 좌표 투영)
    poly([(0, 26), (52, 40), (92, 18), (44, -10)], 133, 88)
    f.cap(133, 30, "A 사이클로뷰테인")
    f.text(133, 140, "주름진(puckered) 구조, 접힘각 ≈ 25°", size=11.5)
    f.text(133, 162, "∠C–C–C ≈ 88°", size=12, color=BLUE, weight="bold")
    f.text(133, 184, "고리 스트레인 ≈ 26 kcal/mol", size=12, color=RED, weight="bold")
    f.text(133, 206, "평면이면 C–H 8쌍 모두 가려짐", size=11, color=GRAY)
    f.text(133, 224, "→ 접혀서 일부 엇갈림 (ㄱ ✗)", size=11, color=GRAY)
    # B: 봉투형 사이클로펜테인
    poly(_proj([(40 * math.cos(math.radians(72 * k + 180)), 40 * math.sin(math.radians(72 * k + 180)), 26 if k == 0 else 0) for k in range(5)], 22, 0), 400, 88)
    f.cap(400, 30, "B 사이클로펜테인")
    f.text(400, 140, "봉투형(envelope): C 1개가 평면 밖", size=11.5)
    f.text(400, 162, "∠C–C–C ≈ 104° (평균)", size=12, color=BLUE, weight="bold")
    f.text(400, 184, "고리 스트레인 ≈ 6 kcal/mol", size=12, color=RED, weight="bold")
    f.text(400, 206, "평면 오각형 108°보다도 작아짐", size=11, color=GRAY)
    f.text(400, 224, "(비틀림 줄이려 접힘)", size=11, color=GRAY)
    # C: 의자형 사이클로헥세인
    poly(_proj([(44 * math.cos(math.radians(60 * k)), 44 * math.sin(math.radians(60 * k)), 10 * (1 if k % 2 else -1)) for k in range(6)], 25, 0), 667, 88)
    f.cap(667, 30, "C 사이클로헥세인")
    f.text(667, 140, "의자형(chair): 모든 C–H 엇갈림", size=11.5)
    f.text(667, 162, "∠C–C–C ≈ 111°", size=12, color=BLUE, weight="bold")
    f.text(667, 184, "고리 스트레인 ≈ 0", size=12, color=RED, weight="bold")
    f.text(667, 206, "각·비틀림 스트레인 모두 거의 없음", size=11, color=GRAY)
    f.box(40, 244, 720, 46, fill="#f7f9fc")
    f.text(400, 258, "ㄱ ✗ (평면·가려짐 아님)    ㄴ ✗ (B 104° < C 111°)    ㄷ ○ (A 26 > C 0 kcal/mol)", size=12.5, weight="bold")
    f.text(400, 278, "고리 스트레인 = 각 스트레인 + 비틀림(가려짐) 스트레인 + 입체(트랜스고리) 스트레인", size=11)
    return f.render()


# ------------------------------------------------------------------ 24
def _mcp(m, oh_at=None, oh_kind="w", me_kind="w", p="r"):
    """3-methylcyclopentan-1-ol 골격: r0(CH₃), r2(오른쪽 아래) 또는 r3(왼쪽 아래)에 OH"""
    cpent(m, p)
    m.sub(p + "me", p + "0", 90, kind=me_kind)
    if oh_at == 2:
        m.sub(p + "oh", p + "2", -54, "OH", anchor="start", kind=oh_kind)
    elif oh_at == 3:
        m.sub(p + "oh", p + "3", 234, "HO", anchor="end", kind=oh_kind)
    return m


def f24():
    f = Fig(800, 330)
    # 출발물 4-methylcyclopentene
    m = Mol(); cpent(m, "r", arom=[2]); m.sub("me", "r0", 90)
    o = place(f, m, 60, 115)
    a, b = mid(m, "r2", "r3", o)
    f.curly(a + 4, b + 4, 104, 170, bend=0.35)
    f.text(130, 176, "H–OH₂^+", size=12)
    f.text(60, 200, "(비카이랄, 거울면 있음)", size=10.5, color=GRAY)
    f.arrow(120, 115, 185, 115, "H^+ 첨가", "(rds)")
    # 탄소 양이온
    m = Mol(); cpent(m, "r"); m.sub("me", "r0", 90, kind="w")
    o = place(f, m, 240, 115)
    x, y = P(m, "r2", o)
    f.charge(x + 11, y + 4, "+")
    f.text(240, 178, "2° 탄소 양이온 (평면 sp²)", size=11)
    f.text(240, 196, "+ 거울상 양이온 (1 : 1)", size=10.5, color=GRAY)
    # H2O 두 면 공격
    f.arrow(300, 100, 400, 65)
    f.text(345, 62, "H₂O: CH₃와 같은 면", size=11)
    f.arrow(300, 130, 400, 170)
    f.text(345, 175, "H₂O: 반대 면", size=11)
    m = _mcp(Mol(), 2, "w")
    place(f, m, 460, 60)
    f.text(530, 52, "→ (−H^+)  A: cis", size=12, anchor="start", color=BLUE, weight="bold")
    f.text(530, 72, "(1S,3R)-3-methylcyclopentan-1-ol", size=11.5, anchor="start")
    m = _mcp(Mol(), 2, "h")
    place(f, m, 460, 175)
    f.text(530, 167, "→ (−H^+)  B: trans", size=12, anchor="start", color=BLUE, weight="bold")
    f.text(530, 187, "(1R,3R)-3-methylcyclopentan-1-ol", size=11.5, anchor="start")
    f.box(20, 245, 760, 78, fill="#f7f9fc")
    f.text(400, 263, "거울상 양이온(CH₃ 점선)에서는 같은 방식으로 C: cis (1R,3S), D: trans (1S,3S)", size=12)
    f.text(400, 285, "비카이랄 출발물 + 비카이랄 시약 → 각 부분입체이성질체는 라셈 혼합물(A:C = 1:1, B:D = 1:1)", size=12)
    f.text(400, 307, "(1,2-H 이동으로 3° 양이온 → 1-methylcyclopentanol도 가능하나, 문제는 A~D를 주생성물로 제시)", size=10.5, color=GRAY)
    return f.render()


def f24b():
    f = Fig(800, 300)
    specs = [("A", 2, "w", "(1S,3R) cis", "그려지지 않은 것"), ("B", 2, "h", "(1R,3R) trans", ""),
             ("C", 3, "w", "(1R,3S) cis", ""), ("D", 3, "h", "(1S,3S) trans", "")]
    for i, (lab, at, k, cfg, note) in enumerate(specs):
        cx = 100 + 200 * i
        m = _mcp(Mol(), at, k)
        o = place(f, m, cx, 70)
        if lab in "BC":
            x, y = P(m, "r" + str(at), o)
            f.text(x + (-9 if at == 2 else 9), y - 9, "*", size=15, weight="bold")
        f.cap(cx, 130, lab)
        f.text(cx, 150, cfg, size=12, color=BLUE)
        if note:
            f.text(cx, 168, note, size=10.5, color=GRAY)
    # 관계 표시
    def bracket(x1, x2, y, txt, color):
        f.raw(f'<path d="M{x1},{y - 8} L{x1},{y} L{x2},{y} L{x2},{y - 8}" fill="none" stroke="{color}" stroke-width="1.4"/>')
        f.text((x1 + x2) / 2, y + 13, txt, size=11.5, color=color, weight="bold")
    bracket(100, 500, 190, "A ↔ C 거울상 (cis 쌍)", GREEN)
    bracket(300, 700, 230, "B ↔ D 거울상 (trans 쌍)", GREEN)
    f.text(400, 272, "ㄱ A(cis)–B(trans): 부분입체 ✗    ㄴ C(cis)–D(trans): 부분입체 ○    ㄷ B·C의 * 탄소 모두 R ○", size=12.5, weight="bold")
    f.text(400, 292, "* 탄소 우선순위: OH > CH₂(CHCH₃ 쪽) > CH₂(CH₂ 쪽) > H", size=11, color=GRAY)
    return f.render()


# ------------------------------------------------------------------ 25
def f25():
    f = Fig(800, 300)
    f.text(400, 16, "ㄷ. 짝염기의 공명 안정화: 음전하가 O로 가는가?", size=13, weight="bold")
    # 아세톤 엔올레이트
    m = Mol(); m.atom("c", 0, 0); m.sub("o", "c", 90, "O", kind="2"); m.sub("me", "c", -150); m.sub("a", "c", -30)
    o = place(f, m, 70, 80)
    ax, ay = P(m, "a", o)
    f.charge(ax + 10, ay + 6, "−")
    mx, my = mid(m, "c", "a", o)
    f.curly(ax + 2, ay - 8, mx + 2, my - 7, bend=0.7)
    cx, cy = mid(m, "c", "o", o)
    ox_, oy_ = P(m, "o", o)
    f.curly(cx + 4, cy, ox_ + 9, oy_ + 2, bend=0.6)
    f.resarrow(118, 158, 85)
    m = Mol(); m.atom("c", 0, 0); m.sub("o", "c", 90, "O"); m.sub("me", "c", -150); m.sub("a", "c", -30, kind="2")
    o = place(f, m, 205, 80)
    ox_, oy_ = P(m, "o", o)
    f.charge(ox_ + 13, oy_ - 4, "−")
    f.text(140, 140, "엔올레이트: 음전하가 전기음성 O에", size=11.5)
    f.text(140, 160, "acetone pKₐ ≈ 19–20", size=13, color=BLUE, weight="bold")
    f.text(400, 90, ">", size=26, weight="bold")
    # 아이소뷰틸렌 알릴 음이온
    m = Mol(); m.atom("c", 0, 0); m.sub("t", "c", 90, kind="2"); m.sub("me", "c", -150); m.sub("a", "c", -30)
    o = place(f, m, 530, 80)
    ax, ay = P(m, "a", o)
    f.charge(ax + 10, ay + 6, "−")
    mx, my = mid(m, "c", "a", o)
    f.curly(ax + 2, ay - 8, mx + 2, my - 7, bend=0.7)
    cx, cy = mid(m, "c", "t", o)
    tx, ty = P(m, "t", o)
    f.curly(cx + 4, cy, tx + 8, ty + 1, bend=0.6)
    f.resarrow(578, 618, 85)
    m = Mol(); m.atom("c", 0, 0); m.sub("t", "c", 90); m.sub("me", "c", -150); m.sub("a", "c", -30, kind="2")
    o = place(f, m, 665, 80)
    tx, ty = P(m, "t", o)
    f.charge(tx + 11, ty - 3, "−")
    f.text(600, 140, "알릴 음이온: 음전하가 탄소에만", size=11.5)
    f.text(600, 160, "isobutylene pKₐ ≈ 43", size=13, color=BLUE, weight="bold")
    f.box(20, 182, 760, 108, fill="#f7f9fc")
    f.text(40, 202, "ㄱ ○  1-propanol 97 °C > butane −0.5 °C : 몰질량 비슷(60 vs 58), O–H···O 수소 결합", size=12, anchor="start")
    f.text(40, 228, "ㄴ ○  diethyl ether ≈ 7 g/100 mL > pentane ≈ 0.004 g/100 mL : 에터 O가 H₂O의 수소 결합 받개", size=12, anchor="start")
    f.text(40, 254, "ㄷ ○  케톤 α-H(pKₐ ≈ 19) ≫ 알릴 H(pKₐ ≈ 43) : 두 경우 모두 공명하지만 O 위 음전하가 훨씬 안정", size=12, anchor="start")
    f.text(400, 278, "→ ⑤ ㄱ, ㄴ, ㄷ", size=13, weight="bold", color=GREEN)
    return f.render()


# ------------------------------------------------------------------ 26
def _orb(f, xs, y, phases, rx=8, ry=16, line=True):
    if line and len(xs) > 1:
        f.raw(f'<line x1="{xs[0]}" y1="{y}" x2="{xs[-1]}" y2="{y}" stroke="{INK}" stroke-width="2"/>')
    for x, ph in zip(xs, phases):
        f.porb(x, y, ph, rx=rx, ry=ry)


def _link(f, x, y1, y2, ok):
    c = GREEN if ok else RED
    f.raw(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{c}" stroke-width="2" stroke-dasharray="4 3"/>')
    f.text(x + (14 if ok else 14), (y1 + y2) / 2, "○" if ok else "✗", size=13, color=c, weight="bold", anchor="start")


def f26():
    f = Fig(800, 330)
    # 패널 1: 반응 1 광화학 [2+2]
    f.text(130, 18, "반응 1 (hν): B ··· B", size=13, weight="bold", color=GREEN)
    f.text(130, 40, "들뜬 에틸렌 SOMO(π*, B)", size=11)
    _orb(f, [100, 160], 85, [1, -1])
    _orb(f, [100, 160], 215, [-1, 1])
    _link(f, 100, 103, 197, True); _link(f, 160, 103, 197, True)
    f.text(130, 258, "바닥 상태 에틸렌 LUMO(π*, B)", size=11)
    f.text(130, 285, "양쪽 끝 모두 같은 위상 → 허용", size=11.5, color=GREEN)
    f.text(130, 305, "(B의 전체 부호는 임의로 뒤집어 그림)", size=10, color=GRAY)
    # 패널 2: 열적 [2+2] (비교)
    f.text(395, 18, "비교: 열적 [2+2] A ··· B", size=13, weight="bold", color=RED)
    f.text(395, 40, "에틸렌 HOMO(π, A)", size=11)
    _orb(f, [365, 425], 85, [1, 1])
    _orb(f, [365, 425], 215, [-1, 1])
    _link(f, 365, 103, 197, True); _link(f, 425, 103, 197, False)
    f.text(395, 258, "에틸렌 LUMO(π*, B)", size=11)
    f.text(395, 285, "한쪽 끝 반대 위상 → 금지", size=11.5, color=RED)
    f.text(395, 305, "(선지 ③의 A···B)", size=10, color=GRAY)
    # 패널 3: 반응 2 Diels–Alder
    f.text(655, 18, "반응 2 (Δ): D ··· B", size=13, weight="bold", color=GREEN)
    f.text(655, 40, "친다이엔체 LUMO(π*, B)", size=11)
    _orb(f, [610, 700], 85, [-1, 1])
    _orb(f, [610, 640, 670, 700], 215, [1, 1, -1, -1])
    _link(f, 610, 103, 197, True); _link(f, 700, 103, 197, True)
    f.text(655, 258, "다이엔 HOMO(ψ₂, D)", size=11)
    f.text(655, 285, "C1·C4 모두 같은 위상 → 허용", size=11.5, color=GREEN)
    f.text(655, 305, "(또는 LUMO_{diene} E ··· HOMO A)", size=10, color=GRAY)
    return f.render()


def f26b():
    f = Fig(800, 250)
    def level(x, y, lab, e, w=60):
        f.raw(f'<line x1="{x - w / 2}" y1="{y}" x2="{x + w / 2}" y2="{y}" stroke="{INK}" stroke-width="2"/>')
        f.text(x + w / 2 + 8, y, lab, size=12, anchor="start", weight="bold")
        if e:
            f.text(x, y - 11, e, size=17, color=BLUE, weight="bold")
    f.text(120, 18, "에틸렌 (바닥)", size=12, weight="bold")
    level(110, 70, "B (π*) LUMO", "")
    level(110, 170, "A (π) HOMO", "↑↓")
    f.text(330, 18, "에틸렌 (hν 들뜬)", size=12, weight="bold")
    level(320, 70, "B  SOMO₂", "↑")
    level(320, 170, "A  SOMO₁", "↑")
    f.arrow(232, 160, 262, 85, color=RED)
    f.text(235, 118, "hν", size=13, color=RED, anchor="end")
    f.text(620, 18, "뷰타-1,3-다이엔 (바닥)", size=12, weight="bold")
    level(600, 45, "F (ψ₄)", "")
    level(600, 95, "E (ψ₃) LUMO", "")
    level(600, 155, "D (ψ₂) HOMO", "↑↓")
    level(600, 205, "C (ψ₁)", "↑↓")
    f.text(400, 236, "마디 수: A 0 · B 1 / C 0 · D 1 · E 2 · F 3 — 마디가 많을수록 에너지 ↑", size=11.5)
    return f.render()


# ------------------------------------------------------------------ 27
def f27():
    f = Fig(800, 300)
    f.text(400, 16, "① 산 촉매 α-브로민화 = α-치환 반응 (환원 아님)", size=13, weight="bold")
    m = Mol(); cpent(m, "r"); m.sub("o", "r0", 90, "O", kind="2")
    place(f, m, 50, 95)
    f.eqarrow(88, 140, 95, "H^+", "엔올화(rds)")
    # 엔올 + Br2
    m = Mol(); cpent(m, "r", arom=[0]); m.sub("o", "r0", 90, "OH")
    o = place(f, m, 185, 95)
    ox_, oy_ = P(m, "o", o)
    f.lp(ox_ - 13, oy_, 180)
    f.curly(ox_ - 14, oy_ + 6, ox_ - 4, oy_ + 24, bend=0.6)
    a, b = mid(m, "r0", "r1", o, 0.5)
    bx, by = 252, 92
    f.text(bx, by, "Br", size=13); f.raw(f'<line x1="{bx + 10}" y1="{by}" x2="{bx + 30}" y2="{by}" stroke="{INK}" stroke-width="1.4"/>'); f.text(bx + 40, by, "Br", size=13)
    f.curly(a + 4, b - 3, bx - 10, by - 4, bend=-0.4)
    f.curly(bx + 18, by - 3, bx + 40, by - 10, bend=-0.9)
    f.arrow(310, 95, 355, 95)
    # 옥소카베늄
    m = Mol(); cpent(m, "r"); m.sub("o", "r0", 90, "OH^+", kind="2"); m.sub("br", "r1", 18, "Br")
    place(f, m, 405, 95)
    f.text(405, 150, "+ Br^−", size=11)
    f.arrow(462, 95, 520, 95, "−H^+")
    m = Mol(); cpent(m, "r"); m.sub("o", "r0", 90, "O", kind="2"); m.sub("br", "r1", 18, "Br")
    place(f, m, 575, 95)
    f.text(575, 150, "2-bromocyclopentanone", size=11)
    f.text(725, 80, "α-C 산화수", size=11.5, weight="bold")
    f.text(725, 100, "−2 → 0", size=13, color=RED, weight="bold")
    f.text(725, 120, "(오히려 산화)", size=11, color=RED)
    f.box(20, 172, 760, 120, fill="#f7f9fc")
    rows = ["① Br₂/AcOH: C–H → C–Br, α-치환(엔올 경유) → ‘환원’ 분류는 틀림 ✗ (정답)",
            "② CrO₃/H₂SO₄(Jones): 1° 알코올 → 알데하이드(수화물) → 카복실산 (산화 ○)",
            "③ 3° RBr + CH₃O⁻: E2, Zaitsev → 2-methylbut-2-ene (제거 ○)",
            "④ HBr: Markovnikov 첨가 → 2-bromohexane (첨가 ○)",
            "⑤ 2° RCl + CH₃S⁻(강한 친핵체, 약한 염기): SN2 → 티오에터 (치환 ○)"]
    for i, r in enumerate(rows):
        f.text(36, 192 + i * 22, r, size=12, anchor="start", color=RED if i == 0 else INK)
    return f.render()


# ------------------------------------------------------------------ 28
def f28():
    f = Fig(800, 230)
    f.text(400, 16, "① 벤자인(제거–첨가) 메커니즘", size=13, weight="bold")
    m = Mol(); benzene(m, "b", 0, 0, start=90); m.sub("cl", "b1", 30, "Cl"); m.sub("h", "b2", -30, "H")
    o = place(f, m, 70, 105)
    hx, hy = P(m, "h", o)
    f.text(hx + 30, hy + 22, "^−NH₂", size=12)
    f.curly(hx + 22, hy + 16, hx + 8, hy + 5, bend=0.4)
    f.arrow(140, 105, 210, 105, "① o-H 제거", "② Cl^− 이탈")
    # 벤자인
    m = Mol(); m.ring("b", 0, 0, 6, L, 90, arom=[1, 3, 5])
    o = place(f, m, 260, 105)
    x1, y1 = P(m, "b1", o); x2, y2 = P(m, "b2", o)
    f.raw(f'<line x1="{x1 + 5.5:.1f}" y1="{y1 + 3:.1f}" x2="{x2 + 5.5:.1f}" y2="{y2 - 3:.1f}" stroke="{INK}" stroke-width="1.4"/>')
    f.text(260, 160, "벤자인 (변형된 π 결합)", size=11)
    f.text(330, 72, "^−NH₂", size=12)
    f.curly(322, 80, x1 + 9, y1 + 2, bend=0.3)
    f.arrow(320, 105, 390, 105, "NH₂^− 첨가", "NH₃가 H^+ 공급")
    m = Mol(); benzene(m, "b", 0, 0, start=90); m.sub("n", "b1", 30, "NH_2")
    place(f, m, 445, 105)
    f.text(445, 160, "aniline (○ 정답)", size=12, weight="bold", color=GREEN)
    f.box(530, 40, 260, 130, fill="#f7f9fc")
    f.text(660, 60, "조건과 특징", size=12, weight="bold")
    f.text(545, 84, "· 활성화기 없는 ArX + 매우 강한 염기", size=11, anchor="start")
    f.text(545, 106, "· o-H 산도가 Cl의 −I로 증가", size=11, anchor="start")
    f.text(545, 128, "· ¹⁴C 표지 시 ipso:ortho ≈ 1:1", size=11, anchor="start")
    f.text(545, 150, "· 클로로벤젠은 대칭 → 한 생성물", size=11, anchor="start")
    f.text(400, 205, "③ 아실기는 m-지향 · ④ 1° 양이온 → 3° 자리옮김 · ⑤ CH₃(o,p)·NO₂(m) 모두 CH₃의 ortho 지시", size=11.5, color=GRAY)
    return f.render()


def f28b():
    f = Fig(800, 250)
    f.text(400, 16, "선지 ②–⑤의 실제 주생성물", size=13, weight="bold")
    # ② 4-nitrophenol
    m = Mol(); benzene(m, "b", 0, 0, start=90); m.sub("oh", "b1", 30, "OH"); m.sub("n", "b4", 210, "O_2N", anchor="end")
    place(f, m, 100, 100)
    f.text(100, 165, "② 4-nitrophenol", size=12, weight="bold", color=BLUE)
    f.text(100, 185, "SNAr: ipso 치환", size=11)
    f.text(100, 203, "(Meisenheimer 착물 경유)", size=10.5, color=GRAY)
    # ③ 3-nitropropiophenone
    m = Mol(); benzene(m, "b", 0, 0, start=90); c = m.sub("c", "b5", 150); m.sub("o", c, 210, "O", kind="2"); e1 = m.sub("e1", c, 90); m.sub("e2", e1, 150)
    m.sub("n", "b2", -30, "NO_2", anchor="start")
    place(f, m, 300, 95)
    f.text(300, 165, "③ m-nitro 생성물", size=12, weight="bold", color=BLUE)
    f.text(300, 185, "C=O(−M): meta 지향", size=11)
    # ④ tert-butylbenzene
    m = Mol(); benzene(m, "b", 0, 0, start=90); q = m.sub("q", "b1", 30); m.sub("m1", q, 90); m.sub("m2", q, -30); m.sub("m3", q, 30)
    place(f, m, 500, 100)
    f.text(500, 165, "④ tert-butylbenzene", size=12, weight="bold", color=BLUE)
    f.text(500, 185, "1° → 3° 양이온(1,2-H 이동)", size=11)
    # ⑤ 2-bromo-4-nitrotoluene
    m = Mol(); benzene(m, "b", 0, 0, start=90); m.sub("me", "b1", 30); m.sub("br", "b0", 90, "Br"); m.sub("n", "b4", 210, "O_2N", anchor="end")
    place(f, m, 700, 100)
    f.text(700, 165, "⑤ 2-bromo-4-nitrotoluene", size=12, weight="bold", color=BLUE)
    f.text(700, 185, "Br은 CH₃의 ortho", size=11)
    f.text(700, 203, "(NO₂의 meta와 일치)", size=10.5, color=GRAY)
    f.text(400, 235, "제시된 ②(cine 치환형)·③(para)·④(이소뷰틸)·⑤(NO₂의 ortho)는 모두 틀림", size=11.5, color=RED)
    return f.render()


# ------------------------------------------------------------------ 29
def f29():
    f = Fig(800, 330)
    # A
    m = Mol(); chex(m, "r", arom=[1]); m.sub("me", "r1", 30)
    place(f, m, 60, 150)
    f.cap(60, 205, "A")
    f.arrow(110, 130, 220, 70)
    f.text(70, 52, "1. BH₃·THF", size=11, anchor="start")
    f.text(70, 70, "2. H₂O₂, NaOH", size=11, anchor="start")
    f.arrow(110, 170, 220, 230)
    f.text(90, 255, "1. Hg(OAc)₂, H₂O", size=11, anchor="start")
    f.text(90, 273, "2. NaBH₄", size=11, anchor="start")
    # C
    m = Mol(); chex(m, "r"); m.sub("me", "r1", 30, kind="w"); m.sub("oh", "r2", -30, "OH", kind="h")
    place(f, m, 280, 65)
    f.text(345, 40, "C: trans-2-methylcyclohexanol", size=12, anchor="start", weight="bold", color=BLUE)
    f.text(345, 60, "(라셈) 역-Markovnikov, syn 첨가", size=11, anchor="start")
    f.text(345, 80, "→ CH₃와 OH는 trans", size=11, anchor="start")
    f.text(345, 100, "ㄴ 구조(쐐기·쐐기 = cis) ✗", size=11, anchor="start", color=RED)
    # D
    m = Mol(); chex(m, "r"); m.sub("me", "r1", 60); m.sub("oh", "r1", 0, "OH")
    place(f, m, 280, 245)
    f.text(345, 235, "D: 1-methylcyclohexanol", size=12, anchor="start", weight="bold", color=BLUE)
    f.text(345, 255, "Markovnikov, 자리옮김 없음", size=11, anchor="start")
    f.text(345, 275, "(3° C에 OH)", size=11, anchor="start")
    # B 쪽
    f.box(560, 110, 230, 210, fill="#f7f9fc")
    m = Mol(); chex(m, "r"); m.sub("ch2", "r1", 30, kind="2")
    place(f, m, 620, 155)
    f.text(675, 140, "B = methylene-", size=11.5, anchor="start", weight="bold")
    f.text(675, 158, "cyclohexane (ㄱ ○)", size=11.5, anchor="start", weight="bold")
    f.text(675, 182, "수소붕소화 → E", size=11, anchor="start")
    f.text(675, 200, "(CH₂OH: 역-Mark.)", size=11, anchor="start")
    f.text(675, 230, "옥시수은화 → F", size=11, anchor="start")
    f.text(675, 248, "= 1-methyl-", size=11, anchor="start")
    f.text(675, 266, "cyclohexanol", size=11, anchor="start")
    f.text(675, 292, "D = F (ㄷ ○)", size=12.5, anchor="start", weight="bold", color=GREEN)
    f.text(620, 230, "E·F 모두", size=10.5, color=GRAY)
    f.text(620, 248, "C₇H₁₄O", size=10.5, color=GRAY)
    return f.render()


def f29b():
    """수소붕소화의 4중심 전이 상태 (syn 첨가)"""
    f = Fig(800, 220)
    f.text(400, 16, "수소붕소화: 4중심 협동 전이 상태 → H와 BR₂가 같은 면(syn)으로 첨가", size=13, weight="bold")
    m = Mol(); chex(m, "r", arom=[1]); m.sub("me", "r1", 30)
    o = place(f, m, 80, 115)
    a, b = mid(m, "r1", "r2", o)
    f.text(150, 75, "H–BH₂", size=12)
    f.curly(a + 5, b, 145, 85, bend=0.4)
    f.arrow(190, 115, 250, 115)
    # TS
    m = Mol(); chex(m, "r"); m.sub("me", "r1", 30)
    m.atom("B", 0, 0, "BH_2"); m.atom("H", 0, 0, "H")
    x1, y1 = m.pos("r1"); x2, y2 = m.pos("r2")
    m.a["H"][0], m.a["H"][1] = x1 + 30, y1 + 4
    m.a["B"][0], m.a["B"][1] = x2 + 32, y2 + 2
    m.bond("r1", "H", "form"); m.bond("r2", "B", "form"); m.bond("H", "B", "dash")
    m.set_bond("r1", "r2", "dash")
    place(f, m, 320, 115)
    f.text(320, 175, "4중심 TS (‡)", size=11.5)
    f.arrow(385, 115, 445, 115)
    m = Mol(); chex(m, "r"); m.sub("me", "r1", 30, kind="w"); m.sub("h", "r1", 90, "H", kind="h"); m.sub("bb", "r2", -30, "BR_2", anchor="start", kind="h"); m.sub("hh", "r2", -90, "H", kind="w")
    place(f, m, 495, 110)
    f.text(495, 185, "H·B 같은 면(뒤) → CH₃(앞)와 trans", size=11)
    f.arrow(585, 115, 655, 115, "H₂O₂, OH^−")
    f.text(620, 140, "배열 유지", size=10.5)
    m = Mol(); chex(m, "r"); m.sub("me", "r1", 30, kind="w"); m.sub("oh", "r2", -30, "OH", kind="h")
    place(f, m, 715, 110)
    f.text(715, 180, "C (+ 거울상)", size=11.5, weight="bold", color=BLUE)
    return f.render()


# ------------------------------------------------------------------ 30
def _eaa(m, alpha_label=None):
    m.atom("me", 0, 0)
    k = m.sub("k", "me", 30); m.sub("ko", k, 90, "O", kind="2")
    a = m.sub("a", k, -30, alpha_label)
    e = m.sub("e", a, 30); m.sub("eo", e, 90, "O", kind="2")
    m.sub("oe", e, -30, "OEt", anchor="start")
    return m


def f30():
    f = Fig(800, 330)
    f.text(400, 16, "아세토아세트산 에스터 합성: 이중 알킬화 → 고리화(4원 고리) → 가수분해·탈카복실화", size=12.5, weight="bold")
    m = _eaa(Mol())
    place(f, m, 60, 75)
    f.arrow(145, 75, 195, 75, "NaOEt", "(pKₐ ≈ 11)")
    m = _eaa(Mol())
    o = place(f, m, 262, 75)
    x, y = P(m, "a", o)
    f.charge(x, y + 13, "−")
    f.text(262, 132, "엔올레이트(공명 안정)", size=10.5, color=GRAY)
    f.arrow(345, 75, 410, 75, "Br(CH₂)₃Br", "S_N2 (분자 간)")
    m = _eaa(Mol())
    x1 = m.sub("x1", "a", -90); x2 = m.sub("x2", x1, -30); x3 = m.sub("x3", x2, -90); m.sub("br", x3, -30, "Br")
    place(f, m, 480, 95)
    f.text(565, 70, "2차 NaOEt", size=11.5, anchor="start")
    f.text(565, 88, "→ 남은 α-H 제거", size=11.5, anchor="start")
    f.text(565, 106, "→ 분자 내 S_N2", size=11.5, anchor="start")
    f.text(565, 124, "(4-exo-tet 고리화)", size=10.5, anchor="start", color=GRAY)
    # 2행: 분자 내 SN2
    m = _eaa(Mol())
    x1 = m.sub("x1", "a", -90); x2 = m.sub("x2", x1, -150); x3 = m.sub("x3", x2, 90); br = m.sub("br", x3, 210, "Br")
    o = place(f, m, 110, 250)
    ax, ay = P(m, "a", o)
    f.charge(ax + 12, ay + 10, "−")
    x3x, x3y = P(m, "x3", o)
    f.curly(ax - 4, ay + 2, x3x + 4, x3y - 2, bend=0.5)
    bx, by = P(m, "br", o)
    f.curly((x3x + bx) / 2 + 2, (x3y + by) / 2 + 4, bx + 2, by + 14, bend=-0.9)
    f.arrow(205, 245, 250, 245, "−Br^−")
    # 고리화 생성물
    m = Mol(); m.ring("cb", 0, 0, 4, R4, 90)
    kc = m.sub("kc", "cb0", 150); m.sub("ko", kc, 90, "O", kind="2"); m.sub("km", kc, 210)
    ec = m.sub("ec", "cb0", 30); m.sub("eo", ec, 90, "O", kind="2"); m.sub("oe", ec, -30, "OEt", anchor="start")
    place(f, m, 320, 245)
    f.text(320, 300, "ethyl 1-acetylcyclobutane-", size=10.5)
    f.text(320, 316, "1-carboxylate", size=10.5)
    f.arrow(408, 245, 478, 245, "H₃O^+, 가열", "가수분해 → −CO₂")
    m = Mol(); m.ring("cb", 0, 0, 4, R4, 90)
    kc = m.sub("kc", "cb0", 90); m.sub("ko", kc, 30, "O", kind="2"); m.sub("km", kc, 150)
    place(f, m, 535, 240)
    f.text(535, 300, "A: cyclobutyl methyl ketone", size=12, weight="bold", color=GREEN)
    f.text(535, 316, "(1-cyclobutylethan-1-one, ④)", size=10.5)
    f.box(610, 160, 180, 120, fill="#f7f9fc")
    f.text(700, 180, "고리 크기 = 알킬 사슬 C3", size=11)
    f.text(700, 198, "+ α-탄소 1 = 4원 고리", size=11)
    f.text(700, 222, "CH₃CO– 남음 → 케톤", size=11)
    f.text(700, 240, "(말론산 에스터였다면", size=10.5, color=GRAY)
    f.text(700, 258, "카복실산 ⑤)", size=10.5, color=GRAY)
    return f.render()


def f30b():
    f = Fig(800, 210)
    f.text(400, 16, "β-케토산의 탈카복실화: 6원 고리 협동 전이 상태 → 엔올 → 케톤", size=13, weight="bold")
    m = Mol(); m.ring("cb", 0, 0, 4, R4, 90)
    kc = m.sub("kc", "cb0", 150); ko = m.sub("ko", kc, 90, "O", kind="2"); m.sub("km", kc, 210)
    ec = m.sub("ec", "cb0", 30); eo2 = m.sub("eo2", ec, 90, "O"); m.sub("eo1", ec, -30, "O", kind="2")
    x, y = m.pos("cb0")
    m.atom("h", x, y - 2 * L - 8, "H")
    m.bond("eo2", "h"); m.bond("h", "ko", "dash")
    o = place(f, m, 110, 115)
    kox, koy = P(m, "ko", o); hx, hy = P(m, "h", o)
    a, b = mid(m, "kc", "ko", o)
    f.curly(a - 5, b, hx - 7, hy - 5, bend=0.5)
    a, b = mid(m, "eo2", "h", o)
    c, d = mid(m, "eo2", "ec", o)
    f.curly(a + 5, b - 3, c + 6, d, bend=0.7)
    a, b = mid(m, "cb0", "ec", o)
    c, d = mid(m, "cb0", "kc", o)
    f.curly(a, b + 5, c, d + 5, bend=0.7)
    f.text(110, 185, "β-케토산 (6원 고리 TS)", size=11)
    f.arrow(200, 110, 280, 110, "−CO₂", "")
    m = Mol(); m.ring("cb", 0, 0, 4, R4, 90)
    kc = m.sub("kc", "cb0", 90, kind="2"); m.sub("ko", kc, 30, "OH"); m.sub("km", kc, 150)
    place(f, m, 340, 110)
    f.text(340, 175, "엔올", size=11)
    f.eqarrow(395, 455, 110, "토토머화")
    m = Mol(); m.ring("cb", 0, 0, 4, R4, 90)
    kc = m.sub("kc", "cb0", 90); m.sub("ko", kc, 30, "O", kind="2"); m.sub("km", kc, 150)
    place(f, m, 510, 110)
    f.text(510, 175, "A (케토형 우세)", size=11.5, weight="bold", color=GREEN)
    f.box(590, 50, 200, 110, fill="#f7f9fc")
    f.text(690, 70, "조건", size=11.5, weight="bold")
    f.text(690, 92, "C=O가 카복실기의 β 위치", size=11)
    f.text(690, 112, "→ 6원 고리 TS 가능", size=11)
    f.text(690, 136, "단순 카복실산은", size=11, color=GRAY)
    f.text(690, 152, "가열해도 탈카복실 ✗", size=11, color=GRAY)
    return f.render()
