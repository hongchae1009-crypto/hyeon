"""김지현 5회 손그림 도표: A9 LMCT 준위도, B10 Hammond 에너지 도표."""
import os
IMG = os.path.join(os.path.dirname(__file__), '..', 'img')
INK, MUT, ACC, RED = '#1f2933', '#6b7280', '#1d4ed8', '#c0392b'
F = "font-family='Noto Sans KR, sans-serif'"


def T(x, y, s, size=13, anchor='middle', color=INK, w='normal'):
    return f"<text x='{x}' y='{y}' font-size='{size}' text-anchor='{anchor}' fill='{color}' font-weight='{w}' {F}>{s}</text>"


def lev(x, y, n, elec, w=22, gap=6):
    out = ''
    for i in range(n):
        x0 = x + i * (w + gap)
        out += f"<line x1='{x0}' y1='{y}' x2='{x0+w}' y2='{y}' stroke='{INK}' stroke-width='2'/>"
        e = elec[i] if i < len(elec) else ''
        cx = x0 + w / 2
        if 'u' in e:
            xx = cx - (4 if 'd' in e else 0)
            out += f"<path d='M{xx} {y-3} L{xx} {y-18} M{xx-3.5} {y-13} L{xx} {y-18} L{xx+3.5} {y-13}' stroke='{ACC}' stroke-width='1.6' fill='none'/>"
        if 'd' in e:
            xx = cx + 4
            out += f"<path d='M{xx} {y-18} L{xx} {y-3} M{xx-3.5} {y-8} L{xx} {y-3} L{xx+3.5} {y-8}' stroke='{ACC}' stroke-width='1.6' fill='none'/>"
    return out


def arrow(x1, y1, x2, y2, c=RED):
    # 아래→위 화살표(들뜸)
    return (f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2+6}' stroke='{c}' stroke-width='1.6'/>"
            f"<polygon points='{x2},{y2} {x2-4},{y2+8} {x2+4},{y2+8}' fill='{c}'/>")


def lmct():
    W, H = 360, 300
    b = ''
    for k, (title, t2g, ox) in enumerate([('[Fe(CN)₆]³⁻ 저스핀 d⁵', ['ud', 'ud', 'u'], 10), ('[Fe(CN)₆]⁴⁻ 저스핀 d⁶', ['ud', 'ud', 'ud'], 185)]):
        b += T(ox + 82, 20, title, 13, w='bold')
        b += lev(ox + 48, 70, 2, []) + T(ox + 38, 74, 'e<tspan baseline-shift="sub" font-size="9">g</tspan>*', 12, 'end')
        b += lev(ox + 34, 150, 3, t2g) + T(ox + 28, 154, 't<tspan baseline-shift="sub" font-size="9">2g</tspan>', 12, 'end')
        b += lev(ox + 34, 250, 3, ['ud', 'ud', 'ud']) + T(ox + 28, 254, 'L(σ/π)', 11, 'end')
        b += arrow(ox + 140, 245, ox + 140, 74) + T(ox + 150, 170, '①', 12, 'start', RED)
        if k == 0:
            b += arrow(ox + 125, 245, ox + 125, 154, '#d97706') + T(ox + 112, 205, '②', 12, 'end', '#d97706')
        b += T(ox + 82, 285, '띠 2개 (①, ②)' if k == 0 else 't₂g 꽉 참 → 띠 1개 (①)', 12, color=MUT)
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' width='{W}' height='{H}'><rect width='{W}' height='{H}' fill='white'/>{b}</svg>"


def hammond():
    W, H = 360, 330
    b = ''
    for k, (title, dh1, dh2, ox) in enumerate([('Cl· (발열)', -21, -34, 10), ('Br· (흡열)', 42, 29, 190)]):
        b += T(ox + 80, 20, title, 13, w='bold')
        y0 = 190
        s = 1.6
        y1, y2 = y0 - dh1 * s, y0 - dh2 * s
        top1, top2 = (y0 - 60, y0 - 55) if k == 0 else (y1 - 22, y2 - 20)
        b += f"<line x1='{ox+10}' y1='{y0}' x2='{ox+40}' y2='{y0}' stroke='{INK}' stroke-width='2'/>"
        for (yt, ye, col, lab) in [(top1, y1, RED, '1°'), (top2, y2, ACC, '2°')]:
            b += (f"<path d='M{ox+40},{y0} C{ox+65},{y0} {ox+70},{yt} {ox+85},{yt} S{ox+105},{ye} {ox+130},{ye}' "
                  f"fill='none' stroke='{col}' stroke-width='1.8'/>")
            b += f"<line x1='{ox+130}' y1='{ye}' x2='{ox+160}' y2='{ye}' stroke='{col}' stroke-width='2'/>"
            b += T(ox + 163, ye + 4, f'{lab}', 11, 'start', col)
        b += T(ox + 25, y0 + 16, 'R–H + X·', 10.5)
        b += T(ox + 85, 290, 'TS가 반응물 닮음 → 차이 작음' if k == 0 else 'TS가 라디칼 닮음 → 차이 큼', 11.5, color=MUT)
        b += T(ox + 85, 308, '1°/2° 혼합 (선택성 작음)' if k == 0 else '2° 우세 (선택성 큼)', 11.5, color=MUT)
    b += f"<path d='M8 270 L8 40 M3 50 L8 40 L13 50' stroke='{MUT}' fill='none'/>" + T(14, 48, 'E', 11, 'start', MUT)
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' width='{W}' height='{H}'><rect width='{W}' height='{H}' fill='white'/>{b}</svg>"


for n, s in [('d_A09_lmct', lmct()), ('d_B10_hammond', hammond())]:
    open(os.path.join(IMG, n + '.svg'), 'w').write(s)
    print(n)
