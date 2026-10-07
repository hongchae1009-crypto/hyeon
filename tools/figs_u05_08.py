"""5 친핵성 치환 · 6 제거 · 7 알켄 · 8 알카인 문항 그림"""
import math
from chemsvg import Mol, Fig, benzene, phenyl_at, L, RED, BLUE, INK, rich

GREEN = "#1e7b34"
GRAY = "#6b7280"
ORANGE = "#d97706"


# ------------------------------------------------------------------ 공통 헬퍼
def P(m, name, ox, oy):
    x, y = m.pos(name)
    return ox + x, oy + y


def zig(m, p, x, y, n, up_first=True, start=None):
    """n개 원자 지그재그 사슬 (p1..pn). 반환: 이름 목록"""
    names = []
    prev = None
    if start is not None:
        prev = start
    else:
        m.atom(p + "1", x, y)
        prev = p + "1"
        names.append(prev)
        n -= 1
    ang = 30 if up_first else -30
    for i in range(n):
        nm = f"{p}{len(names) + 1}"
        m.sub(nm, prev, ang)
        names.append(nm)
        prev = nm
        ang = -ang
    return names


def ring_on_edge(m, p, a1, a2, n, away, labels=None, bonds=True):
    """a1–a2 변을 공유하는 정n각형 고리를 away 점의 반대쪽에 만든다. 새 원자 p1..p(n-2) (a2 쪽부터)."""
    (x1, y1), (x2, y2) = m.pos(a1), m.pos(a2)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    s = math.hypot(dx, dy)
    nx, ny = -dy / s, dx / s
    ax, ay = away
    if (ax - mx) * nx + (ay - my) * ny > 0:
        nx, ny = -nx, -ny
    ap = s / (2 * math.tan(math.pi / n))
    cx, cy = mx + nx * ap, my + ny * ap
    R = s / (2 * math.sin(math.pi / n))
    # a2에서 시작해 a1 반대 방향으로 회전
    t1 = math.atan2(y1 - cy, x1 - cx)
    t2 = math.atan2(y2 - cy, x2 - cx)
    step = 2 * math.pi / n
    d = (t2 - t1 + math.pi) % (2 * math.pi) - math.pi
    sgn = 1 if d > 0 else -1
    names, prev = [], a2
    for k in range(1, n - 1):
        t = t2 + sgn * step * k
        nm = f"{p}{k}"
        lab = labels[k - 1] if labels else None
        m.atom(nm, cx + R * math.cos(t), cy + R * math.sin(t), lab)
        if bonds:
            m.bond(prev, nm)
        names.append(nm)
        prev = nm
    if bonds:
        m.bond(prev, a1)
    return names, (cx, cy)


def bracket(f, x1, y1, x2, y2, dagger=True):
    f.raw(f'<path d="M{x1 + 8},{y1} L{x1},{y1} L{x1},{y2} L{x1 + 8},{y2} M{x2 - 8},{y1} L{x2},{y1} L{x2},{y2} L{x2 - 8},{y2}" '
          f'fill="none" stroke="{INK}" stroke-width="1.3"/>')
    if dagger:
        f.text(x2 + 8, y1 + 4, "‡", size=15)


