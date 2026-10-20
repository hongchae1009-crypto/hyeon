"""해설지에 들어가는 손그림 SVG(결정장 준위도, 단위세포, PCl2F3 이성질체)를 만든다."""
import math, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'img')
INK, ACC, MUT = '#1f2933', '#1d4ed8', '#6b7280'
FONT = "font-family='Noto Sans KR, sans-serif'"

def svg(w, h, body):
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}'>"
            f"<rect width='{w}' height='{h}' fill='white'/>{body}</svg>")

def text(x, y, s, size=13, anchor='start', color=INK, weight='normal'):
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
        out += text(xe + 8, y + 4, label, 12) if side == 'right' else text(x - 8, y + 4, label, 12, 'end')
    return out, xe

def dash(x1, y1, x2, y2):
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{MUT}' stroke-width='1' stroke-dasharray='3 3'/>"

def td_jahn_teller():
    """[FeO4]4- (Td, d4 고스핀) z-out / z-in."""
    W, H = 760, 300
    b = ''
    for k, (title, t2split, esplit) in enumerate([
        ('z-out (z축 늘어남)', [('b<tspan baseline-shift="sub" font-size="9">2</tspan> (d<tspan baseline-shift="sub" font-size="9">xy</tspan>)', -30, ['']),
                               ('e (d<tspan baseline-shift="sub" font-size="9">xz</tspan>, d<tspan baseline-shift="sub" font-size="9">yz</tspan>)', 15, ['u', 'u'])],
                              [('b<tspan baseline-shift="sub" font-size="9">1</tspan> (d<tspan baseline-shift="sub" font-size="9">x²−y²</tspan>)', -22, ['u']),
                               ('a<tspan baseline-shift="sub" font-size="9">1</tspan> (d<tspan baseline-shift="sub" font-size="9">z²</tspan>)', 22, ['u'])]),
        ('z-in (z축 줄어듦)', [('e (d<tspan baseline-shift="sub" font-size="9">xz</tspan>, d<tspan baseline-shift="sub" font-size="9">yz</tspan>)', -15, ['u', '']),
                              ('b<tspan baseline-shift="sub" font-size="9">2</tspan> (d<tspan baseline-shift="sub" font-size="9">xy</tspan>)', 30, ['u'])],
                             [('a<tspan baseline-shift="sub" font-size="9">1</tspan> (d<tspan baseline-shift="sub" font-size="9">z²</tspan>)', -22, ['u']),
                              ('b<tspan baseline-shift="sub" font-size="9">1</tspan> (d<tspan baseline-shift="sub" font-size="9">x²−y²</tspan>)', 22, ['u'])])]):
        ox = 20 + k * 380
        b += text(ox + 170, 22, title, 14, 'middle', weight='bold')
        for (parent, py, pe, split) in [('t<tspan baseline-shift="sub" font-size="9">2</tspan>', 95, ['u', 'u', ''], t2split),
                                        ('e', 225, ['u', 'u'], esplit)]:
            s, xe = level(ox + 40, py, pe, '')
            b += s + text(ox + 32, py + 4, parent, 13, 'end')
            for lab, dy, el in split:
                s2, _ = level(ox + 190, py + dy, el, lab)
                b += s2 + dash(xe + 2, py, ox + 188, py + dy)
        b += text(ox + 70, 285, 'T<tspan baseline-shift="sub" font-size="9">d</tspan>', 12, 'middle', MUT)
    return svg(W, H, b)

def oh_jahn_teller():
    """[Cr(CN)6]4- (Oh, d4 저스핀) t2g4 → z-out."""
    W, H = 560, 260
    b = text(110, 22, 'O<tspan baseline-shift="sub" font-size="9">h</tspan> (t<tspan baseline-shift="sub" font-size="9">2g</tspan>⁴)', 14, 'middle', weight='bold')
    b += text(400, 22, 'z-out 일그러짐 (D<tspan baseline-shift="sub" font-size="9">4h</tspan>)', 14, 'middle', weight='bold')
    s, xe1 = level(60, 80, ['', ''], ''); b += s + text(52, 84, 'e<tspan baseline-shift="sub" font-size="9">g</tspan>', 13, 'end')
    s, xe2 = level(60, 190, ['ud', 'u', 'u'], ''); b += s + text(52, 194, 't<tspan baseline-shift="sub" font-size="9">2g</tspan>', 13, 'end')
    for lab, y, el, px, py in [('d<tspan baseline-shift="sub" font-size="9">x²−y²</tspan>', 58, [''], xe1, 80),
                               ('d<tspan baseline-shift="sub" font-size="9">z²</tspan>', 102, [''], xe1, 80),
                               ('d<tspan baseline-shift="sub" font-size="9">xy</tspan>  (+⅔δ<tspan baseline-shift="sub" font-size="9">2</tspan>)', 165, [''], xe2, 190),
                               ('d<tspan baseline-shift="sub" font-size="9">xz</tspan>, d<tspan baseline-shift="sub" font-size="9">yz</tspan>  (−⅓δ<tspan baseline-shift="sub" font-size="9">2</tspan> 씩)', 205, ['ud', 'ud'], xe2, 190)]:
        s, _ = level(300, y, el, lab); b += s + dash(px + 2, py, 298, y)
    b += f"<path d='M175 135 L235 135 M226 129 L235 135 L226 141' stroke='{INK}' stroke-width='1.6' fill='none'/>"
    return svg(W, H, b)

