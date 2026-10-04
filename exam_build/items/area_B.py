"""영역 B: 방향족 치환·다이아조늄 화학 (12문항)."""
from chem import M, L, arrow, varrow, scheme, rows, frame, nmr, ir, spec, plus

BX = '<b class="lbltxt">{}</b>'.format
A_, B_, C_, D_, E_, X_ = (BX(c) for c in 'ABCDEX')
NOTE = '(단, 각 반응에서는 적절한 분리·정제 과정을 수행하였다.)'

ITEMS = [
# ---------------------------------------------------------------- 2026A-10
dict(
    key='2026A-10',
    src='2026학년도 A형 10번',
    src_topic='p-bromotoluene의 벤자인(제거–첨가) 아미노화 → 다이아조화 → Sandmeyer(CuCN)',
    change='위치 선택성이 갈리지 않는 p-치환 벤자인 대신 2-bromoanisole에서 생기는 3-methoxybenzyne을 사용해 '
           '“친핵체가 어느 탄소에 첨가하는가(유발 효과에 의한 카브음이온 안정화)”를 이유로 서술하게 하고, '
           'Sandmeyer 대신 다이아조늄 염의 Pd 촉매 Suzuki 짝지음(2010 노벨상)으로 마무리하도록 변형',
    paper=dict(cite='Org. Lett. 1999, 1, 985–988', book='Klein 19.88',
               what='7-hydroxynitidine 합성: 아릴 브로마이드 + NaNH₂(2 당량) → 벤자인 생성 후 분자 내 탄소 친핵체 첨가(아라인 고리화). '
                    '메톡시기에 인접한 벤자인에서 친핵체가 OMe에서 먼 탄소에 첨가하는 위치 선택성을 단순 모델(2-bromoanisole)로 변환'),
    nobel='2010 노벨 화학상(R. F. Heck·E. Negishi·A. Suzuki — Pd 촉매 교차 짝지음), 1950 노벨 화학상(O. Diels·K. Alder — 벤자인 포획 근거)',
    body=f'''다음은 2-bromoanisole로부터 중간 주생성물 {A_}(C<sub>7</sub>H<sub>9</sub>NO)와 {B_}를 거쳐 최종 주생성물 {C_}(C<sub>13</sub>H<sub>12</sub>O)를 합성하는 반응을 나타낸 것이다. 2-Bromoanisole이 {A_}로 전환될 때 중간체(C<sub>7</sub>H<sub>6</sub>O)를 거친다. {NOTE}
{frame(scheme(M('COc1ccccc1Br', scale=16), arrow('NaNH<sub>2</sub>', 'NH<sub>3</sub>(<i>l</i>), −33 ℃'), L('A')),
       scheme(L('A'), arrow('NaNO<sub>2</sub>, HBF<sub>4</sub>', 'H<sub>2</sub>O, 0 ℃'), L('B'),
              arrow('PhB(OH)<sub>2</sub>', 'Pd(OAc)<sub>2</sub>(촉매)'), L('C')),
       '<div class="chem" style="text-align:center">(Pd 짝지음 단계: CH<sub>3</sub>OH, 25 ℃, 염기 없음)</div>')}
<p class="ask">중간체(C<sub>7</sub>H<sub>6</sub>O)의 구조를 그리시오. 또한 {A_}의 구조를 그리고, {A_}의 위치 이성질체가 아닌 {A_}가 주생성물로 생성되는 이유를 중간체에 대한 친핵체의 첨가 방향과 관련지어 서술하시오. 그리고 {C_}의 구조를 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('COC1=CC=CC#C1', '중간체: 3-methoxybenzyne', 15)}{M('COc1cccc(N)c1', 'A: 3-methoxyaniline', 15)}{M('COc1cccc(-c2ccccc2)c1', 'C: 3-methoxybiphenyl', 14)}</div>
B = 3-methoxybenzenediazonium tetrafluoroborate. 이유: NH<sub>2</sub><sup>−</sup>가 OMe에서 먼 벤자인 탄소(C3)에 첨가해야 생기는 아릴 음이온(sp<sup>2</sup> 카브음이온)이 전기음성도가 큰 O에 인접(C2)하여 유발 효과로 안정화되므로, 이 방향의 첨가만 일어나 <i>m</i>-이성질체가 생긴다.''',
    explain='''<p><b>핵심 반응: 제거–첨가(벤자인) 메커니즘의 위치 선택성 + 아릴다이아조늄 염의 Suzuki–Miyaura 짝지음</b></p>
<p>① 2-bromoanisole에서 Br의 오쏘 수소는 C3–H 하나뿐이다(C1에는 OMe). NH<sub>2</sub><sup>−</sup>가 C3–H를 떼어 내고(Br의 유발 효과로 산성도 증가), 생긴 아릴 음이온이 Br<sup>−</sup>를 내보내 C2≡C3 벤자인, 즉 <b>3-methoxybenzyne</b>(C<sub>7</sub>H<sub>6</sub>O)이 생성된다. 벤자인의 “삼중 결합”의 두 번째 π 결합은 고리 평면 안의 sp<sup>2</sup> 오비탈끼리의 약한 겹침이므로 반응성이 매우 크다.</p>
<p>② NH<sub>2</sub><sup>−</sup>가 C2에 첨가하면 음전하가 C3에, C3에 첨가하면 음전하가 C2(OMe 바로 옆)에 놓인다. 생성되는 카브음이온의 비공유 전자쌍은 고리 평면 안의 sp<sup>2</sup> 오비탈에 있어 π계와 공명하지 못하므로, 공명 효과가 아니라 <b>유발 효과</b>가 결정적이다. 전기음성도가 큰 O가 붙은 탄소에 인접한 음전하(C2)가 더 안정하므로 첨가는 C3에서 일어나고, NH<sub>3</sub>가 C2를 양성자화하여 <b>3-methoxyaniline(<i>m</i>-anisidine)</b>만 얻는다. (흔한 오답: Br이 있던 자리에 NH<sub>2</sub>가 들어간 <i>o</i>-anisidine — 직접 치환으로 착각한 경우. 이 반응은 <i>cine</i> 치환이다.)</p>
<p>③ 논문(Klein 19.88) 연결: 7-hydroxynitidine 합성에서도 NaNH<sub>2</sub>가 C5–Br의 오쏘 C6–H를 떼어 C5≡C6 아라인을 만들고, 나프틸 카브음이온이 OMe(C4)에서 먼 C6에 첨가하여 음전하가 OMe 옆 C5에 놓인다 — 같은 규칙이다.</p>
<p>④ NaNO<sub>2</sub>/HBF<sub>4</sub>: HNO<sub>2</sub> → NO<sup>+</sup>, 아민 N이 NO<sup>+</sup>를 공격 → N-나이트로소아민 → 토토머화·탈수 → ArN<sub>2</sub><sup>+</sup>. 짝음이온이 BF<sub>4</sub><sup>−</sup>이면 다이아조늄 염이 비교적 안정한 고체로 분리된다(<b>B</b> = 3-MeOC<sub>6</sub>H<sub>4</sub>N<sub>2</sub><sup>+</sup> BF<sub>4</sub><sup>−</sup>).</p>
<p>⑤ Suzuki 짝지음: Pd(0)가 Ar–N<sub>2</sub><sup>+</sup> 결합에 <b>산화성 첨가</b>(N<sub>2</sub> 방출, Ar–Pd(II)<sup>+</sup>) → PhB(OH)<sub>2</sub>와 <b>금속 교환</b>(Ar–Pd–Ph) → <b>환원성 제거</b>로 Ar–Ph 결합 형성, Pd(0) 재생. N<sub>2</sub>가 매우 좋은 이탈기이므로 아릴 할라이드보다 산화성 첨가가 쉽고, 양이온성 Pd 중간체가 금속 교환을 쉽게 하므로 염기 없이 실온에서 진행된다. <b>C</b> = 3-methoxybiphenyl(C<sub>13</sub>H<sub>12</sub>O).</p>
<p>⑥ 벤자인 존재의 증거: 같은 조건에서 furan을 넣으면 벤자인이 친다이엔체로 [4+2] Diels–Alder 고리화 첨가하여 5-methoxy-1,4-dihydro-1,4-epoxynaphthalene(C<sub>11</sub>H<sub>10</sub>O<sub>2</sub>)이 포획된다.</p>''',
),
# ---------------------------------------------------------------- 2025A-10
dict(
    key='2025A-10',
    src='2025학년도 A형 10번',
    src_topic='톨루엔 염소화 → KMnO₄ 산화 → 아마이드 → Hofmann 자리옮김(아이소사이아네이트 중간체)',
    change='벤젠 고리 대신 피리딘 고리(2-chloro-5-methylpyridine)에서 곁사슬 산화 → 아마이드 → Hofmann 자리옮김을 수행하고, '
           '같은 산에서 논문 경로(아마이드 → LiAlH₄ 환원)로 2차 아민을 만드는 경로를 병치하여 '
           '“탄소 1개를 잃는 아민 합성(Hofmann)”과 “탄소 수를 유지하는 아민 합성(아마이드 환원)”을 비교하도록 변형',
    paper=dict(cite='Bioorg. Med. Chem. Lett. 2006, 16, 2013–2016', book='Klein 23.90',
               what='니코틴 유사 진통제 후보: 6-chloronicotinic acid → SOCl₂ → cyclopentylamine → 과량 LiAlH₄ → '
                    'N-[(6-chloropyridin-3-yl)methyl]cyclopentanamine'),
    nobel='',
    body=f'''다음은 2-chloro-5-methylpyridine으로부터 중간 주생성물 {A_}(C<sub>6</sub>H<sub>4</sub>ClNO<sub>2</sub>)를 거쳐 두 가지 아민 {D_}(C<sub>5</sub>H<sub>5</sub>ClN<sub>2</sub>)와 {E_}(C<sub>11</sub>H<sub>15</sub>ClN<sub>2</sub>)를 합성하는 반응을 나타낸 것이다. {C_}가 {D_}로 전환되는 과정에서 중간체(C<sub>6</sub>H<sub>3</sub>ClN<sub>2</sub>O)가 생성된다. {NOTE}
{frame(scheme(M('Cc1ccc(Cl)nc1', scale=16), arrow('1) KMnO<sub>4</sub>, H<sub>2</sub>O, 가열', '2) H<sub>3</sub>O<sup>+</sup>'), L('A')),
       '<div class="ft">[경로 1]</div>',
       scheme(L('A'), arrow('1) SOCl<sub>2</sub>', '2) NH<sub>3</sub>(과량)'), L('C'), arrow('1) Br<sub>2</sub>, NaOH, H<sub>2</sub>O', '2) 가열'), L('D')),
       '<div class="ft">[경로 2]</div>',
       scheme(L('A'), arrow('1) SOCl<sub>2</sub>', '2) <i>c</i>-C<sub>5</sub>H<sub>9</sub>NH<sub>2</sub>'), L('F'), arrow('1) LiAlH<sub>4</sub>(과량)', '2) H<sub>2</sub>O'), L('E')),
       '<div class="chem" style="text-align:center"><i>c</i>-C<sub>5</sub>H<sub>9</sub>NH<sub>2</sub> = cyclopentylamine(2 당량)</div>')}
<p class="ask">{A_}의 구조를 그리시오. 또한 {C_}가 {D_}로 전환되는 과정에서 생성되는 중간체(C<sub>6</sub>H<sub>3</sub>ClN<sub>2</sub>O)와 {D_}의 구조를 각각 그리고, {E_}의 구조를 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('OC(=O)c1ccc(Cl)nc1', 'A: 6-chloronicotinic acid', 15)}{M('O=C=Nc1ccc(Cl)nc1', '중간체: 아이소사이아네이트', 15)}{M('Nc1ccc(Cl)nc1', 'D: 6-chloropyridin-3-amine', 15)}{M('Clc1ccc(CNC2CCCC2)cn1', 'E', 14)}</div>
(C = 6-chloronicotinamide, F = 6-chloro-N-cyclopentylnicotinamide C<sub>11</sub>H<sub>13</sub>ClN<sub>2</sub>O, E = N-[(6-chloropyridin-3-yl)methyl]cyclopentanamine)''',
    explain='''<p><b>핵심 반응: Hofmann 자리옮김(아이소사이아네이트 경유, 탄소 1개 손실) vs 아마이드의 LiAlH<sub>4</sub> 환원(탄소 수 유지)</b></p>
<p>① KMnO<sub>4</sub>는 벤질(여기서는 피리딜메틸) 위치에 C–H가 있는 알킬기를 COOH로 산화한다. 피리딘 고리 자체는 전자가 부족해 산화에 강하다. 산 처리 후 <b>A</b> = 6-chloronicotinic acid(C<sub>6</sub>H<sub>4</sub>ClNO<sub>2</sub>).</p>
<p>② [경로 1] SOCl<sub>2</sub> → 산 염화물, 과량 NH<sub>3</sub> → 1차 아마이드 <b>C</b>(C<sub>6</sub>H<sub>5</sub>ClN<sub>2</sub>O). Br<sub>2</sub>/NaOH: N–H 탈양성자화 → N-브로민화(RCONHBr) → 두 번째 N–H 탈양성자화 → 피리딜기가 C에서 N으로 1,2-이동하면서 Br<sup>−</sup>가 동시에 떨어져 <b>아이소사이아네이트</b>(Ar–N=C=O, C<sub>6</sub>H<sub>3</sub>ClN<sub>2</sub>O) 생성. 이동기는 결합 전자쌍과 함께 이동하며 이동 탄소의 배열은 유지된다.</p>
<p>③ 물/OH<sup>−</sup>가 N=C=O 탄소에 첨가 → 카밤산(ArNHCOOH) → 탈카복실화(CO<sub>2</sub> 손실) → <b>D</b> = 6-chloropyridin-3-amine. 카보닐 탄소가 CO<sub>2</sub>로 빠지므로 <b>탄소 수가 1 감소</b>(C<sub>6</sub> → C<sub>5</sub>)하고 NH<sub>2</sub>는 원래 카복실기가 붙어 있던 고리 탄소에 직접 결합한다.</p>
<p>④ [경로 2](논문) 산 염화물 + cyclopentylamine(2 당량: 1 당량은 HCl 포착) → 2차 아마이드 <b>F</b> → LiAlH<sub>4</sub>: 하이드라이드 첨가 → 알루미늄 알콕사이드가 이탈하면서 이미늄 이온 형성 → 두 번째 하이드라이드 첨가 → C=O가 CH<sub>2</sub>로 바뀐 2차 아민 <b>E</b>(C<sub>11</sub>H<sub>15</sub>ClN<sub>2</sub>). 탄소 수 유지, 아미노기는 CH<sub>2</sub>를 사이에 두고 고리에 연결.</p>
<p>⑤ 피리딘 C2의 Cl은 LiAlH<sub>4</sub>, Br<sub>2</sub>/NaOH 조건에서 보존된다. 흔한 오답: D를 Ar–CH<sub>2</sub>NH<sub>2</sub>(탄소 보존)로 그리거나, 중간체를 카밤산(C<sub>6</sub>H<sub>5</sub>ClN<sub>2</sub>O<sub>2</sub>)으로 그리는 것 — 분자식 C<sub>6</sub>H<sub>3</sub>ClN<sub>2</sub>O는 아이소사이아네이트만 만족한다.</p>''',
),
# ---------------------------------------------------------------- 2024A-10
dict(
    key='2024A-10',
    src='2024학년도 A형 10번',
    src_topic='p-X-chlorobenzene + NaOCH₃ SNAr 속도(NO₂ > CF₃ > H), Meisenheimer 착물, 이어지는 FC 알킬화 위치 선택성',
    change='두 할로젠(F, Cl)이 모두 NO₂의 오쏘 자리에 있는 기질을 사용해, 이탈기 능력(Cl > F)과 반대로 F가 치환되는 사실로부터 '
           '“첨가 단계가 속도 결정 단계”임을 논증하게 하고, 친핵체를 탄소 친핵체(아세틸라이드)로 바꿈',
    paper=dict(cite='Org. Lett. 2007, 9, 2741–2743', book='Klein 19.85',
               what='1-chloro-3-fluoro-2-nitrobenzene + sodium (4-methoxyphenyl)acetylide → F만 치환된 아릴알카인(전이 금속 없는 SNAr 알카인화)'),
    nobel='',
    body=f'''다음은 1-chloro-3-fluoro-2-nitrobenzene과 소듐 아세틸라이드의 반응으로 주생성물 {A_}(C<sub>15</sub>H<sub>10</sub>ClNO<sub>3</sub>)를 얻는 반응을 나타낸 것이다. 이 반응은 음이온 중간체를 거쳐 진행된다. {NOTE}
{frame(scheme(M('O=[N+]([O-])c1c(F)cccc1Cl', scale=17), arrow('Ar–C≡C<sup>−</sup> Na<sup>+</sup>', 'THF'), L('A')),
       '<div class="chem" style="text-align:center">Ar = 4-CH<sub>3</sub>OC<sub>6</sub>H<sub>4</sub>(4-methoxyphenyl)</div>')}
<p class="ask">{A_}의 구조를 그리시오. 또한 {A_}가 생성될 때 거치는 음이온 중간체의 공명 구조 중 음전하가 나이트로기의 산소에 있는 구조를 그리시오. 그리고 할로젠 음이온의 이탈기 능력은 Cl<sup>−</sup>가 F<sup>−</sup>보다 큰데도 F가 치환되는 이유를 속도 결정 단계와 관련지어 서술하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('COc1ccc(C#Cc2cccc(Cl)c2[N+](=O)[O-])cc1', 'A', 14)}{M('COc1ccc(cc1)C#CC1(F)C=CC=C(Cl)C1=[N+]([O-])[O-]', '중간체(Meisenheimer 착물)', 14)}</div>
이유: SNAr은 첨가–제거 메커니즘이며 친핵체가 고리에 첨가해 Meisenheimer 착물을 만드는 단계가 속도 결정 단계이다. C–X 결합 절단은 그 뒤의 빠른 단계이므로 이탈기 능력은 속도에 거의 영향을 주지 않는다. 전기음성도가 가장 큰 F는 붙은 탄소(ipso)를 더 δ+로 만들고, 유발 효과로 음이온성 전이 상태·중간체를 안정화하므로 C–F 탄소에 대한 첨가가 더 빠르다.''',
    explain='''<p><b>핵심 반응: 친핵성 방향족 치환(SNAr, 첨가–제거)과 Meisenheimer 착물</b></p>
<p>① SNAr의 3조건: 강한 전자 끄는 기(NO<sub>2</sub>), 이탈기, 그리고 EWG가 이탈기의 오쏘/파라에 위치. 이 기질은 F와 Cl이 <b>모두</b> NO<sub>2</sub>의 오쏘 자리에 있으므로 활성화 정도(공명)는 같고, 차이는 할로젠 자체의 효과뿐이다.</p>
<p>② 메커니즘: 아세틸라이드 탄소가 C–F 탄소(ipso)를 공격 → sp<sup>3</sup> 탄소를 가진 사이클로헥사다이엔일 음이온(Meisenheimer 착물). 음전하는 NO<sub>2</sub>가 붙은 탄소(오쏘)와 파라 탄소로 비편재화되고, NO<sub>2</sub>의 공명(−M)으로 산소까지 퍼진다(문제에서 요구한 구조: C=N<sup>+</sup>(O<sup>−</sup>)O<sup>−</sup>). 이어 F<sup>−</sup>가 떨어지며 방향족성이 회복된다.</p>
<p>③ 속도 결정 단계는 방향족성이 깨지는 ①의 첨가 단계(흡열적)이다. 이 단계의 전이 상태에서는 C–X 결합이 아직 끊어지지 않으므로, 이탈기 능력(I > Br > Cl > F)이 아니라 ipso 탄소의 친전자성과 음전하 안정화가 속도를 좌우한다. 따라서 SNAr의 할로젠 반응성은 <b>F ≫ Cl ≈ Br > I</b>로 S<sub>N</sub>2와 반대이다. 만약 C–X 절단이 속도 결정 단계라면 Cl이 치환된 생성물(C<sub>15</sub>H<sub>10</sub>FNO<sub>3</sub>)이 얻어졌을 것이다 — 이 생성물의 부재가 메커니즘의 증거이다.</p>
<p>④ <b>A</b> = 1-chloro-3-[(4-methoxyphenyl)ethynyl]-2-nitrobenzene(C<sub>15</sub>H<sub>10</sub>ClNO<sub>3</sub>). 남은 Cl은 이후 다른 변환(예: Pd 짝지음)에 쓸 수 있는 손잡이가 된다. 이 반응은 Pd/Cu를 쓰는 Sonogashira 짝지음 없이 아릴알카인을 만드는 대안이다.</p>
<p>⑤ 흔한 오답: Cl이 치환된 구조, 또는 NO<sub>2</sub>가 치환된 구조. 또 중간체의 음전하를 NO<sub>2</sub>와 메타 관계인 탄소에 두는 것(불가능한 공명)도 틀린다.</p>''',
),
# ---------------------------------------------------------------- 2024A-11
dict(
    key='2024A-11',
    src='2024학년도 A형 11번',
    src_topic='다이아조늄 → 페놀, Williamson 알릴 에터, 방향족 Claisen 자리옮김, 산 촉매 고리화(dihydrobenzofuran)',
    change='두 오쏘 자리가 모두 메틸로 막힌 페놀(2,6-dimethylphenol)과 (E)-크로틸 에터를 사용하여, 오쏘 Claisen 후 Cope 자리옮김이 '
           '이어지는 “파라-Claisen 자리옮김”을 묻고, 곁사슬이 두 번 뒤집혀(이중 알릴 전위) 가지 없는 사슬로 돌아오는 것을 NMR 단서로 판단하게 함',
    paper=dict(cite='Tetrahedron Lett. 2010, 51, 4494–4496', book='Klein 20.88',
               what='furo[2,3-b]indole 합성: 2-nitrobenzaldehyde의 알릴옥시메틸렌 Wittig → 알릴 바이닐 에터 → 가열 [3,3] Claisen 자리옮김'),
    nobel='',
    body=f'''다음은 2,6-dimethylaniline으로부터 중간 주생성물 {B_}(C<sub>8</sub>H<sub>10</sub>O)와 {C_}(C<sub>12</sub>H<sub>16</sub>O)를 거쳐 최종 주생성물 {D_}(C<sub>12</sub>H<sub>16</sub>O)를 합성하는 반응을 나타낸 것이다. {B_}와 {D_}의 IR 스펙트럼은 3400 cm<sup>−1</sup> 부근에서 강하고 넓은 띠를 보이지만 {C_}는 그렇지 않다. {D_}의 <sup>1</sup>H NMR 스펙트럼에서 방향족 수소의 피크는 1개(2H, s)이며, 1.0~1.3 ppm에서 이중선(doublet)은 나타나지 않는다. {NOTE}
{frame(scheme(M('Cc1cccc(C)c1N', scale=16), arrow('1) NaNO<sub>2</sub>, H<sub>2</sub>SO<sub>4</sub>, 0 ℃', '2) H<sub>2</sub>O, 가열'), L('B')),
       scheme(L('B'), arrow('(<i>E</i>)-CH<sub>3</sub>CH=CHCH<sub>2</sub>Br', 'K<sub>2</sub>CO<sub>3</sub>, 아세톤'), L('C'), arrow('200 ℃', ''), L('D')))}
<p class="ask">{C_}와 {D_}의 구조를 각각 그리시오. 또한 {C_}가 {D_}로 전환되는 첫 단계에서 생성되는 비방향족 중간체(C<sub>12</sub>H<sub>16</sub>O)의 구조를 그리고, {D_}에서 곁사슬이 고리의 파라 자리에 가지 없이 결합하게 되는 이유를 페리고리 반응의 종류와 관련지어 서술하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('C/C=C/COc1c(C)cccc1C', 'C', 15)}{M('C=CC(C)C1(C)C=CC=C(C)C1=O', '중간체', 15)}{M('C/C=C/Cc1cc(C)c(O)c(C)c1', 'D', 15)}</div>
B = 2,6-dimethylphenol, C = 2-[(<i>E</i>)-but-2-enyloxy]-1,3-dimethylbenzene, 중간체 = 6-(but-3-en-2-yl)-2,6-dimethylcyclohexa-2,4-dien-1-one, D = 4-[(<i>E</i>)-but-2-enyl]-2,6-dimethylphenol.<br>
이유: 첫 [3,3] Claisen 자리옮김은 오쏘 탄소로 일어나며 알릴 말단이 뒤집혀(1-methylallyl) 붙지만, 오쏘 탄소에 CH<sub>3</sub>가 있어 토토머화로 방향족성을 회복할 수 없다. 이 다이엔온이 두 번째 [3,3] 자리옮김(Cope)을 하여 곁사슬을 파라 탄소로 옮기면서 다시 한번 뒤집으므로 원래의 크로틸(가지 없는 but-2-enyl) 형태로 파라에 붙고, 파라 C–H의 토토머화로 방향족 페놀이 된다.''',
    explain='''<p><b>핵심 반응: 다이아조늄 가수분해 → Williamson 에터 합성 → 방향족 Claisen 자리옮김(파라-Claisen = Claisen + Cope)</b></p>
<p>① 2,6-dimethylaniline → ArN<sub>2</sub><sup>+</sup> → 가열 수용액에서 N<sub>2</sub>가 떨어진 아릴 양이온을 물이 포착 → <b>B</b> = 2,6-dimethylphenol(O–H, 3400 cm<sup>−1</sup>).</p>
<p>② K<sub>2</sub>CO<sub>3</sub>가 페놀(p<i>K</i><sub>a</sub> ≈ 10)을 페녹사이드로 만들고 1차 알릴 브로마이드에 S<sub>N</sub>2 → <b>C</b> = 크로틸 아릴 에터(O–H 없음). C=C 기하는 유지(<i>E</i>).</p>
<p>③ 200 ℃: 의자형 6원 고리 전이 상태의 협동 [3,3] 시그마 결합 자리옮김. O–CH<sub>2</sub> 결합이 끊어지고 크로틸의 CH(CH<sub>3</sub>) 말단(γ 탄소)이 오쏘 탄소와 결합 → 알릴기가 <b>뒤집혀</b> 1-methylallyl(but-3-en-2-yl)로 붙은 cyclohexa-2,4-dienone(중간체, C<sub>12</sub>H<sub>16</sub>O, 방향족 아님, C=O). 오쏘 탄소에 이미 CH<sub>3</sub>가 있어 H가 없으므로 토토머화할 수 없다.</p>
<p>④ 이 다이엔온에서 C6(사차 탄소)–C(H)(CH<sub>3</sub>) 결합, 고리 C=C, 곁사슬 C=C가 1,5-다이엔을 이루므로 두 번째 [3,3](Cope) 자리옮김이 일어나 곁사슬 말단 CH<sub>2</sub>가 파라 탄소(C4)와 결합하고 사슬은 다시 뒤집혀 –CH<sub>2</sub>CH=CHCH<sub>3</sub>가 된다. 의자형 전이 상태에서 CH<sub>3</sub>가 평면형(equatorial) 자리를 차지하므로 (<i>E</i>)-알켄이 주로 생긴다. 파라 C–H가 토토머화되며 방향족 페놀 <b>D</b>로 회복 — 이것이 반응의 열역학적 구동력이다.</p>
<p>⑤ NMR 단서: 방향족 H 1종(2H, s) → 3,5-H가 동등한 2,4,6-삼치환 페놀(파라 생성물). 1.0~1.3 ppm 이중선 없음 → –CH(CH<sub>3</sub>)CH=CH<sub>2</sub>(가지 사슬)가 아니라 CH<sub>3</sub>CH= (≈1.7 ppm, d이지만 알릴 위치) 형태의 가지 없는 사슬. 흔한 오답: 오쏘 생성물(오쏘가 막혀 불가), 또는 파라에 1-methylallyl이 붙은 구조(한 번만 뒤집힌 것으로 착각).</p>''',
),
# ---------------------------------------------------------------- 2023A-2
dict(
    key='2023A-2',
    src='2023학년도 A형 2번',
    src_topic='아세트아닐라이드 나이트로화·탈보호 → 다이아조늄 → 살리실산과 아조 짝지음(alizarin yellow R)',
    change='아닐린의 술폰화(파라, 열역학 조절)로 술파닐산을 만든 뒤 다이아조화하고, 짝지음 상대를 2-naphthol로 바꾸어 '
           '“나프톨의 C1(α) 위치 선택성”을 묻는 산성 아조 염료(Orange II) 합성으로 변형',
    paper=dict(cite='Anal. Chem. 2013, 85, 831–836', book='Klein 15.69',
               what='섬유 산성 염료(술폰산염 발색단을 가진 안트라퀴논 염료)의 질량 분석 확인 — 본 문항은 같은 “술폰산염 산성 염료” 계열의 아조 염료 합성으로 모델화'),
    nobel='',
    body=f'''다음은 아닐린으로부터 중간 주생성물 {A_}(C<sub>6</sub>H<sub>7</sub>NO<sub>3</sub>S)를 거쳐 산성 아조 염료 {B_}(C<sub>16</sub>H<sub>11</sub>N<sub>2</sub>NaO<sub>4</sub>S)를 합성하는 반응을 나타낸 것이다. {B_}는 소듐 염으로 분리하였다. {NOTE}
{frame(scheme(M('Nc1ccccc1', scale=16), arrow('진한 H<sub>2</sub>SO<sub>4</sub>', '180 ℃'), L('A'),
              arrow('1) NaNO<sub>2</sub>, HCl, 0~5 ℃', '2) 2-naphthol, NaOH'), L('B')),
       scheme('<span class="chem">2-naphthol =</span>', M('Oc1ccc2ccccc2c1', scale=15)))}
<p class="ask">{A_}와 {B_}의 구조를 각각 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('Nc1ccc(cc1)S(=O)(=O)O', 'A: sulfanilic acid', 15)}{M('[Na+].[O-]S(=O)(=O)c1ccc(cc1)/N=N/c1c(O)ccc2ccccc12', 'B: Orange II', 13)}</div>
(A는 실제로 쯔비터이온 H<sub>3</sub>N<sup>+</sup>–C<sub>6</sub>H<sub>4</sub>–SO<sub>3</sub><sup>−</sup>로 존재. B = sodium 4-[(2-hydroxynaphthalen-1-yl)diazenyl]benzenesulfonate)''',
    explain='''<p><b>핵심 반응: 방향족 술폰화(열역학 조절) → 다이아조화 → 아조 짝지음(나프톨 C1 위치 선택성)</b></p>
<p>① 아닐린 + 진한 H<sub>2</sub>SO<sub>4</sub> → 아닐리늄 황산수소염 → 고온(180 ℃)에서 술폰화. 술폰화는 가역적이므로 고온에서는 입체 장애가 작고 열역학적으로 가장 안정한 <b>파라</b> 생성물이 축적된다. <b>A</b> = 4-aminobenzenesulfonic acid(C<sub>6</sub>H<sub>7</sub>NO<sub>3</sub>S).</p>
<p>② NaNO<sub>2</sub>/HCl, 0~5 ℃: NO<sup>+</sup>에 의한 N-나이트로소화 → 탈수 → ArN<sub>2</sub><sup>+</sup>(술포네이트와 함께 쯔비터이온 <sup>−</sup>O<sub>3</sub>S–C<sub>6</sub>H<sub>4</sub>–N<sub>2</sub><sup>+</sup>). 저온 유지는 N<sub>2</sub> 손실(페놀 생성)을 막기 위함이다.</p>
<p>③ 다이아조늄 이온은 약한 친전자체이므로 매우 활성화된 고리(나프톡사이드)와만 반응한다. NaOH는 2-naphthol(p<i>K</i><sub>a</sub> ≈ 9.5)을 나프톡사이드로 바꿔 친핵성을 높인다. 2-나프톡사이드는 <b>C1</b>에서 공격하는데, C1 공격 σ-착물은 다른 벤젠 고리의 방향족 6전자를 그대로 유지한 공명 구조를 가지면서 O<sup>−</sup>의 공여로 안정화된다(C3 공격은 옆 고리의 방향족성을 깨야 O의 공명 안정화를 받음). 탈양성자화로 방향족성 회복 → 아조 화합물.</p>
<p>④ <b>B</b> = Orange II(Acid Orange 7). 술폰산염기는 물 용해도와 섬유(양모·나일론의 양이온 자리)와의 이온 결합을 제공하는 “산성 염료”의 특징이다. 아조 결합으로 두 방향족계가 콘쥬게이션되어 가시광(주황)을 흡수한다.</p>
<p>⑤ 흔한 오답: C3 또는 C6에 짝지음한 구조, 술폰산기를 메타에 둔 A(아닐리늄의 메타 지향과 혼동 — 고온 가역 조건에서는 파라가 주생성물).</p>''',
),
# ---------------------------------------------------------------- 2022B-8
dict(
    key='2022B-8',
    src='2022학년도 B형 8번',
    src_topic='다이아조늄→페놀; SNAr 위치 활성화; FC 알킬화의 탄소 양이온 재배열 vs FC 아실화–Clemmensen',
    change='분자 간 FC 알킬화의 재배열(1-chloro-2-methylpropane → tert-butylbenzene)과 아실화–환원에 의한 isobutylbenzene(이부프로펜 원료) 합성을 묻고, '
           '논문의 “에틸렌 + 아실륨 → 분자 내 FC 알킬화” 2-tetralone 합성을 추가하여 아실륨·탄소 양이온의 운명을 종합적으로 판단하게 함',
    paper=dict(cite='J. Org. Chem. 2012, 77, 5503–5514', book='Klein 19.84',
               what='아미노테트랄린(항우울제 후보) 합성: 2-(2-bromo-5-methylphenyl)acetyl chloride + 에틸렌/AlCl₃ → 8-bromo-5-methyl-2-tetralone'),
    nobel='',
    body=f'''다음은 방향족 화합물의 Friedel–Crafts 반응을 나타낸 것이다. {NOTE}
{frame('<div class="ft">[반응 1]</div>',
       scheme(M('O=C(Cl)Cc1cc(C)ccc1Br', scale=15), arrow('H<sub>2</sub>C=CH<sub>2</sub>, AlCl<sub>3</sub>', 'CH<sub>2</sub>Cl<sub>2</sub>'), L('A')),
       '<div class="ft">[반응 2]</div>',
       scheme(M('c1ccccc1', scale=15), arrow('(CH<sub>3</sub>)<sub>2</sub>CHCH<sub>2</sub>Cl', 'AlCl<sub>3</sub>'), L('B')),
       '<div class="chem" style="margin-top:4px">&lt;보 기&gt; (CH<sub>3</sub>)<sub>2</sub>CHCOCl, (CH<sub>3</sub>)<sub>2</sub>C=CH<sub>2</sub>, AlCl<sub>3</sub>, H<sub>3</sub>PO<sub>4</sub>, NaBH<sub>4</sub>, Zn(Hg)/HCl</div>')}
<p class="ask">[반응 1]에서 {A_}(C<sub>11</sub>H<sub>11</sub>BrO)의 구조를 그리시오. [반응 2]에서 단일 주생성물 {B_}(C<sub>10</sub>H<sub>14</sub>)의 구조를 그리고, {B_}가 isobutylbenzene이 아닌 이유를 서술하시오. 또한 &lt;보기&gt;에서 시약을 골라 벤젠으로부터 isobutylbenzene(이부프로펜의 원료)을 합성하는 가장 적절한 반응식을 2단계로 쓰시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('O=C1CCc2c(C)ccc(Br)c2C1', 'A: 8-bromo-5-methyl-2-tetralone', 15)}{M('CC(C)(C)c1ccccc1', 'B: tert-butylbenzene', 15)}</div>
이유: AlCl<sub>3</sub>와 1차 할로젠화 알킬의 착물에서 C–Cl이 이온화되는 동시에 이웃 C–H의 하이드라이드가 1,2-이동하여 안정한 3차 탄소 양이온((CH<sub>3</sub>)<sub>3</sub>C<sup>+</sup>)이 생성되고, 이것이 벤젠을 공격하기 때문이다.<br>
합성: ① 벤젠 + (CH<sub>3</sub>)<sub>2</sub>CHCOCl, AlCl<sub>3</sub> → PhCOCH(CH<sub>3</sub>)<sub>2</sub> (아실륨은 재배열하지 않음) ② Zn(Hg)/HCl(Clemmensen 환원) → PhCH<sub>2</sub>CH(CH<sub>3</sub>)<sub>2</sub>''',
    explain='''<p><b>핵심 반응: Friedel–Crafts 아실화(아실륨, 재배열 없음) vs 알킬화(탄소 양이온 재배열) + Clemmensen 환원</b></p>
<p>① [반응 1] AlCl<sub>3</sub>가 산 염화물의 Cl을 떼어 공명 안정화된 아실륨 이온(R–C≡O<sup>+</sup>)을 만든다. 아실륨이 자기 고리를 공격하면 4원 고리가 되어 불가능하고, 다른 분자의 고리(Br으로 불활성화)보다 과량 존재하는 에틸렌의 π 전자가 아실륨을 공격하는 지방족 아실화가 먼저 일어나 ArCH<sub>2</sub>C(=O)CH<sub>2</sub>CH<sub>2</sub><sup>+</sup>(또는 Cl<sup>−</sup>가 포착한 β-클로로케톤, AlCl<sub>3</sub>로 재이온화)가 생긴다.</p>
<p>② 이 1차 양이온 등가체는 하이드라이드 이동을 해도 카보닐 옆(α) 양이온이 되어 오히려 불안정하므로 재배열하지 않고, 6원 고리를 닫을 수 있는 방향족 탄소(CH<sub>2</sub>의 오쏘, Br이 없는 쪽 = CH<sub>3</sub>의 오쏘로 활성화)를 분자 내 FC 알킬화로 공격 → 아레늄 이온 → 탈양성자화 → <b>A</b> = 8-bromo-5-methyl-3,4-dihydronaphthalen-2(1<i>H</i>)-one(C<sub>11</sub>H<sub>11</sub>BrO). CH<sub>2</sub>의 다른 오쏘(C–Br)는 치환 불가.</p>
<p>③ [반응 2] 1-chloro-2-methylpropane은 1차 할로젠화물이라 자유 1차 양이온을 만들지 않지만, AlCl<sub>3</sub> 착물의 이온화와 2번 탄소 H의 1,2-하이드라이드 이동이 함께 일어나 3차 양이온이 되고, 이 친전자체가 벤젠과 반응하므로 isobutylbenzene 대신 <b>tert-butylbenzene</b>이 주생성물이다. (보기의 (CH<sub>3</sub>)<sub>2</sub>C=CH<sub>2</sub>/H<sub>3</sub>PO<sub>4</sub>도 Markovnikov 양성자화로 같은 t-Bu<sup>+</sup>를 주므로 오답.)</p>
<p>④ 재배열 없는 직쇄 알킬 도입: 아실륨 이온은 C≡O<sup>+</sup> 공명으로 안정하여 재배열하지 않고, 생성된 아릴 케톤은 고리를 불활성화하므로 다중 치환도 없다. 이어서 Zn(Hg)/HCl(Clemmensen)으로 C=O → CH<sub>2</sub>. NaBH<sub>4</sub>는 알코올까지만 환원하므로 부적절하다.</p>
<p>⑤ 이부프로펜 공정(BHC)은 isobutylbenzene의 FC 아세틸화로 시작한다 — 순서상 isobutyl기를 먼저 정확히 만들어야 하므로 ④의 아실화–환원이 산업적으로도 핵심이다.</p>''',
),
# ---------------------------------------------------------------- 2020A-4
dict(
    key='2020A-4',
    src='2020학년도 A형 4번',
    src_topic='아닐리늄 + 아세트산 무수물/NaOAc(완충) → 아세트아닐라이드; N–H⁺, O–H, sp C–H 산도 비교',
    change='아민 질소의 염기도(=짝산의 p<i>K</i><sub>a</sub>)를 판단하는 핵심 개념을 유지하되, 한 분자 안에 성질이 다른 세 질소(구아니딘, 피리딘형, 피롤/인돌형)를 가진 '
           '천연물 β-carboline에 HCl을 가해 어느 질소가 양성자화되는지 판단하도록 변형',
    paper=dict(cite='J. Nat. Prod. 2011, 74, 1972–1979', book='Klein 18.72',
               what='뉴질랜드 멍게(ascidian)에서 분리한 항말라리아 7-bromo-1-(4-guanidinobutyl)-β-carboline의 질소 염기도와 2 HCl 염'),
    nobel='',
    body=f'''다음은 뉴질랜드 멍게에서 분리한 항말라리아 알칼로이드 {X_}(C<sub>16</sub>H<sub>18</sub>BrN<sub>5</sub>)를 HCl(2 당량)과 반응시켜 염 {B_}를 얻는 반응을 나타낸 것이다. {NOTE}
{frame(scheme(M('NC(=N)NCCCCc1nccc2c1[nH]c1cc(Br)ccc12', scale=14), arrow('HCl(2 당량)', 'CH<sub>3</sub>OH'), L('B')),
       '<div class="chem">㉠ 구아니딘기의 C=NH 질소　㉡ 피리딘 고리의 질소(N2)　㉢ 인돌 고리의 N–H 질소(N9)</div>')}
<p class="ask">{B_}의 구조를 그리시오. 또한 ㉠~㉢의 질소가 각각 양성자화된 짝산의 p<i>K</i><sub>a</sub>만을 고려할 때, 그 값이 작은 것부터 큰 순서대로 나열하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('NC(=[NH2+])NCCCCc1[nH+]ccc2c1[nH]c1cc(Br)ccc12.[Cl-].[Cl-]', 'B (이염산염)', 13)}</div>
p<i>K</i><sub>a</sub>(짝산): ㉢ &lt; ㉡ &lt; ㉠''',
    explain='''<p><b>핵심 개념: 질소 비공유 전자쌍의 위치(방향족 π계 참여 여부, 혼성)와 짝산의 공명 안정화로 결정되는 아민 염기도</b></p>
<p>① ㉠ 구아니딘: 양성자화된 구아니디늄 이온은 양전하가 세 질소에 고르게 비편재화되는 공명(Y자형 공명)으로 크게 안정화되어 짝산 p<i>K</i><sub>a</sub> ≈ 13으로 가장 강한 염기이다.</p>
<p>② ㉡ 피리딘형 N: 비공유 전자쌍이 고리 평면의 sp<sup>2</sup> 오비탈에 있고 방향족 6π계에 참여하지 않으므로 양성자를 받을 수 있다(피리디늄 p<i>K</i><sub>a</sub> ≈ 5; β-carboline은 인돌 N의 전자 공여로 약 7 정도). sp<sup>2</sup>는 s 성질이 커 sp<sup>3</sup> 아민보다 약한 염기이다.</p>
<p>③ ㉢ 인돌(피롤형) N–H: 비공유 전자쌍이 p 오비탈에서 방향족 π계(4n+2)의 일부이므로 양성자화하면 방향족성이 깨진다. 짝산 p<i>K</i><sub>a</sub> ≈ −3 수준으로 사실상 염기가 아니다.</p>
<p>④ 따라서 HCl 2 당량은 가장 염기성이 큰 ㉠과 그 다음 ㉡을 차례로 양성자화하여 <b>B</b> = 이염산염(구아니디늄 + β-carbolinium, Cl<sup>−</sup> 2개)이 된다. 인돌 N–H는 그대로이다.</p>
<p>⑤ 기출(2020A-4)과의 연결: 아닐리늄(p<i>K</i><sub>a</sub> 4.6)이 아세트산 소듐(아세트산 p<i>K</i><sub>a</sub> 4.8)으로 일부 탈양성자화되어 아실화되는 것처럼, 산–염기 평형의 방향은 언제나 “짝산의 p<i>K</i><sub>a</sub>가 큰 쪽으로” 양성자가 이동한다. 흔한 오답: 인돌 N을 양성자화하거나, 피리딘 N과 구아니딘의 순서를 바꾸는 것.</p>''',
),
# ---------------------------------------------------------------- 2018A-12
dict(
    key='2018A-12',
    src='2018학년도 A형 12번',
    src_topic='tert-butylbenzene 나이트로화(입체 효과로 para 주) / SO₃H 차단기(술폰화–나이트로화–탈술폰화)로 오쏘 생성물 합성',
    change='anisole의 브로민화에서 소량만 생기는 2-bromoanisole(벤자인 문항의 출발물)을 술폰산 차단기로 선택적으로 합성하게 하고, '
           '탈술폰화 단계를 ipso 양성자화 메커니즘(논문의 산 촉매 수소 교환과 같은 원리)으로 굽은 화살표로 제시하게 함',
    paper=dict(cite='J. Am. Chem. Soc. 1967, 89, 4418–4424', book='Klein 19.86',
               what='2,4-dimethoxy-/2,4,6-trimethoxy-1-tritiobenzene의 산 촉매 탈삼중수소화: ipso 탄소 양성자화 → OMe로 안정화된 아레늄 이온 → T⁺ 이탈 (술폰화의 역반응과 같은 ipso 치환)'),
    nobel='1994 노벨 화학상(G. A. Olah — 탄소 양이온/아레늄 이온의 직접 관찰)',
    body=f'''다음 [반응 1]에서 {A_}와 {B_}가 각각 주생성물과 부생성물로 얻어졌다. [반응 2]는 {B_}를 주생성물로 합성하기 위한 3단계 반응이다. {NOTE}
{frame('<div class="ft">[반응 1]</div>',
       scheme(M('COc1ccccc1', scale=15), arrow('Br<sub>2</sub>', 'CH<sub>3</sub>COOH'), M('COc1ccc(Br)cc1', 'A', 15), plus(), M('COc1ccccc1Br', 'B', 15)),
       '<div class="ft">[반응 2]</div>',
       scheme(M('COc1ccccc1', scale=15), arrow('(1)', ''), L('C'), arrow('(2)', ''), L('D'), arrow('(3)', ''), L('B')),
       '<div class="chem" style="margin-top:4px">&lt;보 기&gt; ㉠ HNO<sub>3</sub>, H<sub>2</sub>SO<sub>4</sub>　㉡ 진한 H<sub>2</sub>SO<sub>4</sub>(SO<sub>3</sub>)　㉢ Br<sub>2</sub>, FeBr<sub>3</sub><br>　　　　㉣ 묽은 H<sub>2</sub>SO<sub>4</sub>, H<sub>2</sub>O, 가열　㉤ NaNO<sub>2</sub>, HCl</div>')}
<p class="ask">[반응 2]의 (1)~(3)에 들어갈 반응 조건을 &lt;보기&gt;에서 1개씩 골라 순서대로 쓰고, 중간 주생성물 {C_}와 {D_}의 구조를 그리시오. 또한 (3) 단계에서 {D_}가 {B_}로 전환되는 반응 메커니즘을 굽은 화살표를 사용하여 제시하시오. [[PTS]]</p>''',
    answer=f'''(1) ㉡, (2) ㉢, (3) ㉣
<div class="ansbox">{M('COc1ccc(cc1)S(=O)(=O)O', 'C: 4-methoxybenzenesulfonic acid', 15)}{M('COc1ccc(cc1Br)S(=O)(=O)O', 'D: 3-bromo-4-methoxybenzenesulfonic acid', 15)}</div>
메커니즘: H<sub>3</sub>O<sup>+</sup>가 SO<sub>3</sub>H가 붙은 고리 탄소(ipso, OMe의 파라)를 양성자화 → 아레늄 이온(양전하가 OMe의 산소까지 비편재화된 옥소늄 공명 구조로 안정화) → C–S 결합의 전자쌍이 고리로 돌아오며 SO<sub>3</sub>(+H<sup>+</sup>)가 떨어져 방향족성 회복 → B.''',
    explain='''<p><b>핵심 반응: 가역적 술폰화를 이용한 차단기(blocking group) 전략과 ipso 양성자화에 의한 탈술폰화</b></p>
<p>① [반응 1] OMe는 비공유 전자쌍의 공명 공여로 강하게 활성화하는 o,p-지향기이다. 오쏘 공격은 OMe와의 입체 반발이 있고 통계적 이점(오쏘 2자리)을 상쇄하므로 파라 생성물 <b>A</b>가 주생성물이다.</p>
<p>② (1) 진한 H<sub>2</sub>SO<sub>4</sub>(SO<sub>3</sub>): 부피 큰 SO<sub>3</sub>H가 파라 자리에 들어가 이를 막는다 → <b>C</b>. (2) Br<sub>2</sub>/FeBr<sub>3</sub>: OMe(오쏘 지향, 강한 활성화)와 SO<sub>3</sub>H(메타 지향)가 <b>모두</b> OMe의 오쏘(= SO<sub>3</sub>H의 메타) 자리를 가리키는 협동 배향 → <b>D</b>. (3) 묽은 산·가열(수증기): 술폰화의 역반응으로 SO<sub>3</sub>H 제거 → <b>B</b> = 2-bromoanisole.</p>
<p>③ (3) 메커니즘 상세: 고농도의 물과 열이 평형을 탈술폰화 쪽으로 이동시킨다(르샤틀리에). H<sup>+</sup>가 ipso 탄소에 첨가하는 것이 속도 결정 단계이며, 이 탄소는 OMe의 파라이므로 생성되는 아레늄 이온의 공명 구조 중 하나가 CH<sub>3</sub>O<sup>+</sup>=C(모든 원자가 옥텟)로 특히 안정하다. 이어 C–SO<sub>3</sub>H 결합이 끊어지며 SO<sub>3</sub>(→ H<sub>2</sub>SO<sub>4</sub>)가 이탈한다. 논문(Klein 19.86)의 탈삼중수소화도 ipso 양성자화 → 아레늄 이온 → T<sup>+</sup> 이탈로, 같은 친전자성 ipso 치환이며 OMe가 오쏘/파라에 많을수록 빠르다.</p>
<p>④ 오답 함정: ㉠(나이트로화)을 넣으면 Br이 아닌 NO<sub>2</sub>가 들어가고, ㉤은 아민이 없어 의미가 없다. 순서를 (2)→(1)로 하면 파라 브로민화가 먼저 일어난다. 또 탈술폰화 조건(㉣)과 술폰화 조건(㉡)은 같은 평형의 양 방향 — 농도(SO<sub>3</sub>/물)로 방향을 정한다.</p>
<p>⑤ 생성된 <b>B</b>(2-bromoanisole)는 NaNH<sub>2</sub>와의 벤자인 반응으로 <i>m</i>-anisidine을 주는 출발물로 쓰인다.</p>''',
),
# ---------------------------------------------------------------- 2018B-4
dict(
    key='2018B-4',
    src='2018학년도 B형 4번',
    src_topic='퓨란의 브로민화: C2 vs C3 공격 σ-착물의 공명 구조 비교로 주생성물(2-bromofuran) 판단',
    change='“중간체 양이온의 구조와 안정성으로 반응성을 설명”하는 평가 요소를 유지하되, 초강산 CF₃SO₃H에서 생성되는 초친전자체(superelectrophile, 이가 양이온)가 '
           '비활성 벤젠과 이중 Friedel–Crafts 반응을 하는 논문 반응으로 바꾸어, 이가 양이온·벤질 양이온 중간체를 그리고 그 반응성을 설명하게 함',
    paper=dict(cite='J. Org. Chem. 1999, 64, 6702–6705', book='Klein 19.90',
               what='quinuclidin-3-one + 벤젠, CF₃SO₃H → N·O 이중 양성자화 초친전자체 → 3,3-diphenylquinuclidinium'),
    nobel='1994 노벨 화학상(G. A. Olah — 초강산과 탄소 양이온, 초친전자체 개념)',
    body=f'''다음은 quinuclidin-3-one을 초강산 CF<sub>3</sub>SO<sub>3</sub>H(p<i>K</i><sub>a</sub> ≈ −14) 속에서 과량의 벤젠과 반응시켜 {C_}(C<sub>19</sub>H<sub>22</sub>N<sup>+</sup>, 트라이플레이트 염)를 얻는 반응이다. 반응은 이가 양이온 중간체 {A_}(C<sub>7</sub>H<sub>13</sub>NO<sup>2+</sup>)와, 첫 번째 페닐화 후 물이 떨어져 생성되는 이가 양이온 중간체 {B_}(C<sub>13</sub>H<sub>17</sub>N<sup>2+</sup>)를 거친다. {NOTE}
{frame(scheme(M('O=C1CN2CCC1CC2', scale=17), arrow('C<sub>6</sub>H<sub>6</sub>(과량)', 'CF<sub>3</sub>SO<sub>3</sub>H, 25 ℃'), L('[A]'), arrow('C<sub>6</sub>H<sub>6</sub>', '−H<sub>2</sub>O'), L('[B]')),
       scheme(arrow('C<sub>6</sub>H<sub>6</sub>', ''), L('C')))}
<p class="ask">{A_}와 {C_}의 구조를 각각 그리시오. 또한 {B_}의 공명 구조 중 양전하가 벤젠 고리의 탄소에 있는 구조를 1개 그리고, 아세톤과 같은 단순 케톤은 같은 조건에서 벤젠과 거의 반응하지 않지만 {A_}는 반응하는 이유를 서술하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('[OH+]=C1C[NH+]2CCC1CC2', 'A', 16)}{M('[CH+]1C=CC(=C2C[NH+]3CCC2CC3)C=C1', 'B의 공명 구조(파라)', 15)}{M('[NH+]12CCC(CC1)C(c1ccccc1)(c1ccccc1)C2', 'C: 3,3-diphenylquinuclidinium', 15)}</div>
이유: A에서는 카보닐 산소뿐 아니라 이웃(β) 위치의 질소도 양성자화되어 있어 암모늄 양전하가 강한 유발 효과로 카보닐 탄소의 양전하(옥소카베늄)를 비편재화·안정화하지 못하게 한다. 두 양전하가 가까이 있어 정전기적으로 불안정한 이가 양이온은 LUMO 에너지가 매우 낮은 “초친전자체”가 되므로, 친핵성이 약한 벤젠의 π 전자도 공격할 수 있다.''',
    explain='''<p><b>핵심 반응: Friedel–Crafts형 하이드록시알킬화(카보닐 친전자체) — 초산(superacid)에서의 초친전자적 활성화(Olah)</b></p>
<p>① CF<sub>3</sub>SO<sub>3</sub>H는 먼저 염기성이 큰 3차 아민 N을 양성자화하고(암모늄), 이어 카보닐 O까지 양성자화하여 이가 양이온 <b>A</b>(C<sub>7</sub>H<sub>13</sub>NO<sup>2+</sup>)를 만든다. 보통 산에서는 O-양성자화 정도가 낮지만 초강산에서는 충분하다.</p>
<p>② 벤젠의 π 전자가 A의 카보닐 탄소를 공격 → 아레늄 이온(σ-착물) → 탈양성자화로 방향족성 회복 → 3-hydroxy-3-phenylquinuclidinium. OH가 양성자화되고 H<sub>2</sub>O가 떨어지면 3차·벤질 탄소 양이온 <b>B</b>가 생성된다. B의 양전하는 페닐 고리의 오쏘·파라 탄소로 비편재화된다(정답의 파라 공명 구조; 오쏘 구조도 정답).</p>
<p>③ 두 번째 벤젠이 B의 양이온 탄소를 공격(두 번째 S<sub>E</sub>Ar), 탈양성자화 → <b>C</b> = 3,3-diphenylquinuclidinium(C<sub>19</sub>H<sub>22</sub>N<sup>+</sup>). 염기 처리하면 중성 아민 C<sub>19</sub>H<sub>21</sub>N이 된다.</p>
<p>④ 초친전자성의 근거: 양성자화된 카보닐은 보통 O의 비공유 전자쌍과 알킬기의 공여로 양전하가 분산된다. 그러나 A는 C=O<sup>+</sup>H 탄소에서 두 결합 떨어진 곳에 N<sup>+</sup>H가 있어 전자를 강하게 끌어당기므로 카보닐 탄소가 극도로 전자 부족해진다(전하–전하 반발 = 불안정 = 고반응성). 같은 이유로 B도 일반 벤질 양이온보다 친전자성이 커서 두 번째 페닐화가 빠르다.</p>
<p>⑤ 기출(퓨란 브로민화)과의 공통 원리: 반응성과 위치 선택성은 <b>양이온 중간체(또는 그에 이르는 전이 상태)의 안정성</b>(Hammond 가설)으로 판단한다. 여기서는 반대로 친전자체가 불안정할수록(이가 양이온) 약한 친핵체와도 반응한다. 흔한 오답: 페닐이 1개만 붙은 3차 알코올을 최종 생성물로 쓰거나, N이 양성자화되지 않은 단일 양이온을 A로 그리는 것(분자식 불일치).</p>''',
),
# ---------------------------------------------------------------- 2017A-5
dict(
    key='2017A-5',
    src='2017학년도 A형 5번',
    src_topic='o-톨루이딘 → 다이아조늄 → CuCN(Sandmeyer) → 나이트릴 가수분해 → 협동 배향 브로민화',
    change='Sandmeyer 대신 “아미노기를 임시 배향기로 쓰고 H₃PO₂로 제거(탈아미노화)”하는 전략으로 바꾸어, '
           '직접 브로민화로는 얻을 수 없는 메타-브로모톨루엔을 합성하게 함(아세틸 보호로 다중 브로민화 억제 포함)',
    paper=dict(cite='J. Org. Chem. 2012, 77, 5503–5514', book='Klein 21.82',
               what='아미노테트랄린 합성의 출발물인 메타-브로모 메틸아렌 1-bromo-3,5-dimethylbenzene → NBS → NaCN → H₃O⁺로 아릴아세트산 합성. '
                    '본 문항은 이러한 메타-브로모 메틸벤젠을 아미노기 배향–탈아미노화로 만드는 단계를 모델화'),
    nobel='',
    body=f'''다음은 <i>p</i>-toluidine으로부터 중간 주생성물 {A_}(C<sub>7</sub>H<sub>8</sub>BrN)를 거쳐 최종 주생성물 {B_}(C<sub>7</sub>H<sub>7</sub>Br)를 합성하는 반응을 나타낸 것이다. {NOTE}
{frame(scheme(M('Cc1ccc(N)cc1', scale=16), arrow('1) (CH<sub>3</sub>CO)<sub>2</sub>O', '2) Br<sub>2</sub>, CH<sub>3</sub>COOH'), arrow('3) H<sub>3</sub>O<sup>+</sup>', '가열'), L('A')),
       scheme(arrow('1) NaNO<sub>2</sub>, HCl, 0 ℃', '2) H<sub>3</sub>PO<sub>2</sub>'), L('B')))}
<p class="ask">{A_}와 {B_}의 구조를 각각 그리시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('Cc1ccc(N)c(Br)c1', 'A: 2-bromo-4-methylaniline', 16)}{M('Cc1cccc(Br)c1', 'B: 3-bromotoluene', 16)}</div>''',
    explain='''<p><b>핵심 반응: 아세틸 보호로 조절한 EAS + 다이아조늄의 H<sub>3</sub>PO<sub>2</sub> 환원(탈아미노화) — “임시 배향기” 전략</b></p>
<p>① NH<sub>2</sub>는 너무 강한 활성화기라 Br<sub>2</sub>와 바로 반응시키면 비어 있는 오쏘 자리가 모두 브로민화된다(다중 치환). 아세트산 무수물로 아세트아마이드(NHAc)로 바꾸면 N 비공유 전자쌍이 카보닐과 공명하여 활성화가 중간 정도로 낮아져 1치환만 일어난다.</p>
<p>② <i>N</i>-(4-methylphenyl)acetamide에서 NHAc(공명 공여, 더 강한 활성화기)와 CH<sub>3</sub>(약한 활성화기)가 경쟁한다. 파라는 CH<sub>3</sub>로 막혀 있으므로 더 강한 활성화기인 NHAc의 <b>오쏘</b> 자리(= CH<sub>3</sub>의 메타)에 Br이 들어간다. 산 가수분해로 아마이드를 제거하면 <b>A</b> = 2-bromo-4-methylaniline.</p>
<p>③ NaNO<sub>2</sub>/HCl로 다이아조늄 염을 만든 뒤 H<sub>3</sub>PO<sub>2</sub>(하이포아인산)로 처리하면 라디칼 연쇄 과정으로 N<sub>2</sub>가 H로 치환된다(Ar–N<sub>2</sub><sup>+</sup> → Ar–H). 결과적으로 NH<sub>2</sub>는 Br의 위치를 정해 준 뒤 흔적 없이 사라진다 → <b>B</b> = 3-bromotoluene(1-bromo-3-methylbenzene).</p>
<p>④ 의의: 톨루엔을 직접 브로민화하면 o-/p-bromotoluene만 생기고, 메타 생성물은 거의 얻을 수 없다. CH<sub>3</sub>와 Br이 메타 관계인 화합물은 이처럼 “아미노기 배향 → 제거”로 만든다(같은 전략: 2,6-dimethylaniline → 4-bromo-2,6-dimethylaniline → 1-bromo-3,5-dimethylbenzene, 논문의 출발물).</p>
<p>⑤ 흔한 오답: A에서 Br을 CH<sub>3</sub>의 오쏘에 둔 것(약한 활성화기를 우선시), B를 Sandmeyer로 착각하여 Br이 2개인 구조(C<sub>7</sub>H<sub>6</sub>Br<sub>2</sub>)로 쓰는 것.</p>''',
),
# ---------------------------------------------------------------- 2016B-4
dict(
    key='2016B-4',
    src='2016학년도 B형 4번',
    src_topic='치환 벤젠 브로민화 속도 순서(NHAc > CH₃ > COCH₃), NHAc의 para 지향, 인돌 C3 브로민화',
    change='나이트로화 속도 순서(–OCH₃, –CH₃, –Cl, –CO₂CH₃)로 할로젠의 “불활성화하면서 o,p-지향” 성질을 서술하게 하고, '
           '인돌 브로민화 대신 전자 풍부한 고리가 이미늄 이온을 공격하는 Pictet–Spengler 고리화(위치 선택성: OMe의 파라)로 변형',
    paper=dict(cite='J. Org. Chem. 2011, 76, 1605–1613', book='Klein 23.96',
               what='crispine A 전합성: 3,4-dimethoxyphenylalanine 에스터 + 4-chlorobutanal, H₃O⁺ → 이미늄 → Pictet–Spengler(OMe의 파라에서 고리화) → N-알킬화'),
    nobel='',
    body=f'''다음은 방향족 화합물의 친전자성 방향족 치환 반응을 나타낸 것이다. {NOTE}
{frame('<div class="ft">[반응 1]</div>',
       scheme(L('C<sub>6</sub>H<sub>5</sub>–X'), arrow('HNO<sub>3</sub>, H<sub>2</sub>SO<sub>4</sub>', '25 ℃'), L('X–C<sub>6</sub>H<sub>4</sub>–NO<sub>2</sub>')),
       '<div class="chem" style="text-align:center">X = –OCH<sub>3</sub>, –CH<sub>3</sub>, –Cl, –CO<sub>2</sub>CH<sub>3</sub></div>',
       '<div class="ft">[반응 2]</div>',
       scheme(M('COc1ccc(CCN)cc1OC', scale=15), arrow('HCHO, HCl(aq)', '가열'), L('C')))}
<p class="ask">X가 각각 –OCH<sub>3</sub>, –CH<sub>3</sub>, –Cl, –CO<sub>2</sub>CH<sub>3</sub>일 때, 동일 조건에서 [반응 1]의 반응 속도가 큰 것부터 작은 것 순서대로 나열하시오. 또한 X가 –Cl일 때 주생성물 {B_}의 구조를 그리고, –Cl이 반응 속도를 감소시키면서도 {B_}를 주생성물로 주는 이유를 서술하시오. 그리고 [반응 2]에서 주생성물 {C_}(C<sub>11</sub>H<sub>15</sub>NO<sub>2</sub>)의 구조를 그리시오. [[PTS]]</p>''',
    answer=f'''속도: –OCH<sub>3</sub> &gt; –CH<sub>3</sub> &gt; –Cl &gt; –CO<sub>2</sub>CH<sub>3</sub>
<div class="ansbox">{M('O=[N+]([O-])c1ccc(Cl)cc1', 'B: 1-chloro-4-nitrobenzene', 15)}{M('COc1cc2c(cc1OC)CNCC2', 'C: 6,7-dimethoxy-1,2,3,4-tetrahydroisoquinoline', 15)}</div>
이유: Cl은 전기음성도가 커 유발 효과(−I)로 고리 전체의 전자 밀도를 낮추므로 속도는 감소한다. 그러나 오쏘/파라 공격으로 생긴 σ-착물에서는 양전하가 Cl이 붙은 탄소에 놓이는 공명 구조가 있어 Cl의 비공유 전자쌍이 공여(+M)하여 클로로늄(C=Cl<sup>+</sup>) 공명 구조로 안정화하므로 o,p 공격이 메타 공격보다 유리하다. 오쏘는 입체 장애가 있어 파라 생성물이 주생성물이다.''',
    explain='''<p><b>핵심 반응: 치환기 효과(활성화/불활성화, 배향)와 Pictet–Spengler 반응(이미늄 이온에 대한 분자 내 S<sub>E</sub>Ar)</b></p>
<p>① 속도 결정 단계는 σ-착물(아레늄 이온) 형성. –OCH<sub>3</sub>: O 비공유 전자쌍의 강한 공명 공여(+M ≫ −I) → 강한 활성화. –CH<sub>3</sub>: 유발·초공액 공여 → 약한 활성화. –Cl: −I &gt; +M → 약한 불활성화(o,p 지향). –CO<sub>2</sub>CH<sub>3</sub>: 카보닐의 공명·유발 끌기 → 중간 정도 불활성화(메타 지향). 상대 속도(벤젠 = 1) 대략 anisole ≫ 톨루엔(~25) &gt; 1 &gt; 클로로벤젠(~0.03) &gt; 벤조산 메틸(~0.004).</p>
<p>② X = Cl: 메타 공격 σ-착물은 Cl의 공명 공여를 받을 수 없고 −I만 작용한다. 오쏘/파라 공격 σ-착물은 Cl의 3p 비공유 전자쌍이 C=Cl<sup>+</sup> 형태로 양전하를 나누는 네 번째 공명 구조를 가지므로 상대적으로 안정 → o,p 지향. 파라 : 오쏘 ≈ 2 : 1 정도로 파라가 주생성물(<b>B</b> = 1-chloro-4-nitrobenzene).</p>
<p>③ [반응 2] 1차 아민 + HCHO → 카비놀아민 → 탈수 → 이미늄 이온(CH<sub>2</sub>=N<sup>+</sup>H–). 다이메톡시 고리가 친핵체로 이미늄 탄소를 공격(6-endo 고리화) → 아레늄 이온 → 탈양성자화 → 1,2,3,4-tetrahydroisoquinoline.</p>
<p>④ 위치 선택성: 원료 고리를 C1(CH<sub>2</sub>CH<sub>2</sub>NH<sub>2</sub>), C3·C4(OMe)로 번호 매기면, 고리화가 가능한 탄소는 곁사슬의 두 오쏘 자리인 C2(3-OMe의 오쏘, 두 치환기 사이)와 C6(3-OMe의 파라, 4-OMe의 메타)이다. 3-OMe의 <b>파라</b>인 C6은 공명 활성화를 받으면서 입체 장애가 없으므로 이곳에서 고리화하여 <b>C</b> = 6,7-dimethoxy-THIQ가 생성된다(7,8-dimethoxy 이성질체는 소량). 논문의 crispine A 합성에서도 OMe의 파라에서 Pictet–Spengler 고리화가 일어난다.</p>
<p>⑤ 흔한 오답: 속도 순서에서 Cl을 CO<sub>2</sub>CH<sub>3</sub>보다 느리게 쓰는 것, B를 메타 생성물로 그리는 것, C를 고리화되지 않은 이민/N-메틸 아민으로 그리는 것(분자식 C<sub>11</sub>H<sub>15</sub>NO<sub>2</sub> = 원료 + C − H<sub>2</sub>O 이므로 고리화 필요).</p>''',
),
# ---------------------------------------------------------------- 2014B-논술2
dict(
    key='2014B-논술2',
    src='2014학년도 B형 논술형 2번(유기 부분)',
    src_topic='벤젠으로부터 4′-bromo-3′-nitroacetophenone 3단계 합성과 단계 순서 결정 이유',
    change='같은 “다치환 벤젠 합성 순서” 논리(FC 아실화의 한계, 협동 배향)를 유지하되, 최종 단계에 Pd 촉매 Suzuki–Miyaura 짝지음을 추가하여 '
           '바이아릴 표적 1-(2-nitro-[1,1′-biphenyl]-4-yl)ethan-1-one을 4단계로 설계하고 촉매 순환(산화성 첨가–금속 교환–환원성 제거)을 서술하게 함',
    paper=dict(cite='Prog. Stereochem. 1958, 2, 125', book='Klein 19.87',
               what='picryl iodide에서 부피 큰 오쏘 치환기가 나이트로기를 고리 평면 밖으로 비틀어 공명을 막는 효과(공명의 입체 억제) — 표적 화합물의 오쏘-페닐/나이트로 비틀림 해석에 적용'),
    nobel='2010 노벨 화학상(R. F. Heck·E. Negishi·A. Suzuki — Pd 촉매 교차 짝지음)',
    body=f'''다음은 벤젠으로부터 바이아릴 화합물 {D_}를 합성하려는 계획에 대한 자료이다.
{frame(scheme(M('CC(=O)c1ccc(-c2ccccc2)c([N+](=O)[O-])c1', 'D: 1-(2-nitro-[1,1′-biphenyl]-4-yl)ethan-1-one', 16)),
       '<div class="chem">사용 가능한 시약: benzene, Br<sub>2</sub>, FeBr<sub>3</sub>, CH<sub>3</sub>COCl, AlCl<sub>3</sub>, HNO<sub>3</sub>, H<sub>2</sub>SO<sub>4</sub>, PhB(OH)<sub>2</sub>, Pd(PPh<sub>3</sub>)<sub>4</sub>(촉매), Na<sub>2</sub>CO<sub>3</sub></div>')}
<p class="ask">위 시약을 이용하여 벤젠으로부터 {D_}를 주생성물로 합성하는 반응식을 중간 생성물의 구조를 포함하여 4단계로 쓰고, 각 단계의 순서를 결정한 이유를 서술하시오. 또한 마지막 단계의 촉매 순환을 구성하는 기본 단계 3가지를 순서대로 쓰고, 각 단계 전후 Pd의 산화수를 쓰시오. (단, 각 단계에서는 적절한 분리·정제 과정을 수행하였다.) [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('Brc1ccccc1', '① Br<sub>2</sub>, FeBr<sub>3</sub>', 14)}{M('CC(=O)c1ccc(Br)cc1', '② CH<sub>3</sub>COCl, AlCl<sub>3</sub>', 14)}{M('CC(=O)c1ccc(Br)c([N+](=O)[O-])c1', '③ HNO<sub>3</sub>, H<sub>2</sub>SO<sub>4</sub>', 14)}</div>
④ PhB(OH)<sub>2</sub>, Pd(PPh<sub>3</sub>)<sub>4</sub>, Na<sub>2</sub>CO<sub>3</sub> → D<br>
순서 이유: (가) FC 아실화는 NO<sub>2</sub> 같은 강한 불활성화기가 있는 고리에서 일어나지 않으므로 나이트로화는 아실화 뒤에 해야 한다. (나) 아세틸기는 메타 지향기이므로 아실화를 먼저 하면 Br이 메타로 들어간다 → 브로민화를 먼저 하여 Br(o,p 지향)이 아세틸기를 파라로 보내게 한다. (다) 4-bromoacetophenone의 나이트로화에서 Br(오쏘 지향)과 COCH<sub>3</sub>(메타 지향)가 같은 탄소(Br의 오쏘)를 가리킨다(협동 배향). (라) 짝지음을 먼저 하면 바이페닐의 활성화된 다른 고리(페닐 치환기의 파라)에서 아실화·나이트로화가 일어나므로 Suzuki 짝지음은 마지막에 한다.<br>
촉매 순환: 산화성 첨가 [Pd(0) → Pd(II)] → 금속 교환 [Pd(II) → Pd(II)] → 환원성 제거 [Pd(II) → Pd(0)]''',
    explain='''<p><b>핵심 반응: 다치환 벤젠의 역합성(배향 효과·FC 한계) + Suzuki–Miyaura 교차 짝지음</b></p>
<p>① 역합성: D의 Ar–Ph 결합은 Suzuki로, 그 전구체는 4′-bromo-3′-nitroacetophenone. 이 화합물에서 COCH<sub>3</sub>와 Br은 파라, NO<sub>2</sub>는 Br의 오쏘·COCH<sub>3</sub>의 메타 → Br과 COCH<sub>3</sub>가 이미 있는 고리에 마지막으로 NO<sub>2</sub>를 넣는 것이 협동 배향으로 유일한 위치를 준다.</p>
<p>② 1단계 Br<sub>2</sub>/FeBr<sub>3</sub>: FeBr<sub>3</sub>가 Br–Br을 분극시켜 Br<sup>+</sup> 등가체 생성 → bromobenzene. 2단계 CH<sub>3</sub>COCl/AlCl<sub>3</sub>: 아실륨 이온이 Br의 파라(오쏘는 입체 장애)를 공격 → 4-bromoacetophenone. Br은 불활성화기지만 할로젠 정도의 약한 불활성화는 FC 아실화를 허용한다.</p>
<p>③ 3단계 HNO<sub>3</sub>/H<sub>2</sub>SO<sub>4</sub>: NO<sub>2</sub><sup>+</sup>가 Br의 오쏘(= COCH<sub>3</sub>의 메타)를 공격. 고리가 두 EWG로 불활성화되어 있으나 나이트로늄 이온은 강한 친전자체라 반응한다.</p>
<p>④ 4단계 Suzuki: (i) <b>산화성 첨가</b> — Pd(0)L<sub>n</sub>이 Ar–Br 결합에 끼어들어 Ar–Pd(II)–Br (Pd 0 → +2). 오쏘-NO<sub>2</sub>와 파라-COCH<sub>3</sub>가 고리를 전자 부족하게 하여 이 단계가 빠르다. (ii) <b>금속 교환</b> — Na<sub>2</sub>CO<sub>3</sub>가 PhB(OH)<sub>2</sub>를 붕산염 [PhB(OH)<sub>3</sub>]<sup>−</sup>으로 활성화하여 Ph를 Pd로 전달 → Ar–Pd(II)–Ph (+2 유지). (iii) <b>환원성 제거</b> — cis 배치된 Ar과 Ph가 결합하며 생성물 방출, Pd(II) → Pd(0) 재생.</p>
<p>⑤ 논문(Klein 19.87) 연결: D에서 NO<sub>2</sub>는 부피 큰 페닐기와 오쏘 관계이므로 둘 다 고리 평면 밖으로 비틀려 공명이 줄어든다(공명의 입체 억제) — 피크릴 아이오다이드의 오쏘-NO<sub>2</sub>가 C–N 결합이 길어지는 것과 같은 현상이다.</p>
<p>⑥ 흔한 오답 순서: 나이트로화 → 아실화(FC 실패), 아실화 → 브로민화(Br이 메타), Suzuki → 아실화 → 나이트로화(치환이 바이페닐의 다른 고리 4′ 자리로 감).</p>''',
),
]
