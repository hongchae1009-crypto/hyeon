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
    ih = 50 if insets else 0
    H = 150 + ih
    base = H - 22
    ptop = ih + 22
    span = W - 2 * pad
    X = lambda d: pad + (x0 - d) / (x0 - x1) * span
    pxHz = span / ((x0 - x1) * mhz) * exag
    s = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
    s += f'<text x="{pad}" y="9" font-size="8" font-weight="700" {_F}>[{title}]</text>'
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
    s += f'<text x="{pad}" y="9" font-size="8" font-weight="700" {_F}>[{title}]</text>'
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
    pad = 18; top = 14; base = H - 22; span = W - pad - 10
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
    s += f'<text x="{pad}" y="9" font-size="8" font-weight="700" {_F}>[{title}]</text>'
    s += f'<rect x="{pad}" y="{top}" width="{span}" height="{base-top}" fill="none" stroke="#000" stroke-width="0.7"/>'
    for v in ticks:
        x = X(v)
        s += (f'<line x1="{x:.1f}" y1="{base}" x2="{x:.1f}" y2="{base+3}" stroke="#000" stroke-width="0.6"/>'
              f'<text x="{x:.1f}" y="{base+11}" font-size="7.5" text-anchor="middle" {_A}>{v}</text>')
    for t in (0, 50, 100):
        y = Y(t / 100)
        s += f'<text x="{pad-2}" y="{y+2.5:.1f}" font-size="6.5" text-anchor="end" {_A}>{t}</text>'
    s += f'<polyline points="{" ".join(pts)}" fill="none" stroke="#000" stroke-width="0.8"/>'
    s += f'<text x="{pad+span/2}" y="{H-1}" font-size="7.5" text-anchor="middle" {_F}>파수(cm⁻¹)</text>'
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
    s += f'<text x="{pad}" y="9" font-size="8" font-weight="700" {_F}>[{title}]</text>'
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


def T(rows_, head=('피크', 'δ (ppm)', '갈라짐 (<i>J</i>, Hz)', '수소 수')):
    h = ''.join(f'<th>{c}</th>' for c in head)
    b = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows_)
    return f'<table class="data"><tr>{h}</tr>{b}</table>'


def lb(x):
    return f'<b class="lbltxt">{x}</b>'


A_, B_ = lb('A'), lb('B')

# ───────────────────────── 문항 ─────────────────────────
ITEMS = []