def ml5_levels():
    """d6 저스핀 [ML5]+ : 삼각쌍뿔(TBP) / 사각뿔(SP), 에너지는 Dq 눈금."""
    W, H = 720, 400
    def y(e): return 215 - e * 19
    b = ''
    cols = [('삼각쌍뿔 (D<tspan baseline-shift="sub" font-size="9">3h</tspan>)', 40,
             [(7.07, ['' ], "a<tspan baseline-shift='sub' font-size='9'>1</tspan>′ (d<tspan baseline-shift='sub' font-size='9'>z²</tspan>)  7.07"),
              (-0.82, ['u', 'u'], "e′ (d<tspan baseline-shift='sub' font-size='9'>x²−y²</tspan>, d<tspan baseline-shift='sub' font-size='9'>xy</tspan>)  −0.82"),
              (-2.72, ['ud', 'ud'], "e″ (d<tspan baseline-shift='sub' font-size='9'>xz</tspan>, d<tspan baseline-shift='sub' font-size='9'>yz</tspan>)  −2.72")]),
            ('사각뿔 (C<tspan baseline-shift="sub" font-size="9">4v</tspan>)', 390,
             [(9.14, [''], "b<tspan baseline-shift='sub' font-size='9'>1</tspan> (d<tspan baseline-shift='sub' font-size='9'>x²−y²</tspan>)  9.14"),
              (0.86, [''], "a<tspan baseline-shift='sub' font-size='9'>1</tspan> (d<tspan baseline-shift='sub' font-size='9'>z²</tspan>)  0.86"),
              (-0.86, ['ud'], "b<tspan baseline-shift='sub' font-size='9'>2</tspan> (d<tspan baseline-shift='sub' font-size='9'>xy</tspan>)  −0.86"),
              (-4.57, ['ud', 'ud'], "e (d<tspan baseline-shift='sub' font-size='9'>xz</tspan>, d<tspan baseline-shift='sub' font-size='9'>yz</tspan>)  −4.57")])]
    for title, ox, lv in cols:
        b += text(ox + 140, 22, title, 14, 'middle', weight='bold')
        b += f"<path d='M{ox} 380 L{ox} 40 M{ox-5} 50 L{ox} 40 L{ox+5} 50' stroke='{MUT}' stroke-width='1.2' fill='none'/>" + text(ox + 6, 48, 'E (Dq)', 11, color=MUT)
        b += dash(ox, y(0), ox + 300, y(0)) + text(ox + 302, y(0) + 4, '0', 10, color=MUT)
        for e, el, lab in lv:
            s, _ = level(ox + 40, y(e) + (-9 if e == 0.86 else 0) + (9 if e == -0.86 else 0), el, lab)
            b += s
    return svg(W, H, b)

def unit_cell():
    W, H = 420, 380
    a, cx, cy = 130, 190, 200
    r = a / 2; rp = r * (math.sqrt(2) - 1)
    x0, y0 = cx - a / 2, cy - a / 2
    b = f"<clipPath id='c'><rect x='{x0}' y='{y0}' width='{a}' height='{a}'/></clipPath>"
    for dx in (0, a):
        for dy in (0, a):
            b += f"<circle cx='{x0+dx}' cy='{y0+dy}' r='{r}' fill='none' stroke='{MUT}' stroke-width='1.2'/>"
            b += f"<circle cx='{x0+dx}' cy='{y0+dy}' r='{r}' fill='#dbe4f0' stroke='{INK}' stroke-width='1.5' clip-path='url(#c)'/>"
    b += f"<rect x='{x0}' y='{y0}' width='{a}' height='{a}' fill='none' stroke='{INK}' stroke-width='2'/>"
    b += f"<circle cx='{cx}' cy='{cy}' r='{rp}' fill='#555' stroke='{INK}'/>"
    b += f"<line x1='{x0}' y1='{y0+a}' x2='{x0+a}' y2='{y0}' stroke='#c2410c' stroke-width='1.5' stroke-dasharray='5 3'/>"
    b += text(cx, y0 + a + r + 22, '한 변 a = 2r₋', 13, 'middle')
    b += text(cx, y0 + a + r + 42, '대각선 √2a = 2r₋ + 2r₊', 12, 'middle', '#c2410c')
    b += text(cx, 20, '음이온 4 × ¼ = 1,  양이온 1 → XY', 13, 'middle', weight='bold')
    return svg(W, H, b)

