"""안병천 6회 해설의 손그림 SVG: CH₃ Walsh 상관도, [18]annulene 고리 준위, d⁶ 고스핀·저스핀 배치."""
import math, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'img')
INK, ACC, RED, MUT, GRN = '#1f2933', '#1d4ed8', '#c0392b', '#6b7280', '#15803d'
FONT = "font-family='Noto Sans KR, sans-serif'"
W = 330


def svg(h, body, w=W):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}'>"
            f"<rect width='{w}' height='{h}' fill='white'/>{body}</svg>")


def T(x, y, s, size=12, anchor='middle', color=INK, weight='normal'):
    return (f"<text x='{x:.1f}' y='{y:.1f}' font-size='{size}' text-anchor='{anchor}' fill='{color}' "
            f"font-weight='{weight}' {FONT}>{s}</text>")


def L(x1, y1, x2, y2, color=INK, w=1.6, dash=''):
    d = f" stroke-dasharray='{dash}'" if dash else ''
    return f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{color}' stroke-width='{w}'{d}/>"


def sub(t):
    return f"<tspan baseline-shift='sub' font-size='9'>{t}</tspan>"


def sup(t):
    return f"<tspan baseline-shift='super' font-size='9'>{t}</tspan>"


def save(name, s):
    open(os.path.join(OUT, name + '.svg'), 'w').write(s)
    print(name)


def lobe(cx, cy, rx, ry, filled, color=ACC):
    """p 오비탈 한쪽 로브(타원). filled=True면 + 위상(색칠), False면 − 위상(흰색)."""
    f = color if filled else 'white'
    return (f"<ellipse cx='{cx:.1f}' cy='{cy:.1f}' rx='{rx:.1f}' ry='{ry:.1f}' fill='{f}' fill-opacity='0.55' "
            f"stroke='{color}' stroke-width='1.3'/>")


def p_orb(cx, cy, c, scale=1.0):
    """세로 방향 p 오비탈. c: 계수(부호=위쪽 로브 위상, 크기=로브 크기). c=0이면 마디(점)."""
    if abs(c) < 1e-6:
        return f"<circle cx='{cx}' cy='{cy}' r='2.5' fill='{INK}'/>"
    r = 7 + 9 * abs(c) * scale
    up = c > 0
    return lobe(cx, cy - r, 0.55 * r, r, up) + lobe(cx, cy + r, 0.55 * r, r, not up) + f"<circle cx='{cx}' cy='{cy}' r='2' fill='{INK}'/>"


def arrows(cx, y, e):
    o = ''
    if 'u' in e:
        x = cx - (5 if 'd' in e else 0)
        o += f"<path d='M{x} {y-3} L{x} {y-19} M{x-4} {y-13} L{x} {y-19} L{x+4} {y-13}' stroke='{ACC}' stroke-width='1.6' fill='none'/>"
    if 'd' in e:
        x = cx + 5
        o += f"<path d='M{x} {y-19} L{x} {y-3} M{x-4} {y-9} L{x} {y-3} L{x+4} {y-9}' stroke='{ACC}' stroke-width='1.6' fill='none'/>"
    return o


def lev(x, y, es, w=20, gap=25):
    o = ''
    for i, e in enumerate(es):
        x0 = x + i * gap
        o += L(x0, y, x0 + w, y, INK, 2) + arrows(x0 + w / 2, y, e)
    return o


