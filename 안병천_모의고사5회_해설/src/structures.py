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


# A형 2번: 광학 활성 알카인 A → 수소화 B, 오존 분해 C
grid('s_A02', [('CC#C[C@@H](C)CC', 'A (S)-4-methylhex-2-yne'), ('CCC[C@@H](C)CC', 'B 3-methylhexane'),
               ('CC(=O)O', 'acetic acid'), ('OC(=O)[C@@H](C)CC', 'C (S)-2-methylbutanoic acid')])
# A형 3번: A → B, 질량 조각
grid('s_A03', [('OC(C)Cc1ccccc1', 'A 1-phenylpropan-2-ol'), ('CC(=O)Cc1ccccc1', 'B phenylacetone (M=134)'),
               ('[cH+]1cccccc1', 'm/z 91 tropylium C7H7+'), ('CC#[O+]', 'm/z 43 acylium CH3CO+')])
# A형 8번: Diels-Alder (endo, all-cis), 수소붕소화·산화 → B
grid('s_A08a', [('C[C@@H]1C=C[C@H](C)[C@H](C=O)C1', 'A (1R,2S,5S) all-cis'),
                ('C[C@@H]1C=C[C@H](C)C[C@@H]1C=O', 'A (1S,2R,5R) enantiomer')])
grid('s_A08b', [('C=C1C[C@H](C)C=C[C@@H]1C', 'start (3S,6S)'),
               ('OC[C@@H]1C[C@H](C)C=C[C@@H]1C', 'alcohol (all-cis)'),
               ('C[C@@H]1C=C[C@H](C)[C@H](C=O)C1', 'B (1R,2S,5S)')], per_row=3)
# B형 9번
grid('s_B09', [('CC(=O)C1CCCCC1', 'A cyclohexyl methyl ketone'), ('NC(=O)C1CCCCC1', 'B amide'),
               ('N#CC1CCCCC1', 'C nitrile'), ('CC(C)C(=O)C1CCCCC1', 'D isopropyl ketone'),
               ('O=CC1CCCCC1', 'E cyclohexanecarbaldehyde')])
