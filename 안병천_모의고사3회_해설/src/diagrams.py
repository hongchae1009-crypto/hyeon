"""해설지에 들어가는 손그림 SVG(결정장 전자 배치, fac·mer 구조, 확률 밀도 그래프)를 만든다."""
import math, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'img')
INK, ACC, MUT = '#1f2933', '#1d4ed8', '#6b7280'
FONT = "font-family='Noto Sans KR, sans-serif'"

def svg(w, h, body):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}'>"
            f"<rect width='{w}' height='{h}' fill='white'/>{body}</svg>")

def text(x, y, s, size=15, anchor='start', color=INK, weight='normal'):
    return f"<text x='{x}' y='{y}' font-size='{size}' text-anchor='{anchor}' fill='{color}' font-weight='{weight}' {FONT}>{s}</text>"

def arrows(cx, y, e):
    """e: '' / 'u' / 'ud' 한 오비탈의 전자."""
    out = ''
    if 'u' in e:
        x = cx - (5 if 'd' in e else 0)
        out += f"<path d='M{x} {y-3} L{x} {y-21} M{x-4} {y-15} L{x} {y-21} L{x+4} {y-15}' stroke='{ACC}' stroke-width='1.8' fill='none'/>"
    if 'd' in e:
        x = cx + 5
        out += f"<path d='M{x} {y-21} L{x} {y-3} M{x-4} {y-9} L{x} {y-3} L{x+4} {y-9}' stroke='{ACC}' stroke-width='1.8' fill='none'/>"
    return out

def level(x, y, elec, label='', w=26, gap=8, side='right'):
    """elec: 오비탈별 전자 리스트. (x,y)=왼쪽 끝. 반환: (svg, 오른쪽 끝 x)"""
    out = ''
    for i, e in enumerate(elec):
        x0 = x + i * (w + gap)
        out += f"<line x1='{x0}' y1='{y}' x2='{x0+w}' y2='{y}' stroke='{INK}' stroke-width='2'/>"
        out += arrows(x0 + w / 2, y, e)
    xe = x + len(elec) * (w + gap) - gap
    if label:
        out += text(xe + 8, y + 5, label, 15) if side == 'right' else text(x - 8, y + 5, label, 15, 'end')
    return out, xe

def dash(x1, y1, x2, y2):
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{MUT}' stroke-width='1' stroke-dasharray='3 3'/>"

def sub(t):
    return f'<tspan baseline-shift="sub" font-size="11">{t}</tspan>'

def td_jahn_teller():
    """[FeO4]4- (Td, d4 고스핀) z-out(위) / z-in(아래)."""

def sub(t):
    return f'<tspan baseline-shift="sub" font-size="11">{t}</tspan>'


def d3_states():
    """Cr³⁺(d³) 바닥 ⁴A₂g와 들뜬 ⁴T₂g, ⁴T₁g(F), ⁴T₁g(P)의 대표 전자 배치."""
    cols = [(f'⁴A{sub("2g")} (바닥)', ['u', 'u', 'u'], ['', ''], f't{sub("2g")}³'),
            (f'⁴T{sub("2g")} / ⁴T{sub("1g")}(F)', ['u', 'u', ''], ['u', ''], f't{sub("2g")}²e{sub("g")}¹'),
            (f'⁴T{sub("1g")}(P)', ['u', '', ''], ['u', 'u'], f't{sub("2g")}¹e{sub("g")}²')]
    b = ''
    for k, (title, t2g, eg, cfg) in enumerate(cols):
        ox = 34 + k * 116
        b += text(ox + 55, 20, title, 12.5, 'middle', weight='bold')
        s1, _ = level(ox + 22, 70, eg, '', w=22, gap=8); b += s1
        s1, _ = level(ox + 7, 150, t2g, '', w=22, gap=8); b += s1
        b += text(ox + 55, 180, cfg, 14, 'middle', ACC, 'bold')
    b += text(4, 74, f'e{sub("g")}', 12, color=MUT) + text(4, 154, f't{sub("2g")}', 12, color=MUT)
    return svg(380, 195, b)


