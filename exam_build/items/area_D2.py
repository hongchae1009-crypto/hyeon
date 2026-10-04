"""영역 D(입체화학·형태 분석) 기출변형 9문항 — 2026A-1 은 area_D.py 에 있음.
모든 입체 SMILES 는 RDKit(CIP, 3D 면 판정)로 검증함. 의자 형태·Newman 투영·에너지 도표·크로마토그램은 이 파일의 SVG 도우미로 그린다."""
import math
from chem import M, L, arrow, varrow, scheme, rows, frame, plus

# ───────────────────────── SVG 도우미 (이 파일 전용) ─────────────────────────
_F = 'font-family="Arial, NanumGothic, sans-serif"'


def _sub(t):
    """'CH(CH3)2' 같은 간단 표기를 아래첨자 tspan 으로."""
    out = ''
    for ch in t:
        out += f'<tspan baseline-shift="sub" font-size="75%">{ch}</tspan>' if ch.isdigit() else ch
    return out


def chair(subs, label='', w=170, h=104, R=46, hz=13, elev=0.30, L_ax=24, L_eq=24, fs=10.5, ring_lbl=None):
    """의자 형태 사이클로헥세인.
    고리 원자 번호 k=0..5 (k=0 오른쪽 끝[위로 솟은 끝], k=3 왼쪽 끝[아래로 처진 끝]).
    짝수 k 의 축 방향은 위(up), 홀수 k 의 축 방향은 아래(down).
    subs = {(k, 'ax'|'eq'): '라벨'}"""
    cx, cy = w / 2, h / 2 + 2
    P, AX, EQ = [], [], []
    for k in range(6):
        th = math.radians(60 * k)
        z = hz if k % 2 == 0 else -hz
        x, y = R * math.cos(th), R * math.sin(th)
        P.append((cx + x, cy - (z + y * elev)))
        sgn = 1 if k % 2 == 0 else -1
        AX.append((0, -sgn))
        ex, ey, ez = math.cos(th), math.sin(th), -0.38 * sgn
        vx, vy = ex, -(ez * 1.0 + ey * elev)
        n = math.hypot(vx, vy)
        EQ.append((vx / n, vy / n))
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
    for k in range(6):
        a, b = P[k], P[(k + 1) % 6]
        s += f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#000" stroke-width="1.3"/>'
    for (k, kind), lab in subs.items():
        d = AX[k] if kind == 'ax' else EQ[k]
        Ln = L_ax if kind == 'ax' else L_eq
        x0, y0 = P[k]
        x1, y1 = x0 + d[0] * Ln, y0 + d[1] * Ln
        s += f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#000" stroke-width="1.1"/>'
        if d[0] > 0.35:
            anc, tx = 'start', x1 + 1
        elif d[0] < -0.35:
            anc, tx = 'end', x1 - 1
        else:
            anc, tx = 'middle', x1
        ty = y1 + (fs * 0.85 if d[1] > 0.3 else (-2 if d[1] < -0.3 else fs * 0.35))
        s += f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="{fs}" text-anchor="{anc}" {_F}>{_sub(lab)}</text>'
    if ring_lbl:
        for k, t in ring_lbl.items():
            x0, y0 = P[k]
            s += f'<text x="{x0+3:.1f}" y="{y0+11:.1f}" font-size="7.5" {_F} fill="#444">{t}</text>'
    s += '</svg>'
    lab = f'<div class="lbl">{label}</div>' if label else ''
    return f'<div class="cmpd">{s}{lab}</div>'


def newman(front, back, label='', r=22, Lf=30, Lb=14, w=150, h=120, fs=10.5):
    """Newman 투영. front/back = [(화면각도°, '라벨'), ...]  (0°=오른쪽, 90°=위)."""
    cx, cy = w / 2, h / 2
    s = f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff" stroke="#000" stroke-width="1.2"/>'

    def lab(x, y, a, t):
        c = math.cos(math.radians(a))
        anc = 'start' if c > 0.3 else ('end' if c < -0.3 else 'middle')
        dy = fs * 0.35 if abs(math.sin(math.radians(a))) < 0.5 else (-2 if math.sin(math.radians(a)) > 0 else fs * 0.85)
        return f'<text x="{x + (2 if c > 0.3 else -2 if c < -0.3 else 0):.1f}" y="{y + dy:.1f}" font-size="{fs}" text-anchor="{anc}" {_F}>{_sub(t)}</text>'
    for a, t in back:
        ra = math.radians(a)
        x0, y0 = cx + r * math.cos(ra), cy - r * math.sin(ra)
        x1, y1 = cx + (r + Lb) * math.cos(ra), cy - (r + Lb) * math.sin(ra)
        s += f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#000" stroke-width="1.1"/>' + lab(x1, y1, a, t)
    for a, t in front:
        ra = math.radians(a)
        x1, y1 = cx + Lf * math.cos(ra), cy - Lf * math.sin(ra)
        s += f'<line x1="{cx}" y1="{cy}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#000" stroke-width="1.2"/>' + lab(x1, y1, a, t)
    s += '</svg>'
    lb = f'<div class="lbl">{label}</div>' if label else ''
    return f'<div class="cmpd">{s}{lb}</div>'


def energy_profile():
    """사이클로헥세인 고리 뒤집힘 에너지 도표 (Klein 값, kJ/mol)."""
    W, H = 300, 150
    x0, y0, ys = 34, 128, 2.2          # y = y0 - E*ys
    pts = [(0, 0, 'C'), (1, 45, 'A'), (2, 23, 'D'), (3, 29, 'B'), (4, 23, 'D'), (5, 45, 'A'), (6, 0, 'C')]
    X = lambda i: x0 + i * 40
    s = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
    s += f'<line x1="{x0-8}" y1="{y0+6}" x2="{x0-8}" y2="10" stroke="#000" stroke-width="0.9"/><path d="M{x0-11},14 L{x0-8},6 L{x0-5},14 z"/>'
    s += f'<line x1="{x0-8}" y1="{y0+6}" x2="{W-10}" y2="{y0+6}" stroke="#000" stroke-width="0.9"/>'
    s += f'<text x="10" y="{(y0+10)/2}" font-size="8" {_F} transform="rotate(-90 10 {(y0+10)/2})" text-anchor="middle">상대 에너지 (kJ/mol)</text>'
    s += f'<text x="{(W+x0)/2}" y="{H-2}" font-size="8" {_F} text-anchor="middle">반응 좌표 (고리 뒤집힘)</text>'
    d = ''
    for j in range(len(pts) - 1):
        xa, ya = X(pts[j][0]), y0 - pts[j][1] * ys
        xb, yb = X(pts[j + 1][0]), y0 - pts[j + 1][1] * ys
        xm = (xa + xb) / 2
        d += (f'M{xa:.1f},{ya:.1f} ' if j == 0 else '') + f'C{xm:.1f},{ya:.1f} {xm:.1f},{yb:.1f} {xb:.1f},{yb:.1f} '
    s += f'<path d="{d}" fill="none" stroke="#000" stroke-width="1.3"/>'
    for i, E, t in pts:
        x, y = X(i), y0 - E * ys
        s += f'<line x1="{x-9}" y1="{y:.1f}" x2="{x+9}" y2="{y:.1f}" stroke="#000" stroke-width="2"/>'
        s += f'<text x="{x}" y="{y-5:.1f}" font-size="10" font-weight="700" text-anchor="middle" {_F}>{t}</text>'
    for E in (0, 23, 29, 45):
        y = y0 - E * ys
        s += f'<line x1="{x0-8}" y1="{y:.1f}" x2="{x0-5}" y2="{y:.1f}" stroke="#000" stroke-width="0.8"/>'
        s += f'<line x1="{x0-5}" y1="{y:.1f}" x2="{W-10}" y2="{y:.1f}" stroke="#999" stroke-width="0.4" stroke-dasharray="2,2"/>'
        s += f'<text x="{x0-10}" y="{y+3:.1f}" font-size="7.5" text-anchor="end" {_F}>{E}</text>'
    return s + '</svg>'


def chrom(peaks, title, W=140, H=74, t0=4, t1=16):
    """크로마토그램: peaks = [(t, 높이0~1, '라벨'), ...]"""
    pad = 10; base = H - 16
    X = lambda t: pad + (t - t0) / (t1 - t0) * (W - 2 * pad)
    pts = []
    for i in range(201):
        t = t0 + (t1 - t0) * i / 200
        yv = sum(hh * math.exp(-((t - tc) / 0.28) ** 2) for tc, hh, _ in peaks)
        pts.append(f'{X(t):.1f},{base - yv * (base - 18):.1f}')
    s = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">'
    s += f'<text x="{W/2}" y="9" font-size="8" text-anchor="middle" {_F}>{title}</text>'
    s += f'<line x1="{pad}" y1="{base}" x2="{W-pad}" y2="{base}" stroke="#000" stroke-width="0.8"/>'
    s += f'<polyline points="{" ".join(pts)}" fill="none" stroke="#000" stroke-width="1"/>'
    for tc, hh, lab in peaks:
        x = X(tc)
        s += f'<text x="{x:.1f}" y="{base - hh*(base-18) - 3:.1f}" font-size="8.5" text-anchor="middle" {_F}>{lab}</text>'
    s += f'<text x="{W-pad}" y="{H-3}" font-size="7.5" text-anchor="end" {_F}>시간 →</text>'
    return s + '</svg>'


def svgbox(svg, label=''):
    lb = f'<div class="lbl">{label}</div>' if label else ''
    return f'<div class="cmpd">{svg}{lb}</div>'