def newman(f, cx, cy, front, back, r=22, ln=42, colors=None):
    """front/back: [(ang, label)].  colors: {label_index: color}"""
    colors = colors or {}
    f.raw(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="1.4"/>')
    for i, (a, lab) in enumerate(back):
        c = colors.get(("b", i), INK)
        ra = math.radians(a)
        x1, y1 = cx + r * math.cos(ra), cy - r * math.sin(ra)
        x2, y2 = cx + ln * math.cos(ra), cy - ln * math.sin(ra)
        f.raw(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="1.4"/>')
        f.text(cx + (ln + 13) * math.cos(ra), cy - (ln + 11) * math.sin(ra), lab, size=12, color=c)
    for i, (a, lab) in enumerate(front):
        c = colors.get(("f", i), INK)
        ra = math.radians(a)
        x2, y2 = cx + (ln - 8) * math.cos(ra), cy - (ln - 8) * math.sin(ra)
        f.raw(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="1.4"/>')
        f.text(cx + (ln + 5) * math.cos(ra), cy - (ln + 3) * math.sin(ra), lab, size=12, color=c)
    f.raw(f'<circle cx="{cx}" cy="{cy}" r="1.8" fill="{INK}"/>')


def sawhorse(f, x, y, front, back, d=50, ln=30):
    """앞 탄소 (x,y), 뒤 탄소 (x+d, y-d). front/back: [(ang, label)]"""
    bx, by = x + d, y - d
    f.raw(f'<line x1="{x}" y1="{y}" x2="{bx}" y2="{by}" stroke="{INK}" stroke-width="1.5"/>')
    for (cx, cy, lst) in ((bx, by, back), (x, y, front)):
        for a, lab in lst:
            ra = math.radians(a)
            f.raw(f'<line x1="{cx}" y1="{cy}" x2="{cx + ln * math.cos(ra):.1f}" y2="{cy - ln * math.sin(ra):.1f}" stroke="{INK}" stroke-width="1.4"/>')
            f.add(rich(cx + (ln + 11) * math.cos(ra), cy - (ln + 9) * math.sin(ra), lab, size=12, halo=True))


def fischer(f, x, y, rows, top="CH_3", bot="CH_3", gap=46, arm=32, hl=None):
    """rows: [(왼쪽, 오른쪽)] 위에서부터. hl: 강조색으로 칠할 라벨"""
    n = len(rows)
    y0, y1 = y - 30, y + gap * (n - 1) + 30
    f.raw(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="{INK}" stroke-width="1.5"/>')
    f.text(x, y0 - 10, top, size=13)
    f.text(x, y1 + 11, bot, size=13)
    for i, (lft, rgt) in enumerate(rows):
        yy = y + gap * i
        f.raw(f'<line x1="{x - arm}" y1="{yy}" x2="{x + arm}" y2="{yy}" stroke="{INK}" stroke-width="1.5"/>')
        f.text(x - arm - 5, yy, lft, size=13, anchor="end", color=RED if lft == hl else INK)
        f.text(x + arm + 5, yy, rgt, size=13, anchor="start", color=RED if rgt == hl else INK)


def energy_curve(f, pts, color=INK):
    """pts: [(x,y)] 극점들을 코사인 보간으로 부드럽게 잇는다."""
    d = [f"M{pts[0][0]},{pts[0][1]}"]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        for k in range(1, 21):
            t = k / 20
            xx = x1 + (x2 - x1) * t
            yy = y1 + (y2 - y1) * (1 - math.cos(math.pi * t)) / 2
            d.append(f"L{xx:.1f},{yy:.1f}")
    f.raw(f'<path d="{" ".join(d)}" fill="none" stroke="{color}" stroke-width="2"/>')


def axes(f, x0, y0, w, h, ylab="에너지", xlab="반응 좌표"):
    f.raw(f'<path d="M{x0},{y0 - h} L{x0},{y0} L{x0 + w},{y0}" fill="none" stroke="{INK}" stroke-width="1.3" '
          f'marker-start="url(#{f.id}k)"/>')
    f.text(x0 - 8, y0 - h / 2, ylab, size=12, anchor="end")
    f.text(x0 + w / 2, y0 + 16, xlab, size=12)


def chair_pts(cx, cy, r=30, h=9, k=0.34):
    """의자형 6원자 투영 좌표 (0: 오른쪽 끝(위), 3: 왼쪽 끝(아래)). 반환 [(x,y,zsign)]"""
    out = []
    for i in range(6):
        t = math.radians(60 * i)
        z = h if i % 2 == 0 else -h
        x = r * math.cos(t) * 1.25
        yd = r * math.sin(t)
        out.append((cx + x, cy - z - yd * k, 1 if z > 0 else -1, t))
    return out


def chair(f, cx, cy, subs=None, r=30):
    """subs: {i: [('ax'|'eq', label, color)]}"""
    pts = chair_pts(cx, cy, r)
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y, _, _ in pts) + " Z"
    f.raw(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>')
    subs = subs or {}
    for i, lst in subs.items():
        x, y, zs, t = pts[i]
        for kind, lab, col in lst:
            if kind == "ax":
                ex, ey = x, y - zs * 30
                tx, ty = x, y - zs * 39
            else:
                ex = x + 27 * math.cos(t) * 1.1
                ey = y - 27 * math.sin(t) * 0.34 + zs * 9
                tx = x + 38 * math.cos(t) * 1.1
                ty = y - 38 * math.sin(t) * 0.34 + zs * 12
            f.raw(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{col}" stroke-width="1.4"/>')
            if lab:
                f.add(rich(tx, ty, lab, size=12, color=col, halo=True))
    return pts


def tbox(f, x, y, w, lines, size=12, color=INK, lh=17, fill="#f7f8fa", stroke="#cfd4db", anchor="start", bold_first=False):
    h = lh * len(lines) + 12
    f.box(x, y, w, h, fill=fill, stroke=stroke)
    for i, t in enumerate(lines):
        f.text(x + 10 if anchor == "start" else x + w / 2, y + 6 + lh * i + lh / 2 + 1, t, size=size, anchor=anchor,
               color=color, weight="bold" if (bold_first and i == 0) else "normal")
    return h


# ================================================================== 단원 5
# ---------------------------------------------------------- 2013 논술형 3 (반응 Ⅰ)
def _enone_ring(m, p):
    r = m.ring(p, 0, 0, 6, L, 90)
    m.set_bond(f"{p}5", f"{p}0", "in", (0, 0))
    m.sub(p + "O", f"{p}4", 210, "O", kind="2")
    m.sub(p + "Me5", f"{p}5", 150)
    return r


def f2013_3_I():
    f = Fig(800, 400)
    # 기질: 이중 고리 락톤
    m = Mol()
    _enone_ring(m, "r")
    new, c = ring_on_edge(m, "q", "r1", "r2", 6, (0, 0), labels=[None, None, None, "O"])
    # new: q1(r2쪽 = O? ) → labels는 a2(r2)부터: q1, q2, q3, q4
    m.label("q1", "O")
    m.label("q4", None)
    m.sub("qO", "q2", -60, "O", kind="2")
    m.sub("me1", "r1", 90, kind="h")
    m.sub("br", "r3", 235, "Br", kind="h")
    m.sub("me3", "r3", 305, kind="w")
    f.mol(m, 80, 105)
    f.cap(110, 190, "기질 (브로모 락톤)")
    # OH- 공격 표시
    qx, qy = P(m, "q2", 80, 105)
    f.text(qx + 40, qy - 45, "HO^−", size=13, color=BLUE)
    f.curly(qx + 30, qy - 38, qx + 4, qy - 6, bend=0.3, color=BLUE)
    f.arrow(230, 105, 345, 105, "(1) KOH", "아실 치환: 락톤 열림")
    # 중간체: 알콕사이드 + 카복실레이트
    m = Mol()
    _enone_ring(m, "r")
    m.sub("me1", "r1", 90, kind="h")
    c1 = m.sub("c1", "r1", 30, kind="w")
    c2 = m.sub("c2", c1, -30)
    c3 = m.sub("c3", c2, 30)
    m.sub("o1", c3, 90, "O", kind="2")
    m.sub("o2", c3, -30, "O^−")
    m.sub("ox", "r2", -30, "O^−", kind="w")
    m.sub("br", "r3", 235, "Br", kind="h")
    m.sub("me3", "r3", 300, kind="w")
    ox, oy = 440, 110
    f.mol(m, ox, oy)
    f.cap(470, 190, "알콕사이드–카복실레이트 (O^− 와 Br은 anti)")
    # 굽은 화살표: O- → C3, C–Br → Br
    xo, yo = P(m, "ox", ox, oy)
    x3, y3 = P(m, "r3", ox, oy)
    xb, yb = P(m, "br", ox, oy)
    f.curly(xo - 2, yo + 9, x3 + 7, y3 + 3, bend=-0.6)
    f.curly((x3 + xb) / 2 + 3, (y3 + yb) / 2 + 2, xb + 5, yb + 8, bend=-0.6)
    f.text(620, 52, "분자 내 S_N2", size=12, color=RED, anchor="start")
    f.text(620, 70, "(뒤쪽 공격, C–Br 탄소 반전)", size=11, color=RED, anchor="start")
    # 2행: 에폭사이드 카복실레이트 → 산
    f.arrow(120, 300, 225, 300, "−Br^−", "3-exo-tet")
    m = Mol()
    _enone_ring(m, "r")
    m.sub("me1", "r1", 90, kind="h")
    c1 = m.sub("c1", "r1", 30, kind="w")
    c2 = m.sub("c2", c1, -30)
    c3 = m.sub("c3", c2, 30)
    m.sub("o1", c3, 90, "O", kind="2")
    m.sub("o2", c3, -30, "O^−")
    x2, y2 = m.pos("r2")
    x3_, y3_ = m.pos("r3")
    mx, my = (x2 + x3_) / 2, (y2 + y3_) / 2
    dd = math.hypot(mx, my)
    m.atom("ep", mx + mx / dd * 24, my + my / dd * 24, "O")
    m.bond("r2", "ep")
    m.bond("r3", "ep")
    m.sub("me3", "r3", 220, kind="h")
    f.mol(m, 290, 305)
    f.cap(330, 382, "에폭사이드 (O와 CH_3는 반대 면)")
    f.arrow(470, 300, 560, 300, "(2) H_3O^+", "양성자화")
    m = Mol()
    _enone_ring(m, "r")
    m.sub("me1", "r1", 90, kind="h")
    c1 = m.sub("c1", "r1", 30, kind="w")
    c2 = m.sub("c2", c1, -30)
    c3 = m.sub("c3", c2, 30)
    m.sub("o1", c3, 90, "O", kind="2")
    m.sub("o2", c3, -30, "OH")
    m.atom("ep", mx + mx / dd * 24, my + my / dd * 24, "O")
    m.bond("r2", "ep")
    m.bond("r3", "ep")
    m.sub("me3", "r3", 220, kind="h")
    f.mol(m, 620, 305)
    f.cap(660, 382, "생성물", color=GREEN)
    return f.render()


# ---------------------------------------------------------- 반응 Ⅱ (아지리디늄)
def f2013_3_II():
    f = Fig(800, 250)
    # 반응물
    m = Mol()
    n = m.atom("n", 0, 0, "N")
    m.sub("nm1", n, 150)
    m.sub("nm2", n, 270)
    c1 = m.sub("c1", n, 30)
    c2 = m.sub("c2", c1, -30)
    c3 = m.sub("c3", c2, 30)
    c4 = m.sub("c4", c3, -30)
    m.sub("c5", c4, 30)
    m.sub("cl", c2, 270, "Cl", kind="w")
    ox, oy = 50, 80
    f.mol(m, ox, oy)
    xn, yn = P(m, "n", ox, oy)
    x2, y2 = P(m, "c2", ox, oy)
    xc, yc = P(m, "cl", ox, oy)
    f.lp(xn, yn - 11, 90)
    f.curly(xn + 4, yn - 14, x2 - 2, y2 - 7, bend=-0.5)
    f.curly(x2 + 5, (y2 + yc) / 2, xc + 10, yc - 2, bend=-0.6)
    f.cap(110, 160, "(R) 반응물")
    f.text(110, 180, "N 비공유쌍의 분자 내 S_N2 (C2 반전)", size=11, color=RED)
    f.arrow(215, 80, 290, 80, "−Cl^−", "이웃기 관여")
    # 아지리디늄
    m = Mol()
    n = m.atom("n", 0, 0, "N^+")
    a = m.atom("a", -17, 30)
    b = m.atom("b", 17, 30)
    m.bond(n, a)
    m.bond(a, b)
    m.bond(b, n)
    m.sub("m1", n, 60, "CH_3", anchor="start")
    m.sub("m2", n, 120, "CH_3", anchor="end")
    c3 = m.sub("c3", b, -30)
    c4 = m.sub("c4", c3, 30)
    m.sub("c5", c4, -30)
    ox, oy = 350, 70
    f.mol(m, ox, oy)
    xa, ya = P(m, "a", ox, oy)
    f.text(xa - 38, ya + 44, "HO^−", size=13, color=BLUE)
    f.curly(xa - 30, ya + 34, xa - 4, ya + 6, bend=-0.3, color=BLUE)
    xn, yn = P(m, "n", ox, oy)
    f.curly((xa + xn) / 2 - 3, (ya + yn) / 2, xn - 13, yn + 2, bend=-0.9)
    f.cap(390, 160, "아지리디늄 이온")
    f.text(390, 180, "HO^− 는 덜 붐빈 CH_2(C1)를 공격", size=11, color=BLUE)
    f.arrow(470, 80, 545, 80, "", "고리 열림")
    # 생성물
    m = Mol()
    o = m.atom("o", 0, 0, "HO", anchor="end")
    c1 = m.sub("c1", o, 30)
    c2 = m.sub("c2", c1, -30)
    nn = m.sub("n", c2, 270, "N", kind="h")
    m.sub("nm1", nn, 210)
    m.sub("nm2", nn, 330)
    c3 = m.sub("c3", c2, 30)
    c4 = m.sub("c4", c3, -30)
    m.sub("c5", c4, 30)
    f.mol(m, 600, 80)
    f.cap(660, 160, "(S) 생성물", color=GREEN)
    f.text(660, 180, "C2: 반전 1회 (N이 Cl 반대편에 결합)", size=11)
    f.text(400, 225, "C2 기준 순서: Cl > CH_2N > C_3H_7 (R)  →  N > CH_2OH > C_3H_7 (S)", size=12, color=GRAY)
    return f.render()


# ---------------------------------------------------------- 반응 Ⅲ (SN2 TS)
def f2013_3_III():
    f = Fig(800, 300)
    m = Mol()
    ch = zig(m, "c", 0, 0, 6, up_first=False)
    # c1..c6: c5가 위 꼭짓점 → 2번 탄소
    m.sub("ots", "c5", 90, "OTs", kind="w")
    f.mol(m, 20, 95)
    f.cap(95, 150, "(S)-2-hexyl tosylate")
    # TS
    cx, cy = 360, 95
    m = Mol()
    c = m.atom("c", 0, 0)
    m.atom("n", -62, 0, "N_3", anchor="middle")
    m.atom("o", 62, 0, "OTs", anchor="middle")
    m.bond("n", "c", "form")
    m.bond("c", "o", "dash")
    m.sub("me", c, 90, "CH_3", length=32)
    m.sub("h", c, 230, "H", kind="w", length=28)
    m.sub("bu", c, 310, "C_4H_9", kind="h", length=30)
    f.mol(m, cx, cy)
    f.text(cx - 62, cy - 18, "δ−", size=11, color=RED)
    f.text(cx + 62, cy - 18, "δ−", size=11, color=RED)
    bracket(f, cx - 95, cy - 55, cx + 100, cy + 60)
    f.cap(cx, 180, "S_N2 전이상태 (삼각쌍뿔, 180°)")
    f.arrow(165, 95, 245, 95, "NaN_3", "뒷면 공격")
    f.arrow(485, 95, 560, 95, "", "−TsO^−")
    m = Mol()
    ch = zig(m, "c", 0, 0, 6, up_first=False)
    m.sub("n3", "c5", 90, "N_3", kind="h")
    f.mol(m, 590, 95)
    f.cap(665, 150, "(R)-2-azidohexane (반전)", color=GREEN)
    # 용매 비교
    tbox(f, 30, 205, 350, ["CH₃OH (양성자성): N₃⁻를 수소 결합으로 둘러쌈",
                             "→ 친핵체 안정화·부피 증가 → 느림"], size=12)
    tbox(f, 420, 205, 350, ["DMF (비양성자성 극성): Na⁺만 용매화",
                              "→ '벗겨진' N₃⁻ → 매우 빠름 (10³~10⁴배)"], size=12, fill="#eef7f0", stroke="#9fd0ab")
    return f.render()


def f2013_3_umbrella():
    f = Fig(800, 250)
    f.text(200, 20, "우산 비유 (비유 영역)", size=13, weight="bold")
    f.text(600, 20, "S_N2 반응 (목표 개념)", size=13, weight="bold")
    pairs = [("우산살 3개", "중심 탄소에 붙은 세 치환기 (H, CH₃, C₄H₉)"),
             ("우산살이 모이는 꼭지(중심)", "반응 중심 탄소 (sp³ → sp² 유사 → sp³)"),
             ("우산을 뒤집는 바람(미는 쪽)", "뒤쪽에서 접근하는 친핵체 N₃⁻"),
             ("살이 일직선으로 펴진 순간", "전이상태: 세 치환기가 한 평면 (삼각쌍뿔)")]
    for i, (a, b) in enumerate(pairs):
        y = 45 + i * 48
        f.box(40, y, 320, 36)
        f.box(440, y, 330, 36, fill="#eef4fc", stroke="#a9c1e6")
        f.text(200, y + 18, a, size=12.5)
        f.text(605, y + 18, b, size=12.5)
        f.resarrow(365, 435, y + 18)
    f.text(400, 243, "한계: 우산 손잡이(이탈기 쪽)는 뒤집힌 뒤에도 붙어 있지만, 실제로는 TsO⁻가 떨어지고 N₃가 반대편에 새로 결합한다.",
           size=11.5, color=RED)
    return f.render()


# ---------------------------------------------------------- 2012 #34
def f2012_34():
    f = Fig(800, 230)
    # ㄱ: methyltropylium
    m = Mol()
    r = m.ring("t", 0, 0, 7, L, 90)
    m.sub("me", "t0", 90)
    f.mol(m, 110, 110)
    f.raw(f'<circle cx="110" cy="110" r="18" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    f.text(110, 111, "+", size=15)
    f.cap(110, 180, "ㄱ: 메틸트로필륨")
    f.text(110, 200, "6π 방향족 (Hückel), + 7개 C에 분산", size=11, color=GREEN)
    f.text(250, 110, ">", size=26, weight="bold")
    # ㄷ: cumyl
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("m1", c, 30)
    m.sub("m2", c, 150)
    phenyl_at(m, "p", c, 270)
    f.mol(m, 390, 60)
    f.charge(390, 43, "+")
    f.cap(390, 200, "ㄷ: 큐밀 (3°, 벤질)")
    f.text(390, 218, "공명으로 o, p 탄소에 분산", size=11)
    f.text(510, 110, ">", size=26, weight="bold")
    # ㄴ: t-butyl
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("m1", c, 90)
    m.sub("m2", c, 210)
    m.sub("m3", c, 330)
    f.mol(m, 650, 110)
    f.charge(664, 104, "+")
    f.cap(650, 180, "ㄴ: tert-뷰틸 (3°)")
    f.text(650, 200, "초공액·유발 효과만", size=11)
    return f.render()


# ---------------------------------------------------------- 2000 #10
def f2000_10():
    f = Fig(800, 260)
    f.text(400, 18, "CH₃CH₂CH₂CH₃ → CH₃CHClCH₂CH₃ (C* 1개) → CH₃CHClCHClCH₃ (C* 2개, 2,3-dichlorobutane)", size=12)
    fischer(f, 110, 90, [("Cl", "H"), ("H", "Cl")], hl="Cl")
    f.cap(110, 205, "(2R,3R)")
    fischer(f, 290, 90, [("H", "Cl"), ("Cl", "H")], hl="Cl")
    f.cap(290, 205, "(2S,3S)")
    f.raw(f'<line x1="200" y1="45" x2="200" y2="185" stroke="{GRAY}" stroke-dasharray="4 4"/>')
    f.text(200, 38, "거울", size=11, color=GRAY)
    f.text(200, 232, "한 쌍의 거울상 이성질체 (광학 활성)", size=12)
    fischer(f, 560, 90, [("H", "Cl"), ("H", "Cl")], hl="Cl")
    f.raw(f'<line x1="505" y1="113" x2="620" y2="113" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="6 4"/>')
    f.text(632, 113, "대칭면", size=11, color=BLUE, anchor="start")
    f.cap(560, 205, "meso-(2R,3S)")
    f.text(560, 232, "메소 화합물 (광학 비활성)", size=12)
    return f.render()


# ---------------------------------------------------------- 1999 #8
def _tbu(m, p, x, y, lab=None):
    c = m.atom(p, x, y, lab)
    m.sub(p + "a", c, 90)
    m.sub(p + "b", c, 210)
    m.sub(p + "c", c, 330)
    return c


def f1999_8_scheme():
    f = Fig(800, 200)
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("a", c, 150)
    m.sub("b", c, 210)
    m.sub("d", c, 270)
    m.sub("cl", c, 30, "Cl")
    f.mol(m, 70, 90)
    f.curly(78, 80, 104, 66, bend=-0.6)
    f.arrow(135, 90, 220, 90, "① 이온화", "느림 (RDS)", color=RED)
    m = Mol()
    _tbu(m, "t", 0, 0)
    f.mol(m, 265, 90)
    f.charge(281, 83)
    f.text(300, 120, "+ Cl^−", size=12)
    f.text(223, 150, "3° 탄소 양이온 (sp², 평면)", size=11)
    f.arrow(335, 90, 420, 90, "② H_2O 공격", "빠름")
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("a", c, 150)
    m.sub("b", c, 210)
    m.sub("d", c, 270)
    o = m.sub("o", c, 30, "O^+")
    m.sub("h1", o, 90, "H")
    m.sub("h2", o, -30, "H")
    f.mol(m, 470, 95)
    f.text(465, 150, "옥소늄 이온", size=11)
    f.arrow(540, 90, 625, 90, "③ H_2O", "양성자 이동 (빠름)")
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("a", c, 150)
    m.sub("b", c, 210)
    m.sub("d", c, 270)
    m.sub("o", c, 30, "OH")
    f.mol(m, 680, 95)
    f.text(705, 150, "+ H_3O^+", size=12)
    f.cap(400, 185, "(CH₃)₃C–Cl + 2 H₂O → (CH₃)₃C–OH + H₃O⁺ + Cl⁻     속도 = k[(CH₃)₃CCl]")
    return f.render()


def f1999_8_energy():
    f = Fig(800, 270)
    axes(f, 90, 240, 640, 220)
    pts = [(110, 190), (230, 60), (330, 140), (420, 110), (500, 165), (570, 150), (650, 215), (720, 215)]
    energy_curve(f, pts)
    f.text(230, 48, "TS1 (가장 높음)", size=12, color=RED, weight="bold")
    f.text(420, 98, "TS2", size=12)
    f.text(570, 138, "TS3", size=12)
    f.text(330, 158, "(CH₃)₃C⁺", size=12)
    f.text(500, 183, "(CH₃)₃COH₂⁺", size=12)
    f.text(130, 205, "(CH₃)₃CCl", size=12)
    f.text(690, 230, "(CH₃)₃COH", size=12)
    f.raw(f'<line x1="120" y1="190" x2="230" y2="190" stroke="{GRAY}" stroke-dasharray="3 3"/>')
    f.arrow(215, 188, 215, 64, color=RED)
    f.text(205, 130, "E_a1", size=12, color=RED, anchor="end")
    return f.render()


# ================================================================== 단원 6
# ---------------------------------------------------------- 2008 #15
def f2008_15_a():
    f = Fig(800, 420)
    # 1행: 기질 → 2° 양이온 → 3° 벤질 양이온
    def core(m, p, c3lab=None):
        c2 = m.atom(p + "2", 0, 0)
        m.sub(p + "1", c2, 150)
        m.sub(p + "m", c2, 90)
        phenyl_at(m, p + "P", c2, 270)
        c3 = m.sub(p + "3", c2, 30, c3lab)
        m.sub(p + "4", c3, -30)
        return c2, c3
    m = Mol()
    c2, c3 = core(m, "a")
    m.sub("cl", c3, 90, "Cl")
    f.mol(m, 70, 70)
    f.cap(125, 200, "3-chloro-2-methyl-2-phenylbutane")
    f.arrow(160, 70, 225, 70, "−Cl^−", "이온화")
    m = Mol()
    c2, c3 = core(m, "b")
    f.mol(m, 275, 70)
    x3, y3 = P(m, c3, 275, 70)
    f.charge(x3 + 2, y3 - 13)
    xm, ym = P(m, "bm", 275, 70)
    f.curly(xm + 4, ym + 12, x3 - 6, y3 - 4, bend=0.5)
    f.cap(290, 200, "2° 양이온 (불안정)")
    f.arrow(345, 70, 440, 70, "1,2-CH_3 이동", "")
    # 3° 벤질 양이온
    m = Mol()
    c2 = m.atom("c2", 0, 0)
    m.sub("c1", c2, 150)
    phenyl_at(m, "P", c2, 270)
    c3 = m.sub("c3", c2, 30)
    m.sub("c4", c3, -30)
    m.sub("c5", c3, 90)
    f.mol(m, 500, 70)
    f.charge(500, 54)
    f.cap(520, 200, "3° 벤질 양이온 (공명 안정화)")
    f.text(640, 60, "C⁺: Ph, CH₃, CH(CH₃)₂", size=11, anchor="start")
    # 2행: S_N1, E1
    f.raw(f'<line x1="20" y1="222" x2="780" y2="222" stroke="#e5e7eb"/>')
    f.arrow(40, 300, 120, 300, "CH_3OH, −H^+", "S_N1 (느림)")
    m = Mol()
    c2 = m.atom("c2", 0, 0)
    m.sub("c1", c2, 150)
    phenyl_at(m, "P", c2, 270)
    m.sub("o", c2, 90, "OCH_3")
    c3 = m.sub("c3", c2, 30)
    m.sub("c4", c3, -30)
    m.sub("c5", c3, 90)
    f.mol(m, 170, 285)
    f.text(200, 395, "부생성물: 2-methoxy-3-methyl-2-phenylbutane", size=12, color=GRAY)
    f.text(200, 412, "C⁺ 주변이 붐벼(Ph, CH₃, iPr) CH₃OH 접근 불리", size=10.5, color=GRAY)
    f.arrow(410, 300, 490, 300, "CH_3OH (염기), −H^+", "E1 (빠름)")
    m = Mol()
    c2 = m.atom("c2", 0, 0)
    m.sub("c1", c2, 150)
    phenyl_at(m, "P", c2, 270)
    c3 = m.sub("c3", c2, 30, kind="2")
    m.sub("c4", c3, -30)
    m.sub("c5", c3, 90)
    f.mol(m, 550, 285)
    f.cap(590, 395, "주생성물: 2-methyl-3-phenylbut-2-ene (E1)", color=GREEN)
    f.text(690, 290, "Zaitsev: 사치환", size=11, anchor="start")
    f.text(690, 306, "(Ph와 공액)", size=11, anchor="start")
    f.text(690, 322, "C3–H 제거", size=11, anchor="start")
    return f.render()


def f2008_15_b():
    f = Fig(800, 210)
    m = Mol()
    ch = zig(m, "c", 0, 0, 4)
    m.sub("i", "c2", 90, "I", kind="h")
    f.mol(m, 40, 100)
    f.cap(85, 160, "(S)-2-iodobutane")
    f.arrow(150, 100, 225, 100, "H_2O", "−I^−")
    m = Mol()
    ch = zig(m, "c", 0, 0, 4)
    f.mol(m, 255, 100)
    x, y = P(m, "c2", 255, 100)
    f.charge(x, y - 14)
    f.cap(300, 160, "평면 2° 양이온")
    f.text(300, 180, "양쪽 면 공격 가능", size=11)
    f.arrow(370, 90, 450, 60, "위", "")
    f.arrow(370, 110, 450, 140, "", "아래")
    m = Mol()
    zig(m, "c", 0, 0, 4)
    m.sub("o", "c2", 90, "OH", kind="w")
    f.mol(m, 480, 60)
    f.text(620, 55, "(R)-butan-2-ol", size=12, anchor="start")
    m = Mol()
    zig(m, "c", 0, 0, 4)
    m.sub("o", "c2", 90, "OH", kind="h")
    f.mol(m, 480, 155)
    f.text(620, 150, "(S)-butan-2-ol", size=12, anchor="start")
    f.text(620, 195, "→ 라셈화 (S_N1)", size=12, anchor="start", color=GREEN, weight="bold")
    return f.render()


# ================================================================== 단원 7
def f2011_35():
    f = Fig(800, 250)
    f.text(400, 18, "속도 결정 단계: 알켄 π 전자가 Br₂를 공격 → 브로모늄 이온(양전하가 치환된 탄소에 치우침)", size=12)
    items = [("B", "Ph", "벤질 위치: 페닐 공명으로 δ+ 안정화", GREEN),
             ("C", "CH_2CH_3", "알킬 전자 주개(+I, 초공액)", INK),
             ("A", "Br", "전기음성 Br의 −I → π 전자 밀도 감소", RED)]
    for i, (lab, R, note, col) in enumerate(items):
        x = 60 + i * 260
        m = Mol()
        a = m.atom("a", 0, 0)
        b = m.atom("b", 40, 0)
        m.bond(a, b)
        br = m.atom("br", 20, -32, "Br^+")
        m.bond(a, br, "dash")
        m.bond(b, br)
        if R == "Ph":
            phenyl_at(m, "p", a, 210)
        else:
            m.sub("r", a, 210, R, anchor="end" if len(R) > 2 else "middle")
        f.mol(m, x + 90, 110)
        f.text(x + 90 + 2, 125, "δ+", size=11, color=col)
        f.cap(x + 100, 190, f"{lab}  (R = {R})", color=col)
        f.text(x + 100, 210, note, size=11)
        if i < 2:
            f.text(x + 230, 110, ">", size=26, weight="bold")
    f.text(400, 238, "반응 속도: B > C > A  (③)", size=13, weight="bold", color=GREEN)
    return f.render()


def f2010_36():
    f = Fig(800, 300)
    # ㄱ: 수소화 엔탈피 준위
    f.text(130, 18, "ㄱ ✗  수소화 |ΔH°|", size=13, weight="bold", color=RED)
    f.raw(f'<line x1="30" y1="60" x2="110" y2="60" stroke="{INK}" stroke-width="2"/>')
    f.raw(f'<line x1="150" y1="92" x2="230" y2="92" stroke="{INK}" stroke-width="2"/>')
    f.raw(f'<line x1="30" y1="250" x2="230" y2="250" stroke="{INK}" stroke-width="2"/>')
    f.text(70, 48, "1,4-pentadiene", size=11)
    f.text(190, 80, "(E)-1,3-pentadiene", size=11)
    f.text(130, 265, "pentane", size=11)
    f.arrow(70, 62, 70, 247)
    f.arrow(190, 94, 190, 247)
    f.text(76, 160, "254", size=11, anchor="start")
    f.text(196, 170, "226", size=11, anchor="start")
    f.text(130, 285, "(kJ/mol) 공액 다이엔이 약 28 kJ 더 안정", size=11)
    # ㄴ
    f.text(400, 18, "ㄴ ○  산 촉매 수화 속도", size=13, weight="bold", color=GREEN)
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("a", c, 150)
    m.sub("b", c, 30)
    f.mol(m, 330, 90)
    f.charge(330, 105)
    f.text(330, 120, "propene → 2° C⁺", size=11)
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("a", c, 150)
    m.sub("b", c, 30)
    m.sub("d", c, 270)
    f.mol(m, 470, 90)
    f.charge(470, 73)
    f.text(470, 140, "isobutylene → 3° C⁺", size=11)
    f.text(400, 90, "<", size=20, weight="bold")
    f.text(400, 175, "RDS = 양성자 첨가(탄소 양이온 형성)", size=11)
    f.text(400, 193, "3° 양이온 TS가 더 낮음 → 빠름", size=11)
    # ㄷ: HOMO
    f.text(670, 18, "ㄷ ○  Diels–Alder 속도", size=13, weight="bold", color=GREEN)
    f.raw(f'<line x1="570" y1="80" x2="630" y2="80" stroke="{BLUE}" stroke-width="2"/>')
    f.text(600, 68, "MVK LUMO", size=11, color=BLUE)
    f.raw(f'<line x1="660" y1="200" x2="720" y2="200" stroke="{INK}" stroke-width="2"/>')
    f.raw(f'<line x1="700" y1="175" x2="760" y2="175" stroke="{RED}" stroke-width="2"/>')
    f.text(690, 216, "butadiene HOMO", size=11)
    f.text(735, 162, "2,3-Me₂ HOMO", size=11, color=RED)
    f.raw(f'<line x1="630" y1="80" x2="660" y2="200" stroke="{GRAY}" stroke-dasharray="3 3"/>')
    f.raw(f'<line x1="630" y1="80" x2="700" y2="175" stroke="{RED}" stroke-dasharray="3 3"/>')
    f.text(670, 250, "CH₃(전자 주개)가 HOMO를 올려", size=11)
    f.text(670, 267, "HOMO–LUMO 간격 감소 → 빠름", size=11)
    return f.render()


# ---------------------------------------------------------- 2009 #23
def _mch(m, p, x=0, y=0):
    """cyclohexane: p1 = C1(오른쪽 위, CH3 자리), p0 = C2(위)"""
    return m.ring(p, x, y, 6, L, 90)


def f2009_23():
    f = Fig(800, 250)
    data = []
    m = Mol()
    _mch(m, "r")
    m.sub("me", "r1", 60)
    m.sub("i", "r1", 0, "I")
    data.append((m, "a ✗", "HI: Markovnikov", "3° 탄소에 I (보기는 2°)", RED))
    m = Mol()
    _mch(m, "r")
    m.sub("me", "r1", 20, kind="w")
    m.sub("oh", "r0", 100, "OH", kind="h")
    data.append((m, "b ✗", "syn 첨가, 역-Markovnikov", "trans (보기는 cis)", RED))
    m = Mol()
    _mch(m, "r")
    x0, y0 = m.pos("r0")
    x1, y1 = m.pos("r1")
    m.atom("o", (x0 + x1) / 2 + 22, (y0 + y1) / 2 - 13, "O")
    m.bond("r0", "o")
    m.bond("r1", "o")
    m.sub("me", "r1", -10, kind="w")
    data.append((m, "c ○", "과산 → 에폭사이드", "syn, 라셈", GREEN))
    m = Mol()
    _mch(m, "r")
    m.sub("oh1", "r1", 0, "OH", kind="w")
    m.sub("me", "r1", 55, kind="h")
    m.sub("oh2", "r0", 110, "OH", kind="w")
    data.append((m, "d ○", "차가운 KMnO₄: syn", "cis-다이올", GREEN))
    m = Mol()
    _mch(m, "r")
    m.sub("br1", "r1", 0, "Br", kind="w")
    m.sub("me", "r1", 55, kind="h")
    m.sub("br2", "r0", 110, "Br", kind="h")
    data.append((m, "e ○", "브로모늄 → anti", "trans-이브로민화물", GREEN))
    for i, (m, t, l1, l2, col) in enumerate(data):
        x = 20 + i * 156
        f.box(x, 20, 148, 210, fill="#fff", stroke="#e5e7eb")
        f.mol(m, x + 64, 115)
        f.cap(x + 74, 180, t, color=col)
        f.text(x + 74, 200, l1, size=10.5)
        f.text(x + 74, 216, l2, size=10.5, color=col)
    f.text(400, 243, "올바른 것: c, d, e → ⑤", size=13, weight="bold", color=GREEN)
    return f.render()


# ---------------------------------------------------------- 2008 #12
def _benz(m, p, x=0, y=0):
    return benzene(m, p, x, y, start=90)  # p1(오른쪽 위), p2(오른쪽 아래)


def _indene(m, p, x=0, y=0):
    """벤젠 + 5원 고리.  5원 고리 원자 p5a(C1, 위), p5b(C2), p5c(C3, 아래)"""
    _benz(m, p, x, y)
    names, c = ring_on_edge(m, p + "5", p + "1", p + "2", 5, (x, y))
    # ring_on_edge는 a2(p2)부터: p51(C3), p52(C2), p53(C1)
    return {"C3": names[0], "C2": names[1], "C1": names[2], "c": c}


def f2008_12_a():
    f = Fig(800, 230)
    m = Mol()
    _benz(m, "b")
    new, c = ring_on_edge(m, "d", "b1", "b2", 6, (0, 0))
    # new: d1(b2쪽=C1), d2(C2), d3(C3), d4(C4, b1쪽)
    m.set_bond("d3", "d4", "in", c)
    f.mol(m, 50, 100)
    f.cap(80, 170, "1,2-dihydronaphthalene")
    f.arrow(140, 100, 240, 100, "OsO_4; NaHSO_3", "HIO_4 (C3=C4 절단)")
    m = Mol()
    _benz(m, "b")
    c1 = m.sub("a1", "b1", 30)
    m.sub("ao", c1, 90, "O", kind="2")
    c2 = m.sub("c1", "b2", -30)
    c3 = m.sub("c2", c2, 30)
    c4 = m.sub("c3", c3, -30)
    m.sub("co", c4, 30, "O", kind="2")
    f.mol(m, 290, 100)
    f.cap(330, 170, "A: 2-(3-oxopropyl)benzaldehyde")
    f.text(330, 188, "C₁₀H₁₀O₂, Tollens (+)", size=11)
    xa, ya = P(m, "c2", 290, 100)
    f.text(xa, ya + 20, "α-H", size=11, color=RED)
    f.arrow(430, 100, 520, 100, "NaOH, EtOH", "분자 내 aldol 축합")
    m = Mol()
    I = _indene(m, "i")
    m.set_bond(I["C2"], I["C3"], "in", I["c"])
    m.sub("cho", I["C2"], 0, "CHO", anchor="start")
    f.mol(m, 580, 100)
    f.cap(640, 170, "B: 1H-indene-2-carbaldehyde")
    f.text(640, 188, "C₁₀H₈O (−H₂O), Tollens (+)", size=11)
    f.text(400, 220, "알데하이드 CH₂ α-탄소 엔올레이트 → 방향족 CHO 공격 → 5원 고리 → 탈수(벤젠과 공액된 α,β-불포화 알데하이드)", size=11, color=GRAY)
    return f.render()


def f2008_12_b():
    f = Fig(800, 420)
    m = Mol()
    I = _indene(m, "i")
    m.set_bond(I["C2"], I["C3"], "in", I["c"])
    v1 = m.sub("v1", I["C2"], 30)
    m.sub("v2", v1, -30, kind="2")
    f.mol(m, 60, 100)
    f.cap(110, 170, "2-vinylindene (다이엔)")
    f.text(240, 100, "+", size=18)
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.atom("b", 32, 0)
    m.bond(a, b, "2")
    e1 = m.sub("e1", a, 240, "CO_2CH_3", anchor="end")
    e2 = m.sub("e2", b, 300, "CO_2CH_3", anchor="start")
    m.sub("h1", a, 120, "H")
    m.sub("h2", b, 60, "H")
    f.mol(m, 320, 100)
    f.cap(336, 170, "C: dimethyl maleate (cis)", color=GREEN)
    f.text(336, 188, "C₆H₈O₄", size=11)
    f.arrow(470, 100, 560, 100, "Δ", "[4+2] 협동")
    f.text(600, 90, "다이엔 말단: 비닐 CH₂, 인덴 C3", size=11, anchor="start")
    f.text(600, 108, "새 C=C: 인덴 C2 = 비닐 CH", size=11, anchor="start")
    def adduct(m, lab):
        I = _indene(m, "i")
        new, c = ring_on_edge(m, "h", I["C2"], I["C3"], 6, I["c"])
        m.set_bond(I["C2"], "h4", "in", c)
        m.sub("x1", "h1", 250, lab, kind="h", anchor="middle")
        m.sub("x2", "h2", 320, lab, kind="h", anchor="start")
        m.sub("hh", I["C3"], 215, "H", kind="w", length=24)
        return I
    f.raw('<line x1="20" y1="210" x2="780" y2="210" stroke="#e5e7eb"/>')
    m = Mol()
    adduct(m, "CO_2CH_3")
    f.mol(m, 80, 270)
    f.cap(150, 385, "DA 부가물 (두 에스터 cis)")
    f.arrow(300, 290, 400, 290, "(1) LiAlH_4 (2 eq)", "(2) H_3O^+")
    m = Mol()
    adduct(m, "CH_2OH")
    f.mol(m, 470, 270)
    f.cap(540, 385, "D: 다이올 C₁₅H₁₈O₂", color=GREEN)
    f.text(400, 405, "C₁₁H₁₀ + C₆H₈O₄ = C₁₇H₁₈O₄ → 2 CO₂CH₃ → 2 CH₂OH : C₁₅H₁₈O₂ ✓", size=11.5, color=GRAY)
    return f.render()


# ---------------------------------------------------------- 2006 #10
def f2006_10_a():
    f = Fig(800, 260)
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 0, kind="2")
    m.sub("pa", a, 120, "C_6H_5", anchor="end")
    m.sub("ha", a, 240, "H")
    m.sub("pb", b, -60, "C_6H_5", anchor="start")
    m.sub("hb", b, 60, "H")
    f.mol(m, 60, 110)
    f.cap(75, 180, "trans-stilbene")
    f.arrow(150, 110, 230, 110, "Br_2", "anti 첨가")
    # 브로모늄
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.atom("b", 40, 0)
    m.bond(a, b)
    br = m.atom("br", 20, -32, "Br^+")
    m.bond(a, br)
    m.bond(b, br)
    m.sub("pa", a, 235, "Ph", kind="w")
    m.sub("ha", a, 165, "H", kind="h", length=24)
    m.sub("pb", b, 305, "Ph", kind="h")
    m.sub("hb", b, 15, "H", kind="w", length=24)
    f.mol(m, 280, 115)
    f.text(300, 175, "Br^−", size=13, color=BLUE)
    f.text(300, 195, "(아래쪽에서 공격)", size=11, color=BLUE)
    f.cap(300, 220, "브로모늄 이온")
    f.arrow(370, 110, 440, 110, "", "")
    # 톱질대 A (anti-Br, 메소)
    sawhorse(f, 530, 145, [(90, "Br"), (210, "Ph"), (330, "H")], [(270, "Br"), (30, "Ph"), (150, "H")])
    f.cap(560, 225, "A: meso-1,2-dibromo-1,2-diphenylethane")
    f.text(560, 243, "(1R,2S) — 대칭 중심(i) → 비카이랄", size=11, color=GREEN)
    f.text(660, 70, "Br anti Br", size=11, anchor="start")
    f.text(660, 86, "Ph anti Ph", size=11, anchor="start")
    f.text(660, 102, "H anti H", size=11, anchor="start")
    return f.render()


def f2006_10_b():
    f = Fig(800, 250)
    newman(f, 110, 120, [(90, "Br"), (210, "Ph"), (330, "H")], [(270, "H"), (30, "Br"), (150, "Ph")],
           colors={("f", 0): RED, ("b", 0): RED})
    f.text(110, 30, "A의 E2 형태: H(뒤)와 Br(앞) anti", size=12)
    f.text(45, 215, "B:^−", size=13, color=BLUE)
    f.curly(60, 210, 102, 180, bend=-0.3, color=BLUE)
    f.text(110, 240, "두 Ph는 같은 쪽(왼쪽)에 놓임", size=11)
    f.arrow(215, 120, 320, 120, "염기", "−HBr (E2)")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 0, kind="2", length=34)
    m.sub("pa", a, 120, "C_6H_5", anchor="end")
    m.sub("ha", a, 240, "H")
    m.sub("pb", b, 60, "C_6H_5", anchor="start")
    m.sub("bb", b, -60, "Br")
    f.mol(m, 420, 120)
    f.cap(440, 200, "B: (E)-1-bromo-1,2-diphenylethene", color=GREEN)
    f.text(440, 220, "(두 Ph는 cis, Br은 Ph와 trans)", size=11)
    f.text(640, 90, "Z는 생성 ✗:", size=12, anchor="start", color=RED)
    f.text(640, 108, "anti-periplanar H가", size=11, anchor="start")
    f.text(640, 124, "하나뿐(입체 특이적)", size=11, anchor="start")
    return f.render()


# ---------------------------------------------------------- 2005 #10 (상이동 촉매)
def _cyclopropanate(m, p, x, y, lab="Cl"):
    r = m.ring(p, x, y, 6, L, 90)
    # 오른쪽 변 p1–p2에 3원 고리
    x1, y1 = m.pos(p + "1")
    x2, y2 = m.pos(p + "2")
    cx = (x1 + x2) / 2 + 26
    m.atom(p + "c", cx, (y1 + y2) / 2)
    m.bond(p + "1", p + "c")
    m.bond(p + "2", p + "c")
    m.sub(p + "x1", p + "c", 40, lab)
    m.sub(p + "x2", p + "c", -40, lab)
    return r


def f2005_10():
    f = Fig(800, 330)
    # 두 상 상자
    f.box(20, 20, 480, 130, fill="#fdf8ec", stroke="#e8d7a8")
    f.box(20, 170, 480, 110, fill="#eef4fc", stroke="#a9c1e6")
    f.text(30, 36, "유기층 (CHCl₃ + cyclohexene)", size=12, anchor="start", weight="bold")
    f.text(30, 186, "수용액층 (50% NaOH)", size=12, anchor="start", weight="bold")
    f.raw(f'<line x1="20" y1="160" x2="500" y2="160" stroke="{GRAY}" stroke-dasharray="6 4"/>')
    f.text(505, 160, "계면", size=11, color=GRAY, anchor="start")
    f.text(260, 70, "Q⁺ ⁻CCl₃  →  :CCl₂ + Q⁺Cl⁻   (α-제거)", size=13)
    f.text(260, 100, ":CCl₂ + cyclohexene → 생성물 (syn 고리 첨가)", size=13)
    f.text(260, 130, "CHCl₃ + Q⁺OH⁻ → Q⁺⁻CCl₃ + H₂O", size=12, color=GRAY)
    f.text(260, 215, "Na⁺ OH⁻ (유기층에 녹지 않음)", size=13)
    f.text(260, 245, "Q⁺Cl⁻ + NaOH ⇌ Q⁺OH⁻ + NaCl", size=13)
    f.arrow(455, 250, 455, 60, color=BLUE)
    f.text(448, 40, "Q⁺가 음이온 운반", size=11, color=BLUE, anchor="end")
    f.text(260, 300, "Q⁺ = PhCH₂N⁺Et₃ (지용성 유기 양이온 + 이온성 머리)", size=12)
    # 생성물
    m = Mol()
    _cyclopropanate(m, "r", 0, 0)
    f.mol(m, 610, 120)
    f.cap(650, 200, "7,7-dichlorobicyclo[4.1.0]heptane", color=GREEN)
    f.text(650, 220, "(cis 융합, 메소)", size=11)
    return f.render()


# ---------------------------------------------------------- 2004 #8
def f2004_8():
    f = Fig(800, 250)
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("a", c, 150)
    m.sub("b", c, 210)
    m.sub("d", c, 0, kind="2")
    f.mol(m, 55, 125)
    f.text(62, 165, "2-methylpropene", size=11, weight="bold")
    prods = []
    # A
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("a", c, 90)
    m.sub("b", c, 210)
    m.sub("o", c, 150, "HO", anchor="end")
    x = m.sub("x", c, -30)
    m.sub("br", x, 30, "Br")
    prods.append((m, "A: Br₂/H₂O", "1-bromo-2-methylpropan-2-ol", "브로모늄 → H₂O가 3° 탄소 공격"))
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("a", c, 90)
    m.sub("b", c, 210)
    x = m.sub("x", c, -30)
    m.sub("o", x, 30, "OH")
    prods.append((m, "B: BH₃; H₂O₂/OH⁻", "2-methylpropan-1-ol", "역-Markovnikov, syn"))
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("a", c, 90)
    m.sub("b", c, 210)
    x = m.sub("x", c, -30)
    m.sub("br", x, 30, "Br")
    prods.append((m, "C: HBr/H₂O₂", "1-bromo-2-methylpropane", "라디칼, 역-Markovnikov"))
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("a", c, 150)
    m.sub("b", c, 210)
    d = m.atom("d", 34, 0)
    m.bond(c, d)
    o = m.atom("o", 17, -26, "O")
    m.bond(c, o)
    m.bond(d, o)
    prods.append((m, "D: C₆H₅CO₃H", "2,2-dimethyloxirane", "협동 산소 전달"))
    for i, (m, t, name, note) in enumerate(prods):
        x = 140 + i * 162
        f.box(x, 25, 152, 205, fill="#fff", stroke="#e5e7eb")
        f.text(x + 76, 45, t, size=11.5, weight="bold")
        f.mol(m, x + 62, 125)
        f.text(x + 76, 190, name, size=10.5, color=GREEN)
        f.text(x + 76, 210, note, size=10)
    return f.render()


# ---------------------------------------------------------- 2002 #12
def f2002_12_mech():
    f = Fig(800, 240)
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.set_bond("r1", "r2", "in", (0, 0))
    f.mol(m, 60, 110)
    f.text(140, 60, "Br–Br", size=13)
    f.curly(95, 100, 128, 68, bend=-0.4)
    f.curly(145, 52, 168, 40, bend=-0.6)
    f.arrow(180, 110, 250, 110, "CCl_4", "")
    # 브로모늄 (Br 위 = 쐐기)
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    x1, y1 = m.pos("r1")
    x2, y2 = m.pos("r2")
    m.atom("br", (x1 + x2) / 2 + 28, (y1 + y2) / 2, "Br^+")
    m.bond("r1", "br", "w")
    m.bond("r2", "br", "w")
    f.mol(m, 300, 110)
    f.text(350, 175, "Br^−", size=13, color=BLUE)
    f.curly(350, 162, 328, 130, bend=0.3, color=BLUE)
    f.text(320, 200, "고리형 브로모늄 (위 면)", size=11)
    f.text(320, 216, "Br⁻는 반대(아래) 면에서 S_N2", size=11, color=BLUE)
    f.arrow(410, 110, 480, 110, "anti", "")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.sub("b1", "r1", 30, "Br", kind="w")
    m.sub("b2", "r2", -30, "Br", kind="h")
    f.mol(m, 540, 110)
    f.cap(560, 185, "(1R,2R)")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.sub("b1", "r1", 30, "Br", kind="h")
    m.sub("b2", "r2", -30, "Br", kind="w")
    f.mol(m, 690, 110)
    f.cap(710, 185, "(1S,2S)")
    f.text(635, 215, "trans-1,2-dibromocyclohexane (라셈, 1 : 1)", size=12, color=GREEN)
    return f.render()


def f2002_12_chair():
    f = Fig(800, 190)
    chair(f, 170, 95, {0: [("ax", "Br", RED)], 1: [("ax", "Br", RED)]})
    f.cap(170, 170, "처음 생성: trans-이축 (anti 공격)")
    f.eqarrow(330, 440, 95, "고리 뒤집기", "")
    chair(f, 600, 95, {0: [("eq", "Br", RED)], 1: [("eq", "Br", RED)]})
    f.cap(600, 170, "trans-이적도 (둘 다 trans)")
    return f.render()


# ---------------------------------------------------------- 2000 #15 (2)
def f2000_15():
    f = Fig(800, 220)
    f.text(70, 110, "CH_3–CH=CH_2", size=14)
    f.arrow(130, 95, 200, 55, "HBr", "")
    f.arrow(130, 125, 200, 165, "", "HBr, ROOR")
    f.text(220, 20, "친전자성 첨가 (Markovnikov)", size=12, anchor="start", weight="bold")
    f.box(220, 38, 165, 36, fill="#fff")
    f.text(302, 56, "CH_3–C^+H–CH_3", size=13)
    f.text(302, 90, "2° 탄소 양이온 (더 안정)", size=11)
    f.arrow(395, 56, 470, 56, "Br^−", "")
    f.box(480, 38, 175, 36, fill="#eef7f0", stroke="#9fd0ab")
    f.text(567, 56, "CH_3–CHBr–CH_3", size=13, color=GREEN)
    f.text(567, 90, "2-bromopropane", size=11, color=GREEN)
    f.text(220, 132, "라디칼 첨가 (역-Markovnikov)", size=12, anchor="start", weight="bold")
    f.box(220, 148, 165, 36, fill="#fff")
    f.text(302, 166, "CH_3–C•H–CH_2Br", size=13)
    f.text(302, 200, "Br•이 CH₂에 → 2° 라디칼", size=11)
    f.arrow(395, 166, 470, 166, "H–Br", "(+ Br•)")
    f.box(480, 148, 175, 36, fill="#eef7f0", stroke="#9fd0ab")
    f.text(567, 166, "CH_3–CH_2–CH_2Br", size=13, color=GREEN)
    f.text(567, 200, "1-bromopropane", size=11, color=GREEN)
    return f.render()


# ---------------------------------------------------------- 1999 #6
def _cp(m, p):
    r = m.ring(p, 0, 0, 5, L * 0.95, 90)
    return r


def f1999_6():
    f = Fig(800, 430)
    # 1행: OsO4
    m = Mol()
    _cp(m, "r")
    m.set_bond("r0", "r1", "in", (0, 0))
    f.mol(m, 50, 110)
    f.arrow(90, 110, 175, 110, "OsO_4, pyridine", "syn 첨가")
    m = Mol()
    _cp(m, "r")
    x0, y0 = m.pos("r0")
    x1, y1 = m.pos("r1")
    o1 = m.sub("o1", "r0", 110, "O", kind="w", length=26)
    o2 = m.sub("o2", "r1", 70, "O", kind="w", length=26)
    xa, ya = m.pos("o1")
    xb, yb = m.pos("o2")
    os_ = m.atom("os", (xa + xb) / 2, min(ya, yb) - 24, "Os")
    m.bond(o1, os_)
    m.bond(o2, os_)
    m.sub("oa", os_, 165, "O", kind="2", length=28)
    m.sub("ob", os_, 15, "O", kind="2", length=28)
    f.mol(m, 235, 125)
    f.cap(245, 180, "고리형 오스메이트 에스터")
    f.arrow(320, 110, 410, 110, "NaHSO_3, H_2O", "Os–O 절단")
    m = Mol()
    _cp(m, "r")
    m.sub("o1", "r0", 110, "OH", kind="w")
    m.sub("o2", "r1", 40, "OH", kind="w")
    f.mol(m, 470, 120)
    f.cap(490, 180, "cis-cyclopentane-1,2-diol (메소)", color=GREEN)
    f.raw('<line x1="20" y1="200" x2="780" y2="200" stroke="#e5e7eb"/>')
    # 2행: 옥시수은화
    m = Mol()
    _cp(m, "r")
    m.set_bond("r0", "r1", "in", (0, 0))
    f.mol(m, 50, 255)
    f.arrow(90, 255, 200, 255, "1. Hg(OAc)_2, H_2O", "2. NaBH_4")
    m = Mol()
    _cp(m, "r")
    m.sub("o", "r0", 90, "OH")
    f.mol(m, 250, 265)
    f.text(330, 265, "cyclopentanol (비카이랄)", size=13, weight="bold", color=GREEN, anchor="start")
    f.text(660, 245, "Markovnikov, 자리옮김 없음", size=11)
    f.text(660, 262, "대칭 알켄 → 입체 중심 없음", size=11)
    f.raw('<line x1="20" y1="305" x2="780" y2="305" stroke="#e5e7eb"/>')
    # 3행: 카벤
    m = Mol()
    _cp(m, "r")
    m.set_bond("r0", "r1", "in", (0, 0))
    f.mol(m, 50, 370)
    f.arrow(90, 370, 200, 370, "CHCl_3, KOH", ":CCl_2")
    m = Mol()
    _cp(m, "r")
    x0, y0 = m.pos("r0")
    x1, y1 = m.pos("r1")
    m.atom("c", (x0 + x1) / 2 + 16, (y0 + y1) / 2 - 22)
    m.bond("r0", "c")
    m.bond("r1", "c")
    m.sub("c1", "c", 100, "Cl")
    m.sub("c2", "c", 10, "Cl")
    m.sub("h0", "r0", 200, "H", kind="h", length=22)
    m.sub("h1", "r1", -40, "H", kind="h", length=22)
    f.mol(m, 250, 385)
    f.cap(470, 370, "6,6-dichlorobicyclo[3.1.0]hexane", color=GREEN)
    f.text(470, 390, "(cis 융합: 알켄 기하 보존, 메소)", size=11)
    return f.render()


# ---------------------------------------------------------- 1998 #12
def f1998_12():
    f = Fig(800, 200)
    items = []
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30, kind="2")
    c = m.sub("c", b, -30)
    m.sub("d", c, 30)
    items.append((m, "1-butene"))
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 30)
    c = m.sub("c", b, -30, kind="2")
    m.sub("d", c, 30)
    items.append((m, "trans-2-butene"))
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 60)
    c = m.sub("c", b, 0, kind="2")
    m.sub("d", c, -60)
    items.append((m, "cis-2-butene"))
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("a", c, 210)
    m.sub("b", c, 330)
    m.sub("d", c, 90, kind="2")
    items.append((m, "2-methylpropene"))
    m = Mol()
    m.ring("r", 0, 0, 4, L * 0.75, 45)
    items.append((m, "cyclobutane"))
    m = Mol()
    m.ring("r", 0, 0, 3, L * 0.6, 90)
    m.sub("me", "r1", -30)
    items.append((m, "methylcyclopropane"))
    for i, (m, nm) in enumerate(items):
        x = 60 + i * 130
        f.mol(m, x, 80)
        f.text(x + 12, 140, nm, size=11.5)
    f.raw(f'<rect x="20" y="25" width="520" height="130" rx="8" fill="none" stroke="{GREEN}" stroke-dasharray="5 4"/>')
    f.text(280, 170, "알켄 C₄H₈ (구조 이성질체 3가지, 2-butene은 cis/trans 기하 이성질체)", size=11, color=GREEN)
    f.text(680, 170, "고리형 C₄H₈ (알켄 아님)", size=11, color=GRAY)
    return f.render()


# ================================================================== 단원 8
def f2007_9():
    f = Fig(800, 330)
    # A: (R)-3-methylpent-1-yne
    def skel(m, left):
        c3 = m.atom("c3", 0, 0)
        m.sub("me", c3, 90, kind="h")
        c4 = m.sub("c4", c3, -30)
        m.sub("c5", c4, 30)
        return c3
    m = Mol()
    c3 = skel(m, None)
    c2 = m.sub("c2", c3, 210)
    m.sub("c1", c2, 210, kind=3)
    f.mol(m, 110, 90)
    f.cap(90, 150, "A: (R)-3-methylpent-1-yne")
    f.text(90, 168, "말단 ≡C–H (산성 H), C* 1개", size=11)
    f.arrow(200, 90, 290, 90, "H_3O^+, HgSO_4", "Markovnikov 수화")
    m = Mol()
    c3 = skel(m, None)
    c2 = m.sub("c2", c3, 210)
    m.sub("o", c2, 270, "O", kind="2")
    m.sub("c1", c2, 150)
    f.mol(m, 360, 90)
    f.cap(360, 150, "C: (R)-3-methylpentan-2-one", color=GREEN)
    f.text(360, 168, "C* 유지 → 광학 활성", size=11)
    f.text(600, 70, "H₂/Pt → 3-methylpentane", size=11, anchor="start")
    f.text(600, 88, "(두 에틸기 동일 → 비카이랄)", size=11, anchor="start")
    # B
    m = Mol()
    m.ring("r", 0, 0, 5, L * 0.95, 90)
    m.set_bond("r1", "r2", "in", (0, 0))
    m.sub("me", "r0", 90, kind="w")
    f.mol(m, 110, 260)
    f.cap(100, 315, "B: (R)-3-methylcyclopentene")
    f.arrow(200, 260, 290, 260, "1. O_3", "2. Zn/H_3O^+")
    m = Mol()
    c2 = m.atom("c2", 0, 0)
    m.sub("me", c2, 90, kind="h")
    c1 = m.sub("c1", c2, 210)
    m.sub("o1", c1, 150, "O", kind="2")
    c3 = m.sub("c3", c2, -30)
    c4 = m.sub("c4", c3, 30)
    c5 = m.sub("c5", c4, -30)
    m.sub("o5", c5, 30, "O", kind="2")
    f.mol(m, 360, 260)
    f.cap(400, 315, "D: (R)-2-methylpentanedial", color=GREEN)
    f.text(600, 240, "H₂/Pt → methylcyclopentane", size=11, anchor="start")
    f.text(600, 258, "(대칭면 → 비카이랄)", size=11, anchor="start")
    f.text(600, 276, "산성 H 없음 (말단 알카인 아님)", size=11, anchor="start")
    return f.render()


def f2006_12():
    f = Fig(800, 300)
    f.text(60, 60, "HC≡CH", size=14)
    f.arrow(105, 60, 185, 60, "1. NaNH_2", "2. CH_3I")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 0)
    m.sub("c", b, 0, kind=3)
    f.mol(m, 200, 60)
    f.text(230, 85, "propyne", size=11)
    f.arrow(270, 60, 360, 60, "1. NaNH_2", "2. CH_3CH_2Br")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 0)
    c = m.sub("c", b, 0, kind=3)
    d = m.sub("d", c, 0)
    m.sub("e", d, -45)
    f.mol(m, 375, 55)
    f.cap(430, 95, "B: pent-2-yne (C₅H₈)")
    f.arrow(500, 60, 580, 60, "H_2", "Lindlar (syn)")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 60)
    c = m.sub("c", b, 0, kind="2")
    d = m.sub("d", c, -60)
    m.sub("e", d, 0)
    f.mol(m, 610, 65)
    f.cap(660, 95, "C: (Z)-pent-2-ene (cis)")
    # 아래: A
    f.arrow(230, 105, 230, 175, "H_2SO_4, HgSO_4", "H_2O")
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("a", c, 210)
    m.sub("b", c, 330)
    m.sub("o", c, 90, "O", kind="2")
    f.mol(m, 230, 235)
    f.cap(230, 270, "A: acetone (propan-2-one)", color=GREEN)
    f.text(230, 288, "엔올 → 케토 토토머화", size=11)
    f.arrow(660, 105, 660, 175, "1. O_3", "2. Zn, H_3O^+")
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("a", c, 210)
    m.sub("o", c, 330, "O", kind="2")
    f.mol(m, 540, 225)
    f.text(560, 260, "acetaldehyde", size=11)
    f.text(600, 225, "+", size=16)
    m = Mol()
    c = m.atom("c", 0, 0)
    b = m.sub("b", c, 210)
    m.sub("a", b, 150)
    m.sub("o", c, 330, "O", kind="2")
    f.mol(m, 680, 225)
    f.cap(680, 270, "D: propanal (C₃H₆O)", color=GREEN)
    return f.render()


