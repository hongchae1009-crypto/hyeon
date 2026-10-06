# -*- coding: utf-8 -*-
"""문항별 탐구 그림·모형 (인라인 SVG). 전자 껍질 등 교육과정 범위 밖 표현은 사용하지 않음."""
F = "font-family='NanumGothic' font-size='12'"
S = "stroke='#222' stroke-width='1.4' fill='none'"

def svg(w, h, body):
    return f"<svg class='fig' viewBox='0 0 {w} {h}' width='{w}' height='{h}' xmlns='http://www.w3.org/2000/svg' {F}>{body}</svg>"

def t(x, y, s, size=12, anchor="middle", weight="normal"):
    return f"<text x='{x}' y='{y}' font-size='{size}' text-anchor='{anchor}' font-weight='{weight}' fill='#111'>{s}</text>"

def particles(x, y, w, h, pts, r=6, fill="#9bb7d4"):
    out = f"<rect x='{x}' y='{y}' width='{w}' height='{h}' {S}/>"
    for px, py in pts:
        out += f"<circle cx='{x+px}' cy='{y+py}' r='{r}' fill='{fill}' stroke='#234' stroke-width='1'/>"
    return out

def beaker(x, y, w, h, level=None, fill="#cfe5f7"):
    out = ""
    if level is not None:
        out += f"<rect x='{x+2}' y='{y+h-level}' width='{w-4}' height='{level-2}' fill='{fill}'/>"
    out += f"<path d='M{x} {y} L{x} {y+h} L{x+w} {y+h} L{x+w} {y}' {S}/>"
    return out

def axes(x, y, w, h, xl="시간", yl="온도(℃)"):
    return (f"<path d='M{x} {y} L{x} {y+h} L{x+w} {y+h}' {S}/>"
            f"<path d='M{x-4} {y+6} L{x} {y} L{x+4} {y+6}' {S}/><path d='M{x+w-6} {y+h-4} L{x+w} {y+h} L{x+w-6} {y+h+4}' {S}/>"
            + t(x + w - 4, y + h + 16, xl, 11, "end") + t(x + 4, y - 4, yl, 11, "start"))

FIG = {}

# 1. 세 가지 상태 탐구 장치
FIG[1] = svg(620, 150,
    beaker(20, 50, 60, 70, 0) + "".join(f"<rect x='{30+i*14}' y='{100-(i%2)*12}' width='12' height='12' fill='#f2b866' stroke='#844'/>" for i in range(3))
    + t(50, 140, "플라스틱 블록") +
    beaker(110, 50, 60, 70, 45, "#ffcf7a") + t(140, 140, "주스") +
    beaker(190, 70, 45, 50, 30, "#ffcf7a") + f"<path d='M190 70 L235 70' {S}/>" + t(212, 140, "모양이 다른 컵") +
    # syringes
    f"<rect x='280' y='70' width='120' height='26' {S}/><rect x='282' y='72' width='60' height='22' fill='#ffcf7a'/>"
    f"<rect x='398' y='78' width='18' height='10' fill='#555'/><path d='M280 83 L250 83' stroke='#222' stroke-width='3' fill='none'/><rect x='244' y='68' width='6' height='30' fill='#222'/>"
    + t(340, 60, "주스를 넣은 주사기") + t(430, 74, "고무", 10) + t(430, 86, "마개", 10) +
    f"<rect x='470' y='70' width='120' height='26' {S}/><rect x='588' y='78' width='18' height='10' fill='#555'/>"
    f"<path d='M470 83 L450 83' stroke='#222' stroke-width='3' fill='none'/><rect x='444' y='68' width='6' height='30' fill='#222'/>"
    + t(530, 60, "공기를 넣은 주사기") + t(530, 120, "피스톤을 누른다 →", 11))

