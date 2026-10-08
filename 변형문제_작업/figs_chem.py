# -*- coding: utf-8 -*-
"""고등학교 '화학' 기출 변형 — 문항별 탐구 그림·모형 (인라인 SVG). 키는 items_chem.QC와 같다."""
from figs import svg, t, beaker, axes, ball, S, HC, OC, NC, CC

FIGC = {}

def scale(x, y, val, lab):
    return (f"<rect x='{x}' y='{y}' width='110' height='16' fill='#ddd' stroke='#555'/>"
            f"<rect x='{x+30}' y='{y+18}' width='50' height='16' fill='#223'/>"
            f"<text x='{x+55}' y='{y+30}' font-size='11' text-anchor='middle' fill='#6f6'>{val}</text>" + t(x + 55, y + 52, lab, 10))

# 몰: 0.1 몰씩 측정 — 전자저울과 눈금실린더
FIGC["mol"] = svg(620, 175,
    t(310, 16, "0.1 몰에 해당하는 물질의 양 측정하기", 12, weight='bold')
    + "<rect x='45' y='70' width='40' height='22' fill='#555'/>" + scale(10, 95, "1.20 g", "흑연(C)")
    + "<rect x='160' y='72' width='40' height='20' fill='#bbb'/>" + scale(125, 95, "2.70 g", "알루미늄(Al)")
    + beaker(270, 55, 40, 38, 14) + scale(235, 95, "1.80 g", "물(H₂O)")
    + "<rect x='430' y='30' width='30' height='110' fill='none' stroke='#555'/><rect x='432' y='96' width='26' height='42' fill='#eef6d8'/>"
    + "".join(f"<path d='M460 {40+k*10} L{467 if k%5 else 472} {40+k*10}' stroke='#333'/>" for k in range(10))
    + t(445, 160, "에탄올(C₂H₅OH)", 10) + t(530, 80, "㉡ 4.6 mL?", 11, weight='bold')
    + t(530, 100, "(밀도 0.79 g/mL)", 10))

# 양적 관계: CaCO3 + HCl, 반응 전후 질량
FIGC["stoich"] = svg(620, 180,
    t(150, 16, "반응 전", 11, weight='bold') + t(460, 16, "반응 후", 11, weight='bold')
    + beaker(90, 50, 60, 70, 40) + "<path d='M170 60 l20 0 l-4 20 l-12 0 z' fill='#fff' stroke='#555'/>" + t(180, 50, "CaCO₃ 1.00 g", 10)
    + "<rect x='70' y='122' width='140' height='14' fill='#ddd' stroke='#555'/>" + t(140, 160, "전체 질량 측정", 10)
    + f"<path d='M250 90 L340 90 M333 85 L340 90 L333 95' {S}/>"
    + beaker(430, 50, 60, 70, 40) + "".join(f"<circle cx='{440+i*9}' cy='{100-(i%3)*12}' r='3' fill='white' stroke='#36c'/>" for i in range(5))
    + "<path d='M455 45 q5 -10 0 -20 M470 45 q5 -10 0 -20' stroke='#999' fill='none'/>" + t(520, 34, "CO₂(g) ↑", 11, "start")
    + "<rect x='410' y='122' width='140' height='14' fill='#ddd' stroke='#555'/>" + t(480, 160, "질량 감소 = CO₂ 질량", 10))

# 물의 전기 분해: 압정 전극 + 9 V 전지
FIGC["elec"] = svg(620, 190,
    "<path d='M120 40 L135 150 L265 150 L280 40' fill='#e8f3fb' stroke='#555' stroke-width='1.4'/>" + t(200, 30, "증류수 + Na₂SO₄ 1 g", 11)
    + "<path d='M170 150 L170 125 M230 150 L230 125' stroke='#666' stroke-width='3'/>"
    + "".join(f"<circle cx='{168+(i%2)*4}' cy='{118-i*11}' r='3' fill='white' stroke='#36c'/>" for i in range(7))
    + "".join(f"<circle cx='{228+(i%2)*4}' cy='{118-i*14}' r='3' fill='white' stroke='#c33'/>" for i in range(4))
    + t(160, 115, "(−)", 10, "end") + t(242, 115, "(+)", 10, "start")
    + "<rect x='175' y='165' width='50' height='20' fill='#444'/>" + t(200, 179, "9 V", 10, weight='bold').replace("#111", "#fff")
    + "<path d='M170 150 L170 175 L175 175 M230 150 L230 175 L225 175' stroke='#c33' fill='none'/>"
    + "<rect x='360' y='40' width='230' height='110' rx='6' fill='#fafafa' stroke='#999'/>"
    + t(475, 62, "기체 부피 측정(모둠 5)", 11, weight='bold')
    + "<rect x='400' y='75' width='22' height='60' fill='none' stroke='#555'/><rect x='402' y='95' width='18' height='38' fill='#dfe9fb'/>"
    + "<rect x='500' y='75' width='22' height='60' fill='none' stroke='#555'/><rect x='502' y='117' width='18' height='16' fill='#fbe0e0'/>"
    + t(411, 147, "(−)극 2.2", 10) + t(511, 147, "(+)극 1", 10))