# ================================================================== 참고 해설 반영 추가 그림
# ---------------------------------------------------------- 2013 논술형 3: 용매 효과 에너지 도표
def f2013_3_energy():
    f = Fig(800, 270)
    axes(f, 70, 240, 420, 215, ylab="G", xlab="반응 좌표")
    # 전이 상태는 두 용매에서 비슷(전하 분산) — 반응물(친핵체) 준위만 다름
    energy_curve(f, [(80, 150), (280, 50), (480, 200)], color=RED)
    energy_curve(f, [(80, 200), (280, 60), (480, 215)], color=GREEN)
    f.raw(f'<line x1="80" y1="150" x2="150" y2="150" stroke="{RED}" stroke-dasharray="4 3"/>')
    f.raw(f'<line x1="80" y1="200" x2="150" y2="200" stroke="{GREEN}" stroke-dasharray="4 3"/>')
    f.arrow(250, 150, 250, 54, color=RED)
    f.arrow(310, 200, 310, 64, color=GREEN)
    f.text(244, 110, "E_a (작음)", size=11, anchor="end", color=RED)
    f.text(316, 140, "E_a (큼)", size=11, anchor="start", color=GREEN)
    f.text(90, 172, "DMF: '벗겨진' N₃⁻", size=11, anchor="start", color=RED)
    f.text(160, 212, "CH₃OH: H-결합으로 안정화된 N₃⁻", size=11, anchor="start", color=GREEN)
    f.text(280, 30, "[N₃···C···OTs]‡ (전하 분산 → 용매 영향 작음)", size=11)
    tbox(f, 520, 50, 260, ["DMF(극성 비양성자성)",
                            "N₃⁻ 용매화 약함 → 바닥 상태 높음",
                            "→ E_a 작음 → 빠름"], size=11.5, fill="#fdeeee", stroke="#e7a9a3", bold_first=True)
    tbox(f, 520, 150, 260, ["CH₃OH(양성자성)",
                             "N₃⁻···H–OCH₃ 수소 결합",
                             "→ 바닥 상태 낮아짐 → E_a 큼 → 느림"], size=11.5, fill="#eef7f0", stroke="#9fd0ab", bold_first=True)
    return f.render()


