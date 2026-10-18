# -*- coding: utf-8 -*-
"""5회분 문항 구성표(출제 가능성·근거) 1면 → PDF"""
import importlib, subprocess, sys, pathlib
sys.path.insert(0, ".")
from mock_render import CHROME
HERE = pathlib.Path(__file__).parent
rows = []
for r in range(1, 6):
    for it in importlib.import_module(f"mock{r}").ITEMS:
        basis = it["note"].split(". ")[0].split("계열")[0]
        rows.append(f"<tr><td>{r}회</td><td>{it['part']}{it['no']}</td><td class='l'>{it['topic']}</td><td class='s'>{it.get('star','')}</td><td class='l b'>{basis}</td></tr>")
doc = f"""<!doctype html><html lang='ko'><head><meta charset='utf-8'><title>출제 예상 구성표</title><style>
@page{{size:297mm 420mm;margin:0}} body{{margin:0;font-family:'NanumGothic',sans-serif;font-size:9.2pt;line-height:1.42}}
.p{{padding:16mm 15mm}} h1{{font-size:16pt;margin:0 0 2mm}} .sub{{color:#444;margin:0 0 4mm}}
table{{border-collapse:collapse;width:100%}} td,th{{border:.6pt solid #999;padding:.9mm 2mm;text-align:center;vertical-align:top}}
th{{background:#eef2f7}} .l{{text-align:left}} .s{{color:#b8860b;white-space:nowrap}} .b{{font-size:8.3pt;color:#333}}
.box{{border:1pt solid #c9b46b;background:#fafaf3;padding:3mm 4mm;margin:0 0 4mm}} .box p{{margin:.8mm 0}}
</style></head><body><div class='p'>
<h1>화학교육론 실전 모의고사 1~5회 — 2027 출제 예상 구성표</h1>
<p class='sub'>근거: 화학교육론 기출 2014~2026, 물리·생물·지구과학 교육론 2024~2026 분석</p>
<div class='box'>
<p><b>선정 원칙</b></p>
<p>① 매년 출제되는 영역(★★★★★)을 회마다 고정 배치: A5 실험 과정 오류·오차·계산, A7 2022 개정 성취기준 해설 ‘다루지 않는 범위’, 평가(채점 기준표·준거·신뢰도), 내용 체계 빈칸, 과학철학·과학적 추론</p>
<p>② 2026 타 과목에서 출제되었으나 화학에서는 최근 출제되지 않은 주제를 우선 반영: 로슨 3유형 구분, 라카토슈, 포퍼 반증 가능성, 유추, 분석적 채점표·피드백, 조작적 정의, 프로젝트 학습, 오수벨 상위적 학습·선행 조직자</p>
<p>③ 2026 화학 기출과 소재·발문이 같은 문항(식초 중화 적정, 포스너 유용성, 질량수·동위 원소)은 교체하고, 같은 계열의 다른 이론·소재로 대비</p>
<p>④ 4점 문항은 작성 방법 2~3개, 채점 요소 약 4개(요소당 1점)로 기출 분량에 맞춤. 교육과정 문장은 원문 그대로 인용</p>
</div>
<table><tr><th style='width:6%'>회</th><th style='width:6%'>문항</th><th style='width:34%'>주제</th><th style='width:11%'>출제 가능성</th><th>출제 근거(기출 연계)</th></tr>{''.join(rows)}</table>
</div></body></html>"""
h = HERE / "출제예상_구성표.html"; h.write_text(doc, encoding="utf-8")
subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={HERE/'출제예상_구성표.pdf'}", f"file://{h}"], capture_output=True)
