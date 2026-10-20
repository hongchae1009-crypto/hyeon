"""해설지에 들어가는 손그림 SVG(결정장 준위도, 단위세포, PCl2F3 이성질체)를 만든다."""
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
    W, H = 360, 560
    b = ''
    panels = [
        ('z-out (z축 늘어남)', [(f'b{sub(2)} (d{sub("xy")})', -30, ['']), (f'e (d{sub("xz")}, d{sub("yz")})', 15, ['u', 'u'])],
                              [(f'b{sub(1)} (d{sub("x²−y²")})', -20, ['u']), (f'a{sub(1)} (d{sub("z²")})', 20, ['u'])]),
        ('z-in (z축 줄어듦)', [(f'e (d{sub("xz")}, d{sub("yz")})', -15, ['u', '']), (f'b{sub(2)} (d{sub("xy")})', 30, ['u'])],
                             [(f'a{sub(1)} (d{sub("z²")})', -20, ['u']), (f'b{sub(1)} (d{sub("x²−y²")})', 20, ['u'])])]
    for k, (title, t2split, esplit) in enumerate(panels):
        oy = k * 280
        b += text(180, oy + 22, title, 16, 'middle', weight='bold')
        for parent, py, pe, split in [(f't{sub(2)}', oy + 85, ['u', 'u', ''], t2split), ('e', oy + 205, ['u', 'u'], esplit)]:
            s1, xe = level(34, py, pe, '')
            b += s1 + text(28, py + 5, parent, 15, 'end')
            for lab, dy, el in split:
                s2, _ = level(170, py + dy, el, lab)
                b += s2 + dash(xe + 2, py, 168, py + dy)
        if k == 0:
            b += f"<line x1='10' y1='270' x2='350' y2='270' stroke='{MUT}' stroke-width='0.8'/>"
    return svg(W, H, b)

def oh_jahn_teller():
    """[Cr(CN)6]4- (Oh, d4 저스핀) t2g4 → z-out."""
    W, H = 370, 250
    b = text(80, 22, f'O{sub("h")} (t{sub("2g")}⁴)', 16, 'middle', weight='bold')
    b += text(270, 22, 'z-out 일그러짐', 16, 'middle', weight='bold')
    s1, xe1 = level(40, 75, ['', ''], ''); b += s1 + text(34, 80, f'e{sub("g")}', 15, 'end')
    s1, xe2 = level(40, 185, ['ud', 'u', 'u'], ''); b += s1 + text(34, 190, f't{sub("2g")}', 15, 'end')
    for lab, y, el, px, py in [(f'd{sub("x²−y²")}', 55, [''], xe1, 75), (f'd{sub("z²")}', 95, [''], xe1, 75),
                               (f'd{sub("xy")} +⅔δ{sub(2)}', 160, [''], xe2, 185),
                               (f'd{sub("xz")}, d{sub("yz")} −⅓δ{sub(2)}', 205, ['ud', 'ud'], xe2, 185)]:
        s1, _ = level(180, y, el, lab); b += s1 + dash(px + 2, py, 178, y)
    return svg(W, H, b)

def ml5_levels():
    """d6 저스핀 [ML5]+ : 삼각쌍뿔(위) / 사각뿔(아래), 에너지는 Dq 눈금."""
    W, H = 360, 520
    b = ''
    panels = [(f'삼각쌍뿔 (D{sub("3h")})', 0, 7.07, -2.72,
               [(7.07, [''], f"a{sub(1)}′ (d{sub('z²')})  7.07"),
                (-0.82, ['u', 'u'], f"e′ (d{sub('x²−y²')}, d{sub('xy')})  −0.82"),
                (-2.72, ['ud', 'ud'], f"e″ (d{sub('xz')}, d{sub('yz')})  −2.72")]),
              (f'사각뿔 (C{sub("4v")})', 230, 9.14, -4.57,
               [(9.14, [''], f"b{sub(1)} (d{sub('x²−y²')})  9.14"),
                (0.86, [''], f"a{sub(1)} (d{sub('z²')})  0.86"),
                (-0.86, ['ud'], f"b{sub(2)} (d{sub('xy')})  −0.86"),
                (-4.57, ['ud', 'ud'], f"e (d{sub('xz')}, d{sub('yz')})  −4.57")])]
    for title, oy, top, bot, lv in panels:
        y0 = oy + 50 + top * 14
        def y(e): return y0 - e * 14
        b += text(180, oy + 22, title, 16, 'middle', weight='bold')
        b += f"<path d='M20 {y(bot)+20} L20 {oy+34} M15 {oy+44} L20 {oy+34} L25 {oy+44}' stroke='{MUT}' stroke-width='1.2' fill='none'/>"
        b += text(28, oy + 44, 'E (Dq)', 12, color=MUT)
        b += dash(20, y(0), 350, y(0)) + text(352, y(0) + 4, '0', 11, color=MUT)
        for e, el, lab in lv:
            off = -7 if e == 0.86 else (7 if e == -0.86 else 0)
            s1, _ = level(50, y(e) + off, el, lab)
            b += s1
    return svg(W, H, b)