# ---------------------------------------------------------- 2012 #34: 이온화(rds) 단계
def f2012_34_ion():
    f = Fig(800, 210)
    # ㄴ t-BuBr
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("m1", c, 90)
    m.sub("m2", c, 210)
    m.sub("m3", c, 150, kind="w")
    m.sub("br", c, 330, "Br")
    f.mol(m, 70, 90)
    f.curly(70 + 14, 90 + 2, 70 + 38, 90 + 30, bend=0.5)
    f.text(80, 160, "ㄴ: (CH₃)₃C–Br", size=12, weight="bold")
    f.arrow(130, 90, 200, 90, "−Br^−", "slow")
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("m1", c, 90)
    m.sub("m2", c, 210)
    m.sub("m3", c, 330)
    f.mol(m, 230, 95)
    f.charge(244, 89)
    f.text(240, 160, "3° 양이온", size=11)
    f.text(240, 176, "공명 구조 없음", size=11, color=GRAY)
    # ㄷ cumyl bromide
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("m1", c, 150)
    m.sub("m2", c, 210, kind="w")
    m.sub("br", c, 330, "Br")
    phenyl_at(m, "p", c, 90)
    f.mol(m, 330, 140)
    f.curly(330 + 14, 140 + 2, 330 + 38, 140 + 30, bend=0.5)
    f.text(330, 195, "ㄷ: PhC(CH₃)₂–Br", size=12, weight="bold")
    f.arrow(380, 125, 440, 125, "−Br^−", "fast")
    f.text(410, 160, "3° + 벤질 공명", size=11)
    # ㄱ 7-bromo-7-methylcycloheptatriene
    m = Mol()
    m.ring("t", 0, 0, 7, L, 90)
    for a, b in (("t1", "t2"), ("t3", "t4"), ("t5", "t6")):
        m.set_bond(a, b, "in", (0, 0))
    m.sub("me", "t0", 150)
    m.sub("br", "t0", 30, "Br")
    f.mol(m, 540, 125)
    xb, yb = m.pos("br")
    x0, y0 = m.pos("t0")
    f.curly(540 + (x0 + xb) / 2 + 2, 125 + (y0 + yb) / 2 + 5, 540 + xb + 18, 125 + yb + 6, bend=0.7)
    f.text(560, 195, "ㄱ: 7-bromo-7-methylcycloheptatriene", size=11, weight="bold")
    f.arrow(610, 115, 680, 115, "−Br^−", "faster")
    m = Mol()
    m.ring("t", 0, 0, 7, L, 90)
    m.sub("me", "t0", 90)
    f.mol(m, 735, 115)
    f.raw(f'<circle cx="735" cy="115" r="17" fill="none" stroke="{INK}" stroke-width="1.3"/>')
    f.text(735, 116, "+", size=14)
    f.text(735, 180, "방향족(6π, 7p 공액)", size=11, color=GREEN)
    f.text(400, 20, "속도 결정 단계 = C–Br 이온화(흡열) → 생기는 양이온이 안정할수록 TS가 낮다", size=12)
    return f.render()


