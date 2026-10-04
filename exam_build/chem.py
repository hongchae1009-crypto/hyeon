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


def arrow(top="", bottom="", width=110):
    """시약을 위/아래에 적은 반응 화살표 (HTML)."""
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
