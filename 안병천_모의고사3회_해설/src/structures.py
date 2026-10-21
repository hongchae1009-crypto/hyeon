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



# A형 2번: A·C (사슬), B·D (5원 고리). 그린 거울상 이성질체도 정답(검토 메모 참고)
grid('s_A02', [('C#C[C@@H](C)CC', 'A (S)-3-methylpent-1-yne'), ('O=CC[C@@H](C)CC', 'C (S)-3-methylpentanal'),
               ('C[C@H]1C=CCC1', 'B (R)-3-methylcyclopentene'), ('C[C@H]1C[C@H](O)CC1', 'D (1R,3R) trans-3-methylcyclopentanol')])
grid('s_A02h', [('CCC(C)CC', 'A + 2H2: 3-methylpentane (achiral)'), ('CC1CCCC1', 'B + H2: methylcyclopentane (achiral)')])
# A형 3번
grid('s_A03', [('COc1ccc(CC(C)=O)cc1', '1-(4-methoxyphenyl)propan-2-one (C10H12O2)')], per_row=1, size=(330, 170))
# A형 8번
grid('s_A08', [('OCCC', 'A 1-propanol'), ('BrCCC', 'B 1-bromopropane'), ('C=CC', 'C propene')], per_row=3, size=(110, 110))
# B형 8번 (R = OMe)
grid('s_B08', [('COC1(C)C=CC(=O)C=C1', 'start (R = OMe)'), ('COC1(C)C=CC(=[OH+])C=C1', 'protonated dienone'),
               ('CO[C+]1C=CC(O)=CC1C', 'B (oxocarbenium, Me shifted)'), ('COc1ccc(O)cc1C', 'product: 4-methoxy-3-methylphenol')])
# B형 9번
grid('s_B09', [('Nc1ccccc1', 'aniline'), ('CC(=O)Nc1ccc(cc1)C(C)(C)C', 'A'),
               ('Nc1ccc(cc1)C(C)(C)C', 'B'), ('Nc1c(Cl)cc(cc1Cl)C(C)(C)C', 'C'),
               ('N#[N+]c1c(Cl)cc(cc1Cl)C(C)(C)C', 'diazonium salt'), ('Brc1c(Cl)cc(cc1Cl)C(C)(C)C', 'D')])