# ---------------------------------------------------------- 2013 #37: E2 전이상태와 S_N2 전이상태 비교
def _partial_double(f, x1, y1, x2, y2, off=4.5):
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)
    nx, ny = -dy / d * off, dx / d * off
    f.raw(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{INK}" stroke-width="1.4"/>')
    f.raw(f'<line x1="{x1 + nx:.1f}" y1="{y1 + ny:.1f}" x2="{x2 + nx:.1f}" y2="{y2 + ny:.1f}" stroke="{INK}" stroke-width="1.3" stroke-dasharray="3 3"/>')


def f2013_37():
    f = Fig(800, 400)
    f.text(20, 18, "ㄴ: E2 (C₂H₅O⁻ = 강염기)", size=12.5, anchor="start", weight="bold")
    # 반응물: Cβ–Cα, H(β)와 Br(α)가 anti-periplanar
    m = Mol()
    cb = m.atom("cb", 0, 0)
    ca = m.atom("ca", 44, 0)
    m.bond(cb, ca)
    m.sub("hb", cb, 90, "H")
    m.sub("h2", cb, 210, "H", kind="w", length=26)
    m.sub("h3", cb, 250, "H", kind="h", length=26)
    m.sub("br", ca, 270, "Br")
    m.sub("me", ca, 70, "CH_3", kind="w", length=30)
    m.sub("ha", ca, 20, "H", kind="h", length=26)
    f.mol(m, 50, 100)
    f.text(42, 60, "β", size=11, color=GRAY)
    f.text(108, 110, "α", size=11, color=GRAY)
    f.text(80, 175, "+ C₂H₅O⁻Na⁺", size=12)
    f.arrow(160, 100, 215, 100)
    # E2 전이상태
    ox, oy = 300, 122
    hx, hy = ox - 20, oy - 45
    cbx, cby, cax, cay = ox - 30, oy, ox + 18, oy
    f.text(ox - 70, oy - 80, "C_2H_5O", size=13, anchor="middle")
    f.text(ox - 70, oy - 97, "δ−", size=10, color=RED)
    f.raw(f'<line x1="{ox - 52}" y1="{oy - 72}" x2="{hx - 4}" y2="{hy - 5}" stroke="{RED}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    f.text(hx, hy, "H", size=13)
    f.raw(f'<line x1="{hx - 3}" y1="{hy + 9}" x2="{cbx}" y2="{cby - 4}" stroke="{INK}" stroke-width="1.4" stroke-dasharray="3 3"/>')
    _partial_double(f, cbx, cby, cax, cay)
    f.raw(f'<line x1="{cax + 2}" y1="{cay + 4}" x2="{cax + 18}" y2="{cay + 34}" stroke="{INK}" stroke-width="1.4" stroke-dasharray="3 3"/>')
    f.text(cax + 22, cay + 44, "Br", size=13)
    f.text(cax + 40, cay + 36, "δ−", size=10, color=RED)
    f.raw(f'<line x1="{cbx}" y1="{cby}" x2="{cbx - 22}" y2="{cby + 16}" stroke="{INK}" stroke-width="1.4"/>')
    f.text(cbx - 30, cby + 22, "H", size=12)
    f.raw(f'<line x1="{cbx}" y1="{cby}" x2="{cbx - 8}" y2="{cby + 26}" stroke="{INK}" stroke-width="1.4"/>')
    f.text(cbx - 10, cby + 36, "H", size=12)
    f.raw(f'<line x1="{cax}" y1="{cay}" x2="{cax + 14}" y2="{cay - 24}" stroke="{INK}" stroke-width="1.4"/>')
    f.text(cax + 22, cay - 33, "CH_3", size=12)
    f.raw(f'<line x1="{cax}" y1="{cay}" x2="{cax + 26}" y2="{cay - 6}" stroke="{INK}" stroke-width="1.4"/>')
    f.text(cax + 34, cay - 8, "H", size=12)
    f.text(cax - 2, cay + 16, "α", size=11, color=GRAY)
    f.text(cbx - 2, cby - 14, "β", size=11, color=GRAY)
    bracket(f, ox - 110, oy - 112, ox + 85, oy + 62)
    f.text(ox - 10, oy + 74, "anti-β-H 제거의 E2 전이 상태 (한 단계)", size=11)
    f.arrow(400, 100, 470, 100, "", "−EtOH, −Br^−")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 0, kind="2", length=36)
    m.sub("h1", a, 120, "H")
    m.sub("h2", a, 240, "H")
    m.sub("me", b, 60, "CH_3")
    m.sub("h3", b, -60, "H")
    f.mol(m, 520, 100)
    f.text(556, 125, "α", size=11, color=GRAY)
    f.text(538, 165, "propene: α 탄소 sp²", size=11.5, color=GREEN)
    tbox(f, 640, 40, 150, ["ㄱ ○ 속도 =", "k[RBr][EtO⁻]", "(m + n = 2)", "ㄴ ✗ sp³ → sp²"], size=11.5)
    f.raw(f'<line x1="20" y1="208" x2="780" y2="208" stroke="#e5e7eb"/>')
    # ㄷ: CH3CO2Na → S_N2
    f.text(20, 228, "ㄷ: CH₃CO₂⁻ = 약염기·친핵체 → S_N2 (뒷면 공격)", size=12.5, anchor="start", weight="bold")
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("br", c, 270, "Br")
    m.sub("m1", c, 150)
    m.sub("m2", c, 30)
    m.sub("h", c, 90, "H")
    f.mol(m, 80, 310)
    f.text(80, 375, "+ CH₃CO₂⁻Na⁺", size=12)
    f.arrow(150, 310, 210, 310)
    cx, cy = 300, 312
    m = Mol()
    c = m.atom("c", 0, 0)
    m.atom("o", 0, -46, "OAc")
    m.atom("br", 0, 46, "Br")
    m.bond("o", c, "form")
    m.bond(c, "br", "dash")
    m.sub("m1", c, 190, "H_3C", length=30, anchor="end")
    m.sub("m2", c, 345, "CH_3", kind="w", length=28, anchor="start")
    m.sub("h", c, 25, "H", kind="h", length=24)
    f.mol(m, cx, cy)
    f.text(cx - 26, cy - 52, "δ−", size=10, color=RED)
    f.text(cx - 24, cy + 52, "δ−", size=10, color=RED)
    bracket(f, cx - 70, cy - 70, cx + 72, cy + 66)
    f.arrow(400, 312, 470, 312, "", "−Br^−")
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("m1", c, 150)
    m.sub("m2", c, 210)
    o = m.sub("o", c, -30, "O")
    cc = m.sub("cc", o, 30)
    m.sub("co", cc, 90, "O", kind="2")
    m.sub("cm", cc, -30)
    f.mol(m, 510, 315)
    f.text(560, 370, "isopropyl acetate (치환 생성물)", size=11.5)
    tbox(f, 640, 260, 150, ["ㄷ ✗ 염기성↓ 친핵성↑", "→ 알켄 수득률 감소"], size=11.5)
    return f.render()


# ---------------------------------------------------------- 2005 #10: 다이클로로카벤 생성과 협동 첨가
def f2005_10_mech():
    f = Fig(800, 330)
    f.text(20, 18, "① 탈양성자화 → ② α-제거(−Cl⁻) → :CCl₂ (단일항: sp² 비공유쌍 + 빈 p 오비탈)", size=12, anchor="start", weight="bold")
    # CHCl3 + OH-
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("h", c, 0, "H")
    m.sub("c1", c, 90, "Cl")
    m.sub("c2", c, 180, "Cl")
    m.sub("c3", c, 270, "Cl")
    f.mol(m, 80, 95)
    f.text(160, 95, "HO^−", size=13, color=BLUE)
    f.lp(150, 82, 90)
    f.curly(150, 84, 116, 84, bend=0.5, color=BLUE)
    f.curly(97, 100, 84, 104, bend=-0.9)
    f.arrow(195, 95, 255, 95, "50% NaOH", "−H_2O")
    # -CCl3
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("c1", c, 90, "Cl")
    m.sub("c2", c, 180, "Cl")
    m.sub("c3", c, 270, "Cl")
    f.mol(m, 310, 95)
    f.lp(320, 95, 0)
    f.charge(326, 80, "−")
    f.curly(313, 108, 324, 124, bend=-0.6)
    f.text(310, 160, "trichloromethanide", size=11)
    f.arrow(360, 95, 420, 95, "−Cl^−", "α-제거")
    # :CCl2
    cx, cy = 490, 95
    f.porb(cx, cy, 0)
    f.lobe(cx, cy, up=True, filled=False)
    f.lobe(cx, cy, up=False, filled=False)
    f.raw(f'<ellipse cx="{cx - 16}" cy="{cy}" rx="13" ry="7" fill="#c0392b" fill-opacity="0.25" stroke="{RED}" stroke-width="1"/>')
    f.lp(cx - 16, cy, 90)
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("a", c, 30, "Cl")
    m.sub("b", c, -30, "Cl")
    f.mol(m, cx, cy)
    f.text(cx - 10, 150, "빈 p 오비탈(친전자성) + sp² 비공유쌍(친핵성)", size=11)
    f.text(cx - 34, cy - 30, "sp² LP", size=10, color=RED, anchor="end")
    f.text(cx + 10, cy - 36, "빈 p", size=10, color=BLUE, anchor="start")
    f.raw(f'<line x1="20" y1="175" x2="780" y2="175" stroke="#e5e7eb"/>')
    f.text(20, 195, "③ :CCl₂ + cyclohexene — 한 단계 협동 syn 첨가 (π → 빈 p, LP → 다른 탄소)", size=12, anchor="start", weight="bold")
    m = Mol()
    m.ring("r", 0, 0, 6, L, 90)
    m.set_bond("r1", "r2", "2l")
    f.mol(m, 110, 265)
    x1, y1 = P(m, "r1", 110, 265)
    x2, y2 = P(m, "r2", 110, 265)
    kx, ky = 230, 265
    m = Mol()
    c = m.atom("c", 0, 0)
    m.sub("a", c, 30, "Cl")
    m.sub("b", c, -30, "Cl")
    f.mol(m, kx, ky)
    f.lp(kx - 10, ky + 8, 200)
    f.lobe(kx, ky, up=True, filled=False, rx=6, ry=12)
    f.curly(x1 + 6, (y1 + y2) / 2 - 4, kx - 3, ky - 22, bend=-0.4)
    f.curly(kx - 14, ky + 12, x2 + 6, y2 + 4, bend=-0.4)
    f.text(175, 318, "협동(동시) — 알켄 기하 보존", size=11)
    f.arrow(300, 265, 400, 265, "", "")
    m = Mol()
    _cyclopropanate(m, "p", 0, 0)
    f.mol(m, 470, 265)
    f.text(580, 255, "7,7-dichlorobicyclo[4.1.0]heptane", size=12, color=GREEN, weight="bold", anchor="start")
    f.text(580, 275, "두 새 C–C 결합이 같은 면 → cis 융합", size=11, anchor="start")
    return f.render()


# ---------------------------------------------------------- 2006 #10: anti(빠름) vs syn(느림) E2
def f2006_10_c():
    f = Fig(800, 300)
    # anti-periplanar
    cx, cy = 120, 140
    newman(f, cx, cy, [(90, "Br"), (210, "Ph"), (330, "H")], [(270, "H"), (30, "Br"), (150, "Ph")],
           colors={("f", 0): RED, ("b", 0): RED})
    f.text(cx, 28, "anti-periplanar (엇갈린 형태)", size=12, weight="bold", color=RED)
    f.text(cx - 75, cy + 70, "EtO^−", size=12, color=BLUE)
    f.curly(cx - 58, cy + 64, cx - 6, cy + 58, bend=-0.3, color=BLUE)
    f.curly(cx + 5, cy + 34, cx + 6, cy + 6, bend=0.6)
    f.curly(cx + 4, cy - 14, cx + 20, cy - 44, bend=-0.5)
    f.arrow(205, 140, 275, 140, "E2 빠름", "−HBr")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 0, kind="2", length=34)
    m.sub("pa", a, 120, "Ph")
    m.sub("ha", a, 240, "H")
    m.sub("pb", b, 60, "Ph")
    m.sub("bb", b, -60, "Br")
    f.mol(m, 310, 140)
    f.text(327, 205, "(E) — 주생성물 B", size=12, color=GREEN, weight="bold")
    f.text(327, 223, "두 Ph cis", size=11)
    f.raw(f'<line x1="400" y1="30" x2="400" y2="280" stroke="#e5e7eb"/>')
    # syn-periplanar
    cx, cy = 520, 140
    newman(f, cx, cy, [(90, "Br"), (210, "Ph"), (330, "H")], [(118, "H"), (238, "Br"), (358, "Ph")],
           colors={("f", 0): ORANGE, ("b", 0): ORANGE})
    f.text(cx, 28, "syn-periplanar (가려진 형태)", size=12, weight="bold", color=ORANGE)
    f.arrow(605, 140, 675, 140, "E2 느림", "−HBr")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 0, kind="2", length=34)
    m.sub("pa", a, 240, "Ph")
    m.sub("ha", a, 120, "H")
    m.sub("pb", b, 60, "Ph")
    m.sub("bb", b, -60, "Br")
    f.mol(m, 710, 140)
    f.text(727, 205, "(Z) — 거의 안 생김", size=12, color=ORANGE, weight="bold")
    f.text(727, 223, "두 Ph trans", size=11)
    f.text(400, 270, "메소 A: H–C–C–Br anti 배열을 잡으면 두 Ph가 gauche → (E)만 생성. (Z)는 가려진(syn) 배열이 필요해 매우 느리다.", size=11)
    return f.render()



