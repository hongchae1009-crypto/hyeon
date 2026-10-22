"""안병천 1~3회 상세해설에서 2027 출제 가능성이 높은 문항만 골라 한 권으로 묶는다.

각 회차 md에서 문항 절(## … {#id})을 그대로 가져와 id·제목·이미지 경로만 바꾼다.
(이미지는 img/r{회차}_원래이름 으로 복사해 둔다.)
"""
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
HOME = os.path.dirname(ROOT)
OUT = os.path.join(ROOT, '안병천_엄선문제_1-3회.md')

# (영역 묶음, [(회차, 문항 id, 고른 이유)])
PICKS = [
    ('유기화학', [
        (1, 'a3', '분광(IR·NMR) 구조 결정 + 가수분해 — 매년 나오는 유형'),
        (2, 'a3', 'IR·MS·NMR 종합 구조 결정'),
        (3, 'a3', '¹H·¹³C NMR까지 쓰는 구조 결정, 최근 기출과 형식이 가장 비슷'),
        (1, 'a2', '고리 SN2 반전 + 토실화(입체 유지)를 거꾸로 추적하는 입체화학 대표 유형'),
        (2, 'a8', '수소붕소화의 syn 첨가 + 고리 E2(anti-periplanar) 입체 선택성'),
        (2, 'b9', '데칼린 고리의 E2·수소붕소화 — 의자형 입체 특이성 고난도'),
        (1, 'b8', 'NBS → E2 → Diels–Alder(endo) → 오존 분해로 구조를 추적하는 다단계 서술형'),
        (3, 'b9', '보호기·지향성·다이아조늄을 엮는 방향족 다단계 합성'),
    ]),
    ('무기화학', [
        (2, 'a9', '진동 모드 기약표현과 IR/Raman 활성 — 군론 고정 출제'),
        (1, 'a1', 'Td 사면체 음이온의 IR·Raman 띠 수 — 군론 기본형'),
        (3, 'b6', '카보닐 IR 띠 수로 fac/mer 판별 + 치환 반응 기구'),
        (2, 'b6', 'Ni²⁺ Tanabe–Sugano 해석(Δo, B, 혼합 x) — 결정장 대표 문항'),
        (1, 'b6', 'd³ 세 스핀 허용 띠 배정과 배치 혼합 — 결정장 분광'),
        (3, 'a11', 'π 주개 MO 도표 + 분광화학 계열 + d³ 전이 에너지'),
        (1, 'b2', 'Monsanto 촉매 순환의 기본 단계·전자 수 — 유기금속 단골'),
    ]),
    ('분석화학', [
        (2, 'b1', '다양성자산 혼합물 적정과 지시약 — 분석 최빈출'),
        (3, 'a9', 'EDTA 치환 적정·조건 형성 상수·분율'),
        (1, 'a12', '산화–환원 적정 당량점 전위 유도(활동도 포함)'),
        (2, 'b11', '전지 전위 ↔ Ksp 연결 계산'),
        (1, 'b11', 'pH로 조절하는 황화물 선택적 침전'),
        (1, 'a9', 'van Deemter 극소 조건과 분리도 — 크로마토그래피 계산'),
    ]),
    ('물리화학', [
        (1, 'b7', '사전평형 근사와 겉보기 활성화 에너지 — 2024 기출 계열'),
        (2, 'b7', '라디칼 연쇄 반응의 정류 상태 근사 속도식'),
        (3, 'a10', '내부 압력·α·κT 편미분 관계식 — 서술형 단골'),
        (1, 'a4', '이상 기체 등온·등압 가역 과정의 q·w·ΔU·ΔS'),
        (2, 'a4', '진동-회전 스펙트럼과 결합 차이법'),
        (3, 'b11', '수소 원자 3p 파동함수의 마디·정규화·각운동량'),
    ]),
]


