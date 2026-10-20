# 해설 2쪽 구성(교과서 탐구 캡처 전용 쪽 + 모범 답안·해설 쪽) — build_v3 기반 빌더 공용
import re
CAP_JS = """<script>
window.addEventListener("load",function(){const mm=96/25.4, lim=248*mm;
document.querySelectorAll('.capp').forEach(pg=>{const c=pg.querySelector('.caps'); if(!c) return; const ims=[...c.querySelectorAll('img')]; const n=ims.length;
 const tall=ims.every(im=>im.naturalHeight>im.naturalWidth*0.9); let h;
 if(n==1){h=228;} else if(n==2&&tall){c.style.flexDirection='row';c.style.alignItems='flex-start';c.querySelectorAll('figure').forEach(f=>f.style.flex='1');h=228;}
 else if(n==2){c.style.flexDirection='column';h=110;} else {h=n<=4?108:72;}
 ims.forEach(im=>{im.style.maxHeight=h+'mm';im.style.maxWidth='100%';});
 while(pg.scrollHeight>lim && h>30){h-=2; ims.forEach(im=>im.style.maxHeight=h+'mm');}});});
</script>"""
GRID_CSS = ("<style>.caps:has(figure:nth-child(3)){display:grid!important;grid-template-columns:1fr 1fr;gap:4px 8px;align-items:start}"
            ".caps:has(figure:nth-child(3)) img{max-width:100%}</style>")

def install(B):
    def _cover():
        rows, N = [], len(B.Q)
        for i, it in enumerate(B.Q, 1):
            theme = re.sub(r"\s*변형$", "", it["src"])
            a = N + 2 + 2 * (i - 1)
            rows.append(f"<tr><td>{i}</td><td>{B.esc(B.unit_of(it['tb']))}</td><td>{B.esc(theme)}</td><td class='star'>{B.stars(it['star'])}</td><td>{i+1}</td><td>{a}–{a+1}</td></tr>")
        return f"""<section class='pg cover'><h1>{B.COVER_TITLE.format(N=N)}</h1>
<div class='sub'>{B.COVER_SUB.format(CUR=B.CUR)}</div>
<div class='legend'>{B.COVER_LEGEND}{GRID_CSS}
◦ 별점은 2024–2026 물화생지 과교론 출제 경향 기준 중요도·출제 가능성입니다. ◦ 모든 문항은 4점 서술형이며, 한 문항이 한 쪽입니다.<br>
◦ 모범 답안 및 해설({N+2}–{3*N+1}쪽)은 문항별 2쪽으로, 첫 쪽에 관련 교과서 탐구 캡처(비상교육·미래엔)를 크게 싣고, 둘째 쪽에 모범 답안 · 해설(핵심 이론, 교육과정 근거, 채점 포인트, 두 교과서 비교, 출제 포인트)을 실었습니다.</div>
<table class='idx'><tr><th>번호</th><th>교과서·단원</th><th>원 기출 / 핵심 이론</th><th>별점</th><th>문제 쪽</th><th>해설 쪽</th></tr>{''.join(rows)}</table></section>"""
    B.cover = _cover

def split_answer_pages(html_path):
    html = html_path.read_text(encoding="utf-8")
    def rep(m):
        sec = m.group(0)
        meta = re.search(r"<div class='meta'>.*?</div>\n", sec, re.S).group(0)
        i_ans = sec.index("<div class='h3'>■ 모범 답안</div>")
        top = sec[:i_ans].replace("<section class='pg ansp'>", "<section class='pg ansp capp'>", 1) + "</section>"
        bottom = "<section class='pg ansp'>" + meta.replace("모범 답안 및 해설", "모범 답안 및 해설 (계속)") + sec[i_ans:]
        return top + bottom
    html = re.sub(r"<section class='pg ansp'>.*?</section>", rep, html, flags=re.S)
    html = html.replace("</body></html>", CAP_JS + "</body></html>")
    html_path.write_text(html, encoding="utf-8")
