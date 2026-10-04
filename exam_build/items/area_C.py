"""영역 C — 분광학적 구조 결정(IR·NMR·MS) 기출변형 13문항 (모두 2점 기입형).

이 파일 안에 시험지용 스펙트럼 그리기 함수(H1·C13·IRS·MS)를 둔다.
chem.py 의 nmr()/ir() 와 같은 흑백 스타일이며, 다중선을 실제 J(Hz)로 계산하고
기출처럼 여백에 확대 그림(inset), 적분 곡선, 질량 스펙트럼 막대그래프를 그린다.
"""
from chem import M, L, arrow, varrow, scheme, rows, frame, nmr, ir, spec, plus
import math

_F = 'font-family="NanumGothic"'
_A = 'font-family="Arial"'


# ───────────────────────── 스펙트럼 그리기 도구 ─────────────────────────
def _binom(n):
    r = [1]
    for _ in range(n):
        r = [a + b for a, b in zip([0] + r, r + [0])]
    return r


def _lines(Js):
    """Js = [(J_Hz, 짝지은 수소 수), ...] → [(Hz 오프셋, 상대세기)] (합 = 1)."""
    if Js == 'm':   # 방향족 다중선 근사
        Js = [(7.6, 2), (1.6, 1), (5.5, 1)]
    ls = [(0.0, 1.0)]
    for J, n in Js:
        b = _binom(n)
        ls = [(o + (i - n / 2) * J, a * c) for o, a in ls for i, c in enumerate(b)]
    tot = sum(a for _, a in ls)
    return [(o, a / tot) for o, a in ls]


def _ticks(lo, hi, maxn=3):
    for st in (0.02, 0.05, 0.1, 0.2, 0.5, 1.0):
        vs = [round(k * st, 3) for k in range(math.ceil(lo / st - 1e-9), math.floor(hi / st + 1e-9) + 1)]
        if len(vs) <= maxn:
            return vs, st
    return [lo, hi], 1


