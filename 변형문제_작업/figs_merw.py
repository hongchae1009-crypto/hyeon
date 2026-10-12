# -*- coding: utf-8 -*-
"""'물질과 에너지'(FIGE)·'화학 반응의 세계'(FIGR) 기출 변형 — 문항별 탐구 그림 (인라인 SVG). 키는 items_me.QE / items_rw.QR와 같다."""
import math
from figs import svg, t, beaker, axes, ball, S, HC, OC, NC, CC

FIGE, FIGR = {}, {}

def scale(x, y, val, lab="", w=110):
    return (f"<rect x='{x}' y='{y}' width='{w}' height='16' fill='#ddd' stroke='#555'/>"
            f"<rect x='{x+w/2-25}' y='{y+18}' width='50' height='16' fill='#223'/>"
            f"<text x='{x+w/2}' y='{y+30}' font-size='11' text-anchor='middle' fill='#6f6'>{val}</text>" + (t(x + w / 2, y + 52, lab, 10) if lab else ""))

def plot(x0, y0, w, h, xs, ys, xr, yr, col="#36c", dots=True, line=True):
    X = lambda v: x0 + (v - xr[0]) / (xr[1] - xr[0]) * w
    Y = lambda v: y0 + h - (v - yr[0]) / (yr[1] - yr[0]) * h
    pts = [(X(a), Y(b)) for a, b in zip(xs, ys)]
    out = f"<path d='M{' L'.join(f'{a:.0f} {b:.0f}' for a, b in pts)}' stroke='{col}' fill='none' stroke-width='2'/>" if line else ""
    if dots: out += "".join(f"<circle cx='{a:.0f}' cy='{b:.0f}' r='3' fill='{col}'/>" for a, b in pts)
    return out

# ─────────────── 물질과 에너지 ───────────────
FIGE["gas"] = svg(620, 170,
    "<rect x='30' y='40' width='50' height='90' rx='10' fill='#e3edf8' stroke='#456'/>" + t(55, 30, "기체통", 11)
    + scale(0, 135, "144.80 g", "포집 전")
    + f"<path d='M80 70 Q130 70 150 85' {S}/>"
    + "<rect x='150' y='75' width='170' height='24' fill='#f6f6f6' stroke='#555'/><rect x='300' y='70' width='8' height='34' fill='#888'/>"
    + "".join(f"<path d='M{160+i*14} 75 L{160+i*14} 82' stroke='#333'/>" for i in range(11)) + t(235, 118, "유리 주사기 100.0 mL", 10)
    + "<rect x='360' y='40' width='50' height='90' rx='10' fill='#e3edf8' stroke='#456'/>" + scale(330, 135, "144.67 g", "포집 후")
    + "<rect x='450' y='30' width='160' height='110' rx='6' fill='#fffbe8' stroke='#cba'/>" + t(530, 52, "25.0 ℃, 1.000 atm", 10)
    + t(530, 78, "모형: PV = nRT", 11, weight='bold') + t(530, 102, "M = ? (㉠ 식 점검)", 10) + t(530, 124, "N₂ 28 · O₂ 32 · Ar 40 · CO₂ 44", 9))

FIGE["colli"] = svg(620, 190,
    "<path d='M40 40 L40 150 Q40 170 60 170 L100 170 Q120 170 120 150 L120 40' fill='#e8f3fb' stroke='#555'/>"
    + "<rect x='35' y='30' width='90' height='10' fill='#ccc' stroke='#555'/>" + t(80, 22, "㉠ 입구를 막지 않으면?", 10)
    + "<path d='M80 0 L80 140' stroke='#c33' stroke-width='3'/>" + t(130, 120, "온도 센서", 10, "start")
    + "<path d='M60 15 q4 -8 0 -14 M95 15 q4 -8 0 -14' stroke='#999' fill='none'/>" + t(80, 186, "끓는점 측정", 10)
    + axes(250, 25, 340, 140, "몰랄 농도(m)", "ΔT(℃)")
    + plot(250, 25, 330, 140, [0.5, 1, 1.5, 2, 2.5, 3], [0.91, 1.88, 2.82, 3.70, 4.62, 5.61], (0, 3.2), (0, 6), "#36c")
    + plot(250, 25, 330, 140, [0.5, 1, 1.5, 2, 2.5, 3], [0.58, 1.08, 1.54, 2.12, 2.58, 3.18], (0, 3.2), (0, 6), "#c33")
    + plot(250, 25, 330, 140, [0, 3], [0, 1.53], (0, 3.2), (0, 6), "#c33", dots=False).replace("stroke-width='2'", "stroke-width='1' stroke-dasharray='4 3'")
    + t(585, 55, "ΔT_f", 10, "end") + t(585, 100, "ΔT_b(측정)", 10, "end") + t(585, 135, "0.51×m", 9, "end"))

