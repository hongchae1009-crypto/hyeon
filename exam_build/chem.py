"""RDKit 기반 구조식 SVG 생성 + 반응식(scheme) HTML 조립 헬퍼."""
import re
from rdkit import Chem
from rdkit.Chem import AllChem, rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D

rdDepictor.SetPreferCoordGen(True)


def mol_svg(smiles, scale=22, label=None, wedge=True, legend=""):
    """SMILES → 흑백 시험지 스타일 SVG 문자열 (크기는 분자 크기에 비례)."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"bad SMILES: {smiles}")
    rdDepictor.Compute2DCoords(mol)
    conf = mol.GetConformer()
    xs = [conf.GetAtomPosition(i).x for i in range(mol.GetNumAtoms())]
    ys = [conf.GetAtomPosition(i).y for i in range(mol.GetNumAtoms())]
    w = int((max(xs) - min(xs)) * scale + 2.6 * scale)
    h = int((max(ys) - min(ys)) * scale + 2.2 * scale)
    w, h = max(w, 40), max(h, 34)
    d = rdMolDraw2D.MolDraw2DSVG(w, h)
    o = d.drawOptions()
    o.useBWAtomPalette()
    o.clearBackground = False
    o.bondLineWidth = 1.3
    o.fixedBondLength = scale
    o.fixedFontSize = int(scale * 0.62)
    o.fontFile = ""
    o.additionalAtomLabelPadding = 0.08
    o.padding = 0.06
    o.addStereoAnnotation = False
    d.DrawMolecule(Chem.Mol(mol), legend=legend)
    d.FinishDrawing()
    svg = d.GetDrawingText()
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
    svg = svg.replace("<!-- END OF HEADER -->", "")
    svg = re.sub(r"<rect[^>]*style='opacity:1.0;fill:#FFFFFF[^>]*>\s*</rect>", "", svg)
    return svg


def _vislen(s):
    t = re.sub(r"<[^>]+>", "", s)
    return sum(1.9 if ord(ch) > 0x2E80 else 1 for ch in t)


def arrow(top="", bottom="", width=None):
    """시약을 위/아래에 적은 반응 화살표 (HTML). width 생략 시 시약 길이에 맞춤."""
    if width is None:
        width = int(max(44, 5.4 * max(_vislen(top), _vislen(bottom)) + 12))
    return (
        f'<div class="arr" style="width:{width}px"><div class="rt">{top}</div>'
        f'<svg width="{width}" height="10" viewBox="0 0 {width} 10"><line x1="2" y1="5" x2="{width-4}" y2="5" stroke="#000" stroke-width="1.1"/>'
        f'<path d="M{width-10},1 L{width-2},5 L{width-10},9 z" fill="#000"/></svg>'
        f'<div class="rb">{bottom}</div></div>'
    )


def box(content, label=""):
    lab = f'<div class="lbl">{label}</div>' if label else ""
    return f'<div class="cmpd">{content}{lab}</div>'


def M(smiles, label="", scale=22):
    return box(mol_svg(smiles, scale=scale), label)


def L(text):
    """구조 대신 굵은 문자 (A, B, ? 등)."""
    return f'<div class="cmpd letter">{text}</div>'


def scheme(*parts, cls=""):
    return f'<div class="scheme {cls}">' + "".join(parts) + "</div>"


def plus():
    return '<div class="plus">+</div>'


def varrow(left="", right="", height=46):
    """아래로 향하는 화살표, 시약은 오른쪽(또는 왼쪽)에."""
    return (f'<div class="varr"><div class="vl">{left}</div><svg width="10" height="{height}" viewBox="0 0 10 {height}">'
            f'<line x1="5" y1="1" x2="5" y2="{height-6}" stroke="#000" stroke-width="1.1"/>'
            f'<path d="M1,{height-10} L5,{height-1} L9,{height-10} z" fill="#000"/></svg><div class="vr">{right}</div></div>')


def rows(*rs):
    """여러 줄 반응식: rows(scheme(...), scheme(...))"""
    return '<div class="rows">' + "".join(rs) + '</div>'


def frame(*parts, title=""):
    t = f'<div class="ft">{title}</div>' if title else ""
    return f'<div class="frame">{t}' + "".join(parts) + '</div>'


def _axis(x0, x1, W, pad, y, ticks, fmt=lambda v: f"{v:g}"):
    s = f'<line x1="{pad}" y1="{y}" x2="{W-pad}" y2="{y}" stroke="#000" stroke-width="0.8"/>'
    for v in ticks:
        x = pad + (x0 - v) / (x0 - x1) * (W - 2 * pad)
        s += (f'<line x1="{x:.1f}" y1="{y}" x2="{x:.1f}" y2="{y+3}" stroke="#000" stroke-width="0.6"/>'
              f'<text x="{x:.1f}" y="{y+11}" font-size="7.5" text-anchor="middle" font-family="Arial">{fmt(v)}</text>')
    return s


def nmr(peaks, title="¹H NMR 스펙트럼", x0=10, x1=0, W=300, H=120, tms=True, unit="화학적 이동(ppm)"):
    """막대형 ¹H/¹³C NMR. peaks = [(δ, 'd'|'s'|..., 상대 적분(높이용), '표시문자'), ...]
    다중선은 J≈7 Hz(300 MHz 기준 0.023 ppm) 간격 막대로 그린다. 표시문자 예: '2', '㉠'."""
    pad = 14; base = H - 22; span = W - 2 * pad
    X = lambda d: pad + (x0 - d) / (x0 - x1) * span
    pas = {'s': [1], 'd': [1, 1], 't': [1, 2, 1], 'q': [1, 3, 3, 1], 'quint': [1, 4, 6, 4, 1],
           'sext': [1, 5, 10, 10, 5, 1], 'sept': [1, 6, 15, 20, 15, 6, 1], 'dd': [1, 1, 1, 1], 'm': [1, 2, 3, 3, 2, 1],
           'br': [1]}
    hmax = max(p[2] for p in peaks) if peaks else 1
    s = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
    s += _axis(x0, x1, W, pad, base, [v for v in range(int(x0), int(x1) - 1, -1 if x0 - x1 <= 12 else -20)])
    s += f'<text x="{W/2}" y="{H-1}" font-size="7.5" text-anchor="middle" font-family="NanumGothic">{unit}</text>'
    s += f'<text x="{pad}" y="9" font-size="8" font-family="NanumGothic">{title}</text>'
    for p in peaks:
        d, m, integ = p[0], p[1], p[2]
        lab = p[3] if len(p) > 3 else ""
        pat = pas.get(m, [1]); tot = max(pat)
        hh = (base - 24) * (0.35 + 0.65 * integ / hmax)
        sp = 0.023 * (x0 - x1) / 10 * 10 / (x0 - x1) * span / 10 * 10  # ~ plot units per line
        sp = 0.023 / (x0 - x1) * span * (2.2 if m != 'br' else 0)
        n = len(pat)
        for i, a in enumerate(pat):
            x = X(d) + (i - (n - 1) / 2) * max(sp, 1.6)
            h = hh * a / tot
            if m == 'br':
                s += f'<path d="M{X(d)-6:.1f},{base} Q{X(d):.1f},{base-2*h:.1f} {X(d)+6:.1f},{base}" fill="none" stroke="#000" stroke-width="0.9"/>'
            else:
                s += f'<line x1="{x:.1f}" y1="{base}" x2="{x:.1f}" y2="{base-h:.1f}" stroke="#000" stroke-width="0.9"/>'
        if lab:
            s += f'<text x="{X(d):.1f}" y="{base-hh-4:.1f}" font-size="8" text-anchor="middle" font-family="NanumGothic">{lab}</text>'
    if tms:
        s += f'<line x1="{X(0):.1f}" y1="{base}" x2="{X(0):.1f}" y2="{base-14}" stroke="#000" stroke-width="0.9"/>'
        s += f'<text x="{X(0):.1f}" y="{base-17}" font-size="6.5" text-anchor="middle" font-family="Arial">TMS</text>'
    return s + '</svg>'


def ir(bands, title="IR 스펙트럼", W=300, H=110, labels=True):
    """IR 투과율 스펙트럼. bands = [(파수, 깊이0~1, 폭cm-1, 'broad'?), ...]  4000→500 cm-1."""
    import math
    pad = 16; top = 14; base = H - 22; span = W - 2 * pad
    X = lambda v: pad + (4000 - v) / 3500 * span
    pts = []
    for i in range(0, 351):
        v = 4000 - i * 10
        t = 0.92
        for b in bands:
            c, dep, w = b[0], b[1], b[2]
            t -= dep * math.exp(-((v - c) / w) ** 2)
        t = max(t, 0.02)
        pts.append(f'{X(v):.1f},{top + (1 - t) * (base - top):.1f}')
    s = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
    s += f'<rect x="{pad}" y="{top}" width="{span}" height="{base-top}" fill="none" stroke="#000" stroke-width="0.7"/>'
    s += _axis(4000, 500, W, pad, base, [4000, 3000, 2000, 1500, 1000, 500])
    s += f'<polyline points="{" ".join(pts)}" fill="none" stroke="#000" stroke-width="0.9"/>'
    s += f'<text x="{pad}" y="9" font-size="8" font-family="NanumGothic">{title}</text>'
    s += f'<text x="{W/2}" y="{H-1}" font-size="7.5" text-anchor="middle" font-family="NanumGothic">파수(cm⁻¹)</text>'
    s += f'<text x="5" y="{(top+base)/2}" font-size="7" font-family="NanumGothic" transform="rotate(-90 5 {(top+base)/2})" text-anchor="middle">투과율(%)</text>'
    if labels:
        for b in bands:
            if len(b) > 3 and b[3]:
                yy = top + (1 - (0.92 - b[1])) * (base - top)
                s += f'<text x="{X(b[0]):.1f}" y="{yy+10:.1f}" font-size="7" text-anchor="middle" font-family="Arial">{b[3]}</text>'
    return s + '</svg>'


def spec(svg):
    return f'<div class="spec">{svg}</div>'