def unit_cell():
    W, H = 360, 360
    a, cx, cy = 120, 180, 185
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
    b += text(cx, 22, '음이온 4 × ¼ = 1, 양이온 1 → XY', 15, 'middle', weight='bold')
    b += text(cx, y0 + a + r + 24, '한 변 a = 2r₋', 15, 'middle')
    b += text(cx, y0 + a + r + 46, '대각선 √2a = 2r₋ + 2r₊', 15, 'middle', '#c2410c')
    return svg(W, H, b)

def tbp(ox, ax1, ax2, eq_left, eq_w, eq_d, title, pg):
    cx, cy = ox + 62, 115
    b = text(cx, 22, title, 14, 'middle', weight='bold')
    b += f"<line x1='{cx}' y1='{cy}' x2='{cx}' y2='{cy-48}' stroke='{INK}' stroke-width='2'/>"
    b += f"<line x1='{cx}' y1='{cy}' x2='{cx}' y2='{cy+48}' stroke='{INK}' stroke-width='2'/>"
    b += f"<line x1='{cx}' y1='{cy}' x2='{cx-38}' y2='{cy}' stroke='{INK}' stroke-width='2'/>"
    b += f"<polygon points='{cx},{cy} {cx+34},{cy+17} {cx+31},{cy+24}' fill='{INK}'/>"
    for i in range(1, 6):
        t = i / 6
        x, yy = cx + 34 * t, cy - 18 * t
        b += f"<line x1='{x}' y1='{yy-3*t}' x2='{x}' y2='{yy+3*t}' stroke='{INK}' stroke-width='1.5'/>"
    b += f"<circle cx='{cx}' cy='{cy}' r='11' fill='white'/>" + text(cx, cy + 6, 'P', 16, 'middle', weight='bold')
    b += text(cx, cy - 54, ax1, 15, 'middle') + text(cx, cy + 66, ax2, 15, 'middle')
    b += text(cx - 43, cy + 6, eq_left, 15, 'end') + text(cx + 36, cy + 38, eq_w, 15) + text(cx + 38, cy - 20, eq_d, 15)
    b += text(cx, 222, pg, 16, 'middle', ACC, 'bold')
    return b

def pcl2f3():
    b = tbp(0, 'F', 'F', 'F', 'Cl', 'Cl', '주어진 구조', f'C{sub("2v")}')
    b += tbp(120, 'Cl', 'Cl', 'F', 'F', 'F', '구조 Ⅰ', f'D{sub("3h")}')
    b += tbp(240, 'F', 'Cl', 'F', 'Cl', 'F', '구조 Ⅱ', f'C{sub("s")}')
    return svg(360, 235, b)

def benzyne(ox, tri, dbl, title):
    cx, cy, R = ox + 72, 95, 38
    v = [(cx + R * math.cos(math.radians(-30 + 60 * i)), cy + R * math.sin(math.radians(-30 + 60 * i))) for i in range(6)]
    b = ''
    for i in range(6):
        (x1, y1), (x2, y2) = v[i], v[(i + 1) % 6]
        b += f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{INK}' stroke-width='2'/>"
    def inner(i, k):
        (x1, y1), (x2, y2) = v[i], v[(i + 1) % 6]
        f, sh = 1 - 0.17 * k, 0.18
        ax, ay = cx + (x1 - cx) * f, cy + (y1 - cy) * f
        bx, by = cx + (x2 - cx) * f, cy + (y2 - cy) * f
        ax, bx, ay, by = ax + (bx - ax) * sh, bx - (bx - ax) * sh, ay + (by - ay) * sh, by - (by - ay) * sh
        return f"<line x1='{ax:.1f}' y1='{ay:.1f}' x2='{bx:.1f}' y2='{by:.1f}' stroke='{INK}' stroke-width='2'/>"
    for i in dbl: b += inner(i, 1)
    b += inner(tri, 1) + inner(tri, -1)
    mx, my = v[0]
    b += f"<line x1='{mx:.1f}' y1='{my:.1f}' x2='{mx+26:.1f}' y2='{my-14:.1f}' stroke='{INK}' stroke-width='2'/>" + text(mx + 28, my - 14, 'CH₃', 15)
    b += text(cx, 172, title, 14, 'middle', weight='bold')
    return b

def benzynes():
    # v0 = 메틸 탄소. 3-methylbenzyne: 삼중결합 v1–v2 (메틸에 이웃), 4-methylbenzyne: v2–v3
    b = benzyne(0, 1, [3, 5], 'E-1 3-methylbenzyne') + benzyne(180, 2, [4, 0], 'E-2 4-methylbenzyne')
    return svg(360, 185, b)

for name, s in [('d_B07_E', benzynes()), ('d_B08_td', td_jahn_teller()), ('d_B08_oh', oh_jahn_teller()), ('d_B09', ml5_levels()),
                ('d_A04', unit_cell()), ('d_A12', pcl2f3())]:
    open(os.path.join(OUT, name + '.svg'), 'w').write(s)
    print(name)