def oct_fac_mer():
    """[Mn(CO)₃(H₂O)₃]⁺의 fac / mer 이성질체와 점군, CO 신축 Γ."""
    def octa(ox, labels, title, pg, gam):
        cx, cy, r = ox + 85, 110, 55
        pos = {'t': (cx, cy - r), 'b': (cx, cy + r), 'l': (cx - r, cy), 'r': (cx + r, cy),
               'f': (cx - 28, cy + 22), 'k': (cx + 28, cy - 22)}
        s = text(cx, 18, title, 14, 'middle', weight='bold')
        for key, (x, y) in pos.items():
            dash_ = " stroke-dasharray='4 3'" if key == 'k' else ''
            s += f"<line x1='{cx}' y1='{cy}' x2='{x}' y2='{y}' stroke='{INK}' stroke-width='2'{dash_}/>"
        s += f"<circle cx='{cx}' cy='{cy}' r='13' fill='white' stroke='{INK}'/>" + text(cx, cy + 5, 'Mn', 12, 'middle', weight='bold')
        off = {'t': (0, -8), 'b': (0, 18), 'l': (-6, 5), 'r': (6, 5), 'f': (-10, 16), 'k': (10, -6)}
        anc = {'t': 'middle', 'b': 'middle', 'l': 'end', 'r': 'start', 'f': 'end', 'k': 'start'}
        for key, lab in labels.items():
            x, y = pos[key]; dx, dy = off[key]
            col = '#c0392b' if lab == 'CO' else INK
            s += text(x + dx, y + dy, lab, 13, anc[key], col, 'bold' if lab == 'CO' else 'normal')
        s += text(cx, 200, pg, 14, 'middle', ACC, 'bold') + text(cx, 220, gam, 13, 'middle')
        return s
    b = octa(0, {'t': 'CO', 'r': 'CO', 'k': 'CO', 'b': 'H₂O', 'l': 'H₂O', 'f': 'H₂O'},
             'fac (면 배치)', f'C{sub("3v")}', f'Γ{sub("CO")} = A{sub(1)} + E → 띠 2개')
    b += octa(185, {'t': 'CO', 'b': 'CO', 'r': 'CO', 'l': 'H₂O', 'f': 'H₂O', 'k': 'H₂O'},
              'mer (자오선 배치)', f'C{sub("2v")}', f'Γ{sub("CO")} = 2A{sub(1)} + B{sub(1)} → 띠 3개')
    return svg(370, 232, b)


def plot(fn, xs, xlabel, ylabel, marks, W=360, H=210, ymax=None, xticks=()):
    """간단한 선 그래프. marks: [(x, 이름)] 세로 점선."""
    x0, x1, y0, y1 = 46, W - 14, H - 34, 34
    ys = [fn(x) for x in xs]
    lo, hi = min(min(ys), 0), ymax or max(ys)
    X = lambda x: x0 + (x - xs[0]) / (xs[-1] - xs[0]) * (x1 - x0)
    Y = lambda y: y0 - (y - lo) / (hi - lo) * (y0 - y1)
    b = f"<line x1='{x0}' y1='{Y(0):.1f}' x2='{x1}' y2='{Y(0):.1f}' stroke='{MUT}'/>"
    b += f"<line x1='{x0}' y1='{y0}' x2='{x0}' y2='{y1}' stroke='{MUT}'/>"
    pts = ' '.join(f'{X(x):.1f},{Y(y):.1f}' for x, y in zip(xs, ys))
    b += f"<polyline points='{pts}' fill='none' stroke='{ACC}' stroke-width='2'/>"
    for x, lab in marks:
        b += f"<line x1='{X(x):.1f}' y1='{y0}' x2='{X(x):.1f}' y2='{y1}' stroke='#c0392b' stroke-dasharray='4 3'/>"
        b += text(X(x) + 4, y1 + 26, lab, 11.5, 'start', '#c0392b')
    for x, lab in xticks:
        b += text(X(x), y0 + 16, lab, 11.5, 'middle', MUT)
    b += text((x0 + x1) / 2, H - 2, xlabel, 12, 'middle') + text(4, 16, ylabel, 12)
    return svg(W, H, b)


if __name__ == '__main__':
    out = {
        'd_A11': d3_states(),
        'd_B06': oct_fac_mer(),
        'd_B10': plot(lambda p: 4 / (3 * math.pi) * math.sin(p) ** 4, [i * 2 * math.pi / 400 for i in range(401)],
                      'φ', 'P(φ)', [(math.pi / 2, '최대 4/3π'), (3 * math.pi / 2, '최대 4/3π')],
                      xticks=[(0, '0'), (math.pi / 2, 'π/2'), (math.pi, 'π'), (3 * math.pi / 2, '3π/2'), (2 * math.pi, '2π')]),
        'd_B11': plot(lambda r: (6 * r - r * r) * math.exp(-r / 3), [i * 25 / 400 for i in range(401)],
                      'r / a₀', 'R₃₁ (상대값)', [(6, '마디 r = 6a₀')],
                      xticks=[(0, '0'), (5, '5'), (10, '10'), (15, '15'), (20, '20'), (25, '25')]),
    }
    for name, s in out.items():
        open(os.path.join(OUT, name + '.svg'), 'w').write(s)
        print(name)