# ---------------------------------------------------------- 2011 #35: 브로민화 메커니즘
def f2011_35_mech():
    f = Fig(800, 220)
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.sub("b", a, 0, kind="2", length=36)
    m.sub("r", a, 225, "R")
    f.mol(m, 60, 140)
    f.text(78, 50, "Br", size=13)
    f.text(78, 82, "Br", size=13)
    f.raw(f'<line x1="78" y1="58" x2="78" y2="74" stroke="{INK}" stroke-width="1.4"/>')
    f.curly(78, 136, 70, 88, bend=-0.5)
    f.curly(84, 66, 104, 58, bend=-0.9)
    f.text(78, 185, "π 전자 → Br–Br σ*", size=11)
    f.arrow(140, 110, 230, 110, "속도 결정 단계", "흡열")
    m = Mol()
    a = m.atom("a", 0, 0)
    b = m.atom("b", 40, 0)
    m.bond(a, b)
    m.atom("br", 20, -32, "Br^+")
    m.bond(a, "br", "dash")
    m.bond(b, "br")
    m.sub("r", a, 225, "R")
    f.mol(m, 270, 130)
    f.text(262, 118, "δ+", size=11, color=RED)
    f.text(320, 190, "Br^−", size=13, color=BLUE)
    f.curly(312, 182, 274, 138, bend=-0.4, color=BLUE)
    f.text(300, 210, "고리형 브로모늄 (R 쪽 탄소에 δ+ 치우침)", size=11)
    f.arrow(380, 110, 470, 110, "anti 고리 열림", "(S_N2 유사)")
    m = Mol()
    a = m.atom("a", 0, 0)
    m.sub("r", a, 210, "R")
    m.sub("x", a, 90, "Br")
    b = m.sub("b", a, -30)
    m.sub("y", b, -90, "Br")
    f.mol(m, 530, 120)
    f.text(540, 190, "RCHBr–CH₂Br", size=12)
    tbox(f, 620, 50, 170, ["δ+ 안정화 = TS 낮춤",
                            "Ph(공명, EDG) > Et(+I)",
                            "> Br(−I, EWG)",
                            "→ B > C > A"], size=11.5)
    return f.render()