FIGE["fuel"] = svg(620, 180,
    t(150, 16, "단위 질량당 연소열 (kJ/g)", 11, weight='bold')
    + "".join(f"<rect x='{20+i*55}' y='{160-v*0.95:.0f}' width='34' height='{v*0.95:.0f}' fill='{c}' stroke='#456'/>" + t(37 + i * 55, 174, n, 9) + t(37 + i * 55, 154 - v * 0.95, f"{v}", 9)
              for i, (n, v, c) in enumerate([("에탄올", 29.7, "#b7e0b0"), ("수소", 141.8, "#b7e0b0"), ("휘발유", 46.5, "#d9c7b0"), ("천연가스", 54.0, "#d9c7b0"), ("무연탄", 34.6, "#d9c7b0")]))
    + "<rect x='340' y='30' width='270' height="
      "'120' rx='6' fill='#fafafa' stroke='#999'/>" + t(475, 52, "단위 부피당이라면?", 11, weight='bold')
    + t(475, 80, "수소 0.082 g/L × 141.8 kJ/g", 10) + t(475, 102, "에탄올 789 g/L × 29.7 kJ/g", 10) + t(475, 132, "→ 기준에 따라 순위가 달라진다", 10))

FIGE["hess"] = svg(620, 200,
    t(310, 16, "엔탈피 변화 (NaOH 0.20 mol 기준)", 11, weight='bold')
    + "<path d='M60 40 L200 40 M60 100 L200 100 M60 170 L200 170' stroke='#222' stroke-width='2'/>"
    + t(130, 34, "NaOH(s) + H₂O + HCl(aq)", 10) + t(130, 94, "NaOH(aq) + HCl(aq)", 10) + t(130, 188, "NaCl(aq) + H₂O(l)", 10)
    + f"<path d='M90 44 L90 96 M85 89 L90 96 L95 89' {S}/>" + t(96, 74, "ΔH₁ (가)-1", 10, "start")
    + f"<path d='M90 104 L90 166 M85 159 L90 166 L95 159' {S}/>" + t(96, 140, "ΔH₂ (가)-2", 10, "start")
    + f"<path d='M180 44 L180 166 M175 159 L180 166 L185 159' stroke='#c33' fill='none' stroke-width='1.6'/>" + t(186, 110, "ΔH₃ (나)", 10, "start")
    + "".join(beaker(300 + i * 105, 70, 60, 70, 45) + "<rect x='" + str(306 + i * 105) + "' y='60' width='48' height='10' fill='#ddd' stroke='#555'/>"
              + t(330 + i * 105, 160, lab, 10) for i, lab in enumerate(["(가) 물+NaOH", "(가) +HCl", "(나) 한꺼번에"]))
    + t(330, 54, "22.0→32.0", 9) + t(435, 54, "22.0→28.0", 9) + t(540, 54, "㉠ 24.0→35.2", 9))

FIGE["ent"] = svg(620, 170,
    "".join(f"<rect x='{20+i*100}' y='40' width='80' height='80' fill='#f7f7f7' stroke='#555'/>" for i in range(2))
    + "".join(f"<circle cx='{30+(k%4)*18}' cy='{55+(k//4)*18}' r='5' fill='#36c'/>" for k in range(12))
    + "".join(f"<circle cx='{130+((k*37)%60)}' cy='{50+((k*23)%60)}' r='5' fill='#36c'/>" for k in range(12))
    + f"<path d='M102 80 L118 80' {S}/>" + t(100, 140, "모인 배열 → 퍼진 배열", 10) + t(100, 160, "(잉크·증발·용해)", 9)
    + "<rect x='250' y='30' width='360' height='120' rx='6' fill='#fafafa' stroke='#999'/>"
    + t(430, 52, "자발적 변화의 공통점은?", 11, weight='bold')
    + t(265, 80, "N₂H₄(g) + O₂(g) → N₂(g) + 2H₂O(g)   ΔH < 0", 10, "start")
    + t(265, 104, "4Fe(s) + 3O₂(g) → 2Fe₂O₃(s)   ΔH < 0", 10, "start")
    + t(265, 132, "얼음 융해 · NH₄NO₃ 용해: ΔH > 0 (㉠ 반례)", 10, "start"))

