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
    room = (base - 34) if not neg else (base - 22)
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

# 2 ─ 2025B-1 : 3-phenylpropyl acetate
ITEMS.append(dict(
    key='2025B-1',
    src='2025학년도 B형 1번',
    src_topic='C₈H₈O(styrene oxide)의 ¹H NMR — 적분 비와 dd 갈라짐으로 구조 결정, 특정 피크 수소 표시',
    change='고리 화합물의 부분입체 위치 양성자(dd) 대신, 사슬형 에스터에서 n+1 규칙(t·t·quintet)과 적분 비, '
           'CH₃ 단일선의 위치(아세틸 2.0 vs 메톡시 3.7)로 이성질체(2-phenylethyl propanoate, propyl phenylacetate, methyl 4-phenylbutanoate 등)를 '
           '가려내도록 변형. 분자식 + ¹H NMR + IR 한 줄 정보만으로 유일하게 결정',
    paper=dict(cite='J. Agric. Food Chem. 2003, 51, 4344–4348', book='Klein 12.32',
               what='스리랑카 고유종 계피의 휘발 성분 27종 중 하나인 3-phenylpropyl acetate(톨루엔 → benzyl bromide → 알카인화 → Lindlar → HBr/ROOR → CH₃CO₂⁻ S<sub>N</sub>2)'),
    nobel='',
    body=f'''다음은 계피의 향기 성분 중 하나인 분자식이 C<sub>11</sub>H<sub>14</sub>O<sub>2</sub>인 화합물의 <sup>1</sup>H NMR 스펙트럼이다. 피크의 적분 비 ㉠ : ㉡ : ㉢ : ㉣ : ㉤은 5 : 2 : 2 : 3 : 2이며, 이 화합물의 IR 스펙트럼에는 1740 cm<sup>−1</sup>에 강한 흡수가 있고 3200~3600 cm<sup>−1</sup>에는 흡수가 없다. (단, <sup>1</sup>H NMR 스펙트럼의 여백에 있는 그림은 피크 ㉡~㉤을 확대한 것이다.)
{spec(H1([(7.24, 'm', 5, '㉠'), (4.09, [(6.6, 2)], 2, '㉡'), (2.69, [(7.7, 2)], 2, '㉢'), (2.05, [], 3, '㉣'), (1.96, [(7.1, 4)], 2, '㉤')],
          insets=[[1], [2], [3, 4]]))}
{T([('㉠', '7.32~7.16', 'm', '', '5'), ('㉡', '4.09', 't', '6.6', '2'), ('㉢', '2.69', 't', '7.7', '2'), ('㉣', '2.05', 's', '', '3'), ('㉤', '1.96', 'quintet', '≈7', '2')])}
<p class="ask">이 화합물의 구조를 그리고, 피크 ㉤에 해당하는 수소에 동그라미로 표시하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CC(=O)OCCCc1ccccc1', '3-phenylpropyl acetate', 16)}</div>
㉤(δ 1.96, quintet) = Ph–CH<sub>2</sub>–<u><b>CH<sub>2</sub></b></u>–CH<sub>2</sub>–O의 가운데 CH<sub>2</sub> 수소 2개에 동그라미.''',
    explain='''<p>① 불포화도 = (2×11+2−14)/2 = 5 → 벤젠 고리(4) + C=O(1). IR 1740 cm<sup>−1</sup>(포화 에스터 C=O), O–H 없음 → 에스터. ㉠ 7.3~7.2(5H)는 일치환 벤젠(C<sub>6</sub>H<sub>5</sub>–).</p>
<p>② ㉣ 2.05(s, 3H): 이웃 수소가 없는 CH<sub>3</sub>. 2.0~2.1 ppm은 CH<sub>3</sub>–C(=O)–O(아세틸)의 전형적 위치이다. 만약 에스터의 O–CH<sub>3</sub>였다면 3.6~3.7 ppm에 나타났을 것이다. ⇒ 아세테이트(CH<sub>3</sub>CO<sub>2</sub>–R).</p>
<p>③ 남은 조각 C<sub>3</sub>H<sub>6</sub>: CH<sub>2</sub> 3개. ㉡ 4.09(t, 2H) = O–CH<sub>2</sub>(에스터 산소에 결합, 약 +3 ppm 보정), ㉢ 2.69(t, 2H) = Ph–CH<sub>2</sub>(벤질 위치). 두 삼중선은 각각 이웃 CH<sub>2</sub> 2H와 짝지음 → 가운데에 CH<sub>2</sub>가 있다. ㉤ 1.96: 양쪽 CH<sub>2</sub>의 수소 4개와 짝지음(<i>J</i> ≈ 6.6, 7.7 Hz로 비슷) → n+1 = 5, 오중선(quintet).</p>
<p>④ 따라서 PhCH<sub>2</sub>CH<sub>2</sub>CH<sub>2</sub>OC(=O)CH<sub>3</sub> (3-phenylpropyl acetate). 적분 5:2:2:3:2 = 14H 일치.</p>
<p>⑤ 함정 이성질체(모두 C<sub>11</sub>H<sub>14</sub>O<sub>2</sub>): 2-phenylethyl propanoate는 4.29(t)·2.93(t)·2.31(q)·1.12(t)로 CH<sub>3</sub>가 삼중선이고 단일선이 없다. propyl phenylacetate는 3.60(s, 2H)·4.03(t)·1.62(sext)·0.90(t). methyl 4-phenylbutanoate는 CH<sub>3</sub> 단일선이 3.66(OCH<sub>3</sub>)에 있다. benzyl butanoate는 5.11(s, 2H)이 있다. 모두 자료와 다르다.</p>
<p>⑥ 논문 연계: 계피 휘발 성분인 이 에스터는 allylbenzene에 HBr/ROOR(반 Markovnikov 라디칼 첨가)로 1-bromo-3-phenylpropane을 만든 뒤 CH<sub>3</sub>CO<sub>2</sub><sup>−</sup>의 S<sub>N</sub>2로 얻을 수 있다.</p>''',
))

