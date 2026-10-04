"""영역 E(고리화 첨가·자리옮김·방향족성) 6문항 + 영역 F(유기 산·염기) 2문항."""
from chem import M, L, arrow, varrow, scheme, rows, frame, plus

# ---------------------------------------------------------------- 공용 SMILES
TROPOLONE = 'O=C1C=CC=CC=C1O'
TROPONE = 'O=C1C=CC=CC=C1'
CHEPTENONE = 'O=C1C=CCCCC1'
CHEPTANONE = 'O=C1CCCCCC1'
CP = 'C1=CCC=C1'
E64 = 'O=C1C2C=CC=CC1C1CC2C=C1'                      # [6+4] 첨가물 C12H12O

CNT = 'C1=CC=CCC=CCC1'                               # 1,3,6-cyclononatriene C9H12

HEXENYL = 'CC(=O)OCCCCC=C'
DIENE_E = 'CC(=O)OCC/C=C/C=C'
NPM = 'O=C1C=CC(=O)N1c1ccccc1'
DA_ENDO = 'CC(=O)OCC[C@H]1C=CC[C@H]2C(=O)N(c3ccccc3)C(=O)[C@@H]12'   # (3aS,4S,7aR) 및 거울상
DA_EXO = 'CC(=O)OCC[C@H]1C=CC[C@@H]2C(=O)N(c3ccccc3)C(=O)[C@H]12'    # (3aR,4S,7aS) 및 거울상

HDIENE = 'COC(=O)C(=O)/C=C/c1ccccc1'
HDA_A = 'CCOC1CC(c2ccccc2)C=C(C(=O)OC)O1'
HDA_B = 'CCOC1COC(C(=O)OC)=CC1c1ccccc1'
HDA_C = 'COC(=O)C(=O)CC(c1ccccc1)CC=O'

OCTYNE = 'CN1C(=O)c2ccccc2C#Cc2ccccc21'
TRZ_B = 'CN1C(=O)c2ccccc2-c2nnn(Cc3ccccc3)c2-c2ccccc21'
TRZ_C = 'CN1C(=O)c2ccccc2-c2n(Cc3ccccc3)nnc2-c2ccccc21'
TRZ_D = 'c1ccc(Cn2cc(-c3ccccc3)nn2)cc1'

THIOAMIDE = 'CCC(=S)N1CCCC1'
ALLYLBR = 'BrCC=C1CCCCC1'
KETENE_NS = 'C/C=C(\\SCC=C1CCCCC1)N1CCCC1'
THIO_B = 'CC(C(=S)N1CCCC1)C1(C=C)CCCCC1'

LYS_PH1 = '[NH3+][C@@H](CCCCNC(=O)OCC#C)C(=O)O'
LYS_PH7 = '[NH3+][C@@H](CCCCNC(=O)OCC#C)C(=O)[O-]'

B_ = lambda t: f'<b class="lbltxt">{t}</b>'

