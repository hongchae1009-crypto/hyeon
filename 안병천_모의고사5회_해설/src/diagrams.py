"""안병천 5회 해설의 손그림 SVG: 알릴 π MO와 역결합, d⁸ 사면체/팔면체 배치, 3중심 2전자 MO,
2s 동경 함수, 의자형 1,3-이축 상호작용."""
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
def allyl():
    b = T(W / 2, 16, '알릴(C₃H₅) π 분자 궤도함수 (위에서 아래로 에너지↓)', 11.5, weight='bold')
    rows = [('ψ₃ (마디 2, 빈 π*)', [0.5, -0.707, 0.5], 62, RED),
            ('ψ₂ (마디 1, 비결합)', [0.707, 0, -0.707], 142, INK),
            ('ψ₁ (마디 0, 결합)', [0.5, 0.707, 0.5], 222, INK)]
    for lab, cs, y, col in rows:
        for k, c in enumerate(cs):
            x = 40 + 40 * k
            b += p_orb(x, y, c)
        b += L(40, y, 120, y, MUT, 1, '3 3')
        b += T(135, y + 4, lab, 11, 'start', col, 'bold' if col == RED else 'normal')
    b += T(80, 262, 'C1   C2   C3', 10, color=MUT)
    # 오른쪽 아래: 겹침 그림 (x축 방향에서 본 모습)
    b += L(10, 278, W - 10, 278, '#e5e7eb', 1)
    b += T(W / 2, 296, 'ψ₃ ↔ Mn d' + sub('yz') + ' 겹침 (x축 방향에서 본 모습)', 11.5, weight='bold')
    zc = 345     # 알릴 평면 높이
    # 왼쪽 열: C1·C3 (y<0, 겹쳐 보임), 오른쪽 열: C2 (y>0)
    b += lobe(120, zc - 16, 9, 16, False) + lobe(120, zc + 16, 9, 16, True)
    b += lobe(210, zc - 20, 11, 20, True) + lobe(210, zc + 20, 11, 20, False)
    b += f"<circle cx='120' cy='{zc}' r='2.5' fill='{INK}'/><circle cx='210' cy='{zc}' r='2.5' fill='{INK}'/>"
    b += T(92, zc + 4, 'C1·C3', 10.5, 'end') + T(238, zc + 4, 'C2', 10.5, 'start')
    mz = 440     # Mn 위치
    for sx, sz, fill in [(-1, -1, True), (1, -1, False), (-1, 1, False), (1, 1, True)]:
        cx, cy = 165 + sx * 22, mz + sz * 22
        ang = -45 if sx * sz > 0 else 45
        b += (f"<ellipse cx='{cx}' cy='{cy}' rx='9' ry='20' transform='rotate({ang} {cx} {cy})' "
              f"fill='{RED if fill else 'white'}' fill-opacity='0.5' stroke='{RED}' stroke-width='1.3'/>")
    b += f"<circle cx='165' cy='{mz}' r='3' fill='{INK}'/>" + T(165, mz + 50, 'Mn (d' + sub('yz') + ', 채워짐)', 10.5, color=RED)
    b += L(285, 470, 285, 420, MUT, 1.2) + T(285, 414, 'z', 10, color=MUT) + L(285, 470, 315, 470, MUT, 1.2) + T(322, 474, 'y', 10, color=MUT)
    b += T(W / 2, 512, '같은 색 로브끼리 마주봄 → 0이 아닌 겹침', 10.5, color=RED)
    b += T(W / 2, 528, 'Mn의 채워진 d 전자가 빈 ψ₃로 이동 (π 역결합)', 10.5, color=RED)
    return svg(538, b)