# 2. 감압 장치
FIG[2] = svg(620, 175,
    f"<rect x='40' y='135' width='170' height='22' rx='4' {S}/>" + t(125, 151, "전자저울 266.1 g", 11) +
    f"<rect x='60' y='55' width='130' height='80' rx='10' {S}/><rect x='105' y='40' width='40' height='15' {S}/>"
    f"<path d='M85 110 q15 -12 30 0 q15 12 30 0 L145 125 L85 125 Z' fill='#e8e0f5' stroke='#555'/>"
    + t(125, 100, "아세톤 1 mL", 10) + t(125, 32, "감압 장치(공기를 뺀 상태)", 11) +
    f"<path d='M250 95 L300 95' {S}/><path d='M292 89 L300 95 L292 101' {S}/>" + t(275, 85, "가열", 11) +
    beaker(330, 60, 260, 95, 55, "#f6c9b5") + t(460, 172, "뜨거운 물이 담긴 수조", 11) +
    f"<rect x='395' y='45' width='130' height='90' rx='10' {S} fill='white'/><rect x='440' y='30' width='40' height='15' {S}/>"
    f"<ellipse cx='460' cy='92' rx='50' ry='32' fill='#e8e0f5' stroke='#555'/>" + t(460, 96, "부풀어 오른 비닐 주머니", 10))

# 3. 드라이아이스 하얀 김
FIG[3] = svg(620, 158,
    f"<ellipse cx='170' cy='125' rx='110' ry='14' {S}/>"
    + "".join(f"<rect x='{105+i*30}' y='{100-(i%2)*6}' width='26' height='20' fill='#f4f6fb' stroke='#667'/>" for i in range(4))
    + "".join(f"<path d='M{110+i*28} 85 q-12 -20 4 -36 q14 -14 0 -30' stroke='#aab' stroke-width='5' fill='none' opacity='0.7'/>" for i in range(5))
    + t(170, 150, "드라이아이스") + t(270, 40, "하얀 김", 13, "start", "bold") +
    f"<path d='M400 120 L400 70 Q400 50 430 50 L520 50 Q550 50 550 70 L550 120 Z' {S}/><path d='M550 70 L585 50' stroke='#222' stroke-width='5'/>"
    + "".join(f"<path d='M{590+i*4} 45 q-10 -15 4 -28' stroke='#aab' stroke-width='4' fill='none' opacity='0.7'/>" for i in range(2))
    + t(475, 140, "물을 끓이는 주전자") + t(600, 14, "김", 12))

# 4. 상태 변화 관계도
FIG[4] = svg(620, 190,
    "".join(f"<rect x='{x-45}' y='{y-18}' width='90' height='36' rx='8' {S}/>" + t(x, y + 5, s, 13, weight='bold')
            for x, y, s in [(310, 30, "기체"), (130, 160, "고체"), (490, 160, "액체")])
    + f"<path d='M175 152 L445 152' {S}/><path d='M437 147 L445 152 L437 157' {S}/>" + t(310, 146, "융해", 11)
    + f"<path d='M445 170 L175 170' {S}/><path d='M183 165 L175 170 L183 175' {S}/>" + t(310, 186, "응고", 11)
    + f"<path d='M470 140 L340 48' {S}/><path d='M350 49 L340 48 L344 57' {S}/>" + t(452, 110, "기화", 11)
    + f"<path d='M352 40 L490 138' {S}/><path d='M480 137 L490 138 L486 129' {S}/>" + t(388, 66, "액화", 11)
    + f"<path d='M150 140 L280 48' {S}/><path d='M270 49 L280 48 L276 57' {S}/>" + t(168, 110, "승화", 11)
    + f"<path d='M268 40 L130 138' {S}/><path d='M140 137 L130 138 L134 129' {S}/>" + t(232, 66, "승화", 11))