# 전기음성도: 빨대 입체 주기율표 + 그래프
FIGC["en"] = svg(620, 190,
    t(150, 16, "빨대 입체 주기율표(2주기)", 11, weight='bold')
    + "".join(f"<rect x='{30+i*34}' y='{160-h}' width='22' height='{h}' fill='#c9dcf2' stroke='#456'/>" + t(41 + i * 34, 176, s, 10)
              for i, (s, h) in enumerate([("Li", 20), ("Be", 31), ("B", 41), ("C", 51), ("N", 61), ("O", 70), ("F", 80)]))
    + "<rect x='268' y='60' width='22' height='100' fill='none' stroke='#c33' stroke-dasharray='4 3'/>" + t(279, 176, "Ne", 10)
    + t(279, 52, "4.5?", 10, weight='bold')
    + axes(360, 40, 230, 120, "원자 번호", "전기음성도")
    + "<path d='M380 150 L410 140 L440 129 L470 118 L500 108 L530 98 L560 86' stroke='#36c' fill='none' stroke-width='2'/>"
    + "<circle cx='585' cy='45' r='4' fill='#c33'/>" + t(580, 34, "AI 그래프의 Ne", 10, "end"))

# 전자쌍 반발: 쇠구슬과 자석 + NH3
def magnets(cx, cy, angs, lab):
    import math
    out = f"<circle cx='{cx}' cy='{cy}' r='11' fill='#bbb' stroke='#444'/>"
    for a in angs:
        r = math.radians(a)
        x, y = cx + 34 * math.cos(r), cy - 34 * math.sin(r)
        out += f"<path d='M{cx} {cy} L{x:.0f} {y:.0f}' stroke='#888'/><rect x='{x-8:.0f}' y='{y-6:.0f}' width='16' height='12' fill='#e55' stroke='#733'/>"
    return out + t(cx, cy + 58, lab, 10)
FIGC["vsepr"] = svg(620, 170,
    t(200, 16, "(1차시) 쇠구슬 + 자석", 11, weight='bold')
    + magnets(70, 80, [0, 180], "2개") + magnets(190, 80, [90, 210, 330], "3개") + magnets(310, 80, [90, 200, 260, 340], "4개")
    + t(510, 16, "(2차시) NH₃는 어떤 모양?", 11, weight='bold')
    + ball(510, 70, "N", NC) + ball(470, 110, "H", HC, 10) + ball(550, 110, "H", HC, 10) + ball(510, 120, "H", HC, 10)
    + "<path d='M510 70 L470 110 M510 70 L550 110 M510 70 L510 120' stroke='#555'/>"
    + "<ellipse cx='510' cy='40' rx='9' ry='13' fill='none' stroke='#36c' stroke-dasharray='3 2'/>" + t(530, 40, "비공유 전자쌍", 9, "start")
    + t(510, 155, "평면 삼각형? 삼각뿔?", 10))

# 극성: 물줄기와 대전된 빨대, 아이오딘 용해
FIGC["polar"] = svg(620, 190,
    "<rect x='60' y='10' width='14' height='60' fill='none' stroke='#555'/><path d='M67 70 L67 80' stroke='#555'/>" + t(40, 40, "뷰렛", 10, "end")
    + "<path d='M67 82 Q70 120 95 175' stroke='#36c' stroke-width='2.5' fill='none'/>"
    + "<path d='M67 82 L67 175' stroke='#9bb' stroke-width='1' stroke-dasharray='3 3' fill='none'/>"
    + "<rect x='115' y='110' width='80' height='8' rx='4' fill='#fbd' stroke='#a57' transform='rotate(-20 115 110)'/>" + t(170, 145, "문지른 빨대(−−)", 10, "start")
    + t(130, 186, "실험 가", 11, weight='bold')
    + "<rect x='380' y='40' width='80' height='120' rx='8' fill='none' stroke='#555'/><rect x='382' y='60' width='76' height='50' fill='#f1d4f3'/>"
    + "<rect x='382' y='110' width='76' height='48' fill='#e2eef9'/>" + t(470, 85, "사이클로헥세인 + I₂", 10, "start") + t(470, 135, "물", 10, "start")
    + "<rect x='395' y='30' width='50' height='10' fill='#ccc' stroke='#555'/>" + t(420, 186, "실험 나(후드 안, 마개)", 11, weight='bold'))

