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




# A형 2번: 각 화합물에서 가장 산성인 수소(빨간 원)
grid('s_A02', [('O=C1CCCCC1C(=O)O', 'A  Hc (COOH, pKa~4)'),
               ('c1ccccc1CC(=O)CC(=O)CC', 'B  Hb (1,3-dicarbonyl CH2)'),
               ('CC(=O)C1=CCCCC1', 'C  Hc (gamma-H, vinylogous)')],
     per_row=1, size=(330, 115), highlight={0: [9], 1: [9], 2: [5]})
# A형 3번: butanal (C4H8O)
grid('s_A03', [('CCCC=O', 'butanal (red dot = aldehyde C-H)')], per_row=1, size=(330, 110), highlight={0: [3]})
# A형 8번
grid('s_A08', [('CC(C)C1=CCCCC1', '1-isopropylcyclohexene'),
               ('O[C@H]1CCCC[C@@H]1C(C)C', 'A trans-2-isopropylcyclohexanol (racemic)'),
               ('CC(C)C1CCCC=C1', 'B = C  3-isopropylcyclohexene (racemic)')], per_row=1, size=(330, 125))
# B형 8번
grid('s_B08', [('C#C[C@H](C)CC', 'A 3-methylpent-1-yne (chiral)'), ('C=C[C@H](C)CC', 'B 3-methylpent-1-ene'),
               ('CCC(C)CC', 'C 3-methylpentane (achiral)'), ('C=C[C@H](C)CC', 'D = B (same compound)')])
# B형 9번
grid('s_B09', [('O[C@H]1CCC[C@]2([2H])CCCC[C@@]12[H]', 'A (OH axial, trans to H-8a)'),
               ('CS(=O)(=O)O[C@H]1CCC[C@]2([2H])CCCC[C@@]12[H]', 'B mesylate (retention)'),
               ('[2H]C12CCCCC1=CCCC2', 'C octalin (C1=C8a, Zaitsev)'),
               ('O[C@H]1CCC[C@@]2([2H])CCCC[C@]12[2H]', 'D (OH equatorial, cis to D-8a)')])