# 3 ─ 2024A-3 : 1-penten-3-ol
ITEMS.append(dict(
    key='2024A-3',
    src='2024학년도 A형 3번',
    src_topic='C₉H₁₂O₂(4-ethoxybenzyl alcohol): H₂CrO₄ 산화로 카복실산 생성, IR O–H 띠 ㉮에 해당하는 ¹H 피크 찾기',
    change='1차 알코올(→카복실산) 대신 산화하면 케톤이 되는 2차 알릴 알코올을 사용. 화학 반응 단서(1°/2°/3° 구별) + IR(O–H, =C–H, 비닐 면외 굽힘) + '
           '말단 비닐기의 세 가지 ³J/²J(trans 17 > cis 10 > gem ≈ 1.5 Hz) 해석을 결합하여, 특정 수소와 trans 관계인 수소의 피크를 고르게 함',
    paper=dict(cite='J. Agric. Food Chem. 2005, 53, 7204–7211', book='Klein 12.34',
               what='메추리 사료의 휘발 성분 1-penten-3-ol — 아세틸렌화 이온 + propanal → 1-pentyn-3-ol → H₂/Lindlar'),
    nobel='',
    body=f'''어떤 화합물 {A_}(C<sub>5</sub>H<sub>10</sub>O)를 H<sub>2</sub>CrO<sub>4</sub>와 반응시키면 분자식이 C<sub>5</sub>H<sub>8</sub>O인 케톤이 생성된다. 다음은 {A_}의 IR와 <sup>1</sup>H NMR 스펙트럼, 그리고 <sup>1</sup>H NMR 피크 자료이다. (단, <sup>1</sup>H NMR 스펙트럼의 여백에 있는 그림은 피크 ㉠~㉣을 확대한 것이며, <sup>2</sup>J와 <sup>4</sup>J 짝지음은 생략하였다.)
{spec(IRS([(3360, .62, 170, '㉮'), (3085, .15, 20), (2965, .45, 30), (2880, .3, 25), (1645, .18, 12, '1645'), (1460, .3, 18), (1120, .25, 20), (1030, .45, 18), (990, .42, 9), (920, .55, 10, '920')]))}
{spec(H1([(5.87, [(17.2, 1), (10.4, 1), (6.2, 1)], 1, '㉠'), (5.23, [(17.2, 1)], 1, '㉡'), (5.12, [(10.4, 1)], 1, '㉢'),
          (4.03, [(6.4, 3)], 1, '㉣'), (1.80, 'br', 1, '㉤'), (1.56, [(7.0, 4)], 2, '㉥'), (0.93, [(7.4, 2)], 3, '㉦')],
         insets=[[0], [1, 2], [3]]))}
{T([('㉠', '5.87', 'ddd', '17.2, 10.4, 6.2', '1'), ('㉡', '5.23', 'd', '17.2', '1'), ('㉢', '5.12', 'd', '10.4', '1'), ('㉣', '4.03', 'q 모양', '6.4', '1'),
    ('㉤', '1.80', 'br s', '', '1'), ('㉥', '1.56', 'quintet', '≈7', '2'), ('㉦', '0.93', 't', '7.4', '3')])}
<p class="ask">{A_}의 구조를 그리고, 피크 ㉠에 해당하는 수소와 서로 트랜스(<i>trans</i>) 관계에 있는 수소의 피크를 ㉡~㉦에서 찾아 쓰시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('C=CC(O)CC', 'A: pent-1-en-3-ol', 18)}</div>
㉠과 <i>trans</i> 관계인 수소의 피크: <b>㉡</b> (δ 5.23, <sup>3</sup><i>J</i><sub>trans</sub> = 17.2 Hz)''',
    explain='''<p>① 불포화도 = (12−10)/2 = 1. IR ㉮(3360 cm<sup>−1</sup>, 넓고 강함) = 수소 결합한 O–H → 알코올. 3085(=C–H, sp<sup>2</sup>), 1645(약한 C=C), 990·920 cm<sup>−1</sup>(일치환 비닐 RCH=CH<sub>2</sub>의 면외 굽힘) → 말단 알켄. 불포화도 1을 C=C가 차지하므로 C=O나 고리는 없다.</p>
<p>② 화학 단서: H<sub>2</sub>CrO<sub>4</sub>로 산화하여 H가 2개 적은 <b>케톤</b>(C<sub>5</sub>H<sub>8</sub>O)이 생기므로 2차 알코올이다(1차면 카복실산, 3차면 반응하지 않음).</p>
<p>③ 비닐 영역: ㉠ 5.87(ddd, 1H)은 –CH= 수소로 =CH<sub>2</sub>의 두 수소(17.2, 10.4 Hz)와 CH–O의 수소(6.2 Hz)에 의해 갈라진다. ㉡ 5.23(d, 17.2) 과 ㉢ 5.12(d, 10.4)는 말단 =CH<sub>2</sub>의 두 수소이다. ³<i>J</i><sub>trans</sub>(12~18 Hz) > ³<i>J</i><sub>cis</sub>(6~12 Hz)이므로 17.2 Hz로 짝지은 ㉡이 ㉠과 <i>trans</i>, 10.4 Hz인 ㉢이 <i>cis</i>이다(제미널 ²<i>J</i> ≈ 1.5 Hz는 생략).</p>
<p>④ ㉣ 4.03(1H) = CH–OH(카비놀 수소, 산소에 의한 탈가림). 비닐 H(6.2 Hz)와 CH<sub>2</sub>의 2H(≈6.5 Hz)에 거의 같은 <i>J</i>로 짝지어 사중선 모양. ㉤ 1.80(br s) = O–H(빠른 양성자 교환으로 짝지음 없음; D<sub>2</sub>O를 가하면 사라짐) → IR ㉮와 같은 작용기. ㉥ 1.56(2H) = CH<sub>2</sub>(CH 1H + CH<sub>3</sub> 3H → 4개, 오중선 모양), ㉦ 0.93(t, 3H) = CH<sub>3</sub>.</p>
<p>⑤ 따라서 A = CH<sub>2</sub>=CH–CH(OH)–CH<sub>2</sub>CH<sub>3</sub>, 산화 생성물은 pent-1-en-3-one(ethyl vinyl ketone). 함정: 4-penten-2-ol(2차·말단 비닐이지만 CH<sub>3</sub>가 이중선 1.2 ppm), 2-methyl-3-buten-2-ol(3차, 산화 안 됨, 6H 단일선), (<i>E</i>)-2-penten-1-ol(1차 → 카복실산, 내부 알켄), cyclopentanol(비닐 H 없음).</p>
<p>⑥ 논문 연계: 1-pentyn-3-ol(HC≡C<sup>−</sup> + propanal)을 Lindlar 촉매로 부분 수소화하여 말단 알켄을 만든다.</p>''',
))