ITEMS = [
# =====================================================================  E-1  2025B-7
dict(
    key='2025B-7',
    src='2025학년도 B형 7번',
    src_topic='tropone·cyclohept-2-enone·cycloheptanone: 트로폰의 방향족 공명 구조, C=O 신축 파수 비교, 트로폰의 [4+2] 및 '
              'cis-다이엔오필의 Diels–Alder 입체특이성',
    change='트로폰 대신 tropolone(Klein 2.78, 산성과 염기성을 동시에 갖는 칠원 고리)을 넣어 “짝염기의 방향족 공명 구조”를 묻고, '
           'IR 파수 비교를 같은 원리(C⁺–O⁻ 기여)의 다른 관측량인 카보닐 산소의 염기도 비교로 바꾸었다. 고리 첨가는 트로폰이 4π 다이엔으로 '
           '작용하는 [4+2] 대신 6π 성분으로 작용하는 열적 [6+4] 고리 첨가(Woodward–Hoffmann 규칙의 대표 검증례)로 바꾸어 '
           '페리고리 선택 규칙을 π 전자 수·FMO로 직접 서술하게 하였다.',
    paper=dict(cite='J. Org. Chem. 1997, 62, 3200–3207', book='Klein 2.78',
               what='tropolone은 산(→ tropolonate 음이온)이자 염기(→ 1,2-dihydroxytropylium 양이온)로 작용하며, 두 이온 모두 '
                    '방향족 tropylium 성격 때문에 고리 C–C 결합 길이가 균일해진다'),
    nobel='1981 노벨 화학상(K. Fukui·R. Hoffmann — 전선 궤도함수 이론과 궤도함수 대칭 보존 규칙)',
    body=f'''다음은 칠원 고리 화합물 {B_('A')}~{B_('D')}의 [구조]와 [자료], [반응]을 나타낸 것이다.
{frame('<div class="ft">[구조]</div>',
       scheme(M(TROPOLONE, 'A', 13), M(TROPONE, 'B', 13), M(CHEPTENONE, 'C', 13), M(CHEPTANONE, 'D', 13)),
       '<div class="ft">[자료]</div><div class="chem">25 ℃ 수용액에서 pK<sub>a</sub>: '
       f'{B_("A")}(O–H) 6.7, phenol(O–H) 10.0</div>',
       '<div class="ft">[반응]</div>',
       scheme(M(TROPONE, 'B', 13), plus(), M(CP, '', 13), arrow('가열', ''), L('E')),
       '<div class="chem" style="text-align:center">(<b class="lbltxt">E</b>(C<sub>12</sub>H<sub>12</sub>O)는 '
       f'{B_("B")}의 고리 탄소 6개의 π 전자와 cyclopentadiene의 다이엔 4π 전자가 모두 참여한 고리 첨가 생성물)</div>')}
<p class="ask">{B_('A')}가 phenol보다 강한 산인 이유를 설명할 수 있도록, {B_('A')}의 짝염기의 공명 구조 중 칠원 고리가 방향족성을 갖는 구조를 그리시오.
{B_('B')}~{B_('D')}를 카보닐 산소의 염기도(짝산의 pK<sub>a</sub>)가 큰 것부터 순서대로 나열하시오. 또한, {B_('E')}의 구조를 그리고,
이 반응이 가열 조건에서 협동적으로 일어날 수 있는 이유를 참여하는 π 전자 수와 전선 궤도함수(HOMO·LUMO)의 위상에 근거하여 서술하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('[O-]c1ccccc[c+]1[O-]', 'A의 짝염기(방향족 공명 구조)', 15)}{M(E64, 'E', 15)}</div>
· 방향족 공명 구조: 두 산소가 모두 O<sup>−</sup>이고 칠원 고리가 tropylium(6π) 양이온인 구조(전체 전하 −1)<br>
· 염기도: {B_('B')} &gt; {B_('C')} &gt; {B_('D')}<br>
· {B_('E')}: tricyclo[4.4.1.1<sup>2,5</sup>]dodeca-3,7,9-trien-11-one 골격(트로폰 C2·C7이 cyclopentadiene C1·C4와 결합; exo 첨가물)<br>
· 이유: 6π + 4π = 10π(4<i>n</i>+2, <i>n</i> = 2)이므로 두 성분이 모두 같은 면(supra–supra)에서 결합하는 열적 고리 첨가가 대칭 허용이다.
cyclopentadiene의 HOMO(ψ<sub>2</sub>)와 트로폰 6π 부분의 LUMO(ψ<sub>4</sub>*)의 양 말단 위상이 서로 일치하여 두 σ 결합이 동시에 결합성 겹침을 한다.''',
    explain=f'''<p><b>핵심 반응: 방향족성(Hückel 4<i>n</i>+2)과 열적 [6+4] 고리 첨가(Woodward–Hoffmann 선택 규칙).</b></p>
<p>① <b>tropolone의 산성</b>: O–H가 떨어진 tropolonate에서 음전하는 두 산소에 걸쳐 비편재화된다(비닐로그 카복실산: O=C–C=C–OH ⇄ ⁻O–C=C–C=O).
여기에 더해 C=O의 π 전자를 산소로 옮기면 두 산소가 모두 O<sup>−</sup>, 칠원 고리는 6개의 π 전자를 가진 cycloheptatrienyl 양이온(tropylium)이 되는 공명 구조가 가능하다.
평면 단일 고리·연속된 p 오비탈·6π(4<i>n</i>+2, <i>n</i> = 1)를 모두 만족하므로 방향족이며, 이 기여 때문에 짝염기가 특별히 안정하여 pK<sub>a</sub>가 6.7로 phenol(10.0)보다 작다.
Klein 2.78의 근거 자료처럼 tropolonate에서는 고리 C–C 결합 길이가 거의 같아진다(결합 교대 소멸).</p>
<p>② <b>카보닐 산소의 염기도</b>: 산소에 H<sup>+</sup>가 붙은 짝산의 안정성을 비교한다. {B_('B')}의 짝산은 hydroxytropylium 이온(HO–C<sub>7</sub>H<sub>6</sub><sup>+</sup>)으로 양전하가 방향족 6π 고리 전체에 퍼진다 → 짝산 pK<sub>a</sub> ≈ −1로 보통 케톤보다 염기성이 10<sup>5</sup>배 이상 크다.
{B_('C')}의 짝산은 하이드록시알릴 양이온으로 양전하가 C1과 C3에 비편재화되고, {B_('D')}의 짝산은 양전하가 C1(과 O)에만 머무는 국재화된 옥소카베늄(pK<sub>a</sub> ≈ −7)이다.
따라서 염기도 {B_('B')} &gt; {B_('C')} &gt; {B_('D')}. 같은 이유(C<sup>+</sup>–O<sup>−</sup> 기여 증가 → C=O 결합 차수 감소)로 기출의 IR C=O 신축 파수는 정확히 반대 순서({B_('D')} &gt; {B_('C')} &gt; {B_('B')})가 된다.</p>
<p>③ <b>[6+4] 고리 첨가</b>: 분자식 C<sub>12</sub>H<sub>12</sub>O = C<sub>7</sub>H<sub>6</sub>O + C<sub>5</sub>H<sub>6</sub>(단순 1:1 첨가). 단서대로 트로폰의 6π(C2~C7) 말단 C2·C7이 cyclopentadiene의 4π 말단 C1·C4와 각각 새 σ 결합을 만든다.
그 결과 C=O는 1탄소 다리, cyclopentadiene의 CH<sub>2</sub>는 또 하나의 1탄소 다리가 되고, 트로폰 쪽에는 C3=C4·C5=C6 다이엔, cyclopentadiene 쪽에는 C=C 하나가 남는다(sp<sup>3</sup> 탄소 4개).</p>
<p>④ <b>선택 규칙</b>: 열적 고리 첨가는 바닥 상태의 HOMO–LUMO 상호작용으로 일어난다. 다이엔 HOMO ψ<sub>2</sub>는 양 말단의 위상이 반대(마디 1개), 트라이엔 LUMO ψ<sub>4</sub>*도 양 말단 위상이 반대(마디 3개)이므로 두 말단에서 모두 같은 위상끼리 겹친다 → 대칭 허용(supra/supra).
일반화하면 총 π 전자 4<i>n</i>+2(6, 10, …)는 열적 허용, 4<i>n</i>(4, 8)은 열적 금지·광화학 허용이다. [4+2](6π)와 [6+4](10π)는 허용, [2+2]·[4+4]·[6+2](8π)는 열적으로 금지된다.</p>
<p>⑤ (심화) Woodward–Hoffmann은 [6+4]에서는 endo 배향의 이차 궤도 상호작용이 오히려 불리하여 <b>exo</b> 첨가물이 우세할 것이라 예측하였고, 트로폰 + cyclopentadiene 반응에서 실제로 exo [6+4] 첨가물이 주생성물로 확인되었다(Diels–Alder [4+2]의 endo 규칙과 대비).</p>
<p>⑥ 흔한 오답: (i) tropolonate의 방향족 구조에서 고리에 음전하를 두는 것(8π 반방향족이 됨), (ii) 트로폰을 2π 다이엔오필로 보고 cyclopentadiene과 [4+2] 첨가물(노보넨형)을 그리는 것 — 단서의 “트로폰 고리 탄소 6개의 π 전자가 모두 참여”와 모순, (iii) 염기도 순서를 IR 순서와 같게 쓰는 것.</p>''',
),

# =====================================================================  E-2  2022A-2
dict(
    key='2022A-2',
    src='2022학년도 A형 2번',
    src_topic='4가지 methylene cyclopentadiene(풀벤): 짝염기의 방향족성에 근거한 C–H 산도 비교, 6,6-diphenylfulvene의 쌍극성 공명 구조',
    change='풀벤의 “짝염기가 방향족이 되는 C–H” 대신, 탈양성자화로 생긴 음이온이 비편재화는 되지만 고리 콘쥬게이션이 끊겨 방향족이 아닌 '
           'cyclononatrienyl 음이온(Klein 16.73)의 ¹H NMR 자료를 해석하게 하고, 10π 방향족 cyclononatetraenide와 비교하게 하였다. '
           '공명 구조(음전하 위치)와 방향족성 판정 조건(고리형·연속 p 오비탈·4n+2)을 분광 자료로 연결하는 사고를 요구한다.',
    paper=dict(cite='J. Am. Chem. Soc. 1973, 95, 3437–3438', book='Klein 16.73',
               what='1,3,6-cyclononatriene을 KNH₂/액체 NH₃로 탈양성자화한 음이온의 ¹H NMR: 홀수 번째 탄소의 H(δ 3.74, 3.39)는 '
                    '크게 가리움, 짝수 번째 탄소의 H(δ 5.63, 5.52)는 보통 비닐 영역'),
    nobel='',
    body=f'''다음은 1,3,6-cyclononatriene({B_('X')})을 액체 암모니아에서 KNH<sub>2</sub>로 처리하여 음이온 {B_('Y')}(C<sub>9</sub>H<sub>11</sub><sup>−</sup>)를 얻는 반응과 {B_('Y')}의 <sup>1</sup>H NMR 자료이다.
{B_('Y')}의 sp<sup>2</sup> 탄소 7개는 한쪽 끝부터 C1~C7, sp<sup>3</sup> 탄소 2개는 C8, C9로 번호를 붙였다(C7–C8–C9–C1).
{frame(scheme(M(CNT, 'X', 15), arrow('KNH<sub>2</sub>', '액체 NH<sub>3</sub>'), L('Y')),
       '<table class="data"><tr><th>δ (ppm)</th><td>5.63</td><td>5.52</td><td>3.74</td><td>3.39</td></tr>'
       '<tr><th>적분 합</th><td colspan="2">3H</td><td colspan="2">4H</td></tr></table>'
       '<div class="chem" style="text-align:center">(sp<sup>3</sup> CH<sub>2</sub> 신호는 생략함)</div>',
       '<div class="chem">[참고] cyclononatetraenyl 음이온(C<sub>9</sub>H<sub>9</sub><sup>−</sup>, 평면 정구각형)의 <sup>1</sup>H NMR: δ ≈ 7에 단일선 1개</div>')}
<p class="ask">{B_('Y')}에서 δ 3.39와 3.74에 해당하는 수소가 결합한 탄소의 번호를 모두 쓰시오. 또한, C<sub>9</sub>H<sub>9</sub><sup>−</sup>은 방향족이지만 {B_('Y')}는 방향족이 아닌 이유를 π 전자 수를 포함하여 서술하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('[CH-]1C=CC=CC=CCC1', 'C1에 음전하', 14)}{M('C1=C[CH-]C=CC=CCC1', 'C3에 음전하', 14)}</div>
· δ 3.39, 3.74: C1, C3, C5, C7에 결합한 H(음전하가 놓이는 홀수 번째 탄소; C1/C7, C3/C5는 각각 대칭 동등)<br>
· C<sub>9</sub>H<sub>9</sub><sup>−</sup>: 9개 탄소 모두 sp<sup>2</sup>인 평면 고리에서 p 오비탈이 끊김 없이 고리를 따라 이어지고 π 전자가 10개(4<i>n</i>+2, <i>n</i> = 2)이므로 방향족이다.
{B_('Y')}: π 전자는 8개가 7개 탄소(C1~C7)에 비편재화되어 있지만 C8·C9가 sp<sup>3</sup>이어서 고리 콘쥬게이션이 끊긴 사슬형(헵타트라이엔일) 음이온이므로 방향족이 아니다.''',
    explain=f'''<p><b>핵심 반응: 탄소산의 탈양성자화와 짝염기의 공명·방향족성(Hückel 규칙).</b></p>
<p>① <b>탈양성자화 위치</b>: {B_('X')}에서 두 C=C 사이에 끼인 C5–H<sub>2</sub>는 이중 알릴 위치이므로 가장 산성이 크다. KNH<sub>2</sub>(NH<sub>3</sub> pK<sub>a</sub> ≈ 38)가 이 H를 떼면 음전하는 두 C=C로 비편재화되어 C1~C7의 7개 탄소에 걸친 헵타트라이엔일 음이온(8π/7중심)이 된다.</p>
<p>② <b>공명 구조</b>: 음전하를 C1에 둔 구조에서 출발하여 이웃 π 결합 쪽으로 계속 밀면 음전하는 C1 → C3 → C5 → C7로 옮겨 간다. 짝수 번째 탄소(C2, C4, C6)에는 음전하가 놓이는 공명 구조가 없다(홀수 교대 계의 비결합 MO 마디).
따라서 음전하 밀도가 큰 C1, C3, C5, C7의 H는 전자 가리움이 커서 δ 3.4~3.7로 크게 높은 장 이동하고(4H), C2, C4, C6의 H는 보통 비닐 H 영역(δ 5.5~5.6, 3H)에 나타난다. 적분(4H : 3H)이 이 해석과 일치한다.
대칭면(C4와 C8–C9 결합 중점을 지남) 때문에 C1/C7, C3/C5, C2/C6이 각각 동등하여 sp<sup>2</sup> H 신호는 4개(3.74, 3.39, 5.63, 5.52)이다.</p>
<p>③ <b>방향족성 판정</b>: (i) 고리형, (ii) 고리를 이루는 모든 원자에 p 오비탈(연속 콘쥬게이션), (iii) 평면, (iv) π 전자 4<i>n</i>+2개. C<sub>9</sub>H<sub>9</sub><sup>−</sup>(cyclononatetraene의 sp<sup>3</sup> C–H 탈양성자화)은 네 조건을 모두 만족하는 10π 방향족 이온으로, 9개 H가 모두 동등하고 고리 전류의 반가리움 때문에 δ ≈ 7(방향족 영역)에 단일선이 나타난다.
반면 {B_('Y')}는 (ii)를 만족하지 못한다. 만약 음전하가 방향족 고리 전류 때문에 안정화되었다면 모든 H가 δ 6~7 근처에 비슷하게 나타나야 하지만, 실제로는 “음전하가 놓이는 자리/놓이지 않는 자리”로 뚜렷이 나뉘어 국부적 공명만 존재함을 보여 준다.</p>
<p>④ 기출(풀벤)과의 연결: 6,6-dimethylfulvene의 메틸 C–H는 짝염기가 방향족 사이클로펜타다이엔일 음이온(6π)이 되어 특별히 산성이 크다. 산도 비교에서는 “짝염기가 방향족(4<i>n</i>+2)인가, 단순 비편재화인가, 반방향족(4<i>n</i>)인가”를 순서대로 판단한다.</p>
<p>⑤ 흔한 오답: (i) 8π이므로 “반방향족”이라고 쓰는 것 — 반방향족은 고리형 연속 콘쥬게이션이 있을 때만 해당하며 {B_('Y')}는 비방향족이다. (ii) 높은 장 신호를 C2, C4, C6으로 고르는 것.</p>''',
),

# =====================================================================  E-3  2020B-7
dict(
    key='2020B-7',
    src='2020학년도 B형 7번',
    src_topic='cyclohexene → (NBS, hν; t-BuOK) 1,3-cyclohexadiene → diethyl maleate Diels–Alder(endo, cis 보존) → O₃/NaBH₄',
    change='다이엔을 할로젠화·제거 대신 말단 알켄의 촉매적 탈수소화로 만들고(Klein 5.66 탠덤 탈수소화–Diels–Alder), 대칭 고리 다이엔 대신 '
           '1-치환 사슬형 (E)-다이엔을 N-phenylmaleimide와 반응시켜 새 입체 중심이 3개 생기게 하였다. endo 규칙뿐 아니라 '
           '“outside 치환기와 endo 치환기가 cis가 되는” 상대 배열, 라셈체 생성, 부생성물(exo)과의 부분입체이성질 관계까지 묻는다.',
    paper=dict(cite='J. Am. Chem. Soc. 2011, 133, 14892–14895', book='Klein 5.66',
               what='hex-5-en-1-yl acetate의 촉매적 탈수소화로 생긴 1,3-다이엔이 같은 용기에서 N-phenylmaleimide와 Diels–Alder 반응 → '
                    'cis-접합 tetrahydroisoindole-1,3-dione 입체이성질체 4개(주 2: endo 거울상 쌍, 부 2: exo 거울상 쌍)'),
    nobel='1950 노벨 화학상(O. Diels·K. Alder — 다이엔 합성)',
    body=f'''다음은 hex-5-en-1-yl acetate로부터 중간 주생성물 {B_('A')}(C<sub>8</sub>H<sub>12</sub>O<sub>2</sub>)를 거쳐 최종 주생성물 {B_('B')}(C<sub>18</sub>H<sub>19</sub>NO<sub>4</sub>)를 합성하는 반응을 나타낸 것이다.
{B_('A')}는 촉매적 탈수소화로 생성되며, 같은 반응 용기에서 N-phenylmaleimide와 반응한다. (단, 각 반응에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(scheme(M(HEXENYL, '', 15), arrow('탈수소화 촉매(cat.)', '수소 받개, 가열'), L('A')),
       scheme(L('A'), plus(), M(NPM, '', 13), arrow('가열', ''), L('B'), '<span class="chem">+ 부생성물</span>', L('B′')),
       '<div class="chem" style="text-align:center"><b class="lbltxt">B</b>와 <b class="lbltxt">B′</b>(C<sub>18</sub>H<sub>19</sub>NO<sub>4</sub>)는 모두 라셈 혼합물이고, 각각 고리 접합 수소 2개는 서로 cis이다.</div>')}
<p class="ask">{B_('A')}의 입체 구조를 그리시오. {B_('B')}의 입체 구조를 그리고, 이와 같은 상대 배열이 얻어지는 이유를 전이 상태 구조를 그려서 설명하시오.
또한, {B_('B′')}의 입체 구조를 그리고 {B_('B')}와 {B_('B′')}의 입체화학적 관계를 쓰시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M(DIENE_E, 'A: (E)-hexa-3,5-dien-1-yl acetate', 14)}</div>
<div class="ansbox">{M(DA_ENDO, 'B (endo, 라셈체 중 한 거울상)', 14)}{M(DA_EXO, 'B′ (exo)', 14)}</div>
· {B_('B')}: 고리 접합 H(C3a, C7a)와 C4–H가 모두 같은 면(= C4의 CH<sub>2</sub>CH<sub>2</sub>OAc가 이미드 C=O들과 같은 면), (3a<i>S</i>,4<i>S</i>,7a<i>R</i>)/(3a<i>R</i>,4<i>R</i>,7a<i>S</i>) 라셈체<br>
· 이유: endo 전이 상태 — 이미드의 두 C=O가 다이엔 C2–C3 아래에 놓여 C=O π*와 다이엔 HOMO(C2·C3 계수) 사이의 이차 궤도 상호작용으로 안정화된다. 이때 다이엔 말단의 outside 치환기(CH<sub>2</sub>CH<sub>2</sub>OAc)는 endo C=O와 같은 면에 놓인다.<br>
· {B_('B′')}: C4 치환기가 고리 접합 H와 같은 면(이미드 C=O의 반대 면)인 exo 첨가물. {B_('B')}와 {B_('B′')}는 부분입체이성질체.''',
    explain=f'''<p><b>핵심 반응: Diels–Alder 반응의 입체특이성(suprafacial)과 endo 규칙, 1-치환 다이엔의 outside 치환기 배향.</b></p>
<p>① <b>A</b>: 말단 알켄의 C3–C4 탈수소화로 콘쥬게이션된 1,3-다이엔이 생긴다(C<sub>8</sub>H<sub>14</sub>O<sub>2</sub> − H<sub>2</sub> = C<sub>8</sub>H<sub>12</sub>O<sub>2</sub>). 열역학적으로 안정한 (<i>E</i>)-다이엔이 주로 생기며, (<i>E</i>)-1-치환 다이엔은 치환기가 바깥쪽(outside)에 있어 s-cis 형태를 쉽게 취하므로 Diels–Alder에 적합하다((<i>Z</i>)-다이엔은 inside 치환기가 C4-H와 부딪혀 s-cis가 불리하다).</p>
<p>② <b>입체특이성</b>: 다이엔과 다이엔오필 모두 같은 면으로 결합(supra/supra)하므로 cis-다이엔오필(말레이미드)의 두 C=O는 생성물에서 cis로 보존되고 → 고리 접합 H 2개도 cis이다.</p>
<p>③ <b>endo 규칙</b>: 다이엔오필의 전자 끄는 기(C=O)가 다이엔 π계 아래(“안쪽”)에 놓이는 endo 전이 상태가, 새 σ 결합을 만드는 1차 겹침 외에 C=O의 p 오비탈과 다이엔 C2·C3의 p 오비탈 사이의 2차 궤도 상호작용으로 더 안정하다(속도론적 생성물).
전이 상태 그림: 위에 s-cis 다이엔(C1 outside에 CH<sub>2</sub>CH<sub>2</sub>OAc), 아래에 말레이미드 고리가 다이엔 쪽으로 겹쳐 놓이고 N-Ph는 다이엔 C2–C3 아래 방향, 말레이미드 C–H는 바깥쪽을 향한다.</p>
<p>④ <b>outside 치환기의 운명</b>: 고리가 닫히면 다이엔 말단의 outside 치환기는 endo 치환기와 같은 면으로 간다(예: (<i>E</i>,<i>E</i>)-2,4-hexadiene + maleic anhydride → all-cis 첨가물). 따라서 {B_('B')}에서 CH<sub>2</sub>CH<sub>2</sub>OAc와 이미드 C=O들은 cis, 즉 C4–H·C3a–H·C7a–H 세 수소가 모두 같은 면에 놓인다. RDKit CIP: (3a<i>S</i>,4<i>S</i>,7a<i>R</i>) 및 거울상.</p>
<p>⑤ <b>라셈체와 B′</b>: 출발물, 시약, 촉매가 모두 비카이랄이므로 다이엔의 위·아래 면 공격이 같은 확률 → endo 첨가물은 거울상 쌍(주생성물 2개), exo 첨가물도 거울상 쌍(부생성물 2개)으로 모두 4개의 입체이성질체가 생긴다(논문 관찰과 일치).
endo와 exo는 고리 접합 배열(cis)은 같고 C4의 상대 배열만 달라 거울상이 아닌 입체이성질체, 즉 부분입체이성질체이다.</p>
<p>⑥ 흔한 오답: (i) 고리 접합을 trans로 그림(다이엔오필 cis 보존 위반), (ii) CH<sub>2</sub>CH<sub>2</sub>OAc를 고리 접합 H와 같은 면(=exo)으로 그림, (iii) {B_('B')}를 단일 거울상이라고 기술(광학 비활성 라셈체임), (iv) 위치이성질 고려 없이 치환기를 C5에 둠(다이엔 C1 치환기는 생성물 C4, 즉 고리 접합 탄소 옆 “ortho” 자리).</p>''',
),

# =====================================================================  E-4  2019B-4
dict(
    key='2019B-4',
    src='2019학년도 B형 4번',
    src_topic='2-치환 1,3-butadiene + maleic anhydride 속도(OMe > H > Cl), 1-(diethylamino)butadiene + ethyl acrylate의 “ortho” 위치선택성(FMO), '
              'vinylphosphonium Diels–Alder → 일라이드 → Wittig',
    change='정상 전자 요구형 Diels–Alder를 역전자 요구형 혼성(oxa-)Diels–Alder로 바꾸었다(Klein 17.75). 이번에는 전자가 부족한 1-oxadiene(β,γ-불포화 α-케토 에스터)의 '
           'LUMO와 전자가 풍부한 다이엔오필의 HOMO가 상호작용하므로 다이엔오필 치환기 효과가 기출과 반대 방향으로 나타나고, 위치선택성도 '
           '“음전하 자리–양전하 자리” 공명 구조/FMO 계수로 판정해야 한다. 마지막 단계는 Wittig 대신 생성물(고리형 아세탈+엔올 에터)의 산 가수분해로 '
           '1,5-다이카보닐 화합물을 얻게 하여 작용기 인식을 함께 평가한다.',
    paper=dict(cite='Org. Lett. 2001, 3, 723–726', book='Klein 17.75',
               what='4-(vinyloxy)butyl (E)-2-oxo-4-phenylbut-3-enoate 2분자가 195 ℃에서 연속 두 번의 역전자 요구형 oxa-Diels–Alder 반응으로 '
                    '2-alkoxy-3,4-dihydro-2H-pyran 고리 2개를 가진 거대 고리 이량체를 형성(머리–꼬리)'),
    nobel='1981 노벨 화학상(K. Fukui·R. Hoffmann — 전선 궤도함수 이론), 1950 노벨 화학상(O. Diels·K. Alder)',
    body=f'''다음은 β,γ-불포화 α-케토 에스터 {B_('X')}의 혼성 Diels–Alder(hetero-Diels–Alder) 반응을 나타낸 것이다. (단, 각 반응에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(scheme('<span class="chem">X = </span>', M(HDIENE, '', 14)),
       '<div class="ft">[반응 1]</div>',
       scheme(L('X'), plus(), '<span class="chem">H<sub>2</sub>C=CH–Y</span>', arrow('가열', ''), '<span class="chem">3,4-dihydro-2<i>H</i>-pyran 유도체</span>'),
       '<div class="chem" style="text-align:center">Y = –OCH<sub>2</sub>CH<sub>3</sub>, –CH<sub>2</sub>CH<sub>3</sub>, –CO<sub>2</sub>CH<sub>3</sub></div>',
       '<div class="ft">[반응 2]</div>',
       scheme(L('X'), plus(), '<span class="chem">H<sub>2</sub>C=CH–OCH<sub>2</sub>CH<sub>3</sub></span>', arrow('가열', ''), L('A'), '<span class="chem">(C<sub>15</sub>H<sub>18</sub>O<sub>4</sub>)</span>'),
       scheme('<span class="chem">(위치 이성질체</span>', M(HDA_B, '', 10), '<span class="chem">: 거의 없음)</span>'),
       '<div class="ft">[반응 3]</div>',
       scheme(L('A'), arrow('H<sub>3</sub>O<sup>+</sup>', 'THF/H<sub>2</sub>O'), L('C'), '<span class="chem">(C<sub>13</sub>H<sub>14</sub>O<sub>4</sub>)</span>'))}
<p class="ask">[반응 1]에서 Y가 각각 –OCH<sub>2</sub>CH<sub>3</sub>, –CH<sub>2</sub>CH<sub>3</sub>, –CO<sub>2</sub>CH<sub>3</sub>일 때, 동일 조건에서 반응 속도가 큰 것부터 순서대로 나열하시오.
[반응 2]에서 주생성물 {B_('A')}의 구조를 그리고, {B_('A')}가 위치 이성질체보다 우세하게 생성되는 이유를 전선 궤도함수의 계수(또는 공명 구조의 부분 전하)에 근거하여 서술하시오.
또한, {B_('C')}의 구조를 그리시오. [[PTS]]</p>''',
    answer=f'''· 속도: –OCH<sub>2</sub>CH<sub>3</sub> &gt; –CH<sub>2</sub>CH<sub>3</sub> &gt; –CO<sub>2</sub>CH<sub>3</sub><br>
<div class="ansbox">{M(HDA_A, 'A', 14)}{M(HDA_C, 'C', 14)}</div>
· {B_('A')}: methyl 2-ethoxy-4-phenyl-3,4-dihydro-2<i>H</i>-pyran-6-carboxylate &nbsp; · {B_('C')}: methyl 2,6-dioxo-4-phenylhexanoate(OHC–CH<sub>2</sub>–CH(Ph)–CH<sub>2</sub>–CO–CO<sub>2</sub>CH<sub>3</sub>)<br>
· 이유: 역전자 요구형이므로 주된 상호작용은 LUMO(X)–HOMO(vinyl ether)이다. X의 LUMO 계수는 β-탄소(C4, Ph가 붙은 탄소)에서 가장 크고(공명 구조에서 C4가 δ+), vinyl ether의 HOMO 계수는 말단 CH<sub>2</sub>에서 가장 크다(산소 비공유 전자쌍의 공명으로 CH<sub>2</sub>가 δ−).
큰 계수끼리(δ+ C4 ↔ δ− CH<sub>2</sub>) C–C 결합이 생기고 카보닐 O는 OEt가 붙은 탄소와 결합하므로 2-alkoxy 아세탈형 생성물 {B_('A')}가 생긴다.''',
    explain=f'''<p><b>핵심 반응: 역전자 요구형 oxa-Diels–Alder 반응의 FMO 해석(속도·위치선택성)과 고리형 아세탈의 산 가수분해.</b></p>
<p>① <b>다이엔 성분</b>: X에서 C=C–C=O(엔온의 O=C2–C3=C4) 4원자가 1-oxa-1,3-diene으로 작용한다. 케톤 C=O에 이웃한 에스터(–CO<sub>2</sub>CH<sub>3</sub>)가 전자를 더 끌어 다이엔 LUMO를 크게 낮춘다 → 전자가 부족한 다이엔.</p>
<p>② <b>속도(역전자 요구형)</b>: 에너지 차가 가장 작은 쌍은 LUMO(다이엔)–HOMO(다이엔오필)이다. 다이엔오필의 HOMO가 높을수록 빠르다. –OEt는 비공유 전자쌍의 공명 주게로 HOMO를 크게 높이고(엔올 에터), –CH<sub>2</sub>CH<sub>3</sub>는 약한 유발 주게, –CO<sub>2</sub>CH<sub>3</sub>는 HOMO를 낮추는 끌개이다 → OEt &gt; Et &gt; CO<sub>2</sub>Me.
기출(정상 요구형, 다이엔 쪽 치환기)과 비교하면 “전자가 풍부한 쪽의 HOMO를 높이고 전자가 부족한 쪽의 LUMO를 낮출수록 빠르다”는 같은 원리이며, 단지 역할이 바뀌었을 뿐이다.</p>
<p>③ <b>위치선택성</b>: 공명 구조 O<sup>−</sup>–C2=C3–C4<sup>+</sup>에서 다이엔 말단 C4가 δ+(LUMO 계수 최대), vinyl ether는 <sup>−</sup>CH<sub>2</sub>–CH=O<sup>+</sup>Et에서 말단 CH<sub>2</sub>가 δ−(HOMO 계수 최대).
두 말단이 결합하면 다이엔의 O1은 CH(OEt)와 결합하여 O–CH(OEt)–CH<sub>2</sub>–CH(Ph)–CH=C(CO<sub>2</sub>Me)–O 고리, 즉 {B_('A')}가 된다. 반대 배향의 생성물(3-ethoxy 이성질체)은 작은 계수끼리 결합해야 하므로 불리하다.
또한 {B_('A')}의 C2는 산소 두 개를 가진 아세탈 탄소로, 비대칭 전이 상태에서 형성되는 부분 양전하를 OEt가 안정화할 수 있다.</p>
<p>④ (입체) 이 반응도 endo 선택적이어서(OEt가 다이엔 아래로) {B_('A')}는 주로 2-OEt와 4-Ph가 cis인 라셈체로 얻어진다 — 논문의 거대 고리 이량화에서 두 번의 oxa-DA가 모두 같은 원리(머리–꼬리 위치선택성)로 진행된다.</p>
<p>⑤ <b>[반응 3]</b>: {B_('A')}의 C2는 고리형 아세탈(2-alkoxy-tetrahydropyran형)이고 C5=C6–O는 엔올 에터이다. H<sub>3</sub>O<sup>+</sup>에서 (i) OEt가 양성자화·이탈하여 옥소카베늄 → 물 첨가 → 락톨, (ii) 락톨이 열려 알데하이드(C2 → CHO)와 엔올(C6–OH)이 생기고, (iii) 엔올이 케토형으로 토토머화하여 α-케토 에스터가 된다.
따라서 {B_('C')} = OHC–CH<sub>2</sub>–CH(Ph)–CH<sub>2</sub>–C(=O)–CO<sub>2</sub>CH<sub>3</sub> (C<sub>15</sub>H<sub>18</sub>O<sub>4</sub> + H<sub>2</sub>O − C<sub>2</sub>H<sub>5</sub>OH = C<sub>13</sub>H<sub>14</sub>O<sub>4</sub>). oxa-DA/가수분해는 엔온의 β-탄소에 CH<sub>2</sub>CHO를 붙인 것과 같은 결과(아세트알데하이드 엔올 등가체의 짝지음 첨가)를 준다.</p>
<p>⑥ 흔한 오답: (i) 정상 요구형으로 착각하여 CO<sub>2</sub>Me를 가장 빠르다고 답함, (ii) C=O를 다이엔오필로 보고 2-옥세테인/옥사이클로헥센을 그림, (iii) {B_('C')}에서 에스터까지 가수분해하거나 엔올 에터 부분을 그대로 남김.</p>''',
),

# =====================================================================  E-5  2015B-논술2
dict(
    key='2015B-논술2',
    src='2015학년도 B형 논술형 2번(방향족성) · 2019학년도 B형 4번(고리 첨가) 유형',
    src_topic='벤젠·1,3-cyclopentadiene·1,3,5-cycloheptatriene의 C–H 산도를 짝염기의 방향족성으로 비교(논술 문항의 유기 소문항)',
    change='원 기출의 유기 소문항(탄소산의 산도)은 다른 문항(2022A-2 변형)에서 다루므로, 이 자리에서는 같은 영역의 더 중요한 핵심 반응인 '
           '아자이드–알카인 1,3-쌍극자 [3+2] 고리 첨가(클릭 화학)를 다루었다(정책에 따른 재구성). 고리 변형으로 촉진되는 무구리 SPAAC(Klein 17.77)의 '
           '위치 비선택성과 Cu 촉매 CuAAC의 1,4-위치특이성을 대비시키고, 생성물 1,2,3-triazole의 방향족성(π 전자 수 세기)을 묻게 하여 '
           '원 기출의 “방향족성 판정” 평가 요소를 유지하였다.',
    paper=dict(cite='J. Am. Chem. Soc. 2012, 134, 9199–9208', book='Klein 17.77',
               what='고리 변형된 dibenzo-azacyclooctynone(N-methyl lactam)과 benzyl azide의 무구리 고리 첨가 → 위치 이성질 triazole B, C가 약 1:1; '
                    '2-butyne은 반응하지 않음'),
    nobel='2022 노벨 화학상(C. R. Bertozzi·M. Meldal·K. B. Sharpless — 클릭 화학과 생체직교 화학)',
    body=f'''다음은 benzyl azide(BnN<sub>3</sub>, Bn = C<sub>6</sub>H<sub>5</sub>CH<sub>2</sub>)의 고리 첨가 반응 [반응 1]~[반응 3]을 나타낸 것이다.
{frame('<div class="ft">[반응 1]</div>',
       scheme(M(OCTYNE, 'P', 13), plus(), '<span class="chem">BnN<sub>3</sub></span>', arrow('25 ℃', '촉매 없음'), L('B'), plus(), L('C')),
       '<div class="chem" style="text-align:center"><b class="lbltxt">B</b>, <b class="lbltxt">C</b>: 모두 C<sub>23</sub>H<sub>18</sub>N<sub>4</sub>O, 약 1 : 1</div>',
       '<div class="ft">[반응 2]</div>',
       scheme('<span class="chem">CH<sub>3</sub>C≡CCH<sub>3</sub> + BnN<sub>3</sub></span>', arrow('25 ℃', '촉매 없음'), '<span class="chem">반응하지 않음</span>'),
       '<div class="ft">[반응 3]</div>',
       scheme('<span class="chem">PhC≡CH + BnN<sub>3</sub></span>', arrow('CuSO<sub>4</sub>(cat.), sodium ascorbate', '<i>t</i>-BuOH/H<sub>2</sub>O, 25 ℃'), L('D'), '<span class="chem">(C<sub>15</sub>H<sub>13</sub>N<sub>3</sub>, 단일 생성물)</span>'))}
<p class="ask">{B_('B')}와 {B_('C')}의 구조를 그리시오. [반응 1]은 25 ℃에서 촉매 없이 진행되지만 [반응 2]는 일어나지 않는 이유를 {B_('P')}의 구조적 특징에 근거하여 서술하시오.
{B_('D')}의 구조를 그리고, {B_('D')}의 1,2,3-triazole 고리가 방향족성을 갖는 이유를 고리의 π 전자 수에 근거하여 서술하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M(TRZ_B, 'B', 12)}{M(TRZ_C, 'C', 12)}</div>
<div class="ansbox">{M(TRZ_D, 'D: 1-benzyl-4-phenyl-1H-1,2,3-triazole', 14)}</div>
· {B_('B')}, {B_('C')}: 트라이아졸의 N-Bn이 카보닐 쪽 벤젠 고리에 붙은 탄소에 이웃하는 것과 N-Me 쪽 벤젠 고리에 붙은 탄소에 이웃하는 것(위치 이성질체; 어느 쪽을 B로 하든 무방)<br>
· 이유: {B_('P')}는 팔원 고리 안에 sp 탄소(이상적 180°)가 있어 C–C≡C 각이 크게 굽은(약 155° 내외) 고리 변형 알카인이다. 바닥 상태가 이미 전이 상태 구조 쪽으로 변형되어 있어 변형 에너지가 방출되며 활성화 에너지가 작고(또 굽은 알카인은 HOMO–LUMO 간격이 작다), 선형인 2-butyne은 이런 변형이 없어 실온 장벽을 넘지 못한다.<br>
· 방향족성: 평면 오원자 고리의 모든 원자가 sp<sup>2</sup>로 p 오비탈이 연속되고, C=C 2개 + N=N 2개 + N1(Bn) 비공유 전자쌍 2개 = 6π(4<i>n</i>+2, <i>n</i> = 1)이다.''',
    explain=f'''<p><b>핵심 반응: Huisgen 1,3-쌍극자 [3+2] 고리 첨가 — 변형 촉진형(SPAAC)과 Cu(I) 촉매형(CuAAC) 클릭 반응.</b></p>
<p>① <b>메커니즘(SPAAC)</b>: 아자이드(R–N=N<sup>+</sup>=N<sup>−</sup> ↔ R–N<sup>−</sup>–N<sup>+</sup>≡N)는 3원자 4π 성분(1,3-쌍극자), 알카인의 한 π 결합은 2π 성분이다. 4π + 2π = 6π(4<i>n</i>+2)이므로 열적으로 허용된 협동 반응이며, 굽은 화살표로는 (i) 말단 N<sup>−</sup>의 비공유 전자쌍 → 알카인 탄소 한쪽, (ii) C≡C π 전자 → 아자이드 치환 N(N1)과의 결합, (iii) N=N<sup>+</sup> π 전자 → 가운데 N 쪽으로 이동시켜 고리를 한 번에 닫는다.</p>
<p>② <b>위치 이성질체 B, C</b>: {B_('P')}의 두 알카인 탄소는 각각 다른 벤젠 고리(락탐 C=O 쪽, N-CH<sub>3</sub> 쪽)에 붙어 있어 전자적으로 약간 다르지만, 협동 고리 첨가의 두 배향에서 결합 형성 정도와 입체 장애가 거의 같아 아자이드의 N1(Bn이 붙은 N)이 어느 쪽 탄소와 결합하든 비슷한 속도로 반응한다 → 약 1:1의 위치 이성질체 혼합물(무구리 클릭의 한계).</p>
<p>③ <b>반응성 차이</b>: 협동 고리 첨가에서 알카인은 전이 상태에서 약 150~160°로 굽어야 하며, 이 “변형(distortion) 에너지”가 장벽의 대부분을 차지한다. 사이클로옥타인류는 바닥 상태에서 이미 굽어 있어(약 18 kcal/mol의 고리 변형) 이 비용을 미리 지불한 셈이고, 생성물에서는 변형이 해소된다.
2-butyne은 선형이므로 전부 새로 지불해야 하여 100 ℃ 이상의 가열이 필요하다. Klein 17.77에서 벤조 고리가 없거나 알카인 옆에 메틸이 있는 유도체가 수백~수천 배 느린 것도 변형 정도와 입체 장애 차이 때문이다.</p>
<p>④ <b>CuAAC(D)</b>: Cu(I)(CuSO<sub>4</sub>를 ascorbate가 환원)가 말단 알카인 C–H(pK<sub>a</sub> ≈ 25, 배위로 산성 증가)를 구리 아세틸라이드로 만든 뒤, 아자이드가 Cu에 배위하고 단계적으로 고리가 닫혀(6원 메탈라사이클 경유) 1,4-이치환 triazole만 생긴다.
열적 Huisgen 반응(촉매 없이 가열)은 1,4-와 1,5-이성질체 혼합물을 주는 반면 CuAAC는 실온·물 속에서 1,4-위치특이적이며, 내부 알카인(C–H 없음)은 반응하지 않는다.</p>
<p>⑤ <b>triazole의 방향족성</b>: 고리 다섯 원자(N1, N2, N3, C4, C5) 모두 sp<sup>2</sup>, 평면. π 전자: C4=C5 2개, N2=N3 2개, N1(피롤형 N, Bn 결합)의 비공유 전자쌍 2개 → 6π. N2·N3의 비공유 전자쌍은 sp<sup>2</sup> 오비탈(고리 평면)에 있어 π계에 포함되지 않는다(피리딘형). 방향족 고리가 생기는 것도 반응의 큰 열역학적 추진력이다.</p>
<p>⑥ 생체직교 화학: 세포 독성이 있는 Cu 없이도 실온에서 진행되는 SPAAC는 살아있는 세포의 글리칸·단백질 표지에 쓰인다(Bertozzi). 흔한 오답: B와 C를 입체이성질체(거울상)로 그림, triazole의 π 전자를 N 비공유 전자쌍 모두 포함해 10개로 셈.</p>''',
),

# =====================================================================  E-6  2014A-기입7
dict(
    key='2014A-기입7',
    src='2014학년도 A형 기입형 7번 · 2024학년도 A형 11번 유형',
    src_topic='산 촉매 다이엔온–페놀 자리옮김: 1,2-메틸 이동 후 생기는 탄소 양이온 중간체의 공명 구조',
    change='저빈도 주제인 다이엔온–페놀 1,2-이동 대신, 같은 “자리옮김” 영역의 최빈출 핵심 반응인 [3,3] 시그마 자리옮김(Claisen 계열)으로 재구성하였다. '
           '논문의 thio-Claisen(Klein 17.80)을 모델화하여 thioamide 엔올레이트의 S-알킬화 → ketene N,S-acetal → [3,3] 자리옮김으로 '
           '사차 탄소 옆에 새 카이랄 중심이 생기는 과정을 구조로 추적하게 하였다(2점 기입형 유지).',
    paper=dict(cite='J. Am. Chem. Soc. 2000, 122, 190–191', book='Klein 17.80',
               what='C₂ 대칭 trans-2,5-diphenylpyrrolidine thioamide를 BuLi로 탈양성자화 후 2-cyclohexylideneethyl bromide로 S-알킬화 → '
                    '(Z)-ketene N,S-acetal → 의자형 thio-Claisen [3,3] 자리옮김으로 사차 탄소 옆 α-카이랄 중심 형성'),
    nobel='',
    body=f'''다음은 thioamide로부터 중간체 {B_('A')}(C<sub>15</sub>H<sub>25</sub>NS)를 거쳐 주생성물 {B_('B')}(C<sub>15</sub>H<sub>25</sub>NS)를 합성하는 반응을 나타낸 것이다.
{B_('A')}는 탄소–황 이중 결합이 없는 화합물이고, {B_('A')} → {B_('B')}는 [3,3] 시그마 자리옮김이다. (단, 각 반응에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(scheme(M(THIOAMIDE, '', 15), arrow('1) <i>n</i>-BuLi, THF, −78 ℃', f'2) R–Br'), L('A')),
       scheme(L('A'), arrow('25 ℃', ''), L('B'), '<span class="chem">&nbsp;&nbsp;&nbsp;(R–Br = </span>', M(ALLYLBR, '', 13), '<span class="chem">)</span>'))}
<p class="ask">{B_('A')}와 {B_('B')}의 구조를 각각 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M(KETENE_NS, 'A (ketene N,S-acetal)', 14)}{M(THIO_B, 'B', 14)}</div>
· {B_('A')}: 1-[1-((2-cyclohexylideneethyl)thio)prop-1-en-1-yl]pyrrolidine — S-알킬화된 ketene N,S-acetal(주로 <i>Z</i>)<br>
· {B_('B')}: 2-(1-vinylcyclohexyl)-1-(pyrrolidin-1-yl)propane-1-thione (α-탄소가 카이랄 중심, 라셈체)''',
    explain=f'''<p><b>핵심 반응: [3,3] 시그마 자리옮김(thio-Claisen; Claisen·Cope와 같은 6원자 의자형 협동 반응).</b></p>
<p>① <b>탈양성자화</b>: <i>n</i>-BuLi가 C=S에 이웃한 α-CH<sub>2</sub>의 H를 떼어 thioenolate(⁻S–C(NR<sub>2</sub>)=CH–CH<sub>3</sub> ↔ S=C(NR<sub>2</sub>)–CH<sup>−</sup>–CH<sub>3</sub>)를 만든다. 피롤리딘 고리와 CH<sub>3</sub>의 A(1,3) 변형을 피하는 (<i>Z</i>)-엔올레이트가 주로 생긴다.</p>
<p>② <b>S-알킬화</b>: 황은 크고 분극성이 큰(무른) 친핵체 자리이며 음전하 밀도도 크므로 알릴형 브로마이드를 S<sub>N</sub>2로 공격한다 → C=S가 사라지고 C=C가 생긴 ketene N,S-acetal {B_('A')}(분자식 변화: C<sub>7</sub>H<sub>13</sub>NS − H + C<sub>8</sub>H<sub>13</sub> = C<sub>15</sub>H<sub>25</sub>NS). 단서 “C=S 없음”이 C-알킬화가 아님을 알려 준다.</p>
<p>③ <b>[3,3] 자리옮김</b>: {B_('A')}에는 C=C(N)–S–CH<sub>2</sub>–CH=C(고리) 의 1,5-다이엔형 6원자 배열(알릴 비닐 설파이드)이 있다. 의자형 전이 상태에서 S–CH<sub>2</sub> σ 결합이 끊어지고, 엔아민 탄소(CH–CH<sub>3</sub>)와 사이클로헥실리덴 탄소 사이에 새 C–C σ 결합이 생기며, π 결합은 C=S와 CH=CH<sub>2</sub>로 옮겨 간다.
결과적으로 고리 탄소는 비닐기와 새 C–C 결합을 가진 사차 탄소가 되고, α-탄소(CH(CH<sub>3</sub>))는 새 카이랄 중심이 된다. 강한 C=S(티오아마이드 공명) 형성이 추진력이며, 일반 Claisen(O)보다 낮은 온도에서 진행된다.</p>
<p>④ <b>입체화학</b>: 이 모델(비카이랄 피롤리딘)에서는 {B_('B')}가 라셈체이다. 논문에서는 C<sub>2</sub> 대칭 (2<i>R</i>,5<i>R</i>)-diphenylpyrrolidine이 ketene N,S-acetal의 한쪽 면을 가려, (<i>Z</i>)-기하 + 의자형 전이 상태로 α-카이랄 중심의 절대 배열이 하나로 정해진다(키랄 보조기).</p>
<p>⑤ 흔한 오답: (i) {B_('A')}를 C-알킬화물(CH<sub>3</sub>CH(R)C(=S)N)로 그림 — 분자식은 같지만 C=S가 남아 단서와 모순, (ii) {B_('B')}에서 비닐기 대신 사이클로헥실리덴을 남기고 CH<sub>2</sub>로 연결(이는 1,3-이동 생성물), (iii) 이동 후 C=S 대신 C=C–SH를 그림.</p>''',
),

# =====================================================================  F-1  2023B-1
dict(
    key='2023B-1',
    src='2023학년도 B형 1번',
    src_topic='benzoic acid·salicylic acid·4-hydroxybenzoic acid의 pKa 순서(공명·분자 내 수소 결합)와 Henderson–Hasselbalch 해리 분율',
    change='카복실산 대신 Bordwell의 DMSO 탄소산 산도 자료(Klein 3.70)를 소재로, 같은 벤질 CH₂에 붙은 치환기(Ph, C(=O)CH₃, C≡N, C(=O)N(CH₃)₂)에 따라 '
           '짝염기 음전하의 비편재화 정도가 어떻게 달라지는지 순서를 매기게 하고, 정량 문항은 해리 분율 대신 두 탄소산 사이 양성자 전달 평형상수로 바꾸었다.',
    paper=dict(cite='J. Org. Chem. 1981, 46, 4327–4331', book='Klein 3.70',
               what='Bordwell DMSO pKa: CH₃COCH₂CO₂Et 14.1, PhCH₂CN 21.9, PhCH₂CO₂Et 22.7, PhCH₂CON(CH₃)₂ 26.6; '
                    'diphenylmethane 32.2 vs phenylacetone 19.9'),
    nobel='',
    body=f'''표는 탄소산 (가)~(라)의 구조를 나타낸 것이다. 각 화합물에서 벤질 위치 CH<sub>2</sub>의 수소(H<sub>α</sub>)가 가장 산성이 큰 수소이다.
<table class="data"><tr><th>(가)</th><th>(나)</th></tr>
<tr><td>{M('c1ccc(Cc2ccccc2)cc1', '', 12)}</td><td>{M('CC(=O)Cc1ccccc1', '', 12)}</td></tr>
<tr><th>(다)</th><th>(라)</th></tr>
<tr><td>{M('N#CCc1ccccc1', '', 12)}</td><td>{M('CN(C)C(=O)Cc1ccccc1', '', 12)}</td></tr></table>
<p class="ask">(가)~(라)를 DMSO에서 H<sub>α</sub>에 해당하는 pK<sub>a</sub> 값이 큰 것부터 순서대로 나열하시오. 또한, DMSO에서 (나)의 pK<sub>a</sub>가 19.9, (라)의 pK<sub>a</sub>가 26.6일 때,
(나) + (라)의 짝염기 ⇌ (나)의 짝염기 + (라) 반응의 평형상수(<i>K</i>)를 쓰시오. [[PTS]]</p>''',
    answer='''· pK<sub>a</sub>: (가) &gt; (라) &gt; (다) &gt; (나) &nbsp;(DMSO 실측 32.2 &gt; 26.6 &gt; 21.9 &gt; 19.9)<br>
· <i>K</i> = 10<sup>(26.6 − 19.9)</sup> = 10<sup>6.7</sup> ≈ 5 × 10<sup>6</sup>''',
    explain='''<p><b>핵심 개념: 탄소산의 산도 = 짝염기(카보음이온) 안정성 — 공명(전기음성 원자로의 비편재화) > 고리로의 비편재화, 그리고 pK<sub>a</sub> 차로 평형 위치 예측.</b></p>
<p>① 네 화합물 모두 벤질 CH<sub>2</sub>이므로 음전하는 페닐 고리(o, p 탄소)로 비편재화되는 공통 기여가 있다. 차이는 다른 쪽 치환기가 음전하를 얼마나 잘 받느냐이다.</p>
<p>② (가) Ph<sub>2</sub>CH<sub>2</sub>: 음전하가 두 벤젠 고리의 탄소에만 퍼진다(전기음성 원자 없음, 비편재화 때 고리 방향족성 일부 손실) → 가장 약한 산(32.2).</p>
<p>③ (나) phenylacetone: 엔올레이트에서 음전하가 카보닐 <b>산소</b>에 놓이는 공명 구조가 가장 크게 기여한다 → 가장 강한 산(19.9). (다) PhCH<sub>2</sub>CN: 음전하가 질소로 비편재화(케텐이민 음이온형 C=C=N<sup>−</sup>)되지만 N은 O보다 전기음성도가 작고 sp 직선 구조의 공명 기여가 작다(21.9).
(라) 아마이드: N의 비공유 전자쌍이 이미 C=O로 공명 주게 역할을 하고 있어(아마이드 공명) C=O가 α-음전하를 받아들이는 능력이 줄어든다 → 케톤·나이트릴보다 약한 산(26.6). 같은 이유로 에스터(22.7)도 케톤보다 약하다.</p>
<p>④ 평형상수: <i>K</i> = <i>K</i><sub>a</sub>(나)/<i>K</i><sub>a</sub>(라) = 10<sup>−19.9</sup>/10<sup>−26.6</sup> = 10<sup>6.7</sup>. 평형은 더 약한 산((라), pK<sub>a</sub> 큼)과 더 안정한 짝염기 쪽으로 크게 치우친다.</p>
<p>⑤ 참고: 물에서의 pK<sub>a</sub>(케톤 ≈ 19, 나이트릴·에스터 ≈ 25)와 DMSO 값은 다르다. DMSO는 음이온을 수소 결합으로 안정화하지 못해 값이 전반적으로 크지만, 같은 용매 안의 상대 순서는 구조로 해석할 수 있다. 흔한 오답: 나이트릴의 강한 유발 효과만 보고 (다)를 가장 강한 산으로 고르는 것.</p>''',
),

# =====================================================================  F-2  2019A-5
dict(
    key='2019A-5',
    src='2019학년도 A형 5번',
    src_topic='pH 1에서의 글루탐산(H_A 곁사슬 COOH, H_B NH₃⁺, H_C α-COOH) 산도 순서와 pH 3.0에서 우세한 화학종',
    change='글루탐산 대신 단백질 부위 특이적 표지(클릭 화학용 말단 알카인 손잡이)를 위해 설계된 비천연 아미노산 Nε-(propargyloxycarbonyl)-L-lysine(Klein 3.64/3.72)을 사용하여, '
           '수용액에서 해리되는 산(COOH, NH₃⁺)과 해리되지 않는 약한 산(카바메이트 N–H, 말단 알카인 C–H)을 함께 순서 짓게 하였다. '
           '주어진 pKa 2개를 스스로 배정한 뒤 pH에 따른 우세 화학종을 그리게 하였다.',
    paper=dict(cite='J. Am. Chem. Soc. 2009, 131, 8720–8721', book='Klein 3.64·3.72',
               what='단백질 표지용 alkyne-lysine(Nε-propargyloxycarbonyl-L-lysine)의 산성 수소 4종(COOH, 카바메이트 N–H, ≡C–H, NH)의 산도 순서와 염기 당량별 탈양성자화'),
    nobel='2022 노벨 화학상(C. R. Bertozzi·M. Meldal·K. B. Sharpless — 클릭 화학: 단백질에 도입한 말단 알카인의 CuAAC 표지)',
    body=f'''그림은 단백질 표지에 쓰이는 비천연 아미노산 Nε-(propargyloxycarbonyl)-L-lysine이 pH = 1.0인 수용액에서 가장 많이 존재하는 형태의 구조를 나타낸 것이다.
25 ℃ 수용액에서 이 화합물의 측정 가능한 pK<sub>a</sub>는 2.2와 9.0 두 개뿐이다.
{frame(M(LYS_PH1, '', 15),
       '<div class="chem">H<sub>A</sub>: 말단 알카인의 ≡C–H &nbsp; H<sub>B</sub>: 카바메이트(–NH–C(=O)O–)의 N–H<br>'
       'H<sub>C</sub>: –NH<sub>3</sub><sup>+</sup>의 H &nbsp; H<sub>D</sub>: –COOH의 O–H</div>')}
<p class="ask">H<sub>A</sub>~H<sub>D</sub>를 산도(acidity)가 큰 것부터 순서대로 나열하시오. 또한, 이 화합물이 pH = 6.0인 수용액에서 가장 많이 존재하는 형태의 구조를 그리시오. [[PTS]]</p>''',
    answer=f'''· 산도: H<sub>D</sub> &gt; H<sub>C</sub> &gt; H<sub>B</sub> &gt; H<sub>A</sub> &nbsp;(pK<sub>a</sub> ≈ 2.2 &lt; 9.0 &lt; 약 17~20 &lt; 약 25)<br>
<div class="ansbox">{M(LYS_PH7, 'pH 6.0: 쌍극자 이온(−COO⁻, −NH₃⁺)', 15)}</div>''',
    explain=f'''<p><b>핵심 개념: ARIO(원자·공명·유발·오비탈)에 의한 산도 비교와 pH–pK<sub>a</sub> 관계에 따른 우세 화학종 판정.</b></p>
<p>① H<sub>D</sub>(α-COOH, pK<sub>a</sub> 2.2): 카복실레이트는 두 산소에 음전하가 공명 비편재화되고, 이웃한 –NH<sub>3</sub><sup>+</sup>의 강한 유발 효과가 짝염기를 더 안정화하여 보통 카복실산(≈ 4.8)보다 강하다.</p>
<p>② H<sub>C</sub>(–NH<sub>3</sub><sup>+</sup>, 9.0): 양이온 산으로, 떨어진 뒤 중성 아민이 된다. 측정 가능한 두 번째 pK<sub>a</sub>.</p>
<p>③ H<sub>B</sub>(카바메이트 N–H, ≈ 17~20): 짝염기 N<sup>−</sup>의 음전하가 C=O 산소로 공명 비편재화되어 아민 N–H(≈ 38)보다 훨씬 산성이지만 물(15.7)보다 약해 수용액에서는 해리되지 않는다.</p>
<p>④ H<sub>A</sub>(말단 알카인 ≡C–H, ≈ 25): 짝염기의 음전하가 s 성질 50%인 sp 오비탈에 있어 sp<sup>2</sup>·sp<sup>3</sup> C–H보다 안정하지만, 공명 안정화가 없어 카바메이트 N–H보다는 약하다(원자 N &gt; C의 전기음성도 + 공명).
이 C–H가 물속 어떤 pH에서도 유지되기 때문에 단백질에 도입된 뒤 Cu(I) 아세틸라이드를 거치는 CuAAC로 형광 아자이드를 선택적으로 붙일 수 있다(클릭 표지).</p>
<p>⑤ pH 6.0: pK<sub>a1</sub>(2.2) &lt; pH이므로 COOH는 거의 모두 COO<sup>−</sup>([A<sup>−</sup>]/[HA] = 10<sup>3.8</sup>), pH &lt; pK<sub>a2</sub>(9.0)이므로 NH<sub>3</sub><sup>+</sup>는 그대로([B]/[BH<sup>+</sup>] = 10<sup>−3</sup>). 카바메이트 N–H와 ≡C–H는 변하지 않는다 → 알짜 전하 0인 쌍극자 이온(등전점 ≈ (2.2 + 9.0)/2 = 5.6 부근). L-배열(α-C = <i>S</i>)은 유지된다.</p>
<p>⑥ 흔한 오답: (i) 카바메이트 N–H를 염기성 아민으로 보고 양성자화된 형태로 그림(카바메이트 N은 비공유 전자쌍이 C=O로 비편재화되어 염기성이 거의 없음), (ii) 측정된 pK<sub>a</sub> 9.0을 알카인 C–H로 배정, (iii) pH 6.0에서 NH<sub>2</sub>로 그림.</p>''',
),
]