# ---------------------------------------------------------- 2009 #23: a·b·e의 중간체
def _mchene(m, p):
    _mch(m, p)
    m.set_bond(p + "0", p + "1", "in", (0, 0))
    m.sub(p + "me", p + "1", 30)


def f2009_23_mech():
    f = Fig(800, 390)
    rows = [(65, "a  HI"), (190, "b  BH₃ → H₂O₂/OH⁻"), (315, "e  Br₂")]
    for y, t in rows:
        f.text(15, y - 48, t, size=12, anchor="start", weight="bold")
        m = Mol()
        _mchene(m, "r")
        f.mol(m, 70, y + 5, scale=0.85)
    # a
    y = 65
    f.arrow(130, y, 220, y, "H^+ (C2에)", "Markovnikov")
    m = Mol(); _mch(m, "r"); m.sub("me", "r1", 30)
    f.mol(m, 270, y + 5, scale=0.85)
    xr, yr = m.pos("r1")
    f.charge(270 + xr * 0.85 + 12, y + 5 + yr * 0.85 + 12)
    f.text(275, y + 48, "3° 탄소 양이온", size=11)
    f.arrow(330, y, 420, y, "I^−", "")
    m = Mol(); _mch(m, "r"); m.sub("me", "r1", 60); m.sub("i", "r1", 0, "I")
    f.mol(m, 470, y + 5, scale=0.85)
    f.text(480, y + 48, "1-iodo-1-methylcyclohexane", size=11, color=GREEN)
    f.text(620, y, "보기 a (I가 2° 탄소) ✗", size=11.5, anchor="start", color=RED)
    # b
    y = 190
    f.arrow(130, y, 220, y, "BH_3 (syn, 4중심 TS)", "B → 덜 치환된 C2")
    m = Mol(); _mch(m, "r")
    m.sub("me", "r1", 60, kind="h", length=26)
    m.sub("h", "r1", -10, "H", kind="w", length=24)
    m.sub("b", "r0", 110, "BH_2", kind="w")
    f.mol(m, 275, y + 8, scale=0.85)
    f.text(280, y + 52, "H와 BH₂가 같은 면(쐐기)", size=11)
    f.arrow(340, y, 430, y, "H_2O_2, OH^−", "C–B → C–O 보존")
    m = Mol(); _mch(m, "r")
    m.sub("me", "r1", 60, kind="h", length=26)
    m.sub("h", "r1", -10, "H", kind="w", length=24)
    m.sub("o", "r0", 110, "OH", kind="w")
    f.mol(m, 485, y + 8, scale=0.85)
    f.text(490, y + 52, "trans-2-methylcyclohexanol", size=11, color=GREEN)
    f.text(620, y, "CH₃와 OH trans → 보기 b(cis) ✗", size=11.5, anchor="start", color=RED)
    # e
    y = 315
    f.arrow(130, y, 220, y, "Br_2", "위 면에서")
    m = Mol(); _mch(m, "r")
    m.sub("me", "r1", -20)
    x0, y0 = m.pos("r0"); x1, y1 = m.pos("r1")
    m.atom("br", (x0 + x1) / 2 + 13, (y0 + y1) / 2 - 23, "Br^+")
    m.bond("r0", "br", "w")
    m.bond("r1", "br", "w")
    f.mol(m, 275, y + 8, scale=0.85)
    f.text(250, y + 52, "Br⁻는 아래 면에서 (δ+ 큰 C1)", size=11, color=BLUE)
    f.arrow(340, y, 430, y, "Br^−", "anti 고리 열림")
    m = Mol(); _mch(m, "r")
    m.sub("me", "r1", 55, kind="w")
    m.sub("b1", "r1", 0, "Br", kind="h")
    m.sub("b2", "r0", 110, "Br", kind="w")
    f.mol(m, 485, y + 8, scale=0.85)
    f.text(490, y + 52, "trans-1,2-dibromo-1-methyl (라셈)", size=11, color=GREEN)
    f.text(620, y, "두 Br trans → 보기 e ○", size=11.5, anchor="start", color=GREEN)
    return f.render()


