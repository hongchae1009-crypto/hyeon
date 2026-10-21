"""안병천 2회 손그림 SVG: A형 9번 C–H 신축 진동(Au, Bu), A형 1번 단위 세포 대각선."""
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'img')
INK, RED, BLUE, MUT = '#1f2933', '#c0392b', '#1d4ed8', '#6b7280'
F = "font-family='Noto Sans KR, sans-serif'"


def t(x, y, s, size=14, anchor='middle', color=INK, weight='normal'):
    return f"<text x='{x}' y='{y}' font-size='{size}' text-anchor='{anchor}' fill='{color}' font-weight='{weight}' {F}>{s}</text>"


def line(a, b, w=2, color=INK, dash=''):
    d = f" stroke-dasharray='{dash}'" if dash else ''
    return f"<line x1='{a[0]}' y1='{a[1]}' x2='{b[0]}' y2='{b[1]}' stroke='{color}' stroke-width='{w}'{d}/>"


def wedge(a, b):
    import math
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy); px, py = -dy / L * 4, dx / L * 4
    return f"<polygon points='{a[0]},{a[1]} {b[0]+px:.1f},{b[1]+py:.1f} {b[0]-px:.1f},{b[1]-py:.1f}' fill='{INK}'/>"


def arrow(a, b, color):
    import math
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    h1 = (b[0] - 8 * ux + 4 * uy, b[1] - 8 * uy - 4 * ux); h2 = (b[0] - 8 * ux - 4 * uy, b[1] - 8 * uy + 4 * ux)
    return line(a, (b[0] - 6 * ux, b[1] - 6 * uy), 2.4, color) + \
        f"<polygon points='{b[0]},{b[1]} {h1[0]:.1f},{h1[1]:.1f} {h2[0]:.1f},{h2[1]:.1f}' fill='{color}'/>"


def molecule(ox, signs, title, sub):
    """signs: H1(Ca 아래 쐐기), H2(Ca 점선), H3(Cb 쐐기), H4(Cb 점선) 각각 +1 늘어남 / -1 줄어듦."""
    import math
    Ca, Cb = (ox + 95, 130), (ox + 170, 130)
    head = t(ox + 132, 22, title, 16, weight='bold') + t(ox + 132, 42, sub, 12, color=MUT)
    b = line(Ca, Cb) + line(Ca, (ox + 58, 97)) + line(Cb, (ox + 207, 163))
    b += t(ox + 46, 95, 'Cl', 15) + t(ox + 220, 175, 'Cl', 15)
    H = {1: (Ca, (ox + 62, 168), 'w'), 2: (Ca, (ox + 105, 178), 'd'),
         3: (Cb, (ox + 203, 92), 'w'), 4: (Cb, (ox + 160, 82), 'd')}
    for k, (c, h, kind) in H.items():
        b += wedge(c, h) if kind == 'w' else line(c, h, 1.6, INK, '3 3')
        dx, dy = h[0] - c[0], h[1] - c[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
        lab = (h[0] + ux * 11, h[1] + uy * 11)
        b += t(lab[0], lab[1] + 5, f'H{k}', 12)
        p1 = (lab[0] + ux * 13, lab[1] + uy * 13); p2 = (lab[0] + ux * 36, lab[1] + uy * 36)
        b += arrow(p1, p2, RED) if signs[k - 1] > 0 else arrow(p2, p1, BLUE)
    for c in (Ca, Cb):
        b += f"<circle cx='{c[0]}' cy='{c[1]}' r='9' fill='white'/>" + t(c[0], c[1] + 5, 'C', 14, weight='bold')
    return head + f"<g transform='translate(0,28)'>{b}</g>"


def a09():
    # 쐐기(H1, H3) = 분자 평면 위, 점선(H2, H4) = 아래.  C2(z)는 평면에 수직.
    b = molecule(0, (+1, -1, +1, -1), 'A<tspan baseline-shift="sub" font-size="10">u</tspan>  (z 편광)',
                 'r₁ − r₂ + r₃ − r₄')
    b += molecule(270, (+1, +1, -1, -1), 'B<tspan baseline-shift="sub" font-size="10">u</tspan>  (x, y 편광)',
                  'r₁ + r₂ − r₃ − r₄')
    b += t(270, 268, '빨강 = 늘어남, 파랑 = 줄어듦 (반 주기 뒤에는 반대)', 12, color=MUT)
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 540 278' width='540' height='278'><rect width='540' height='278' fill='white'/>{b}</svg>"


open(os.path.join(OUT, 'd_A09.svg'), 'w').write(a09())
print('d_A09')
