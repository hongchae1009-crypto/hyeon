"""김지현 4회 해설의 손그림 SVG: 구조 투영도, MO 준위도, 반응 에너지 도표, 의자형, 팔면체 이성질체."""
import math, os

OUT = os.path.join(os.path.dirname(__file__), '..', 'img')
INK, ACC, RED, MUT = '#1f2933', '#1d4ed8', '#c0392b', '#6b7280'
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


def save(name, s):
    open(os.path.join(OUT, name + '.svg'), 'w').write(s)
    print(name)


# ---------- A1: Mn2(CO)10 엇갈린 구조 (z축 방향에서 본 그림 + 옆모습) ----------
def mn2co10():
    b = T(W / 2, 16, 'z축 위에서 본 모습 (위 Mn: 검정, 아래 Mn: 파랑)', 11.5, weight='bold')
    cx, cy, r = 95, 105, 62
    for k in range(4):
        a = math.radians(90 * k)
        b += L(cx, cy, cx + r * math.cos(a), cy + r * math.sin(a), INK, 2)
        b += T(cx + (r + 13) * math.cos(a), cy + (r + 13) * math.sin(a) + 4, 'CO', 10.5)
        a2 = math.radians(90 * k + 45)
        b += L(cx, cy, cx + r * math.cos(a2), cy + r * math.sin(a2), ACC, 2, '5 3')
        b += T(cx + (r + 13) * math.cos(a2), cy + (r + 13) * math.sin(a2) + 4, 'CO', 10.5, color=ACC)
    b += f"<circle cx='{cx}' cy='{cy}' r='11' fill='white' stroke='{INK}'/>" + T(cx, cy + 4, 'Mn', 9.5, weight='bold')
    # 옆모습
    x0 = 235
    b += T(x0 + 20, 196, '(옆모습)', 10, color=MUT)
    for y, c in [(75, INK), (135, ACC)]:
        b += f"<circle cx='{x0+20}' cy='{y}' r='10' fill='white' stroke='{c}'/>" + T(x0 + 20, y + 4, 'Mn', 9, color=c)
        b += L(x0 - 20, y, x0 + 10, y, c) + L(x0 + 30, y, x0 + 60, y, c)
        b += T(x0 - 30, y + 4, 'CO', 9.5, color=c) + T(x0 + 72, y + 4, 'CO', 9.5, color=c)
    b += L(x0 + 20, 85, x0 + 20, 125, RED, 2) + T(x0 + 38, 108, 'Mn–Mn', 9.5, color=RED)
    b += L(x0 + 20, 65, x0 + 20, 47) + T(x0 + 20, 44, 'CO(축)', 9.5)
    b += L(x0 + 20, 145, x0 + 20, 163, ACC) + T(x0 + 20, 176, 'CO(축)', 9.5, color=ACC)
    b += T(W / 2, 216, '적도 CO 4개씩이 45° 엇갈림 → S₈ 축, D₄d', 11.5, color=RED)
    return svg(226, b)


