"""모범답안 파일과 같은 스타일의 구조식 SVG를 만드는 작은 그리기 도구.

좌표는 px 단위, 결합 길이 기본 30 px.  y축은 아래 방향(+)이다.
라벨 문법: '_x' 또는 '_{..}' 아래 첨자, '^x' 또는 '^{..}' 위 첨자.
"""
import math

INK = "#1d1d1f"
RED = "#c0392b"
BLUE = "#1f5fbf"
FONT = "Arial, 'Malgun Gothic', 'Noto Sans CJK KR', sans-serif"
L = 30.0

_fig_counter = [0]


def _esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _tokens(label):
    """'CO_2Et^+' → [(text, mode)] mode: n/sub/sup"""
    out, i, n = [], 0, len(label)
    buf = ""
    while i < n:
        c = label[i]
        if c in "_^" and i + 1 < n:
            if buf:
                out.append((buf, "n"))
                buf = ""
            mode = "sub" if c == "_" else "sup"
            if label[i + 1] == "{":
                j = label.index("}", i)
                out.append((label[i + 2:j], mode))
                i = j + 1
            else:
                out.append((label[i + 1], mode))
                i += 2
            continue
        buf += c
        i += 1
    if buf:
        out.append((buf, "n"))
    return out


def rich(x, y, label, size=13, anchor="middle", weight="normal", color=INK, halo=False, italic=False):
    small = round(size * 0.72, 1)
    dsub, dsup = round(size * 0.32, 1), round(-size * 0.38, 1)
    parts, cur = [], 0.0
    for text, mode in _tokens(label):
        if mode == "n":
            dy = -cur
            cur = 0.0
            attr = f' dy="{dy}"' if dy else ""
            parts.append(f"<tspan{attr}>{_esc(text)}</tspan>")
        else:
            target = dsub if mode == "sub" else dsup
            dy = target - cur
            cur = target
            parts.append(f'<tspan dy="{dy}" font-size="{small}">{_esc(text)}</tspan>')
    if cur:
        parts.append(f'<tspan dy="{-cur}"></tspan>')
    h = ' stroke="#fff" stroke-width="4" paint-order="stroke" stroke-linejoin="round"' if halo else ""
    st = ' font-style="italic"' if italic else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-family="{FONT}" fill="{color}" '
            f'text-anchor="{anchor}" dominant-baseline="central" font-weight="{weight}"{st}{h}>{"".join(parts)}</text>')