# 4 ─ 2023A-3 : 1-(4-bromophenyl)ethanol
ITEMS.append(dict(
    key='2023A-3',
    src='2023학년도 A형 3번',
    src_topic='C₉H₉ClO(3-chloropropiophenone)의 IR·¹H NMR·MS — Cl 동위원소(3:1), α-절단 아실륨 이온(m/z 105)',
    change='Cl(3:1) 대신 Br(1:1) 동위원소 쌍을 쓰고, 케톤의 아실륨 대신 알코올의 α-절단으로 생기는 산소 안정화 양이온(옥소늄)을 묻는다. '
           '위치 이성질체 2-(4-bromophenyl)ethanol(α-절단 시 •CH₂OH 손실 → m/z 169/171)과의 구별이 MS 단서의 핵심',
    paper=dict(cite='J. Chem. Ed. 2008, 85, 832–833', book='Klein 15.71',
               what='1-(4-bromophenyl)ethanol과 2-(4-bromophenyl)ethanol의 EI 질량 스펙트럼(m/z 202/200, 187/185, 159/157, 121 대 171/169) 구별'),
    nobel='',
    body=f'''다음은 어떤 화합물 {A_}(C<sub>8</sub>H<sub>9</sub>BrO)의 IR, <sup>1</sup>H NMR, 질량 스펙트럼이다. (단, <sup>1</sup>H NMR 스펙트럼의 여백에 있는 그림은 각각의 피크를 확대한 것이며, 질량 스펙트럼에서 m/z 200 이상의 피크는 분자 이온 피크이다.)
{spec(IRS([(3350, .6, 160, '3350'), (2975, .35, 30), (2925, .2, 20), (1592, .2, 10), (1488, .55, 10, '1488'), (1405, .2, 10), (1370, .2, 10), (1205, .25, 15), (1090, .45, 12), (1010, .55, 10), (825, .6, 12, '825')]))}
{spec(H1([(7.46, [(8.4, 1)], 2, ''), (7.24, [(8.4, 1)], 2, ''), (4.86, [(6.5, 3)], 1, ''), (1.90, 'br', 1, ''), (1.46, [(6.5, 1)], 3, '')],
          insets=[[0, 1], [2], [4]]))}
{spec(MS([(43, 28), (50, 10), (51, 12), (77, 42, '77'), (78, 30), (121, 24, '121'), (157, 26), (159, 25, '157, 159'), (185, 100), (187, 97, '185, 187'),
          (200, 22), (202, 21, '200, 202')], x0=20, x1=220))}
<p class="ask">{A_}의 구조를 그리고, 질량 스펙트럼에서 m/z가 185인 피크에 해당하는 조각 이온(fragment ion)의 구조를 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CC(O)c1ccc(Br)cc1', 'A: 1-(4-bromophenyl)ethan-1-ol', 15)}{M('[OH+]=Cc1ccc([79Br])cc1', 'm/z 185 (⁷⁹Br)', 15)}</div>
m/z 185 = [M − CH<sub>3</sub>]<sup>+</sup> = 4-<sup>79</sup>BrC<sub>6</sub>H<sub>4</sub>–CH=O<sup>+</sup>H (⁸¹Br이면 m/z 187)''',
    explain='''<p>① MS: m/z 200과 202가 거의 1:1 → Br 원자 1개(⁷⁹Br : ⁸¹Br ≈ 51 : 49). M = 200(C<sub>8</sub>H<sub>9</sub><sup>79</sup>BrO). 불포화도 = (2×8+2−9−1)/2 = 4 → 벤젠 고리.</p>
<p>② IR 3350 cm<sup>−1</sup>(넓음) = O–H, C=O 띠 없음 → 알코올. 825 cm<sup>−1</sup>은 <i>para</i>-이치환 벤젠의 C–H 면외 굽힘. ¹H NMR 7.46(d, 2H)·7.24(d, 2H), <i>J</i> = 8.4 Hz의 AA′BB′ 두 이중선 → <i>para</i>-이치환(Br과 탄소 곁사슬).</p>
<p>③ 곁사슬 C<sub>2</sub>H<sub>5</sub>O: 4.86(q, <i>J</i> = 6.5, 1H) = Ar–CH(OH)–(벤질 + 산소, 이웃 CH<sub>3</sub> → 사중선), 1.46(d, 3H) = CH–CH<sub>3</sub>, 1.90(br s, 1H) = OH. ⇒ A = 4-BrC<sub>6</sub>H<sub>4</sub>CH(OH)CH<sub>3</sub>.</p>
<p>④ 조각 이온: 알코올 분자 이온(산소의 비공유 전자 하나가 떨어진 라디칼 양이온)은 C–O에 이웃한 C–C 결합이 끊어지는 <b>α-절단</b>을 한다. C<sub>α</sub>–CH<sub>3</sub> 결합이 균일 분해되어 •CH<sub>3</sub>(15)가 떨어지고, 산소의 전자쌍이 C=O<sup>+</sup> π 결합을 만들어 공명 안정화된 옥소늄 이온 ArCH=OH<sup>+</sup>(m/z 185/187, 기준 피크)이 된다. 이 이온은 벤젠 고리와도 콘쥬게이션되어 특히 안정하다.</p>
<p>⑤ 나머지: 157/159 = 185/187 − CO(28) → C<sub>6</sub>H<sub>6</sub>Br<sup>+</sup>(1-phenylethanol의 107 → 79와 같은 경로), 121 = [M − Br]<sup>+</sup>(C<sub>8</sub>H<sub>9</sub>O<sup>+</sup>, Br 없음 → 단일 피크), 77 = C<sub>6</sub>H<sub>5</sub><sup>+</sup>.</p>
<p>⑥ 함정: 위치 이성질체 2-(4-bromophenyl)ethanol은 α-절단으로 •CH<sub>2</sub>OH(31)를 잃어 m/z 169/171(브로모벤질/트로필륨 이온)이 크게 나타나고 m/z 185/187은 거의 없다. ¹H NMR에서도 3.84(t)·2.82(t) 두 삼중선을 보인다. 4-bromobenzyl methyl ether는 O–H 띠가 없고 4.40(s)·3.38(s) 두 단일선을 보인다.</p>''',
))