FIGE["press"] = svg(620, 190,
    "<path d='M60 60 L60 100 L30 160 L130 160 L100 100 L100 60' fill='#eef6fb' stroke='#555'/>" + "<path d='M33 155 L127 155 L110 120 L50 120 Z' fill='#d9ecfb'/>"
    + "<rect x='55' y='48' width='50' height='14' fill='#666'/>" + f"<path d='M80 48 L80 20 L170 20' {S}/>"
    + "<rect x='170' y='8' width='50' height='24' rx='4' fill='#223'/>" + t(195, 24, "센서", 10).replace("#111", "#fff")
    + "<rect x='70' y='145' width='18' height='4' fill='#999'/>" + t(80, 178, "Mg + HCl(aq)", 10)
    + "".join(f"<circle cx='{75+i*6}' cy='{135-i*4}' r='2.5' fill='white' stroke='#36c'/>" for i in range(4))
    + axes(300, 25, 290, 140, "시간(s)", "압력(kPa)")
    + plot(300, 25, 280, 140, [0, 10, 20, 30, 40, 50, 60, 70], [102.5, 106.6, 111, 115, 119, 122.5, 125, 127], (0, 75), (100, 130))
    + t(320, 155, "102.5", 9, "start") + t(345, 128, "106.6 (10 s)", 9, "start"))

FIGE["order"] = svg(620, 180,
    axes(40, 25, 250, 130, "시간(s)", "[N₂O₅](M)")
    + plot(40, 25, 240, 130, [0, 50, 100, 150, 200], [0.40, 0.28, 0.20, 0.14, 0.10], (0, 210), (0, 0.42), "#c33")
    + "<path d='M154 87 L154 155 M268 118 L268 155' stroke='#999' stroke-dasharray='3 3'/>" + t(154, 170, "100", 9) + t(268, 170, "200", 9)
    + "<rect x='340' y='30' width='270' height='120' rx='6' fill='#fafafa' stroke='#999'/>" + t(475, 52, "NO₂ + CO → NO + CO₂", 11, weight='bold')
    + t(475, 80, "[NO₂] ×2 → v ×4", 10) + t(475, 102, "[CO] ×2 → v ×2", 10) + t(475, 130, "v = k[NO₂]ᵐ[CO]ⁿ,  m = ? n = ?", 10))

FIGE["conc"] = svg(620, 180,
    "".join(f"<circle cx='{60+i*70}' cy='70' r='26' fill='{c}' stroke='#555'/>" + f"<path d='M{50+i*70} 60 L{70+i*70} 80 M{70+i*70} 60 L{50+i*70} 80' stroke='#222' stroke-width='2.5' opacity='{o}'/>" + t(60 + i * 70, 116, l, 11, weight='bold') + t(60 + i * 70, 134, s, 9)
              for i, (l, c, o, s) in enumerate([("A", "#fbfbf3", 1, "70 s"), ("B", "#f4f2e2", .8, "40 s"), ("C", "#ece8cc", .55, "25 s"), ("D", "#e2dcb4", .35, "20 s")]))
    + t(165, 20, "12홈판 바닥의 ×표가 가려질 때까지", 10)
    + axes(340, 25, 250, 130, "농도(M)", "1/시간(s⁻¹)")
    + plot(340, 25, 240, 130, [0.1, 0.2, 0.3, 0.4], [0.014, 0.025, 0.040, 0.050], (0, 0.42), (0, 0.055))
    + plot(340, 25, 240, 130, [0, 0.4], [0, 0.056], (0, 0.42), (0, 0.055), "#999", dots=False).replace("stroke-width='2'", "stroke-width='1' stroke-dasharray='4 3'")
    + t(585, 32, "정비례선?", 9, "end"))

def dist(x0, y0, w, h, peak, spread, col):
    pts = []
    for i in range(0, 61):
        e = i / 60
        y = (e / peak) ** 2 * math.exp(-2 * (e / peak - 1)) if e > 0 else 0
        y = y * 0.9 / (1 + spread)
        pts.append((x0 + e * w, y0 + h - y * h))
    return f"<path d='M{' L'.join(f'{a:.0f} {b:.0f}' for a, b in pts)}' stroke='{col}' fill='none' stroke-width='2'/>"