# 동적 평형: 카드 놀이 그래프
def gpt(i, v): return 330 + i * 40, 170 - v * 2.6
FIGC["dyn"] = svg(620, 200,
    "".join(f"<rect x='{20+(i%7)*24}' y='{30+(i//7)*34}' width='18' height='26' rx='2' fill='{'#e66' if i < 12 else '#69d'}' stroke='#555'/>" for i in range(28))
    + t(100, 190, "빨간색(NO₂) · 파란색(N₂O₄) 카드", 10)
    + axes(330, 30, 270, 140, "회", "남은 카드 수")
    + f"<path d='M{' L'.join(f'{x:.0f} {y:.0f}' for x, y in (gpt(i, v) for i, v in enumerate([49, 37, 32, 29, 28, 28, 28])))}' stroke='#d33' fill='none' stroke-width='2'/>"
    + f"<path d='M{' L'.join(f'{x:.0f} {y:.0f}' for x, y in (gpt(i, v) for i, v in enumerate([0, 12, 17, 20, 21, 21, 21])))}' stroke='#36c' fill='none' stroke-width='2'/>"
    + t(580, 92, "28", 10, "start") + t(580, 118, "21", 10, "start"))

# 평형 상수: 농도 자료 → 규칙성 / Q와 K 비교 수직선
FIGC["K"] = svg(620, 160,
    "<rect x='20' y='20' width='250' height='120' rx='6' fill='#fafafa' stroke='#999'/>" + t(145, 40, "2NO₂ ⇌ N₂O₄", 12, weight='bold')
    + t(145, 70, "[N₂O₄]/2[NO₂] → 일정하지 않음", 10) + t(145, 95, "[N₂O₄]/[NO₂]² → 10.0 일정", 10) + t(145, 122, "(1차시: 자료 → 규칙)", 10)
    + f"<path d='M320 100 L600 100' {S}/>" + "<path d='M594 96 L600 100 L594 104' stroke='#222' fill='none'/>"
    + "<path d='M400 92 L400 108' stroke='#2a7' stroke-width='2'/>" + t(400, 125, "K = 240", 10)
    + "<path d='M550 92 L550 108' stroke='#c33' stroke-width='2'/>" + t(550, 125, "Q = 1000", 10)
    + f"<path d='M540 75 L410 75 M417 70 L410 75 L417 80' stroke='#c33' fill='none'/>" + t(475, 65, "역반응 쪽으로 진행", 10)
    + t(460, 150, "(2차시: K를 적용해 예측)", 10))

# 평형 이동: 염화 코발트 온도 실험
FIGC["shift"] = svg(620, 170,
    "".join(beaker(60 + i * 150, 60, 70, 70, 50, c) + t(95 + i * 150, 150, lab, 11) + t(95 + i * 150, 50, col, 10)
            for i, (lab, c, col) in enumerate([("얼음물", "#f3b6c6", "붉은색"), ("실온", "#c6a8e0", "보라색"), ("뜨거운 물", "#8db4ec", "푸른색")]))
    + "<rect x='470' y='45' width='140' height='90' rx='6' fill='#fffbe8' stroke='#cba'/>"
    + t(540, 68, "Cr₂O₇²⁻(주황)", 10) + t(540, 88, "⇌ 2CrO₄²⁻(노랑)", 10) + t(540, 112, "+ HCl(aq) → ?", 10, weight='bold'))

