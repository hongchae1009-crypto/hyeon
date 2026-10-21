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



# A형 2번: trans-데칼린(4a-메틸). 3-OH/OTs는 Me와 같은 면 축, 7-OAc는 Me와 반대 면 축, A의 7-Cl은 적도
# (3D 배치·MMFF 최적화로 축/적도와 면을 확인한 SMILES)
grid('s_A02', [('Cl[C@@H]1CC[C@@]2(C)C[C@H](O)CC[C@@H]2C1', 'A  C11H19ClO (Cl equatorial)'),
               ('CC(=O)O[C@H]1CC[C@@]2(C)C[C@H](O)CC[C@@H]2C1', 'B  C13H22O3 (OAc axial)'),
               ('CC(=O)O[C@H]1CC[C@@]2(C)C[C@H](OS(=O)(=O)c3ccc(C)cc3)CC[C@@H]2C1', 'C  (OTs, OAc both axial)')],
     per_row=1, size=(330, 170))
# A형 3번
grid('s_A03', [('COC(=O)C(C)(C)C', 'A  C6H12O2'), ('CC(C)(C)C(=O)O', 'pivalic acid'), ('CO', 'methanol')],
     per_row=3, size=(130, 120))
# A형 8번: exo-cis 다이올 → 산화 절단 / 메틸렌 아세탈
grid('s_A08', [('CC1=CC2CCC1C2', 'A  2-methylnorborn-2-ene'), ('C[C@@]1(O)[C@H]2CC[C@H](C2)[C@@H]1O', 'B  exo-cis diol C8H14O2'),
               ('CC(=O)[C@H]1CC[C@@H](C=O)C1', 'C  cis-1,3 C8H12O2'), ('C[C@@]1(O9)[C@H]2CC[C@H](C2)[C@@H]1OC9', 'D  C9H14O2 (IHD 3)')])
# B형 8번
grid('s_B08', [('CCCc1ccc(cc1)[N+](=O)[O-]', 'A  C9H11NO2'), ('C/C=C/c1ccc(cc1)[N+](=O)[O-]', 'B  (E)-alkene C9H9NO2'),
               ('C[C@H]1[C@H](c2ccc([N+](=O)[O-])cc2)[C@@H]2C=C[C@H]1C2', 'C  Ar endo, Me exo (rac)'),
               ('C[C@H]1[C@H](c2ccc([N+](=O)[O-])cc2)[C@H](C=O)C[C@@H]1C=O', 'D  C14H15NO4 (rac)')])
# B형 9번
grid('s_B09', [('COC(=O)c1ccccc1', 'A  methyl benzoate'), ('CC(=O)c1ccccc1', 'acetophenone')],
     highlight={0: [5, 9]})
