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


# A형 2번: 1-phenylpentane-2,4-dione → 말단(벤질) 알릴화 → 다이올 → 브로모에터화
grid('s_A02', [('O=C(Cc1ccccc1)CC(C)=O', 'start: HB > HA > HC'),
               ('C=CCC(c1ccccc1)C(=O)CC(C)=O', 'allylated dione C14H16O2'),
               ('C=CCC(c1ccccc1)C(O)CC(C)O', 'diol (NaBH4) C14H20O2'),
               ('CC(O)CC1OC(CBr)CC1c1ccccc1', 'A  C14H19BrO2')])
# A형 3번: 트라이클로로페놀 네 가지
grid('s_A03', [('Oc1cc(Cl)c(Cl)cc1Cl', 'A 2,4,5-: s + s'), ('Oc1c(Cl)cc(Cl)cc1Cl', 'B 2,4,6-: one s (2H)'),
               ('Oc1cc(Cl)cc(Cl)c1Cl', 'C 2,3,5-: meta d, J~2 Hz'), ('Oc1ccc(Cl)c(Cl)c1Cl', 'D 2,3,4-: ortho d, J~9 Hz')])
# A형 8번
grid('s_A08', [('CC(C)(C)CCO', 'A 3,3-dimethylbutan-1-ol'), ('CC(C)(C)CC(=O)O', 'B 3,3-dimethylbutanoic acid'),
               ('CC(C)(C)CC(=O)N(C)C', 'C N,N-dimethylamide'), ('CC(C)(C)CCN(C)C', 'D (given)')])
# B형 8번 (고리 입체는 문제의 A 그림을 3차원으로 읽은 값, 곁사슬 CH(OH) 탄소는 NaBH4라 R/S 혼합)
grid('s_B08', [('CC1=C[C@H]2CC[C@@H]1C[C@@H]2CCO', 'A (as drawn)'),
               ('C[C@@H](O)[C@@H]1CC[C@H](CO)[C@@H](CCO)C1', 'B triol C11H22O3'),
               ('C[C@@H](O)[C@@H]1CC[C@@H]2COCC[C@H]2C1', 'C (4aR,6R,8aS), trans-fused'),
               ('C[C@H](O)[C@@H]1CC[C@@H]2COCC[C@H]2C1', 'C side-chain epimer')])
# B형 9번
grid('s_B09', [('[S-]c1ccccc1Br.[Na+]', 'B 2-bromothiophenolate'), ('O=[N+]([O-])c1cc(Cl)ccc1Sc1ccccc1Br', 'C  C12H7BrClNO2S'),
               ('Nc1cc(Cl)ccc1Sc1ccccc1Br', 'D (given)')])
