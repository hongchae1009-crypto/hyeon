"""해설지의 유기 구조식 SVG를 RDKit으로 그린다 (분자식 검산 출력 포함)."""
import os
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit.Chem.rdMolDescriptors import CalcMolFormula

OUT = os.path.join(os.path.dirname(__file__), '..', 'img')


def grid(name, items, per_row=None, size=(260, 200)):
    mols, legends = [], []
    for smi, label in items:
        m = Chem.MolFromSmiles(smi)
        AllChem.Compute2DCoords(m)
        mols.append(m)
        legends.append(label)
        print(f'{name:7s} {CalcMolFormula(m):12s} {label}')
    n = per_row or len(mols)
    d = rdMolDraw2D.MolDraw2DSVG(size[0] * n, size[1] * ((len(mols) + n - 1) // n), size[0], size[1])
    o = d.drawOptions()
    o.legendFontSize, o.bondLineWidth, o.legendFraction = 18, 2, 0.16
    d.DrawMolecules(mols, legends=legends)
    d.FinishDrawing()
    open(os.path.join(OUT, name + '.svg'), 'w').write(d.GetDrawingText())


grid('s_A03', [('CCOc1ccc(cc1)C(=O)OCC', 'ethyl p-ethoxybenzoate (C11H14O3, M=194)')], size=(420, 220))
grid('s_A10', [('CC(=O)CC(=O)CC', 'A  (2,4-hexanedione)'), ('C=CC(C)=O', 'B  (MVK, C4H6O)'),
               ('CC(=O)C1CCC(C)=CC1=O', 'C  (C9H12O2)'), ('CC(=O)C1CCC(=O)C=C1C', 'D  (C9H12O2)'),
               ('CC(=O)C(C(C)=O)C1CCCC(=O)C1', 'E  (C11H16O3)')], per_row=5, size=(250, 200))
grid('s_A11', [('CCN=C1CCCCC1', 'A  (imine)'), ('CCN(CC)C1=CCCCC1', 'B  (enamine)'),
               ('CCCNC(CC)CC', 'C  (secondary amine)')])
grid('s_A11m', [('CCCN.CCC(=O)CC', '(1) amine + ketone'), ('CCC[NH2+]C([O-])(CC)CC', '(2) N attacks C=O'),
                ('CCCNC(O)(CC)CC', '(3) carbinolamine'), ('CCC[NH+]=C(CC)CC', '(4) iminium (-H2O)'),
                ('CCCNC(CC)CC', '(5) + H- (NaBH4) = C')], per_row=5, size=(220, 190))
grid('s_B02', [('NCc1ccccc1', 'A  benzylamine'), ('O=Cc1ccccc1', 'B  benzaldehyde'),
               ('c1ccc(cc1)/C=N/Cc1ccccc1', 'C  (C14H13N)'), ('N#CC(O)c1ccccc1', 'D  (C8H7NO)')],
     per_row=4, size=(240, 200))
grid('s_B07a', [('COC1(Cl)C=CC=C[N-]1', 'A-1 (charge on N)'), ('COC1(Cl)[CH-]C=CC=N1', 'A-2 (charge on C3)'),
                ('COC1(Cl)C=C[CH-]C=N1', 'A-3 (charge on C5)'), ('COc1ccccn1', 'B  (C6H7NO)')],
     per_row=4, size=(240, 200))
grid('s_B07b', [('COC1=CCC(C)=CC1', 'C  (C8H12O)'), ('COC(=O)C/C=C(\\C)CC=O', 'D  (C8H12O3)')], size=(320, 210))
grid('s_B07c', [('Cc1ccccc1N', 'F  o-toluidine'), ('Cc1cccc(N)c1', 'F  m-toluidine'),
                ('Cc1ccc(N)cc1', 'F  p-toluidine')], per_row=3, size=(230, 190))
