"""MDEET 2027학년도 자연과학Ⅱ 유기화학 21–30번 상세 해설 (27학년도 중등 화학 임용 대비)."""
import figs_md_2027 as F

ITEMS = [
    # ------------------------------------------------------------------ 21
    {
        "id": "md-2027-21", "year": 2027, "q": 21, "exam": "MDEET 자연과학Ⅱ 21번", "pts": 3,
        "sub": "명명법 — 할로알케인·할로알코올·고리형 알켄의 IUPAC 번호 매기기",
        "title": "구조와 IUPAC 이름의 짝: 1-bromo-3-methylbutane, 4-bromobutan-1-ol, 1,6,6-trimethylcyclohex-1-ene",
        "stem": "구조와 IUPAC 이름이 옳게 짝지어진 것만을 고르시오.<br>"
                "ㄱ. (CH₃)₂CHCH₂CH₂Br — 1-Bromo-3-methylbutane<br>"
                "ㄴ. HOCH₂CH₂CH₂CH₂Br — 4-Bromobutan-1-ol<br>"
                "ㄷ. 고리 C=C의 한 탄소에 CH₃, 그 이웃 고리 탄소에 CH₃ 2개(gem-다이메틸) — 1,2,2-Trimethylcyclohex-1-ene<br>"
                "① ㄴ ② ㄷ ③ ㄱ, ㄴ ④ ㄱ, ㄷ ⑤ ㄱ, ㄴ, ㄷ",
        "answer": "<b>③</b> — ㄱ ○(주사슬 4C, 치환기 위치 {1,3}이 {2,4}보다 낮음), ㄴ ○(–OH가 접미사로 표시되는 주작용기이므로 C1), "
                  "ㄷ ✗(C=C에 1·2를 주고 남은 치환기 위치가 최소가 되도록 하면 <b>1,6,6-trimethylcyclohex-1-ene</b>; "
                  "‘1,2,2-’는 sp² 탄소 C2에 CH₃가 2개 붙어야 하므로 존재할 수 없는 구조).",
        "concepts": [
            "명명 순서: 주작용기(접미사) 결정 → 주사슬/고리 선택 → 주작용기 > 다중결합 > 치환기(접두사) 순으로 낮은 위치 번호",
            "할로젠(–Br, –Cl)은 항상 접두사(bromo-) — 순위가 없으므로 알킬기와 같은 자격으로 ‘가장 먼저 다른 점’ 규칙 적용",
            "–OH는 접미사(-ol)로 표시되는 주작용기 → 할로젠보다 낮은 번호 우선",
            "사이클로알켄: C=C의 두 탄소가 반드시 C1·C2 → 그다음 치환기 위치 집합이 가장 작게(첫 번째 차이점 비교)",
            "알파벳 순서는 이름 쓰기 순서일 뿐, 번호는 위치 집합이 동률일 때만 알파벳으로 결정",
        ],
        "sol": """<p><b>① 보기별 판정</b></p>
<table class="tb"><tr><th>보기</th><th>번호 매기기</th><th>올바른 이름</th><th>판정</th></tr>
<tr><td>ㄱ</td><td>가장 긴 사슬 4C(butane). Br 쪽 끝부터: Br-C1, CH₃-C3 → {1,3}; 반대쪽: {2,4}. 첫 차이점에서 1 &lt; 2</td><td>1-bromo-3-methylbutane</td><td>○</td></tr>
<tr><td>ㄴ</td><td>–OH = 주작용기(접미사 -ol) → OH 탄소가 C1, Br은 C4. 할로젠은 접두사이므로 OH보다 우선권 없음</td><td>4-bromobutan-1-ol</td><td>○</td></tr>
<tr><td>ㄷ</td><td>C=C 두 탄소가 C1·C2. (가) CH₃가 붙은 알켄 탄소=C1, =CH=C2 → gem-다이메틸 탄소=C6 → {1,6,6}<br>(나) =CH=C1, CH₃ 알켄 탄소=C2 → gem 탄소=C3 → {2,3,3}<br>첫 차이점 1 &lt; 2 → (가)</td><td>1,6,6-trimethylcyclohex-1-ene</td><td>✗</td></tr></table>
<p><b>② ㄷ의 함정</b>: ‘1,2,2-’는 치환기 번호를 1·2·2로 몰아 보려는 실수이다. 그러나 C1=C2이면 C2는 sp² 탄소로 고리 결합 2개 + C1과의 이중결합을 가지므로 치환기를 <b>하나</b>만 더 가질 수 있다. 따라서 2,2-다이메틸은 구조적으로 불가능하다. gem-다이메틸 탄소는 C1의 이웃이지만 C2가 아닌 쪽(C6)이다. 이 골격은 β-ionone·β-carotene의 말단 고리(β-cyclocitral 계열)와 같다.</p>
<p><b>③ 주의</b>: 1993 권고 이후 이름은 ‘cyclohex-1-ene’처럼 위치 번호를 어미 바로 앞에 쓴다. 고리에서 C=C가 C1·C2일 때 ‘-1-ene’의 1은 생략하기도 한다(1,6,6-trimethylcyclohexene).</p>""",
        "figs": [(F.f21, "보기 ㄱ·ㄴ·ㄷ의 번호 매기기: ㄷ은 C=C에 1·2를 주면 gem-다이메틸 탄소가 C6 → 1,6,6-trimethylcyclohex-1-ene")],
        "extra": [
            ("원리 정리", """<p><b>IUPAC 번호 매기기 우선순위(위에서부터 먼저 적용)</b></p>
<ol><li>주작용기(접미사로 쓰는 기: –COOH &gt; 유도체 &gt; –CHO &gt; C=O &gt; –OH &gt; –NH₂)에 가장 낮은 번호</li>
<li>수소화 정도 표시(다중결합: -ene, -yne)에 낮은 번호. 고리 알켄은 C=C가 C1·C2.</li>
<li>모든 접두사 치환기(알킬, 할로젠, –NO₂ 등)를 함께 묶어 위치 집합이 가장 작게 — 첫 번째 차이점 비교</li>
<li>그래도 같으면 알파벳 순서가 앞서는 치환기에 낮은 번호</li></ol>
<table class="tb"><tr><th>예</th><th>판단 포인트</th><th>이름</th></tr>
<tr><td>(CH₃)₂CHCH₂CH₂Br</td><td>{1,3} vs {2,4}</td><td>1-bromo-3-methylbutane</td></tr>
<tr><td>BrCH₂CH₂CH₂CH₂OH</td><td>OH(접미사) 우선</td><td>4-bromobutan-1-ol</td></tr>
<tr><td>CH₃CH=CHCH(CH₃)OH</td><td>OH 우선, 그다음 C=C</td><td>pent-3-en-2-ol</td></tr>
<tr><td>3-methylcyclohexene</td><td>C=C 1·2, CH₃는 3 (6이 아님)</td><td>3-methylcyclohex-1-ene</td></tr>
<tr><td>cyclohex-2-en-1-ol</td><td>OH가 C1, C=C는 2·3</td><td>cyclohex-2-en-1-ol</td></tr></table>"""),
            ("27 임용 연관 분석", """<p><b>① 연관 기출</b>: 임용에서 명명법 단독 문항은 드물고, 구조 결정·합성 문항의 답을 <b>IUPAC 이름으로 쓰게</b> 하는 형태로 나온다. 예: 2008 서술형 15번(3-chloro-2-methyl-2-phenylbutane, (S)-2-iodo… 의 반응 생성물을 이름으로), 2019 전공A 기입형 6번(ethyl 3-bromobenzoate), 2024 전공B 서술형 7번(cyclohex-2-enone·cyclohexanone), 2016 전공A 기입형 4번(1-methylcyclohexanol 탈수 → 1-methylcyclohexene). 특히 고리 알켄·알켄올의 번호(‘cyclohex-2-en-1-ol’, ‘1-methylcyclohex-1-ene’)는 서술형 답안 채점 요소가 된다.</p>
<p><b>② 서술형 변형 예상</b>: “β-ionone 말단 고리에 해당하는 C₉H₁₆ 알켄 X의 IUPAC 이름을 쓰고, ‘1,2,2-trimethylcyclohex-1-ene’이 불가능한 이유를 서술하시오.” — 모범 답안: X = 1,6,6-trimethylcyclohex-1-ene. C=C 탄소에 1·2를 준 뒤 치환기 집합 {1,6,6} &lt; {2,3,3}. C2는 sp²로 치환기 1개만 가능하므로 2,2-이치환은 원자가를 초과한다.</p>
<p><b>③ 체크포인트</b>: 할로젠은 언제나 접두사, OH/C=O는 접미사 → 번호 우선권이 다르다. 고리 알켄에서 ‘C=C 1·2’ 규칙과 ‘첫 번째 차이점’ 비교를 습관화할 것.</p>"""),
        ],
        "faq": [
            ("ㄱ을 3-methyl-1-bromobutane이라고 쓰면 틀리나요?",
             "번호는 같지만 접두사는 알파벳 순서(bromo &lt; methyl)로 써야 하므로 1-bromo-3-methylbutane이 정식 이름입니다."),
            ("ㄴ에서 Br이 C1이 되면 안 되나요?",
             "Br은 접두사로만 표시되고 –OH는 접미사(-ol)로 표시되는 주작용기라 –OH에 낮은 번호가 먼저 돌아갑니다. 할로젠과 알킬은 번호 우선권이 같지만 –OH보다는 낮습니다."),
            ("ㄷ을 2,3,3-trimethylcyclohex-1-ene으로 쓰면요?",
             "그것도 C=C에 1·2를 준 번호이지만 치환기 집합 {2,3,3}이 {1,6,6}보다 첫 차이점에서 크므로 틀린 이름입니다."),
        ],
    },
    # ------------------------------------------------------------------ 22
    {
        "id": "md-2027-22", "year": 2027, "q": 22, "exam": "MDEET 자연과학Ⅱ 22번", "pts": 4,
        "sub": "결합과 구조 — 알켄 안정도, 혼성과 결합각, 공명·초공액과 결합 길이",
        "title": "알켄 치환도와 안정도, 벤젠 vs 사이클로헥세인 결합각, 아세트아마이드 vs 아세톤의 C–C(=O) 길이",
        "stem": "두 화합물의 물리·화학적 성질 크기 비교가 옳은 것만을 고르시오.<br>"
                "ㄱ. 분자의 안정도: 3-methylpent-2-ene &gt; 3-methylpent-1-ene<br>"
                "ㄴ. ∠(C–C–C): benzene &gt; cyclohexane<br>"
                "ㄷ. 화살표로 표시된 CH₃–C(=O) 결합의 길이: CH₃CONH₂ &gt; CH₃COCH₃<br>"
                "① ㄱ ② ㄷ ③ ㄱ, ㄴ ④ ㄴ, ㄷ ⑤ ㄱ, ㄴ, ㄷ",
        "answer": "<b>⑤</b> — ㄱ ○(삼치환 알켄 &gt; 일치환 알켄: 초공액·sp²–sp³ 결합 강화, 수소화열 작음), "
                  "ㄴ ○(벤젠 sp² 평면 120° &gt; 사이클로헥세인 의자형 ≈111°), "
                  "ㄷ ○(아마이드는 n<sub>N</sub>→π*<sub>C=O</sub> 공명으로 π*가 높아지고 카보닐 탄소의 δ+가 줄어 CH₃의 초공액이 약함 → C–C가 케톤보다 약간 김).",
        "concepts": [
            "알켄 안정도: 사치환 &gt; 삼치환 &gt; 이치환(trans &gt; cis) &gt; 일치환 — 수소화열(ΔH°hydrog)로 비교",
            "안정화 원인: C–H σ → π* 초공액, 강한 C(sp²)–C(sp³) 결합 수 증가",
            "결합각: sp² 평면 120°, sp³ 109.5° — 사이클로헥세인 의자형은 각 무리 거의 없이 ≈111°",
            "아마이드 공명: N 비공유쌍 → C=O π* (C–N 부분 이중결합, C=O 약화)",
            "초공액에 의한 결합 단축: 인접 σ(C–H) → π* 주개가 강할수록 C(sp³)–C(sp²) 결합에 이중결합성",
        ],
        "sol": """<p><b>① 보기별 판정</b></p>
<table class="tb"><tr><th>보기</th><th>비교</th><th>근거</th><th>판정</th></tr>
<tr><td>ㄱ</td><td>CH₃CH=C(CH₃)CH₂CH₃ (삼치환) vs CH₂=CHCH(CH₃)CH₂CH₃ (일치환)</td><td>같은 C₆H₁₂ 이성질체로 수소화하면 같은 3-methylpentane이 된다. 삼치환 알켄의 수소화열이 더 작아(≈ −112 vs −126 kJ/mol 수준) 더 안정. C=C에 이웃한 C–H(초공액 주개)가 많고, 강한 C(sp²)–C(sp³) 결합이 3개</td><td>○</td></tr>
<tr><td>ㄴ</td><td>benzene vs cyclohexane</td><td>벤젠: 모든 C가 sp², 평면 정육각형 → 내각 120°. 사이클로헥세인: sp³, 의자형으로 각 무리·비틀림 무리를 거의 없앤 결합각 ≈111.4°</td><td>○</td></tr>
<tr><td>ㄷ</td><td>CH₃–C(=O)NH₂ vs CH₃–C(=O)CH₃ 의 CH₃–C 결합</td><td>아래 ② 참고. 아마이드 쪽이 약간 길다(차이는 매우 작으며, 정답표 기준의 정성적 판단)</td><td>○</td></tr></table>
<p><b>② ㄷ의 원리 — 공명과 초공액의 경쟁</b></p>
<ol><li>케톤의 C=O는 π*<sub>C=O</sub>가 비어 있고 에너지가 낮으며, 카보닐 탄소의 δ+가 크다. 이웃 CH₃의 C–H σ 전자가 π*로 일부 비편재(초공액) → CH₃–C(=O) 결합에 약간의 이중결합성 → 짧아짐.</li>
<li>아마이드는 N의 비공유쌍이 굽은 화살표처럼 C–N 쪽으로 밀려 들어가고(n<sub>N</sub> → π*<sub>C=O</sub>), C=O π 전자는 O 위로 이동한다(H₃C–C(O⁻)=N⁺H₂ 공명 구조). π* 궤도는 N 쪽 기여로 이미 일부 채워지고 에너지가 높아져, CH₃의 초공액 받개 역할이 약해진다.</li>
<li>또한 공명으로 카보닐 탄소의 전자 결핍이 줄어 CH₃–C 결합의 극성 강화(짧아지는 요인)가 작다. 결과적으로 CH₃–C(=O) 결합은 아마이드에서 상대적으로 길다.</li></ol>
<p>같은 이유로 아마이드의 C=O 신축 진동수(≈1650–1690 cm⁻¹)는 케톤(≈1715 cm⁻¹)보다 낮고, C–N(≈1.33–1.38 Å)은 아민의 C–N(1.47 Å)보다 짧다.</p>""",
        "figs": [(F.f22, "ㄱ 치환도와 안정도, ㄴ 혼성과 결합각, ㄷ 표시된 CH₃–C(=O) 결합"),
                 (F.f22b, "아마이드 공명(굽은 화살표): C–N 부분 이중결합 → π*C=O 상승 → CH₃ 초공액 약화")],
        "extra": [
            ("원리 정리", """<table class="tb"><tr><th>성질</th><th>지배 요인</th><th>대표 비교</th></tr>
<tr><td>알켄 안정도</td><td>치환도(초공액), trans/cis(입체 반발)</td><td>2-methylbut-2-ene &gt; trans-2-butene &gt; cis-2-butene &gt; 1-butene</td></tr>
<tr><td>결합각</td><td>혼성(s성질), 고리 크기, 입체</td><td>sp 180° &gt; sp² 120° &gt; sp³ 109.5°; cyclopropane 60°(굽은 결합)</td></tr>
<tr><td>C–C 길이</td><td>혼성(s성질↑ → 짧음), 공명·초공액</td><td>C(sp³)–C(sp³) 1.54 &gt; C(sp³)–C(sp²) 1.50–1.52 &gt; C(sp²)–C(sp²) 1.47 &gt; 벤젠 1.39</td></tr>
<tr><td>C–N / C=O (아마이드)</td><td>n<sub>N</sub>→π*<sub>C=O</sub> 공명</td><td>C–N 짧아짐, C=O 길어짐·IR 진동수↓, C–N 회전 장벽 ≈ 75–85 kJ/mol</td></tr></table>
<p><b>예외·주의</b>: 알켄 안정도 비교는 같은 생성물로 수소화되는 이성질체끼리만 수소화열로 직접 비교할 수 있다. 결합 길이 비교에서 혼성이 같으면 공명·초공액의 미세 효과로 판단한다.</p>"""),
            ("27 임용 연관 분석", """<p><b>① 연관 기출</b>: 2009 1차 21번(안트라센의 공명 구조로 가장 짧은 C–C 결합 판단), 2012 1차 35번(히스타민 N의 혼성 — 비공유쌍의 공명 참여 여부), 2025 전공B 서술형 7번(tropone의 C=O 신축 파수 순서 — 공명에 따른 C=O 결합 차수), 2020 전공A 기입형 4번(N-아실화 생성물과 pKa — 아마이드 공명으로 N 염기도 감소), 2015 전공A 기입형 8번·2025 전공B 기입형 2번(사이클로헥세인 의자형·배형).</p>
<p><b>② 서술형 변형 예상</b>: “acetamide와 acetone의 C=O 신축 진동수와 CH₃–C(=O) 결합 길이를 비교하고, 그 이유를 공명 구조를 그려 서술하시오.” — 모범 답안: 아마이드는 H₃C–C(O⁻)=N⁺H₂ 공명 기여로 C=O 결합 차수가 낮아 ν(C=O)가 낮고(≈1690 vs 1715 cm⁻¹), π*C=O가 N에 의해 채워지고 높아져 CH₃ 초공액이 약해지므로 CH₃–C 결합이 약간 길다.</p>
<p><b>③ 체크포인트</b>: 결합 길이·진동수·회전 장벽·염기도는 모두 ‘공명에 의한 결합 차수 변화’ 하나로 설명된다. 알켄 안정도는 수소화열 그래프로 답할 준비.</p>"""),
        ],
        "faq": [
            ("ㄷ은 혼성이 같은데 왜 길이가 달라지나요?",
             "두 경우 모두 C(sp³)–C(sp²) 결합이라 큰 차이는 없고, 미세한 차이는 이웃 π계와의 초공액 정도가 결정합니다. 케톤의 π*C=O가 더 낮고 비어 있어 CH₃ 초공액이 강하므로 케톤 쪽이 약간 짧습니다."),
            ("사이클로헥세인 결합각이 109.5°가 아니라 111°인 이유는?",
             "의자형은 비틀림 무리가 없는 엇갈린 배치를 이루면서 C–C–C가 약간 벌어진(≈111°) 형태가 가장 안정합니다. 각 무리는 거의 0입니다."),
            ("ㄱ의 두 알켄을 실험으로 비교하려면?",
             "둘 다 H₂/Pt로 3-methylpentane이 되므로 수소화열을 측정해 작은 쪽(삼치환)이 더 안정하다고 결론냅니다."),
        ],
    },
    # ------------------------------------------------------------------ 23
    {
        "id": "md-2027-23", "year": 2027, "q": 23, "exam": "MDEET 자연과학Ⅱ 23번", "pts": 3,
        "sub": "입체화학 — 쐐기 구조·뉴먼 투영·의자형의 동일성 판정",
        "title": "trans-1,2-dimethylcyclohexane 거울상 쌍, 2-methylbutane 뉴먼 투영 쌍, 2,5-dimethylcyclohexan-1-amine 평면식–의자형",
        "stem": "각 쌍이 서로 같은 화합물의 구조인 것만을 고르시오.<br>"
                "ㄱ. (C1 CH₃ 쐐기, C2 CH₃ 점선) vs (C1 CH₃ 점선, C2 CH₃ 쐐기)인 1,2-dimethylcyclohexane<br>"
                "ㄴ. 앞 탄소(H, H, CH₃)·뒤 탄소(CH₃, CH₃, H)인 두 엇갈린 뉴먼 투영<br>"
                "ㄷ. NH₂ 쐐기·C2-CH₃ 점선·C5-CH₃ 점선인 평면 구조식 vs NH₂·CH₃가 놓인 의자형<br>"
                "① ㄱ ② ㄷ ③ ㄱ, ㄴ ④ ㄴ, ㄷ ⑤ ㄱ, ㄴ, ㄷ",
        "answer": "<b>④</b> — ㄱ ✗((1R,2R)과 (1S,2S)의 trans-1,2-dimethylcyclohexane: 서로 거울상이성질체), "
                  "ㄴ ○(둘 다 2-methylbutane의 CH₃/CH₃ gauche 1개·anti 1개 엇갈린 형태 — 비카이랄 분자의 형태 이성질체이므로 같은 화합물), "
                  "ㄷ ○(의자형: NH₂ eq·위, C2-CH₃ eq·아래, C5-CH₃ ax·아래 → 평면식의 위/아래 관계와 고리 방향이 모두 일치, (1S,2S,5R)).",
        "concepts": [
            "같은 화합물 = 결합 회전·고리 뒤집기(형태 변화)로 겹쳐지는 구조. 거울상·부분입체이성질체는 다른 화합물",
            "1,2-이치환 사이클로헥세인: cis = ax/eq, trans = ax/ax 또는 eq/eq; 1,3: cis = eq/eq; 1,4: cis = ax/eq",
            "trans-1,2-dimethylcyclohexane은 키랄(거울상 쌍 존재), cis-1,2는 메조(고리 뒤집기로 상호 전환)",
            "뉴먼 투영: 앞 탄소 결합은 중심에서, 뒤 탄소 결합은 원 둘레에서 — 먼저 치환기 구성(constitution) 확인",
            "의자형에서 ‘위/아래’ 판단: 축 방향은 그 탄소의 퍼커 방향과 같고, 적도 방향은 반대쪽으로 약간 기운다",
        ],
        "sol": """<p><b>① 보기별 판정</b></p>
<table class="tb"><tr><th>보기</th><th>분석</th><th>판정</th></tr>
<tr><td>ㄱ</td><td>두 구조 모두 CH₃가 하나는 위(쐐기), 하나는 아래(점선) → trans. 왼쪽 C1: 순위 C2 &gt; 고리 CH₂ &gt; CH₃, H 뒤 → R; C2도 R → (1R,2R). 오른쪽은 쐐기/점선이 바뀌어 (1S,2S). 수직 거울면에 대해 서로 거울상이며, 분자 내 대칭면이 없어 겹쳐지지 않음 → <b>거울상이성질체</b></td><td>✗</td></tr>
<tr><td>ㄴ</td><td>왼쪽: 앞 C(H 위, H 왼아래, CH₃ 오른아래), 뒤 C(CH₃ 왼위, H 오른위, CH₃ 아래). 오른쪽: 앞 C(H, CH₃ 왼아래, H), 뒤 C(H, CH₃ 오른위, CH₃ 아래). 두 경우 모두 앞 C = CH₂(에틸의 CH₂, 앞 CH₃ 포함), 뒤 C = CH(CH₃)₂ → <b>2-methylbutane</b>. 앞 CH₃는 뒤 CH₃ 하나와 gauche, 하나와 anti — 두 투영은 같은 에너지의 형태(서로 거울상 관계의 형태)이며 C2–C3 회전으로 상호 전환. 분자는 비카이랄</td><td>○</td></tr>
<tr><td>ㄷ</td><td>평면식: C1 NH₂ 위, C2 CH₃ 아래(1,2-trans), C5 CH₃ 아래(C1과 1,3-trans, C2와 1,4-cis). 의자형: NH₂ 결합은 기울어진 적도(eq), C2-CH₃ 적도, C5-CH₃ 수직 축(ax, 아래). C1·C5는 ‘아래’ 퍼커 탄소 → C1의 eq는 위쪽으로 기움(NH₂ 위), C5의 ax는 아래; C2는 ‘위’ 퍼커 탄소 → eq는 아래쪽(CH₃ 아래). 위/아래 관계가 평면식과 동일하고, 위에서 볼 때 C1→C2→…방향(반시계)도 같으므로 거울상이 아님 → (1S,2S,5R) 동일</td><td>○</td></tr></table>
<p><b>② ㄷ의 R/S 확인(평면식)</b>: C1: NH₂(①) &gt; C2(C,C,H)(②) &gt; C6(C,H,H)(③), H 뒤 → 반시계 → <b>S</b>. C2: C1(N,C,H) &gt; C3 &gt; CH₃, H 앞 → 시계가 뒤집혀 <b>S</b>. C5: C6(→C1의 N에서 승) &gt; C4 &gt; CH₃, H 앞 → <b>R</b>. 의자형도 같은 값을 준다.</p>
<p><b>③ 함정</b>: ㄱ은 ‘trans끼리 같다’고 착각하기 쉽다. cis-1,2-dimethylcyclohexane이었다면 메조 화합물(실온에서 의자 뒤집기로 두 거울상 형태가 빠르게 전환)이라 같은 화합물이 된다. ㄷ은 의자형의 ax/eq를 ‘위/아래’로 바꾸는 과정과 고리 방향 확인이 핵심이다.</p>""",
        "figs": [(F.f23, "ㄱ: trans-1,2-dimethylcyclohexane의 (1R,2R)/(1S,2S) 거울상 쌍, ㄴ: 두 뉴먼 투영 = 2-methylbutane"),
                 (F.f23b, "ㄷ: 평면 구조식의 위/아래 관계를 의자형의 ax/eq로 옮겨 비교")],
        "extra": [
            ("원리 정리", """<table class="tb"><tr><th>관계</th><th>cis</th><th>trans</th></tr>
<tr><td>1,2</td><td>ax/eq (메조, 1,2-dimethyl)</td><td>eq/eq ⇌ ax/ax (키랄)</td></tr>
<tr><td>1,3</td><td>eq/eq ⇌ ax/ax (메조)</td><td>ax/eq (키랄)</td></tr>
<tr><td>1,4</td><td>ax/eq (비카이랄)</td><td>eq/eq ⇌ ax/ax (비카이랄)</td></tr></table>
<p><b>동일성 판정 절차</b>: ① 분자식·연결(constitution) 비교 → 다르면 구조 이성질체. ② 같으면 각 입체 중심의 R/S 비교: 모두 같으면 동일(또는 형태 이성질체), 모두 반대면 거울상, 일부만 다르면 부분입체. ③ 메조는 R/S가 ‘모두 반대’여도 동일 화합물.</p>
<p><b>의자형 읽기</b>: 수직선 = 축(ax), 고리 결합과 평행하게 기운 선 = 적도(eq). 각 탄소의 ax는 그 꼭짓점이 향한 방향(위 꼭짓점이면 위). eq는 ax와 반대 방향으로 약간 기운다.</p>"""),
            ("27 임용 연관 분석", """<p><b>① 연관 기출</b>: 2013 1차 34번(뉴먼 투영 A·B의 해석 — 구조 이성질체/입체이성질체 수), 2011 1차 34번(타타르산의 뉴먼 투영 — 키랄 vs 메조), 2021 전공B 서술형 8번(neomenthyl/menthyl chloride의 의자형 E2·뉴먼 투영), 2016 전공A 서술형 13번(A값에 따른 의자형 평형), 2025 전공B 기입형 2번(의자형·보트형 그리기와 점군).</p>
<p><b>② 서술형 변형 예상</b>: “(1S,2S,5R)-2,5-dimethylcyclohexan-1-amine의 두 의자형을 그리고, 더 안정한 형태와 그 이유를 A값으로 서술하시오.” — 모범 답안: 형태 Ⅰ(NH₂ eq, 2-CH₃ eq, 5-CH₃ ax)와 형태 Ⅱ(NH₂ ax, 2-CH₃ ax, 5-CH₃ eq). Ⅰ은 축 CH₃ 1개(≈7.3 kJ/mol), Ⅱ는 축 NH₂ + 축 CH₃(≈5.9 + 7.3 kJ/mol)이므로 Ⅰ이 더 안정.</p>
<p><b>③ 체크포인트</b>: 쐐기 ↔ 의자형 ↔ 뉴먼 변환을 손으로 빠르게 할 것. trans-1,2(키랄)와 cis-1,2(메조)의 차이는 임용 객관식·서술형 모두 반복 출제 소재.</p>"""),
        ],
        "faq": [
            ("ㄱ의 두 구조를 180° 돌리면 겹쳐지지 않나요?",
             "종이 평면 안에서 돌리거나 수직축으로 뒤집으면 쐐기/점선과 좌우가 함께 바뀌어 원래 오른쪽 구조로만 돌아옵니다. 왼쪽 구조와는 겹쳐지지 않으므로 거울상입니다(R,R vs S,S)."),
            ("ㄴ의 두 투영은 거울상 형태인데 왜 같은 화합물인가요?",
             "2-methylbutane은 입체 중심이 없는 비카이랄 분자입니다. 거울상 관계의 ‘형태’는 단일 결합 회전으로 바로 전환되므로 같은 화합물의 두 형태 이성질체일 뿐입니다."),
            ("ㄷ에서 의자 뒤집기를 하면 달라지나요?",
             "뒤집으면 ax/eq가 모두 바뀌지만 위/아래 관계는 그대로라 같은 분자의 다른 형태입니다. 문항의 의자형은 축 CH₃가 1개뿐인 더 안정한 형태입니다."),
        ],
    },
    # ------------------------------------------------------------------ 24
    {
        "id": "md-2027-24", "year": 2027, "q": 24, "exam": "MDEET 자연과학Ⅱ 24번", "pts": 4,
        "sub": "입체화학 — 피셔 투영과 R/S, 알도테트로스 입체이성질체",
        "title": "L-threose의 C2 배열, 입체이성질체 수, 지그재그 구조와의 관계",
        "stem": "L-threose의 피셔 투영도(CHO / H–C*–OH / HO–C–H / CH₂OH)에 대한 설명으로 옳은 것만을 고르시오.<br>"
                "ㄱ. *로 표시된 탄소의 절대 배열은 (R)이다.<br>"
                "ㄴ. 모든 입체이성질체 개수는 2이다.<br>"
                "ㄷ. (C2-OH 쐐기, C3-OH 점선인 지그재그 구조)와 거울상이성질체 관계이다.<br>"
                "① ㄱ ② ㄴ ③ ㄱ, ㄷ ④ ㄴ, ㄷ ⑤ ㄱ, ㄴ, ㄷ",
        "answer": "<b>①</b> — ㄱ ○(C2: OH &gt; CHO &gt; C3, H가 가로줄 → 반시계(S)를 뒤집어 R), "
                  "ㄴ ✗(입체 중심 2개, 메조 없음 → 2² = 4: D/L-threose, D/L-erythrose), "
                  "ㄷ ✗(지그재그 구조는 (2R,3R) = D-erythrose; L-threose (2R,3S)와 C3 한 곳만 다른 부분입체이성질체).",
        "concepts": [
            "피셔 투영: 가로줄 = 관찰자 쪽(쐐기), 세로줄 = 뒤쪽(점선)",
            "R/S: 최저 순위(H)가 가로줄에 있으면 ①→②→③ 회전 방향을 반대로 읽는다",
            "CIP 순위: –OH &gt; –CHO(O,O,H) &gt; –CH(OH)R(O,C,H) &gt; –CH₂OH(O,H,H) &gt; H",
            "D/L: 카보닐에서 가장 먼 입체 중심(끝에서 두 번째 C)의 OH가 오른쪽 D, 왼쪽 L",
            "erythro(두 OH 같은 쪽) / threo(반대쪽); 입체이성질체 최대 수 2ⁿ",
        ],
        "sol": """<p><b>① ㄱ — C2의 배열</b>: C2의 네 치환기: OH(오른쪽 가로), CHO(위), C3(아래), H(왼쪽 가로). 순위: OH(①) &gt; CHO(O,O,H)(②) &gt; C3 = CH(OH)CH₂OH(O,C,H)(③) &gt; H(④). ①(오른쪽) → ②(위) → ③(아래)는 반시계 방향(S처럼 보임). 그러나 H가 가로줄(관찰자 쪽)에 있으므로 반대로 읽어 <b>R</b>. ○</p>
<p><b>② ㄴ — 입체이성질체 수</b>: 알도테트로스 HOCH₂–CH(OH)–CH(OH)–CHO는 입체 중심 2개(C2, C3)이고 양 끝이 달라 메조가 없다 → 2² = <b>4개</b>: D-erythrose(2R,3R), L-erythrose(2S,3S), D-threose(2S,3R), L-threose(2R,3S). ✗</p>
<p><b>③ ㄷ — 지그재그 구조</b>: C1(CHO)이 왼쪽 위, C2(아래 꼭짓점)에 OH 쐐기(아래), C3(위 꼭짓점)에 OH 점선(위), C4 CH₂OH.</p>
<table class="tb"><tr><th>탄소</th><th>순위와 배치</th><th>배열</th></tr>
<tr><td>C2</td><td>OH(아래, 앞) ① → C1(왼쪽 위) ② → C3(오른쪽 위) ③, H 뒤 → 시계</td><td>R</td></tr>
<tr><td>C3</td><td>OH(위, 뒤) ① → C2(왼쪽 아래) ② → C4(오른쪽 아래) ③ 반시계, H 앞 → 뒤집음</td><td>R</td></tr></table>
<p>→ (2R,3R) = <b>D-erythrose</b>. L-threose(2R,3S)와 비교하면 C2는 같고 C3만 다르므로 <b>부분입체이성질체(C3 에피머)</b>이다. 거울상이 되려면 두 중심이 모두 반대인 (2S,3R) = D-threose여야 한다. ✗</p>
<p><b>④ 피셔 투영으로 바꾸어 확인</b>: 지그재그를 세로로 세우면 C2·C3의 OH가 모두 오른쪽 → D-erythrose 피셔 투영과 일치한다.</p>""",
        "figs": [(F.f24, "L-threose C2의 R 판정(H 가로 → 회전 방향 반대)과 알도테트로스 4개의 피셔 투영"),
                 (F.f24b, "ㄷ의 지그재그 구조 = D-erythrose (2R,3R): L-threose의 부분입체이성질체")],
        "extra": [
            ("원리 정리", """<p><b>피셔 투영 다루기 규칙</b></p>
<ul><li>종이 평면에서 180° 회전 → 같은 분자. 90° 회전 → 거울상(배열 반전).</li>
<li>한 탄소의 치환기 두 개 교환 → 배열 반전; 두 번 교환 → 원래대로.</li>
<li>H가 세로줄이면 보이는 방향 그대로, 가로줄이면 반대로 R/S를 읽는다.</li></ul>
<table class="tb"><tr><th>이름</th><th>C2</th><th>C3</th><th>관계</th></tr>
<tr><td>D-erythrose</td><td>R</td><td>R</td><td rowspan="2">거울상 쌍</td></tr><tr><td>L-erythrose</td><td>S</td><td>S</td></tr>
<tr><td>D-threose</td><td>S</td><td>R</td><td rowspan="2">거울상 쌍</td></tr><tr><td>L-threose</td><td>R</td><td>S</td></tr></table>
<p>erythrose ↔ threose는 부분입체이성질체. 산화(HNO₃)로 양 끝을 COOH로 바꾸면 erythrose → 메조-타타르산, threose → 키랄 타타르산이 된다(메조 판정의 고전 예).</p>"""),
            ("27 임용 연관 분석", """<p><b>① 연관 기출</b>: 2000 서술형 10번(2,3-dichlorobutane 입체이성질체와 피셔 투영), 2011 1차 34번(타타르산 키랄/메조, 부분입체이성질체의 성질), 2019 전공A 기입형 5번(글루탐산 — 아미노산 구조·L 표기), 2023 전공B 기입형 2번(메조 화합물의 입체구조), 2024 전공B 기입형 2번(리파제 분할 생성물의 R/S와 ee).</p>
<p><b>② 서술형 변형 예상</b>: “L-threose를 NaBH₄로 환원한 생성물과 HNO₃로 산화한 생성물의 광학 활성 여부를 피셔 투영을 그려 판단하시오.” — 모범 답안: 환원 → threitol(양 끝 CH₂OH, threo) — 대칭면 없음 → 광학 활성(L-threitol). 산화 → (R,R) 또는 (S,S) 타타르산(키랄) → 광학 활성. D-erythrose라면 두 경우 모두 메조(erythritol, meso-타타르산) → 광학 비활성.</p>
<p><b>③ 체크포인트</b>: 피셔 ↔ 지그재그 변환, H가 가로줄일 때의 반전 규칙, 2ⁿ 규칙과 메조 감소를 빠르게 처리할 것.</p>"""),
        ],
        "faq": [
            ("C3가 CHO보다 순위가 낮은 이유는?",
             "첫 원자는 둘 다 C이므로 붙은 원자 집합을 비교합니다. CHO는 이중결합 O를 두 번 세어 (O,O,H), C3는 (O,C,H)이므로 CHO가 높습니다."),
            ("D/L과 R/S는 관련이 있나요?",
             "직접적인 대응 관계는 없습니다. D/L은 글리세르알데하이드 기준의 상대 배열, R/S는 CIP 규칙에 따른 절대 배열 표기입니다. L-threose의 C3(D/L 기준 탄소)는 S, C2는 R입니다."),
            ("ㄷ 구조가 L-threose 자신일 가능성은?",
             "L-threose는 (2R,3S)인데 ㄷ은 (2R,3R)이므로 다릅니다. 지그재그에서 인접한 두 OH가 쐐기/점선으로 반대이면 피셔 투영에서는 같은 쪽(erythro)이 된다는 점을 기억하세요."),
        ],
    },
    # ------------------------------------------------------------------ 25
    {
        "id": "md-2027-25", "year": 2027, "q": 25, "exam": "MDEET 자연과학Ⅱ 25번", "pts": 4,
        "sub": "산과 염기·방향족성 — C–H 산도, 아민 염기도, 헤테로고리의 수용성",
        "title": "cyclopentane vs cyclopentadiene 산도, pyrrolidine vs pyrrole 염기도, THF vs furan 용해도",
        "stem": "두 화합물의 물리·화학적 성질의 크기 비교가 옳은 것만을 고르시오.<br>"
                "ㄱ. 밑줄 친 수소의 산도: cyclopentane &gt; 1,3-cyclopentadiene(CH₂의 H)<br>"
                "ㄴ. 질소의 염기도: pyrrolidine &gt; pyrrole<br>"
                "ㄷ. 물에서의 용해도: tetrahydrofuran &gt; furan<br>"
                "① ㄱ ② ㄷ ③ ㄱ, ㄴ ④ ㄴ, ㄷ ⑤ ㄱ, ㄴ, ㄷ",
        "answer": "<b>④</b> — ㄱ ✗(cyclopentadiene의 짝염기 C₅H₅⁻는 6π 방향족 → pKa ≈ 16, cyclopentane ≈ 50: cyclopentadiene이 훨씬 강한 산), "
                  "ㄴ ○(pyrrolidine sp³ N, pKaH ≈ 11.3; pyrrole의 N 비공유쌍은 방향족 6π의 일부 → pKaH ≈ −3.8), "
                  "ㄷ ○(THF의 O 비공유쌍은 국재되어 강한 수소결합 받개 → 물과 완전 혼화; furan은 비공유쌍 하나가 방향족에 비편재, 쌍극자 작음 → 약간만 용해).",
        "concepts": [
            "산도 = 짝염기 안정성: 방향족 짝염기(4n+2 π) 형성 시 산도 급증",
            "Hückel 규칙: 고리·평면·완전 공액·(4n+2)π → 방향족",
            "아민 염기도: 비공유쌍이 국재(sp³)일수록 강염기; 공명·방향족 참여 시 약염기",
            "피롤의 양성자화는 N이 아니라 C2(α)에서 일어난다(N 양성자화는 방향족성 상실)",
            "수용성: 수소결합 받개 능력(비공유쌍의 가용성)과 극성(쌍극자 모멘트)",
        ],
        "sol": """<p><b>① 보기별 판정</b></p>
<table class="tb"><tr><th>보기</th><th>비교</th><th>근거</th><th>판정</th></tr>
<tr><td>ㄱ</td><td>pKa: cyclopentane ≈ 50, cyclopentadiene ≈ 16</td><td>cyclopentadiene의 sp³ CH₂에서 H⁺가 떨어지면 그 탄소가 sp²가 되어 고리 전체가 공액된 C₅H₅⁻(6π, 방향족)가 된다. 음전하가 다섯 탄소에 고르게 비편재 → 짝염기 매우 안정. cyclopentane의 짝염기는 국재된 sp³ 탄소 음이온 → 매우 불안정. 산도는 cyclopentadiene ≫ cyclopentane</td><td>✗</td></tr>
<tr><td>ㄴ</td><td>pKaH: pyrrolidine 11.3, pyrrole ≈ −3.8</td><td>pyrrolidine: 포화 2차 아민, sp³ N의 비공유쌍이 국재 → 전형적 강한 아민 염기. pyrrole: N은 sp², 비공유쌍이 p 궤도에서 4개 π 전자와 함께 6π 방향족을 구성 → 양성자화하면 방향족성 상실. 실제 양성자화는 C2에서 일어나며 매우 약한 염기</td><td>○</td></tr>
<tr><td>ㄷ</td><td>THF: 물과 완전 혼화 / furan ≈ 1 g/100 mL</td><td>THF의 sp³ O는 두 비공유쌍이 모두 국재 → 물의 O–H와 강한 수소결합 받개, 쌍극자 ≈ 1.7 D. furan은 O의 비공유쌍 1개가 방향족 6π에 참여해 고리로 비편재, 고리 π 쪽으로 전자가 이동해 쌍극자 ≈ 0.7 D로 작음 → 수소결합 받개 능력·극성 모두 작음</td><td>○</td></tr></table>
<p><b>② 공통 원리</b>: 세 보기 모두 ‘전자쌍이 방향족 π계에 참여하느냐’로 정리된다. 참여하면 (ㄱ) 짝염기가 안정해져 산도↑, (ㄴ) 비공유쌍을 내놓기 어려워 염기도↓, (ㄷ) 수소결합 받개 능력↓.</p>""",
        "figs": [(F.f25, "ㄱ 방향족 짝염기 C₅H₅⁻, ㄴ N 비공유쌍의 국재 vs 6π 참여, ㄷ O 비공유쌍과 수소결합 받개 능력")],
        "extra": [
            ("원리 정리", """<table class="tb"><tr><th>화합물</th><th>비공유쌍 상태</th><th>pKa(산) / pKaH(짝산)</th></tr>
<tr><td>cyclopentane C–H</td><td>—</td><td>≈ 50</td></tr>
<tr><td>cyclopentadiene CH₂</td><td>짝염기 6π 방향족</td><td>≈ 16</td></tr>
<tr><td>cycloheptatriene CH₂</td><td>짝염기 8π 반방향족</td><td>≈ 36–39</td></tr>
<tr><td>pyrrolidine</td><td>sp³ 국재</td><td>pKaH 11.3</td></tr>
<tr><td>pyridine</td><td>sp² 궤도(π계 밖)</td><td>pKaH 5.2</td></tr>
<tr><td>pyrrole</td><td>p 궤도, 6π 참여</td><td>pKaH ≈ −3.8, N–H pKa ≈ 17</td></tr>
<tr><td>aniline</td><td>벤젠 고리와 공명</td><td>pKaH 4.6</td></tr></table>
<p><b>정리</b>: 비공유쌍의 s성질이 클수록(sp &gt; sp² &gt; sp³) 염기도↓, 공명·방향족 참여 시 염기도↓. 산도는 짝염기에서 음전하의 비편재·방향족화·전기음성도·s성질을 본다.</p>"""),
            ("27 임용 연관 분석", """<p><b>① 연관 기출</b>: 2005 서술형 12번(cyclopentadiene vs cycloheptatriene 산성도와 짝염기의 방향족성), 2022 전공A 기입형 2번(풀벤 A~D의 C–H pKa), 2013 1차 35번(혼성·원자 크기·방향족성·치환기 효과에 따른 산도 — 피롤륨 vs 피리디늄), 2012 1차 35번(히스타민 N의 혼성 — 피롤형/피리딘형 N), 2004 서술형 9번(pyrrole 포함 염기 세기 순서), 2018 전공B 서술형 4번(퓨란의 친전자성 치환과 σ 착물 공명), 2009 1차 24번(Hückel 규칙 판정).</p>
<p><b>② 서술형 변형 예상</b>: “pyrrole과 pyridine의 염기도를 비교하고, pyrrole이 양성자화되는 위치와 그 이유를 공명 구조로 서술하시오.” — 모범 답안: pyridine(pKaH 5.2)의 비공유쌍은 고리 평면의 sp² 궤도에 있어 방향족성과 무관하게 H⁺와 결합 가능 → 더 강한 염기. pyrrole은 비공유쌍이 6π에 포함되어 N 양성자화 시 방향족성 상실 → 매우 약한 염기; 양성자화는 C2에서 일어나 양전하가 N까지 비편재된 이미늄형 양이온(N⁺=C)이 생긴다.</p>
<p><b>③ 체크포인트</b>: ‘비공유쌍이 π계 안인가 밖인가’를 구조마다 즉시 판단. 방향족 이온(C₅H₅⁻, C₇H₇⁺)과 반방향족 이온의 pKa 경향은 서술형 단골.</p>"""),
        ],
        "faq": [
            ("cyclopentadiene의 pKa 16이면 물(15.7)과 비슷한데 정말 탄화수소인가요?",
             "네. 짝염기의 방향족 안정화 덕분에 알코올 수준의 산도를 갖는 이례적인 탄화수소입니다. NaH나 n-BuLi로 쉽게 C₅H₅⁻Na⁺를 만들어 페로센 합성 등에 씁니다."),
            ("피롤의 N–H는 산성인가요?",
             "pKa ≈ 17로 약한 산입니다. N–H가 떨어져도 방향족 피롤라이드 음이온이 되므로 아민 N–H(≈35)보다 훨씬 산성입니다."),
            ("THF가 물과 완전히 섞이는데 diethyl ether는 왜 덜 섞이나요?",
             "THF는 고리 구조라 O 주위의 알킬기가 뒤로 묶여 있어 비공유쌍이 노출되고 수소결합에 유리합니다. diethyl ether는 에틸기가 O를 가리고 소수성 부분이 커 ≈ 7 g/100 mL 정도만 녹습니다."),
        ],
    },
    # ------------------------------------------------------------------ 26
    {
        "id": "md-2027-26", "year": 2027, "q": 26, "exam": "MDEET 자연과학Ⅱ 26번", "pts": 5,
        "sub": "알카인의 환원과 알켄의 에폭시화·개환 — 입체특이성(syn/anti, 메조/라셈)",
        "title": "but-2-yne → Lindlar(cis) → mCPBA / Na, NH₃(trans) → mCPBA → HO⁻ 개환",
        "stem": "but-2-yne을 H₂/Lindlar 촉매로 환원해 A, A를 mCPBA로 에폭시화해 B; Na/NH₃(l)로 환원해 C, C를 1. mCPBA 2. HO⁻, H₂O로 처리해 D를 얻었다. 옳은 것만을 고르시오.<br>"
                "ㄱ. A와 C는 구조 이성질체 관계이다.<br>"
                "ㄴ. B는 cis-2,3-dimethyloxirane(두 CH₃ 쐐기)이다.<br>"
                "ㄷ. D는 메조 화합물이다.<br>"
                "① ㄱ ② ㄷ ③ ㄱ, ㄴ ④ ㄴ, ㄷ ⑤ ㄱ, ㄴ, ㄷ",
        "answer": "<b>④</b> — A = cis-but-2-ene(Lindlar, syn 첨가), C = trans-but-2-ene(용해 금속 환원, anti) → ㄱ ✗(연결이 같은 cis/trans 부분입체이성질체, 구조 이성질체 아님). "
                  "ㄴ ○(mCPBA는 syn·입체특이적 → cis 알켄에서 cis-에폭사이드, 메조). "
                  "ㄷ ○(trans-에폭사이드(라셈)를 HO⁻가 뒤쪽에서 SN2 개환 → anti 다이올 = meso-butane-2,3-diol).",
        "concepts": [
            "Lindlar 촉매(Pd/BaSO₄ 또는 CaCO₃, 퀴놀린 피독): 알카인 → cis-알켄 (표면 syn 첨가, 알켄에서 멈춤)",
            "Na 또는 Li/NH₃(l): 라디칼 음이온 → 비닐 라디칼(trans 선호) → 비닐 음이온 → trans-알켄",
            "과산(mCPBA) 에폭시화: 협동 ‘나비형’ 전이상태, syn 첨가, 알켄 기하가 그대로 보존(입체특이적)",
            "염기성 에폭사이드 개환: SN2, 덜 가려진 C 공격, 공격 탄소 반전 → 전체적으로 anti 다이하이드록시화",
            "cis-알켄 + anti 첨가 → 라셈(threo); trans-알켄 + anti 첨가 → 메조(erythro) — 대칭 알켄",
        ],
        "sol": """<p><b>① 반응 경로</b></p>
<ol><li><b>A</b>: H₂가 피독된 Pd 표면에서 알카인의 같은 면으로 전달 → <b>cis-but-2-ene</b>.</li>
<li><b>B</b>: mCPBA의 말단 O가 C=C π 전자를 받아들이며 O–O가 끊기고, 동시에 O–H의 H가 카보닐 O로 옮겨지는 협동 과정 → 두 C–O 결합이 같은 면에서 생성 → <b>cis-2,3-dimethyloxirane</b>((2R,3S), 대칭면을 가진 메조).</li>
<li><b>C</b>: Na가 전자를 주어 라디칼 음이온 → NH₃가 양성자화 → 비닐 라디칼(두 CH₃가 멀어지는 trans 배치) → 두 번째 전자로 비닐 음이온 → 양성자화 → <b>trans-but-2-ene</b>.</li>
<li><b>D</b>: mCPBA로 trans-2,3-dimethyloxirane((2R,3R)+(2S,3S) 라셈). HO⁻의 비공유쌍이 C–O σ*의 뒤쪽으로 들어가며(굽은 화살표: HO⁻ → C, C–O 결합 전자 → O) 공격 탄소가 반전 → 알콕사이드 → H₂O에서 양성자 이동 → <b>meso-butane-2,3-diol</b>((2R,3S)). 어느 거울상에서 출발하든, 어느 탄소를 공격하든 같은 메조 생성물.</li></ol>
<p><b>② 보기별 판정</b></p>
<table class="tb"><tr><th>보기</th><th>근거</th><th>판정</th></tr>
<tr><td>ㄱ</td><td>A(cis)·C(trans)는 원자 연결이 같고 공간 배열만 다름 → 입체이성질체 중 <b>부분입체이성질체</b>. ‘구조(constitutional) 이성질체’는 연결 순서가 다른 경우</td><td>✗</td></tr>
<tr><td>ㄴ</td><td>syn 에폭시화로 cis 기하 보존. 두 CH₃가 모두 쐐기 = cis = 메조 에폭사이드</td><td>○</td></tr>
<tr><td>ㄷ</td><td>trans 알켄에 대한 전체 anti 첨가(에폭시화 syn + 개환 반전) → 메조 다이올</td><td>○</td></tr></table>
<p><b>③ 비교</b>: A(cis)를 같은 방법(1. mCPBA 2. HO⁻)으로 처리하면 라셈 (2R,3R)/(2S,3S)-다이올이 되고, OsO₄(syn 다이하이드록시화)로 처리하면 A → 메조, C → 라셈이 된다.</p>""",
        "figs": [(F.f26, "but-2-yne의 두 환원 경로와 에폭시화·개환 생성물 A~D"),
                 (F.f26b, "D 생성 메커니즘: HO⁻의 뒤쪽 SN2 공격(반전) → 알콕사이드 → meso-다이올")],
        "extra": [
            ("원리 정리", """<table class="tb"><tr><th>반응</th><th>첨가 방식</th><th>cis-2-butene</th><th>trans-2-butene</th></tr>
<tr><td>Br₂ (브로모늄)</td><td>anti</td><td>라셈 dibromide</td><td>메조 dibromide</td></tr>
<tr><td>OsO₄ 또는 찬 KMnO₄</td><td>syn</td><td>메조 다이올</td><td>라셈 다이올</td></tr>
<tr><td>1. mCPBA 2. H₃O⁺ 또는 HO⁻</td><td>anti</td><td>라셈 다이올</td><td>메조 다이올</td></tr>
<tr><td>mCPBA만</td><td>syn</td><td>cis(메조) 에폭사이드</td><td>trans(라셈) 에폭사이드</td></tr>
<tr><td>H₂/Pt</td><td>syn</td><td colspan="2">(대칭 치환일 때 메조/라셈 판정에 사용)</td></tr></table>
<p><b>알카인 환원</b>: H₂/Pd–C(과량) → 알케인, H₂/Lindlar 또는 P-2 Ni → cis-알켄, Na(Li)/NH₃(l) → trans-알켄(말단 알카인은 아세틸라이드가 되어 잘 환원되지 않음).</p>"""),
            ("27 임용 연관 분석", """<p><b>① 연관 기출</b>: 2015 전공A 서술형 3번(2-butyne → cis-2-butene → syn/anti 다이하이드록시화, 메조 vs 라셈 — 거의 같은 골격), 2023 전공B 기입형 2번(meso-2,3-dibromobutane에서 출발 알켄 추론, 에폭시화·가수분해로 메조), 2026 전공A 기입형 1번(Wittig → m-CPBA → cis-2,3-diphenyloxirane), 2025 전공A 서술형 11번(아세틸라이드 알킬화–용해 금속 환원으로 E-알켄), 2006 서술형 12번(Lindlar 환원), 2007 서술형 11번·2012 1차 36번(에폭사이드 개환의 입체 특이성).</p>
<p><b>② 서술형 변형 예상</b>: “trans-2-butene에서 meso-butane-2,3-diol을 얻는 과정을 메커니즘(굽은 화살표)으로 나타내고, cis-2-butene을 같은 조건에서 반응시킨 생성물의 광학 활성 여부를 쓰시오.” — 모범 답안: 협동 syn 에폭시화 → HO⁻ 뒤쪽 공격(SN2, 반전) → 알콕사이드 양성자화 → 메조. cis 알켄은 cis-에폭사이드(메조) → 두 탄소 중 어느 쪽을 공격하느냐에 따라 (R,R)/(S,S)가 1:1 → 라셈, 광학 비활성(분할 가능).</p>
<p><b>③ 체크포인트</b>: ‘알켄 기하 × 첨가 방식(syn/anti) → 메조/라셈’ 표를 외우기보다 한 번 그려서 확인하는 습관. 구조 이성질체 vs 입체이성질체(부분입체) 용어 구분은 객관식 함정 단골.</p>"""),
        ],
        "faq": [
            ("Lindlar 촉매에서 퀴놀린의 역할은?",
             "Pd 표면의 활성 자리를 일부 피독해 알켄이 다시 흡착·수소화되는 것을 막습니다. 알카인은 알켄보다 표면에 더 강하게 흡착하므로 알카인만 선택적으로 환원됩니다."),
            ("B는 키랄 중심이 2개인데 왜 광학 비활성인가요?",
             "cis-2,3-dimethyloxirane은 (2R,3S)로 두 C 사이와 O를 지나는 대칭면을 가진 메조 화합물입니다."),
            ("D를 얻을 때 산성(H₃O⁺) 개환을 해도 같은가요?",
             "대칭 에폭사이드이므로 위치 선택성 문제가 없고, 산성 개환도 뒤쪽 공격(반전)이라 똑같이 메조 다이올을 줍니다."),
        ],
    },
    # ------------------------------------------------------------------ 27
    {
        "id": "md-2027-27", "year": 2027, "q": 27, "exam": "MDEET 자연과학Ⅱ 27번", "pts": 4,
        "sub": "친전자성 방향족 치환 — 보호기(아세틸화)와 지향성, 반응 순서",
        "title": "aniline → acetanilide → 4-bromoacetanilide → 4-bromoaniline; nitrobenzene → 3-bromonitrobenzene → 3-bromoaniline",
        "stem": "aniline을 CH₃COCl/pyridine으로 처리해 A, (가)로 B, HO⁻/H₂O·가열로 4-bromoaniline을 얻고, nitrobenzene을 Br₂/FeBr₃로 처리해 C, Fe/HCl로 D를 얻었다. 옳은 것만을 고르시오.<br>"
                "ㄱ. A는 acetanilide(PhNHCOCH₃)이다.<br>"
                "ㄴ. Br₂는 (가)로 적절하다.<br>"
                "ㄷ. D는 3-bromoaniline이다.<br>"
                "① ㄴ ② ㄷ ③ ㄱ, ㄴ ④ ㄱ, ㄷ ⑤ ㄱ, ㄴ, ㄷ",
        "answer": "<b>⑤</b> — ㄱ ○(아민의 N-아실화, pyridine은 HCl 제거 염기), "
                  "ㄴ ○(–NHCOCH₃는 중간 정도 활성 o/p 지향기 → Br₂(CH₃COOH 용매)만으로 일브로민화, 입체적으로 para 우세; 루이스산 불필요), "
                  "ㄷ ○(–NO₂ meta 지향 → 1-bromo-3-nitrobenzene → Fe/HCl로 NO₂만 NH₂로 환원 → 3-bromoaniline).",
        "concepts": [
            "–NH₂: 매우 강한 활성기 → Br₂/H₂O와 바로 2,4,6-tribromoaniline (일치환 조절 불가)",
            "아세틸 보호: –NHCOCH₃는 N 비공유쌍이 C=O와도 공명해 활성 감소 → 일치환, 부피로 para 우세",
            "아마이드 가수분해(HO⁻ 또는 H₃O⁺, 가열)로 보호기 제거",
            "–NO₂: 강한 불활성화·meta 지향 (o/p 공격 σ 착물은 N⁺에 인접한 C⁺ 공명 구조 → 불안정)",
            "Fe/HCl, Sn/HCl, H₂/Pd: ArNO₂ → ArNH₂ (Ar–Br 유지)",
            "합성 순서 = 지향성 설계: meta 생성물은 NO₂ 단계에서 치환, para는 NH(Ac) 단계에서 치환",
        ],
        "sol": """<p><b>① 첫 번째 경로</b></p>
<ol><li><b>A</b>: aniline의 N 비공유쌍이 CH₃COCl의 카보닐 C를 공격 → 사면체 중간체 → Cl⁻ 이탈(친핵성 아실 치환) → pyridine이 H⁺(HCl)를 제거 → <b>acetanilide</b>.</li>
<li><b>(가)</b>: Br₂(CH₃COOH). –NHCOCH₃의 N 비공유쌍이 고리로 전자를 밀어 o/p의 σ 착물을 안정화(N⁺=C 공명 구조). 활성은 –NH₂보다 약해 한 번만 치환되고, 부피 큰 아세트아마이드기 때문에 ortho보다 <b>para</b>가 우세 → <b>B</b> = 4-bromoacetanilide.</li>
<li>HO⁻/H₂O, 가열: 아마이드 가수분해(HO⁻가 C=O 공격 → 사면체 → ArNH⁻ 이탈·양성자화) → <b>4-bromoaniline</b> + CH₃COO⁻.</li></ol>
<p><b>② 두 번째 경로</b>: Br₂/FeBr₃가 Br–Br···FeBr₃ 착물(Br⁺ 성질)을 만들고, 강한 불활성화기 –NO₂가 meta로 지향 → <b>C</b> = 1-bromo-3-nitrobenzene. Fe/HCl은 NO₂ → NO → NHOH → NH₂로 환원(아닐리늄 염 후 염기 처리) → <b>D</b> = 3-bromoaniline.</p>
<p><b>③ 보기별 판정</b></p>
<table class="tb"><tr><th>보기</th><th>근거</th><th>판정</th></tr>
<tr><td>ㄱ</td><td>CH₃COCl + ArNH₂ → ArNHCOCH₃ (pyridine: 산 제거·친핵 촉매)</td><td>○</td></tr>
<tr><td>ㄴ</td><td>활성화된 고리는 FeBr₃ 없이 Br₂만으로 브로민화. 생성물이 para-Br이고 가수분해 후 4-bromoaniline이 됨과 일치</td><td>○</td></tr>
<tr><td>ㄷ</td><td>NO₂(meta 지향) 상태에서 Br 도입 후 환원 → meta 관계 유지</td><td>○</td></tr></table>
<p><b>④ 함정</b>: aniline에 바로 Br₂/FeBr₃를 쓰면 (1) 다중 브로민화, (2) –NH₂가 루이스산 FeBr₃와 착물을 이뤄 강한 불활성화기(–NH₂⁺–FeBr₃⁻)가 되는 문제가 생긴다. 반대로 3-bromoaniline을 aniline에서 만들 수는 없다(–NH₂는 o/p 지향) — 그래서 nitrobenzene에서 출발한다.</p>""",
        "figs": [(F.f27, "보호–치환–탈보호로 4-bromoaniline, meta 지향 후 환원으로 3-bromoaniline(D)")],
        "extra": [
            ("원리 정리", """<table class="tb"><tr><th>치환기</th><th>효과</th><th>지향</th><th>비고</th></tr>
<tr><td>–NH₂, –OH, –O⁻</td><td>강한 활성(+M ≫ −I)</td><td>o/p</td><td>Br₂/H₂O로 삼치환</td></tr>
<tr><td>–NHCOR, –OR</td><td>중간 활성</td><td>o/p</td><td>일치환 조절, para 우세</td></tr>
<tr><td>–R, –Ar</td><td>약한 활성</td><td>o/p</td><td>초공액·+I</td></tr>
<tr><td>–X (할로젠)</td><td>약한 불활성(−I &gt; +M)</td><td>o/p</td><td>예외적 조합</td></tr>
<tr><td>–CHO, –COR, –COOH, –CN, –SO₃H</td><td>불활성</td><td>m</td><td></td></tr>
<tr><td>–NO₂, –NR₃⁺, –CF₃</td><td>강한 불활성</td><td>m</td><td>Friedel–Crafts 불가</td></tr></table>
<p><b>합성 설계 원칙</b>: 원하는 위치 관계(o/p 또는 m)를 만드는 지향기가 존재하는 단계에서 두 번째 치환기를 도입한다. NO₂ ⇄ NH₂(환원), NH₂ ⇄ NHAc(보호/탈보호), NH₂ → N₂⁺ → 여러 치환기(Sandmeyer)로 지향성을 ‘바꿔 쓰는’ 전략이 핵심.</p>"""),
            ("27 임용 연관 분석", """<p><b>① 연관 기출</b>: 2016 전공B 서술형 4번(치환 벤젠의 브로민화 속도와 4-bromoacetanilide), 2023 전공A 기입형 2번(N-acetylaniline 나이트로화 → 다이아조화 → 아조 짝지음), 2020 전공A 기입형 4번(아닐리늄 + 아세트산 무수물 → acetanilide, pKa), 2014 전공B 논술형 2번(4′-bromo-3′-nitroacetophenone 합성 순서), 2018 전공A 서술형 12번(tert-butylbenzene 나이트로화와 차단기 전략), 2025 전공A 서술형 10번(톨루엔에서 다단계 방향족 합성).</p>
<p><b>② 서술형 변형 예상</b>: “aniline을 Br₂/H₂O와 반응시키면 생성물이 무엇인지 쓰고, 4-bromoaniline을 주생성물로 얻기 위한 3단계 합성과 각 단계의 역할을 서술하시오.” — 모범 답안: 2,4,6-tribromoaniline. ① Ac₂O 또는 CH₃COCl/pyridine으로 아세틸화(N 비공유쌍이 C=O와 공명해 활성 감소, 부피 증가) ② Br₂/CH₃COOH로 para 일브로민화 ③ 산 또는 염기 가수분해로 보호기 제거.</p>
<p><b>③ 체크포인트</b>: σ 착물 공명 구조를 그려 o/p vs m을 설명하는 서술형 대비. –NH₂ + 루이스산 착물화, 아닐린의 Friedel–Crafts 불가도 함께 정리.</p>"""),
        ],
        "faq": [
            ("ㄴ에서 FeBr₃가 없어도 반응하나요?",
             "–NHCOCH₃로 활성화된 고리는 친핵성이 커서 분극된 Br₂만으로 충분히 반응합니다(보통 아세트산 용매). 촉매를 쓰면 오히려 다중 치환 위험이 커집니다."),
            ("acetanilide 브로민화에서 ortho 생성물은 전혀 없나요?",
             "소량 생기지만 부피 큰 –NHCOCH₃가 ortho를 가려 para가 주생성물이며, 재결정으로 분리합니다."),
            ("Fe/HCl 환원에서 C–Br은 영향을 받지 않나요?",
             "용해 금속–산 조건은 NO₂를 선택적으로 환원하고 방향족 C–Br은 그대로 둡니다(H₂/Pd에서는 장시간 시 탈할로젠화 가능)."),
        ],
    },
    # ------------------------------------------------------------------ 28
    {
        "id": "md-2027-28", "year": 2027, "q": 28, "exam": "MDEET 자연과학Ⅱ 28번", "pts": 4,
        "sub": "친핵성 치환 — SN2 반전, 알코올의 할로젠화(PBr₃, 토실레이트), Markovnikov 첨가",
        "title": "(R)-2-chloro-3-methylbutane + LiBr → (S)-2-bromo-3-methylbutane과 같은 생성물을 주는 반응",
        "stem": "(R)-2-chloro-3-methylbutane(Cl 쐐기)을 LiBr/acetone으로 처리해 얻은 A와 동일한 화합물이 주생성물로 얻어지는 것만을 고르시오.<br>"
                "ㄱ. 2-methylbut-2-ene + HBr<br>"
                "ㄴ. (R)-3-methylbutan-2-ol(OH 쐐기) + PBr₃<br>"
                "ㄷ. (S)-3-methylbutan-2-ol(OH 점선) + 1. TsCl, pyridine 2. LiBr<br>"
                "① ㄱ ② ㄴ ③ ㄱ, ㄷ ④ ㄴ, ㄷ ⑤ ㄱ, ㄴ, ㄷ",
        "answer": "<b>②</b> — A = (S)-2-bromo-3-methylbutane(2차 탄소 SN2, 반전). "
                  "ㄱ ✗(Markovnikov: 3° 탄소 양이온 → 2-bromo-2-methylbutane, 구조가 다름), "
                  "ㄴ ○(ROH + PBr₃ → ROPBr₂(C–O 유지) → Br⁻ 뒤쪽 SN2, 반전: R-알코올 → S-브로마이드), "
                  "ㄷ ✗(토실화는 C–O 결합을 건드리지 않아 배열 보존 → (S)-OTs → LiBr SN2 반전 → (R)-브로마이드 = A의 거울상).",
        "concepts": [
            "SN2: 뒤쪽 공격, 한 단계 협동, Walden 반전, 속도 = k[RX][Nu⁻]",
            "Finkelstein형 치환: acetone(극성 비양성자성)에서 할라이드 교환 — LiCl/NaCl 침전이 평형을 끄는 효과",
            "PBr₃: 1°·2° 알코올 → 브로마이드, 자리옮김 없음, 배열 반전",
            "TsCl/pyridine: R–O–H의 O–H만 O–Ts로 → 배열 보존, 좋은 이탈기 생성; 이후 SN2에서 반전",
            "HX의 알켄 첨가: Markovnikov(더 안정한 탄소 양이온 경유)",
            "CIP: 이탈기와 친핵체가 모두 1순위이면 SN2 반전 시 R ↔ S 표기도 바뀜",
        ],
        "sol": """<p><b>① 기준 반응 A</b>: C2의 순위 Cl(①) &gt; CH(CH₃)₂(②) &gt; CH₃(③), H 뒤 → (R). Br⁻가 C–Cl σ*의 뒤쪽 로브로 접근 → [Br···C···Cl]⁻ 삼각쌍뿔 전이상태 → 우산 뒤집히듯 반전. Br도 1순위이므로 <b>(S)-2-bromo-3-methylbutane</b>(그림에서 Br이 점선).</p>
<p><b>② 보기별 판정</b></p>
<table class="tb"><tr><th>보기</th><th>단계</th><th>생성물</th><th>판정</th></tr>
<tr><td>ㄱ</td><td>H⁺가 C3(CH)에 첨가 → C2가 3° 탄소 양이온(더 안정) → Br⁻ 결합</td><td>2-bromo-2-methylbutane (비카이랄, 구조 이성질체)</td><td>✗</td></tr>
<tr><td>ㄴ</td><td>O 비공유쌍이 P 공격 → R–O–PBr₂ + HBr(이때 C–O는 그대로) → Br⁻가 C 뒤쪽 공격, HOPBr₂ 이탈 → 반전</td><td>(R)-알코올 → <b>(S)</b>-브로마이드 = A</td><td>○</td></tr>
<tr><td>ㄷ</td><td>O–H의 O가 S를 공격 → R–OTs (C–O 유지, 보존: S) → Br⁻ SN2 → 반전</td><td>(S)-OTs → <b>(R)</b>-브로마이드 = A의 거울상</td><td>✗</td></tr></table>
<p><b>③ 핵심</b>: 알코올 → 할로젠화물 변환에서 ‘반전 횟수’를 센다. PBr₃·SOCl₂(pyridine) = 반전 1회. TsCl(보존) + SN2(반전) = 반전 1회. 따라서 ㄴ과 ㄷ은 <b>출발 알코올의 배열이 반대</b>이므로 서로 거울상의 브로마이드를 준다. ㄴ의 출발물 (R)-알코올이 A의 출발물 (R)-염화물과 같은 공간 배열이므로 같은 (S)-브로마이드가 된다.</p>
<p><b>④ 참고</b>: 이 기질은 2차이고 이웃에 3차 탄소가 있어 SN1 조건(HBr, 가열)에서는 히드라이드 이동으로 2-bromo-2-methylbutane이 생긴다. PBr₃·토실레이트 경로는 탄소 양이온을 만들지 않아 자리옮김이 없다.</p>""",
        "figs": [(F.f28, "기준 SN2와 보기 ㄱ·ㄴ·ㄷ의 생성물 비교(구조·배열)")],
        "extra": [
            ("원리 정리", """<table class="tb"><tr><th>시약</th><th>메커니즘</th><th>입체화학</th><th>자리옮김</th></tr>
<tr><td>HBr, HCl (3°·2°)</td><td>SN1</td><td>라셈화(부분)</td><td>가능</td></tr>
<tr><td>PBr₃ / SOCl₂ + pyridine</td><td>O 활성화 후 SN2</td><td>반전</td><td>없음</td></tr>
<tr><td>SOCl₂ (용매 없이/에터)</td><td>SNi</td><td>보존</td><td>없음</td></tr>
<tr><td>TsCl, py → Nu⁻</td><td>보존 + SN2</td><td>전체 반전</td><td>없음</td></tr>
<tr><td>Mitsunobu (PPh₃, DEAD, Nu–H)</td><td>SN2</td><td>반전</td><td>없음</td></tr></table>
<p><b>SN2 속도 요인</b>: 기질(메틸 &gt; 1° &gt; 2° ≫ 3°, β-가지 증가 시 느려짐), 친핵체(극성 비양성자성 용매에서 F⁻ &gt; Cl⁻ &gt; Br⁻ &gt; I⁻가 아니라 염기도 순; 양성자성 용매에서는 I⁻ &gt; Br⁻ &gt; Cl⁻), 이탈기(TsO⁻ ≈ I⁻ &gt; Br⁻ &gt; Cl⁻), 용매(DMSO, DMF, acetone).</p>"""),
            ("27 임용 연관 분석", """<p><b>① 연관 기출</b>: 2008 서술형 15번(3-chloro-2-methyl-2-phenylbutane의 SN1 자리옮김과 (S)-2-iodo… SN2의 입체화학), 2013 2차 논술형 3번(2-hexyl tosylate의 SN2 전이상태·용매 효과), 2017 전공B 서술형 4번(ROTs 가용매분해 속도), 2019 전공A 기입형 4번(OH → NH₂ 변환 순서: 토실화 후 치환), 2010 2차 논술형 1번(SN1/E2 입체 조건), 2009 1차 23번·2004 서술형 8번(알켄 첨가의 Markovnikov 위치 선택성).</p>
<p><b>② 서술형 변형 예상</b>: “(S)-3-methylbutan-2-ol을 (S)-2-bromo-3-methylbutane으로 바꾸는 2가지 방법을 제시하고, HBr을 사용하면 안 되는 이유를 서술하시오.” — 모범 답안: (1) TsCl/py → LiCl(SN2, R-염화물) → LiBr(SN2, S-브로마이드)처럼 반전 2회, 또는 (2) Mitsunobu로 반전된 에스터 → 가수분해 → (R)-알코올 → PBr₃(반전). HBr은 SN1로 2° 양이온을 거쳐 히드라이드 이동이 일어나 2-bromo-2-methylbutane이 생기고 입체도 잃는다.</p>
<p><b>③ 체크포인트</b>: 각 단계의 C–O(또는 C–X) 결합이 끊기는지 여부로 보존/반전을 판단. 쐐기 구조에서 R/S를 빠르게 매기는 연습.</p>"""),
        ],
        "faq": [
            ("2차 할로젠화물인데 SN2가 잘 일어나나요?",
             "β-가지(isopropyl) 때문에 느리지만, acetone 같은 극성 비양성자성 용매와 좋은 친핵체(Br⁻)를 쓰면 SN2가 주경로입니다. 문제도 ‘주생성물’로 반전 생성물을 가정합니다."),
            ("LiBr/acetone에서 Cl⁻를 Br⁻로 바꾸는 반응도 평형을 끌 수 있나요?",
             "NaI/acetone(NaCl·NaBr 침전)만큼 극적이지는 않지만, 과량의 LiBr을 써서 평형을 생성물 쪽으로 이동시킵니다."),
            ("ㄷ의 토실화가 배열을 보존하는 이유는?",
             "반응은 알코올의 O가 S를 공격하는 O–S 결합 형성일 뿐, 입체 중심의 C–O 결합은 끊어지지 않기 때문입니다."),
        ],
    },
    # ------------------------------------------------------------------ 29
    {
        "id": "md-2027-29", "year": 2027, "q": 29, "exam": "MDEET 자연과학Ⅱ 29번", "pts": 4,
        "sub": "알켄의 반응 — 옥시수은화, 수소붕소화, 오존 분해, 브로민 첨가, 할로하이드린",
        "title": "다섯 알켄 반응 중 주생성물 구조가 틀린 것: octalin 오존 분해는 cyclodecane-1,6-dione",
        "stem": "알켄 화합물의 반응에서 주생성물의 구조가 옳지 않은 것은?<br>"
                "① 3-methylbut-1-ene + 1. Hg(OAc)₂, H₂O 2. NaBH₄ → 3-methylbutan-2-ol<br>"
                "② hex-1-ene + 1. BH₃, THF 2. H₂O₂, NaOH → hexan-1-ol<br>"
                "③ Δ⁹⁽¹⁰⁾-octalin + 1. O₃ 2. Zn, AcOH → 두 C=O 사이에 CH₂ 3개/5개인 10원 고리 다이온<br>"
                "④ trans-hex-3-ene + Br₂ → (3R,4S)-3,4-dibromohexane(쐐기/점선)<br>"
                "⑤ 2-ethylbut-1-ene + Br₂, H₂O → 1-bromo-2-ethylbutan-2-ol",
        "answer": "<b>③</b> — 사치환 C9=C10이 끊기면 각 고리의 CH₂ 4개가 두 C=O 사이에 남으므로 <b>cyclodecane-1,6-dione</b>(4개/4개)이어야 한다. 문항의 그림은 3개/5개인 cyclodecane-1,5-dione이라 틀림. "
                  "①(머큐리늄 이온, 자리옮김 없는 Markovnikov) ②(역-Markovnikov, syn) ④(anti 첨가 → 메조) ⑤(H₂O가 더 치환된 C 공격) 모두 옳음.",
        "concepts": [
            "옥시수은화–탈수은화: 고리형 머큐리늄 이온 → Markovnikov OH, 탄소 양이온 자리옮김 없음",
            "수소붕소화–산화: B가 덜 치환된 C, H는 더 치환된 C(syn), 산화 시 배열 보존 → 역-Markovnikov 알코올",
            "오존 분해(환원적 후처리 Zn/AcOH 또는 Me₂S): C=C → 두 C=O, 고리 알켄은 사슬/큰 고리 다이카보닐",
            "Br₂ 첨가: 브로모늄 이온 → Br⁻ 뒤쪽 공격(anti); trans-대칭 알켄 → 메조",
            "할로하이드린: 브로모늄을 H₂O가 양전하를 더 잘 견디는(더 치환된) C에서 공격 → Br은 덜 치환된 C",
        ],
        "sol": """<p><b>① 선지별 판정</b></p>
<table class="tb"><tr><th>선지</th><th>메커니즘·선택성</th><th>주생성물</th><th>판정</th></tr>
<tr><td>①</td><td>Hg(OAc)⁺가 C=C에 첨가 → 머큐리늄 이온(자유 2° 양이온 아님) → H₂O가 더 치환된 C2를 anti로 공격 → NaBH₄가 C–Hg를 C–H로. 이웃 3° C로의 히드라이드 이동 없음</td><td>3-methylbutan-2-ol</td><td>옳음</td></tr>
<tr><td>②</td><td>BH₃의 B가 말단 C1(입체·전자적), H가 C2로 4중심 syn 첨가 → H₂O₂/HO⁻로 C–B → C–OH(보존)</td><td>hexan-1-ol</td><td>옳음</td></tr>
<tr><td>③</td><td>O₃ 1,3-쌍극 고리 첨가 → 몰오조나이드 → 역고리 첨가 → 오조나이드 → Zn/AcOH 환원 → C9, C10이 각각 C=O. C9과 C10은 각 고리에서 CH₂ 4개로 연결되어 있으므로 두 C=O 사이는 양쪽 모두 4개</td><td>cyclodecane-1,6-dione</td><td><b>틀림</b></td></tr>
<tr><td>④</td><td>Br₂가 π 전자를 받아 브로모늄 이온 → Br⁻가 반대면에서 공격(anti). trans-알켄 + anti → (3R,4S) 메조. 그림의 쐐기/점선(지그재그에서 반대) = (3R,4S)</td><td>meso-3,4-dibromohexane</td><td>옳음</td></tr>
<tr><td>⑤</td><td>브로모늄 이온에서 C2(3°)가 C–Br 결합이 더 길고 δ+가 큼 → H₂O가 C2 공격 → H⁺ 이탈</td><td>1-bromo-2-ethylbutan-2-ol</td><td>옳음</td></tr></table>
<p><b>② ③의 탄소 세기</b>: octalin은 C₁₀H₁₆, C9=C10 외 CH₂ 8개(각 고리 4개). 오존 분해는 탄소를 잃지 않으므로 생성물은 C₁₀H₁₆O₂의 10원 고리이고, 원래 고리 A의 C1–C4 사슬과 고리 B의 C5–C8 사슬이 C9(=O)와 C10(=O) 사이를 각각 잇는다 → 1,6 관계. 1,5-다이온은 한쪽 다리에 CH₂가 3개뿐이라 원래 골격과 맞지 않는다.</p>
<p><b>③ ④의 R/S 확인</b>: C3(위 꼭짓점, Br 쐐기): Br &gt; C4(Br,C,H) &gt; C2, H 뒤 → 시계 → R. C4(아래 꼭짓점, Br 점선): Br &gt; C3 &gt; C5, H 앞 → 시계를 뒤집어 S. (3R,4S) = 메조.</p>""",
        "figs": [(F.f29, "③ octalin 오존 분해: 옳은 생성물 cyclodecane-1,6-dione vs 문항 그림(1,5-dione)"),
                 (F.f29b, "④ 브로모늄 이온의 anti 개환 → meso-3,4-dibromohexane, 나머지 선지 요약")],
        "extra": [
            ("원리 정리", """<table class="tb"><tr><th>반응</th><th>위치 선택성</th><th>입체</th><th>자리옮김</th></tr>
<tr><td>HX</td><td>Markovnikov</td><td>무작위</td><td>있음</td></tr>
<tr><td>H₃O⁺ 수화</td><td>Markovnikov</td><td>무작위</td><td>있음</td></tr>
<tr><td>Hg(OAc)₂, H₂O; NaBH₄</td><td>Markovnikov</td><td>(anti, 탈수은화 단계 비입체특이)</td><td>없음</td></tr>
<tr><td>BH₃; H₂O₂/HO⁻</td><td>역-Markovnikov</td><td>syn</td><td>없음</td></tr>
<tr><td>Br₂ / Br₂, H₂O</td><td>— / OH는 더 치환된 C</td><td>anti</td><td>없음</td></tr>
<tr><td>O₃; Zn 또는 Me₂S</td><td>C=C 절단</td><td>—</td><td>—</td></tr>
<tr><td>O₃; H₂O₂</td><td>절단 후 –CHO → –COOH</td><td>—</td><td>—</td></tr></table>
<p><b>오존 분해 역추적 팁</b>: 생성물의 두 C=O 탄소를 이으면 원래 C=C. 고리 다이온은 ‘두 고리의 공유 이중결합’ 또는 ‘고리 내 이중결합’에서 온다.</p>"""),
            ("27 임용 연관 분석", """<p><b>① 연관 기출</b>: 2016 전공A 기입형 4번(1-methylcyclohexanol 탈수 → 오존 분해 → 분자 내 aldol), 2024 전공B 서술형 7번(오존 분해·분자 내 aldol 축합), 2014 전공A 기입형 8번(오존 분해로 아세톤 생성 — 구조 결정), 2016 전공A 서술형 13번(옥시수은화 생성물), 1999 서술형 6번(옥시수은화·syn 다이하이드록시화), 2018 전공A 기입형 4번(수소붕소화 라셈 알코올), 2002 서술형 12번(브로모늄 이온과 anti 첨가), 2017 전공A 서술형 13번(할로하이드린 → 에폭사이드 → 개환, 수소붕소화).</p>
<p><b>② 서술형 변형 예상</b>: “cyclodecane-1,6-dione을 염기로 처리할 때 생기는 분자 내 aldol 축합 생성물(이환 엔온)을 그리고, 5원·6원·7원 고리 중 어느 것이 생기는지 이유와 함께 서술하시오.” — 모범 답안: C6 카보닐의 α-탄소(C5 또는 C7) 엔올레이트가 C1 카보닐을 공격하면 5원 고리와 7원 고리가 융합된 이환 골격이 생긴다(전형적 예: 1,6-다이온 → bicyclo[5.3.0] 엔온). 6원 고리를 만드는 조합은 없으며, 생성 엔온은 공액으로 안정화된다. (또는 반대로 octalin → O₃ → 다이온 → aldol로 고리 크기 변환을 묻는 형태)</p>
<p><b>③ 체크포인트</b>: 오존 분해 생성물의 탄소 수·고리 크기를 반드시 세어 볼 것. 옥시수은화 vs 산 촉매 수화(자리옮김 유무) 대비는 단골 비교.</p>"""),
        ],
        "faq": [
            ("①에서 3-methylbut-1-ene을 묽은 황산으로 수화하면?",
             "2° 탄소 양이온이 3°로 히드라이드 이동하여 2-methylbutan-2-ol이 주생성물이 됩니다. 옥시수은화는 머큐리늄 이온을 거쳐 자리옮김이 없습니다."),
            ("③에서 Zn/AcOH 대신 H₂O₂를 쓰면 생성물이 달라지나요?",
             "C9·C10은 모두 사치환(수소 없음) 탄소라 케톤이 되므로 산화적 후처리를 해도 같은 다이케톤입니다. 알데하이드가 생기는 경우에만 카복실산으로 바뀝니다."),
            ("④의 생성물은 왜 광학 비활성인가요?",
             "(3R,4S)-3,4-dibromohexane은 C3–C4 중점에 대칭 요소(반전 중심/대칭면 형태)를 가진 메조 화합물입니다."),
        ],
    },
    # ------------------------------------------------------------------ 30
    {
        "id": "md-2027-30", "year": 2027, "q": 30, "exam": "MDEET 자연과학Ⅱ 30번", "pts": 5,
        "sub": "α,β-불포화 카보닐 — 1,2- vs 1,4-첨가, 선택적 수소화",
        "title": "cyclohex-2-en-1-one + LiAlH₄ / H₂(1당량), Pd/C / (CH₃)₂CuLi",
        "stem": "cyclohex-2-en-1-one을 1. LiAlH₄ 2. H₂O로 처리해 A, H₂(1당량)/Pd–C로 B, 1. (CH₃)₂CuLi 2. H₂O로 C를 얻었다. A~C를 옳게 나열한 것은?<br>"
                "① cyclohex-2-en-1-ol / cyclohexanone / 3-methylcyclohexanone<br>"
                "② cyclohex-2-en-1-ol / cyclohexanol / 2-methylcyclohexanone<br>"
                "③ cyclohexanol / cyclohex-2-en-1-ol / 3-methylcyclohexanone<br>"
                "④ cyclohexanol / cyclohexanone / 1-methylcyclohex-2-en-1-ol<br>"
                "⑤ cyclohexanone / cyclohexanol / 1-methylcyclohex-2-en-1-ol",
        "answer": "<b>①</b> — A: LiAlH₄의 H⁻(단단한 친핵체)는 C=O에 직접 1,2-첨가 → cyclohex-2-en-1-ol(알릴 알코올). "
                  "B: Pd/C에서 C=C가 C=O보다 훨씬 쉽게 수소화 → 1당량이면 cyclohexanone. "
                  "C: Gilman 시약(부드러운 친핵체)은 β-탄소에 1,4-(짝지은) 첨가 → 엔올레이트 → 양성자화·토토머화 → 3-methylcyclohexanone.",
        "concepts": [
            "α,β-불포화 카보닐의 두 친전자 자리: 카보닐 C(1,2-첨가)와 β-C(1,4-첨가, 공명 구조 C=C–C=O ↔ ⁺C–C=C–O⁻)",
            "단단한(전하 밀집) 친핵체: LiAlH₄, NaBH₄(대체로), RLi, RMgX → 1,2-첨가 (속도론적)",
            "부드러운 친핵체: R₂CuLi, 엔올레이트(Michael), 아민, 티올, CN⁻ → 1,4-첨가 (열역학적, C=O 보존)",
            "촉매 수소화: C=C ≫ C=O (Pd/C, 1당량) → 포화 케톤",
            "Luche 환원(NaBH₄/CeCl₃): 선택적 1,2-환원의 대표 조건",
        ],
        "sol": """<p><b>① 각 반응</b></p>
<table class="tb"><tr><th>생성물</th><th>메커니즘</th><th>구조</th></tr>
<tr><td>A</td><td>AlH₄⁻의 H⁻가 카보닐 C(LUMO 계수·전하가 큰 자리)를 직접 공격 → 알콕시알루미네이트 → H₂O 후처리로 OH. C=C는 고립되어 남음</td><td>cyclohex-2-en-1-ol</td></tr>
<tr><td>B</td><td>H₂가 Pd 표면에서 C=C에 syn 첨가. C=O의 수소화는 훨씬 느려 1당량 소모 시 멈춤</td><td>cyclohexanone</td></tr>
<tr><td>C</td><td>CH₃⁻(Cu 경유)가 β-탄소(C3) 공격 → C2=C3 π 전자가 C1–C2로, C=O π 전자가 O로 이동(굽은 화살표) → 리튬 엔올레이트 → H₂O가 C2를 양성자화(토토머화) → 케톤 회복</td><td>3-methylcyclohexanone (라셈)</td></tr></table>
<p><b>② 오답 선지의 함정</b></p>
<ul><li>②·⑤의 B = cyclohexanol: C=C와 C=O를 모두 환원하려면 2당량 이상·더 강한 조건이 필요. 1당량 Pd/C는 C=C만.</li>
<li>②의 C = 2-methylcyclohexanone: 큐프레이트는 α가 아니라 β 탄소에 결합(α-메틸화는 LDA/CH₃I 조건).</li>
<li>③·④의 A = cyclohexanol: LiAlH₄는 일반적으로 고리 엔온의 C=C를 환원하지 않는다(1,2-환원 우세).</li>
<li>④·⑤의 C = 1-methylcyclohex-2-en-1-ol: CH₃Li나 CH₃MgBr(단단한 친핵체)의 1,2-첨가 생성물 — Gilman 시약의 결과가 아님.</li></ul>""",
        "figs": [(F.f30, "cyclohex-2-en-1-one의 세 반응: 1,2-환원(A), C=C 선택 수소화(B), 큐프레이트 1,4-첨가(C)"),
                 (F.f30b, "1,4-첨가 메커니즘: β-탄소 공격 → 리튬 엔올레이트 → 양성자화")],
        "extra": [
            ("원리 정리", """<table class="tb"><tr><th>시약</th><th>주된 첨가</th><th>cyclohex-2-enone 생성물</th></tr>
<tr><td>LiAlH₄, DIBAL-H</td><td>1,2</td><td>cyclohex-2-en-1-ol</td></tr>
<tr><td>NaBH₄/CeCl₃ (Luche)</td><td>1,2 (선택적)</td><td>cyclohex-2-en-1-ol</td></tr>
<tr><td>CH₃Li, CH₃MgBr</td><td>1,2</td><td>1-methylcyclohex-2-en-1-ol</td></tr>
<tr><td>(CH₃)₂CuLi</td><td>1,4</td><td>3-methylcyclohexanone</td></tr>
<tr><td>엔올레이트(Michael), RNH₂, RSH, CN⁻</td><td>1,4</td><td>3-치환 cyclohexanone</td></tr>
<tr><td>H₂ (1당량), Pd/C</td><td>C=C 환원</td><td>cyclohexanone</td></tr>
<tr><td>Li/NH₃(l)</td><td>C=C 환원(엔올레이트 경유)</td><td>cyclohexanone</td></tr></table>
<p><b>설명 틀</b>: 1,2-첨가는 전하 지배(카보닐 C의 δ+가 가장 큼)·빠르고 비가역, 1,4-첨가는 궤도 지배(LUMO의 β 계수가 큼)·C=O(강한 결합)를 남기므로 열역학적으로 유리. 1,4 후 엔올레이트를 친전자체(R–X)로 포획하면 α,β-이중 작용화도 가능.</p>"""),
            ("27 임용 연관 분석", """<p><b>① 연관 기출</b>: 2017 전공A 기입형 4번(mesityl oxide에 CH₃Li(1,2) vs (CH₃)₂CuLi(1,4) 첨가 — 같은 개념), 2002 서술형 14번(2-cyclohexenone + C₂H₅MgBr / CH₃NH₂ / 1,3-butadiene: 1,2 vs 1,4, Diels–Alder), 2024 전공B 서술형 7번(cyclopentanone → cyclohex-2-enone(C)·cyclohexanone(D)), 2015 전공A 기입형 9번(Stork 엔아민 Michael → Robinson), 2026 전공A 서술형 11번(β-keto ester + MVK Robinson annulation), 2010 1차 37번(Michael 첨가/탈카복실).</p>
<p><b>② 서술형 변형 예상</b>: “cyclohex-2-en-1-one에 CH₃MgBr와 (CH₃)₂CuLi를 각각 반응시킨 생성물을 쓰고, 첨가 위치가 다른 이유를 공명 구조와 HSAB(또는 전하·궤도 지배)로 서술하시오.” — 모범 답안: CH₃MgBr → 1-methylcyclohex-2-en-1-ol(1,2), (CH₃)₂CuLi → 3-methylcyclohexanone(1,4). 엔온의 공명 구조 ⁺C3–C2=C1–O⁻에서 β-C도 친전자성. 단단한 친핵체는 δ+가 가장 큰 카보닐 C를 빠르게(비가역) 공격, 부드러운 큐프레이트는 LUMO 계수가 큰 β-C를 공격하고 C=O를 보존한 엔올레이트를 거친다.</p>
<p><b>③ 체크포인트</b>: 시약별 1,2/1,4 표, 1당량 수소화의 선택성, 엔올레이트 중간체를 굽은 화살표로 그리는 연습. Robinson annulation(Michael + aldol)까지 연결해 정리.</p>"""),
        ],
        "faq": [
            ("NaBH₄는 1,2와 1,4 중 어느 쪽인가요?",
             "고리 엔온에서는 1,2와 1,4(이후 케톤 재환원으로 포화 알코올)가 섞이기 쉽습니다. 1,2만 원하면 CeCl₃를 넣은 Luche 조건을 씁니다."),
            ("C는 왜 라셈인가요?",
             "β-탄소가 평면 엔온의 위·아래 어느 면에서나 같은 확률로 공격받아 (R)과 (S)-3-methylcyclohexanone이 1:1로 생깁니다."),
            ("B에서 Pd/C 대신 NaBH₄를 쓰면?",
             "주로 C=O가 환원되어(1,2) 알릴 알코올이나 포화 알코올이 섞여 나오므로, C=C만 환원하려면 촉매 수소화(1당량)나 Li/NH₃가 적합합니다."),
        ],
    },
]