def tbp(ox, ax1, ax2, eq_left, eq_w, eq_d, title, pg):
    cx, cy = ox + 90, 120
    b = text(cx, 22, title, 13, 'middle', weight='bold')
    b += f"<line x1='{cx}' y1='{cy}' x2='{cx}' y2='{cy-55}' stroke='{INK}' stroke-width='2'/>"
    b += f"<line x1='{cx}' y1='{cy}' x2='{cx}' y2='{cy+55}' stroke='{INK}' stroke-width='2'/>"
    b += f"<line x1='{cx}' y1='{cy}' x2='{cx-55}' y2='{cy}' stroke='{INK}' stroke-width='2'/>"
    b += f"<polygon points='{cx},{cy} {cx+48},{cy+22} {cx+44},{cy+30}' fill='{INK}'/>"
    for i in range(1, 7):
        t = i / 7
        x, yy = cx + 48 * t, cy - 24 * t
        b += f"<line x1='{x}' y1='{yy-3*t}' x2='{x}' y2='{yy+3*t}' stroke='{INK}' stroke-width='1.5'/>"
    b += f"<circle cx='{cx}' cy='{cy}' r='13' fill='white'/>" + text(cx, cy + 5, 'P', 15, 'middle', weight='bold')
    b += text(cx, cy - 60, ax1, 14, 'middle') + text(cx, cy + 73, ax2, 14, 'middle')
    b += text(cx - 62, cy + 5, eq_left, 14, 'end') + text(cx + 54, cy + 38, eq_w, 14) + text(cx + 54, cy - 24, eq_d, 14)
    b += text(cx, 222, pg, 14, 'middle', ACC, 'bold')
    return b

def pcl2f3():
    b = tbp(0, 'F', 'F', 'F', 'Cl', 'Cl', '주어진 구조 (축 F 2개)', 'C<tspan baseline-shift="sub" font-size="10">2v</tspan>')
    b += tbp(200, 'Cl', 'Cl', 'F', 'F', 'F', '구조 Ⅰ (축 Cl 2개)', 'D<tspan baseline-shift="sub" font-size="10">3h</tspan>')
    b += tbp(400, 'F', 'Cl', 'F', 'Cl', 'F', '구조 Ⅱ (축 F, Cl)', 'C<tspan baseline-shift="sub" font-size="10">s</tspan>')
    return svg(600, 235, b)

def benzyne(ox, tri, dbl, title):
    cx, cy, R = ox + 90, 105, 42
    v = [(cx + R * math.cos(math.radians(-90 + 60 * i + 60)), cy + R * math.sin(math.radians(-90 + 60 * i + 60))) for i in range(6)]
    # v[5]은 위쪽 꼭짓점... 메틸은 v[0](오른쪽 위)에 단다
    b = ''
    for i in range(6):
        (x1, y1), (x2, y2) = v[i], v[(i + 1) % 6]
        b += f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{INK}' stroke-width='2'/>"
    def inner(i, k):
        (x1, y1), (x2, y2) = v[i], v[(i + 1) % 6]
        f = 1 - 0.17 * k
        sh = 0.18
        ax, ay = cx + (x1 - cx) * f, cy + (y1 - cy) * f
        bx, by = cx + (x2 - cx) * f, cy + (y2 - cy) * f
        ax, bx = ax + (bx - ax) * sh, bx - (bx - ax) * sh
        ay, by = ay + (by - ay) * sh, by - (by - ay) * sh
        return f"<line x1='{ax:.1f}' y1='{ay:.1f}' x2='{bx:.1f}' y2='{by:.1f}' stroke='{INK}' stroke-width='2'/>"
    for i in dbl: b += inner(i, 1)
    b += inner(tri, 1) + inner(tri, -1)
    mx, my = v[0]
    b += f"<line x1='{mx:.1f}' y1='{my:.1f}' x2='{mx+34:.1f}' y2='{my-18:.1f}' stroke='{INK}' stroke-width='2'/>" + text(mx + 36, my - 18, 'CH₃', 14)
    b += text(cx, 190, title, 13, 'middle', weight='bold')
    return b

def benzynes():
    # v0=메틸 탄소. 3-methylbenzyne: 삼중결합 v1–v2 (메틸에 이웃), 4-methylbenzyne: 삼중결합 v2–v3
    b = benzyne(0, 1, [3, 5], 'E-1  3-methylbenzyne') + benzyne(260, 2, [4, 0], 'E-2  4-methylbenzyne')
    return svg(520, 205, b)

for name, s in [('d_B07_E', benzynes()), ('d_B08_td', td_jahn_teller()), ('d_B08_oh', oh_jahn_teller()), ('d_B09', ml5_levels()),
                ('d_A04', unit_cell()), ('d_A12', pcl2f3())]:
    open(os.path.join(OUT, name + '.svg'), 'w').write(s)
    print(name)