# ---------- A11: d⁸ 사면체 바닥·들뜬 배치와 팔면체 비교 ----------
def d8():
    b = T(55, 16, 'Td 바닥 ³T₁(F)', 11, weight='bold') + T(165, 16, 'Td 들뜸 ³T₂', 11, weight='bold')
    b += T(275, 16, 'Oh [NiCl₆]⁴⁻', 11, weight='bold')
    # Td: t2 위, e 아래
    b += lev(20, 55, ['ud', 'u', 'u']) + T(14, 59, f't{sub("2")}', 11, 'end')
    b += lev(32, 115, ['ud', 'ud']) + T(26, 119, 'e', 11, 'end')
    b += lev(130, 55, ['ud', 'ud', 'u']) + T(124, 59, f't{sub("2")}', 11, 'end')
    b += lev(142, 115, ['ud', 'u']) + T(136, 119, 'e', 11, 'end')
    b += f"<path d='M{100} 55 L{100} 115' stroke='{ACC}' stroke-width='1.2'/>" + T(102, 90, 'Δt', 10.5, 'start', ACC)
    # Oh: eg 위, t2g 아래
    b += lev(252, 45, ['u', 'u']) + T(246, 49, f'e{sub("g")}', 11, 'end')
    b += lev(240, 120, ['ud', 'ud', 'ud']) + T(234, 124, f't{sub("2g")}', 11, 'end')
    b += T(55, 142, f'e{sup("4")}t{sub("2")}{sup("4")}', 11) + T(165, 142, f'e{sup("3")}t{sub("2")}{sup("5")}', 11)
    b += T(275, 142, f't{sub("2g")}{sup("6")}e{sub("g")}{sup("2")}', 11)
    b += T(55, 160, '−0.8Δt', 10.5, color=RED) + T(165, 160, '(e→t₂ 1개 = Δt)', 10, color=MUT)
    b += T(275, 160, '−1.2Δo', 10.5, color=RED)
    return svg(170, b)


# ---------- B6: B–H–B 3중심 2전자 결합 MO ----------
def threec():
    b = T(W / 2, 16, 'B₁–H_A–B₂ 3중심 2전자 결합', 11.5, weight='bold')
    xl, xm, xr = 40, 150, 265
    # 왼쪽: B sp³ 두 개의 대칭·반대칭 조합
    b += L(xl, 120, xl + 50, 120) + T(xl + 25, 112, 'χB₁−χB₂', 10.5)
    b += L(xl, 140, xl + 50, 140) + T(xl + 25, 158, 'χB₁+χB₂', 10.5)
    b += T(xl + 25, 178, 'B sp³ 조합', 10, color=MUT)
    # 오른쪽: H 1s
    b += L(xr, 130, xr + 40, 130) + T(xr + 20, 122, 'H 1s', 10.5)
    # 가운데 MO
    b += L(xm, 50, xm + 50, 50, RED, 2) + T(xm + 25, 42, 'ψ_a (반결합)', 10.5, color=RED)
    b += L(xm, 120, xm + 50, 120, INK, 2) + T(xm + 25, 112, 'ψ_n (비결합)', 10.5)
    b += L(xm, 215, xm + 50, 215, ACC, 2) + arrows(xm + 25, 215, 'ud') + T(xm + 25, 233, 'ψ_b (결합, 전자 2개)', 10.5, color=ACC)
    for y1, y2 in [(140, 50), (140, 215)]:
        b += L(xl + 50, y1, xm, y2, MUT, 1, '3 3')
    for y2 in (50, 215):
        b += L(xr, 130, xm + 50, y2, MUT, 1, '3 3')
    b += L(xl + 50, 120, xm, 120, MUT, 1, '3 3')
    b += T(W / 2, 256, 'ψ_b = ½χB₁ + (1/√2)χH + ½χB₂', 10.5)
    b += T(W / 2, 272, 'ψ_n = (1/√2)(χB₁ − χB₂)   (H 1s와 대칭이 안 맞음)', 10.5)
    b += T(W / 2, 288, 'ψ_a = ½χB₁ − (1/√2)χH + ½χB₂', 10.5, color=RED)
    return svg(298, b)


