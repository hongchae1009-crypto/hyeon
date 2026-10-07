# -*- coding: utf-8 -*-
"""통합과학 기출 변형 10제 — 문항별 탐구 그림·모형 (인라인 SVG)."""
from figs import svg, t, beaker, axes, ball, S, HC, OC

FIGT = {}

# 1. 운동장–탁구공 비유 + 크기 규모 축
FIGT[1] = svg(620, 175,
    "<ellipse cx='150' cy='80' rx='130' ry='62' fill='#e6f2df' stroke='#5a8a4a' stroke-width='1.5'/>"
    "<circle cx='150' cy='80' r='5' fill='#f5a623' stroke='#a66'/>" + t(150, 160, "운동장 한가운데의 탁구공", 11)
    + f"<path d='M290 80 L330 80 M323 75 L330 80 L323 85' {S}/>"
    + "<circle cx='420' cy='80' r='62' fill='none' stroke='#888' stroke-dasharray='4 3'/><circle cx='420' cy='80' r='3' fill='#d33'/>"
    + "".join(f"<circle cx='{420+62*c}' cy='{80+62*s}' r='3' fill='#36c'/>" for c, s in ((0.8, -0.6), (-0.7, 0.71), (0.1, 1.0)))
    + t(420, 160, "원자(원자핵 + 전자)", 11)
    + t(560, 40, "원자핵 지름", 10) + t(560, 55, "약 10⁻¹⁵ m", 10) + t(560, 95, "원자 지름", 10) + t(560, 110, "약 10⁻¹⁰ m", 10))

# 2. 물의 질량 어림 + 눈금실린더 읽기
FIGT[2] = svg(620, 205,
    beaker(40, 70, 60, 70, 40) + "<rect x='20' y='140' width='100' height='14' fill='#ddd' stroke='#555'/>"
    + "<rect x='45' y='156' width='50' height='16' fill='#223'/><text x='70' y='168' font-size='11' text-anchor='middle' fill='#6f6'>42.1 g</text>"
    + t(70, 60, "어림한 물 50 g?", 11)
    + "<rect x='300' y='20' width='40' height='160' fill='none' stroke='#555'/><rect x='302' y='75' width='36' height='103' fill='#cfe5f7'/>"
    + "<path d='M302 75 Q320 83 338 75' stroke='#246' fill='none'/>"
    + "".join(f"<path d='M340 {30+k*10} L{350 if k%5 else 356} {30+k*10}' stroke='#333'/>" for k in range(15))
    + t(362, 34, "80", 10, "start") + t(362, 84, "75", 10, "start") + t(362, 134, "70", 10, "start") + t(330, 196, "(mL)", 9)
    + "<circle cx='450' cy='40' r='9' fill='none' stroke='#c33'/>" + f"<path d='M440 46 L345 80' stroke='#c33' stroke-dasharray='4 3' fill='none'/>" + t(500, 38, "㉢ 위에서 내려다봄", 10)
    + "<circle cx='450' cy='80' r='9' fill='none' stroke='#2a7'/>" + f"<path d='M440 80 L345 80' stroke='#2a7' fill='none'/>" + t(500, 84, "눈높이 맞춤", 10))

# 3. 교실 평면도와 센서 위치, 온도 그래프
FIGT[3] = svg(620, 200,
    "<rect x='20' y='20' width='240' height='160' fill='#fafafa' stroke='#555'/>" + t(140, 14, "교실 평면도", 11)
    + "<rect x='20' y='70' width='8' height='60' fill='#9cf'/>" + t(24, 62, "냉방기", 10, "start")
    + "<rect x='252' y='40' width='8' height='120' fill='#cde'/>" + t(240, 175, "창가", 10, "end")
    + "<path d='M262 50 L300 30 M262 80 L300 60 M262 110 L300 90' stroke='#f5a623' stroke-width='2'/>" + t(300, 24, "햇빛", 10, "start")
    + "<circle cx='45' cy='100' r='7' fill='#e33'/>" + t(60, 104, "P", 11, weight='bold')
    + "<circle cx='240' cy='70' r='7' fill='#e33'/>" + t(225, 74, "Q", 11, "end", 'bold')
    + axes(360, 40, 230, 130, "시간(분)", "온도(℃)")
    + "<path d='M360 70 L390 72 L420 110 L470 130 L580 140' stroke='#36c' fill='none' stroke-width='2'/>" + t(585, 150, "P", 10, "start")
    + "<path d='M360 62 L390 63 L420 70 L470 80 L580 90' stroke='#c33' fill='none' stroke-width='2'/>" + t(585, 94, "Q", 10, "start")
    + "<path d='M390 40 L390 170' stroke='#999' stroke-dasharray='3 3'/>" + t(392, 186, "냉방기 가동", 10, "start"))