class Mol:
    """원자 좌표 + 결합 목록으로 골격 구조식을 그린다."""

    def __init__(self):
        self.a = {}      # name -> [x, y, label, anchor]
        self.b = []      # (a1, a2, kind, extra)
        self.extra = []  # 추가 SVG 조각 (분자 좌표계)

    # ---- 원자 ----
    def atom(self, name, x, y, label=None, anchor="middle"):
        self.a[name] = [x, y, label, anchor]
        return name

    def sub(self, name, frm, ang, label=None, anchor=None, length=L, kind=1):
        """frm 원자에서 ang(도, 0=오른쪽, 90=위) 방향으로 새 원자 + 결합."""
        x0, y0 = self.a[frm][:2]
        x = x0 + length * math.cos(math.radians(ang))
        y = y0 - length * math.sin(math.radians(ang))
        if anchor is None:
            c = math.cos(math.radians(ang))
            anchor = "start" if c > 0.5 and label and len(label) > 2 else ("end" if c < -0.5 and label and len(label) > 2 else "middle")
        self.atom(name, x, y, label, anchor)
        self.bond(frm, name, kind)
        return name

    def ring(self, p, cx, cy, n=6, r=L, start=90, arom=None, bonds=True):
        """p0..p(n-1): start 각도에서 시계 방향.  arom: 이중결합(안쪽 선)을 둘 변의 시작 인덱스 목록."""
        for i in range(n):
            ang = math.radians(start - 360.0 * i / n)
            self.atom(f"{p}{i}", cx + r * math.cos(ang), cy - r * math.sin(ang))
        if bonds:
            for i in range(n):
                k = ("in", (cx, cy)) if arom and i in arom else (1, None)
                self.b.append((f"{p}{i}", f"{p}{(i + 1) % n}", k[0], k[1]))
        return [f"{p}{i}" for i in range(n)]

    def bond(self, a1, a2, kind=1, extra=None):
        self.b.append((a1, a2, kind, extra))

    def set_bond(self, a1, a2, kind, extra=None):
        for i, (x1, x2, k, e) in enumerate(self.b):
            if {x1, x2} == {a1, a2}:
                self.b[i] = (x1, x2, kind, extra)
                return
        self.bond(a1, a2, kind, extra)

    def label(self, name, text, anchor="middle"):
        self.a[name][2] = text
        self.a[name][3] = anchor

    def pos(self, name):
        return tuple(self.a[name][:2])

    # ---- 렌더링 ----
    def _end(self, name, toward):
        x, y, lab, anc = self.a[name]
        if not lab:
            return x, y
        tx, ty = toward
        d = math.hypot(tx - x, ty - y) or 1
        cut = 8.5 if len(lab.replace('_', '').replace('^', '')) <= 2 or anc != "middle" else 10
        return x + (tx - x) * cut / d, y + (ty - y) * cut / d

    def svg(self, ox=0, oy=0, color=INK, lw=1.4, scale=1.0):
        sc = f" scale({scale})" if scale != 1.0 else ""
        s = [f'<g transform="translate({ox:.1f},{oy:.1f}){sc}">']
        ln = lambda x1, y1, x2, y2, c=color: s.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{lw}" stroke-linecap="round"/>')
        for a1, a2, kind, extra in self.b:
            p1, p2 = self.pos(a1), self.pos(a2)
            x1, y1 = self._end(a1, p2)
            x2, y2 = self._end(a2, p1)
            dx, dy = x2 - x1, y2 - y1
            d = math.hypot(dx, dy) or 1
            nx, ny = -dy / d, dx / d
            c = extra if (isinstance(extra, str) and extra.startswith("#")) else color
            if kind == 1:
                ln(x1, y1, x2, y2, c)
            elif kind == "in":  # 고리 안쪽 이중 결합
                cx, cy = extra
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                sgn = 1 if (cx - mx) * nx + (cy - my) * ny > 0 else -1
                o, sh = 5.5 * sgn, 0.16
                ln(x1, y1, x2, y2)
                ln(x1 + dx * sh + nx * o, y1 + dy * sh + ny * o, x2 - dx * sh + nx * o, y2 - dy * sh + ny * o)
            elif kind in ("2", 2):  # 가운데 이중 결합
                o = 2.6
                ln(x1 + nx * o, y1 + ny * o, x2 + nx * o, y2 + ny * o, c)
                ln(x1 - nx * o, y1 - ny * o, x2 - nx * o, y2 - ny * o, c)
            elif kind in ("2l", "2r"):  # 한쪽으로 치우친 이중 결합 (l: 진행 방향 왼쪽)
                sgn = -1 if kind == "2l" else 1
                o, sh = 5.5 * sgn, 0.14
                ln(x1, y1, x2, y2, c)
                ln(x1 + dx * sh + nx * o, y1 + dy * sh + ny * o, x2 - dx * sh + nx * o, y2 - dy * sh + ny * o, c)
            elif kind == 3:
                o = 3.4
                ln(x1, y1, x2, y2, c)
                ln(x1 + nx * o, y1 + ny * o, x2 + nx * o, y2 + ny * o, c)
                ln(x1 - nx * o, y1 - ny * o, x2 - nx * o, y2 - ny * o, c)
            elif kind == "w":  # 쐐기 (a1 좁은 끝)
                w = 3.6
                s.append(f'<polygon points="{x1:.1f},{y1:.1f} {x2 + nx * w:.1f},{y2 + ny * w:.1f} {x2 - nx * w:.1f},{y2 - ny * w:.1f}" fill="{color}"/>')
            elif kind == "h":  # 점선 쐐기
                for k in range(1, 7):
                    t = k / 6.5
                    w = 3.8 * t
                    px, py = x1 + dx * t, y1 + dy * t
                    ln(px + nx * w, py + ny * w, px - nx * w, py - ny * w)
            elif kind == "dash":
                s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{lw}" stroke-dasharray="3 3"/>')
            elif kind == "form":  # 형성 중인 결합 (TS)
                s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{RED}" stroke-width="1.6" stroke-dasharray="4 3"/>')
        for name, (x, y, lab, anc) in self.a.items():
            if lab:
                xx = x - 4.6 if anc == "start" else (x + 4.6 if anc == "end" else x)
                s.append(rich(xx, y, lab, anchor=anc, halo=True))
        s.extend(self.extra)
        s.append("</g>")
        return "".join(s)