# ---------- A8: π 주개 리간드가 Δo를 줄이는 MO 그림 ----------
def pi_donor():
    b = T(W / 2, 16, 'σ만 있을 때 (왼쪽)  vs  π 주개 F⁻ (오른쪽)', 11.5, weight='bold')
    # 왼쪽: σ only
    b += L(30, 60, 90, 60) + T(60, 54, f'e{sub("g")}*', 11)
    b += L(30, 140, 90, 140) + T(60, 158, f't{sub("2g")} (비결합)', 11)
    b += f"<path d='M100 60 L100 140' stroke='{ACC}' stroke-width='1.3'/>" + T(118, 104, 'Δo', 12, color=ACC)
    # 오른쪽
    x = 190
    b += L(x, 60, x + 60, 60) + T(x + 30, 54, f'e{sub("g")}*', 11)
    b += L(x, 105, x + 60, 105, RED, 2) + T(x + 30, 97, f't{sub("2g")}* (위로 밀림)', 10.5, color=RED)
    b += L(x, 140, x + 60, 140, MUT, 1, '4 3') + T(x + 92, 144, '원래 t₂g', 9.5, 'start', MUT)
    b += L(x, 200, x + 60, 200, INK, 2) + T(x + 30, 218, f'리간드 π (채워짐, t{sub("2g")}) → 결합성', 10.5)
    b += f"<path d='M{x+70} 60 L{x+70} 105' stroke='{ACC}' stroke-width='1.3'/>" + T(x + 92, 86, "Δo′", 12, 'start', ACC)
    b += L(x + 30, 194, x + 30, 112, MUT, 1, '3 3')
    b += T(W / 2, 244, '채워진 리간드 π와 섞여 t₂g가 올라감 → Δo′ &lt; Δo', 10.5, color=RED)
    b += T(W / 2, 262, '(π 받개 CO·CN⁻는 빈 π*가 t₂g를 끌어내려 Δo가 커짐)', 10, color=MUT)
    return svg(272, b)


# ---------- A10: HBr + 2,3-dimethyl-1,3-butadiene 반응 에너지 도표 ----------
def energy_diagram():
    b = T(W / 2, 16, '반응 진행 좌표', 11.5, weight='bold')
    b += f"<path d='M28 240 L28 30' stroke='{INK}' stroke-width='1.3'/>" + T(14, 135, 'E', 12)
    b += L(28, 240, 318, 240, INK, 1.3)
    # 다이엔 + HBr
    pts = [(40, 150), (70, 150)]
    b += L(40, 150, 75, 150, INK, 2) + T(57, 166, '다이엔+HBr', 9.5)
    b += f"<path d='M75 150 C95 150 100 60 115 60 C130 60 135 125 150 125' fill='none' stroke='{INK}' stroke-width='1.6'/>"
    b += T(115, 52, 'TS₁', 10)
    b += L(145, 125, 175, 125, INK, 2) + T(160, 141, '알릴 양이온 D', 9.5)
    # 1,2 경로 (낮은 TS, 덜 안정 생성물)
    b += f"<path d='M175 125 C190 125 195 95 210 95 C228 95 238 175 262 175' fill='none' stroke='{ACC}' stroke-width='1.8'/>"
    b += T(210, 88, 'TS(1,2)', 9.5, color=ACC)
    b += L(262, 175, 300, 175, ACC, 2) + T(282, 168, 'E', 11, color=ACC, weight='bold')
    # 1,4 경로 (높은 TS, 더 안정 생성물)
    b += f"<path d='M175 125 C192 125 200 70 218 70 C238 70 245 205 270 205' fill='none' stroke='{RED}' stroke-width='1.8'/>"
    b += T(222, 62, 'TS(1,4)', 9.5, color=RED)
    b += L(270, 205, 308, 205, RED, 2) + T(290, 222, 'F', 11, color=RED, weight='bold')
    b += T(W / 2, 258, 'E: Ea 작음 → 저온에서 빨리 생김(속도론적)', 10.5, color=ACC)
    b += T(W / 2, 274, 'F: 에너지 낮음 → 고온 평형에서 우세(열역학적)', 10.5, color=RED)
    return svg(284, b)


# ---------- 의자형 그리기 ----------
# 꼭짓점: 0 왼쪽 끝, 1 왼쪽 아래, 2 오른쪽 아래, 3 오른쪽 끝, 4 오른쪽 위, 5 왼쪽 위
CHAIR = [(0, 14), (24, 28), (58, 20), (82, 6), (58, -8), (24, 0)]
AX = {0: 1, 1: -1, 2: 1, 3: -1, 4: 1, 5: -1}   # 축 결합 방향(+1 아래, -1 위): 이웃끼리 반대


def chair(ox, oy, subs):
    """subs: {꼭짓점: [(종류 'ax'|'eq', 라벨, 색), ...]}"""
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
                x2, y2 = x + 24 * dx, y - 7 * d
                b += L(x, y, x2, y2, col, 1.7)
                b += T(x2 + 3 * dx, y2 + 4, lab, 10.5, 'end' if dx < 0 else 'start', col, 'bold')
    return b