def section(n, qid):
    src = open(os.path.join(HOME, f'안병천_모의고사{n}회_해설', f'안병천_모의고사{n}회_상세해설.md'), encoding='utf-8').read()
    m = re.search(r'^## (.+?) \{#%s\}\s*$' % qid, src, re.M)
    rest = src[m.end():]
    end = re.search(r'^(## |# |---\s*$)', rest, re.M)
    body = rest[:end.start()] if end else rest
    title = m.group(1)
    # 단 높이로 나눈 원문 조각(_2, _3)은 build.py가 자동으로 붙이므로 본문 참조는 지운다
    body = re.sub(r'<img class="q" src="img/[^"]+_\d+\.png"[^>]*>\s*', '', body)
    body = re.sub(r'src="img/([^"]+)"', lambda k: f'src="img/r{n}_{k.group(1)}"', body)
    body = body.replace('검토 메모', f'{n}회 해설지의 검토 메모')
    return title, body.strip()


def stars(n, qid):
    src = open(os.path.join(HOME, f'안병천_모의고사{n}회_해설', f'안병천_모의고사{n}회_상세해설.md'), encoding='utf-8').read()
    i = src.index('{#%s}' % qid)
    s = re.compile(r'<span class="stars">([★☆]+)</span>').search(src, i)
    return s.group(1)


def main():
    rows, parts = [], []
    k = 0
    for area, items in PICKS:
        if not parts:
            parts.append('# 전공 A')
        for n, qid, why in items:
            k += 1
            title, body = section(n, qid)
            label = f'{n}회 {qid[0].upper()}형 {qid[1:]}번'
            new_id = f'r{n}{qid}'
            topic = title.split('·', 1)[1].strip() if '·' in title else title
            rows.append(f'| [{k}](#{new_id}) | {label} | {area} · {topic} | {stars(n, qid)} |')
            parts.append(f'## {k}. {label} · {topic} {{#{new_id}}}\n\n<div class="note" markdown="1">\n\n**엄선 이유** — {why}\n\n</div>\n\n{body}')
    cover = f"""# 안병천 1~3회 전공 엄선 문항 — 2027 출제 가능성 높은 문제

안병천 전공화학 모의고사 1·2·3회에서 **교육론을 빼고 전공(유기·무기·분석·물리) 문항만** 골라 영역별로 묶었습니다. 전공 51문항 중 ★5 문항은 모두 넣고, ★4 가운데 기출 유형과 가장 가깝고 풀이 가치가 큰 문항을 더했습니다. 총 **{k}문항**(유기 8, 무기 7, 분석 6, 물리 6)입니다.

**고른 기준**: ① 1997~2026 기출에서 거의 매년 나오는 유형인가, ② 영역별 핵심 단원(분광 구조 결정, 입체화학, 군론, 결정장, 적정·평형, 속도론·열역학 관계식)을 빠짐없이 덮는가, ③ 한 문항 안에 여러 개념을 묶어 실전 서술형 형식에 가까운가, ④ 풀이 과정·메커니즘이 공부할 가치가 있을 만큼 좋은가. 계산만 반복하는 2점 문항(헤스 법칙, 단순 pH 등)과 출제 빈도가 낮은 소재(고리 위 입자, 라만 회전 분광, 다이에논–페놀 자리옮김 등)는 뺐습니다.

각 문항의 원문·정답·공식 박스·단계별 풀이·메커니즘은 원래 회차 해설지와 같습니다. 본문의 "검토 메모"는 해당 회차 해설지 1쪽의 메모를 가리킵니다.

## 엄선 문항 목록 {{#toc}}

### 전공 A 엄선 목록 (유기·무기)

| 번호 | 출처 | 영역 · 주제 | 출제 가능성 |
|---|---|---|---|
{chr(10).join(rows[:15])}

### 전공 B 엄선 목록 (분석·물리)

| 번호 | 출처 | 영역 · 주제 | 출제 가능성 |
|---|---|---|---|
{chr(10).join(rows[15:])}

<p class="foot">원문: 2027학년도 대비 안병천 전공화학통합모의고사 제1·2·3회(임용닷컴) 문제지·답지·강의 필기. 개인 학습용 정리입니다.</p>

"""
    open(OUT, 'w', encoding='utf-8').write(cover + '\n\n'.join(parts) + '\n\n---\n\n<p class="foot"></p>\n')
    print(k, 'questions')


if __name__ == '__main__':
    main()