def H1(peaks, title='¹H NMR 스펙트럼(300 MHz, CDCl₃)', mhz=300, x0=10, x1=0, insets=(), W=300,
       integ=True, tms=True, exag=3.0, inset_w=72):
    """peaks = [(δ, Js, 수소수, '표시'), ...]; Js = [(J, n), ...] | [] (단일선) | 'br' | 'm'.
    insets = [[피크 index, ...], ...] → 위 여백에 확대 그림."""
    pad = 14
    ih = 46 if insets else 0
    H = 136 + ih
    base = H - 22
    ptop = ih + 22
    span = W - 2 * pad
    X = lambda d: pad + (x0 - d) / (x0 - x1) * span
    pxHz = span / ((x0 - x1) * mhz) * exag
    s = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
    s += f'<text x="{pad}" y="9" font-size="8" font-weight="700" {_F}>[{_t(title)}]</text>'
    # 눈금
    s += f'<line x1="{pad}" y1="{base}" x2="{W-pad}" y2="{base}" stroke="#000" stroke-width="0.8"/>'
    for v in range(int(x0), int(x1) - 1, -1):
        x = X(v)
        s += (f'<line x1="{x:.1f}" y1="{base}" x2="{x:.1f}" y2="{base+3}" stroke="#000" stroke-width="0.6"/>'
              f'<text x="{x:.1f}" y="{base+11}" font-size="7.5" text-anchor="middle" {_A}>{v}</text>')
    s += f'<text x="{W/2}" y="{H-1}" font-size="7.5" text-anchor="middle" {_F}>δ (ppm)</text>'
    PL = []
    for p in peaks:
        d, Js, n = p[0], p[1], p[2]
        PL.append(None if Js == 'br' else _lines(Js))
    hmax = max((n * max(a for _, a in ls)) if ls else n * 0.12 for (d, Js, n, *_), ls in zip(peaks, PL))
    K = (base - ptop - 12) / hmax
    nmax = max(p[2] for p in peaks)
    for p, ls in zip(peaks, PL):
        d, Js, n = p[0], p[1], p[2]
        lab = p[3] if len(p) > 3 else ''
        xc = X(d)
        if ls is None:  # 넓은 봉우리
            h = max(K * n * 0.12, 6)
            s += f'<path d="M{xc-5:.1f},{base} C{xc-2:.1f},{base} {xc-1.5:.1f},{base-h:.1f} {xc:.1f},{base-h:.1f} C{xc+1.5:.1f},{base-h:.1f} {xc+2:.1f},{base} {xc+5:.1f},{base}" fill="none" stroke="#000" stroke-width="0.8"/>'
            top, hw = h, 5
        else:
            amax = max(a for _, a in ls)
            sc = max(1.0, 9 / (K * n * amax))
            hw = 0
            for o, a in ls:
                x = xc - o * pxHz
                hw = max(hw, abs(o * pxHz))
                h = K * n * a * sc
                s += f'<line x1="{x:.2f}" y1="{base}" x2="{x:.2f}" y2="{base-h:.1f}" stroke="#000" stroke-width="0.7"/>'
            top = K * n * amax * sc
        if integ:
            hi = 26 * n / nmax
            xl, xr = xc - hw - 3, xc + hw + 3
            y0 = base - top / 2 + 4 if top < 40 else base - 30
            y0 = min(y0, base - 4)
            s += (f'<path d="M{xl-3:.1f},{y0:.1f} L{xl:.1f},{y0:.1f} C{xc:.1f},{y0:.1f} {xc:.1f},{y0-hi:.1f} {xr:.1f},{y0-hi:.1f} L{xr+3:.1f},{y0-hi:.1f}" '
                  f'fill="none" stroke="#000" stroke-width="0.5"/>')
        if lab:
            s += f'<text x="{xc:.1f}" y="{base-top-4:.1f}" font-size="8.5" text-anchor="middle" {_F}>{lab}</text>'
    if tms:
        s += f'<line x1="{X(0):.1f}" y1="{base}" x2="{X(0):.1f}" y2="{base-12}" stroke="#000" stroke-width="0.8"/>'
        s += f'<text x="{X(0)-2:.1f}" y="{base-15}" font-size="6.5" text-anchor="middle" {_A}>TMS</text>'
    # 확대 그림
    if insets:
        n_in = len(insets)
        bw = min(inset_w, (span - 6 * (n_in - 1)) / n_in)
        cents = [sum(X(peaks[i][0]) for i in g) / len(g) for g in insets]
        xs = []
        for c in cents:
            x = min(max(c - bw / 2, pad), W - pad - bw)
            if xs and x < xs[-1] + bw + 6:
                x = xs[-1] + bw + 6
            xs.append(x)
        over = xs[-1] + bw - (W - pad)
        if over > 0:
            xs = [x - over for x in xs]
            for k in range(len(xs) - 2, -1, -1):
                if xs[k] > xs[k + 1] - bw - 6:
                    xs[k] = xs[k + 1] - bw - 6
        yt, yb = 14, 14 + ih - 14
        for g, bx in zip(insets, xs):
            ext = max(max(abs(o) for o, _ in PL[i]) / mhz if PL[i] else 0.03 for i in g)
            dmax = max(peaks[i][0] for i in g) + ext
            dmin = min(peaks[i][0] for i in g) - ext
            wpp = (dmax - dmin) * 1.25 + 0.02
            mid = (dmax + dmin) / 2
            lo, hi = mid - wpp / 2, mid + wpp / 2
            Xi = lambda d: bx + 3 + (hi - d) / (hi - lo) * (bw - 6)
            gm = max(peaks[i][2] * max(a for _, a in PL[i]) for i in g if PL[i])
            s += f'<line x1="{bx:.1f}" y1="{yb}" x2="{bx+bw:.1f}" y2="{yb}" stroke="#000" stroke-width="0.6"/>'
            for i in g:
                for o, a in PL[i]:
                    x = Xi(peaks[i][0] - o / mhz)
                    h = (yb - yt - 3) * peaks[i][2] * a / gm
                    s += f'<line x1="{x:.2f}" y1="{yb}" x2="{x:.2f}" y2="{yb-h:.1f}" stroke="#000" stroke-width="0.6"/>'
            tv, st = _ticks(lo + (hi - lo) * 0.08, hi - (hi - lo) * 0.08)
            dec = 2 if st < 0.1 else 1
            for v in tv:
                x = Xi(v)
                s += (f'<line x1="{x:.1f}" y1="{yb}" x2="{x:.1f}" y2="{yb+2}" stroke="#000" stroke-width="0.5"/>'
                      f'<text x="{x:.1f}" y="{yb+9}" font-size="6.3" text-anchor="middle" {_A}>{v:.{dec}f}</text>')
    return s + '</svg>'