def block(y, title, subs, notes):
    b = T(W / 2, y, title, 11, weight='bold')
    b += chair(62, y + 42, subs)
    for k, (txt, col) in enumerate(notes):
        b += T(200, y + 32 + 16 * k, txt, 10.5, 'start', col)
    return b


def chairs_a11():
    G = '#15803d'
    b = block(16, '반응 1 (trans): 고리 뒤집은 의자형', {3: [('ax', 'O⁻', RED), ('eq', 'H', INK)], 2: [('ax', 'Cl', G)]},
              [('O⁻·Cl 모두 축', INK), ('서로 180° anti', INK), ('→ SN2 → A', ACC)])
    b += block(140, '반응 2 (cis): O⁻ 적도, Cl 축', {3: [('ax', 'H', RED), ('eq', 'O⁻', RED)], 2: [('ax', 'Cl', G)]},
               [('O⁻ 적도: 뒤로 못 감', INK), ('C1–H·C2–Cl anti', INK), ('→ E2 → 엔올 → B', ACC)])
    b += block(264, 'C (mCPBA): O 적도, CH₂ 축', {0: [('ax', 'CH₂', MUT), ('eq', 'O', RED)], 3: [('eq', 't-Bu', INK)]},
               [('t-Bu 적도 고정', INK), ('큰 과산: 적도 접근', INK), ('→ O 적도', ACC)])
    b += block(388, 'D (Br₂/H₂O → NaH): O 축, CH₂ 적도', {0: [('ax', 'O', RED), ('eq', 'CH₂', MUT)], 3: [('eq', 't-Bu', INK)]},
               [('물: 축 방향 공격', INK), ('OH 축, CH₂Br 적도', INK), ('→ SN2 → O 축', ACC)])
    b += T(W / 2, 500, 'C와 D: 산소 방향이 반대인 부분입체이성질체', 10.5, color=RED)
    return svg(510, b)


# ---------- B7: [Co(trien)X2]+ 이성질체 ----------
POS = {1: (0, -48), 6: (0, 48), 2: (-30, 12), 3: (34, 16), 4: (30, -12), 5: (-34, -16)}
# 1 위, 6 아래, 2 앞-왼쪽, 3 앞-오른쪽, 4 뒤-오른쪽, 5 뒤-왼쪽 (2↔4, 3↔5 trans)


def octa(ox, oy, chain, xs, title, mirror=False):
    m = -1 if mirror else 1
    P = {k: (ox + m * x, oy + y) for k, (x, y) in POS.items()}
    b = T(ox, oy - 64, title, 10.5, weight='bold')
    for k in (2, 3, 4, 5):
        b += L(ox, oy, *P[k], MUT, 1, '3 2' if k in (4, 5) else '')
    b += L(ox, oy, *P[1], MUT, 1) + L(ox, oy, *P[6], MUT, 1)
    # 킬레이트 고리 (인접 N 사이 굽은 선)
    for a, c in zip(chain, chain[1:]):
        (x1, y1), (x2, y2) = P[a], P[c]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        vx, vy = mx - ox, my - oy
        n = math.hypot(vx, vy) or 1
        cx, cy = mx + 14 * vx / n, my + 14 * vy / n
        b += f"<path d='M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}' fill='none' stroke='{ACC}' stroke-width='2'/>"
    for k in chain:
        x, y = P[k]
        b += f"<circle cx='{x:.1f}' cy='{y:.1f}' r='7' fill='white' stroke='{ACC}'/>" + T(x, y + 3.5, 'N', 9, color=ACC, weight='bold')
    for k in xs:
        x, y = P[k]
        b += f"<circle cx='{x:.1f}' cy='{y:.1f}' r='7' fill='white' stroke='{RED}'/>" + T(x, y + 3.5, 'X', 9, color=RED, weight='bold')
    b += f"<circle cx='{ox}' cy='{oy}' r='8' fill='{INK}'/>" + T(ox, oy + 3.5, 'Co', 7.5, color='white')
    return b


