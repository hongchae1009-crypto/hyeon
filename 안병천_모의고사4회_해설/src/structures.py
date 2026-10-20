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


# A형 2번: 출발물과 이온 4가지
grid('s_A02', [('C1C=CC=C1', 'A cyclopentadiene (pKa~16)'), ('C1C=CC=CC=C1', 'B cycloheptatriene (pKa~36)'),
               ('[cH-]1cccc1', '(ga) C5H5-  6pi aromatic'), ('[CH+]1C=CC=C1', '(na) C5H5+  4pi antiaromatic'),
               ('[CH-]1C=CC=CC=C1', '(da) C7H7-  8pi antiaromatic'), ('[cH+]1cccccc1', '(ra) C7H7+  6pi aromatic')])
# A형 3번: 오존 분해 → 에스터화 → Claisen 축합. A의 원자 1(CH2, 2.5 ppm) 강조
grid('s_A03', [('CCC(=O)O', 'propanoic acid (x2)'), ('CCC(=O)OC', 'methyl propanoate'),
               ('CCC(=O)C(C)C(=O)OC', 'A  C7H12O3 (red dot = 2.5 ppm CH2)')],
     highlight={2: [1]})
# A형 8번
grid('s_A08', [('CC#CC(=O)c1ccccc1', 'A  1-phenylbut-2-yn-1-one'),
               ('CC1=C(C(=O)c2ccccc2)CC(C)=C(C)C1', 'Diels-Alder adduct'),
               ('CC1=C(C(=O)c2ccccc2)C[C@]2(C)O[C@]2(C)C1', 'B  (racemic, cis-epoxide)')])
# B형 8번: cis 고리에서 오존 분해 → meso 이산
grid('s_B08', [('O=C1OC(=O)[C@@H]2CC=CC[C@H]12', 'A (cis)'),
               ('COC[C@@H]1CC=CC[C@@H]1COC', 'B  C10H18O2 (cis, meso)'),
               ('OC(=O)C[C@@H](COC)[C@@H](COC)CC(=O)O', 'C  meso (3R,4S)')])
# B형 9번 합성 경로
grid('s_B09', [('Cc1ccccc1N', 'A'), ('Cc1ccccc1NC(C)=O', '(c) Ac2O, pyridine'),
               ('Cc1cc(Br)ccc1NC(C)=O', '(d-1) Br2'), ('Cc1cc(Br)ccc1N', '(d-2) NaOH, hydrolysis'),
               ('Cc1cc(Br)ccc1[N+]#N', '(a) NaNO2, H2SO4'), ('Cc1cccc(Br)c1', '(e) H3PO2 -> B')])