def C13(peaks, title='¹³C NMR 스펙트럼(75 MHz, CDCl₃)', x0=220, x1=0, W=300, H=96, step=20, show_dv=False):
    """peaks = [(δ, 높이(음수면 아래로), '표시'), ...]. 가까운 표시는 자동으로 엇갈리게 놓는다."""
    pad = 14
    neg = any(p[1] < 0 for p in peaks)
    base = (H - 22) if not neg else (H - 22) / 2 + 8
    span = W - 2 * pad
    X = lambda d: pad + (x0 - d) / (x0 - x1) * span
    hm = max(abs(p[1]) for p in peaks)
    room = (base - 24) if not neg else (base - 22)
    s = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
    s += f'<text x="{pad}" y="9" font-size="8" font-weight="700" {_F}>[{_t(title)}]</text>'
    ya = H - 22
    s += f'<line x1="{pad}" y1="{ya}" x2="{W-pad}" y2="{ya}" stroke="#000" stroke-width="0.8"/>'
    for v in range(int(x0), int(x1) - 1, -step):
        x = X(v)
        s += (f'<line x1="{x:.1f}" y1="{ya}" x2="{x:.1f}" y2="{ya+3}" stroke="#000" stroke-width="0.6"/>'
              f'<text x="{x:.1f}" y="{ya+11}" font-size="7.5" text-anchor="middle" {_A}>{v}</text>')
    if neg:
        s += f'<line x1="{pad}" y1="{base}" x2="{W-pad}" y2="{base}" stroke="#000" stroke-width="0.4" stroke-dasharray="2,2"/>'
    s += f'<text x="{W/2}" y="{H-1}" font-size="7.5" text-anchor="middle" {_F}>δ (ppm)</text>'
    placed = []
    for p in sorted(peaks, key=lambda q: -q[0]):
        d, h = p[0], p[1]
        lab = p[2] if len(p) > 2 else ''
        x = X(d)
        hh = room * abs(h) / hm
        y2 = base - hh if h > 0 else base + hh
        s += f'<line x1="{x:.1f}" y1="{base}" x2="{x:.1f}" y2="{y2:.1f}" stroke="#000" stroke-width="0.9"/>'
        if lab:
            if h > 0:
                ly = base - hh - 3
                for (px, py) in placed:
                    if abs(px - x) < 11 and abs(py - ly) < 8:
                        ly = py - 9
                placed.append((x, ly))
            else:
                ly = base + hh + 8
            s += f'<text x="{x:.1f}" y="{ly:.1f}" font-size="7.5" text-anchor="middle" {_F}>{lab}</text>'
    return s + '</svg>'