# 5 ─ 2022A-3 : Dieckmann 생성물의 케토–엔올 IR
ITEMS.append(dict(
    key='2022A-3',
    src='2022학년도 A형 3번 유형',
    src_topic='C₅H₈O₂(vinyl propanoate)의 IR(1760, 비닐 에스터)·¹H NMR — C=O 진동수에 영향을 주는 요인과 알켄 J',
    change='“구조에 따라 C=O 신축 진동수가 달라지는 이유”라는 평가 요소를 유지하면서, Dieckmann 축합 생성물(β-케토 에스터)의 '
           '케토–엔올 호변 이성 평형을 IR 4개 띠(1740·1718·1658·1618)로 해석하도록 변형. 콘쥬게이션과 분자 내 수소 결합에 의한 진동수 감소, '
           '킬레이트 O–H의 ¹H 신호(δ 12.2)를 함께 다룸. 기출의 단순 구조 결정을 반응 생성물 + 호변 이성질체 판단으로 확장',
    paper=dict(cite='J. Am. Chem. Soc. 1952, 74, 4070–4073', book='Klein 15.70',
               what='ethyl 2-oxocyclohexanecarboxylate의 케토형·엔올형 평형 혼합물 IR(1600~1850 cm⁻¹의 1620, 1660, 1720, 1740 cm⁻¹) 귀속'),
    nobel='',
    body=f'''다음은 diethyl heptanedioate로부터 주생성물 {A_}(C<sub>9</sub>H<sub>14</sub>O<sub>3</sub>)를 합성하는 반응과, {A_}의 CCl<sub>4</sub> 용액에서 얻은 IR 스펙트럼의 1550~1850 cm<sup>−1</sup> 영역을 나타낸 것이다. (단, 반응 후 적절한 분리·정제 과정을 수행하였다.)
{frame(scheme(M('CCOC(=O)CCCCCC(=O)OCC', scale=13), arrow('1) NaOEt, EtOH', '2) H<sub>3</sub>O<sup>+</sup>'), L('A')))}
{spec(IRS([(1742, .42, 9, '㉠'), (1717, .48, 9, '㉡'), (1657, .74, 11, '㉢'), (1617, .66, 10, '㉣')], title='IR 스펙트럼 (CCl₄)', v0=1850, v1=1550, ticks=(1850, 1800, 1750, 1700, 1650, 1600, 1550), H=100))}
<div class="chem" style="font-size:9pt">◦ 3200~3600 cm<sup>−1</sup>에는 날카로운 O–H 띠가 없고 2500~3200 cm<sup>−1</sup>에 넓고 약한 흡수가 있다.<br>
◦ {A_}의 <sup>1</sup>H NMR(CDCl<sub>3</sub>)에는 δ 12.2에 D<sub>2</sub>O를 가하면 사라지는 날카로운 단일선과 δ 3.37(1H 미만, m)의 피크가 함께 나타난다.</div>
<p class="ask">{A_}의 구조를 그리고, IR 띠 ㉢과 ㉣을 나타내는 {A_}의 호변 이성질체의 구조를 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CCOC(=O)C1CCCCC1=O', 'A: ethyl 2-oxocyclohexane-1-carboxylate', 15)}{M('CCOC(=O)C1=C(O)CCCC1', '엔올형 (㉢ 1657: C=O, ㉣ 1617: C=C)', 15)}</div>
㉢·㉣은 엔올형 ethyl 2-hydroxycyclohex-1-ene-1-carboxylate의 에스터 C=O(㉢)와 C=C(㉣) 신축 띠이다(O–H…O=C 분자 내 수소 결합).''',
    explain='''<p>① 반응: NaOEt가 에스터 α-탄소를 탈양성자화 → 엔올레이트가 같은 분자의 다른 에스터 C=O를 공격(분자 내 Claisen = <b>Dieckmann 축합</b>) → 사면체 중간체에서 EtO<sup>−</sup> 이탈 → 6원 고리 β-케토 에스터. 생성물의 두 카보닐 사이 C–H(pK<sub>a</sub> ≈ 11)가 EtO<sup>−</sup>에 의해 탈양성자화되어 평형이 생성물 쪽으로 끌려가며, H<sub>3</sub>O<sup>+</sup> 처리로 중성 β-케토 에스터 A를 얻는다. C<sub>11</sub>H<sub>20</sub>O<sub>4</sub> − EtOH = C<sub>9</sub>H<sub>14</sub>O<sub>3</sub> ✓.</p>
<p>② IR 귀속(케토형): ㉠ 1742 cm<sup>−1</sup> = 포화 에스터 C=O, ㉡ 1717 cm<sup>−1</sup> = 고리 케톤(사이클로헥산온형) C=O.</p>
<p>③ IR 귀속(엔올형): ㉢ 1657 cm<sup>−1</sup> = 엔올형의 에스터 C=O. C=C와 콘쥬게이션되어 C=O 결합 차수가 낮아지고, 엔올 O–H와 6원 고리 모양의 분자 내 수소 결합(O–H⋯O=C)을 이루어 결합이 더 약해지므로 일반 에스터보다 약 85 cm<sup>−1</sup> 낮다. ㉣ 1617 cm<sup>−1</sup> = 엔올 C=C. 보통 C=C는 약하지만, 여기서는 전자 주개(OH)와 받개(CO<sub>2</sub>Et)가 양 끝에 붙은 밀고–당기는(push–pull) 분극 이중 결합이어서 쌍극자 변화가 커 강하게 나타난다.</p>
<p>④ 보조 단서: 날카로운 자유 O–H(≈3600)가 없고 2500~3200의 넓은 흡수만 있는 것은 강한 분자 내 수소 결합 O–H의 특징이다. δ 12.2(s)는 킬레이트된 엔올 OH, δ 3.37은 케토형의 C1–H(두 C=O 사이 메타인)이며, 이 피크가 1H보다 작게 적분되는 것은 두 호변 이성질체가 함께 존재한다는 뜻이다.</p>
<p>⑤ 단순 케톤은 엔올 함량이 무시할 만하지만 β-케토 에스터는 (i) C=C–C=O 콘쥬게이션, (ii) 6원 킬레이트 수소 결합, (iii) 고리 안 사치환 C=C의 안정성 때문에 엔올형이 상당량 존재한다. 함정: ㉡을 에스터로, ㉢을 케톤으로 귀속하는 것(콘쥬게이션·수소 결합은 진동수를 <i>낮춘다</i>).</p>''',
))

