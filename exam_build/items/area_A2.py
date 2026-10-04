"""영역 A(카보닐 α-탄소·축합 반응) 변형 문항 2부: 2021A-9, 2020A-9, 2019A-12, 2016A-4, 2016A-5, 2015A-기입9, 2014A-서술4."""
from chem import M, L, arrow, varrow, scheme, rows, frame, nmr, ir, spec, plus

ITEMS = [
# ─────────────────────────────────────────────────────────────── 2021A-9
dict(
    key='2021A-9',
    src='2021학년도 A형 9번 유형',
    src_topic='tetronic acid의 토토머·방향족성, 2-아세톡시 에스터의 LDA 분자 내 Claisen(Dieckmann형) 고리 형성',
    change='원 기출의 평가 요소(케토–엔올 토토머, 방향족 토토머, Claisen형 C–C 결합 형성 메커니즘)를 유지하되, 분자 내 Claisen 대신 '
           '<b>교차 Claisen 축합(ethyl formate에 의한 α-포밀화)</b>을 핵심 반응으로 삼았다. 생성된 1,3-다이카보닐의 가장 안정한 토토머'
           '(분자 내 수소 결합 엔올)와 산성도, 그리고 hydrazine 고리 축합으로 생기는 방향족 피라졸(tetrahydroindazole)의 6π 방향족성과 '
           '고리 토토머(1H/2H)를 묻는다.',
    paper=dict(cite='Klein 22장 반응의 복습(교차 Claisen 축합: ethyl benzoate + ethyl acetate; Claisen 축합의 구동력)',
               book='Klein 22 Key reactions (pp. 1057–1058)',
               what='α-H가 없는 에스터(포메이트·벤조에이트)를 친전자체로 쓰는 교차 Claisen 축합으로 1,3-다이카보닐을 만들고, '
                    '생성물의 산성 C–H 탈양성자화가 평형을 끄는 원리'),
    nobel='',
    body=f'''다음은 cyclohexanone으로부터 중간 주생성물 <b class="lbltxt">A</b>(C<sub>7</sub>H<sub>10</sub>O<sub>2</sub>)를 거쳐 최종 주생성물 <b class="lbltxt">B</b>(C<sub>7</sub>H<sub>10</sub>N<sub>2</sub>)를 합성하는 반응식이다. <b class="lbltxt">A</b>는 CDCl<sub>3</sub> 용액에서 대부분 한 가지 엔올 형태로 존재하며, ¹H NMR에서 δ 14 부근에 넓은 단일선(1H)과 δ 8.6 부근에 단일선(1H)을 보이고 FeCl<sub>3</sub> 정색 반응에 양성이다. (단, 각 단계에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(scheme(M('O=C1CCCCC1', scale=15), arrow('1) HCO<sub>2</sub>Et, NaOEt (1 당량)', '2) H<sub>3</sub>O<sup>+</sup>'), L('A'),
              arrow('H<sub>2</sub>NNH<sub>2</sub>', 'EtOH, 가열'), L('B')))}
<p class="ask"><b class="lbltxt">A</b>를 다이카보닐(케토–알데하이드) 형태와 주된 엔올 형태로 각각 그리고, 굽은 화살표를 사용하여 cyclohexanone으로부터 <b class="lbltxt">A</b>의 C–C 결합이 형성되어 다이카보닐이 되기까지의 메커니즘을 제시하시오. 또한, <b class="lbltxt">B</b>의 구조를 그리고 <b class="lbltxt">B</b>의 고리가 방향족인 이유를 π 전자 수를 들어 서술하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('O=CC1CCCCC1=O', 'A (다이카보닐형): 2-oxocyclohexane-1-carbaldehyde', 15)}{M('O=C1CCCC/C1=C/O', 'A (주된 엔올형): (Z)-2-(hydroxymethylene)cyclohexanone', 15)}{M('c1n[nH]c2c1CCCC2', 'B: 4,5,6,7-tetrahydro-1H-indazole', 15)}</div>
메커니즘: EtO<sup>−</sup>가 cyclohexanone α-H를 떼어 엔올레이트 → 엔올레이트 탄소가 HCO<sub>2</sub>Et의 C=O 탄소 공격(사면체 알콕사이드) → C=O 재형성하며 EtO<sup>−</sup> 이탈 → 2-oxocyclohexane-1-carbaldehyde.<br>
(이어서 두 C=O 사이 C–H가 EtO<sup>−</sup>에 의해 즉시 탈양성자화되어 안정한 엔올레이트로 고정되고, H<sub>3</sub>O<sup>+</sup> 처리로 A가 된다.)<br>
B의 방향족성: 피라졸 고리는 평면이고 순환 콘쥬게이트되어 있으며, C=C(2) + C=N(2) + N–H 질소의 비공유 전자쌍(2) = 6π 전자(4<i>n</i>+2, <i>n</i>=1)이므로 Hückel 규칙을 만족한다(피리딘형 N의 비공유 전자쌍은 고리 평면의 sp<sup>2</sup> 궤도함수에 있어 π계에 포함되지 않는다).''',
    explain='''<p>핵심 반응: <b>교차 Claisen 축합</b>(α-H가 없는 에스터를 친전자체로 사용) → 1,3-다이카보닐의 <b>케토–엔올 토토머</b> → hydrazine과의 <b>고리 축합(Knorr형 피라졸 합성)</b>.</p>
<p>① 교차 Claisen의 설계: ethyl formate는 α-H가 없어 엔올레이트를 만들 수 없으므로 친전자체로만 작용하고, 포밀기(H–C=O)는 매우 친전자성이 커서 케톤 엔올레이트가 우선적으로 공격한다. 케톤끼리의 자기 알돌은 가역적이며, 반응은 생성물 쪽으로 끌려간다.</p>
<p>② 메커니즘(굽은 화살표): (i) EtO<sup>−</sup> 비공유 전자쌍 → α-H, C–H 결합 전자 → C=C(엔올레이트, 음전하는 산소에 비편재화). (ii) 엔올레이트 C=C π 전자 → HCO<sub>2</sub>Et의 카보닐 탄소, C=O π 전자 → 산소(사면체 중간체). (iii) O<sup>−</sup> 전자쌍이 C=O를 다시 만들면서 C–OEt 결합 전자가 EtO<sup>−</sup>로 이탈(친핵성 아실 치환). (iv) 생성된 1,3-다이카보닐의 C–H(p<i>K</i><sub>a</sub> ≈ 6–9)를 EtO<sup>−</sup>(EtOH p<i>K</i><sub>a</sub> ≈ 16)가 제거 — 이 비가역적 탈양성자화가 전체 평형의 구동력이므로 염기는 <b>1당량</b> 이상 필요하다.</p>
<p>③ <b>A</b>의 토토머: 다이카보닐형(케토–알데하이드)보다 하이드록시메틸렌형 엔올이 압도적이다. 이유: (a) C=C가 C=O와 콘쥬게이트(비닐로가스 카복실산 구조), (b) OH와 C=O가 <i>cis</i>(<i>Z</i>)로 놓여 6원 고리형 분자 내 수소 결합(O–H···O=C) 형성. 이 수소 결합 때문에 엔올 OH가 δ ≈ 14로 매우 낮은 장으로 이동하고, =CH–O 비닐 수소가 δ ≈ 8.6에 나타나며 알데하이드 CHO(δ 9.5–10, d) 신호는 거의 없다. 다른 엔올(고리 안 C=C, 알데하이드 보존형)은 콘쥬게이션·수소 결합이 덜 유리하다. FeCl<sub>3</sub> 양성도 엔올 OH의 증거.</p>
<p>④ <b>B</b>: hydrazine의 NH<sub>2</sub>가 더 친전자성인 알데하이드(엔올형에서는 비닐로가스 위치)에 먼저 축합하여 하이드라존을 만들고, 남은 NH<sub>2</sub>가 고리 케톤 C=O를 분자 내 공격 → 카비놀아민 → 탈수 → 방향족 피라졸 4,5,6,7-tetrahydro-1<i>H</i>-indazole(C<sub>7</sub>H<sub>10</sub>N<sub>2</sub> = C<sub>7</sub>H<sub>10</sub>O<sub>2</sub> + N<sub>2</sub>H<sub>4</sub> − 2H<sub>2</sub>O). 두 번의 탈수가 모두 일어나는 구동력이 방향족성 획득이다.</p>
<p>⑤ 고리 토토머: N–H 수소는 N1과 N2 사이를 빠르게 이동(1<i>H</i>-/2<i>H</i>-indazole형 고리 토토머)하며, 두 형태 모두 6π 방향족이므로 어느 것으로 그려도 정답이다. 피롤형 N(N–H)의 비공유 전자쌍은 p 궤도함수에 있어 방향족 6π에 기여하고, 피리딘형 N(=N–)의 비공유 전자쌍은 sp<sup>2</sup> 궤도함수에 있어 염기성을 띤다.</p>
<p>⑥ 흔한 오답: (i) Claisen 생성물을 에스터가 남은 β-케토 에스터로 그림(포메이트에는 남을 알콕시 탄소가 없음), (ii) A의 엔올을 OH와 C=O가 <i>trans</i>인 (<i>E</i>)형으로 그림(수소 결합 불가), (iii) B를 비방향족 다이하이드로피라졸(피라졸린)로 그림(분자식 C<sub>7</sub>H<sub>12</sub>N<sub>2</sub>로 불일치).</p>''',
),
# ─────────────────────────────────────────────────────────────── 2020A-9
dict(
    key='2020A-9',
    src='2020학년도 A형 9번 유형',
    src_topic='β-케토에스터 아실화 → MVK Michael 첨가 → 가수분해·탈카복실화 → 분자 내 알돌(다리걸친 고리)',
    change='원 기출의 “엔올(엔올레이트)의 C–C 결합 형성 → Michael 첨가 → 메커니즘 서술” 흐름을 유지하되, 핵심 반응을 '
           '<b>Mannich 반응</b>(산성 조건의 엔올 + 이미늄)과 <b>Mannich 염기의 완전 메틸화–E1cB 탈리</b>로 바꾸었다. '
           '이렇게 생긴 반응성 큰 α-메틸렌 케톤(Michael 받개)을 제자리에서 말론산 에스터로 포획하게 하여, '
           '“이미늄 친전자체”와 “Michael 받개의 마스킹(masked enone)”을 함께 평가.',
    paper=dict(cite='J. Am. Chem. Soc. 1945, 67, 860–874', book='Klein 23.92 · 22장 반응의 복습(Michael 첨가)',
               what='Woodward–Doering 퀴닌 형식 합성: 1차 아민을 과량 CH<sub>3</sub>I로 완전 메틸화한 뒤 염기·가열로 Hofmann 탈리하여 '
                    '바이닐기를 만드는 단계(본 문항은 이 완전 메틸화–탈리를 β-아미노 케톤(Mannich 염기)에 적용)'),
    nobel='1965 노벨 화학상(R. B. Woodward — 유기 합성 기술; 퀴닌 합성)',
    body=f'''다음은 cyclohexanone으로부터 중간 주생성물 <b class="lbltxt">A</b>(C<sub>9</sub>H<sub>17</sub>NO)와 <b class="lbltxt">B</b>, 중간체 <b class="lbltxt">C</b>(C<sub>7</sub>H<sub>10</sub>O)를 거쳐 최종 주생성물 <b class="lbltxt">D</b>(C<sub>14</sub>H<sub>22</sub>O<sub>5</sub>)를 합성하는 반응식이다. <b class="lbltxt">C</b>는 분리하지 않고 반응 혼합물 안에서 바로 다음 반응에 사용하였다. (단, <b class="lbltxt">C</b>를 제외한 각 단계에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(rows(scheme(M('O=C1CCCCC1', scale=15), arrow('HCHO, (CH<sub>3</sub>)<sub>2</sub>NH·HCl', 'EtOH, 가열; NaHCO<sub>3</sub>'), L('A')),
            scheme(arrow('CH<sub>3</sub>I (과량)', ''), L('B'), arrow('NaOEt, EtOH', '가열'), L('[C]')),
            scheme(arrow('CH<sub>2</sub>(CO<sub>2</sub>Et)<sub>2</sub>', 'NaOEt'), L('D'))))}
<p class="ask"><b class="lbltxt">A</b>, <b class="lbltxt">C</b>, <b class="lbltxt">D</b>의 구조를 각각 그리시오. 또한, 굽은 화살표를 사용하여 <b class="lbltxt">A</b>가 생성될 때 C–C 결합이 형성되는 단계의 메커니즘을 (친전자체가 만들어지는 과정을 포함하여) 제시하고, <b class="lbltxt">B</b>가 <b class="lbltxt">C</b>로 될 때 탈리가 쉽게 일어나는 이유를 서술하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CN(C)CC1CCCCC1=O', 'A: 2-[(dimethylamino)methyl]cyclohexanone', 15)}{M('C=C1CCCCC1=O', 'C: 2-methylenecyclohexanone', 15)}{M('CCOC(=O)C(CC1CCCCC1=O)C(=O)OCC', 'D: diethyl 2-[(2-oxocyclohexyl)methyl]malonate', 14)}</div>
(B = 2-oxocyclohexylmethyl-trimethylammonium iodide)<br>
메커니즘: (CH<sub>3</sub>)<sub>2</sub>NH가 HCHO에 첨가 → 카비놀아민 → OH 양성자화·H<sub>2</sub>O 이탈 → 이미늄 이온 CH<sub>2</sub>=N<sup>+</sup>(CH<sub>3</sub>)<sub>2</sub>. 산 촉매로 생긴 cyclohexanone의 엔올 C=C가 이미늄 탄소를 공격(C–C 결합) → 양성자화된 카보닐 → 탈양성자화 → A(염산염, 중화하여 A).<br>
탈리가 쉬운 이유: B에서 NMe<sub>3</sub><sup>+</sup>는 카보닐의 β-위치에 있고 α-H는 카보닐에 의해 산성(p<i>K</i><sub>a</sub> ≈ 19)이므로, 염기가 α-H를 떼어 엔올레이트를 만든 뒤 좋은 중성 이탈기 N(CH<sub>3</sub>)<sub>3</sub>를 밀어내는 E1cB 탈리가 일어나고, 생성된 C=C는 C=O와 콘쥬게이트된다.''',
    explain='''<p>핵심 반응: <b>Mannich 반응</b>(엔올 + 이미늄 → β-아미노 카보닐), <b>완전 메틸화–E1cB(Hofmann형) 탈리</b>, <b>Michael 첨가</b>.</p>
<p>① 친전자체 생성: 2차 아민과 폼알데하이드는 산성 조건(아민 염산염)에서 카비놀아민을 거쳐 이미늄 CH<sub>2</sub>=N<sup>+</sup>Me<sub>2</sub>(Eschenmoser 염과 같은 종)을 만든다. 이미늄 탄소는 알데하이드 탄소보다 훨씬 친전자성이 크다.</p>
<p>② C–C 결합 형성: 산성 조건이므로 친핵체는 엔올레이트가 아니라 <b>엔올</b>이다. 엔올 O의 비공유 전자쌍이 C=C를 밀어 C=C π 전자가 이미늄 탄소를 공격하고, C=N π 전자는 질소로 간다 → 옥소카베늄(양성자화된 케톤) → 탈양성자화. 생성물은 염산염으로 침전하며 NaHCO<sub>3</sub>로 중화하면 자유 아민 <b>A</b>(C<sub>9</sub>H<sub>17</sub>NO). 아민 염 형태라 두 번째 Mannich(2,6-이치환)는 억제된다.</p>
<p>③ <b>B</b>: 3차 아민 질소가 CH<sub>3</sub>I에 S<sub>N</sub>2 → 4차 암모늄 염(완전 메틸화, 퀴닌 합성의 Hofmann 탈리 전 단계와 동일).</p>
<p>④ <b>B → C</b>: 일반 Hofmann 탈리(E2, Ag<sub>2</sub>O/가열)는 강한 가열이 필요하지만, 여기서는 이탈기가 카보닐의 β-위치에 있어 α-H가 산성이므로 약한 조건에서 E1cB로 빠르게 빠진다: α-H 제거 → 엔올레이트 → 엔올레이트 전자쌍이 C=C를 만들며 NMe<sub>3</sub> 이탈 → 2-methylenecyclohexanone(C<sub>7</sub>H<sub>10</sub>O). 이 엑소-메틸렌 엔온은 β-탄소가 치환되지 않은 매우 반응성 큰 Michael 받개로, 그대로 두면 이합체화(헤테로 Diels–Alder)·중합하므로 제자리에서 포획한다. 즉 Mannich 염기는 “가려진(masked) 엔온”이다.</p>
<p>⑤ <b>D</b>: 말론산 에스터 엔올레이트(안정화된 무른 친핵체)가 C의 말단 CH<sub>2</sub>(β-탄소)에 1,4-첨가 → 케톤 엔올레이트 → 양성자화 → diethyl 2-[(2-oxocyclohexyl)methyl]malonate(C<sub>14</sub>H<sub>22</sub>O<sub>5</sub> = C<sub>7</sub>H<sub>10</sub>O + C<sub>7</sub>H<sub>12</sub>O<sub>4</sub>). 1,2-첨가는 가역적이고 무른 친핵체는 1,4-첨가가 유리하다.</p>
<p>⑥ 흔한 오답: (i) Mannich에서 아민 N이 고리 탄소에 직접 붙은 엔아민/이민을 그림, (ii) C를 고리 안 C=C 엔온(2-methylcyclohex-2-enone, 같은 C<sub>7</sub>H<sub>10</sub>O)으로 그림 — 탈리는 CH<sub>2</sub>–N 결합이 끊어지므로 C=C는 고리 밖 CH<sub>2</sub>= 이다, (iii) D를 말론산 에스터가 카보닐 탄소에 붙은 1,2-첨가물로 그림.</p>''',
),
# ─────────────────────────────────────────────────────────────── 2019A-12
dict(
    key='2019A-12',
    src='2019학년도 A형 12번',
    src_topic='diethyl adipate의 Dieckmann 축합 → C-알킬화 → 가수분해·탈카복실화(β-케토산의 고리형 전이 상태)',
    change='대칭 다이에스터 대신 비대칭 diethyl 2-methylhexanedioate를 사용하여 Dieckmann 축합의 <b>위치 선택성</b>'
           '(생성물에 산성 C–H가 남아야 평형이 고정됨)을 추가로 묻고, 알킬화제를 알릴 브로마이드로 바꾸었다. '
           '“Dieckmann–알킬화–탈카복실화”라는 고빈도 연속 반응을 한 문항에서 모두 다룬다.',
    paper=dict(cite='Klein 22장 반응의 복습(Dieckmann 축합: diethyl adipate → 2-carbethoxycyclopentanone; β-케토산 탈카복실화)',
               book='Klein 22 Key reactions',
               what='Dieckmann 축합으로 고리 β-케토 에스터를 만들고 엔올레이트 알킬화 후 가수분해·탈카복실화하는 아세토아세트산 에스터형 합성'),
    nobel='',
    body=f'''다음은 diethyl 2-methylhexanedioate로부터 중간 주생성물 <b class="lbltxt">A</b>(C<sub>9</sub>H<sub>14</sub>O<sub>3</sub>), <b class="lbltxt">B</b>(C<sub>12</sub>H<sub>18</sub>O<sub>3</sub>)와 중간체 <b class="lbltxt">C</b>(C<sub>10</sub>H<sub>14</sub>O<sub>3</sub>)를 거쳐 최종 주생성물 <b class="lbltxt">D</b>(C<sub>9</sub>H<sub>14</sub>O)를 합성하는 반응식이다. (단, 각 단계에서는 적절한 분리·정제 과정을 수행하였고, 입체 이성질체는 구별하지 않는다.)
{frame(rows(scheme(M('CCOC(=O)C(C)CCCC(=O)OCC', scale=15)),
            varrow('', '1) NaOEt, EtOH<br>2) H<sub>3</sub>O<sup>+</sup>', height=40),
            scheme(L('A'), arrow('1) NaOEt', '2) CH<sub>2</sub>=CHCH<sub>2</sub>Br'), L('B')),
            scheme(arrow('H<sub>3</sub>O<sup>+</sup>', '가열'), L('[C]'), arrow('가열', '−CO<sub>2</sub>'), L('D'))))}
<p class="ask"><b class="lbltxt">A</b>와 <b class="lbltxt">D</b>의 구조를 각각 그리고, <b class="lbltxt">A</b>의 구조 이성질체인 다른 Dieckmann 생성물이 주생성물로 얻어지지 않는 이유를 서술하시오. 또한, 굽은 화살표를 사용하여 <b class="lbltxt">C</b>로부터 <b class="lbltxt">D</b>가 생성되는 반응 메커니즘을 제시하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CCOC(=O)C1CCC(C)C1=O', 'A: ethyl 3-methyl-2-oxocyclopentane-1-carboxylate', 15)}{M('C=CCC1CCC(C)C1=O', 'D: 2-allyl-5-methylcyclopentanone', 15)}</div>
이유: 다른 이성질체 ethyl 1-methyl-2-oxocyclopentane-1-carboxylate는 두 카보닐 사이 탄소가 사급이라 산성 H가 없어, 마지막 탈양성자화(평형을 끄는 단계)가 불가능하므로 역-Claisen으로 되돌아간다. A는 산성 C–H(p<i>K</i><sub>a</sub> ≈ 11)가 EtO<sup>−</sup>에 의해 엔올레이트로 고정된다.<br>
C → D: β-케토산 C(1-allyl-3-methyl-2-oxocyclopentane-1-carboxylic acid)가 6원자 고리형 전이 상태에서 COOH의 H를 케톤 O로 전달, C–COOH σ결합이 C=C(엔올)로, CO<sub>2</sub> 이탈 → 엔올 → 케토 토토머화하여 D.''',
    explain='''<p>핵심 반응: <b>Dieckmann 축합 → β-케토 에스터 엔올레이트의 C-알킬화 → 가수분해·탈카복실화</b>(아세토아세트산 에스터 합성의 고리판).</p>
<p>① 가능한 엔올레이트 두 가지: (a) 비치환 쪽 C5(CH<sub>2</sub>, 에스터 α)의 엔올레이트가 C1 에스터(CHCH<sub>3</sub> 쪽)를 공격 → 5원 고리, 생성물 C=O가 CH(CH<sub>3</sub>)와 CH(CO<sub>2</sub>Et) 사이에 위치 = <b>A</b>. (b) 메틸 치환 C2(CH)의 엔올레이트가 C6 에스터를 공격 → ethyl 1-methyl-2-oxocyclopentane-1-carboxylate.</p>
<p>② Claisen/Dieckmann의 각 단계(엔올레이트 형성, 첨가, EtO<sup>−</sup> 이탈)는 모두 가역적이고, 생성물 β-케토 에스터의 산성 C–H(p<i>K</i><sub>a</sub> ≈ 11)를 EtO<sup>−</sup>(EtOH p<i>K</i><sub>a</sub> ≈ 16)가 떼는 마지막 단계만이 크게 내리막이다. (b)는 이 H가 없으므로 EtO<sup>−</sup>가 케톤 C=O를 공격하는 역-Claisen으로 열려 다시 (a) 경로로 흘러간다(열역학적 조절). 따라서 <b>A</b> = ethyl 3-methyl-2-oxocyclopentane-1-carboxylate (C<sub>9</sub>H<sub>14</sub>O<sub>3</sub>).</p>
<p>③ <b>B</b>: NaOEt가 다시 C1–H(두 C=O 사이)를 떼어 안정한 엔올레이트를 만들고 알릴 브로마이드와 S<sub>N</sub>2 → C1에 알릴과 CO<sub>2</sub>Et가 붙은 사급 탄소, ethyl 1-allyl-3-methyl-2-oxocyclopentane-1-carboxylate (C<sub>12</sub>H<sub>18</sub>O<sub>3</sub>). C3(CH<sub>3</sub> 쪽) α-H는 단일 카보닐 α-H(p<i>K</i><sub>a</sub> ≈ 20)라 경쟁하지 못한다.</p>
<p>④ <b>C</b>: H<sub>3</sub>O<sup>+</sup>/가열로 에스터가 가수분해되어 β-케토산(C<sub>10</sub>H<sub>14</sub>O<sub>3</sub>).</p>
<p>⑤ <b>C → D</b> 메커니즘(협동적, 6원자 고리 전이 상태 — 케톤 O, C2, C1, 카복실 C, 카복실 O, H): (i) 케톤 C=O 산소의 전자쌍 → 카복실 H (O–H 형성), (ii) 카복실 O–H 결합 전자 → 카복실 C=O 쪽으로 이동하여 CO<sub>2</sub>의 C=O 형성, (iii) C1–C(OOH) σ 결합 전자 → C1=C2 π 결합, 케톤 C=O π 전자 → 산소. 결과: CO<sub>2</sub> + 엔올(2-allyl-5-methylcyclopent-1-en-1-ol) → 케토–엔올 토토머화로 <b>D</b>(C<sub>9</sub>H<sub>14</sub>O, 2-allyl-5-methylcyclopentanone, cis/trans 혼합). 알릴의 C=C는 이 조건에서 그대로 남는다.</p>
<p>⑥ 흔한 오답: (i) 메틸이 붙은 탄소에서 고리가 닫힌 사급 β-케토 에스터를 A로 고르는 것, (ii) 탈카복실화를 단순 C–C 이종 분해(카복실 음이온 → 탄소 음이온)로 그리는 것 — 산성 조건에서는 고리형 전이 상태로 엔올을 거친다. 쉽게 탈카복실화되려면 카복실기의 β-위치에 C=O가 반드시 있어야 한다는 점도 확인할 것.</p>''',
),
# ─────────────────────────────────────────────────────────────── 2016A-4
dict(
    key='2016A-4',
    src='2016학년도 A형 4번 유형',
    src_topic='E1 탈수 → 환원성 오존 분해(1,6-다이카보닐) → 분자 내 알돌 축합(1-acetylcyclopentene)',
    change='알돌 축합은 다른 문항(영역 A 1부)에서 다루므로, 같은 “α-탄소의 엔올/엔올레이트 반응” 중 고빈도인 '
           '<b>할로폼 반응</b>(염기성 다중 할로젠화 → C–C 절단)과 <b>Hell–Volhard–Zelinsky(HVZ) 반응</b>(산 브로민화물의 엔올을 통한 α-브로민화)을 '
           '연결하였다. 염기성/산성 α-할로젠화의 차이(다중 vs 단일 치환)와 카복실산이 직접 α-할로젠화되지 않는 이유를 평가.',
    paper=dict(cite='Klein 22장 반응의 복습(할로폼 반응: NaOH, Br<sub>2</sub>; H<sub>3</sub>O<sup>+</sup> / Hell–Volhard–Zelinsky: Br<sub>2</sub>, PBr<sub>3</sub>; H<sub>2</sub>O)',
               book='Klein 22 Key reactions (pp. 1057–1058)',
               what='메틸 케톤 → 카복실산(할로폼), 카복실산 → α-브로모 카복실산(HVZ)'),
    nobel='',
    body=f'''다음은 1-cyclohexylethan-1-one으로부터 중간 주생성물 <b class="lbltxt">A</b>(C<sub>7</sub>H<sub>12</sub>O<sub>2</sub>)를 거쳐 최종 주생성물 <b class="lbltxt">B</b>(C<sub>7</sub>H<sub>11</sub>BrO<sub>2</sub>)를 합성하는 반응식이다. 첫 단계에서는 물에 녹지 않는 무거운 액체(CHBr<sub>3</sub>)가 부산물로 생긴다. (단, 각 단계에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(scheme(M('CC(=O)C1CCCCC1', scale=15), arrow('1) Br<sub>2</sub> (과량), NaOH, H<sub>2</sub>O', '2) H<sub>3</sub>O<sup>+</sup>'), L('A'),
              arrow('1) Br<sub>2</sub>, PBr<sub>3</sub> (촉매)', '2) H<sub>2</sub>O'), L('B')))}
<p class="ask"><b class="lbltxt">A</b>와 <b class="lbltxt">B</b>의 구조를 각각 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('OC(=O)C1CCCCC1', 'A: cyclohexanecarboxylic acid', 15)}{M('OC(=O)C1(Br)CCCCC1', 'B: 1-bromocyclohexane-1-carboxylic acid', 15)}</div>''',
    explain='''<p>핵심 반응: <b>할로폼 반응</b>(메틸 케톤 → 카복실산 + CHX<sub>3</sub>)과 <b>Hell–Volhard–Zelinsky 반응</b>(카복실산의 α-브로민화).</p>
<p>① 할로폼: OH<sup>−</sup>가 메틸 α-H를 떼어 엔올레이트 → Br<sub>2</sub>와 반응하여 CH<sub>2</sub>Br. 도입된 Br의 유발 효과로 남은 α-H가 더 산성이 되어 같은 탄소에서 두 번째, 세 번째 브로민화가 더 빨리 일어난다 → CBr<sub>3</sub> 케톤. 따라서 염기성 조건에서는 한 번 할로젠화된 탄소가 끝까지 할로젠화된다(산 촉매 α-할로젠화가 단일 치환에서 멈추는 것과 대조).</p>
<p>② C–C 절단: OH<sup>−</sup>가 카보닐 탄소에 첨가 → 사면체 중간체가 C=O를 다시 만들며 <sup>−</sup>CBr<sub>3</sub>(세 Br로 안정화된 탄소 음이온)를 이탈기로 내보냄 → 카복실산 + <sup>−</sup>CBr<sub>3</sub> → 양성자 교환으로 카복실레이트 + CHBr<sub>3</sub>(브로모폼, d ≈ 2.9 g/cm<sup>3</sup>). H<sub>3</sub>O<sup>+</sup> 처리로 <b>A</b> = cyclohexanecarboxylic acid(C<sub>7</sub>H<sub>12</sub>O<sub>2</sub>). 고리 쪽 3차 α-H는 입체 장애가 크고 한 번만 치환될 수 있어 절단에 관여하지 않으며, CH<sub>3</sub>의 연속 브로민화가 훨씬 빠르다.</p>
<p>③ HVZ: 카복실산은 염기와 만나면 카복실레이트가 되고, 산 조건에서도 엔올 함량이 매우 낮아 Br<sub>2</sub>와 직접 반응하지 않는다. PBr<sub>3</sub>가 일부를 산 브로민화물 RCOBr로 바꾸면, 산 브로민화물은 엔올화가 쉬워 엔올이 Br<sub>2</sub>를 공격 → α-브로모 산 브로민화물. 이것이 다른 카복실산과 교환(또는 H<sub>2</sub>O로 가수분해)하여 α-브로모 카복실산이 된다. 유일한 α-H가 고리의 3차 C–H이므로 <b>B</b> = 1-bromocyclohexane-1-carboxylic acid(C<sub>7</sub>H<sub>11</sub>BrO<sub>2</sub>).</p>
<p>④ 흔한 오답: (i) A를 α-브로모 케톤(1-bromo-1-cyclohexylethanone)으로 그림(과량 Br<sub>2</sub>·염기이므로 할로폼까지 진행), (ii) A를 탄소 수가 유지된 산으로 착각(CH<sub>3</sub> 탄소는 CHBr<sub>3</sub>로 빠져 C<sub>8</sub> → C<sub>7</sub>), (iii) B에서 Br을 고리 2번 탄소(β)에 넣음 — HVZ는 엔올을 거치므로 반드시 α-탄소.</p>''',
),
# ─────────────────────────────────────────────────────────────── 2016A-5
dict(
    key='2016A-5',
    src='2016학년도 A형 5번',
    src_topic='Birch 환원·환원적 알킬화 → 엔올 에터 가수분해·탈카복실화 → 2-ethylcyclohex-2-enone, 수득률',
    change='2-methoxybenzoic acid 대신 4-methylanisole의 Birch 환원 생성물(1-methoxy-4-methylcyclohexa-1,4-diene)을 사용하고, '
           'HCl 첨가 → 엔올 에터(α-클로로 에터) 가수분해 → <b>분자 내 엔올레이트 C-알킬화(γ-위치 할로젠, 3원 고리 형성)</b>로 '
           'bicyclo[3.1.0]hexan-2-one(사비넨 골격)을 만드는 흐름으로 변형. Birch의 위치 선택성과 엔올레이트 알킬화를 함께 평가.',
    paper=dict(cite='Aust. J. Chem. 1987, 40, 1321–1325', book='Klein 9.68',
               what='4-methylanisole의 Birch 생성물에 과량 HCl을 가해 1,4-dichloro-1-methoxy-4-methylcyclohexane을 얻고, '
                    '두 단계를 거쳐 사비넨류 향 성분의 bicyclo[3.1.0]hexane 골격을 구축'),
    nobel='',
    body=f'''다음은 4-methylanisole(<b class="lbltxt">A</b>)로부터 중간 주생성물 <b class="lbltxt">B</b>(C<sub>8</sub>H<sub>12</sub>O), <b class="lbltxt">C</b>(C<sub>8</sub>H<sub>14</sub>Cl<sub>2</sub>O), <b class="lbltxt">D</b>(C<sub>7</sub>H<sub>11</sub>ClO)를 거쳐 최종 주생성물 <b class="lbltxt">E</b>(C<sub>7</sub>H<sub>10</sub>O)를 합성하는 과정을 나타낸 것이다. (단, 각 단계에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(rows(scheme(M('COc1ccc(C)cc1', 'A', 15), arrow('Li, NH<sub>3</sub>(<i>l</i>)', 'EtOH, −78 ℃'), L('B'), arrow('HCl (과량)', ''), L('C')),
            scheme(arrow('H<sub>2</sub>O', ''), L('D'), arrow('<i>t</i>-BuOK', '<i>t</i>-BuOH'), L('E'))),
       '<div class="chem" style="text-align:left">· 첫 단계에서 Li을 넣으면 용액이 푸른색을 띠었고, <b>B</b>는 콘쥬게이트되지 않은 다이엔이다.<br>· <b>D</b>는 IR 1715 cm<sup>−1</sup>에서 강한 흡수를 보이고, <b>E</b>의 ¹H NMR에는 δ 0.3–1.0 부근(고리 긴장이 큰 3원 고리 CH<sub>2</sub>) 신호가 나타난다.</div>')}
<p class="ask"><b class="lbltxt">B</b>와 <b class="lbltxt">E</b>의 구조를 각각 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('COC1=CCC(C)=CC1', 'B: 1-methoxy-4-methylcyclohexa-1,4-diene', 15)}{M('CC12CCC(=O)C1C2', 'E: 5-methylbicyclo[3.1.0]hexan-2-one', 16)}</div>
(C = 1,4-dichloro-1-methoxy-4-methylcyclohexane, D = 4-chloro-4-methylcyclohexan-1-one)''',
    explain='''<p>핵심 반응: <b>Birch 환원</b>(전자 주개 치환 탄소는 환원되지 않음) + <b>엔올 에터 가수분해</b> + <b>엔올레이트의 분자 내 C-알킬화</b>.</p>
<p>① Li/NH<sub>3</sub>의 푸른색은 용매화 전자. 전자 첨가 → 라디칼 음이온 → EtOH 양성자화 → 두 번째 전자 → 양성자화. OCH<sub>3</sub>와 CH<sub>3</sub>는 전자 주개이므로 이들이 붙은 C1, C4는 sp<sup>2</sup>로 남고 C2/C3·C5/C6 중 마주 보는 두 탄소(C3, C6)가 양성자화된다 → <b>B</b> = 1-methoxy-4-methylcyclohexa-1,4-diene (콘쥬게이트되지 않은 1,4-다이엔, C<sub>8</sub>H<sub>12</sub>O).</p>
<p>② <b>C</b>: 엔올 에터 C=C는 C2에 양성자화되어 산소 공명으로 안정한 옥소카베늄을 만들고 Cl<sup>−</sup>가 첨가(α-클로로 에터). 3치환 알켄은 마르코프니코프 방향으로 3차 탄소 양이온을 거쳐 3차 염화물. → 1,4-dichloro-1-methoxy-4-methylcyclohexane.</p>
<p>③ <b>D</b>: α-클로로 에터는 물에서 쉽게 이온화(옥소카베늄) → 헤미아세탈 → 케톤(−CH<sub>3</sub>OH, −HCl). 3차 C–Cl은 남아 4-chloro-4-methylcyclohexan-1-one (C<sub>7</sub>H<sub>11</sub>ClO, IR 1715 cm<sup>−1</sup>).</p>
<p>④ <b>E</b>: <i>t</i>-BuOK가 C2(α)–H를 떼어 엔올레이트 형성 → 엔올레이트 탄소 C2가 1,3-관계의 C4를 뒤쪽에서 공격하여 Cl<sup>−</sup>를 밀어내는 분자 내 S<sub>N</sub>2(3-exo-tet). C2–C3–C4가 사이클로프로페인이 되어 5-methylbicyclo[3.1.0]hexan-2-one (C<sub>7</sub>H<sub>10</sub>O, D − HCl). 엔올레이트의 다른 α-탄소(C6)도 대칭적으로 동등하므로 같은 생성물이다. 고리 접합은 반드시 <i>cis</i>(3원 고리 융합)이다.</p>
<p>⑤ 흔한 오답: (i) Birch에서 OCH<sub>3</sub>가 붙은 탄소가 환원된 다이엔(전자 끄는 기 규칙과 혼동), (ii) <b>B</b>를 산 처리한 콘쥬게이트 엔온(4-methylcyclohex-2-enone)으로 착각, (iii) <i>t</i>-BuOK에 의한 E2 탈리 생성물(4-methylcyclohex-3-enone, C<sub>7</sub>H<sub>10</sub>O로 분자식이 같음!) — 이 경우 NMR에 비닐 H(δ ≈ 5.4)가 나타나고 0.3–1.0 ppm 3원 고리 신호가 없으므로 제시된 단서로 배제된다.</p>''',
),
# ─────────────────────────────────────────────────────────────── 2015A-기입9
dict(
    key='2015A-기입9',
    src='2015학년도 A형 기입형 9번 유형',
    src_topic='사이클로헥산온–피롤리딘 엔아민의 Stork Michael 첨가 → 가수분해 → Robinson 고리 형성',
    change='엔아민(Stork) 화학은 다른 문항에서 다루므로, 같은 평가 요소인 “비대칭 케톤의 어느 α-탄소가 반응하는가”를 '
           '<b>동역학적 엔올레이트(LDA, −78 ℃) vs 열역학적 엔올레이트(NaH, 25 ℃ 평형 조건)</b>의 알킬화로 바꾸었다. '
           '두 생성물이 같은 분자식(C<sub>10</sub>H<sub>16</sub>O)의 구조 이성질체가 되도록 하여 위치 선택성 판단만으로 답을 가르게 하였다.',
    paper=dict(cite='Klein 22장 반응의 복습(엔올레이트 알킬화: LDA, −78 ℃ 동역학적 vs NaH, 25 ℃ 열역학적)',
               book='Klein 22 Key reactions (pp. 1057–1058)',
               what='비대칭 케톤에서 LDA는 덜 치환된 α-탄소, 평형 조건 염기는 더 치환된 α-탄소에서 엔올레이트를 만들어 알킬화'),
    nobel='',
    body=f'''다음은 2-methylcyclohexanone을 서로 다른 조건에서 allyl bromide로 알킬화하여 주생성물 <b class="lbltxt">A</b>와 <b class="lbltxt">B</b>를 각각 얻는 반응식이다. <b class="lbltxt">A</b>와 <b class="lbltxt">B</b>는 분자식이 C<sub>10</sub>H<sub>16</sub>O로 같다. (단, 각 단계에서는 적절한 분리·정제 과정을 수행하였고, 입체 이성질체는 구별하지 않는다.)
{frame(rows(scheme(M('CC1CCCCC1=O', scale=15), arrow('1) LDA, THF, −78 ℃', '2) CH<sub>2</sub>=CHCH<sub>2</sub>Br'), L('A')),
            scheme(M('CC1CCCCC1=O', scale=15), arrow('1) NaH, THF, 25 ℃ (평형 조건)', '2) CH<sub>2</sub>=CHCH<sub>2</sub>Br'), L('B'))))}
<p class="ask"><b class="lbltxt">A</b>와 <b class="lbltxt">B</b>의 구조를 각각 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('C=CCC1CCCC(C)C1=O', 'A: 2-allyl-6-methylcyclohexanone', 15)}{M('C=CCC1(C)CCCCC1=O', 'B: 2-allyl-2-methylcyclohexanone', 15)}</div>''',
    explain='''<p>핵심 반응: <b>엔올레이트 알킬화의 위치 선택성</b> — 동역학적 조절(LDA, −78 ℃, 비가역) vs 열역학적 조절(약한 염기/양성자 공급원 존재, 25 ℃, 가역).</p>
<p>① LDA: 부피가 큰 강염기(짝산 p<i>K</i><sub>a</sub> ≈ 36)로, 낮은 온도에서 케톤(p<i>K</i><sub>a</sub> ≈ 20)을 비가역적·정량적으로 탈양성자화한다. 입체적으로 덜 가려지고 H가 더 많은(통계적으로 유리한) C6–H(CH<sub>2</sub>)가 더 빨리 떨어진다 → 덜 치환된 엔올레이트(동역학적 생성물). 남은 케톤이 없으므로 엔올레이트 사이의 양성자 교환(평형화)이 일어나지 않는다. S<sub>N</sub>2 알킬화 → <b>A</b> = 2-allyl-6-methylcyclohexanone(cis/trans 혼합).</p>
<p>② NaH, 25 ℃: 탈양성자화가 느리고 남아 있는 케톤과 엔올레이트 사이에서 양성자 교환이 일어나 두 엔올레이트가 평형을 이룬다. 더 많이 치환된 C=C를 가진 엔올레이트(C1=C2, 사치환 알켄형)가 더 안정하므로 우세하다 → 더 치환된 C2에서 알킬화 → 사급 탄소를 가진 <b>B</b> = 2-allyl-2-methylcyclohexanone. (실제로는 위치 이성질체와 다중 알킬화가 일부 섞이지만, 주생성물은 B이다.)</p>
<p>③ 비교 정리: 동역학적 엔올레이트 = 덜 치환된 쪽, 빠르게 생성 / 열역학적 엔올레이트 = 더 치환된 쪽, 더 안정. 엔아민(Stork)도 A<sup>1,3</sup> 변형 때문에 덜 치환된 쪽에서 반응하므로 A와 같은 위치 선택성을 준다.</p>
<p>④ 흔한 오답: 두 조건의 생성물을 뒤바꾸어 쓰거나, 동역학적 조건에서 O-알킬화(알릴 엔올 에터)를 그리는 것 — Li 엔올레이트와 알킬 브로마이드의 반응은 주로 C-알킬화이다.</p>''',
),
# ─────────────────────────────────────────────────────────────── 2014A-서술4
dict(
    key='2014A-서술4',
    src='2014학년도 A형 서술형 4번',
    src_topic='cyclohexanone의 Henry 반응, 사이아노하이드린/LiAlH4, Darzens 축합(글리시드산 에스터) 메커니즘',
    change='Henry·사이아노하이드린 경로 대신 “같은 생성물에 이르는 두 경로”의 틀은 유지하면서, Wittig(메톡시메틸렌 일라이드) → 엔올 에터 가수분해와 '
           'Darzens 축합 → 비누화·탈카복실화라는 두 가지 <b>탄소 1개 증가 알데하이드 합성</b>으로 바꾸었다. '
           '원 기출의 Darzens 메커니즘 대신 엔올 에터의 산 촉매 가수분해 메커니즘을 묻는다.',
    paper=dict(cite='Chem. Ber. 1962, 95, 2514–2525', book='Klein 20.90',
               what='cyclohexanone + Ph<sub>3</sub>P=CHOMe(Wittig) → (methoxymethylene)cyclohexane, H<sub>3</sub>O<sup>+</sup> → cyclohexanecarbaldehyde'),
    nobel='1979 노벨 화학상(G. Wittig — 인 일라이드를 이용한 알켄 합성)',
    body=f'''다음은 cyclohexanone으로부터 두 가지 경로로 같은 주생성물 <b class="lbltxt">B</b>(C<sub>7</sub>H<sub>12</sub>O)를 합성하는 반응식이다. <b class="lbltxt">A</b>(C<sub>8</sub>H<sub>14</sub>O)는 중간 주생성물이고, <b class="lbltxt">C</b>(C<sub>10</sub>H<sub>16</sub>O<sub>3</sub>)는 IR 1745 cm<sup>−1</sup>에서 강한 흡수를 보이며 O–H 흡수가 없다. (단, 각 단계에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(rows(scheme(M('O=C1CCCCC1', scale=15), arrow('Ph<sub>3</sub>P=CHOCH<sub>3</sub>', 'THF'), L('A'), arrow('H<sub>3</sub>O<sup>+</sup>', ''), L('B')),
            scheme(M('O=C1CCCCC1', scale=15), arrow('ClCH<sub>2</sub>CO<sub>2</sub>Et', 'NaOEt'), L('C'),
                   arrow('1) NaOH, H<sub>2</sub>O', '2) H<sub>3</sub>O<sup>+</sup>, 가열'), L('B'))))}
<p class="ask"><b class="lbltxt">A</b>, <b class="lbltxt">B</b>, <b class="lbltxt">C</b>의 구조를 각각 그리고, 굽은 화살표를 사용하여 <b class="lbltxt">A</b>로부터 <b class="lbltxt">B</b>가 생성되는 반응 메커니즘을 제시하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('COC=C1CCCCC1', 'A: (methoxymethylene)cyclohexane', 15)}{M('O=CC1CCCCC1', 'B: cyclohexanecarbaldehyde', 15)}{M('CCOC(=O)C1OC12CCCCC2', 'C: ethyl 1-oxaspiro[2.5]octane-2-carboxylate', 14)}</div>
A → B: ① 엔올 에터의 C=C가 H<sub>3</sub>O<sup>+</sup>의 H를 공격 — 양성자는 고리 탄소(β-탄소)에 붙고 옥소카베늄(CH=O<sup>+</sup>CH<sub>3</sub>) 생성 ② H<sub>2</sub>O가 옥소카베늄 탄소 공격 ③ 양성자 이동 → 헤미아세탈 ④ OCH<sub>3</sub> 양성자화, O–H 비공유 전자쌍이 C=O<sup>+</sup>H를 만들며 CH<sub>3</sub>OH 이탈 ⑤ 탈양성자화 → B.''',
    explain='''<p>핵심 반응: <b>Wittig 반응</b>(옥사포스페테인) 및 <b>Darzens 글리시드산 에스터 축합</b> — 둘 다 케톤을 탄소 1개 늘어난 알데하이드로 바꾸는 고전적 방법.</p>
<p>① <b>A</b>: 일라이드 탄소가 C=O 탄소를 공격 → 옥사포스페테인 → Ph<sub>3</sub>P=O(강한 P=O 결합이 구동력) 이탈 → 엔올 에터 (methoxymethylene)cyclohexane (C<sub>8</sub>H<sub>14</sub>O). 고리 탄소가 이중 치환이므로 <i>E</i>/<i>Z</i> 문제는 없다.</p>
<p>② <b>A → B</b>(산 촉매 엔올 에터 가수분해): 엔올 에터 C=C는 산소의 공명 주개 효과로 전자가 풍부하며, 양성자는 산소에서 먼 탄소(고리 C)에 붙어 산소 비공유 전자쌍으로 안정화된 옥소카베늄이 된다(속도 결정 단계). 물 첨가 → 헤미아세탈 → 메톡시기 양성자화·CH<sub>3</sub>OH 이탈 → 양성자화된 알데하이드 → 탈양성자화. <b>B</b> = cyclohexanecarbaldehyde (C<sub>7</sub>H<sub>12</sub>O, ¹H NMR δ ≈ 9.6, d).</p>
<p>③ <b>C</b>(Darzens): EtO<sup>−</sup>가 ClCH<sub>2</sub>CO<sub>2</sub>Et의 α-H(Cl과 에스터가 함께 안정화)를 떼어 엔올레이트 → cyclohexanone C=O에 알돌형 첨가 → 알콕사이드가 인접 C–Cl을 뒤쪽에서 분자 내 S<sub>N</sub>2 → α,β-에폭시 에스터(글리시드산 에스터) C<sub>10</sub>H<sub>16</sub>O<sub>3</sub>. IR 1745 cm<sup>−1</sup>(에스터), O–H 없음 → 할로하이드린이 아님을 확인.</p>
<p>④ <b>C → B</b>: NaOH로 비누화 → 글리시드산 → 가열하면 카복실 H가 에폭사이드 산소로 전달되면서 C–C(OOH) 결합이 끊어지고 CO<sub>2</sub>가 빠지며 에폭사이드 C–O가 열려 엔올(cyclohexylidenemethanol)이 생성 → 토토머화하여 <b>B</b>. (β-케토산 탈카복실화와 같은 고리형 전이 상태 원리)</p>
<p>⑤ 흔한 오답: (i) A를 메틸렌사이클로헥세인 + 메탄올로 착각, (ii) 엔올 에터 양성자화를 산소에서 일으키는 것(옥소카베늄이 생기지 않음), (iii) B를 cyclohexanone + 1C인 케톤(cycloheptanone, Tiffeneau–Demjanov형 고리 확장 생성물)으로 쓰는 것 — cycloheptanone도 C<sub>7</sub>H<sub>12</sub>O이지만 Wittig/Darzens 경로는 고리 밖에 CHO를 만든다.</p>''',
),
]