FIGE["tcat"] = svg(620, 180,
    axes(40, 25, 280, 130, "운동 에너지", "분자 수")
    + dist(40, 25, 270, 130, 0.25, 0, "#36c") + dist(40, 25, 270, 130, 0.38, 0.35, "#c33")
    + "<path d='M230 30 L230 155' stroke='#555' stroke-dasharray='4 3'/>" + t(232, 42, "E_a", 10, "start")
    + t(120, 45, "T₁", 10) + t(170, 82, "T₂ > T₁", 10, "start")
    + "<rect x='390' y='60' width='34' height='100' fill='none' stroke='#555'/><rect x='392' y='120' width='30' height='38' fill='#eef6fb'/>"
    + "<rect x='480' y='60' width='34' height='100' fill='none' stroke='#555'/><rect x='482' y='120' width='30' height='38' fill='#fdf3c4'/>"
    + "".join(f"<circle cx='{490+(k%3)*7}' cy='{115-k*6}' r='3' fill='white' stroke='#999'/>" for k in range(8))
    + t(407, 175, "H₂O₂", 10) + t(497, 175, "H₂O₂ + KI", 10) + t(450, 30, "촉매와 반응 속도", 11, weight='bold'))

# ─────────────── 화학 반응의 세계 ───────────────
FIGR["ph4"] = svg(620, 170,
    "".join(beaker(20 + i * 75, 60, 50, 60, 40, c) + t(45 + i * 75, 140, n, 10) + t(45 + i * 75, 50, p, 10)
            for i, (n, c, p) in enumerate([("HCl", "#f7c9c9", "1.07"), ("CH₃COOH", "#fbe3d0", "2.84"), ("NaOH", "#c9d6f7", "12.82"), ("NH₃", "#d8e6fb", "10.90")]))
    + t(160, 20, "0.1 M 수용액 (모둠 1 평균 pH)", 11, weight='bold')
    + "<rect x='340' y='30' width='60' height='100' rx='6' fill='#334'/>" + "<rect x='348' y='40' width='44' height='22' fill='#cfc'/>" + t(370, 56, "pH", 10)
    + "<path d='M370 130 L370 150 M420 70 L470 70' stroke='#555'/>" + "<rect x='470' y='40' width='130' height='70' rx='6' fill='#fffbe8' stroke='#cba'/>"
    + t(535, 62, "㉠ 전극을 헹구지 않고", 10) + t(535, 82, "다음 용액에 담그면?", 10) + t(535, 102, "→ 1.62", 10, weight='bold'))

FIGR["titc"] = svg(620, 185,
    axes(30, 20, 260, 140, "NaOH 부피(mL)", "pH")
    + plot(30, 20, 250, 140, [0, 20, 29.6, 29.9, 30, 30.1, 30.2, 35, 45], [1.1, 1.7, 3.2, 3.8, 7.1, 10.2, 10.5, 11.9, 12.3], (0, 46), (0, 14))
    + t(195, 72, "중화점 30.0 mL", 9, "start")
    + axes(350, 20, 250, 140, "시간(s)", "pH")
    + plot(350, 20, 240, 140, [0, 20, 40, 55, 60, 62, 64, 80, 100], [1.1, 1.5, 2.0, 3.0, 4.0, 7.0, 10.3, 11.6, 12.2], (0, 105), (0, 14), "#c33")
    + t(470, 178, "MBL ‘시간–pH’ (㉠ 62 s?)", 10) + t(160, 178, "표의 값으로 그린 그래프", 10))

FIGR["salt"] = svg(620, 160,
    "".join(beaker(30 + i * 95, 50, 60, 60, 42, c) + t(60 + i * 95, 130, n, 10) + t(60 + i * 95, 40, p, 10)
            for i, (n, c, p) in enumerate([("NaCl", "#e2f0d9", "7.0"), ("CH₃COONa", "#cfe0f7", "8.9"), ("NH₄Cl", "#f8d4cf", "4.9"), ("NaHCO₃", "#d8e6fb", "8.3")]))
    + t(200, 15, "염 수용액의 pH (예상: 모두 중성?)", 11, weight='bold')
    + "<rect x='420' y='30' width='190' height="
      "'100' rx='6' fill='#fafafa' stroke='#999'/>" + t(515, 52, "짝산 K_a vs 짝염기 K_b", 10, weight='bold')
    + t(515, 76, "NH₄⁺ K_a 5.6×10⁻¹⁰", 9) + t(515, 94, "CH₃COO⁻ K_b 5.6×10⁻¹⁰", 9) + t(515, 112, "HCO₃⁻ K_a 4.7×10⁻¹¹ / K_b 2.2×10⁻⁸", 9))