# ───────────────────────── 구조 SMILES (RDKit 검증값) ─────────────────────────
HEXA_IPR = 'CC(C)[C@H]1[C@H](C(C)C)[C@@H](C(C)C)[C@H](C(C)C)[C@@H](C(C)C)[C@@H]1C(C)C'   # all-trans (위·아래 교대)
MICHAEL_S = 'CCOC(=O)C(C(=O)OCC)[C@H](C[N+](=O)[O-])c1ccccc1'                          # (S)
MICHAEL_R = 'CCOC(=O)C(C(=O)OCC)[C@@H](C[N+](=O)[O-])c1ccccc1'                         # (R)
DIBR_MESO = 'Br[C@@H](c1ccccc1)[C@H](Br)c1ccccc1'          # meso-(1R,2S)
BRHYD = 'O[C@@H](c1ccccc1)[C@H](Br)c1ccccc1'               # (1S,2R) (+거울상)
STO_RR = 'c1ccccc1[C@H]1O[C@@H]1c1ccccc1'                  # trans-stilbene oxide (R,R)
HB_MESO = 'O[C@@H](c1ccccc1)[C@H](O)c1ccccc1'              # meso-hydrobenzoin
E_STILB = 'C(=C/c1ccccc1)\\c1ccccc1'
A_TRANS = 'C[C@@H]1CCCC[C@H]1Br'                          # (1R,2R)-trans
C_CIS = 'C[C@@H]1CCCC[C@@H]1Br'                           # (1S,2R)-cis
A_D = 'C[C@@H]1CCC[C@@H]([2H])[C@H]1Br'                   # D 와 Br cis, (1R,2R,6R)
B_PROD = 'C[C@@H]1CCCC=C1'                                 # (R)-3-methylcyclohexene
D_PROD = 'CC1=CCCCC1'
E_PROD = 'C[C@@H]1CCCC([2H])=C1'                          # (R)-1-deuterio-3-methylcyclohexene
PINENE = 'CC1=CC[C@@H]2C[C@H]1C2(C)C'                      # (+)-α-pinene (1R,5R)
SH_SM = 'OC/C(C)=C/COCc1ccccc1'
SH_A = 'OC[C@@]1(C)O[C@@H]1COCc1ccccc1'                    # (2R,3R)
SH_B = 'OC[C@](C)(OC)[C@H](O)COCc1ccccc1'                  # (2S,3R)
SH_C = 'OC[C@@](C)(O)[C@@H](N=[N+]=[N-])COCc1ccccc1'       # (2S,3S)
LAC1 = 'O=C1C[C@H]2C[C@H]3CCCC[C@@H]3C[C@@H]2O1'           # 락톤 결합 2개 모두 적도 (안정)
LAC2 = 'O=C1C[C@H]2C[C@@H]3CCCC[C@H]3C[C@@H]2O1'           # 락톤 결합이 trans-이축이어야 함 → 꼬인보트
HEXD_RR = 'CC[C@@H](O)[C@H](O)CC'                          # (3R,4R)
HEXD_MESO = 'CC[C@@H](O)[C@@H](O)CC'                       # meso (3R,4S)
OSMATE = 'CC[C@@H]1O[Os](=O)(=O)O[C@H]1CC'                 # trans 오스뮴산 에스터
EPOX_T = 'CC[C@@H]1O[C@H]1CC'                              # trans-2,3-diethyloxirane (S,S)
TDEC = 'C1CC[C@H]2CCCC[C@@H]2C1'
CDEC = 'C1CC[C@H]2CCCC[C@H]2C1'

BEF_BOX = '<div class="ansbox">' + M('C/C=C/C', 'B: (E)-2-butene', 14) + M('C/C=C\\C', 'E: (Z)-2-butene', 14) + M('C[C@@H](O)CC', 'F: (R)-2-butanol (주)', 14) + '</div>'
DEF = '(단, 각 반응에서는 적절한 분리·정제 과정을 수행하였다.)'

