"""영역 A(카보닐 α-탄소·축합 반응) 변형 문항 1부 — 2026A-11, 2025A-11, 2024B-7, 2023B-7, 2023A-10, 2022B-9, 2022A-9."""
from chem import M, L, arrow, varrow, scheme, rows, frame, nmr, ir, spec, plus

LB = lambda t: f'<b class="lbltxt">{t}</b>'
A_, B_, C_, D_, E_ = (LB(x) for x in 'ABCDE')
NOTE = '(단, 각 반응에서는 적절한 분리·정제 과정을 수행하였다.)'

ITEMS = [
# ─────────────────────────────────────────────────────────────── 2026A-11
dict(
    key='2026A-11',
    src='2026학년도 A형 11번',
    src_topic='β-keto ester + MVK의 Robinson 고리화(Michael + 분자 내 알돌), 싸이오아세탈/Raney Ni, LiAlH₄, 하이드로보레이션, Jones 산화',
    change='염기(NaOEt) 대신 (S)-proline 유기촉매를 쓰는 Hajos–Parrish 비대칭 Robinson 고리화로 바꾸어, '
           '“고리 형성 단계 메커니즘”을 엔아민 촉매 메커니즘으로, “작용기 변환”을 NaBH₄의 화학선택적·부분입체선택적 환원으로 묻도록 변형. '
           '알돌 첨가물(케톨)과 탈수 엔온을 분리하여 단계별 사고를 요구하고, 거울상 선택성(절대 배열)까지 평가한다.',
    paper=dict(cite='Klein 22장 반응의 복습(Robinson 고리화)', book='Klein 22 (pp. 1057–1058)',
               what='2-methyl-1,3-dione + MVK의 Michael 첨가와 분자 내 알돌 축합(Robinson 고리화). 본 문항은 이를 (S)-proline 촉매 Hajos–Parrish 반응(스테로이드 CD 고리 합성 단위)으로 확장'),
    nobel='2021 노벨 화학상(B. List·D. W. C. MacMillan — 비대칭 유기촉매). List의 프롤린 엔아민 촉매 연구의 출발점이 Hajos–Parrish 반응이다.',
    body=f'''다음은 2-methylcyclopentane-1,3-dione으로부터 중간 주생성물 {A_}(C<sub>10</sub>H<sub>14</sub>O<sub>3</sub>), {B_}(C<sub>10</sub>H<sub>14</sub>O<sub>3</sub>), {C_}(C<sub>10</sub>H<sub>12</sub>O<sub>2</sub>)를 거쳐 최종 주생성물 {D_}(C<sub>10</sub>H<sub>14</sub>O<sub>2</sub>)를 합성하는 반응을 나타낸 것이다. {B_}는 두고리 화합물이며 한 가지 거울상 이성질체가 주로 얻어진다. {NOTE}
{frame(rows(
    scheme(M('CC1C(=O)CCC1=O', scale=15), plus(), M('C=CC(C)=O', scale=15),
           arrow('Et<sub>3</sub>N (촉매량)', 'EtOAc, 25 ℃'), L('A')),
    scheme(arrow('(<i>S</i>)-proline (3 mol%)', 'DMF, 25 ℃'), L('B'),
           arrow('TsOH (촉매량)', '벤젠, 가열'), L('C')),
    scheme(arrow('NaBH<sub>4</sub> (0.3 당량)', 'EtOH, 0 ℃'), L('D'))),
    scheme('<div class="chem">(<i>S</i>)-proline =</div>', M('OC(=O)[C@@H]1CCCN1', scale=13)))}
<p class="ask">{A_}의 구조와 {B_}의 입체구조를 각각 그리시오. (<i>S</i>)-proline에 의해 {A_}로부터 {B_}가 생성되는 과정에서 고리가 형성되는 단계를 포함한 반응 메커니즘을 굽은 화살표를 사용하여 제시하시오. 또한, {D_}의 입체구조를 그리고, NaBH<sub>4</sub>가 {C_}의 두 카보닐기 중 한쪽만 환원하는 이유를 서술하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CC(=O)CCC1(C)C(=O)CCC1=O', 'A', 14)}{M('C[C@]12CCC(=O)C[C@@]1(O)CCC2=O', 'B: (3aS,7aS)-케톨', 14)}</div>
<div class="ansbox">{M('C[C@]12CCC(=O)C=C1CCC2=O', 'C: (S)-Hajos–Parrish 케톤', 14)}{M('C[C@]12CCC(=O)C=C1CC[C@@H]2O', 'D: (1S,7aS)', 14)}</div>
A = 2-methyl-2-(3-oxobutyl)cyclopentane-1,3-dione (Michael 첨가물). B = (3a<i>S</i>,7a<i>S</i>)-3a-hydroxy-7a-methylhexahydro-1<i>H</i>-indene-1,5(4<i>H</i>)-dione (<i>cis</i> 접합, OH와 CH<sub>3</sub>가 같은 쪽).
D = (1<i>S</i>,7a<i>S</i>)-1-hydroxy-7a-methyl-1,2,3,6,7,7a-hexahydro-5<i>H</i>-inden-5-one (OH와 각진 CH<sub>3</sub>가 <i>cis</i>).<br>
메커니즘: ① proline의 N이 A의 곁사슬 메틸 케톤 C=O에 첨가 → 카비놀아민 → 탈수하여 이미늄 → α-H(말단 CH<sub>3</sub>) 제거로 엔아민. ② 엔아민의 β-탄소가 고리의 두 카보닐(거울상 위치 관계) 중 하나를 공격하여 6원 고리 형성(proline의 CO<sub>2</sub>H가 생성되는 알콕사이드 O에 양성자를 전달하며 한쪽 면을 지정). ③ 생성된 이미늄이 가수분해되어 B와 proline 재생.<br>
이유: C의 고리 접합부에 있는 오각 고리 케톤은 짝지어지지 않은 포화 케톤이지만 육각 고리 케톤은 C=C와 짝지어진 엔온이다. 짝지음(공명 C=C–C=O ↔ <sup>+</sup>C–C=C–O<sup>−</sup>)으로 엔온 카보닐 탄소의 친전자성이 낮아지므로, 저온에서 소량의 NaBH<sub>4</sub>는 포화 케톤(C1)만 환원한다.''',
    explain=f'''<p>핵심 반응: <b>Robinson 고리화(Michael 첨가 + 분자 내 알돌 축합)와 프롤린 엔아민 촉매(Hajos–Parrish 반응)</b>.</p>
<p>① <b>A 생성(Michael 첨가)</b>: 2-methylcyclopentane-1,3-dione의 C2–H는 두 카보닐 사이에 있어 매우 산성이다(고리형 1,3-다이온은 대부분 엔올로 존재하며 p<i>K</i><sub>a</sub> ≈ 5 수준). Et<sub>3</sub>N이 만든 엔올레이트가 MVK의 β-탄소에 1,4-첨가 → 엔올레이트 양성자화 → A(C<sub>10</sub>H<sub>14</sub>O<sub>3</sub>, 4차 탄소에 CH<sub>3</sub>와 3-oxobutyl). A는 대칭면을 가지는 비카이랄(prochiral) 트라이케톤이며 두 고리 카보닐은 거울상 위치(enantiotopic)이다.</p>
<p>② <b>B 생성(엔아민 알돌)</b>: proline(2차 아민)이 곁사슬 메틸 케톤과 이미늄을 거쳐 엔아민을 만든다(고리 케톤은 4차 탄소에 인접해 입체 장애가 크다). 엔아민의 말단 탄소가 고리 C=O를 공격하면 6원 고리가 생긴다(6-enolendo). 이때 proline의 카복실산이 알콕사이드가 되는 산소와 수소 결합하여 양성자를 주는 고리형(의자형) 전이 상태(Houk–List 모델)를 이루므로, 두 거울상 위치의 카보닐 중 한쪽, 한쪽 면에서만 반응한다 → <b>탈대칭화(desymmetrization)</b>. 이미늄 가수분해로 케톨 B와 proline이 재생된다(촉매). B의 분자식이 A와 같은 것(C<sub>10</sub>H<sub>14</sub>O<sub>3</sub>)은 알돌 <u>첨가</u> 단계에서 멈추었음을 뜻한다. 5–6 접합 고리에서 OH와 각진 CH<sub>3</sub>는 <i>cis</i>(3a<i>S</i>,7a<i>S</i>)이다.</p>
<p>③ <b>C 생성(탈수)</b>: TsOH/가열에서 3차 β-하이드록시 케톤이 탈수(엔올 경유 E1)하여 짝지어진 엔온 C, 즉 (<i>S</i>)-7a-methyl-2,3,7,7a-tetrahydro-1<i>H</i>-indene-1,5(6<i>H</i>)-dione(Hajos–Parrish 케톤)이 된다. 7a의 배열은 그대로 유지된다(입체 중심은 반응에 참여하지 않음).</p>
<p>④ <b>D 생성(화학선택적·입체선택적 환원)</b>: 엔온 카보닐은 C=C와의 공명으로 친전자성이 낮고 1,2-첨가 시 짝지음 안정화를 잃으므로, NaBH<sub>4</sub>(소량, 0 ℃)는 오각 고리의 포화 케톤만 환원한다. 하이드라이드는 각진 메틸이 막고 있는 면의 반대쪽(α면)에서 접근하므로 생성된 OH는 메틸과 같은 쪽(β, <i>cis</i>)에 놓인다 → (1<i>S</i>,7a<i>S</i>)-D (스테로이드의 17β-OH·18-CH<sub>3</sub> 관계와 같다).</p>
<p>⑤ <b>흔한 오답</b>: (가) B를 탈수된 엔온으로 그리는 것 — B의 분자식은 A와 같으므로 H<sub>2</sub>O가 빠지지 않았다. (나) 곁사슬의 안쪽 CH<sub>2</sub>(C3′)로부터 엔아민/엔올레이트가 고리를 공격한다고 보는 것 — 4원 고리가 되어 불가능하다. (다) D에서 엔온을 환원하거나(알릴 알코올) OH를 메틸과 <i>trans</i>로 그리는 것. (라) 라셈체로 답하는 것 — 키랄 촉매 (<i>S</i>)-proline이 한쪽 거울상 이성질체를 우세하게 만든다(문헌상 93% ee 수준). 같은 반응을 2-methylcyclohexane-1,3-dione으로 하면 Wieland–Miescher 케톤이 얻어진다.</p>''',
),
# ─────────────────────────────────────────────────────────────── 2025A-11
dict(
    key='2025A-11',
    src='2025학년도 A형 11번',
    src_topic='말론산 에스터 합성(알킬화–가수분해–탈카복실화)과 알카인 알킬화 + Na/NH₃(l) trans 환원의 두 경로로 같은 카복실산 합성',
    change='말론산 에스터 합성을 유지하되 이중 알킬화(다이알릴화) 후 Grubbs 촉매 고리 닫기 복분해(RCM)로 고리를 만드는 경로로 바꾸고, '
           '“반응 조건 쓰기” 대신 β-다이카복실산 탈카복실화의 고리형 메커니즘(굽은 화살표)을 요구하도록 변형.',
    paper=dict(cite='Org. Lett. 2000, 2, 791–794', book='Klein 21.81',
               what='Grubbs 촉매를 이용한 다이엔의 고리 닫기 복분해(RCM)로 고리 알켄과 에틸렌 생성 — 본 문항은 말론산 에스터 다이알릴화 기질(복분해의 표준 기질)로 모델화'),
    nobel='2005 노벨 화학상(Y. Chauvin·R. H. Grubbs·R. R. Schrock — 올레핀 복분해)',
    body=f'''다음은 diethyl malonate로부터 중간 주생성물 {A_}(C<sub>13</sub>H<sub>20</sub>O<sub>4</sub>)와 {B_}(C<sub>11</sub>H<sub>16</sub>O<sub>4</sub>)를 거쳐 최종 주생성물 카복실산 {C_}(C<sub>6</sub>H<sub>8</sub>O<sub>2</sub>)를 합성하는 반응을 나타낸 것이다. {B_}가 생성될 때 기체 화합물이 함께 생성된다. {NOTE}
{frame(rows(
    scheme(M('CCOC(=O)CC(=O)OCC', scale=14),
           arrow('1) NaOEt 2) CH<sub>2</sub>=CHCH<sub>2</sub>Br', '3) NaOEt 4) CH<sub>2</sub>=CHCH<sub>2</sub>Br'), L('A')),
    scheme(L('A'), arrow('Grubbs 촉매 (5 mol%)', 'CH<sub>2</sub>Cl<sub>2</sub>, 25 ℃'), L('B'), plus(), '<div class="chem">기체</div>'),
    scheme(L('B'), arrow('1) KOH, H<sub>2</sub>O, 가열', '2) H<sub>3</sub>O<sup>+</sup>, 가열'), L('C'))),
    '<div class="chem" style="text-align:center">Grubbs 촉매 = (Cy<sub>3</sub>P)<sub>2</sub>Cl<sub>2</sub>Ru=CHPh</div>')}
<p class="ask">{A_}, {B_}, {C_}의 구조를 각각 그리시오. 또한, {B_}를 가수분해하여 얻은 다이카복실산(C<sub>7</sub>H<sub>8</sub>O<sub>4</sub>)이 가열에 의해 {C_}로 전환되는 반응 메커니즘을 굽은 화살표를 사용하여 제시하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('C=CCC(CC=C)(C(=O)OCC)C(=O)OCC', 'A', 13)}{M('CCOC(=O)C1(C(=O)OCC)CC=CC1', 'B', 13)}{M('OC(=O)C1CC=CC1', 'C', 14)}</div>
A = diethyl 2,2-diallylmalonate, B = diethyl cyclopent-3-ene-1,1-dicarboxylate(+ CH<sub>2</sub>=CH<sub>2</sub>↑), C = cyclopent-3-ene-1-carboxylic acid.<br>
탈카복실화: 다이카복실산의 한 COOH의 O–H 수소가 다른 C=O 산소로 옮겨 가는 6원 고리 전이 상태에서 ① 카보닐 O가 산성 H를 받고 ② O–H 결합 전자가 C=O로 가서 CO<sub>2</sub>가 형성되며 ③ C1–COOH 결합 전자가 C1=C(OH)<sub>2</sub> π 결합이 된다(협동, 페리고리 반응) → CO<sub>2</sub> + 엔올(1,1-다이하이드록시알켄) → 토토머화(엔올 C=C가 양성자를 받고 O–H가 C=O로) → C.''',
    explain=f'''<p>핵심 반응: <b>말론산 에스터 합성(엔올레이트 알킬화 → 가수분해 → 탈카복실화)</b> + <b>고리 닫기 복분해(RCM)</b>.</p>
<p>① diethyl malonate의 CH<sub>2</sub>(p<i>K</i><sub>a</sub> ≈ 13)는 EtO<sup>−</sup>로 완전히 엔올레이트가 되며, 알릴 브로마이드(활성화된 1차 할라이드)에 S<sub>N</sub>2 → 모노알릴 말로네이트. 남은 α-H 한 개도 여전히 산성이므로 NaOEt/알릴 브로마이드를 한 번 더 반복하면 4차 탄소의 다이알릴 말로네이트 A(C<sub>13</sub>H<sub>20</sub>O<sub>4</sub>)가 된다. 염기로 NaOEt를 쓰는 것은 에스터 교환으로 섞인 에스터가 생기는 것을 막기 위해서이다.</p>
<p>② Grubbs 촉매(Ru 카벤)는 [2+2] 고리 첨가/역고리 첨가(메탈라사이클로뷰테인)를 반복하여 두 말단 알켄을 연결한다. 분자 내 반응으로 5원 고리 알켄 B가 생기고 CH<sub>2</sub>=CH<sub>2</sub>가 기체로 빠져나가 평형이 생성물 쪽으로 이동한다(엔트로피 + Le Chatelier). B의 분자식 C<sub>11</sub>H<sub>16</sub>O<sub>4</sub> = A − C<sub>2</sub>H<sub>4</sub>로 확인된다.</p>
<p>③ KOH로 두 에스터를 비누화하고 산성화하면 cyclopent-3-ene-1,1-dicarboxylic acid(C<sub>7</sub>H<sub>8</sub>O<sub>4</sub>)가 된다. 같은 탄소에 COOH가 두 개 있는 말론산(β-다이카복실산)은 6원 고리 전이 상태를 통해 가열만으로 CO<sub>2</sub>를 잃어 엔올을 주고, 이것이 토토머화하여 C(C<sub>6</sub>H<sub>8</sub>O<sub>2</sub>)가 된다. 고리 안의 C=C는 이 과정에서 변하지 않는다.</p>
<p>④ <b>흔한 오답</b>: (가) RCM 생성물을 6원 고리로 그리는 것 — 두 알릴의 내부 탄소 사이에 새 C=C가 생기므로 고리 원자는 C1, CH<sub>2</sub>, CH=, =CH, CH<sub>2</sub>의 5개이다. (나) 탈카복실화를 음이온 메커니즘(카복실레이트에서 CO<sub>2</sub> 이탈)으로 그리는 것 — 산성 조건에서는 고리형 협동 메커니즘이며 엔올 중간체를 반드시 거친다. (다) C에서 알켄이 짝지음 위치(C1=C2)로 이동했다고 보는 것 — 산 촉매 토토머화는 C1에만 양성자를 주므로 고리 C=C 위치는 보존된다.</p>''',
),
# ─────────────────────────────────────────────────────────────── 2024B-7
dict(
    key='2024B-7',
    src='2024학년도 B형 7번',
    src_topic='cyclopentanone → Grignard/탈수 → 오존 분해 → 분자 내 알돌 축합 vs α-브로민화–탈리로 2-cyclohexenone 합성',
    change='CH₃MgBr 대신 EtMgBr를 써서 케토알데하이드의 알돌 위치 선택성(6원 고리만 가능한 경로 판별)을 요구하고, '
           '두 번째 경로는 비대칭 케톤(2-methylcyclohexanone)의 산 촉매 α-브로민화 위치 선택성(더 치환된 엔올)까지 묻도록 변형.',
    paper=dict(cite='J. Org. Chem. 2003, 68, 6455–6458', book='Klein 20.87',
               what='고리 케톤에 Grignard 첨가 → H₂SO₄ 가열 탈수 → 오존 분해로 곁사슬 카보닐을 도입하는 서열의 화학선택성 분석 — 본 문항 1·2단계의 모델'),
    nobel='',
    body=f'''다음은 cyclopentanone으로부터 중간 주생성물 {A_}(C<sub>7</sub>H<sub>12</sub>)와 {B_}(C<sub>7</sub>H<sub>12</sub>O<sub>2</sub>)를 거쳐 최종 주생성물 {C_}(C<sub>7</sub>H<sub>10</sub>O)를 합성하는 반응과, 고리 화합물 {D_}(C<sub>7</sub>H<sub>12</sub>O)로부터 2단계로 {C_}를 합성하는 반응을 나타낸 것이다. {NOTE}
{frame(rows(
    scheme(M('O=C1CCCC1', scale=15), arrow('1) CH<sub>3</sub>CH<sub>2</sub>MgBr', '2) H<sub>2</sub>SO<sub>4</sub>, 가열'), L('A'),
           arrow('1) O<sub>3</sub>', '2) Zn, H<sub>3</sub>O<sup>+</sup>'), L('B')),
    scheme(L('B'), arrow('NaOH, H<sub>2</sub>O', '가열'), L('C')),
    scheme(L('D'), arrow('1) Br<sub>2</sub>, CH<sub>3</sub>COOH', '2) Li<sub>2</sub>CO<sub>3</sub>, LiBr, DMF, 가열'), L('C'))))}
<p class="ask">{A_}, {C_}, {D_}의 구조를 각각 그리시오. 또한, {B_}가 {C_}로 전환되는 과정에서 생성되는 중간체(C<sub>7</sub>H<sub>12</sub>O<sub>2</sub>)의 구조를 그리고, {D_}에서 Br이 도입되는 탄소의 위치를 그 이유와 함께 서술하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CCC1=CCCC1', 'A', 15)}{M('CC1=CCCCC1=O', 'C', 15)}{M('CC1CCCCC1=O', 'D', 15)}{M('CC1C(O)CCCC1=O', '중간체', 15)}</div>
A = 1-ethylcyclopentene, (B = 5-oxoheptanal), C = 2-methylcyclohex-2-en-1-one, D = 2-methylcyclohexan-1-one, 중간체 = 3-hydroxy-2-methylcyclohexan-1-one.<br>
Br 위치: 메틸이 붙은 C2(더 치환된 α-탄소). 산 촉매 할로젠화는 엔올을 거치며, 더 치환된(사치환) C1=C2 엔올이 열역학적으로 더 안정하여 주로 생성되므로 Br<sub>2</sub>가 C2를 공격한다 → 2-bromo-2-methylcyclohexanone → 염기에 의한 E2(C3–H 제거)로 짝지어진 엔온 C.''',
    explain=f'''<p>핵심 반응: <b>분자 내 알돌 축합(고리 크기 선택)</b>과 <b>산 촉매 α-할로젠화–탈할로젠화수소</b>.</p>
<p>① EtMgBr 첨가 → 1-ethylcyclopentanol(3차 알코올). H<sub>2</sub>SO<sub>4</sub>/가열에서 E1 탈수: 고리 안 삼치환 알켄 A(1-ethylcyclopentene)가 주생성물이다(5원 고리에서는 고리 내 이중 결합이 고리 밖 ethylidene보다 안정). 고리 밖 알켄이었다면 오존 분해로 cyclopentanone + CH<sub>3</sub>CHO가 생겨 B의 분자식(C<sub>7</sub>H<sub>12</sub>O<sub>2</sub>)과 맞지 않는다.</p>
<p>② 환원성 오존 분해는 고리를 열어 C1→케톤(에틸 케톤), C2→알데하이드인 B = CH<sub>3</sub>CH<sub>2</sub>C(O)CH<sub>2</sub>CH<sub>2</sub>CH<sub>2</sub>CHO(5-oxoheptanal)를 준다.</p>
<p>③ B의 α-탄소는 C2(알데하이드 α), C4·C6(케톤 α) 세 곳이다. C2→C5 공격과 C4→C1 공격은 4원 고리, <b>C6(에틸의 CH<sub>2</sub>) 엔올레이트 → C1 알데하이드</b> 공격만 6원 고리를 만든다. 알데하이드는 케톤보다 친전자성이 커서 이 경로가 빠르다. 알콕사이드가 양성자화되어 β-하이드록시 케톤(3-hydroxy-2-methylcyclohexanone, C<sub>7</sub>H<sub>12</sub>O<sub>2</sub>)이 되고, 가열 시 E1cB(엔올레이트 형성 후 OH<sup>−</sup> 이탈)로 탈수되어 C(2-methylcyclohex-2-enone)가 된다.</p>
<p>④ D 경로: 산 촉매 할로젠화의 속도 결정 단계는 엔올 형성이며, 더 치환된 엔올이 주로 생기므로 Br은 C2(3차 α-탄소)에 들어간다(염기성 조건/LDA의 덜 치환된 쪽 선택과 대비). Li<sub>2</sub>CO<sub>3</sub>/LiBr, DMF는 약하고 비친핵성인 염기 조건으로 C3–H를 제거하는 E2를 일으켜 짝지어진 엔온을 준다. 고리 밖 메틸의 H를 떼면 2-methylenecyclohexanone(이치환, 덜 안정)이 되므로 부생성물이다.</p>
<p>⑤ <b>흔한 오답</b>: C를 3-methylcyclohex-2-enone(원 기출의 답과 혼동)이나 1-acetylcyclopentene(5원 고리)으로 그리는 것 — 원자 번호를 따라가면 CH<sub>3</sub>는 C2, 즉 카보닐 옆 알켄 탄소에 위치한다. D를 3-methylcyclohexanone으로 쓰면 브로민화가 C2/C6에서 섞여 C가 단일하게 나오지 않는다.</p>''',
),
# ─────────────────────────────────────────────────────────────── 2023B-7
dict(
    key='2023B-7',
    src='2023학년도 B형 7번',
    src_topic='ethyl acetate의 Claisen 축합으로 acetoacetate를 얻고, Michael–알돌 고리화·케탈 보호–Grignard에 활용; 1,3-다이카보닐 음이온 공명',
    change='Claisen 축합 생성물(ethyl acetoacetate)의 활용을 Knoevenagel 축합–락톤화(쿠마린 형광 염료 합성)와 아세토아세트산 에스터 합성(알킬화–가수분해–탈카복실화)으로 바꾸어, '
           '같은 1,3-다이카보닐 화합물의 두 가지 친핵성 반응을 비교하도록 변형. 음이온 공명 구조 요구는 유지.',
    paper=dict(cite='J. Chem. Ed. 2006, 83, 287–289', book='Klein 2.74',
               what='4-(diethylamino)salicylaldehyde와 ethyl acetoacetate의 piperidine 촉매 Knoevenagel 축합–고리화로 3-acetyl-7-(diethylamino)coumarin 합성(IR로 확인)'),
    nobel='2021 노벨 화학상(B. List·D. W. C. MacMillan) — piperidine의 이미늄 형성에 의한 Knoevenagel 축합은 아민 유기촉매(이미늄/엔아민 촉매)의 원형으로 꼽힌다.',
    body=f'''다음은 {A_}(C<sub>4</sub>H<sub>8</sub>O<sub>2</sub>)의 클라이젠 축합 반응(Claisen condensation)으로 얻은 {B_}로부터 최종 주생성물 {D_}(C<sub>15</sub>H<sub>17</sub>NO<sub>3</sub>)와 {E_}(C<sub>10</sub>H<sub>12</sub>O)를 각각 합성하는 반응을 나타낸 것이다. {D_}는 고리 화합물이다. {NOTE}
{frame(rows(
    scheme(L('A'), arrow('1) NaOEt, EtOH', '2) H<sub>3</sub>O<sup>+</sup>'), M('CCOC(=O)CC(C)=O', 'B', 15)),
    scheme(L('B'), plus(), M('CCN(CC)c1ccc(C=O)c(O)c1', scale=14), arrow('piperidine (촉매량)', 'EtOH, 가열'), L('D')),
    scheme(L('B'), arrow('1) NaOEt 2) PhCH<sub>2</sub>Br', '3) NaOH(aq) 4) H<sub>3</sub>O<sup>+</sup>, 가열'), L('E'))))}
<p class="ask">{A_}, {D_}, {E_}의 구조를 각각 그리시오. 또한, {B_}와 NaOEt가 같은 당량으로 반응할 때 생성되는 가장 안정한 음이온의 공명 구조를 모두 그리고, 클라이젠 축합에서 염기를 1당량 이상 사용해야 하는 이유를 이 음이온과 관련지어 서술하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CCOC(C)=O', 'A', 15)}{M('CCN(CC)c1ccc2cc(C(C)=O)c(=O)oc2c1', 'D', 14)}{M('CC(=O)CCc1ccccc1', 'E', 15)}</div>
<div class="ansbox">{M('CCOC(=O)[CH-]C(C)=O', '', 14)}<span class="chem">↔</span>{M('CCOC(=O)C=C(C)[O-]', '', 14)}<span class="chem">↔</span>{M('CCOC([O-])=CC(C)=O', '', 14)}</div>
A = ethyl acetate, D = 3-acetyl-7-(diethylamino)-2<i>H</i>-chromen-2-one(쿠마린), E = 4-phenylbutan-2-one.<br>
이유: Claisen 축합의 첨가–제거 단계는 모두 가역적이고 평형이 불리하다(에스터 엔올레이트 + 에스터 → β-케토 에스터 + EtO<sup>−</sup>). 생성된 β-케토 에스터의 C2–H(p<i>K</i><sub>a</sub> ≈ 11)는 EtOH(p<i>K</i><sub>a</sub> ≈ 16)보다 훨씬 산성이므로 EtO<sup>−</sup>가 이를 비가역적으로 떼어 위의 공명 안정화 음이온을 만든다. 이 마지막 산–염기 단계가 평형을 생성물 쪽으로 끌어당기므로 염기가 1당량 이상 소모되며, 반응 후 H<sub>3</sub>O<sup>+</sup>로 중화해야 B를 얻는다.''',
    explain=f'''<p>핵심 반응: <b>Claisen 축합</b>, <b>Knoevenagel 축합</b>, <b>아세토아세트산 에스터 합성</b>.</p>
<p>① A(C<sub>4</sub>H<sub>8</sub>O<sub>2</sub>) = CH<sub>3</sub>CO<sub>2</sub>Et. EtO<sup>−</sup>가 α-H를 떼어 에스터 엔올레이트 → 다른 에스터 C=O에 친핵성 아실 치환(사면체 중간체 → EtO<sup>−</sup> 이탈) → ethyl acetoacetate B. 생성물의 탈양성자화가 구동력이다(정답 참조).</p>
<p>② B의 음이온은 C2 탄소 음이온, 케톤 산소 엔올레이트, 에스터 산소 엔올레이트의 세 공명 구조로 비편재화된다. 음전하가 전기음성도가 큰 산소에 있는 두 구조(특히 케톤 O<sup>−</sup>)의 기여가 크다. 말단 CH<sub>3</sub>나 OCH<sub>2</sub>의 H를 뗀 음이온은 한 카보닐에만 비편재화되어 덜 안정하다.</p>
<p>③ D(Knoevenagel–락톤화): piperidine이 알데하이드와 <b>이미늄 이온</b>을 만들어 친전자성을 높이고, 동시에 B의 활성 메틸렌을 탈양성자화한다. B의 엔올(레이트)이 이미늄 탄소를 공격 → 아민 제거(E1cB) → 벤질리덴 아세토아세테이트(C=C 형성). 이어 오쏘 위치의 페놀 OH가 에스터 C=O를 분자 내 공격(에스터 교환)하여 EtOH를 내보내고 6원 고리 락톤(쿠마린)이 닫힌다. 분자식 확인: C<sub>11</sub>H<sub>15</sub>NO<sub>2</sub> + C<sub>6</sub>H<sub>10</sub>O<sub>3</sub> − H<sub>2</sub>O − C<sub>2</sub>H<sub>5</sub>OH = C<sub>15</sub>H<sub>17</sub>NO<sub>3</sub>. 논문에서는 IR에서 페놀 O–H, 알데하이드 C–H(2720/2820 cm<sup>−1</sup>) 띠가 사라지고 락톤 C=O(≈1720 cm<sup>−1</sup>)가 나타나는 것으로 확인한다. 7-다이에틸아미노기(주개)와 3-아세틸(받개)의 push–pull 구조로 강한 형광을 낸다.</p>
<p>④ E(아세토아세트산 에스터 합성): NaOEt로 만든 엔올레이트가 PhCH<sub>2</sub>Br에 S<sub>N</sub>2 → ethyl 2-benzylacetoacetate → NaOH 비누화 → 산성화하여 β-케토산 → 가열 시 6원 고리 전이 상태로 탈카복실화 → 엔올 → 토토머화 → PhCH<sub>2</sub>CH<sub>2</sub>COCH<sub>3</sub>(C<sub>10</sub>H<sub>12</sub>O). 즉 B는 “CH<sub>3</sub>COCH<sub>2</sub><sup>−</sup>” 등가체이다.</p>
<p>⑤ <b>흔한 오답</b>: D를 락톤화 전의 Knoevenagel 생성물(C<sub>17</sub>H<sub>23</sub>NO<sub>4</sub>)로 그리는 것(분자식 불일치), E를 4-phenylbutanoic acid(말론산 에스터 합성과 혼동)나 탈카복실화 전의 β-케토산으로 그리는 것, 음이온 공명 구조에서 에스터 쪽 O<sup>−</sup> 구조를 빠뜨리는 것.</p>''',
),
# ─────────────────────────────────────────────────────────────── 2023A-10
dict(
    key='2023A-10',
    src='2023학년도 A형 10번',
    src_topic='2,6-octanedione의 분자 내 알돌(구조 이성질체 B/C, 열역학 조절), LDA 동역학적 엔올레이트 + MVK Robinson 고리화',
    change='1,5-다이케톤(6원 고리) 대신 1,4-다이케톤(5원 고리, 논문의 fulvene 전구체 합성 단계)을 쓰고, 한쪽 α-탄소를 벤질 위치로 바꾸어 '
           '알돌 위치 선택성을 공액·치환도로 판단하게 하였다. 마지막 단계는 엔온의 동역학적 α′-탈양성자화(LDA)와 알킬화로 바꾸어 γ-탈양성자화(확장 엔올레이트)와 대비시켰다.',
    paper=dict(cite='J. Org. Chem. 2012, 77, 6371–6376', book='Klein 22.112',
               what='1-phenylpentane-1,4-dione의 NaOH 분자 내 알돌 축합으로 3-phenylcyclopent-2-enone을 얻고 Grignard·탈수로 fulvene 전구체 합성 — 1,4-다이케톤 고리화를 모델화'),
    nobel='',
    body=f'''다음은 1-phenylhexane-2,5-dione({A_})으로부터 서로 구조 이성질체 관계인 {B_}와 {C_}(C<sub>12</sub>H<sub>12</sub>O)가 생성되는 반응과, 주생성물 {B_}로부터 최종 주생성물 {D_}(C<sub>15</sub>H<sub>16</sub>O)를 합성하는 반응이다. 또한 {C_}의 <sup>1</sup>H NMR 자료를 나타낸 것이다. {NOTE}
{frame(rows(
    scheme(M('CC(=O)CCC(=O)Cc1ccccc1', 'A', 15), arrow('NaOH, H<sub>2</sub>O', 'EtOH, 가열'), L('B'), plus(), L('C')),
    scheme(L('B'), arrow('1) LDA, THF, −78 ℃', '2) CH<sub>2</sub>=CHCH<sub>2</sub>Br'), L('D'))),
    '<div class="chem" style="text-align:center">LDA = [(CH<sub>3</sub>)<sub>2</sub>CH]<sub>2</sub>N<sup>−</sup>Li<sup>+</sup></div>',
    '<div class="chem" style="text-align:center"><b>C</b>의 <sup>1</sup>H NMR 자료(300 MHz, CDCl<sub>3</sub>)</div>',
    '<table class="data"><tr><th>δ (ppm)</th><td>7.15–7.40</td><td>5.92</td><td>3.68</td><td>2.48–2.56</td><td>2.36–2.44</td></tr>'
    '<tr><th>다중도(적분)</th><td>m (5H)</td><td>s (1H)</td><td>s (2H)</td><td>m (2H)</td><td>m (2H)</td></tr></table>')}
<p class="ask">{A_}로부터 {B_}가 생성되는 반응 메커니즘을 굽은 화살표를 사용하여 제시하고 {C_}의 구조를 그리시오. 또한, {B_}와 {C_} 중에서 {B_}가 주생성물인 이유를 서술하고, {D_}의 구조를 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CC1=C(c2ccccc2)C(=O)CC1', 'B', 15)}{M('O=C1C=C(Cc2ccccc2)CC1', 'C', 15)}{M('C=CCC1CC(C)=C(c2ccccc2)C1=O', 'D', 15)}</div>
B = 3-methyl-2-phenylcyclopent-2-en-1-one, C = 3-benzylcyclopent-2-en-1-one, D = 5-allyl-3-methyl-2-phenylcyclopent-2-en-1-one(라셈).<br>
메커니즘(A→B): ① OH<sup>−</sup>가 C1(PhCH<sub>2</sub>, C2=O의 α이며 벤질 위치)의 H를 떼어 엔올레이트 형성 → ② 엔올레이트 C1이 C5 카보닐 탄소를 공격하여 5원 고리 알콕사이드 → ③ H<sub>2</sub>O가 양성자를 주어 β-하이드록시 케톤(3-hydroxy-3-methyl-2-phenylcyclopentanone) → ④ OH<sup>−</sup>가 C1–H(이제 고리의 C2–H)를 다시 떼어 엔올레이트 → ⑤ E1cB로 OH<sup>−</sup>가 떨어지며 C=C 형성 → B.<br>
이유: NaOH/가열 조건에서 알돌 첨가와 탈수는 가역적이어서 열역학적으로 더 안정한 엔온이 쌓인다. B의 C=C는 사치환이고 C=O뿐 아니라 페닐 고리와도 짝지어져 있어, 삼치환이며 페닐과 짝지어지지 않은 C보다 안정하다(또한 벤질 위치 α-H가 더 산성이어서 B로 가는 엔올레이트가 더 쉽게 생긴다).''',
    explain=f'''<p>핵심 반응: <b>분자 내 알돌 축합(위치 선택성, 열역학 조절)</b>과 <b>LDA에 의한 동역학적 엔올레이트 알킬화</b>.</p>
<p>① A = PhCH<sub>2</sub>–C(O)–CH<sub>2</sub>CH<sub>2</sub>–C(O)–CH<sub>3</sub> (C1~C6). α-탄소는 C1, C3, C4, C6이다. 5원 고리를 만드는 경로는 두 가지뿐이다: (가) C1 엔올레이트 → C5 공격 → B, (나) C6(CH<sub>3</sub>) 엔올레이트 → C2 공격 → C. C3→C5, C4→C2 공격은 3원 고리라 불가능하다.</p>
<p>② C의 NMR: δ 5.92(s, 1H)는 엔온의 비닐 H(C2–H, 이웃 H 없음), 3.68(s, 2H)는 이웃 H가 없는 PhC<u>H<sub>2</sub></u>–C=, 2.4–2.6의 두 m(각 2H)은 고리의 C4·C5 CH<sub>2</sub>, 7.15–7.40(5H)은 일치환 벤젠이다. 이는 3-benzylcyclopent-2-enone과 일치한다. B였다면 비닐 H가 없고 δ ≈ 2.1의 CH<sub>3</sub> 단일선이 보여야 한다.</p>
<p>③ 주생성물 판단: 알돌은 가역적이며 가열·수산화 나트륨 조건은 열역학 조절이다(원 기출 2,3-dimethylcyclohex-2-enone과 같은 논리). B는 (i) 이중 결합의 치환도가 더 높고(사치환 > 삼치환), (ii) 페닐–C=C–C=O의 확장된 짝지음을 가진다. 논문(1-phenylpentane-1,4-dione → 3-phenylcyclopent-2-enone)에서도 아릴과 짝지어진 사이클로펜텐온이 얻어진다.</p>
<p>④ D: LDA(부피 큰 강염기, −78 ℃, 비가역)는 엔온에서 카보닐 바로 옆 α′-탄소(C5)의 H를 가장 빨리 뗀다(동역학적 엔올레이트, Li<sup>+</sup>가 카보닐 O에 배위한 상태에서 가까운 H 제거). 열역학적 조건(예: NaOEt, 실온)에서는 γ-H(C4 또는 3-CH<sub>3</sub>) 제거로 더 비편재화된 확장(다이엔) 엔올레이트가 생겨 α-알킬화(탈짝지음 생성물)가 섞일 수 있다. 엔올레이트 C5가 알릴 브로마이드에 S<sub>N</sub>2하여 D(C<sub>15</sub>H<sub>16</sub>O)가 된다. C5는 새 입체 중심이지만 비카이랄 조건이므로 라셈체이다.</p>
<p>⑤ <b>흔한 오답</b>: B를 2-benzyl… 또는 3-phenyl…로 잘못 번호 매기는 것, D에서 알릴이 C4(γ)나 메틸에 붙는다고 보는 것, B가 “동역학적 생성물”이라고만 쓰는 것(가역 반응이므로 근거는 열역학적 안정성).</p>''',
),
# ─────────────────────────────────────────────────────────────── 2022B-9
dict(
    key='2022B-9',
    src='2022학년도 B형 9번',
    src_topic='ethyl prolinate의 aza-Michael → Dieckmann 축합 → 가수분해·탈카복실화로 pyrrolizidinone; Dieckmann 메커니즘',
    change='aza-Michael 대신 아민의 N-아실화(ethyl malonyl chloride)로 다이에스터를 만들고, Dieckmann 고리화로 천연물(equisetin·fusarisetin·tenuazonic acid)의 핵심 골격인 '
           'tetramic acid(pyrrolidine-2,4-dione)를 만드는 경로로 변형. 두 가지 가능한 엔올레이트 중 어느 것이 반응하는지(산도 비교)와 생성물 탈양성자화의 구동력을 함께 묻는다.',
    paper=dict(cite='J. Am. Chem. Soc. 2012, 134, 920–923', book='Klein 22.118',
               what='fusarisetin A 합성에서 β-케토 아마이드의 엔올레이트가 N-methylserine 메틸 에스터를 공격하는 NaOMe Dieckmann 고리화로 tetramic acid 고리 형성 — 단순 모델(sarcosine 유도체)로 바꿈'),
    nobel='',
    body=f'''다음은 sarcosine ethyl ester(<i>N</i>-methylglycine ethyl ester)로부터 중간 주생성물 {A_}(C<sub>10</sub>H<sub>17</sub>NO<sub>5</sub>)와 {B_}(C<sub>8</sub>H<sub>11</sub>NO<sub>4</sub>)를 거쳐 최종 주생성물 {C_}(C<sub>5</sub>H<sub>7</sub>NO<sub>2</sub>)를 합성하는 반응을 나타낸 것이다. {B_}와 {C_}는 오각 고리 화합물이다. {NOTE}
{frame(rows(
    scheme(M('CNCC(=O)OCC', scale=15), arrow('ClC(O)CH<sub>2</sub>CO<sub>2</sub>Et', 'Et<sub>3</sub>N, CH<sub>2</sub>Cl<sub>2</sub>'), L('A')),
    scheme(L('A'), arrow('1) NaOEt, EtOH', '2) H<sub>3</sub>O<sup>+</sup>'), L('B'), arrow('1) NaOH(aq)', '2) H<sub>3</sub>O<sup>+</sup>, 가열'), L('C'))))}
<p class="ask">{A_}, {B_}, {C_}의 구조를 각각 그리시오. 또한, 굽은 화살표를 사용하여 {A_}로부터 {B_}가 생성되는 반응 메커니즘을 제시하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CCOC(=O)CC(=O)N(C)CC(=O)OCC', 'A', 13)}{M('CCOC(=O)C1C(=O)CN(C)C1=O', 'B', 14)}{M('CN1CC(=O)CC1=O', 'C', 15)}</div>
A = ethyl <i>N</i>-(3-ethoxy-3-oxopropanoyl)-<i>N</i>-methylglycinate, B = ethyl 1-methyl-2,4-dioxopyrrolidine-3-carboxylate, C = 1-methylpyrrolidine-2,4-dione(<i>N</i>-methyltetramic acid).<br>
메커니즘: ① EtO<sup>−</sup>가 말로닐 CH<sub>2</sub>(아마이드 C=O와 에스터 C=O 사이)의 H를 떼어 엔올레이트 형성 → ② 엔올레이트 탄소가 글리신 쪽 에스터 C=O를 분자 내 공격(5원 고리) → 사면체 알콕사이드 중간체 → ③ C=O가 다시 형성되며 EtO<sup>−</sup> 이탈 → B(케토 형) → ④ 세 카보닐 사이의 C3–H가 EtO<sup>−</sup>에 의해 제거되어 안정한 음이온(비가역, 구동력) → ⑤ H<sub>3</sub>O<sup>+</sup> 처리로 양성자화되어 B.''',
    explain=f'''<p>핵심 반응: <b>Dieckmann 축합(분자 내 Claisen)</b>과 <b>β-케토 에스터의 가수분해·탈카복실화</b>.</p>
<p>① A: 2차 아민(sarcosine)이 산 염화물(ethyl malonyl chloride)에 친핵성 아실 치환하여 3차 아마이드 A를 만든다(Et<sub>3</sub>N은 HCl 제거). A는 에스터 두 개를 가진 다이에스터이다.</p>
<p>② 엔올레이트 선택: A에서 탈양성자화될 수 있는 α-탄소는 (가) 말로닐 CH<sub>2</sub>(두 카보닐 사이, p<i>K</i><sub>a</sub> ≈ 13)와 (나) 글리신 CH<sub>2</sub>(에스터 하나의 α, p<i>K</i><sub>a</sub> ≈ 25)이다. EtO<sup>−</sup>는 (가)를 거의 정량적으로 엔올레이트로 만든다. (가) 탄소가 글리신 에스터를 공격하면 C3–C4 결합이 생기며 5원 고리(N1, C2=O, C3, C4=O, C5) — pyrrolidine-2,4-dione이 된다. (나)가 말로닐 에스터를 공격하는 경로(3,5-dioxopyrrolidine-2-carboxylate)는 훨씬 적은 엔올레이트에서 출발하므로 무시된다.</p>
<p>③ 구동력: 생성된 B의 C3–H는 세 개의 카보닐(아마이드, 케톤, 에스터)에 둘러싸여 매우 산성이므로 EtO<sup>−</sup>가 즉시 떼어 낸다. 이 비가역적 산–염기 반응이 가역적인 Claisen 단계의 평형을 끌어당긴다(원 기출에서 β-케토 에스터 α-H 제거가 구동력인 것과 같다). 따라서 반응 후 반드시 산 처리가 필요하다.</p>
<p>④ C: NaOH로 에스터를 비누화 → 산성화하면 β-케토산(3-카복실산) → 가열 시 6원 고리 전이 상태로 CO<sub>2</sub>를 잃고 엔올 → 토토머화 → 1-methylpyrrolidine-2,4-dione(C<sub>5</sub>H<sub>7</sub>NO<sub>2</sub>). 이 tetramic acid는 CDCl<sub>3</sub>에서는 주로 다이케토 형이지만 C3–H가 산성(p<i>K</i><sub>a</sub> ≈ 6)이어서 극성 용매에서는 4-하이드록시-3-피롤린-2-온(엔올) 형도 존재한다. 3-아실 유도체가 equisetin, tenuazonic acid 같은 천연물의 골격이며, 논문(fusarisetin A)도 같은 Dieckmann으로 이 고리를 만든다.</p>
<p>⑤ <b>흔한 오답</b>: 아마이드 C=O를 친전자체로 보아 고리를 그리는 것(아마이드는 에스터보다 훨씬 약한 친전자체이고 아민 음이온은 이탈기가 되지 못한다), B를 6원 고리로 그리는 것, C에서 고리 N–C(=O) 아마이드까지 가수분해된다고 보는 것.</p>''',
),
# ─────────────────────────────────────────────────────────────── 2022A-9
dict(
    key='2022A-9',
    src='2022학년도 A형 9번',
    src_topic='엔아민 형성의 위치 선택성(짝지음), Stork 엔아민 알킬화, FC 아실화 고리화로 2-tetralone, 환원성 아민화',
    change='엔아민 위치 선택성을 짝지음이 아닌 A(1,3) 변형(알릴 변형)으로 판단하게 하여(2-methylcyclohexanone: 엔아민은 덜 치환된 쪽, 엔올레이트(열역학)는 더 치환된 쪽) '
           '“엔아민 경로 vs 염기 경로”로 서로 구조 이성질체인 Robinson 고리화 생성물이 얻어짐을 묻도록 변형. Stork 엔아민 Michael 첨가 → 분자 내 알돌이 핵심.',
    paper=dict(cite='J. Am. Chem. Soc. 1954, 76, 2029–2030', book='Klein 22.110',
               what='Stork 엔아민 반응: cyclohexanone의 pyrrolidine 엔아민이 탄소 친핵체로 알킬화·Michael 첨가된 뒤 가수분해되어 α-치환 케톤을 준다'),
    nobel='2021 노벨 화학상(B. List·D. W. C. MacMillan) — Stork 엔아민의 화학량론적 반응을 2차 아민(프롤린 등) 촉매 엔아민 반응으로 확장한 것이 유기촉매의 한 축이다.',
    body=f'''다음은 2-methylcyclohexanone의 반응을 나타낸 것이다. (단, 각 반응에서는 적절한 분리·정제 과정을 수행하였고, 입체 이성질체는 고려하지 않는다.)
{frame(
    '<div class="chem"><b>[반응 1]</b></div>',
    scheme(M('CC1CCCCC1=O', scale=15), arrow('pyrrolidine, TsOH(촉매량)', '벤젠, 가열(−H<sub>2</sub>O)'),
           M('CC1CCCC=C1N1CCCC1', 'A', 14), M('CC1=C(N2CCCC2)CCCC1', 'B', 14)),
    '<div class="chem"><b>[반응 2]</b></div>',
    scheme(L('A'), arrow('1) CH<sub>2</sub>=CHCOCH<sub>3</sub>, 다이옥세인', '2) H<sub>3</sub>O<sup>+</sup>'), L('C'),
           arrow('KOH, MeOH', '가열'), L('D')),
    '<div class="chem"><b>[반응 3]</b></div>',
    scheme(M('CC1CCCCC1=O', scale=15), arrow('1) NaOEt, EtOH, CH<sub>2</sub>=CHCOCH<sub>3</sub>', '2) KOH, 가열'), L('E')))}
<p class="ask">[반응 1]에서 {A_}와 {B_} 중 주생성물을 쓰고 그 이유를 서술하시오. 또한, [반응 2]에서 중간 주생성물 {C_}(C<sub>11</sub>H<sub>18</sub>O<sub>2</sub>)와 최종 주생성물 {D_}(C<sub>11</sub>H<sub>16</sub>O), [반응 3]의 최종 주생성물 {E_}(C<sub>11</sub>H<sub>16</sub>O)의 구조를 각각 그리시오. [[PTS]]</p>''',
    answer=f'''주생성물: <b>A</b>(덜 치환된 엔아민).<br>
이유: 엔아민에서는 N의 비공유 전자쌍이 C=C와 짝지어지기 위해 N이 sp<sup>2</sup>가 되고 피롤리딘 고리가 C=C와 같은 평면에 놓인다. B처럼 메틸이 붙은 탄소에 이중 결합이 생기면 메틸과 피롤리딘 α-CH<sub>2</sub>가 같은 평면에서 심하게 부딪친다(A<sup>1,3</sup> 변형). A에서는 메틸이 sp<sup>3</sup> 탄소에 있으며 축 방향으로 놓여 이 반발을 피하므로, 이중 결합이 덜 치환된 쪽에 생긴 A가 더 안정하다.
<div class="ansbox">{M('CC(=O)CCC1CCCC(C)C1=O', 'C', 14)}{M('CC1CCCC2CCC(=O)C=C12', 'D', 15)}{M('CC12CCCCC1=CC(=O)CC2', 'E', 15)}</div>
C = 2-methyl-6-(3-oxobutyl)cyclohexan-1-one, D = 8-methyl-4,4a,5,6,7,8-hexahydronaphthalen-2(3<i>H</i>)-one, E = 4a-methyl-4,4a,5,6,7,8-hexahydronaphthalen-2(3<i>H</i>)-one.''',
    explain=f'''<p>핵심 반응: <b>Stork 엔아민 반응(Michael 첨가)</b>과 <b>Robinson 고리화</b>, 그리고 <b>엔아민 vs 엔올레이트의 위치 선택성</b>.</p>
<p>① 엔아민 형성: 케톤 + 2차 아민 → 카비놀아민 → (H<sup>+</sup>, −H<sub>2</sub>O) 이미늄 → α-H 제거 → 엔아민. 2-methylcyclohexanone에서는 두 α-탄소 중 어느 쪽 H를 떼느냐에 따라 A(Δ<sup>1,6</sup>)와 B(Δ<sup>1,2</sup>)가 생기고, 산 촉매 조건에서 서로 평형을 이룬다. 엔올(레이트)이라면 더 치환된 B형이 열역학적으로 유리하지만, 엔아민은 N-치환기와 C2-치환기 사이의 A<sup>1,3</sup> 변형 때문에 A가 주생성물(약 9:1)이 된다. 이것이 Stork 엔아민 반응이 비대칭 케톤의 <u>덜 치환된</u> α-탄소에서 일어나는 이유이다.</p>
<p>② [반응 2] Stork Michael 첨가: A의 β-탄소(C6)가 MVK의 β-탄소에 1,4-첨가 → 이미늄/엔올레이트 → 양성자 이동 → 가수분해(H<sub>3</sub>O<sup>+</sup>)로 피롤리딘이 떨어지고 1,5-다이케톤 C(2,6-이치환)가 된다. 엔아민은 중성 친핵체여서 MVK의 중합이나 다중 알킬화가 적다.</p>
<p>③ C → D(분자 내 알돌 축합): KOH가 곁사슬 메틸 케톤의 CH<sub>3</sub>를 탈양성자화 → 고리 C=O(C1) 공격(6원 고리) → β-하이드록시 케톤 → E1cB 탈수 → 짝지어진 엔온 D. 메틸은 고리 접합 sp<sup>2</sup> 탄소(C8a) 옆 C8에 놓인다. (곁사슬 안쪽 CH<sub>2</sub>가 공격하면 4원 고리, 고리 C2′가 곁사슬 C=O를 공격하면 다리걸친 고리가 되어 탈수로 짝지어진 엔온을 만들 수 없으므로 가역 조건에서 D로 수렴한다.)</p>
<p>④ [반응 3]: NaOEt 조건(열역학적 엔올레이트)에서는 더 치환된 C2 엔올레이트가 MVK에 Michael 첨가하여 4차 탄소가 생기고, 이어 Robinson 고리화하면 각진(angular) 메틸을 가진 E가 된다. D와 E는 서로 구조 이성질체(C<sub>11</sub>H<sub>16</sub>O)이며, <b>같은 출발 물질에서 엔아민 경로와 엔올레이트 경로가 상보적인 위치 선택성</b>을 보인다는 것이 이 문항의 요점이다.</p>
<p>⑤ <b>흔한 오답</b>: 원 기출의 “짝지음” 논리를 그대로 적용해 B를 고르는 것(여기에는 짝지을 방향족 고리가 없다), C를 2,2-이치환(4차 탄소) 다이케톤으로 그리는 것, D와 E를 같은 화합물로 그리는 것. 참고로 프롤린 같은 키랄 2차 아민을 쓰면 엔아민의 한쪽 면을 가려 거울상 선택적 반응이 가능하며(Klein 22.111, 22.116), 이것이 2021년 노벨상 주제인 엔아민 유기촉매로 이어진다.</p>''',
),
]
