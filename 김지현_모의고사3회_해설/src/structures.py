"""해설지의 유기 구조식 SVG를 RDKit으로 그린다 (분자식·CIP 검산 출력 포함)."""
import os
from rdkit import Chem
from rdkit.Chem import AllChem, rdCIPLabeler
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

OUT = os.path.join(os.path.dirname(__file__), '..', 'img')


def grid(name, items, per_row=2, size=(165, 140), highlight=None):
    """items: (SMILES, 이름표). highlight: {그림 번호: [원자 번호, …]} — 동그라미로 강조할 원자."""
    mols, legends = [], []
    for smi, label in items:
        m = Chem.MolFromSmiles(smi)
        AllChem.Compute2DCoords(m)
        mols.append(m)
        legends.append(label)
        rdCIPLabeler.AssignCIPLabels(m)   # 새 CIP 규칙으로 R/S 판정
        cip = [f'{a.GetIdx()}:{a.GetProp("_CIPCode")}' for a in m.GetAtoms() if a.HasProp('_CIPCode')]
        print(f'{name:8s} {CalcMolFormula(m):14s} {label}  {" ".join(cip)}')
    n = min(per_row, len(mols))
    d = rdMolDraw2D.MolDraw2DSVG(size[0] * n, size[1] * ((len(mols) + n - 1) // n), size[0], size[1])
    o = d.drawOptions()
    o.legendFontSize, o.bondLineWidth, o.legendFraction = 13, 1.6, 0.17
    o.addStereoAnnotation = True
    hl = [highlight.get(i, []) if highlight else [] for i in range(len(mols))]
    d.DrawMolecules(mols, legends=legends, highlightAtoms=hl)
    d.FinishDrawing()
    open(os.path.join(OUT, name + '.svg'), 'w').write(d.GetDrawingText())


grid('s_A03', [('CC(=O)CC(OC)OC', '4,4-dimethoxy-2-butanone (C6H12O3)')], per_row=1, size=(330, 160))
grid('s_A10', [('Nc1c(Br)cc(Br)cc1Br', 'A  2,4,6-tribromoaniline'), ('N#[N+]c1ccccc1', 'B  benzenediazonium'),
               ('CN(C)c1ccc(cc1)/N=N/c1ccccc1', 'C  butter yellow')])
grid('s_A10r', [('CC(=O)Nc1ccccc1', '(a) Ac2O: acetanilide'), ('CC(=O)Nc1ccc(cc1)S(=O)(=O)O', '(b) conc H2SO4: para SO3H'),
                ('CC(=O)Nc1ccc(cc1[N+](=O)[O-])S(=O)(=O)O', '(c) HNO3: ortho NO2'), ('Nc1ccccc1[N+](=O)[O-]', '(d) dil H2SO4, heat; HO-'),
                ('CC(=O)Nc1ccc(cc1)[N+](=O)[O-]', '(e)(f) Ac2O; HNO3/H2SO4'), ('Nc1ccc(cc1)[N+](=O)[O-]', '(g)(h) H3O+; HO-')])
grid('s_A11', [('Cc1cc(C/C=C/C)cc(C)c1O', 'A  (Claisen + Cope, para)'), ('C=CCC1(C)C=CC=C(C)C1=O', 'dienone (Claisen, ortho blocked)'),
               ('O=C1C2(C)C=CC(C1(C)CC=C)C3C2C(=O)OC3=O', 'B  Diels-Alder adduct (endo)')])
grid('s_B01', [('C#CCCCC', 'A  1-hexyne'), ('CCC#CCC', 'B  3-hexyne'), ('C1=CCCCC1', 'C  cyclohexene')], per_row=3, size=(110, 120))
grid('s_B10', [('O=C1CCCCO1', 'B  delta-valerolactone'), ('OCCCCCO', 'A  1,5-pentanediol'),
               ('OCCCCC(=O)O', 'C  5-hydroxypentanoic acid'), ('OCCCCC(O)(c1ccccc1)c1ccccc1', 'D  (C17H20O2)')])