# 6 ─ 2021A-2 : 1,1-dibromopentane
ITEMS.append(dict(
    key='2021A-2',
    src='2021학년도 A형 2번',
    src_topic='할로젠 2개를 포함한 화합물(1,3-dibromobenzene)의 MS(1:2:1)·¹H NMR로 구조 결정',
    change='방향족 대칭 판단 대신 지방족 다이할라이드의 위치 이성질체(1,1-/1,2-/1,5-/2,2-dibromopentane)를 ¹H NMR의 δ·갈라짐으로 구별하고, '
           'Br₂ 동위원소 1:2:1, [M−Br]⁺의 1:1 쌍, 할로젠 비공유 전자쌍에 의한 양이온 안정화(조각 이온 구조)를 함께 묻도록 변형. '
           '이중 E2로 말단 알카인을 주는 반응 단서도 추가',
    paper=dict(cite='J. Agric. Food Chem. 2009, 57, 3818–3830', book='Klein 12.40',
               what='(E)-2-hexenal 합성의 출발 물질 1,1-dibromopentane — 과량의 NaNH₂로 이중 E2 → 1-pentyne(펜타인화 이온)'),
    nobel='',
    body=f'''다음은 할로젠 원자 2개를 포함하는 어떤 화합물 {A_}의 질량 스펙트럼과 <sup>1</sup>H NMR 스펙트럼이다. {A_}를 과량의 NaNH<sub>2</sub>와 반응시킨 후 물로 처리하면 1-pentyne이 생성된다. (단, <sup>1</sup>H NMR 스펙트럼의 여백에 있는 그림은 피크 ㉠과 ㉡을 확대한 것이다.)
{spec(MS([(39, 30), (41, 78, '41'), (43, 22), (55, 35, '55'), (67, 12), (69, 100, '69'), (107, 4), (149, 46), (151, 45, '149, 151'), (228, 6), (230, 12), (232, 6, '228, 230, 232')], x0=20, x1=240))}
{spec(H1([(5.70, [(6.2, 2)], 1, '㉠'), (2.40, [(7.0, 3)], 2, '㉡'), (1.50, [(7.3, 4)], 2, '㉢'), (1.36, [(7.3, 5)], 2, '㉣'), (0.93, [(7.2, 2)], 3, '㉤')],
          insets=[[0], [1]]))}
{T([('㉠', '5.70', 't', '6.2', '1'), ('㉡', '2.40', 'q 모양', '≈7', '2'), ('㉢', '1.50', 'm', '', '2'), ('㉣', '1.36', 'm', '', '2'), ('㉤', '0.93', 't', '7.2', '3')])}
<p class="ask">{A_}의 구조를 그리고, 질량 스펙트럼에서 m/z가 149인 피크에 해당하는 조각 이온의 구조를 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CCCCC(Br)Br', 'A: 1,1-dibromopentane', 17)}{M('CCCCC=[79Br+]', 'm/z 149 (⁷⁹Br)', 17)}</div>
m/z 149 = [M − Br]<sup>+</sup> = CH<sub>3</sub>(CH<sub>2</sub>)<sub>3</sub>CH<sup>+</sup>–<sup>79</sup>Br ⟷ CH<sub>3</sub>(CH<sub>2</sub>)<sub>3</sub>CH=<sup>79</sup>Br<sup>+</sup> (⁸¹Br이면 151)''',
    explain='''<p>① MS: m/z 228·230·232가 약 1:2:1 → Br 2개(⁷⁹Br⁷⁹Br : ⁷⁹Br⁸¹Br : ⁸¹Br⁸¹Br ≈ 1:2:1). M = 228 → 228 − 158(⁷⁹Br<sub>2</sub>) = 70 = C<sub>5</sub>H<sub>10</sub>. 분자식 C<sub>5</sub>H<sub>10</sub>Br<sub>2</sub>, 불포화도 0. m/z 149/151(1:1)은 Br 하나를 잃은 [M − Br]<sup>+</sup>(Br 1개 남음), 69는 여기서 HBr을 더 잃은 C<sub>5</sub>H<sub>9</sub><sup>+</sup>(Br 없음 → 짝 피크 없음).</p>
<p>② ¹H NMR: ㉠ 5.70(t, 1H)은 Br 두 개가 붙은 CHBr<sub>2</sub> 수소이다(전기음성 원자 두 개의 탈가림 누적; 이웃 CH<sub>2</sub> → 삼중선). ㉡ 2.40(2H) = CHBr<sub>2</sub> 옆 CH<sub>2</sub>(CH 1H + CH<sub>2</sub> 2H → 사중선 모양), ㉢ 1.50·㉣ 1.36 = 사슬 CH<sub>2</sub>, ㉤ 0.93(t, 3H) = 말단 CH<sub>3</sub>. 적분 1:2:2:2:3 = 10H.</p>
<p>③ 반응 단서: 제미널(1,1-) 또는 비시널(1,2-) 다이브로마이드는 강염기 NaNH<sub>2</sub>로 E2가 두 번 일어나 알카인이 되고, 말단 알카인은 과량의 NH<sub>2</sub><sup>−</sup>에 의해 알카인화 이온이 되었다가 물 처리로 1-pentyne이 된다. 1-pentyne이 생기려면 Br이 C1(또는 C1·C2)에 있어야 한다.</p>
<p>④ 위치 이성질체 구별: 1,2-dibromopentane은 CHBr(δ ≈ 4.15, m)과 부분입체 위치 CH<sub>2</sub>Br(δ ≈ 3.85, 3.63; 각 dd)를 보여 5.7 ppm 신호가 없다. 1,5-dibromopentane(3.41 t, 4H)이나 2,2-dibromopentane(2.57 s, 3H)은 1-pentyne을 주지도 않는다. ⇒ A = 1,1-dibromopentane.</p>
<p>⑤ 조각 이온: 분자 이온에서 C–Br 결합이 끊어져 Br•가 떨어지면 남은 탄소 양이온은 이웃한 Br의 비공유 전자쌍이 빈 p 오비탈로 주개 작용(공명)하여 안정화된다(브로모늄형 C=Br<sup>+</sup>). 이 이온은 Br 1개를 포함하므로 149/151이 1:1로 나타난다. 함정: 149를 C<sub>5</sub>H<sub>10</sub>Br의 라디칼이나 Br 없는 이온으로 그리는 것.</p>''',
))