ITEMS = [
# ───────────────────────────── 1. 2025B-2 ─────────────────────────────
dict(
    key='2025B-2',
    src='2025학년도 B형 2번',
    src_topic='사이클로헥세인 고리 뒤집힘 에너지 도표에서 의자·반쪽의자·보트·꼬인보트 형태 찾기, 의자 형태의 점군',
    change='도표의 기호 배치를 바꾸어(최저=C, 최고=A) 단순 암기를 막고, 묻는 형태를 보트·꼬인보트와 꼬인보트의 점군(D<sub>2</sub>)으로 바꿈. '
           '여기에 JACS 1990 논문의 all-trans-hexaisopropylcyclohexane(모든 치환기가 축 방향인 의자 형태가 더 안정)을 붙여, '
           '“치환기는 적도가 유리하다”는 규칙이 언제 깨지는지를 이면각(Karplus식 사고) 단서로 판단하게 함',
    paper=dict(cite='J. Am. Chem. Soc. 1990, 112, 893–894', book='Klein 4.72',
               what='all-trans-1,2,3,4,5,6-hexaethylcyclohexane은 모두 적도인 의자 형태, hexaisopropyl 유도체는 모두 축 방향인 의자 형태를 선호'),
    nobel='1969 노벨 화학상(D. H. R. Barton·O. Hassel — 형태 분석의 개념 확립)',
    body=f'''다음은 사이클로헥세인(cyclohexane)의 고리 뒤집힘 과정에서 나타나는 형태 <b class="lbltxt">A</b>~<b class="lbltxt">D</b>의 상대 에너지를 나타낸 것이다. <b class="lbltxt">A</b>~<b class="lbltxt">D</b>는 각각 의자(chair), 반쪽의자(half-chair), 보트(boat), 꼬인보트(twist-boat) 형태 중 하나이다.
{frame('<div class="spec">' + energy_profile() + '</div>')}
다음은 all-<i>trans</i>-1,2,3,4,5,6-hexaisopropylcyclohexane(<b class="lbltxt">X</b>)에 대한 자료이다.
{frame(scheme(M(HEXA_IPR, 'X', 13)),
       '<div class="chem">◦ <b class="lbltxt">X</b>의 가장 안정한 의자 형태에서, 이웃한 두 고리 탄소에 결합한 수소의 H–C–C–H 이면각은 모두 약 60°이다.</div>')}
<p class="ask"><b class="lbltxt">B</b>와 <b class="lbltxt">D</b>에 해당하는 형태의 이름을 각각 쓰고, <b class="lbltxt">D</b>의 점군을 쓰시오. 또한 <b class="lbltxt">X</b>의 가장 안정한 의자 형태에서 6개의 아이소프로필기가 축(axial) 방향과 적도(equatorial) 방향 중 어느 쪽에 놓이는지 쓰시오. [[PTS]]</p>''',
    answer='''<b class="lbltxt">B</b> = 보트 형태, <b class="lbltxt">D</b> = 꼬인보트 형태, <b class="lbltxt">D</b>의 점군 = <b>D<sub>2</sub></b><br>
<b class="lbltxt">X</b>: 6개의 아이소프로필기가 모두 <b>축 방향</b>(고리 수소는 모두 적도 방향)''',
    explain='''<p><b>핵심 반응·개념:</b> 사이클로헥세인의 형태 에너지 지형(의자 ⇄ 반쪽의자 ⇄ 꼬인보트 ⇄ 보트), 점군, 이웃 치환기의 기어(gear) 충돌.</p>
<p>① 양 끝의 최저점 <b>C</b>는 각 변형·비틀림 변형이 모두 없는 <b>의자 형태</b>(0 kJ/mol, 점군 D<sub>3d</sub>)이다. 가장 높은 봉우리 <b>A</b>는 고리 탄소 5개(4개 이상)가 거의 한 평면에 놓여 가림이 심한 <b>반쪽의자</b>(≈45 kJ/mol, C<sub>2</sub>)로, 고리 뒤집힘의 전이 상태이다.</p>
<p>② 두 개의 국소 최저점 <b>D</b>(≈23 kJ/mol)는 실제로 존재하는 중간체인 <b>꼬인보트</b>이다. 보트의 깃대(flagpole) 수소 반발과 C2–C3·C5–C6 결합의 가림을 비틀어서 줄인 형태다. 서로 수직인 C<sub>2</sub> 축 3개를 가지며 거울면이 없으므로 점군은 <b>D<sub>2</sub></b>이다(카이랄한 형태로, 두 <b>D</b>는 서로 거울상 관계다).</p>
<p>③ 두 꼬인보트 사이의 작은 봉우리 <b>B</b>(≈29 kJ/mol)가 <b>보트</b>(C<sub>2v</sub>)다. 보트는 에너지 최저점이 아니라 두 꼬인보트를 잇는 전이 상태라는 점이 흔한 오답 포인트다(“보트=중간체”로 답하면 틀림).</p>
<p>④ 25 ℃에서 꼬인보트의 비율은 대략 e<sup>−23000/(8.314×298)</sup> ≈ 1×10<sup>−4</sup>로 매우 적다. 따라서 상온의 사이클로헥세인 유도체는 거의 전부 의자 형태로 존재한다.</p>
<p>⑤ <b>X</b>(all-<i>trans</i>): 이웃 치환기가 모두 <i>trans</i>이므로 위·아래가 번갈아 놓이고, 의자 형태는 “6개 모두 적도” 아니면 “6개 모두 축” 둘 중 하나다. <i>trans</i>-1,2 관계인 이웃 수소의 이면각은 둘 다 축이면 ≈180°, 둘 다 적도이면 ≈60°이다. 자료에서 이면각이 모두 약 60°이므로 <b>고리 수소가 모두 적도 → 아이소프로필기는 모두 축 방향</b>이다.</p>
<p>⑥ 이유(논문): 모두 적도인 형태에서는 각 iPr이 양쪽 이웃 iPr 사이에 끼인다. iPr은 CH<sub>3</sub>가 2개라서 C(고리)–CH 결합을 어떻게 회전해도 메틸 하나가 이웃 iPr과 gauche·가림 반발을 일으킨다(기어 충돌). 에틸기(CH<sub>3</sub> 1개)는 메틸을 바깥으로 돌려 피할 수 있어서 hexaethyl 유도체는 모두 적도 형태를 택한다. 모두 축인 형태에서는 1,3-이축 상대가 수소가 아니라 다른 iPr이다. 그러나 각 iPr이 메타인 H를 고리 안쪽으로 향하게 맞물리면 이웃 간 반발이 크게 줄어든다. A값(iPr ≈ 9.2 kJ/mol)을 단순히 더해서 예측하면 틀리는 대표적인 예다.</p>''',
),

# ───────────────────────────── 2. 2024B-2 ─────────────────────────────
dict(
    key='2024B-2',
    src='2024학년도 B형 2번',
    src_topic='리파제 동역학적 분할 후 카이랄 HPLC 크로마토그램에서 피크의 R/S 배열과 거울상 초과도(ee) 구하기',
    change='효소 동역학적 분할 대신, 산화 상태에 따라 선택성이 뒤바뀌는 카이랄 Cu 촉매의 비대칭 Michael 첨가(JACS 2012)를 소재로 바꿈. '
           '그려 준 생성물 P의 CIP 판정에서 –CH<sub>2</sub>NO<sub>2</sub> > –C<sub>6</sub>H<sub>5</sub> > –CH(CO<sub>2</sub>Et)<sub>2</sub> 순위(산소 수에 속기 쉬운 함정)를 묻고, '
           '피크 면적비 → ee → 실험 조건(용매)을 역추적하게 하여 사고 단계를 늘림',
    paper=dict(cite='J. Am. Chem. Soc. 2012, 134, 8054–8057', book='Klein 5.65',
               what='산화·환원으로 전환되는 카이랄 Cu 촉매: Cu(I)형은 (S), Cu(II)형은 (R) Michael 부가물(diethyl malonate + trans-β-nitrostyrene)을 주로 생성; 용매별 ee 자료'),
    nobel='2001 노벨 화학상(W. S. Knowles·R. Noyori — 카이랄 금속 촉매에 의한 비대칭 반응). 같은 malonate–nitroalkene 비대칭 Michael 첨가는 2021 노벨 화학상(B. List·D. MacMillan) 비대칭 유기촉매 반응의 대표 예이기도 하다',
    body=f'''다음은 카이랄 구리 촉매를 이용한 diethyl malonate와 <i>trans</i>-β-nitrostyrene의 비대칭 마이클(Michael) 첨가 반응의 [반응식]과, 카이랄 칼럼을 이용한 액체 크로마토그래피로 생성물을 분석한 [자료]이다. 이 촉매는 Cu(I) 형태일 때 <b class="lbltxt">P</b>를, Cu(II) 형태일 때 <b class="lbltxt">P</b>의 거울상이성질체를 주로 생성한다. (단, 반응에서는 적절한 정제 과정을 수행하였다.)
{frame(scheme(M('CCOC(=O)CC(=O)OCC', '', 13), plus(), M('[O-][N+](=O)/C=C/c1ccccc1', '', 13)),
       scheme(arrow('카이랄 Cu(I) 촉매', '염기, 용매 <i>X</i>'), M(MICHAEL_S, 'P', 14)), title='[반응식]')}
{frame('<table class="data"><tr><th>용매</th><th>톨루엔</th><th>THF</th><th>CH<sub>3</sub>CN</th><th>CHCl<sub>3</sub></th><th>CH<sub>2</sub>Cl<sub>2</sub></th><th>헥세인</th></tr>'
       '<tr><td><b class="lbltxt">P</b>의 ee(%)</td><td>24</td><td>48</td><td>72</td><td>30</td><td>46</td><td>51</td></tr></table>',
       scheme(svgbox(chrom([(8, .8, ''), (12, .8, '')], 'P의 라세믹 표준 시료')),
              svgbox(chrom([(8, .16, '㉠'), (12, .95, '㉡')], 'Cu(I), 용매 X 생성물'))),
       '<div class="chem" style="text-align:center">라세믹 표준 시료의 두 피크 면적비는 1 : 1이고, 생성물의 ㉠ : ㉡ 면적비는 7 : 43이다.</div>', title='[자료]')}
<p class="ask">피크 ㉠에 해당하는 화합물의 <i>R</i>, <i>S</i> 배열을 쓰고, 용매 <i>X</i>를 쓰시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M(MICHAEL_R, '㉠: (R)-거울상이성질체', 14)}</div>
㉠ = <b><i>R</i></b> (P는 <i>S</i>) · ee = (43 − 7)/(43 + 7) × 100 = 72 % → 용매 <i>X</i> = <b>CH<sub>3</sub>CN</b>''',
    explain='''<p><b>핵심 반응·개념:</b> 카이랄 촉매에 의한 거울상선택적 Michael 첨가, CIP 우선순위, 카이랄 크로마토그래피와 ee 계산.</p>
<p>① 메커니즘: 염기와 Cu 촉매가 diethyl malonate의 산성 α-H(pK<sub>a</sub> ≈ 13)를 떼어 Cu에 배위한 엔올레이트를 만든다. 이 엔올레이트가 nitroalkene의 β-탄소(Ph가 붙은 탄소)를 공격하고, 생긴 나이트로네이트가 양성자화되어 P가 된다. 카이랄 리간드가 nitroalkene의 한쪽 거울상 면(enantiotopic face)만 열어 두므로 한 거울상이성질체가 우세해진다. 생성물에서 새로 생긴 카이랄 중심은 Ph가 붙은 벤질 탄소 하나뿐이다.</p>
<p>② CIP: 카이랄 중심에 붙은 원자는 C(H<sub>2</sub>NO<sub>2</sub>) = (N, H, H), C<sub>6</sub>H<sub>5</sub> = (C, C, C), CH(CO<sub>2</sub>Et)<sub>2</sub> = (C, C, H), H이다. 첫 번째 차이점에서 원자 번호가 가장 큰 N을 가진 <b>CH<sub>2</sub>NO<sub>2</sub> &gt; Ph &gt; CH(CO<sub>2</sub>Et)<sub>2</sub> &gt; H</b>이다. “산소가 4개 있는 malonate 쪽이 1순위”라고 판단하는 것은 흔한 오답이다. 순위는 바로 붙은 원자 집합을 먼저 비교한다. 그려진 P는 <b><i>S</i></b>이다(RDKit로 확인).</p>
<p>③ Cu(I) 촉매가 P(<i>S</i>)를 주로 주므로 큰 피크 ㉡ = (<i>S</i>)-P, 작은 피크 ㉠ = <b>(<i>R</i>)-거울상이성질체</b>이다. 카이랄 칼럼에서 두 거울상이성질체는 정지상의 카이랄 선택자와 부분입체이성질체 관계의 일시적 착물을 만들기 때문에 머무름 시간이 달라진다.</p>
<p>④ ee = (43 − 7)/(43 + 7) × 100 = <b>72 %</b>, 즉 <i>S</i> : <i>R</i> = 86 : 14이다. 표에서 ee 72 %인 용매는 <b>CH<sub>3</sub>CN</b>이다(논문에서도 ee가 가장 높고 수득률 55 %로 최적 조건이었다).</p>
<p>⑤ 같은 반응을 Cu(II) 형태로 하면 ㉠(<i>R</i>)이 큰 피크가 된다. “촉매의 산화 상태만 바꿔 같은 리간드로 두 거울상이성질체를 모두 얻는” 산화·환원 전환형 촉매라는 점이 논문의 요지다. 라세믹 표준 시료(1 : 1)로 피크 위치를 먼저 확인하는 이유도 함께 기억해 두자.</p>''',
),

# ───────────────────────────── 3. 2023B-2 ─────────────────────────────
dict(
    key='2023B-2',
    src='2023학년도 B형 2번',
    src_topic='trans-2-butene의 Br<sub>2</sub> 안티 첨가(메조), 과산 에폭시화 후 산 촉매 개환으로 메조 다이올 형성, 메조 화합물 고르기',
    change='기질을 (E)-stilbene으로 바꾸고, 에폭사이드를 과산 대신 브로모하이드린 → 분자 내 S<sub>N</sub>2(NaOH) 경로로 만들게 함. '
           '중간체 C(브로모하이드린)는 두 입체 중심을 가져도 메조가 아님을 판별하게 하여 메조 판정 함정을 하나 더 둠',
    paper=dict(cite='J. Org. Chem. 1991, 56, 2582–2584', book='Klein 8.92',
               what='meso-1,2-dibromo-1,2-diphenylethane을 DMF 속에서 가열하면 탈브로민화되어 (E)-stilbene만 생성됨(입체특이성 vs 입체선택성 논의)'),
    nobel='',
    body=f'''다음은 반응물 <b class="lbltxt">A</b>(C<sub>14</sub>H<sub>12</sub>)로부터 주생성물 <b class="lbltxt">B</b>를 합성하는 브로민 첨가 반응과, 중간 주생성물 <b class="lbltxt">C</b>와 <b class="lbltxt">D</b>(C<sub>14</sub>H<sub>12</sub>O)를 거쳐 최종 주생성물 <b class="lbltxt">E</b>(C<sub>14</sub>H<sub>14</sub>O<sub>2</sub>)를 합성하는 반응식이다. {DEF}
{frame(scheme(L('A'), arrow('Br<sub>2</sub>', 'CH<sub>2</sub>Cl<sub>2</sub>'), M(DIBR_MESO, 'B', 14)),
       scheme(L('A'), arrow('Br<sub>2</sub>, H<sub>2</sub>O'), L('C'), arrow('NaOH'), L('D'), arrow('H<sub>3</sub>O<sup>+</sup>'), L('E')))}
<p class="ask"><b class="lbltxt">D</b>의 입체구조를 그리고, <b class="lbltxt">A</b>~<b class="lbltxt">E</b> 중에서 메조 화합물(meso compound)을 모두 쓰시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M(STO_RR, 'D: trans-stilbene oxide (라셈)', 15)}</div>
<b class="lbltxt">D</b> = <i>trans</i>-2,3-diphenyloxirane((2<i>R</i>,3<i>R</i>)와 (2<i>S</i>,3<i>S</i>)의 라셈 혼합물, 한쪽만 그려도 됨)<br>
메조 화합물: <b class="lbltxt">B</b>, <b class="lbltxt">E</b>''',
    explain=f'''<p><b>핵심 반응:</b> 브로모늄 이온을 거치는 안티 첨가, 할로하이드린 형성, 분자 내 S<sub>N</sub>2 에폭사이드 고리 닫힘, 산 촉매 에폭사이드 안티 개환 → <i>trans</i> 알켄 + 순(net) 안티 다이하이드록시화 = 메조.</p>
<p>① <b class="lbltxt">B</b>는 그림에서 (1<i>R</i>,2<i>S</i>)이고 대칭면을 가지는 meso-1,2-dibromo-1,2-diphenylethane이다. Br<sub>2</sub> 첨가는 브로모늄 이온을 거친 <b>안티 첨가</b>이고, 대칭 알켄에 안티 첨가하여 메조가 생기려면 알켄이 <i>trans</i>여야 한다. 따라서 <b class="lbltxt">A</b> = (<i>E</i>)-stilbene이다(<i>cis</i>-stilbene이면 (<i>R,R</i>)/(<i>S,S</i>) 라셈 다이브로마이드).</p>
<div class="ansbox">{M(E_STILB, 'A: (E)-stilbene', 13)}{M(BRHYD, 'C: 브로모하이드린 (라셈)', 13)}{M(HB_MESO, 'E: meso-hydrobenzoin', 13)}</div>
<p>② Br<sub>2</sub>/H<sub>2</sub>O: 브로모늄 이온을 용매인 물이 뒤쪽에서 연다(안티). 두 탄소가 모두 벤질 탄소라 위치 문제는 없다. <b class="lbltxt">C</b> = (1<i>S</i>,2<i>R</i>)-2-bromo-1,2-diphenylethanol과 그 거울상이성질체(라셈)이다. <b>입체 중심이 2개여도 두 중심의 치환기(OH와 Br)가 다르므로 내부 대칭면이 없어 메조가 아니다.</b> 이것이 이 문항의 함정이다.</p>
<p>③ NaOH가 OH를 알콕사이드로 만들고, O<sup>−</sup>가 Br이 붙은 탄소를 뒤쪽에서 공격하는 분자 내 S<sub>N</sub>2가 일어난다. 이 반응은 O<sup>−</sup>와 Br이 anti-periplanar한 형태에서만 진행된다. 그 형태에서 두 Ph는 서로 anti이므로 <b class="lbltxt">D</b> = <i>trans</i>-stilbene oxide이다. 브로민 탄소는 반전되고 OH 탄소는 유지된다. <b class="lbltxt">D</b>는 C<sub>2</sub> 축만 있고 대칭면이 없는 카이랄 분자이며 라셈으로 얻어진다.</p>
<p>④ H<sub>3</sub>O<sup>+</sup>: 양성자화된 에폭사이드를 물이 뒤쪽에서 공격한다(한 탄소만 반전). <i>trans</i>-에폭사이드에 안티 개환이 일어나므로 <b class="lbltxt">E</b> = meso-hydrobenzoin((1<i>R</i>,2<i>S</i>)-1,2-diphenylethane-1,2-diol)이다. (<i>E</i>)-알켄에서 시작한 경로 전체를 보면 “할로하이드린 형성(안티) → 고리 닫힘(반전) → 개환(반전)”으로 순 안티 다이하이드록시화가 된다. 기출의 과산 경로와 결과가 같다.</p>
<p>⑤ 메조 판정: <b class="lbltxt">A</b>는 비카이랄이지만 입체 중심이 없으므로 메조가 아니다. <b class="lbltxt">C</b>, <b class="lbltxt">D</b>는 카이랄이다. 따라서 메조는 <b class="lbltxt">B</b>와 <b class="lbltxt">E</b>뿐이다.</p>
<p>⑥ 논문 연계: <b class="lbltxt">B</b>를 DMF에서 가열하면 (<i>E</i>)-stilbene만 생긴다. 그런데 (<i>R,R</i>)-다이브로마이드에서도 <i>E</i>만 생기므로, 협동적 anti 제거(입체특이적)가 아니라 회전이 자유로운 중간체를 거치는 <b>입체선택적</b> 반응임이 밝혀졌다. 입체특이성(출발물의 입체가 생성물의 입체를 결정)과 입체선택성(더 안정한 생성물이 우세)을 구분하는 좋은 예다.</p>''',
),

# ───────────────────────────── 4. 2021B-8 ─────────────────────────────
dict(
    key='2021B-8',
    src='2021학년도 B형 8번',
    src_topic='menthyl·neomenthyl chloride의 E2(이축 anti-periplanar 요구)와 의자 형태, 반응 속도 비교, Hofmann 제거의 Newman 투영도',
    change='기질을 trans-/cis-2-methylcyclohexyl bromide로 바꾸고, Hofmann 제거 대신 스테로이드 중수소 표지 실험(Tetrahedron Lett. 2010)을 모델화한 '
           '“D 표지 기질의 E2”를 넣었다. 어느 수소(중수소)가 제거되는지를 Newman 투영도로 직접 판정하게 하여 anti-periplanar 요구 조건을 가장 엄밀하게 확인하도록 함',
    paper=dict(cite='Tetrahedron Lett. 2010, 51, 6948–6950', book='Klein 8.90',
               what='cholic acid형 스테로이드의 12α-OTs(축)를 NaOAc로 E2 제거할 때, C11의 축 방향(11β) 수소만 제거되므로 적도 방향에 D를 표지한 기질만 생성물에 D가 남음'),
    nobel='1969 노벨 화학상(D. H. R. Barton — 스테로이드의 축·적도 형태와 반응성의 상관관계)',
    body=f'''다음은 E2 제거 반응을 거쳐 최종 생성물이 형성되는 반응이다. <b class="lbltxt">A′</b>은 <b class="lbltxt">A</b>의 C6 수소 하나가 중수소(D)로 치환된 화합물이다. (단, <b class="lbltxt">A</b>, <b class="lbltxt">A′</b>, <b class="lbltxt">C</b>는 카이랄 화합물이고, 각 반응에서 적절한 분리·정제 과정을 수행하였다.)
{frame(scheme(M(A_TRANS, 'A', 16), arrow('NaOEt', 'EtOH, 가열'), L('B')),
       scheme(M(C_CIS, 'C', 16), arrow('NaOEt', 'EtOH, 가열'), L('D'), '<span class="chem">(주생성물)</span>'), title='[반응 1]')}
{frame(scheme(M(A_D, 'A′', 16), arrow('NaOEt', 'EtOH, 가열'), L('E'), '<span class="chem">(C<sub>7</sub>H<sub>11</sub>D)</span>'), title='[반응 2]')}
<p class="ask">[반응 1]에서 주생성물 <b class="lbltxt">B</b>와 <b class="lbltxt">D</b>의 입체구조를 각각 그리시오. 또한 동일 반응 조건에서 <b class="lbltxt">A</b>와 <b class="lbltxt">C</b> 중 반응 속도가 큰 것의 구조를 가장 안정한 의자 형태로 그리시오. 그리고 [반응 2]에서 <b class="lbltxt">E</b>의 입체구조를 그리고, <b class="lbltxt">E</b>가 생성되는 과정을 <b class="lbltxt">A′</b>의 C1–C6 결합에 대한 뉴먼 투영도(Newman projection)를 그려서 설명하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M(B_PROD, 'B: (R)-3-methylcyclohexene', 15)}{M(D_PROD, 'D: 1-methylcyclohexene', 15)}</div>
반응 속도: <b class="lbltxt">C</b> &gt; <b class="lbltxt">A</b>. <b class="lbltxt">C</b>의 가장 안정한 의자 형태(Br 축, CH<sub>3</sub> 적도):
<div class="ansbox">{chair({(0, 'ax'): 'Br', (0, 'eq'): 'H', (1, 'eq'): 'CH3', (1, 'ax'): 'H'}, 'C (Br 축 · CH₃ 적도)', ring_lbl={0: '1', 1: '2'})}</div>
<div class="ansbox">{M(E_PROD, 'E: (R)-1-deuterio-3-methylcyclohexene', 15)}{newman([(270, 'Br'), (30, 'C2'), (150, 'H')], [(90, 'H'), (330, 'C5'), (210, 'D')], 'A′ 반응성 형태 (C1 앞, C6 뒤)')}</div>''',
    explain='''<p><b>핵심 반응:</b> E2 제거 — 이탈기와 β-H가 anti-periplanar(고리에서는 <b>trans-이축</b>)여야 한다. 그 결과 위치선택성(Zaitsev 여부)과 속도가 형태로 결정된다.</p>
<p>① <b class="lbltxt">A</b> = (1<i>R</i>,2<i>R</i>)-<i>trans</i>-1-bromo-2-methylcyclohexane. 안정한 형태는 Br·CH<sub>3</sub>가 모두 적도인 형태인데, 이때 Br과 anti인 β-H가 없다. 고리가 뒤집혀 Br·CH<sub>3</sub>가 모두 축이 되어야 E2가 가능하다. 그 형태에서 C2의 축 자리는 CH<sub>3</sub>가 차지하므로 C2–H는 적도이고 제거될 수 없다. 남은 것은 C6의 축 H뿐이다. 그래서 Zaitsev 규칙에 어긋나는 <b class="lbltxt">B</b> = 3-methylcyclohexene만 생긴다. C2는 반응에 참여하지 않으므로 배열이 유지된다 → (<i>R</i>)-3-methylcyclohexene.</p>
<p>② <b class="lbltxt">C</b> = (1<i>S</i>,2<i>R</i>)-<i>cis</i>-이성질체. 두 의자 형태 중 (Br 축, CH<sub>3</sub> 적도)가 (Br 적도, CH<sub>3</sub> 축)보다 A값 차이(CH<sub>3</sub> 7.3 vs Br ≈ 2 kJ/mol)만큼 안정하다. 바로 이 <b>가장 안정한 형태가 반응성 형태</b>다. Br(축)과 anti인 축 H가 C2와 C6에 모두 있으므로 더 치환된 <b class="lbltxt">D</b> = 1-methylcyclohexene(Zaitsev)이 주생성물이다(3-methylcyclohexene은 소량).</p>
<p>③ 속도: <b class="lbltxt">A</b>는 평형 분율이 매우 작은 불리한 이축 형태(이적도 형태보다 대략 CH<sub>3</sub> 7.3 + Br ≈ 2 kJ/mol에서 이적도의 CH<sub>3</sub>/Br gauche 반발만큼을 뺀 수 kJ/mol 불안정)를 거쳐야 하므로 느리다. <b class="lbltxt">C</b>는 바닥 상태 형태 그대로 반응하므로 빠르다(neomenthyl > menthyl과 같은 원리). <b>반응 가능한(이탈기가 축인) 형태의 몰분율</b>이 속도를 결정한다는 점이 핵심이다.</p>
<p>④ [반응 2] <b class="lbltxt">A′</b>(1<i>R</i>,2<i>R</i>,6<i>R</i>)에서 D는 Br과 <i>cis</i>이다. 반응성 형태(Br 축)에서 C6의 축 자리는 Br과 <i>trans</i>인 쪽이므로 <b>축에는 H, 적도에는 D</b>가 놓인다. C1–C6 결합을 따라 본 Newman 투영도에서 앞 탄소(C1)의 Br(아래)과 정확히 180°인 뒤 탄소(C6)의 원자는 H이다. D는 Br과 gauche(약 60°)라 제거될 수 없다. EtO<sup>−</sup>가 anti인 H를 떼고, C–H σ 전자쌍이 새 π 결합을 이루면서 Br<sup>−</sup>가 동시에 떠난다. 그 결과 D는 새 C=C의 탄소(C6 → 생성물 C1)에 남아 <b class="lbltxt">E</b> = (<i>R</i>)-1-deuterio-3-methylcyclohexene(C<sub>7</sub>H<sub>11</sub>D)이 된다.</p>
<p>⑤ 만약 D가 Br과 <i>trans</i>인 이성질체였다면 D가 축(anti) 자리에 놓여 제거되므로 생성물에 D가 남지 않는다(C–D 절단이므로 1차 동위원소 효과로 더 느리다). 논문(스테로이드 12α-OTs → Δ<sup>11</sup>)에서도 축 방향 11β에 D를 표지한 기질은 D를 잃고, 적도 방향에 표지한 기질만 D를 보존했다. Barton이 정립한 “축 이탈기의 trans-이축 제거”를 그대로 보여 준 실험이다.</p>''',
),

# ───────────────────────────── 5. 2018A-4 ─────────────────────────────
dict(
    key='2018A-4',
    src='2018학년도 A형 4번',
    src_topic='2-bromobutane의 E2(Zaitsev) → 수소화붕소 첨가–산화로 라세미 2-butanol; 생성물로부터 출발물 역추론',
    change='기출의 [E2 → BH<sub>3</sub>] 경로(라세미)에 [알카인 Lindlar 환원 → 카이랄 보레인 Ipc<sub>2</sub>BH] 경로(광학 활성)를 나란히 놓아, '
           '두 출발물(A, D)을 분자식과 생성물의 입체화학으로 역추론하고 “비카이랄 시약 → 라세미, 카이랄 시약 → 광학 활성”의 원리를 서술하게 함',
    paper=dict(cite='J. Org. Chem. 1984, 49, 945–947', book='Klein 9.84',
               what='(+)-α-pinene과 BH<sub>3</sub>(0.5 당량)로부터 단일 입체이성질체 diisopinocampheylborane(Ipc<sub>2</sub>BH)을 얻는 방법; 비대칭 수소화붕소 첨가 시약'),
    nobel='1979 노벨 화학상(H. C. Brown — 유기 붕소 화합물, 수소화붕소 첨가 반응)',
    body=f'''다음은 반응물 <b class="lbltxt">A</b>와 <b class="lbltxt">D</b>로부터 같은 분자식의 알코올을 합성하는 두 반응식이다. [반응 1]의 최종 생성물은 라세미 혼합물이고, [반응 2]의 최종 생성물은 광학 활성이다. {DEF}
{frame(scheme(L('A'), '<span class="chem">(C<sub>4</sub>H<sub>9</sub>Br)</span>', arrow('NaOEt', 'EtOH'), L('B'), '<span class="chem">(C<sub>4</sub>H<sub>8</sub>, 주)</span>'),
       scheme(arrow('1) BH<sub>3</sub>·THF', '2) H<sub>2</sub>O<sub>2</sub>, NaOH'), L('C'), '<span class="chem">(C<sub>4</sub>H<sub>10</sub>O, 라세미)</span>'), title='[반응 1]')}
{frame(scheme(L('D'), '<span class="chem">(C<sub>4</sub>H<sub>6</sub>)</span>', arrow('H<sub>2</sub>', 'Lindlar 촉매'), L('E'),
              arrow('1) Ipc<sub>2</sub>BH', '2) H<sub>2</sub>O<sub>2</sub>, NaOH'), L('F'), '<span class="chem">(C<sub>4</sub>H<sub>10</sub>O, 광학 활성)</span>'),
       scheme(M(PINENE, '(+)-α-pinene', 14), arrow('BH<sub>3</sub>·THF', '(0.5 당량)'), L('Ipc<sub>2</sub>BH'), '<span class="chem">(단일 입체이성질체)</span>'), title='[반응 2]')}
<p class="ask"><b class="lbltxt">A</b>와 <b class="lbltxt">D</b>의 구조를 각각 그리시오. 또한 [반응 2]의 <b class="lbltxt">F</b>는 광학 활성인 반면 [반응 1]의 <b class="lbltxt">C</b>는 라세미 혼합물로 얻어지는 이유를 서술하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M('CCC(C)Br', 'A: 2-bromobutane', 16)}{M('CC#CC', 'D: 2-butyne', 16)}</div>
<b class="lbltxt">B</b>·<b class="lbltxt">E</b>의 두 면(re/si)은 거울상 관계(enantiotopic)이다. 비카이랄 BH<sub>3</sub>는 두 면에 같은 속도로 첨가되므로(거울상 전이 상태, 에너지 같음) C는 1 : 1 라세미가 된다. 카이랄 Ipc<sub>2</sub>BH는 두 면에서 부분입체이성질체 관계의 전이 상태를 만들고 그 에너지가 서로 달라 한 면으로 우선 첨가된다. 그래서 F는 한 거울상이성질체가 과량인 광학 활성 2-butanol이 된다.''',
    explain=f'''<p><b>핵심 반응:</b> E2(Zaitsev) · Lindlar 환원(syn, <i>cis</i>-알켄) · 수소화붕소 첨가–산화(anti-Markovnikov, syn, 배열 유지) · 카이랄 보레인에 의한 비대칭 수소화붕소 첨가.</p>
<p>① 역추론: 최종 생성물 C<sub>4</sub>H<sub>10</sub>O가 라세미 또는 광학 활성이므로 OH가 입체 중심에 있어야 하고, 이 조건을 만족하는 것은 2-butanol뿐이다. 수소화붕소 첨가로 2-butanol을 주려면 알켄이 2-butene이어야 한다. 1-butene은 anti-Markovnikov 첨가로 비카이랄 1-butanol을 주고, 2-methylpropene은 비카이랄 2-methyl-1-propanol을 준다.</p>
<p>② [반응 1]: <b class="lbltxt">A</b>(C<sub>4</sub>H<sub>9</sub>Br) + NaOEt → 2-butene(주)이 되려면 <b class="lbltxt">A</b> = <b>2-bromobutane</b>이다. Zaitsev 규칙에 따라 더 치환된 2-butene(<i>trans</i> &gt; <i>cis</i>)이 1-butene보다 많다. 1-bromobutane은 S<sub>N</sub>2가 우세하고 E2를 해도 1-butene만 준다. <b class="lbltxt">B</b> = (<i>E</i>)-2-butene(주)이다.</p>
<p>③ [반응 2]: <b class="lbltxt">D</b>(C<sub>4</sub>H<sub>6</sub>)를 Lindlar 촉매로 수소화(syn 첨가 1당량)하여 2-butene을 얻으려면 <b class="lbltxt">D</b> = <b>2-butyne</b>이다(1-butyne → 1-butene → 1-butanol은 비카이랄이고, 1,3-butadiene은 Lindlar로 2-butene을 주지 않는다). <b class="lbltxt">E</b> = <i>cis</i>-2-butene이다.</p>
{BEF_BOX}
<p>④ Ipc<sub>2</sub>BH: (+)-α-pinene에 BH<sub>3</sub>가 gem-다이메틸 다리의 반대쪽 면으로만 syn 첨가하고, B는 덜 치환된 탄소에 붙는다. 두 pinene이 똑같은 방식으로 붙으므로 단일 입체이성질체가 생긴다(논문의 요지). 이 부피 큰 카이랄 보레인은 <i>cis</i>-2-butene과 특히 잘 맞물려, Brown의 실험에서 (<i>R</i>)-2-butanol이 높은 거울상 초과율로 얻어졌다. 산화(H<sub>2</sub>O<sub>2</sub>, NaOH) 단계는 B를 OH로 바꿀 때 배열을 유지하므로(1,2-이동이 배열 유지), 수소화붕소 첨가에서 정해진 입체가 그대로 남는다.</p>
<p>⑤ 오답 주의: “BH<sub>3</sub>의 syn 첨가는 입체특이적이니 C도 한 입체이성질체”라고 쓰면 틀린다. syn 첨가는 두 원자가 <b>같은 면</b>으로 들어온다는 뜻이다. 비카이랄 시약은 두 거울상 면을 구별하지 못하므로 결국 라세미가 된다. 거울상선택성은 카이랄 시약·촉매가 있어야만 생긴다(Brown 1979 노벨상: 유기 붕소 화학).</p>''',
),

# ───────────────────────────── 6. 2017A-13 ─────────────────────────────
dict(
    key='2017A-13',
    src='2017학년도 A형 13번',
    src_topic='1-methylcyclohexene → 브로모하이드린 → 에폭사이드, 산 촉매 메탄올 분해의 위치·입체선택성, 수소화붕소 첨가 생성물의 의자 형태',
    change='라셈 에폭사이드 대신 Sharpless 비대칭 에폭시화로 광학 활성 2,3-에폭시 알코올을 만들고(JOC 2002, 2-C-methyl-D-erythritol 합성 단계), '
           '같은 에폭사이드를 산성(CH<sub>3</sub>OH/H<sup>+</sup>)과 염기성·강한 친핵체(NaN<sub>3</sub>) 조건에서 각각 열어 위치선택성의 역전과 반전(입체)을 절대 배열(R/S)로 함께 묻도록 변형',
    paper=dict(cite='J. Org. Chem. 2002, 67, 4856–4859', book='Klein 14.64',
               what='(E)-4-(benzyloxy)-2-methylbut-2-en-1-ol을 (−)-DET Sharpless 에폭시화로 (2R,3R)-에폭시 알코올로 만들고, 산 촉매로 3차 탄소에서 반전 개환하여 2-C-methyl-D-erythritol을 합성'),
    nobel='2001 노벨 화학상(K. B. Sharpless — 키랄 촉매 산화 반응)',
    body=f'''다음은 알릴 알코올 <b class="lbltxt">S</b>로부터 중간 주생성물 <b class="lbltxt">A</b>(C<sub>12</sub>H<sub>16</sub>O<sub>3</sub>)를 거쳐 최종 주생성물 <b class="lbltxt">B</b>(C<sub>13</sub>H<sub>20</sub>O<sub>4</sub>)와 <b class="lbltxt">C</b>(C<sub>12</sub>H<sub>17</sub>N<sub>3</sub>O<sub>3</sub>)를 각각 합성하는 반응식이다. {DEF}
{frame(scheme(M(SH_SM, 'S', 14)),
       scheme(arrow('<i>t</i>-BuOOH, Ti(O<i>i</i>-Pr)<sub>4</sub>', '(−)-DET, −20 ℃'), L('A'), arrow('CH<sub>3</sub>OH', 'H<sub>2</sub>SO<sub>4</sub>(촉매)'), L('B')),
       scheme(L('A'), arrow('NaN<sub>3</sub>, NH<sub>4</sub>Cl', 'CH<sub>3</sub>OH/H<sub>2</sub>O'), L('C')),
       '<div class="chem">◦ DET = diethyl tartrate. 알릴 알코올을 평면에 놓고 CH<sub>2</sub>OH가 오른쪽 아래에 오도록 그리면, (−)-DET는 위쪽 면에서, (+)-DET는 아래쪽 면에서 산소를 전달한다.</div>')}
<p class="ask"><b class="lbltxt">A</b>의 입체구조를 그리고 <b class="lbltxt">A</b>의 두 카이랄 중심의 <i>R</i>, <i>S</i> 배열을 쓰시오. <b class="lbltxt">B</b>와 <b class="lbltxt">C</b>의 입체구조를 각각 그리고, <b class="lbltxt">B</b>와 <b class="lbltxt">C</b>에서 친핵체가 공격한 탄소의 위치가 서로 다른 이유를 서술하시오. [[PTS]]</p>''',
    answer=f'''<div class="ansbox">{M(SH_A, 'A: (2R,3R)', 14)}</div>
<div class="ansbox">{M(SH_B, 'B: (2S,3R)', 13)}{M(SH_C, 'C: (2S,3S)', 13)}</div>
A: C2 = <i>R</i>, C3 = <i>R</i>. B는 CH<sub>3</sub>OH가 <b>3차 탄소(C2)</b>를, C는 N<sub>3</sub><sup>−</sup>가 <b>2차 탄소(C3)</b>를 공격했고 두 경우 모두 공격받은 탄소는 반전되었다. 산 촉매 조건에서는 양성자화된 에폭사이드의 C–O 결합이 길어지면서 생기는 부분 양전하를 더 잘 안정화하는 3차 탄소가 공격받는다(S<sub>N</sub>1 성격, 전자 효과). 강한 음이온 친핵체(N<sub>3</sub><sup>−</sup>)는 S<sub>N</sub>2로 입체 장애가 작은 2차 탄소를 공격한다(입체 효과).''',
    explain='''<p><b>핵심 반응:</b> Sharpless 비대칭 에폭시화(알릴 알코올의 OH가 Ti에 배위 → 면 선택), 에폭사이드 개환의 위치선택성(산: 더 치환된 C / 강한 친핵체: 덜 치환된 C)과 입체특이성(뒤쪽 공격 → 반전).</p>
<p>① <b class="lbltxt">S</b>는 (<i>E</i>)-삼치환 알릴 알코올이다. Ti(O<i>i</i>-Pr)<sub>4</sub>–타르트레이트 착물에 S의 알콕사이드와 <i>t</i>-BuOO<sup>−</sup>가 함께 배위하고, 산소가 C=C의 한쪽 면으로만 전달된다(협동적, syn). 알켄의 기하가 그대로 유지되어 CH<sub>2</sub>OH와 CH<sub>2</sub>OBn은 <i>trans</i>로 남는다. 주어진 규칙에서 (−)-DET는 위쪽 면에 산소를 전달하므로 <b class="lbltxt">A</b> = (2<i>R</i>,3<i>R</i>)-3-[(benzyloxy)methyl]-2-methyloxiranylmethanol이다. (+)-DET라면 (2<i>S</i>,3<i>S</i>)가 된다(RDKit로 공간 배치를 대응시켜 확인).</p>
<p>② CIP(A): C2 = O(고리) &gt; C3(O,C,H) &gt; CH<sub>2</sub>OH(O,H,H) &gt; CH<sub>3</sub> → <i>R</i>. C3 = O(고리) &gt; C2(O,C,C) &gt; CH<sub>2</sub>OBn(O,H,H) &gt; H → <i>R</i>.</p>
<p>③ <b class="lbltxt">B</b>(산성 메탄올 분해): H<sup>+</sup>가 에폭사이드 O에 붙는다. 이어 C2–O 결합이 먼저 길어지면서 3차 탄소 C2에 부분 양전하가 쌓이는, “느슨한” S<sub>N</sub>2 전이 상태가 된다. CH<sub>3</sub>OH는 이 C2를 <b>뒤쪽에서</b> 공격하므로 C2가 반전되고, C3–O는 OH로 남아 배열이 유지된다 → (2<i>S</i>,3<i>R</i>)-4-(benzyloxy)-2-methoxy-2-methylbutane-1,3-diol. 자유 탄소 양이온이 생기는 S<sub>N</sub>1이었다면 양쪽 면 공격으로 부분입체이성질체 혼합물이 생겼을 것이다. 생성물이 하나라는 사실이 “S<sub>N</sub>1 성격의 S<sub>N</sub>2”임을 보여 준다. 논문에서는 같은 원리로 아세테이트의 C=O 산소가 분자 내에서 C2를 공격(반전)하여 2-C-methyl-D-erythritol의 (2<i>S</i>,3<i>R</i>) 배열을 만들었다.</p>
<p>④ <b class="lbltxt">C</b>(NaN<sub>3</sub>): 양성자화가 일어나지 않는 조건에서는 결합 끊김보다 결합 형성이 앞선다(전형적 S<sub>N</sub>2). 그래서 입체 장애가 작은 2차 탄소 C3가 공격받고 반전된다. C2–O는 3차 알코올로 남는다 → (2<i>S</i>,3<i>S</i>)-3-azido-4-(benzyloxy)-2-methylbutane-1,2-diol. C2의 공간 배치는 유지되었지만 치환기 순위가 바뀌어 기호가 <i>R</i>→<i>S</i>로 달라진 점에 주의하자(“기호가 바뀌면 반전”이라는 오해 금지).</p>
<p>⑤ 정리: 같은 에폭사이드라도 [산 촉매·약한 친핵체] → 전자 효과(더 치환된 C), [강한 친핵체·염기성] → 입체 효과(덜 치환된 C)가 위치를 결정한다. 어느 경우든 공격은 C–O의 반대쪽에서 일어나므로 <b>공격받은 탄소만 반전</b>되고, 결과적으로 두 작용기는 <i>anti</i>(트레오/에리트로 관계로 표현 가능)가 된다.</p>''',
),

# ───────────────────────────── 7. 2016A-13 ─────────────────────────────
dict(
    key='2016A-13',
    src='2016학년도 A형 13번',
    src_topic='일치환 사이클로헥세인의 A값과 [적도]/[축] 비, 옥시수은화 생성물의 의자 형태, L-Selectride의 입체선택성',
    change='치환기를 –OH, –CH(CH<sub>3</sub>)<sub>2</sub>, –C<sub>6</sub>H<sub>5</sub>로 바꾸고, 기질을 t-Bu로 형태가 고정된 4-tert-butylcyclohexanone으로 바꾸어 L-Selectride의 적도 방향 공격을 명확히 함. '
           '옥시수은화 대신 trans-decalin에 접합된 두 γ-락톤의 연소열 비교(JACS 1961)를 넣어, 고리 고정 → 꼬인보트 강제 → 에너지 증가라는 형태 분석을 열화학 자료와 연결',
    paper=dict(cite='J. Am. Chem. Soc. 1961, 83, 606–614', book='Klein 4.74',
               what='trans-decalin에 접합된 부분입체이성질 γ-락톤 두 개의 연소열 차이 17.2 kJ/mol — 락톤 고리 결합이 trans-이축이어야 하는 이성질체는 꼬인보트를 취해 덜 안정'),
    nobel='1969 노벨 화학상(D. H. R. Barton·O. Hassel — 형태 분석)',
    body=f'''다음은 일치환 사이클로헥세인의 두 의자 형태 <b class="lbltxt">P</b>와 <b class="lbltxt">Q</b>의 [평형식], 이와 관련된 [반응]과 [자료]이다.
{frame(scheme(chair({(0, 'ax'): 'R', (0, 'eq'): 'H'}, 'P', w=120, h=80, R=34, hz=10), '<div class="plus">⇌</div>',
              chair({(3, 'eq'): 'R', (3, 'ax'): 'H'}, 'Q', w=120, h=80, R=34, hz=10)),
       '<div class="chem" style="text-align:center">R = –OH, –CH(CH<sub>3</sub>)<sub>2</sub>, –C<sub>6</sub>H<sub>5</sub></div>', title='[평형식]')}
{frame(scheme(M('O=C1CCC(CC1)C(C)(C)C', '', 14), arrow('1) L-Selectride, THF, −78 ℃', '2) H<sub>3</sub>O<sup>+</sup>'), L('C'), '<span class="chem">(C<sub>10</sub>H<sub>20</sub>O)</span>'),
       '<div class="chem" style="text-align:center">L-Selectride = Li<sup>+</sup>[HB(<i>sec</i>-Bu)<sub>3</sub>]<sup>−</sup></div>', title='[반응]')}
{frame(scheme(M(LAC1, '1', 14), M(LAC2, '2', 14)),
       '<div class="chem">◦ <b class="lbltxt">1</b>과 <b class="lbltxt">2</b>는 <i>trans</i>-decalin에 γ-락톤이 <i>trans</i>로 접합된 부분입체이성질체이며, 연소열의 차이는 17.2 kJ/mol이다.</div>', title='[자료]')}
<p class="ask">[평형식]에서 R가 각각 –OH, –CH(CH<sub>3</sub>)<sub>2</sub>, –C<sub>6</sub>H<sub>5</sub>일 때 25 ℃에서 [<b class="lbltxt">Q</b>]/[<b class="lbltxt">P</b>]가 큰 것부터 순서대로 나열하시오. [반응]의 주생성물 <b class="lbltxt">C</b>의 구조를 안정한 의자 형태로 그리고, <b class="lbltxt">C</b>가 주생성물로 생성된 이유를 서술하시오. 또한 [자료]에서 연소열이 더 큰 것을 쓰시오. [[PTS]]</p>''',
    answer=f'''[Q]/[P]: –C<sub>6</sub>H<sub>5</sub> &gt; –CH(CH<sub>3</sub>)<sub>2</sub> &gt; –OH<br>
<div class="ansbox">{chair({(0, 'ax'): 'OH', (0, 'eq'): 'H', (3, 'eq'): 'C(CH3)3', (3, 'ax'): 'H'}, 'C: cis-4-tert-butylcyclohexanol (OH 축)')}</div>
이유: t-Bu가 적도에 고정된 의자 형태에서, 부피가 큰 L-Selectride는 C3·C5의 축 방향 H와 1,3-이축 반발을 일으키는 축 방향 접근을 하지 못한다. 그래서 덜 막힌 <b>적도 방향</b>에서 하이드라이드를 전달하고, 그 결과 O는 축으로 밀려나 열역학적으로 덜 안정한 <i>cis</i>(OH 축) 알코올이 생긴다(입체 접근 조절, 속도론적 생성물).<br>
연소열이 더 큰 것: <b class="lbltxt">2</b>''',
    explain='''<p><b>핵심 개념:</b> A값(ΔG°<sub>축→적도</sub>)과 K = e<sup>ΔG°/RT</sup>, t-Bu에 의한 형태 고정, 하이드라이드 환원의 축/적도 공격(작은 NaBH<sub>4</sub> vs 부피 큰 L-Selectride), 고리 고정과 꼬인보트 변형.</p>
<p>① A값(kJ/mol, 25 ℃): C<sub>6</sub>H<sub>5</sub> ≈ 11.7(2.8 kcal) &gt; CH(CH<sub>3</sub>)<sub>2</sub> ≈ 9.2(2.2 kcal) &gt; OH ≈ 3.8(0.9 kcal, 용매에 따라 2.5–4). K = [Q]/[P] = e<sup>A/RT</sup>로 Ph ≈ 110, iPr ≈ 40, OH ≈ 5이다. iPr은 메타인 H를 고리 쪽으로 돌릴 수 있어 메틸(7.3)보다 A값이 조금 클 뿐이다. 평면인 Ph는 축 방향에서 고리 평면을 어느 쪽으로 돌려도 축 H나 이웃 적도 H와 부딪혀 iPr보다 크다(“iPr이 더 커 보인다”는 오답 유도).</p>
<p>② <b class="lbltxt">C</b>: t-Bu(A ≈ 21 kJ/mol 이상)는 사실상 항상 적도에 있으므로 고리가 뒤집히지 않는다. 카보닐 탄소에 하이드라이드가 접근하는 경로는 두 가지다. (a) <b>축 방향 공격</b>: 비틀림(가림) 변형이 작다. 그러나 C3·C5의 축 H 쪽을 지나가므로 부피 큰 시약에는 막힌다. 작은 NaBH<sub>4</sub>·LiAlH<sub>4</sub>는 이 경로로 공격하여 OH가 적도인 <i>trans</i> 알코올(약 90 %)을 준다. (b) <b>적도 방향 공격</b>: C2·C3 수소와의 비틀림 변형이 있지만 입체적으로 열려 있다. 세 개의 <i>sec</i>-뷰틸을 가진 L-Selectride는 (b)를 택하므로 O<sup>−</sup>가 축 방향으로 밀려난다. 그 결과 <b class="lbltxt">C</b> = <i>cis</i>-4-<i>tert</i>-butylcyclohexan-1-ol(OH 축, t-Bu 적도)이 >95 % 생긴다.</p>
<p>③ 열역학적으로는 <i>trans</i>(OH 적도)가 약 3.8 kJ/mol 더 안정하다. 그러나 −78 ℃의 비가역 환원에서는 전이 상태 에너지 차(속도론)가 생성물을 결정한다. 이것이 기출의 “입체 접근 조절” 서술 포인트다.</p>
<p>④ [자료]: 두 락톤 모두 <i>trans</i>-decalin이라 B 고리가 뒤집힐 수 없다. <b class="lbltxt">1</b>은 락톤 고리의 두 결합(C–CH<sub>2</sub>, C–O)이 B 고리에서 <b>모두 적도</b>(이면각 ≈ 60°)여서 5원 고리가 쉽게 닫히고 B 고리는 의자를 유지한다. <b class="lbltxt">2</b>는 <i>trans</i> 접합이 <b>이축</b>(180°)이 되는 배열이라 5원 고리로 이을 수 없다. 그래서 B 고리가 꼬인보트로 비틀려야 한다. 따라서 <b class="lbltxt">2</b>가 17.2 kJ/mol 덜 안정하고 연소열이 더 크다(MMFF 계산으로도 <b class="lbltxt">2</b>가 약 20 kJ/mol 높음을 확인). 이성질체의 연소열이 클수록 위치 에너지(변형)가 크다는 4장 원리의 실제 측정 예다.</p>''',
),

# ───────────────────────────── 8. 2015A-서술3 ─────────────────────────────
dict(
    key='2015A-서술3',
    src='2015학년도 A형 서술형 3번',
    src_topic='2-butyne의 Lindlar 환원 → cis-2-butene, OsO<sub>4</sub>(syn) → meso, 과산/H<sub>3</sub>O<sup>+</sup>(anti) → 라셈 다이올; 시약 선택과 중간체·이유 서술',
    change='기질을 3-hexyne으로 바꾸고, 알카인 환원 시약 (가)를 [시약]에서 고르게 하여 생성물 B(라셈)·C(메조)의 입체로부터 '
           '“Na/NH<sub>3</sub>(trans) vs Lindlar(cis)”를 역추론하게 함. 결과적으로 syn → 라셈, anti → 메조로 기출과 정반대가 되는 경우를 다룸',
    paper=dict(cite='Angew. Chem. Int. Ed. 1994, 33, 2187–2190', book='Klein 9.85 (+10장 알카인 환원)',
               what='zaragozic acid A 합성(Nicolaou)에서 OsO<sub>4</sub>(촉매)/NMO syn 다이하이드록시화가 알켄의 한쪽 면에서만 일어남 — 이 문항은 그 syn 다이하이드록시화 단계를 단순 알켄으로 모델화'),
    nobel='2001 노벨 화학상(K. B. Sharpless — OsO<sub>4</sub> 비대칭 다이하이드록시화; 해설 ⑥ 참고)',
    body=f'''다음은 [시약] 중 일부를 사용하여 3-hexyne으로부터 <b class="lbltxt">A</b>(C<sub>6</sub>H<sub>12</sub>)를 거쳐 서로 부분입체이성질체 관계인 <b class="lbltxt">B</b>와 <b class="lbltxt">C</b>(C<sub>6</sub>H<sub>14</sub>O<sub>2</sub>)를 합성하는 [반응 과정]을 나타낸 것이다. <b class="lbltxt">B</b>는 라셈 혼합물이며 한 거울상이성질체만 나타내었다. {DEF}
{frame('<div class="chem">H<sub>2</sub>/Lindlar 촉매,　Na/NH<sub>3</sub>(<i>l</i>),　CH<sub>3</sub>CO<sub>3</sub>H,　OsO<sub>4</sub>,　NaHSO<sub>3</sub>/H<sub>2</sub>O,　H<sub>3</sub>O<sup>+</sup>,　O<sub>3</sub></div>', title='[시약]')}
{frame(scheme(M('CCC#CCC', '3-hexyne', 14), arrow('(가)'), L('A')),
       scheme(L('A'), arrow('', ''), M(HEXD_RR, 'B (라셈)', 14)),
       scheme(L('A'), arrow('', ''), M(HEXD_MESO, 'C', 14)), title='[반응 과정]')}
<p class="ask">(가)에 해당하는 시약과 <b class="lbltxt">A</b>의 구조를 쓰시오. [시약]에서 <b class="lbltxt">A</b> → <b class="lbltxt">B</b>와 <b class="lbltxt">A</b> → <b class="lbltxt">C</b> 반응 과정에 적절한 시약을 각각 선택하여 쓰고, 두 과정의 중간체를 입체구조로 그리시오. 또한 <b class="lbltxt">B</b>가 라셈 혼합물로, <b class="lbltxt">C</b>가 메조 화합물로 얻어지는 이유를 각각 서술하시오. [[PTS]]</p>''',
    answer=f'''(가) Na/NH<sub>3</sub>(<i>l</i>) · <b class="lbltxt">A</b> = (<i>E</i>)-3-hexene
<div class="ansbox">{M('CC/C=C/CC', 'A', 14)}</div>
A → B: OsO<sub>4</sub> 후 NaHSO<sub>3</sub>/H<sub>2</sub>O (중간체: 고리형 오스뮴산 에스터) · A → C: CH<sub>3</sub>CO<sub>3</sub>H 후 H<sub>3</sub>O<sup>+</sup> (중간체: <i>trans</i>-2,3-diethyloxirane과 양성자화된 에폭사이드)
<div class="ansbox">{M(OSMATE, '오스뮴산 에스터 (+거울상)', 13)}{M(EPOX_T, 'trans-에폭사이드 (라셈)', 13)}</div>
B: <i>trans</i>-알켄의 두 면 어느 쪽에서든 OsO<sub>4</sub>가 두 O를 같은 면에(syn) 동시에 첨가한다. 위 면 첨가와 아래 면 첨가는 서로 거울상인 (3<i>R</i>,4<i>R</i>)/(3<i>S</i>,4<i>S</i>)를 같은 양으로 주므로 라셈이다.<br>
C: 과산이 <i>trans</i>-에폭사이드(라셈)를 만들고, 산 촉매 조건에서 물이 양성자화된 에폭사이드를 뒤쪽에서 공격하여 한 탄소만 반전된다(순 anti 첨가). <i>trans</i>-알켄의 anti 다이하이드록시화는 어느 쪽 에폭사이드에서 어느 탄소를 공격하든 같은 (3<i>R</i>,4<i>S</i>) 메조 다이올을 준다.''',
    explain='''<p><b>핵심 반응:</b> 알카인의 입체선택적 환원(Na/NH<sub>3</sub> → <i>trans</i>, Lindlar → <i>cis</i>) + syn/anti 다이하이드록시화의 입체특이성 → “같은 대칭 알켄 + 같은 종류 첨가 → 메조, 반대 → 라셈” 규칙.</p>
<p>① 역추론: B(트레오, 라셈)와 C(메조)가 둘 다 같은 A에서 나왔다. 대칭 알켄에서 [<i>cis</i>+syn → 메조, <i>cis</i>+anti → 라셈, <i>trans</i>+syn → 라셈, <i>trans</i>+anti → 메조]이다. syn 시약(OsO<sub>4</sub>)이 라셈 B를 주려면 A는 <b><i>trans</i></b>여야 한다. 따라서 (가) = <b>Na/NH<sub>3</sub>(<i>l</i>)</b>(용해 금속 환원)이다. Lindlar를 고르면 B와 C의 입체가 서로 뒤바뀐다(기출 2015A의 상황).</p>
<p>② Na/NH<sub>3</sub> 메커니즘: Na에서 전자 1개가 알카인 π*로 들어가 라디칼 음이온이 된다 → NH<sub>3</sub>가 양성자를 주어 비닐 라디칼이 된다(두 R가 멀리 떨어진 <i>trans</i> 배치가 더 안정) → 전자 1개를 더 받아 비닐 음이온이 된다 → 다시 양성자화되어 (<i>E</i>)-3-hexene이 된다.</p>
<p>③ A → B: OsO<sub>4</sub>가 [3+2] 고리 첨가로 C=C 한 면에 두 O를 동시에 붙여 5원 고리 오스뮴산 에스터를 만든다(두 C–O가 같은 면, 두 에틸은 <i>trans</i>). NaHSO<sub>3</sub>/H<sub>2</sub>O가 Os–O 결합을 끊어 다이올을 내놓는데, 이때 C–O 결합은 끊어지지 않으므로 배열이 유지된다. 면 선택의 근거가 없으므로 (3<i>R</i>,4<i>R</i>)+(3<i>S</i>,4<i>S</i>)-hexane-3,4-diol 라셈이 된다.</p>
<p>④ A → C: 과산의 협동적 산소 전달(나비형 전이 상태)은 syn이므로 <i>trans</i>-2,3-diethyloxirane(카이랄, 라셈)이 생긴다. H<sub>3</sub>O<sup>+</sup>가 에폭사이드 O를 양성자화하면 물이 C–O의 반대쪽에서 S<sub>N</sub>2형으로 공격하여 그 탄소만 반전된다. 두 거울상 에폭사이드와 두 탄소(동등) 중 어느 조합이든 결과는 (3<i>R</i>,4<i>S</i>)-메조 다이올 하나이다. 메조는 분자 내 대칭면이 있어 광학 비활성이다.</p>
<p>⑤ 흔한 오답: (a) “에폭사이드 개환도 syn” — 산 촉매 개환은 뒤쪽 공격이므로 anti이다. (b) 중간체로 열린 탄소 양이온을 그리면 입체특이성을 설명할 수 없다. (c) O<sub>3</sub>는 C=C를 끊어 propanal을 주므로 오답 시약이다.</p>
<p>⑥ 확장(노벨상): OsO<sub>4</sub>에 카이랄 cinchona 알칼로이드 리간드를 더한 Sharpless 비대칭 다이하이드록시화(AD-mix-α/β)를 쓰면, 같은 (<i>E</i>)-알켄에서 B의 두 거울상이성질체 중 하나를 선택적으로 얻을 수 있다. 논문(zaragozic acid A)에서도 OsO<sub>4</sub>/NMO가 기질의 덜 가려진 면에서만 syn 첨가하여 단일 부분입체이성질체를 주었다.</p>''',
),

# ───────────────────────────── 9. 2015A-기입8 ─────────────────────────────
dict(
    key='2015A-기입8',
    src='2015학년도 A형 기입형 8번 유형',
    src_topic='에테인·뷰테인의 회전 장벽으로부터 가림 상호작용 에너지를 구해 의자–보트 에너지 차(6.8 kcal/mol)를 계산',
    change='저빈도 소재(보트의 깃대 상호작용)를 대신하여 같은 “상호작용 에너지의 가산성” 사고를 (1) 메탄올의 C–O 회전 장벽(J. Phys. Chem. A 2002)으로 '
           '비공유 전자쌍/C–H 가림 에너지를 구하는 문제와, (2) 더 중요한 cis-/trans-decalin의 gauche-뷰테인 상호작용 개수 세기로 재구성',
    paper=dict(cite='J. Phys. Chem. A 2002, 106, 1642–1646', book='Klein 4.70',
               what='메탄올의 C–O 결합 회전 장벽 ≈ 4.2 kJ/mol; 가려진 형태 = H/H 가림 1개 + C–H/비공유 전자쌍 가림 2개'),
    nobel='1969 노벨 화학상(D. H. R. Barton·O. Hassel — 형태 분석; Hassel은 decalin·사이클로헥세인의 형태를 전자 회절로 규명)',
    body=f'''다음은 비틀림 변형과 입체 변형에 관한 자료와 decalin의 두 입체이성질체 <b class="lbltxt">X</b>, <b class="lbltxt">Y</b>를 나타낸 것이다.
{frame('<div class="chem">◦ 에테인의 C–C 회전 에너지 장벽은 12 kJ/mol이다.<br>'
       '◦ 메탄올(CH<sub>3</sub>OH)의 C–O 회전 에너지 장벽은 4.2 kJ/mol이다.<br>'
       '◦ <i>n</i>-뷰테인의 gauche 형태는 anti 형태보다 3.8 kJ/mol 불안정하다.</div>',
       scheme(M(TDEC, 'X', 15), M(CDEC, 'Y', 15)))}
<p class="ask">메탄올의 가려진(eclipsed) 형태에서 C–H 결합과 산소의 비공유 전자쌍 사이의 가림 상호작용 1개의 에너지는 ( ㉠ ) kJ/mol이다. 가장 안정한 의자–의자 형태에서 <b class="lbltxt">Y</b>는 <b class="lbltxt">X</b>보다 gauche-뷰테인 상호작용이 ( ㉡ )개 더 많으며, 입체 효과만 고려한 <b class="lbltxt">X</b>와 <b class="lbltxt">Y</b>의 에너지 차이는 ( ㉢ ) kJ/mol이다. ㉠~㉢에 해당하는 값을 순서대로 쓰시오. [[PTS]]</p>''',
    answer='''㉠ 0.1　㉡ 3　㉢ 11.4 (≈ 11 kJ/mol, Y가 더 불안정)''',
    explain='''<p><b>핵심 개념:</b> 비틀림·입체 상호작용의 가산성, gauche-뷰테인 단위 세기, <i>cis</i>-/<i>trans</i>-decalin의 상대 안정성.</p>
<p>① 에테인의 가려진 형태에는 H/H 가림이 3쌍 있으므로 1쌍 = 12/3 = 4.0 kJ/mol이다.</p>
<p>② 메탄올의 가려진 형태에서 C의 세 C–H는 O의 세 “치환기”(O–H 1개, 비공유 전자쌍 2개)와 각각 가려진다. 따라서 4.2 = 4.0(H/H) + 2x에서 x = <b>0.1 kJ/mol</b>로, 비공유 전자쌍의 가림은 거의 무시할 만하다. 비공유 전자쌍은 전자 밀도가 핵에 가깝게 모여 있어 결합 전자쌍보다 공간을 덜 차지하기 때문이다(논문의 결론). 같은 논리로 메틸아민(가림 H/H 2쌍 + C–H/n 1쌍)의 장벽이 약 8 kJ/mol로 추정된다.</p>
<p>③ <b class="lbltxt">X</b> = <i>trans</i>-decalin(접합 수소가 서로 반대 면), <b class="lbltxt">Y</b> = <i>cis</i>-decalin이다. <b class="lbltxt">X</b>에서는 각 고리가 상대 고리를 1,2-이적도 치환기로 가지므로, 고리 자체에 원래 있는 gauche 외에 추가 gauche가 없다. 고리를 이루는 C4–C4a–C8a–C8 이면각도 180°(anti)이다.</p>
<p>④ <b class="lbltxt">Y</b>에서는 각 접합 탄소에서 한 고리 결합이 다른 고리에 대해 <b>축 방향</b>이다. 그 결과 (i) C8–C8a–C1–C2, (ii) C4–C4a–C5–C6, (iii) C4–C4a–C8a–C8의 세 단위가 gauche-뷰테인 관계가 된다. (iii)은 두 고리 관점에서 각각 한 번씩 세면 중복되므로 한 번만 센다. 따라서 ㉡ = <b>3</b>, ㉢ = 3 × 3.8 = <b>11.4 kJ/mol</b>이다. 실험 연소열 차(≈ 11 kJ/mol, 2.7 kcal/mol)와 잘 맞는다. 이것이 형태 분석이 정량적으로 성공한 고전적 예다.</p>
<p>⑤ 덧붙여 <b class="lbltxt">Y</b>(<i>cis</i>)는 고리 뒤집기가 가능해 두 의자–의자 형태가 빠르게 바뀐다(두 형태는 거울상이므로 광학 비활성). <b class="lbltxt">X</b>(<i>trans</i>)는 고리를 뒤집으면 두 결합이 이축이 되어야 하므로 뒤집을 수 없는 “고정된” 골격이다. 스테로이드의 A/B·B/C·C/D <i>trans</i> 접합이 단단한 이유이며, Barton 형태 분석의 출발점이다.</p>''',
),
]