# ---------------------------------------------------------- 2010 #36 ㄷ: s-cis 형태 비율
def f2010_36_scis():
    f = Fig(800, 200)
    def diene(m, p, s_cis, me=False):
        a = m.atom(p + "1", 0, 0)
        if s_cis:
            b = m.sub(p + "2", a, 60, kind="2")
            c = m.sub(p + "3", b, 0)
            m.sub(p + "4", c, -60, kind="2")
            if me:
                m.sub(p + "m2", b, 120)
                m.sub(p + "m3", c, 60)
        else:
            b = m.sub(p + "2", a, 30, kind="2")
            c = m.sub(p + "3", b, -30)
            m.sub(p + "4", c, 30, kind="2")
            if me:
                m.sub(p + "m2", b, 90)
                m.sub(p + "m3", c, -90)
    f.text(200, 20, "1,3-butadiene", size=12.5, weight="bold")
    f.text(600, 20, "2,3-dimethyl-1,3-butadiene", size=12.5, weight="bold")
    for x0, me in ((30, False), (430, True)):
        m = Mol(); diene(m, "t", False, me)
        f.mol(m, x0, 110)
        f.eqarrow(x0 + 120, x0 + 190, 100)
        m = Mol(); diene(m, "c", True, me)
        f.mol(m, x0 + 225, 125)
    f.text(70, 160, "s-trans (우세)", size=11)
    f.text(275, 160, "s-cis (반응 형태)", size=11, color=RED)
    f.text(200, 185, "s-trans가 훨씬 안정 → s-cis 분율 작음 → 느림", size=11)
    f.text(470, 160, "s-trans: CH₃↔H 반발", size=11)
    f.text(680, 160, "s-cis (비율 증가)", size=11, color=GREEN)
    f.text(600, 185, "s-cis 분율 ↑ + CH₃(EDG)가 HOMO ↑ → 빠름", size=11, color=GREEN)
    return f.render()


# ---------------------------------------------------------- 2008 #12: 분자 내 aldol 메커니즘
def f2008_12_aldol():
    f = Fig(800, 240)
    f.text(20, 18, "① OH⁻가 지방족 CHO의 α-H 제거 → 엔올레이트  ② 분자 내 친핵성 첨가(5원 고리)  ③ 양성자화  ④ E1cB 탈수", size=12, anchor="start")
    # 엔올레이트
    m = Mol()
    _benz(m, "b")
    a1 = m.sub("a1", "b1", 0)
    m.sub("ao", a1, 60, "O", kind="2")
    c1 = m.sub("c1", "b2", -30)
    c2 = m.sub("c2", c1, 30)
    c3 = m.sub("c3", c2, -30, kind="2")
    m.sub("o", c3, 30, "O^−")
    ox, oy = 50, 125
    f.mol(m, ox, oy)
    X = lambda n: P(m, n, ox, oy)
    (xa, ya), (xo, yo), (x2, y2), (x3, y3), (xq, yq) = X("a1"), X("ao"), X("c2"), X("c3"), X("o")
    f.curly(xq + 2, yq - 10, (x3 + xq) / 2 + 2, (y3 + yq) / 2 - 7, bend=0.9)
    f.curly((x2 + x3) / 2 + 2, (y2 + y3) / 2 + 8, xa + 2, ya + 7, bend=-0.9)
    f.curly((xa + xo) / 2 + 5, (ya + yo) / 2 + 2, xo + 12, yo + 2, bend=-0.7)
    f.text(xa - 6, ya - 12, "δ+", size=10, color=RED)
    f.text(ox + 40, 205, "엔올레이트 (α-C 친핵체)", size=11)
    f.arrow(205, 120, 265, 120, "5-exo", "고리 형성")
    # aldol (양성자화 후)
    m = Mol()
    I = _indene(m, "i")
    m.sub("oh", I["C1"], 90, "OH")
    m.sub("cho", I["C2"], 0, "CHO", anchor="start")
    f.mol(m, 320, 120)
    f.text(360, 195, "β-하이드록시 알데하이드", size=11)
    f.text(360, 211, "(1-hydroxyindane-2-carbaldehyde)", size=10.5, color=GRAY)
    f.arrow(455, 120, 545, 120, "OH^−, 가열", "−H_2O (E1cB)")
    m = Mol()
    I = _indene(m, "j")
    m.set_bond(I["C1"], I["C2"], "in", I["c"])
    m.sub("cho", I["C2"], 0, "CHO", anchor="start")
    f.mol(m, 600, 120)
    f.text(650, 195, "B: 1H-indene-2-carbaldehyde", size=11.5, color=GREEN, weight="bold")
    f.text(650, 211, "벤젠·C=O와 공액 → 탈수 유리", size=10.5)
    return f.render()