FIGR["buf"] = svg(620, 180,
    t(150, 16, "1 M 산·염기 한 방울 (50 mL)", 11, weight='bold')
    + axes(40, 30, 250, 130, "", "pH")
    + "".join(f"<rect x='{70+i*55}' y='{160-v*9:.0f}' width='18' height='{v*9:.0f}' fill='#9bb7d4'/>" + f"<rect x='{90+i*55}' y='{160-u*9:.0f}' width='18' height='{u*9:.0f}' fill='#e4a96b'/>" + t(89 + i * 55, 175, l, 9)
              for i, (l, v, u) in enumerate([("처음", 6.53, 7.11), ("+HCl", 3.74, 7.08), ("+NaOH", 10.51, 7.21)]))
    + "<rect x='230' y='30' width='12' height='10' fill='#9bb7d4'/>" + t(246, 39, "증류수", 9, "start") + "<rect x='230' y='46' width='12' height='10' fill='#e4a96b'/>" + t(246, 55, "완충 용액", 9, "start")
    + "<rect x='340' y='30' width='270' height='120' rx='6' fill='#fafafa' stroke='#999'/>" + t(475, 52, "선행조직자: 르샤틀리에 원리", 11, weight='bold')
    + t(475, 80, "CH₃COO⁻ + H₃O⁺ → CH₃COOH + H₂O", 10) + t(475, 104, "CH₃COOH + OH⁻ → CH₃COO⁻ + H₂O", 10) + t(475, 132, "같은 점? 다른 점?", 10))

def box(x, y, w, s, fill="#eef3fb"):
    return f"<rect x='{x}' y='{y}' width='{w}' height='30' rx='6' fill='{fill}' stroke='#789'/>" + t(x + w / 2, y + 19, s, 10)
FIGR["hyper"] = svg(620, 170,
    box(20, 20, 170, "과호흡 → 혈액 CO₂ 감소") + f"<path d='M105 50 L105 66 M100 60 L105 66 L110 60' {S}/>"
    + box(20, 68, 170, "H₂CO₃ ⇌ HCO₃⁻ + H₃O⁺") + f"<path d='M105 98 L105 114 M100 108 L105 114 L110 108' {S}/>"
    + box(20, 116, 170, "[H₃O⁺] ? → pH ?", "#fde7c9")
    + "<rect x='240' y='15' width='370' height='145' rx='6' fill='#fafafa' stroke='#999'/>" + t(425, 35, "툴민 논증 구조", 11, weight='bold')
    + box(255, 50, 100, "자료(D)") + f"<path d='M355 65 L395 65 M388 60 L395 65 L388 70' {S}/>" + box(395, 50, 90, "한정어(Q)") + f"<path d='M485 65 L505 65' {S}/>" + box(505, 50, 95, "주장(C)")
    + box(330, 92, 90, "논거(W)") + f"<path d='M375 92 L375 80' {S}/>" + box(330, 125, 90, "뒷받침(B)") + box(505, 100, 95, "반박(R)"))

FIGR["oxn"] = svg(620, 190,
    box(230, 10, 160, "산화·환원 반응", "#fde7c9")
    + "".join(box(30 + i * 200, 75, 150, s) + f"<path d='M310 40 L{105+i*200} 75' stroke='#555'/>" for i, s in enumerate(["산소의 이동", "전자의 이동", "산화수 변화"]))
    + box(30, 145, 120, "산화제: 환원됨") + box(200, 145, 120, "환원제: 산화됨") + box(450, 145, 150, "예: SO₂ (㉠ 환원제?)")
    + "<path d='M505 105 Q300 125 90 145' stroke='#c33' stroke-dasharray='5 3' fill='none'/>" + t(300, 132, "㉡ 교차 연결?", 10)
    + "<path d='M260 160 L450 160' stroke='#555'/>")