# ---------- A10: 2s 동경 함수와 마디 ----------
def radial2s():
    x0, y0, sx, sy = 40, 110, 22, 38      # r/a0 1당 22 px, R 1당 38 px (R = (2 − ρ)e^(−ρ/2))
    b = T(W / 2, 16, 'R(r) ∝ (2 − r/a₀) e' + sup('−r/2a₀') + '  와  r²R²', 11.5, weight='bold')
    b += L(x0, y0, x0 + 12 * sx, y0, MUT, 1.2) + L(x0, 30, x0, 150, MUT, 1.2)
    for k in range(0, 13, 2):
        b += L(x0 + k * sx, y0, x0 + k * sx, y0 + 4, MUT, 1) + T(x0 + k * sx, y0 + 16, str(k), 9.5, color=MUT)
    b += T(x0 + 12 * sx + 6, y0 + 4, 'r/a₀', 10, 'start', MUT)
    pts = ' '.join(f'{x0 + r * sx:.1f},{y0 - sy * (2 - r) * math.exp(-r / 2):.1f}' for r in [i * 0.05 for i in range(241)])
    b += f"<polyline points='{pts}' fill='none' stroke='{ACC}' stroke-width='1.8'/>"
    rd = [i * 0.05 for i in range(241)]
    pr = [(r * r * (2 - r) ** 2 * math.exp(-r)) for r in rd]
    m = max(pr)
    pts2 = ' '.join(f'{x0 + r * sx:.1f},{y0 - 60 * p / m:.1f}' for r, p in zip(rd, pr))
    b += f"<polyline points='{pts2}' fill='none' stroke='{GRN}' stroke-width='1.5' stroke-dasharray='5 3'/>"
    b += f"<circle cx='{x0 + 2 * sx}' cy='{y0}' r='4' fill='{RED}'/>" + T(x0 + 2 * sx + 4, y0 + 36, '↑ r = 2a₀ (방사상 마디)', 10.5, 'start', RED)
    b += T(x0 + 6, 40, 'R (파랑)', 10, 'start', ACC) + T(x0 + 150, 38, 'r²R² (초록 점선, 상대값)', 10, 'start', GRN)
    return svg(160, b)


# ---------- B8: 의자형 1,3-이축 상호작용 ----------
CHAIR = [(0, 14), (24, 28), (58, 20), (82, 6), (58, -8), (24, 0)]
AX = {0: 1, 1: -1, 2: 1, 3: -1, 4: 1, 5: -1}   # 축 결합 방향(+1 아래, -1 위)


def chair(ox, oy, subs):
    P = [(ox + x, oy + y) for x, y in CHAIR]
    b = ''
    for i in range(6):
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % 6]
        b += L(x1, y1, x2, y2, INK, 1.8)
    cx = sum(p[0] for p in P) / 6
    for i, items in subs.items():
        x, y = P[i]
        d = AX[i]
        for kind, lab, col in items:
            if kind == 'ax':
                x2, y2 = x, y + 26 * d
                b += L(x, y, x2, y2, col, 1.7)
                b += T(x2, y2 + (12 if d > 0 else -4), lab, 10.5, color=col, weight='bold')
            else:
                dx = -1 if x < cx else 1
                x2, y2 = x + 24 * dx, y - (2 if i == 5 else 7) * d - (6 if i == 5 else 0)
                b += L(x, y, x2, y2, col, 1.7)
                b += T(x2 + 3 * dx, y2 + 4, lab, 10.5, 'end' if dx < 0 else 'start', col, 'bold')
    return b


def chairs_b8():
    b = ''
    blocks = [
        ('B cis-1-Cl-3-CH₃', 'Cl', 'CH₃', GRN, 'ΔE = 3.7', '0.25 + 0.90 + E(Cl↔CH₃)'),
        ('C cis-1,3-(CH₃)₂', 'CH₃', 'CH₃', INK, 'ΔE = 5.5', '0.90 + 0.90 + E(CH₃↔CH₃)'),
    ]
    y = 16
    for title, s1, s2, c1, de, formula in blocks:
        b += T(W / 2, y, title + ' : 이적도(왼쪽) ⇌ 이축(오른쪽)', 11, weight='bold')
        b += chair(28, y + 46, {3: [('eq', s1, c1)], 5: [('eq', s2, INK)]})
        b += chair(200, y + 56, {3: [('ax', s1, c1)], 5: [('ax', s2, INK)]})
        # 1,3-이축 상호작용 표시 (두 축 결합 끝 사이)
        P = [(200 + x, y + 56 + yy) for x, yy in CHAIR]
        b += L(P[5][0] + 6, P[5][1] - 30, P[3][0] - 6, P[3][1] - 30, RED, 1.4, '3 2')
        b += T(W / 2, y + 112, f'{de} kcal/mol = {formula}', 10.5, color=RED)
        y += 132
    return svg(y - 6, b)


save('d_A04_allyl', allyl())
save('d_A10_radial', radial2s())
save('d_A11_d8', d8())
save('d_B06_3c2e', threec())
save('d_B08_chair', chairs_b8())