# 5. 가열 곡선 장치 + 그래프 틀
FIG[5] = svg(620, 205,
    f"<rect x='40' y='160' width='160' height='18' rx='3' {S}/>" + t(120, 173, "가열 장치", 10) +
    f"<path d='M84 155 L100 105 L100 60 L130 60 L130 105 L146 155 Z' {S}/>" +
    f"<path d='M84 155 L100 110 L130 110 L146 155 Z' fill='#cfe5f7'/>"
    + "".join(f"<circle cx='{100+i*10}' cy='150' r='3' fill='#777'/>" for i in range(4)) + t(60, 150, "끓임쪽", 10, "end") +
    f"<path d='M115 30 L115 130' stroke='#333' stroke-width='3'/><rect x='110' y='22' width='10' height='10' fill='#333'/>"
    f"<path d='M120 26 L200 26' stroke='#333'/><rect x='200' y='10' width='40' height='60' rx='5' {S}/>" + t(220, 86, "스마트 기기", 10)
    + t(160, 120, "온도 센서", 10, "start") + t(120, 198, "삼각 플라스크 속 증류수", 10) +
    axes(330, 30, 260, 130) + f"<path d='M330 150 Q420 120 470 60 L580 60' stroke='#c33' stroke-width='2' fill='none' stroke-dasharray='4 3'/>"
    + t(470, 20, "시간-온도 그래프(앱 화면)", 11))

# 6. 냉각 곡선 (한제)
FIG[6] = svg(620, 190,
    beaker(40, 70, 120, 100, 80, "#e6eef6") + "".join(f"<rect x='{50+i*20}' y='{100+(i%3)*18}' width='14' height='12' fill='white' stroke='#8aa'/>" for i in range(5)) +
    f"<rect x='88' y='40' width='24' height='115' rx='12' {S} fill='#d8ecfb'/>" + f"<path d='M100 20 L100 140' stroke='#333' stroke-width='3'/>"
    + t(100, 14, "온도 센서", 10) + t(100, 186, "얼음 : 소금 = 3 : 1(한제)", 10) + t(175, 120, "물이 든 시험관", 10, "start") +
    axes(330, 25, 260, 140) + f"<path d='M330 50 Q370 80 400 105 L480 105 Q520 120 580 150' stroke='#1b5fa8' stroke-width='2.2' fill='none'/>"
    + f"<path d='M326 105 L340 105' {S}/>" + t(320, 109, "0", 11, "end") + t(540, 135, "㉡", 12))

# 7. 로르산 냉각 곡선 (구간)
FIG[7] = svg(620, 180,
    axes(150, 20, 330, 140, "시간(분)") + f"<path d='M150 40 Q200 70 245 95 L380 95 Q420 115 470 140' stroke='#1b5fa8' stroke-width='2.4' fill='none'/>"
    + f"<path d='M245 30 L245 160 M380 30 L380 160' stroke='#888' stroke-dasharray='4 3'/>"
    + t(197, 155, "A", 13, weight='bold') + t(312, 155, "B", 13, weight='bold') + t(425, 155, "C", 13, weight='bold')
    + f"<path d='M146 95 L156 95' {S}/>" + t(140, 99, "43.9", 10, "end") + t(310, 85, "온도 일정", 11))

# 8. 주사기 + 압력 센서 + 입자 모형
FIG[8] = svg(620, 180,
    f"<rect x='30' y='40' width='150' height='34' {S}/><path d='M180 57 L240 57' stroke='#222' stroke-width='3' fill='none'/><rect x='240' y='45' width='30' height='24' fill='#555'/>"
    f"<path d='M30 57 L10 57' stroke='#222' stroke-width='3' fill='none'/><rect x='4' y='40' width='6' height='34' fill='#222'/>"
    f"<path d='M270 57 L300 57' stroke='#333'/><rect x='300' y='30' width='40' height='60' rx='5' {S}/>"
    + t(105, 30, "주사기(공기 40 mL)", 11) + t(255, 90, "압력 센서", 10) + t(320, 105, "스마트 기기", 10) +
    particles(390, 30, 100, 110, [(15, 20), (70, 15), (40, 55), (85, 70), (20, 95), (60, 92), (50, 30)])
    + particles(510, 60, 100, 80, [(15, 15), (40, 25), (70, 12), (85, 40), (25, 55), (55, 60), (80, 66)])
    + t(440, 160, "(가) 누르기 전") + t(560, 160, "(나) 누른 후"))