FIGR["mb"] = svg(620, 170,
    "".join(f"<path d='M{60+i*170} 40 L{60+i*170} 70 L{30+i*170} 140 L{120+i*170} 140 L{90+i*170} 70 L{90+i*170} 40' fill='none' stroke='#555'/>"
            + f"<path d='M{33+i*170} 135 L{117+i*170} 135 L{100+i*170} 100 L{50+i*170} 100 Z' fill='{c}'/>"
            + f"<rect x='{55+i*170}' y='30' width='40' height='10' fill='#a77' />" + t(75 + i * 170, 160, l, 10)
            for i, (c, l) in enumerate([("#5b8fd8", "섞은 직후"), ("#f6f6f6", "마개를 막아 둠"), ("#5b8fd8", "흔들면")]))
    + f"<path d='M135 90 L195 90 M188 85 L195 90 L188 95' {S}/>" + f"<path d='M305 90 L365 90 M358 85 L365 90 L358 95' {S}/>"
    + "<path d='M400 60 q15 -10 30 0 M410 50 q15 -10 30 0' stroke='#999' fill='none'/>" + t(540, 30, "반복된다!", 11, weight='bold')
    + t(540, 60, "포도당 1.5 g, NaOH 2 g", 9) + t(540, 76, "메틸렌 블루 약 2 mL", 9))

FIGR["cell"] = svg(620, 180,
    beaker(40, 70, 90, 80, 55, "#dfe7ee") + beaker(220, 70, 90, 80, 55, "#cfe0f7")
    + "<rect x='70' y='40' width='14' height='95' fill='#9aa'/>" + "<rect x='260' y='40' width='14' height='95' fill='#c87'/>"
    + "<path d='M100 80 L100 55 L250 55 L250 80' stroke='#888' stroke-width='8' fill='none' opacity='.5'/>" + t(175, 50, "염다리", 9)
    + "<path d='M77 40 L77 20 L150 20 M267 40 L267 20 L200 20' stroke='#c33' fill='none'/>" + "<rect x='150' y='8' width='50' height='24' rx='4' fill='#223'/>" + t(175, 24, "V", 11, weight='bold').replace("#111", "#fff")
    + t(85, 168, "Zn | 1 M ZnSO₄", 10) + t(265, 168, "Cu | 1 M CuSO₄", 10)
    + "<rect x='380' y='30' width='230' height="
      "'120' rx='6' fill='#fafafa' stroke='#999'/>" + t(495, 52, "측정 전위차", 11, weight='bold')
    + t(495, 80, "Zn/Cu 0.90 V", 10) + t(495, 102, "Zn/Fe 0.23 V  (㉡ 오류?)", 10) + t(495, 124, "Fe/Cu 0.65 V", 10))

FIGR["plate"] = svg(620, 170,
    beaker(60, 60, 200, 80, 60, "#eef0f4") + "<rect x='90' y='30' width='14' height='100' fill='#ccc' stroke='#777'/>" + t(97, 24, "은판 (+)", 10)
    + "<ellipse cx='220' cy='105' rx='16' ry='22' fill='#d9a066' stroke='#855'/><path d='M220 83 L220 30' stroke='#855'/>" + t(220, 24, "구리 펜던트 (−)", 10)
    + "<path d='M97 30 L97 10 L140 10 M220 10 L180 10' stroke='#c33' fill='none'/>" + "<rect x='140' y='0' width='40' height='18' fill='#444'/>"
    + t(160, 160, "K[Ag(CN)₂](aq)", 10)
    + "<path d='M110 155 q8 -12 0 -24 M130 155 q8 -12 0 -24' stroke='#e55' fill='none'/>" + t(40, 165, "㉠ 가열?", 10, "start")
    + "<rect x='330' y='30' width='280' height="
      "'120' rx='6' fill='#fafafa' stroke='#999'/>" + t(470, 52, "채점 기준(총체적?)", 11, weight='bold')
    + t(345, 80, "8~10점: 정확히 이해, 안전하게 잘 수행", 9, "start") + t(345, 102, "4~7점: 대체로 이해·수행", 9, "start") + t(345, 124, "0~3점: 이해와 수행 부족", 9, "start"))