# 7 ─ 2020A-3 : 4-(acetoxymethyl)benzonitrile
ITEMS.append(dict(
    key='2020A-3',
    src='2020학년도 A형 3번',
    src_topic='C₁₀H₉NO₂ 방향족 화합물(ethyl 4-cyanobenzoate)의 IR(C≡N, C=O)·¹H·¹³C NMR로 구조 결정',
    change='같은 분자식 C₁₀H₉NO₂의 다른 이성질체(벤질 아세테이트형)를 정답으로 하여, 원 기출 정답(ethyl 4-cyanobenzoate)과 '
           'methyl 4-cyanophenylacetate·4-(cyanomethyl)phenyl acetate 등을 δ<sub>H</sub>·δ<sub>C</sub>로 가려내게 함. '
           '구조에 더해 ¹³C에서 나이트릴 탄소(≈118)와 C–CN ipso 탄소(≈112)를 구별하는 귀속을 요구',
    paper=dict(cite='Tetrahedron Lett. 2010, 51, 6542–6544', book='Klein 21.85',
               what='γ-secretase 저해제 BMS-708163 중간체: 4-(bromomethyl)-3-fluorobenzonitrile + KOAc → 4-(acetoxymethyl)-3-fluorobenzonitrile → NaOMe/MeOH 에스터 교환. 본 문항은 F를 뺀 모델 화합물'),
    nobel='',
    body=f'''다음은 분자식이 C<sub>10</sub>H<sub>9</sub>NO<sub>2</sub>인 방향족 화합물 {B_}의 IR, <sup>1</sup>H NMR(300 MHz), <sup>13</sup>C NMR(75 MHz) 스펙트럼이다. (단, <sup>1</sup>H NMR 스펙트럼의 여백에 있는 그림은 7.3~7.8 ppm 영역의 피크를 확대한 것이며, <sup>13</sup>C NMR에서 용매 피크는 생략하였다.)
{spec(IRS([(3060, .1, 20), (2950, .12, 25), (2229, .5, 12, '2229'), (1741, .85, 14, '1741'), (1612, .25, 10), (1380, .3, 12), (1228, .75, 18, '1228'), (1030, .4, 12), (822, .35, 12)]))}
{spec(H1([(7.65, [(8.3, 1)], 2, ''), (7.45, [(8.3, 1)], 2, ''), (5.15, [], 2, ''), (2.13, [], 3, '')], insets=[[0, 1]]))}
{spec(C13([(170.5, .45, '170.5'), (141.2, .45, '㉠'), (132.3, 1.0, '㉡'), (128.2, .95, '㉢'), (118.6, .4, '㉣'), (112.0, .38, '㉤'), (65.0, .8, '65.0'), (20.8, .75, '20.8')], x0=200, x1=0))}
<p class="ask">{B_}의 구조를 그리고, <sup>13</sup>C NMR 피크 ㉠~㉤ 중 C≡N 탄소에 해당하는 피크를 찾아 쓰시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CC(=O)OCc1ccc(C#N)cc1', 'B: 4-(acetoxymethyl)benzonitrile (4-cyanobenzyl acetate)', 16)}</div>
C≡N 탄소: <b>㉣</b> (δ 118.6) (㉤ 112.0은 CN이 붙은 고리 탄소)''',
    explain='''<p>① 불포화도 = (2×10+2+1−9)/2 = 7 → 벤젠(4) + C≡N(2) + C=O(1). IR 2229 cm<sup>−1</sup>(날카로움) = 방향족 나이트릴 C≡N, 1741 cm<sup>−1</sup> = <b>콘쥬게이션되지 않은</b> 에스터 C=O, 1228 cm<sup>−1</sup> = 아세테이트 C–O. 콘쥬게이션된 벤조에이트 에스터라면 ≈1720 cm<sup>−1</sup>이었을 것이다.</p>
<p>② ¹H NMR: 7.65·7.45(각 d, <i>J</i> = 8.3, 2H) → <i>para</i>-이치환 벤젠. 5.15(s, 2H) = Ar–CH<sub>2</sub>–O–C(=O)(벤질 + 에스터 산소, 이웃 H 없음), 2.13(s, 3H) = CH<sub>3</sub>C(=O)O. ⇒ NC–C<sub>6</sub>H<sub>4</sub>–CH<sub>2</sub>OC(=O)CH<sub>3</sub>.</p>
<p>③ ¹³C NMR: 신호 8개(대칭으로 방향족 탄소 4종). 170.5 = C=O, ㉠ 141.2 = CH<sub>2</sub>가 붙은 고리 C(4차), ㉡ 132.3 = CN 쪽 오쏘 CH, ㉢ 128.2 = CH<sub>2</sub> 쪽 오쏘 CH(두 CH는 세기가 크다), <b>㉣ 118.6 = C≡N</b>(나이트릴 탄소는 115~125), ㉤ 112.0 = CN이 붙은 ipso 탄소(C≡N의 반자기 이방성으로 가려짐; 4차라 약함), 65.0 = OCH<sub>2</sub>, 20.8 = CH<sub>3</sub>.</p>
<p>④ 같은 분자식의 함정: ethyl 4-cyanobenzoate(원 기출 정답)는 4.4(q)·1.4(t)와 C=O 1724를 보인다. methyl 4-cyanophenylacetate는 3.70(s, OCH<sub>3</sub>)·3.68(s, CH<sub>2</sub>)과 δ<sub>C</sub> 52, 41을 보인다. 4-(cyanomethyl)phenyl acetate는 페닐 에스터라 C=O ≈1760, CH<sub>3</sub> 2.30, CH<sub>2</sub>CN 3.75를 보인다. 5.15(s)/65.0과 2.13(s)/20.8의 조합은 벤질 아세테이트에만 맞는다.</p>
<p>⑤ 논문 연계: 벤질 브로마이드에 아세테이트 이온이 S<sub>N</sub>2로 치환하여 이 에스터가 생기고, NaOMe/MeOH의 에스터 교환으로 벤질 알코올을 얻는다. NaOH 수용액으로 바로 가수분해하지 않는 것은 C≡N이 함께 가수분해(아마이드/카복실산)될 수 있기 때문이다.</p>''',
))