# 9. 밀도 (얼음·동전, 눈금실린더)
FIG[9] = svg(620, 180,
    beaker(40, 40, 170, 120, 90, "#cfe5f7") + f"<rect x='70' y='58' width='70' height='40' fill='#f4f8ff' stroke='#7aa'/>"
    + f"<ellipse cx='170' cy='152' rx='14' ry='4' fill='#c9a24a' stroke='#875'/>" + t(105, 52, "얼음덩어리", 10) + t(170, 140, "동전", 10) +
    t(125, 176, "(가) 교사의 시범", 11) +
    f"<path d='M330 20 L330 160 L370 160 L370 20' {S}/><rect x='331' y='70' width='38' height='89' fill='#cfe5f7'/>"
    + "".join(f"<path d='M330 {30+i*13} L340 {30+i*13}' stroke='#555'/>" for i in range(10))
    + f"<path d='M350 0 L350 120' stroke='#333'/><rect x='342' y='120' width='16' height='22' fill='#888' stroke='#333'/>"
    + t(390, 75, "물 50.0 mL → 55.8 mL", 11, "start") + t(390, 128, "실로 묶은 금속 조각", 11, "start") + t(470, 176, "(나) 금속 조각의 부피 측정", 11))

# 10. 용해도 (물중탕 시험관 3개)
FIG[10] = svg(620, 175,
    beaker(140, 70, 340, 90, 70, "#f6d6c4")
    + "".join(f"<rect x='{185+i*100}' y='30' width='26' height='110' rx='13' {S} fill='white'/><path d='M{198+i*100} 10 L{198+i*100} 120' stroke='#333' stroke-width='2'/>"
              + t(198 + i * 100, 158, "(" + "가나다"[i] + ")", 12, weight='bold') for i in range(3))
    + t(310, 174, "물중탕으로 질산 칼륨을 모두 녹인 뒤, 꺼내어 식히며 온도를 측정", 11) + t(560, 40, "온도계", 10))

# 11. 공유 플랫폼 게시판
FIG[11] = svg(620, 150,
    f"<rect x='20' y='10' width='580' height='130' rx='10' {S}/>" + t(310, 30, "공유 플랫폼 – 순물질과 혼합물을 구별하는 기준", 12, weight='bold')
    + "".join(f"<rect x='{40+i*140}' y='45' width='120' height='80' fill='{c}' stroke='#999'/>" + t(100 + i * 140, 70, f"{i+1}모둠", 11, weight='bold')
              + t(100 + i * 140, 95, "기준 : ?", 11) for i, c in enumerate(["#fff6b3", "#d9f2d0", "#ffd9d9", "#d9e8ff"])))

# 12. 분리 도구
FIG[12] = svg(620, 190,
    f"<path d='M60 20 Q60 10 75 10 Q90 10 90 20 L110 90 Q75 120 40 90 Z' {S}/><path d='M75 105 L75 150' stroke='#222' stroke-width='3' fill='none'/><rect x='68' y='118' width='14' height='6' fill='#555'/>"
    + f"<path d='M47 80 L103 80' stroke='#777'/>" + t(75, 172, "분별 깔때기", 11) +
    f"<path d='M230 150 L210 100 L210 60 L240 60 L240 100 L260 150 Z' {S}/><path d='M240 75 L320 110' stroke='#222' stroke-width='3' fill='none'/>"
    f"<path d='M225 40 L225 120' stroke='#333' stroke-width='2'/>" + beaker(300, 110, 60, 50, 30, "#dfefff")
    + f"<rect x='315' y='95' width='18' height='60' rx='9' {S} fill='white'/>" + t(225, 34, "온도 센서", 10) + t(280, 182, "증류 장치(가지 달린 삼각 플라스크)", 11) +
    f"<path d='M460 110 Q520 160 580 110 Z' {S}/><path d='M470 125 L570 125' stroke='#bbb'/>" + t(520, 182, "증발 접시", 11)
    + f"<rect x='450' y='140' width='140' height='12' rx='3' {S}/>")

