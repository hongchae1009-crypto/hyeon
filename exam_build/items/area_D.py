"""표준 예시 문항 (작성 에이전트용 견본). 최종본에서는 set1.py 에 편입."""
from chem import M, L, arrow, varrow, scheme, rows, frame, nmr, ir, spec, plus

ITEMS = [
dict(
    key='2026A-1',
    src='2026학년도 A형 1번',
    src_topic='benzaldehyde의 Wittig 반응(oxaphosphetane) → (Z)-stilbene → m-CPBA 입체특이적 에폭시화',
    change='불안정화 일라이드(Z) 대신 안정화 일라이드(E-선택성)를 사용하고, m-CPBA 대신 Sharpless 비대칭 에폭시화로 바꾸어 '
           '“입체특이성 + 거울상선택성”을 동시에 묻도록 변형',
    paper=dict(cite='Klein 14장 참고문헌 (reboxetine 공정 합성, Sharpless 비대칭 에폭시화)', book='Klein 14.63',
               what='(E)-cinnamyl alcohol류의 Sharpless 비대칭 에폭시화로 3-phenylglycidol을 얻고 이를 (S,S)-reboxetine으로 전환'),
    nobel='2001 노벨 화학상(K. B. Sharpless — 키랄 촉매 산화반응), 1979 노벨 화학상(G. Wittig)',
    body=f'''다음은 benzaldehyde로부터 중간 주생성물 <b class="lbltxt">A</b>(C<sub>11</sub>H<sub>12</sub>O<sub>2</sub>)와 <b class="lbltxt">B</b>를 거쳐 최종 주생성물 <b class="lbltxt">C</b>를 합성하는 반응을 나타낸 것이다. (단, 각 반응에서는 적절한 분리·정제 과정을 수행하였다.)
{frame(scheme(M('O=Cc1ccccc1', scale=17), arrow('Ph<sub>3</sub>P=CHCO<sub>2</sub>Et', 'CH<sub>2</sub>Cl<sub>2</sub>'), L('A'),
              arrow('1) DIBAL-H (2 당량)', '2) H<sub>3</sub>O<sup>+</sup>'), L('B')),
       scheme(arrow('Ti(O<i>i</i>-Pr)<sub>4</sub>, L-(+)-DET', '<i>t</i>-BuOOH, −20 ℃'), L('C')),
       '<div class="chem" style="text-align:center">DET = diethyl tartrate</div>')}
<p class="ask"><b class="lbltxt">A</b>의 입체구조를 그리고, <b class="lbltxt">C</b>의 입체구조를 그린 후 <b class="lbltxt">C</b>에 있는 모든 카이랄 중심의 절대 배열(<i>R</i>/<i>S</i>)을 쓰시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CCOC(=O)/C=C/c1ccccc1', 'A: ethyl (E)-cinnamate', 15)}{M('OC[C@@H]1O[C@H]1c1ccccc1', 'C: (2S,3S)-3-phenylglycidol', 15)}</div>
C의 두 카이랄 중심: C2 = <i>S</i>, C3 = <i>S</i> (B = (<i>E</i>)-cinnamyl alcohol)''',
    explain='''<p>① 안정화 일라이드(Ph<sub>3</sub>P=CHCO<sub>2</sub>Et)는 oxaphosphetane 형성이 가역적이어서 열역학적으로 유리한 <i>trans</i>-oxaphosphetane을 거쳐 (<i>E</i>)-알켄을 준다(cf. 기출의 비안정화 일라이드 PhCH=PPh<sub>3</sub>는 <i>Z</i> 선택적).</p>
<p>② DIBAL-H 2당량은 에스터를 1차 알코올로 환원하며 C=C는 보존된다 → B = (<i>E</i>)-cinnamyl alcohol.</p>
<p>③ Sharpless 비대칭 에폭시화: Ti–tartrate 촉매가 알릴 알코올의 OH에 배위하여 한쪽 면에만 산소를 전달한다. 알릴 알코올을 CH<sub>2</sub>OH가 오른쪽 아래에 오도록 그리면 L-(+)-DET는 아래쪽 면, D-(−)-DET는 위쪽 면에서 산소를 전달한다. (<i>E</i>)-알켄의 기하가 그대로 유지(입체특이적)되므로 <i>trans</i>-에폭사이드, 즉 (2<i>S</i>,3<i>S</i>)-3-phenylglycidol이 생성된다.</p>
<p>④ CIP: C2(–O–, –C3, –CH<sub>2</sub>OH, H), C3(–O–, –C2, –Ph, H) 모두 <i>S</i>. 기출(m-CPBA)은 라셈 <i>cis</i>-에폭사이드이므로 광학 비활성이지만, 이 문항의 C는 광학 활성이다.</p>''',
),
]
