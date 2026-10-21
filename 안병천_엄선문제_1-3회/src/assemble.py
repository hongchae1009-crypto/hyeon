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
        (2, 'a8', '수소붕소화의 syn 첨가 + 고리 E2(anti-periplanar) 입체 선택성'),
        (3, 'b9', '보호기·지향성·다이아조늄을 엮는 방향족 다단계 합성'),
    ]),
    ('무기화학', [
        (2, 'a9', '진동 모드 기약표현과 IR/Raman 활성 — 군론 고정 출제'),
        (2, 'b6', 'Ni²⁺ Tanabe–Sugano 해석(Δo, B, 혼합 x) — 결정장 대표 문항'),
    ]),
    ('분석화학', [
        (2, 'b1', '다양성자산 혼합물 적정과 지시약 — 분석 최빈출'),
        (2, 'b11', '전지 전위 ↔ Ksp 연결 계산'),
    ]),
    ('물리화학', [
        (1, 'b7', '사전평형 근사와 겉보기 활성화 에너지 — 2024 기출 계열 (★4 중 선별)'),
        (3, 'a10', '내부 압력·α·κT 편미분 관계식 — 서술형 단골 (★4 중 선별)'),
    ]),
    ('화학교육론', [
        (1, 'a5', '2022 개정 「교육과정 설계의 개요」 — 적용 첫해 핵심'),
        (1, 'b4', 'STS 수업모형 + 통합과학 2 내용 체계'),
        (1, 'b5', '2022 개정 [화학] 성취기준 해설 + 포스너·로슨'),
        (2, 'a5', '라카토스 연구 프로그램 + 개념 변화'),
        (2, 'a6', '헤론 탐구 수준 + 통합과학 성취기준 적용 범위'),
        (2, 'a7', '2022 개정 과정·기능 용어 + 동료평가'),
        (2, 'b3', '귀추·비유 수업(TWA)·오수벨 조합'),
        (2, 'b5', '로슨 순환학습 3유형 구별과 재구성'),
        (3, 'a5', '2022 개정 [화학] 「화학의 언어」 + 피아제·오수벨'),
        (3, 'a6', '로슨 순환학습 연속 적용 + 통합과학 2 산화·환원'),
        (3, 'b3', '드라이버 개념 변화 모형 + 질량 보존'),
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
    cover = f"""# 안병천 1~3회 엄선 문항 — 2027 출제 가능성 높은 문제

안병천 전공화학 모의고사 1·2·3회(69문항)에서 **2027학년도 중등 화학 임용에 나올 가능성이 매우 높은(★★★★★) 문항**을 골라 영역별로 묶었습니다. 물리화학은 ★5 문항이 없어, ★4 가운데 기출 유형과 가장 가까운 2문항을 넣었습니다. 총 **{k}문항**입니다.

**고른 기준**: ① 1997~2026 기출에서 거의 매년 나오는 유형인가, ② 2022 개정 교육과정 첫 적용 시기에 맞는 소재인가(교육론), ③ 한 문항 안에 여러 개념을 묶어 실전 서술형 형식에 가까운가, ④ 풀이 과정·메커니즘이 공부할 가치가 있을 만큼 좋은가. 계산만 반복하는 2점 문항이나 출제 빈도가 낮은 소재(고리 위 입자, 라만 회전 분광, 자리옮김 반응 등)는 뺐습니다.

각 문항의 원문·정답·공식 박스·단계별 풀이·메커니즘은 원래 회차 해설지와 같습니다. 본문의 "검토 메모"는 해당 회차 해설지 1쪽의 메모를 가리킵니다.

## 엄선 문항 목록 {{#toc}}

### 전공 A 엄선 목록

| 번호 | 출처 | 영역 · 주제 | 출제 가능성 |
|---|---|---|---|
{chr(10).join(rows[:11])}

### 전공 B 엄선 목록 (화학교육론)

| 번호 | 출처 | 영역 · 주제 | 출제 가능성 |
|---|---|---|---|
{chr(10).join(rows[11:])}

<p class="foot">원문: 2027학년도 대비 안병천 전공화학통합모의고사 제1·2·3회(임용닷컴) 문제지·답지·강의 필기. 개인 학습용 정리입니다.</p>

"""
    open(OUT, 'w', encoding='utf-8').write(cover + '\n\n'.join(parts) + '\n\n---\n\n<p class="foot"></p>\n')
    print(k, 'questions')


if __name__ == '__main__':
    main()