# 13. 라부아지에 장치 + 물의 전기 분해
FIG[13] = svg(620, 190,
    f"<path d='M40 150 L40 100 Q40 80 60 80 L80 80 Q100 80 100 100 L100 150 Z' {S}/><path d='M42 120 L98 120 L98 148 L42 148 Z' fill='#cfe5f7'/>"
    + t(70, 172, "물 가열", 10) + f"<path d='M70 80 L70 60 L130 60' stroke='#222' stroke-width='2' fill='none'/>"
    + f"<rect x='130' y='45' width='170' height='30' rx='4' fill='#ffd8b0' stroke='#a54'/><path d='M130 60 L300 60' stroke='#444' stroke-width='6'/>"
    + t(215, 38, "뜨겁게 가열한 주철관", 11) + f"<path d='M300 60 L340 60 L340 120' stroke='#222' stroke-width='2' fill='none'/>"
    + beaker(320, 100, 60, 50, 35, "#dfefff") + t(350, 172, "냉각", 10)
    + f"<path d='M352 110 L400 110 L400 70 L430 70' stroke='#222' stroke-width='2' fill='none'/><rect x='430' y='40' width='30' height='70' {S}/>" + t(445, 128, "기체 수집", 10) + t(445, 34, "?", 13, weight='bold')
    + f"<path d='M490 160 L490 60 M590 160 L590 60' {S}/><path d='M490 160 L590 160' {S}/><path d='M492 100 L588 100 L588 158 L492 158 Z' fill='#cfe5f7'/>"
    + f"<rect x='505' y='40' width='20' height='80' rx='10' {S} fill='white'/><rect x='555' y='40' width='20' height='80' rx='10' {S} fill='white'/>"
    + t(515, 34, "(+)극", 10) + t(565, 34, "(−)극", 10) + t(540, 182, "물의 전기 분해", 11))

def atom(cx, cy, z, ne, label, ion=None):
    import math
    out = f"<circle cx='{cx}' cy='{cy}' r='13' fill='#f6b3a6' stroke='#a33'/>" + t(cx, cy + 4, f"+{z}", 11, weight='bold')
    for k in range(ne):
        a = 2 * math.pi * k / ne + 0.4
        rr = 34 + (k % 2) * 10
        out += f"<circle cx='{cx + rr*math.cos(a):.1f}' cy='{cy + rr*math.sin(a):.1f}' r='4' fill='#3a6fc4'/>"
    out += t(cx, cy + 62, label, 11)
    return out

# 14. 원자·이온 모형 (전자 껍질 없이)
FIG[14] = svg(620, 175,
    atom(70, 70, 1, 1, "수소 원자") + atom(200, 70, 6, 6, "탄소 원자") + atom(330, 70, 8, 8, "산소 원자")
    + f"<path d='M400 10 L400 160' stroke='#bbb' stroke-dasharray='4 3'/>" + atom(500, 70, 11, 10, "나트륨 이온(양성자 11, 전자 10)")
    + t(560, 22, "●: 전자", 10, "start"))

# 15. 주기율표 일부 + 카드
def cell(x, y, s, fill="white"):
    return f"<rect x='{x}' y='{y}' width='38' height='26' fill='{fill}' stroke='#555'/>" + t(x + 19, y + 18, s, 12, weight='bold')