# 4. 알칼리 금속 조각의 크기 비교 + 협업 플랫폼 댓글
def piece(x, y, s, lab):
    return f"<rect x='{x}' y='{y}' width='{s}' height='{s*0.7}' fill='#ddd' stroke='#555'/>" + t(x + s / 2, y + s * 0.7 + 16, lab, 10)
FIGT[4] = svg(620, 170,
    piece(40, 70, 10, "리튬(쌀알)") + piece(120, 60, 26, "나트륨(콩알)") + piece(210, 60, 26, "칼륨(콩알)")
    + t(140, 30, "모둠 1이 자른 금속 조각", 11)
    + "<rect x='330' y='20' width='270' height='135' rx='8' fill='#f3f7ff' stroke='#7895c8'/>" + t(465, 40, "온라인 협업 플랫폼", 11, weight='bold')
    + "<rect x='345' y='52' width='240' height='36' rx='6' fill='white' stroke='#aaa'/>" + t(355, 74, "모둠 1: 실험 설계 올림", 10, "start")
    + "<rect x='365' y='98' width='220' height='40' rx='6' fill='#fffbe8' stroke='#cba'/>" + t(375, 122, "모둠 2: 재미있어 보여요! 최고예요.", 10, "start"))

# 5. 2·3주기 원자의 전자 배치 모형(보어 모형)
def bohr(cx, cy, z, shells, lab):
    out = "".join(f"<circle cx='{cx}' cy='{cy}' r='{12+14*k}' fill='none' stroke='#999'/>" for k in range(len(shells)))
    out += f"<circle cx='{cx}' cy='{cy}' r='9' fill='#f6b2b2' stroke='#a44'/>" + t(cx, cy + 4, f"{z}+", 8, weight='bold')
    import math
    for k, n in enumerate(shells):
        r = 12 + 14 * k
        for j in range(n):
            a = 2 * math.pi * j / n - math.pi / 2
            out += f"<circle cx='{cx + r*math.cos(a):.1f}' cy='{cy + r*math.sin(a):.1f}' r='3' fill='#36c'/>"
    return out + t(cx, cy + 62, lab, 10)
FIGT[5] = svg(620, 200,
    bohr(70, 70, 3, [2, 1], "리튬(Li)") + bohr(200, 70, 9, [2, 7], "플루오린(F)")
    + bohr(380, 70, 11, [2, 8, 1], "나트륨(Na)") + bohr(530, 70, 17, [2, 8, 7], "염소(Cl)")
    + t(135, 165, "2주기", 11, weight='bold') + t(455, 165, "3주기", 11, weight='bold')
    + "<path d='M300 15 L300 175' stroke='#bbb' stroke-dasharray='4 3'/>" + t(310, 192, "1족: Li, Na   17족: F, Cl", 10))