def IRS(bands, title='IR 스펙트럼', W=300, H=112, v0=4000, v1=500, ticks=(4000, 3000, 2000, 1500, 1000, 500)):
    """IR 투과율 스펙트럼. bands = [(파수, 깊이0~1, 폭, '표시'), ...]; 표시는 화살표와 함께 띠 아래에 쓴다."""
    pad = 18; top = 16; base = H - 22; span = W - pad - 10
    X = lambda v: pad + (v0 - v) / (v0 - v1) * span
    def T(v):
        t = 0.93
        for b in bands:
            t -= b[1] * math.exp(-((v - b[0]) / b[2]) ** 2)
        return max(t, 0.02)
    Y = lambda t: top + (1 - t) * (base - top)
    n = 600
    pts = [f'{X(v0 - (v0 - v1) * i / n):.1f},{Y(T(v0 - (v0 - v1) * i / n)):.1f}' for i in range(n + 1)]
    s = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
    s += f'<text x="{pad}" y="9" font-size="8" font-weight="700" {_F}>[{_t(title)}]</text>'
    s += f'<rect x="{pad}" y="{top}" width="{span}" height="{base-top}" fill="none" stroke="#000" stroke-width="0.7"/>'
    for v in ticks:
        x = X(v)
        s += (f'<line x1="{x:.1f}" y1="{base}" x2="{x:.1f}" y2="{base+3}" stroke="#000" stroke-width="0.6"/>'
              f'<text x="{x:.1f}" y="{base+11}" font-size="7.5" text-anchor="middle" {_A}>{v}</text>')
    for t in (0, 50, 100):
        y = Y(t / 100)
        s += f'<text x="{pad-2}" y="{y+2.5:.1f}" font-size="6.5" text-anchor="end" {_A}>{t}</text>'
    s += f'<polyline points="{" ".join(pts)}" fill="none" stroke="#000" stroke-width="0.8"/>'
    s += f'<text x="{pad+span/2}" y="{H-1}" font-size="7.5" text-anchor="middle" {_F}>파수(cm<tspan baseline-shift="super" font-size="5.5">−1</tspan>)</text>'
    s += f'<text x="6" y="{(top+base)/2}" font-size="7" {_F} transform="rotate(-90 6 {(top+base)/2})" text-anchor="middle">투과율(%)</text>'
    for b in bands:
        if len(b) > 3 and b[3]:
            x = X(b[0]); yb = Y(T(b[0]))
            ly = min(yb + 13, base - 2) if yb < base - 20 else yb - 14
            if yb < base - 20:
                s += f'<line x1="{x:.1f}" y1="{ly-7:.1f}" x2="{x:.1f}" y2="{yb+2:.1f}" stroke="#000" stroke-width="0.5"/>'
                s += f'<text x="{x:.1f}" y="{ly+1:.1f}" font-size="7" text-anchor="middle" {_A}>{b[3]}</text>'
            else:
                s += f'<text x="{x+3:.1f}" y="{yb+3:.1f}" font-size="7" text-anchor="start" {_A}>{b[3]}</text>'
    return s + '</svg>'