rows = [("H", "He"), ("Li", "Ne"), ("Na", "Ar"), ("K", "Kr"), ("Rb", "Xe")]
FIG[15] = svg(620, 185,
    "".join(cell(60, 20 + i * 28, a if a not in ("Rb",) else "?", "#ffe2b8" if i else "white") + cell(300, 20 + i * 28, b if b != "Kr" else "?", "#d7e8ff")
            + f"<rect x='100' y='{20+i*28}' width='198' height='26' fill='#f3f3f3' stroke='#ccc'/>" + t(40, 38 + i * 28, f"{i+1}", 11)
            for i, (a, b) in enumerate(rows))
    + t(79, 14, "1족", 11) + t(319, 14, "18족", 11) + t(199, 92, "(2∼17족 생략)", 11)
    + "".join(f"<rect x='{390+(i%3)*72}' y='{30+(i//3)*60}' width='62' height='48' rx='5' fill='#fffbe8' stroke='#aa9'/>" + t(421 + (i % 3) * 72, 59 + (i // 3) * 60, s, 12, weight='bold')
              for i, s in enumerate(["헬륨", "칼륨", "아르곤", "나트륨", "리튬", "네온"]))
    + t(497, 160, "원소 카드(뒷면에 성질)", 11))

# ═════════════ 중3 Ⅰ. 화학 반응의 규칙성 ═════════════
def ball(cx, cy, s, fill, r=13):
    return f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{fill}' stroke='#234' stroke-width='1'/>" + t(cx, cy + 4, s, 10, weight='bold')
NC, HC, OC, CC = "#8fb2e8", "#f4f4f4", "#f08c8c", "#888"

# 16. 원형 자석 모형 → 활동지 그림 → 화학 반응식
def n2(x, y): return ball(x, y, "N", NC) + ball(x + 24, y, "N", NC)
def h2(x, y): return ball(x, y, "H", HC, 10) + ball(x + 18, y, "H", HC, 10)
def nh3(x, y): return ball(x, y, "N", NC) + ball(x - 20, y + 16, "H", HC, 10) + ball(x + 20, y + 16, "H", HC, 10) + ball(x, y - 22, "H", HC, 10)
FIG[16] = svg(620, 200,
    t(310, 16, "(가) 자석 칠판 위 원형 자석 모형", 11) + f"<rect x='20' y='24' width='580' height='96' rx='6' fill='#f7f7f2' stroke='#999'/>"
    + n2(50, 72) + t(100, 77, "+", 16) + h2(120, 50) + h2(120, 75) + h2(120, 100) + f"<path d='M175 75 L235 75 M228 70 L235 75 L228 80' {S}/>"
    + nh3(285, 72) + nh3(350, 72)
    + f"<rect x='410' y='34' width='180' height='78' fill='white' stroke='#aaa' stroke-dasharray='4 3'/>" + t(500, 58, "자석 하나 = 원자 하나", 11)
    + t(500, 78, "반응물 자석만 다시 써서", 11) + t(500, 96, "생성물을 만든다", 11)
    + t(160, 142, "(나) 활동지 그림·입자 수", 11) + f"<rect x='40' y='150' width='240' height='40' fill='white' stroke='#555'/>"
    + t(160, 175, "질소 ( )개 + 수소 ( )개 → 암모니아 ( )개", 11)
    + t(450, 142, "(다) 화학 반응식", 11) + f"<rect x='330' y='150' width='240' height='40' fill='white' stroke='#555'/>" + t(450, 176, "N₂ + 3H₂ → 2NH₃", 15, weight='bold'))

# 17. 질량 보존 – 유리병 2개 / 플라스틱 병(뚜껑 닫음·열음)
def scale(x, y, w, val):
    return (f"<rect x='{x}' y='{y}' width='{w}' height='18' fill='#ddd' stroke='#555'/><rect x='{x+w/2-30}' y='{y+20}' width='60' height='16' fill='#223'/>"
            + f"<text x='{x+w/2}' y='{y+32}' font-size='11' text-anchor='middle' fill='#6f6'>{val}</text>")
FIG[17] = svg(620, 190,
    t(100, 16, "탐구 ① 앙금 생성", 11)
    + f"<rect x='45' y='70' width='40' height='60' fill='none' stroke='#555'/><rect x='47' y='96' width='36' height='32' fill='#eef'/><rect x='45' y='60' width='40' height='10' fill='#222'/>"
    + f"<rect x='115' y='70' width='40' height='60' fill='none' stroke='#555'/><rect x='117' y='96' width='36' height='32' fill='#eef'/><rect x='115' y='60' width='40' height='10' fill='#222'/>"
    + t(65, 52, "KI 수용액", 10) + t(135, 52, "AgNO₃ 수용액", 10) + scale(30, 130, 140, "52.40 g")
    + t(320, 16, "탐구 ② 모둠 1 (뚜껑 닫음)", 11)
    + f"<path d='M270 40 L270 130 L370 130 L370 40 Z' fill='#f5fbff' stroke='#555'/><rect x='265' y='30' width='110' height='10' fill='#2a63b8'/>"
    + f"<rect x='295' y='80' width='26' height='48' fill='none' stroke='#555'/><rect x='297' y='100' width='22' height='26' fill='#e6f2e6'/>" + t(308, 74, "묽은 염산", 9)
    + "".join(f"<path d='M{335+i*9} 126 l6 -6 l5 6 z' fill='#eee6d6' stroke='#a98'/>" for i in range(3)) + t(345, 112, "달걀 껍데기", 9)
    + scale(255, 130, 130, "85.62 g")
    + t(510, 16, "탐구 ② 모둠 2 (뚜껑 열고 반응)", 11)
    + f"<path d='M460 40 L460 130 L560 130 L560 40' fill='#f5fbff' stroke='#555'/>"
    + f"<rect x='485' y='80' width='26' height='48' fill='none' stroke='#555'/>" + "".join(f"<circle cx='{505+i*8}' cy='{60-i*9}' r='3' fill='none' stroke='#777'/>" for i in range(3))
    + t(538, 36, "CO₂", 10) + scale(445, 130, 130, "85.62 g"))

# 18. 공유 플랫폼에 올린 모둠별 구리 가열 자료
pts = [(1.2, 1.5), (2.0, 2.5), (2.8, 3.5), (3.6, 4.2), (4.4, 5.5)]
def gx(v): return 330 + v * 55
def gy(v): return 170 - v * 26
FIG[18] = svg(620, 200,
    f"<path d='M20 100 Q65 135 110 100 Z' fill='#f6f6f6' stroke='#333' stroke-width='1.4'/><path d='M40 106 Q65 118 90 106' stroke='#b8742a' stroke-width='5' fill='none'/>" + t(65, 92, "구리 가루", 10)
    + f"<path d='M65 125 Q55 140 65 160 Q75 140 65 125 Z' fill='#f96' stroke='#d42'/><rect x='55' y='160' width='20' height='22' fill='#555'/>" + t(65, 196, "증발 접시 가열", 10)
    + f"<rect x='130' y='30' width='160' height='150' rx='8' fill='#f3f7ff' stroke='#7895c8'/>" + t(210, 48, "공유 플랫폼", 11, weight='bold')
    + "".join(t(210, 70 + i * 22, f"모둠 {i+1}: {a} g → {b} g", 10) for i, (a, b) in enumerate(pts))
    + axes(330, 30, 270, 140, "구리의 질량(g)", "산화 구리(Ⅱ)의 질량(g)")
    + "".join(f"<circle cx='{gx(a)}' cy='{gy(b)}' r='4' fill='{'#e33' if i == 3 else '#245'}'/>" for i, (a, b) in enumerate(pts))
    + t(gx(3.6) + 6, gy(4.2) + 16, "모둠 4", 10, "start"))

# 19. 같은 부피 상자 – 돌턴의 원자 vs 아보가드로의 분자
def box(x, y, lab, inner):
    return f"<rect x='{x}' y='{y}' width='70' height='60' fill='white' stroke='#555'/>" + inner + t(x + 35, y + 76, lab, 10)
FIG[19] = svg(620, 215,
    t(60, 20, "(가) 돌턴의 방식", 11, "start")
    + box(20, 30, "수소 1부피", ball(55, 60, "H", HC, 11)) + box(100, 30, "수소 1부피", ball(135, 60, "H", HC, 11)) + t(185, 64, "+", 15)
    + box(200, 30, "산소 1부피", ball(235, 60, "O", OC, 11)) + f"<path d='M280 60 L310 60 M304 55 L310 60 L304 65' {S}/>"
    + box(320, 30, "수증기 1부피", ball(343, 60, "H", HC, 9) + f"<path d='M362 50 A10 10 0 0 1 362 70 Z' fill='{OC}' stroke='#234'/>")
    + box(400, 30, "수증기 1부피", ball(423, 60, "H", HC, 9) + f"<path d='M442 50 A10 10 0 0 1 442 70 Z' fill='{OC}' stroke='#234'/>")
    + t(480, 56, "물 입자(HO)마다 산소 원자", 10, "start") + t(480, 72, "반 개 → 원자가 쪼개져야 함", 10, "start")
    + t(60, 130, "(나) 아보가드로의 방식", 11, "start")
    + box(20, 140, "수소 1부피", ball(45, 170, "H", HC, 9) + ball(65, 170, "H", HC, 9)) + box(100, 140, "수소 1부피", ball(125, 170, "H", HC, 9) + ball(145, 170, "H", HC, 9)) + t(185, 174, "+", 15)
    + box(200, 140, "산소 1부피", ball(225, 170, "O", OC, 9) + ball(245, 170, "O", OC, 9)) + f"<path d='M280 170 L310 170 M304 165 L310 170 L304 175' {S}/>"
    + box(320, 140, "수증기 1부피", ball(343, 168, "O", OC, 9) + ball(330, 182, "H", HC, 7) + ball(356, 182, "H", HC, 7))
    + box(400, 140, "수증기 1부피", ball(423, 168, "O", OC, 9) + ball(410, 182, "H", HC, 7) + ball(436, 182, "H", HC, 7))
    + t(480, 174, "같은 부피 = 같은 수의 분자", 10, "start"))

# 20. 열 변색 붙임딱지 실험 + 요소 냉각 장치
def flask(x, y, lab, sticker):
    return (f"<path d='M{x+20} {y} L{x+20} {y+30} L{x} {y+80} L{x+60} {y+80} L{x+40} {y+30} L{x+40} {y}' fill='#f2f8ff' stroke='#555'/>"
            + f"<rect x='{x+18}' y='{y+50}' width='24' height='14' fill='{sticker}' stroke='#333'/>" + t(x + 30, y + 100, lab, 10))
FIG[20] = svg(620, 175,
    flask(30, 30, "염화 칼슘 + 물", "#9c6") + flask(140, 30, "수산화 바륨 + 염화 암모늄", "#69c") + t(115, 18, "열 변색 붙임딱지 관찰", 11)
    + f"<path d='M300 20 L300 165' stroke='#bbb' stroke-dasharray='4 3'/>"
    + f"<rect x='330' y='40' width='150' height='100' rx='10' fill='#f7fbff' stroke='#555'/>" + "".join(f"<circle cx='{350+(i%7)*18}' cy='{110+(i//7)*14}' r='3' fill='#ddd' stroke='#999'/>" for i in range(14))
    + f"<rect x='360' y='55' width='90' height='40' rx='5' fill='#cfe5f7' stroke='#468'/>" + t(405, 80, "물(지퍼 백)", 10) + t(405, 156, "요소가 든 봉지(열 봉합)", 10)
    + f"<path d='M500 90 L540 90 M534 85 L540 90 L534 95' {S}/>" + t(570, 80, "눌러서", 10) + t(570, 96, "섞기", 10) + t(470, 22, "간단한 냉각 장치", 11))