FIGR["fut"] = svg(620, 140,
    "".join(f"<rect x='{10+i*152}' y='40' width='140' height='50' rx='8' fill='{c}' stroke='#789'/>" + t(80 + i * 152, 62, s, 10, weight='bold') + t(80 + i * 152, 80, d, 9)
            + (f"<path d='M{150+i*152} 65 L{162+i*152} 65 M{156+i*152} 60 L{162+i*152} 65 L{156+i*152} 70' {S}/>" if i < 3 else "")
            for i, (s, d, c) in enumerate([("문제로의 초대", "뉴스 → 질문 만들기", "#eef3fb"), ("탐색", "전지 장단점 조사", "#eef3fb"), ("설명·해결 방안", "미래 전지 설계", "#eef3fb"), ("실행", "축제 발표·의견서", "#fde7c9")]))
    + t(310, 22, "야거의 STS 수업 모형", 12, weight='bold') + t(310, 120, "수소 연료 전지: (−) 2H₂ → 4H⁺ + 4e⁻   (+) O₂ + 4H⁺ + 4e⁻ → 2H₂O", 10))

# 2. 수소 화합물의 분자량–끓는점 그래프
_HB = {"14족": ([16, 32, 77, 122], [-161, -112, -88, -52], "#2a7"), "15족": ([17, 34, 78, 125], [-33, -88, -62, -17], "#a33"),
       "16족": ([18, 34, 81, 130], [100, -60, -41, -2], "#36c"), "17족": ([20, 37, 81, 128], [20, -85, -67, -35], "#e80")}
FIGE["hbp"] = svg(620, 200,
    axes(50, 15, 330, 165, "분자량", "끓는점(℃)")
    + "".join(plot(50, 15, 320, 165, xs, ys, (0, 140), (-180, 110), c) + t(50 + xs[-1] / 140 * 320 + 4, 15 + 165 - (ys[-1] + 180) / 290 * 165 + 4, g, 9, "start")
              for g, (xs, ys, c) in _HB.items())
    + "<path d='M50 " + f"{15+165-(0+180)/290*165:.0f}" + " L380 " + f"{15+165-(0+180)/290*165:.0f}" + "' stroke='#bbb' stroke-dasharray='3 3'/>" + t(46, 15 + 165 - 180 / 290 * 165 + 4, "0", 9, "end")
    + "<rect x='420' y='30' width='190' height='130' rx='6' fill='#fafafa' stroke='#999'/>" + t(515, 52, "분자량 32~37 비교", 11, weight='bold')
    + t(515, 78, "SiH₄ −112 / PH₃ −88", 10) + t(515, 100, "HCl −85 / H₂S −60", 10) + t(515, 130, "NH₃ −33 vs SbH₃ −17 (㉡?)", 10))

# 4. 삼투압 실험 장치
FIGE["osm"] = svg(620, 190,
    "<path d='M60 20 L60 150 Q60 175 85 175 L175 175 Q200 175 200 150 L200 20' fill='none' stroke='#555' stroke-width='1.6'/>"
    + "<path d='M80 20 L80 150 Q80 158 88 158 L172 158 Q180 158 180 150 L180 20' fill='none' stroke='#555' stroke-width='1.6'/>"
    + "<path d='M62 90 L78 90 L78 152 Q80 172 100 172 L160 172 Q182 172 182 150 L182 60 L198 60 L198 152 Q198 173 175 173 L85 173 Q62 173 62 152 Z' fill='#e8f3fb'/>"
    + "<path d='M130 158 L130 175' stroke='#c33' stroke-width='3' stroke-dasharray='3 2'/>" + t(130, 188, "반투막", 9)
    + t(70, 82, "증류수", 9) + t(190, 52, "설탕물", 9)
    + f"<path d='M215 60 L215 90 M210 66 L215 60 L220 66 M210 84 L215 90 L220 84' {S}/>" + t(222, 78, "Δh", 10, "start")
    + "<rect x='280" + "' y='25' width='330' height='145' rx='6' fill='#fafafa' stroke='#999'/>" + t(445, 47, "우리 모둠의 설계 점검", 11, weight='bold')
    + t(295, 75, "조작: 몰농도  → ㉡ 1 M 한 가지만?", 10, "start") + t(295, 99, "통제: ㉠ 온도뿐?", 10, "start")
    + t(295, 123, "종속: 높이 차 → ㉢ 멈출 때까지?", 10, "start") + t(295, 152, "π = CRT = 1 × 0.082 × 298 ≈ ?", 10, "start"))
