"""해설지에 들어가는 손그림 SVG(스핀-궤도 갈라짐, Cu²⁺ Jahn–Teller)를 만든다."""
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


def au4f():
    """Au 4f 스핀-궤도 갈라짐: j=7/2(+3/2 hcÃ, 8겹), j=5/2(−2 hcÃ, 6겹)."""
    W, H = 360, 260
    b = text(180, 22, 'Au 4f (l = 3, s = ½)', 15, 'middle', weight='bold')
    b += f"<line x1='30' y1='140' x2='110' y2='140' stroke='{INK}' stroke-width='2'/>" + text(70, 160, '4f', 14, 'middle')
    for y, lab, n in [(70, 'j = 7/2  (+3/2 hcÃ)', 8), (215, 'j = 5/2  (−2 hcÃ)', 6)]:
        b += dash(112, 140, 150, y)
        b += f"<line x1='150' y1='{y}' x2='210' y2='{y}' stroke='{INK}' stroke-width='2'/>"
        b += text(216, y + 5, lab, 13)
        b += text(180, y - 8, f'{n}겹', 11, 'middle', MUT)
    return svg(W, H, b)


def cu_jt():
    """[Cu(H2O)6]2+ d9, z-out: 두 전이(b2g→b1g, eg→b1g)."""
    W, H = 400, 300
    b = text(80, 22, 'Oh', 15, 'middle', weight='bold') + text(260, 22, 'z-out (D4h)', 15, 'middle', weight='bold')
    s1, xe1 = level(50, 80, ['ud', 'u'], ''); b += s1 + text(44, 85, f'e{sub("g")}', 14, 'end')
    s1, xe2 = level(40, 220, ['ud', 'ud', 'ud'], ''); b += s1 + text(34, 225, f't{sub("2g")}', 14, 'end')
    lv = [(f'b{sub("1g")} (x²−y²)', 55, ['u'], xe1, 80), (f'a{sub("1g")} (z²)', 105, ['ud'], xe1, 80),
          (f'b{sub("2g")} (xy)', 195, ['ud'], xe2, 220), (f'e{sub("g")} (xz, yz)', 245, ['ud', 'ud'], xe2, 220)]
    for lab, y, el, px, py in lv:
        s1, _ = level(190, y, el, lab); b += s1 + dash(px + 2, py, 188, y)
    for x, y0, x0, c in [(345, 195, 292, '#c2410c'), (375, 245, 342, '#c2410c')]:
        b += f"<path d='M{x} {y0} L{x} 60 M{x-4} 68 L{x} 60 L{x+4} 68' stroke='{c}' stroke-width='1.5' fill='none'/>"
        b += dash(x0, y0, x, y0) + dash(308, 55, x, 55)
    b += text(345, 213, 'ν₁', 12, 'middle', '#c2410c') + text(375, 263, 'ν₂', 12, 'middle', '#c2410c')
    b += text(200, 292, 'ν₁, ν₂: 가까운 두 d–d 전이 → 어깨(shoulder)', 12, 'middle', '#c2410c')
    return svg(W, H, b)


for name, s in [('d_B07', au4f()), ('d_B09', cu_jt())]:
    open(os.path.join(OUT, name + '.svg'), 'w').write(s)
    print(name)
