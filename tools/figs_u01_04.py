"""1 결합과 구조 · 2 산과 염기 · 3 알케인과 사이클로알케인 · 4 입체화학 문항 그림"""
import math
from chemsvg import Mol, Fig, benzene, L, RED, BLUE, INK, rich

GREEN = "#2f7d5b"
GRAY = "#5b6270"
ORANGE = "#d97706"


# ------------------------------------------------------------------ 공용 헬퍼
def line(f, x1, y1, x2, y2, color=INK, w=1.4, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    f.raw(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{w}"{d} stroke-linecap="round"/>')


def newman(f, x, y, front, back, r=20, ln=42, size=12, hl=None):
    """뉴먼 투영. front: 90°, 210°, 330° 방향 라벨 / back: 30°, 150°, 270° 방향 라벨.
    hl: 강조할 라벨 목록(빨강)."""
    hl = hl or []
    f.raw(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="1.4"/>')

    def put(ang, lab, frm):
        a = math.radians(ang)
        c, s = math.cos(a), -math.sin(a)
        x1, y1 = x + frm * c, y + frm * s
        x2, y2 = x + (ln - 10) * c, y + (ln - 10) * s
        line(f, x1, y1, x2, y2)
        anc = "start" if c > 0.3 else ("end" if c < -0.3 else "middle")
        lx = x + ln * c + (-6 if anc == "start" else 6 if anc == "end" else 0)
        ly = y + ln * s + (0 if anc != "middle" else (-2 if s < 0 else 2))
        f.add(rich(lx, ly, lab, size=size, anchor=anc, color=RED if lab in hl else INK, halo=True))

    for ang, lab in zip((30, 150, 270), back):
        put(ang, lab, r)
    for ang, lab in zip((90, 210, 330), front):
        put(ang, lab, 0)
    f.raw(f'<circle cx="{x}" cy="{y}" r="2" fill="{INK}"/>')


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


def numline(f, x0, x1, y, lo, hi, marks, title=None, step=None):
    """pKₐ 수직선. marks: [(값, 라벨, 위(True)/아래)]"""
    sx = lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)
    f.arrow(x0 - 5, y, x1 + 12, y)
    if step:
        v = lo
        while v <= hi + 1e-9:
            line(f, sx(v), y - 4, sx(v), y + 4, color=GRAY, w=1)
            f.text(sx(v), y + 14, f"{v:g}", size=9.5, color=GRAY)
            v += step
    if title:
        f.text(x0 - 12, y, title, size=12, anchor="end", weight="bold")
    for v, lab, top, *col in marks:
        c = col[0] if col else BLUE
        f.raw(f'<circle cx="{sx(v):.1f}" cy="{y}" r="4" fill="{c}"/>')
        if top:
            line(f, sx(v), y - 5, sx(v), y - 16, color=c, w=1)
            f.text(sx(v), y - 25, lab, size=11, color=c)
        else:
            line(f, sx(v), y + 5, sx(v), y + 22, color=c, w=1)
            f.text(sx(v), y + 32, lab, size=11, color=c)
    return sx


def pyrrole_like(m, p, cx, cy, start=90, r=None):
    """오각 고리 원자 p0..p4 (결합은 호출자가 지정)"""
    r = r or L / (2 * math.sin(math.radians(36)))
    return m.ring(p, cx, cy, 5, r, start, bonds=False)


def ring_bonds(m, p, n, dbl, c):
    for i in range(n):
        a, b = f"{p}{i}", f"{p}{(i + 1) % n}"
        m.bond(a, b, "in", c) if i in dbl else m.bond(a, b)


# ================================================================== 단원 1
def f2012_35():
    """히스타민의 세 N 혼성과 비공유 전자쌍 궤도"""
    f = Fig(800, 270)
    m = Mol()
    # 오각 고리: r0=C4(측쇄), r1=C5, r2=N1(H), r3=C2, r4=N3
    pyrrole_like(m, "r", 0, 0, 126)
    ring_bonds(m, "r", 5, [0, 3], (0, 0))
    m.label("r2", "N")
    m.label("r4", "N")
    m.sub("h", "r2", -18, "H")
    a = m.sub("c1", "r0", 90)
    b = m.sub("c2", a, 150)
    m.sub("n", b, 90, "H_2N", anchor="end")
    f.mol(m, 170, 150)
    # 라벨
    nx, ny = m.pos("n")
    f.text(170 + nx + 20, 150 + ny - 2, "(가) sp³", size=13, anchor="start", color=RED, weight="bold")
    f.lp(170 + nx - 4, 150 + ny - 12, 0)
    x4, y4 = m.pos("r4")
    f.text(170 + x4 - 24, 150 + y4 + 2, "(나) sp²", size=13, anchor="end", color=RED, weight="bold")
    f.lp(170 + x4 - 9, 150 + y4 + 1, 90)
    x2, y2 = m.pos("r2")
    f.text(170 + x2 + 4, 150 + y2 + 26, "(다) sp²", size=13, anchor="middle", color=RED, weight="bold")
    f.lp(170 + x2 + 1, 150 + y2 - 10, 0)
    f.text(160, 250, "histamine", size=12, color=GRAY)
    # 오른쪽 설명 상자
    f.box(330, 14, 455, 242, fill="#f7f9fc")
    f.text(345, 34, "비공유 전자쌍이 든 궤도로 혼성 판단", size=12.5, anchor="start", weight="bold")
    rows = [
        ("(가) 1차 아민 N", "σ 결합 3 + 비공유쌍 1 = 입체수 4 → sp³ (피라미드형)"),
        ("(나) 피리딘형 =N–", "σ 2 + 비공유쌍 1 = 3 → sp², 비공유쌍은 sp² (고리 면 안)"),
        ("", "→ 방향족 6π에 불참, 염기 자리(짝산 pKₐ ≈ 7)"),
        ("(다) 피롤형 N–H", "σ 3 + 비공유쌍(p 궤도) → sp²"),
        ("", "→ 비공유쌍이 6π 방향족 고리에 참여 (평면)"),
    ]
    yy = 62
    for a, b in rows:
        if a:
            f.text(345, yy, a, size=12, anchor="start", color=RED, weight="bold")
        f.text(470 if a else 470, yy, b, size=11.5, anchor="start")
        yy += 24
    # 궤도 모식도: 오각 고리 옆모습
    y0 = 206
    for i in range(5):
        cx = 380 + i * 26
        f.porb(cx, y0, 1, rx=6, ry=12)
    line(f, 372, y0, 488, y0, w=2)
    f.text(430, y0 + 38, "고리 p 궤도 5개 + 전자 6개", size=11)
    f.text(430, y0 + 52, "(C 3개 × 1, N(나) 1, N(다) 2)", size=10.5, color=GRAY)
    f.raw(f'<ellipse cx="{530}" cy="{y0}" rx="18" ry="7" fill="#f0c36d" stroke="{INK}"/>')
    f.text(560, y0 - 12, "N(나)의 sp² 비공유쌍:", size=11, anchor="start")
    f.text(560, y0 + 6, "고리 면 안 → π계와 직교(염기성)", size=11, anchor="start")
    return f.render()


def _anthracene(m, p, x0, y0):
    """안트라센 14개 원자 좌표(세로 변을 가진 육각형 3개). 반환: 이름 목록, 결합 목록, 고리 중심"""
    w = 2 * L * math.cos(math.radians(30))
    names, pos = {}, {}
    rings = []
    for j in range(3):
        cx = x0 + j * w
        ids = []
        for i in range(6):
            ang = math.radians(90 - 60 * i)
            x, y = cx + L * math.cos(ang), y0 - L * math.sin(ang)
            key = (round(x, 1), round(y, 1))
            if key not in pos:
                nm = f"{p}{len(pos)}"
                pos[key] = nm
                m.atom(nm, x, y)
            ids.append(pos[key])
        rings.append((ids, (cx, y0)))
    bonds = {}
    for ids, c in rings:
        for i in range(6):
            e = frozenset((ids[i], ids[(i + 1) % 6]))
            bonds.setdefault(e, c)
    return list(pos.values()), bonds, rings


def _kekule(atoms, bonds):
    """완전 짝지음(케쿨레 구조) 전부"""
    out = []
    edges = list(bonds)

    def rec(left, chosen):
        if not left:
            out.append(list(chosen))
            return
        a = left[0]
        for e in edges:
            if a in e:
                b = next(iter(e - {a}))
                if b in left:
                    rec([x for x in left if x not in (a, b)], chosen + [e])
    rec(list(atoms), [])
    return out


def anthracene_bond_names(p="a"):
    m = Mol()
    atoms, bonds, rings = _anthracene(m, p, 0, 0)
    L_ids = rings[0][0]   # 왼쪽 고리: 0 위, 1 오른위(C9a), 2 오른아래(C4a), 3 아래, 4 왼아래, 5 왼위
    M_ids = rings[1][0]   # 가운데 고리: 0 위(C9)
    return {
        "a": frozenset((L_ids[4], L_ids[5])),   # C2–C3
        "b": frozenset((L_ids[5], L_ids[0])),   # C1–C2
        "c": frozenset((L_ids[0], L_ids[1])),   # C1–C9a
        "d": frozenset((L_ids[1], M_ids[0])),   # C9a–C9
        "e": frozenset((L_ids[1], L_ids[2])),   # C9a–C4a
    }


def f2009_21():
    f = Fig(800, 340)
    m0 = Mol()
    atoms, bonds, rings = _anthracene(m0, "a", 0, 0)
    ks = _kekule(atoms, bonds)
    names = anthracene_bond_names("a")
    xs = [45, 240, 435, 630]
    for i, dbl in enumerate(ks):
        m = Mol()
        atoms, bonds, rings = _anthracene(m, "a", 0, 0)
        for e, c in bonds.items():
            a, b = tuple(e)
            if e in dbl:
                m.bond(a, b, "in", c)
            else:
                m.bond(a, b)
        f.mol(m, xs[i], 75, scale=0.85)
        f.text(xs[i] + 56, 135, f"({i + 1})", size=12)
    # 첫 구조에 결합 이름 표시 (좌표 × 0.85)
    w = 2 * L * math.cos(math.radians(30))
    sc = 0.85
    lab_pos = {"a": (-w / 2 - 12, 0), "b": (-w / 4 - 8, -L * 0.75 - 9), "c": (w / 4 + 2, -L * 0.75 - 11),
               "d": (3 * w / 4 + 6, -L * 0.75 - 11), "e": (w / 2 - 10, 0)}
    for k, (dx, dy) in lab_pos.items():
        f.text(xs[0] + sc * dx, 75 + sc * dy, k, size=13, color=RED if k == "b" else BLUE, weight="bold", italic=True)
    cnt = {k: sum(1 for d in ks if e in d) for k, e in names.items()}
    x0, y0 = 90, 170
    heads = ["결합", "위치", "이중 결합인 구조 수", "Pauling 결합 차수", "실측 길이(Å)"]
    pos = ["C2–C3", "C1–C2", "C1–C9a", "C9–C9a", "C4a–C9a"]
    exp = ["1.42", "1.37", "1.43", "1.40", "1.44"]
    cw = [60, 90, 160, 150, 120]
    xx = x0
    for h, wd in zip(heads, cw):
        f.text(xx + wd / 2, y0, h, size=12, weight="bold")
        xx += wd
    line(f, x0, y0 + 12, x0 + sum(cw), y0 + 12, color=GRAY, w=1)
    for r, k in enumerate("abcde"):
        yy = y0 + 32 + r * 24
        col = RED if k == "b" else INK
        vals = [k, pos[r], f"{cnt[k]} / 4", f"{1 + cnt[k] / 4:.2f}", exp[r]]
        xx = x0
        for v, wd in zip(vals, cw):
            f.text(xx + wd / 2, yy, v, size=12, color=col, weight="bold" if k == "b" else "normal")
            xx += wd
    f.text(400, 328, "이중 결합으로 가장 많이 그려지는 b(C1–C2)가 결합 차수 최대 → 가장 짧다", size=12.5, color=RED, weight="bold")
    return f.render()


# ================================================================== 단원 2
def f2013_35():
    f = Fig(800, 300)
    f.text(20, 20, "② 짝산–짝염기 쌍 비교: 짝염기가 안정할수록 강한 산", size=12.5, anchor="start", weight="bold")
    # 피롤륨(N-양성자화) → 피롤
    m = Mol()
    pyrrole_like(m, "r", 0, 0, 90)
    ring_bonds(m, "r", 5, [1, 3], (0, 0))
    m.label("r0", "N^+")
    m.sub("h1", "r0", 130, "H", length=24)
    m.sub("h2", "r0", 50, "H", length=24)
    f.mol(m, 80, 100)
    f.text(80, 150, "N-양성자화 피롤륨", size=11.5)
    f.text(80, 166, "(N sp³, 방향족성 상실)", size=10.5, color=RED)
    f.arrow(130, 95, 200, 95, "−H^+", "")
    m = Mol()
    pyrrole_like(m, "r", 0, 0, 90)
    ring_bonds(m, "r", 5, [1, 3], (0, 0))
    m.label("r0", "N")
    m.sub("h1", "r0", 90, "H", length=24)
    f.mol(m, 245, 100)
    f.text(245, 150, "피롤 (6π 방향족 회복)", size=11.5, color=GREEN)
    f.text(160, 190, "pKₐ ≪ 0 (매우 강한 산)", size=12, color=RED, weight="bold")
    # 피리디늄 → 피리딘
    m = Mol()
    benzene(m, "p", 0, 0, 90)
    m.label("p3", "N^+")
    m.sub("h", "p3", -90, "H", length=24)
    f.mol(m, 420, 85)
    f.text(420, 160, "피리디늄", size=11.5)
    f.arrow(470, 90, 540, 90, "−H^+", "")
    m = Mol()
    benzene(m, "p", 0, 0, 90)
    m.label("p3", "N")
    f.mol(m, 590, 85)
    f.text(590, 160, "피리딘 (방향족 유지)", size=11.5)
    f.text(505, 190, "pKₐ = 5.2", size=12, weight="bold")
    f.text(400, 214, "→ 실제 산도: 피롤륨(N–H) ≫ 피리디늄 이므로 ②의 “<”는 틀림", size=12.5, color=RED, weight="bold")
    # 나머지 쌍
    f.box(20, 230, 760, 62, fill="#f7f9fc")
    rows = ["① CH₃CH₂CH₂OH 16.1 < HC≡CCH₂OH 13.6 (sp 탄소의 −I) ○   ③ PhOH 10.0 < PhSH 6.6 (S–H 약함, S⁻ 큼) ○",
            "④ m-NO₂ 3.45 < o-NO₂ 2.17 (ortho 효과 + 가까운 −I) ○   ⑤ 이미다졸륨 7.0 < 옥사졸륨 0.8 (O 전기음성, 공명 주개 약함) ○"]
    for i, r in enumerate(rows):
        f.text(32, 250 + i * 24, r, size=11.2, anchor="start")
    return f.render()


def _aniline(m, p, x, y, n_lab="NH_2", nitro=False, me2=False):
    benzene(m, p, x, y, 90)
    n = m.sub(p + "N", p + "0", 90, n_lab if not me2 else "N")
    if me2:
        m.sub(p + "m1", n, 150)
        m.sub(p + "m2", n, 30)
    if nitro:
        m.sub(p + "n2", p + "1", -30, "NO_2", anchor="start")
        m.sub(p + "n6", p + "5", 210, "O_2N", anchor="end")
        m.sub(p + "n4", p + "3", -90, "NO_2")
    return n


def f2012_38():
    f = Fig(800, 430)
    f.text(20, 18, "산 1몰은 두 염기 중 더 강한 염기(짝산 pKₐ가 큰 쪽)를 양성자화한다", size=12.5, anchor="start", weight="bold")
    # ㄱ
    m = Mol()
    benzene(m, "a", 0, 0, 90)
    n = m.sub("n", "a0", 90, "N")
    m.sub("m1", n, 150)
    m.sub("m2", n, 30)
    m.sub("o1", "a1", 30)
    m.sub("o2", "a5", 150)
    f.mol(m, 80, 95, scale=0.8)
    f.text(80, 145, "pKₐH > 5.1", size=11.5, color=GREEN, weight="bold")
    f.text(155, 85, "vs", size=13)
    m = Mol()
    benzene(m, "b", 0, 0, 90)
    n = m.sub("n", "b0", 90, "N")
    m.sub("m1", n, 150)
    m.sub("m2", n, 30)
    f.mol(m, 225, 95, scale=0.8)
    f.text(225, 145, "pKₐH 5.1", size=11.5)
    f.text(320, 60, "ㄱ ○", size=14, color=GREEN, weight="bold", anchor="start")
    f.text(320, 84, "o-CH₃가 NMe₂를 비틀어 공명(비공유쌍 비편재화)을 억제", size=11.5, anchor="start")
    f.text(320, 104, "→ N 비공유쌍이 국재화되어 염기성 ↑ (공명의 입체 억제)", size=11.5, anchor="start")
    f.text(320, 124, "→ 보기처럼 tetramethylaniline이 양성자화 ✓", size=11.5, anchor="start", color=GREEN)
    # ㄴ: 아미디늄 공명
    y = 225
    for i, x in enumerate((64, 225)):
        m = Mol()
        c = m.atom("c", 0, 0)
        m.sub("me", c, 270)
        m.sub("n1", c, 150, "NH_2^+" if i == 0 else "NH_2", kind="2" if i == 0 else 1, anchor="end")
        m.sub("n2", c, 30, "NH_2" if i == 0 else "NH_2^+", kind=1 if i == 0 else "2", anchor="start")
        f.mol(m, x, y)
    f.resarrow(124, 162, y - 8)
    f.text(132, y + 52, "아세트아미디늄 (양전하 비편재화)", size=11, color=GREEN)
    f.text(132, y + 70, "짝산 pKₐ 12.4", size=11.5, color=GREEN, weight="bold")
    f.text(292, y + 6, "vs", size=13)
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("a", c, 150)
    m.sub("b", c, 30)
    m.sub("n", c, -90, "NH_3^+")
    f.mol(m, 342, y - 10)
    f.text(342, y + 52, "i-PrNH₃⁺", size=11)
    f.text(342, y + 70, "pKₐ 10.6", size=11.5)
    f.text(400, y - 30, "ㄴ ✗", size=14, color=RED, weight="bold", anchor="start")
    f.text(400, y - 6, "아미딘(C(=NH)NH₂)이 더 강한 염기:", size=11.5, anchor="start")
    f.text(400, y + 14, "=NH에 H⁺가 붙으면 양전하가 두 N에 대칭 비편재화", size=11.5, anchor="start")
    f.text(400, y + 34, "→ 주생성물은 아미디늄, 보기의 i-PrNH₃⁺ ✗", size=11.5, anchor="start", color=RED)
    # ㄷ
    y = 360
    m = Mol()
    benzene(m, "p", 0, 0, 90)
    m.sub("n", "p0", 90, "NH_2")
    m.sub("no", "p3", -90, "NO_2")
    f.mol(m, 70, y, scale=0.7)
    f.text(70, y + 58, "p-: pKₐH 1.0", size=11.5)
    f.text(135, y, "vs", size=13)
    m = Mol()
    benzene(m, "q", 0, 0, 90)
    m.sub("n", "q0", 90, "NH_2")
    m.sub("no", "q2", -30, "NO_2", anchor="start")
    f.mol(m, 190, y, scale=0.7)
    f.text(200, y + 58, "m-: pKₐH 2.5", size=11.5, color=GREEN, weight="bold")
    f.text(300, y - 25, "ㄷ ✗", size=14, color=RED, weight="bold", anchor="start")
    f.text(300, y - 1, "para-NO₂는 N 비공유쌍을 공명(−M)으로 직접 끌어감 → 염기성 매우 약함", size=11.5, anchor="start")
    f.text(300, y + 19, "meta-NO₂는 유발(−I)만 → 상대적으로 강한 염기 → m-nitroanilinium 생성", size=11.5, anchor="start")
    return f.render()


def _cp3(m, p, x=0, y=0, dbl=False):
    """삼원 고리: a(오른쪽 꼭짓점), b(왼위), c(왼아래)"""
    a = m.atom(p + "a", x, y)
    b = m.atom(p + "b", x - 26, y - 15)
    c = m.atom(p + "c", x - 26, y + 15)
    m.bond(a, b)
    m.bond(b, c, "2r" if dbl else 1)
    m.bond(c, a)
    m.sub(p + "p1", b, 150, "Ph", anchor="end")
    m.sub(p + "p2", c, 210, "Ph", anchor="end")
    return a


def f2010_35():
    f = Fig(800, 310)
    f.text(20, 18, "짝염기의 안정성 비교", size=12.5, anchor="start", weight="bold")
    for x, lab, txt, col in ((110, "O^−", "serine의 알콕사이드 (짝산 pKₐ ≈ 13 이상)", INK),
                             (340, "S^−", "cysteine의 싸이올레이트 (짝산 pKₐ 8.3)", GREEN)):
        m = Mol()
        c = m.atom("c", 0, 0)
        m.sub("co", c, 210, "HOOC", anchor="end")
        m.sub("n", c, 90, "NH_2")
        xx = m.sub("x", c, -30)
        m.sub("o", xx, 30, lab)
        f.mol(m, x, 80)
        f.text(x, 122, txt, size=11, color=col)
    f.text(480, 62, "① ✗ (정답): S–H가 더 산성", size=12.5, color=RED, weight="bold", anchor="start")
    f.text(480, 84, "S는 O보다 크다 → S–H 결합 약하고", size=11.5, anchor="start")
    f.text(480, 102, "음전하가 큰 부피에 분산 → S⁻ 안정", size=11.5, anchor="start")
    y = 205
    m = Mol()
    a = _cp3(m, "l", 0, 0)
    k = m.sub("k", a, 0, kind="2")
    m.sub("o", k, 60, "O^−")
    m.sub("ph", k, -60, "Ph", anchor="start")
    f.mol(m, 110, y)
    f.text(110, y + 58, "사이클로프로필 엔올레이트 (공명 안정)", size=11, color=GREEN)
    m = Mol()
    a = _cp3(m, "r", 0, 0, dbl=True)
    m.sub("k", a, 0, "COPh", anchor="start")
    f.mol(m, 330, y)
    f.charge(336, y + 16, "−")
    f.text(330, y + 58, "사이클로프로페닐 음이온 (4π 반방향족)", size=11, color=RED)
    f.text(480, y - 45, "② ○: 왼쪽 H가 더 산성", size=12.5, color=GREEN, weight="bold", anchor="start")
    f.text(480, y - 23, "오른쪽 짝염기는 고리 내 4π 전자 → Hückel 4n", size=11.5, anchor="start")
    f.text(480, y - 5, "반방향족 → 매우 불안정 (공명 안정화 포기)", size=11.5, anchor="start")
    f.text(480, y + 22, "③ RC≡N⁺H ≈ −10 > PyH⁺ 5.2 ○", size=11.5, anchor="start")
    f.text(480, y + 42, "④ m-Cl 3.83 > p-Cl 3.98 (pKₐ 작을수록 강산) ○", size=11.5, anchor="start")
    f.text(480, y + 62, "⑤ o-t-Bu ≈ 3.5 > p-t-Bu 4.4 (ortho 효과) ○", size=11.5, anchor="start")
    return f.render()


def _diacid(m, p, x, y, cis=True, n_anion=0, hbond=False):
    """뷰텐다이오산. n_anion: 0, 1(왼쪽 음이온), 2"""
    a = m.atom(p + "a", x, y)
    b = m.sub(p + "b", a, 0, kind="2")
    if cis:
        c1 = m.sub(p + "c1", a, 120)
        c2 = m.sub(p + "c2", b, 60)
        m.sub(p + "o1", c1, 180, "O", kind="2")
        m.sub(p + "o2", c2, 0, "O", kind="2")
        m.sub(p + "x1", c1, 90, "O^−" if n_anion >= 1 else "OH")
        m.sub(p + "x2", c2, 90, "O^−" if n_anion == 2 else ("O" if hbond else "OH"))
        if hbond:
            m.sub(p + "hh", p + "x2", 180, "H", length=20)
    else:
        c1 = m.sub(p + "c1", a, 120)
        c2 = m.sub(p + "c2", b, -60)
        m.sub(p + "o1", c1, 180, "O", kind="2")
        m.sub(p + "o2", c2, 0, "O", kind="2")
        m.sub(p + "x1", c1, 60, "O^−" if n_anion >= 1 else "OH")
        m.sub(p + "x2", c2, -120, "O^−" if n_anion == 2 else "OH")
    return m


def f2007_10():
    f = Fig(800, 360)
    f.text(20, 18, "Maleic acid (cis)", size=13, anchor="start", weight="bold")
    m = Mol()
    _diacid(m, "a", 0, 0, True, 0)
    f.mol(m, 60, 115)
    f.text(75, 150, "pKₐ₁ 1.9", size=11.5)
    f.arrow(150, 100, 215, 100, "−H^+", "빠름")
    m = Mol()
    _diacid(m, "b", 0, 0, True, 1, hbond=True)
    f.mol(m, 275, 115)
    x1, y1 = m.pos("bx1")
    xh, yh = m.pos("bhh")
    line(f, 275 + x1 + 10, 115 + y1, 275 + xh - 7, 115 + yh, color=RED, w=1.6, dash="3 3")
    f.text(290, 150, "분자 내 수소 결합 (7원 고리)", size=11.5, color=GREEN)
    f.text(290, 168, "→ 1차 짝염기 안정 → Kₐ₁ 큼", size=11.5, color=GREEN, weight="bold")
    f.arrow(385, 100, 450, 100, "−H^+", "어려움")
    m = Mol()
    _diacid(m, "c", 0, 0, True, 2)
    f.mol(m, 510, 115)
    f.text(525, 150, "pKₐ₂ 6.2", size=11.5)
    f.text(640, 82, "H-결합 끊어야 하고", size=11.5, anchor="start", color=RED)
    f.text(640, 100, "가까운 두 −CO₂⁻의", size=11.5, anchor="start", color=RED)
    f.text(640, 118, "정전기적 반발 → Kₐ₂ 작음", size=11.5, anchor="start", color=RED, weight="bold")
    f.text(20, 198, "Fumaric acid (trans)", size=13, anchor="start", weight="bold")
    for x, n in ((60, 0), (275, 1), (510, 2)):
        m = Mol()
        _diacid(m, "d", 0, 0, False, n)
        f.mol(m, x, 262)
    f.text(75, 345, "pKₐ₁ 3.0", size=11.5)
    f.arrow(150, 262, 215, 262, "−H^+", "")
    f.text(290, 345, "H-결합 불가 (−I 효과만)", size=11.5)
    f.arrow(385, 262, 450, 262, "−H^+", "")
    f.text(525, 345, "pKₐ₂ 4.4", size=11.5)
    f.text(640, 240, "두 음전하가 멀리", size=11.5, anchor="start")
    f.text(640, 258, "떨어져 반발 작음", size=11.5, anchor="start")
    f.text(640, 290, "Kₐ₁: 말레산 > 푸마르산", size=12, anchor="start", weight="bold", color=BLUE)
    f.text(640, 310, "Kₐ₂: 말레산 < 푸마르산", size=12, anchor="start", weight="bold", color=BLUE)
    return f.render()


def f2006_9():
    f = Fig(800, 290)
    specs = [("aniline", False, False, "4.6", INK),
             ("N,N-dimethylaniline", False, True, "5.1 (최대)", GREEN),
             ("2,4,6-trinitroaniline", True, False, "≈ −9.4 (최소)", RED),
             ("2,4,6-trinitro-N,N-dimethylaniline", True, True, "≈ −4.8", INK)]
    xs = [90, 280, 480, 680]
    for (name, nitro, me2, pk, col), x in zip(specs, xs):
        m = Mol()
        _aniline(m, "r", 0, 0, nitro=nitro, me2=me2)
        f.mol(m, x, 110, scale=0.82)
        f.text(x, 186, name, size=11 if len(name) < 25 else 10, color=col, weight="bold")
        f.text(x, 204, "pKₐH " + pk, size=11.5, color=col)
    f.text(20, 236, "• NMe₂: 메틸의 +I로 N 전자 밀도 ↑ → aniline보다 강한 염기.  • 2,4,6-NO₂: ortho/para에서 N 비공유쌍을 −M으로 끌어감 → 극도로 약한 염기", size=11, anchor="start")
    f.text(20, 258, "• trinitro-NMe₂: o-NO₂와 N-CH₃의 입체 반발로 NMe₂가 고리 면에서 비틀림 → 공명 억제 → trinitroaniline보다 약 10⁴배 강한 염기", size=11, anchor="start")
    f.text(20, 280, "  (단, NO₂ 3개의 강한 −I 효과는 남으므로 N,N-dimethylaniline보다는 훨씬 약하다)", size=11, anchor="start", color=GRAY)
    return f.render()


def f2004_9():
    f = Fig(800, 410)
    f.text(20, 18, "짝산(또는 산 자신)의 pKₐ 수직선 — 오른쪽으로 갈수록 약한 산 / 강한 짝염기", size=12.5, anchor="start", weight="bold")
    numline(f, 150, 760, 85, 0, 20, [(18, "① 사이클로헥산올 ~18", True), (10.0, "③ 페놀 10.0", True),
                                      (7.15, "② p-NO₂-페놀 7.15", False), (4.47, "⑤ p-MeO-벤조산 4.47", True),
                                      (4.20, "④ 벤조산 4.20", False)], "9-1 산", step=2)
    f.text(760, 142, "산 세기 증가: ① → ③ → ② → ⑤ → ④", size=12, anchor="end", color=RED, weight="bold")
    numline(f, 150, 760, 210, 0, 50, [(9.2, "HCN 9.2", True), (15.5, "CH₃OH 15.5", False), (25, "HC≡CH 25", True),
                                       (44, "CH₂=CH₂ 44", False), (50, "CH₃CH₃ 50", True)], "9-2 짝산", step=5)
    f.text(760, 267, "염기 세기 증가: ① CN⁻ → ⑤ CH₃O⁻ → ③ HC≡C⁻ → ④ CH₂=CH⁻ → ② CH₃CH₂⁻", size=12, anchor="end", color=RED, weight="bold")
    numline(f, 150, 760, 335, -5, 12, [(-3.8, "③ 피롤 −3.8", True), (4.6, "② 아닐린 4.6", False),
                                        (5.2, "① 피리딘 5.2", True), (10.6, "④ 사이클로헥실아민 10.6", False)], "9-3 짝산", step=1)
    f.text(760, 395, "염기 세기 증가: ③ → ② → ① → ④", size=12, anchor="end", color=RED, weight="bold")
    return f.render()


# ================================================================== 단원 3
def f2009_22():
    f = Fig(800, 380)
    f.text(20, 18, "고오시 상호작용 1개 = 0.9 kcal/mol (축 방향 CH₃ 1개 = 고리 탄소와 고오시 2개 = 1.8)", size=12.5, anchor="start", weight="bold")
    # cis
    f.text(20, 50, "cis (a,e) ⇌ (e,a): 두 형태의 에너지 동일", size=12.5, anchor="start", color=BLUE, weight="bold")
    chair(f, 130, 120, {1: ("!CH_3", ""), 2: ("", "CH_3")})
    f.eqarrow(215, 275, 120)
    chair(f, 370, 120, {1: ("", "CH_3"), 2: ("!CH_3", "")})
    f.text(250, 180, "각 형태: CH₃–CH₃ 고오시 1 + 축 CH₃ 고오시 2 = 3 × 0.9 = 2.7 kcal/mol", size=11.5)
    # trans
    f.text(20, 216, "trans (e,e) ⇌ (a,a): 에너지 다름", size=12.5, anchor="start", color=BLUE, weight="bold")
    chair(f, 130, 290, {1: ("", "CH_3"), 2: ("", "CH_3")})
    f.eqarrow(215, 275, 290)
    chair(f, 370, 290, {1: ("!CH_3", ""), 2: ("!CH_3", "")})
    f.text(130, 350, "(e,e): 고오시 1개 = 0.9", size=11.5, color=GREEN, weight="bold")
    f.text(370, 350, "(a,a): 고오시 4개 = 3.6", size=11.5)
    f.box(505, 60, 280, 300, fill="#fff8e6", stroke="#f0c36d")
    f.text(520, 82, "안정성 비교 (가장 안정한 형태끼리)", size=12, anchor="start", weight="bold")
    f.text(520, 108, "cis: 2.7 kcal/mol", size=12, anchor="start")
    f.text(520, 130, "trans (e,e): 0.9 kcal/mol", size=12, anchor="start")
    f.text(520, 156, "ΔE = 2.7 − 0.9 = 1.8 kcal/mol", size=12.5, anchor="start", color=RED, weight="bold")
    f.text(520, 184, "⑤의 2.7 kcal/mol ✗", size=12.5, anchor="start", color=RED, weight="bold")
    f.text(520, 220, "입체이성질체", size=12, anchor="start", weight="bold")
    f.text(520, 242, "• cis: 메조(두 의자형은 서로 거울상,", size=11.5, anchor="start")
    f.text(520, 260, "  빠른 뒤집힘 → 광학 비활성)", size=11.5, anchor="start")
    f.text(520, 282, "• trans: (1R,2R), (1S,2S) 광학 활성", size=11.5, anchor="start")
    f.text(520, 304, "→ 총 3개 (①○), 광학 활성 2개 (②○)", size=11.5, anchor="start")
    f.text(520, 330, "③ ○, ④ ○, ⑤ ✗", size=12.5, anchor="start", color=BLUE, weight="bold")
    return f.render()


# ================================================================== 단원 4
def _zig(m, p, n, x=0, y=0):
    """지그재그 사슬 원자 p0..p(n-1)"""
    names = []
    for i in range(n):
        m.atom(f"{p}{i}", x + i * L * math.cos(math.radians(30)), y + (0 if i % 2 == 0 else -L / 2))
        names.append(f"{p}{i}")
        if i:
            m.bond(names[i - 1], names[i])
    return names


def f2013_34():
    f = Fig(800, 350)
    newman(f, 80, 85, ["CH_3", "H_3C", "CH_3"], ["CH_3", "H_3C", "CH_3"], size=11)
    f.cap(80, 150, "A")
    f.arrow(135, 85, 185, 85)
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 0)
    for i, ang in enumerate((90, 210, -90)):
        m.sub(f"x{i}", a, ang + (0 if ang != 210 else 0))
    for i, ang in enumerate((90, -30, -90)):
        m.sub(f"y{i}", b, ang)
    f.mol(m, 220, 85)
    f.text(240, 135, "2,2,3,3-tetramethylbutane", size=11.5)
    f.text(240, 152, "C₈H₁₈, mp 100.7 ℃ (구형·고대칭)", size=11, color=GREEN)
    newman(f, 450, 85, ["CH_2CH_3", "H", "CH_3"], ["H", "H_3C", "CH_2CH_3"], size=11)
    f.cap(450, 150, "B")
    f.arrow(515, 85, 565, 85)
    m = Mol()
    z = _zig(m, "z", 6)
    m.sub("m1", "z2", -90)
    m.sub("m2", "z3", 90)
    f.mol(m, 600, 95)
    f.text(670, 135, "3,4-dimethylhexane", size=11.5)
    f.text(670, 152, "C₈H₁₈, 상온 액체", size=11)
    f.text(400, 185, "A와 B는 분자식은 같지만 연결 순서가 다르다 → 구조(구성) 이성질체 (형태 이성질체 ✗ → ㄷ ✗)", size=12, color=RED, weight="bold")
    # B의 입체이성질체 3개
    f.text(20, 215, "3,4-dimethylhexane의 입체이성질체 (입체 중심 2개, 분자 대칭) → 3개 (ㄴ ✗)", size=12.5, anchor="start", weight="bold")
    confs = [("h", "h", "(3R,4R)"), ("w", "w", "(3S,4S)"), ("w", "h", "meso (3R,4S)")]
    for i, (k1, k2, name) in enumerate(confs):
        m = Mol()
        _zig(m, "z", 6)
        m.sub("m1", "z2", -90, kind=k1)
        m.sub("m2", "z3", 90, kind=k2)
        x = 60 + i * 260
        f.mol(m, x, 285)
        f.text(x + 65, 330, name, size=12, color=GREEN if "meso" in name else INK, weight="bold")
    f.text(255, 330, "← 거울상 쌍 →", size=11, color=GRAY)
    return f.render()


def f2011_34():
    f = Fig(800, 330)
    newman(f, 90, 95, ["CO_2H", "H", "OH"], ["OH", "H", "CO_2H"], size=11, hl=["OH"])
    f.cap(90, 160, "A")
    newman(f, 90, 250, ["CO_2H", "HO", "H"], ["OH", "H", "CO_2H"], size=11, hl=["OH", "HO"])
    f.cap(90, 315, "B")
    f.arrow(160, 95, 230, 95, "C–C 회전", "")
    f.arrow(160, 250, 230, 250, "C–C 회전", "")

    def tart(k2, k3):
        m = Mol()
        c1 = m.atom("c1", 0, 0, "HO_2C", anchor="end")
        c2 = m.sub("c2", c1, -30)
        c3 = m.sub("c3", c2, 30)
        m.sub("c4", c3, -30, "CO_2H", anchor="start")
        m.sub("o2", c2, -90, "OH", kind=k2)
        m.sub("o3", c3, 90, "OH", kind=k3)
        return m
    f.mol(tart("w", "w"), 280, 95)
    f.text(320, 162, "(2R,3R)-tartaric acid (키랄)", size=12, weight="bold")
    f.text(520, 80, "A: C₂ 대칭축만 있음 → 키랄", size=12, anchor="start")
    f.text(520, 100, "앞 탄소: OH(1) → CO₂H(2) → C3(3) 시계 방향,", size=11.5, anchor="start")
    f.text(520, 118, "H(4)는 관찰자 쪽이 아님 → R (C3도 R)", size=11.5, anchor="start")
    f.mol(tart("w", "h"), 280, 250)
    f.text(320, 317, "meso-tartaric acid (2R,3S)", size=12, weight="bold", color=GREEN)
    f.text(520, 235, "B: 반대로 놓인 두 쌍(H/H, OH/OH, CO₂H/CO₂H)", size=12, anchor="start")
    f.text(520, 253, "→ 대칭 중심(i) 존재 → 아키랄(메조), [α] = 0", size=12, anchor="start", color=GREEN)
    f.text(520, 285, "ㄱ ○ 부분입체이성질체, ㄴ ○ [α] = 0", size=12, anchor="start", weight="bold", color=BLUE)
    f.text(520, 303, "ㄷ ✗ mp: (R,R) 170 ℃, meso 146 ℃", size=12, anchor="start", weight="bold", color=RED)
    return f.render()


def _allene(m, p, flip=False):
    c1 = m.atom(p + "c1", 0, 0)
    c2 = m.sub(p + "c2", c1, 0, kind="2")
    c3 = m.sub(p + "c3", c2, 0, kind="2")
    m.sub(p + "a", c1, 150, "H_3C", anchor="end")
    m.sub(p + "b", c1, 210, "H")
    if not flip:
        m.sub(p + "c", c3, 70, "CH_3", kind="w")
        m.sub(p + "d", c3, -70, "H", kind="h")
    else:
        m.sub(p + "c", c3, 70, "H", kind="w")
        m.sub(p + "d", c3, -70, "CH_3", kind="h")
    return m


def f2010_34():
    f = Fig(800, 290)
    f.mol(_allene(Mol(), "a"), 90, 90)
    mm = _allene(Mol(), "b")
    for k, v in mm.a.items():
        v[0] = -v[0]
        v[3] = {"start": "end", "end": "start"}.get(v[3], v[3])
        if v[2] == "H_3C":
            v[2] = "CH_3"
        elif v[2] == "CH_3":
            v[2] = "H_3C"
    f.mol(mm, 400, 90)
    line(f, 245, 30, 245, 150, color=GRAY, w=1.2, dash="5 4")
    f.text(245, 170, "거울", size=11, color=GRAY)
    f.text(210, 190, "겹쳐지지 않는 거울상 (축 카이랄성) → ① ○", size=12.5, color=GREEN, weight="bold")
    # 궤도 모식도
    f.box(470, 14, 315, 200, fill="#f7f9fc")
    f.text(485, 34, "C2=C3=C4 π 결합의 방향", size=12, anchor="start", weight="bold")
    y0, x0 = 120, 520
    line(f, x0, y0, x0 + 180, y0, w=2)
    for x in (x0, x0 + 180):
        f.raw(f'<circle cx="{x}" cy="{y0}" r="4" fill="{INK}"/>')
    f.raw(f'<circle cx="{x0 + 90}" cy="{y0}" r="4" fill="{INK}"/>')
    # C2–C3 π: 위/아래 로브 (종이 면)
    for x in (x0 + 10, x0 + 80):
        f.porb(x, y0, 1, rx=7, ry=15)
    # C3–C4 π: 앞/뒤 로브(타원을 옆으로)
    for x in (x0 + 100, x0 + 170):
        f.raw(f'<ellipse cx="{x}" cy="{y0}" rx="15" ry="6" fill="{ORANGE}" fill-opacity="0.8" stroke="{INK}"/>')
    f.text(x0 + 45, y0 - 42, "π(C2=C3)", size=11)
    f.text(x0 + 135, y0 - 42, "π(C3=C4)", size=11)
    f.text(x0 + 90, y0 + 38, "가운데 C(sp)의 두 p 궤도는 서로 수직", size=11)
    f.text(x0 + 90, y0 + 56, "→ 두 π 결합 직교: 공액 ✗ (⑤ ✗)", size=11, color=RED)
    f.text(x0 + 90, y0 + 74, "→ 양 끝 치환기 평면도 서로 수직 (② ✗)", size=11, color=RED)
    f.text(20, 230, "③ ✗ 비대칭(카이랄) 탄소 없음 — 카이랄성은 C=C=C 축에서 생김(입체 중심 = 축)", size=12, anchor="start")
    f.text(20, 252, "④ ✗ 혼성: sp³ – sp² – sp – sp² – sp³ (가운데 탄소는 σ 결합 2개 → sp)", size=12, anchor="start")
    f.text(20, 276, "⑤ ✗ 누적(cumulated) 이중 결합: 두 π가 직교하므로 공액이 아니다", size=12, anchor="start")
    return f.render()


ALL = [f2012_35, f2009_21, f2013_35, f2012_38, f2010_35, f2007_10, f2006_9, f2004_9, f2009_22, f2013_34, f2011_34, f2010_34]

if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from preview import shot
    shot([fn() for fn in ALL], sys.argv[1])
