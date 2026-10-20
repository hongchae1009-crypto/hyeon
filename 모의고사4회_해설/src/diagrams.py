"""해설지에 들어가는 손그림 SVG(d⁷ 결정장 전자 배치)를 만든다."""
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

def sub(t):
    return f'<tspan baseline-shift="sub" font-size="11">{t}</tspan>'


def oh_config(ox, t2g, eg, title):
    """정팔면체 d 오비탈 두 준위에 전자를 채운 그림 한 개."""
    b = text(ox + 85, 22, title, 15, 'middle', weight='bold')
    s1, _ = level(ox + 30, 70, eg, f'e{sub("g")}'); b += s1
    s1, _ = level(ox + 13, 160, t2g, f't{sub("2g")}'); b += s1
    b += f"<path d='M{ox+8} 160 L{ox+8} 70' stroke='{MUT}' stroke-width='1' stroke-dasharray='3 3'/>"
    b += text(ox + 4, 120, 'Δ<tspan baseline-shift=\"sub\" font-size=\"11\">o</tspan>', 13, 'end', MUT)
    return b


def d7():
    b = oh_config(30, ['ud', 'ud', 'u'], ['u', 'u'], f'바닥 ⁴T{sub("1g")}: t{sub("2g")}⁵e{sub("g")}²')
    b += oh_config(215, ['u', 'u', 'u'], ['ud', 'ud'], f'⁴A{sub("2g")}: t{sub("2g")}³e{sub("g")}⁴')
    return svg(400, 190, b)


open(os.path.join(OUT, 'd_B06.svg'), 'w').write(d7())
print('d_B06')