# ---------- A4: 알릴 π MO 세 개와 Mn d → ψ3 역결합 ----------
def walsh():
    """CH3 (C3v, 피라미드) ↔ CH3+ (D3h, 평면) 상관도. 왼쪽 C3v, 오른쪽 D3h."""
    h = 330
    yL = {'2a1': 290, '1e': 215, '3a1': 150, '4a1': 75, '2e': 40}
    yR = {"1a1'": 268, "1e'": 228, "1a2''": 125, "2a1'": 92, "2e'": 25}
    lab = {'2a1': ('㉠ 2a', '1'), '1e': ('㉡ 1e', ''), '3a1': ('㉢ 3a', '1'), '4a1': ('㉣ 4a', '1'), '2e': ('㉤ 2e', '')}
    pair = [('2a1', "1a1'", 'u'), ('1e', "1e'", 'd'), ('3a1', "1a2''", 'u'), ('4a1', "2a1'", 'd'), ('2e', "2e'", 'u')]
    b = T(75, 16, 'CH₃ (C' + sub('3v') + ', 피라미드)', 11.5, weight='bold') + T(255, 16, 'CH₃⁺ (D' + sub('3h') + ', 평면)', 11.5, weight='bold')
    rlab = {"1a1'": "1a" + sub("1") + "′", "1e'": "1e′", "1a2''": "1a" + sub("2") + "″ (2p" + sub("z") + ")", "2a1'": "2a" + sub("1") + "′", "2e'": "2e′"}
    elec = {'2a1': 'ud', '1e': 'ud', '3a1': 'u'}
    for k, rk, d in pair:
        n2 = 2 if 'e' in k and 'a' not in k else 1
        yl, yr = yL[k], yR[rk]
        # 왼쪽 준위
        for j in range(n2):
            x0 = 70 + j * 26 - (13 if n2 == 2 else 0)
            b += L(x0, yl, x0 + 20, yl, w=2)
            if k in elec:
                b += arrows(x0 + 10, yl, elec[k])
        b += T(20, yl + 4, lab[k][0] + sub(lab[k][1]), 11, 'start', RED if k in ('2a1', '3a1', '2e') else INK)
        for j in range(n2):
            x0 = 240 + j * 26 - (13 if n2 == 2 else 0)
            b += L(x0, yr, x0 + 20, yr, w=2)
        b += T(318, yr + 4, rlab[rk], 10.5, 'end')
        b += L(110, yl, 225, yr, color=RED if yr < yl else MUT, w=1.2, dash='4 3')
    b += T(165, h - 8, '결합각 증가(피라미드 → 평면): 빨간 점선 = 에너지 상승', 10.5, color=RED)
    return svg(h, b)


def ring18():
    """2차원 고리 위 입자 준위: m = 0, ±1 … ±5, π 전자 18개."""
    h = 300
    b = T(165, 16, '[18]annulene π 전자 18개', 12, weight='bold')
    y0, s = 275, 46
    for m in range(0, 6):
        y = y0 - s * m
        n = 1 if m == 0 else 2
        for j in range(n):
            x0 = 135 + (j * 40 - (20 if n == 2 else 0))
            b += L(x0, y, x0 + 30, y, w=2)
            if m <= 4:
                b += arrows(x0 + 15, y, 'ud')
        b += T(106, y + 4, f'm = {"±" if m else ""}{m}', 11, 'end')
        b += T(215, y + 4, f'E = {m*m} ħ²/2mr²', 10.5, 'start', MUT)
    yH, yL5 = y0 - s * 4, y0 - s * 5
    b += T(352, yH + 4, 'HOMO', 10.5, 'end', ACC) + T(352, yL5 + 4, 'LUMO', 10.5, 'end', RED)
    b += L(102, yH, 102, yL5, color=RED, w=1.3) + T(96, (yH + yL5) / 2 + 4, 'ΔE = 9ħ²/2mr²', 10.5, 'end', RED)
    b += T(180, h - 4, '(준위 간격은 개략, 에너지는 m²에 비례)', 9.5, color=MUT)
    return svg(h + 10, b, w=360)


def d6():
    """d⁶ 고스핀 ([CoF6]3−) 과 저스핀 ([Co(en)3]3+) 배치."""
    h = 210
    b = ''
    for ox, title, t2g, eg, term in [(10, '[CoF' + sub('6') + ']³⁻ 고스핀', ['ud', 'u', 'u'], ['u', 'u'], '⁵T' + sub('2g') + ' (축퇴도 15)'),
                                     (170, '[Co(en)' + sub('3') + ']³⁺ 저스핀', ['ud', 'ud', 'ud'], ['', ''], '¹A' + sub('1g') + ' (축퇴도 1)')]:
        b += T(ox + 75, 18, title, 11.5, weight='bold')
        yE, yT = 70, (125 if ox == 10 else 155)
        for j, e in enumerate(eg):
            x0 = ox + 45 + j * 34
            b += L(x0, yE, x0 + 24, yE, w=2) + arrows(x0 + 12, yE, e)
        for j, e in enumerate(t2g):
            x0 = ox + 28 + j * 34
            b += L(x0, yT, x0 + 24, yT, w=2) + arrows(x0 + 12, yT, e)
        b += T(ox + 140, yE + 4, 'e' + sub('g'), 11, 'start') + T(ox + 140, yT + 4, 't' + sub('2g'), 11, 'start')
        b += L(ox + 20, yE, ox + 20, yT, color=MUT, w=1) + T(ox + 16, (yE + yT) / 2 + 4, 'Δ' + sub('o'), 11, 'end', MUT)
        b += T(ox + 75, 195, term, 11, color=ACC)
    return svg(h, b)


save('d_A04_walsh', walsh())
save('d_A10_ring', ring18())
save('d_B10_d6', d6())