# 표준 용액: 비커 → 부피 플라스크
FIGC["std"] = svg(620, 180,
    "<rect x='15' y='120' width='100' height='14' fill='#ddd' stroke='#555'/><rect x='40' y='136' width='50' height='16' fill='#223'/>"
    + "<text x='65' y='148' font-size='11' text-anchor='middle' fill='#6f6'>9.00 g</text>" + t(65, 170, "① 포도당 측정", 10)
    + beaker(170, 70, 60, 60, 35) + t(200, 150, "② 소량의 물에 녹임", 10)
    + f"<path d='M240 90 L300 90 M293 85 L300 90 L293 95' {S}/>"
    + "<path d='M370 30 L370 70 Q330 90 330 125 Q330 150 370 150 L390 150 Q430 150 430 125 Q430 90 390 70 L390 30' fill='none' stroke='#555' stroke-width='1.4'/>"
    + "<path d='M333 115 Q332 148 370 148 L390 148 Q428 148 427 115 Z' fill='#e8f3fb'/>"
    + "<path d='M366 45 L394 45' stroke='#c33' stroke-width='2'/>" + t(400, 48, "표시선 (500 mL)", 10, "start")
    + t(380, 170, "③ 헹군 물까지 옮기고 표시선까지", 10)
    + "<rect x='490' y='60' width='110' height='70' rx='6' fill='#fffbe8' stroke='#cba'/>" + t(545, 82, "㉠ 용매 500 mL?", 10) + t(545, 108, "㉡ 헹구지 않음?", 10))

# pH: 10배 희석과 그래프 변환
FIGC["ph"] = svg(620, 190,
    "".join(beaker(15 + i * 55, 70, 40, 60, 40, c) + t(35 + i * 55, 150, l, 11, weight='bold') + t(35 + i * 55, 168, f"10⁻{i+1} M", 9)
            for i, (l, c) in enumerate(zip("ABCDE", ["#f7c9c9", "#f9d8d0", "#fbe6d9", "#fdf0e4", "#fff8f0"])))
    + t(140, 50, "10배씩 희석", 11)
    + axes(330, 30, 250, 130, "−log[HCl]", "pH")
    + "".join(f"<circle cx='{330+k*45}' cy='{160-p*22:.0f}' r='3.5' fill='#36c'/>" for k, p in zip(range(1, 6), [1.00, 2.15, 3.19, 4.09, 5.10]))
    + "<path d='M330 160 L575 46' stroke='#999' stroke-dasharray='4 3'/>" + t(585, 54, "기울기 1", 10, "start"))

# 적정: 뷰렛 눈금
FIGC["titr"] = svg(620, 200,
    "<rect x='90' y='10' width='22' height='150' fill='none' stroke='#555'/><rect x='92' y='40' width='18' height='118' fill='#eef3fb'/>"
    + "".join(f"<path d='M112 {20+k*14} L{120 if k%2 else 126} {20+k*14}' stroke='#333'/>" for k in range(10))
    + t(130, 24, "0", 9, "start") + t(130, 80, "20", 9, "start") + t(130, 136, "40", 9, "start") + t(150, 60, "눈금은 아래로 갈수록 커짐", 10, "start")
    + "<path d='M101 160 L101 172' stroke='#555'/>" + t(60, 100, "0.1 M NaOH", 10, "end")
    + "<path d='M70 185 L85 140 L117 140 L132 185 Z' fill='#fde8ef' stroke='#555'/>" + t(101, 198, "묽힌 식초 20 mL + 페놀프탈레인", 9)
    + "<rect x='330' y='30' width='270' height='140' rx='6' fill='#fafafa' stroke='#999'/>" + t(465, 52, "기록지", 11, weight='bold')
    + t(345, 82, "처음 눈금: 45.00 mL", 11, "start") + t(345, 108, "나중 눈금: 25.00 mL", 11, "start") + t(345, 140, "㉡ 사용 부피 = ?", 11, "start"))

# SSI: 의사 결정 단계
FIGC["ssi"] = svg(620, 130,
    "".join(f"<rect x='{8+i*102}' y='40' width='92' height='44' rx='6' fill='{'#fde7c9' if i == 2 else '#eef3fb'}' stroke='#789'/>" + t(54 + i * 102, 67, s, 10)
            + (f"<path d='M{100+i*102} 62 L{110+i*102} 62' stroke='#555'/>" if i < 5 else "")
            for i, s in enumerate(["쟁점 확인", "대안 탐색", "판단 기준 설정", "대안 평가", "결정", "결정의 평가"]))
    + t(310, 22, "수돗물 불소화 — SSI 의사 결정 토론", 12, weight='bold') + t(310, 110, "Ca²⁺(aq) + 2F⁻(aq) ⇌ CaF₂(s),  F⁻ 0.5~1 ppm", 11))