def trien_isomers():
    b = ''
    b += octa(165, 80, [2, 3, 4, 5], [1, 6], 'trans (비활성, 1개)')
    b += T(165, 152, 'N 4개가 한 평면, X는 위·아래 → 대칭면 있음', 9.5, color=MUT)
    y = 235
    b += octa(85, y, [1, 2, 3, 6], [4, 5], 'cis-α (Λ)')
    b += octa(245, y, [1, 2, 3, 6], [4, 5], 'cis-α (Δ)', mirror=True)
    b += L(165, y - 50, 165, y + 50, MUT, 1, '4 3') + T(165, y + 64, '거울', 9.5, color=MUT)
    b += T(165, y + 82, '말단 N 두 개가 서로 trans(위·아래)', 9.5, color=MUT)
    y = 395
    b += octa(85, y, [2, 1, 3, 6], [4, 5], 'cis-β (Λ)')
    b += octa(245, y, [2, 1, 3, 6], [4, 5], 'cis-β (Δ)', mirror=True)
    b += L(165, y - 50, 165, y + 50, MUT, 1, '4 3') + T(165, y + 64, '거울', 9.5, color=MUT)
    b += T(165, y + 82, '말단 N 하나가 가운데 N과 trans', 9.5, color=MUT)
    b += T(W / 2, y + 104, '총 5개 = trans 1 + cis-α 1쌍 + cis-β 1쌍', 11, color=RED, weight='bold')
    return svg(y + 114, b)


# ---------- A8: d⁶ 고스핀/저스핀 전자 배치 ----------
def d6():
    def arrows(cx, y, e):
        o = ''
        if 'u' in e:
            x = cx - (5 if 'd' in e else 0)
            o += f"<path d='M{x} {y-3} L{x} {y-19} M{x-4} {y-13} L{x} {y-19} L{x+4} {y-13}' stroke='{ACC}' stroke-width='1.6' fill='none'/>"
        if 'd' in e:
            x = cx + 5
            o += f"<path d='M{x} {y-19} L{x} {y-3} M{x-4} {y-9} L{x} {y-3} L{x+4} {y-9}' stroke='{ACC}' stroke-width='1.6' fill='none'/>"
        return o

    def lev(x, y, es):
        o = ''
        for i, e in enumerate(es):
            x0 = x + i * 30
            o += L(x0, y, x0 + 24, y, INK, 2) + arrows(x0 + 12, y, e)
        return o
    b = T(85, 16, '[CoF₆]³⁻ 고스핀', 11.5, weight='bold') + T(250, 16, '[Co(NH₃)₆]³⁺ 저스핀', 11.5, weight='bold')
    b += lev(55, 60, ['u', 'u']) + T(40, 64, f'e{sub("g")}', 11, 'end')
    b += lev(40, 110, ['ud', 'u', 'u']) + T(32, 114, f't{sub("2g")}', 11, 'end')
    b += lev(220, 45, ['', '']) + T(205, 49, f'e{sub("g")}', 11, 'end')
    b += lev(205, 120, ['ud', 'ud', 'ud']) + T(197, 124, f't{sub("2g")}', 11, 'end')
    b += T(85, 140, '홀전자 4 → 상자성', 10.5, color=RED) + T(250, 146, '홀전자 0 → 반자성', 10.5, color=RED)
    b += T(85, 158, 'CFSE = −0.4Δo', 10.5) + T(250, 164, 'CFSE = −2.4Δo', 10.5)
    return svg(172, b)


save('d_A01', mn2co10())
save('d_A08_d6', d6())
save('d_A08_pi', pi_donor())
save('d_A10_energy', energy_diagram())
save('d_A11_chair', chairs_a11())
save('d_B07', trien_isomers())