# 8 ─ 2019A-6 : flutamide
ITEMS.append(dict(
    key='2019A-6',
    src='2019학년도 A형 6번',
    src_topic='C₉H₉BrO₂(ethyl 3-bromobenzoate)의 IR·¹H NMR — 방향족 갈라짐 양상으로 치환 위치 판정, 특정 피크 수소 표시',
    change='meta-이치환 대신 1,2,4-삼치환 벤젠(오쏘 J ≈ 9, 메타 J ≈ 2 Hz)의 d/d/dd 양상을 해석하게 하고, '
           '전립선암 치료제 flutamide 합성(아마이드화) 반응의 생성물로 출제. 2차 아마이드 IR(N–H 1개 띠), NO₂ 띠, 아이소프로필 septet/doublet를 함께 다룸',
    paper=dict(cite='J. Chem. Ed. 2003, 80, 1439–1443', book='Klein 16.74',
               what='4-nitro-3-(trifluoromethyl)aniline + isobutyryl chloride(피리딘) → flutamide; 아마이드화에 따른 방향족 ¹H 화학적 이동 변화'),
    nobel='',
    body=f'''다음은 4-nitro-3-(trifluoromethyl)aniline으로부터 전립선암 치료제 {B_}(C<sub>11</sub>H<sub>11</sub>F<sub>3</sub>N<sub>2</sub>O<sub>3</sub>)를 합성하는 반응과 {B_}의 IR, <sup>1</sup>H NMR 스펙트럼을 나타낸 것이다. (단, <sup>1</sup>H NMR 스펙트럼의 여백에 있는 그림은 7.8~8.1 ppm 영역과 피크 ㉤을 확대한 것이며, <sup>1</sup>H–<sup>19</sup>F 짝지음은 무시한다.)
{frame(scheme(M('Nc1ccc([N+](=O)[O-])c(C(F)(F)F)c1', scale=14), arrow('(CH<sub>3</sub>)<sub>2</sub>CHCOCl', '피리딘'), L('B')))}
{spec(IRS([(3355, .45, 45, '3355'), (3100, .12, 20), (2975, .2, 25), (1712, .75, 14, '1712'), (1600, .3, 10), (1535, .65, 12), (1345, .6, 12), (1320, .55, 12), (1180, .5, 14), (1140, .6, 14), (900, .25, 10)]))}
{spec(H1([(8.03, [(2.2, 1)], 1, '㉠'), (7.97, [(8.9, 1)], 1, '㉡'), (7.92, [(8.9, 1), (2.2, 1)], 1, '㉢'), (7.65, 'br', 1, '㉣'), (2.61, [(6.9, 6)], 1, '㉤'), (1.29, [(6.9, 1)], 6, '㉥')],
          insets=[[0, 1, 2], [4]], inset_w=110))}
{T([('㉠', '8.03', 'd', '2.2', '1'), ('㉡', '7.97', 'd', '8.9', '1'), ('㉢', '7.92', 'dd', '8.9, 2.2', '1'), ('㉣', '7.65', 'br s', '', '1'), ('㉤', '2.61', 'septet', '6.9', '1'), ('㉥', '1.29', 'd', '6.9', '6')])}
<p class="ask">{B_}의 구조를 그리고, 피크 ㉡에 해당하는 수소에 동그라미로 표시하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CC(C)C(=O)Nc1ccc([N+](=O)[O-])c(C(F)(F)F)c1', 'B: flutamide', 15)}</div>
㉡(δ 7.97, d, <i>J</i> = 8.9 Hz) = NO<sub>2</sub>의 오쏘 위치 고리 수소(C5–H; 아마이드 N 기준 메타)에 동그라미.''',
    explain='''<p>① 반응: 아닐린 N의 비공유 전자쌍이 산 염화물 C=O를 공격 → 사면체 중간체 → Cl<sup>−</sup> 이탈(친핵성 아실 치환), 피리딘이 HCl을 중화. B = <i>N</i>-[4-nitro-3-(trifluoromethyl)phenyl]-2-methylpropanamide(flutamide). C<sub>7</sub>H<sub>5</sub>F<sub>3</sub>N<sub>2</sub>O<sub>2</sub> + C<sub>4</sub>H<sub>7</sub>ClO − HCl ✓.</p>
<p>② IR: 3355 cm<sup>−1</sup> 띠 <b>1개</b> = 2차 아마이드 N–H(출발 물질의 1차 아민 NH<sub>2</sub>는 대칭·비대칭 신축 2개 띠), 1712 = 아마이드 C=O(전자 끄는 고리에 붙어 N의 공명 주개 능력이 약해져 일반 아닐라이드보다 높다), 1535·1345 = NO<sub>2</sub> 비대칭·대칭 신축, 1320~1140 = C–F 신축.</p>
<p>③ 곁사슬: ㉤ 2.61(septet, 1H)과 ㉥ 1.29(d, 6H), 같은 <i>J</i> 6.9 Hz → 아이소프로필 (CH<sub>3</sub>)<sub>2</sub>CH–C(=O). ㉣ 7.65(br s) = N–H.</p>
<p>④ 방향족(1,2,4-삼치환; C1 = NHCOR, C3 = CF<sub>3</sub>, C4 = NO<sub>2</sub>): 남은 H는 C2, C5, C6. 오쏘 짝지음 ≈ 8~9 Hz, 메타 ≈ 2 Hz, 파라 ≈ 0. C2–H는 오쏘 이웃 H가 없고 C6–H와 메타 → <b>d, 2.2 Hz = ㉠</b>. C5–H는 C6–H와 오쏘, C2–H와 파라 → <b>d, 8.9 Hz = ㉡</b>. C6–H는 C5–H(오쏘)·C2–H(메타) → <b>dd = ㉢</b>.</p>
<p>⑤ 출발 아닐린에서는 NH<sub>2</sub>의 강한 공명 주개 효과로 오쏘 H(C2, C6)가 6.98, 6.78 ppm으로 가려지고 NO<sub>2</sub> 오쏘의 C5–H만 7.95 ppm이다. 아마이드화하면 N 비공유 전자쌍이 C=O 쪽으로도 비편재되어 주개 효과가 약해지므로 C2–H, C6–H는 1 ppm 이상 낮은 장으로 이동(+ C=O의 이방성)하지만, N의 메타 위치인 C5–H(㉡)는 거의 변하지 않는다. 함정: 가장 낮은 장 피크 ㉠을 NO<sub>2</sub> 오쏘 H로 고르는 것 — 갈라짐(<i>J</i>)이 결정적 근거이다.</p>''',
))
