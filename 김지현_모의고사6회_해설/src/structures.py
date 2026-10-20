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
grid('s_A03', [('CC1OC(C)OC(C)O1', 'paraldehyde  C6H12O3')], per_row=1, size=(330, 170))
# A형 10번 (산 촉매: 3차 탄소 공격 / 염기: 1차 탄소 공격)
grid('s_A10', [('CCC1(C)CO1', '2-ethyl-2-methyloxirane'), ('CCC(C)([18OH])CO', 'A  (18O on tertiary C)'),
               ('CCC(C)(O)C[18OH]', 'B  (18O on primary C)')], per_row=3, size=(165, 140))
# A형 11번
grid('s_A11', [('[cH-]1cccc1-c1ccccc1', 'conj. base of B (aromatic)'),
               ('CC(=C)c1[cH-]cc(C)c1', 'conj. base of D (aromatic)')])
# B형 1번
grid('s_B01', [('[O-][N+](=O)c1ccc[nH]1', 'C  2-nitropyrrole (major)'), ('[O-][N+](=O)c1cc[nH]c1', 'D  3-nitropyrrole (minor)')])
# B형 11번
grid('s_B11', [('C(=N/Nc1ccccc1)\\c1ccccc1', 'A  phenylhydrazone'), ('C=C/C=C/c1ccccc1', 'B  1-phenyl-1,3-butadiene'),
               ('OC(=O)/C=C/c1ccccc1', 'C  cinnamic acid (C9H8O2)'), ('CCOC(=O)C(=Cc1ccccc1)C(=O)OCC', 'Knoevenagel product')])
