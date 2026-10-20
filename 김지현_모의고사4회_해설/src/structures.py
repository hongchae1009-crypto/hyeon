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
grid('s_A03', [('CCOC(=O)c1ccc(N)cc1', 'Data 1  ethyl p-aminobenzoate'), ('CCOc1ccc(C(N)=O)cc1', 'Data 2  p-ethoxybenzamide')])
# A형 10번
grid('s_A10', [('CC(C)=CCCl', '1-chloro-3-methyl-2-butene'), ('CC(C)(O)C=C', 'B  (85%, attack at 3-deg C)'),
               ('CC(C)=CCO', 'C  (15%)'), ('C=C(C)C(C)=C', '2,3-dimethyl-1,3-butadiene'),
               ('C=C(C)C(C)(C)Br', 'E  1,2-adduct (kinetic)'), ('CC(C)=C(C)CBr', 'F  1,4-adduct (thermodyn.)')])
# A형 11번
grid('s_A11', [('C1CCC2OC2C1', 'A  cyclohexene oxide (from trans)'), ('O=C1CCCCC1', 'B  cyclohexanone (from cis)'),
               ('CC(C)(C)C1CCC2(CC1)CO2', 'C, D  spiro-epoxide (diastereomers)')])
# B형 1번
grid('s_B01', [('C1CCN(C1)C1=Cc2ccccc2CC1', 'X  enamine'), ('C1CCN(C1)C1=CCc2ccccc2C1CCC(C)=O', 'A  C18H23NO'),
               ('O=C1CCc2ccccc2C1CCC(C)=O', 'B  C14H16O2'), ('O=C1C=C2CCc3ccccc3C2CC1', 'C  C14H14O')])
# B형 10번
grid('s_B10', [('CC1=CCCC2C(C(C)(C)O)CCC2(C)C1', 'A  C15H26O'), ('CC12OC1CCC3C(C(C)(C)O)CCC3(C)C2', 'B  C15H26O2'),
               ('CC12OC1CCC3C(C(C)=C)CCC3(C)C2', 'C  C15H24O'), ('CC12OC1CCC3C(C(C)=O)CCC3(C)C2', 'D  C14H22O2')])
