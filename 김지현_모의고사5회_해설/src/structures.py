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


# A형 3번
grid('s_A03', [('CC1(C)CC(=O)c2ccccc21', '3,3-dimethylindan-1-one (C11H12O, M=160)')], per_row=1, size=(330, 170))
# A형 10번
grid('s_A10', [('COCC1C2C=CC1CC2=O', 'A  C9H12O2'), ('COCC1C2C=CC1OC(=O)C2', 'B  lactone C9H12O3'),
               ('COCC1C(O)C=CC1CC(=O)O', 'C  C9H14O4')])
# A형 11번
grid('s_A11', [('CN(C)CCCC=C', 'A  N,N-dimethylpent-4-en-1-amine'), ('C=CCC=C', 'B  penta-1,4-diene (+ NMe3)'),
               ('CC(C)(C)CN', 'C  neopentylamine (Curtius)'), ('NC1Cc2ccccc2C1', 'D  indan-2-amine (Hofmann)')])
# B형 1번
grid('s_B01', [('Cc1ccc(cc1)C(=O)CCC(=O)O', 'A  C11H12O3'), ('Cc1ccc(cc1)CCCC(=O)O', 'B  C11H14O2 (Wolff-Kishner)'),
               ('Cc1ccc(cc1)CCCC(=O)Cl', 'C  C11H13ClO'), ('Cc1ccc2CCCC(=O)c2c1', 'D  7-methyl-1-tetralone C11H12O')])