class Fig:
    def __init__(self, w, h):
        _fig_counter[0] += 1
        self.id = f"f{_fig_counter[0]}"
        self.w, self.h = w, h
        self.el = []

    def add(self, x):
        self.el.append(x)
        return self

    def mol(self, m, ox, oy, **kw):
        return self.add(m.svg(ox, oy, **kw))

    def text(self, x, y, t, size=13, anchor="middle", weight="normal", color=INK, italic=False):
        return self.add(rich(x, y, t, size=size, anchor=anchor, weight=weight, color=color, italic=italic))

    def cap(self, x, y, t, color=INK):
        return self.text(x, y, t, weight="bold", color=color)

    def arrow(self, x1, y1, x2, y2, top=None, bot=None, color=INK, kind="solid"):
        mk = {"#c0392b": "r", "#1f5fbf": "b"}.get(color, "k")
        dash = ' stroke-dasharray="5 4"' if kind == "dash" else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="1.5"{dash} '
                 f'marker-end="url(#{self.id}{mk})" stroke-linecap="round"/>')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        vertical = abs(x2 - x1) < abs(y2 - y1)
        if top:
            if vertical:
                self.text(mx + 8, my - 8, top, size=11, anchor="start")
            else:
                self.text(mx, my - 13, top, size=11)
        if bot:
            if vertical:
                self.text(mx + 8, my + 9, bot, size=11, anchor="start")
            else:
                self.text(mx, my + 14, bot, size=11)
        return self

    def eqarrow(self, x1, x2, y, top=None, bot=None):
        """평형(⇌) 화살표"""
        self.add(f'<path d="M{x1:.1f},{y - 2.5:.1f} L{x2:.1f},{y - 2.5:.1f} l-8,-5" fill="none" stroke="{INK}" stroke-width="1.4"/>')
        self.add(f'<path d="M{x2:.1f},{y + 2.5:.1f} L{x1:.1f},{y + 2.5:.1f} l8,5" fill="none" stroke="{INK}" stroke-width="1.4"/>')
        if top:
            self.text((x1 + x2) / 2, y - 14, top, size=11)
        if bot:
            self.text((x1 + x2) / 2, y + 15, bot, size=11)
        return self

    def resarrow(self, x1, x2, y):
        """공명 ↔"""
        return self.add(f'<line x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" stroke="{INK}" stroke-width="1.4" '
                        f'marker-start="url(#{self.id}k)" marker-end="url(#{self.id}k)"/>')

    def curly(self, x1, y1, x2, y2, bend=0.35, color=RED, half=False):
        """굽은 화살표 (bend: 오른쪽(+)/왼쪽(−)으로 휘는 정도)"""
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        cx, cy = mx - dy * bend, my + dx * bend
        mk = "rh" if half else ("r" if color == RED else "b")
        return self.add(f'<path d="M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}" fill="none" stroke="{color}" '
                        f'stroke-width="1.4" marker-end="url(#{self.id}{mk})"/>')

    def lp(self, x, y, ang=90):
        """비공유 전자쌍 (두 점)"""
        a = math.radians(ang + 90)
        dx, dy = 3.2 * math.cos(a), -3.2 * math.sin(a)
        return self.add(f'<circle cx="{x + dx:.1f}" cy="{y + dy:.1f}" r="1.5" fill="{INK}"/><circle cx="{x - dx:.1f}" cy="{y - dy:.1f}" r="1.5" fill="{INK}"/>')

    def charge(self, x, y, sign="+"):
        t = "+" if sign == "+" else "−"
        return self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#fff" stroke="{INK}" stroke-width="1"/>'
                        + rich(x, y + 0.5, t, size=11))

    def lobe(self, x, y, up=True, filled=True, rx=7, ry=15, color=BLUE):
        cy = y - ry if up else y + ry
        fill = color if filled else "#fff"
        op = ' fill-opacity="0.8"' if filled else ""
        return self.add(f'<ellipse cx="{x:.1f}" cy="{cy:.1f}" rx="{rx}" ry="{ry}" fill="{fill}"{op} stroke="{INK}" stroke-width="1"/>')

    def porb(self, x, y, phase=1, rx=7, ry=14):
        """p 오비탈 (phase=+1: 위쪽 로브 채움, -1: 아래쪽 로브 채움, 0: 기여 없음)"""
        if phase == 0:
            return self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="{INK}"/>')
        self.lobe(x, y, up=True, filled=phase > 0, rx=rx, ry=ry)
        self.lobe(x, y, up=False, filled=phase < 0, rx=rx, ry=ry)
        return self

    def box(self, x, y, w, h, fill="#f7f8fa", stroke="#cfd4db", r=8, dash=False):
        d = ' stroke-dasharray="5 4"' if dash else ""
        return self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"{d}/>')

    def cross(self, x, y, s=9, color=RED):
        return self.add(f'<path d="M{x - s},{y - s} L{x + s},{y + s} M{x + s},{y - s} L{x - s},{y + s}" stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>')

    def rotarrow(self, x, y, cw=True, r=11, color=RED):
        """원자 위의 회전 방향 표시"""
        if cw:
            d = f"M{x - r:.1f},{y:.1f} A{r},{r} 0 1 1 {x:.1f},{y + r:.1f}"
        else:
            d = f"M{x + r:.1f},{y:.1f} A{r},{r} 0 1 0 {x:.1f},{y + r:.1f}"
        return self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.5" marker-end="url(#{self.id}r)"/>')

    def raw(self, s):
        return self.add(s)

    def render(self):
        i = self.id
        mk = lambda n, c: (f'<marker id="{i}{n}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                           f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
        half = (f'<marker id="{i}rh" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
                f'<path d="M0,0 L10,5 L0,5 z" fill="{RED}"/></marker>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" class="fig" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}">'
                f'<defs>{mk("k", INK)}{mk("r", RED)}{mk("b", BLUE)}{half}</defs><rect width="100%" height="100%" fill="#fff"/>'
                + "".join(self.el) + "</svg>")


# ---------- 자주 쓰는 조각 ----------

def benzene(m, p, cx, cy, start=90):
    """방향족 고리 (Kekulé, 안쪽 이중 결합 0,2,4번 변)"""
    return m.ring(p, cx, cy, 6, L, start, arom=[0, 2, 4])


def phenyl_at(m, p, attach, ang, arom_shift=0):
    """attach 원자에서 ang 방향으로 붙은 페닐기.  반환: 고리 원자 목록 (p0 = ipso)"""
    x0, y0 = m.pos(attach)
    cx = x0 + 2 * L * math.cos(math.radians(ang))
    cy = y0 - 2 * L * math.sin(math.radians(ang))
    start = ang + 180
    atoms = m.ring(p, cx, cy, 6, L, start, arom=[(0 + arom_shift) % 6, (2 + arom_shift) % 6, (4 + arom_shift) % 6])
    m.bond(attach, f"{p}0")
    return atoms
