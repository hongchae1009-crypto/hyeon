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
grid('s_A03', [('COC(=O)C(Br)C(Br)c1ccc([N+](=O)[O-])cc1', 'C10H9NO4Br2  (M+ 365/367/369)')], per_row=1, size=(330, 170))
# A형 10번
grid('s_A10', [('CC(Br)CBr', '1,2-dibromopropane'), ('CC#C', 'propyne'), ('C=CC', 'A  propene'),
               ('ClCC=C', 'allyl chloride (Cl2, 400 C)'), ('OC(CCl)CCl', 'B  1,3-dichloro-2-propanol'),
               ('ClCC1CO1', 'C  epichlorohydrin'), ('OCC(O)CO', 'D  glycerol')])
# A형 11번
grid('s_A11', [('OC(=O)c1ccccc1', 'A  benzoic acid'), ('OCc1ccccc1', 'B  benzyl alcohol'),
               ('C/C(=C\\c1ccccc1)[N+](=O)[O-]', 'C  (Henry + -H2O)'), ('C=C/C=C/c1ccccc1', 'D  (Wittig)')])
# B형 1번
grid('s_B01', [('OC(=O)/C=C/C(=O)O', 'B  fumaric acid (trans)'), ('OC(=O)/C=C\\C(=O)O', 'E  maleic acid (cis)'),
               ('OC(=O)[C@@H](O)[C@H](O)C(=O)O', 'A  (R,R) + (S,S) racemic'), ('OC(=O)[C@@H](Br)[C@@H](Br)C(=O)O', 'C  meso'),
               ('OC(=O)[C@@H](O)[C@@H](O)C(=O)O', 'D  meso'), ('OC(=O)[C@@H](Br)[C@H](Br)C(=O)O', 'F  (R,R) + (S,S) racemic')])
# B형 10번
grid('s_B10', [('O=C(O)CCC(=O)c1ccc(Cl)c(Cl)c1', 'A'), ('O=C1CCC(c2ccc(Cl)c(Cl)c2)O1', 'B  C10H8O2Cl2 (lactone)'),
               ('O=C(O)CCC(c1ccccc1)c1ccc(Cl)c(Cl)c1', 'C  C16H14O2Cl2'), ('O=C1CCC(c2ccc(Cl)c(Cl)c2)c2ccccc21', 'D  C16H12OCl2 (tetralone)')])