# 6. 6홈판과 간이 전기 전도성 측정기
FIGT[6] = svg(620, 190,
    "<rect x='40' y='30' width='300' height='150' rx='10' fill='#f3f3f3' stroke='#777'/>"
    + "".join(f"<circle cx='{90+i*100}' cy='{60+j*72}' r='20' fill='white' stroke='#888'/>" for i in range(3) for j in range(2))
    + "".join(t(90 + (k % 3) * 100, 95 + (k // 3) * 72, lab, 9) for k, lab in enumerate(["가: 증류수", "나: 설탕", "다: 황산 구리(Ⅱ)", "라: 염화 나트륨"]))
    + t(190, 22, "6홈판", 11)
    + "<rect x='420' y='40' width='60' height='80' rx='6' fill='#ffe7a8' stroke='#a87'/><circle cx='450' cy='62' r='9' fill='#ff4'/>"
    + "<path d='M440 120 L440 155 M460 120 L460 155' stroke='#555' stroke-width='3'/>" + t(450, 172, "간이 전기 전도성 측정기", 10)
    + t(560, 70, "전류가 흐르면", 10) + t(560, 86, "불이 켜지고", 10) + t(560, 102, "소리가 남", 10))

# 7. 산화 구리(Ⅱ) + 탄소 가열 장치 / 구리 선 + 질산 은
FIGT[7] = svg(620, 190,
    "<path d='M40 90 L170 60' stroke='#555' stroke-width='14' stroke-linecap='round'/><path d='M40 90 L170 60' stroke='#f7f7f7' stroke-width='10' stroke-linecap='round'/>"
    + "<ellipse cx='60' cy='86' rx='16' ry='5' fill='#333' transform='rotate(-13 60 86)'/>" + t(60, 112, "CuO + C", 10)
    + "<path d='M70 160 L70 120' stroke='#e55' stroke-width='3'/><rect x='55' y='160' width='30' height='20' fill='#88a'/>" + t(110, 178, "알코올램프", 10, "start")
    + f"<path d='M170 60 L230 60 L230 120' {S}/>" + beaker(205, 100, 50, 60, 40, "#eef") + t(230, 178, "석회수", 10)
    + "<path d='M330 20 L330 180' stroke='#bbb' stroke-dasharray='4 3'/>"
    + beaker(420, 50, 90, 110, 85, "#e9f1fb") + "<path d='M465 20 L465 145' stroke='#c96' stroke-width='4'/>"
    + "".join(f"<circle cx='{458+(k%2)*14}' cy='{80+k*12}' r='3' fill='#bbb' stroke='#777'/>" for k in range(6))
    + t(465, 178, "질산 은 수용액 속 구리 선", 10) + t(560, 100, "은 석출,", 10) + t(560, 116, "용액은 푸른색", 10))

# 8. 24홈판과 리트머스·BTB
FIGT[8] = svg(620, 170,
    "<rect x='30' y='30' width='370' height='120' rx='10' fill='#f3f3f3' stroke='#777'/>"
    + "".join(f"<circle cx='{70+i*58}' cy='60' r='18' fill='{c}' stroke='#888'/>" for i, c in enumerate(["#ffe36b", "#ffe36b", "#ffe36b", "#6aa0ff", "#6aa0ff", "#6aa0ff"]))
    + "".join(t(70 + i * 58, 100, s, 9) for i, s in enumerate(["묽은 염산", "레몬즙", "식초", "NaOH", "제빵 소다", "세정제"]))
    + t(215, 135, "BTB를 떨어뜨린 24홈판(일부)", 10)
    + "<rect x='440' y='40' width='14' height='60' fill='#e88' stroke='#a55'/><rect x='470' y='40' width='14' height='60' fill='#88f' stroke='#55a'/>" + t(462, 120, "리트머스 종이", 10)
    + "<path d='M540 40 L560 100' stroke='#999' stroke-width='5'/>" + t(560, 120, "마그네슘 리본", 10))

# 9. A~E 혼합과 최고 온도 그래프
pts9 = [(2, 23.0), (4, 25.4), (6, 27.4), (8, 25.3), (10, 23.1)]
pts9b = [(2, 22.1), (4, 23.9), (6, 25.6), (8, 26.8), (10, 24.0)]
def gx9(v): return 330 + (v - 1) * 26
def gy9(v): return 170 - (v - 20) * 16
FIGT[9] = svg(620, 200,
    "".join(f"<circle cx='{50+i*52}' cy='70' r='20' fill='{c}' stroke='#888'/>" + t(50 + i * 52, 104, "ABCDE"[i], 11, weight='bold')
            for i, c in enumerate(["#6aa0ff", "#6aa0ff", "#7cd67c", "#ffe36b", "#ffe36b"]))
    + t(155, 30, "BTB 색 (모둠 1)", 11) + t(155, 135, "블루투스 온도계로 최고 온도 측정", 10)
    + axes(330, 30, 270, 140, "묽은 염산 부피(mL)", "최고 온도(℃)")
    + "<polyline fill='none' stroke='#245' stroke-width='2' points='" + " ".join(f"{gx9(a):.0f},{gy9(b):.0f}" for a, b in pts9) + "'/>"
    + "<polyline fill='none' stroke='#c33' stroke-width='2' stroke-dasharray='5 3' points='" + " ".join(f"{gx9(a):.0f},{gy9(b):.0f}" for a, b in pts9b) + "'/>"
    + t(560, 40, "— 모둠 1", 10, "start") + "<text x='560' y='56' font-size='10' fill='#c33'>- - 모둠 2</text>")

# 10. 물 + 산화 칼슘 조리 장치(모둠 설계)
FIGT[10] = svg(620, 190,
    "<path d='M60 50 L80 170 L220 170 L240 50 Z' fill='#f7fbff' stroke='#555'/>" + "<rect x='50' y='40' width='200' height='12' fill='#2a63b8'/>" + t(150, 34, "㉡ 뚜껑을 꽉 닫음", 10)
    + "<rect x='70' y='120' width='160' height='48' fill='#e8e2d4'/>" + t(150, 160, "산화 칼슘 20 g + 물 500 mL", 9)
    + "<rect x='115' y='70' width='70' height='60' fill='white' stroke='#777'/><ellipse cx='150' cy='105' rx='16' ry='20' fill='#fff8e8' stroke='#b96'/>" + t(150, 88, "달걀", 9)
    + t(150, 186, "얇은 플라스틱 컵", 10)
    + axes(330, 30, 260, 130, "시간(분)", "물의 온도(℃)")
    + "<path d='M330 145 Q380 105 420 108 L590 125' stroke='#c33' fill='none' stroke-width='2'/>"
    + "<path d='M330 62 L590 62' stroke='#2a7' stroke-dasharray='5 3'/>" + t(592, 60, "70 ℃", 10, "start") + t(425, 100, "최고 41 ℃", 10, "start"))