def MS(peaks, title='질량 스펙트럼', x0=20, x1=220, W=300, H=118, step=20):
    """peaks = [(m/z, 상대세기%, '표시'), ...]"""
    pad = 22; top = 14; base = H - 22; span = W - pad - 10
    X = lambda m: pad + (m - x0) / (x1 - x0) * span
    Y = lambda r: base - r / 100 * (base - top)
    s = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
    s += f'<text x="{pad}" y="9" font-size="8" font-weight="700" {_F}>[{_t(title)}]</text>'
    s += f'<line x1="{pad}" y1="{base}" x2="{pad+span}" y2="{base}" stroke="#000" stroke-width="0.8"/>'
    s += f'<line x1="{pad}" y1="{base}" x2="{pad}" y2="{top}" stroke="#000" stroke-width="0.8"/>'
    for r in (0, 50, 100):
        s += (f'<line x1="{pad-3}" y1="{Y(r):.1f}" x2="{pad}" y2="{Y(r):.1f}" stroke="#000" stroke-width="0.6"/>'
              f'<text x="{pad-4}" y="{Y(r)+2.5:.1f}" font-size="6.5" text-anchor="end" {_A}>{r}</text>')
    v = (x0 // step + 1) * step if x0 % step else x0
    while v <= x1:
        x = X(v)
        s += (f'<line x1="{x:.1f}" y1="{base}" x2="{x:.1f}" y2="{base+3}" stroke="#000" stroke-width="0.6"/>'
              f'<text x="{x:.1f}" y="{base+11}" font-size="7.5" text-anchor="middle" {_A}>{v}</text>')
        v += step
    s += f'<text x="{pad+span/2}" y="{H-1}" font-size="7.5" text-anchor="middle" {_A} font-style="italic">m/z</text>'
    s += f'<text x="6" y="{(top+base)/2}" font-size="7" {_F} transform="rotate(-90 6 {(top+base)/2})" text-anchor="middle">상대 세기(%)</text>'
    for p in peaks:
        m, r = p[0], p[1]
        lab = p[2] if len(p) > 2 else ''
        x = X(m)
        s += f'<line x1="{x:.1f}" y1="{base}" x2="{x:.1f}" y2="{Y(r):.1f}" stroke="#000" stroke-width="1.1"/>'
        if lab:
            s += f'<text x="{x:.1f}" y="{Y(r)-3:.1f}" font-size="7" text-anchor="middle" {_A}>{lab}</text>'
    return s + '</svg>'


def T(rows_, head=('피크', 'δ (ppm)', '갈라짐', '<i>J</i> (Hz)', '수소 수')):
    """가로형 압축 표: rows_ = [(표시, δ, 갈라짐, J, 수소수), ...]"""
    cols = list(zip(*rows_))
    st = 'style="font-size:7.8pt;margin:1mm auto"'
    out = ''
    for h, c in zip(head, cols):
        out += f'<tr><th style="padding:.4mm 1.2mm">{h}</th>' + ''.join(f'<td style="padding:.4mm 1.2mm">{x}</td>' for x in c) + '</tr>'
    return f'<table class="data" {st}>{out}</table>'


def _t(title):
    """SVG 제목: ¹H, ¹³C, CDCl₃ 등 첨자를 tspan으로."""
    title = title.replace('¹H', '<tspan baseline-shift="super" font-size="5.5">1</tspan>H')
    title = title.replace('¹³C', '<tspan baseline-shift="super" font-size="5.5">13</tspan>C')
    title = title.replace('CDCl₃', 'CDCl<tspan baseline-shift="sub" font-size="5.5">3</tspan>')
    title = title.replace('CCl₄', 'CCl<tspan baseline-shift="sub" font-size="5.5">4</tspan>')
    return title


def lb(x):
    return f'<b class="lbltxt">{x}</b>'


A_, B_ = lb('A'), lb('B')

# ───────────────────────── 문항 ─────────────────────────
ITEMS = []

# 1 ─ 2026B-1 : (E)-2-hexenal
ITEMS.append(dict(
    key='2026B-1',
    src='2026학년도 B형 1번',
    src_topic='C₉H₁₀O₃(3,5-dimethoxybenzaldehyde)의 IR·¹H NMR — 알데하이드 C=O·C–H, 대칭과 짝지음 양상으로 구조 결정',
    change='방향족 알데하이드 대신 α,β-불포화 지방족 알데하이드를 써서 ① 콘쥬게이션에 의한 C=O 진동수 감소, ② Fermi 이중선, '
           '③ 알켄 ³J(trans ≈ 16 Hz)로 기하 이성질체 판정, ④ 공명에 의한 β-수소 탈가림을 한 문항에서 묻도록 변형. '
           '요구도 “구조 + 기하 + 특정 피크 수소 표시”로 강화',
    paper=dict(cite='J. Agric. Food Chem. 2009, 57, 3818–3830', book='Klein 12.40',
               what='Cabernet Sauvignon 포도 휘발 성분 (E)-2-hexenal — 1,1-dibromopentane → 펜타인화 이온 + HCHO → 2-hexyn-1-ol → Na/NH₃(l) → (E)-2-hexen-1-ol → 산화'),
    nobel='',
    body=f'''다음은 포도의 향기 성분인 어떤 화합물 {A_}(C<sub>6</sub>H<sub>10</sub>O)의 IR와 <sup>1</sup>H NMR 스펙트럼, 그리고 <sup>1</sup>H NMR 피크 자료를 나타낸 것이다. (단, <sup>1</sup>H NMR 스펙트럼의 여백에 있는 그림은 피크 ㉠~㉢을 확대한 것이며, <sup>4</sup>J 짝지음은 생략하였다.)
{spec(IRS([(2960, .42, 35), (2875, .28, 25), (2815, .22, 18), (2730, .24, 18, '2730'), (1692, .86, 18, '1692'), (1640, .3, 12), (1460, .28, 18), (1380, .15, 12), (1140, .28, 25), (975, .52, 12, '975')]))}
{spec(H1([(9.51, [(7.9, 1)], 1, '㉠'), (6.85, [(15.6, 1), (6.8, 2)], 1, '㉡'), (6.12, [(15.6, 1), (7.9, 1)], 1, '㉢'),
          (2.32, [(7.0, 3)], 2, '㉣'), (1.54, [(7.4, 5)], 2, '㉤'), (0.97, [(7.4, 2)], 3, '㉥')], insets=[[0], [1], [2]]))}
{T([('㉠', '9.51', 'd', '7.9', '1'), ('㉡', '6.85', 'dt', '15.6, 6.8', '1'), ('㉢', '6.12', 'dd', '15.6, 7.9', '1'),
    ('㉣', '2.32', 'q 모양', '7.0', '2'), ('㉤', '1.54', 'sext', '7.4', '2'), ('㉥', '0.97', 't', '7.4', '3')])}
<p class="ask">{A_}의 구조를 기하 이성질 관계가 드러나도록 그리고, 피크 ㉡에 해당하는 수소에 동그라미로 표시하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CCC/C=C/C=O', '(E)-hex-2-enal', 18)}</div>
㉡(δ 6.85)은 C3–H(β-수소, CH<sub>2</sub>와 이웃한 비닐 수소)이다. 즉 CH<sub>3</sub>CH<sub>2</sub>CH<sub>2</sub>–<u>C<b>H</b></u>=CH–CHO의 밑줄 수소에 동그라미.''',
    explain='''<p>① 불포화도 = (2×6+2−10)/2 = 2. IR 1692 cm<sup>−1</sup>의 강한 띠(C=O)와 2815·2730 cm<sup>−1</sup>의 약한 쌍(알데하이드 C–H 신축과 C–H 굽힘 배음의 Fermi 공명)은 알데하이드를 뜻한다. 포화 지방족 알데하이드(≈1730)보다 약 40 cm<sup>−1</sup> 낮으므로 C=O가 C=C와 콘쥬게이션되어 있다(단일 결합성 증가). 1640 cm<sup>−1</sup>은 콘쥬게이션된 C=C, 975 cm<sup>−1</sup>은 <i>trans</i>-이치환 알켄의 =C–H 면외 굽힘이다. ⇒ C=C 1개 + C=O 1개.</p>
<p>② ¹H NMR: ㉠ 9.51(d, 1H) = CHO. 이중선이므로 CHO 탄소 옆에 H가 1개(C2–H)뿐이다. ㉢ 6.12(dd, <i>J</i> = 15.6, 7.9) = C2–H(α): CHO 수소(7.9 Hz)와 C3–H(15.6 Hz)에 의해 갈라진다. ㉡ 6.85(dt, <i>J</i> = 15.6, 6.8) = C3–H(β): C2–H(15.6)와 C4의 CH<sub>2</sub> 2개(6.8)에 의해 이중선의 삼중선. </p>
<p>③ β-수소가 α-수소보다 0.7 ppm이나 낮은 장에 나타나는 이유: 공명 구조 <sup>+</sup>CH–CH=CH–O<sup>−</sup>에서 C3(β)가 부분 양전하를 띠어 탈가림되기 때문이다(α,β-불포화 카보닐의 공통 특징).</p>
<p>④ ³<i>J</i>(H2–H3) = 15.6 Hz는 <i>trans</i>(12~18 Hz) 범위이므로 (<i>E</i>)-이성질체이다. (<i>Z</i>)-2-hexenal이라면 ³<i>J</i> ≈ 11 Hz이고 975 cm<sup>−1</sup> 띠가 없다.</p>
<p>⑤ 나머지: ㉣ 2.32(2H) = 알릴 CH<sub>2</sub>(C4); C3–H와 C5–H<sub>2</sub>에 대한 <i>J</i>가 거의 같아(≈7 Hz) 이웃 수소 3개 → 사중선 모양. ㉤ 1.54(sextet, 2H) = C5 CH<sub>2</sub>(이웃 H 5개 → 6중선). ㉥ 0.97(t, 3H) = CH<sub>3</sub>. 적분 1:1:1:2:2:3 = 10H 일치.</p>
<p>⑥ 함정: 3-hexenal(비콘쥬게이션: C=O ≈1725, CHO는 t, C2–H₂는 δ 3.1 d), 2-methyl-2-pentenal(CHO 단일선, CH<sub>3</sub> 단일선), 케톤 이성질체(9.5 ppm 피크 없음, Fermi 쌍 없음)는 자료와 맞지 않는다. 논문 경로에서 2-hexyn-1-ol의 Na/NH<sub>3</sub>(l) 용해 금속 환원이 <i>anti</i> 첨가로 (<i>E</i>)-알켄을 주므로 J = 15.6 Hz와 일치한다(Lindlar 환원이면 <i>Z</i>).</p>''',
))
