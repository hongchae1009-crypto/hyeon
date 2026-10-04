"""영역 G: 작용기 변환·친핵성 반응 메커니즘 (9문항)."""
from chem import M, L, arrow, varrow, scheme, rows, frame, nmr, ir, spec, plus

Z_ACET = 'CC/C=C\\CCOC(C)=O'   # (Z)-3-hexenyl acetate
Z_OL = 'CC/C=C\\CCO'           # (Z)-hex-3-en-1-ol


def larrow(top='', bottom='', width=None):
    """왼쪽을 향하는 시약 화살표(글자는 정방향)."""
    a = arrow(top, bottom, width)
    return (a.replace('class="arr"', 'class="arr" style="transform:scaleX(-1)"', 1)
             .replace('<div class="rt">', '<div class="rt" style="transform:scaleX(-1)">')
             .replace('<div class="rb">', '<div class="rb" style="transform:scaleX(-1)">'))

ITEMS = [
# ---------------------------------------------------------------- 2026B-7
dict(
    key='2026B-7',
    src='2026학년도 B형 7번 유형',
    src_topic='acetophenone + HC≡CMgBr → 프로파질 알코올 → Hg²⁺ 촉매 알카인 수화 → 옥살산 에스터 축합·락톤화, 토토머',
    change='알카이닐 Grignard 첨가는 유지하되 1-propynyl Grignard로 내부 알카인을 만든 뒤, salvinorin A 합성에 쓰인 '
           'NaNH₂ 알카인 “지퍼(zipper)” 이성질화(알렌 경유)를 핵심으로 삼았다. 이어 말단 알카인의 anti-Markovnikov 수소붕소화–산화로 '
           'γ-하이드록시 알데하이드를 만들고, 분자 내 고리형 헤미아세탈(락톨)로 존재함을 IR 단서로 판단하게 하여 '
           '“알카인 작용기 변환 + 산·염기 평형 논리 + 카보닐 첨가”를 한 문항에서 묻도록 변형',
    paper=dict(cite='J. Am. Chem. Soc. 2007, 129, 8968–8969', book='Klein 10.71',
               what='salvinorin A 합성: 1-(furan-3-yl)but-2-yn-1-ol을 NaNH₂로 처리해 말단 알카인 1-(furan-3-yl)but-3-yn-1-ol로 이성질화'),
    nobel='1912 노벨 화학상(V. Grignard — Grignard 시약), 1979 노벨 화학상(H. C. Brown — 유기붕소 화합물·수소붕소화)',
    body=f'''다음은 3-furaldehyde로부터 중간 주생성물 <b class="lbltxt">A</b>(C<sub>8</sub>H<sub>8</sub>O<sub>2</sub>)와 <b class="lbltxt">B</b>(C<sub>8</sub>H<sub>8</sub>O<sub>2</sub>)를 거쳐 최종 주생성물 <b class="lbltxt">C</b>(C<sub>8</sub>H<sub>10</sub>O<sub>3</sub>)를 합성하는 반응을 나타낸 것이다. <b class="lbltxt">B</b>는 <b class="lbltxt">A</b>의 구조 이성질체이다. (단, 각 반응에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(scheme(M('O=Cc1ccoc1', scale=16), arrow('1) CH<sub>3</sub>C≡CMgBr', '2) H<sub>3</sub>O<sup>+</sup>'), L('A'),
              arrow('1) NaNH<sub>2</sub> (과량)', '2) H<sub>2</sub>O'), L('B')),
       scheme(L('B'), arrow('1) (Sia)<sub>2</sub>BH (과량)', '2) H<sub>2</sub>O<sub>2</sub>, NaOH'), L('C')),
       '<div class="chem" style="text-align:center">(Sia)<sub>2</sub>BH = disiamylborane</div>')}
<p>◦ <b class="lbltxt">B</b>의 IR 스펙트럼에는 3300 cm<sup>−1</sup> 부근의 날카로운 흡수와 2120 cm<sup>−1</sup> 부근의 약한 흡수가 있다.</p>
<p>◦ <b class="lbltxt">C</b>의 IR 스펙트럼에는 3400 cm<sup>−1</sup> 부근의 넓은 흡수가 있으나, 1700~1740 cm<sup>−1</sup> 영역의 강한 흡수는 거의 나타나지 않는다.</p>
<p class="ask"><b class="lbltxt">A</b>와 <b class="lbltxt">B</b>의 구조를 각각 그리고, <b class="lbltxt">A</b>가 <b class="lbltxt">B</b>로 전환되는 반응 메커니즘을 굽은 화살표를 사용하여 제시하시오(단, O–H의 탈양성자화와 재양성자화 과정은 생략한다). 또한 <b class="lbltxt">C</b>의 구조를 그리고, <b class="lbltxt">C</b>가 이 구조로 존재하는 이유를 서술하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CC#CC(O)c1ccoc1', 'A', 15)}{M('C#CCC(O)c1ccoc1', 'B', 15)}{M('OC1CCC(c2ccoc2)O1', 'C (락톨)', 15)}</div>
A = 1-(furan-3-yl)but-2-yn-1-ol, B = 1-(furan-3-yl)but-3-yn-1-ol, C = 5-(furan-3-yl)oxolan-2-ol(고리형 헤미아세탈; 아노머 혼합물).<br>
메커니즘: ① NH<sub>2</sub><sup>−</sup>가 C4–H(프로파질 CH<sub>3</sub>)를 떼어 프로파질/알레닐 음이온 → ② C2가 NH<sub>3</sub>에서 H<sup>+</sup>를 받아 알렌 {M('C=C=CC(O)c1ccoc1', '', 12)} → ③ NH<sub>2</sub><sup>−</sup>가 말단 =CH<sub>2</sub>의 H를 떼어 알레닐/프로파질 음이온 → ④ C2가 양성자화되어 말단 알카인 → ⑤ NH<sub>2</sub><sup>−</sup>가 ≡C–H를 비가역적으로 떼어 아세틸라이드 → H<sub>2</sub>O 처리로 B.<br>
C의 존재 형태: 수소붕소화–산화로 생긴 4-hydroxy-4-(furan-3-yl)butanal의 OH가 분자 내에서 C=O에 첨가해 고리 무리가 거의 없는 5원 고리 헤미아세탈을 만들며, 분자 내 반응이라 엔트로피 손실이 작아 평형이 고리형 쪽에 있으므로 C=O 흡수가 거의 없다.''',
    explain='''<p><b>핵심 반응:</b> 알카이닐 Grignard의 카보닐 1,2-첨가 → 염기에 의한 알카인 위치 이성질화(알카인 지퍼) → 말단 알카인의 anti-Markovnikov 수소붕소화–산화 → 분자 내 헤미아세탈 형성.</p>
<p>① CH<sub>3</sub>C≡C–MgBr의 탄소 음이온성 말단이 알데하이드 C=O에 첨가하여 알콕사이드를 만들고 H<sub>3</sub>O<sup>+</sup> 처리로 2차 프로파질 알코올 A(C<sub>8</sub>H<sub>8</sub>O<sub>2</sub>)가 된다.</p>
<p>② A → B: NaNH<sub>2</sub>(짝산 NH<sub>3</sub>, pK<sub>a</sub> ≈ 38)는 프로파질 C–H(pK<sub>a</sub> ≈ 35 내외)를 뗄 수 있을 만큼 강하다. 탈양성자화–재양성자화가 반복되며 삼중 결합이 C2≡C3 → (알렌 C2=C3=C4) → C3≡C4로 이동한다. 각 단계는 가역이지만, 말단 알카인이 생기는 순간 ≡C–H(pK<sub>a</sub> ≈ 25)가 NH<sub>2</sub><sup>−</sup>에 의해 비가역적으로 탈양성자화되어 아세틸라이드로 빠져나가므로(르샤틀리에) 열역학적으로 불리한 말단 알카인 쪽으로 평형이 완전히 끌려간다. 그래서 NaNH<sub>2</sub>는 과량(알코올 O–H, 이성질화, 아세틸라이드 형성에 모두 소모)이 필요하다. B의 IR 3300 cm<sup>−1</sup>(≡C–H 신축, 날카로움)과 2120 cm<sup>−1</sup>(C≡C)는 말단 알카인의 증거이다.</p>
<p>③ 흔한 오답: NaNH<sub>2</sub>를 단순 염기로만 보고 “A의 O–H만 떼어지고 변화 없음”이라 답하거나, 알렌(C<sub>8</sub>H<sub>8</sub>O<sub>2</sub>, 같은 분자식)을 B로 고르는 경우. 알렌은 IR에 ≡C–H 3300 cm<sup>−1</sup> 흡수가 없고 약 1950 cm<sup>−1</sup>의 C=C=C 흡수를 보이므로 단서와 맞지 않는다.</p>
<p>④ B → C: 부피 큰 (Sia)<sub>2</sub>BH는 말단 알카인에 한 번만 syn 첨가하고 붕소는 덜 치환된 말단 탄소에 붙는다(anti-Markovnikov). H<sub>2</sub>O<sub>2</sub>/NaOH 산화로 C–B 결합이 C–OH로 바뀌어(배열 유지) 엔올이 되고, 토토머화하여 알데하이드가 된다(cf. HgSO<sub>4</sub>/H<sub>2</sub>SO<sub>4</sub> 수화라면 Markovnikov 방향의 메틸 케톤). (Sia)<sub>2</sub>BH를 과량 쓰는 것은 O–H가 붕소화제 일부를 소모하기 때문이다.</p>
<p>⑤ 생성된 4-hydroxy-4-(furan-3-yl)butanal은 OH와 CHO가 1,4-관계(γ)여서 분자 내 첨가로 5원 고리 헤미아세탈(oxolan-2-ol)을 만든다. 5·6원 고리는 고리 무리가 작고 분자 내 반응이라 유효 농도가 높아, γ-·δ-하이드록시 알데하이드는 대부분 고리형으로 존재한다(당의 푸라노스·피라노스와 같은 원리). 따라서 C는 1720 cm<sup>−1</sup> 부근 C=O 흡수가 거의 없고 O–H 흡수만 강하다. 새로 생긴 아노머 탄소(C2) 때문에 두 부분입체이성질체(아노머)의 혼합물로 존재한다.</p>''',
),
# ---------------------------------------------------------------- 2021B-9
dict(
    key='2021B-9',
    src='2021학년도 B형 9번 유형',
    src_topic='methyl 4-chlorobenzoate + vinylMgBr(2당량) → HBr/(PhCO₂)₂ anti-Markovnikov → NH₃ 이중 SN2로 piperidinol',
    change='에스터 + Grignard 2당량(3차 알코올) 단계는 유지하고, HBr/과산화물 대신 클릭 반응으로 분류되는 라디칼 thiol–ene 결합(AIBN 개시)을 '
           '사용하였다. 개시제(AIBN)의 역할뿐 아니라 개시·전파 단계를 반쪽 굽은 화살표로 직접 쓰게 하고, '
           '이온성(Markovnikov) 경로가 일어나지 않는 이유까지 서술하게 하여 라디칼 anti-Markovnikov 첨가의 본질을 평가하도록 변형',
    paper=dict(cite='J. Am. Chem. Soc. 2012, 134, 6916–6919', book='Klein 11.49',
               what='thiol–ene 결합: R–CH=CH₂ + R′SH → R–CH₂CH₂–SR′(라디칼 개시, anti-Markovnikov); 단백질의 N-알릴 아마이드와 시스테인 thiol의 결합'),
    nobel='2022 노벨 화학상(Sharpless·Meldal·Bertozzi — 클릭 화학·생체직교 화학; thiol–ene은 대표적 클릭형 반응), 1912 노벨 화학상(V. Grignard)',
    body=f'''다음은 ethyl 4-fluorobenzoate(<b class="lbltxt">A</b>)로부터 중간 주생성물 <b class="lbltxt">B</b>(C<sub>11</sub>H<sub>11</sub>FO)를 거쳐 최종 주생성물 <b class="lbltxt">C</b>(C<sub>17</sub>H<sub>23</sub>FO<sub>5</sub>S<sub>2</sub>)를 합성하는 반응식이다. (단, 각 반응에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(scheme(M('CCOC(=O)c1ccc(F)cc1', 'A', 15), arrow('1) CH<sub>2</sub>=CHMgBr (2 당량)', '2) H<sub>3</sub>O<sup>+</sup>'), L('B')),
       scheme(L('B'), arrow('HSCH<sub>2</sub>CO<sub>2</sub>CH<sub>3</sub> (2 당량)', 'AIBN (촉매량), 80 ℃'), L('C')),
       scheme(M('CC(C)(C#N)N=NC(C)(C)C#N', 'AIBN', 13)))}
<p class="ask"><b class="lbltxt">B</b>와 <b class="lbltxt">C</b>의 구조를 각각 그리시오. 또한 <b class="lbltxt">B</b>가 <b class="lbltxt">C</b>로 전환되는 과정에서 개시 단계와 전파 단계를 반쪽 굽은 화살표(fishhook arrow)를 사용하여 제시하고, 황이 말단 탄소에 결합하는 위치선택성이 나타나는 이유를 서술하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('C=CC(O)(C=C)c1ccc(F)cc1', 'B', 15)}{M('COC(=O)CSCCC(O)(CCSCC(=O)OC)c1ccc(F)cc1', 'C', 12)}</div>
B = 3-(4-fluorophenyl)penta-1,4-dien-3-ol, C = dimethyl 2,2′-[3-(4-fluorophenyl)-3-hydroxypentane-1,5-diylbis(sulfanediyl)]diacetate (두 비닐기 말단 탄소에 각각 SCH<sub>2</sub>CO<sub>2</sub>CH<sub>3</sub>가 결합한 비스(싸이오에터)).<br>
개시: AIBN —(Δ)→ 2 (CH<sub>3</sub>)<sub>2</sub>C(CN)• + N<sub>2</sub>; (CH<sub>3</sub>)<sub>2</sub>C(CN)• + H–SR′ → (CH<sub>3</sub>)<sub>2</sub>CH(CN) + R′S•<br>
전파 ①: R′S• + CH<sub>2</sub>=CH–R → R′S–CH<sub>2</sub>–C•H–R (2차 라디칼)<br>
전파 ②: R′S–CH<sub>2</sub>–C•H–R + H–SR′ → R′S–CH<sub>2</sub>–CH<sub>2</sub>–R + R′S• (연쇄 운반체 재생)<br>
위치선택성: R′S•가 덜 치환된 말단 CH<sub>2</sub>에 첨가해야 더 안정한 2차 라디칼(초공액 안정화)이 생기고 입체 장애도 작다. 즉 첫 단계에서 생기는 라디칼의 안정성이 위치를 결정하므로 S가 말단 탄소에 결합한다(anti-Markovnikov).''',
    explain='''<p><b>핵심 반응:</b> 에스터 + Grignard 2당량(친핵성 아실 치환 → 케톤 → 1,2-첨가) / 라디칼 연쇄 thiol–ene 첨가(anti-Markovnikov).</p>
<p>① A → B: 첫 번째 CH<sub>2</sub>=CH<sup>−</sup>가 에스터 C=O에 첨가해 사면체 중간체를 만들고 EtO<sup>−</sup>가 떨어져 aryl vinyl ketone이 된다. 케톤은 에스터보다 반응성이 커서 즉시 두 번째 비닐 Grignard가 첨가하고, H<sub>3</sub>O<sup>+</sup> 처리로 3차 알코올 B(C<sub>11</sub>H<sub>11</sub>FO)를 준다. 케톤 단계에서 멈추지 않으므로 Grignard는 2당량 이상이 필요하다.</p>
<p>② AIBN은 약 60~80 ℃에서 C–N 결합이 균일 분해되며 매우 안정한 N<sub>2</sub>를 내보내는 것이 구동력이다. 생긴 2-cyano-2-propyl 라디칼은 S–H(결합 해리 에너지 약 365 kJ/mol, C–H보다 약함)에서 H를 떼어 싸이일 라디칼 R′S•를 만든다.</p>
<p>③ 전파는 두 단계가 서로의 연쇄 운반체를 만들어 주는 순환이다. R′S•가 비닐기의 말단 CH<sub>2</sub>에 첨가하면 2차 탄소 라디칼(벤질 위치는 아님—Ar은 3차 카비놀 탄소에 붙어 있음)이 생기고, 이 라디칼이 다른 thiol에서 H를 떼어 생성물과 새 R′S•를 만든다. 두 비닐기가 각각 반응하므로 thiol 2당량이 소비되어 C(C<sub>17</sub>H<sub>23</sub>FO<sub>5</sub>S<sub>2</sub> = B + 2 C<sub>3</sub>H<sub>6</sub>O<sub>2</sub>S)가 된다.</p>
<p>④ 왜 Markovnikov 생성물이 생기지 않는가: thiol(pK<sub>a</sub> ≈ 8~10)은 HBr처럼 알켄을 양성자화할 만큼 강한 산이 아니므로 탄소 양이온 경로(이온성 첨가)가 거의 일어나지 않는다. 생성물의 위치는 “H<sup>+</sup>가 먼저 붙어 더 안정한 양이온” 대신 “R′S•가 먼저 붙어 더 안정한 라디칼”로 결정된다—기출의 HBr/과산화물 효과와 같은 논리이며, 첫 번째로 붙는 원자가 H가 아니라 헤테로 원자라서 결과가 anti-Markovnikov가 된다.</p>
<p>⑤ thiol–ene 반응은 산소·물 존재에서도 빠르고, 부산물이 없으며, 정량적·위치선택적이어서 고분자 가교와 단백질 접합(논문: 시스테인 thiol과 N-알릴 아마이드의 결합)에 쓰이는 클릭형 반응이다. 흔한 오답: (i) Grignard 1당량만 반응한 케톤을 B로 그림(분자식 불일치), (ii) S가 내부 탄소에 붙은 Markovnikov 형태, (iii) 3차 알코올이 탈수된 구조(라디칼 조건에서는 일어나지 않음).</p>''',
),
# ---------------------------------------------------------------- 2021A-3
dict(
    key='2021A-3',
    src='2021학년도 A형 3번 유형',
    src_topic='phenylacetylene → (HgSO₄ 수화 vs 수소붕소화 선택) → acetophenone → Claisen–Schmidt → chalcone, IR 파수 비교',
    change='말단 알카인의 위치선택성 비교 대신, 페닐 치환 내부 알카인에 HCl을 첨가할 때 생기는 선형 비닐 양이온의 위치선택성과 '
           'E/Z 입체선택성(t-Bu 크기 효과, E:Z = 100:0 문헌값)을 묻고, 같은 기질의 Hg²⁺ 촉매 수화 생성물을 함께 그리게 하여 '
           '“비닐 양이온 = 공통 중간체” 관점으로 알카인 친전자성 첨가를 평가하도록 변형',
    paper=dict(cite='J. Am. Chem. Soc. 1976, 98, 3295–3300', book='Klein 10.78',
               what='Ph–C≡C–R + HCl → PhC(Cl)=CHR; R = Me, Et, i-Pr, t-Bu에서 E:Z = 70:30, 80:20, 95:5, 100:0'),
    nobel='',
    body=f'''다음은 3,3-dimethyl-1-phenylbut-1-yne(<b class="lbltxt">X</b>)에 반응 조건 (가)와 (나)를 각각 적용하여 주생성물 <b class="lbltxt">A</b>(C<sub>12</sub>H<sub>15</sub>Cl)와 <b class="lbltxt">B</b>(C<sub>12</sub>H<sub>16</sub>O)를 얻는 반응을 나타낸 것이다. (단, 각 반응에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(scheme(L('A'), larrow('(가) HCl (1 당량)', 'CH<sub>3</sub>COOH, 25 ℃'), M('CC(C)(C)C#Cc1ccccc1', 'X', 15),
              arrow('(나) HgSO<sub>4</sub>', 'H<sub>2</sub>SO<sub>4</sub>, H<sub>2</sub>O'), L('B')))}
<p>◦ (가)에서는 두 기하 이성질체 중 하나만 얻어진다.</p>
<p class="ask"><b class="lbltxt">A</b>의 입체구조를 그리고 이중 결합의 배열을 <i>E</i>/<i>Z</i>로 쓰시오. 또한 <b class="lbltxt">B</b>의 구조를 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('Cl/C(c1ccccc1)=C/C(C)(C)C', 'A: (E)', 15)}{M('CC(C)(C)CC(=O)c1ccccc1', 'B', 15)}</div>
A = (<i>E</i>)-(1-chloro-3,3-dimethylbut-1-en-1-yl)benzene (Cl과 t-Bu가 서로 반대편, Ph와 t-Bu가 같은 편), B = 3,3-dimethyl-1-phenylbutan-1-one''',
    explain='''<p><b>핵심 반응:</b> 알카인의 친전자성 첨가(HX, Hg<sup>2+</sup> 촉매 수화) — 비닐 양이온의 위치선택성과 입체선택성.</p>
<p>① 위치선택성: H<sup>+</sup>가 t-Bu 쪽 탄소(C2)에 붙으면 양전하가 Ph에 결합한 C1에 생기고, 이 비닐 양이온은 Ph의 π계와 공명하여 안정화된다(반대 방향이면 공명 안정화가 없는 알킬 치환 비닐 양이온). 따라서 Cl과 O는 모두 Ph 쪽 탄소에 결합한다.</p>
<p>② 입체선택성: C1<sup>+</sup>는 sp 혼성의 선형 구조로, 비어 있는 p 오비탈이 C2의 치환기(H와 t-Bu)가 놓인 평면 안에 있다. Cl<sup>−</sup>은 이 평면 안에서 C1에 접근하므로 H 쪽(덜 붐빔)과 t-Bu 쪽 중 H 쪽으로 접근한다. 결과적으로 Cl은 H와 같은 편(cis), t-Bu와 반대편(trans)이 된다. CIP 우선순위는 C1에서 Cl &gt; Ph, C2에서 t-Bu &gt; H이므로 Cl과 t-Bu가 반대편인 A는 <i>E</i>이다. 논문 데이터에서 R이 Me → Et → i-Pr → t-Bu로 커질수록 E:Z가 70:30 → 100:0으로 증가하는 것이 이 입체 접근 모델의 근거이다.</p>
<p>③ (나): Hg<sup>2+</sup>가 π 결합을 활성화하면 물은 양전하를 더 잘 지탱하는 Ph 쪽 탄소를 공격한다(Markovnikov 형). 탈수은화로 엔올 PhC(OH)=CH–t-Bu가 생기고 토토머화하여 아릴 케톤 B가 된다. Ph–CO–CH<sub>2</sub>–C(CH<sub>3</sub>)<sub>3</sub>.</p>
<p>④ 흔한 오답: (i) A를 Z로 그림(Cl과 Ph의 “크기”만 비교한 경우) — 입체를 결정하는 것은 Cl<sup>−</sup>이 접근하는 C2 쪽의 H와 t-Bu의 크기 차이이다. (ii) B를 1-phenyl의 반대쪽 케톤 PhCH<sub>2</sub>CO–t-Bu로 그림 — 이는 비닐 양이온이 t-Bu 쪽에 생길 때의 생성물이다. (iii) gem-이염화물 — HCl 1당량 조건이므로 해당하지 않는다.</p>''',
),
# ---------------------------------------------------------------- 2020B-8
dict(
    key='2020B-8',
    src='2020학년도 B형 8번 유형',
    src_topic='methyl benzoate 염기 가수분해의 BAc2 vs BAl2 메커니즘을 ¹⁸O 표지 위치로 판별',
    change='에스터 가수분해 대신 Corey 프로스타글란딘 합성의 Baeyer–Villiger 산화(bicyclo[2.2.1]heptenone → 이환 락톤)를 소재로, '
           'Criegee 중간체 경로와 다이옥시레인 경로를 카보닐 ¹⁸O 표지로 판별하게 하였다(Doering–Dorfman 실험의 사고과정). '
           '이어 표지 락톤의 염기 가수분해(아실–산소 절단)까지 추적하게 하여 기출의 BAc2 논리를 한 번 더 적용하도록 변형하고, '
           '이동 기의 선택(이동 경향성)도 함께 묻는다.',
    paper=dict(cite='J. Am. Chem. Soc. 1970, 92, 397–398', book='Klein 21.87',
               what='E. J. Corey 프로스타글란딘 합성: 7-(methoxymethyl)bicyclo[2.2.1]hept-5-en-2-one의 Baeyer–Villiger 산화 → 이환 락톤 → NaOH 가수분해로 하이드록시산'),
    nobel='1990 노벨 화학상(E. J. Corey — 유기 합성 이론과 방법론, 역합성 분석)',
    body=f'''다음은 카보닐 산소를 <sup>18</sup>O로 표지한 bicyclo[2.2.1]hept-5-en-2-one(<b class="lbltxt">A</b>)으로부터 락톤 <b class="lbltxt">B</b>(C<sub>7</sub>H<sub>8</sub>O<sub>2</sub>)를 거쳐 <b class="lbltxt">C</b>(C<sub>7</sub>H<sub>10</sub>O<sub>3</sub>)를 합성하는 반응과, <b class="lbltxt">A</b> → <b class="lbltxt">B</b> 단계에 대해 제안된 두 가지 메커니즘을 나타낸 것이다. (단, *O는 <sup>18</sup>O이며, 각 반응에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(scheme(M('[18O]=C1CC2C=CC1C2', 'A', 16), arrow('<i>m</i>-CPBA', 'NaHCO<sub>3</sub>'), L('B'),
              arrow('1) NaOH, H<sub>2</sub>O', '2) H<sub>3</sub>O<sup>+</sup>'), L('C')),
       '<div><b>[메커니즘 1]</b> 퍼옥시산이 C=*O 탄소에 첨가하여 사면체 Criegee 중간체 R<sub>2</sub>C(*OH)–O–O–C(=O)Ar가 생긴 뒤, 카보닐 탄소에 결합한 한 탄소가 O–O 결합의 O로 이동하면서 ArCO<sub>2</sub><sup>−</sup>가 떨어지고, *OH가 C=*O로 되어 락톤이 된다.</div>'
       '<div><b>[메커니즘 2]</b> 케톤이 먼저 3원 고리 다이옥시레인(카보닐 탄소에 *O와 O가 함께 결합)으로 산화된 뒤, 탄소 하나가 두 산소 중 하나로 이동하며 O–O 결합이 끊어져 락톤이 된다. 다이옥시레인의 두 산소는 대칭적으로 동등하다.</div>',
       title='')}
<p class="ask">[메커니즘 1]을 따를 때 <b class="lbltxt">B</b>의 구조를 *O의 위치를 표시하여 그리고, 카보닐 탄소에 결합한 두 탄소 중 이동하는 탄소를 그 이유와 함께 쓰시오. [메커니즘 2]를 따를 때 *O가 <b class="lbltxt">B</b>의 어느 산소에 어떤 비율로 분포하는지 쓰시오. 실험 결과 [메커니즘 1]이 타당하였을 때, <b class="lbltxt">C</b>의 입체구조를 *O의 위치를 표시하여 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('[18O]=C1CC2CC(O1)C=C2', 'B ([메커니즘 1])', 16)}{M('OC(=[18O])C[C@@H]1C=C[C@H](O)C1', 'C (cis, 라셈)', 16)}</div>
이동하는 탄소: 2차 알킬기인 다리목 C1(카보닐 탄소 외에 탄소 2개와 결합)이 1차 알킬기인 CH<sub>2</sub>(C3, 카보닐 외에 탄소 1개)보다 이동 경향성이 크다 → O는 C1과 C2 사이에 삽입된다(2-oxabicyclo[3.2.1]oct-6-en-3-one).<br>
[메커니즘 2]: *O가 락톤의 카보닐 산소와 고리 산소(에스터 알킬 쪽 O)에 1 : 1로 분포한다.<br>
C = cis-2-(4-hydroxycyclopent-2-en-1-yl)acetic acid, *O는 카복실기(COOH)에 있고 고리의 OH에는 없다.''',
    explain='''<p><b>핵심 반응:</b> Baeyer–Villiger 산화(Criegee 중간체, 이동 경향성, 배열 유지) + 친핵성 아실 치환(BAc2)에 의한 락톤 가수분해 + <sup>18</sup>O 표지에 의한 메커니즘 판별.</p>
<p>① 이동 경향성: Baeyer–Villiger의 이동 단계에서 이동하는 탄소는 전자가 부족해지는 O 쪽으로 결합 전자쌍과 함께 옮겨 가므로, 부분 양전하를 잘 지탱하는 더 치환된 탄소가 이동한다(3차 &gt; 2차 ≈ 페닐 &gt; 1차 &gt; 메틸). A에서 카보닐 양옆은 2차 다리목 탄소 C1과 1차 CH<sub>2</sub>(C3)이므로 C1이 이동한다. 이동은 분자 내 1,2-이동이라 이동 탄소의 배열이 유지되어, 이환 골격이 그대로 보존된 2-oxabicyclo[3.2.1]oct-6-en-3-one이 된다. <i>m</i>-CPBA는 C=C 에폭시화도 가능하지만, 변형된 이환 케톤의 B–V 산화가 빠르고 NaHCO<sub>3</sub>로 산을 중화하여 화학선택성을 확보한다(Corey 합성의 조건).</p>
<p>② [메커니즘 1]: 원래의 C=*O 산소는 Criegee 중간체에서 C–*OH가 되고, 이동 후 다시 C=*O가 된다. 새로 삽입되는 고리 산소는 퍼옥시산에서 온다. ∴ *O는 100 % 락톤 카보닐 산소에 있다.</p>
<p>③ [메커니즘 2]: 다이옥시레인에서는 *O와 O가 동등하므로 C1이 어느 쪽 O로 이동해도 되고, 그 결과 *O는 카보닐 O와 고리 O에 50 : 50으로 나뉜다. 실제로 Doering과 Dorfman(1953)은 <sup>18</sup>O-benzophenone의 B–V 산화에서 표지가 phenyl benzoate의 카보닐 산소에만 남는 것을 확인하여 Criegee 메커니즘을 확정하였다—기출의 “표지 위치가 메커니즘마다 달라지는 산소를 고른다”는 논리와 같다.</p>
<p>④ B → C: OH<sup>−</sup>가 락톤 C=*O에 첨가해 사면체 중간체가 생기고, 고리 산소(알콕사이드)가 이탈하는 아실–산소 절단(BAc2)이 일어난다. 따라서 *O는 카복실레이트에 남고(공명으로 두 O가 동등), 새로 생긴 고리의 OH는 원래 락톤 고리 산소이므로 표지되지 않는다. H<sub>3</sub>O<sup>+</sup>로 양성자화하면 C가 된다(사면체 중간체의 양성자 교환으로 일부 *O가 용매와 교환될 수 있으나 표지는 카복실기에만 나타난다). 만약 [메커니즘 2]였다면 C의 OH에도 50 %의 *O가 나타났을 것이다.</p>
<p>⑤ 입체: 이환 락톤에서 C1(O 결합)과 C4(CH<sub>2</sub>C=O 결합)는 같은 다리(C7)로 묶여 있어, 고리를 열면 OH와 CH<sub>2</sub>CO<sub>2</sub>H가 사이클로펜텐 고리의 같은 면에 놓인다 → cis-1,4-이치환(라셈). 이 cis 관계가 Corey 락톤·프로스타글란딘 골격의 입체를 정한다. 흔한 오답: (i) CH<sub>2</sub>가 이동한 위치 이성질체(O가 C2–C3 사이), (ii) C를 trans로 그림, (iii) *O를 C의 OH에 표시(알킬–산소 절단으로 착각).</p>''',
),
# ---------------------------------------------------------------- 2019A-4
dict(
    key='2019A-4',
    src='2019학년도 A형 4번 유형',
    src_topic='bromobenzene → Grignard + 에폭사이드(2C 연장) → MsCl → NaN₃ → LiAlH₄ 순서 고르기',
    change='Grignard + 에폭사이드 대신 아세틸라이드 + 에폭사이드로 2탄소 연장을 하고, 알카인의 cis 선택 환원(Lindlar)과 '
           '에스터화를 결합하여 “잎 냄새” 휘발성 물질 (Z)-3-hexenyl acetate를 합성하는 순서 고르기로 변형. '
           '<보기>에 Na/NH₃(trans), H₂/Pt(과환원), CH₃CHO(잘못된 연장) 같은 함정을 넣고, 함정 시약을 썼을 때의 입체구조도 묻는다.',
    paper=dict(cite='Nat. Prod. Rep. 2012, 29, 1288–1303', book='Klein 12.37',
               what='상처 입은 식물이 방출하는 녹엽 휘발성 물질 (Z)-3-hexenyl acetate를 아세틸라이드–에폭사이드 반응과 Lindlar 환원으로 합성'),
    nobel='',
    body=f'''다음은 1-butyne으로부터 중간 주생성물 <b class="lbltxt">A</b>(C<sub>6</sub>H<sub>10</sub>O)와 <b class="lbltxt">B</b>(C<sub>6</sub>H<sub>12</sub>O)를 거쳐 녹엽 휘발성 물질인 (<i>Z</i>)-3-hexenyl acetate를 합성하는 과정이다. (단, 각 단계에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(scheme(M('CCC#C', '', 15), arrow('(1)', '', 34), arrow('(2)', '', 34), L('A'), arrow('(3)', '', 34), L('B')),
       scheme(arrow('(4)', '', 34), M(Z_ACET, '', 15)))}
{frame('<div style="text-align:center"><b>&lt;보 기&gt;</b></div>'
       '<table class="chem" style="width:100%;border-collapse:collapse"><tr><td>㉠ NaNH<sub>2</sub>, NH<sub>3</sub>(<i>l</i>)</td><td>㉡ 1) oxirane　2) H<sub>2</sub>O</td></tr>'
       '<tr><td>㉢ 1) CH<sub>3</sub>CHO　2) H<sub>2</sub>O</td><td>㉣ H<sub>2</sub>, Lindlar 촉매</td></tr>'
       '<tr><td>㉤ Na, NH<sub>3</sub>(<i>l</i>)</td><td>㉥ H<sub>2</sub>, Pt</td></tr>'
       '<tr><td colspan="2">㉦ CH<sub>3</sub>COCl, pyridine　　(oxirane = ethylene oxide)</td></tr></table>')}
<p class="ask">(1)~(4)에 들어갈 반응 조건을 &lt;보기&gt;의 ㉠~㉦에서 1가지씩 골라 순서대로 쓰시오. 또한 (3)에서 ㉤를 사용했을 때 얻어지는 <b class="lbltxt">B</b>의 입체이성질체의 입체구조를 그리시오. [[PTS]]</p>''',
    answer=f'''(1) ㉠ → (2) ㉡ → (3) ㉣ → (4) ㉦<br>
<div class="ansbox">{M('CCC#CCCO', 'A: hex-3-yn-1-ol', 14)}{M(Z_OL, 'B: (Z)-hex-3-en-1-ol', 14)}{M('CC/C=C/CCO', '㉤ 사용 시: (E)-hex-3-en-1-ol', 14)}</div>''',
    explain='''<p><b>핵심 반응:</b> 아세틸라이드의 형성과 에폭사이드 SN2 개환(탄소 2개 + OH 도입) → Lindlar 수소화(syn, cis-알켄) → 알코올의 아실화(친핵성 아실 치환).</p>
<p>① (1) ㉠: 말단 알카인 C–H(pK<sub>a</sub> ≈ 25)는 NH<sub>2</sub><sup>−</sup>(짝산 pK<sub>a</sub> ≈ 38)로 완전히 탈양성자화된다. (2) ㉡: 아세틸라이드가 oxirane의 탄소를 뒤쪽에서 공격(SN2)하여 고리 무리(약 110 kJ/mol)가 풀리며 알콕사이드가 되고, H<sub>2</sub>O로 양성자화되어 A = hex-3-yn-1-ol(C<sub>6</sub>H<sub>10</sub>O). OH가 새 사슬의 두 번째 탄소에 오는 것이 에폭사이드 개환의 특징이다.</p>
<p>② 함정 ㉢: CH<sub>3</sub>CHO에 첨가하면 2차 프로파질 알코올 hex-3-yn-2-ol(C<sub>6</sub>H<sub>10</sub>O, 분자식은 같음)이 생겨 최종물의 1차 OCH<sub>2</sub> 구조가 나오지 않는다. 분자식이 같은 이성질체를 구별하려면 목표물의 탄소 골격(CH<sub>2</sub>CH<sub>2</sub>O)을 역합성으로 따져야 한다.</p>
<p>③ (3) ㉣: Lindlar 촉매(Pd/CaCO<sub>3</sub>, Pb(OAc)<sub>2</sub>, quinoline으로 피독)는 알카인에 H<sub>2</sub>를 촉매 표면에서 syn 첨가하고 알켄 단계에서 멈추므로 (<i>Z</i>)-알켄 B(C<sub>6</sub>H<sub>12</sub>O, 잎 알코올)를 준다. ㉥(H<sub>2</sub>, Pt)은 알케인까지 환원(C<sub>6</sub>H<sub>14</sub>O)하므로 분자식이 맞지 않는다.</p>
<p>④ ㉤(Na, NH<sub>3</sub>)를 쓰면 용해 금속 환원으로 라디칼 음이온 → 비닐 라디칼 → 비닐 음이온을 거치며 두 알킬기가 반대편에 놓이는 더 안정한 trans 배치가 선택되어 (<i>E</i>)-hex-3-en-1-ol이 된다. 단, 실제로는 NH<sub>3</sub> 조건에서 OH가 Na와 반응하므로 Na를 과량 쓴다.</p>
<p>⑤ (4) ㉦: 알코올 O가 아실 클로라이드 C=O를 공격 → 사면체 중간체 → Cl<sup>−</sup> 이탈 → pyridine이 HCl을 중화. (3)과 (4)의 순서가 바뀌면 B(C<sub>6</sub>H<sub>12</sub>O)의 분자식이 맞지 않으므로 순서는 유일하다.</p>''',
),
# ---------------------------------------------------------------- 2018A-5
dict(
    key='2018A-5',
    src='2018학년도 A형 5번 유형',
    src_topic='3-pentanone → 사이아노하이드린 A → (HCl/H₂O, 가열) 하이드록시산 B / (진한 H₂SO₄, 가열) 불포화산 C로 분기',
    change='케톤 카보닐 첨가 후 조건에 따라 두 생성물로 갈라지는 구조는 유지하되, 사이아노하이드린 대신 Corey–Chaykovsky 에폭시화(황 일라이드)로 '
           '에폭사이드를 만들고, 염기성(NaOCH₃) 대 산성(CH₃OH, H₂SO₄) 개환의 위치선택성 차이(입체 지배 SN2 vs 전자 지배 SN1형)를 묻도록 변형. '
           '두 생성물이 같은 분자식의 위치 이성질체여서 메커니즘 이해 없이는 구별할 수 없다.',
    paper=dict(cite='Synth. Commun. 2003, 33, 2135–2143', book='Klein 14.65',
               what='trimethylsulfonium 염 + NaH → 황 일라이드, acetophenone과 반응하여 2-methyl-2-phenyloxirane + Me₂S (Corey–Chaykovsky)'),
    nobel='',
    body=f'''다음은 acetophenone으로부터 중간 주생성물 <b class="lbltxt">A</b>(C<sub>9</sub>H<sub>10</sub>O)를 거쳐 최종 주생성물 <b class="lbltxt">B</b>와 <b class="lbltxt">C</b>를 각각 합성하는 반응식이다. <b class="lbltxt">B</b>와 <b class="lbltxt">C</b>는 분자식이 C<sub>10</sub>H<sub>14</sub>O<sub>2</sub>인 구조 이성질체이다. (단, 각 단계에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(scheme(M('CC(=O)c1ccccc1', '', 15), arrow('(CH<sub>3</sub>)<sub>3</sub>S<sup>+</sup> I<sup>−</sup>', 'NaH, DMSO'), L('A')),
       scheme(L('B'), larrow('NaOCH<sub>3</sub>', 'CH<sub>3</sub>OH, 가열', width=70),
              L('A'), arrow('CH<sub>3</sub>OH', 'H<sub>2</sub>SO<sub>4</sub> (촉매량)'), L('C')))}
<p class="ask"><b class="lbltxt">B</b>와 <b class="lbltxt">C</b>의 구조를 각각 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CC1(c2ccccc2)CO1', 'A', 14)}{M('COCC(C)(O)c1ccccc1', 'B', 14)}{M('COC(C)(CO)c1ccccc1', 'C', 14)}</div>
A = 2-methyl-2-phenyloxirane, B = 1-methoxy-2-phenylpropan-2-ol, C = 2-methoxy-2-phenylpropan-1-ol''',
    explain='''<p><b>핵심 반응:</b> 황 일라이드에 의한 에폭사이드 합성(Corey–Chaykovsky) / 에폭사이드 개환의 위치선택성 — 강한 친핵체(염기성)는 덜 치환된 탄소, 산 촉매는 더 치환된 탄소.</p>
<p>① A: NaH가 (CH<sub>3</sub>)<sub>3</sub>S<sup>+</sup>의 C–H(양전하 S에 인접해 산성)를 떼어 황 일라이드 (CH<sub>3</sub>)<sub>2</sub>S<sup>+</sup>–CH<sub>2</sub><sup>−</sup>를 만든다. 일라이드 탄소가 케톤 C=O에 첨가해 베타인(알콕사이드–설포늄)이 생기고, 알콕사이드 O가 분자 내 SN2로 CH<sub>2</sub>를 공격하면서 중성의 좋은 이탈기 (CH<sub>3</sub>)<sub>2</sub>S가 떨어져 에폭사이드가 닫힌다. (Wittig의 인 일라이드와 달리 S–O 결합 형성 경향이 약해 알켄 대신 에폭사이드가 된다.)</p>
<p>② B(염기성): CH<sub>3</sub>O<sup>−</sup>는 강한 친핵체로 SN2 메커니즘을 따르므로 입체 장애가 작은 1차 CH<sub>2</sub>를 뒤쪽에서 공격한다. 4차(3차 치환) 탄소는 SN2에 거의 반응하지 않는다. 개환된 3차 알콕사이드가 CH<sub>3</sub>OH에서 양성자를 받아 1-methoxy-2-phenylpropan-2-ol.</p>
<p>③ C(산성): 에폭사이드 O가 양성자화되면 C–O 결합이 약해지고, 전이 상태에서 양전하가 3차·벤질 탄소에 크게 쌓인다(SN1 성격). 약한 친핵체 CH<sub>3</sub>OH는 양전하를 더 잘 지탱하는 C2(3차·벤질)를 공격하고 탈양성자화되어 2-methoxy-2-phenylpropan-1-ol이 된다. 즉 산성 조건에서는 “입체”가 아닌 “전자적 요인”이 위치를 정한다.</p>
<p>④ 확인 포인트: B는 3차 알코올(OH가 붙은 탄소에 H 없음), C는 1차 알코올(–CH<sub>2</sub>OH). 흔한 오답은 두 생성물을 뒤바꾸는 것, 또는 산성 조건에서 3차 벤질 양이온의 Meinwald 자리옮김(2-phenylpropanal)·탈수를 주생성물로 쓰는 것이다—용매인 CH<sub>3</sub>OH가 대과량이므로 친핵체 포획이 우세하다.</p>''',
),
# ---------------------------------------------------------------- 2017A-4
dict(
    key='2017A-4',
    src='2017학년도 A형 4번 유형',
    src_topic='mesityl oxide에 CH₃Li(1,2-첨가) vs (CH₃)₂CuLi/CH₃I(1,4-첨가 후 엔올레이트 α-알킬화) 비교',
    change='단단한(유기리튬) 대 무른(큐프레이트) 친핵체의 1,2- vs 1,4-첨가 대비를 유지하되, 엔올레이트를 외부 CH₃I 대신 같은 분자 안의 '
           '1차 토실레이트로 포획하여 5원 고리를 닫는 “짝첨가–분자 내 알킬화” 연속 반응(vine mealybug 페로몬 합성)으로 바꾸었다. '
           '네오펜틸형 토실레이트가 분자 간 SN2에는 둔하지만 분자 내 5-exo-tet 고리화는 가능하다는 점까지 해설에서 다룬다.',
    paper=dict(cite='Tetrahedron Lett. 2010, 51, 5291–5293', book='Klein 22.117',
               what='γ-토실옥시 α,β-불포화 에스터에 Me₂CuLi 짝첨가 → 에스터 엔올레이트의 분자 내 SN2로 cyclopentane 형성(vine mealybug 성페로몬 합성)'),
    nobel='',
    body=f'''다음은 화합물 <b class="lbltxt">A</b>로부터 최종 주생성물 <b class="lbltxt">B</b>(C<sub>17</sub>H<sub>26</sub>O<sub>4</sub>S)와 <b class="lbltxt">C</b>(C<sub>11</sub>H<sub>20</sub>O<sub>2</sub>)를 각각 합성하는 반응식이다. (단, 각 단계에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(scheme(M('CCOC(=O)/C=C/CC(C)(C)COS(=O)(=O)c1ccc(C)cc1', 'A', 13)),
       scheme(L('B'), larrow('1) CH<sub>3</sub>Li (과량), −78 ℃', '2) H<sub>2</sub>O'),
              L('A'), arrow('1) (CH<sub>3</sub>)<sub>2</sub>CuLi, −78 → 0 ℃', '2) H<sub>2</sub>O'), L('C')))}
<p>◦ <b class="lbltxt">C</b>는 고리 화합물이며, IR 스펙트럼에서 1735 cm<sup>−1</sup> 부근에 강한 흡수를 보인다. (단, 상대 입체 배열은 고려하지 않는다.)</p>
<p class="ask"><b class="lbltxt">B</b>와 <b class="lbltxt">C</b>의 구조를 각각 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CC(C)(O)/C=C/CC(C)(C)COS(=O)(=O)c1ccc(C)cc1', 'B', 12)}{M('CCOC(=O)C1CC(C)(C)CC1C', 'C', 15)}</div>
B = (<i>E</i>)-5-hydroxy-2,2,5-trimethylhex-3-enyl tosylate (3차 알릴 알코올, OTs 보존), C = ethyl 2,4,4-trimethylcyclopentane-1-carboxylate''',
    explain='''<p><b>핵심 반응:</b> 단단한 유기리튬의 C=O 1,2-첨가(에스터 → 3차 알코올) vs 무른 큐프레이트의 1,4-짝첨가 → 엔올레이트의 분자 내 SN2 알킬화(탠덤 짝첨가–알킬화).</p>
<p>① B: CH<sub>3</sub>Li는 C–Li 결합의 이온성이 커서 전하 밀도가 큰 단단한 친핵체이고, 전하 지배적으로 가장 양전하가 큰 카보닐 탄소를 직접 공격한다(1,2-첨가). 첫 첨가 후 EtO<sup>−</sup>가 떨어져 메틸 케톤이 생기고 즉시 두 번째 CH<sub>3</sub>Li가 첨가하여 3차 알콕사이드 → H<sub>2</sub>O 처리로 3차 알릴 알코올 B(C<sub>17</sub>H<sub>26</sub>O<sub>4</sub>S = A − OEt + 2 CH<sub>3</sub> + H). C=C의 <i>E</i> 배치와 OTs는 그대로이다(−78 ℃, 네오펜틸형 1차 토실레이트는 SN2가 매우 느림).</p>
<p>② C: (CH<sub>3</sub>)<sub>2</sub>CuLi는 무른 친핵체로 오비탈 지배적으로 LUMO 계수가 큰 β-탄소에 메틸을 전달한다(1,4-짝첨가). 이때 생긴 에스터 엔올레이트의 α-탄소가 같은 분자의 CH<sub>2</sub>–OTs 탄소를 뒤쪽에서 공격(분자 내 SN2, 5-exo-tet)하여 TsO<sup>−</sup>를 내보내고 cyclopentane 고리가 닫힌다. 고리 원자: C<sub>α</sub>(CO<sub>2</sub>Et) – C<sub>β</sub>(새 CH<sub>3</sub>) – CH<sub>2</sub> – C(CH<sub>3</sub>)<sub>2</sub> – CH<sub>2</sub> – C<sub>α</sub>. 분자식 C<sub>11</sub>H<sub>20</sub>O<sub>2</sub>, IR 1735 cm<sup>−1</sup>는 포화 에스터 C=O(콘쥬게이션이 사라져 A의 약 1720 cm<sup>−1</sup>보다 높음).</p>
<p>③ 왜 분자 간 SN2(큐프레이트가 OTs를 직접 치환)나 엔올레이트의 분자 간 반응이 아닌가: 토실레이트 탄소는 4차 탄소 옆(네오펜틸형)이라 분자 간 뒤쪽 공격이 크게 방해받는다. 그러나 분자 내 5원 고리 형성은 반응 중심이 가까워 유효 농도가 매우 크고(엔트로피 손실 작음), gem-다이메틸기의 Thorpe–Ingold 효과도 고리화를 돕는다. 기출의 “짝첨가로 생긴 엔올레이트를 CH<sub>3</sub>I로 포획”을 분자 내 포획으로 바꾼 것이다.</p>
<p>④ 흔한 오답: (i) B를 1,4-첨가물로 그림, (ii) C를 고리화되지 않은 짝첨가물 EtO<sub>2</sub>C–CH<sub>2</sub>–CH(CH<sub>3</sub>)–…–CH<sub>2</sub>OTs로 그림(분자식 C<sub>18</sub>…로 불일치), (iii) O-알킬화(엔올 에터 고리)로 그림 — 탄소 친핵성 α-위치의 SN2가 일반적이며 IR 1735 cm<sup>−1</sup>가 에스터 C=O의 존재를 보여 준다.</p>''',
),
# ---------------------------------------------------------------- 2017B-4
dict(
    key='2017B-4',
    src='2017학년도 B형 4번 유형',
    src_topic='ROTs 가에탄올분해 속도(벤질 > 알릴 > 에틸) + 황 인접기 관여(EtSCH₂CH₂Cl 가수분해 가속)',
    change='치환기 종류에 따른 SN1 속도 비교를 실측 데이터(α-할로젠 치환 벤질 할라이드의 가수분해 속도)로 바꾸어, '
           '“전기음성 원자인데도 α-Cl이 양이온을 안정화하는” 역설과 이탈기 효과를 분리해 해석하게 하였다. '
           '황의 인접기 관여는 유지하되 속도 가속 대신 biotin 합성(Hoffmann-La Roche)의 SOCl₂ 염소화에서 나타나는 “이중 반전 = 배열 유지”의 입체화학으로 평가하도록 변형',
    paper=dict(cite='J. Am. Chem. Soc. 1951, 73, 22–23; J. Am. Chem. Soc. 1982, 104, 6460–6462', book='Klein 7.85, 7.88',
               what='PhCXYZ의 50 % 수용성 아세톤 가수분해 속도 / biotin 전구체의 2차 알코올을 SOCl₂·pyridine으로 염소화할 때 고리 황의 관여로 배열 유지'),
    nobel='1994 노벨 화학상(G. A. Olah — 탄소 양이온 화학; 할로젠 안정화 탄소 양이온 연구 포함)',
    body=f'''다음은 [반응 1]에서 벤질형 할로젠화물의 가수분해 반응 속도 상수(<i>k</i>)와, [반응 2]에서 고리 황을 가진 2차 알코올의 염소화 반응을 나타낸 것이다.
{frame('<div class="ft">[반응 1] 50 % 수용성 acetone, 30 ℃ (S<sub>N</sub>1 반응)</div>'
       '<table class="data" style="white-space:nowrap"><tr><th>기질</th><th><i>k</i></th><th>기질</th><th><i>k</i></th></tr>'
       '<tr><td>㉠ PhCH<sub>2</sub>Cl</td><td>0.22</td><td>㉢ PhCCl<sub>3</sub></td><td>110.5</td></tr>'
       '<tr><td>㉡ PhCHCl<sub>2</sub></td><td>2.21</td><td>㉣ PhCHClBr</td><td>31.1</td></tr></table>'
       '<div class="chem" style="text-align:right">(<i>k</i>의 단위: 10<sup>−4</sup> min<sup>−1</sup>)</div>'
       '<div class="ft">[반응 2]</div>'
       + scheme(M('CCC[C@@H](O)[C@@H]1CCCS1', '', 14), arrow('SOCl<sub>2</sub>', 'pyridine', 50), M('CCC[C@@H](Cl)[C@@H]1CCCS1', '', 14))
       + '<div class="chem">· 생성물의 입체구조는 X선 결정 구조로 확인하였다.<br>· 같은 조건에서 황이 없는 (<i>R</i>)-1-cyclopentylbutan-1-ol은 배열이 반전된 염화물을 준다.</div>')}
<p class="ask">[반응 1]에서 ㉠~㉢의 반응 속도가 ㉠ &lt; ㉡ &lt; ㉢인 이유를 반응 중간체의 공명 구조를 근거로 서술하고, ㉣가 ㉡보다 빠른 이유를 쓰시오. 또한 [반응 2]의 반응 메커니즘을 굽은 화살표를 사용하여 제시하고, [반응 2]에서 배열이 유지되는 이유를 서술하시오. [[PTS]]</p>''',
    answer=f'''㉠ &lt; ㉡ &lt; ㉢: 속도 결정 단계에서 생기는 벤질 양이온의 α-위치에 Cl이 늘어날수록, Cl의 비공유 전자쌍이 빈 p 오비탈로 주개 작용을 하는 공명 구조 Ph–C(R)=Cl<sup>+</sup>가 추가되어(그리고 Ph 고리의 o,p 공명과 함께) 양이온이 더 안정해지고 전이 상태 에너지가 낮아진다. 이 공명 효과가 Cl의 유발(−I) 효과보다 크다.<br>
㉣ &gt; ㉡: 두 기질은 같은 양이온 PhCHCl<sup>+</sup>를 만들지만 ㉣는 Br<sup>−</sup>가 이탈한다. Br<sup>−</sup>는 더 약한 염기(HBr이 더 강한 산)이고 C–Br 결합이 더 약해 더 좋은 이탈기이다.<br>
[반응 2]: ① ROH + SOCl<sub>2</sub> → 클로로설파이트 R–O–S(=O)Cl (C–O 결합 유지, pyridine이 HCl 제거) → ② 고리 S의 비공유 전자쌍이 C–OS(O)Cl 탄소를 뒤쪽에서 공격(분자 내 S<sub>N</sub>2, 1차 반전), SO<sub>2</sub> + Cl<sup>−</sup> 이탈 → 3원 고리 설포늄(에피설포늄, 1-thioniabicyclo[3.1.0]hexane) → ③ Cl<sup>−</sup>가 같은 탄소를 S의 반대편에서 공격(2차 반전)하여 고리를 연다.<br>
배열 유지: 반전이 두 번 일어나므로(이중 반전) 전체적으로 배열이 유지된다. 황이 없는 경우에는 Cl<sup>−</sup>의 한 번의 S<sub>N</sub>2만 일어나 반전된다.''',
    explain='''<p><b>핵심 반응:</b> S<sub>N</sub>1 속도 = 탄소 양이온(전이 상태) 안정성 + 이탈기 능력 / 인접기 관여(anchimeric assistance)에 의한 이중 반전·배열 유지.</p>
<p>① ㉠→㉡→㉢: 이탈기가 모두 Cl<sup>−</sup>로 같으므로 차이는 양이온 안정성에서 온다. α-Cl은 전기음성도 때문에 σ 결합으로 전자를 끌지만(−I), 3p 비공유 전자쌍으로 빈 p 오비탈에 π 주개(+R) 작용을 한다: [Ph–C<sup>+</sup>H–Cl ↔ Ph–CH=Cl<sup>+</sup>]. 결과적으로 Cl 하나 추가에 약 10배, 두 개 추가에 약 500배 빨라진다. (3p–2p 겹침은 O·N의 2p–2p보다 약하지만 효과는 분명하다. 이런 할로카베늄 이온은 Olah가 초산 매질에서 직접 관찰하였다.)</p>
<p>② ㉡ vs ㉣: 같은 PhCHCl<sup>+</sup>를 거치므로 이탈기만 다르다. Br<sup>−</sup>가 더 크고 분극성이 커서 음전하를 더 잘 분산시키며(약한 염기), C–Br 결합이 C–Cl보다 약하다 → 약 14배 빠르다. (기출의 R-OTs 비교처럼 “양이온 안정성”과 “이탈기”를 분리해 해석하는 것이 출제 의도이다.)</p>
<p>③ [반응 2]의 메커니즘: SOCl<sub>2</sub>는 OH를 좋은 이탈기 –OS(O)Cl로 바꾼다(이 단계에서 탄소의 배열은 변하지 않음). 일반적인 2차 알코올에서는 pyridine·HCl에서 나온 Cl<sup>−</sup>가 뒤쪽에서 S<sub>N</sub>2 하여 반전된다. 그러나 이 기질에서는 고리 황이 반응 중심 바로 옆(β 위치)에 있어 분자 내 친핵체로서 Cl<sup>−</sup>보다 먼저, 훨씬 빠르게 뒤쪽 공격을 한다(3원 고리 전이 상태, 높은 유효 농도). 생긴 이환 에피설포늄 이온은 고리 무리와 양전하 때문에 반응성이 커서, Cl<sup>−</sup>가 S–C 결합의 반대편(원래 OH가 있던 쪽)에서 공격한다.</p>
<p>④ 입체: 1차 반전(S가 OH의 반대편에서 결합) + 2차 반전(Cl이 S의 반대편에서 결합) = 배열 유지. CIP 우선순위가 O→Cl로 바뀌어도 순서(Cl/O &gt; 고리 C(S) &gt; 프로필 &gt; H)가 같아 출발물과 생성물 모두 (<i>R</i>) 카비놀 탄소, (<i>S</i>) 고리 탄소이다. 이는 기출의 겨자 가스형 S 인접기 관여(EtSCH<sub>2</sub>CH<sub>2</sub>Cl 가수분해 3000배 가속)와 같은 원리이다.</p>
<p>⑤ 참고·오답: 에피설포늄을 Cl<sup>−</sup>가 고리 탄소 쪽에서 열면 6원 고리로 확장된 3-chlorothiane이 생길 수 있으나, 문헌(biotin 합성)에서는 고리 크기가 유지된 배열 유지 염화물이 얻어졌다. “SOCl<sub>2</sub>는 S<sub>N</sub>i로 배열을 유지한다”는 답은 pyridine 존재 조건(반전이 정상)과 황 없는 대조 실험 결과를 설명하지 못하므로 불충분하다.</p>''',
),
# ---------------------------------------------------------------- 2014A-기입6
dict(
    key='2014A-기입6',
    src='2014학년도 A형 기입형 6번 유형',
    src_topic='propene + HBr/HOOH → 1-bromopropane → 아세틸라이드 SN2 → Hg²⁺ 수화로 2-pentanone',
    change='원 기출(과산화물 효과·아세틸라이드 알킬화)은 다른 문항(2021B-9, 2019A-4)과 겹치므로, 같은 영역의 최고 빈출 핵심인 '
           '“알코올의 술폰산 에스터화(배열 유지) → 같은 기질의 S<sub>N</sub>2(반전) vs 부피 큰 염기의 E2(Hofmann)”로 재구성. '
           '입체(R/S) 판정과 위치선택성을 동시에 묻는다.',
    paper=dict(cite='J. Am. Chem. Soc. 1965, 87, 287–291; J. Am. Chem. Soc. 1965, 87, 5517–5518', book='Klein 7.82, 8.96',
               what='광학 활성 2-octyl 술폰산 에스터의 가용매분해(반전·이중 반전) / 2-butyl–Y + t-BuOK에서 1-butene 주생성, OTs는 cis-2-butene 우세'),
    nobel='',
    body=f'''다음은 (<i>R</i>)-2-octanol로부터 중간 주생성물 <b class="lbltxt">A</b>를 거쳐 최종 주생성물 <b class="lbltxt">B</b>(C<sub>9</sub>H<sub>17</sub>N)와 <b class="lbltxt">C</b>(C<sub>8</sub>H<sub>16</sub>)를 각각 합성하는 반응식이다. (단, 각 단계에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(scheme(M('CCCCCC[C@@H](C)O', '', 15), arrow('TsCl', 'pyridine'), L('A')),
       scheme(L('B'), larrow('NaCN', 'DMSO, 25 ℃'),
              L('A'), arrow('<i>t</i>-BuOK', '<i>t</i>-BuOH, 50 ℃'), L('C')),
       '<div class="chem" style="text-align:center">TsCl = <i>p</i>-toluenesulfonyl chloride</div>')}
<p class="ask"><b class="lbltxt">B</b>의 입체구조를 그리고 카이랄 중심의 절대 배열(<i>R</i>/<i>S</i>)을 쓰시오. 또한 <b class="lbltxt">C</b>의 구조를 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CCCCCC[C@@H](C)OS(=O)(=O)c1ccc(C)cc1', 'A: (R)-2-octyl tosylate', 12)}{M('CCCCCC[C@H](C)C#N', 'B: (S)', 14)}{M('C=CCCCCCC', 'C: 1-octene', 14)}</div>
B = (<i>S</i>)-2-methyloctanenitrile, C = 1-octene''',
    explain='''<p><b>핵심 반응:</b> 알코올 → 토실레이트(C–O 결합 유지, 배열 유지) → 강한 친핵체·약한 염기의 S<sub>N</sub>2(반전) vs 부피 큰 강염기의 E2(Hofmann 위치선택성).</p>
<p>① A: 알코올 O가 TsCl의 S를 공격하고 Cl<sup>−</sup>가 떨어지며 pyridine이 HCl을 받는다. 카이랄 탄소의 C–O 결합은 끊어지지 않으므로 (<i>R</i>)이 유지된다. OH(나쁜 이탈기, HO<sup>−</sup>의 짝산 pK<sub>a</sub> 15.7)가 TsO<sup>−</sup>(짝산 pK<sub>a</sub> ≈ −2.8, 좋은 이탈기)로 바뀐다.</p>
<p>② B: CN<sup>−</sup>는 강한 친핵체이면서 비교적 약한 염기이고, DMSO(극성 비양성자성 용매)는 음이온을 거의 용매화하지 않아 친핵성을 크게 높인다 → 2차 기질이라도 S<sub>N</sub>2가 우세하다. 뒤쪽 공격으로 배열이 반전된다(Walden 반전). CIP: CN(C에 N,N,N) &gt; 헥실 &gt; CH<sub>3</sub> &gt; H이고 CN이 원래 OTs 자리의 우선순위를 그대로 이어받으므로 공간 배열 반전 = 표기도 <i>R</i> → <i>S</i>. 탄소가 하나 늘어난 C<sub>9</sub>H<sub>17</sub>N이 확인된다.</p>
<p>③ C: <i>t</i>-BuO<sup>−</sup>는 부피가 커서 2차 탄소 뒤쪽 공격(S<sub>N</sub>2)을 거의 못 하고 염기로 작용(E2)한다. 내부 C3–H보다 입체 장애가 작은 말단 CH<sub>3</sub>(C1)의 H를 떼는 것이 유리하여 덜 치환된 1-octene(Hofmann 생성물)이 주생성물이다. 논문 데이터에서도 2-butyl–Y/<i>t</i>-BuOK는 모든 이탈기에서 1-butene이 주생성물이었고, 특히 OTs는 이탈기가 크고 산소에 결합해 있어 2-알켄 중에서도 <i>cis</i>가 <i>trans</i>보다 많았다(trans:cis = 0.6). 이 이탈기 크기 효과 때문에 토실레이트는 E2에서 Hofmann 선택성이 할로젠화물보다 더 크게 나타난다.</p>
<p>④ 확장: 같은 (<i>R</i>)-2-octyl 술폰산 에스터를 H<sub>2</sub>O–dioxane에서 가수분해하면 물의 직접 S<sub>N</sub>2로 (<i>S</i>)-2-octanol이 생기지만, dioxane 비율이 높을수록 광학 순도가 떨어진다(100 % 물 → 100 %, 25:75 → 77 %). dioxane O가 먼저 S<sub>N</sub>2(반전)로 옥소늄을 만들고 물이 다시 S<sub>N</sub>2(반전)하는 이중 반전 경로가 (<i>R</i>)-알코올을 섞기 때문이다(Klein 7.82).</p>
<p>⑤ 흔한 오답: (i) A 단계에서 반전을 적용해 B를 (<i>R</i>)로 씀 — 반전은 S<sub>N</sub>2 단계에서 한 번만 일어난다. (ii) C를 Zaitsev 생성물 (<i>E</i>)-2-octene으로 씀 — 부피 큰 염기 조건을 무시한 것이다. (iii) B를 아이소나이트릴(–NC)로 씀 — CN<sup>−</sup>는 탄소 말단으로 S<sub>N</sub>2 한다.</p>''',
),
]
